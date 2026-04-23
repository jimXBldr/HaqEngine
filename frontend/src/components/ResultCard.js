// frontend/src/components/ResultCard.js
// Renders a single claim's verification result as a styled card.
// Left border color and badge color are determined by the verdict.
// Shows the ground-truth source citation with a clickable link.

import React from "react";

// Maps verdict string to CSS class suffixes used in App.css
const VERDICT_BADGE_CLASS = {
  Supported:        "badge-Supported",
  Contradicted:     "badge-Contradicted",
  Incomplete:       "badge-Incomplete",
  "Not Verifiable": "badge-Not-Verifiable",
};

export default function ResultCard({ result, index }) {
  const { claim, topic, verdict, verdict_emoji, reason, source } = result;

  // Normalize topic label for display (underscores → spaces, title case)
  const topicLabel = topic
    ? topic.replace(/_/g, " ").toUpperCase()
    : "UNKNOWN";

  const badgeClass = VERDICT_BADGE_CLASS[verdict] || "badge-Not-Verifiable";

  return (
    <div
      className="result-card"
      data-verdict={verdict}
      style={{ animationDelay: `${index * 0.06}s` }}
    >
      {/* ── Card Header: claim text + verdict badge ── */}
      <div className="card-header">
        <p className="card-claim">
          <span className="claim-index">{String(index + 1).padStart(2, "0")}.</span>{" "}
          {claim}
        </p>
        <span className={`card-verdict-badge ${badgeClass}`}>
          {verdict_emoji} {verdict.toUpperCase()}
        </span>
      </div>

      {/* ── Card Body: reason ── */}
      <div className="card-reason-row">
        <span className="card-topic-tag">{topicLabel}</span>
        <p className="card-reason">{reason}</p>
      </div>

      {/* ── Card Footer: source citation ── */}
      {source && source.name && (
        <div className="card-source">
          <span className="source-icon">⊕</span>
          <span className="source-label">SOURCE</span>
          {source.url ? (
            <a
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="source-link"
              title={source.url}
            >
              {source.name}
              <span className="source-arrow">↗</span>
            </a>
          ) : (
            <span className="source-name">{source.name}</span>
          )}
        </div>
      )}
    </div>
  );
}