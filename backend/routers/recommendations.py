from fastapi import APIRouter, HTTPException
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_conn
from models import RecommendationResponse

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


# ─────────────────────────────────────────────────────────────────────────────
# HELPER — GET BOOKS USER HAS ALREADY READ OR SHELVED
#
# We never recommend a book the user already knows about.
# This function returns a set of book IDs to exclude.
# ─────────────────────────────────────────────────────────────────────────────
def get_user_book_ids(user_id: int) -> set:
    conn = get_conn()
    rows = conn.execute(
        "SELECT book_id FROM user_books WHERE user_id = ?", (user_id,)
    ).fetchall()
    conn.close()
    return {row["book_id"] for row in rows}


# ─────────────────────────────────────────────────────────────────────────────
# HELPER — CONTENT BASED FILTERING
#
# "You liked Mystery books → recommend more Mystery books"
#
# How it works:
# 1. Find genres the user has rated highly (4+ stars)
# 2. Find authors the user has rated highly
# 3. Find books matching those genres/authors
# 4. Exclude books already on their shelf
# 5. Return top 5 with reason
#
# This is the FALLBACK when a user has fewer than 2 ratings.
# ─────────────────────────────────────────────────────────────────────────────
def content_based(user_id: int, exclude_ids: set) -> list:
    conn = get_conn()

    # Find genres the user rated 4 or 5 stars
    # We GROUP BY genre and take the average rating
    # to find their most loved genres
    liked_genres = conn.execute("""
        SELECT b.genre, ROUND(AVG(ub.rating), 1) as avg_rating
        FROM user_books ub
        JOIN books b ON ub.book_id = b.id
        WHERE ub.user_id = ?
          AND ub.rating >= 4
        GROUP BY b.genre
        ORDER BY avg_rating DESC
        LIMIT 3
    """, (user_id,)).fetchall()

    # Find authors the user rated 4 or 5 stars
    liked_authors = conn.execute("""
        SELECT a.id, a.name, ROUND(AVG(ub.rating), 1) as avg_rating
        FROM user_books ub
        JOIN books b    ON ub.book_id   = b.id
        JOIN authors a  ON b.author_id  = a.id
        WHERE ub.user_id = ?
          AND ub.rating >= 4
        GROUP BY a.id
        ORDER BY avg_rating DESC
        LIMIT 3
    """, (user_id,)).fetchall()

    recommendations = []

    # Recommend by favourite genres first
    for genre_row in liked_genres:
        genre = genre_row["genre"]
        books = conn.execute("""
            SELECT b.*, a.name as author_name
            FROM books b
            JOIN authors a ON b.author_id = a.id
            WHERE b.genre = ?
            ORDER BY b.publish_year DESC
        """, (genre,)).fetchall()

        for book in books:
            if book["id"] not in exclude_ids:
                recommendations.append({
                    "book_id":     book["id"],
                    "title":       book["title"],
                    "author_name": book["author_name"],
                    "genre":       book["genre"],
                    "cover_url":   book["cover_url"],
                    "description": book["description"],
                    "reason":      f"Because you love {genre} books",
                    "method":      "content"
                })
                exclude_ids.add(book["id"])  # don't recommend same book twice

    # Recommend by favourite authors
    for author_row in liked_authors:
        books = conn.execute("""
            SELECT b.*, a.name as author_name
            FROM books b
            JOIN authors a ON b.author_id = a.id
            WHERE a.id = ?
            ORDER BY b.publish_year DESC
        """, (author_row["id"],)).fetchall()

        for book in books:
            if book["id"] not in exclude_ids:
                recommendations.append({
                    "book_id":     book["id"],
                    "title":       book["title"],
                    "author_name": book["author_name"],
                    "genre":       book["genre"],
                    "cover_url":   book["cover_url"],
                    "description": book["description"],
                    "reason":      f"Because you loved {author_row['name']}'s work",
                    "method":      "content"
                })
                exclude_ids.add(book["id"])

    conn.close()
    return recommendations[:5]


# ─────────────────────────────────────────────────────────────────────────────
# HELPER — COLLABORATIVE FILTERING
#
# "Users who liked the same books as you also loved these"
#
# How it works:
# 1. Get all books this user has rated
# 2. Find OTHER users who rated the SAME books similarly
# 3. Those are "similar users"
# 4. Find books similar users loved that THIS user hasn't read
# 5. Return top 5 with reason
#
# This uses a simple similarity score:
#   score = number of books both users rated similarly (within 1 star)
# ─────────────────────────────────────────────────────────────────────────────
def collaborative_filtering(user_id: int, exclude_ids: set) -> list:
    conn = get_conn()

    # Get this user's ratings
    # { book_id: rating } dictionary
    my_ratings = {}
    rows = conn.execute("""
        SELECT book_id, rating FROM user_books
        WHERE user_id = ? AND rating > 0
    """, (user_id,)).fetchall()
    for row in rows:
        my_ratings[row["book_id"]] = row["rating"]

    if not my_ratings:
        conn.close()
        return []

    # Find all other users who rated at least one of the same books
    other_users = conn.execute("""
        SELECT DISTINCT user_id FROM user_books
        WHERE book_id IN ({})
          AND user_id != ?
          AND rating > 0
    """.format(",".join("?" * len(my_ratings))),
        list(my_ratings.keys()) + [user_id]
    ).fetchall()

    # Calculate similarity score for each other user
    # Score = number of books where ratings are within 1 star of each other
    # e.g. I rated Sherlock 5, they rated it 4 → similar (difference = 1)
    # e.g. I rated Dracula 5, they rated it 2 → not similar (difference = 3)
    similarity_scores = {}
    for other in other_users:
        other_id = other["user_id"]
        other_ratings = {}
        other_rows = conn.execute("""
            SELECT book_id, rating FROM user_books
            WHERE user_id = ? AND rating > 0
        """, (other_id,)).fetchall()
        for row in other_rows:
            other_ratings[row["book_id"]] = row["rating"]

        # Count how many books we both rated similarly
        score = 0
        for book_id, my_rating in my_ratings.items():
            if book_id in other_ratings:
                difference = abs(my_rating - other_ratings[book_id])
                if difference <= 1:
                    score += 1

        if score > 0:
            similarity_scores[other_id] = score

    if not similarity_scores:
        conn.close()
        return []

    # Sort users by similarity score — most similar first
    similar_users = sorted(
        similarity_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]  # top 3 most similar users

    # Find books similar users loved (rated 4+) that we haven't read
    recommendations = []
    for similar_user_id, score in similar_users:

        # Get their display name for the reason message
        user_row = conn.execute(
            "SELECT display_name FROM users WHERE id = ?",
            (similar_user_id,)
        ).fetchone()
        similar_user_name = user_row["display_name"] if user_row else "A reader like you"

        # Get books they rated 4+ that we haven't read
        loved_books = conn.execute("""
            SELECT b.*, a.name as author_name, ub.rating
            FROM user_books ub
            JOIN books b   ON ub.book_id  = b.id
            JOIN authors a ON b.author_id = a.id
            WHERE ub.user_id = ?
              AND ub.rating >= 4
            ORDER BY ub.rating DESC
        """, (similar_user_id,)).fetchall()

        for book in loved_books:
            if book["id"] not in exclude_ids:
                recommendations.append({
                    "book_id":     book["id"],
                    "title":       book["title"],
                    "author_name": book["author_name"],
                    "genre":       book["genre"],
                    "cover_url":   book["cover_url"],
                    "description": book["description"],
                    "reason":      f"Readers like you loved this ({score} books in common)",
                    "method":      "collaborative"
                })
                exclude_ids.add(book["id"])

    conn.close()
    return recommendations[:5]


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENDPOINT — HYBRID RECOMMENDATIONS
# GET /recommendations/{user_id}
#
# This is the hybrid engine:
# - If user has 2+ ratings → try collaborative filtering first
# - If collaborative returns < 5 results → fill remaining with content-based
# - If user has < 2 ratings → use content-based only
#
# Always returns up to 5 recommendations with a reason for each.
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/{user_id}", response_model=list[RecommendationResponse])
def get_recommendations(user_id: int):
    conn = get_conn()

    # Check user exists
    user = conn.execute(
        "SELECT id FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    # Count how many books this user has rated
    rated_count = conn.execute("""
        SELECT COUNT(*) as cnt FROM user_books
        WHERE user_id = ? AND rating > 0
    """, (user_id,)).fetchone()["cnt"]
    conn.close()

    # Books to exclude — already on their shelf
    exclude_ids = get_user_book_ids(user_id)

    recommendations = []

    if rated_count >= 2:
        # ── Collaborative filtering first ─────────────────────────────────
        recommendations = collaborative_filtering(user_id, exclude_ids.copy())

        # ── Fill remaining spots with content-based ───────────────────────
        if len(recommendations) < 5:
            content_recs = content_based(user_id, exclude_ids.copy())
            # Add content recs until we have 5 total
            for rec in content_recs:
                if len(recommendations) >= 5:
                    break
                # Make sure we don't add duplicates
                existing_ids = {r["book_id"] for r in recommendations}
                if rec["book_id"] not in existing_ids:
                    recommendations.append(rec)
    else:
        # ── Content-based only for new users ─────────────────────────────
        recommendations = content_based(user_id, exclude_ids.copy())

    # If still no recommendations — user has read everything!
    if not recommendations:
        raise HTTPException(
            status_code=404,
            detail="No new recommendations — you've read everything!"
        )

    return recommendations[:5]


# ─────────────────────────────────────────────────────────────────────────────
# ENDPOINT — CONTENT BASED ONLY
# GET /recommendations/{user_id}/content
#
# Forces content-based recommendations regardless of rating count.
# Useful for testing and for the "More like this genre" feature.
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/{user_id}/content", response_model=list[RecommendationResponse])
def get_content_recommendations(user_id: int):
    exclude_ids = get_user_book_ids(user_id)
    recommendations = content_based(user_id, exclude_ids.copy())
    if not recommendations:
        raise HTTPException(
            status_code=404,
            detail="No recommendations found"
        )
    return recommendations


# ─────────────────────────────────────────────────────────────────────────────
# ENDPOINT — COLLABORATIVE ONLY
# GET /recommendations/{user_id}/collaborative
#
# Forces collaborative filtering regardless of rating count.
# Useful for testing.
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/{user_id}/collaborative", response_model=list[RecommendationResponse])
def get_collaborative_recommendations(user_id: int):
    exclude_ids = get_user_book_ids(user_id)
    recommendations = collaborative_filtering(user_id, exclude_ids.copy())
    if not recommendations:
        raise HTTPException(
            status_code=404,
            detail="Not enough data for collaborative filtering yet"
        )
    return recommendations

