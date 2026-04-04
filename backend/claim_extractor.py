# backend/claim_extractor.py
# Step 1 of the pipeline: extract atomic claims from raw LLM-generated text.
# Uses Groq to decompose paragraphs into standalone, verifiable statements.

from groq_client import call_groq

SYSTEM_PROMPT = """You are a precise claim extraction engine.

Your job is to break a block of text into atomic, standalone factual claims.

Rules:
- Each claim must be self-contained and independently verifiable.
- One claim per line. No numbering, no bullet points, no explanations.
- Do not rephrase into questions.
- Do not merge multiple claims into one line.
- Do not include opinions, advice, or general commentary.
- Output ONLY the claims, nothing else."""


def extract_claims(text: str) -> list[str]:
    """
    Extract atomic claims from a block of text.

    Args:
        text: Raw LLM-generated text (paragraph or multi-sentence input).

    Returns:
        List of atomic claim strings. Empty list if extraction fails.
    """
    if not text or not text.strip():
        return []

    user_message = f"Extract all atomic factual claims from this text:\n\n{text.strip()}"

    try:
        raw_response = call_groq(SYSTEM_PROMPT, user_message, temperature=0.0)
    except RuntimeError as e:
        raise RuntimeError(f"Claim extraction failed: {e}")

    # Split by newline, strip whitespace, remove empty lines
    claims = [
        line.strip()
        for line in raw_response.split("\n")
        if line.strip()
    ]

    # Filter out lines that look like headers or meta-commentary from the model
    claims = [
        c for c in claims
        if len(c) > 10 and not c.lower().startswith("here are")
    ]

    return claims