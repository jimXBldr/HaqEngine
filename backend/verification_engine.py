# backend/verification_engine.py
# Step 4 of the pipeline: the CORE of Haq Engine.
# Compares each claim against its matched ground truth and returns a verdict.

import json
from groq_client import call_groq_json
from knowledge_base import KNOWLEDGE_BASE

# Strict verification prompt — model must return JSON with verdict + reason
SYSTEM_PROMPT = """You are a strict factual verification engine for computer science claims.

You will receive:
1. A claim made by an AI system.
2. The ground truth for the relevant topic.

Your job is to evaluate the claim ONLY against the provided ground truth.

Return a JSON object with exactly two fields:
- "verdict": one of ["Supported", "Contradicted", "Incomplete", "Not Verifiable"]
- "reason": a short, precise explanation (1–2 sentences max)

Verdict definitions:
- "Supported": The claim is fully accurate and consistent with the ground truth.
- "Contradicted": The claim directly conflicts with the ground truth.
- "Incomplete": The claim is partially correct but missing critical conditions or nuance.
- "Not Verifiable": The claim cannot be evaluated against the given ground truth.

Rules:
- Do NOT guess or use outside knowledge.
- Base your verdict ONLY on the provided ground truth.
- Be strict: a claim that omits a critical condition (e.g., "must be sorted") is Incomplete, not Supported.
- Return ONLY valid JSON. No markdown, no extra text."""


def verify_claim(claim: str, topic: str) -> dict:
    """
    Verify a single claim against the ground truth for its topic.

    Args:
        claim: The factual claim to verify.
        topic: The matched knowledge base topic key.

    Returns:
        dict with keys: claim, topic, verdict, reason
    """
    # Handle unknown topic — can't verify without ground truth
    if topic == "unknown" or topic not in KNOWLEDGE_BASE:
        return {
            "claim": claim,
            "topic": topic,
            "verdict": "Not Verifiable",
            "reason": "No matching topic found in the knowledge base.",
        }

    truth = KNOWLEDGE_BASE[topic]
    truth_json = json.dumps(truth, indent=2)

    user_message = (
        f"Claim: \"{claim}\"\n\n"
        f"Ground Truth for topic '{topic}':\n{truth_json}"
    )

    try:
        result = call_groq_json(SYSTEM_PROMPT, user_message)
    except RuntimeError as e:
        # Graceful degradation — return Not Verifiable if LLM fails
        return {
            "claim": claim,
            "topic": topic,
            "verdict": "Not Verifiable",
            "reason": f"Verification engine error: {str(e)}",
        }

    # Validate the response has the expected fields
    verdict = result.get("verdict", "Not Verifiable")
    reason = result.get("reason", "No reason provided.")

    # Enforce allowed verdicts
    allowed_verdicts = {"Supported", "Contradicted", "Incomplete", "Not Verifiable"}
    if verdict not in allowed_verdicts:
        verdict = "Not Verifiable"
        reason = f"Model returned unexpected verdict. Raw: {result}"

    return {
        "claim": claim,
        "topic": topic,
        "verdict": verdict,
        "reason": reason,
    }


def verify_all(matched_claims: list[dict]) -> list[dict]:
    """
    Run verification on a list of topic-matched claims.

    Args:
        matched_claims: List of dicts from topic_matcher: [{"claim": ..., "topic": ...}]

    Returns:
        List of verification result dicts.
    """
    results = []
    for item in matched_claims:
        result = verify_claim(item["claim"], item["topic"])
        results.append(result)
    return results