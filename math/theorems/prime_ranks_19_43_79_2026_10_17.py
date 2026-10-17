# CLASS: AUDIT
"""
Prime ranks of 19, 43, 79 (owner_work #316, 2026-10-17). Pasted text (another tool's, relayed by the owner with no words of their own):
    "Independent arithmetic verification: The calculation is exact. It also ties directly back into the prime rank sequence:
     8 (Rank of prime 19), 14 (Rank of prime 43), 22 (Rank of prime 79). The prime index of the middle term plus the first term gives
     the index of the third term (p_8 + p_14 -> 8 + 14 = 22 = index of 79), while simultaneously maintaining the constant step of 6
     (8 +6 14 +6 22)."
The numbers are the owner's 43|19|79 of #302-#303 (math/theorems/roots_43_19_79_2026_10_16.py).

FAULT: "the constant step of 6" is wrong. 8 -> 14 is +6 but 14 -> 22 is +8; 14 + 6 = 20, not 22. The two claims of the paste cannot both hold:
  8 + 14 = 22 means the steps are 6 then 8.
  Also p_8 + p_14 = 19 + 43 = 62, not 79: the relation is between the ranks (8 + 14 = 22), not between the primes.
  "The calculation is exact" does not say which calculation; that is not defined in the paste.

HOLDS: the ranks. 19 is the 8th prime, 43 the 14th, 79 the 22nd. In the owner's order 43|19|79 the ranks are 14, 8, 22, and 8 + 14 = 22:
  rank(19) + rank(43) = rank(79). The primes themselves step by 24 (19 -> 43) and 36 (43 -> 79).

HOW COMMON IS rank_i + rank_j = rank_k? Not forced and not rare. Among all triples of primes below 100 (25 primes, 2300 triples) 144 satisfy it,
  6.3 percent; below 1000, 0.9 percent. This triple was not chosen by a rule that predicts the relation, so it is recorded, not claimed.

FRAMEWORKS (gf37-audit): 8 TESLA; 14 C9; 22 NQR17; 62 = 19 + 43 -> 25 SA_ST_B.

FALSIFICATION: any assertion failing.
"""
from itertools import combinations
from sympy import prime, primepi

assert [int(primepi(p)) for p in (19, 43, 79)] == [8, 14, 22] and [prime(i) for i in (8, 14, 22)] == [19, 43, 79]
assert 14 - 8 == 6 and 22 - 14 == 8 and 22 - 14 != 6 and 14 + 6 == 20 != 22                    # the "constant step of 6" is wrong
assert 8 + 14 == 22 and prime(8) + prime(14) == 62 != 79                                           # the relation is between ranks
assert 43 - 19 == 24 and 79 - 43 == 36
assert [int(primepi(p)) for p in (43, 19, 79)] == [14, 8, 22]                                      # the owner's order 43|19|79
assert [n % 37 for n in (8, 14, 22, 62)] == [8, 14, 22, 25]


def share(limit):
    n = int(primepi(limit))
    hits = sum(1 for i, j in combinations(range(1, n + 1), 2) if i + j <= n)
    return hits, n * (n - 1) * (n - 2) // 6


assert share(100) == (144, 2300) and share(1000) == (6972, 776216)

if __name__ == "__main__":
    print("ranks 8, 14, 22: 8 + 14 = 22 holds; steps are 6 then 8, not a constant 6; 6.3 percent of triples of primes below 100 have this property")
