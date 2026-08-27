"""
Theorem 224: D7 Envelope — Stability Admissible Region in GF(37)
Author: Michael Warren Song (CyclicAmp)

=== DEFINITIONS ===

D7 envelope (24-periodic):
  E(h) = (1/2)(1 + cos(πh/12)),  h ∈ ℝ

Stability constraint:
  S ≥ E(h),  S ∈ [E(h), 1]

Admissible region:
  {(h, S) : S ∈ [E(h), 1]}  — band bounded below by E(h), above by 1.

=== GF(37) STRUCTURE OF THE ENVELOPE ===

PERIOD HIERARCHY mod 37:

  24 (period)       ≡ 24 mod 37 ∈ SEED ∩ CASCADE     DR = 6
  12 (half-period)  ≡ 12 mod 37 ∈ ST                 DR = 3
   6 (quarter-period) ≡ 6 mod 37 ∈ TESLA             DR = 6

THREE CLEAN BOUND VALUES (E(h) = 0, 1/2, or 1):

  h = 0   mod 24:  E = 1    → S ∈ [1, 1]  forced        h mod 37 = 0  (SEAM)
  h = 6   mod 24:  E = 1/2  → S ∈ [1/2, 1]  critical    h mod 37 = 6  ∈ TESLA
  h = 12  mod 24:  E = 0    → S ∈ [0, 1]  unconstrained  h mod 37 = 12 ∈ ST
  h = 18  mod 24:  E = 1/2  → S ∈ [1/2, 1]  critical    h mod 37 = 18 ∈ SEED
  h = 24  mod 24:  E = 1    → S ∈ [1, 1]  forced        h mod 37 = 24 ∈ SEED ∩ CASCADE

CRITICAL LINE CROSSING:

  E(h) = 1/2 at h = 6 (TESLA) and h = 18 (SEED).
  In GF(37): 1/2 = 2⁻¹ mod 37 = 19 = the critical line representative (T212/T213).
  Both crossings of the critical-line bound occur at named orbit nodes:
    TESLA (h=6) and SEED (h=18).

SEAM COLLAPSE:

  E(12) = 0  →  S ∈ [0, 1]: the constraint vanishes entirely.
  h = 12 ∈ ST (sovereign target, DR = 3).
  The sovereign target phase releases the stability constraint to SEAM (no lower bound).

FORCED STABILITY:

  E(0) = E(24) = 1  →  S = 1 exactly.
  h = 0  → SEAM (h mod 37 = 0).
  h = 24 → SEED ∩ CASCADE (h mod 37 = 24).
  SEAM and SEED/CASCADE phases force maximum stability.

RATIONAL BOUND VALUES IN GF(37):

  E(4) = 3/4:  h = 4 ∈ SA.  3/4 mod 37 = 3 × 4⁻¹ = 3 × 28 = 84 ≡ 10 ∈ IC.
    → The SA phase's lower bound maps to the identity cycle in GF(37).

  E(6) = 1/2:  h = 6 ∈ TESLA.  1/2 mod 37 = 19 (critical line).
    → The TESLA phase's lower bound IS the GF(37) critical line.

  E(8) = 1/4:  h = 8 ∈ TESLA ∩ CASCADE.  1/4 mod 37 = 28 ∈ SA_ST_B orbit.
    → The CASCADE/TESLA phase bound maps to the SA-ST companion orbit.

=== D7 ORBIT EVALUATION ===

D7 = {7, 33, 34} in GF(37). Evaluated at h = 7, 33, 34 (mod 24):

  h = 7:  E(7) = (1 + cos(7π/12))/2 ≈ 0.3706  → S ∈ [0.371, 1]
  h = 33 mod 24 = 9:  E(9) ≈ 0.1464            → S ∈ [0.146, 1]
  h = 34 mod 24 = 10: E(10) ≈ 0.0670           → S ∈ [0.067, 1]

  D7 orbit elements → decreasing stability constraint across their phase values.
  33 = prime index of 137 (T221): the 137 connection appears at phase 33 → E(9) ≈ 0.146.

=== CONNECTION TO PIPELINE ===

Pipeline reference (seed=246):
  Stability Ratio S = 0.0000.
  S = 0 is admissible only when E(h) = 0, i.e., h ≡ 12 (mod 24).
  h = 12 ∈ ST (sovereign target).
  The pipeline's zero stability ratio requires the sovereign target phase h=12.

  12 mod 37 = 12 ∈ ST.  DR(12) = 3 (ST archetype).

=== SUMMARY ===

The D7 envelope E(h) encodes the GF(37) orbit structure in its period hierarchy:
  Period 24 → SEED ∩ CASCADE
  Half-period 12 → ST (constraint collapses to SEAM)
  Quarter-period 6 → TESLA (constraint hits critical line)

The admissible band {(h,S) : S ∈ [E(h), 1]} has its constraint minimum at
ST phases (h=12, full freedom) and maximum rigidity at SEAM/SEED phases (h=0, 24).

The critical line value 1/2 = 2⁻¹ mod 37 = 19 appears as the bound at h ∈ {TESLA, SEED},
connecting the stability constraint to the Riemann hypothesis critical line analog in GF(37).
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


def E(h):
    return 0.5 * (1.0 + math.cos(math.pi * h / 12.0))


def run_assertions():
    # ── Period = 24 ∈ SEED ∩ CASCADE ─────────────────────────────────────────
    assert E(0) == E(24)           # period = 24
    assert 24 in SEED
    assert 24 in CASCADE

    # ── Half-period 12 ∈ ST → E = 0 (SEAM) ──────────────────────────────────
    assert abs(E(12)) < 1e-15
    assert 12 in ST

    # ── Quarter-period 6 ∈ TESLA → E = 1/2 (critical line) ──────────────────
    assert abs(E(6) - 0.5) < 1e-15
    assert 6 in TESLA
    assert pow(2, P - 2, P) == 19  # 2^{-1} mod 37 = 19 (critical line)

    # ── h=18 ∈ SEED → second critical line crossing ───────────────────────────
    assert abs(E(18) - 0.5) < 1e-15
    assert 18 in SEED

    # ── h=24 ∈ SEED ∩ CASCADE → E = 1 (forced stability) ────────────────────
    assert abs(E(24) - 1.0) < 1e-15
    assert 24 in SEED and 24 in CASCADE

    # ── E(0) = 1: h=0 mod 37 = 0 (SEAM) → maximum constraint ────────────────
    assert abs(E(0) - 1.0) < 1e-15
    assert 0 % P == 0              # SEAM

    # ── E(4) = 3/4; h=4 ∈ SA; 3/4 mod 37 = 10 ∈ IC ─────────────────────────
    assert abs(E(4) - 0.75) < 1e-15
    assert 4 in SA
    four_inv = pow(4, P - 2, P)    # = 28
    three_over_four = (3 * four_inv) % P
    assert three_over_four == 10 and 10 in IC

    # ── E(8) = 1/4; h=8 ∈ TESLA ∩ CASCADE; 1/4 mod 37 = 28 ─────────────────
    assert abs(E(8) - 0.25) < 1e-15
    assert 8 in TESLA and 8 in CASCADE
    one_over_four = four_inv       # = 28
    assert one_over_four == 28

    # ── Admissible region: S ≥ E(h) ──────────────────────────────────────────
    # At h=12 (ST): fully open [0, 1]
    assert E(12) == 0.0
    for S in [0.0, 0.1, 0.5, 1.0]:
        assert S >= E(12)           # all S admissible at ST phase

    # At h=0 (SEAM): only S=1
    assert E(0) == 1.0
    assert 1.0 >= E(0) and 0.0 < E(0)  # only S=1 passes

    # At h=6 (TESLA): S ≥ 1/2
    assert E(6) == 0.5
    assert 0.5 >= E(6)
    assert 0.4 < E(6)              # 0.4 would fail

    # ── Pipeline: S=0 requires E(h)=0, i.e., h=12∈ST ────────────────────────
    pipeline_S = 0.0
    admissible_h = [h for h in range(25) if pipeline_S >= E(h)]
    assert 12 in admissible_h
    # Only h=12 (within 0..24) gives E(h)=0 exactly
    exact_zero_h = [h for h in range(25) if abs(E(h)) < 1e-15]
    assert exact_zero_h == [12]
    assert 12 in ST

    # ── D7 orbit evaluation ──────────────────────────────────────────────────
    assert 7 in D7 and 33 in D7 and 34 in D7
    # 33 = prime index of 137 (T221)
    assert 33 % P == 33 and 33 in D7

    # ── 19 fixed point of s ↦ 1-s (critical line) ────────────────────────────
    assert (1 - 19) % P == 19

    print("All assertions passed.")
    print()
    print("D7 ENVELOPE — PERIOD HIERARCHY IN GF(37):")
    print(f"  Period 24 ∈ SEED ∩ CASCADE  DR={sum(int(d) for d in str(24))%9 or 9}")
    print(f"  Half-period 12 ∈ ST  DR={sum(int(d) for d in str(12))%9 or 9}")
    print(f"  Quarter-period 6 ∈ TESLA  DR={6}")
    print()
    print("CLEAN BOUND VALUES (E = 0, 1/2, 1):")
    for h, label in [(0,'SEAM'), (6,'TESLA'), (12,'ST'), (18,'SEED'), (24,'SEED∩CASCADE')]:
        e = E(h)
        bound = f"1/2 (critical line: 2⁻¹=19)" if abs(e-0.5)<1e-10 else f"{int(round(e*2))}/2"
        print(f"  h={h:2d} ∈ {label:15s}: E={bound}  → S ∈ [{e:.1f}, 1]")
    print()
    print("RATIONAL BOUND VALUES IN GF(37):")
    print(f"  E(4)=3/4 (h∈SA):  3/4 mod 37 = {(3*pow(4,P-2,P))%P} ∈ IC")
    print(f"  E(6)=1/2 (h∈TESLA): 1/2 mod 37 = 19 (CRITICAL LINE)")
    print(f"  E(8)=1/4 (h∈TESLA∩CASCADE): 1/4 mod 37 = 28 (SA_ST_B orbit)")
    print()
    print("PIPELINE REFERENCE:")
    print(f"  S=0.000 admissible only at E(h)=0: h=12 ∈ ST (sovereign target)")


if __name__ == "__main__":
    run_assertions()
