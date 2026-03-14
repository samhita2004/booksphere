import streamlit as st
import requests

API = "http://localhost:8000"

USER_MAP = {
    "Priya Sharma": 1, "Rahul Verma": 2,
    "Ananya Iyer": 3, "Karthik Rao": 4, "Meera Nair": 5
}

GENRES = ["All", "Romance", "Mystery", "Horror", "Fantasy", 
          "Adventure", "Historical", "Psychological", "Literary Fiction"]

def show():
    st.title("🔍 Discover Books")

    # User selector
    selected_user = st.selectbox("Select User", list(USER_MAP.keys()))
    user_id = USER_MAP[selected_user]

    st.divider()

    # Search bar
    query = st.text_input("🔎 Search by title, author or genre")

    # Genre filter buttons
    selected_genre = st.selectbox("Filter by Genre", GENRES)

    st.divider()

    # Fetch books based on search or genre filter
    if query:
        res = requests.get(f"{API}/books/search/{query}")
    elif selected_genre != "All":
        res = requests.get(f"{API}/books/genre/{selected_genre}")
    else:
        res = requests.get(f"{API}/books/")

    if res.status_code != 200:
        st.error("Could not load books.")
        return

    books = res.json()

    if not books:
        st.info("No books found!")
        return

    st.markdown(f"**{len(books)} books found**")
    st.divider()

    # Show books in a grid — 3 columns
    cols = st.columns(3)

    for i, book in enumerate(books):
        with cols[i % 3]:
            # Book cover
            if book["cover_url"]:
                st.image(book["cover_url"], width=120)

            st.subheader(book["title"])
            st.caption(f"✍️ {book['author_name']}")
            st.caption(f"📚 {book['genre']} · {book['publish_year']}")
            st.write(book["description"][:100] + "...")

            # Add to shelf buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📖 Reading", key=f"read_{book['id']}"):
                    r = requests.post(f"{API}/shelf/", json={
                        "user_id": user_id,
                        "book_id": book["id"],
                        "status": "reading",
                        "current_page": 0,
                        "rating": 0
                    })
                    if r.status_code == 200:
                        st.success("Added!")
                    else:
                        st.warning("Already on shelf!")

            with col2:
                if st.button("🔖 Want", key=f"want_{book['id']}"):
                    r = requests.post(f"{API}/shelf/", json={
                        "user_id": user_id,
                        "book_id": book["id"],
                        "status": "want_to_read",
                        "current_page": 0,
                        "rating": 0
                    })
                    if r.status_code == 200:
                        st.success("Added!")
                    else:
                        st.warning("Already on shelf!")

            st.divider()