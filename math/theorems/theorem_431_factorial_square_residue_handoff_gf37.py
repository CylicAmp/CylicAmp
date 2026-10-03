# CLASS: THEOREM
"""
T431 — n! is never a square for n > 1: the residue-oracle -> moving-witness handoff

Supplied reading (2026-09-27), verified here.

CLAIM. n! is not a perfect square for any n > 1.

PROOF. Bertrand's postulate (conjectured by Bertrand 1845, checked by him to 3e6;
proved by Chebyshev 1852; Ramanujan 1919; Erdos's elementary proof 1932) gives a
prime p in (n/2, n]. Since 2p > n, Legendre gives v_p(n!) = 1, which is odd.

THE HANDOFF. A fixed-modulus oracle only works for small n:
  * mod 9: squares are {0,1,4,7}. n! mod 9 = 1, 2, 6, 6, 3 for n = 1..5, so mod 9
    rules out n = 2, 3, 4, 5. From n = 6 on, 9 | n!, residue 0 is a square
    residue, and the oracle is blind.
  * mod 37 (GF(37)): n! mod 37 is a quadratic non-residue for exactly 17 values
    n <= 36: 2,3,4,6,7,13,15,16,18,20,21,23,29,30,32,33,34. n = 36 is NOT caught:
    Wilson gives 36! = -1, and -1 is a QR mod 37 (37 = 1 mod 4). From n = 37 on,
    37 | n! and the oracle is blind.
  * any fixed m: n! = 0 (mod m) once n is large, and 0 is a square residue.
So no fixed residue class excludes large factorials from the squares; the
certificate that does is a moving witness p(n) in (n/2, n] with v_p = 1.

Same three-stage shape as the T245 family search: fixed residue filter
(divisibility / valuation prunes), moving witness (read-off prime), and a coupled
case the first two miss (supply cycles). Here the witness never fails, so the
proof closes; in T245 the coupled case must be enumerated.

DISTINCT FROM Brocard: n! + 1 = m^2 is open; solutions n = 4, 5, 7 only are
known (searched to n < 1e9, Berndt-Galway 2000; finitely many under abc,
Overholt 1993). Checked here for n <= 1000.

FALSIFICATION: a square n! with n > 1, or a mod-9 / mod-37 table that differs
from the one asserted below.
"""
from math import factorial, isqrt
from sympy import primerange

SQ9 = {x * x % 9 for x in range(9)}
QR37 = {x * x % 37 for x in range(1, 37)}

assert SQ9 == {0, 1, 4, 7}
mod9_forbids = [n for n in range(1, 40) if factorial(n) % 9 not in SQ9]
assert mod9_forbids == [2, 3, 4, 5], mod9_forbids

mod37_forbids = [n for n in range(1, 60) if factorial(n) % 37 and factorial(n) % 37 not in QR37]
assert mod37_forbids == [2, 3, 4, 6, 7, 13, 15, 16, 18, 20, 21, 23, 29, 30, 32, 33, 34], mod37_forbids
assert factorial(36) % 37 == 36 and 36 in QR37          # Wilson: 36! = -1, a QR since 37 = 1 mod 4
assert all(factorial(n) % 37 == 0 for n in range(37, 60))

N = 300
for n in range(2, N + 1):
    f = factorial(n)
    assert isqrt(f) ** 2 != f, n
    p = max(primerange(n // 2 + 1, n + 1))              # Bertrand witness
    assert 2 * p > n
    v = sum(n // p ** k for k in range(1, 5) if p ** k <= n)   # Legendre
    assert v == 1, (n, p, v)

brocard = [n for n in range(1, 1001) if isqrt(factorial(n) + 1) ** 2 == factorial(n) + 1]
assert brocard == [4, 5, 7], brocard

if __name__ == "__main__":
    print("T431: n! never a square for 2 <= n <=", N, "(witness v_p = 1 each n)")
    print("  mod 9 forbids n =", mod9_forbids, "; blind from n = 6")
    print("  mod 37 forbids n =", mod37_forbids, "; blind from n = 37 (36! = -1 is a QR)")
    print("  Brocard n! + 1 = m^2, n <= 1000:", brocard)
