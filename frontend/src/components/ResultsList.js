// frontend/src/components/ResultsList.js
// Renders the full list of verified claims and the rejected claims section.

import React from "react";
import ResultCard from "./ResultCard";

export default function ResultsList({ results, rejected }) {
  const hasResults  = results && results.length > 0;
  const hasRejected = rejected && rejected.length > 0;

  return (
    <div className="results-list">
      {/* ── Verified Claims ── */}
      {hasResults ? (
        results.map((result, i) => (
          <ResultCard key={`${result.claim}-${i}`} result={result} index={i} />
        ))
      ) : (
        <div className="results-empty">
          <p>No verifiable claims were found in the provided text.</p>
          <p style={{ marginTop: 8, fontSize: "0.72rem" }}>
            Try including specific statements about binary search, stacks, queues, or hash tables.
          </p>
        </div>
      )}

      {/* ── Rejected Claims (filtered out) ── */}
      {hasRejected && (
        <div className="rejected-section">
          <p className="rejected-title">
            FILTERED OUT — {rejected.length} claim{rejected.length !== 1 ? "s" : ""} rejected (non-factual / opinion / vague)
          </p>
          <ul className="rejected-list">
            {rejected.map((claim, i) => (
              <li key={i} className="rejected-item">
                {claim}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}