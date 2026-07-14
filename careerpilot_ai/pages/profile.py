"""Feature 1: Student Profile."""

import streamlit as st
from database import database as db
from ui_helpers import hero, empty_state, back_button


def render():
    back_button()
    hero("Student Profile", "Tell us about yourself so CareerPilot AI can personalize everything.", "👤")

    existing = db.get_profile()

    with st.container():
        st.markdown('<div class="cp-card">', unsafe_allow_html=True)
        with st.form("profile_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name", value=existing["name"] if existing else "")
                degree = st.text_input("Degree", value=existing["degree"] if existing else "",
                                        placeholder="e.g. B.Tech Computer Science")
                year = st.selectbox(
                    "Year of Study",
                    ["1st Year", "2nd Year", "3rd Year", "4th Year", "Final Year", "Graduated"],
                    index=(["1st Year", "2nd Year", "3rd Year", "4th Year", "Final Year", "Graduated"]
                           .index(existing["year"]) if existing and existing["year"] in
                           ["1st Year", "2nd Year", "3rd Year", "4th Year", "Final Year", "Graduated"] else 0)
                )
            with col2:
                college = st.text_input("College / University", value=existing["college"] if existing else "")
                career_goal = st.text_input("Career Goal", value=existing["career_goal"] if existing else "",
                                             placeholder="e.g. Become a Machine Learning Engineer")

            skills = st.text_area("Current Skills (comma-separated)",
                                   value=existing["skills"] if existing else "",
                                   placeholder="e.g. Python, SQL, Communication, Excel")
            interests = st.text_area("Interests (comma-separated)",
                                      value=existing["interests"] if existing else "",
                                      placeholder="e.g. Artificial Intelligence, Product Design, Finance")

            submitted = st.form_submit_button("💾 Save Profile", use_container_width=True)

            if submitted:
                if not name or not skills or not career_goal:
                    st.error("Please fill in at least your Name, Skills, and Career Goal.")
                else:
                    db.save_profile(name, degree, year, college, skills, interests, career_goal)
                    st.success("Profile saved successfully!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if existing:
        st.markdown("### Profile Summary")
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="cp-card"><b>Name</b><br>{existing["name"] or "—"}</div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="cp-card"><b>Degree</b><br>{existing["degree"] or "—"} ({existing["year"] or "—"})</div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="cp-card"><b>Goal</b><br>{existing["career_goal"] or "—"}</div>', unsafe_allow_html=True)
    else:
        empty_state("No profile yet — fill in the form above to get started.", "📝")
