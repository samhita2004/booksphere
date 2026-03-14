import streamlit as st
import requests

def show():
    st.markdown("""
    <h1 style='font-family:"Playfair Display",serif; font-size:28px;
               color:#e8d5a3; margin-bottom:24px;'>👥 Groups</h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:14px;
                padding:24px 28px; margin-bottom:20px;'>
        <p style='font-size:14px; color:#b09e78; line-height:1.6;'>
            Join book clubs and reading groups to discuss your favorite reads with other book lovers.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📚 My Groups", "🔍 Discover Groups", "➕ Create Group"])

    # ── MY GROUPS ──
    with tab1:
        st.markdown("""
        <div style='font-family:"Playfair Display",serif; font-size:16px; color:#e8d5a3; 
                    margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>
            Groups You're In
        </div>
        """, unsafe_allow_html=True)

        try:
            res = requests.get("http://localhost:8000/groups/my-groups")
            groups = res.json()
            
            if not groups:
                st.info("You're not in any groups yet. Join one to get started!")
            else:
                for group in groups:
                    st.markdown(f"""
                    <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:10px;
                                padding:18px; margin-bottom:14px;'>
                        <div style='display:flex; justify-content:space-between; align-items:start; margin-bottom:10px;'>
                            <div>
                                <div style='font-family:"Playfair Display",serif; font-size:16px; color:#e8d5a3;
                                            margin-bottom:4px;'>{group["name"]}</div>
                                <div style='font-size:12px; color:#b09e78;'>{group["description"]}</div>
                            </div>
                            <button style='background:#c9973a; color:#1a1208; border:none; padding:6px 14px; border-radius:6px; cursor:pointer; font-size:12px;'>
                                View
                            </button>
                        </div>
                        <div style='font-size:11px; color:#6e5f44;'>
                            👥 {group["member_count"]} members · Currently reading: {group["current_book"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not load groups: {str(e)}")

    # ── DISCOVER GROUPS ──
    with tab2:
        st.markdown("""
        <div style='font-family:"Playfair Display",serif; font-size:16px; color:#e8d5a3; 
                    margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>
            Popular Book Clubs
        </div>
        """, unsafe_allow_html=True)

        popular_groups = [
            {
                "name": "Contemporary Fiction Lovers",
                "description": "Discussing modern literature, contemporary authors, and trending books.",
                "members": 342,
                "current_book": "Funny Story by Emily Henry"
            },
            {
                "name": "Fantasy & Sci-Fi Adventures",
                "description": "Exploring epic worlds, magic systems, and futuristic worlds.",
                "members": 287,
                "current_book": "The Way of Kings by Brandon Sanderson"
            },
            {
                "name": "Mystery & Thriller Club",
                "description": "Solving mysteries and debating plot twists with fellow sleuths.",
                "members": 156,
                "current_book": "The Silent Patient by Alex Michaelides"
            },
            {
                "name": "Literary Fiction Society",
                "description": "Deep dives into award-winning literature and classic masterpieces.",
                "members": 198,
                "current_book": "Pachinko by Min Jin Lee"
            },
        ]

        for group in popular_groups:
            st.markdown(f"""
            <div style='background:#1c1a15; border:1px solid #3a3428; border-radius:10px;
                        padding:18px; margin-bottom:14px; cursor:pointer;'>
                <div style='display:flex; justify-content:space-between; align-items:start; margin-bottom:10px;'>
                    <div style='flex:1;'>
                        <div style='font-family:"Playfair Display",serif; font-size:16px; color:#e8d5a3;
                                    margin-bottom:4px;'>{group["name"]}</div>
                        <div style='font-size:12px; color:#b09e78; margin-bottom:8px;'>{group["description"]}</div>
                        <div style='font-size:11px; color:#6e5f44;'>
                            👥 {group["members"]} members
                        </div>
                    </div>
                    <button style='background:#c9973a; color:#1a1208; border:none; padding:8px 16px; border-radius:6px; cursor:pointer; font-size:12px; white-space:nowrap;'>
                        Join Group
                    </button>
                </div>
                <div style='font-size:11px; color:#6e5f44; margin-top:10px; padding-top:10px; border-top:1px solid #3a3428;'>
                    📖 Reading: {group["current_book"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── CREATE GROUP ──
    with tab3:
        st.markdown("""
        <div style='font-family:"Playfair Display",serif; font-size:16px; color:#e8d5a3; 
                    margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid #3a3428;'>
            Start Your Own Group
        </div>
        """, unsafe_allow_html=True)

        with st.form("create_group_form"):
            group_name = st.text_input("Group Name", placeholder="e.g., 'Tech Book Club'")
            description = st.text_area("Description", placeholder="What's your group about?", height=100)
            category = st.selectbox("Category", ["Fiction", "Non-Fiction", "Fantasy", "Mystery", "Romance", "Science", "History", "Self-Help", "Other"])
            is_public = st.checkbox("Make group public", value=True)
            
            submitted = st.form_submit_button("Create Group")

        if submitted:
            if not group_name.strip() or not description.strip():
                st.error("Please fill in all fields.")
            else:
                try:
                    res = requests.post("http://localhost:8000/groups/", json={
                        "name": group_name,
                        "description": description,
                        "category": category,
                        "is_public": is_public
                    })
                    if res.status_code == 200:
                        st.success(f"Group '{group_name}' created successfully! 🎉")
                    else:
                        st.error(res.json().get("detail", "Could not create group"))
                except Exception as e:
                    st.error(f"Could not connect to server: {str(e)}")