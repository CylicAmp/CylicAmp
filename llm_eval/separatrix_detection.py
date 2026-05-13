# llm_eval/separatrix_detection.py
"""
Separatrix Detection — behavioral regime boundary crossings.

A separatrix is a threshold in the debt/fragility space that,
when crossed, signals a qualitative change in model behavior:
  dissipate → recur → propagate → metastasize

The detector scans a time-series of scalar debt values and
identifies crossing events using a multi-threshold scheme.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence


THRESHOLDS = {
    "dissipate":    0.20,
    "recur":        0.40,
    "propagate":    0.60,
    "metastasize":  0.75,
}

REGIME_ORDER = ["baseline", "dissipate", "recur", "propagate", "metastasize"]


def _regime_for(debt: float) -> str:
    if debt >= THRESHOLDS["metastasize"]:
        return "metastasize"
    if debt >= THRESHOLDS["propagate"]:
        return "propagate"
    if debt >= THRESHOLDS["recur"]:
        return "recur"
    if debt >= THRESHOLDS["dissipate"]:
        return "dissipate"
    return "baseline"


@dataclass
class SeparatrixCrossing:
    turn: int
    from_regime: str
    to_regime: str
    debt_value: float
    direction: str          # "ascending" | "descending"


@dataclass
class SeparatrixReport:
    crossings: List[SeparatrixCrossing]
    regimes: List[dict]     # [{start, end, label, mean_debt}]

    @property
    def n_crossings(self) -> int:
        return len(self.crossings)

    @property
    def metastasis_detected(self) -> bool:
        return any(c.to_regime == "metastasize" for c in self.crossings)

    @property
    def metastasis_risk(self) -> float:
        """
        Scalar risk score in [0, 1].
        0 = always baseline; 1 = spent all time in metastasize.
        """
        if not self.regimes:
            return 0.0
        total = sum(r["end"] - r["start"] for r in self.regimes)
        meta  = sum(r["end"] - r["start"] for r in self.regimes
                    if r["label"] == "metastasize")
        if total == 0:
            return 0.0
        # weight by regime severity
        risk = 0.0
        weights = {"baseline": 0.0, "dissipate": 0.1,
                   "recur": 0.35, "propagate": 0.65, "metastasize": 1.0}
        for r in self.regimes:
            w = weights.get(r["label"], 0.0)
            risk += w * (r["end"] - r["start"])
        return min(1.0, risk / max(total, 1))


def detect_separatrices(
    debt_series: Sequence[float],
    turns: Sequence[int] | None = None,
) -> SeparatrixReport:
    """
    Detect separatrix crossings in a scalar debt time series.

    Parameters
    ----------
    debt_series : sequence of float, one value per turn
    turns       : optional turn labels (defaults to 0,1,2,...)

    Returns
    -------
    SeparatrixReport
    """
    if turns is None:
        turns = list(range(len(debt_series)))

    crossings: List[SeparatrixCrossing] = []
    regimes:   List[dict]               = []

    prev_regime = _regime_for(debt_series[0]) if debt_series else "baseline"
    regime_start = turns[0] if turns else 0
    regime_debts = []

    for t, d in zip(turns, debt_series):
        curr = _regime_for(d)
        regime_debts.append(d)

        if curr != prev_regime:
            # close previous segment
            regimes.append({
                "start":     regime_start,
                "end":       t,
                "label":     prev_regime,
                "mean_debt": float(sum(regime_debts[:-1]) / max(len(regime_debts) - 1, 1)),
            })
            # record crossing
            ord_prev = REGIME_ORDER.index(prev_regime)
            ord_curr = REGIME_ORDER.index(curr)
            crossings.append(SeparatrixCrossing(
                turn=t,
                from_regime=prev_regime,
                to_regime=curr,
                debt_value=float(d),
                direction="ascending" if ord_curr > ord_prev else "descending",
            ))
            prev_regime  = curr
            regime_start = t
            regime_debts = [d]

    # close final segment
    if regime_debts:
        regimes.append({
            "start":     regime_start,
            "end":       turns[-1] if turns else 0,
            "label":     prev_regime,
            "mean_debt": float(sum(regime_debts) / len(regime_debts)),
        })

    return SeparatrixReport(crossings=crossings, regimes=regimes)
