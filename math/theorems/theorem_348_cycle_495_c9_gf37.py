# CLASS: THEOREM
"""
Theorem 348: cycling the chain's three numbers gives 495, and its rotation
class is C9 complete -- the zero floor and the twin pair together
Author: Michael Warren Song (CyclicAmp)

Standing method: given three numbers, cycle them.  Exactly.

I had been handed 4, 9 and 5 as the addends of 4 + 9 = 13 + 5 = 18 and read
them only as sums.  Cycled, they are 495 -- the three-digit Kaprekar
constant -- and the cycle completes one orbit.

=== THE CYCLE ===

        4, 9, 5   ->   495, 549, 954
                  ->    14,  31,  29
                  ->   C9 = {14, 29, 31}, complete

    495 is the Kaprekar fixed point, confirmed by running the routine:
    321 -> 198 -> 792 -> 693 -> 594 -> 495 -> 495.

=== WHAT C9 CONTAINS ===

        14  =  floor(gamma_1),  the first Riemann zero at 14.134725...
        29, 31  a twin prime pair

    So the rotation class of the chain's three addends lands on the single
    orbit holding both the first zeta-zero floor and a twin prime pair --
    two of this project's three driving objects, in one 3-cycle.

=== WHAT IS FORCED AND WHAT IS NOT ===

    FORCED (T325, T326).  Any rotation class of a 3-digit word is exactly
    one 137-orbit, because rotation IS multiplication by 26; and it sums to
    zero mod 37, because 111 = 3 x 37.  Here 495+549+954 = 1998 = 111 x 18.
    That the three arrangements fill an orbit is not a finding -- it is the
    method working as designed.

    ALREADY HELD (T223).  495 == 14 and floor(gamma_1) = 14 lie in the same
    orbit.  That was recorded, with its own "Wait:" line, and resolved
    earlier in this session.

    NEW HERE.  The other two arrangements are not decoration: 549 == 31 and
    954 == 29 are the twin pair itself.  T223 had one element of C9; the
    cycle produces all three, and the two it adds are exactly the twins.

    GRADED.  That this particular triple is 4, 9, 5 -- and so cycles to the
    Kaprekar constant -- is contingent.  The orbit hit is 1 in 12, post hoc,
    n = 1.  Suggestive, not established, and recorded at that grade.

=== THE OTHER TRIPLES IN PLAY, CYCLED ===

    trinity      3,6,9  ->  369 936 693  ->  36 11 27  ->  NEG_H, orbit of -1
    gaps         2,4,6  ->  246 624 462  ->  24 32 18  ->  SEED
    baseline     1,2,3  ->  123 312 231  ->  12 16  9  ->  SA_ST_A
    chain        4,9,5  ->  495 549 954  ->  14 31 29  ->  C9

    Each is one orbit, each sums to a multiple of 111.  The trinity cycles
    onto the orbit of -1; the three commonest prime gaps cycle onto SEED.

=== FALSIFICATION ===
    A rotation class spanning two orbits; or 495 not a Kaprekar fixed point.
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
BY = {r: n for n, o in ORBITS.items() for r in o}


def cycle3(a, b, c):
    return [int(f"{a}{b}{c}"), int(f"{c}{a}{b}"), int(f"{b}{c}{a}")]


def kaprekar(n):
    d = f"{n:03d}"
    return int("".join(sorted(d, reverse=True))) - int("".join(sorted(d)))


def is_prime(m):
    return m > 1 and all(m % k for k in range(2, int(m ** .5) + 1))


def run():
    # --- the cycle ---
    w = cycle3(4, 9, 5)
    assert w == [495, 549, 954]
    assert [x % P for x in w] == [14, 31, 29]
    assert {x % P for x in w} == set(ORBITS['C9'])
    assert len({BY[x % P] for x in w}) == 1

    # --- 495 is the Kaprekar fixed point ---
    assert kaprekar(495) == 495
    x, seen = 321, []
    for _ in range(12):
        x = kaprekar(x)
        seen.append(x)
        if x == 495:
            break
    assert seen == [198, 792, 693, 594, 495]

    # --- what C9 holds ---
    assert 14 in ORBITS['C9']                       # floor(gamma_1)
    assert is_prime(29) and is_prime(31) and 31 - 29 == 2
    assert {29, 31} <= set(ORBITS['C9'])

    # --- forced: rotation is x26, class sums to 0 ---
    assert (26 * 495) % P == 549 % P
    assert (26 * 549) % P == 954 % P
    assert sum(w) == 1998 == 111 * 18 and sum(w) % P == 0
    assert 111 == 3 * P
    for n in range(100, 1000):                      # every 3-digit word
        d = f"{n:03d}"
        rot = int(d[-1] + d[:-1])
        assert rot % P == (26 * n) % P

    # --- the other triples ---
    table = {(3, 6, 9): 'NEG_H', (2, 4, 6): 'SEED',
             (1, 2, 3): 'SA_ST_A', (4, 9, 5): 'C9'}
    for t, name in table.items():
        ws = cycle3(*t)
        assert len({BY[x % P] for x in ws}) == 1
        assert BY[ws[0] % P] == name, (t, BY[ws[0] % P])
        assert sum(ws) % 111 == 0 and sum(ws) % P == 0
    assert set(ORBITS['NEG_H']) == {x % P for x in cycle3(3, 6, 9)}
    assert 36 == P - 1                              # trinity -> orbit of -1

    print("All assertions passed.\n")
    print("THEOREM 348.  Cycle the three numbers.\n")
    print("   chain 4 + 9 = 13 + 5 = 18; the addends are 4, 9, 5")
    print(f"   cycled -> {w} -> {[x%P for x in w]} -> C9 complete\n")
    print(f"   495 is the Kaprekar fixed point: 321 -> {' -> '.join(map(str,seen))}\n")
    print("   C9 = {14, 29, 31} holds")
    print("     14      = floor(gamma_1), first Riemann zero 14.134725...")
    print("     29, 31  = a twin prime pair\n")
    print("   FORCED (T325/T326): rotation is x26, so any rotation class is")
    print(f"   one orbit and sums to 0 -- here {sum(w)} = 111 x 18.")
    print("   ALREADY HELD (T223): 495 == 14 and floor(gamma_1) = 14 agree.")
    print("   NEW: the other two arrangements are the twin pair itself,")
    print("   549 == 31 and 954 == 29. T223 had one element; the cycle")
    print("   produces all three.")
    print("   GRADED: that the triple is 4,9,5 is contingent -- 1 in 12,")
    print("   post hoc, n = 1. Suggestive, not established.\n")
    print("   THE OTHER TRIPLES, CYCLED")
    for t, name in table.items():
        ws = cycle3(*t)
        print(f"     {t}  ->  {ws}  ->  {[x%P for x in ws]}  ->  {name}")
    print("     the trinity cycles onto the orbit of -1;")
    print("     the three commonest prime gaps cycle onto SEED.")


if __name__ == "__main__":
    run()
