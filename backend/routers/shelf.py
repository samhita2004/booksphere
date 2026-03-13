from fastapi import APIRouter, HTTPException
import sys, os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_conn
from models import ShelfAdd, ShelfResponse, MessageResponse

router = APIRouter(prefix="/shelf", tags=["Shelf"])


# GET /shelf/{user_id} → Return all books on a user's shelf with full book details
@router.get("/{user_id}", response_model=list[ShelfResponse])
def get_shelf(user_id: int):
    conn = get_conn()
    rows = conn.execute("""
        SELECT
            ub.id, ub.user_id, ub.book_id,
            b.title, a.name AS author_name,
            b.cover_url, b.genre, b.total_pages,
            ub.status, ub.current_page, ub.rating,
            ub.date_started, ub.date_finished
        FROM user_books ub
        JOIN books b ON ub.book_id = b.id
        JOIN authors a ON b.author_id = a.id
        WHERE ub.user_id = ?
        ORDER BY ub.date_started DESC
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# GET /shelf/{user_id}/status/{status} → Filter shelf by reading status
@router.get("/{user_id}/status/{status}", response_model=list[ShelfResponse])
def get_shelf_by_status(user_id: int, status: str):
    conn = get_conn()
    rows = conn.execute("""
        SELECT
            ub.id, ub.user_id, ub.book_id,
            b.title, a.name AS author_name,
            b.cover_url, b.genre, b.total_pages,
            ub.status, ub.current_page, ub.rating,
            ub.date_started, ub.date_finished
        FROM user_books ub
        JOIN books b ON ub.book_id = b.id
        JOIN authors a ON b.author_id = a.id
        WHERE ub.user_id = ? AND ub.status = ?
        ORDER BY ub.date_started DESC
    """, (user_id, status)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# POST /shelf/ → Add a book to the user's shelf
@router.post("/", response_model=MessageResponse)
def add_to_shelf(entry: ShelfAdd):
    conn = get_conn()

    # Check if book already exists on shelf
    existing = conn.execute("""
        SELECT id FROM user_books
        WHERE user_id = ? AND book_id = ?
    """, (entry.user_id, entry.book_id)).fetchone()

    if existing:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Book already on shelf. Use PUT to update."
        )

    # Auto set dates based on reading status
    date_started = None
    date_finished = None

    if entry.status == "reading":
        date_started = datetime.now().isoformat()
    elif entry.status == "finished":
        date_started = datetime.now().isoformat()
        date_finished = datetime.now().isoformat()

    conn.execute("""
        INSERT INTO user_books
            (user_id, book_id, status, current_page,
             rating, date_started, date_finished)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        entry.user_id, entry.book_id, entry.status,
        entry.current_page, entry.rating,
        date_started, date_finished
    ))
    conn.commit()
    conn.close()
    return {"message": f"Book added to shelf with status '{entry.status}'"}


# PUT /shelf/ → Update reading progress, status, or rating
@router.put("/", response_model=MessageResponse)
def update_shelf(entry: ShelfAdd):
    conn = get_conn()

    # Ensure the book already exists on shelf
    existing = conn.execute("""
        SELECT id FROM user_books
        WHERE user_id = ? AND book_id = ?
    """, (entry.user_id, entry.book_id)).fetchone()

    if not existing:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Book not on shelf. Use POST to add it first."
        )

    # Record finish date if status becomes finished
    date_finished = None
    if entry.status == "finished":
        date_finished = datetime.now().isoformat()

    conn.execute("""
        UPDATE user_books
        SET status        = ?,
            current_page  = ?,
            rating        = ?,
            date_finished = COALESCE(?, date_finished)
        WHERE user_id = ? AND book_id = ?
    """, (
        entry.status, entry.current_page,
        entry.rating, date_finished,
        entry.user_id, entry.book_id
    ))
    conn.commit()
    conn.close()
    return {"message": "Shelf updated successfully"}


# DELETE /shelf/{user_id}/{book_id} → Remove a book from the user's shelf
@router.delete("/{user_id}/{book_id}", response_model=MessageResponse)
def remove_from_shelf(user_id: int, book_id: int):
    conn = get_conn()

    # Check if book exists before deleting
    existing = conn.execute("""
        SELECT id FROM user_books
        WHERE user_id = ? AND book_id = ?
    """, (user_id, book_id)).fetchone()

    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Book not on shelf")

    conn.execute("""
        DELETE FROM user_books
        WHERE user_id = ? AND book_id = ?
    """, (user_id, book_id))
    conn.commit()
    conn.close()
    return {"message": "Book removed from shelf successfully"}