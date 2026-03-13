import streamlit as st
import requests
 
API = "http://localhost:8000"
 
st.title("⭐ Book Reviews")
st.markdown("---")
 
# ── Section 1: View reviews for a book ───────────────────────────────────────
st.subheader("📖 Read Reviews")
 
book_id = st.number_input("Enter Book ID to see its reviews", min_value=1, step=1, value=1)
 
if st.button("Load Reviews"):
    try:
        res = requests.get(f"{API}/reviews/book/{book_id}")
        reviews = res.json()
 
        if not reviews:
            st.info("No reviews yet for this book. Be the first to write one!")
        else:
            for r in reviews:
                with st.container():
                    stars = "⭐" * r["rating"]
                    st.markdown(f"**User #{r['user_id']}** — {stars}")
                    st.write(r["review_text"])
 
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        # Like button for each review
                        if st.button(f"👍 Helpful ({r['helpful_votes']})", key=f"like_{r['id']}"):
                            like_res = requests.post(f"{API}/reviews/{r['id']}/like")
                            if like_res.status_code == 200:
                                st.success("Marked as helpful!")
                                st.rerun()
                    with col2:
                        st.caption(f"Posted on {r['created_at'][:10]}")
 
                    st.markdown("---")
 
    except Exception:
        st.error("Could not connect to server. Is the backend running?")
 
# ── Section 2: Write a new review ─────────────────────────────────────────────
st.subheader("✍️ Write a Review")
 
with st.form("review_form"):
    user_id     = st.number_input("Your User ID", min_value=1, step=1)
    review_book = st.number_input("Book ID you're reviewing", min_value=1, step=1)
    rating      = st.slider("Rating", min_value=1, max_value=5, value=3)
    review_text = st.text_area("Your Review", placeholder="Write your thoughts about the book...")
    submitted   = st.form_submit_button("Submit Review")
 
if submitted:
    if not review_text.strip():
        st.error("Please write something in your review")
    else:
        try:
            res = requests.post(f"{API}/reviews/", json={
                "user_id": user_id,
                "book_id": review_book,
                "rating": rating,
                "review_text": review_text
            })
            if res.status_code == 200:
                st.success("Review submitted successfully! 🎉")
                st.rerun()
            else:
                st.error(res.json().get("detail", "Could not submit review"))
        except Exception:
            st.error("Could not connect to server. Is the backend running?")