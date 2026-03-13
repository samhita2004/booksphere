import streamlit as st
from pages import reader, library, discover, highlights, reviews, leaderboard, challenges, analytics, group, home

st.set_page_config(
    page_title="BookSphere",
    page_icon="📚",
    layout="wide"
)

st.sidebar.title("📚 BookSphere")
st.sidebar.markdown("*Read Together, Grow Together*")
st.sidebar.divider()

page = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "📖 Reader",
    "📚 Library",
    "🔍 Discover",
    "💡 Highlights",
    "⭐ Reviews",
    "🏆 Leaderboard",
    "🎯 Challenges",
    "📊 Analytics",
    "👥 Groups",
])

if page == "🏠 Home":
    home.show()
elif page == "📖 Reader":
    reader.show()
elif page == "📚 Library":
    library.show()
elif page == "🔍 Discover":
    discover.show()
elif page == "💡 Highlights":
    highlights.show()
elif page == "⭐ Reviews":
    reviews.show()
elif page == "🏆 Leaderboard":
    leaderboard.show()
elif page == "🎯 Challenges":
    challenges.show()
elif page == "📊 Analytics":
    analytics.show()
elif page == "👥 Groups":
    group.show()