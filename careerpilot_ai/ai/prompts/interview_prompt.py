"""Prompt builders for Feature 6: AI Mock Interview."""


def build_questions_prompt(role: str, num_questions: int = 5) -> str:
    return f"""
You are a senior technical interviewer hiring for the role of {role}.
Generate a set of realistic mock interview questions covering a mix of
technical, behavioral, and role-specific scenario questions.

Return ONLY a valid JSON object (no markdown, no commentary, no code fences)
with EXACTLY this structure:

{{
  "role": "{role}",
  "questions": [
    {{
      "id": integer starting at 1,
      "question": "string",
      "type": "Technical" | "Behavioral" | "Scenario"
    }}
  ]
}}

Rules:
- Provide exactly {num_questions} questions.
- Mix the types; do not make them all Technical.
- Do not include any text outside the JSON object.
"""


def build_evaluation_prompt(role: str, qa_pairs: list) -> str:
    formatted_pairs = "\n".join(
        f"Q{i+1} ({pair['type']}): {pair['question']}\nA{i+1}: {pair['answer']}\n"
        for i, pair in enumerate(qa_pairs)
    )

    return f"""
You are a senior technical interviewer hiring for the role of {role}.
Evaluate the candidate's answers below.

{formatted_pairs}

Return ONLY a valid JSON object (no markdown, no commentary, no code fences)
with EXACTLY this structure:

{{
  "role": "{role}",
  "overall_score": number between 0 and 10 (one decimal place),
  "per_question_feedback": [
    {{
      "question_id": integer,
      "score": number between 0 and 10,
      "feedback": "1-2 sentence specific feedback"
    }}
  ],
  "strengths": ["strength1", "strength2"],
  "improvement_suggestions": ["suggestion1", "suggestion2", "suggestion3"]
}}

Rules:
- Be honest and constructive, not overly generous.
- per_question_feedback must include one entry per question, in order.
- Do not include any text outside the JSON object.
"""
