"""
database.py
------------
Handles all SQLite persistence for CareerPilot AI.

The database is intentionally lightweight for a hackathon MVP:
one file (careerpilot.db) with a handful of tables covering the
student profile plus a history of every AI-generated artifact
(career recommendations, skill gaps, roadmaps, resume scores,
interview scores, simulation results). The Career Readiness Score
is derived from these history tables at read time.
"""

import sqlite3
import json
import os
from datetime import datetime
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "careerpilot.db")


@contextmanager
def get_connection():
    """Context-managed SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Create all tables if they do not already exist. Safe to call every app run."""
    with get_connection() as conn:
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                name TEXT,
                degree TEXT,
                year TEXT,
                college TEXT,
                skills TEXT,
                interests TEXT,
                career_goal TEXT,
                updated_at TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS career_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                result_json TEXT,
                created_at TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS skill_gap_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_career TEXT,
                result_json TEXT,
                created_at TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS roadmaps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_career TEXT,
                result_json TEXT,
                created_at TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS resume_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                ats_score INTEGER,
                result_json TEXT,
                created_at TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS interview_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                avg_score REAL,
                result_json TEXT,
                created_at TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS simulations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                result_json TEXT,
                created_at TEXT
            )
        """)

        conn.commit()


# ---------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------

def save_profile(name, degree, year, college, skills, interests, career_goal):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO profile (id, name, degree, year, college, skills, interests, career_goal, updated_at)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                degree=excluded.degree,
                year=excluded.year,
                college=excluded.college,
                skills=excluded.skills,
                interests=excluded.interests,
                career_goal=excluded.career_goal,
                updated_at=excluded.updated_at
        """, (name, degree, year, college, skills, interests, career_goal, datetime.now().isoformat()))


def get_profile():
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM profile WHERE id = 1").fetchone()
        return dict(row) if row else None


# ---------------------------------------------------------------------
# Career Recommendations
# ---------------------------------------------------------------------

def save_career_recommendation(result: dict):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO career_recommendations (result_json, created_at) VALUES (?, ?)",
            (json.dumps(result), datetime.now().isoformat())
        )


def get_latest_career_recommendation():
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM career_recommendations ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return json.loads(row["result_json"]) if row else None


# ---------------------------------------------------------------------
# Skill Gap
# ---------------------------------------------------------------------

def save_skill_gap(target_career: str, result: dict):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO skill_gap_results (target_career, result_json, created_at) VALUES (?, ?, ?)",
            (target_career, json.dumps(result), datetime.now().isoformat())
        )


def get_latest_skill_gap():
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM skill_gap_results ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return json.loads(row["result_json"]) if row else None


# ---------------------------------------------------------------------
# Roadmap
# ---------------------------------------------------------------------

def save_roadmap(target_career: str, result: dict):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO roadmaps (target_career, result_json, created_at) VALUES (?, ?, ?)",
            (target_career, json.dumps(result), datetime.now().isoformat())
        )


def get_latest_roadmap():
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM roadmaps ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return json.loads(row["result_json"]) if row else None


# ---------------------------------------------------------------------
# Resume Analysis
# ---------------------------------------------------------------------

def save_resume_analysis(filename: str, ats_score: int, result: dict):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO resume_analysis (filename, ats_score, result_json, created_at) VALUES (?, ?, ?, ?)",
            (filename, ats_score, json.dumps(result), datetime.now().isoformat())
        )


def get_latest_resume_analysis():
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM resume_analysis ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return dict(row) if row else None


# ---------------------------------------------------------------------
# Interview Sessions
# ---------------------------------------------------------------------

def save_interview_session(role: str, avg_score: float, result: dict):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO interview_sessions (role, avg_score, result_json, created_at) VALUES (?, ?, ?, ?)",
            (role, avg_score, json.dumps(result), datetime.now().isoformat())
        )


def get_latest_interview_session():
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM interview_sessions ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return dict(row) if row else None


# ---------------------------------------------------------------------
# Simulations
# ---------------------------------------------------------------------

def save_simulation(role: str, result: dict):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO simulations (role, result_json, created_at) VALUES (?, ?, ?)",
            (role, json.dumps(result), datetime.now().isoformat())
        )


def get_latest_simulation():
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM simulations ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return json.loads(row["result_json"]) if row else None


# ---------------------------------------------------------------------
# Career Readiness Score
# ---------------------------------------------------------------------

def compute_readiness_score():
    """
    Derives an overall 0-100 Career Readiness Score from whatever
    artifacts exist so far. Each component contributes up to 20 points
    and only counts if the student has actually generated that artifact,
    so the score grows organically as the student uses more features.
    """
    with get_connection() as conn:
        resume = conn.execute("SELECT ats_score FROM resume_analysis ORDER BY id DESC LIMIT 1").fetchone()
        interview = conn.execute("SELECT avg_score FROM interview_sessions ORDER BY id DESC LIMIT 1").fetchone()
        roadmap = conn.execute("SELECT id FROM roadmaps ORDER BY id DESC LIMIT 1").fetchone()
        skill_gap = conn.execute("SELECT id FROM skill_gap_results ORDER BY id DESC LIMIT 1").fetchone()
        simulation = conn.execute("SELECT id FROM simulations ORDER BY id DESC LIMIT 1").fetchone()

    breakdown = {}

    resume_component = round((resume["ats_score"] / 100) * 20) if resume else 0
    breakdown["Resume"] = resume_component

    interview_component = round((interview["avg_score"] / 10) * 20) if interview else 0
    breakdown["Interview"] = interview_component

    roadmap_component = 20 if roadmap else 0
    breakdown["Roadmap"] = roadmap_component

    skills_component = 20 if skill_gap else 0
    breakdown["Skills"] = skills_component

    projects_component = 20 if simulation else 0
    breakdown["Projects"] = projects_component

    total = sum(breakdown.values())
    return total, breakdown
