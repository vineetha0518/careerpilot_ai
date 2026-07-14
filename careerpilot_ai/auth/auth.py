"""
auth.py
-------
Authentication layer for CareerPilot AI.

Adds a `users` table to the existing SQLite database (careerpilot.db)
and provides small, well-tested helper functions for signup, login,
email validation, and password-strength checking. Passwords are never
stored in plain text — they are hashed with bcrypt before hitting disk.

This module intentionally has zero Streamlit imports so it can be unit
tested / reused outside the UI layer.
"""

import re
from datetime import datetime
from typing import Optional

import bcrypt

from database.database import get_connection

# A pragmatic (not fully RFC-5322) email pattern — good enough to catch
# the vast majority of typos without rejecting valid real-world addresses.
_EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

PASSWORD_RULES = [
    ("At least 8 characters", lambda pwd: len(pwd) >= 8),
    ("One uppercase letter", lambda pwd: bool(re.search(r"[A-Z]", pwd))),
    ("One lowercase letter", lambda pwd: bool(re.search(r"[a-z]", pwd))),
    ("One number", lambda pwd: bool(re.search(r"[0-9]", pwd))),
]


def init_auth_db() -> None:
    """Create the users table if it doesn't already exist. Safe to call every app run."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def is_valid_email(email: str) -> bool:
    """Lightweight email format validation."""
    return bool(email) and bool(_EMAIL_PATTERN.match(email.strip()))


def validate_password_strength(password: str) -> list[str]:
    """Returns the list of rule descriptions that the password FAILS to satisfy."""
    if not password:
        return [rule for rule, _ in PASSWORD_RULES]
    return [rule for rule, check in PASSWORD_RULES if not check(password)]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def email_exists(email: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id FROM users WHERE email = ?", (email.strip().lower(),)
        ).fetchone()
        return row is not None


def create_user(full_name: str, email: str, password: str) -> None:
    """Insert a new user. Caller is expected to have already validated the inputs
    (name non-empty, email format, password strength, no duplicate email)."""
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO users (full_name, email, password_hash, created_at)
               VALUES (?, ?, ?, ?)""",
            (
                full_name.strip(),
                email.strip().lower(),
                hash_password(password),
                datetime.now().isoformat(),
            ),
        )


def authenticate_user(email: str, password: str) -> Optional[dict]:
    """Returns the user record (dict) on success, or None on invalid credentials."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email.strip().lower(),)
        ).fetchone()
    if row and verify_password(password, row["password_hash"]):
        return dict(row)
    return None
