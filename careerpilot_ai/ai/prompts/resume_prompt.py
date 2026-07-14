"""Prompt builder for Feature 5: Resume Analyzer."""


def build_resume_prompt(resume_text: str, target_role: str = "") -> str:
    role_line = f"TARGET ROLE: {target_role}" if target_role else "TARGET ROLE: Not specified — evaluate generally."

    return f"""
You are an ATS (Applicant Tracking System) expert and senior technical
recruiter. Analyze the resume text below.

{role_line}

RESUME TEXT:
\"\"\"
{resume_text}
\"\"\"

Return ONLY a valid JSON object (no markdown, no commentary, no code fences)
with EXACTLY this structure:

{{
  "ats_score": integer between 0 and 100,
  "missing_keywords": ["keyword1", "keyword2", "keyword3"],
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["weakness1", "weakness2", "weakness3"],
  "suggestions": ["suggestion1", "suggestion2", "suggestion3", "suggestion4"]
}}

Rules:
- ats_score should reflect formatting, keyword relevance, quantified
  achievements, and clarity.
- Be specific and actionable in suggestions, not generic.
- Do not include any text outside the JSON object.
"""
