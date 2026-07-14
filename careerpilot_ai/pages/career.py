"""Feature 2: Career Recommendation."""

import streamlit as st
from database import database as db
from ai.gemini import generate_json, GeminiConfigError, GeminiResponseError
from ai.prompts.career_prompt import build_career_prompt
from ui_helpers import hero, pill_list, empty_state, back_button


def render():
    back_button()
    hero("Career Recommendation", "AI-matched careers based on your skills, interests, and goals.", "🎯")

    profile = db.get_profile()
    if not profile:
        empty_state("Please complete your Student Profile first.", "👤")
        return

    st.markdown('<div class="cp-card">', unsafe_allow_html=True)
    st.write(f"**Skills:** {profile['skills']}")
    st.write(f"**Interests:** {profile['interests']}")
    st.write(f"**Career Goal:** {profile['career_goal']}")
    generate = st.button("✨ Generate Career Recommendations", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if generate:
        with st.spinner("Analyzing your profile against current market trends..."):
            try:
                prompt = build_career_prompt(
                    profile["name"], profile["degree"], profile["year"],
                    profile["skills"], profile["interests"], profile["career_goal"]
                )
                result = generate_json(prompt)
                db.save_career_recommendation(result)
                st.session_state["career_result"] = result
            except (GeminiConfigError, GeminiResponseError) as e:
                st.error(str(e))
                return

    result = st.session_state.get("career_result") or db.get_latest_career_recommendation()

    if not result:
        empty_state("Click 'Generate Career Recommendations' to see your top 3 career matches.", "🎯")
        return

    st.markdown("### Your Top Career Matches")
    cols = st.columns(3)
    for i, career in enumerate(result.get("careers", [])):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="cp-card">
                <h3>#{i+1} {career['title']}</h3>
                <div style="font-size:26px; font-weight:800; color:#2563EB;">{career['match_percentage']}% match</div>
                <p style="color:#64748B; margin-top:10px;">{career['reason']}</p>
                <p><b>Required Skills:</b><br>{pill_list(career.get('required_skills', []))}</p>
                <p><b>Salary Range:</b> {career.get('salary_range', '—')}</p>
                <p><b>Future Outlook:</b> {career.get('future_opportunities', '—')}</p>
            </div>
            """, unsafe_allow_html=True)
