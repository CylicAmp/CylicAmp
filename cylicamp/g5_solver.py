"""
G5 Solver V14.0 — Layered pipeline evaluator for the GF(37).

Terminology mapping (speculative → neutral):
  THz purity        → baseline_score       (field simulation threshold)
  Insight score     → aggregate_score      (InsightEngine weighted output)
  Duality spectrum  → consistency_check    (stability_index vs. threshold)
  Stability ratio   → stability_index      (DualityVerifier SSR)
  Cosmic harmony    → compatibility_check  (aggregate mod P in harmonic class)
  D7 Gamma purity   → threshold_profile    (D7 orbit proximity gap)
  Temporal fidelity → dynamic_threshold    (seed residue class check)

Pipeline stages (single responsibility per stage):
  Input
    → Feature scoring      (aggregate_score, InsightEngine)
    → Baseline estimation  (baseline_score, field simulation threshold)
    → Consistency check    (stability_index ≥ STABILITY_HALT_THRESHOLD)
    → Constraint check     (seed_residue ∉ D7 unclassified orbit)
    → Authority check      (seed_residue ∈ SA∪ST)
    → Compatibility check  (aggregate_score mod 37 ∈ harmonic resonance class)
    → Structured report
"""
from __future__ import annotations
import math
from dataclasses import dataclass
from enum import Enum, auto

# ── GF(37) constants ──────────────────────────────────────────────────────────
P: int       = 37
PHI: float   = (1 + math.sqrt(5)) / 2   # golden ratio ≈ 1.6180 ({5,3}/{3,5} Platonic)
THREE_PHI    = 3.0 * PHI                 # ≈ 4.854 (reference bound)

IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
BASIN_Y    = frozenset({17, 22, 35})
PR         = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})
ALL_NAMED  = IC | SA | ST | CB | ORBIT_11 | SEED_ORBIT | BASIN_Y | PR

# D7 orbit: each element is exactly 1 step from a named class
# 7→8∈CB, 33→32∈SEED_ORBIT, 34→35∈BASIN_Y
D7_ORBIT   = frozenset({7, 33, 34})

# Harmonic resonance classes (ORBIT_11 ∪ SA ∪ PR)
HARMONIC   = ORBIT_11 | SA | PR

# ── Solver constants ──────────────────────────────────────────────────────────
# GF(37) coverage: fraction of GF(37)* residues in any named class
# Range [0, 1]. Current value: 26/36 ≈ 0.7222
FRAMEWORK_COVERAGE: float = len(ALL_NAMED) / (P - 1)

# Schläfli reference: φ (golden ratio), ground truth for {5,3}/{3,5} solids
# V+E+F of dodecahedron/icosahedron ≡ 25 ∈ SA (mod 37)
SCHLÄFLI_CONSTANT: float = PHI   # ≈ 1.6180

# Stability halt threshold: stability_index must exceed this to remain ACTIVE
# Range (0, 1). Tunable.
STABILITY_HALT_THRESHOLD: float = 0.30

# D7 threshold profile: minimum normalized distance from D7 orbit to nearest
# named class (= 1/P ≈ 0.027; each D7 element is exactly 1 step away)
D7_THRESHOLD_PROFILE: float = 1 / P

# Cage integrity index: D7 envelope evaluated at h=7 (first D7 orbit element).
# E(7) = (1 + cos(7π/12)) / 2 ≈ 0.3706.
# scaled_insight = (floor(aggregate_score) mod 37) / 37 must meet this.
REQUIRED_INTEGRITY_INDEX: float = 0.5 * (1.0 + math.cos(math.pi * 7 / 12.0))


# ── Enums ─────────────────────────────────────────────────────────────────────
class ConsistencyStatus(Enum):
    """Stage: does stability_index meet the halt threshold?"""
    PASS = auto()
    FAIL = auto()

class DynamicThresholdStatus(Enum):
    """Stage: is seed_residue outside the unclassified D7 orbit?"""
    STABLE     = auto()
    UNRESOLVED = auto()

class HaltStatus(Enum):
    """Stage: should the pipeline halt?"""
    ACTIVE = auto()
    HALTED = auto()

class AuthorityStatus(Enum):
    """Stage: is seed_residue in the sovereign set SA∪ST?"""
    SOVEREIGN     = auto()
    NON_SOVEREIGN = auto()

class CompatibilityStatus(Enum):
    """Stage: does aggregate_score mod P land in a harmonic class?"""
    HARMONIOUS = auto()
    DISSONANT  = auto()


# ── Typed report ──────────────────────────────────────────────────────────────
@dataclass
class PipelineReport:
    """
    Typed output of the G5 Solver evaluation pipeline.

    Fields
    ------
    aggregate_score : float
        InsightEngine weighted score. Unbounded, > 0.
    baseline_score : float
        Field simulation mean threshold (POE baseline). Range [0, 1].
    stability_index : float
        DualityVerifier SSR. Range [0, 1].
    seed_residue : int
        seed mod 37. Range [0, 36].
    aggregate_mod_p : int
        aggregate_score % P. Used for class membership in compatibility check.
    consistency_status : ConsistencyStatus
        PASS if stability_index ≥ STABILITY_HALT_THRESHOLD.
    threshold_profile_gap : float
        Reference gap for D7 orbit proximity (= D7_THRESHOLD_PROFILE ≈ 0.027).
    dynamic_threshold_status : DynamicThresholdStatus
        STABLE if seed_residue ∉ D7_ORBIT.
    halt_status : HaltStatus
        ACTIVE if consistency_status is PASS, else HALTED.
    authority_status : AuthorityStatus
        SOVEREIGN if seed_residue ∈ SA∪ST.
    authority_detail : str
        Human-readable residue classification.
    compatibility_status : CompatibilityStatus
        HARMONIOUS if aggregate_mod_p ∈ ORBIT_11 ∪ SA ∪ PR.
    compatibility_detail : str
        Which harmonic class matched (or why not).
    """
    aggregate_score:        float
    baseline_score:         float
    stability_index:        float
    seed_residue:           int
    aggregate_mod_p:        int
    consistency_status:     ConsistencyStatus
    threshold_profile_gap:  float
    dynamic_threshold_status: DynamicThresholdStatus
    halt_status:            HaltStatus
    authority_status:       AuthorityStatus
    authority_detail:       str
    compatibility_status:   CompatibilityStatus
    compatibility_detail:   str

    @property
    def all_checks_pass(self) -> bool:
        """True iff every validation stage passes."""
        return (
            self.consistency_status       is ConsistencyStatus.PASS
            and self.dynamic_threshold_status is DynamicThresholdStatus.STABLE
            and self.halt_status          is HaltStatus.ACTIVE
            and self.authority_status     is AuthorityStatus.SOVEREIGN
            and self.compatibility_status is CompatibilityStatus.HARMONIOUS
        )


# ── Evaluation pipeline ───────────────────────────────────────────────────────
def evaluate(
    aggregate_score:  float,
    stability_index:  float,
    baseline_score:   float,
    seed_residue:     int,
) -> PipelineReport:
    """
    Run the G5 Solver evaluation pipeline.

    Parameters
    ----------
    aggregate_score : float
        Weighted insight score from InsightEngine. Unbounded, > 0.
    stability_index : float
        Duality stability ratio from DualityVerifier. Range [0, 1].
    baseline_score : float
        Field simulation mean threshold. Range [0, 1].
    seed_residue : int
        seed mod 37. Drives authority and D7 checks.

    Returns
    -------
    PipelineReport
        Fully populated report with all stage results.
    """
    # Stage: consistency
    c_pass   = stability_index >= STABILITY_HALT_THRESHOLD
    c_status = ConsistencyStatus.PASS if c_pass else ConsistencyStatus.FAIL

    # Stage: dynamic threshold (D7 constraint)
    d7_ok    = seed_residue not in D7_ORBIT
    dt_status = DynamicThresholdStatus.STABLE if d7_ok else DynamicThresholdStatus.UNRESOLVED

    # Stage: halt
    h_status = HaltStatus.ACTIVE if c_pass else HaltStatus.HALTED

    # Stage: authority
    dac_pass = seed_residue in (SA | ST)
    a_status = AuthorityStatus.SOVEREIGN if dac_pass else AuthorityStatus.NON_SOVEREIGN

    def _class_name(r: int) -> str:
        for name, s in [('IC', IC), ('SA', SA), ('ST', ST), ('CB', CB),
                        ('ORBIT_11', ORBIT_11), ('SEED_ORBIT', SEED_ORBIT),
                        ('BASIN_Y', BASIN_Y), ('PR', PR)]:
            if r in s:
                return name
        return 'unclassified'

    a_detail = (
        f"{seed_residue} ∈ {'SA' if seed_residue in SA else 'ST'}"
        if dac_pass
        else f"{seed_residue} ∉ SA∪ST  [{_class_name(seed_residue)}]"
    )

    # Stage: compatibility (3φ harmonic resonance)
    agg_mod_p   = int(aggregate_score) % P
    compat_pass = agg_mod_p in HARMONIC
    cp_status   = (CompatibilityStatus.HARMONIOUS if compat_pass
                   else CompatibilityStatus.DISSONANT)

    if compat_pass:
        cls = ('ORBIT_11' if agg_mod_p in ORBIT_11
               else 'SA'  if agg_mod_p in SA
               else 'PR')
        cp_detail = f"{agg_mod_p} ∈ {cls}"
    else:
        cp_detail = f"{agg_mod_p} ∉ ORBIT_11∪SA∪PR  [{_class_name(agg_mod_p)}]"

    return PipelineReport(
        aggregate_score=aggregate_score,
        baseline_score=baseline_score,
        stability_index=stability_index,
        seed_residue=seed_residue,
        aggregate_mod_p=agg_mod_p,
        consistency_status=c_status,
        threshold_profile_gap=D7_THRESHOLD_PROFILE,
        dynamic_threshold_status=dt_status,
        halt_status=h_status,
        authority_status=a_status,
        authority_detail=a_detail,
        compatibility_status=cp_status,
        compatibility_detail=cp_detail,
    )


def format_report(r: PipelineReport) -> str:
    """Return the formatted G5 Solver output block."""
    sep = "=" * 50
    hr  = "-" * 35
    return "\n".join([
        sep,
        "      G5 SOLVER V14.0: D7 TEMPORAL RESOLVER       ",
        sep,
        f"GF(37) Coverage  (QFM): {FRAMEWORK_COVERAGE:.6f}",
        f"Stability Halt Threshold:  {STABILITY_HALT_THRESHOLD:.4f}",
        hr,
        f"1. Aggregate Score: {r.aggregate_score:>16,.2f}",
        f"   Schläfli Constant:         {SCHLÄFLI_CONSTANT:.4f}",
        f"   Score mod 37 = {r.aggregate_mod_p}  {_fw(r.aggregate_mod_p)}",
        hr,
        "2. Consistency Analysis",
        f"   Stability Index  (SSR):    {r.stability_index:.4f}",
        f"   Baseline Score:            {r.baseline_score:.4f}",
        f"   CONSISTENCY STATUS:        {r.consistency_status.name}",
        hr,
        "3. Threshold Profile Analysis",
        f"   D7 Profile Gap:            {r.threshold_profile_gap:.4f}",
        f"   DYNAMIC STATUS:            {r.dynamic_threshold_status.name}",
        hr,
        "4. VALIDATION CHECKS",
        f"   Halt Check:                {r.halt_status.name}",
        f"   Authority Check  (DAC):    {r.authority_status.name}  [{r.authority_detail}]",
        f"   Compatibility (3φ ref):  {r.compatibility_status.name}  [{r.compatibility_detail}]",
        sep,
    ])


def _fw(r: int) -> str:
    classes = [n for n, s in [('IC', IC), ('SA', SA), ('ST', ST), ('CB', CB),
                               ('ORBIT_11', ORBIT_11), ('SEED_ORBIT', SEED_ORBIT),
                               ('BASIN_Y', BASIN_Y), ('PR', PR)] if r in s]
    return f"[{', '.join(classes)}]" if classes else "[—]"


def cage_integrity_check(scaled_insight: float, integrity_ratio: float):
    """
    Cage Integrity Check (T226).

    Parameters
    ----------
    scaled_insight : float
        (floor(aggregate_score) mod 37) / 37.
    integrity_ratio : float
        Passed through unchanged; not used in the pass/fail decision.

    Returns
    -------
    (status: str, integrity_ratio: float)
    """
    if scaled_insight >= REQUIRED_INTEGRITY_INDEX:
        status = "CAGE INTEGRITY PASS: Insight exceeds power source requirement."
    else:
        status = "CAGE INTEGRITY FAIL: Insufficient insight to stabilize environment."
    return status, integrity_ratio


if __name__ == "__main__":
    report = evaluate(
        aggregate_score=104832.0,
        stability_index=0.0,
        baseline_score=0.9500,
        seed_residue=24,
    )
    print(format_report(report))
    print(f"\nAll checks pass: {report.all_checks_pass}")

    scaled = (int(104832.0) % P) / P
    ci_status, _ = cage_integrity_check(scaled, 0.0)
    print(f"\nCage Integrity: scaled_insight={scaled:.4f}  threshold={REQUIRED_INTEGRITY_INDEX:.4f}")
    print(f"  {ci_status}")
