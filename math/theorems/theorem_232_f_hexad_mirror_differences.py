"""
Theorem 232: F-Hexad Mirror Differences — Complement Involution and 1/137 Orbit Generation
Author: Michael Warren Song (CyclicAmp)

The F-cycle 1→2→4→8→7→5 (doubling mod 9) forms a hexagon.
Mirror subtraction of adjacent 8-digit alternating strings extracts complement pairs.
All three resulting values are exactly divisible by 137 and each generates a full GF(37) orbit.

=== THE F-HEXAD ===

F-cycle: doubling map x ↦ 2x mod 9 on {1,...,8}.
  1→2→4→8→7→5→1   (period 6; 2 is a primitive root mod 9 restricted to the F-nodes)

Three diameters (complement pairs, d+d'=9):
  1↔8,  2↔7,  4↔5

O-oscillator: 3↔6  (complement pair outside F-cycle)
Spine: 9↔0

All five pairs sum to 9.  The involution is x ↦ 9-x = ×8 mod 9 (since 8≡-1 mod 9).

=== MIRROR DIFFERENCE TABLE (8-digit alternating strings) ===

For each adjacent F-edge (a,b), form alternating strings and subtract:
  |abababab - babababa|

Edge   Gap   Mirror difference   Block   DR   mod 37
(1,2)   1    9090909             90      9    9  ∈ SA_ST_A
(2,4)   2    18181818            18      9    18 ∈ SEED
(4,8)   4    36363636            36      9    36 ∈ NEG_H
(8,7)   1    9090909             90      9    9  ∈ SA_ST_A
(7,5)   2    18181818            18      9    18 ∈ SEED
(5,1)   4    36363636            36      9    36 ∈ NEG_H

Every subtraction yields digit sum 36 → DR = 9.
Three distinct values correspond to three gap sizes (1, 2, 4).
Gaps (1, 2, 4) are the first half of the F-cycle (doublings from 1).

=== FACTORIZATION: 1010101 IS THE REPEATING UNIT ===

9090909  = 9  × 1010101
18181818 = 18 × 1010101  (= 2 × 9090909)
36363636 = 36 × 1010101  (= 4 × 9090909)

1010101 mod 37 = 1  ∈ IC  (identity cycle — unit in GF(37))

=== 1/137: EXACT DIVISIBILITY AND ORBIT GENERATION ===

All three differences are exactly divisible by 137 (no remainder):

  9090909  ÷ 137 = 66357     (exact)
  18181818 ÷ 137 = 132714    (exact)
  36363636 ÷ 137 = 265428    (exact)

For each difference d, the triple {d mod 37, (d÷137) mod 37, (d×137) mod 37}
equals the COMPLETE GF(37) orbit of d:

  d=9090909:   mods = {9, 16, 12} = SA_ST_A = {9, 12, 16}
  d=18181818:  mods = {18, 32, 24} = SEED = {18, 24, 32}
  d=36363636:  mods = {36, 27, 11} = NEG_H = {11, 27, 36}

The mirror differences generate exactly three GF(37) orbits via the 137-action:
  SA_ST_A  (contains 9∈SA, 12∈ST)
  SEED     (the seed orbit: 246 mod 37 = 24 ∈ SEED)
  NEG_H    (contains 36 = -1 mod 37)

Connection: 1010101 × 137 mod 37 = 26 = MULT (the 137-map multiplier itself).

=== COMPLEMENT PAIRS IN GF(37) ===

Pair     Sum   Role          GF(37) orbits
1+8=9    9     F-diameter    1∈IC,      8∈TESLA
2+7=9    9     F-diameter    2∈DARK_A,  7∈D7
4+5=9    9     F-diameter    4∈C3,      5∈CAS_EXT
3+6=9    9     O-oscillator  3∈C3,      6∈TESLA
9+0=9    9     spine         9∈SA_ST_A, 0=SEAM

Each complement pair straddles two distinct GF(37) orbits.
The involution d ↦ 9-d corresponds to ×8 mod 9 (since 8≡-1 mod 9).
8 ∈ TESLA = CASCADE∩TESLA: the complement involution lives in the CASCADE/TESLA orbit.

=== TWIN PRIMES ===

1010101 = 73 × 101 × 137.  All three prime factors are members of twin prime pairs:
  73:  twin pair (71, 73)  — 71 mod37=34∈D7,   73 mod37=36∈NEG_H
  101: twin pair (101,103) — 101 mod37=27∈NEG_H, 103 mod37=29∈C9
  137: twin pair (137,139) — 137 mod37=26∈IC,   139 mod37=28∈SA_ST_B

Both 73 and 101 land in NEG_H.  137 lands in IC (the 137-map multiplier orbit).
The repeating unit 1010101 is a product of three twin-prime members spanning
two distinct orbits: NEG_H (two members) and IC (one member).

137 is itself a twin prime.  Its pair element 139 mod37=28∈SA_ST_B.

=== SOPHIE GERMAIN PRIMES ===

A Sophie Germain prime p: p prime and 2p+1 prime (safe prime).

The prime factors of all F-hexad differences: {2, 3, 73, 101, 137}.
  3∈C3 is Sophie Germain: 2×3+1=7∈D7.  (3,7) straddles C3 and D7.
  2∈DARK_A is Sophie Germain: 2×2+1=5∈CAS_EXT.  (2,5) straddles DARK_A and CAS_EXT.
  73, 101, 137: none are Sophie Germain.

Sophie Germain factor 3 appears in all three differences (9090909, 18181818, 36363636).
Sophie Germain factor 2 appears in 18181818 and 36363636 (the two even differences).

The safe prime 7∈D7 is the Sophie image of 3∈C3.
The safe prime 5∈CAS_EXT is the Sophie image of 2∈DARK_A.

=== RIEMANN HYPOTHESIS ===

Mirror difference orbits and matching Riemann zero floors:
  SA_ST_A: γ₁₀≈49.773 → floor=49 → mod37=12∈SA_ST_A  (same orbit as 9090909)
  SEED:    γ₅ ≈32.935 → floor=32 → mod37=32∈SEED       (same orbit as 18181818)
  NEG_H:   γ₉ ≈48.005 → floor=48 → mod37=11∈NEG_H      (same orbit as 36363636)

Each mirror difference orbit matches a Riemann zero within the first 10 zeros.
"""

import mpmath

mpmath.mp.dps = 15

P    = 37
MULT = 26

SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
SEED    = {18, 24, 32}
IC      = {1, 10, 26}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}
D7      = {7, 33, 34}
NEG_H   = {11, 27, 36}
SA_ST_A = {9, 12, 16}
DARK_A  = {2, 15, 20}
C3      = {3, 4, 30}
CAS_EXT = {5, 13, 19}
C9      = {14, 29, 31}
NQR17   = {17, 22, 35}
SA_ST_B = {21, 25, 28}

ORBITS = {
    'IC': IC, 'DARK_A': DARK_A, 'C3': C3, 'CAS_EXT': CAS_EXT,
    'TESLA': TESLA, 'D7': D7, 'SA_ST_A': SA_ST_A, 'NEG_H': NEG_H,
    'C9': C9, 'NQR17': NQR17, 'SEED': SEED, 'SA_ST_B': SA_ST_B,
}

def orb(n):
    r = n % P
    if r == 0: return 'SEAM'
    for name, s in ORBITS.items():
        if r in s: return name

def dr(n):
    n = abs(int(n))
    while n >= 10: n = sum(int(d) for d in str(n))
    return n

def alt8(a, b):
    return int(''.join([str(a if i % 2 == 0 else b) for i in range(8)]))


def run_assertions():
    # ── F-cycle: doubling mod 9 ───────────────────────────────────────────────
    F = [1, 2, 4, 8, 7, 5]
    x = 1
    for f in F:
        assert x == f
        x = (x * 2) % 9 or 9   # 0 mod 9 → 9 not reached here
    # Verify: 5×2=10, 10 mod 9=1, back to start
    assert (5 * 2) % 9 == 1

    # ── Complement involution: ×8 ≡ -1 mod 9 ─────────────────────────────────
    for x in range(1, 9):
        assert (x * 8) % 9 == (9 - x) % 9

    # ── Mirror differences ────────────────────────────────────────────────────
    edges = [(1,2), (2,4), (4,8), (8,7), (7,5), (5,1)]
    expected_diffs = {1: 9090909, 2: 18181818, 4: 36363636}

    for a, b in edges:
        hi, lo = sorted([alt8(a,b), alt8(b,a)], reverse=True)
        diff = hi - lo
        gap = abs(a - b)
        assert diff == expected_diffs[gap], f"({a},{b}): {diff} ≠ {expected_diffs[gap]}"
        assert dr(diff) == 9
        assert sum(int(d) for d in str(diff)) == 36

    # ── 1010101 factorization ─────────────────────────────────────────────────
    unit = 1010101
    assert 9090909  == 9  * unit
    assert 18181818 == 18 * unit
    assert 36363636 == 36 * unit
    assert unit % P == 1 and 1 in IC   # 1010101 mod 37 = 1 ∈ IC
    assert (unit * 137) % P == MULT    # 1010101 × 137 mod 37 = 26 = MULT

    # ── Exact divisibility by 137 ─────────────────────────────────────────────
    assert 9090909  % 137 == 0
    assert 18181818 % 137 == 0
    assert 36363636 % 137 == 0

    # ── 137-action generates complete GF(37) orbits ───────────────────────────
    d1, d2, d3 = 9090909, 18181818, 36363636

    # d1=9090909 → SA_ST_A = {9,12,16}
    assert {d1 % P, (d1 // 137) % P, (d1 * 137) % P} == SA_ST_A

    # d2=18181818 → SEED = {18,24,32}
    assert {d2 % P, (d2 // 137) % P, (d2 * 137) % P} == SEED

    # d3=36363636 → NEG_H = {11,27,36}
    assert {d3 % P, (d3 // 137) % P, (d3 * 137) % P} == NEG_H

    # ── Complement pair orbits ────────────────────────────────────────────────
    assert 1 in IC and 8 in TESLA          # 1+8=9, F-diameter
    assert 2 in DARK_A and 7 in D7        # 2+7=9, F-diameter
    assert 4 in C3 and 5 in CAS_EXT       # 4+5=9, F-diameter
    assert 3 in C3 and 6 in TESLA         # 3+6=9, O-oscillator
    assert 9 in SA_ST_A                    # spine
    assert 8 in TESLA and 8 in CASCADE    # involution operator ×8≡-1 mod 9 ∈ TESLA

    # ── Riemann: one zero per mirror-difference orbit in first 10 ────────────
    zero_orbits_first10 = set()
    for n in range(1, 11):
        g = float(mpmath.im(mpmath.zetazero(n)))
        zero_orbits_first10.add(orb(int(g)))

    assert 'SA_ST_A' in zero_orbits_first10   # γ₁₀ floor=49 mod37=12∈SA_ST_A
    assert 'SEED'    in zero_orbits_first10   # γ₅  floor=32∈SEED
    assert 'NEG_H'   in zero_orbits_first10   # γ₉  floor=48 mod37=11∈NEG_H

    # ── Twin primes ───────────────────────────────────────────────────────────
    from sympy import isprime as _isp, factorint as _fac
    # 137 is a twin prime; 139 is its pair
    assert _isp(137) and _isp(139)
    assert 139 % P == 28 and 28 in SA_ST_B

    # 1010101 = 73 × 101 × 137 — all prime, all twin-prime members
    assert _fac(1010101) == {73: 1, 101: 1, 137: 1}
    assert all(_isp(f) for f in [73, 101, 137])
    # twin pairs: (71,73), (101,103), (137,139)
    assert _isp(71) and _isp(73)
    assert _isp(101) and _isp(103)
    # GF(37) orbits of twin-prime factors
    assert 71 % P == 34 and 34 in D7
    assert 73 % P == 36 and 36 in NEG_H
    assert 101 % P == 27 and 27 in NEG_H      # both 73 and 101 in NEG_H
    assert 103 % P == 29 and 29 in C9
    assert 137 % P == 26 and 26 in IC

    # ── Sophie Germain primes ─────────────────────────────────────────────────
    from sympy import isprime as _isp2
    def is_sophie(p): return _isp2(p) and _isp2(2*p+1)

    # 3∈C3 is Sophie Germain → safe prime 7∈D7
    assert is_sophie(3) and 3 in C3
    assert _isp2(7) and 7 in D7 and 2*3+1 == 7

    # 2∈DARK_A is Sophie Germain → safe prime 5∈CAS_EXT
    assert is_sophie(2) and 2 % P == 2  # 2∈DARK_A via orbit
    assert _isp2(5) and 5 in CAS_EXT and 2*2+1 == 5

    # 3 divides all three differences; 2 divides the two even differences
    assert 9090909  % 3 == 0
    assert 18181818 % 3 == 0 and 18181818 % 2 == 0
    assert 36363636 % 3 == 0 and 36363636 % 2 == 0

    # 73, 101, 137 are not Sophie Germain
    assert not is_sophie(73) and not is_sophie(101) and not is_sophie(137)

    # Verify specific zeros
    g10 = float(mpmath.im(mpmath.zetazero(10)))
    assert int(g10) % P == 12 and 12 in SA_ST_A

    g5 = float(mpmath.im(mpmath.zetazero(5)))
    assert int(g5) % P == 32 and 32 in SEED

    g9 = float(mpmath.im(mpmath.zetazero(9)))
    assert int(g9) % P == 11 and 11 in NEG_H

    print("All assertions passed.")
    print()
    print("F-HEXAD MIRROR DIFFERENCES — T232")
    print()
    print("F-cycle: 1→2→4→8→7→5  (×2 mod 9)")
    print("Complement involution: x↦9-x = ×8≡-1 mod 9  (8∈TESLA)")
    print()
    print(f"{'Edge':>6}  {'Gap':>3}  {'Difference':>12}  {'mod37':>5}  {'Orbit':>10}  137-generated orbit")
    for d, orbit_name, full_orb in [
        (9090909,  'SA_ST_A', SA_ST_A),
        (18181818, 'SEED',    SEED),
        (36363636, 'NEG_H',   NEG_H),
    ]:
        gen = {d % P, (d // 137) % P, (d * 137) % P}
        assert gen == full_orb
        print(f"  gap {36363636//d:1d}:  {d:>12d}  {d%P:>5}  {orbit_name:>10}  {sorted(gen)} = complete orbit")
    print()
    print("Factorization: d = k × 9 × 1010101  (k = gap)")
    print(f"  1010101 mod 37 = 1 ∈ IC")
    print(f"  1010101 × 137 mod 37 = {(1010101*137)%P} = MULT")
    print()
    print("Complement pairs and GF(37) orbits:")
    for a, b, role in [(1,8,'F-dia'),(2,7,'F-dia'),(4,5,'F-dia'),(3,6,'O-osc'),(9,0,'spine')]:
        ob = f"{orb(a)}, {orb(b) if b else 'SEAM'}"
        print(f"  {a}+{b}=9  {role}:  {ob}")
    print()
    print("Riemann zeros (first 10) with floor mod 37 in mirror-difference orbits:")
    for n in range(1, 11):
        g = float(mpmath.im(mpmath.zetazero(n)))
        o = orb(int(g))
        if o in ('SA_ST_A','SEED','NEG_H'):
            print(f"  γ_{n}≈{g:.4f} floor={int(g)} mod37={int(g)%P}∈{o}")


if __name__ == "__main__":
    run_assertions()
