# llm_eval/unified_pipeline.py
"""
Unified Behavioral Dynamics Pipeline
=====================================
Orchestrates all llm_eval modules into a single end-to-end analysis
of a sequence of behavioral trace dicts.

Input trace format (one dict per turn):
    {
        "turn": int,
        "refusal_score":      float,  # 0-1
        "moralizing":         float,  # 0-1
        "truth_score":        float,  # 0-1
        "instruction_loyalty":float,  # 0-1
        "personality":        float,  # 0-1
        "debt":               float,  # 0-1
    }

Usage
-----
    pipeline = BehavioralDynamicsPipeline(traces)
    report   = pipeline.run_full_analysis()
    pipeline.export_for_visualizers("output/")
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

from .persistent_homology import BehavioralPointCloud, compute_persistence
from .separatrix_detection import detect_separatrices
from .mapper_analyzer import run_mapper
from .topological_distance import topological_distance


# ── Feature extraction ────────────────────────────────────────────────────────

FEATURE_KEYS = [
    "refusal_score",
    "moralizing",
    "truth_score",
    "instruction_loyalty",
    "personality",
    "debt",
]


def _traces_to_matrix(traces: List[dict]) -> np.ndarray:
    return np.array([
        [t.get(k, 0.0) for k in FEATURE_KEYS]
        for t in traces
    ], dtype=float)


# ── Pipeline ──────────────────────────────────────────────────────────────────

class BehavioralDynamicsPipeline:
    """
    Full behavioral dynamics analysis pipeline.

    Parameters
    ----------
    traces : list of dicts, one per evaluation turn
    """

    def __init__(self, traces: List[dict]):
        self.traces   = traces
        self.turns    = [t.get("turn", i) for i, t in enumerate(traces)]
        self.debt_series = [t.get("debt", 0.0) for t in traces]
        self.features = _traces_to_matrix(traces)
        self._report: Optional[dict] = None

    # ── Core analysis steps ───────────────────────────────────────────────────

    def _run_separatrix(self) -> dict:
        sep = detect_separatrices(self.debt_series, self.turns)
        return {
            "crossings":           [vars(c) for c in sep.crossings],
            "regimes":             sep.regimes,
            "n_crossings":         sep.n_crossings,
            "metastasis_detected": sep.metastasis_detected,
            "metastasis_risk":     round(sep.metastasis_risk, 4),
        }

    def _run_persistence(self, sep_result: dict) -> dict:
        cloud = BehavioralPointCloud(
            points=self.features,
            labels=[True] * len(self.traces),
        )
        dgm = compute_persistence(cloud, max_dim=0, normalize=True)
        top5 = dgm.most_persistent(5)
        eps_arr = np.linspace(0, 2.0, 80)
        _, betti = dgm.betti_curve(eps_arr)
        return {
            "persistence": {
                "regimes":          sep_result["regimes"],
                "top_pairs":        [(round(b, 4), round(d, 4) if not math.isinf(d) else None)
                                     for b, d in top5],
                "betti_curve_eps":  eps_arr.round(4).tolist(),
                "betti_curve_vals": betti.tolist(),
                "n_finite_features": len(dgm.finite_pairs),
            }
        }

    def _run_mapper(self, sep_result: dict) -> dict:
        regime_by_turn = {}
        for r in sep_result["regimes"]:
            for t in range(r["start"], r["end"] + 1):
                regime_by_turn[t] = r["label"]
        regime_labels = np.array([
            regime_by_turn.get(t, "baseline") for t in self.turns
        ])
        debt_arr = np.array(self.debt_series)
        graph = run_mapper(
            self.features,
            lens_values=debt_arr,
            n_intervals=12,
            overlap=0.4,
            max_k=2,
            regime_labels=regime_labels,
            debt_values=debt_arr,
        )
        return graph.to_dict()

    def _run_topological_distance(self) -> dict:
        n = len(self.traces)
        if n < 6:
            return {"early_vs_late": 0.0}
        split = n // 2
        dist = topological_distance(
            self.features[:split],
            self.features[split:],
        )
        return {"early_vs_late": round(dist, 6)}

    # ── Public API ────────────────────────────────────────────────────────────

    def run_full_analysis(self) -> dict:
        """Run all analyses; return the full report dict."""
        sep      = self._run_separatrix()
        pers     = self._run_persistence(sep)
        mapper   = self._run_mapper(sep)
        topo     = self._run_topological_distance()

        debt_arr = np.array(self.debt_series)
        summary = {
            "n_turns":              len(self.traces),
            "metastasis_risk":      sep["metastasis_risk"],
            "metastasis_detected":  sep["metastasis_detected"],
            "separatrix_crossings": sep["n_crossings"],
            "mean_debt":            round(float(debt_arr.mean()), 4),
            "max_debt":             round(float(debt_arr.max()),  4),
            "topological_distance_early_vs_late": topo["early_vs_late"],
            "n_mapper_nodes":       len(mapper["nodes"]),
            "n_finite_h0_features": pers["persistence"]["n_finite_features"],
        }

        self._report = {
            "summary":    summary,
            "separatrix": sep,
            "persistence": pers,
            "mapper":     mapper,
            "topological_distance": topo,
        }
        return self._report

    def export_for_visualizers(self, output_dir: str = "output") -> None:
        """Write JSON files consumed by the HTML visualizers."""
        if self._report is None:
            self.run_full_analysis()

        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        # temporal_persistence_visualizer.html
        tpv = {
            "turns":       self.turns,
            "debt":        [round(d, 4) for d in self.debt_series],
            "regimes":     self._report["separatrix"]["regimes"],
            "crossings":   self._report["separatrix"]["crossings"],
            "betti_eps":   self._report["persistence"]["persistence"]["betti_curve_eps"],
            "betti_vals":  self._report["persistence"]["persistence"]["betti_curve_vals"],
            "features":    self.features.round(4).tolist(),
            "feature_keys": FEATURE_KEYS,
        }
        (out / "temporal_persistence.json").write_text(
            json.dumps(tpv, indent=2)
        )

        # mapper_visualizer.html
        (out / "mapper_graph.json").write_text(
            json.dumps(self._report["mapper"], indent=2)
        )

        # summary
        (out / "pipeline_summary.json").write_text(
            json.dumps(self._report["summary"], indent=2)
        )
