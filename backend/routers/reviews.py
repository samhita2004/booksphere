from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import sqlite3
 
router = APIRouter(prefix="/reviews", tags=["reviews"])
 
# Shape of data needed to write a review
class ReviewCreate(BaseModel):
    user_id: int
    book_id: int
    rating: int        # must be 1 to 5
    review_text: str
 
# Shape of data we send back
class ReviewResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: int
    review_text: str
    created_at: str
    helpful_votes: int
 
# Helper: connect to database
def get_db():
    conn = sqlite3.connect("booksphere.db")
    conn.row_factory = sqlite3.Row
    return conn
 
 
# ── ENDPOINT 1: Write a review ────────────────────────────────────────────────
# URL: POST /reviews/
# What it does: takes user_id, book_id, rating, review_text → saves to database
@router.post("/", response_model=ReviewResponse)
def write_review(review: ReviewCreate):
    # Validate rating is between 1 and 5
    if not 1 <= review.rating <= 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
 
    conn = get_db()
    cursor = conn.cursor()
 
    # Check if this user already reviewed this book
    existing = cursor.execute(
        "SELECT id FROM reviews WHERE user_id = ? AND book_id = ?",
        (review.user_id, review.book_id)
    ).fetchone()
 
    if existing:
        conn.close()
        raise HTTPException(status_code=400, detail="You already reviewed this book")
 
    # Save the review
    now = datetime.now().isoformat()
    cursor.execute(
        """INSERT INTO reviews (user_id, book_id, rating, review_text, created_at, helpful_votes)
           VALUES (?, ?, ?, ?, ?, 0)""",
        (review.user_id, review.book_id, review.rating, review.review_text, now)
    )
    conn.commit()
 
    # Fetch and return the saved review
    new_review = cursor.execute(
        "SELECT * FROM reviews WHERE user_id = ? AND book_id = ?",
        (review.user_id, review.book_id)
    ).fetchone()
    conn.close()
 
    return dict(new_review)
 
 
# ── ENDPOINT 2: Get all reviews for a book ────────────────────────────────────
# URL: GET /reviews/book/{book_id}
# What it does: returns every review written for a specific book
@router.get("/book/{book_id}", response_model=List[ReviewResponse])
def get_reviews_for_book(book_id: int):
    conn = get_db()
    cursor = conn.cursor()
 
    reviews = cursor.execute(
        "SELECT * FROM reviews WHERE book_id = ? ORDER BY created_at DESC",
        (book_id,)
    ).fetchall()
    conn.close()
 
    if not reviews:
        return []  # no reviews yet, return empty list (not an error)
 
    return [dict(r) for r in reviews]
 
 
# ── ENDPOINT 3: Like a review ─────────────────────────────────────────────────
# URL: POST /reviews/{review_id}/like
# What it does: adds 1 helpful vote to a review
@router.post("/{review_id}/like")
def like_review(review_id: int):
    conn = get_db()
    cursor = conn.cursor()
 
    # Check the review exists
    review = cursor.execute(
        "SELECT id FROM reviews WHERE id = ?", (review_id,)
    ).fetchone()
 
    if not review:
        conn.close()
        raise HTTPException(status_code=404, detail="Review not found")
 
    # Add 1 to helpful_votes
    cursor.execute(
        "UPDATE reviews SET helpful_votes = helpful_votes + 1 WHERE id = ?",
        (review_id,)
    )
    conn.commit()
    conn.close()
 
    return {"message": "Review liked!", "review_id": review_id}