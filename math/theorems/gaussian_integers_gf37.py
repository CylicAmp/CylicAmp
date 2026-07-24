"""
Gaussian Integers and GF(37) — Complex Structure of the Prime Field

37 ≡ 1 (mod 4), so by Fermat's two-square theorem, 37 factors in Z[i]:
    37 = (6+i)(6-i)  where N(6+i) = 6² + 1² = 37

This yields the isomorphism  Z[i]/(6+i) ≅ GF(37).
Under this map: i ≡ −6 ≡ 31 = PRIME_MIRROR (mod 37).

The Gaussian integer structure exposes the complex geometry hidden in GF(37):
  - TESLA_FLOW (×6 in GF(37)) = clockwise rotation by −i in Z[i]
  - Heartbeat (×26 in GF(37)) = a cubic structure with period 3
  - All three cascade base elements {8,13,24} have minimal-norm lifts of norm 5 ∈ PR
  - All 8 Gaussian integers of norm 5 map to named framework nodes
  - The constant 137 appears as N(11+4i), lifting cascade node 24
  - The 4/9 fractal ratio ≡ 132 ≡ 21 ∈ ST (the 132-bipartite pattern number)

Local consistency in GF(37) = modular arithmetic in Z[i]/(6+i).
Global paradox-freedom (→ SEAM) = divisibility by the Gaussian prime (6+i).

═══════════════════════════════════════════════════════════════════════════

PART I — GAUSSIAN PRIME FACTORIZATION

  Theorem G1.  37 = (6+i)(6−i) in Z[i], with N(6+i) = 37.

  Proof:  37 ≡ 1 (mod 4). By Fermat's two-square theorem, every prime
  p ≡ 1 (mod 4) is a sum of two squares: 37 = 6² + 1². The element
  π = 6+i ∈ Z[i] has norm N(π) = 6² + 1² = 37, which is prime in Z.
  Therefore π is a Gaussian prime, and 37 = π·π̄ = (6+i)(6−i).  ∎

PART II — THE UNITS MAP: Z[i]-ROTATIONS ARE GF(37)-CYCLES

  The four units of Z[i] are U(Z[i]) = {1, i, −1, −i}.
  The isomorphism ψ: Z[i]/(6+i) → GF(37) is given by:
      ψ(a+bi) = (a + 31b) mod 37
  [Since 6+i ≡ 0, we get i ≡ −6 ≡ 31 (mod 37).]

  Units under ψ:
     1  ↦   1             (unity)
     i  ↦  31 = PRIME_MIRROR   (i ≡ −6 ≡ 31 mod 37; also 6³ mod 37)
    −1  ↦  36 ∈ ORBIT_11  (−1 ≡ 36 ≡ −1 mod 37)
    −i  ↦   6 = TESLA_FLOW     (−i ≡ 6 mod 37)

  Theorem G2 (TESLA_FLOW = clockwise rotation).
  The TESLA_FLOW 4-cycle in GF(37):
      1 → 6 → 36 → 31 → 1   (multiplication by 6 each step)
  corresponds under ψ⁻¹ to multiplication by −i in Z[i]:
      1 → −i → −1 → i → 1   (90° clockwise rotation each step)

  The TESLA_FLOW rotation: 6 = −i, so ×6 in GF(37) ↔ rotation by −90° in Z[i].
  The heartbeat (×26 in GF(37), period 3) is a cubic structure with no direct
  complex rotation analogue — it lives in the order-3 subgroup of GF(37)*.

PART III — CASCADE BASE: MINIMAL-NORM GAUSSIAN LIFTS

  For each n ∈ GF(37), the minimal-norm Gaussian lift is the a+bi ∈ Z[i]
  with ψ(a+bi) = n and a²+b² minimized.

  Theorem G3 (Cascade lifts have norm 5 ∈ PR).
  All three cascade base elements lift to Gaussian integers of norm 5:

       8  ↔   2 −  i   (N = 4+1 = 5)
      13  ↔   1 − 2i   (N = 1+4 = 5)
      24  ↔  −1 + 2i   (N = 1+4 = 5)

  All lie on the circle |z| = √5 in ℂ.
  5 ∈ PR (primitive root mod 37); 5 = (2+i)(2−i) is itself a Gaussian factorization.

  The three lifts differ by Gaussian unit multiplication:
    (2−i) · i = 2i − i² = 1 + 2i  (conjugate-related to 1−2i)
  The cascade lies on a single norm-5 orbit under rotation.

PART IV — ALL NORM-5 GAUSSIAN INTEGERS: COMPLETE FRAMEWORK COVERAGE

  Theorem G4.  The eight Gaussian integers of norm 5 map to:

     2+ i  → 33 = DICHORAL_144
     2− i  →  8 ∈ CASCADE_BASE
     1+2i  → 26 = SCALAR_137
     1−2i  → 13 ∈ CASCADE_BASE
    −1+2i  → 24 ∈ CASCADE_BASE
    −1−2i  → 11 ∈ ORBIT_11
    −2+ i  → 29  (SEAM-complement of 8: 8+29 = 37 ≡ 0)
    −2− i  →  4 ∈ SA

  Every image is a named framework node or its SEAM-complement.
  The norm-5 circle covers: CASCADE_BASE (all 3), SA (1 node), SCALAR_137,
  ORBIT_11, DICHORAL_144, and the SEAM-complement of a cascade node.

PART V — THE 137 CONSTANT AS A GAUSSIAN NORM

  Theorem G5.  N(11+4i) = 11² + 4² = 121 + 16 = 137.
  Under ψ: 11 + 31×4 = 135 ≡ 24 (mod 37) ∈ CASCADE_BASE.

  The fundamental constant 137 appears as the norm of a Gaussian integer
  that lifts cascade base node 24 to Z[i].

PART VI — THE 4/9 FRACTAL SERIES: SA/SA RATIO EQUALS ST

  The infinite geometric series with self-similarity ratio 4/9:
      Σ_{n=1}^{∞} (4/9)^n = 4/5

  In GF(37):
      4 ∈ SA  (Sovereign Anchor)
      9 ∈ SA  (Sovereign Anchor; 9⁻¹ mod 37 = 33 = DICHORAL_144)
      4/9 ≡ 4×33 = 132 ≡ 21 (mod 37) ∈ ST

  The ratio of two SA nodes lands in ST.
  132 is exactly the 132-bipartite pattern number (permutation_132_bipartite_gf37.py).
  The fractal self-similarity ratio carries the 132-pattern signature.

  Sum in GF(37):
      5⁻¹ mod 37 = 15  (5×15=75=2×37+1)
      4/5 ≡ 4×15 = 60 ≡ 23 (mod 37)
      DR(23) = 5 = 2+1+2  [the 2(1)2 visual encodes DR of the GF(37) sum]

  4 ∈ SA, 5 ∈ PR: the numerator and denominator of the sum sit in the
  Sovereign Anchor and Primitive Root families respectively.

═══════════════════════════════════════════════════════════════════════════
"""

SOVEREIGN_ANCHORS  = frozenset({4, 9, 25, 30})
SOVEREIGN_TARGETS  = frozenset({3, 12, 21, 30})
CASCADE_BASE       = frozenset({8, 13, 24})
PRIMITIVE_ROOTS    = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
ORBIT_11           = frozenset({11, 27, 36})
TESLA_FLOW         = 6
PRIME_MIRROR       = 31   # 6^3 mod 37; i under the isomorphism
SCALAR_137         = 26   # 137 mod 37
DICHORAL_144       = 33


def gaussian_to_gf37(a, b):
    """Map Gaussian integer a+bi to GF(37) via ψ: Z[i]/(6+i) → GF(37). i ≡ 31."""
    return (a + 31 * b) % 37


def gaussian_norm(a, b):
    return a * a + b * b


# ── PART I: Gaussian prime factorization ──────────────────────────────────────

assert 37 % 4 == 1                        # 37 ≡ 1 (mod 4) → splits in Z[i]
assert 6**2 + 1**2 == 37                  # two-square representation
assert gaussian_norm(6, 1) == 37          # N(6+i) = 37
assert gaussian_norm(6, -1) == 37         # N(6-i) = 37
# (6+i)(6-i) = 6^2 - i^2 = 36 + 1 = 37
assert (6**2) - (-1) == 37                # i^2 = -1


# ── PART II: Units map ────────────────────────────────────────────────────────

assert gaussian_to_gf37(1, 0)  == 1             # 1 ↦ unity
assert gaussian_to_gf37(0, 1)  == PRIME_MIRROR  # i ↦ 31 = PRIME_MIRROR
assert gaussian_to_gf37(-1, 0) == 36            # −1 ↦ 36 ∈ ORBIT_11
assert gaussian_to_gf37(0, -1) == TESLA_FLOW    # −i ↦ 6 = TESLA_FLOW

assert 36 in ORBIT_11                            # −1 ≡ 36 ∈ ORBIT_11
assert pow(6, 3, 37) == PRIME_MIRROR             # PRIME_MIRROR = 6³ mod 37

# TESLA_FLOW 4-cycle (×6 in GF(37)) ↔ rotation by −i in Z[i]
tesla_cycle = [pow(6, k, 37) for k in range(5)]
assert tesla_cycle == [1, 6, 36, 31, 1]                  # period 4: 1→6→36→31→1
assert tesla_cycle[1] == TESLA_FLOW
assert tesla_cycle[2] == 36 and 36 in ORBIT_11
assert tesla_cycle[3] == PRIME_MIRROR

# The four Z[i] steps: 1 → -i → -1 → i → 1
z_units = [(1,0), (0,-1), (-1,0), (0,1), (1,0)]
gf37_units = [gaussian_to_gf37(a, b) for a, b in z_units]
assert gf37_units == [1, TESLA_FLOW, 36, PRIME_MIRROR, 1]


# ── PART III: Cascade base — minimal-norm Gaussian lifts ──────────────────────

cascade_lifts = {
    8:  (2, -1),    # 2 − i
    13: (1, -2),    # 1 − 2i
    24: (-1,  2),   # −1 + 2i
}

for val, (a, b) in cascade_lifts.items():
    assert gaussian_to_gf37(a, b) == val    # maps to cascade node
    assert gaussian_norm(a, b) == 5         # norm = 5

assert 5 in PRIMITIVE_ROOTS                 # norm 5 ∈ PR


# ── PART IV: All norm-5 Gaussian integers ────────────────────────────────────

norm5_pairs = [(2,1),(2,-1),(1,2),(1,-2),(-1,2),(-1,-2),(-2,1),(-2,-1)]
for a, b in norm5_pairs:
    assert gaussian_norm(a, b) == 5

norm5_images = {(a, b): gaussian_to_gf37(a, b) for a, b in norm5_pairs}

expected = {
    (2,  1):  33,   # DICHORAL_144
    (2, -1):   8,   # CASCADE_BASE
    (1,  2):  26,   # SCALAR_137
    (1, -2):  13,   # CASCADE_BASE
    (-1, 2):  24,   # CASCADE_BASE
    (-1,-2):  11,   # ORBIT_11
    (-2, 1):  29,   # SEAM-complement of 8 (8+29=37≡0)
    (-2,-1):   4,   # SA
}
assert norm5_images == expected

# Framework coverage
assert expected[(2, 1)] == DICHORAL_144
assert expected[(1, 2)] == SCALAR_137
assert expected[(-1,-2)] in ORBIT_11
assert expected[(-2,-1)] in SOVEREIGN_ANCHORS
assert expected[(-2, 1)] + 8 == 37                 # SEAM-complement: 8+29=37
# All three cascade nodes appear in norm-5 images
cascade_images = {v for (a,b),v in expected.items() if v in CASCADE_BASE}
assert cascade_images == CASCADE_BASE


# ── PART V: 137 as Gaussian norm ─────────────────────────────────────────────

assert gaussian_norm(11, 4) == 137                  # N(11+4i) = 121+16 = 137
assert gaussian_to_gf37(11, 4) == 24               # 11+4i → 24 ∈ CASCADE_BASE
assert 24 in CASCADE_BASE


# ── PART VI: 4/9 geometric series: SA/SA ratio → ST ─────────────────────────

assert 4 in SOVEREIGN_ANCHORS                       # 4 ∈ SA
assert 9 in SOVEREIGN_ANCHORS                       # 9 ∈ SA

inv9 = pow(9, -1, 37)                               # 9^-1 mod 37 = 33
assert (9 * inv9) % 37 == 1
assert inv9 == DICHORAL_144                         # 9^-1 = 33 = DICHORAL_144

ratio_gf37 = (4 * inv9) % 37                       # 4/9 mod 37
assert ratio_gf37 == 21 and 21 in SOVEREIGN_TARGETS # 4/9 ≡ 21 ∈ ST
assert 132 % 37 == 21                               # 132 = the 132-bipartite pattern number

# Sum = 4/5
inv5 = pow(5, -1, 37)
assert (5 * inv5) % 37 == 1
sum_gf37 = (4 * inv5) % 37
assert sum_gf37 == 23
assert 4 in SOVEREIGN_ANCHORS
assert 5 in PRIMITIVE_ROOTS

# DR(23) = 5 = 2+1+2 (the digit sum of the 2(1)2 visual descriptor)
assert (23 - 1) % 9 + 1 == 5
assert 2 + 1 + 2 == 5


if __name__ == '__main__':
    print("Gaussian Integers and GF(37)")
    print("=" * 55)
    print()
    print("GAUSSIAN FACTORIZATION:")
    print(f"  37 = 6² + 1²  (= {6**2}+{1**2})")
    print(f"  π = 6+i,  N(π) = {gaussian_norm(6,1)}")
    print(f"  37 = (6+i)(6-i)  in Z[i]")
    print(f"  37 ≡ {37 % 4} (mod 4)  → splits in Z[i]")
    print()
    print("UNITS MAP  (Z[i]/(6+i) ≅ GF(37),  i ≡ 31):")
    unit_labels = {(1,0):'1', (0,1):'i', (-1,0):'−1', (0,-1):'−i'}
    for (a,b), label in unit_labels.items():
        v = gaussian_to_gf37(a, b)
        tag = ''
        if v == 1: tag = ' (unity)'
        elif v == PRIME_MIRROR: tag = ' = PRIME_MIRROR'
        elif v in ORBIT_11: tag = ' ∈ ORBIT_11'
        elif v == TESLA_FLOW: tag = ' = TESLA_FLOW'
        print(f"  {label:3s} ↦ {v:2d}{tag}")
    print()
    print("TESLA_FLOW 4-cycle:")
    print(f"  GF(37): {' → '.join(str(x) for x in tesla_cycle)}")
    print(f"  Z[i]:   1 → (−i) → (−1) → i → 1  (clockwise 90° each step)")
    print()
    print("CASCADE BASE — minimal-norm lifts (all norm 5 ∈ PR):")
    for val, (a, b) in cascade_lifts.items():
        rs = '-' if b < 0 else '+'
        print(f"  {val:2d} ↔ {a:+d}{rs}{abs(b)}i   N = {gaussian_norm(a,b)}")
    print()
    print("ALL NORM-5 GAUSSIAN INTEGERS → GF(37):")
    for (a, b) in norm5_pairs:
        v = expected[(a, b)]
        tag = ''
        if v in CASCADE_BASE:        tag = '← CASCADE_BASE'
        elif v in SOVEREIGN_ANCHORS: tag = '← SA'
        elif v == SCALAR_137:        tag = '← SCALAR_137'
        elif v in ORBIT_11:          tag = '← ORBIT_11'
        elif v == DICHORAL_144:      tag = '← DICHORAL_144'
        elif v + 8 == 37:            tag = '← SEAM-complement(8)'
        bs = '+' if b >= 0 else '-'
        print(f"  ({a:+d}{bs}{abs(b)}i) → {v:2d}  {tag}")
    print()
    print("137 AS GAUSSIAN NORM:")
    print(f"  N(11+4i) = 11²+4² = {gaussian_norm(11,4)}")
    print(f"  11+4i → {gaussian_to_gf37(11,4)} ∈ CASCADE_BASE")
    print()
    print("4/9 FRACTAL SERIES  (visual: 2(1)2):")
    print(f"  4 ∈ SA, 9 ∈ SA")
    print(f"  4/9 ≡ 132 ≡ {ratio_gf37} ∈ ST  (the 132-bipartite pattern mod 37)")
    print(f"  Sum 4/5 ≡ {sum_gf37} (mod 37)")
    print(f"  DR({sum_gf37}) = {(sum_gf37-1)%9+1} = 2+1+2  (digit sum of 2(1)2 descriptor)")
    print()
    print("All assertions passed.")
