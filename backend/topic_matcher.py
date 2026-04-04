# backend/topic_matcher.py
# Step 3 of the pipeline: map each claim to a topic in the knowledge base.
# Uses keyword matching first (fast), falls back to LLM if no match found.

from groq_client import call_groq
from knowledge_base import SUPPORTED_TOPICS

# Keyword hints to quickly route claims to the right topic
KEYWORD_MAP = {
    "binary_search": [
        "binary search", "binary-search", "binarysearch",
        "sorted array", "halving", "log n", "divide and conquer search",
    ],
    "stack": [
        "stack", "lifo", "last in first out", "last-in-first-out",
        "push", "pop", "call stack",
    ],
    "queue": [
        "queue", "fifo", "first in first out", "first-in-first-out",
        "enqueue", "dequeue",
    ],
    "hash_table": [
        "hash table", "hash map", "hashtable", "hashmap",
        "hash function", "collision", "bucket", "hashing",
        "dictionary", "key-value",
    ],
}

LLM_SYSTEM_PROMPT = f"""You are a topic classification engine for computer science concepts.

Map the given claim to exactly one of these topics:
{", ".join(SUPPORTED_TOPICS)}

Rules:
- Return ONLY the topic label, exactly as listed above.
- If the claim does not match any topic, return "unknown".
- Do not explain. Do not add punctuation."""


def _keyword_match(claim: str) -> str | None:
    """
    Fast keyword-based matching. Returns topic string or None if no match.
    """
    lowered = claim.lower()
    for topic, keywords in KEYWORD_MAP.items():
        for kw in keywords:
            if kw in lowered:
                return topic
    return None


def _llm_match(claim: str) -> str:
    """
    LLM-based fallback topic matching.
    Returns matched topic string or "unknown".
    """
    user_message = f'Map this claim to a topic: "{claim}"'
    try:
        response = call_groq(LLM_SYSTEM_PROMPT, user_message, temperature=0.0)
        topic = response.strip().lower().replace(" ", "_")
        return topic if topic in SUPPORTED_TOPICS else "unknown"
    except RuntimeError:
        return "unknown"


def match_topic(claim: str) -> str:
    """
    Match a single claim to a knowledge base topic.

    Strategy:
    1. Try fast keyword matching.
    2. Fall back to LLM if keyword matching finds nothing.

    Args:
        claim: A single factual/definitional claim string.

    Returns:
        Topic string (e.g. "binary_search") or "unknown".
    """
    # Try keyword match first — zero API cost
    topic = _keyword_match(claim)
    if topic:
        return topic

    # Fallback: ask the LLM
    return _llm_match(claim)


def match_topics(claims: list[str]) -> list[dict]:
    """
    Match a list of claims to topics.

    Args:
        claims: List of factual claim strings.

    Returns:
        List of dicts: [{"claim": ..., "topic": ...}, ...]
    """
    return [
        {"claim": claim, "topic": match_topic(claim)}
        for claim in claims
    ]