"""Feature 3: Skill Gap Analysis."""

import streamlit as st
from database import database as db
from ai.gemini import generate_json, GeminiConfigError, GeminiResponseError
from ai.prompts.skill_gap_prompt import build_skill_gap_prompt
from ui_helpers import hero, priority_badge, empty_state, back_button


def render():
    back_button()
    hero("Skill Gap Analysis", "See exactly what stands between you and your target career.", "📊")

    profile = db.get_profile()
    if not profile:
        empty_state("Please complete your Student Profile first.", "👤")
        return

    career_result = db.get_latest_career_recommendation()
    suggested_targets = [c["title"] for c in career_result["careers"]] if career_result else []

    st.markdown('<div class="cp-card">', unsafe_allow_html=True)
    if suggested_targets:
        target_career = st.selectbox(
            "Target Career",
            suggested_targets + ["Other (type below)"],
        )
        if target_career == "Other (type below)":
            target_career = st.text_input("Enter target career")
    else:
        target_career = st.text_input("Target Career", value=profile["career_goal"] or "")

    analyze = st.button("🔍 Analyze Skill Gap", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if analyze and target_career:
        with st.spinner("Comparing your skills against industry requirements..."):
            try:
                prompt = build_skill_gap_prompt(profile["skills"], target_career)
                result = generate_json(prompt)
                db.save_skill_gap(target_career, result)
                st.session_state["skill_gap_result"] = result
            except (GeminiConfigError, GeminiResponseError) as e:
                st.error(str(e))
                return

    result = st.session_state.get("skill_gap_result") or db.get_latest_skill_gap()

    if not result:
        empty_state("Select a target career and click 'Analyze Skill Gap' to begin.", "📊")
        return

    st.markdown(f"### Gap Analysis for {result.get('target_career', '—')}")
    st.progress(result.get("overall_readiness_percentage", 0) / 100,
                text=f"Overall Readiness: {result.get('overall_readiness_percentage', 0)}%")

    st.markdown("### Missing Skills")
    for skill in result.get("missing_skills", []):
        st.markdown(f"""
        <div class="cp-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3 style="margin:0;">{skill['skill']}</h3>
                {priority_badge(skill.get('priority', 'Medium'))}
            </div>
            <p style="color:#64748B; margin: 8px 0 4px 0;">
                Difficulty: <b>{skill.get('difficulty', '—')}</b> &nbsp;•&nbsp;
                Estimated Time: <b>{skill.get('estimated_learning_time', '—')}</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
