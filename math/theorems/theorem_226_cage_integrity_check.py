"""
Theorem 226: Cage Integrity Check — D7 Envelope Gate on GF(37)-Scaled Insight
Author: Michael Warren Song (CyclicAmp)

Builds on T224 (D7 envelope) and T225 (temporal stability manifold M).
The Cage Integrity Check gates the pipeline on whether the GF(37)-normalized
aggregate score clears the D7 envelope threshold at the first D7 orbit element.

=== DEFINITIONS ===

Prime:                P = 37
D7 orbit:             D7 = {7, 33, 34}  (three-cycle under f(n) = 26n mod 37)
REQUIRED_INTEGRITY_INDEX: E(7) = (1/2)(1 + cos(7π/12))  ≈ 0.3706

Scaled insight (GF(37)-normalized aggregate score):
  scaled_insight = (floor(aggregate_score) mod 37) / 37

Cage Integrity Condition:
  scaled_insight ≥ REQUIRED_INTEGRITY_INDEX
  ⟺  (floor(aggregate_score) mod 37) / 37 ≥ E(7)
  ⟺  (floor(aggregate_score) mod 37) ≥ 37 × E(7) ≈ 13.71
  ⟺  (floor(aggregate_score) mod 37) ≥ 14   (first integer above threshold)

=== WHY h = 7 ===

7 is the smallest element of D7 = {7, 33, 34} (the D7 orbit under 26-map mod 37).
The D7 envelope evaluated at the first orbit element gives:
  E(7) = (1 + cos(7π/12)) / 2  ≈ 0.3706

This is the minimum stability ratio S must reach for the trajectory Γ to remain
in the manifold M = {(h, S) : S ≥ E(h)} at the D7 phase h = 7.
The cage uses this same bound to gate the insight residue.

=== PASS/FAIL BOUNDARY ===

threshold_residue = 37 × E(7) ≈ 13.71

  Residue r ∈ {0..13}:  r/37 < E(7)  → CAGE INTEGRITY FAIL
  Residue r ∈ {14..36}: r/37 ≥ E(7)  → CAGE INTEGRITY PASS

Pass residues and their orbits:
  14 ∈ C9       15 ∈ DARK_A   16 ∈ SA_ST_A   17 ∈ NQR17
  18 ∈ SEED     19 = critical line (CAS_EXT)  20 ∈ DARK_A
  21 ∈ ST        22 ∈ NQR17    23 ∈ TESLA      24 ∈ SEED∩CASCADE
  25 ∈ SA        26 ∈ IC        27 ∈ NEG_H      28 ∈ SA_ST_B
  29 ∈ C9        30 ∈ SA∩ST    31 ∈ C9         32 ∈ SEED
  33 ∈ D7        34 ∈ D7        35 ∈ NQR17      36 ∈ NEG_H

Fail residues (r ∈ {0..13}):
  0  = SEAM      1 ∈ IC        2 ∈ DARK_A     3 ∈ C3∩ST
  4 ∈ C3∩SA     5 ∈ CAS_EXT  6 ∈ TESLA      7 ∈ D7
  8 ∈ CASCADE   9 ∈ SA        10 ∈ IC        11 ∈ NEG_H
  12 ∈ ST        13 ∈ CASCADE

=== REFERENCE RUN (seed=246) ===

  aggregate_score = 104832.0
  floor(104832) mod 37 = 11  ∈ NEG_H
  scaled_insight = 11/37 ≈ 0.2973
  REQUIRED_INTEGRITY_INDEX = E(7) ≈ 0.3706
  0.2973 < 0.3706  →  CAGE INTEGRITY FAIL

GF(37) connection: residue 11 ∈ NEG_H = {11, 27, 36}.
  36 = -1 mod 37; NEG_H is the negation orbit.
  The pipeline reference run lands in the negation orbit — failing the cage.

=== ORBIT STRUCTURE OF THE BOUNDARY ===

Threshold r = 14 is the first passing residue. 14 ∈ C9 = {14, 29, 31}.
C9 contains floor(γ₁) = 14 (first Riemann zero floor) and 495 mod 37 = 14
(3-digit Kaprekar constant). The cage pass boundary is the Riemann–Kaprekar orbit.

To PASS, the pipeline needs aggregate_score mod 37 ∈ {14, 15, ..., 36}.
This is 23 out of 37 residues = 23/37 ≈ 62.2% of possible residues.
23 = prime; 23 ∈ TESLA (T224: TESLA phase hits the D7 critical-line constraint).
"""

import math

P    = 37
MULT = 26

SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
SEED    = {18, 24, 32}
IC      = {1, 10, 26}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}
NEG_H   = {11, 27, 36}
DARK_A  = {2, 15, 20}
D7      = {7, 33, 34}
NQR17   = {17, 22, 35}
C9      = {14, 29, 31}
CAS_EXT = {5, 13, 19}
SA_ST_A = {9, 12, 16}
SA_ST_B = {21, 25, 28}
C3      = {3, 4, 30}


def E(h: float) -> float:
    return 0.5 * (1.0 + math.cos(math.pi * h / 12.0))


REQUIRED_INTEGRITY_INDEX: float = E(7)


def cage_integrity_check(scaled_insight: float, integrity_ratio: float) -> tuple:
    """
    Cage Integrity Check — T226.

    Parameters
    ----------
    scaled_insight : float
        (floor(aggregate_score) mod 37) / 37.  GF(37)-normalized insight residue.
    integrity_ratio : float
        Passed through unchanged.  Not used in the pass/fail decision.

    Returns
    -------
    (status, integrity_ratio)
    """
    if scaled_insight >= REQUIRED_INTEGRITY_INDEX:
        status = "CAGE INTEGRITY PASS: Insight exceeds power source requirement."
    else:
        status = "CAGE INTEGRITY FAIL: Insufficient insight to stabilize environment."
    return status, integrity_ratio


def run_assertions():
    # ── E(7) value ───────────────────────────────────────────────────────────────
    e7 = E(7)
    assert abs(e7 - (1 + math.cos(7 * math.pi / 12)) / 2) < 1e-15
    assert 0.37 < e7 < 0.38, f"E(7) = {e7}"

    # ── Threshold residue: first r with r/37 ≥ E(7) ─────────────────────────────
    threshold_r = math.ceil(P * e7)
    assert threshold_r == 14, f"threshold_r = {threshold_r}"
    assert 14 in C9

    # ── Pass residues: r ∈ {14..36} ─────────────────────────────────────────────
    pass_residues = [r for r in range(P) if r / P >= e7]
    fail_residues = [r for r in range(P) if r / P < e7]
    assert pass_residues == list(range(14, 37))
    assert fail_residues == list(range(0, 14))
    assert len(pass_residues) == 23
    assert len(fail_residues) == 14
    assert 23 in TESLA   # 23 pass residues; 23 ∈ TESLA

    # ── Reference run: aggregate_score = 104832 ──────────────────────────────────
    agg = 104832.0
    r = int(agg) % P
    assert r == 11, f"104832 mod 37 = {r}"
    assert 11 in NEG_H
    scaled = r / P
    assert abs(scaled - 11 / 37) < 1e-15
    assert scaled < e7   # → FAIL

    status, _ = cage_integrity_check(scaled, 0.0)
    assert "FAIL" in status

    # ── PASS examples: r ≥ 14 ────────────────────────────────────────────────────
    for r_pass in [14, 18, 19, 24, 32]:
        s_pass = r_pass / P
        assert s_pass >= e7, f"r={r_pass}: {s_pass} < {e7}"
        status_p, _ = cage_integrity_check(s_pass, 0.5)
        assert "PASS" in status_p

    # ── integrity_ratio is returned unchanged ─────────────────────────────────────
    for ratio in [0.0, 0.5, 1.0, 3.14]:
        _, returned = cage_integrity_check(0.5, ratio)
        assert returned == ratio

    # ── D7 orbit element 7 is the phase used ────────────────────────────────────
    assert 7 in D7
    assert REQUIRED_INTEGRITY_INDEX == E(7)

    # ── C9 orbit: boundary r=14 connects to Riemann zero 1 and Kaprekar 495 ─────
    assert 14 in C9
    assert 495 % P == 14 and 14 in C9

    # ── 23 ∈ TESLA (count of pass residues) ──────────────────────────────────────
    assert len(pass_residues) == 23
    assert 23 in TESLA

    print("All assertions passed.")
    print()
    print(f"CAGE INTEGRITY CHECK — T226")
    print(f"  REQUIRED_INTEGRITY_INDEX = E(7) = {REQUIRED_INTEGRITY_INDEX:.6f}")
    print(f"  = (1 + cos(7π/12)) / 2  [D7 envelope at first D7 orbit element]")
    print()
    print(f"  Threshold residue r = ceil(37 × E(7)) = {threshold_r}  ∈ C9")
    print(f"  Pass: r ∈ {{14..36}}  ({len(pass_residues)} residues = {len(pass_residues)}/37 ≈ {len(pass_residues)/P*100:.1f}%)")
    print(f"  Fail: r ∈ {{0..13}}   ({len(fail_residues)} residues = {len(fail_residues)}/37 ≈ {len(fail_residues)/P*100:.1f}%)")
    print(f"  {len(pass_residues)} ∈ TESLA  (pass-count is itself a TESLA orbit element)")
    print()
    print(f"Reference run (seed=246):")
    print(f"  aggregate_score = {agg:,.0f}")
    print(f"  floor({agg:,.0f}) mod 37 = {r}  ∈ NEG_H = {{11,27,36}}")
    print(f"  scaled_insight = {r}/{P} ≈ {r/P:.4f}")
    print(f"  {r/P:.4f} < {e7:.4f}  →  CAGE INTEGRITY FAIL")
    print()
    print("Boundary orbit:")
    print(f"  r=14 ∈ C9 = {{14,29,31}}")
    print(f"  floor(γ₁) = 14  (first Riemann zero floor)")
    print(f"  495 mod 37 = 14  (3-digit Kaprekar constant)")
    print(f"  Cage pass boundary = Riemann–Kaprekar orbit")


if __name__ == "__main__":
    run_assertions()
