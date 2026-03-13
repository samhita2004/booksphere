import sqlite3
import os

# This tells Python where to save the database file.
# __file__ means "this current file (database.py)"
# So the .db file will be saved right inside the backend/ folder
DB_PATH = os.path.join(os.path.dirname(__file__), "booksphere.db")


def get_conn():
    """
    This function opens a connection to the database.
    Call this every time you need to read or write data.

    row_factory = sqlite3.Row
        → lets you access data by column name: row["title"]
          instead of by index: row[2]

    foreign_keys = ON
        → enforces relationships — e.g. you can't add a book
          with an author_id that doesn't exist in authors table

    journal_mode = WAL
        → makes reads and writes faster and safer
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def init_db():
    """
    Creates all 6 tables if they don't already exist.
    'CREATE TABLE IF NOT EXISTS' means it's safe to call
    every time the app starts — it won't delete existing data.
    """
    conn = get_conn()
    c = conn.cursor()

    # ── TABLE 1: AUTHORS ──────────────────────────────────────────────────────
    # We separate authors from books so that one author entry
    # covers all their books. Arthur Conan Doyle is stored once,
    # then all his books just reference his id.
    c.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL UNIQUE,
            birth_year  INTEGER,
            death_year  INTEGER,
            nationality TEXT    DEFAULT '',
            bio         TEXT    DEFAULT '',
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)

    # ── TABLE 2: BOOKS ────────────────────────────────────────────────────────
    # Core book catalog.
    # gutenberg_id → used to fetch full book text from Project Gutenberg
    # author_id    → FOREIGN KEY linking to authors table
    # cover_url    → image link from Open Library API
    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            gutenberg_id  INTEGER UNIQUE,
            title         TEXT    NOT NULL,
            author_id     INTEGER NOT NULL,
            genre         TEXT    DEFAULT 'Classic',
            cover_url     TEXT    DEFAULT '',
            total_pages   INTEGER DEFAULT 200,
            description   TEXT    DEFAULT '',
            publish_year  INTEGER,
            language      TEXT    DEFAULT 'en',
            created_at    TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (author_id) REFERENCES authors(id)
        )
    """)

    # ── TABLE 3: USERS ────────────────────────────────────────────────────────
    # Reader profiles.
    # username is UNIQUE — no two people can have the same handle
    # avatar_emoji → fun profile picture e.g. 🌸 🎯 ✨
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    NOT NULL UNIQUE,
            display_name  TEXT    NOT NULL,
            email         TEXT    DEFAULT '',
            avatar_emoji  TEXT    DEFAULT '📚',
            bio           TEXT    DEFAULT '',
            joined_at     TEXT    DEFAULT (datetime('now'))
        )
    """)

    # ── TABLE 4: USER_BOOKS (the shelf) ───────────────────────────────────────
    # This is the most important table for recommendations.
    # It tracks EVERY user's relationship with EVERY book.
    #
    # status values:
    #   want_to_read → saved for later
    #   reading      → currently reading
    #   finished     → completed
    #   abandoned    → gave up on it
    #
    # UNIQUE(user_id, book_id) → one user can't add the same book twice
    # rating 0 means not rated yet, 1-5 are actual star ratings
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_books (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id        INTEGER NOT NULL,
            book_id        INTEGER NOT NULL,
            status         TEXT    DEFAULT 'want_to_read',
            current_page   INTEGER DEFAULT 0,
            rating         INTEGER DEFAULT 0,
            date_started   TEXT,
            date_finished  TEXT,
            UNIQUE (user_id, book_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)

    # ── TABLE 5: REVIEWS ──────────────────────────────────────────────────────
    # Full written reviews — longer than just a star rating.
    # title      → optional headline e.g. "A masterpiece!"
    # body       → the full review text
    # is_spoiler → 1 means the review contains spoilers,
    #              UI will hide it behind a warning
    # UNIQUE(user_id, book_id) → one review per user per book
    c.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            book_id     INTEGER NOT NULL,
            rating      INTEGER NOT NULL,
            title       TEXT    DEFAULT '',
            body        TEXT    NOT NULL,
            likes       INTEGER DEFAULT 0,
            is_spoiler  INTEGER DEFAULT 0,
            created_at  TEXT    DEFAULT (datetime('now')),
            updated_at  TEXT    DEFAULT (datetime('now')),
            UNIQUE (user_id, book_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)

    # ── TABLE 6: HIGHLIGHTS ───────────────────────────────────────────────────
    # Quotes saved while reading inside the app.
    # note → user's own thought about the quote (optional)
    #
    # WHY THIS MATTERS FOR RECOMMENDATIONS:
    # If a user saves many highlights from Mystery books,
    # we know they love Mystery even if they haven't rated anything yet.
    # This helps the content-based fallback in our hybrid engine.
    c.execute("""
        CREATE TABLE IF NOT EXISTS highlights (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            book_id      INTEGER NOT NULL,
            quote        TEXT    NOT NULL,
            page_number  INTEGER DEFAULT 0,
            note         TEXT    DEFAULT '',
            likes        INTEGER DEFAULT 0,
            created_at   TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ All 6 tables created successfully.")


if __name__ == "__main__":
    init_db()