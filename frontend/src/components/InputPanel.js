// frontend/src/components/InputPanel.js
// Text input area + action buttons for submitting text to the verification pipeline.

import React from "react";

const MAX_CHARS = 10000;

export default function InputPanel({ value, onChange, onVerify, onReset, loading }) {
  const charCount = value.length;
  const overLimit = charCount > MAX_CHARS;

  return (
    <div className="input-panel">
      <div className="textarea-wrapper">
        <span className="input-label-corner">INPUT_TEXT</span>
        <textarea
          className="input-textarea"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Paste LLM-generated text here. The engine will extract claims, filter them, and verify each one against the knowledge base..."
          spellCheck={false}
          disabled={loading}
        />
        <span
          className="char-count"
          style={{ color: overLimit ? "var(--accent-red)" : undefined }}
        >
          {charCount.toLocaleString()} / {MAX_CHARS.toLocaleString()}
        </span>
      </div>

      <div className="input-actions">
        <button
          className="btn btn-secondary"
          onClick={onReset}
          disabled={loading || (!value && true)}
          title="Clear input and results"
        >
          RESET
        </button>
        <button
          className="btn btn-primary"
          onClick={onVerify}
          disabled={loading || !value.trim() || overLimit}
          title="Run the verification pipeline"
        >
          {loading ? (
            <>
              <span className="btn-spinner" />
              VERIFYING
            </>
          ) : (
            <>▶ VERIFY</>
          )}
        </button>
      </div>
    </div>
  );
}