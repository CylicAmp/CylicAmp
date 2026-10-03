# CLASS: THEOREM
"""
Theorem 371: the rotation cycle of 12321 carries a D_5 action, and at
length 5 rotation is NOT the 137-map
Author: Michael Warren Song (CyclicAmp)

PRIOR ART, checked first.  The number itself is already in the corpus:
T328 and T330 both record 12321 = 111^2 = (3 x 37)^2 = 9 x 37^2 with
residue 0 and DR 9, and palindrome_gf37 (declares THEOREM 56) together
with connection_map give the ABCBA rule -- a five-digit palindrome is
SEAM exactly when C = A + B, which 1+2 = 3 satisfies.  None of that is new
here.  What is new is the ORBIT: the strings 11232, 21123, 32112 and 23211
appear in no theorem file, and neither does the group action below.

=== THE TWO COLUMNS ===

    left (rotate)   right (reverse)   left mod 37   right mod 37
      12321            12321                0            0
      11232            23211               21           12
      21123            32112               33           33
      32112            21123               33           33
      23211            11232               12           21
      12321            12321                0            0

    THE RIGHT COLUMN IS THE LEFT COLUMN READ BOTTOM-TO-TOP.  Verified on
    all six rows, residues included.

=== WHY: D_5, ANCHORED AT THE PALINDROME ===

    Rotation r (last digit to the front) has order 5 on this string; the
    string has no shorter rotational period.  Reversal s has order 2.
    Together they satisfy

        s r^k = r^-k s,

    the dihedral relation, so <r, s> = D_5.  Because 12321 is its own
    reverse, s fixes the base point, and then

        reverse(r^k (12321)) = r^-k (12321)

    -- checked for k = 0..4.  That single identity is the whole table:
    reversing the STRING is the same as walking the cycle BACKWARDS, so
    the two columns are one cycle traversed in opposite directions.

    As an involution on the 5-cycle, s has 1 fixed point (the palindrome)
    and 2 two-cycles: 11232 <-> 23211 and 21123 <-> 32112.  Same shape as
    T364's involution on the 37-point fibre, which has 1 fixed point and 18
    two-cycles; here the count is 1 + 2 x 2 = 5.

=== AT LENGTH 5 ROTATION IS NOT MULTIPLICATION BY 26 ===

    The three-digit result -- rotation of a 3-digit word equals
    multiplication by 26 mod 37, so a rotation class IS a 137-orbit --
    needs 3 | length, because ord_37(10) = 3.  Five is not a multiple of
    three, 10^5 == 26 (not 1), and the rotation law acquires a correction
    term:

        R(N) == 26 N - 16 e   (mod 37),    e = the last digit.

    Affine, not multiplicative.  Verified on every step of the cycle.  So
    the residues wander -- SEAM, SA_ST_B, D7, D7, SA_ST_A -- instead of
    staying inside one orbit the way 346 -> 634 -> 463 stays inside
    CAS_EXT.  This is the clean counterexample to reading rotation as the
    137-map in general: it is that only at lengths divisible by 3.

=== WHAT IS FORCED ===

    Every member has DR 9, because rotation preserves the digit sum and
    1+2+3+2+1 = 9.  And the five members sum to

        9 x 11111 = 99999 = 10^5 - 1,

    since the sum of all cyclic rotations is always (digit sum) x (repunit).
    Both are automatic and carry no information about this particular word.
    (Contrast T326/T330: a 3-digit rotation class sums to a multiple of
    111 = 3 x 37; at length 5 the repunit is 11111 = 41 x 271, which has
    no 37 in it.)

=== GRADED DOWN ===

    The first two-cycle's residues sum to 21 + 12 = 33, which is the second
    two-cycle's common residue.  Baselined rather than reported: a random
    5-digit N has N + reverse(N) == 33 (mod 37) with probability 0.0317
    against 1/37 = 0.0270.  Noise.

=== FALSIFICATION ===
    A rotation of 12321 outside the listed five; the right column failing
    to be the left reversed; R(N) != 26N - 16e for some member; or a member
    with DR other than 9.
"""
P = 37
ORBITS = {
    'IC': (1, 10, 26), 'DARK_A': (2, 15, 20), 'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23), 'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36), 'C9': (14, 29, 31),
    'NQR17': (17, 22, 35), 'SEED': (18, 24, 32), 'SA_ST_B': (21, 25, 28),
}
orbit_of = lambda n: ('SEAM' if n % P == 0 else
                      next(k for k, v in ORBITS.items() if n % P in v))
dr = lambda n: 1 + (n - 1) % 9
rot = lambda s: s[-1] + s[:-1]


def rotk(s, k):
    for _ in range(k % 5):
        s = rot(s)
    return s


def run():
    base = "12321"
    cyc = [rotk(base, k) for k in range(5)]
    assert cyc == ["12321", "11232", "21123", "32112", "23211"]
    assert len(set(cyc)) == 5 and rotk(base, 5) == base      # period exactly 5

    # the number itself (prior art: T328, T330)
    assert int(base) == 111 ** 2 == 9 * 37 ** 2 == 12321
    assert int(base) % (37 ** 2) == 0                         # 37^2, not just 37

    # the two columns
    left = cyc + [base]
    right = [s[::-1] for s in left]
    assert right == left[::-1]                                # THE table
    assert [int(a) % P for a in right] == [int(a) % P for a in left][::-1]

    # dihedral: s r^k = r^-k s, and s fixes the base point
    assert base[::-1] == base
    for k in range(5):
        assert rotk(base, k)[::-1] == rotk(base, -k % 5)
    for s in cyc:
        assert rot(s)[::-1] == rotk(s[::-1], -1 % 5)

    # the involution on the cycle: 1 fixed point, 2 two-cycles
    fixed = [s for s in cyc if s[::-1] == s]
    assert fixed == [base]
    pairs = {frozenset((s, s[::-1])) for s in cyc if s[::-1] != s}
    assert len(pairs) == 2 and 1 + 2 * 2 == 5

    # rotation is NOT x26 at length 5
    assert pow(10, 3, P) == 1 and pow(10, 5, P) == 26 and 5 % 3 != 0
    for s in cyc:
        n, e = int(s), int(s[-1])
        assert int(rot(s)) % P == (26 * n - 16 * e) % P
    assert len({orbit_of(int(s)) for s in cyc}) == 4          # wanders, 4 orbits

    # forced
    assert all(dr(int(s)) == 9 for s in cyc)
    assert sum(int(s) for s in cyc) == 9 * 11111 == 99999 == 10 ** 5 - 1
    assert 11111 == 41 * 271 and 11111 % 37 != 0              # no 37 at length 5

    print("T371  the 12321 rotation cycle and its reversal\n")
    print("   left      right     mod 37")
    for a, b in zip(left, right):
        print("   %-8s  %-8s  %3d  %3d" % (a, b, int(a) % P, int(b) % P))
    print("\n  right column = left column read bottom-to-top, residues too.")
    print("  reverse(r^k(12321)) = r^-k(12321): reversing the string is")
    print("  walking the cycle backwards. <r,s> = D_5, anchored at the")
    print("  palindrome. Involution on 5 points: 1 fixed + 2 two-cycles.\n")
    print("  AT LENGTH 5 ROTATION IS NOT THE 137-MAP.")
    print("   ord_37(10) = 3 and 3 does not divide 5, so 10^5 = 26 not 1 and")
    print("   R(N) = 26N - 16e (mod 37), e the last digit -- affine, not")
    print("   multiplicative. Residues wander over %d orbits: %s"
          % (len({orbit_of(int(s)) for s in cyc}),
             [orbit_of(int(s)) for s in cyc]))
    print("   (at length 3, rotation IS x26 and a rotation class is an orbit.)\n")
    print("  FORCED: every member has DR 9 (rotation preserves digit sum),")
    print("  and the five sum to 9 x 11111 = 99999 = 10^5 - 1. The length-5")
    print("  repunit is 41 x 271 -- no 37 in it, unlike 111 = 3 x 37.\n")
    print("  GRADED DOWN: 21 + 12 = 33 matching the other pair's residue is")
    print("  noise -- baseline 0.0317 against 1/37 = 0.0270.")
    print("\n  ALL ASSERTIONS PASS")


if __name__ == '__main__':
    run()
