"""
Text Audit Pipeline — network extraction, regex parsing, unittest assertions, JSON logging.

Architecture:
  SecureNetworkLayer      — urllib fetch with mock:// and error failover
  TextAuditorEngine       — regex-based metric extraction into typed dict
  DynamicLatticeTestHarness — unittest assertions against extracted metrics
  JSONResultReportingHook — structured JSON telemetry sink

Usage:
    python text_audit_pipeline.py
    # or import and call execute_robust_pipeline(url, fallback_text)

Test contract (DynamicLatticeTestHarness):
  baseline_coherence_time  <= 2.0 s
  max_coherence_time       >= 5.0 s  (only when is_quasi_periodic)
  qubit_count              == 10
  hyperbolic_count         <= 1
"""

import json
import re
import unittest
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# =============================================================================
# SecureNetworkLayer
# =============================================================================

class SecureNetworkLayer:
    """urllib fetch with mock:// passthrough and automatic error failover."""

    @staticmethod
    def fetch_article(url: str, mock_fallback_text: str = "") -> str:
        if url.startswith("mock://") or not url:
            return mock_fallback_text
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TokenAuditor/1.0"},
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode("utf-8", errors="ignore")
        except (urllib.error.URLError, urllib.error.HTTPError) as err:
            print(f"[Network Warning] Connection failed: {err}. Executing local fallback.")
            return mock_fallback_text


# =============================================================================
# TextAuditorEngine
# =============================================================================

class TextAuditorEngine:
    """Deterministic regex extraction into a typed metrics dict."""

    HYPERBOLIC_KEYWORDS = [
        "unbreakable",
        "shielding errors",
        "two time dimensions",
        "absolute immunity",
        "impenetrable",
    ]

    def __init__(self, target_text: str):
        self.text = target_text
        self.metrics: Dict[str, Any] = {}

    def execute_audit(self) -> Dict[str, Any]:
        # Baseline coherence time — requires explicit "second" / "-second" vocabulary
        baseline_match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:-second|second)", self.text, re.IGNORECASE
        )
        self.metrics["baseline_coherence_time"] = (
            float(baseline_match.group(1)) if baseline_match else None
        )

        # Max coherence time — explicit phrase first, fall back to second time mention
        max_match = re.search(
            r"(?:length of the experiment, about|extended to|up to)\s*(\d+(?:\.\d+)?)",
            self.text,
            re.IGNORECASE,
        )
        if max_match:
            self.metrics["max_coherence_time"] = float(max_match.group(1))
        else:
            all_times = re.findall(
                r"(\d+(?:\.\d+)?)\s*(?:-second|second)", self.text, re.IGNORECASE
            )
            self.metrics["max_coherence_time"] = (
                float(all_times[1]) if len(all_times) >= 2 else None
            )

        # Qubit / ion count
        ion_match = re.search(r"(\d+)\s*(?:-ion|Yb\+|qubit)", self.text, re.IGNORECASE)
        self.metrics["qubit_count"] = int(ion_match.group(1)) if ion_match else None

        # Hyperbolic language audit
        detected = [kw for kw in self.HYPERBOLIC_KEYWORDS if kw in self.text.lower()]
        self.metrics["hyperbolic_count"] = len(detected)
        self.metrics["detected_hyperbole_list"] = detected

        # Quasi-periodic / Fibonacci signal
        self.metrics["is_quasi_periodic"] = (
            "quasi-periodic" in self.text.lower() or "fibonacci" in self.text.lower()
        )

        return self.metrics


# =============================================================================
# DynamicLatticeTestHarness
# =============================================================================

class DynamicLatticeTestHarness(unittest.TestCase):
    """Runtime assertions against the metrics ledger populated by TextAuditorEngine."""

    metrics_ledger: Dict[str, Any] = {}

    def test_baseline_duration_bounds(self):
        val = self.metrics_ledger.get("baseline_coherence_time")
        self.assertIsNotNone(val, "Baseline coherence time missing from text data.")
        self.assertLessEqual(
            val, 2.0, f"Baseline coherence ({val}s) exceeds expected physical limits."
        )

    def test_quasiperiodic_gain_threshold(self):
        if self.metrics_ledger.get("is_quasi_periodic"):
            val = self.metrics_ledger.get("max_coherence_time")
            self.assertIsNotNone(val, "Maximum coherence time missing from text data.")
            self.assertGreaterEqual(
                val, 5.0, f"Coherence scaling ({val}s) drops below target boundary."
            )

    def test_ion_chain_capacity(self):
        val = self.metrics_ledger.get("qubit_count")
        self.assertIsNotNone(val, "Qubit element count missing from text data.")
        self.assertEqual(val, 10, f"Qubit register size discrepancy. Found {val}, expected 10.")

    def test_linguistic_rigor_index(self):
        count = self.metrics_ledger.get("hyperbolic_count", 0)
        self.assertLessEqual(
            count, 1, f"Document failed strict peer-review audit. Hyperbolic load count: {count}"
        )


# =============================================================================
# JSONResultReportingHook
# =============================================================================

class JSONResultReportingHook:
    """Structured JSON telemetry sink for pipeline execution results."""

    def __init__(self, target_url: str, metrics: Dict[str, Any]):
        self.report: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_url": target_url,
            "extracted_metrics": metrics,
            "test_results": {"suite_passed": True, "failures": []},
        }

    def log_failure(self, test_name: str, error_message: str) -> None:
        self.report["test_results"]["suite_passed"] = False
        self.report["test_results"]["failures"].append(
            {"test_case": test_name, "error": error_message}
        )

    def write_to_disk(self, filename: str = "audit_telemetry.json") -> str:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2)
        return json.dumps(self.report, indent=2)


# =============================================================================
# Orchestration
# =============================================================================

def execute_robust_pipeline(target_url: str, fallback_payload: str) -> Dict[str, Any]:
    """Full pipeline: fetch → extract → test → JSON log."""
    raw_text = SecureNetworkLayer.fetch_article(target_url, fallback_payload)
    metrics  = TextAuditorEngine(raw_text).execute_audit()
    logger   = JSONResultReportingHook(target_url, metrics)

    DynamicLatticeTestHarness.metrics_ledger = metrics
    suite  = unittest.TestLoader().loadTestsFromTestCase(DynamicLatticeTestHarness)
    result = unittest.TestResult()
    suite.run(result)

    for failure in result.failures:
        logger.log_failure(failure[0].id().split(".")[-1], failure[1].strip())
    for error in result.errors:
        logger.log_failure(error[0].id().split(".")[-1], error[1].strip())

    safe_name   = target_url.split("://")[-1].replace(".", "_")
    json_output = logger.write_to_disk(f"audit_{safe_name}.json")

    print(f"\n=== TELEMETRY: {target_url} ===")
    print(json_output)
    print("=" * 72)

    return logger.report


# =============================================================================
# Demo payloads
# =============================================================================

if __name__ == "__main__":
    rigorous_payload = (
        "10 Yb+ hyperfine qubits in H1. "
        "Periodic baseline: 1.5 seconds. "
        "Fibonacci pattern extended to 5.5 seconds."
    )
    execute_robust_pipeline("mock://quantum_nature_review", rigorous_payload)

    marketing_payload = (
        "Our 10-ion qubit chain features an unbreakable barrier and two time dimensions. "
        "Smashed the periodic 1.5s clock up to 5.5s!"
    )
    execute_robust_pipeline("mock://quantum_marketing_press", marketing_payload)
