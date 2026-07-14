"""Prompt builder for Feature 3: Skill Gap Analysis."""


def build_skill_gap_prompt(current_skills: str, target_career: str) -> str:
    return f"""
You are a technical career advisor. Compare the student's CURRENT SKILLS
against what is required for their TARGET CAREER, and identify the gap.

CURRENT SKILLS: {current_skills}
TARGET CAREER: {target_career}

Return ONLY a valid JSON object (no markdown, no commentary, no code fences)
with EXACTLY this structure:

{{
  "target_career": "{target_career}",
  "overall_readiness_percentage": integer between 0 and 100,
  "missing_skills": [
    {{
      "skill": "string",
      "difficulty": "Beginner" | "Intermediate" | "Advanced",
      "priority": "High" | "Medium" | "Low",
      "estimated_learning_time": "string, e.g. 3 weeks"
    }}
  ]
}}

Rules:
- Include 5 to 8 missing_skills, ordered by priority (High first).
- overall_readiness_percentage reflects how close current_skills already
  are to the target career's requirements.
- Do not include any text outside the JSON object.
"""
