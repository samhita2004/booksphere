from fastapi import APIRouter, HTTPException
from datetime import datetime
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_conn
from models import HighlightCreate, HighlightResponse, MessageResponse

router = APIRouter(prefix="/highlights", tags=["Highlights"])


# Returns all highlights saved by a specific user
@router.get("/user/{user_id}", response_model=list[HighlightResponse])
def get_user_highlights(user_id: int):
    conn = get_conn()
    rows = conn.execute("""
        SELECT h.*, u.display_name, u.avatar_emoji, b.title AS book_title
        FROM highlights h
        JOIN users u ON h.user_id = u.id
        JOIN books b ON h.book_id = b.id
        WHERE h.user_id = ?
        ORDER BY h.created_at DESC
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# Returns all highlights for a specific book from all users
@router.get("/book/{book_id}", response_model=list[HighlightResponse])
def get_book_highlights(book_id: int):
    conn = get_conn()
    rows = conn.execute("""
        SELECT h.*, u.display_name, u.avatar_emoji, b.title AS book_title
        FROM highlights h
        JOIN users u ON h.user_id = u.id
        JOIN books b ON h.book_id = b.id
        WHERE h.book_id = ?
        ORDER BY h.likes DESC
    """, (book_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# Save a new quote while reading
@router.post("/", response_model=MessageResponse)
def add_highlight(highlight: HighlightCreate):
    conn = get_conn()
    conn.execute("""
        INSERT INTO highlights (user_id, book_id, quote, page_number, note)
        VALUES (?, ?, ?, ?, ?)
    """, (
        highlight.user_id, highlight.book_id, highlight.quote,
        highlight.page_number, highlight.note
    ))
    conn.commit()
    conn.close()
    return {"message": "Highlight saved successfully"}


# Like someone's highlight — increments like count by 1
@router.put("/{highlight_id}/like", response_model=MessageResponse)
def like_highlight(highlight_id: int):
    conn = get_conn()
    existing = conn.execute(
        "SELECT id FROM highlights WHERE id = ?", (highlight_id,)
    ).fetchone()

    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Highlight not found")

    conn.execute(
        "UPDATE highlights SET likes = likes + 1 WHERE id = ?", (highlight_id,)
    )
    conn.commit()
    conn.close()
    return {"message": "Highlight liked!"}


# Delete a highlight
@router.delete("/{highlight_id}", response_model=MessageResponse)
def delete_highlight(highlight_id: int):
    conn = get_conn()
    existing = conn.execute(
        "SELECT id FROM highlights WHERE id = ?", (highlight_id,)
    ).fetchone()

    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Highlight not found")

    conn.execute("DELETE FROM highlights WHERE id = ?", (highlight_id,))
    conn.commit()
    conn.close()
    return {"message": "Highlight deleted successfully"}