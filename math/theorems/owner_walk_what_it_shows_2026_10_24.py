# CLASS: AUDIT
"""
What the long walks showed, and what they could not (owner_work #436, 2026-10-24: "Well, what did going to 10 trillion
achieve? Or a trillion?").

1. "MISSED BY THE PREDICTION: 0" COULD NOT HAVE COME OUT ANY OTHER WAY. It is proved for every n:
   if n > 2 is not at place 3 of 1 2 3 (n is not a multiple of 3), then 2n is not a multiple of 3 either, so one of
   2n - 1, 2n + 1 is (of three numbers in a row, 2n - 1, 2n, 2n + 1, one is a multiple of 3), and it is bigger than 3,
   so it is not prime. Every walk -- to a million or to ten trillion -- had to report 0. (The light from above of
   pasted_shadows_critical_experiment_audit_2026_10_23.py: a check every candidate passes.)

2. THE TWIN COUNTS ARE ALREADY PUBLISHED, much further. OEIS A007508 (twin pairs below 10^n, fetched 2026-10-24) lists
   them to 10^19: ... 15834664872 (10^13), 135780321665 (10^14), ..., 7237518093734545 (10^19). The walks' counts at
   every power of 10 up to 10^13 equal those -- which shows the walk code is right, and adds no new count.

3. WHAT THE WALKS DID PRODUCE: a checked, fast form of the owner's walk (tools/owner_walk_fast.c: 10^11 in 52 s,
   10^13 in 2 h 11 min), agreeing with the published counts at 13 checkpoints and with the numpy walks block by block;
   and the per-billion counts to 10^13 (records/owner_walk_1e13.json, 10,000 blocks).

4. A WALK THAT COULD TELL SOMETHING has to ask a question whose answer is not forced -- one that could come out either
   way. The walk to a hundred trillion would be the same check again (it is not run).

FALSIFICATION: any assertion failing.
"""
import json
import pathlib

from sympy import isprime

ROOT = pathlib.Path(__file__).resolve().parents[2]

# 1. the proof, and the check that it is what the walk reports
for n in range(3, 200_000):
    if n % 3:
        lo, hi = 2 * n - 1, 2 * n + 1
        assert (lo % 3 == 0 and lo > 3) or (hi % 3 == 0 and hi > 3)
        assert not (isprime(lo) and isprime(hi))
for name in ("owner_walk_1e10.json", "owner_walk_1e11.json", "owner_walk_1e12.json", "owner_walk_1e13.json"):
    assert json.loads((ROOT / "records" / name).read_text())["missed"] == 0

# 2. the published counts, and the walks' match
A007508 = [2, 8, 35, 205, 1224, 8169, 58980, 440312, 3424506, 27412679, 224376048, 1870585220, 15834664872,
           135780321665, 1177209242304, 10304195697298, 90948839353159, 808675888577436, 7237518093734545]
w13 = json.loads((ROOT / "records" / "owner_walk_1e13.json").read_text())
assert list(w13["pairs_up_to"].values()) == A007508[:13]
assert len(A007508) - 13 == 6                      # published six powers of 10 past the longest walk

# 3. the per-billion table
assert len(w13["per_billion"]) == 10_000 and sum(w13["per_billion"]) == w13["pairs"] == 30_198_862_775

if __name__ == "__main__":
    print("missed = 0 is proved for every n (one of 2n-1, 2n+1 is a multiple of 3 when n is not); the twin counts "
          "match OEIS A007508, which is published to 10^19; the walks checked the code, not the mathematics")
