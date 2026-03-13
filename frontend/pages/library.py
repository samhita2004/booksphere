import streamlit as st
import requests

API = "http://localhost:8000"

# Demo users
USER_MAP = {
    "Priya Sharma": 1, "Rahul Verma": 2,
    "Ananya Iyer": 3, "Karthik Rao": 4, "Meera Nair": 5
}

def show():
    st.title("📚 My Library")

    # User selector
    selected_user = st.selectbox("Select User", list(USER_MAP.keys()))
    user_id = USER_MAP[selected_user]

    st.divider()

    # Tabs for each shelf status
    tab1, tab2, tab3 = st.tabs(["📖 Reading", "✅ Finished", "🔖 Want to Read"])

    with tab1:
        show_shelf(user_id, "reading")

    with tab2:
        show_shelf(user_id, "finished")

    with tab3:
        show_shelf(user_id, "want_to_read")


def show_shelf(user_id, status):
    # Fetch books filtered by status
    res = requests.get(f"{API}/shelf/{user_id}/status/{status}")

    if res.status_code != 200:
        st.error("Could not load shelf.")
        return

    books = res.json()

    if not books:
        st.info("No books here yet!")
        return

    # Show each book as a card
    for book in books:
        col1, col2 = st.columns([1, 4])

        with col1:
            if book["cover_url"]:
                st.image(book["cover_url"], width=80)

        with col2:
            st.subheader(book["title"])
            st.caption(f"✍️ {book['author_name']} · {book['genre']}")

            # Show progress bar for reading books
            if status == "reading" and book["total_pages"] > 0:
                progress = book["current_page"] / book["total_pages"]
                st.progress(progress)
                st.caption(f"Page {book['current_page']} of {book['total_pages']}")

            # Show star rating for finished books
            if status == "finished" and book["rating"] > 0:
                stars = "⭐" * book["rating"]
                st.caption(f"Your rating: {stars}")

            # Show dates
            if book["date_started"]:
                st.caption(f"📅 Started: {book['date_started'][:10]}")
            if book["date_finished"]:
                st.caption(f"🏁 Finished: {book['date_finished'][:10]}")

            # Remove from shelf button
            if st.button(f"🗑️ Remove", key=f"remove_{book['book_id']}"):
                requests.delete(f"{API}/shelf/{user_id}/{book['book_id']}")
                st.rerun()

        st.divider()