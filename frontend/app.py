import streamlit as st
from pages import reader, library, discover  # Divya's pages

st.set_page_config(
    page_title="BookSphere",
    page_icon="📚",
    layout="wide"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500&display=swap');
 
:root {
    --bg:      #0f0e0c;
    --bg2:     #1c1a15;
    --bg3:     #2a2720;
    --text:    #e8d5a3;
    --text2:   #b09e78;
    --text3:   #6e5f44;
    --gold:    #c9973a;
    --gold-lt: #e8c46a;
    --border:  #3a3428;
}
 
/* ── global background & text ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0f0e0c !important;
    color: #e8d5a3 !important;
    font-family: 'DM Sans', sans-serif !important;
}
 
[data-testid="stSidebar"] {
    background-color: #1c1a15 !important;
    border-right: 1px solid #3a3428 !important;
}
 
[data-testid="stSidebar"] * {
    color: #b09e78 !important;
    font-family: 'DM Sans', sans-serif !important;
}
 
/* hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
 
/* sidebar radio buttons */
[data-testid="stSidebar"] .stRadio label {
    color: #b09e78 !important;
    font-size: 14px !important;
    padding: 6px 0 !important;
    cursor: pointer !important;
    transition: color 0.2s !important;
}
 
[data-testid="stSidebar"] .stRadio label:hover {
    color: #c9973a !important;
}
 
/* headings */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #e8d5a3 !important;
}
 
/* all text in main area */
p, li, span, div {
    color: #e8d5a3;
}
 
/* streamlit columns gap fix */
[data-testid="column"] {
    padding: 0 8px !important;
}
 
/* buttons */
.stButton > button {
    background-color: #c9973a !important;
    color: #1a1208 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 8px 20px !important;
    transition: background 0.2s !important;
}
.stButton > button:hover {
    background-color: #e8c46a !important;
}
 
/* selectbox, text inputs */
.stSelectbox > div > div,
.stTextInput > div > div > input {
    background-color: #2a2720 !important;
    color: #e8d5a3 !important;
    border: 1px solid #3a3428 !important;
    border-radius: 6px !important;
}
 
/* tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: #1c1a15 !important;
    border-bottom: 1px solid #3a3428 !important;
    gap: 4px !important;
}
 
.stTabs [data-baseweb="tab"] {
    background-color: #2a2720 !important;
    color: #b09e78 !important;
    border-radius: 20px !important;
    border: 1px solid #4a4235 !important;
    font-size: 13px !important;
    padding: 6px 18px !important;
}
 
.stTabs [aria-selected="true"] {
    background-color: #c9973a !important;
    color: #1a1208 !important;
    border-color: #c9973a !important;
}
 
/* metric cards */
[data-testid="metric-container"] {
    background-color: #1c1a15 !important;
    border: 1px solid #3a3428 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
 
[data-testid="metric-container"] label {
    color: #b09e78 !important;
}
 
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #c9973a !important;
    font-size: 18px !important;
}
 
/* expanders */
.streamlit-expanderHeader {
    background-color: #1c1a15 !important;
    color: #e8d5a3 !important;
    border: 1px solid #3a3428 !important;
    border-radius: 8px !important;
}
 
.streamlit-expanderContent {
    background-color: #2a2720 !important;
    border: 1px solid #3a3428 !important;
}
 
/* dividers */
hr { border-color: #3a3428 !important; }
 
/* info / success / error boxes */
.stAlert {
    background-color: #2a2720 !important;
    border-radius: 8px !important;
    border: 1px solid #3a3428 !important;
    color: #e8d5a3 !important;
}
</style>
""", unsafe_allow_html=True)

COVER_COLORS = [
    "linear-gradient(145deg,#1a2a4a,#2d4a7a)",
    "linear-gradient(145deg,#4a1a00,#8b3a00)",
    "linear-gradient(145deg,#0d2a1a,#1a4a2e)",
    "linear-gradient(145deg,#2a0a4a,#52186e)",
    "linear-gradient(145deg,#4a2000,#7a3a10)",
    "linear-gradient(145deg,#001a2a,#003a5a)",
    "linear-gradient(145deg,#2a1a00,#5a3a00)",
    "linear-gradient(145deg,#0a2a1a,#1a5a38)",
]

 
def book_card(title, author, color_index=0, width=130, height=185):
    bg = COVER_COLORS[color_index % len(COVER_COLORS)]
    return f"""
    <div style='
        display:inline-block; width:{width}px; cursor:pointer;
        transition:transform 0.2s; vertical-align:top; margin-right:14px;
    '>
        <div style='
            width:{width}px; height:{height}px;
            background:{bg}; border-radius:6px;
            box-shadow:4px 6px 18px rgba(0,0,0,0.65);
            display:flex; align-items:flex-end; padding:10px;
            position:relative; overflow:hidden; margin-bottom:8px;
        '>
            <div style='
                position:absolute; left:0; top:0; bottom:0; width:8px;
                background:rgba(0,0,0,0.3); border-radius:6px 0 0 6px;
            '></div>
            <span style='
                font-family:"Playfair Display",serif;
                font-size:10px; font-weight:600; color:white;
                text-shadow:0 1px 6px rgba(0,0,0,0.9);
                line-height:1.3; position:relative; z-index:1;
            '>{title}</span>
        </div>
        <div style='font-size:11px; font-weight:500; color:#e8d5a3; line-height:1.3; margin-bottom:2px;'>{title}</div>
        <div style='font-size:10px; color:#6e5f44;'>{author}</div>
    </div>
    """
 
def books_row(books):
    """books = list of (title, author, color_index)"""
    html = "<div style='display:flex; overflow-x:auto; padding-bottom:8px; gap:0px; margin-bottom:32px;'>"
    for i, (title, author, ci) in enumerate(books):
        html += book_card(title, author, ci)
    html += "</div>"
    return html
 
def section_title(text, subtitle=""):
    sub = f"<span style='font-family:DM Sans,sans-serif; font-size:12px; color:#6e5f44; margin-left:10px; font-weight:400;'>{subtitle}</span>" if subtitle else ""
    return f"""
    <div style='font-family:"Playfair Display",serif; font-size:20px; font-weight:600;
                color:#e8d5a3; margin:28px 0 14px 0;'>
        {text}{sub}
    </div>
    """

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
    "👤 Register",   
    "👥 Users", 
    "🎭 Genres",       
    "✍️ Authors",      
    "📚 My Shelf",     
])

if page == "🏠 Home":
    try:
        from pages import home
        home.show()
    except AttributeError:
        st.title("🏠 Home")
        st.info("Home page coming soon.")
elif page == "📖 Reader":
    reader.show()
elif page == "📚 Library":
    library.show()
elif page == "🔍 Discover":
    discover.show()
#elif page == "💡 Highlights":
#   from pages import highlights
#  highlights.show()
#elif page == "🏆 Leaderboard":
#    from pages import leaderboard
#    leaderboard.show()
elif page == "🎯 Challenges":
    from pages import challenges
    challenges.show()
elif page == "📊 Analytics":
    from pages import analytics
    analytics.show()
elif page == "👥 Groups":
    from pages import group
    group.show()

elif page == "👤 Register":
    st.title("👤 Create an Account")
    with st.form("register_form"):
        username = st.text_input("Username")
        email    = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")
    if submitted:
        import requests
        try:
            res = requests.post("http://localhost:8000/users/register", json={
                "username": username, "email": email, "password": password
            })
            if res.status_code == 200:
                st.success(f"Welcome, {username}!")
            else:
                st.error(res.json().get("detail", "Registration failed"))
        except Exception:
            st.error("Could not connect to server.")

elif page == "👥 Users":
    st.title("👥 All Users")
    import requests
    try:
        res = requests.get("http://localhost:8000/users/")
        for u in res.json():
            st.write(f"**{u['username']}** — {u['email']}")
    except Exception:
        st.error("Could not connect to server.")
elif page == "🎭 Genres":
 
    st.markdown("""
    <h1 style='font-family:"Playfair Display",serif; font-size:28px;
               color:#e8d5a3; margin-bottom:24px;'>Genres</h1>
    """, unsafe_allow_html=True)
 
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Mystery", "🌹 Romance", "✨ Fantasy", "🔪 Crime"])
 
    # ── MYSTERY ──
    with tab1:
        st.markdown("""
        <div style='background:#0d1520; border-radius:14px; padding:32px 36px;
                    margin:16px 0 28px 0; position:relative; overflow:hidden;'>
            <div style='position:absolute; right:36px; top:50%; transform:translateY(-50%);
                        font-size:80px; opacity:0.15;'>🔍</div>
            <h2 style='font-family:"Playfair Display",serif; font-size:30px;
                       color:#c8d8f0; margin-bottom:8px;'>Mystery</h2>
            <p style='font-size:13px; color:#a0b8d0; line-height:1.6; max-width:400px;'>
                Riddles, red herrings, and reveals. Every clue leads you deeper into the dark.
            </p>
        </div>
        """, unsafe_allow_html=True)
 
        st.markdown("<div style='font-family:\"Playfair Display\",serif; font-size:16px; color:#e8d5a3; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>Top picks</div>", unsafe_allow_html=True)
 
        mystery_books = [
            ("The Thursday Murder Club", "Richard Osman", 0),
            ("Magpie Murders", "Anthony Horowitz", 5),
            ("In the Woods", "Tana French", 2),
            ("The Silent Patient", "Alex Michaelides", 3),
            ("And Then There Were None", "Agatha Christie", 6),
            ("The No. 1 Ladies' Detective", "Alexander McCall Smith", 7),
        ]
        cols = st.columns(6)
        for i, (title, author, ci) in enumerate(mystery_books):
            with cols[i]:
                st.markdown(book_card(title, author, ci, width=120, height=170), unsafe_allow_html=True)
 
        st.markdown("<br><div style='font-family:\"Playfair Display\",serif; font-size:16px; color:#e8d5a3; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>Notable authors</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        for col, (name, books) in zip([c1,c2,c3,c4], [
            ("Agatha Christie", "66 detective novels"),
            ("Tana French", "Dublin Murder Squad series"),
            ("Richard Osman", "Thursday Murder Club series"),
            ("Anthony Horowitz", "Hawthorne series, Magpie Murders"),
        ]):
            col.markdown(f"""
            <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:10px; padding:14px 16px; cursor:pointer;'>
                <div style='font-size:14px; font-weight:500; color:#e8d5a3; margin-bottom:4px;'>{name}</div>
                <div style='font-size:12px; color:#6e5f44;'>{books}</div>
            </div>
            """, unsafe_allow_html=True)
 
    # ── ROMANCE ──
    with tab2:
        st.markdown("""
        <div style='background:#20090f; border-radius:14px; padding:32px 36px;
                    margin:16px 0 28px 0; position:relative; overflow:hidden;'>
            <div style='position:absolute; right:36px; top:50%; transform:translateY(-50%);
                        font-size:80px; opacity:0.15;'>🌹</div>
            <h2 style='font-family:"Playfair Display",serif; font-size:30px;
                       color:#f0c8d8; margin-bottom:8px;'>Romance</h2>
            <p style='font-size:13px; color:#d0a0b8; line-height:1.6; max-width:400px;'>
                Slow burns, second chances, enemies to lovers — stories that make your heart race.
            </p>
        </div>
        """, unsafe_allow_html=True)
 
        st.markdown("<div style='font-family:\"Playfair Display\",serif; font-size:16px; color:#e8d5a3; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>Top picks</div>", unsafe_allow_html=True)
 
        romance_books = [
            ("Beach Read", "Emily Henry", 1),
            ("People We Meet on Vacation", "Emily Henry", 4),
            ("The Hating Game", "Sally Thorne", 2),
            ("It Ends with Us", "Colleen Hoover", 1),
            ("The Kiss Quotient", "Helen Hoang", 3),
            ("Normal People", "Sally Rooney", 5),
        ]
        cols = st.columns(6)
        for i, (title, author, ci) in enumerate(romance_books):
            with cols[i]:
                st.markdown(book_card(title, author, ci, width=120, height=170), unsafe_allow_html=True)
 
        st.markdown("<br><div style='font-family:\"Playfair Display\",serif; font-size:16px; color:#e8d5a3; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>Notable authors</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        for col, (name, books) in zip([c1,c2,c3,c4], [
            ("Emily Henry", "Beach Read, Funny Story"),
            ("Colleen Hoover", "It Ends with Us, Verity"),
            ("Sally Rooney", "Normal People, Intermezzo"),
            ("Helen Hoang", "The Kiss Quotient series"),
        ]):
            col.markdown(f"""
            <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:10px; padding:14px 16px;'>
                <div style='font-size:14px; font-weight:500; color:#e8d5a3; margin-bottom:4px;'>{name}</div>
                <div style='font-size:12px; color:#6e5f44;'>{books}</div>
            </div>
            """, unsafe_allow_html=True)
 
    # ── FANTASY ──
    with tab3:
        st.markdown("""
        <div style='background:#130d20; border-radius:14px; padding:32px 36px;
                    margin:16px 0 28px 0; position:relative; overflow:hidden;'>
            <div style='position:absolute; right:36px; top:50%; transform:translateY(-50%);
                        font-size:80px; opacity:0.15;'>✨</div>
            <h2 style='font-family:"Playfair Display",serif; font-size:30px;
                       color:#d8c8f0; margin-bottom:8px;'>Fantasy</h2>
            <p style='font-size:13px; color:#b0a0d0; line-height:1.6; max-width:400px;'>
                Worlds that don't exist but feel more real than our own. Magic, myth, epic battles.
            </p>
        </div>
        """, unsafe_allow_html=True)
 
        st.markdown("<div style='font-family:\"Playfair Display\",serif; font-size:16px; color:#e8d5a3; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>Top picks</div>", unsafe_allow_html=True)
 
        fantasy_books = [
            ("The Name of the Wind", "Patrick Rothfuss", 3),
            ("The Way of Kings", "Brandon Sanderson", 0),
            ("Piranesi", "Susanna Clarke", 2),
            ("A Court of Thorns and Roses", "Sarah J. Maas", 4),
            ("Priory of the Orange Tree", "Samantha Shannon", 1),
            ("The Hobbit", "J.R.R. Tolkien", 6),
        ]
        cols = st.columns(6)
        for i, (title, author, ci) in enumerate(fantasy_books):
            with cols[i]:
                st.markdown(book_card(title, author, ci, width=120, height=170), unsafe_allow_html=True)
 
        st.markdown("<br><div style='font-family:\"Playfair Display\",serif; font-size:16px; color:#e8d5a3; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>Notable authors</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        for col, (name, books) in zip([c1,c2,c3,c4], [
            ("Brandon Sanderson", "Stormlight Archive, Mistborn"),
            ("Patrick Rothfuss", "Kingkiller Chronicle"),
            ("Susanna Clarke", "Piranesi, Jonathan Strange"),
            ("Sarah J. Maas", "ACOTAR, Throne of Glass"),
        ]):
            col.markdown(f"""
            <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:10px; padding:14px 16px;'>
                <div style='font-size:14px; font-weight:500; color:#e8d5a3; margin-bottom:4px;'>{name}</div>
                <div style='font-size:12px; color:#6e5f44;'>{books}</div>
            </div>
            """, unsafe_allow_html=True)
 
    # ── CRIME ──
    with tab4:
        st.markdown("""
        <div style='background:#201408; border-radius:14px; padding:32px 36px;
                    margin:16px 0 28px 0; position:relative; overflow:hidden;'>
            <div style='position:absolute; right:36px; top:50%; transform:translateY(-50%);
                        font-size:80px; opacity:0.15;'>🔪</div>
            <h2 style='font-family:"Playfair Display",serif; font-size:30px;
                       color:#f0d8a8; margin-bottom:8px;'>Crime</h2>
            <p style='font-size:13px; color:#c0a870; line-height:1.6; max-width:400px;'>
                Heists, investigations, and moral ambiguity. Stories that keep you reading past midnight.
            </p>
        </div>
        """, unsafe_allow_html=True)
 
        st.markdown("<div style='font-family:\"Playfair Display\",serif; font-size:16px; color:#e8d5a3; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>Top picks</div>", unsafe_allow_html=True)
 
        crime_books = [
            ("Gone Girl", "Gillian Flynn", 4),
            ("The Girl with the Dragon Tattoo", "Stieg Larsson", 1),
            ("Big Little Lies", "Liane Moriarty", 2),
            ("Verity", "Colleen Hoover", 5),
            ("The Couple Next Door", "Shari Lapena", 6),
            ("The Woman in the Window", "A.J. Finn", 7),
        ]
        cols = st.columns(6)
        for i, (title, author, ci) in enumerate(crime_books):
            with cols[i]:
                st.markdown(book_card(title, author, ci, width=120, height=170), unsafe_allow_html=True)
 
        st.markdown("<br><div style='font-family:\"Playfair Display\",serif; font-size:16px; color:#e8d5a3; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>Notable authors</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        for col, (name, books) in zip([c1,c2,c3,c4], [
            ("Gillian Flynn", "Gone Girl, Sharp Objects"),
            ("Liane Moriarty", "Big Little Lies, Nine Perfect Strangers"),
            ("Stieg Larsson", "Millennium series"),
            ("Shari Lapena", "The Couple Next Door"),
        ]):
            col.markdown(f"""
            <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:10px; padding:14px 16px;'>
                <div style='font-size:14px; font-weight:500; color:#e8d5a3; margin-bottom:4px;'>{name}</div>
                <div style='font-size:12px; color:#6e5f44;'>{books}</div>
            </div>
            """, unsafe_allow_html=True)

elif page == "✍️ Authors":
 
    st.markdown("""
    <h1 style='font-family:"Playfair Display",serif; font-size:28px;
               color:#e8d5a3; margin-bottom:24px;'>Authors</h1>
    """, unsafe_allow_html=True)
 
    authors = [
        {
            "name": "Matt Haig",
            "meta": "British · Fiction & Non-fiction · Born 1975",
            "note": "Writes about mental health, hope, and the human experience. His work has helped millions feel less alone.",
            "books": ["The Midnight Library", "Reasons to Stay Alive", "The Humans", "Notes on a Nervous Planet"],
            "bio": "Sunday Times and New York Times bestselling author. The Midnight Library was translated into over 40 languages and adapted for Netflix. He lives in Edinburgh, Scotland."
        },
        {
            "name": "Min Jin Lee",
            "meta": "Korean-American · Literary Fiction · Born 1968",
            "note": "Writes sweeping multigenerational sagas exploring identity, diaspora, and family sacrifice across generations.",
            "books": ["Pachinko", "Free Food for Millionaires"],
            "bio": "Pachinko was a finalist for the National Book Award — considered one of the most important works of fiction about the Korean diaspora in Japan. Currently a Writer in Residence at Amherst College."
        },
        {
            "name": "Gabrielle Zevin",
            "meta": "American · Literary Fiction · Born 1977",
            "note": "Crafts intricate love stories set against unexpected backdrops — from the afterlife to the video game industry.",
            "books": ["Tomorrow, and Tomorrow", "Elsewhere", "The Storied Life of A.J. Fikry"],
            "bio": "Tomorrow, and Tomorrow, and Tomorrow spent over 80 weeks on the New York Times bestseller list and was longlisted for the Booker Prize. Also a screenwriter."
        },
    ]
 
    for author in authors:
        st.markdown(f"""
        <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:14px;
                    padding:28px; margin-bottom:20px;'>
            <div style='display:flex; gap:20px; align-items:flex-start; margin-bottom:16px;'>
                <div style='width:80px; height:80px; background:#2a2720; border:1px solid #4a4235;
                            border-radius:8px; display:flex; align-items:center; justify-content:center;
                            font-size:28px; flex-shrink:0;'>👤</div>
                <div style='flex:1;'>
                    <div style='font-family:"Playfair Display",serif; font-size:21px; font-weight:700;
                                color:#e8d5a3; margin-bottom:4px;'>{author["name"]}</div>
                    <div style='font-size:12px; color:#6e5f44; margin-bottom:10px;'>{author["meta"]}</div>
                    <div style='font-size:13px; color:#b09e78; line-height:1.6; margin-bottom:12px;'>{author["note"]}</div>
                    <div>{"".join([f"<span style='display:inline-block; background:#2a2720; border:1px solid #4a4235; border-radius:5px; padding:4px 12px; font-size:12px; color:#b09e78; margin:3px 3px 3px 0; cursor:pointer;'>{b}</span>" for b in author["books"]])}</div>
                </div>
            </div>
            <div style='background:#2a2720; border-left:3px solid #c9973a;
                        border-radius:0 8px 8px 0; padding:14px 18px;
                        font-size:13px; line-height:1.7; color:#b09e78;'>
                {author["bio"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
 
 
# ══════════════════════════════════════════════════════════════════════════════
# MY SHELF PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📚 My Shelf":
 
    st.markdown("""
    <h1 style='font-family:"Playfair Display",serif; font-size:28px;
               color:#e8d5a3; margin-bottom:24px;'>My Shelf</h1>
    """, unsafe_allow_html=True)
 
    def shelf_section(title, books_with_progress=None):
        st.markdown(f"""
        <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:14px;
                    padding:24px 28px; margin-bottom:20px;'>
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;'>
                <div style='font-family:"Playfair Display",serif; font-size:17px;
                            font-weight:600; color:#e8d5a3;'>{title}</div>
                <span style='font-size:12px; color:#c9973a; cursor:pointer;'>See all →</span>
            </div>
        """, unsafe_allow_html=True)
 
        if books_with_progress:
            cols = st.columns(len(books_with_progress))
            for col, (t, a, ci, pct) in zip(cols, books_with_progress):
                with col:
                    bg = COVER_COLORS[ci % len(COVER_COLORS)]
                    progress_bar = f"""
                    <div style='width:100%; height:3px; background:#2a2720; border-radius:2px; margin-top:5px;'>
                        <div style='width:{pct}%; height:100%; background:#c9973a; border-radius:2px;'></div>
                    </div>
                    <div style='font-size:10px; color:#6e5f44; margin-top:3px;'>{pct}%</div>
                    """ if pct is not None else ""
                    st.markdown(f"""
                    <div style='cursor:pointer; transition:transform 0.2s;'>
                        <div style='width:100%; aspect-ratio:2/3; background:{bg}; border-radius:7px;
                                    box-shadow:3px 4px 14px rgba(0,0,0,0.5);
                                    display:flex; align-items:flex-end; padding:10px;
                                    position:relative; overflow:hidden; margin-bottom:7px;'>
                            <div style='position:absolute; left:0; top:0; bottom:0; width:7px;
                                        background:rgba(0,0,0,0.25); border-radius:7px 0 0 7px;'></div>
                            <span style='font-family:"Playfair Display",serif; font-size:9px; font-weight:600;
                                         color:white; text-shadow:0 1px 5px rgba(0,0,0,0.9);
                                         position:relative; z-index:1; line-height:1.3;'>{t}</span>
                        </div>
                        <div style='font-size:11px; font-weight:500; color:#e8d5a3; line-height:1.3; margin-bottom:2px;'>{t}</div>
                        <div style='font-size:10px; color:#6e5f44;'>{a}</div>
                        {progress_bar}
                    </div>
                    """, unsafe_allow_html=True)
 
        st.markdown("</div>", unsafe_allow_html=True)
 
    shelf_section("Continue Reading", [
        ("Pachinko",               "Min Jin Lee",    1, 62),
        ("Tomorrow, and Tomorrow", "Gabrielle Zevin", 3, 28),
        ("A Gentleman in Moscow",  "Amor Towles",    5, 85),
        ("The Midnight Library",   "Matt Haig",      0, 10),
        ("Piranesi",               "Susanna Clarke", 2, 45),
    ])
 
    shelf_section("Read Again — Jump Back In", [
        ("The Hitchhiker's Guide", "Douglas Adams",   6, None),
        ("Normal People",          "Sally Rooney",    5, None),
        ("Trust",                  "Hernan Diaz",     7, None),
        ("James",                  "Percival Everett",0, None),
        ("Gone Girl",              "Gillian Flynn",   4, None),
    ])
 
    shelf_section("Read Later", [
        ("Demon Copperhead",     "Barbara Kingsolver", 5, None),
        ("The Covenant of Water","Abraham Verghese",   6, None),
        ("Cloud Cuckoo Land",    "Anthony Doerr",      7, None),
        ("Anxious People",       "Fredrik Backman",    3, None),
        ("The Way of Kings",     "Brandon Sanderson",  2, None),
    ])
elif page == "⭐ Reviews":
 
    st.markdown("""
    <h1 style='font-family:"Playfair Display",serif; font-size:28px;
               color:#e8d5a3; margin-bottom:24px;'>Reviews</h1>
    """, unsafe_allow_html=True)
 
    st.markdown("""
    <div style='font-family:"Playfair Display",serif; font-size:17px; color:#e8d5a3; margin-bottom:14px;'>
        Read Reviews
    </div>
    """, unsafe_allow_html=True)
 
    book_id = st.number_input("Enter Book ID", min_value=1, step=1, value=1)
 
    if st.button("Load Reviews"):
        try:
            res = requests.get(f"http://localhost:8000/reviews/book/{book_id}")
            reviews = res.json()
            if not reviews:
                st.info("No reviews yet for this book. Be the first!")
            else:
                for r in reviews:
                    stars = "⭐" * r["rating"]
                    st.markdown(f"""
                    <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:10px;
                                padding:16px 18px; margin-bottom:12px;'>
                        <div style='font-size:14px; font-weight:500; color:#e8d5a3; margin-bottom:6px;'>
                            User #{r["user_id"]} — {stars}
                        </div>
                        <div style='font-size:13px; color:#b09e78; line-height:1.6; margin-bottom:8px;'>
                            {r["review_text"]}
                        </div>
                        <div style='font-size:11px; color:#6e5f44;'>
                            {r["created_at"][:10]} · 👍 {r["helpful_votes"]} helpful
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception:
            st.error("Could not connect to server. Is the backend running?")
 
    st.markdown("<hr style='border-color:#3a3428; margin:28px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:"Playfair Display",serif; font-size:17px; color:#e8d5a3; margin-bottom:14px;'>
        Write a Review
    </div>
    """, unsafe_allow_html=True)
 
    with st.form("review_form"):
        col1, col2 = st.columns(2)
        with col1:
            user_id = st.number_input("Your User ID", min_value=1, step=1)
        with col2:
            review_book = st.number_input("Book ID", min_value=1, step=1)
        rating = st.slider("Rating", min_value=1, max_value=5, value=3)
        review_text = st.text_area("Your Review", placeholder="Write your thoughts about the book...")
        submitted = st.form_submit_button("Submit Review")
 
    if submitted:
        if not review_text.strip():
            st.error("Please write something in your review.")
        else:
            try:
                res = requests.post("http://localhost:8000/reviews/", json={
                    "user_id": user_id,
                    "book_id": review_book,
                    "rating": rating,
                    "review_text": review_text
                })
                if res.status_code == 200:
                    st.success("Review submitted! 🎉")
                else:
                    st.error(res.json().get("detail", "Could not submit review"))
            except Exception:
                st.error("Could not connect to server. Is the backend running?")