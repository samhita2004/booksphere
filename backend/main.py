from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db

# We import each router — we'll build these files one by one
# For now they are empty files, so we import safely
from routers import users, books, shelf, reviews, highlights, recommendations

# ─────────────────────────────────────────────────────────────────────────────
# CREATE THE FASTAPI APP
# title and description show up in the auto-generated Swagger docs
# at http://localhost:8000/docs — very useful for testing
# ─────────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="BookSphere API",
    description="Backend for BookSphere — Social Reading Platform",
    version="1.0.0"
)

# ─────────────────────────────────────────────────────────────────────────────
# CORS — Cross Origin Resource Sharing
#
# Without this, the browser blocks Streamlit (port 8501) from
# talking to FastAPI (port 8000) because they are on different ports.
# allow_origins=["*"] means any origin is allowed — fine for development.
# In production you would list specific domains instead.
# ─────────────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────────────────────
# STARTUP EVENT
#
# This runs once when the server starts.
# init_db() creates all tables if they don't exist.
# So even if someone runs the server without running database.py first,
# the tables will still be created automatically.
# ─────────────────────────────────────────────────────────────────────────────
@app.on_event("startup")
def on_startup():
    init_db()
    print("✅ BookSphere API is running!")


# ─────────────────────────────────────────────────────────────────────────────
# ROUTERS
#
# Each router handles one feature area.
# prefix="/users" means all routes in users.py start with /users
#   e.g. GET /users, POST /users, GET /users/1
# tags=["Users"] groups them nicely in the Swagger docs
# ─────────────────────────────────────────────────────────────────────────────
app.include_router(users.router,           prefix="/users",           tags=["Users"])
app.include_router(books.router,           prefix="/books",           tags=["Books"])
app.include_router(shelf.router,           prefix="/shelf",           tags=["Shelf"])
app.include_router(reviews.router,         prefix="/reviews",         tags=["Reviews"])
app.include_router(highlights.router,      prefix="/highlights",      tags=["Highlights"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])


# ─────────────────────────────────────────────────────────────────────────────
# ROOT ENDPOINT
#
# A simple health check — visit http://localhost:8000
# to confirm the server is running
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "app":     "BookSphere API",
        "version": "1.0.0",
        "status":  "running",
        "docs":    "http://localhost:8000/docs"
    }