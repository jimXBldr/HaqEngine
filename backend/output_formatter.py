# backend/output_formatter.py
# Final step: formats the raw verification results into a clean, consistent output.
# Also generates a summary statistics block for the frontend.

VERDICT_EMOJI = {
    "Supported": "✅",
    "Contradicted": "❌",
    "Incomplete": "⚠️",
    "Not Verifiable": "❓",
}


def format_results(
    verification_results: list[dict],
    rejected_claims: list[str],
) -> dict:
    """
    Build the final structured output for the API response.

    Args:
        verification_results: List of dicts from verification_engine.verify_all()
        rejected_claims: List of claims filtered out during claim filtering.

    Returns:
        dict with:
            "results"    — list of verified claim objects
            "rejected"   — list of rejected claims
            "summary"    — aggregate counts per verdict
    """
    # Build the per-claim result list
    formatted = []
    for item in verification_results:
        verdict = item.get("verdict", "Not Verifiable")
        formatted.append({
            "claim": item["claim"],
            "topic": item.get("topic", "unknown"),
            "verdict": verdict,
            "verdict_emoji": VERDICT_EMOJI.get(verdict, "❓"),
            "reason": item.get("reason", ""),
            "source": item.get("source", None),   # { name, url } or None
        })

    # Build summary counts
    summary = {
        "total_claims_extracted": len(formatted) + len(rejected_claims),
        "total_verified": len(formatted),
        "total_rejected": len(rejected_claims),
        "verdict_counts": {
            "Supported": 0,
            "Contradicted": 0,
            "Incomplete": 0,
            "Not Verifiable": 0,
        },
    }

    for item in formatted:
        v = item["verdict"]
        if v in summary["verdict_counts"]:
            summary["verdict_counts"][v] += 1

    return {
        "results": formatted,
        "rejected": rejected_claims,
        "summary": summary,
    }