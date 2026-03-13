import streamlit as st
import requests

API = "http://localhost:8000"

USER_MAP = {
    "Priya Sharma": 1, "Rahul Verma": 2,
    "Ananya Iyer": 3, "Karthik Rao": 4, "Meera Nair": 5
}

def show():
    st.title("💡 Highlights")

    # User selector
    selected_user = st.selectbox("Select User", list(USER_MAP.keys()))
    user_id = USER_MAP[selected_user]

    st.divider()

    # Tabs — My Highlights and Book Highlights
    tab1, tab2 = st.tabs(["My Highlights", "Browse by Book"])

    with tab1:
        show_user_highlights(user_id)

    with tab2:
        show_book_highlights()


def show_user_highlights(user_id):
    res = requests.get(f"{API}/highlights/user/{user_id}")

    if res.status_code != 200:
        st.error("Could not load highlights.")
        return

    highlights = res.json()

    if not highlights:
        st.info("No highlights yet! Save quotes while reading.")
        return

    for h in highlights:
        with st.container():
            # Quote in a blockquote style
            st.markdown(f"> *{h['quote']}*")
            st.caption(f"📖 {h['book_title']} · Page {h['page_number']}")

            # Show note if exists
            if h["note"]:
                st.caption(f"💭 {h['note']}")

            # Like button
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button(f"❤️ {h['likes']}", key=f"like_{h['id']}"):
                    requests.put(f"{API}/highlights/{h['id']}/like")
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"del_{h['id']}"):
                    requests.delete(f"{API}/highlights/{h['id']}")
                    st.rerun()

            st.divider()


def show_book_highlights(user_id=None):
    # Get all books for dropdown
    res = requests.get(f"{API}/books/")
    if res.status_code != 200:
        st.error("Could not load books.")
        return

    books = res.json()
    book_map = {b["title"]: b["id"] for b in books}

    selected_book = st.selectbox("Choose a book", list(book_map.keys()))
    book_id = book_map[selected_book]

    # Fetch highlights for selected book
    res = requests.get(f"{API}/highlights/book/{book_id}")
    highlights = res.json()

    if not highlights:
        st.info("No highlights for this book yet!")
        return

    for h in highlights:
        with st.container():
            st.markdown(f"> *{h['quote']}*")
            st.caption(f"👤 {h['display_name']} · Page {h['page_number']}")

            if h["note"]:
                st.caption(f"💭 {h['note']}")

            col1, _ = st.columns([1, 4])
            with col1:
                if st.button(f"❤️ {h['likes']}", key=f"blike_{h['id']}"):
                    requests.put(f"{API}/highlights/{h['id']}/like")
                    st.rerun()

            st.divider()