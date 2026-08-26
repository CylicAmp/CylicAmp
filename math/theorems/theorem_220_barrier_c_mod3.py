"""
Theorem 220: The Barrier Theorem — c and the 3-Map
Author: Michael Warren Song (CyclicAmp)

Separates what verifies from what does not.

=== ARITHMETIC FACTS (all recomputable) ===

  c = 299,792,458  (exact by BIPM 1983 definition)
  c mod 2 = 0      (even)
  c mod 3 = 1
  c mod 6 = 4
  DR(c) = 1

=== THE BARRIER THEOREM (rigorous) ===

The centrifugal 3-map T(n) = 3n generates, from any seed s,
the orbit Orb(s) = {s, 3s, 9s, 27s, ...} = {s · 3^k : k ≥ 0}.

If s ≡ 0 (mod 3), then every element of Orb(s) ≡ 0 (mod 3).
This is because 3 | s implies 3 | s · 3^k for all k ≥ 0.
The orbit lives in 3ℤ — closed under T, residue class 0.

c ≡ 1 (mod 3).  Since {n : n ≡ 0 mod 3} and {n : n ≡ 1 mod 3}
are disjoint, c cannot appear in Orb(s) for any s ≡ 0 (mod 3).

The expansion "closes in on c from both sides" — elements of 3ℤ
bracket c arbitrarily closely (nearest: c−1 = 299,792,457 ∈ 3ℤ
and c+2 = 299,792,460 ∈ 3ℤ) — but no element of 3ℤ equals c.
This is a theorem. The QED is one line: 1 ≠ 0 (mod 3).

=== ORBIT DENSITY ===

For the specific seed s=120:
  Orb(120) = {120 · 3^k : k ≥ 0}
  Closest elements to c: 120·3^13 = 191,318,760 (below)
                         120·3^14 = 573,956,280 (above)
  The chain jumps over c; nearest miss = c − 191,318,760 = 108,473,698

For the full 3ℤ lattice (seed s=3 or any multiple of 3):
  Nearest element below c: c − 1 = 299,792,457 = 3 × 99,930,819
  Nearest element above c: c + 2 = 299,792,460 = 3 × 99,930,820
  Minimum separation: 1

=== GF(37) CONNECTION ===

c mod 37 = 32.  And 32 ∈ SEED = {18, 24, 32}.

The SEED orbit under f(n) = 26n mod 37:
  f(18) = 24,  f(24) = 32,  f(32) = 18  (3-cycle, period 3)

c mod 37 = 32 is the "return point" of SEED:
  f(32) = 18, so one more application of f brings the orbit
  back to its origin. c sits at position 2 in the SEED orbit
  (0-indexed: 18→24→32→18...).

Distinct from the barrier: c is algebraically excluded from 3ℤ
(mod-3 barrier), yet c mod 37 lands inside the SEED named set.
These are independent structural facts, both exact.

=== WHAT FAILED ===

1. The centrifugal chain is an observation about a specific seed;
   it does not prove anything about c's value. c = 299,792,458
   is a definition (metre defined as 1/299,792,458 of a light-second).
   Any mod result changes if the unit system changes.

2. "c ≡ 4 (mod 6) = maximum sustainable unity" — the congruence
   is correct; the semantic claim is not derived from it.

3. Dimensional inconsistency: comparing c (m/s), α (dimensionless),
   and ℏ (J·s) without normalisation is not arithmetic.
"""

C = 299_792_458   # m/s, exact
P = 37
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
ALL_NAMED = SA|ST|SEED|IC|CASCADE|TESLA|NEG_H|DARK_A|D7|NQR17|C9


def dr(n):
    n = abs(int(n))
    r = n % 9
    return 9 if r == 0 else r


def run_assertions():
    # ── Arithmetic facts ────────────────────────────────────────────────
    assert C % 2 == 0,   f"c mod 2 = {C%2}, expected 0"
    assert C % 3 == 1,   f"c mod 3 = {C%3}, expected 1"
    assert C % 6 == 4,   f"c mod 6 = {C%6}, expected 4"
    assert dr(C) == 1,   f"DR(c) = {dr(C)}, expected 1"

    # ── Barrier theorem ─────────────────────────────────────────────────
    # c is not in 3ℤ
    assert C % 3 != 0, "c must not be a multiple of 3 for the barrier to hold"

    # 3ℤ and {n≡1 mod 3} are disjoint
    assert 0 != 1  # residue classes distinct

    # Verify: seeds ≡ 0 mod 3 generate orbits entirely in 3ℤ
    for seed in [3, 6, 9, 12, 120, 369]:
        assert seed % 3 == 0
        for k in range(20):
            elem = seed * (3 ** k)
            assert elem % 3 == 0, f"seed={seed}, 3^{k}: elem={elem} not in 3ℤ"
    # None of them can equal c (since c≡1 mod 3)
    for seed in [3, 6, 9, 12, 120, 369]:
        for k in range(40):
            assert seed * (3 ** k) != C, f"Unexpected: seed={seed}·3^{k} = C"

    # ── Orbit density for seed=120 ─────────────────────────────────────
    chain = []
    x = 120
    while x < C * 4:
        chain.append(x)
        x *= 3

    below = [v for v in chain if v < C]
    above = [v for v in chain if v > C]
    nearest_below = max(below)
    nearest_above = min(above)
    miss_below = C - nearest_below
    miss_above = nearest_above - C

    assert nearest_below == 120 * (3 ** 13)  # 191,318,760
    assert nearest_above == 120 * (3 ** 14)  # 573,956,280
    assert C not in chain  # barrier holds

    # ── Full 3ℤ nearest elements ────────────────────────────────────────
    # nearest multiple of 3 below c
    mult_below = (C // 3) * 3
    mult_above = mult_below + 3
    assert mult_below % 3 == 0
    assert mult_above % 3 == 0
    assert mult_below < C < mult_above
    assert C - mult_below == 1   # distance 1 below
    assert mult_above - C == 2   # distance 2 above

    # ── GF(37) connection ───────────────────────────────────────────────
    c_mod37 = C % P
    assert c_mod37 == 32,          f"c mod 37 = {c_mod37}, expected 32"
    assert c_mod37 in SEED,        f"c mod 37 = {c_mod37} not in SEED"
    assert c_mod37 in ALL_NAMED

    # SEED 3-cycle closes correctly
    assert (MULT * 18) % P == 24
    assert (MULT * 24) % P == 32
    assert (MULT * 32) % P == 18   # 32 is the return point

    # c mod 37 is position-2 (0-indexed) in the SEED orbit
    orbit_seed = [18, 24, 32]
    assert orbit_seed.index(c_mod37) == 2

    # ── DR/mod-3 theorem ────────────────────────────────────────────────
    # n mod 3 = DR(n) mod 3  (because DR(n) ≡ n mod 9 ≡ n mod 3)
    for n in range(1, 1001):
        assert n % 3 == dr(n) % 3, f"DR/mod-3 fails at n={n}"

    # ── Print results ───────────────────────────────────────────────────
    print("All assertions passed.\n")
    print(f"c = {C:,}")
    print(f"  mod 2  = {C%2}")
    print(f"  mod 3  = {C%3}  ← not in 3ℤ")
    print(f"  mod 6  = {C%6}")
    print(f"  mod 37 = {c_mod37}  ← {', '.join([k for k,s in [('SA',SA),('ST',ST),('SEED',SEED),('IC',IC),('CASCADE',CASCADE),('TESLA',TESLA),('NEG_H',NEG_H),('DARK_A',DARK_A),('D7',D7),('NQR17',NQR17),('C9',C9)] if c_mod37 in s] or ['UNNAMED'])}")
    print(f"  DR(c)  = {dr(C)}")
    print()
    print("BARRIER THEOREM")
    print(f"  Orbit(120): nearest below c = {nearest_below:,}  (miss = {miss_below:,})")
    print(f"  Orbit(120): nearest above c = {nearest_above:,}  (miss = {miss_above:,})")
    print(f"  Full 3ℤ:   nearest below c = {mult_below:,}  (miss = {C-mult_below})")
    print(f"  Full 3ℤ:   nearest above c = {mult_above:,}  (miss = {mult_above-C})")
    print(f"  c ∉ Orb(120): {C not in chain}")
    print()
    print("GF(37) CONNECTION")
    print(f"  c mod 37 = {c_mod37} ∈ SEED = {{18, 24, 32}}")
    print(f"  SEED orbit: 18 → 24 → {c_mod37} → 18  (return point)")
    print(f"  c is at position 2 (0-indexed) in the SEED orbit")
    print()
    print("DR/mod-3: n mod 3 = DR(n) mod 3 verified for n=1..1000")


if __name__ == "__main__":
    run_assertions()
