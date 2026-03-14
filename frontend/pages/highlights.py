import streamlit as st
import requests

def show():
    st.markdown("""
    <h1 style='font-family:"Playfair Display",serif; font-size:28px;
               color:#e8d5a3; margin-bottom:24px;'>💡 Highlights</h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:14px;
                padding:24px 28px; margin-bottom:20px;'>
        <p style='font-size:14px; color:#b09e78; line-height:1.6;'>
            Save and organize your favorite quotes and passages from books you're reading.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # View Highlights
    st.markdown("""
    <div style='font-family:"Playfair Display",serif; font-size:17px; color:#e8d5a3; 
                margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>
        Your Highlights
    </div>
    """, unsafe_allow_html=True)

    book_id = st.number_input("Filter by Book ID (optional)", min_value=0, step=1, value=0)

    if st.button("Load Highlights"):
        try:
            if book_id > 0:
                res = requests.get(f"http://localhost:8000/highlights/book/{book_id}")
            else:
                res = requests.get("http://localhost:8000/highlights/")
            
            highlights = res.json()
            if not highlights:
                st.info("No highlights yet. Add some when you're reading!")
            else:
                for h in highlights:
                    st.markdown(f"""
                    <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:10px;
                                padding:16px 18px; margin-bottom:12px; border-left:3px solid #c9973a;'>
                        <div style='font-size:13px; color:#e8d5a3; line-height:1.6; margin-bottom:8px;
                                    font-style:italic;'>
                            "{h["highlight_text"]}"
                        </div>
                        <div style='font-size:11px; color:#6e5f44;'>
                            Book #{h["book_id"]} · Page {h.get("page_number", "N/A")}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not load highlights: {str(e)}")

    st.markdown("<hr style='border-color:#3a3428; margin:28px 0;'>", unsafe_allow_html=True)

    # Add New Highlight
    st.markdown("""
    <div style='font-family:"Playfair Display",serif; font-size:17px; color:#e8d5a3; 
                margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>
        Save a New Highlight
    </div>
    """, unsafe_allow_html=True)

    with st.form("highlight_form"):
        col1, col2 = st.columns(2)
        with col1:
            user_id = st.number_input("Your User ID", min_value=1, step=1)
        with col2:
            book_id_new = st.number_input("Book ID", min_value=1, step=1)
        
        page_number = st.number_input("Page Number (optional)", min_value=1, step=1, value=1)
        highlight_text = st.text_area("Highlight Text", placeholder="Paste the quote or passage you want to save...")
        submitted = st.form_submit_button("Save Highlight")

    if submitted:
        if not highlight_text.strip():
            st.error("Please enter highlight text.")
        else:
            try:
                res = requests.post("http://localhost:8000/highlights/", json={
                    "user_id": user_id,
                    "book_id": book_id_new,
                    "highlight_text": highlight_text,
                    "page_number": page_number
                })
                if res.status_code == 200:
                    st.success("Highlight saved! 🎉")
                else:
                    st.error(res.json().get("detail", "Could not save highlight"))
            except Exception as e:
                st.error(f"Could not connect to server: {str(e)}")
