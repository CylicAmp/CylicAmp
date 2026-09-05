"""
THEOREM 100 — The Milestone Number on GF(37)

100 mod 37 = 26 ∈ IC.

26 is the 137-map multiplier: f(n) = (137 × n) mod 37 = (26 × n) mod 37.
The 100th theorem's index, reduced mod 37, IS the core operator of the
entire GF(37).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FIVE INDEPENDENT PATHS TO IC

  1. Direct residue:
       100 mod 37 = 26  ∈ IC

  2. Digital root:
       DR(100) = 1  ∈ IC

  3. Sovereign anchor factorization:
       100 = 4 × 25,  where 4,25 ∈ SA
       (4 × 25) mod 37 = 26  ∈ IC
       Two sovereign anchors multiply to the 137-map multiplier.

  4. Base-10 power:
       10² mod 37 = 26  ∈ IC
       because ord₃₇(10) = 3, so 10³ ≡ 1, and 10² ≡ 26 (mod 37).
       100 = 10² encodes this directly.

  5. 137-map orbit:
       The orbit of 26 under the 137-map is:
         26 → (26×26) mod 37 = 10 → (26×10) mod 37 = 1 → 26
       Orbit = {26, 10, 1} = IC exactly.
       The 137-map orbit of 100's residue is the identity basin itself.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMPANION RESULTS

  T(100) = 1+2+...+100 = 5050  mod 37 = 18  ∈ SEED_ORBIT
    The triangular number T(100) lands at the seed orbit entry.

  B(100) = 4×100²+1 = 40001  mod 37 = 4  ∈ SA
    The 100th Ulam diagonal value (THEOREM 96) is a sovereign anchor.

  SA pair products:
    4 × 25 mod 37 = 26  ∈ IC        (SA → IC)
    9 × 30 mod 37 = 11  ∈ ORBIT_11  (SA → ORBIT_11)
    Full SA product: 4×9×25×30 mod 37 = 27  ∈ ORBIT_11

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY

  100 mod 37 = 26:  GF(37)'s own multiplier.
  Every path — residue, DR, factorization, base-10 power, orbit —
  returns to IC. The 100th theorem is GF(37) reading itself.
"""

P          = 37
IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
BASIN_Y    = frozenset({17, 22, 35})


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 9


# ── Path 1: direct residue ────────────────────────────────────────────────────

assert 100 % P == 26 and 26 in IC


# ── Path 2: digital root ──────────────────────────────────────────────────────

assert dr(100) == 1 and 1 in IC


# ── Path 3: sovereign anchor factorization ────────────────────────────────────

assert 100 == 4 * 25
assert 4 in SA and 25 in SA
assert (4 * 25) % P == 26 and 26 in IC


# ── Path 4: base-10 power ─────────────────────────────────────────────────────

assert 100 == 10 ** 2
assert pow(10, 2, P) == 26 and 26 in IC
assert pow(10, 3, P) == 1          # ord₃₇(10) = 3


# ── Path 5: 137-map orbit of 26 = IC ─────────────────────────────────────────

orbit_26 = frozenset((26 * c) % P for c in IC)
assert orbit_26 == IC              # orbit of 26 under ×26 is IC itself

# Explicit 3-cycle
assert (26 * 26) % P == 10 and 10 in IC
assert (26 * 10) % P == 1  and 1  in IC
assert (26 *  1) % P == 26 and 26 in IC


# ── Companion: T(100) ────────────────────────────────────────────────────────

T100 = 100 * 101 // 2
assert T100 == 5050
assert T100 % P == 18 and 18 in SEED_ORBIT
assert dr(T100) == 1


# ── Companion: B(100) from THEOREM 96 ────────────────────────────────────────

B100 = 4 * 100 * 100 + 1
assert B100 == 40001
assert B100 % P == 4 and 4 in SA


# ── SA pair products ──────────────────────────────────────────────────────────

assert (4  * 25) % P == 26 and 26 in IC
assert (9  * 30) % P == 11 and 11 in ORBIT_11

prod_SA = 1
for x in SA:
    prod_SA = (prod_SA * x) % P
assert prod_SA == 27 and 27 in ORBIT_11


if __name__ == "__main__":
    def fw(r):
        classes = []
        for name, s in [('IC',IC),('SA',SA),('ST',ST),('CB',CB),
                        ('O11',ORBIT_11),('SEED',SEED_ORBIT),
                        ('T4',TESLA_4),('PR',PR),('BY',BASIN_Y)]:
            if r in s: classes.append(name)
        return classes or ['—']

    print("THEOREM 100 — The Milestone Number on GF(37)")
    print("=" * 60)
    print()
    print("FIVE PATHS TO IC:")
    print(f"  1. 100 mod 37        = {100%P}   ∈ {fw(100%P)}")
    print(f"  2. DR(100)           = {dr(100)}    ∈ {fw(dr(100))}")
    print(f"  3. (4×25) mod 37     = {(4*25)%P}   ∈ {fw((4*25)%P)}  (SA×SA)")
    print(f"  4. 10² mod 37        = {pow(10,2,P)}   ∈ {fw(pow(10,2,P))}")
    print(f"  5. orbit of 26       = {sorted(IC)}  = IC")
    print()
    print("COMPANION RESULTS:")
    print(f"  T(100) = 5050  mod37={T100%P}  ∈ {fw(T100%P)}  (seed orbit entry)")
    print(f"  B(100) = 40001 mod37={B100%P}   ∈ {fw(B100%P)}   (sovereign anchor)")
    print(f"  4×25 mod37={( 4*25)%P} ∈ IC    9×30 mod37={(9*30)%P} ∈ {fw((9*30)%P)}")
    print(f"  SA full product mod37={prod_SA} ∈ {fw(prod_SA)}")
    print()
    print("  100 mod 37 = 26 = the 137-map multiplier.")
    print("  The 100th theorem is GF(37) reading itself.")
    print()
    print("All assertions pass.")
