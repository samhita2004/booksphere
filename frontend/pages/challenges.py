import streamlit as st
import requests
from datetime import datetime, timedelta

def show():
    st.markdown("""
    <h1 style='font-family:"Playfair Display",serif; font-size:28px;
               color:#e8d5a3; margin-bottom:24px;'>🎯 Challenges</h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:14px;
                padding:24px 28px; margin-bottom:20px;'>
        <p style='font-size:14px; color:#b09e78; line-height:1.6;'>
            Take on reading challenges to expand your horizons and connect with other readers.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔥 Active Challenges", "✅ Completed", "🆕 Browse All"])

    # ── ACTIVE CHALLENGES ──
    with tab1:
        st.markdown("""
        <div style='font-family:"Playfair Display",serif; font-size:16px; color:#e8d5a3; 
                    margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>
            Challenges You're Participating In
        </div>
        """, unsafe_allow_html=True)

        try:
            res = requests.get("http://localhost:8000/challenges/active")
            challenges = res.json()
            if not challenges:
                st.info("No active challenges. Join one to get started!")
            else:
                for c in challenges:
                    st.markdown(f"""
                    <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:10px;
                                padding:18px; margin-bottom:14px;'>
                        <div style='font-family:"Playfair Display",serif; font-size:16px; color:#e8d5a3;
                                    margin-bottom:8px;'>{c["name"]}</div>
                        <div style='font-size:12px; color:#b09e78; margin-bottom:10px;'>
                            {c["description"]}
                        </div>
                        <div style='width:100%; height:6px; background:#2a2720; border-radius:3px; margin-bottom:6px;'>
                            <div style='width:{c.get("progress", 0)}%; height:100%; background:#c9973a; border-radius:3px;'></div>
                        </div>
                        <div style='font-size:11px; color:#6e5f44;'>
                            {c.get("progress", 0)}% complete · Ends in 14 days
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not load challenges: {str(e)}")

    # ── COMPLETED ──
    with tab2:
        st.markdown("""
        <div style='font-family:"Playfair Display",serif; font-size:16px; color:#e8d5a3; 
                    margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>
            Challenges You've Completed
        </div>
        """, unsafe_allow_html=True)
        
        st.info("Complete challenges to unlock achievements! 🏆")

    # ── BROWSE ALL ──
    with tab3:
        st.markdown("""
        <div style='font-family:"Playfair Display",serif; font-size:16px; color:#e8d5a3; 
                    margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>
            All Available Challenges
        </div>
        """, unsafe_allow_html=True)

        challenge_categories = [
            {
                "title": "Read 5 Books This Month",
                "description": "Challenge yourself to read 5 books within 30 days.",
                "participants": 234,
                "difficulty": "Medium"
            },
            {
                "title": "Explore 3 New Genres",
                "description": "Step out of your comfort zone and discover new genres.",
                "participants": 156,
                "difficulty": "Easy"
            },
            {
                "title": "50-Page Daily Reading Goal",
                "description": "Read at least 50 pages every single day for a week.",
                "participants": 89,
                "difficulty": "Hard"
            },
            {
                "title": "Diverse Authors Challenge",
                "description": "Read books from authors of different backgrounds and cultures.",
                "participants": 201,
                "difficulty": "Medium"
            },
        ]

        for challenge in challenge_categories:
            st.markdown(f"""
            <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:10px;
                        padding:18px; margin-bottom:14px; cursor:pointer;'>
                <div style='display:flex; justify-content:space-between; align-items:start; margin-bottom:10px;'>
                    <div>
                        <div style='font-family:"Playfair Display",serif; font-size:15px; color:#e8d5a3;
                                    margin-bottom:4px;'>{challenge["title"]}</div>
                        <div style='font-size:12px; color:#b09e78;'>{challenge["description"]}</div>
                    </div>
                    <span style='font-size:11px; color:#6e5f44; background:#2a2720; padding:4px 8px; border-radius:4px;'>
                        {challenge["difficulty"]}
                    </span>
                </div>
                <div style='font-size:11px; color:#6e5f44;'>
                    👥 {challenge["participants"]} participants
                </div>
            </div>
            """, unsafe_allow_html=True)