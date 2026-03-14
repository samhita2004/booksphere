from fastapi import APIRouter, HTTPException
import requests
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_conn
from models import BookCreate, BookResponse, MessageResponse

# All endpoints here will start with /books
router = APIRouter(prefix="/books", tags=["Books"])


# ─────────────────────────────────────────────────────────────────────────────
# GET /books/
# Returns every book in the DB with author name
# Used by: discover.py to show the full catalog
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/", response_model=list[BookResponse])
def get_all_books():
    conn = get_conn()
    rows = conn.execute("""
        SELECT b.*, a.name AS author_name
        FROM books b
        JOIN authors a ON b.author_id = a.id
        ORDER BY b.title
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ─────────────────────────────────────────────────────────────────────────────
# GET /books/search/{query}
# Search books by title, author or genre
# LIKE with % means "contains" — search "sher" finds "Sherlock Holmes"
# MUST be defined BEFORE /{book_id} — FastAPI reads routes top to bottom
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/search/{query}", response_model=list[BookResponse])
def search_books(query: str):
    conn = get_conn()
    pattern = f"%{query}%"
    rows = conn.execute("""
        SELECT b.*, a.name AS author_name
        FROM books b
        JOIN authors a ON b.author_id = a.id
        WHERE b.title LIKE ? OR a.name LIKE ? OR b.genre LIKE ?
        ORDER BY b.title
    """, (pattern, pattern, pattern)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ─────────────────────────────────────────────────────────────────────────────
# GET /books/genre/{genre}
# Filter books by genre — used on Discover page genre buttons
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/genre/{genre}", response_model=list[BookResponse])
def get_books_by_genre(genre: str):
    conn = get_conn()
    rows = conn.execute("""
        SELECT b.*, a.name AS author_name
        FROM books b
        JOIN authors a ON b.author_id = a.id
        WHERE b.genre LIKE ?
        ORDER BY b.title
    """, (f"%{genre}%",)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ─────────────────────────────────────────────────────────────────────────────
# GET /books/text/{gutenberg_id}
# Fetches actual full book text from Project Gutenberg
# gutenberg_id is stored in our books table
# e.g. Pride and Prejudice = 1342
# Returns first 50,000 characters so the reader loads fast
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/text/{gutenberg_id}")
def get_book_text(gutenberg_id: int):
    # Gutenberg serves plain text at this URL pattern
    url = f"https://www.gutenberg.org/cache/epub/{gutenberg_id}/pg{gutenberg_id}.txt"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Book text not found on Gutenberg")

        text = response.text

        # Gutenberg files have a long header/footer with legal info
        # We try to strip everything before "*** START OF" marker
        start_marker = "*** START OF"
        end_marker = "*** END OF"

        if start_marker in text:
            text = text[text.index(start_marker):]
            # Skip past the marker line itself
            text = text[text.index("\n") + 1:]

        if end_marker in text:
            text = text[:text.index(end_marker)]

        # Return only first 50,000 characters — enough for ~150 pages
        return {
            "gutenberg_id": gutenberg_id,
            "text": text[:50000].strip(),
            "total_chars": len(text)
        }

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Gutenberg took too long to respond")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────────────────────
# GET /books/{book_id}
# Get one specific book by its database ID
# Used by reader.py when opening a book
# NOTE: This must come AFTER /search and /genre routes
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    conn = get_conn()
    row = conn.execute("""
        SELECT b.*, a.name AS author_name
        FROM books b
        JOIN authors a ON b.author_id = a.id
        WHERE b.id = ?
    """, (book_id,)).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Book not found")
    return dict(row)


# ─────────────────────────────────────────────────────────────────────────────
# POST /books/
# Add a new book to the database manually
# Used if someone wants to add a book not in the seed data
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/", response_model=BookResponse)
def add_book(book: BookCreate):
    conn = get_conn()

    # Check the author exists first
    author = conn.execute(
        "SELECT * FROM authors WHERE id = ?", (book.author_id,)
    ).fetchone()

    if not author:
        conn.close()
        raise HTTPException(status_code=404, detail="Author not found")

    try:
        c = conn.execute("""
            INSERT INTO books
                (gutenberg_id, title, author_id, genre, cover_url,
                 total_pages, description, publish_year, language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            book.gutenberg_id, book.title, book.author_id,
            book.genre, book.cover_url, book.total_pages,
            book.description, book.publish_year, book.language
        ))
        conn.commit()
        new_id = c.lastrowid
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=str(e))

    # Fetch and return the newly created book
    row = conn.execute("""
        SELECT b.*, a.name AS author_name
        FROM books b
        JOIN authors a ON b.author_id = a.id
        WHERE b.id = ?
    """, (new_id,)).fetchone()
    conn.close()
    return dict(row)
