"""Feature 8: Career Readiness Dashboard (also the app's home page)."""

from datetime import datetime

import streamlit as st
import plotly.graph_objects as go
from database import database as db
from ui_helpers import hero, metric_card, empty_state, PRIMARY


def _gauge(score: int):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "", "font": {"size": 42, "color": PRIMARY}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": PRIMARY},
            "bgcolor": "white",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "#FEE2E2"},
                {"range": [40, 70], "color": "#FEF3C7"},
                {"range": [70, 100], "color": "#DCFCE7"},
            ],
        },
    ))
    fig.update_layout(height=280, margin=dict(l=20, r=20, t=20, b=10), paper_bgcolor="rgba(0,0,0,0)")
    return fig


def render():
    user = st.session_state.get("user") or {}
    display_name = (user.get("full_name") or "there").split(" ")[0]
    today_str = datetime.now().strftime("%A, %d %B %Y")

    hero(f"Welcome back, {display_name} 👋",
         f"📅 {today_str} — here's your career readiness snapshot at a glance.", "🏠")

    profile = db.get_profile()

    # ---- User profile summary ----
    st.markdown('<div class="cp-card">', unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    p1.markdown(f"**👤 Name**  \n{user.get('full_name', '—')}")
    p2.markdown(f"**✉️ Email**  \n{user.get('email', '—')}")
    p3.markdown(f"**🎯 Career Goal**  \n{profile['career_goal'] if profile else '—'}")
    st.markdown('</div>', unsafe_allow_html=True)

    if not profile:
        empty_state("Set up your Student Profile first to unlock personalized insights.", "🚀")
        return

    total_score, breakdown = db.compute_readiness_score()

    col1, col2 = st.columns([1, 1.4])
    with col1:
        st.markdown('<div class="cp-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Career Readiness Score")
        st.plotly_chart(_gauge(total_score), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("#### Score Breakdown")
        b1, b2 = st.columns(2)
        with b1:
            metric_card(f'{breakdown["Resume"]}/20', "Resume")
            metric_card(f'{breakdown["Roadmap"]}/20', "Roadmap")
            metric_card(f'{breakdown["Projects"]}/20', "Projects")
        with b2:
            metric_card(f'{breakdown["Interview"]}/20', "Interview")
            metric_card(f'{breakdown["Skills"]}/20', "Skills")

    st.markdown("---")
    st.markdown("#### Quick Snapshot")

    career = db.get_latest_career_recommendation()
    skill_gap = db.get_latest_skill_gap()
    resume = db.get_latest_resume_analysis()
    interview = db.get_latest_interview_session()

    q1, q2, q3, q4 = st.columns(4)
    with q1:
        st.markdown('<div class="cp-card">', unsafe_allow_html=True)
        st.markdown("**🎯 Top Career Match**")
        if career and career.get("careers"):
            top = career["careers"][0]
            st.write(f"{top['title']} — {top['match_percentage']}%")
        else:
            st.caption("Not generated yet")
        st.markdown('</div>', unsafe_allow_html=True)

    with q2:
        st.markdown('<div class="cp-card">', unsafe_allow_html=True)
        st.markdown("**📊 Skill Readiness**")
        if skill_gap:
            st.write(f"{skill_gap.get('overall_readiness_percentage', '—')}% ready for {skill_gap.get('target_career', '—')}")
        else:
            st.caption("Not generated yet")
        st.markdown('</div>', unsafe_allow_html=True)

    with q3:
        st.markdown('<div class="cp-card">', unsafe_allow_html=True)
        st.markdown("**📄 Resume ATS Score**")
        if resume:
            st.write(f"{resume['ats_score']}/100")
        else:
            st.caption("Not analyzed yet")
        st.markdown('</div>', unsafe_allow_html=True)

    with q4:
        st.markdown('<div class="cp-card">', unsafe_allow_html=True)
        st.markdown("**🎤 Last Interview Score**")
        if interview:
            st.write(f"{interview['avg_score']}/10 as {interview['role']}")
        else:
            st.caption("Not attempted yet")
        st.markdown('</div>', unsafe_allow_html=True)

    st.info("💡 Tip: Complete more features (Resume, Interview, Roadmap, Skill Gap, Simulation) "
            "to raise your Career Readiness Score.")
