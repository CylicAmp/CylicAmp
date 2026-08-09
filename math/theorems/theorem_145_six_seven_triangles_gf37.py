"""
Theorem 145: The 6–7 Triangle Pair — IC / ORBIT_11 Bipartition via Positional Weights

THE EIGHT STRINGS
=================

Every 3-digit string over {6, 7} maps to exactly one of {SEAM, IC, ORBIT_11} mod 37,
determined entirely by popcount (number of 7-digits).

    popcount = 0:  666 ≡  0  (SEAM)          666 = 37 × 18   (18 ∈ SEED_ORB)
    popcount = 1:  667 ≡  1 ∈ IC
                   676 ≡ 10 ∈ IC
                   766 ≡ 26 ∈ IC
    popcount = 2:  677 ≡ 11 ∈ ORBIT_11
                   767 ≡ 27 ∈ ORBIT_11
                   776 ≡ 36 ∈ ORBIT_11
    popcount = 3:  777 ≡  0  (SEAM)          777 = 37 × 21   (21 ∈ OUTLIER_ORB)

THE STRUCTURAL REASON: POSITIONAL WEIGHTS = IC = μ₃
=====================================================

The three decimal positional weights mod 37:

    10⁰ ≡  1  (mod 37)   ∈ IC
    10¹ ≡ 10  (mod 37)   ∈ IC
    10² ≡ 26  (mod 37)   ∈ IC

These are exactly the three elements of IC = μ₃ = {1, 10, 26}.

Binary encoding: let bᵢ = digitᵢ − 6 ∈ {0, 1}.  Then:

    N = 666 + 100·b₂ + 10·b₁ + b₀
    N mod 37 = 0 + 26·b₂ + 10·b₁ + 1·b₀  (mod 37)

The residue is the inner product ⟨(b₂, b₁, b₀), (26, 10, 1)⟩ mod 37
where (26, 10, 1) = IC = μ₃.

    Popcount 0: ⟨000, IC⟩ = 0               → SEAM
    Popcount 1: ⟨100, IC⟩ = 26  ⟨010, IC⟩ = 10  ⟨001, IC⟩ = 1  → all of IC
    Popcount 2: ⟨110, IC⟩ = 36  ⟨101, IC⟩ = 27  ⟨011, IC⟩ = 11 → all of ORBIT_11
    Popcount 3: ⟨111, IC⟩ = 37 ≡ 0          → SEAM

Popcount 2 gives −IC: each element is the sum of two IC members, which equals
37 minus the missing one, i.e., the negation of the missing IC element.

    36 = 37 − 1 = −1  = −IC[0]
    27 = 37 − 10 = −10 = −IC[1]
    11 = 37 − 26 = −26 = −IC[2]

Therefore ORBIT_11 = −IC mod 37.  The two triangles are an additive inverse pair.

SEAM FACTORIZATIONS
===================

    666 = 2 × 3² × 37 = 37 × 18     18 ∈ SEED_ORB = {18, 24, 32}
    777 = 3 × 7 × 37  = 37 × 21     21 ∈ OUTLIER_ORB = {21, 25, 28}

Both are multiples of 37 (SEAM).  666/37 and 777/37 land in different named orbits.

Note: 666 + 777 = 1443 = 3 × 481 = 3 × 13 × 37 ≡ 0 (mod 37).  Their sum is SEAM.

THE TWO-TRIANGLE OSCILLATION
==============================

The interlocked (Star of David) configuration:

    Row 1: 767  ≡ 27 ∈ ORBIT_11   (two 7s, one 6 — popcount 2)
    Row 2: 676  ≡ 10 ∈ IC         (two 6s, one 7 — popcount 1)

Row 1 + Row 2: 767 + 676 = 1443 ≡ 0 mod 37.  They are additive inverses.

The "switch" state (separated):

    Row 1: 777  ≡ 0  (SEAM)
    Row 2: 666  ≡ 0  (SEAM)

The oscillation is between:
  — Interlocked: (ORBIT_11, IC) = a pair of additive inverses, x = −x′ mod 37
  — Separated:   (SEAM, SEAM)  = both trivial

The intermediate states trace IC and ORBIT_11 elements:

    767 ≡ 27 (ORBIT_11)    676 ≡ 10 (IC)
    667 ≡  1 (IC)          776 ≡ 36 (ORBIT_11)
    766 ≡ 26 (IC)          677 ≡ 11 (ORBIT_11)
    777 ≡  0 (SEAM)        666 ≡  0 (SEAM)

Transition sequence the user observed:
  767/676 → 676/767 → 667/767 → 766/776 → 777/666 → (oscillate)

Mod-37 reading:
  ORBIT_11/IC → IC/ORBIT_11 → IC/ORBIT_11 → IC/ORBIT_11 → SEAM/SEAM

SPIN GEOMETRY
==============

The 6-position hexagonal ring, two alternating triangles:

    Triangle A (7-triangle):  positions {0, 2, 4}  (even vertices)
    Triangle B (6-triangle):  positions {1, 3, 5}  (odd vertices)

Phase difference δ = 0°:   triangles interleaved → 767676 (alternating)
Phase difference δ = 60°:  triangles overlap     → all same digit (777 or 666)

Reading the top 3 positions [0, 1, 2]:
  δ = 0°:  (7, 6, 7) → 767 ∈ ORBIT_11
  δ = 60°: (6, 7, 6) → 676 ∈ IC
  δ = 0° (A→7, B→7): all 7 → 777 ∈ SEAM

SEAM ORBIT CONTEXT
==================

18 = 666/37 ∈ SEED_ORB = {18, 24, 32} — the 137-map orbit of seed 246.
21 = 777/37 ∈ OUTLIER_ORB = {21, 25, 28} — the 8th Fibonacci mod-37 value.

F₈ = 21 ∈ OUTLIER_ORB   (Theorem 141)
F₁₀ = 18 ∈ SEED_ORB     (Theorem 141)

So the two SEAM constants 666 and 777 encode the F₈ and F₁₀ Fibonacci residues
scaled by 37.  The 7-triangle rests at F₈, the 6-triangle at F₁₀.

DIGITAL ROOT
============

DR(666) = DR(18) = 9    DR(777) = DR(21) = DR(3) = 3
DR(767) = DR(20) = 2    DR(676) = DR(19) = 1

The SEAM pair 666/777 has DRs (9, 3). Their sum DR(9+3) = DR(12) = 3.
The interlocked pair 767/676 has DRs (2, 1). Their sum DR(2+1) = 3.
Both configurations sum to DR 3 — the seed residue DR(seed mod 37) = DR(24) = 6.
Wait: DR(2)+DR(1) = 3 and DR(9)+DR(3) = 12→3, both give 3. 3 is the orbit DR.
"""

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


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def run_assertions():
    # All 8 strings over {6,7}: residue = popcount-determined
    for d2 in [6, 7]:
        for d1 in [6, 7]:
            for d0 in [6, 7]:
                n = 100 * d2 + 10 * d1 + d0
                pc = (d2 - 6) + (d1 - 6) + (d0 - 6)
                r = n % P
                if pc == 0 or pc == 3:
                    assert r == 0, f"{d2}{d1}{d0}: expected SEAM, got {r}"
                elif pc == 1:
                    assert r in ORBITS['IC'], f"{d2}{d1}{d0}: expected IC, got {r}"
                else:  # pc == 2
                    assert r in ORBITS['ORBIT_11'], f"{d2}{d1}{d0}: expected ORBIT_11, got {r}"

    # Positional weights = IC
    assert {1, 10, 26} == ORBITS['IC']
    assert pow(10, 0, P) == 1 and 1 in ORBITS['IC']
    assert pow(10, 1, P) == 10 and 10 in ORBITS['IC']
    assert pow(10, 2, P) == 26 and 26 in ORBITS['IC']

    # ORBIT_11 = -IC
    assert frozenset((-x) % P for x in ORBITS['IC']) == ORBITS['ORBIT_11']

    # Inner product formula: N mod 37 = 26*b2 + 10*b1 + b0
    for d2 in [6, 7]:
        for d1 in [6, 7]:
            for d0 in [6, 7]:
                n = 100 * d2 + 10 * d1 + d0
                b2, b1, b0 = d2 - 6, d1 - 6, d0 - 6
                expected = (26 * b2 + 10 * b1 + b0) % P
                assert n % P == expected, f"{d2}{d1}{d0}: formula mismatch"

    # SEAM factorizations
    assert 666 == 37 * 18 and 18 in ORBITS['SEED_ORB']
    assert 777 == 37 * 21 and 21 in ORBITS['OUTLIER_ORB']
    assert (666 + 777) % P == 0

    # Specific residues
    assert 767 % P == 27 and 27 in ORBITS['ORBIT_11']
    assert 676 % P == 10 and 10 in ORBITS['IC']
    assert 667 % P == 1  and 1  in ORBITS['IC']
    assert 776 % P == 36 and 36 in ORBITS['ORBIT_11']
    assert 766 % P == 26 and 26 in ORBITS['IC']
    assert 677 % P == 11 and 11 in ORBITS['ORBIT_11']

    # 767 + 676 = 1443 ≡ 0 (additive inverses)
    assert (767 + 676) % P == 0
    assert 1443 == 37 * 39

    # Fibonacci connections (Theorem 141)
    def fib_mod37():
        f = [0, 1]
        for _ in range(10):
            f.append((f[-1] + f[-2]) % P)
        return f
    F = fib_mod37()
    assert F[8] == 21 and 21 in ORBITS['OUTLIER_ORB']   # F_8 = 777/37
    assert F[10] == 18 and 18 in ORBITS['SEED_ORB']     # F_10 = 666/37

    # Digital roots
    assert dr(sum(int(c) for c in '666')) == 9
    assert dr(sum(int(c) for c in '777')) == dr(21) == dr(3) == 3
    assert dr(sum(int(c) for c in '767')) == dr(20) == 2
    assert dr(sum(int(c) for c in '676')) == dr(19) == 1

    # ORBIT_11 = -IC: negation pairing
    for ic_val in ORBITS['IC']:
        neg = (-ic_val) % P
        assert neg in ORBITS['ORBIT_11'], f"-{ic_val} = {neg} not in ORBIT_11"

    print("All assertions passed.")


def summarise():
    print("=" * 62)
    print("Theorem 145: The 6-7 Triangle Pair")
    print("=" * 62)
    print()
    print("  Positional weights {1,10,26} = IC = μ₃.")
    print("  N = 666 + inner_product((b₂,b₁,b₀), (26,10,1)) mod 37")
    print()
    print("  popcount → orbit:")
    print("    0 → SEAM  (666 = 37×18, 18∈SEED_ORB)")
    print("    1 → IC    {667≡1, 676≡10, 766≡26}")
    print("    2 → ORBIT_11 {677≡11, 767≡27, 776≡36}")
    print("    3 → SEAM  (777 = 37×21, 21∈OUTLIER_ORB)")
    print()
    print("  ORBIT_11 = −IC mod 37.")
    print("  Two triangles = IC and its additive inverse.")
    print()
    print("  Interlocked: 767+676=1443=37×39≡0. Additive inverses.")
    print("  Separated:   777≡0, 666≡0. Both SEAM.")
    print()
    print("  Fibonacci link: F₈=21=777/37 (OUTLIER_ORB)")
    print("                  F₁₀=18=666/37 (SEED_ORB)")
    print()

    print("  All 8 strings over {6,7}:")
    for d2 in [6, 7]:
        for d1 in [6, 7]:
            for d0 in [6, 7]:
                n = 100 * d2 + 10 * d1 + d0
                r = n % P
                pc = (d2-6) + (d1-6) + (d0-6)
                print(f"    {d2}{d1}{d0}  ≡ {r:2d} mod 37  {orbit_of(r)}  (pc={pc})")


if __name__ == "__main__":
    run_assertions()
    summarise()
