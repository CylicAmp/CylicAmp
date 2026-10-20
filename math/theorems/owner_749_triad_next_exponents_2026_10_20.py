# CLASS: AUDIT
"""
The owner's 7-4-9 triad run on the next exponents (owner_work #392, 2026-10-20: "run the 7-4-9 triad on the next exponents").
The triad as the owner defined it in April 2026 (discoveries/mersenne_exponents_role_7_4_9_2026_04/): the root of the exponent p in {4, 7, 9}.

NO 53RD EXPONENT IS KNOWN: mersenne.org/primes (fetched 2026-10-20) lists 52 Mersenne primes, the largest 2^136,279,841 - 1 (2024 Oct 12), marked
  "Provisional ranking, not all candidates between M82589933 and M136279841 have been eliminated". So the next exponent is not known, and it could lie
  below 136,279,841 as well as above it.
THE NEXT CANDIDATES (a Mersenne exponent must be prime): the 12 primes after 136,279,841, with their roots, triad membership, and the root a Mersenne prime
  on that exponent would have (#391's theorem: exponent root 1, 4, 7 → 1 ; root 2, 5, 8 → 4):
    136279879  7  in the triad  → 1        136279981  1  no → 1
    136279901  2  no            → 4        136279987  7  in the triad  → 1
    136279919  2  no            → 4        136280003  5  no → 4
    136279933  7  in the triad  → 1        136280009  2  no → 4
    136279967  5  no            → 4        136280051  8  no → 4
                                           136280059  7  in the triad  → 1
                                           136280071  1  no → 1
  4 of the 12 are in the triad (all root 7). Whichever exponent comes next, it is in the triad when it leaves 1 by 3 and its root is not 1, and then
  its Mersenne number has root 1; 9 cannot happen (a prime above 3 is never a multiple of 3).
THE KNOWN 52 AGAIN: 13 in the triad (8 with root 4, 5 with root 7, none with 9). Among the 50 exponents from 5 on that is 13 of 50 = 26 %; a fair draw
  of primes gives 1/3 (two roots out of six): binomial p = 0.30, no detectable lean.

FALSIFICATION: any assertion failing.
"""
from scipy.stats import binomtest
from sympy import isprime, nextprime

dr = lambda n: 1 + (n - 1) % 9
nxt, p = [], 136279841
while len(nxt) < 12:
    p = nextprime(p)
    nxt.append(p)
assert nxt == [136279879, 136279901, 136279919, 136279933, 136279967, 136279981, 136279987, 136280003, 136280009, 136280051, 136280059, 136280071]
assert [dr(q) for q in nxt] == [7, 2, 2, 7, 5, 1, 7, 5, 2, 8, 7, 1]
triad = [q for q in nxt if dr(q) in (4, 7, 9)]
assert triad == [136279879, 136279933, 136279987, 136280059] and all(dr(q) == 7 for q in triad)
mersenne_root = lambda q: 1 + ((pow(2, q, 9) - 1) % 9 - 1) % 9
assert [mersenne_root(q) for q in nxt] == [1 if q % 3 == 1 else 4 for q in nxt]
assert all(mersenne_root(q) == 1 for q in triad)
assert all(q % 3 != 0 for q in nxt)

known_big = [5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209,
             44497, 86243, 110503, 132049, 216091, 756839, 859433, 1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011, 24036583,
             25964951, 30402457, 32582657, 37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933, 136279841]
assert len(known_big) == 50 and all(isprime(q) for q in known_big)
in_triad = [q for q in known_big if dr(q) in (4, 7, 9)]
assert len(in_triad) == 13 and round(binomtest(13, 50, 1 / 3).pvalue, 2) == 0.30

if __name__ == "__main__":
    print("7-4-9 triad on the next candidate exponents: 4 of the next 12 primes after 136,279,841 (all root 7); no 53rd exponent known")
