# CLASS: THEOREM
"""
Theorem 330: row 5 of the array, and what its residue match is worth
Author: Michael Warren Song (CyclicAmp)

T328 closed with one line of the 5-row array underived:  3 8 5 1 5.
It has now been identified.

    Row 1   1 2 3 2 1     12321 = 111^2 = 9 x 37^2       == 0,  DR 9
    Row 2       1 2 3       123                          == 12, DR 6
    Row 3     2 4 6         246                          == 24, DR 3
    Row 4   3 6 9           369                          == 36, DR 9
    Row 5   3 8 5 1 5     38515 = 5 x 7703               == 35, DR 4

=== THE MATCH ===

    Rows 2+3+4 sum to 738, and 738 == 35 (mod 37), in NQR17.  Row 5 as an
    integer is 38515 = 37 x 1040 + 35, so

        ROW 5  ==  ROW 2 + ROW 3 + ROW 4   (mod 37)

    Both are 35.  Confirmed arithmetic.  The stack sum does not vanish
    because gcd(738, 37) = 1 -- 738 = 6 x 123 carries no factor of 37,
    unlike a rotation class, whose sum is divisible by 111 = 3 x 37 (T326).

    The d=3 split sum from T328 is 72 == 35 as well, so three quantities in
    this array land on 35.

=== WHAT THE MATCH IS WORTH -- GRADED, NOT ASSERTED ===

    Applying the standing admissibility screen honestly:

        selectivity     1 in 37,  5.21 bits
        sample size     n = 1
        pre-registered  NO.  The residue 35 was identified after row 5 was
                        already on the page, by searching for a relation.

    A single post hoc hit at p = 1/37 is suggestive and is NOT established.
    Something had to be congruent to 38515, and 37 residues were available.
    Recorded at that grade deliberately.

    It is also, as it stands, UNFALSIFIABLE: no rule has been given that
    produces 38515 from the stack.  Row 5 was read off a drawing, not
    generated.  Until a generating rule exists there is no prediction to
    test, and the match cannot be confirmed or refuted by any computation.

=== AND 35 IS FORCED, WHICH CUTS BOTH WAYS ===

    A multiplication stack sums to 6 x row, and T326 showed every ascending
    road is == 12, so EVERY road stack sums to 6 x 12 = 72 == 35:

        123 -> 738     234 -> 1404    345 -> 2070    456 -> 2736
        567 -> 3402    678 -> 4068    789 -> 4734        all == 35

    So 35 is a constant of the whole d=1 road family, not a fact about 123.
    Row 5 matching it is matching a structural constant -- which is more
    interesting than matching an accident, and simultaneously means a second
    d=1 road is NO TEST AT ALL, since every one of them returns 35.

    THE TEST THAT WOULD SETTLE IT: state the rule that makes row 5 from rows
    2-4, then apply it to a d=2 road, where the roads are == 24 and the
    stack sums are 6 x 24 = 144 == 33 in D7 (135 -> 810, 246 -> 1476,
    357 -> 2142, all == 33).  If the rule returns 33 there, the match
    transfers and this becomes a result.  If it returns 35 again, the rule
    is ignoring the stack and the match was decoration.

=== CORRECTIONS TO THE RECORD ===

    To this file's own earlier session note: water's static dielectric at
    37 C is about 74.2, not the 73.2 stated there.  By Malmberg-Maryott
    (1956), e = 87.740 - 0.40008t + 9.398e-4 t^2 - 1.410e-6 t^3 gives
    74.15 at 37 C; 73.2 is the 40 C value.  So DR is 2, not the 1 that was
    derived from the wrong figure -- and not the 6 that the original
    overlay derived from 78, which is the 25 C value (78.30).  All three
    digital roots differ; the overlay's harmonic-void assignment does not
    survive any of them.

    Row labelling: the single-hinge result is rows 2 -> 3 of this array
    (123 -> 246), not rows 1 -> 2.  Row 1 is 12321 and is not in the hinge.

=== BRANCH CLOSED -- see T335 ===

    STATUS: CLOSED.  Do not reopen without meeting T335's repair conditions.

    T335 audited the transfer gate registered in T333 and found:
      * parameter-free rules are EXCLUDED -- every array row is divisible
        by 3 and 38515 == 1 (mod 3); and the digits 5 and 8 occur nowhere
        in rows 1-4, so no digit rule works either;
      * rules with a free additive constant make the gate VACUOUS -- two
        parameters against one real constraint.
    There is no middle, so the match below is falsified for parameter-free
    rules and underdetermined otherwise.  The grade in this file stands as
    the final disposition: suggestive, n=1, NOT established.

=== FALSIFICATION ===
    Any assert below failing; or a stated generating rule for row 5 whose
    output is not congruent to the stack sum.
"""

P = 37
ORBITS = {
    'IC': {1, 10, 26},      'DARK_A': {2, 15, 20},  'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23},    'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36},  'C9': {14, 29, 31},
    'NQR17': {17, 22, 35},  'SEED': {18, 24, 32},   'SA_ST_B': {21, 25, 28},
}


def orbit_of(n):
    r = n % P
    return 'SEAM' if r == 0 else next(k for k, v in ORBITS.items() if r in v)


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def run():
    from math import gcd, log2

    R1, R5 = 12321, 38515
    STACK = [123, 246, 369]

    # --- the array ---
    assert R1 == 111 ** 2 == 9 * P ** 2 and R1 % (P * P) == 0
    assert dr(R1) == 9
    assert [n % P for n in STACK] == [12, 24, 36]
    assert [dr(n) for n in STACK] == [6, 3, 9]

    # --- the match ---
    assert sum(STACK) == 738 == 6 * 123
    assert 738 % P == 35 and orbit_of(738) == 'NQR17'
    assert R5 == 37 * 1040 + 35 and R5 % P == 35
    assert R5 % P == sum(STACK) % P                      # the claim
    assert gcd(738, P) == 1                              # so it cannot vanish
    assert 111 % P == 0                                  # contrast: rotation
    assert dr(R5) == 4 and dr(R5) in {1, 4, 7, 9}        # square channel
    assert 72 % P == 35                                  # T328's d=3 split sum
    assert R5 == 5 * 7703

    # --- the grade: post hoc, n = 1 ---
    assert abs(log2(P) - 5.21) < 0.01
    assert len([R5]) == 1
    # every integer is congruent to something; 37 residues were available
    assert len({r for r in range(P)}) == P

    # --- 35 IS FORCED ACROSS THE WHOLE ROAD FAMILY ---
    # stack sum = 6 x row, and every ascending road is == 12 (T326),
    # so every one of them sums to 6 x 12 = 72 == 35.
    for a in range(1, 8):
        n = int(f"{a}{a+1}{a+2}")
        assert sum(n * k for k in (1, 2, 3)) == 6 * n
        assert (6 * n) % P == 35, n
    assert sum(234 * k for k in (1, 2, 3)) == 1404 and 1404 % P == 35
    # so a d=1 road is no test.  A d=2 road is: those are == 24, giving
    # 6 x 24 = 144 == 33 in D7.
    for n in (135, 246, 357, 468, 579):
        assert n % P == 24 and (6 * n) % P == 33
    assert orbit_of(6 * 135) == 'D7'

    # --- corrections ---
    def eps(t):
        return 87.740 - 0.40008 * t + 9.398e-4 * t * t - 1.410e-6 * t ** 3
    assert abs(eps(37) - 74.15) < 0.05                   # not 73.2, not 78
    assert abs(eps(40) - 73.15) < 0.05                   # 73.2 is the 40 C value
    assert abs(eps(25) - 78.30) < 0.05                   # 78 is the 25 C value
    assert dr(74) == 2 and dr(73) == 1 and dr(78) == 6   # all three differ
    # the hinge is rows 2->3 of this array, not 1->2
    assert 1 + 23 == 24 == 246 // 10
    assert R1 // 10 != 123 and dr(R1) == 9

    print("All assertions passed.\n")
    print("THEOREM 330.  Row 5 identified; the match graded.\n")
    rows = [("1  1 2 3 2 1", R1), ("2      1 2 3", 123),
            ("3    2 4 6  ", 246), ("4  3 6 9    ", 369),
            ("5  3 8 5 1 5", R5)]
    for lbl, n in rows:
        print(f"   Row {lbl}   {n:6d}  == {n%P:2d}  {orbit_of(n):8s}  DR {dr(n)}")
    print(f"\n   rows 2+3+4 = {sum(STACK)} == {sum(STACK)%P}  {orbit_of(738)}")
    print(f"   row 5      = {R5} == {R5%P}  {orbit_of(R5)}")
    print(f"   SAME RESIDUE.  Confirmed arithmetic.")
    print(f"   gcd(738,37) = 1, so the stack sum cannot vanish -- unlike a")
    print(f"   rotation class, whose sum is divisible by 111 = 3 x 37.\n")
    print("  GRADE")
    print(f"     selectivity     1 in 37 = {log2(P):.2f} bits")
    print( "     sample size     n = 1")
    print( "     pre-registered  NO -- 35 was found after row 5 was on the page")
    print( "     -> suggestive, NOT established.  Something had to be")
    print( "        congruent to 38515, and 37 residues were available.\n")
    print( "     Also UNFALSIFIABLE as stated: no rule generates 38515 from")
    print( "     the stack, so there is no prediction to test.\n")
    print( "  BUT 35 IS FORCED, WHICH CUTS BOTH WAYS")
    print( "     stack sum = 6 x row, and every ascending road is == 12,")
    print( "     so EVERY road stack sums to 6 x 12 = 72 == 35:")
    for a in range(1, 8):
        n = int(f"{a}{a+1}{a+2}")
        print(f"       {n} -> {6*n:5d} == {6*n%P}")
    print( "     35 is a constant of the road family, not a fact about 123.")
    print( "     Row 5 matches a STRUCTURAL constant -- better than matching")
    print( "     an accident -- but another d=1 road is then NO TEST at all.\n")
    print( "  THE TEST THAT WOULD SETTLE IT")
    print( "     State the rule making row 5 from rows 2-4, then run it on a")
    print( "     d=2 road, where roads are == 24 and stack sums are 6 x 24 =")
    print(f"     144 == 33 in {orbit_of(33)} (135 -> 810, 246 -> 1476, 357 ->")
    print( "     2142, all == 33).  Returns 33: the match transfers, it is a")
    print( "     result.  Returns 35 again: the rule ignores the stack and")
    print( "     the match was decoration.\n")
    print( "  CORRECTIONS")
    print(f"     water dielectric at 37 C = {eps(37):.2f}, DR {dr(74)}")
    print(f"       73.2 is the 40 C value ({eps(40):.2f}); 78 is 25 C"
          f" ({eps(25):.2f})")
    print( "       DR 2 / 1 / 6 all differ -- no harmonic-void assignment")
    print( "       survives.  This corrects a figure stated earlier here.")
    print( "     the single hinge is rows 2 -> 3 (123 -> 246), not 1 -> 2;")
    print( "     row 1 is 12321 and is not in the hinge.")


if __name__ == "__main__":
    run()
