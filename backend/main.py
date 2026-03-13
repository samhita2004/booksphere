from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db

# Import all routers — each file handles one feature
from routers import books, shelf, highlights, users, reviews, recommendations

# Create the FastAPI app
app = FastAPI(
    title="BookSphere API",
    description="Social Reading Platform — Backend API",
    version="1.0.0"
)

# CORS middleware — allows the Streamlit frontend (running on port 8501)
# to talk to this FastAPI backend (running on port 8000)
# Without this, the browser blocks cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
# Each router handles its own prefix e.g. /books, /shelf, /highlights
app.include_router(books.router)
app.include_router(shelf.router)
app.include_router(highlights.router)
app.include_router(users.router)
app.include_router(reviews.router)
app.include_router(recommendations.router)

# Create all DB tables when the server starts
@app.on_event("startup")
def startup():
    init_db()
    print("✅ Database ready")

# Root endpoint — just to confirm the API is running
@app.get("/")
def root():
    return {
        "message": "Welcome to BookSphere API 📚",
        "docs": "http://localhost:8000/docs"
    }