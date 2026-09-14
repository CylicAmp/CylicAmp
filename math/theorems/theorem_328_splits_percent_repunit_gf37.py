# CLASS: THEOREM
"""
Theorem 328: reading the counting stack sideways -- percentage, splits,
prefix = residue, and the chevron as 37^2
Author: Michael Warren Song (CyclicAmp)

Four readings of the T327 stack 123 / 246 / 369, each checkable.

=== 1. THE PERCENTAGE READ:  123 = 100% / 50% / 25% = 175% ===

    1 + 1/2 + 1/4 = 7/4 = 175%.  The numerator is 7, and 175 = 7 x 25.

        175 x 1 = 175 == 27   NEG_H
        175 x 2 = 350 == 17   NQR17
        175 x 3 = 525 ==  7   D7

    Halving, not counting: the denominators are 1,2,4 -- the doubling half
    of the Z/9Z partition, not the trinity half the digits 1,2,3 sit in.
    The percentage read and the counting read use DIFFERENT halves of the
    partition on the same row.

=== 2. THE SPLIT  d | 23d  ===

        123 -> 1|23      246 -> 2|46      369 -> 3|69

    Forced, and the reason is one line: 123d = 100d + 23d, so the leading
    digit is d and the trailing pair is 23d.  23 is the TESLA element.

    Adding the parts gives d + 23d = 24d:

        1+23 = 24      2+46 = 48      3+69 = 72

    and 24 is the SEED residue -- the same 24 that is 246 mod 37.

=== 3. PREFIX = RESIDUE ===

    Split the other way, prefix | unit:

        123 -> 12|3      residue 12      12 = 12x1
        246 -> 24|6      residue 24      24 = 12x2
        369 -> 36|9      residue 36      36 = 12x3

    THE FIRST TWO DIGITS OF EACH ROW ARE ITS RESIDUE MOD 37.  Readable off
    the front of the number, no arithmetic.

    This is not deep -- it holds because floor(123d/10) = 12d for d <= 3 and
    12d < 37 there, so the residue has not yet wrapped.  It breaks at d=4
    exactly where everything else in this thread breaks: 492 -> 49|2, prefix
    49, residue 11.  Recorded as a reading aid with its own expiry, not as a
    property of 37.

=== 4. THE HINGE FIRES EXACTLY ONCE ===

        1 + 23 = 24,  and 246 begins "24".

    The sum of row 1's split is the visible prefix of row 2.  It does not
    continue: 2 + 46 = 48, and 369 begins "36", not "48".

    Forced, and the reason it fires once is one equation.  Split sums are
    24d and prefixes are 12(d+1), so the hinge needs

        24d = 12(d+1)   <=>   12d = 12   <=>   d = 1.

    A chain that fires once is a coincidence with a proof, not a pattern.
    Stated here so it is not mistaken for the start of a sequence.

=== 5. THE CHEVRON ROW IS 37^2 ===

    The palindrome row 1 2 3 2 1 is the repunit square:

        12321 = 111^2 = (3 x 37)^2 = 9 x 37^2

    and it is the ONLY repunit square divisible by 37 in the small range --
    R1^2=1, R2^2=121, R4^2=1234321 have residues 1, 10, 1, while R3^2 is 0
    even mod 37^2.  R3 = 111 = 3 x 37 is the same 111 that makes the start
    digit invisible in T326.  The chevron shape of T325 and the modulus of
    T326 are the same number squared.

=== NOT INCLUDED ===
    The biological-pathway overlay supplied alongside this material is not
    in this file.  Its electron-transport topology and two of its three
    dielectric constants are wrong; see the session note.  Nothing here
    depends on it.

=== FALSIFICATION ===
    Any assert below failing.
"""

P = 37
ORBITS = {
    'IC': {1, 10, 26},      'DARK_A': {2, 15, 20},  'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23},    'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36},  'C9': {14, 29, 31},
    'NQR17': {17, 22, 35},  'SEED': {18, 24, 32},   'SA_ST_B': {21, 25, 28},
}
TRINITY, DOUBLING = {3, 6, 9}, {1, 2, 4, 5, 7, 8}


def orbit_of(n):
    r = n % P
    return 'SEAM' if r == 0 else next(k for k, v in ORBITS.items() if r in v)


def run():
    from fractions import Fraction

    # --- 1. the percentage read ---
    assert Fraction(1) + Fraction(1, 2) + Fraction(1, 4) == Fraction(7, 4)
    assert 100 + 50 + 25 == 175 == 7 * 25
    assert [(175 * k) % P for k in (1, 2, 3)] == [27, 17, 7]
    assert [orbit_of(175 * k) for k in (1, 2, 3)] == ['NEG_H', 'NQR17', 'D7']
    # halving uses the doubling half; the digits sit in the trinity half
    assert {1, 2, 4} <= DOUBLING and {3, 6, 9} == TRINITY
    assert {1, 2, 4} & TRINITY == set()

    # --- 2. the split d | 23d ---
    for d in (1, 2, 3):
        n = 123 * d
        assert n == 100 * d + 23 * d
        assert n // 100 == d and n % 100 == 23 * d
        assert d + 23 * d == 24 * d
    assert orbit_of(23) == 'TESLA'
    assert orbit_of(24) == 'SEED' and 246 % P == 24

    # --- 3. prefix = residue, and its expiry ---
    for d in (1, 2, 3):
        n = 123 * d
        assert n // 10 == 12 * d == n % P
    assert 492 // 10 == 49 and 492 % P == 11 and 49 != 11   # breaks at d=4

    # --- 4. the hinge fires once ---
    assert 1 + 23 == 24 == 246 // 10
    assert 2 + 46 == 48 != 369 // 10 == 36
    assert [d for d in range(1, 10) if 24 * d == 12 * (d + 1)] == [1]

    # --- 5. the chevron row is 37^2 ---
    assert 111 ** 2 == 12321 == 9 * P ** 2 == (3 * P) ** 2
    assert 12321 % (P * P) == 0
    assert [int("1" * k) ** 2 % P for k in (1, 2, 3, 4)] == [1, 10, 0, 1]
    assert int("1" * 3) == 111 == 3 * P

    print("All assertions passed.\n")
    print("THEOREM 328.  Four sideways readings of 123 / 246 / 369.\n")
    print("  1. PERCENTAGE   1 + 1/2 + 1/4 = 7/4 = 175%,  175 = 7 x 25")
    for k in (1, 2, 3):
        print(f"       175 x {k} = {175*k:3d} == {175*k%P:2d}  {orbit_of(175*k)}")
    print("     denominators 1,2,4 are the DOUBLING half; the digits 1,2,3")
    print("     are not -- two halves of the partition on one row.\n")
    print("  2. SPLIT  123d = 100d + 23d,  so the row is  d | 23d")
    for d in (1, 2, 3):
        print(f"       {123*d} -> {d}|{23*d}   sum {24*d} = 24 x {d}")
    print(f"     23 in TESLA, 24 in SEED (= 246 mod 37)\n")
    print("  3. PREFIX = RESIDUE")
    for d in (1, 2, 3):
        print(f"       {123*d} -> {123*d//10}|{123*d%10}"
              f"   residue {123*d%P}   same number")
    print("     expires at d=4: 492 -> 49|2, residue 11.  A reading aid.\n")
    print("  4. THE HINGE  1 + 23 = 24, and 246 begins '24'")
    print("     2 + 46 = 48, but 369 begins '36'.  Fires once.")
    print("     24d = 12(d+1) has the single solution d = 1.\n")
    print("  5. THE CHEVRON ROW  1 2 3 2 1  =  12321  =  111^2  =  9 x 37^2")
    for k in (1, 2, 3, 4):
        R = int("1" * k)
        print(f"       R{k}^2 = {R*R:8d}  == {R*R%P:2d} mod 37")
    print("     only R3 vanishes -- R3 = 111 = 3 x 37, the same 111 that")
    print("     makes the start digit invisible in T326.")


if __name__ == "__main__":
    run()
