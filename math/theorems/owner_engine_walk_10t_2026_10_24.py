# CLASS: COMPUTATION
"""
The owner's walk from 1 to 10,000,000,000,000 (owner_work #433, 2026-10-24: "run the walk up to ten trillion").
tools/owner_walk_fast.c: the engine's steps (predict from the place in 1 2 3, act with behind + yourself = 2n - 1
and yourself + right = 2n + 1, verify both prime) on the same table of odd numbers as tools/owner_walk_parallel.py,
written in C. Before the run it gave the hundred-billion walk's answer exactly (all 100 per-billion counts, 52 s).
The run took 7849 seconds (2 h 11 min) on 4 cores; its result is records/owner_walk_1e13.json.

RESULT:
    numbers 10,000,000,000,000    predicted 3,333,333,333,334    twin pairs 30,198,862,775    missed 0
    the last pair: n = 9,999,999,999,915 -> 19,999,999,999,829 and 19,999,999,999,831
    3-step n x n / (n x n - 1) ends only at 3 and 9
  both ways: with the pair at n = 2 (3, 5) 30,198,862,775; without it 30,198,862,774, every one at place 3.
  per 1,000,000,000,000 of n: 3552770943 3204061133 3090010408 3019414386 2968408002 2928728773 2896334922
                              2868970033 2845427949 2824736226 (thinning out; the first is the trillion walk)
  outside check: the walk to 5,000,000,000,000 gives the twin pairs below 10^13, OEIS A007508: 15,834,664,872 -- and
    every checkpoint below it.

WHAT CI RUNS (every push): the checks on the saved result, and the C program compiled and run to 10^10, where it must
give the ten-billion walk (records/owner_walk_1e10.json) number for number. The full run again:
    gcc -O3 -march=native -fopenmp -o owner_walk_fast tools/owner_walk_fast.c -lm && ./owner_walk_fast 10000000000000 4

FALSIFICATION: any assertion failing.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

from sympy import isprime

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import owner_walk_parallel as P  # noqa: E402

A007508 = [2, 8, 35, 205, 1224, 8169, 58980, 440312, 3424506, 27412679, 224376048, 1870585220, 15834664872]

w = json.loads((ROOT / "records" / "owner_walk_1e13.json").read_text())
w12 = json.loads((ROOT / "records" / "owner_walk_1e12.json").read_text())
assert w["N"] == 10 ** 13 and w["predicted"] == 10 ** 13 // 3 + 1 == 3_333_333_333_334
assert (w["pairs"], w["missed"], w["three_ends"]) == (30_198_862_775, 0, [3, 9])
assert w["last_n"] == 9_999_999_999_915 and w["last_pair"] == [19_999_999_999_829, 19_999_999_999_831]
assert isprime(19_999_999_999_829) and isprime(19_999_999_999_831)
assert not any(isprime(2 * n - 1) and isprime(2 * n + 1) for n in range(9_999_999_999_916, 10 ** 13 + 1))
assert len(w["per_billion"]) == 10_000 and sum(w["per_billion"]) == w["pairs"]
assert w["per_billion"][:1000] == w12["per_billion"]                               # the trillion walk
per_t = [sum(w["per_billion"][1000 * i:1000 * (i + 1)]) for i in range(10)]
assert per_t == [3552770943, 3204061133, 3090010408, 3019414386, 2968408002, 2928728773, 2896334922,
                 2868970033, 2845427949, 2824736226]
assert per_t[0] == w12["pairs"] and all(per_t[i] > per_t[i + 1] for i in range(9))
assert list(w["pairs_up_to"].values()) == A007508
smooth = set(P.smooth_25(10 ** 13 + 1))
assert sorted(n for n in (x + 1 for x in smooth) if 2 <= n <= 10 ** 13 and n + 1 in smooth) == [3, 9]

# the C program itself, to 10^10, against the ten-billion walk
gcc = shutil.which("gcc")
if gcc:
    with tempfile.TemporaryDirectory() as d:
        exe = pathlib.Path(d) / "owner_walk_fast"
        subprocess.run([gcc, "-O3", "-fopenmp", "-o", str(exe), str(ROOT / "tools" / "owner_walk_fast.c"), "-lm"], check=True)
        out = json.loads(subprocess.run([str(exe), str(10 ** 10)], check=True, capture_output=True, text=True).stdout)
    w10 = json.loads((ROOT / "records" / "owner_walk_1e10.json").read_text())
    assert (out["pairs"], out["missed"], out["last_n"]) == (w10["pairs"], w10["missed"], w10["last_n"])
    assert out["per_billion"] == w10["per_billion"] and out["pairs_up_to"] == w10["pairs_up_to"]
else:
    print("gcc not found: the C program was not re-run here (the saved result is still checked)")

if __name__ == "__main__":
    print("walk 1 to 10,000,000,000,000: predicted 3,333,333,333,334, twin pairs 30,198,862,775, missed 0, "
          "last n = 9,999,999,999,915; to 5,000,000,000,000: 15,834,664,872 = A007508(10^13)")
