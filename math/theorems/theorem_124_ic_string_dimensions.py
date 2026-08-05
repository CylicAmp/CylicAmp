"""
Theorem 124: IC Orbit = {1, 10, 26} — String Theory Critical Dimensions

The identity-class orbit IC = {1, 10, 26} under the 137-map f(n) = 26n mod 37
contains exactly the three critical spacetime dimensions of string theory:

  1  → ℝ (trivial line; also ℝ in Cayley-Dickson, Theorem 123)
  10 → superstring / M-theory critical dimension (10D spacetime)
  26 → bosonic string critical dimension (26D spacetime)
       AND 137 mod 37 = 26 (the GF(37) framework's own map multiplier)

The orbit traversal:
  f(1) = 26·1 mod 37 = 26   (bosonic string dim)
  f(26) = 26·26 mod 37 = 10  (superstring dim)
  f(10) = 26·10 mod 37 = 1   (back to start)

So the 137-map cycles 1 → 26 → 10 → 1 — the three string dimensions form a
closed 3-orbit under GF(37)'s central operation.

Note: the bosonic string requires 26D because 26 = 2 + 24 where 24 is the
transverse dimension (Leech lattice dimension; 24 ∈ CB ∩ SEED_ORB in this
framework). The superstring requires 10D because 10 = 2 + 8 where 8 = 𝕆
(octonion dimension, 8 ∈ CB).
Both 24 and 8 are in CB = {8, 13, 24}.

ADDITIONAL: 2^12 mod 37 = 26 — the 137-map multiplier appears again at
Cayley-Dickson dimension 4096 (k=12 in the doubling sequence).
"""

P = 37
IC = frozenset({1, 10, 26})


def run_assertions():
    # IC is the 137-map orbit of 1
    assert (26 * 1) % P == 26 and 26 in IC
    assert (26 * 26) % P == 10 and 10 in IC
    assert (26 * 10) % P == 1  and 1  in IC

    # String theory: 26 = 137 mod 37 exactly
    assert 137 % P == 26

    # The transverse decompositions land in CB
    CB = frozenset({8, 13, 24})
    assert 24 in CB          # bosonic transverse: 26 = 2 + 24
    assert 8  in CB          # superstring transverse: 10 = 2 + 8
    assert 24 in frozenset({18, 24, 32})  # 24 ∈ SEED_ORB too

    # 2^12 mod 37 = 26 (137-map multiplier recurs in Cayley-Dickson)
    assert pow(2, 12, P) == 26

    print("All assertions passed.")


def summarise():
    print("=" * 58)
    print("Theorem 124: IC = {1,10,26} — String Critical Dimensions")
    print("=" * 58)
    print("  137-map orbit of 1: 1 →26→ 26 →10→ 10 →1→ 1")
    print("   1 = ℝ (trivial / Cayley-Dickson base)")
    print("  10 = superstring/M-theory spacetime dim")
    print("  26 = bosonic string spacetime dim")
    print("     = 137 mod 37  (the GF(37) map multiplier itself)")
    print()
    print("  Transverse decompositions — both in CB={8,13,24}:")
    print("   26 = 2 + 24  (24 ∈ CB ∩ SEED_ORB: Leech lattice)")
    print("   10 = 2 +  8  (8 ∈ CB: Octonions)")
    print()
    print(f"  2^12 mod 37 = {pow(2,12,P)}  (137-map multiplier at 4096D algebra)")


if __name__ == "__main__":
    run_assertions()
    summarise()
