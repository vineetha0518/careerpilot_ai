"""
gemini.py
---------
Thin wrapper around the google-genai SDK used by every feature page.

All prompts in ai/prompts/ ask the model to return ONLY a JSON object,
so generate_json() centralizes: client creation, the actual call,
stripping markdown code fences if the model adds them anyway, and
raising a clean, user-friendly error if parsing fails.
"""

import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "gemini-2.5-flash"

_client = None


class GeminiConfigError(Exception):
    """Raised when the Gemini API key is missing or invalid."""
    pass


class GeminiResponseError(Exception):
    """Raised when the model response could not be parsed as JSON."""
    pass


def get_client():
    """Lazily create and cache a single genai.Client using the key from .env."""
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            raise GeminiConfigError(
                "GEMINI_API_KEY is not set. Copy .env.example to .env and add your key."
            )
        _client = genai.Client(api_key=api_key)
    return _client


def _strip_code_fences(text: str) -> str:
    """Models sometimes wrap JSON in ```json ... ``` even when told not to. Strip it."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)
        # text now looks like ['', 'json\n{...}\n', ''] or ['', '{...}\n', '']
        if len(text) >= 2:
            body = text[1]
            if body.lower().startswith("json"):
                body = body[4:]
            return body.strip()
    return text


def generate_json(prompt: str, temperature: float = 0.7) -> dict:
    """
    Sends a prompt to Gemini and parses the response as JSON.
    Every prompt builder in ai/prompts/ is responsible for instructing
    the model to return ONLY a JSON object matching a specific schema.
    """
    client = get_client()
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                response_mime_type="application/json",
            ),
        )
        raw_text = response.text
    except Exception as exc:
        raise GeminiConfigError(f"Gemini API call failed: {exc}") from exc

    cleaned = _strip_code_fences(raw_text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise GeminiResponseError(
            f"Could not parse the AI response as JSON: {exc}\n\nRaw response:\n{raw_text[:500]}"
        ) from exc


def generate_text(prompt: str, temperature: float = 0.7) -> str:
    """Plain text generation, used for free-form interview follow-up questions."""
    client = get_client()
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=temperature),
        )
        return response.text.strip()
    except Exception as exc:
        raise GeminiConfigError(f"Gemini API call failed: {exc}") from exc
