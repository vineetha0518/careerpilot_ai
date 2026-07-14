"""
app.py
------
CareerPilot AI — main entry point.

Sets up page config, initializes the SQLite database (app data + users),
and routes between:
  1. The auth flow (Login / Sign Up) when nobody is logged in, and
  2. The authenticated app shell (sidebar nav + feature pages) once a
     user has signed in.

Session state is the single source of truth for "who is logged in" and
"which page is currently shown", so refreshes within a run keep working
without relying on browser history.
"""

import os
import streamlit as st

from database.database import init_db
from auth.auth import init_auth_db
from ui_helpers import inject_global_css, inject_auth_css, sidebar_user_block

from pages import dashboard, career, skill_gap, roadmap, resume, interview, simulation, profile
from pages import login as login_page
from pages import signup as signup_page

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()
init_auth_db()

# ---------------------------------------------------------------------
# Session defaults
# ---------------------------------------------------------------------
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("user", None)
st.session_state.setdefault("auth_view", "login")           # "login" | "signup"
st.session_state.setdefault("current_page", "🏠 Dashboard")
st.session_state.setdefault("nav_history", [])
st.session_state.setdefault("nav_widget_version", 0)
st.session_state.setdefault("just_logged_out", False)

NAV_ITEMS = {
    "🏠 Dashboard": dashboard,
    "🎯 Career Recommendation": career,
    "📊 Skill Gap Analysis": skill_gap,
    "🗺 Learning Roadmap": roadmap,
    "📄 Resume Analyzer": resume,
    "🎤 AI Mock Interview": interview,
    "💼 Internship Simulation": simulation,
    "👤 Profile": profile,
}


def _logout() -> None:
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["current_page"] = "🏠 Dashboard"
    st.session_state["nav_history"] = []
    st.session_state["nav_widget_version"] = 0
    st.session_state["auth_view"] = "login"
    st.session_state["just_logged_out"] = True
    st.rerun()


# ---------------------------------------------------------------------
# Unauthenticated: Login / Sign Up
# ---------------------------------------------------------------------
if not st.session_state["authenticated"]:
    inject_auth_css()

    if st.session_state.get("just_logged_out"):
        st.success("Successfully logged out.")
        st.session_state["just_logged_out"] = False

    if st.session_state["auth_view"] == "signup":
        signup_page.render()
    else:
        login_page.render()

# ---------------------------------------------------------------------
# Authenticated: app shell
# ---------------------------------------------------------------------
else:
    inject_global_css()

    with st.sidebar:
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo.png")
        col_a, col_b, col_c = st.columns([1, 1.4, 1])
        with col_b:
            if os.path.exists(logo_path):
                st.image(logo_path, width=72)

        st.markdown("""
        <div class="cp-sidebar-brand">
            <div class="name">CareerPilot AI</div>
            <div class="tagline">Your AI Career Co-Pilot</div>
        </div>
        """, unsafe_allow_html=True)

        sidebar_user_block(st.session_state["user"])

        nav_labels = list(NAV_ITEMS.keys())
        current_page = st.session_state["current_page"]
        default_index = nav_labels.index(current_page) if current_page in nav_labels else 0
        widget_key = f"nav_radio_{st.session_state['nav_widget_version']}"

        selection = st.radio(
            "Navigation",
            nav_labels,
            index=default_index,
            label_visibility="collapsed",
            key=widget_key,
        )

        if selection != current_page:
            st.session_state["nav_history"].append(current_page)
            st.session_state["current_page"] = selection
            st.rerun()

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            _logout()

        st.caption("Built for national-level hackathons 🏆")
        st.caption("Powered by Google Gemini")

    page_module = NAV_ITEMS[st.session_state["current_page"]]
    page_module.render()
