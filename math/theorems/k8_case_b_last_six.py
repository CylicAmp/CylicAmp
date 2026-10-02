# CLASS: THEOREM
"""
T245, k = 8, case B: the six shapes left open by k8_case_b_shape_mod8.py are
impossible.  Added 2026-10-02.

Tool: the MISSING-DIVISOR rule.  Any product of listed primes that divides n
and is below d_8 must itself be listed.  Then n >= lcm(listed) is set against
n = sum of squares.  4 < p < q < r odd primes; 4 || n unless 8 is listed.

 A  1 2 4 p 2p 4p q r     n = 21 + 21p^2 + q^2 + r^2.  2q | n and 2q is not
    listed, so r < 2q.  4pqr | n, so 4p q^2 < n < 21 + 21p^2 + 5q^2, i.e.
    q^2 (4p - 5) < 21(1 + p^2).  With q > 4p: 16p^2(4p-5) < 21(1+p^2), false
    for p >= 2.                                                         QED
 B  1 2 4 p 2p q 4p r     2p < q < 4p < r; 2q (> 4p) unlisted, so r < 2q < 8p.
    n >= 4pqr > 32p^3, n = 21 + 21p^2 + q^2 + r^2 < 21 + 101p^2.  False for
    p >= 4.                                                             QED
 C  1 2 4 p 2p q 4p p^2   2q unlisted, so p^2 < 2q < 8p: p in {5, 7}.
    p = 7: q in (24.5, 28), no prime.  p = 5: q in {13, 17, 19}, and
    100q | n = 1171 + q^2 fails for each.                              QED
 D  1 2 4 p 2p 4p p^2 q   2p^2 unlisted, so p^2 < q < 2p^2.  4p^2 q | n and
    n = 21 + 21p^2 + p^4 + q^2 < 4p^2 q * 2, so n = 4p^2 q exactly:
    q^2 - 4p^2 q + (p^4 + 21p^2 + 21) = 0, discriminant 12(p^4 - 7p^2 - 7).
    p^2 = 1 (mod 3) gives p^4 - 7p^2 - 7 = 2 (mod 3), so 3 || 12(...)/4 and
    the discriminant is not a square.                                   QED
 E  1 2 4 p 2p 4p q p^2   2q unlisted, so p^2/2 < q < p^2.  4p^2 q > 2p^4 and
    n < 2p^4 + 21p^2 + 21 < 8p^2 q, so again n = 4p^2 q, the same quadratic
    as D, no solution.                                                  QED
 F  1 2 4 8 16 p q r      2p unlisted, so r < 2p.  n >= 16pqr > 16p^3 and
    n = 341 + p^2 + q^2 + r^2 < 341 + 9p^2.  False for p >= 17 (p > 16). QED

With k8_case_b_shape_mod8.py, all 13 shapes that were left to search are
proved empty.  Whether k = 8 case B is CLOSED also needs the 33-shape list
to be complete; that list came from the tree built 2026-09-19 and its
completeness is a separate check.

FALSIFICATION: any assertion failing.
"""
from sympy import divisors, isprime, primerange
from math import isqrt

P = list(primerange(5, 3000))
assert all(16 * p * p * (4 * p - 5) >= 21 * (1 + p * p) for p in P)                    # A
assert all(32 * p ** 3 >= 21 + 101 * p * p for p in P)                                  # B
assert [q for q in range(25, 28) if isprime(q)] == []                                   # C, p=7
assert all((1171 + q * q) % (100 * q) for q in (13, 17, 19))                            # C, p=5
assert all(21 + 21 * 25 + q * q + 625 == 1171 + q * q for q in (13, 17, 19))
for p in P:                                                                             # D, E
    assert 2 * 4 * p ** 4 > p ** 4 + 21 * p * p + 21 + 4 * p ** 4                      # n < 2*4p^2q, q > p^2
    assert 2 * p ** 4 + 21 * p * p + 21 < 4 * p ** 4                                   # n < 8p^2 q, q > p^2/2
    d = 12 * (p ** 4 - 7 * p * p - 7)
    assert (p ** 4 - 7 * p * p - 7) % 3 == 2 and isqrt(d) ** 2 != d
assert all(16 * p ** 3 >= 341 + 9 * p * p for p in primerange(17, 3000))                # F

# brute-force cross-check of the missing-divisor rule on real n: whenever the
# 8 smallest divisors of n have one of these shapes, the stated inequality holds
SH = {"A": lambda d, p, q, r: r < 2 * q, "B": lambda d, p, q, r: r < 2 * q,
      "F": lambda d, p, q, r: r < 2 * p}
seen = 0
for n in range(4, 300000, 4):
    ds = divisors(n)[:8]
    if len(ds) < 8 or ds[:3] != [1, 2, 4]:
        continue
    odd = [x for x in ds if x % 2 and x > 1]
    if len(odd) == 3 and all(isprime(x) for x in odd):
        p, q, r = odd
        if ds == [1, 2, 4, p, 2 * p, 4 * p, q, r]:
            assert SH["A"](ds, p, q, r); seen += 1
        if ds == [1, 2, 4, p, 2 * p, q, 4 * p, r]:
            assert SH["B"](ds, p, q, r); seen += 1
        if ds == [1, 2, 4, 8, 16, p, q, r]:
            assert SH["F"](ds, p, q, r); seen += 1
assert seen > 0

if __name__ == "__main__":
    print("k=8 case B last six shapes: all assertions pass; rule checked on", seen, "real n")
