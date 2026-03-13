from fastapi import APIRouter, HTTPException
import sys, os
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_conn
from models import ReviewCreate, ReviewResponse, MessageResponse

router = APIRouter(prefix="/reviews", tags=["Reviews"])


# ─────────────────────────────────────────────────────────────────────────────
# GET ALL REVIEWS FOR A BOOK
# GET /reviews/book/{book_id}
#
# Returns all reviews for a specific book.
# Used on the book detail page to show what readers think.
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/book/{book_id}", response_model=list[ReviewResponse])
def get_book_reviews(book_id: int):
    conn = get_conn()
    rows = conn.execute("""
        SELECT r.*,
               u.display_name,
               u.avatar_emoji
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.book_id = ?
        ORDER BY r.likes DESC, r.created_at DESC
    """, (book_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ─────────────────────────────────────────────────────────────