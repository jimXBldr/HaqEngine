# backend/claim_filter.py
# Step 2 of the pipeline: filter claims to keep only factual/definitional ones.
# Rejects opinions, advice, vague statements, and complex reasoning chains.

from groq_client import call_groq

SYSTEM_PROMPT = """You are a claim classification engine.

For each claim provided, decide if it is a FACTUAL or DEFINITIONAL claim
that can be verified against a computer science textbook.

Rules:
- Answer YES if the claim is a specific factual statement or a definition
  about a data structure, algorithm, or CS concept.
- Answer NO if the claim is an opinion, general advice, vague, or
  involves subjective judgment.
- Reply with ONLY "YES" or "NO" for each claim. One answer per line.
- Do not explain. Do not add extra text."""


def filter_claims(claims: list[str]) -> dict:
    """
    Filter a list of claims into verifiable and rejected buckets.

    Args:
        claims: List of atomic claim strings.

    Returns:
        dict with keys:
            "verifiable" — list of claims to pass to the verification engine
            "rejected"   — list of claims that were filtered out
    """
    if not claims:
        return {"verifiable": [], "rejected": []}

    # Build a numbered list for the model so we can map answers back
    numbered_claims = "\n".join(
        f"{i + 1}. {claim}" for i, claim in enumerate(claims)
    )

    user_message = (
        f"Classify each claim as YES (factual/definitional) or NO (opinion/vague):\n\n"
        f"{numbered_claims}"
    )

    try:
        raw_response = call_groq(SYSTEM_PROMPT, user_message, temperature=0.0)
    except RuntimeError as e:
        raise RuntimeError(f"Claim filtering failed: {e}")

    # Parse the YES/NO answers — one per line
    answers = [
        line.strip().upper()
        for line in raw_response.split("\n")
        if line.strip()
    ]

    verifiable = []
    rejected = []

    for i, claim in enumerate(claims):
        # Default to "NO" if the model returned fewer answers than claims
        answer = answers[i] if i < len(answers) else "NO"

        # Accept any response containing "YES"
        if "YES" in answer:
            verifiable.append(claim)
        else:
            rejected.append(claim)

    return {"verifiable": verifiable, "rejected": rejected}