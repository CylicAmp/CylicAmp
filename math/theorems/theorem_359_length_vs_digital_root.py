# CLASS: THEOREM
"""
Theorem 359: three levels of information in a string of nines -- length,
its mod-9 quotient, and the constant that retains nothing
Author: Michael Warren Song (CyclicAmp)

From the observation that 9, 99, 999 "go forever 9" while 9+1, 99+2, 999+3
give 10, 20, 30.  Those are two different maps on the same object, and
there is a third between them.

=== THE THREE LEVELS ===

    Write R_k for the string of k nines, R_k = 10^k - 1.

        coordinate       value      retains
        l(R_k) = k       k          everything; additive
        DR(10k)          k mod 9    k up to multiples of 9
        DR(R_k)          9          nothing

    All three checked for k = 1..40:  DR(R_k) takes the single value 9,
    and DR(10k) = DR(k) exactly, since 10 == 1 (mod 9).

=== THE MIDDLE ONE IS A QUOTIENT; THE BOTTOM ONE IS NOT ===

    l -> l mod 9 is a homomorphism, so DR(10k) is a genuine quotient of the
    length coordinate.

    R_k -> DR(R_k) is the CONSTANT map.  It is not a projection of k at all
    -- it factors through nothing, and no information about k survives it.
    "Forever 9" is not a weak signal; it is the absence of one.

    That distinction is what makes the offset worth having.  If DR(R_k) had
    returned k mod 9 the offset would be a convenience.  It returns a
    constant, so the offset is a repair.

=== THE OFFSET CLIMBS TWO LEVELS IN ONE STEP ===

        digitsum(R_k) + k  =  9k + k  =  10k

    Forced in one line.  digitsum(R_k) = 9k because every digit is a nine,
    and adding k recovers 10k, whose length coordinate is k again.  So the
    operation goes from the bottom row to the top in a single step, without
    passing through the quotient.

    Verified for k = 1..39.

=== ADDITIVITY, AND WHAT SURVIVES IT ===

    Under concatenation of nine-blocks,

        l(A|B) = l(A) + l(B)                exact
        DR(10 l(A|B)) = the sum mod 9       exact
        DR(A|B) = 9                          regardless

    So a split never changes the total length coordinate:

        9|999      1 + 3      = 4
        99|99      2 + 2      = 4
        9|9|99     1 + 1 + 2  = 4

    and k = 9 is where the quotient closes a full period, DR(90) = 9 with
    DR(100) = 1 returning to the start.

=== TWO OPERATIONS THAT ARE NOT THE SAME ===

    An outside reading gave (10^k - 1) + k = 10^k + (k - 1), producing
    10, 101, 1002, 10003.  That arithmetic is correct and it is a different
    operation: it does not reproduce 20, 30 or 40.  Literal addition does
    not collapse the string, so it carries no length coordinate -- the
    result is the number again, shifted by one.  Only the digit-sum route
    gives 10k.

=== PRIOR ART, CHECKED ===

    `dr_ring_homomorphism_emirp_palindrome.py` proves DR is a ring
    homomorphism on NUMBERS: DR(a+b) = DR(DR(a)+DR(b)).  That is a
    different statement -- about addition of numbers, not concatenation of
    strings -- and it does not give the three-level split above.
    T226 has the k = 1 case for threes: "three 3s sum to 9; 9+1 = 10".

=== FALSIFICATION ===
    A k with DR(R_k) != 9; or digitsum(R_k) + k != 10k.
"""


def dr(n):
    return 1 + (n - 1) % 9 if n else 0


def ds(n):
    return sum(map(int, str(n)))


def R(k):
    return 10 ** k - 1


def ell(*blocks):
    return sum(blocks)


def run():
    # --- the three levels ---
    assert {dr(R(k)) for k in range(1, 41)} == {9}
    assert all(dr(10 * k) == dr(k) for k in range(1, 200))
    assert all(ds(R(k)) == 9 * k for k in range(1, 40))

    # --- the offset climbs two levels ---
    assert all(ds(R(k)) + k == 10 * k for k in range(1, 40))

    # --- additivity under concatenation ---
    for parts in ([1, 3], [2, 2], [1, 1, 2], [6, 4], [9, 9], [5, 3, 1]):
        k = ell(*parts)
        assert int("9" * k) == R(k)
        assert dr(10 * k) == dr(k)
        assert dr(R(k)) == 9
    assert ell(1, 3) == ell(2, 2) == ell(1, 1, 2) == 4
    assert ell(6, 4) == 10 and dr(100) == 1
    assert dr(90) == 9 and dr(100) == 1          # period closes at k = 9

    # --- the quotient is a homomorphism; the constant map is not ---
    for a in range(1, 30):
        for b in range(1, 30):
            assert dr(10 * (a + b)) == dr(dr(10 * a) + dr(10 * b))
    assert len({dr(R(k)) for k in range(1, 41)}) == 1   # constant

    # --- the literal reading is a different operation ---
    assert R(3) + 3 == 1002 != 30
    assert ds(R(3)) + 3 == 30
    assert all(R(k) + k == 10 ** k + (k - 1) for k in range(1, 12))

    print("All assertions passed.\n")
    print("THEOREM 359.  Three levels, not two.\n")
    print("   k    R_k              DR(R_k)   10k    DR(10k)")
    for k in (1, 2, 3, 4, 9, 10, 18):
        print(f"  {k:2d}    {str(R(k))[:12]:<12s}       {dr(R(k))}     {10*k:3d}"
              f"      {dr(10*k)}")
    print()
    print("   l(R_k) = k        retains everything, additive")
    print("   DR(10k) = k mod 9 a genuine quotient of l")
    print("   DR(R_k) = 9       the CONSTANT map -- retains nothing\n")
    print("   'forever 9' is not a weak signal, it is the absence of one.")
    print("   that is why the offset is a repair and not a convenience.\n")
    print("   digitsum(R_k) + k = 9k + k = 10k  -- bottom row to top row")
    print("   in one step, skipping the quotient entirely.\n")
    print("   splits never change the total:")
    for parts in ([1, 3], [2, 2], [1, 1, 2]):
        print(f"     {' | '.join('9'*p for p in parts):<14s} "
              f"{' + '.join(map(str,parts))} = {ell(*parts)}")
    print(f"\n   k = 9 closes the quotient period: DR(90) = {dr(90)},"
          f" DR(100) = {dr(100)}.\n")
    print("   and the literal reading is a DIFFERENT operation:")
    print(f"     (10^3 - 1) + 3 = {R(3)+3}   -- correct, but not 30")
    print(f"     digitsum(999) + 3 = {ds(R(3))+3}   -- this is the one")


if __name__ == "__main__":
    run()
