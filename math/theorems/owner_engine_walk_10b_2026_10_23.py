# CLASS: COMPUTATION
"""
The owner's walk from 1 to 10,000,000,000 (owner_work #424, 2026-10-23: "run the walk up to ten billion").
tools/owner_walk_segmented.py: the engine's steps (predict from the place in 1 2 3, act with behind + yourself = 2n - 1
and yourself + right = 2n + 1, verify both prime), on the table of odd numbers built one piece at a time.
The full run took 237 seconds; its result is records/owner_walk_1e10.json.

RESULT:
    numbers 10,000,000,000    predicted 3,333,333,334    twin pairs 51,509,099    missed by the prediction 0
    the last pair: n = 9,999,999,885 -> 19,999,999,769 and 19,999,999,771
    3-step n x n / (n x n - 1) ends only at 3 and 9
  both ways: with the pair at n = 2 (3, 5) 51,509,099; without it 51,509,098, every one at place 3.
  per 1,000,000,000 of n: 6388041 5556397 5299971 5139767 5028503 4939468 4870720 4811462 4760465 4714305
  outside check: the walk to 5,000,000,000 gives the twin pairs below 10^10, OEIS A007508: 27,412,679 --
    and every checkpoint below it: 2, 8, 35, 205, 1224, 8169, 58980, 440312, 3424506.

WHAT CI RUNS (every push): the same code to 1,000,000,000, which must give the billion walk's answer
(owner_engine_walk_1b_2026_10_23.py: 6,388,041 pairs, last n = 999,999,936), and the checks on the saved ten-billion
result. The full ten-billion run again: OWNER_WALK_FULL=1 python3 math/theorems/owner_engine_walk_10b_2026_10_23.py

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

A007508 = [2, 8, 35, 205, 1224, 8169, 58980, 440312, 3424506, 27412679]    # twin pairs below 10^1 .. 10^10

# the same code to a billion gives the billion walk
b = S.walk_segmented(10 ** 9)
assert (b["predicted"], b["pairs"], b["missed"], b["last_n"], b["three_ends"]) == (333_333_334, 6_388_041, 0, 999_999_936, [3, 9])
assert list(b["pairs_up_to"].values()) == A007508[:9]

# the saved ten-billion result
w = json.loads((ROOT / "records" / "owner_walk_1e10.json").read_text())
assert w["N"] == 10 ** 10 and w["predicted"] == 10 ** 10 // 3 + 1 == 3_333_333_334
assert (w["pairs"], w["missed"], w["three_ends"]) == (51_509_099, 0, [3, 9])
assert w["last_n"] == 9_999_999_885 and w["last_pair"] == [19_999_999_769, 19_999_999_771]
assert isprime(19_999_999_769) and isprime(19_999_999_771)
assert not any(isprime(2 * n - 1) and isprime(2 * n + 1) for n in range(9_999_999_886, 10 ** 10 + 1))   # truly the last
assert w["per_billion"] == [6388041, 5556397, 5299971, 5139767, 5028503, 4939468, 4870720, 4811462, 4760465, 4714305]
assert sum(w["per_billion"]) == w["pairs"] and w["per_billion"][0] == b["pairs"]
assert list(w["pairs_up_to"].values()) == A007508
smooth = set(S.smooth_25(10 ** 10 + 1))
assert sorted(n for n in (x + 1 for x in smooth) if 2 <= n <= 10 ** 10 and n + 1 in smooth) == [3, 9]

if os.environ.get("OWNER_WALK_FULL") == "1":
    full = S.walk_segmented(10 ** 10)
    assert {k: full[k] for k in full if k != "seconds"} == {k: w[k] for k in w if k != "seconds"}

if __name__ == "__main__":
    print("walk 1 to 10,000,000,000: predicted 3,333,333,334, twin pairs 51,509,099, missed 0, last n = 9,999,999,885; "
          "to 5,000,000,000: 27,412,679 = A007508(10^10)")
