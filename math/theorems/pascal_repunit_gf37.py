# CLASS: THEOREM
"""
1+2+1 = 2^2 and 121 = 11^2 are the same fact: Pascal rows evaluated in base 10
Author: Michael Warren Song (CyclicAmp)

STATEMENT
    Row n of Pascal's triangle, read as base-10 digits, equals 11^n exactly
    as long as every binomial coefficient in that row is a single digit:

        sum_{k=0..n} C(n,k) * 10^(n-k)  =  11^n        (always, by binomial thm)
        concat(C(n,0), ..., C(n,n))     =  11^n        iff max C(n,k) < 10

    The first fails at n = 5, where C(5,2) = 10 forces a carry:

        11^5 = 161051   but the row is  1 5 10 10 5 1

    So the two observations about 1,2,1 are one observation:
        row sum      sum_k C(n,k) = 2^n        n=2 -> 1+2+1 = 4  = 2^2
        row as digits            = 11^n        n=2 -> 121        = 11^2

    Both are the binomial theorem, at x=1 and x=10 respectively:
        (1+1)^n = 2^n          (10+1)^n = 11^n

GF(37)
    ord_37(11) = 6, and the repunit tower alternates between the antipodal
    pair NEG_H = {11,27,36} and IC = {1,10,26}, hitting all three of each:

        11^1 = 11  NEG_H       11^4 = 26  IC
        11^2 = 10  IC          11^5 = 27  NEG_H
        11^3 = 36  NEG_H       11^6 =  1  IC        (36 = -1 mod 37)

    Odd powers land in NEG_H, even powers in IC, with no other orbit touched.
    NEG_H and IC are negation duals (T265), so the tower is exactly the
    alternation between an orbit and its antipode.

    2^n mod 37 has period 36 (2 is a primitive root), so the row-sum side
    sweeps every nonzero residue while the row-digit side is locked to a
    3-cycle. The two readings of the same row diverge completely mod 37.

FALSIFICATION
    Any n < 5 where the digit reading differs from 11^n, or any n where the
    row sum differs from 2^n, or ord_37(11) != 6, or any n where 11^n leaves the NEG_H/IC alternation.
"""

from math import comb

P = 37
ORBITS = {
    'IC': {1, 10, 26},      'DARK_A': {2, 15, 20},  'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23},    'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36},  'C9': {14, 29, 31},
    'NQR17': {17, 22, 35},  'SEED': {18, 24, 32},   'SA_ST_B': {21, 25, 28},
}


def orbit_of(n):
    r = n % P
    if r == 0:
        return 'SEAM'
    for name, s in ORBITS.items():
        if r in s:
            return name
    raise AssertionError(r)


def row(n):
    return [comb(n, k) for k in range(n + 1)]


def row_as_digits(n):
    r = row(n)
    if max(r) > 9:
        return None
    return int("".join(str(c) for c in r))


def run():
    # row sums are 2^n, always
    for n in range(0, 60):
        assert sum(row(n)) == 2 ** n, n

    # weighted-by-powers-of-10 is 11^n, always (binomial theorem at x=10)
    for n in range(0, 60):
        assert sum(comb(n, k) * 10 ** (n - k) for k in range(n + 1)) == 11 ** n, n

    # naive digit concatenation equals 11^n exactly while no coefficient >= 10
    for n in range(0, 5):
        assert row_as_digits(n) == 11 ** n, n
    assert max(row(5)) == 10 and row_as_digits(5) is None
    assert 11 ** 5 == 161051

    # the 1,2,1 case, both readings
    assert sum(row(2)) == 4 == 2 ** 2
    assert row_as_digits(2) == 121 == 11 ** 2

    # GF(37): ord_37(11) = 6, alternating NEG_H / IC
    assert next(k for k in range(1, P) if pow(11, k, P) == 1) == 6
    assert [pow(11, n, P) for n in range(1, 7)] == [11, 10, 36, 26, 27, 1]
    assert pow(11, 3, P) == P - 1                      # 36 = -1
    for n in range(1, 25):
        assert orbit_of(pow(11, n, P)) == ('NEG_H' if n % 2 else 'IC'), n
    # 2 is a primitive root, so 2^n sweeps everything
    assert len({pow(2, n, P) for n in range(36)}) == 36

    print("All assertions passed.\n")
    print("  n   Pascal row            sum = 2^n   digits = 11^n   11^n mod37  orbit")
    for n in range(0, 7):
        r = row(n)
        d = row_as_digits(n)
        ds = str(d) if d is not None else "-- carries --"
        print(f"  {n}   {str(r):<22} {sum(r):9d}   {ds:>13}   {pow(11,n,P):9d}  {orbit_of(pow(11,n,P))}")
    print()
    print(f"  11^5 = {11**5}  but row 5 = {row(5)}  (C(5,2) = 10 carries)")
    print(f"  ord_37(11) = 6   ord_37(2) = 36")


if __name__ == "__main__":
    run()
