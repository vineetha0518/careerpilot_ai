"""Prompt builder for Feature 4: Learning Roadmap."""


def build_roadmap_prompt(target_career: str, current_skills: str, missing_skills: str) -> str:
    return f"""
You are an expert curriculum designer. Build a focused, realistic 8-week
learning roadmap that takes a student from their current skill level to
job-readiness for the target career below.

TARGET CAREER: {target_career}
CURRENT SKILLS: {current_skills}
KNOWN SKILL GAPS: {missing_skills}

Return ONLY a valid JSON object (no markdown, no commentary, no code fences)
with EXACTLY this structure:

{{
  "target_career": "{target_career}",
  "weeks": [
    {{
      "week_number": integer 1-8,
      "title": "short theme for the week",
      "topics": ["topic1", "topic2", "topic3"],
      "mini_project": "a small, concrete project for that week",
      "resources": ["resource1", "resource2"],
      "expected_outcome": "one sentence describing what the student can do by week end"
    }}
  ]
}}

Rules:
- Provide exactly 8 week objects, week_number 1 through 8, difficulty
  increasing progressively.
- Resources should be realistic (named courses, docs, books, or platforms),
  not fake URLs.
- Do not include any text outside the JSON object.
"""
