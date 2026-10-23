# CLASS: COMPUTATION
"""
The owner's walk from 1 to 1,000,000,000 (owner_work #423, 2026-10-23: "run the walk up to a billion").
tools/owner_walk_big.py: the engine's steps (predict from the place in 1 2 3, act with behind + yourself = 2n - 1
and yourself + right = 2n + 1, verify both prime) on one table "is 2k + 1 prime" for k = 0 .. 10^9, where 2n - 1
is entry n - 1 and 2n + 1 is entry n. Checked against the engine's own walk to 1,000,000 and against the walk to
100,000,000 (owner_engine_walk_100m_2026_10_23.py). About a minute and 1.5 GB.

RESULT:
    numbers 1,000,000,000    predicted 333,333,334    twin pairs 6,388,041    missed by the prediction 0
    the last pair: n = 999,999,936 -> 1,999,999,871 and 1,999,999,873
    3-step n x n / (n x n - 1) ends only at 3 and 9
  both ways: with the pair at n = 2 (3, 5) 6,388,041; without it 6,388,040, every one at place 3.
  per 100,000,000 of n: 813371 694362 658568 636450 621755 609332 598861 591283 584603 579456 (thinning out)
  outside check: the walk to 500,000,000 gives the twin pairs below 10^9, OEIS A007508: 3,424,506.

FALSIFICATION: any assertion failing.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
import owner_engine as E  # noqa: E402
import owner_walk_big as B  # noqa: E402

small = B.walk_big(1_000_000, block=250_000)
ref = E.walk(1, 1_000_000)
assert small["pairs"].tolist() == [x[0] for x in ref["pairs"]] and small["predicted"] == ref["predicted"]
assert small["missed"] == 0 and small["three_ends"] == ref["three_ends"]

w = B.walk_big(10 ** 9, block=10_000_000)
p = w["pairs"]
last = int(p[-1])
assert (w["predicted"], len(p), w["missed"], w["three_ends"]) == (333_333_334, 6_388_041, 0, [3, 9])
assert (last, 2 * last - 1, 2 * last + 1) == (999_999_936, 1_999_999_871, 1_999_999_873)
assert E.is_prime(2 * last - 1) and E.is_prime(2 * last + 1)
assert int((p == 2).sum()) == 1 and int((p % 3 == 0).sum()) == 6_388_040
per = [int(((p > (k - 1) * 10 ** 8) & (p <= k * 10 ** 8)).sum()) for k in range(1, 11)]
assert per == [813371, 694362, 658568, 636450, 621755, 609332, 598861, 591283, 584603, 579456] and sum(per) == len(p)
assert per[0] == 813_371                                            # the walk to 100,000,000
assert int((p <= 500_000_000).sum()) == 3_424_506                   # OEIS A007508, 10^9
assert int((p <= 50_000_000).sum()) == 440_312 and int((p <= 5_000_000).sum()) == 58_980

if __name__ == "__main__":
    print("walk 1 to 1,000,000,000: predicted 333,333,334, twin pairs 6,388,041, missed 0, last n = 999,999,936; "
          "to 500,000,000: 3,424,506 = A007508(10^9)")
