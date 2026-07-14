"""Authentication: Sign Up screen."""

import streamlit as st

from auth.auth import (
    create_user,
    email_exists,
    is_valid_email,
    validate_password_strength,
    PASSWORD_RULES,
)
from ui_helpers import auth_header


def _password_checklist(password: str) -> None:
    """Live-updating list of password requirements (rerenders on every keystroke)."""
    failing = set(validate_password_strength(password))
    rows = []
    for rule_text, _ in PASSWORD_RULES:
        state = "bad" if (not password or rule_text in failing) else "ok"
        mark = "✓" if state == "ok" else "○"
        rows.append(f'<div class="pw-rule {state}">{mark} {rule_text}</div>')
    st.markdown(f'<div class="pw-checklist">{"".join(rows)}</div>', unsafe_allow_html=True)


def render() -> None:
    auth_header(
        title="Create your account",
        subtitle="Start your AI-powered career journey today",
        emoji="✨",
    )

    st.markdown('<div class="cp-glass-block">', unsafe_allow_html=True)

    full_name = st.text_input("Full Name", placeholder="Jane Doe", key="signup_full_name")
    email = st.text_input("Email", placeholder="you@example.com", key="signup_email")
    password = st.text_input("Password", type="password", placeholder="••••••••", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="signup_confirm")

    _password_checklist(password)

    create_clicked = st.button("Create Account", key="do_signup")

    st.markdown('</div>', unsafe_allow_html=True)

    if create_clicked:
        errors = []

        if not full_name.strip():
            errors.append("Please enter your full name.")
        if not email or not is_valid_email(email):
            errors.append("Please enter a valid email address.")
        if not password or validate_password_strength(password):
            errors.append("Your password does not meet all the requirements above.")
        if password != confirm_password:
            errors.append("Passwords do not match.")
        if not errors and email_exists(email):
            errors.append("An account with this email already exists. Try logging in instead.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            create_user(full_name, email, password)
            st.success("Account created successfully! Please log in to continue.")
            st.session_state["auth_view"] = "login"
            st.rerun()

    st.markdown('<div class="cp-auth-switch">Already have an account?</div>', unsafe_allow_html=True)
    st.markdown('<div class="cp-secondary-btn">', unsafe_allow_html=True)
    if st.button("Back to Login", key="go_login"):
        st.session_state["auth_view"] = "login"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
