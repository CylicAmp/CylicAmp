# CLASS: THEOREM
"""
Theorem 329: the digital root is NOT invariant on 137-orbits -- refutation,
and the wrap-count law that replaces it
Author: Michael Warren Song (CyclicAmp)

A synthesis offered to this project claimed:

    "Taking the digital root of each orbit element demonstrates an
     invariant: all three elements of any given orbit modulo 37 collapse
     to the exact same digital root modulo 9."

This is false in all twelve orbits, and the table printed alongside the
claim already refutes it -- it lists IC = {1,10,26} with digital roots
{1,1,8} and then calls that an invariant.

    IC       1 10 26    DR 1 1 8          DARK_A   2 15 20   DR 2 6 2
    C3       3  4 30    DR 3 4 3          CAS_EXT  5 13 19   DR 5 4 1
    TESLA    6  8 23    DR 6 8 5          D7       7 33 34   DR 7 6 7
    SA_ST_A  9 12 16    DR 9 3 7          NEG_H   11 27 36   DR 2 9 9
    C9      14 29 31    DR 5 2 4          NQR17   17 22 35   DR 8 4 8
    SEED    18 24 32    DR 9 6 5          SA_ST_B 21 25 28   DR 3 7 1

    Constant in 0 of 12.

=== WHY IT CANNOT BE TRUE ===

    gcd(9, 37) = 1, so by CRT the residue mod 9 and the residue mod 37 are
    independent coordinates.  Nothing computed from one can be constant on
    the orbits of a map defined by the other, short of a constant function.
    No search is needed; the claim is excluded before it is tested.

=== PRIORITY: THE LAW BELOW IS T138 PART I, SPECIALISED ===

    Recorded after the fact.  T138 ("DR Subtraction Law") already proved,
    for ALL 36^2 pairs and not just for the multipliers 10 and 26,

        DR(a x_37 b) = DR(a.b) - DR(floor(a.b / 37))   in Z/9Z

    from the same observation that 37 == 1 (mod 9).  Setting a = 10 gives
    exactly the law stated below.  The general statement is T138's, and
    this cross-reference was added afterwards so the two read together.

    What is NOT in T138 and does stand as this file's own result: the
    refutation.  T138 gives the correction term but never claims DR is
    constant on orbits, and the measurement that it is constant in 0 of 12
    orbits, with the CRT argument excluding it a priori, is new here.

=== THE CORRECT LAW: DIGITAL ROOT SHIFTS BY THE WRAP COUNT ===

    The orbit of x is {x, 26x, 10x} mod 37, and 37 == 1 (mod 9), so every
    subtraction of 37 during reduction moves the value down by exactly 1
    mod 9.  With k the number of times 37 is subtracted:

        10x mod 37  ==  x  - k   (mod 9),   k = floor(10x/37)
        26x mod 37  ==  8x - k   (mod 9),   k = floor(26x/37)

    Verified for every x in 1..36.  The digital root is not invariant; it is
    SHIFTED BY THE WRAP COUNT, which is different for each element.

    The 8 is the real content.  26 == 8 == -1 (mod 9), so the 137-map acts
    as NEGATION mod 9 while acting as the orbit generator mod 37.  Absent
    wrapping the three digital roots would read x, -x, x -- alternating, not
    constant.  IC is the case with no wrapping at all (10 and 26 are both
    below 37), and it reads 1, 8, 1 = x, -x, x exactly.

    So the true relation between the two moduli is an ANTI-invariance
    corrected by a carry term, which is the opposite shape of the claim.

=== WHAT IN THE SYNTHESIS DOES HOLD ===

    Checked and confirmed, so the refutation is not read wider than it goes:

        10^-1 == 26 and 26 == 10^2 (mod 37); 26^2 == 10, so the orbit
          really is {x, 26x, 10x}                              TRUE
        ord_37(10) = 3, and 999 = 27 x 37                      TRUE
        the orbit of -1 is NEG_H = {11,27,36}                  TRUE
        100 == -11 and 23 == -14 (mod 37)                      TRUE
        {24,48,72} == {24,11,35}, i.e. SEED, NEG_H, NQR17      TRUE
        DR(738) = 9                                            TRUE
        squares mod 9 give DR in {1,4,7,9}                      TRUE
        x^6 has DR in {1,9} for every x                        TRUE
        no prime > 3 has DR in {3,6,9}                          TRUE
        a 5-term sequence has 2^4 = 16 contiguous compositions  TRUE

=== TWO FURTHER ERRORS ===

    "Frobenius shift x -> 26x".  Frobenius on F_37 is x -> x^37, which is
    the identity map on F_37 since 37 is prime.  Multiplication by a
    constant is not a Frobenius; the name imports a structure that is not
    present.

    "collapsing at x^6 to {1,9}, perfectly resetting at x^7".  The first
    half is true.  The reset is false: x^7 == x (mod 9) fails for x = 3 and
    x = 6.  3^7 = 2187 has DR 9, not 3.  It holds only for x coprime to 3,
    where Carmichael lambda(9) = 6 applies -- precisely the elements the
    same synthesis calls the harmonic void are the ones that break it.

=== FALSIFICATION ===
    Exhibit one 137-orbit whose three elements share a digital root.
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def run():
    from math import gcd

    # --- the refutation ---
    const = [nm for nm, o in ORBITS.items() if len({dr(x) for x in o}) == 1]
    assert const == [], const
    assert {dr(x) for x in (1, 10, 26)} == {1, 8}        # the table's own row
    assert gcd(9, P) == 1                                # CRT independence

    # --- the wrap-count law, every x ---
    assert 37 % 9 == 1 and 10 % 9 == 1 and 26 % 9 == 8 == (-1) % 9
    for x in range(1, P):
        for m in (10, 26):
            k = (m * x) // P
            assert (m * x) % P == m * x - P * k
            assert ((m * x) % P) % 9 == ((m % 9) * x - k) % 9, (x, m)

    # --- IC is the unwrapped case and reads x, -x, x ---
    assert (26 * 1) // P == 0 and (10 * 1) // P == 0
    assert [dr(1), dr(26), dr(10)] == [1, 8, 1]
    assert 8 == (-1) % 9
    # a wrapped case: orbit of 3 is 3 -> 4 -> 30, and 4 is 8*3-2 mod 9
    assert (26 * 3) % P == 4 and (26 * 3) // P == 2
    assert 4 % 9 == (8 * 3 - 2) % 9

    # --- what holds in the synthesis ---
    assert (10 * 26) % P == 1 and 100 % P == 26 and (26 * 26) % P == 10
    assert pow(10, 3, P) == 1 and 999 == 27 * P
    assert {36, (36 * 26) % P, (36 * 26 * 26) % P} == {11, 27, 36}
    assert (-11) % P == 26 and (-14) % P == 23
    assert [v % P for v in (24, 48, 72)] == [24, 11, 35]
    assert dr(738) == 9
    assert {dr(x * x) for x in range(1, 10)} == {1, 4, 7, 9}
    assert {dr(x ** 6) for x in range(1, 10)} == {1, 9}
    assert all(dr(p) not in {3, 6, 9}
               for p in (5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 43))
    assert 2 ** 4 == 16

    # --- the two further errors ---
    assert all(pow(x, P, P) == x % P for x in range(P))   # Frobenius = id
    assert [x for x in range(1, 10) if dr(x ** 7) != dr(x)] == [3, 6]
    assert dr(3 ** 7) == 9 and dr(3) == 3

    print("All assertions passed.\n")
    print("THEOREM 329.  DR is NOT invariant on 137-orbits.\n")
    for nm, o in ORBITS.items():
        print(f"   {nm:8s} {str(list(o)):14s} DR {[dr(x) for x in o]}"
              f"   constant: {len({dr(x) for x in o})==1}")
    print(f"\n   constant in {len(const)} of 12.")
    print("   gcd(9,37)=1, so by CRT mod-9 and mod-37 are independent")
    print("   coordinates -- the claim is excluded before any test.\n")
    print("  THE LAW THAT REPLACES IT   (37 == 1 mod 9, so each wrap costs 1)")
    print("     10x mod 37 ==  x - k  (mod 9),  k = floor(10x/37)")
    print("     26x mod 37 == 8x - k  (mod 9),  k = floor(26x/37)")
    print("     verified for every x in 1..36\n")
    print("     26 == 8 == -1 (mod 9): the 137-map NEGATES mod 9 while")
    print("     generating the orbit mod 37.  Unwrapped, the three roots")
    print("     read x, -x, x.  IC never wraps and reads 1, 8, 1 exactly.")
    print("     An anti-invariance with a carry term -- the opposite shape")
    print("     of the claim.\n")
    print("  ALSO FALSE:  'perfectly resetting at x^7'")
    print(f"     x^7 == x (mod 9) fails for x = 3 and 6;  3^7 = {3**7}, DR"
          f" {dr(3**7)}, not 3")
    print("     holds only for x coprime to 3 (lambda(9) = 6) -- the very")
    print("     elements called the harmonic void are the ones that break it.")
    print("  ALSO WRONG:  'Frobenius shift x -> 26x'.  Frobenius on F_37 is")
    print("     x -> x^37, the identity.  Multiplying by a constant is not it.")


if __name__ == "__main__":
    run()
