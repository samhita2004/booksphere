import streamlit as st
import requests

API = "http://localhost:8000"

def show():
    st.title("📖 Book Reader")

    # Get book list for the dropdown
    books = requests.get(f"{API}/books/").json()
    book_options = {b["title"]: b for b in books}

    # Book selector dropdown
    selected_title = st.selectbox("Choose a book", list(book_options.keys()))
    book = book_options[selected_title]

    # User selector — hardcoded demo users for now
    user_map = {
        "Priya Sharma": 1, "Rahul Verma": 2,
        "Ananya Iyer": 3, "Karthik Rao": 4, "Meera Nair": 5
    }
    selected_user = st.selectbox("Reading as", list(user_map.keys()))
    user_id = user_map[selected_user]

    st.divider()

    # Show book info header
    col1, col2 = st.columns([1, 3])
    with col1:
        if book["cover_url"]:
            st.image(book["cover_url"], width=120)
    with col2:
        st.subheader(book["title"])
        st.caption(f"✍️ {book['author_name']} · {book['genre']} · {book['total_pages']} pages")
        st.write(book["description"])

    st.divider()

    # Fetch book text from Gutenberg via our API
    if book["gutenberg_id"]:
        with st.spinner("Loading book text..."):
            try:
                res = requests.get(f"{API}/books/text/{book['gutenberg_id']}", timeout=15)
                if res.status_code == 200:
                    full_text = res.json()["text"]
                else:
                    st.error("Could not load book text from Gutenberg.")
                    return
            except Exception as e:
                st.error(f"Connection error: {e}")
                return

        # Split text into pages of 2000 characters each
        page_size = 2000
        pages = [full_text[i:i+page_size] for i in range(0, len(full_text), page_size)]
        total_pages = len(pages)

        # Page navigation using session state so it persists
        if "current_page" not in st.session_state:
            st.session_state.current_page = 0

        # Show current page text
        st.markdown(f"**Page {st.session_state.current_page + 1} of {total_pages}**")
        st.text_area("", pages[st.session_state.current_page], height=400, disabled=True)

        # Previous / Next buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Previous") and st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()
        with col3:
            if st.button("Next ➡️") and st.session_state.current_page < total_pages - 1:
                st.session_state.current_page += 1
                st.rerun()

        # Auto save progress to shelf
        current_page_estimate = int(
            (st.session_state.current_page / total_pages) * book["total_pages"]
        )
        requests.put(f"{API}/shelf/", json={
            "user_id": user_id,
            "book_id": book["id"],
            "status": "reading",
            "current_page": current_page_estimate,
            "rating": 0
        })

        st.divider()

        # Highlight / save quote section
        st.subheader("💡 Save a Highlight")
        quote = st.text_area("Paste a quote from this page")
        note  = st.text_input("Your thought on it (optional)")

        if st.button("💾 Save Highlight"):
            if quote.strip():
                requests.post(f"{API}/highlights/", json={
                    "user_id": user_id,
                    "book_id": book["id"],
                    "quote": quote,
                    "page_number": current_page_estimate,
                    "note": note
                })
                st.success("Highlight saved! ✅")
            else:
                st.warning("Please enter a quote first.")
    else:
        st.info("No Gutenberg text available for this book.")