// frontend/src/App.js
// Root component — manages state and calls the Flask backend.

import React, { useState } from "react";
import InputPanel from "./components/InputPanel";
import ResultsList from "./components/ResultsList";
import SummaryBar from "./components/SummaryBar";
import "./App.css";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:5000";

// Example text pre-filled so users can try immediately
const EXAMPLE_TEXT =
  "Binary search works on any list and runs in O(log n). " +
  "A stack follows FIFO ordering. " +
  "Hash tables always guarantee O(1) lookup time. " +
  "Queues are used in breadth-first search and process elements in FIFO order.";

export default function App() {
  const [inputText, setInputText] = useState(EXAMPLE_TEXT);
  const [results, setResults]     = useState(null);
  const [rejected, setRejected]   = useState([]);
  const [summary, setSummary]     = useState(null);
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState(null);
  const [stage, setStage]         = useState(null); // current pipeline stage label

  const STAGES = [
    "Extracting claims...",
    "Filtering verifiable claims...",
    "Matching to knowledge base...",
    "Running verification engine...",
    "Formatting results...",
  ];

  /**
   * Simulate pipeline stage updates while waiting for the backend.
   * The backend runs all stages server-side; this just gives the user
   * visual feedback that work is happening.
   */
  const runStagedAnimation = () => {
    let i = 0;
    setStage(STAGES[0]);
    const interval = setInterval(() => {
      i += 1;
      if (i < STAGES.length) {
        setStage(STAGES[i]);
      } else {
        clearInterval(interval);
      }
    }, 1200);
    return interval;
  };

  const handleVerify = async () => {
    if (!inputText.trim()) return;

    setLoading(true);
    setError(null);
    setResults(null);
    setRejected([]);
    setSummary(null);

    const stageInterval = runStagedAnimation();

    try {
      const response = await fetch(`${BACKEND_URL}/verify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText }),
      });

      const data = await response.json();
      clearInterval(stageInterval);
      setStage(null);

      if (!response.ok) {
        setError(data.error || "Verification failed. Check backend logs.");
        return;
      }

      setResults(data.results || []);
      setRejected(data.rejected || []);
      setSummary(data.summary || null);
    } catch (err) {
      clearInterval(stageInterval);
      setStage(null);
      setError(
        "Cannot reach the backend. Make sure Flask is running on port 5000."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setInputText("");
    setResults(null);
    setRejected([]);
    setSummary(null);
    setError(null);
    setStage(null);
  };

  return (
    <div className="app">
      {/* ── Header ── */}
      <header className="app-header">
        <div className="header-inner">
          <div className="logo-block">
            <span className="logo-bracket">[</span>
            <span className="logo-text">HAQ</span>
            <span className="logo-bracket">]</span>
            <span className="logo-sub">ENGINE</span>
          </div>
          <p className="header-tagline">
            LLM Claim Verification System(CS FUndamentals) &nbsp;·&nbsp; v1.0
          </p>
        </div>
        <div className="header-status">
          <span className="status-dot" />
          <span className="status-label">SYSTEM ONLINE</span>
        </div>
      </header>

      {/* ── Main Content ── */}
      <main className="app-main">
        {/* Input Section */}
        <section className="section-input">
          <div className="section-label">
            <span className="section-num">01</span>
            INPUT &mdash; LLM-GENERATED TEXT
          </div>
          <InputPanel
            value={inputText}
            onChange={setInputText}
            onVerify={handleVerify}
            onReset={handleReset}
            loading={loading}
          />
        </section>

        {/* Pipeline Status */}
        {loading && stage && (
          <div className="pipeline-status">
            <div className="pipeline-spinner" />
            <span className="pipeline-stage">{stage}</span>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠</span>
            <span>{error}</span>
          </div>
        )}

        {/* Results Section */}
        {results !== null && !loading && (
          <>
            {summary && (
              <section className="section-summary">
                <div className="section-label">
                  <span className="section-num">02</span>
                  VERIFICATION SUMMARY
                </div>
                <SummaryBar summary={summary} />
              </section>
            )}

            <section className="section-results">
              <div className="section-label">
                <span className="section-num">03</span>
                CLAIM VERDICTS
              </div>
              <ResultsList results={results} rejected={rejected} />
            </section>
          </>
        )}
      </main>

      {/* ── Footer ── */}
      <footer className="app-footer">
        <span>HAQ ENGINE &copy; 2025</span>
        <span className="footer-sep">|</span>
        <span>Powered by Groq + LLaMA</span>
        <span className="footer-sep">|</span>
        <span>Flask + React</span>
      </footer>
    </div>
  );
}