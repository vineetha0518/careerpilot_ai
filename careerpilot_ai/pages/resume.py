"""Feature 5: Resume Analyzer."""

import streamlit as st
import pdfplumber
import plotly.graph_objects as go
from database import database as db
from ai.gemini import generate_json, GeminiConfigError, GeminiResponseError
from ai.prompts.resume_prompt import build_resume_prompt
from ui_helpers import hero, empty_state, back_button, PRIMARY, SUCCESS, WARNING, DANGER


def _extract_text(uploaded_file) -> str:
    text_parts = []
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def _score_gauge(score: int):
    color = SUCCESS if score >= 70 else (WARNING if score >= 40 else DANGER)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": " / 100", "font": {"size": 34, "color": color}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 40], "color": "#FEE2E2"},
                {"range": [40, 70], "color": "#FEF3C7"},
                {"range": [70, 100], "color": "#DCFCE7"},
            ],
        },
    ))
    fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
    return fig


def render():
    back_button()
    hero("Resume Analyzer", "Get an instant ATS score and actionable feedback on your resume.", "📄")

    profile = db.get_profile()

    st.markdown('<div class="cp-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    target_role = st.text_input("Target Role (optional)",
                                 value=profile["career_goal"] if profile else "",
                                 placeholder="e.g. Frontend Developer")
    analyze = st.button("📄 Analyze Resume", use_container_width=True, disabled=uploaded_file is None)
    st.markdown('</div>', unsafe_allow_html=True)

    if analyze and uploaded_file:
        with st.spinner("Extracting text and evaluating with AI..."):
            try:
                resume_text = _extract_text(uploaded_file)
                if not resume_text.strip():
                    st.error("Could not extract any text from this PDF. Try a text-based (non-scanned) PDF.")
                    return
                prompt = build_resume_prompt(resume_text, target_role)
                result = generate_json(prompt)
                db.save_resume_analysis(uploaded_file.name, result.get("ats_score", 0), result)
                st.session_state["resume_result"] = result
            except (GeminiConfigError, GeminiResponseError) as e:
                st.error(str(e))
                return

    result = st.session_state.get("resume_result")
    if not result:
        latest = db.get_latest_resume_analysis()
        if latest:
            import json
            result = json.loads(latest["result_json"])

    if not result:
        empty_state("Upload a PDF resume and click 'Analyze Resume' to get your ATS score.", "📄")
        return

    col1, col2 = st.columns([1, 1.6])
    with col1:
        st.markdown('<div class="cp-card">', unsafe_allow_html=True)
        st.markdown("#### ATS Score")
        st.plotly_chart(_score_gauge(result.get("ats_score", 0)), use_container_width=True,
                         config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="cp-card">', unsafe_allow_html=True)
        st.markdown("#### ✅ Strengths")
        for s in result.get("strengths", []):
            st.write(f"- {s}")
        st.markdown("#### ⚠️ Weaknesses")
        for w in result.get("weaknesses", []):
            st.write(f"- {w}")
        st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="cp-card">', unsafe_allow_html=True)
        st.markdown("#### 🔑 Missing Keywords")
        for k in result.get("missing_keywords", []):
            st.write(f"- {k}")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="cp-card">', unsafe_allow_html=True)
        st.markdown("#### 💡 Suggestions")
        for sug in result.get("suggestions", []):
            st.write(f"- {sug}")
        st.markdown('</div>', unsafe_allow_html=True)
