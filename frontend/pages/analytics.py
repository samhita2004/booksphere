import streamlit as st
import requests

def show():
    st.markdown("""
    <h1 style='font-family:"Playfair Display",serif; font-size:28px;
               color:#e8d5a3; margin-bottom:24px;'>📊 Analytics</h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:14px;
                padding:24px 28px; margin-bottom:20px;'>
        <p style='font-size:14px; color:#b09e78; line-height:1.6;'>
            Track your reading habits, progress, and statistics over time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    user_id = st.number_input("Enter Your User ID", min_value=1, step=1, value=1)

    if st.button("Load Analytics"):
        try:
            res = requests.get(f"http://localhost:8000/users/{user_id}/stats")
            stats = res.json()

            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Books Read", stats.get("books_read", 0), "this month")
            
            with col2:
                st.metric("Pages Read", stats.get("pages_read", 0), "this month")
            
            with col3:
                st.metric("Average Rating", f"{stats.get('avg_rating', 0):.1f}", "★")
            
            with col4:
                st.metric("Reading Streak", f"{stats.get('reading_streak', 0)} days", "🔥")

            st.markdown("<hr style='border-color:#3a3428; margin:28px 0;'>", unsafe_allow_html=True)

            # Favorite genres
            st.markdown("""
            <div style='font-family:"Playfair Display",serif; font-size:17px; color:#e8d5a3; 
                        margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>
                Your Favorite Genres
            </div>
            """, unsafe_allow_html=True)

            genres = stats.get("favorite_genres", [])
            if genres:
                for genre, count in genres:
                    st.markdown(f"""
                    <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:8px;
                                padding:12px 16px; margin-bottom:10px;'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span style='color:#e8d5a3;'>{genre}</span>
                            <span style='color:#c9973a; font-weight:500;'>{count} books</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No genre data yet.")

            st.markdown("<hr style='border-color:#3a3428; margin:28px 0;'>", unsafe_allow_html=True)

            # Reading timeline
            st.markdown("""
            <div style='font-family:"Playfair Display",serif; font-size:17px; color:#e8d5a3; 
                        margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>
                This Month's Reading Activity
            </div>
            """, unsafe_allow_html=True)

            st.bar_chart({
                "Week 1": 8,
                "Week 2": 12,
                "Week 3": 10,
                "Week 4": 15
            })

        except Exception as e:
            st.error(f"Could not load analytics: {str(e)}")