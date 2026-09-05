"""
================================================================================
THEOREM 109 — The Prime 137 is Self-Referential in GF(37)
================================================================================

STATEMENT.
The prime 137 has residue 26 mod 37, which is exactly the multiplier used to
define the 137-map: f(n) = 137·n (mod 37) = 26·n (mod 37). The map's defining
prime reduces to its own multiplier in the field. This self-reference is exact.

Five further results:

  (i)   26 is a primitive cube root of unity in GF(37): 26³ ≡ 1 (mod 37).
        IC = {1, 10, 26} is the complete set of cube roots of unity in GF(37).
        137 ≡ ∛1 in GF(37).

  (ii)  139 ≡ 28 (mod 37). The 137-map orbit of 28 is {28, 25, 21} — the
        SA∩ST-spanning 3-cycle. The first step f(28) = 25 ∈ SA lands in the
        Sovereign Anchor set. The twin prime 139 enters the sovereign structure
        on its first map step.

  (iii) The residue pair (26, 28) satisfies:
          26 × 28 ≡ 25 (mod 37) ∈ SA    (product → Sovereign Anchor)
          26 + 28 ≡ 17 (mod 37) ∈ BASIN_Y ∩ PR  (sum → Basin Y)
        Their sum 137 + 139 = 276 ≡ 17 (mod 37) ∈ BASIN_Y ∩ PR.

  (iv)  The seed residue 24 and the map multiplier 26 differ by exactly 2 —
        the twin prime gap — in both Z and GF(37). The pair (24, 26) is
        realized as a twin prime residue pair at (431, 433).
        Additionally:
          26 × 24 ≡ 32 (mod 37) ∈ SEED_ORBIT   (multiplier × seed = f(24))
          26 + 24 ≡ 13 (mod 37) ∈ CB            (multiplier + seed ∈ cascade base)

  (v)   The primitive root 2 raised to the power 137 gives the seed residue:
          2^137 ≡ 24 (mod 37).
        Equivalently, the first digit-sum of the seed 246 (= 2+4+6 = 12)
        is the exponent such that:
          2^12 ≡ 26 (mod 37) = the 137-map multiplier.

================================================================================
DEFINITIONS
================================================================================

  The 137-map:  f(n) = (137 · n) mod 37 = (26 · n) mod 37.
  The multiplier 26 satisfies 137 ≡ 26 (mod 37) and ord₃₇(26) = 3.

  IC = {1, 10, 26}:  the Identity Class — orbit of 1 under the 137-map.
  SA = {4, 9, 25, 30}:  Sovereign Anchors.
  ST = {3, 12, 21, 30}:  Sovereign Targets.
  CB = {8, 13, 24}:  Cascade Base.
  SEED_ORBIT = {18, 24, 32}:  orbit of seed 246 (≡ 24) under the 137-map.
  BASIN_Y = {17, 22, 35}:  Basin Y (orbit of 17 under the 137-map).
  PR = {2,5,13,15,17,18,19,20,22,24,32,35}:  primitive roots mod 37.

================================================================================
LEMMAS
================================================================================

LEMMA 109.1  (Self-reference).
  137 is prime. 137 = 3 × 37 + 26, so 137 ≡ 26 (mod 37).
  The 137-map f(n) = 137n mod 37 uses 26 as its multiplier.
  Therefore the residue of the map's defining prime equals the map's multiplier.

  Equivalently: f(k) = 137k mod 37 = 26k mod 37 for all k, because 137 ≡ 26.
  Applied to k = 1: f(1) = 26 — the map sends the identity to 26 ≡ 137.    ∎

LEMMA 109.2  (26 is a primitive cube root of unity).
  26³ ≡ 1 (mod 37):
    26² = 676 = 18 × 37 + 10 ≡ 10 (mod 37).
    26³ = 26 × 10 = 260 = 7 × 37 + 1 ≡ 1 (mod 37).
  ord₃₇(26) = 3.  26 ≠ 1, so 26 is a primitive cube root of unity.

  The three cube roots of unity in GF(37) are the solutions of x³ = 1,
  i.e. the orbit of 1 under repeated multiplication by 26:
    1 → 26 → 10 → 1.
  Thus IC = {1, 10, 26} is the complete set of cube roots of unity in GF(37).
  Every element of IC has multiplicative order dividing 3 (and exactly 3,
  for 10 and 26).  137 ≡ 26 ≡ ∛1 in GF(37).                               ∎

LEMMA 109.3  (139 and the SA∩ST-spanning orbit).
  139 is prime. 139 = 3 × 37 + 28, so 139 ≡ 28 (mod 37).
  28 is not a member of any named class.

  Under the 137-map:
    f(28) = 26 × 28 = 728 = 19 × 37 + 25 ≡ 25 (mod 37).  25 ∈ SA.
    f(25) = 26 × 25 = 650 = 17 × 37 + 21 ≡ 21 (mod 37).  21 ∈ ST.
    f(21) = 26 × 21 = 546 = 14 × 37 + 28 ≡ 28 (mod 37).  returns to 28.

  Orbit of 28: {28, 25, 21} = {unclassified, SA, ST}.
  This is an SA∩ST-spanning 3-cycle (one of two; the other is {9, 12, 16}).
  The first map step from 28 lands in SA.
  By THEOREM 107 Corollary 107.10, exactly two such orbits exist in GF(37).   ∎

LEMMA 109.4  (Residue arithmetic of the twin pair).
  The residue pair (r₁, r₂) = (137 mod 37, 139 mod 37) = (26, 28).

  Product:  26 × 28 = 728 ≡ 25 (mod 37).  25 ∈ SA.
            Equivalently: the product of the twin prime residues = f(28) ∈ SA.
            (The product of residues equals the first 137-map step of the larger.)

  Sum:      26 + 28 = 54 ≡ 17 (mod 37).   17 ∈ BASIN_Y ∩ PR.
            Equivalently: 137 + 139 = 276 ≡ 17 (mod 37) ∈ BASIN_Y ∩ PR.    ∎

LEMMA 109.5  (Seed–multiplier gap of 2).
  Seed residue:   246 mod 37 = 24.  24 ∈ CB ∩ SEED_ORBIT ∩ PR.
  Map multiplier: 26 ∈ IC.
  Difference:     26 − 24 = 2 in Z.  In GF(37): 26 − 24 ≡ 2 (mod 37).

  The twin prime gap (= 2) equals the difference between the map multiplier
  and the seed residue. The residue pair (24, 26) appears as a twin prime pair:
    431 ≡ 24 (mod 37),  433 ≡ 26 (mod 37),  both prime.

  Additional arithmetic of 26 and 24:
    26 × 24 ≡ 32 (mod 37) ∈ SEED_ORBIT.
    This is f(24) — the product equals the next step in the seed's own orbit.
    The 137-map at the seed residue is encoded in the product of multiplier × seed.

    26 + 24 = 50 ≡ 13 (mod 37) ∈ CB.
    13 is simultaneously in CB and the Metonic orbit {5, 13, 19}.
    The sum of multiplier and seed residue lands at a cascade base element.      ∎

LEMMA 109.6  (2^137 ≡ seed residue in GF(37)).
  Since ord₃₇(2) = 36 (2 is the primitive root of GF(37)),
  by Fermat's little theorem: 2^n ≡ 2^(n mod 36) (mod 37).

  137 mod 36 = 137 − 3 × 36 = 137 − 108 = 29.
  2^29 mod 37:
    2^1  = 2
    2^4  = 16
    2^8  ≡ 256 − 6 × 37 = 34
    2^16 ≡ 34² = 1156 − 31 × 37 = 9
    2^29 = 2^16 × 2^8 × 2^4 × 2^1 ≡ 9 × 34 × 16 × 2 (mod 37)
         ≡ 9 × 34 = 306 ≡ 306 − 8 × 37 = 10 (mod 37)
         × 16 = 160 ≡ 160 − 4 × 37 = 12 (mod 37)
         × 2  = 24 (mod 37).
  2^137 ≡ 24 (mod 37) = seed residue.

  The primitive root 2 raised to the power of the map-defining prime 137
  gives exactly the seed residue 24.

  Complementary result:  digit-sum₁(246) = 2 + 4 + 6 = 12.
  2^12 mod 37 = 4096 mod 37 = 4096 − 110 × 37 = 26 = map multiplier.
  The first digit-sum of seed 246 is the exponent that yields the 137-map
  multiplier from the primitive root 2.                                     ∎

================================================================================
MAIN THEOREM
================================================================================

THEOREM 109.  (Prime 137 — Self-Reference and Twin Prime Structure in GF(37)).

  (i)  [SELF-REFERENCE]  137 is the prime that names the 137-map. Its residue
       mod 37 is 26, which is the map's multiplier. The defining prime reduces
       to its own coefficient in the field. The 137-map sends the identity 1
       to 26 ≡ 137 (mod 37) on its first step.

  (ii) [CUBE ROOT OF UNITY]  26³ ≡ 1 (mod 37). IC = {1, 10, 26} is the
       complete set of cube roots of unity in GF(37). The 137-map multiplier
       is a primitive cube root of unity. The IC orbit of 1 under the 137-map
       is: 1 → 26 → 10 → 1.

  (iii)[TWIN PRIME 139]  139 ≡ 28 (mod 37). The orbit of 28 under the 137-map
       is {28, 25, 21} — an SA∩ST-spanning 3-cycle. The map step f(28) = 25 ∈ SA
       is the first step. The product of the twin residues: 26 × 28 ≡ 25 ∈ SA.
       The sum: 137 + 139 = 276 ≡ 17 (mod 37) ∈ BASIN_Y ∩ PR.

  (iv) [SEED–MULTIPLIER GAP]  The seed residue 24 (CB ∩ SEED_ORBIT) and the
       map multiplier 26 (IC) differ by 2 in both Z and GF(37). The twin prime
       gap equals GF(37) gap. The pair (431, 433) realizes residues
       (24, 26). Furthermore: 26 × 24 ≡ 32 ∈ SEED_ORBIT (multiplier × seed
       = f(seed)); 26 + 24 ≡ 13 ∈ CB (multiplier + seed ∈ cascade base).

  (v)  [PRIMITIVE ROOT ENCODING]  2^137 ≡ 24 (mod 37) = seed residue.
       2^(digit-sum₁(246)) = 2^12 ≡ 26 (mod 37) = map multiplier.
       The seed residue and the map multiplier are both encoded as powers of
       the primitive root 2, with exponents drawn from 137 itself and from
       the digit-sum of the seed.

COROLLARY 109.7  (The four-way closure at 24 and 26).
  24 ∈ CB ∩ SEED_ORBIT ∩ PR (three named classes).
  26 ∈ IC (cube root of unity).
  26 − 24 = 2  (twin prime gap, in Z).
  26 + 24 ≡ 13 ∈ CB (mod 37).
  26 × 24 ≡ 32 ∈ SEED_ORBIT (mod 37).
  The arithmetic operations (difference, sum mod P, product mod P) on the
  pair (seed_residue, multiplier) all land in named named sets.

COROLLARY 109.8  (Self-reference chain).
  137 (prime) → f(1) = 26 ≡ 137 → f(26) = 10 → f(10) = 1 → f(1) = 26.
  The prime 137 enters the IC orbit on step 0 (it is the name of the map).
  In the orbit 1 → 26 → 10 → 1, the prime 137 labels the node 26.
  The map is named for the prime that occupies the first non-identity orbit node.
"""

# ── Python verification ───────────────────────────────────────────────────────

P = 37

IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
BASIN_Y    = frozenset({17, 22, 35})
PR         = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})
D7_ORBIT   = frozenset({7, 33, 34})


def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    return all(n % i != 0 for i in range(3, int(n**0.5) + 1, 2))


def fw(r):
    classes = []
    for name, s in [('IC', IC), ('SA', SA), ('ST', ST), ('CB', CB),
                    ('ORBIT_11', ORBIT_11), ('SEED_ORBIT', SEED_ORBIT),
                    ('BASIN_Y', BASIN_Y), ('PR', PR), ('D7', D7_ORBIT)]:
        if r in s:
            classes.append(name)
    return '[' + ','.join(classes) + ']' if classes else '[—]'


# ── Lemma 109.1 — Self-reference ──────────────────────────────────────────────

assert is_prime(137)
assert 137 % P == 26
assert 26 in IC
assert (26 * 1) % P == 26            # f(1) = 26 — map sends identity to multiplier

# The 137-map and the ×26 map are identical on GF(37)
for n in range(P):
    assert (137 * n) % P == (26 * n) % P

# ── Lemma 109.2 — Cube root of unity ─────────────────────────────────────────

assert pow(26, 2, P) == 10
assert pow(26, 3, P) == 1            # 26 is a primitive cube root of unity
assert next(k for k in range(1, P) if pow(26, k, P) == 1) == 3   # ord = 3

# IC = complete set of cube roots of unity
cube_roots = frozenset(x for x in range(1, P) if pow(x, 3, P) == 1)
assert cube_roots == IC

# IC orbit of 1 under the 137-map
assert (26 * 1) % P  == 26           # 1 → 26
assert (26 * 26) % P == 10           # 26 → 10
assert (26 * 10) % P == 1            # 10 → 1  (closed)

# ── Lemma 109.3 — 139 and SA∩ST-spanning orbit ───────────────────────────────

assert is_prime(139)
assert 139 % P == 28
assert 28 not in (IC | SA | ST | CB | ORBIT_11 | SEED_ORBIT | BASIN_Y | PR)

orbit_28 = [(26 * 28) % P, (26 * (26 * 28) % P) % P, (26 * (26 * (26 * 28) % P) % P) % P]
assert orbit_28[0] == 25 and 25 in SA    # f(28) = 25 ∈ SA
assert orbit_28[1] == 21 and 21 in ST    # f(25) = 21 ∈ ST
assert orbit_28[2] == 28                  # f(21) = 28  (closed)

orbit_28_set = frozenset({28, 25, 21})
assert orbit_28_set & SA == frozenset({25})
assert orbit_28_set & ST == frozenset({21})
assert len(orbit_28_set - (SA | ST)) == 1   # exactly one unclassified element

# ── Lemma 109.4 — Residue arithmetic ─────────────────────────────────────────

r137, r139 = 137 % P, 139 % P
assert r137 == 26 and r139 == 28

assert (r137 * r139) % P == 25 and 25 in SA   # product → SA
assert (r137 + r139) % P == 17 and 17 in BASIN_Y and 17 in PR   # sum → BASIN_Y

total = 137 + 139
assert total == 276 and total % P == 17

# ── Lemma 109.5 — Seed–multiplier gap ────────────────────────────────────────

seed_res = 246 % P
assert seed_res == 24
assert 24 in CB and 24 in SEED_ORBIT and 24 in PR

multiplier = 137 % P
assert multiplier == 26 and 26 in IC

assert multiplier - seed_res == 2     # gap = twin prime gap

# Realized at (431, 433)
assert is_prime(431) and is_prime(433)
assert 431 % P == 24 and 433 % P == 26

# Product and sum of (26, 24)
assert (26 * 24) % P == 32 and 32 in SEED_ORBIT    # = f(24) — next orbit step
assert (26 + 24) % P == 13 and 13 in CB             # sum ∈ cascade base

# ── Lemma 109.6 — 2^137 ≡ seed residue ───────────────────────────────────────

from math import gcd
assert gcd(2, P) == 1
assert next(k for k in range(1, P) if pow(2, k, P) == 1) == 36   # ord₃₇(2) = 36

assert 137 % 36 == 29
assert pow(2, 29, P) == 24                 # 2^29 ≡ 24 (mod 37)
assert pow(2, 137, P) == 24               # 2^137 ≡ seed residue (mod 37)

digit_sum_246 = 2 + 4 + 6
assert digit_sum_246 == 12
assert pow(2, 12, P) == 26               # 2^12 ≡ map multiplier (mod 37)

# ── Corollary 109.7 — Four-way closure ────────────────────────────────────────

assert 26 - 24 == 2
assert (26 + 24) % P == 13 and 13 in CB
assert (26 * 24) % P == 32 and 32 in SEED_ORBIT


if __name__ == "__main__":
    print("THEOREM 109 — The Prime 137 is Self-Referential in GF(37)")
    print("=" * 68)
    print()

    print("I. Self-reference")
    print("-" * 50)
    print(f"   137 prime:       {is_prime(137)}")
    print(f"   137 mod 37:      {137 % P}  = map multiplier")
    print(f"   137-map ≡ ×26 map on GF(37): verified for all {P} residues")
    print(f"   f(1) = {(26*1)%P}  — map sends identity to its own prime's residue")
    print()

    print("II. Cube root of unity")
    print("-" * 50)
    print(f"   26² mod 37 = {pow(26,2,P)}")
    print(f"   26³ mod 37 = {pow(26,3,P)}  (26 is a primitive cube root of unity)")
    print(f"   ord₃₇(26)  = {next(k for k in range(1,P) if pow(26,k,P)==1)}")
    print(f"   IC orbit: 1 → {(26*1)%P} → {(26*26)%P} → 1")
    print(f"   Cube roots of unity = {sorted(cube_roots)} = IC")
    print()

    print("III. Twin prime 139 ≡ 28 mod 37")
    print("-" * 50)
    print(f"   139 prime:  {is_prime(139)}")
    print(f"   139 mod 37: {139%P}")
    print(f"   f(28) = {(26*28)%P} ∈ SA  {fw(25)}")
    print(f"   f(25) = {(26*25)%P} ∈ ST  {fw(21)}")
    print(f"   f(21) = {(26*21)%P}       (returns to 28)")
    print(f"   Orbit {{28,25,21}}: SA∩ST-spanning, one unclassified element (28)")
    print()

    print("IV. Residue arithmetic")
    print("-" * 50)
    print(f"   26 × 28 ≡ {(26*28)%P} (mod 37) ∈ SA  {fw(25)}")
    print(f"   26 + 28 ≡ {(26+28)%P} (mod 37)  {fw(17)}")
    print(f"   137 + 139 = 276 ≡ {276%P} (mod 37)  {fw(17)}")
    print()

    print("V. Seed–multiplier gap of 2")
    print("-" * 50)
    print(f"   Seed residue:    246 mod 37 = {246%P}  {fw(24)}")
    print(f"   Map multiplier:  137 mod 37 = {137%P}  {fw(26)}")
    print(f"   Difference:      26 − 24 = {26-24}  (twin prime gap)")
    print(f"   Realized at:     (431,433) → ({431%P},{433%P})")
    print(f"   26 × 24 ≡ {(26*24)%P} (mod 37)  {fw(32)}  = f(24) = next orbit step")
    print(f"   26 + 24 ≡ {(26+24)%P} (mod 37)  {fw(13)}")
    print()

    print("VI. Primitive root encoding")
    print("-" * 50)
    print(f"   ord₃₇(2)    = {next(k for k in range(1,P) if pow(2,k,P)==1)}")
    print(f"   137 mod 36  = {137%36}")
    print(f"   2^137 mod 37 = {pow(2,137,P)}  = seed residue  {fw(24)}")
    print(f"   digit-sum₁(246) = {2+4+6}")
    print(f"   2^12 mod 37  = {pow(2,12,P)}  = map multiplier  {fw(26)}")
    print()

    print("Corollary 109.7 — Four-way closure at (24, 26)")
    print("-" * 50)
    print(f"   26 − 24      = {26-24}   (twin prime gap)")
    print(f"   26 + 24 mod 37 = {(26+24)%P}  {fw(13)}")
    print(f"   26 × 24 mod 37 = {(26*24)%P}  {fw(32)}")
    print()
    print("All assertions passed.")
