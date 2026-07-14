"""Feature 7: Internship Simulation."""

import streamlit as st
from database import database as db
from ai.gemini import generate_json, GeminiConfigError, GeminiResponseError
from ai.prompts.simulation_prompt import build_simulation_prompt, build_simulation_feedback_prompt
from ui_helpers import hero, empty_state, back_button


def render():
    back_button()
    hero("Internship Simulation", "Complete a realistic task and get hiring-manager-style feedback.", "💼")

    profile = db.get_profile()

    st.markdown('<div class="cp-card">', unsafe_allow_html=True)
    role = st.text_input("Simulated Internship Role",
                          value=profile["career_goal"] if profile else "",
                          placeholder="e.g. AI Engineer")
    generate = st.button("💼 Generate Internship Task", use_container_width=True, disabled=not role)
    st.markdown('</div>', unsafe_allow_html=True)

    if generate:
        with st.spinner("Designing a realistic internship task..."):
            try:
                prompt = build_simulation_prompt(role)
                result = generate_json(prompt)
                st.session_state["simulation_task"] = result
                st.session_state["simulation_feedback"] = None
            except (GeminiConfigError, GeminiResponseError) as e:
                st.error(str(e))
                return

    task = st.session_state.get("simulation_task")
    if not task:
        empty_state("Enter a role and click 'Generate Internship Task' to begin.", "💼")
        return

    st.markdown(f"""
    <div class="cp-card">
        <h3>{task.get('task_title', '—')}</h3>
        <p style="color:#64748B;">{task.get('scenario', '—')}</p>
        <p><b>Objectives:</b></p>
        <ul>{"".join(f"<li>{o}</li>" for o in task.get('objectives', []))}</ul>
        <p><b>Deliverables:</b></p>
        <ul>{"".join(f"<li>{d}</li>" for d in task.get('deliverables', []))}</ul>
        <p><b>Evaluation Criteria:</b></p>
        <ul>{"".join(f"<li>{c}</li>" for c in task.get('evaluation_criteria', []))}</ul>
        <p><b>Estimated Duration:</b> {task.get('estimated_duration', '—')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="cp-card">', unsafe_allow_html=True)
    submission = st.text_area(
        "Submit your work (paste a summary, approach, code, or write-up of what you did)",
        height=200, placeholder="Describe how you approached the task and what you produced..."
    )
    evaluate = st.button("📤 Submit for Evaluation", use_container_width=True, disabled=not submission)
    st.markdown('</div>', unsafe_allow_html=True)

    if evaluate:
        with st.spinner("Reviewing your submission..."):
            try:
                prompt = build_simulation_feedback_prompt(role, task.get("task_title", ""), submission)
                feedback = generate_json(prompt)
                db.save_simulation(role, {"task": task, "feedback": feedback})
                st.session_state["simulation_feedback"] = feedback
            except (GeminiConfigError, GeminiResponseError) as e:
                st.error(str(e))
                return

    feedback = st.session_state.get("simulation_feedback")
    if feedback:
        st.markdown("---")
        st.markdown(f"### Score: {feedback.get('score', '—')}/100 — {feedback.get('hiring_recommendation', '—')}")
        st.progress(feedback.get("score", 0) / 100)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="cp-card">', unsafe_allow_html=True)
            st.markdown("#### ✅ Strengths")
            for s in feedback.get("strengths", []):
                st.write(f"- {s}")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="cp-card">', unsafe_allow_html=True)
            st.markdown("#### ⚠️ Gaps")
            for g in feedback.get("gaps", []):
                st.write(f"- {g}")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="cp-card"><b>Overall Feedback:</b><p style="color:#64748B;">{feedback.get("feedback", "—")}</p></div>',
                     unsafe_allow_html=True)
