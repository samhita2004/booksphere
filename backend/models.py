from pydantic import BaseModel, Field
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
# HOW TO READ THESE MODELS:
#
# BaseModel   → every model inherits from this (Pydantic requirement)
# Optional    → the field is not required — has a default value
# Field(...)  → ... means REQUIRED, no default
# ─────────────────────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════════════════════
# AUTHOR MODELS
# ══════════════════════════════════════════════════════════════════════════════

class AuthorCreate(BaseModel):
    """
    Used when ADDING a new author.
    Only name is required — the rest is optional metadata.
    """
    name:        str
    birth_year:  Optional[int] = None
    death_year:  Optional[int] = None
    nationality: Optional[str] = ""
    bio:         Optional[str] = ""


class AuthorResponse(BaseModel):
    """
    Used when RETURNING author data.
    Includes id and created_at which the DB generates — 
    we never ask the user to send these.
    """
    id:          int
    name:        str
    birth_year:  Optional[int] = None
    death_year:  Optional[int] = None
    nationality: Optional[str] = ""
    bio:         Optional[str] = ""
    created_at:  Optional[str] = None


# ══════════════════════════════════════════════════════════════════════════════
# BOOK MODELS
# ══════════════════════════════════════════════════════════════════════════════

class BookCreate(BaseModel):
    """
    Used when ADDING a new book manually.
    title and author_id are required — everything else is optional.
    """
    title:        str
    author_id:    int
    gutenberg_id: Optional[int]  = None
    genre:        Optional[str]  = "Classic"
    cover_url:    Optional[str]  = ""
    total_pages:  Optional[int]  = 200
    description:  Optional[str]  = ""
    publish_year: Optional[int]  = None
    language:     Optional[str]  = "en"


class BookResponse(BaseModel):
    """
    Used when RETURNING book data.
    author_name is extra — we JOIN the authors table to get it
    so the frontend doesn't need to make a second API call.
    """
    id:           int
    title:        str
    author_id:    int
    author_name:  Optional[str] = ""   # comes from JOIN with authors table
    gutenberg_id: Optional[int] = None
    genre:        Optional[str] = ""
    cover_url:    Optional[str] = ""
    total_pages:  Optional[int] = 200
    description:  Optional[str] = ""
    publish_year: Optional[int] = None
    language:     Optional[str] = "en"
    created_at:   Optional[str] = None


# ══════════════════════════════════════════════════════════════════════════════
# USER MODELS
# ══════════════════════════════════════════════════════════════════════════════

class UserCreate(BaseModel):
    """
    Used when REGISTERING a new user.
    username and display_name are required.
    """
    username:     str
    display_name: str
    email:        Optional[str] = ""
    avatar_emoji: Optional[str] = "📚"
    bio:          Optional[str] = ""


class UserResponse(BaseModel):
    """
    Used when RETURNING user data.
    Never expose passwords here (we don't have one yet, but good habit).
    """
    id:           int
    username:     str
    display_name: str
    email:        Optional[str] = ""
    avatar_emoji: Optional[str] = "📚"
    bio:          Optional[str] = ""
    joined_at:    Optional[str] = None


# ══════════════════════════════════════════════════════════════════════════════
# SHELF (USER_BOOKS) MODELS
# ══════════════════════════════════════════════════════════════════════════════

class ShelfAdd(BaseModel):
    """
    Used when a user ADDS a book to their shelf or UPDATES progress.
    user_id and book_id are required — you must say who and what.
    status must be one of the 4 allowed values.
    """
    user_id:      int
    book_id:      int
    status:       str = "want_to_read"  # want_to_read | reading | finished | abandoned
    current_page: Optional[int] = 0
    rating:       Optional[int] = 0     # 0 = not rated, 1-5 = stars


class ShelfResponse(BaseModel):
    """
    Used when RETURNING shelf data.
    Includes full book details so the frontend
    doesn't need to make extra API calls.
    """
    id:            int
    user_id:       int
    book_id:       int
    title:         Optional[str] = ""   # from books table JOIN
    author_name:   Optional[str] = ""   # from authors table JOIN
    cover_url:     Optional[str] = ""
    genre:         Optional[str] = ""
    total_pages:   Optional[int] = 0
    status:        Optional[str] = ""
    current_page:  Optional[int] = 0
    rating:        Optional[int] = 0
    date_started:  Optional[str] = None
    date_finished: Optional[str] = None


# ══════════════════════════════════════════════════════════════════════════════
# REVIEW MODELS
# ══════════════════════════════════════════════════════════════════════════════

class ReviewCreate(BaseModel):
    """
    Used when WRITING a new review.
    rating and body are required — you must give stars and write something.
    is_spoiler defaults to False (0).
    """
    user_id:    int
    book_id:    int
    rating:     int                    # must be 1 to 5
    title:      Optional[str] = ""
    body:       str                    # required — the review text
    is_spoiler: Optional[int] = 0      # 0 = no spoiler, 1 = spoiler


class ReviewResponse(BaseModel):
    """
    Used when RETURNING reviews.
    Includes display_name and avatar_emoji from users table
    so the frontend can show who wrote the review.
    """
    id:           int
    user_id:      int
    book_id:      int
    display_name: Optional[str] = ""   # from users table JOIN
    avatar_emoji: Optional[str] = "📚"
    rating:       int
    title:        Optional[str] = ""
    body:         str
    likes:        Optional[int] = 0
    is_spoiler:   Optional[int] = 0
    created_at:   Optional[str] = None


# ══════════════════════════════════════════════════════════════════════════════
# HIGHLIGHT MODELS
# ══════════════════════════════════════════════════════════════════════════════

class HighlightCreate(BaseModel):
    """
    Used when SAVING a quote while reading.
    user_id, book_id and quote are all required.
    """
    user_id:     int
    book_id:     int
    quote:       str
    page_number: Optional[int] = 0
    note:        Optional[str] = ""    # user's own thought on the quote


class HighlightResponse(BaseModel):
    """
    Used when RETURNING highlights.
    Includes book title and user name for context.
    """
    id:           int
    user_id:      int
    book_id:      int
    display_name: Optional[str] = ""   # from users table JOIN
    avatar_emoji: Optional[str] = "📚"
    book_title:   Optional[str] = ""   # from books table JOIN
    quote:        str
    page_number:  Optional[int] = 0
    note:         Optional[str] = ""
    likes:        Optional[int] = 0
    created_at:   Optional[str] = None


# ══════════════════════════════════════════════════════════════════════════════
# RECOMMENDATION MODEL
# ══════════════════════════════════════════════════════════════════════════════

class RecommendationResponse(BaseModel):
    """
    Used when RETURNING recommended books.
    reason explains WHY this book was recommended —
    shown in the UI so users understand the suggestion.

    method tells us which engine produced it:
      'collaborative' → similar users liked this
      'content'       → matches your favourite genre/author
    """
    book_id:      int
    title:        str
    author_name:  Optional[str] = ""
    genre:        Optional[str] = ""
    cover_url:    Optional[str] = ""
    description:  Optional[str] = ""
    reason:       str                  # e.g. "Because you loved Mystery books"
    method:       str                  # 'collaborative' or 'content'


# ══════════════════════════════════════════════════════════════════════════════
# GENERIC RESPONSE
# ══════════════════════════════════════════════════════════════════════════════

class MessageResponse(BaseModel):
    """
    Simple response for actions like delete, like, update.
    e.g. { "message": "Review deleted successfully" }
    """
    message: str