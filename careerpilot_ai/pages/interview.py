"""Feature 6: AI Mock Interview."""

import streamlit as st
from database import database as db
from ai.gemini import generate_json, GeminiConfigError, GeminiResponseError
from ai.prompts.interview_prompt import build_questions_prompt, build_evaluation_prompt
from ui_helpers import hero, empty_state, back_button


def _reset_interview():
    for key in ["interview_questions", "interview_answers", "interview_result", "interview_role"]:
        st.session_state.pop(key, None)


def render():
    back_button()
    hero("AI Mock Interview", "Practice with role-specific questions and get instant, honest feedback.", "🎤")

    profile = db.get_profile()

    st.markdown('<div class="cp-card">', unsafe_allow_html=True)
    role = st.text_input("Role you're interviewing for",
                          value=profile["career_goal"] if profile else "",
                          placeholder="e.g. Backend Developer")
    col1, col2 = st.columns([1, 1])
    with col1:
        start = st.button("🎤 Start New Interview", use_container_width=True, disabled=not role)
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            _reset_interview()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if start:
        with st.spinner("Preparing your interview questions..."):
            try:
                prompt = build_questions_prompt(role, num_questions=5)
                result = generate_json(prompt)
                _reset_interview()
                st.session_state["interview_questions"] = result.get("questions", [])
                st.session_state["interview_role"] = role
                st.session_state["interview_answers"] = {q["id"]: "" for q in result.get("questions", [])}
            except (GeminiConfigError, GeminiResponseError) as e:
                st.error(str(e))
                return

    questions = st.session_state.get("interview_questions")

    if not questions:
        empty_state("Enter a role and click 'Start New Interview' to begin.", "🎤")
        return

    st.markdown(f"### Interview for: {st.session_state.get('interview_role')}")

    for q in questions:
        st.markdown(f"""
        <div class="cp-chat-bubble-q"><b>Q{q['id']} ({q['type']}):</b> {q['question']}</div>
        """, unsafe_allow_html=True)
        answer = st.text_area(
            f"Your answer to Q{q['id']}", key=f"answer_{q['id']}",
            value=st.session_state["interview_answers"].get(q["id"], ""),
            label_visibility="collapsed", placeholder="Type your answer here...", height=100
        )
        st.session_state["interview_answers"][q["id"]] = answer

    submit = st.button("✅ Submit for Evaluation", use_container_width=True)

    if submit:
        answers = st.session_state["interview_answers"]
        if any(not a.strip() for a in answers.values()):
            st.warning("Please answer all questions before submitting.")
        else:
            with st.spinner("Evaluating your answers..."):
                try:
                    qa_pairs = [
                        {"question": q["question"], "type": q["type"], "answer": answers[q["id"]]}
                        for q in questions
                    ]
                    prompt = build_evaluation_prompt(st.session_state["interview_role"], qa_pairs)
                    result = generate_json(prompt)
                    db.save_interview_session(
                        st.session_state["interview_role"], result.get("overall_score", 0), result
                    )
                    st.session_state["interview_result"] = result
                except (GeminiConfigError, GeminiResponseError) as e:
                    st.error(str(e))
                    return

    result = st.session_state.get("interview_result")
    if result:
        st.markdown("---")
        st.markdown(f"### Overall Score: {result.get('overall_score', '—')} / 10")
        st.progress(min(result.get("overall_score", 0) / 10, 1.0))

        for fb in result.get("per_question_feedback", []):
            st.markdown(f"""
            <div class="cp-card">
                <b>Q{fb['question_id']} — Score: {fb['score']}/10</b>
                <p style="color:#64748B;">{fb['feedback']}</p>
            </div>
            """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="cp-card">', unsafe_allow_html=True)
            st.markdown("#### ✅ Strengths")
            for s in result.get("strengths", []):
                st.write(f"- {s}")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="cp-card">', unsafe_allow_html=True)
            st.markdown("#### 💡 Improvement Suggestions")
            for s in result.get("improvement_suggestions", []):
                st.write(f"- {s}")
            st.markdown('</div>', unsafe_allow_html=True)
