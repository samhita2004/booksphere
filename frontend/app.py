import streamlit as st
from pages import reader, library, discover  # Divya's pages

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
    from pages import home
    home.show()
elif page == "📖 Reader":
    reader.show()
elif page == "📚 Library":
    library.show()
elif page == "🔍 Discover":
    discover.show()
elif page == "💡 Highlights":
    from pages import highlights
    highlights.show()
elif page == "⭐ Reviews":
    from pages import reviews
    reviews.show()
elif page == "🏆 Leaderboard":
    from pages import leaderboard
    leaderboard.show()
elif page == "🎯 Challenges":
    from pages import challenges
    challenges.show()
elif page == "📊 Analytics":
    from pages import analytics
    analytics.show()
elif page == "👥 Groups":
    from pages import group
    group.show()