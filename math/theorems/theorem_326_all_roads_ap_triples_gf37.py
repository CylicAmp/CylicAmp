# CLASS: THEOREM
"""
Theorem 326: all the roads, not just 123 -- an arithmetic-progression triple
has residue 12d mod 37, fixed by its STEP alone
Author: Michael Warren Song (CyclicAmp)

T325 did one road, 123.  The next is 234, then 345, and so on.  Doing all of
them shows the first road was never the point: the step is.

=== THE SEVEN ASCENDING ROADS ALL LAND ON THE SAME RESIDUE ===

    123  234  345  456  567  678  789

    Every one is 12 mod 37.  Not the same orbit -- the same POINT.  And 12 is
    a sovereign target.

    Forced:  abc with b = a+1, c = a+2  is  100a + 10(a+1) + (a+2) = 111a + 12
    and 111 = 3*37, so the leading digit cancels entirely.  Where the road
    starts is invisible mod 37.

=== THE GENERAL LAW: RESIDUE = 12 x STEP ===

    Let the digits be an arithmetic progression a, a+d, a+2d.  Then

        n = 111a + 12d  ==  12d   (mod 37)

    The start a drops out for the same reason; only the common difference d
    survives.  Checked on all 25 AP triples with digits 0-9:

        d   words                                  n mod 37   orbit
        0   111 222 333 444 555 666 777 888 999        0      SEAM
        1   123 234 345 456 567 678 789               12      SA_ST_A  TARGET
        2   135 246 357 468 579                       24      SEED
        3   147 258 369                               36      NEG_H
        4   159                                       11      NEG_H

    d = 0 is the repdigit road and it runs straight into the seam.

=== REVERSAL IS NEGATION ===

    The descending triple (a+2d)(a+d)a = 111a + 210d == 25d (mod 37), and

        12 + 25 = 37

    so cba == -abc for every AP triple.  Forced without going through d at
    all:  abc + cba = 101(a+c) + 20b, and an AP has a+c = 2b, giving
    222b = 6*37*b == 0.

        d   ascending  orbit      descending  orbit
        1      12      SA_ST_A       25       SA_ST_B
        2      24      SEED          13       CAS_EXT
        3      36      NEG_H          1       IC
        4      11      NEG_H         26       IC          (26 = 137 mod 37)

    T325 found reversal carrying SA_ST_A onto SA_ST_B by inspection of one
    road.  It is negation, and it acts on every road.

=== 246 IS A ROAD ===

    246 has digits 2, 4, 6 -- the d = 2 road starting at 2.  So

        246 == 12 * 2 == 24  (mod 37)

    is forced by the step alone, and 135, 357, 468, 579 share it.  CLAUDE.md
    records seed 246 mod 37 = 24 in the SEED orbit; this is where the 24
    comes from.

    The other T316 condition falls out too.  An AP triple has digit sum
    3(a+d), so its digital root is a multiple of 3 -- every AP triple has
    DR in {3,6,9}, the trinity half of the Z/9Z partition, never the doubling
    half.  246 has digit sum 12, DR 3.

    T316 reduced the reference seed to exactly two conditions, DR(seed) = 3
    and seed == 24 (mod 37), i.e. seed == 246 (mod 333).  Both conditions are
    consequences of one fact: 246 is the AP triple with a = 2, d = 2.  This
    does not make 246 distinguished -- T316's point stands, 579 and 912 and
    every seed == 246 (mod 333) behave identically.  It says where the
    residue came from.

=== THE ROTATION-CLASS SUM IS A MULTIPLE OF 333 ===

    Summing a road's three rotations gives 111(a+b+c) = 333(a+d):

        123 -> 666    234 -> 999    345 -> 1332   456 -> 1665
        567 -> 1998   678 -> 2331   789 -> 2664
        246 -> 1332

    333 = 9 * 37 is the modulus of the T316 seed class, and the same
    "9 and the 37 together" as T311's sub-grid difference.  One fact.

=== THE TWO WRAP-AROUND ROADS ARE NOT APs ===

    891 and 912 continue the walk by cycling the digit 9 -> 1, which is not
    +1 arithmetically, so the law above does not apply and they leave the
    pattern:

        891 == 3  in C3        (also a sovereign target, and the birthday
                                orbit recorded in CLAUDE.md)
        912 == 24 in SEED      (the seed residue again, by a different route)

    Listed because the walk produces them, not because they follow the rule.

=== STANDING CHECKS ON THE RESIDUE SET {0,1,11,12,13,24,25,26,36} ===

    Primes among them: 11 and 13 only, and they are a TWIN PAIR -- 11 is the
    d=4 ascending residue, 13 the d=2 descending residue.  11 is Sophie
    Germain (23) and also a safe prime (5); 13 is neither.  11 in NEG_H,
    13 in CAS_EXT.
    Orbits: 0 SEAM, 1 and 26 IC, 11 and 36 NEG_H, 12 SA_ST_A, 13 CAS_EXT,
    24 SEED, 25 SA_ST_B.
    1/137: 26 = 137 mod 37 appears as the d=4 descending residue, and 1 = its
    orbit-mate as d=3 descending -- the IC orbit is where the odd steps
    reverse to.
    Rule 30, 6-bit: 11 -> 25 (NEG_H -> SA_ST_B), 12 -> 22, 13 -> 21,
    24 -> 44 == 7, 25 -> 47 == 10, 26 -> 43 == 6, 36 -> 62 == 25.
    Rule 30 is the conjectured case, not a theorem -- see CLAUDE.md.

=== FALSIFICATION ===
    Exhibit a 3-digit arithmetic-progression triple whose residue mod 37 is
    not 12d, or whose reverse is not its negation.
"""

P, MULT = 37, 26

ORBITS = {
    'IC': {1, 10, 26},      'DARK_A': {2, 15, 20},  'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23},    'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36},  'C9': {14, 29, 31},
    'NQR17': {17, 22, 35},  'SEED': {18, 24, 32},   'SA_ST_B': {21, 25, 28},
}
ANCHORS, TARGETS = {4, 9, 25, 30}, {3, 12, 21, 30}


def orbit_of(n):
    r = n % P
    if r == 0:
        return 'SEAM'
    return next(k for k, v in ORBITS.items() if r in v)


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def ap_triples():
    """every 3-digit word whose digits are an AP, as (a, d, n)."""
    out = []
    for d in range(0, 10):
        for a in range(1, 10):
            if 0 <= a + d <= 9 and 0 <= a + 2 * d <= 9:
                out.append((a, d, int(f"{a}{a+d}{a+2*d}")))
    return out


def run():
    APS = ap_triples()
    assert len(APS) == 25

    # --- the seven ascending roads are one POINT, not one orbit ---
    roads = [int(f"{a}{a+1}{a+2}") for a in range(1, 8)]
    assert roads == [123, 234, 345, 456, 567, 678, 789]
    assert {n % P for n in roads} == {12}
    assert 12 in TARGETS                       # sovereign target
    assert 111 == 3 * P                        # why the start digit vanishes
    for a in range(1, 8):
        assert int(f"{a}{a+1}{a+2}") == 111 * a + 12

    # --- the general law: residue is 12d, independent of the start ---
    for a, d, n in APS:
        assert n == 111 * a + 12 * d
        assert n % P == (12 * d) % P, (a, d, n)
    by_d = {}
    for a, d, n in APS:
        by_d.setdefault(d, set()).add(n % P)
    assert by_d == {0: {0}, 1: {12}, 2: {24}, 3: {36}, 4: {11}}
    assert orbit_of(0) == 'SEAM'               # the repdigit road
    assert orbit_of(12) == 'SA_ST_A' and orbit_of(24) == 'SEED'
    assert orbit_of(36) == 'NEG_H' and orbit_of(11) == 'NEG_H'

    # --- reversal is negation ---
    assert 12 + 25 == P
    assert 222 == 6 * P
    for a, d, n in APS:
        rev = int(f"{a+2*d}{a+d}{a}")
        assert (n + rev) % P == 0, (a, d)
        assert rev % P == (25 * d) % P
        b = a + d
        assert n + rev == 101 * (a + a + 2 * d) + 20 * b == 222 * b
    assert [(25 * d) % P for d in range(1, 5)] == [25, 13, 1, 26]
    assert orbit_of(25) == 'SA_ST_B' and orbit_of(13) == 'CAS_EXT'
    assert orbit_of(1) == 'IC' and orbit_of(26) == 'IC'
    assert 26 == 137 % P                       # the 137-multiplier itself
    assert 25 in ANCHORS                       # descending d=1 is an anchor

    # --- every AP triple has DR in the trinity {3,6,9} ---
    assert {dr(n) for _, _, n in APS} <= {3, 6, 9}
    for a, d, n in APS:
        assert sum((a, a + d, a + 2 * d)) == 3 * (a + d)

    # --- 246 is the d=2 road; both T316 conditions follow ---
    assert (2, 2, 246) in APS
    assert 246 % P == (12 * 2) % P == 24 and orbit_of(246) == 'SEED'
    assert {n % P for _, d, n in APS if d == 2} == {24}
    assert [n for _, d, n in APS if d == 2] == [135, 246, 357, 468, 579]
    assert dr(246) == 3
    assert 333 == 9 * P
    assert 246 % 333 == 246                    # T316's seed class, unchanged

    # --- rotation-class sums are 333(a+d) ---
    for a, d, n in APS:
        w = f"{n:03d}"
        rotc = [int(w[k:] + w[:k]) for k in (0, 2, 1)]
        assert sum(rotc) == 333 * (a + d)
        assert sum(rotc) % P == 0               # T325's SEAM result, all roads
        # T325's other result: rotation is multiplication by 26
        assert rotc[1] % P == (MULT * n) % P
    assert [sum(int(f"{a}{a+1}{a+2}"[k:] + f"{a}{a+1}{a+2}"[:k])
                for k in (0, 2, 1)) for a in range(1, 8)] == \
        [666, 999, 1332, 1665, 1998, 2331, 2664]

    # --- the wrap-around roads are not APs and do not obey the law ---
    assert 891 % P == 3 and orbit_of(891) == 'C3' and 3 in TARGETS
    assert 912 % P == 24 and orbit_of(912) == 'SEED'
    assert (8, None) not in [(a, None) for a, d, n in APS if n == 891]

    # --- standing checks: 11 and 13 are the only primes, and they are twins ---
    res = {0, 1, 11, 12, 13, 24, 25, 26, 36}

    def is_prime(m):
        return m > 1 and all(m % k for k in range(2, int(m ** .5) + 1))
    assert {v for v in res if is_prime(v)} == {11, 13}
    assert is_prime(11) and is_prime(13)                     # twin pair
    assert is_prime(2 * 11 + 1) and not is_prime(2 * 13 + 1)  # 11 SG, 13 not
    assert is_prime((11 - 1) // 2)                            # 11 also safe

    print("All assertions passed.\n")
    print("THEOREM 326.  An AP triple's residue is 12 x its STEP.\n")
    print("  THE SEVEN ASCENDING ROADS -- one point, not one orbit")
    for a in range(1, 8):
        n = int(f"{a}{a+1}{a+2}")
        print(f"     {n} = 111 x {a} + 12  ==  {n % P} mod 37   {orbit_of(n)}")
    print(f"     111 = 3 x 37, so the start digit is invisible mod 37")
    print(f"     12 is a sovereign TARGET\n")
    print("  THE WHOLE FAMILY   n = 111a + 12d  ==  12d")
    print("   d  words                                  asc  orbit     "
          "desc  orbit")
    for d in range(0, 5):
        ws = [n for _, dd, n in APS if dd == d]
        print(f"   {d}  {str(ws):38s} {(12*d)%P:3d}  {orbit_of(12*d):8s} "
              f"{(25*d)%P:4d}  {orbit_of(25*d)}")
    print("\n  REVERSAL IS NEGATION:  12 + 25 = 37")
    print("     abc + cba = 101(a+c) + 20b, and a+c = 2b for an AP,")
    print("     so the sum is 222b = 6 x 37 x b == 0.\n")
    print("  246 IS THE d=2 ROAD  (digits 2,4,6, start 2)")
    print(f"     246 == 12 x 2 == 24 mod 37, orbit {orbit_of(246)}")
    print(f"     shares that residue with {[n for _,d,n in APS if d==2]}")
    print(f"     digit sum 3(a+d) = {3*(2+2)}, DR {dr(246)} -- every AP triple")
    print(f"     has DR in {{3,6,9}}")
    print("     T316's two conditions, DR=3 and ==24 mod 37, both follow.")
    print("     246 is still not distinguished -- 333 = 9 x 37 and the whole")
    print("     class seed == 246 (mod 333) behaves identically.\n")
    print("  ROTATION-CLASS SUMS = 333(a+d), 333 = 9 x 37")
    for a in range(1, 8):
        w = f"{a}{a+1}{a+2}"
        print(f"     {w} -> {sum(int(w[k:]+w[:k]) for k in (0,2,1))}"
              f" = 333 x {a+1}")
    print("\n  THE WRAP-AROUND ROADS (not APs, law does not apply)")
    print(f"     891 == {891%P} in {orbit_of(891)}   (target, birthday orbit)")
    print(f"     912 == {912%P} in {orbit_of(912)}   (seed residue, other route)")


if __name__ == "__main__":
    run()
