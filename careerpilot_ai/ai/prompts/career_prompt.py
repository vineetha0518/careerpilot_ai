"""Prompt builder for Feature 2: Career Recommendation."""


def build_career_prompt(name: str, degree: str, year: str, skills: str,
                         interests: str, career_goal: str) -> str:
    return f"""
You are an expert career counselor with deep knowledge of the global tech
and non-tech job market in 2026. Analyze the student profile below and
recommend the top 3 careers that best fit them.

STUDENT PROFILE:
- Name: {name}
- Degree: {degree}
- Year of Study: {year}
- Current Skills: {skills}
- Interests: {interests}
- Stated Career Goal: {career_goal}

Return ONLY a valid JSON object (no markdown, no commentary, no code fences)
with EXACTLY this structure:

{{
  "careers": [
    {{
      "title": "string, e.g. Data Scientist",
      "match_percentage": integer between 0 and 100,
      "reason": "2-3 sentence explanation of why this career fits this student",
      "required_skills": ["skill1", "skill2", "skill3", "skill4"],
      "salary_range": "string, e.g. INR 6-12 LPA (entry level, India)",
      "future_opportunities": "1-2 sentence outlook on growth and demand for this role"
    }}
  ]
}}

Rules:
- Return exactly 3 careers, ordered by match_percentage descending.
- match_percentage values must be realistic and distinct.
- Keep salary_range relevant to the Indian job market unless the student's
  profile clearly suggests otherwise.
- Do not include any text outside the JSON object.
"""
