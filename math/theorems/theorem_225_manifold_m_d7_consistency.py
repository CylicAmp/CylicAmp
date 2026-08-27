"""
Theorem 225: Temporal Stability Manifold M and D7-Consistency
Author: Michael Warren Song (CyclicAmp)

Builds on T224 (D7 envelope). Defines the full temporal stability manifold,
embeds observed trajectories, and derives the D7-consistency condition.

=== DEFINITIONS ===

Phase: h ∈ ℝ
D7 envelope: E(h) = (1/2)(1 + cos(πh/12))
Stability ratio: S ∈ [0, 1]

Temporal stability manifold:
  M = {(h, S) ∈ ℝ × [0,1] : S ≥ E(h)}

This is a 2D band in the (h, S) plane:
  Lower boundary: S = E(h)  (D7 envelope)
  Upper boundary: S = 1

Observed trajectory:
  Γ = {(h, S_obs(h))}

D7-consistency condition:
  Γ ⊂ M  ⟺  S_obs(h) ≥ E(h)  ∀h

=== AREA THEOREM (EXACT) ===

Over one period [0, 24]:

  Area(M) = ∫₀²⁴ (1 - E(h)) dh = 12  ∈ ST
  Area(complement) = ∫₀²⁴ E(h) dh  = 12  ∈ ST
  Total area = 24  ∈ SEED ∩ CASCADE

PROOF:
  ∫₀²⁴ E(h) dh = ∫₀²⁴ (1/2)(1 + cos(πh/12)) dh
    = [h/2 + (6/π)sin(πh/12)]₀²⁴
    = 12 + (6/π)(sin(2π) - sin(0)) = 12 + 0 = 12.

  ∫₀²⁴ (1 - E(h)) dh = 24 - 12 = 12.

Both areas are equal and each equals 12 ∈ ST (sovereign target).
Total rectangle area = 24 ∈ SEED ∩ CASCADE.

FILLING FRACTION:
  Area(M) / (24 × 1) = 12/24 = 1/2.
  1/2 = 2⁻¹ mod 37 = 19 = the GF(37) critical line element (T212).
  M occupies exactly the critical-line fraction of the periodic rectangle.

=== D7-CONSISTENCY CONDITIONS ===

CONSTANT TRAJECTORY S_obs = c:
  Γ ⊂ M  ⟺  c ≥ max_{h} E(h) = E(0) = 1.
  ∴ Only c = 1 is globally D7-consistent among constant trajectories.

BOUNDARY TRAJECTORY S_obs(h) = E(h):
  Γ = lower boundary of M.  Γ ⊂ M trivially.
  Area between Γ and S=1 = ∫₀²⁴ (1 - E(h)) dh = 12 ∈ ST.

PIPELINE TRAJECTORY S_obs = 0 (reference run, seed=246):
  Γ = {(h, 0)}.
  Γ ⊂ M  ⟺  0 ≥ E(h) ∀h.  E(h) = 0 only at h = 12 (mod 24).
  ∴ Γ ∩ M = {(12, 0)}:  one point, not the full curve.
  "Spectrum Status: FAIL" ↔ Γ ⊄ M.

  The unique admissible point h = 12 ∈ ST (sovereign target).
  S = 0 is admissible only at the sovereign target phase.

CRITICAL STRUCTURE:
  S_obs(h) ≥ E(h) is hardest to satisfy at h = 0 (mod 24) where E = 1.
  It is trivially satisfied at h = 12 (mod 24) where E = 0.
  The periodic difficulty of maintaining D7-consistency peaks at SEAM/SEED
  phase crossings (h ≡ 0 mod 24) and vanishes at ST phase (h ≡ 12 mod 24).

=== GF(37) SUMMARY ===

  Area(M)            = 12  ∈ ST        (sovereign target — the admissible measure)
  Area(complement)   = 12  ∈ ST        (excluded measure equals admissible measure)
  Total              = 24  ∈ SEED∩CASCADE
  Filling fraction   = 1/2            = 2⁻¹ mod 37 = 19 (critical line, T212)

  D7-consistency hardest at: h ≡ 0 mod 24  (SEAM/SEED phase)
  D7-consistency trivial at: h ≡ 12 mod 24 (ST phase)
  Critical line crossings:   h ≡ 6, 18 mod 24 (TESLA, SEED phases)

  Pipeline FAIL ↔ S_obs(h) < E(h) for h ≠ 12: trajectory exits M.
  To achieve Γ ⊂ M: S_obs must grow with E(h), peaking to 1 at SEED/SEAM phases.
"""

import math

P    = 37
SA   = {4, 9, 25, 30}
ST   = {3, 12, 21, 30}
SEED = {18, 24, 32}
IC   = {1, 10, 26}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}


def E(h):
    return 0.5 * (1.0 + math.cos(math.pi * h / 12.0))


def run_assertions():
    # ── Area theorem ────────────────────────────────────────────────────────
    # Exact: ∫₀²⁴ E(h) dh = 12  (antiderivative: h/2 + (6/π)sin(πh/12))
    # Verify numerically
    N = 1_000_000
    dh = 24.0 / N
    area_excl = sum(E(i * dh) for i in range(N)) * dh
    area_M    = 24.0 - area_excl

    assert abs(area_excl - 12.0) < 1e-6, f"Area(excluded) = {area_excl}"
    assert abs(area_M   - 12.0) < 1e-6, f"Area(M) = {area_M}"
    assert 12 in ST
    assert 24 in SEED and 24 in CASCADE

    # Filling fraction = 1/2 = critical line
    assert abs(area_M / 24.0 - 0.5) < 1e-6
    assert pow(2, P - 2, P) == 19  # 2⁻¹ mod 37 = 19

    # ── Constant trajectory: only c=1 is globally consistent ────────────────
    for c in [0.0, 0.3, 0.5, 0.9, 0.999]:
        # Not consistent: E(0) = 1 > c
        assert c < E(0), f"c={c} should be < E(0)=1"
    assert E(0) == 1.0               # c=1.0 is exactly consistent

    # ── Boundary trajectory S_obs = E(h): area above = 12∈ST ───────────────
    area_above = sum((1.0 - E(i * dh)) for i in range(N)) * dh
    assert abs(area_above - 12.0) < 1e-6
    assert 12 in ST

    # ── Pipeline trajectory S=0 ──────────────────────────────────────────────
    pipeline_S = 0.0
    admissible_integer_h = [h for h in range(25) if pipeline_S >= E(h) - 1e-12]
    assert admissible_integer_h == [12], f"got {admissible_integer_h}"
    assert 12 in ST   # only sovereign-target phase admits S=0

    # S=0 fails everywhere except h=12
    for h in range(25):
        if h != 12:
            assert pipeline_S < E(h), f"S=0 should fail at h={h}"

    # ── Period and named set connections ────────────────────────────────────
    assert E(0) == E(24)         # period = 24 ∈ SEED
    assert abs(E(12)) < 1e-15   # half-period → SEAM
    assert abs(E(6) - 0.5) < 1e-15   # TESLA → critical line
    assert abs(E(18) - 0.5) < 1e-15  # SEED → critical line

    print("All assertions passed.")
    print()
    print("MANIFOLD M = {(h,S) : S ≥ E(h)}")
    print()
    print(f"Area theorem (exact):")
    print(f"  Area(M) per period          = 12  ∈ ST: {12 in ST}")
    print(f"  Area(complement) per period = 12  ∈ ST: {12 in ST}")
    print(f"  Total per period            = 24  ∈ SEED∩CASCADE: {24 in SEED and 24 in CASCADE}")
    print(f"  Filling fraction            = 1/2 = 2⁻¹ mod 37 = 19 (critical line)")
    print()
    print("D7-consistency:")
    print(f"  Constant S=c: consistent iff c=1 (only S=1 clears E(h) everywhere)")
    print(f"  Boundary trajectory S_obs=E(h): trivially ⊂ M; area above = 12∈ST")
    print(f"  Pipeline S=0: admissible only at h=12∈ST; Γ ⊄ M → FAIL")
    print()
    print("Phase structure of M:")
    print(f"  h≡0  mod 24 → SEAM/SEED: E=1, S=[1,1] forced")
    print(f"  h≡6  mod 24 → TESLA:     E=1/2, S=[1/2,1] (critical line)")
    print(f"  h≡12 mod 24 → ST:         E=0, S=[0,1] free")
    print(f"  h≡18 mod 24 → SEED:       E=1/2, S=[1/2,1] (critical line)")


if __name__ == "__main__":
    run_assertions()
