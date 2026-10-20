# CLASS: AUDIT
"""
The PDF "Mersenne Exponents: DR Patterns vs the 7-4-9 Triad" (dated Oct 16, 2026, "@Fisher"; uploaded by the owner, owner_work #391, 2026-10-20;
kept at records/supplied/Mersenne_Exponents_DR_Patterns_vs_the_7-4-9_Triad_2026_10_16.pdf). It opens: "Rebuilt from the logged title after the original was lost;
the original wording was not recoverable from past chats, so every definition below is stated explicitly." Nothing is put in the owner's mouth.

THE ORIGINAL IS IN THE REPOSITORY (found, April 2026, the owner's): discoveries/mersenne_exponents_role_7_4_9_2026_04/ (README, statement.tex, verification.py)
  and discoveries/dr_compression_7_4_9_triad_2026_04/. There the 7-4-9 triad is the set of roots {4, 7, 9} ("DR=9 is the universal attractor", "7 and 4 are
  symmetry anchors") and it is applied to the EXPONENT: "Among the known Mersenne prime exponents p in {2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127}, four have
  digital roots in the 7-4-9 triad {4,7,9}: p = 7, 13, 31, 61". The PDF applies the triad to the root of the Mersenne number 2^p - 1 instead -- a different
  question. Both are checked below.

RIGHT (every number in the PDF re-run):
  the root of 2^n - 1 repeats every 6: n = 1 2 3 4 5 0 (by 6) → 1 3 7 6 4 9 ; odd n → 1 7 4, even n → 3 6 9.
  Theorem (p at least 5): root(p) in {1, 4, 7} → root(2^p - 1) = 1 ; root(p) in {2, 5, 8} → 4 ; p = 2 → 3 ; p = 3 → 7.
  9 is never reached by a prime exponent, 7 only at p = 3. The table p by 18. All 52 rows of section 6.
  Of the 52 known exponents (to 136,279,841): 26 give 4, 1 gives 7, 0 give 9, 24 give 1, 1 gives 3. Exponent roots: 1: 11, 4: 8, 7: 5 ; 2: 9, 5: 12, 8: 6 ; 3: 1.
  Primes 5 to 10,000,000: each of the six roots 16.65 % to 16.68 %, and 49.99 % leave 1 by 3. Family split 24 vs 26: binomial p = 0.89 ; roots 11 8 8 12 5 6
  against 8.33 each: chi-square 4.48 on 5, p = 0.48. Remainders by 37: 14 values, counts 4 1 3 1 1 4 2 5 1 3 4 7 9 7. Section 7 (by 999): the 12 classes by 36,
  every column; M_61 = 2,305,843,009,213,693,951, groups add to 3,016, 3 + 016 = 19.
WRONG:
  "the second half of the cycle 1, 3, 7, 6, 4, 9 with the 6 removed": the second half is 6, 4, 9; removing 6 leaves 4, 9. The 7 sits in the first half (n = 3).
    What gives 7, 4, 9 is the last four, 7 6 4 9, with the 6 removed.
  "the original wording was not recoverable": the original is in the repository (above), and its triad is on the exponent's root.
FORCED: the theorem holds for every n that is not a multiple of 2 or 3, prime or not (it is about n by 6); it says nothing special about Mersenne primes.
  The bias tests find none, which is what the theorem plus a fair split of primes by 3 predicts.
THE ORIGINAL QUESTION ON ALL 52 (the owner's April triad, root of the exponent in {4, 7, 9}):
  13 of the 52: root 4 for 13, 31, 607, 2281, 3217, 4423, 24036583, 74207281 (8) ; root 7 for 7, 61, 2203, 23209, 30402457 (5) ; root 9 for none.
  The April count, 4 of the first 12 (7, 13, 31, 61), is right and is the start of this list. And the PDF's theorem ties the two: an exponent in the owner's
  triad (root 4 or 7, p at least 5) always gives a Mersenne number of root 1.
MISSING (asked): the "3-6-9 build" the PDF cites (its Lemma 6, Theorem 3d, the "insertion rule", and "P3, nine is zero"). The repository's
  prime_insertion_sequence_audit.py has a P3, but it is "111 = 3 x 37", so it is not that document.
FRAMEWORKS: 136279841 = the newest exponent, root 5 ; 2^p - 1 is never a multiple of 3, 27 or 37 for a prime p above 3.

FALSIFICATION: any assertion failing.
"""
import math

import numpy as np
from scipy.stats import binomtest, chi2

EXPONENTS = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209,
             44497, 86243, 110503, 132049, 216091, 756839, 859433, 1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011, 24036583,
             25964951, 30402457, 32582657, 37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933, 136279841]
assert len(EXPONENTS) == 52


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def dr_mersenne(p):                       # root of 2^p - 1 from 2^p by 9
    return dr((pow(2, p, 9) - 1) % 9)


assert [dr(2 ** n - 1) for n in range(1, 13)] == [1, 3, 7, 6, 4, 9] * 2
assert [dr(2 ** n) for n in range(1, 7)] == [2, 4, 8, 7, 5, 1]
assert [1, 3, 7, 6, 4, 9][3:] == [6, 4, 9] and [x for x in [6, 4, 9] if x != 6] == [4, 9] != [7, 4, 9] and [x for x in [7, 6, 4, 9] if x != 6] == [7, 4, 9]
assert all(dr_mersenne(p) == dr(2 ** p - 1) for p in EXPONENTS[:15])
for n in range(5, 5000):
    if n % 2 and n % 3:
        assert dr_mersenne(n) == (1 if n % 3 == 1 else 4)
assert dr_mersenne(2) == 3 and dr_mersenne(3) == 7

pdf_rows = {2: (2, 2, 3), 3: (3, 3, 7), 5: (5, 5, 4), 7: (7, 1, 1), 13: (4, 1, 1), 17: (8, 5, 4), 19: (1, 1, 1), 31: (4, 1, 1), 61: (7, 1, 1),
            89: (8, 5, 4), 107: (8, 5, 4), 127: (1, 1, 1), 521: (8, 5, 4), 607: (4, 1, 1), 1279: (1, 1, 1), 2203: (7, 1, 1), 2281: (4, 1, 1),
            3217: (4, 1, 1), 4253: (5, 5, 4), 4423: (4, 1, 1), 9689: (5, 5, 4), 9941: (5, 5, 4), 11213: (8, 5, 4), 19937: (2, 5, 4), 21701: (2, 5, 4),
            23209: (7, 1, 1), 44497: (1, 1, 1), 86243: (5, 5, 4), 110503: (1, 1, 1), 132049: (1, 1, 1), 216091: (1, 1, 1), 756839: (2, 5, 4),
            859433: (5, 5, 4), 1257787: (1, 1, 1), 1398269: (2, 5, 4), 2976221: (2, 5, 4), 3021377: (5, 5, 4), 6972593: (5, 5, 4),
            13466917: (1, 1, 1), 20996011: (1, 1, 1), 24036583: (4, 1, 1), 25964951: (5, 5, 4), 30402457: (7, 1, 1), 32582657: (2, 5, 4),
            37156667: (5, 5, 4), 42643801: (1, 1, 1), 43112609: (8, 5, 4), 57885161: (5, 5, 4), 74207281: (4, 1, 1), 77232917: (2, 5, 4),
            82589933: (2, 5, 4), 136279841: (5, 5, 4)}
assert sorted(pdf_rows) == sorted(EXPONENTS)
assert all(pdf_rows[p] == (dr(p), p % 6, dr_mersenne(p)) for p in EXPONENTS)

roots_m = [dr_mersenne(p) for p in EXPONENTS]
assert (roots_m.count(4), roots_m.count(7), roots_m.count(9), roots_m.count(1), roots_m.count(3)) == (26, 1, 0, 24, 1)
roots_p = [dr(p) for p in EXPONENTS]
assert {d: roots_p.count(d) for d in (1, 4, 7, 2, 5, 8, 3, 6, 9)} == {1: 11, 4: 8, 7: 5, 2: 9, 5: 12, 8: 6, 3: 1, 6: 0, 9: 0}

# baseline and tests
N = 10_000_000
sieve = np.ones(N + 1, dtype=bool)
sieve[:2] = False
for i in range(2, int(N ** 0.5) + 1):
    if sieve[i]:
        sieve[i * i::i] = False
primes = np.nonzero(sieve)[0]
primes = primes[primes >= 5]
shares = [float(np.mean(1 + (primes - 1) % 9 == d)) for d in (1, 2, 4, 5, 7, 8)]
assert all(0.1665 <= s <= 0.1668 for s in shares) and round(float(np.mean(primes % 3 == 1)), 4) == 0.4999
big = [p for p in EXPONENTS if p >= 5]
assert len(big) == 50 and sum(1 for p in big if p % 3 == 1) == 24
assert round(binomtest(24, 50, 0.5).pvalue, 2) == 0.89
obs = [sum(1 for p in big if dr(p) == d) for d in (1, 2, 4, 5, 7, 8)]
assert obs == [11, 8, 8, 12, 5, 6]
x2 = sum((o - 50 / 6) ** 2 / (50 / 6) for o in obs)
assert round(x2, 2) == 4.48 and round(float(chi2.sf(x2, 5)), 2) == 0.48

# mod 37 and mod 999
m37 = [(pow(2, p, 37) - 1) % 37 for p in EXPONENTS]
assert all(r != 0 for r in m37) and sorted(set(m37)) == [1, 3, 4, 7, 12, 14, 16, 17, 18, 19, 21, 23, 31, 34]
assert [m37.count(v) for v in [1, 3, 4, 7, 12, 14, 16, 17, 18, 19, 21, 23, 31, 34]] == [4, 1, 3, 1, 1, 4, 2, 5, 1, 3, 4, 7, 9, 7]
assert len({p % 36 for p in EXPONENTS if p > 3}) == 12
assert [k for k in range(1, 40) if pow(2, k, 999) == 1][0] == 36 and [k for k in range(1, 40) if pow(2, k, 27) == 1][0] == 18
table = {1: 1, 5: 31, 7: 127, 11: 49, 13: 199, 17: 202, 19: 811, 23: 4, 25: 19, 29: 319, 31: 280, 35: 499}
assert all((pow(2, r, 999) - 1) % 999 == v for r, v in table.items())
assert [table[r] % 27 for r in sorted(table)] == [1, 4, 19, 22, 10, 13, 1, 4, 19, 22, 10, 13]
assert [table[r] % 37 for r in sorted(table)] == [1, 31, 16, 12, 14, 17, 34, 4, 19, 23, 21, 18] and len({table[r] % 37 for r in table}) == 12
known = [sum(1 for p in EXPONENTS if p > 3 and p % 36 == r) for r in sorted(table)]
assert known == [4, 9, 2, 1, 4, 5, 7, 3, 3, 7, 4, 1] and sum(known) == 50
M61 = 2 ** 61 - 1
assert f"{M61:,}" == "2,305,843,009,213,693,951" and sum(int(g) for g in f"{M61:,}".split(",")) == 3016 and 3 + 16 == 19 == M61 % 999 and 61 % 36 == 25
assert all((pow(2, p, 3) - 1) % 3 != 0 for p in EXPONENTS if p > 2)

# the owner's April triad on all 52
april = [p for p in EXPONENTS if dr(p) in (4, 7, 9)]
assert april[:4] == [7, 13, 31, 61] and [p for p in EXPONENTS[:12] if dr(p) in (4, 7, 9)] == [7, 13, 31, 61] and len(april) == 13
assert [p for p in april if dr(p) == 4] == [13, 31, 607, 2281, 3217, 4423, 24036583, 74207281]
assert [p for p in april if dr(p) == 7] == [7, 61, 2203, 23209, 30402457]
assert all(dr_mersenne(p) == 1 for p in april)
assert dr(136279841) == 5

if __name__ == "__main__":
    print("Mersenne 7-4-9 PDF: every number right; 'second half of the cycle' wrong (7 is in the first half); the original is in the repo (April, triad on the "
          "exponent's root): 13 of 52 exponents, all giving root 1")
