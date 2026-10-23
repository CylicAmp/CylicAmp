# CLASS: COMPUTATION
"""
The owner's walk from 1 to 10,000,000 (owner_work #421, 2026-10-23: "run the walk up to ten million").
The walk is tools/owner_engine.py: at each n, predict from n's place in 1 2 3 (place 3, or n = 2), act with the
neighbours -- behind + yourself = 2n - 1, yourself + right = 2n + 1 -- and verify that both are prime.

RESULT:
    numbers 10,000,000    predicted 3,333,334    twin pairs 107,407    missed by the prediction 0
    the last pair: n = 9,999,774 -> 19,999,547 and 19,999,549
    3-step n x n / (n x n - 1) ends only at 3 and 9
  both ways: with the pair at n = 2 (3, 5) 107,407; without it 107,406, every one at place 3.
  per million of n:  14871  11989  11056  10702  10362  10031  9773  9750  9572  9301  (thinning out)
  outside check: the walk to 5,000,000 gives 58,980 = the twin pairs below 10^7 in OEIS A007508 (fetched 2026-10-22).

FALSIFICATION: any assertion failing.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
import owner_engine as E  # noqa: E402

w = E.walk(1, 10_000_000)
pairs = w["pairs"]
assert (w["numbers"], w["predicted"], w["verified"], w["missed"]) == (10_000_000, 3_333_334, 107_407, [])
assert pairs[-1] == (9_999_774, 19_999_547, 19_999_549) and w["three_ends"] == [3, 9]
assert sum(1 for p in pairs if p[0] == 2) == 1 and sum(1 for p in pairs if p[0] % 3 == 0) == 107_406
per_million = [sum(1 for p in pairs if (k - 1) * 10 ** 6 < p[0] <= k * 10 ** 6) for k in range(1, 11)]
assert per_million == [14871, 11989, 11056, 10702, 10362, 10031, 9773, 9750, 9572, 9301] and sum(per_million) == 107_407
assert sum(1 for p in pairs if p[0] <= 5_000_000) == 58_980          # OEIS A007508, 10^7
assert all(E.is_prime(lo) and E.is_prime(hi) for _, lo, hi in pairs[-50:])

if __name__ == "__main__":
    print("walk 1 to 10,000,000: predicted 3,333,334, twin pairs 107,407, missed 0; to 5,000,000: 58,980 = A007508(10^7)")
