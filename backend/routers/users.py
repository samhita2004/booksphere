from fastapi import APIRouter, HTTPException
from database import get_conn
from models import UserCreate, UserResponse, MessageResponse
import sqlite3

# APIRouter() is like a mini FastAPI app
# main.py collects all routers and mounts them together
router = APIRouter()


# ─────────────────────────────────────────────────────────────────────────────
# GET ALL USERS
# GET /users
#
# Returns a list of all registered readers.
# Used by the frontend sidebar to populate the user selector.
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/", response_model=list[UserResponse])
def get_all_users():
    conn = get_conn()
    rows = conn.execute("""
        SELECT id, username, display_name, email,
               avatar_emoji, bio, joined_at
        FROM users
        ORDER BY display_name
    """).fetchall()
    conn.close()

    # dict(row) converts sqlite3.Row to a plain dictionary
    # Pydantic then validates it against UserResponse
    return [dict(row) for row in rows]


# ─────────────────────────────────────────────────────────────────────────────
# GET ONE USER
# GET /users/{user_id}
#
# Returns a single user by their ID.
# Used by the profile page and recommendation engine.
# ───