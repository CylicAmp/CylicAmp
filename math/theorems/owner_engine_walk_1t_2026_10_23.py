# CLASS: COMPUTATION
"""
The owner's walk from 1 to 1,000,000,000,000 (owner_work #428, 2026-10-23: "run the walk up to a trillion").
tools/owner_walk_parallel.py: the engine's steps (predict from the place in 1 2 3, act with behind + yourself = 2n - 1
and yourself + right = 2n + 1, verify both prime) on 4 cores at once; it gives the ten-billion walk's answer exactly
(checked before this run). The run took 7764 seconds (2 h 9 min); its result is records/owner_walk_1e12.json.

RESULT:
    numbers 1,000,000,000,000    predicted 333,333,333,334    twin pairs 3,552,770,943    missed by the prediction 0
    the last pair: n = 999,999,999,924 -> 1,999,999,999,847 and 1,999,999,999,849
    3-step n x n / (n x n - 1) ends only at 3 and 9
  both ways: with the pair at n = 2 (3, 5) 3,552,770,943; without it 3,552,770,942, every one at place 3.
  per 100,000,000,000 of n: 424084653 378733065 364099215 355081506 348586781 343500440 339419575 335972379
                            332948977 330344352 (thinning out; the first is the hundred-billion walk)
  outside check: the walk to 500,000,000,000 gives the twin pairs below 10^12, OEIS A007508: 1,870,585,220 -- and every
    checkpoint below it.

WHAT CI RUNS: the checks on the saved result. The full run again (about 2 hours on 4 cores):
OWNER_WALK_FULL=1 python3 math/theorems/owner_engine_walk_1t_2026_10_23.py

FALSIFICATION: any assertion failing.
"""
import json
import os
import pathlib
import sys

from sympy import isprime

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import owner_walk_parallel as P  # noqa: E402

A007508 = [2, 8, 35, 205, 1224, 8169, 58980, 440312, 3424506, 27412679, 224376048, 1870585220]   # below 10^1 .. 10^12

w = json.loads((ROOT / "records" / "owner_walk_1e12.json").read_text())
w11 = json.loads((ROOT / "records" / "owner_walk_1e11.json").read_text())
assert w["N"] == 10 ** 12 and w["predicted"] == 10 ** 12 // 3 + 1 == 333_333_333_334
assert (w["pairs"], w["missed"], w["three_ends"]) == (3_552_770_943, 0, [3, 9])
assert w["last_n"] == 999_999_999_924 and w["last_pair"] == [1_999_999_999_847, 1_999_999_999_849]
assert isprime(1_999_999_999_847) and isprime(1_999_999_999_849)
assert not any(isprime(2 * n - 1) and isprime(2 * n + 1) for n in range(999_999_999_925, 10 ** 12 + 1))
assert len(w["per_billion"]) == 1000 and sum(w["per_billion"]) == w["pairs"]
assert w["per_billion"][:100] == w11["per_billion"]                                # the hundred-billion walk
per_100b = [sum(w["per_billion"][100 * i:100 * (i + 1)]) for i in range(10)]
assert per_100b == [424084653, 378733065, 364099215, 355081506, 348586781, 343500440, 339419575, 335972379,
                    332948977, 330344352]
assert per_100b[0] == w11["pairs"] and all(per_100b[i] > per_100b[i + 1] for i in range(9))
assert list(w["pairs_up_to"].values()) == A007508
smooth = set(P.smooth_25(10 ** 12 + 1))
assert sorted(n for n in (x + 1 for x in smooth) if 2 <= n <= 10 ** 12 and n + 1 in smooth) == [3, 9]

# the parallel code itself, on a range CI can afford: it must give the ten-billion walk's counts to a billion
small = P.walk_parallel(10 ** 9, workers=2)
w10 = json.loads((ROOT / "records" / "owner_walk_1e10.json").read_text())
assert small["pairs"] == w10["per_billion"][0] == 6_388_041 and small["missed"] == 0 and small["last_n"] == 999_999_936

if os.environ.get("OWNER_WALK_FULL") == "1":
    full = P.walk_parallel(10 ** 12)
    assert {k: full[k] for k in full if k not in ("seconds", "workers")} == \
        {k: w[k] for k in w if k not in ("seconds", "workers")}

if __name__ == "__main__":
    print("walk 1 to 1,000,000,000,000: predicted 333,333,333,334, twin pairs 3,552,770,943, missed 0, "
          "last n = 999,999,999,924; to 500,000,000,000: 1,870,585,220 = A007508(10^12)")
