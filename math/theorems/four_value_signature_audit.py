"""
four_value_signature_audit.py

Audit of the four-value input signature: (144.24, 137.33, 1.41, 14.13).

─────────────────────────────────────────────────────────────────
IDENTIFICATION (corrected):

  144.24 → Nd atomic mass: 144.242 g/mol  (standard value)
  137.33 → Ba atomic mass: 137.327 g/mol  (standard value)
           NOTE: α⁻¹ = 137.036 (CODATA 2018) — NOT 137.33
           Ba mass ≠ fine-structure constant; diff = 0.291
    1.41 → √2 = 1.41421...
   14.13 → first Riemann zeta zero Im(ρ₁) = 14.134725...
           (4.5π = 14.137167...; diff = 0.002 — zeta zero is tighter)

─────────────────────────────────────────────────────────────────
FRAMEWORK CONNECTIONS (integer projections):

  144 = 12²    DR(144) = 9 = NULL
               144 mod 37 = 33 = prime_index(137)  ← structural tie

  137          DR(137) = 2
               137 mod 37 = 26 = 10⁻¹ mod 37      ← modular ratio
               137 = 4² + 11² (sum of two squares)
               137 is the 33rd prime

   14 ~ ρ₁    DR(14) = 5
               14 mod 37 = 14

    1 ~ √2    DR(1) = 1 (identity)
               1 mod 37 = 1 (37-field unity)

OBSERVATION: 144 mod 37 = 33 = prime_index(137).
The integer projection of Nd connects directly to the coset incidence
coordinate of 137 inside the period-333 system.
─────────────────────────────────────────────────────────────────
"""

import math
from sympy import isprime, primepi

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = abs(n) % 9
    return r if r else 9


# ── Standard atomic masses (IUPAC) ───────────────────────────────────────────

ND_MASS  = 144.242   # Neodymium
BA_MASS  = 137.327   # Barium
ALPHA_INV = 137.035999084  # CODATA 2018

check(abs(ND_MASS - 144.24) < 0.01,
      "Nd atomic mass ≈ 144.24", ND_MASS, 144.24)
check(abs(BA_MASS - 137.33) < 0.01,
      "Ba atomic mass ≈ 137.33", BA_MASS, 137.33)

# Ba mass ≠ α⁻¹ — correction
check(abs(BA_MASS - ALPHA_INV) > 0.28,
      "Ba mass and α⁻¹ differ by > 0.28 (not the same constant)",
      round(abs(BA_MASS - ALPHA_INV), 3), 0.291)

# √2
SQRT2 = math.sqrt(2)
check(abs(SQRT2 - 1.41) < 0.005, "√2 ≈ 1.41", round(SQRT2, 5), 1.41421)

# First Riemann zeta zero (imaginary part)
RIEMANN_ZERO_1 = 14.134725141734693
PI_45 = 4.5 * math.pi

check(abs(RIEMANN_ZERO_1 - 14.13) < 0.005,
      "ρ₁ Im ≈ 14.13", RIEMANN_ZERO_1, 14.134725)
check(abs(PI_45 - 14.13) < 0.01,
      "4.5π ≈ 14.13", round(PI_45, 6), 14.137167)
# Zeta zero is tighter match to 14.13 than 4.5π
check(abs(RIEMANN_ZERO_1 - 14.13) < abs(PI_45 - 14.13),
      "ρ₁ closer to 14.13 than 4.5π is",
      abs(RIEMANN_ZERO_1 - 14.13), abs(PI_45 - 14.13))


# ── Integer projections and DR ────────────────────────────────────────────────

# 144 = 12² → already in framework: DR(12²) = DR(144) = 9 = NULL
check(12 ** 2 == 144,    "144 = 12²",        12 ** 2, 144)
check(dr(144) == 9,      "DR(144) = 9 = NULL", dr(144), 9)

check(dr(137) == 2,  "DR(137) = 2", dr(137), 2)
check(dr(14) == 5,   "DR(14) = 5",  dr(14),  5)
check(dr(1) == 1,    "DR(1) = 1",   dr(1),   1)


# ── Mod-37 projections ────────────────────────────────────────────────────────

check(144 % 37 == 33, "144 mod 37 = 33", 144 % 37, 33)
check(137 % 37 == 26, "137 mod 37 = 26", 137 % 37, 26)
check(14  % 37 == 14, "14  mod 37 = 14", 14  % 37, 14)
check(1   % 37 == 1,  "1   mod 37 = 1",  1   % 37,  1)

# Structural tie: 144 mod 37 = 33 = prime_index(137)
check(primepi(137) == 33,
      "137 is the 33rd prime", primepi(137), 33)
check(144 % 37 == primepi(137),
      "Nd projection (144 mod 37) = prime_index(137) = 33",
      144 % 37, primepi(137))

# 26 = 10⁻¹ mod 37 (modular ratio)
check(10 * 26 % 37 == 1, "10 × 26 ≡ 1 (mod 37)", 10 * 26 % 37, 1)
check(137 % 37 == 26,    "137 ≡ 26 = 10⁻¹ (mod 37)", 137 % 37, 26)


# ── 137 framework connections ─────────────────────────────────────────────────

# Sum of two squares
check(4 ** 2 + 11 ** 2 == 137, "137 = 4² + 11²", 4 ** 2 + 11 ** 2, 137)
check(isprime(137), "137 is prime", isprime(137), True)

# α⁻¹ identification: 137.036, not 137.33
check(abs(ALPHA_INV - 137.036) < 0.001,
      "α⁻¹ ≈ 137.036 (not 137.33)", round(ALPHA_INV, 3), 137.036)


# ── DR of integer projections as a vector ─────────────────────────────────────

# (144, 137, 1, 14) → DR (9, 2, 1, 5)
DR_VECTOR = [dr(144), dr(137), dr(1), dr(14)]
check(DR_VECTOR == [9, 2, 1, 5],
      "DR vector of integer projections", DR_VECTOR, [9, 2, 1, 5])

# Sum of DR vector
check(sum(DR_VECTOR) == 17, "sum of DR vector = 17", sum(DR_VECTOR), 17)
check(dr(sum(DR_VECTOR)) == 8, "DR(17) = 8", dr(17), 8)

# Mod-37 vector
MOD37_VECTOR = [144 % 37, 137 % 37, 1 % 37, 14 % 37]
check(MOD37_VECTOR == [33, 26, 1, 14],
      "mod-37 vector", MOD37_VECTOR, [33, 26, 1, 14])


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Four-Value Signature Audit: (144.24, 137.33, 1.41, 14.13)")
    print("=" * 66)

    print(f"\n── Identification (corrected) ──")
    print(f"  144.24 → Nd atomic mass = {ND_MASS}  g/mol")
    print(f"  137.33 → Ba atomic mass = {BA_MASS}  g/mol")
    print(f"           α⁻¹ = {ALPHA_INV}  (CODATA 2018)")
    print(f"           Ba mass ≠ α⁻¹:  diff = {abs(BA_MASS-ALPHA_INV):.3f}")
    print(f"    1.41 → √2  = {SQRT2:.6f}")
    print(f"   14.13 → ρ₁ Im = {RIEMANN_ZERO_1:.6f}  (first Riemann zero)")
    print(f"           4.5π  = {PI_45:.6f}")
    print(f"           ρ₁ Δ from 14.13 = {abs(RIEMANN_ZERO_1-14.13):.6f}")
    print(f"           4.5π Δ from 14.13 = {abs(PI_45-14.13):.6f}")
    print(f"           ρ₁ is the tighter match ✓")

    print(f"\n── Integer projections ──")
    print(f"  {'value':>5}  {'int':>4}  {'DR':>3}  {'mod37':>6}")
    for v, i in [(144.24, 144), (137.33, 137), (1.41, 1), (14.13, 14)]:
        print(f"  {v:5.2f}  {i:4d}  {dr(i):3d}  {i%37:6d}")

    print(f"\n── DR vector: {DR_VECTOR}  sum={sum(DR_VECTOR)}  DR(sum)={dr(sum(DR_VECTOR))}")
    print(f"── Mod-37 vector: {MOD37_VECTOR}")

    print(f"\n── Framework connections ──")
    print(f"  144 = 12²   DR(144) = 9 = NULL")
    print(f"  144 mod 37 = 33 = prime_index(137)  [Nd → coset incidence of 137]")
    print(f"  137 mod 37 = 26 = 10⁻¹ mod 37       [modular ratio]")
    print(f"  137 = 4² + 11²                        [sum of two squares]")
    print(f"  137 = 33rd prime")
    print(f"   14 mod 37 = 14")
    print(f"    1 mod 37 =  1                        [37-field unity]")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
