import streamlit as st

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

def show():
    # Hero Section
    st.write("""
    <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:16px;
                padding:40px 44px; margin-bottom:36px;'>
        <h1 style='font-family:"Playfair Display",serif; font-size:30px;
                   color:#e8d5a3; margin-bottom:10px;'>
            Your next great read is waiting.
        </h1>
        <p style='font-size:14px; color:#b09e78; max-width:380px; line-height:1.6;'>
            Discover books, track your reading journey, and connect with stories that move you.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("""
    <h2 style='font-family:"Playfair Display",serif; font-size:20px; color:#e8d5a3; 
               margin:28px 0 14px 0;'>Recommendations</h2>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    
    books = [
        ("The Midnight Library", "Matt Haig", 0),
        ("Pachinko", "Min Jin Lee", 2),
        ("Tomorrow, and Tomorrow", "Gabrielle Zevin", 3),
        ("Piranesi", "Susanna Clarke", 1),
        ("A Gentleman in Moscow", "Amor Towles", 5),
    ]
    
    for col, (title, author, color_idx) in zip([col1, col2, col3, col4, col5], books):
        with col:
            bg = COVER_COLORS[color_idx % len(COVER_COLORS)]
            st.write(f"""
            <div style='text-align:center;'>
                <div style='width:100%; height:200px; background:{bg}; border-radius:6px;
                            box-shadow:4px 6px 18px rgba(0,0,0,0.65); display:flex; 
                            align-items:flex-end; justify-content:center; padding:10px;'>
                    <p style='color:white; font-weight:bold; text-align:center;'>{title}</p>
                </div>
                <p style='font-size:11px; color:#e8d5a3; margin-top:8px;'>{title}</p>
                <p style='font-size:10px; color:#6e5f44;'>{author}</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("""
    <hr style='border-color:#3a3428; margin:28px 0;'>
    """, unsafe_allow_html=True)

    st.write("""
    <h2 style='font-family:"Playfair Display",serif; font-size:20px; color:#e8d5a3; 
               margin:28px 0 14px 0;'>Books like your recent reads</h2>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    
    recent = [
        ("The Name of the Wind", "Patrick Rothfuss", 1),
        ("Normal People", "Sally Rooney", 5),
        ("The Hitchhiker's Guide", "Douglas Adams", 6),
        ("Lessons in Chemistry", "Bonnie Garmus", 7),
        ("Cloud Cuckoo Land", "Anthony Doerr", 0),
    ]
    
    for col, (title, author, color_idx) in zip([col1, col2, col3, col4, col5], recent):
        with col:
            bg = COVER_COLORS[color_idx % len(COVER_COLORS)]
            st.write(f"""
            <div style='text-align:center;'>
                <div style='width:100%; height:200px; background:{bg}; border-radius:6px;
                            box-shadow:4px 6px 18px rgba(0,0,0,0.65); display:flex; 
                            align-items:flex-end; justify-content:center; padding:10px;'>
                    <p style='color:white; font-weight:bold; text-align:center;'>{title}</p>
                </div>
                <p style='font-size:11px; color:#e8d5a3; margin-top:8px;'>{title}</p>
                <p style='font-size:10px; color:#6e5f44;'>{author}</p>
            </div>
            """, unsafe_allow_html=True)