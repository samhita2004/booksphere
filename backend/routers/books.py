from fastapi import APIRouter, HTTPException, Query
from database import get_conn
from models import BookCreate, BookResponse, MessageResponse
import requests

router = APIRouter()


# ─────────────────────────────────────────────────────────────────────────────
# GET ALL BOOKS
# GET /books
#
# Returns all books with their author name joined in.
# Optional genre filter — GET /books?genre=Mystery
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/", response_model=list[BookResponse])
def get_all_books(genre: str = None):
    conn = get_conn()

    # We JOIN authors table so we get author_name in one query
    # instead of making a separate call for each book
    if genre:
        rows = conn.execute("""
            SELECT b.*, a.name as author_name
            FROM books b
            JOIN authors a ON b.author_id = a.id
            WHERE LOWER(b.genre) = LOWER(?)
            ORDER BY b.title
        """, (genre,)).fetchall()
    else:
        rows = conn.execute("""
            SELECT b.*, a.name as author_name
            FROM books b
            JOIN authors a ON b.author_id = a.id
            ORDER BY b.title
        """).fetchall()

    conn.close()
    return [dict(row) for row in rows]


# ─────────────────────────────────────────────────────────────────────────────
# GET ONE BOOK
# GET /books/{book_id}
#
# Returns a single book with full details.
# Used by the reader page and book detail view.
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    conn = get_conn()
    row = conn.execute("""
        SELECT b.*, a.name as author_name
        FROM books b
        JOIN authors a ON b.author_id = a.id
        WHERE b.id = ?
    """, (book_id,)).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Book not found")

    return dict(row)


# ─────────────────────────────────────────────────────────────────────────────
# SEARCH BOOKS
# GET /books/search/local?q=sherlock
#
# Searches our local database by title, author or genre.
# This is different from the Gutenberg search below —
# this only searches books already in our database.
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/search/local", response_model=list[BookResponse])
def search_local(q: str = Query(..., description="Search by title, author or genre")):
    conn = get_conn()
    # % is a wildcard in SQL LIKE — matches anything before or after
    # e.g. searching "sher" matches "Sherlock Holmes"
    pattern = f"%{q}%"
    rows = conn.execute("""
        SELECT b.*, a.name as author_name
        FROM books b
        JOIN authors a ON b.author_id = a.id
        WHERE b.title      LIKE ? 
           OR a.name       LIKE ?
           OR b.genre      LIKE ?
           OR b.description LIKE ?
        ORDER BY b.title
    """, (pattern, pattern, pattern, pattern)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ─────────────────────────────────────────────────────────────────────────────
# SEARCH GUTENBERG
# GET /books/search/gutenberg?q=dracula
#
# Searches Project Gutenberg live via the Gutendex API.
# Returns books not yet in our database that can be added.
# Gutendex is a free API wrapper around Project Gutenberg —
# no API key needed.
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/search/gutenberg")
def search_gutenberg(q: str = Query(..., description="Search Gutenberg catalogue")):
    try:
        resp = requests.get(
            f"https://gutendex.com/books/?search={q}&languages=en",
            timeout=8
        )
        data = resp.json()
        results = []

        for b in data.get("results", [])[:8]:
            # Gutenberg stores authors as a list — join them
            authors  = ", ".join([a["name"] for a in b.get("authors", [])])
            cover    = b.get("formats", {}).get("image/jpeg", "")
            subjects = b.get("subjects", [])
            genre    = subjects[0].split("--")[0].strip() if subjects else "Classic"

            results.append({
                "gutenberg_id": b["id"],
                "title":        b["title"],
                "author":       authors or "Unknown",
                "genre":        genre[:40],
                "cover_url":    cover,
            })

        return results

    except Exception as e:
        raise HTTPException(status_code=503, detail="Gutenberg search unavailable")


# ─────────────────────────────────────────────────────────────────────────────
# READ BOOK TEXT
# GET /books/{book_id}/read?page=1
#
# This is the core of the in-app reader.
# Fetches full book text from Project Gutenberg,
# cleans the header/footer, and returns one page at a time.
#
# page_size=2500 means each page is ~2500 characters
# which is roughly one screen of comfortable reading.
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/{book_id}/read")
def read_book(book_id: int, page: int = 1, page_size: int = 2500):
    conn = get_conn()
    book = conn.execute(
        "SELECT * FROM books WHERE id = ?", (book_id,)
    ).fetchone()
    conn.close()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    gid = book["gutenberg_id"]
    if not gid:
        raise HTTPException(status_code=400, detail="No Gutenberg source for this book")

    # Try multiple URL formats — Gutenberg has inconsistent file locations
    urls = [
        f"https://www.gutenberg.org/files/{gid}/{gid}-0.txt",
        f"https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt",
    ]

    text = None
    for url in urls:
        try:
            resp = requests.get(url, timeout=12)
            if resp.status_code == 200:
                text = resp.text
                break
        except:
            continue

    # If direct URLs fail, use Gutendex to find the download link
    if not text:
        try:
            meta = requests.get(
                f"https://gutendex.com/books/{gid}", timeout=6
            ).json()
            formats = meta.get("formats", {})
            for fmt in ["text/plain; charset=utf-8", "text/plain"]:
                if fmt in formats:
                    resp = requests.get(formats[fmt], timeout=12)
                    if resp.status_code == 200:
                        text = resp.text
                        break
        except:
            pass

    if not text:
        raise HTTPException(
            status_code=503,
            detail="Could not fetch book text. Try again shortly."
        )

    # ── Clean Gutenberg header and footer ─────────────────────────────────────
    # Every Gutenberg book has a long legal header before the actual text
    # and a footer after it. We strip these out.
    for marker in ["*** START OF", "***START OF"]:
        idx = text.find(marker)
        if idx != -1:
            text = text[idx:]
            text = text[text.find("\n") + 1:]
            break

    for marker in ["*** END OF", "***END OF", "End of Project Gutenberg"]:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
            break

    text = text.strip()

    # ── Paginate ──────────────────────────────────────────────────────────────
    # Split the full text into pages by character count
    total_chars = len(text)
    total_pages = max(1, total_chars // page_size)
    start       = (page - 1) * page_size
    chunk       = text[start: start + page_size]

    return {
        "book_id":     book_id,
        "title":       book["title"],
        "page":        page,
        "total_pages": total_pages,
        "content":     chunk,
        "has_prev":    page > 1,
        "has_next":    (start + page_size) < total_chars,
    }


# ─────────────────────────────────────────────────────────────────────────────
# ADD BOOK MANUALLY
# POST /books
#
# Adds a new book to our local database.
# Used when a user finds a book on Gutenberg and wants to add it.
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/", response_model=BookResponse)
def add_book(data: BookCreate):
    conn = get_conn()

    # Check author exists
    author = conn.execute(
        "SELECT * FROM authors WHERE id = ?", (data.author_id,)
    ).fetchone()
    if not author:
        conn.close()
        raise HTTPException(status_code=404, detail="Author not found")

    conn.execute("""
        INSERT INTO books
            (gutenberg_id, title, author_id, genre, cover_url,
             total_pages, description, publish_year, language)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.gutenberg_id,
        data.title,
        data.author_id,
        data.genre,
        data.cover_url,
        data.total_pages,
        data.description,
        data.publish_year,
        data.language
    ))
    conn.commit()

    # Return the newly added book with author name
    row = conn.execute("""
        SELECT b.*, a.name as author_name
        FROM books b
        JOIN authors a ON b.author_id = a.id
        WHERE b.title = ? AND b.author_id = ?
    """, (data.title, data.author_id)).fetchone()
    conn.close()
    return dict(row)
