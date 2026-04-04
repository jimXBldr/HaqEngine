# backend/app.py
# Main Flask application. Wires together all pipeline components.
# Single endpoint: POST /verify

from flask import Flask, request, jsonify
from flask_cors import CORS

from claim_extractor import extract_claims
from claim_filter import filter_claims
from topic_matcher import match_topics
from verification_engine import verify_all
from output_formatter import format_results

app = Flask(__name__)

# Allow requests from the React dev server
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/health", methods=["GET"])
def health():
    """Simple health check endpoint."""
    return jsonify({"status": "ok", "engine": "Haq Engine v1"})


@app.route("/verify", methods=["POST"])
def verify():
    """
    Main verification endpoint.

    Request body (JSON):
        { "text": "<LLM-generated text to verify>" }

    Response (JSON):
        {
            "results": [...],      // verified claims with verdicts
            "rejected": [...],     // claims filtered out
            "summary": {...}       // aggregate counts
        }
    """
    # --- Input validation ---
    body = request.get_json(silent=True)
    if not body or "text" not in body:
        return jsonify({"error": "Request body must include a 'text' field."}), 400

    text = body["text"].strip()
    if not text:
        return jsonify({"error": "'text' field cannot be empty."}), 400

    if len(text) > 10_000:
        return jsonify({"error": "Input text is too long (max 10,000 characters)."}), 400

    try:
        # --- Step 1: Extract atomic claims ---
        claims = extract_claims(text)

        if not claims:
            return jsonify({
                "results": [],
                "rejected": [],
                "summary": {
                    "total_claims_extracted": 0,
                    "total_verified": 0,
                    "total_rejected": 0,
                    "verdict_counts": {
                        "Supported": 0,
                        "Contradicted": 0,
                        "Incomplete": 0,
                        "Not Verifiable": 0,
                    },
                },
                "message": "No claims could be extracted from the provided text.",
            })

        # --- Step 2: Filter claims (keep only factual/definitional) ---
        filtered = filter_claims(claims)
        verifiable_claims = filtered["verifiable"]
        rejected_claims = filtered["rejected"]

        if not verifiable_claims:
            return jsonify({
                "results": [],
                "rejected": rejected_claims,
                "summary": {
                    "total_claims_extracted": len(claims),
                    "total_verified": 0,
                    "total_rejected": len(rejected_claims),
                    "verdict_counts": {
                        "Supported": 0,
                        "Contradicted": 0,
                        "Incomplete": 0,
                        "Not Verifiable": 0,
                    },
                },
                "message": "All extracted claims were filtered out as non-verifiable.",
            })

        # --- Step 3: Match claims to knowledge base topics ---
        matched = match_topics(verifiable_claims)

        # --- Step 4: Verify claims against ground truth ---
        verification_results = verify_all(matched)

        # --- Step 5: Format and return final output ---
        output = format_results(verification_results, rejected_claims)
        return jsonify(output)

    except RuntimeError as e:
        # Pipeline errors (e.g. Groq API failure) — return 502
        return jsonify({"error": str(e)}), 502

    except Exception as e:
        # Unexpected errors — return 500
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)