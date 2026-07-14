"""
ui_helpers.py
-------------
Shared CSS injection and small reusable UI components so every page
of CareerPilot AI looks like one coherent, premium AI SaaS product
instead of a default Streamlit app.

Two visual "modes" share the same design language:
  * inject_global_css()  -> the authenticated app shell (dark theme)
  * inject_auth_css()    -> the Login / Sign Up screens (gradient + glass)
"""

import streamlit as st

# ---------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------
PRIMARY = "#6366F1"        # indigo
PRIMARY_DARK = "#4F46E5"
SECONDARY = "#A855F7"       # purple
ACCENT = "#22D3EE"          # cyan
BG_DEEP = "#0B1120"
BG_SURFACE = "#111827"
BG_CARD = "#161F32"
BORDER = "rgba(148, 163, 184, 0.14)"
TEXT_LIGHT = "#F1F5F9"
TEXT_MUTED = "#94A3B8"
SUCCESS = "#34D399"
WARNING = "#FBBF24"
DANGER = "#F87171"

GRADIENT = f"linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%)"


# ---------------------------------------------------------------------
# Global theme — authenticated app shell
# ---------------------------------------------------------------------
def inject_global_css() -> None:
    """Injects the premium dark theme used across every page once logged in."""
    st.markdown(f"""
    <style>
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        .stApp {{
            background: radial-gradient(circle at 15% 0%, #1B2340 0%, {BG_DEEP} 45%) fixed;
        }}

        html, body, [class*="css"] {{
            font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif;
            color: {TEXT_LIGHT};
        }}

        h1, h2, h3, h4, h5, p, span, label, div {{
            color: {TEXT_LIGHT};
        }}

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0D1326 0%, #161033 100%);
            border-right: 1px solid {BORDER};
        }}
        section[data-testid="stSidebar"] * {{
            color: {TEXT_LIGHT} !important;
        }}
        section[data-testid="stSidebar"] div[role="radiogroup"] label {{
            padding: 11px 14px;
            border-radius: 12px;
            margin-bottom: 4px;
            transition: background 0.18s ease, transform 0.12s ease;
            border: 1px solid transparent;
        }}
        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
            background: rgba(99, 102, 241, 0.14);
            transform: translateX(2px);
        }}
        section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
            background: rgba(99, 102, 241, 0.22);
            border: 1px solid rgba(99, 102, 241, 0.45);
            box-shadow: 0 2px 12px rgba(99, 102, 241, 0.25);
        }}

        .cp-sidebar-brand {{
            text-align: center;
            padding: 6px 0 18px 0;
        }}
        .cp-sidebar-brand .name {{
            font-size: 19px;
            font-weight: 800;
            background: {GRADIENT};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .cp-sidebar-brand .tagline {{
            font-size: 11px;
            color: {TEXT_MUTED};
        }}

        .cp-user-block {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px;
            border-radius: 14px;
            background: rgba(255,255,255,0.04);
            border: 1px solid {BORDER};
            margin-bottom: 16px;
        }}
        .cp-avatar {{
            min-width: 38px;
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: {GRADIENT};
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 15px;
            color: white;
        }}
        .cp-user-meta .uname {{
            font-size: 13.5px;
            font-weight: 700;
            line-height: 1.2;
        }}
        .cp-user-meta .uemail {{
            font-size: 11px;
            color: {TEXT_MUTED};
            line-height: 1.2;
            word-break: break-all;
        }}

        /* ---------- Hero ---------- */
        .cp-hero {{
            padding: 30px 32px;
            border-radius: 20px;
            background: {GRADIENT};
            color: white;
            margin-bottom: 24px;
            box-shadow: 0 12px 32px rgba(99, 102, 241, 0.28);
        }}
        .cp-hero h1 {{
            margin: 0 0 6px 0;
            font-size: 28px;
            font-weight: 800;
            color: white !important;
        }}
        .cp-hero p {{
            margin: 0;
            opacity: 0.92;
            font-size: 15px;
            color: white !important;
        }}

        /* ---------- Cards ---------- */
        .cp-card {{
            background: {BG_CARD};
            border-radius: 16px;
            padding: 22px 24px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            border: 1px solid {BORDER};
            margin-bottom: 18px;
            transition: border-color 0.2s ease, transform 0.15s ease;
        }}
        .cp-card:hover {{
            border-color: rgba(99, 102, 241, 0.35);
        }}
        .cp-card h3, .cp-card h4 {{
            margin-top: 0;
        }}

        .cp-metric {{
            background: {BG_CARD};
            border-radius: 16px;
            padding: 18px 20px;
            border: 1px solid {BORDER};
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.2);
            text-align: center;
            margin-bottom: 12px;
            transition: transform 0.15s ease;
        }}
        .cp-metric:hover {{
            transform: translateY(-2px);
        }}
        .cp-metric .value {{
            font-size: 30px;
            font-weight: 800;
            background: {GRADIENT};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .cp-metric .label {{
            font-size: 12.5px;
            color: {TEXT_MUTED};
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }}

        .cp-badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
        }}
        .cp-badge-high {{ background: rgba(248, 113, 113, 0.16); color: {DANGER}; }}
        .cp-badge-medium {{ background: rgba(251, 191, 36, 0.16); color: {WARNING}; }}
        .cp-badge-low {{ background: rgba(52, 211, 153, 0.16); color: {SUCCESS}; }}

        .cp-pill {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            background: rgba(99, 102, 241, 0.14);
            color: #C7D2FE;
            font-size: 12px;
            font-weight: 600;
            margin: 2px 4px 2px 0;
            border: 1px solid rgba(99, 102, 241, 0.25);
        }}

        .cp-timeline-week {{
            border-left: 3px solid {PRIMARY};
            padding: 4px 0 4px 20px;
            margin-bottom: 22px;
            position: relative;
        }}
        .cp-timeline-week::before {{
            content: "";
            position: absolute;
            left: -9px;
            top: 6px;
            width: 15px;
            height: 15px;
            border-radius: 50%;
            background: {GRADIENT};
            border: 3px solid {BG_DEEP};
            box-shadow: 0 0 0 2px {PRIMARY};
        }}

        /* ---------- Buttons ---------- */
        div.stButton > button {{
            background: {GRADIENT};
            color: white;
            border: none;
            border-radius: 11px;
            padding: 10px 20px;
            font-weight: 700;
            transition: transform 0.12s ease, box-shadow 0.12s ease, filter 0.12s ease;
        }}
        div.stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.35);
            filter: brightness(1.08);
            color: white;
        }}
        div.stButton > button:active {{
            transform: translateY(0px);
        }}

        .cp-back-btn button {{
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid {BORDER} !important;
            box-shadow: none !important;
            font-weight: 600 !important;
            padding: 6px 14px !important;
        }}
        .cp-back-btn button:hover {{
            background: rgba(99, 102, 241, 0.14) !important;
            transform: none !important;
        }}

        /* ---------- Inputs ---------- */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {{
            background: {BG_SURFACE} !important;
            color: {TEXT_LIGHT} !important;
            border: 1px solid {BORDER} !important;
            border-radius: 10px !important;
        }}
        .stTextInput input:focus, .stTextArea textarea:focus {{
            border-color: {PRIMARY} !important;
            box-shadow: 0 0 0 1px {PRIMARY} !important;
        }}

        /* ---------- Chat bubbles ---------- */
        .cp-chat-bubble-q {{
            background: rgba(99, 102, 241, 0.14);
            border-radius: 14px 14px 14px 2px;
            padding: 12px 16px;
            margin-bottom: 8px;
            color: {TEXT_LIGHT};
            border: 1px solid rgba(99, 102, 241, 0.2);
        }}
        .cp-chat-bubble-a {{
            background: rgba(255,255,255,0.04);
            border-radius: 14px 14px 2px 14px;
            padding: 12px 16px;
            margin-bottom: 16px;
            color: {TEXT_LIGHT};
            border: 1px solid {BORDER};
        }}

        /* ---------- Misc Streamlit widget tint ---------- */
        [data-testid="stMetricValue"] {{ color: {TEXT_LIGHT}; }}
        .stAlert {{ border-radius: 12px; }}
        hr {{ border-color: {BORDER}; }}
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------
# Auth theme — Login / Sign Up screens
# ---------------------------------------------------------------------
def inject_auth_css() -> None:
    """Injects the gradient + glassmorphism theme used only on the auth screens."""
    st.markdown(f"""
    <style>
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        section[data-testid="stSidebar"] {{ display: none; }}

        .stApp {{
            background:
                radial-gradient(circle at 20% 20%, rgba(99, 102, 241, 0.35), transparent 45%),
                radial-gradient(circle at 80% 80%, rgba(168, 85, 247, 0.30), transparent 45%),
                linear-gradient(135deg, #0B1120 0%, #151233 100%);
            background-attachment: fixed;
        }}

        html, body, [class*="css"] {{
            font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif;
        }}

        .block-container {{
            max-width: 460px !important;
            padding-top: 6vh !important;
        }}

        h1, h2, h3, p, span, label, div {{ color: {TEXT_LIGHT}; }}

        @keyframes cp-float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-6px); }}
            100% {{ transform: translateY(0px); }}
        }}
        @keyframes cp-glow {{
            0%, 100% {{ box-shadow: 0 0 24px rgba(99, 102, 241, 0.45); }}
            50% {{ box-shadow: 0 0 40px rgba(168, 85, 247, 0.55); }}
        }}

        .cp-auth-logo {{
            width: 68px;
            height: 68px;
            margin: 0 auto 18px auto;
            border-radius: 20px;
            background: {GRADIENT};
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            animation: cp-float 3.2s ease-in-out infinite, cp-glow 3.2s ease-in-out infinite;
        }}

        .cp-auth-title {{
            text-align: center;
            font-size: 30px;
            font-weight: 800;
            margin-bottom: 4px;
            background: linear-gradient(135deg, #FFFFFF 0%, #C7D2FE 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .cp-auth-subtitle {{
            text-align: center;
            font-size: 14.5px;
            color: {TEXT_MUTED};
            margin-bottom: 26px;
        }}

        /* Glassmorphism card wrapping the form widgets */
        div[data-testid="stForm"], .cp-glass-block {{
            background: rgba(255, 255, 255, 0.055) !important;
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 22px !important;
            padding: 32px 30px !important;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
        }}

        .stTextInput input {{
            background: rgba(255,255,255,0.06) !important;
            color: {TEXT_LIGHT} !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            border-radius: 12px !important;
            padding: 11px 14px !important;
        }}
        .stTextInput input:focus {{
            border-color: {PRIMARY} !important;
            box-shadow: 0 0 0 1px {PRIMARY} !important;
        }}
        .stTextInput label {{
            font-weight: 600;
            font-size: 13px;
            color: {TEXT_MUTED} !important;
        }}

        div.stButton > button {{
            background: {GRADIENT};
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 20px;
            font-weight: 700;
            width: 100%;
            transition: transform 0.12s ease, box-shadow 0.12s ease, filter 0.12s ease;
        }}
        div.stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 10px 26px rgba(99, 102, 241, 0.4);
            filter: brightness(1.08);
            color: white;
        }}

        .cp-secondary-btn button {{
            background: rgba(255,255,255,0.06) !important;
            border: 1px solid rgba(255,255,255,0.16) !important;
            box-shadow: none !important;
        }}
        .cp-secondary-btn button:hover {{
            background: rgba(255,255,255,0.1) !important;
            box-shadow: none !important;
        }}

        .cp-auth-switch {{
            text-align: center;
            color: {TEXT_MUTED};
            font-size: 13.5px;
            margin: 18px 0 8px 0;
        }}

        .pw-checklist {{
            margin: -6px 0 14px 0;
            padding: 10px 14px;
            border-radius: 10px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
        }}
        .pw-rule {{
            font-size: 12.5px;
            padding: 2px 0;
        }}
        .pw-rule.ok {{ color: {SUCCESS}; }}
        .pw-rule.bad {{ color: {TEXT_MUTED}; }}

        .stAlert {{ border-radius: 12px; }}
    </style>
    """, unsafe_allow_html=True)


def auth_header(title: str, subtitle: str, emoji: str = "🚀") -> None:
    """Animated logo + gradient headline shared by the Login and Sign Up screens."""
    st.markdown(f"""
    <div class="cp-auth-logo">{emoji}</div>
    <div class="cp-auth-title">{title}</div>
    <div class="cp-auth-subtitle">{subtitle}</div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------
# Shared small components
# ---------------------------------------------------------------------
def hero(title: str, subtitle: str, emoji: str = "") -> None:
    st.markdown(f"""
    <div class="cp-hero">
        <h1>{emoji} {title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def metric_card(value, label) -> None:
    st.markdown(f"""
    <div class="cp-metric">
        <div class="value">{value}</div>
        <div class="label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def priority_badge(level: str) -> str:
    level_l = (level or "").lower()
    css_class = "cp-badge-medium"
    if "high" in level_l:
        css_class = "cp-badge-high"
    elif "low" in level_l:
        css_class = "cp-badge-low"
    return f'<span class="cp-badge {css_class}">{level}</span>'


def pill_list(items) -> str:
    if not items:
        return ""
    return "".join(f'<span class="cp-pill">{item}</span>' for item in items)


def empty_state(message: str, icon: str = "✨") -> None:
    st.markdown(f"""
    <div class="cp-card" style="text-align:center; padding: 40px 20px;">
        <div style="font-size:40px;">{icon}</div>
        <p style="color:{TEXT_MUTED}; font-size:15px; margin-top:10px;">{message}</p>
    </div>
    """, unsafe_allow_html=True)


def sidebar_user_block(user: dict) -> None:
    """Avatar + name + email block shown at the top of the sidebar."""
    full_name = (user or {}).get("full_name", "?")
    email = (user or {}).get("email", "")
    initials = "".join([p[0] for p in full_name.split()][:2]).upper() or "?"
    st.markdown(f"""
    <div class="cp-user-block">
        <div class="cp-avatar">{initials}</div>
        <div class="cp-user-meta">
            <div class="uname">{full_name}</div>
            <div class="uemail">{email}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def back_button(label: str = "← Back") -> None:
    """
    Renders a small 'Back' button that pops the last page off the
    session-state navigation history stack (see app.py) and reruns.
    Does nothing but render if there is no history (e.g. Dashboard).
    """
    st.markdown('<div class="cp-back-btn">', unsafe_allow_html=True)
    clicked = st.button(label, key=f"back_btn_{st.session_state.get('current_page', '')}")
    st.markdown('</div>', unsafe_allow_html=True)

    if clicked:
        history = st.session_state.get("nav_history", [])
        target = history.pop() if history else "🏠 Dashboard"
        st.session_state["nav_history"] = history
        st.session_state["current_page"] = target
        st.session_state["nav_widget_version"] = st.session_state.get("nav_widget_version", 0) + 1
        st.rerun()
