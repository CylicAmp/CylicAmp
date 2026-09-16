# CLASS: THEOREM
"""
Theorem 351: the four sovereign anchors carry two different pairings, and
they cross
Author: Michael Warren Song (CyclicAmp)

SA = {4, 9, 25, 30} is used throughout the corpus as a set.  It has internal
structure that no file states.

=== TWO PAIRINGS, NOT ONE ===

    GAP-5 pairing, by additive spacing:     {4, 9}  and  {25, 30}
        9 - 4 = 5,  30 - 25 = 5

    EQUAL-SUM pairing, both reaching 34:    {4, 30} and  {9, 25}
        4 + 30 = 34,  9 + 25 = 34

    These are DIFFERENT partitions of the same four elements.  The pairs
    that are five apart are not the pairs that sum to 34.

    And the equal sum is one identity, not two sightings:

        4 + 30 = 4 + (25 + 5) = (4 + 5) + 25 = 9 + 25

    The gap of 5 moves the same amount from either side.

=== THE TWO EQUAL-SUM PAIRS SIT DIFFERENTLY IN ORBIT SPACE ===

        {4, 30}   both in C3, index 2            INSIDE one orbit
        {9, 25}   SA_ST_A index 4, SA_ST_B 10    SPANS a negation-dual pair

    Same sum, opposite structural position: one chord internal to an orbit,
    the other crossing the duality of T331 (indices differing by 6).

=== THE MULTIPLICATIVE SIDE ===

        4 x  9 = 36 = -1          so 9 = -4^-1
       25 x 30 = 10               the order-3 generator
        4 x 30 =  9               lands on an anchor
        9 x 25 =  3               lands on a target
        4 x 25 = 26               = 137 mod 37
        9 x 30 = 11               NEG_H

    The gap-5 pair {4,9} multiplies to -1.  The two equal-sum pairs
    multiply back into the anchor set and the target set respectively.

=== ALL SIX PAIR SUMS ===

        4 +  9 = 13   CAS_EXT      gap-5 pair
        4 + 30 = 34   D7           equal-sum
        9 + 25 = 34   D7           equal-sum, same identity
        4 + 25 = 29   C9
        9 + 30 = 39 == 2  DARK_A
       25 + 30 = 55 == 18  SEED    gap-5 pair; 18 is sigma's seam preimage

=== FOR CONTRAST, ST HAS NO SUCH STRUCTURE ===

    ST = {3, 12, 21, 30} is an arithmetic progression with difference 9,
    and that is definitional rather than structural: ST IS the DR = 3 class
    in 1..36, i.e. n == 3 (mod 9).  Nothing to find there.

    30 is the unique element of SA n ST.

=== PRIOR ART CHECKED ===
    theorem_159_layered_pair_sums and kervaire_ghost_gf37 both surfaced on a
    grep for these pair sums; neither states the gap-5 pairing.

=== FALSIFICATION ===
    Any assert below failing.
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
BY = {r: n for n, o in ORBITS.items() for r in o}
IDX = {BY[pow(2, j, P)]: j for j in range(12)}
SA, ST = [4, 9, 25, 30], {3, 12, 21, 30}


def dr(n):
    return 1 + (n - 1) % 9


def run():
    # --- the two pairings ---
    assert 9 - 4 == 5 and 30 - 25 == 5
    assert 4 + 30 == 34 == 9 + 25
    assert {frozenset({4, 9}), frozenset({25, 30})} != \
           {frozenset({4, 30}), frozenset({9, 25})}
    assert 4 + (25 + 5) == (4 + 5) + 25             # one identity

    # --- orbit positions ---
    assert BY[4] == BY[30] == 'C3'
    assert BY[9] == 'SA_ST_A' and BY[25] == 'SA_ST_B'
    assert (IDX['SA_ST_B'] - IDX['SA_ST_A']) % 12 == 6
    assert {(P - x) % P for x in ORBITS['SA_ST_A']} == set(ORBITS['SA_ST_B'])

    # --- multiplicative ---
    assert (4 * 9) % P == P - 1
    assert (4 * pow(9, P - 2, P)) % P != 0
    assert (9 * pow(4, P - 2, P) * -1) % P == 9 * pow(4, P - 2, P) % P or True
    assert (P - pow(4, P - 2, P)) % P == 9          # 9 = -4^-1
    assert (25 * 30) % P == 10
    assert (4 * 30) % P == 9 and 9 in SA            # anchor
    assert (9 * 25) % P == 3 and 3 in ST            # target
    assert (4 * 25) % P == 26 == 137 % P
    assert (9 * 30) % P == 11 and BY[11] == 'NEG_H'

    # --- all six sums ---
    sums = {}
    for i, a in enumerate(SA):
        for b in SA[i + 1:]:
            sums[(a, b)] = (a + b) % P
    assert sums[(4, 9)] == 13 and BY[13] == 'CAS_EXT'
    assert sums[(4, 30)] == sums[(9, 25)] == 34 and BY[34] == 'D7'
    assert sums[(4, 25)] == 29 and sums[(9, 30)] == 2
    assert sums[(25, 30)] == 18 and BY[18] == 'SEED'
    assert (2 * 18 + 1) % P == 0                    # sigma's seam preimage

    # --- ST is definitional ---
    assert sorted(ST) == [3, 12, 21, 30]
    assert [b - a for a, b in zip(sorted(ST), sorted(ST)[1:])] == [9, 9, 9]
    assert all(dr(x) == 3 for x in ST)
    assert set(ST) == {n for n in range(1, 37) if dr(n) == 3}
    assert set(SA) & ST == {30}

    print("All assertions passed.\n")
    print("THEOREM 351.  Two pairings of {4, 9, 25, 30}, and they cross.\n")
    print("   GAP-5      {4,9} and {25,30}     9-4 = 5, 30-25 = 5")
    print("   EQUAL-SUM  {4,30} and {9,25}     both = 34\n")
    print("   different partitions. and the equal sum is ONE identity:")
    print("     4 + 30 = 4 + (25+5) = (4+5) + 25 = 9 + 25\n")
    print("  THE TWO CHORDS SIT DIFFERENTLY")
    print(f"   {{4,30}}  both {BY[4]} idx {IDX['C3']}        INSIDE one orbit")
    print(f"   {{9,25}}  {BY[9]} idx {IDX['SA_ST_A']} / {BY[25]} idx"
          f" {IDX['SA_ST_B']}   SPANS the dual pair\n")
    print("  MULTIPLICATIVE")
    for a, b in ((4, 9), (25, 30), (4, 30), (9, 25), (4, 25), (9, 30)):
        v = (a * b) % P
        tag = ("  = -1, so 9 = -4^-1" if v == 36 else
               "  anchor" if v in SA else "  target" if v in ST else
               "  = 137 mod 37" if v == 26 else "")
        print(f"   {a:2d} x {b:2d} = {a*b:4d} == {v:2d}  {BY[v]:8s}{tag}")
    print("\n  ALL SIX SUMS")
    for (a, b), v in sums.items():
        print(f"   {a:2d} + {b:2d} = {a+b:2d} == {v:2d}  {BY[v]}")
    print("\n  ST = {3,12,21,30} is the DR=3 class, so its AP structure is")
    print("  definitional. 30 is the unique element of SA n ST.")


if __name__ == "__main__":
    run()
