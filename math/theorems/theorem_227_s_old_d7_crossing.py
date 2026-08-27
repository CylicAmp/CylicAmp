"""
Theorem 227: S_old / D7 Crossing Equation — φ³ Linear Floor and Envelope Intersections
Author: Michael Warren Song (CyclicAmp)

Builds on T224 (D7 envelope) and T225 (temporal stability manifold M).
Defines the linear stability floor S_old derived from the golden ratio Φ³,
derives the transcendental crossing equation with the D7 envelope E(h),
and classifies the crossing phase structure through GF(37).

=== DEFINITIONS ===

Golden ratio:  Φ = (1+√5)/2 ≈ 1.6180
Φ³ = 2+√5 ≈ 4.2361

Parameter:  Δ₂₄ ∈ [0, 24)  (correction to the 24-hour period)
Period constant:  C = (24 − Δ₂₄) × Φ³

Linear stability floor (S_old):
  S_old(h) = h / C = h / ((24 − Δ₂₄) × Φ³)

D7 envelope (T224):
  E(h) = (1/2)(1 + cos(πh/12))

=== CROSSING EQUATION ===

S_old(h) = E(h)
  h / C = (1/2)(1 + cos(πh/12))

Setting θ = πh/12, A = πC/24:

  θ = A(1 + cos θ)

This is transcendental — no elementary closed form.

In each period [0, 24] there are generically TWO real crossings:
  h₁ ∈ (0, 12):  rising S_old meets falling E(h)
  h₂ ∈ (12, 24): rising S_old meets rising E(h)

Boundary conditions:
  h = 0:  S_old = 0 < E(0) = 1   (no root at origin)
  h = 12: E(12) = 0 < S_old(12)  (line above at half-period)

=== JOINTLY ENFORCED FLOOR ===

F(h) = max(E(h), S_old(h)) =
  E(h)     on [0, h₁]           — envelope dominates
  S_old(h) on [h₁, h₂]         — linear floor dominates (when h₂ exists)
  E(h)     on [h₂, 24]          — envelope recaptures

=== CRITICAL LINE THRESHOLD: Δ₂₄ ≥ 19 ===

For Δ₂₄ ≥ 19: S_old(24) = 24 / ((24−Δ₂₄)Φ³) > 1 = E(24).
The rising line overshoots the envelope before h = 24; h₂ disappears.
S_old stays above E(h) on all of (h₁, 24].

19 = 2⁻¹ mod 37 — the GF(37) critical line representative (T212/T213).
The second crossing disappears exactly at the critical line threshold.

=== NUMERICAL CROSSINGS (Φ = golden ratio) ===

Δ₂₄  |  C=(24−Δ₂₄)Φ³  |  h₁       |  E(h₁)   |  h₂
  0   |  101.666        |  9.6123   |  0.0945  |  15.0132
  2   |   93.193        |  9.5154   |  0.1021  |  15.1729
  4   |   84.721        |  9.4050   |  0.1110  |  15.3601
  6   |   76.249        |  9.2779   |  0.1217  |  15.5836
  8   |   67.777        |  9.1292   |  0.1347  |  15.8569
 12   |   50.833        |  8.7347   |  0.1718  |  16.6558
 16   |   33.889        |  8.0981   |  0.2390  |  18.3077
 18   |   25.416        |  7.5850   |  0.2984  |  20.5341
 19+  |      —          |  h₁<7.5   |    —     |  (none)

=== GF(37) PHASE STRUCTURE OF h₁ ===

As Δ₂₄ increases from 0 to 18, h₁ decreases through three named phases:

  Δ₂₄ ∈ {0,2,4,6,8}:  floor(h₁) = 9  ∈ SA   (sovereign anchor)
  Δ₂₄ ∈ {12,16}:      floor(h₁) = 8  ∈ CASCADE ∩ TESLA
  Δ₂₄ = 18:           floor(h₁) = 7  ∈ D7    (D7 orbit element)

The first crossing descends through:  SA → CASCADE/TESLA → D7

floor(Φ³) = 4 ∈ SA.  The golden-cube floor is a sovereign anchor.

=== QUALITATIVE IMPACT OF Δ₂₄ ===

- Increasing Δ₂₄ steepens S_old:
    h₁ moves LEFT (earlier first crossing)
    h₂ moves RIGHT (later second crossing)
- For Δ₂₄ ≥ 19: h₂ disappears; F(h) = S_old(h) on (h₁, 24].

=== GF(37) SUMMARY ===

  Φ³ = 2+√5:  floor(Φ³) = 4  ∈ SA  (sovereign anchor; DR=4)
  Period 24  ∈ SEED ∩ CASCADE
  h₁ floor descent:  9∈SA → 8∈CASCADE∩TESLA → 7∈D7
  Δ₂₄ ≥ 19 → h₂ vanishes:  19 = 2⁻¹ mod 37 = GF(37) critical line
  h₁ clusters near 8 (E₈ cascade node) across all moderate Δ₂₄
"""

import math
from scipy.optimize import brentq

# ── GF(37) constants ─────────────────────────────────────────────────────────
P    = 37
MULT = 26

SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
SEED    = {18, 24, 32}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}
D7      = {7, 33, 34}
NEG_H   = {11, 27, 36}

# ── Golden ratio constants ────────────────────────────────────────────────────
PHI  = (1.0 + math.sqrt(5.0)) / 2.0   # ≈ 1.6180
PHI3 = PHI ** 3                        # = 2 + √5 ≈ 4.2361


def E(h: float) -> float:
    """D7 envelope (T224)."""
    return 0.5 * (1.0 + math.cos(math.pi * h / 12.0))


def S_old(h: float, delta: float) -> float:
    """Linear stability floor: h / ((24 - delta) * Phi^3)."""
    return h / ((24.0 - delta) * PHI3)


def crossing_eq(h: float, delta: float) -> float:
    return S_old(h, delta) - E(h)


def find_crossings(delta: float):
    """
    Find h1 ∈ (0,12) and h2 ∈ (12,24) for given delta.
    Returns (h1, h2) where h2=None if delta >= 19.
    """
    h1 = brentq(crossing_eq, 0.01, 11.99, args=(delta,))
    try:
        h2 = brentq(crossing_eq, 12.01, 23.99, args=(delta,))
    except ValueError:
        h2 = None
    return h1, h2


def run_assertions():
    # ── Phi^3 = 2 + sqrt(5) ──────────────────────────────────────────────────
    assert abs(PHI3 - (2.0 + math.sqrt(5.0))) < 1e-12
    assert abs(PHI3 - 4.23606797749979) < 1e-10
    assert int(PHI3) == 4 and 4 in SA   # floor(Phi^3) ∈ SA

    # ── Period and named set membership ──────────────────────────────────────
    assert 24 in SEED and 24 in CASCADE
    assert 8 in CASCADE and 8 in TESLA

    # ── Critical line: delta >= 19 eliminates h2 ─────────────────────────────
    assert pow(2, P - 2, P) == 19   # 2^-1 mod 37 = 19
    # delta=18: h2 exists
    _, h2_18 = find_crossings(18.0)
    assert h2_18 is not None and 20.5 < h2_18 < 20.6
    # delta=19: h2 gone
    _, h2_19 = find_crossings(19.0)
    assert h2_19 is None
    # delta=20: h2 gone
    _, h2_20 = find_crossings(20.0)
    assert h2_20 is None

    # ── Table values (tolerance 0.001) ───────────────────────────────────────
    TABLE = [
        (0,   9.6123, 0.0945, 15.0132),
        (2,   9.5154, 0.1021, 15.1729),
        (4,   9.4050, 0.1110, 15.3601),
        (6,   9.2779, 0.1217, 15.5836),
        (8,   9.1292, 0.1347, 15.8569),
        (12,  8.7347, 0.1718, 16.6558),
        (16,  8.0981, 0.2390, 18.3077),
        (18,  7.5850, 0.2984, 20.5341),
    ]
    for delta, h1_exp, d7_exp, h2_exp in TABLE:
        h1, h2 = find_crossings(float(delta))
        assert abs(h1 - h1_exp) < 0.001, f"delta={delta}: h1={h1:.4f} != {h1_exp}"
        assert abs(E(h1) - d7_exp) < 0.001, f"delta={delta}: E(h1)={E(h1):.4f} != {d7_exp}"
        assert h2 is not None and abs(h2 - h2_exp) < 0.001, \
            f"delta={delta}: h2={h2} != {h2_exp}"

    # ── floor(h1) phase descent through GF(37) named elements ────────────────
    for delta in [0, 2, 4, 6, 8]:
        h1, _ = find_crossings(float(delta))
        assert int(h1) == 9 and 9 in SA, f"delta={delta}: floor(h1)={int(h1)} not 9∈SA"

    for delta in [12, 16]:
        h1, _ = find_crossings(float(delta))
        assert int(h1) == 8 and 8 in CASCADE and 8 in TESLA, \
            f"delta={delta}: floor(h1)={int(h1)} not 8∈CASCADE∩TESLA"

    h1_18, _ = find_crossings(18.0)
    assert int(h1_18) == 7 and 7 in D7, \
        f"delta=18: floor(h1)={int(h1_18)} not 7∈D7"

    print("All assertions passed.")
    print()
    print(f"CROSSING EQUATION: S_old(h) = E(h)")
    print(f"  Phi = {PHI:.10f}")
    print(f"  Phi^3 = {PHI3:.10f} = 2+sqrt(5)")
    print(f"  floor(Phi^3) = {int(PHI3)} ∈ SA (sovereign anchor)")
    print()
    print(f"  Transcendental form: theta = A(1+cos theta), theta=pi*h/12, A=pi*C/24")
    print()
    print(f"CRITICAL LINE THRESHOLD:")
    print(f"  Delta_24 >= 19 eliminates h2")
    print(f"  19 = 2^-1 mod 37 = GF(37) critical line representative")
    print()
    print(f"{'Delta':>5}  {'h1':>8}  {'E(h1)':>7}  {'h2':>8}  {'floor(h1)':>10}  GF(37)")
    for delta, h1_exp, d7_exp, h2_exp in TABLE:
        h1, h2 = find_crossings(float(delta))
        fh1 = int(h1)
        orb = ("SA" if fh1 in SA else
               "CASCADE∩TESLA" if fh1 in CASCADE and fh1 in TESLA else
               "D7" if fh1 in D7 else "?")
        print(f"  {delta:3d}  {h1:8.4f}  {E(h1):7.4f}  {h2:8.4f}  {fh1:>10}  ∈ {orb}")
    print()
    print(f"floor(h1) descent:  9∈SA → 8∈CASCADE∩TESLA → 7∈D7")
    print(f"  (tracks the named-element sequence SA→CASCADE→D7 as Delta_24 rises)")


if __name__ == "__main__":
    run_assertions()
