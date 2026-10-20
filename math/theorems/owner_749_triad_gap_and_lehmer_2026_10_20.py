# CLASS: AUDIT
"""
The owner's 7-4-9 triad on the gap below 136,279,841, and "Lehmer Primes" (owner_work #393, 2026-10-20: "run the triad on the gap below 136279841 /
Lehmer Primes"). The triad as the owner defined it (April 2026): the root of the exponent p is 4, 7 or 9.

THE GAP: mersenne.org/report_milestones (fetched 2026-10-20): every exponent below 142,262,789 has been tested at least once (2026-10-15), and every
  test below 83,200,483 has been verified by a second test (2026-09-04). So a missed Mersenne prime below 136,279,841 can only be at a prime p between
  83,200,483 and 136,279,841 whose single test was wrong.
THE TRIAD ON THE GAP (every prime in it, sieved here):
  2,868,436 primes. By root: 1: 478,165 ; 2: 478,147 ; 4: 477,860 ; 5: 478,090 ; 7: 478,282 ; 8: 477,892 ; 3, 6, 9: none.
  In the triad: 477,860 + 478,282 = 956,142, one third (33.33 %). Every one of them, if its Mersenne number were prime, would give a Mersenne root of 1;
  the other two thirds would give 4 (1,434,307 primes leave 1 by 3, 1,434,129 leave 2).
"LEHMER PRIMES" -- read as the primes the Lucas-Lehmer test proves, the Mersenne primes, as in the owner's LoB 12.1 (cylicamp/lucas_lehmer_proof.md,
  cylicamp/lucas_lehmer_verify.py). The test: s = 4, then s = s x s - 2 by 2^p - 1, p - 2 times; 2^p - 1 is prime exactly when s ends at 0. Run here from
  scratch on every prime p below 1,300: it finds 2 3 5 7 13 17 19 31 61 89 107 127 521 607 1279 and nothing else (the full run to 4,500 also finds 2203 2281
  3217 4253 4423 -- 20 exponents, as the list says).
  The triad on them: 7 → 7, 13 → 4, 31 → 4, 61 → 7, 607 → 13 → 4 : 5 of the 15 below 1,300 (the April count was 4 of the first 12).

FALSIFICATION: any assertion failing.
"""
from collections import Counter

import numpy as np
from sympy import primerange

LO, HI = 83_200_483, 136_279_841
sieve = np.ones(HI // 2 + 1, dtype=bool)          # index i stands for 2i + 1
sieve[0] = False
for i in range(1, int(HI ** 0.5) // 2 + 1):
    if sieve[i]:
        p = 2 * i + 1
        sieve[p * p // 2::p] = False
odd = 2 * np.nonzero(sieve)[0] + 1
assert len(odd) + 1 == 7713644 and odd[-1] == HI            # 136,279,841 is prime; 7,713,644 primes up to it
gap = odd[(odd > LO) & (odd < HI)]
roots = Counter((1 + (gap - 1) % 9).tolist())
assert len(gap) == 2868436
assert dict(sorted(roots.items())) == {1: 478165, 2: 478147, 4: 477860, 5: 478090, 7: 478282, 8: 477892}
in_triad = roots[4] + roots[7] + roots.get(9, 0)
assert in_triad == 956142 and abs(in_triad / len(gap) - 1 / 3) < 0.0001
assert int(np.sum(gap % 3 == 1)) == 1434307 and int(np.sum(gap % 3 == 2)) == 1434129 and 1434307 + 1434129 == len(gap)


def lucas_lehmer(p):
    if p == 2:
        return True
    m, s = (1 << p) - 1, 4
    for _ in range(p - 2):
        s = (s * s - 2) % m
    return s == 0


found = [p for p in primerange(2, 1300) if lucas_lehmer(p)]
assert found == [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279]
dr = lambda n: 1 + (n - 1) % 9
assert [p for p in found if dr(p) in (4, 7, 9)] == [7, 13, 31, 61, 607] and dr(607) == 4 and 6 + 0 + 7 == 13

if __name__ == "__main__":
    print("triad on the unverified gap 83,200,483..136,279,841: 956,142 of 2,868,436 primes (one third); Lucas-Lehmer to 1,300 finds the 15 exponents, 5 in the triad")
