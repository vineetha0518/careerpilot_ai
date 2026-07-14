"""Authentication: Login screen."""

import streamlit as st

from auth.auth import authenticate_user, is_valid_email
from ui_helpers import auth_header


def render() -> None:
    auth_header(
        title="Welcome back",
        subtitle="Sign in to continue to CareerPilot AI",
        emoji="🚀",
    )

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Login")

    if submitted:
        if not email or not password:
            st.error("Please enter both your email and password.")
        elif not is_valid_email(email):
            st.error("Please enter a valid email address.")
        else:
            user = authenticate_user(email, password)
            if user:
                st.session_state["authenticated"] = True
                st.session_state["user"] = {
                    "id": user["id"],
                    "full_name": user["full_name"],
                    "email": user["email"],
                }
                st.session_state["current_page"] = "🏠 Dashboard"
                st.session_state["nav_history"] = []
                st.success(f"Welcome back, {user['full_name'].split(' ')[0]}! Redirecting to your dashboard…")
                st.rerun()
            else:
                st.error("Invalid email or password. Please try again.")

    st.markdown('<div class="cp-auth-switch">Don\'t have an account yet?</div>', unsafe_allow_html=True)
    st.markdown('<div class="cp-secondary-btn">', unsafe_allow_html=True)
    if st.button("Create Account", key="go_signup"):
        st.session_state["auth_view"] = "signup"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
