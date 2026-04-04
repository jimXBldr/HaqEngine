// frontend/src/components/SummaryBar.js
// Displays aggregate verdict counts as a stat grid.

import React from "react";

export default function SummaryBar({ summary }) {
  if (!summary) return null;

  const { verdict_counts, total_verified, total_rejected, total_claims_extracted } = summary;

  const stats = [
    {
      value: total_claims_extracted,
      label: "Claims Extracted",
      className: "stat-total",
    },
    {
      value: total_verified,
      label: "Verified",
      className: "stat-total",
    },
    {
      value: verdict_counts.Supported,
      label: "Supported",
      className: "stat-supported",
    },
    {
      value: verdict_counts.Contradicted,
      label: "Contradicted",
      className: "stat-contradicted",
    },
    {
      value: verdict_counts.Incomplete,
      label: "Incomplete",
      className: "stat-incomplete",
    },
    {
      value: verdict_counts["Not Verifiable"],
      label: "Not Verifiable",
      className: "stat-nv",
    },
    {
      value: total_rejected,
      label: "Rejected",
      className: "stat-rejected",
    },
  ];

  return (
    <div className="summary-bar">
      {stats.map((s) => (
        <div className="summary-stat" key={s.label}>
          <span className={`stat-value ${s.className}`}>{s.value}</span>
          <span className="stat-label">{s.label}</span>
        </div>
      ))}
    </div>
  );
}