from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sqlite3
import hashlib
 
router = APIRouter(prefix="/users", tags=["users"])
 
# This is the shape of data we expect when someone registers
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
 
# This is the shape of data we send back (never send password back!)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: str
 
# Helper: connect to the database
def get_db():
    conn = sqlite3.connect("booksphere.db")
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn
 
# Helper: hash the password so we never store it as plain text
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
 
 
# ── ENDPOINT 1: Register a new user ──────────────────────────────────────────
# URL: POST /users/register
# What it does: takes username, email, password → saves to database
@router.post("/register", response_model=UserResponse)
def register_user(user: UserRegister):
    conn = get_db()
    cursor = conn.cursor()
 
    # Check if email is already taken
    existing = cursor.execute(
        "SELECT id FROM users WHERE email = ?", (user.email,)
    ).fetchone()
 
    if existing:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
 
    # Save the new user
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO users (username, email, hashed_password, created_at) VALUES (?, ?, ?, ?)",
        (user.username, user.email, hash_password(user.password), now)
    )
    conn.commit()
 
    # Fetch the newly created user to return it
    new_user = cursor.execute(
        "SELECT * FROM users WHERE email = ?", (user.email,)
    ).fetchone()
    conn.close()
 
    return {
        "id": new_user["id"],
        "username": new_user["username"],
        "email": new_user["email"],
        "created_at": new_user["created_at"]
    }
 
 
# ── ENDPOINT 2: Get a single user's profile ───────────────────────────────────
# URL: GET /users/{user_id}
# What it does: receives a user ID → returns that user's info
@router.get("/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
 
    user = cursor.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
 
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
 
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "created_at": user["created_at"]
    }
 
 
# ── ENDPOINT 3: List all users ────────────────────────────────────────────────
# URL: GET /users/
# What it does: returns a list of every user in the database
@router.get("/", response_model=List[UserResponse])
def list_users():
    conn = get_db()
    cursor = conn.cursor()
 
    users = cursor.execute("SELECT * FROM users").fetchall()
    conn.close()
 
    return [
        {
            "id": u["id"],
            "username": u["username"],
            "email": u["email"],
            "created_at": u["created_at"]
        }
        for u in users
    ]
