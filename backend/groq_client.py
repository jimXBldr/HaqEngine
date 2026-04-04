# backend/groq_client.py
# Reusable Groq API client.
# All LLM calls go through this module — keeps API key and model config in one place.

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Fast, capable model for all pipeline steps
MODEL = "openai/gpt-oss-120b"


def call_groq(system_prompt: str, user_message: str, temperature: float = 0.0) -> str:
    """
    Send a chat completion request to Groq and return the raw text response.

    Args:
        system_prompt: Sets the role/behavior of the model.
        user_message: The actual content to process.
        temperature: 0.0 for deterministic, factual tasks.

    Returns:
        Stripped string response from the model.

    Raises:
        RuntimeError: If the API call fails or returns an error.
    """
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Please add it to your .env file."
        )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    }

    try:
        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        raise RuntimeError("Groq API request timed out.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Groq API HTTP error: {e.response.status_code} — {e.response.text}")
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected Groq API response format: {e}")


def call_groq_json(system_prompt: str, user_message: str) -> dict | list:
    """
    Call Groq and parse the response as JSON.
    Strips markdown code fences if the model wraps JSON in them.

    Returns:
        Parsed JSON object (dict or list).

    Raises:
        RuntimeError: If parsing fails.
    """
    raw = call_groq(system_prompt, user_message, temperature=0.0)

    # Strip markdown code fences that some models add
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first line (```json or ```) and last line (```)
        lines = lines[1:] if lines[0].startswith("```") else lines
        lines = lines[:-1] if lines and lines[-1].strip() == "```" else lines
        cleaned = "\n".join(lines).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Failed to parse Groq response as JSON.\n"
            f"Raw response: {raw}\n"
            f"Error: {e}"
        )