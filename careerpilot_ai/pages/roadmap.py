"""Feature 4: Learning Roadmap."""

import streamlit as st
from database import database as db
from ai.gemini import generate_json, GeminiConfigError, GeminiResponseError
from ai.prompts.roadmap_prompt import build_roadmap_prompt
from ui_helpers import hero, pill_list, empty_state, back_button


def render():
    back_button()
    hero("Learning Roadmap", "Your personalized 8-week plan to close the gap and get job-ready.", "🗺")

    profile = db.get_profile()
    if not profile:
        empty_state("Please complete your Student Profile first.", "👤")
        return

    skill_gap = db.get_latest_skill_gap()
    default_target = skill_gap["target_career"] if skill_gap else profile["career_goal"]
    missing_skills_text = ", ".join(
        s["skill"] for s in skill_gap["missing_skills"]
    ) if skill_gap else "Not analyzed yet"

    st.markdown('<div class="cp-card">', unsafe_allow_html=True)
    target_career = st.text_input("Target Career", value=default_target or "")
    st.caption(f"Known skill gaps: {missing_skills_text}")
    generate = st.button("🗺 Generate 8-Week Roadmap", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if generate and target_career:
        with st.spinner("Designing your personalized learning path..."):
            try:
                prompt = build_roadmap_prompt(target_career, profile["skills"], missing_skills_text)
                result = generate_json(prompt)
                db.save_roadmap(target_career, result)
                st.session_state["roadmap_result"] = result
            except (GeminiConfigError, GeminiResponseError) as e:
                st.error(str(e))
                return

    result = st.session_state.get("roadmap_result") or db.get_latest_roadmap()

    if not result:
        empty_state("Click 'Generate 8-Week Roadmap' to build your learning timeline.", "🗺")
        return

    st.markdown(f"### 8-Week Roadmap: {result.get('target_career', '—')}")

    for week in result.get("weeks", []):
        st.markdown(f"""
        <div class="cp-timeline-week">
            <div class="cp-card" style="margin-bottom:0;">
                <h3>Week {week['week_number']}: {week['title']}</h3>
                <p><b>Topics:</b><br>{pill_list(week.get('topics', []))}</p>
                <p><b>Mini Project:</b> {week.get('mini_project', '—')}</p>
                <p><b>Resources:</b><br>{pill_list(week.get('resources', []))}</p>
                <p style="color:#16A34A;"><b>Expected Outcome:</b> {week.get('expected_outcome', '—')}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
