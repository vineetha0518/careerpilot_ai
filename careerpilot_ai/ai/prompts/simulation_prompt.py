"""Prompt builders for Feature 7: Internship Simulation."""


def build_simulation_prompt(role: str) -> str:
    return f"""
You are a hiring manager designing a realistic, self-contained take-home
internship task for a candidate applying for the role of {role}.

Return ONLY a valid JSON object (no markdown, no commentary, no code fences)
with EXACTLY this structure:

{{
  "role": "{role}",
  "task_title": "short, specific task name",
  "scenario": "2-3 sentence realistic business scenario/context",
  "objectives": ["objective1", "objective2", "objective3"],
  "deliverables": ["deliverable1", "deliverable2"],
  "evaluation_criteria": ["criterion1", "criterion2", "criterion3"],
  "estimated_duration": "string, e.g. 3-5 days"
}}

Rules:
- The task must be realistic, specific to the role, and completable by a
  student without access to proprietary company tools.
- Do not include any text outside the JSON object.
"""


def build_simulation_feedback_prompt(role: str, task_title: str, submission: str) -> str:
    return f"""
You are a hiring manager reviewing a candidate's submission for the
internship task "{task_title}" for the role of {role}.

CANDIDATE SUBMISSION:
\"\"\"
{submission}
\"\"\"

Return ONLY a valid JSON object (no markdown, no commentary, no code fences)
with EXACTLY this structure:

{{
  "score": integer between 0 and 100,
  "strengths": ["strength1", "strength2"],
  "gaps": ["gap1", "gap2"],
  "feedback": "3-4 sentence overall feedback",
  "hiring_recommendation": "Strong Fit" | "Potential Fit" | "Needs Development"
}}

Rules:
- Be specific about what was done well and what was missing.
- Do not include any text outside the JSON object.
"""
