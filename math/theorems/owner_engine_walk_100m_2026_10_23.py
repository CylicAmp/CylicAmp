# CLASS: COMPUTATION
"""
The owner's walk from 1 to 100,000,000 (owner_work #422, 2026-10-23: "run the walk up to a hundred million").
The walk of tools/owner_engine.py -- at each n, predict from n's place in 1 2 3 (place 3, or n = 2), act with the
neighbours (behind + yourself = 2n - 1, yourself + right = 2n + 1), verify that both are prime -- done here with
numpy in blocks of 10,000,000 so the table of primes up to 200,000,001 fits in memory. The same steps as the engine;
checked against the engine's own walk to 1,000,000 below.

RESULT:
    numbers 100,000,000    predicted 33,333,334    twin pairs 813,371    missed by the prediction 0
    the last pair: n = 99,999,951 -> 199,999,901 and 199,999,903
    3-step n x n / (n x n - 1) ends only at 3 and 9
  both ways: with the pair at n = 2 (3, 5) 813,371; without it 813,370, every one at place 3.
  per 10,000,000 of n: 107407 89346 83805 80892 78862 77048 75814 74355 73156 72686 (thinning out)
  outside check: the walk to 50,000,000 gives the twin pairs below 10^8, OEIS A007508: 440,312.

FALSIFICATION: any assertion failing.
"""
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
import owner_engine as E  # noqa: E402

N = 100_000_000
BLOCK = 10_000_000


def sieve(limit):
    prime = np.ones(limit + 1, dtype=bool)
    prime[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if prime[i]:
            prime[i * i::i] = False
    return prime


POW5 = np.array([5 ** k for k in range(0, 24)], dtype=np.int64)       # 5^23 > 10^16


def walk_np(a, b, prime):
    hits, predicted, missed, three_ends = [], 0, 0, []
    for s in range(a, b + 1, BLOCK):
        n = np.arange(s, min(s + BLOCK, b + 1), dtype=np.int64)
        guess = (n == 2) | ((n > 2) & (n % 3 == 0))
        hit = prime[2 * n - 1] & prime[2 * n + 1]
        predicted += int(guess.sum())
        missed += int((hit & ~guess).sum())
        hits.append(n[hit])
        m = n[n >= 2]
        q = m * m - 1                                   # n x n - 1, below 10^16
        q = q // (q & -q)                               # take out every 2
        three_ends += m[np.isin(q, POW5)].tolist()      # what is left must be a power of 5
    return np.concatenate(hits), predicted, missed, three_ends


prime = sieve(2 * N + 1)

# the same steps as the engine: compare on 1 .. 1,000,000
small = E.walk(1, 1_000_000)
h, p, mi, te = walk_np(1, 1_000_000, prime)
assert h.tolist() == [x[0] for x in small["pairs"]] and p == small["predicted"] and mi == 0 and te == small["three_ends"]

pairs, predicted, missed, three_ends = walk_np(1, N, prime)
last = int(pairs[-1])
per_10m = [int(((pairs > (k - 1) * 10 ** 7) & (pairs <= k * 10 ** 7)).sum()) for k in range(1, 11)]

assert predicted == 33_333_334 and missed == 0 and three_ends == [3, 9]
assert len(pairs) == 813_371 and int((pairs == 2).sum()) == 1 and int((pairs % 3 == 0).sum()) == 813_370
assert (last, 2 * last - 1, 2 * last + 1) == (99_999_951, 199_999_901, 199_999_903)
assert E.is_prime(2 * last - 1) and E.is_prime(2 * last + 1)
assert per_10m == [107407, 89346, 83805, 80892, 78862, 77048, 75814, 74355, 73156, 72686] and sum(per_10m) == len(pairs)
assert int((pairs <= 5_000_000).sum()) == 58_980 and int((pairs <= 50_000_000).sum()) == 440_312   # OEIS A007508

if __name__ == "__main__":
    print("walk 1 to 100,000,000: predicted %d, twin pairs %d, missed %d, last n = %d (%d, %d), 3-step ends %s"
          % (predicted, len(pairs), missed, last, 2 * last - 1, 2 * last + 1, three_ends))
    print("per 10,000,000 of n:", per_10m)
