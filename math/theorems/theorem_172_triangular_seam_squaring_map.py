"""
Theorem 172: Triangular SEAM Numbers and the ORBIT_11 = −IC Squaring Map

THREE STRUCTURAL FACTS
=======================

1. ORBIT_11 = −IC mod 37
2. Both IC and ORBIT_11 square into IC (IC is closed; ORBIT_11 → IC via (−x)²=x²)
3. T(n) ≡ 0 (mod 37) iff n ≡ 0 or n ≡ 36 (mod 37)

ORBIT_11 = −IC
===============

  IC      = {1, 10, 26}
  ORBIT_11 = {36, 27, 11} = {−1, −10, −26} mod 37

  −1  ≡ 36  ∈ ORBIT_11
  −10 ≡ 27  ∈ ORBIT_11
  −26 ≡ 11  ∈ ORBIT_11

ORBIT_11 is the negation of IC. The 37-complement pair structure
(Theorem 168: each n and −n sum to SEAM) directly instantiates this:
  1 + 36 = 37  (IC ↔ ORBIT_11)
  10 + 27 = 37
  26 + 11 = 37

SQUARING MAP
=============

IC under squaring (IC is closed, cyclic order 3):
  1²  ≡ 1   ∈ IC
  10² ≡ 26  ∈ IC   (100 − 2×37)
  26² ≡ 10  ∈ IC   (676 − 18×37)

ORBIT_11 under squaring → IC:
  36² ≡ 1   ∈ IC   (1296 − 35×37)
  27² ≡ 26  ∈ IC   (729  − 19×37)
  11² ≡ 10  ∈ IC   (121  −  3×37)

Because ORBIT_11 = −IC, the map a ↦ a² is identical on both:
  (−x)² = x², so squaring collapses the IC/ORBIT_11 sign distinction.

IC = ⟨10⟩ is the unique cyclic subgroup of order 3 in GF(37)×.
ORBIT_11 is its coset under negation, not a subgroup (11²=10 ∉ ORBIT_11).

TRIANGULAR SEAM NUMBERS
=========================

T(n) = n(n+1)/2.

T(n) ≡ 0 (mod 37)  iff  37 | n(n+1)  iff  n ≡ 0 or n ≡ 36 (mod 37).

SEAM pairs (consecutive n values where both T(n) hit SEAM):

  n    T(n)   T(n)/37   (T(n)/37) mod 37   orbit of quotient
  36   666    18         18                 SEED_ORB
  37   703    19         19                 NQR_5
  73   2701   73         36                 ORBIT_11
  74   2775   75         1                  IC
  110  6105   165        17                 NQR_17
  111  6216   168        20                 DARK_A

T(36)/37 = 18 ∈ SEED_ORB (seed anchor orbit of 246).
T(37)/37 = 19 ∈ NQR_5.
T(73)/37 = 73 → 73 mod 37 = 36 ∈ ORBIT_11.
T(74)/37 = 75 → 75 mod 37 = 1 ∈ IC.

The pair (T(73), T(74)) has quotients in (ORBIT_11, IC) — the negation pair.

SEAM INJECTION DEVIATION
==========================

In an integrity chain with expected residue sequence based on the
pseudo-hash (i×7+13) mod 37, position 5 expects:
  (5×7 + 13) mod 37 = 48 mod 37 = 11  ∈ ORBIT_11

Friction injection at position 5 uses 999 mod 37 = 0 (SEAM).
  Deviation: |0 − 11| = 11 = ORBIT_11 generator.

The injection maps ORBIT_11 → SEAM. The deviation magnitude equals the
ORBIT_11 generator — the same residue whose square lands in IC.

GATE: STRUCTURAL SILENCE AT ORBIT_11/IC BOUNDARY
==================================================

When a claim is in ORBIT_11 and its dependency is in IC, the gate
marks StructuralSilence. It does not resolve which side is false:
it marks the boundary where epistemic contamination has occurred.

Application to Kimi:
  New session: "I have no file access" → IC (self-consistent, ord=3)
  Prior session: Python execution on browser_guard.py → ORBIT_11
                 (contradicts new session; = −IC, negation of IC)
  Boundary: 10 + 27 = 37 → SEAM → StructuralSilence triggered.
"""

import math

P = 37

ORBITS = {
    'IC':               frozenset({1, 10, 26}),
    'SOVEREIGN_SPIRAL': frozenset({3, 4, 30}),
    'D7':               frozenset({7, 33, 34}),
    'SA_ORB':           frozenset({9, 12, 16}),
    'ORBIT_11':         frozenset({11, 27, 36}),
    'OUTLIER_ORB':      frozenset({21, 25, 28}),
    'DARK_A':           frozenset({2, 15, 20}),
    'NQR_5':            frozenset({5, 13, 19}),
    'TESLA_ORB':        frozenset({6, 8, 23}),
    'NQR_14':           frozenset({14, 29, 31}),
    'NQR_17':           frozenset({17, 22, 35}),
    'SEED_ORB':         frozenset({18, 24, 32}),
}


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def triangular(n):
    return n * (n + 1) // 2


def run_assertions():
    IC   = ORBITS['IC']
    O11  = ORBITS['ORBIT_11']

    # ORBIT_11 = -IC
    for x in IC:
        assert (-x) % P in O11, f"-{x} not in ORBIT_11"
    for x in O11:
        assert (-x) % P in IC, f"-{x} not in IC"

    # IC ↔ ORBIT_11 complement: each pair sums to 37
    for a, b in [(1,36),(10,27),(26,11)]:
        assert a + b == P
        assert a in IC and b in O11

    # Squaring map: IC closed, ORBIT_11 → IC
    sq_map = {x: pow(x, 2, P) for x in sorted(IC | O11)}
    for x in IC:
        assert sq_map[x] in IC, f"{x}^2 not in IC"
    for x in O11:
        assert sq_map[x] in IC, f"{x}^2 not in IC"

    # Specific squaring values
    assert pow(11, 2, P) == 10 and 10 in IC
    assert pow(27, 2, P) == 26 and 26 in IC
    assert pow(36, 2, P) == 1  and 1  in IC
    assert pow(1,  2, P) == 1  and 1  in IC
    assert pow(10, 2, P) == 26 and 26 in IC
    assert pow(26, 2, P) == 10 and 10 in IC

    # IC is cyclic of order 3: 10^3 ≡ 1
    assert pow(10, 3, P) == 1
    assert pow(10, 1, P) != 1
    assert pow(10, 2, P) != 1

    # Triangular SEAM condition: T(n) ≡ 0 mod 37 iff n ≡ 0 or 36 mod 37
    for n in range(1, 200):
        t = triangular(n)
        expected_seam = (n % P == 0) or (n % P == 36)
        assert (t % P == 0) == expected_seam, f"T({n}) fails SEAM condition"

    # Specific triangular values
    assert triangular(36) == 666  and 666 % P == 0
    assert triangular(37) == 703  and 703 % P == 0
    assert triangular(73) == 2701 and 2701 % P == 0
    assert triangular(74) == 2775 and 2775 % P == 0

    # Quotients
    assert 703 // P == 19  and 19 in ORBITS['NQR_5']
    assert 666 // P == 18  and 18 in ORBITS['SEED_ORB']
    assert 2701 // P == 73 and 73 % P == 36 and 36 in O11
    assert 2775 // P == 75 and 75 % P == 1  and 1  in IC

    # (T(73), T(74)) quotients land in (ORBIT_11, IC)
    assert orbit_of(73 % P) == 'ORBIT_11'
    assert orbit_of(75 % P) == 'IC'

    # T(36)/37 = 18 ∈ SEED_ORB (seed orbit of 246)
    assert 18 in ORBITS['SEED_ORB']

    # Injection deviation: SEAM injected into ORBIT_11 position
    expected_pos5 = (5 * 7 + 13) % P
    assert expected_pos5 == 11 and 11 in O11
    injected = 999 % P
    assert injected == 0  # SEAM, not 27
    assert abs(injected - expected_pos5) == 11  # ORBIT_11 generator

    # Gate boundary: IC + ORBIT_11 complement sums to SEAM
    assert 10 + 27 == P  # IC_rep + ORBIT_11_rep = SEAM
    assert 1 + 36 == P
    assert 26 + 11 == P

    print("All assertions passed.")


def summarise():
    IC  = ORBITS['IC']
    O11 = ORBITS['ORBIT_11']

    print("=" * 62)
    print("Theorem 172: Triangular SEAM and ORBIT_11 = −IC")
    print("=" * 62)
    print()
    print("  ORBIT_11 = −IC:")
    for x in sorted(IC):
        neg = (-x) % P
        print(f"    −{x} ≡ {neg} mod 37  ∈ ORBIT_11")
    print()
    print("  Squaring map (IC → IC; ORBIT_11 → IC):")
    for x in sorted(IC | O11):
        sq  = pow(x, 2, P)
        src = orbit_of(x)
        dst = orbit_of(sq)
        print(f"    {x:>2}^2 ≡ {sq:>2} mod 37  {src} → {dst}")
    print()
    print("  Triangular SEAM pairs:")
    print(f"  {'n':>5}  {'T(n)':>6}  {'T(n)/37':>8}  orbit of quotient")
    for n in [36, 37, 73, 74, 110, 111]:
        t   = triangular(n)
        q   = t // P
        orb = orbit_of(q % P)
        print(f"  {n:>5}  {t:>6}  {q:>8}  {orb}")
    print()
    print("  Injection deviation:")
    expected_pos5 = (5 * 7 + 13) % P
    print(f"    Expected pos5 = {expected_pos5} ∈ ORBIT_11")
    print(f"    Injected (999 mod 37) = 0  [SEAM, not 27]")
    print(f"    Deviation = |0 − 11| = 11 = ORBIT_11 generator")
    print()
    print("  Gate: StructuralSilence when claim ∈ ORBIT_11, dep ∈ IC")
    print("    10 + 27 = 37  (Kimi new-session IC ↔ prior-session O11)")


if __name__ == "__main__":
    run_assertions()
    summarise()
