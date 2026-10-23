# CLASS: COMPUTATION
"""
The owner's walk from 1 to 100,000,000,000 (owner_work #425, 2026-10-23: "run the walk up to a hundred billion").
tools/owner_walk_segmented.py in pieces of 100,000,000 odd numbers; the full run took 2628 seconds (44 minutes);
its result is records/owner_walk_1e11.json.

RESULT:
    numbers 100,000,000,000    predicted 33,333,333,334    twin pairs 424,084,653    missed by the prediction 0
    the last pair: n = 99,999,999,945 -> 199,999,999,889 and 199,999,999,891
    3-step n x n / (n x n - 1) ends only at 3 and 9
  both ways: with the pair at n = 2 (3, 5) 424,084,653; without it 424,084,652, every one at place 3.
  per 10,000,000,000 of n: 51509099 45447608 43537690 42361516 41520135 40861939 40322433 39879721 39489346 39155166
  outside check: the walk to 50,000,000,000 gives the twin pairs below 10^11, OEIS A007508: 224,376,048 -- and every
    checkpoint below it.

WHAT CI RUNS: the checks on the saved result (owner_engine_walk_10b_2026_10_23.py re-runs the code to a billion).
The full run again: OWNER_WALK_FULL=1 python3 math/theorems/owner_engine_walk_100b_2026_10_23.py

FALSIFICATION: any assertion failing.
"""
import json
import os
import pathlib
import sys

from sympy import isprime

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import owner_walk_segmented as S  # noqa: E402

A007508 = [2, 8, 35, 205, 1224, 8169, 58980, 440312, 3424506, 27412679, 224376048]   # below 10^1 .. 10^11

w = json.loads((ROOT / "records" / "owner_walk_1e11.json").read_text())
w10 = json.loads((ROOT / "records" / "owner_walk_1e10.json").read_text())
assert w["N"] == 10 ** 11 and w["predicted"] == 10 ** 11 // 3 + 1 == 33_333_333_334
assert (w["pairs"], w["missed"], w["three_ends"]) == (424_084_653, 0, [3, 9])
assert w["last_n"] == 99_999_999_945 and w["last_pair"] == [199_999_999_889, 199_999_999_891]
assert isprime(199_999_999_889) and isprime(199_999_999_891)
assert not any(isprime(2 * n - 1) and isprime(2 * n + 1) for n in range(99_999_999_946, 10 ** 11 + 1))
assert len(w["per_billion"]) == 100 and sum(w["per_billion"]) == w["pairs"]
assert w["per_billion"][:10] == w10["per_billion"]                                  # the ten-billion walk
per_10b = [sum(w["per_billion"][10 * i:10 * (i + 1)]) for i in range(10)]
assert per_10b == [51509099, 45447608, 43537690, 42361516, 41520135, 40861939, 40322433, 39879721, 39489346, 39155166]
assert per_10b[0] == w10["pairs"] and all(per_10b[i] > per_10b[i + 1] for i in range(9))
assert list(w["pairs_up_to"].values()) == A007508
smooth = set(S.smooth_25(10 ** 11 + 1))
assert sorted(n for n in (x + 1 for x in smooth) if 2 <= n <= 10 ** 11 and n + 1 in smooth) == [3, 9]

if os.environ.get("OWNER_WALK_FULL") == "1":
    full = S.walk_segmented(10 ** 11, piece=100_000_000)
    assert {k: full[k] for k in full if k != "seconds"} == {k: w[k] for k in w if k != "seconds"}

if __name__ == "__main__":
    print("walk 1 to 100,000,000,000: predicted 33,333,333,334, twin pairs 424,084,653, missed 0, last n = 99,999,999,945; "
          "to 50,000,000,000: 224,376,048 = A007508(10^11)")
