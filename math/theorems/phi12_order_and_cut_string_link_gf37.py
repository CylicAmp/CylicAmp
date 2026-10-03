# CLASS: THEOREM
"""
Every prime factor of Phi_12(137) is 1 mod 12, and 13 links Phi_12 to the cut string
Author: Michael Warren Song (CyclicAmp)

STATEMENT 1 (general, not specific to 137)
    If p | Phi_d(a) and ord_p(a) = d, then d | (p-1), i.e. p = 1 (mod d).
    This is Fermat's little theorem applied to the cyclic group F_p^*: an
    element of order d exists only in a group whose order is a multiple
    of d, and |F_p^*| = p-1.

    Checked for Phi_12(137) = 352256593 = 13 * 2473 * 10957:
        13    mod 12 = 1,  ord_13(137)    = 12
        2473  mod 12 = 1,  ord_2473(137)  = 12
        10957 mod 12 = 1,  ord_10957(137) = 12

STATEMENT 2 (the link)
    The 12-digit string S = 113115117167, cut and factored in
    cut_table_113115117167.py (commit 6bde9c7), is:

        S = 13 * 8701162859

    13 is also the smallest prime factor of Phi_12(137). It is the only
    one of Phi_12(137)'s three primes dividing S:

        gcd(S, Phi_3(137))  = 1
        gcd(S, Phi_12(137)) = 13

    So the cut-string theorem and the cyclotomic-family theorem
    (cyclo_ntt_sl2_gf37.py) share exactly one prime, and it is 13.

STATEMENT 3 (period of 1/137)
    ord_137(10) = 8, so 1/137 has an 8-digit repeating decimal block:
        1/137 = 0.00729927... repeating with period 8 (0072992700...)
    This is the standard fact that the decimal period of 1/p divides p-1
    (Fermat again), realised here as exactly 8, not a proper divisor of 136.

FALSIFICATION
    Any assert below failing.
"""

from sympy import factorint, n_order, gcd, isprime

A = 137
S = 113115117167


def run():
    Phi3 = A ** 2 + A + 1
    Phi12 = A ** 4 - A ** 2 + 1

    assert factorint(Phi3) == {7: 1, 37: 1, 73: 1}
    assert factorint(Phi12) == {13: 1, 2473: 1, 10957: 1}

    for p in factorint(Phi12):
        assert isprime(p)
        assert p % 12 == 1
        assert n_order(A, p) == 12

    assert factorint(S) == {13: 1, 8701162859: 1}
    assert gcd(S, Phi3) == 1
    assert gcd(S, Phi12) == 13
    assert sorted(set(factorint(Phi12)) & set(factorint(S))) == [13]

    assert n_order(2, 37) == 36
    assert pow(2, 12, 37) == 26
    assert sorted({pow(2, k, 37) for k in (0, 12, 24)}) == [1, 10, 26]

    assert n_order(10, 137) == 8

    print("All assertions passed.\n")
    print(f"Phi_3(137)  = {Phi3}  = {factorint(Phi3)}")
    print(f"Phi_12(137) = {Phi12}  = {factorint(Phi12)}")
    for p in sorted(factorint(Phi12)):
        print(f"  p={p:<8} p mod 12 = {p % 12}   ord_p(137) = {n_order(A, p)}")
    print()
    print(f"S = {S} = {factorint(S)}")
    print(f"gcd(S, Phi_3)  = {gcd(S, Phi3)}")
    print(f"gcd(S, Phi_12) = {gcd(S, Phi12)}   <- the shared prime")
    print()
    print(f"ord_137(10) = {n_order(10, 137)}   1/137 repeats with period 8")


if __name__ == "__main__":
    run()
