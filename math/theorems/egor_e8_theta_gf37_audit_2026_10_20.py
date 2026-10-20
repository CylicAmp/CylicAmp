# CLASS: AUDIT
"""
Egor -- E8 theta-series verification (owner_work #392, 2026-10-20). Computed in the owner's Egor project, so the owner's work; the text is Egor's output.
The E8 theta series is 1 + 240 x (sum of sigma_3(n) q^n), sigma_3(n) = the sum of the cubes of the divisors of n. 240 = 6x37 + 18 is not a multiple of 37,
so a coefficient is 0 by 37 exactly when 37 divides sigma_3(n).

RIGHT (re-run):
  x^3 = -1 (by 37) exactly for x in {11, 27, 36}; 10^3 = 1, 26^3 = 1, 36^3 = -1. (11 = 37-26, 27 = 37-10, 36 = 37-1: the negatives of the cube roots of 1.)
  S_e(p) = 1 + p^3 + ... + p^(3e) = sigma_3(p^e). When p^3 = -1 by 37: S_e = 0 for e odd, 1 for e even. So a prime p = 11, 27 or 36 by 37 with an odd power
    in n makes 37 divide sigma_3(n): a sufficient condition.
  The 100,000-integer test: 15,692 n meet the condition, 17,580 n have 37 dividing sigma_3(n), 0 counterexamples, 1,888 zeros the condition misses, the first n = 49.
  7^3 = 343 = 9x37 + 10, and 1 + 10 + 10x10 = 111 = 3x37: the second way a prime power can vanish.
WRONG:
  "sigma_3(49) = 1+7^3+7^6 = 118,993" -- 1 + 343 + 117,649 = 117,993, and 117,993 = 37 x 3189. The line "118,993 = 37(3216)+1" is right arithmetic on the wrong
  value; the "Correction" that follows notices it but leaves the 118,993 standing.
MISSING (asked): the two "executable files" (the verification engine and the results) are named but not attached; the test was re-run here instead.
THE NEXT EXTENSION, DONE HERE (classify by the order of p^3):
  For a prime p other than 37 put x = p^3 by 37. Then S_e(p) = (x^(e+1) - 1)/(x - 1) when x is not 1, and S_e(p) = e + 1 when x = 1. So the prime-power factor
  vanishes exactly when
     x is not 1 and the order of x divides e + 1,   or   x = 1 and 37 divides e + 1   (p = 37 never: S_e(37) leaves 1).
  The order of x = p^3 by 37 is 1, 2, 3, 4, 6 or 12 (the cubes form the 12 numbers of order dividing 12). Over the 36 residues: order 12: 12, 6: 6, 4: 6, 3: 6, 2: 3, 1: 3.
  Order 2 is the parity rule (x = -1, p = 11, 27, 36); order 3 is the 49 case (p = 7, 9, 12, 16, 33, 34 by 37, e = 2, 5, 8, ...); order 4 needs e = 3, 7, ...;
  order 6 e = 5, 11, ...; order 12 e = 11, 23, ... (2^11 = 2048 is the first: 2^3 = 8 has order 12).
  37 divides sigma_3(n) exactly when one prime power of n vanishes this way (sigma_3 multiplies over prime powers): checked on all n up to 100,000 -- the rule
  gives exactly the 17,580 zeros. By mechanism: order 2 only 15,423 ; order 3 only 1,609 ; order 6 only 236 ; orders 2 and 3 together 234 ; ...

FALSIFICATION: any assertion failing.
"""
from collections import Counter

import numpy as np

P = 37
N = 100_000
assert sorted(x for x in range(1, P) if pow(x, 3, P) == P - 1) == [11, 27, 36]
assert (pow(10, 3, P), pow(26, 3, P), pow(36, 3, P)) == (1, 1, 36) and (37 - 26, 37 - 10, 37 - 1) == (11, 27, 36)
assert 240 % 37 == 18


def order(x):
    k, y = 1, x % P
    while y != 1:
        y, k = y * x % P, k + 1
    return k


spf = np.zeros(N + 1, dtype=np.int64)                     # smallest prime factor
for i in range(2, N + 1):
    if spf[i] == 0:
        spf[i::i][spf[i::i] == 0] = i


def factor(n):
    out = {}
    while n > 1:
        p = int(spf[n])
        out[p] = out.get(p, 0) + 1
        n //= p
    return out


def S_mod(p, e):
    x = pow(p, 3, P)
    return sum(pow(x, k, P) for k in range(e + 1)) % P


for p in (11, 73, 101, 139):
    if pow(p, 3, P) == P - 1:
        assert all(S_mod(p, e) == (0 if e % 2 else 1) for e in range(0, 12))

zeros, parity, mech = [], [], Counter()
for n in range(1, N + 1):
    f = factor(n)
    s = 1
    for p, e in f.items():
        s = s * S_mod(p, e) % P
    if s == 0:
        zeros.append(n)
    if any(p % P in (11, 27, 36) and e % 2 == 1 for p, e in f.items()):
        parity.append(n)
assert (len(parity), len(zeros)) == (15692, 17580)
zs = set(zeros)
assert all(n in zs for n in parity) and len(zs - set(parity)) == 1888 and min(zs - set(parity)) == 49

assert 1 + 7 ** 3 + 7 ** 6 == 117993 == 37 * 3189 and 117993 != 118993 and 37 * 3216 + 1 == 118993
assert 7 ** 3 % P == 10 and 1 + 10 + 100 == 111 == 3 * 37


def vanishes(p, e):
    if p == P:
        return False
    x = pow(p, 3, P)
    return (e + 1) % P == 0 if x == 1 else (e + 1) % order(x) == 0


assert all(vanishes(p, e) == (S_mod(p, e) == 0) for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 43, 47, 53) for e in range(0, 80))
full = [n for n in range(1, N + 1) if any(vanishes(p, e) for p, e in factor(n).items())]
assert full == zeros
assert sorted(Counter(order(pow(r, 3, P)) for r in range(1, P)).items()) == [(1, 3), (2, 3), (3, 6), (4, 6), (6, 6), (12, 12)]
assert sorted(r for r in range(1, P) if order(pow(r, 3, P)) == 3) == [7, 9, 12, 16, 33, 34] and order(8) == 12 and S_mod(2, 11) == 0
assert min(n for n in zeros if n % 2 == 0 and all(not vanishes(p, e) for p, e in factor(n).items() if p != 2)) == 2048

for n in zeros:
    kinds = set()
    for p, e in factor(n).items():
        if vanishes(p, e):
            x = pow(p, 3, P)
            kinds.add(order(x) if x != 1 else 37)
    mech[tuple(sorted(kinds))] += 1
assert (mech[(2,)], mech[(3,)], mech[(6,)], mech[(2, 3)]) == (15423, 1609, 236, 234)

if __name__ == "__main__":
    print("Egor E8: cube roots, S_e rule and the 100,000 counts right; sigma_3(49) = 117,993 = 37 x 3189 (not 118,993); "
          "vanishing classified by the order of p^3 -- matches all 17,580 zeros")
