# CLASS: COMPUTATION
"""
The race of the owner's three twin chains to 1,000,000,000,000, and 29.53 (owner_work #443, 2026-10-26:
"run the twin chain race to a trillion / 29.53"). tools/owner_race_fast.c: the owner's walk (same table, same pair
test) with each pair put in its chain by the root of n -- 3 -> (5, 7), 6 -> (2, 4), 9 -> (8, 1) -- and the lead (the
chain with the most pairs so far) followed pair by pair. It gives the billion-scale race of
owner_walk_twin_chain_race_2026_10_25.py exactly; its count at 10^10 was redone with the numpy walk and agrees.
Run: 1162 seconds on 4 cores; result records/owner_race_1e12.json.

RESULT:
    n up to        root 3 (5,7)     root 6 (2,4)     root 9 (8,1)     apart
    10^6                4979             4978             4913           66
    10^7               35876            35811            35719          157
    10^8              271509           271038           270823          686
    10^9             2131202          2127929          2128909         3273
    10^10           17172821         17167372         17168905         5449
    10^11          141364133        141359928        141360591         4205
    10^12         1184255027       1184257144       1184258771         3744
  the lead changed 69,231 times; the (5, 7) lead of the billion did not hold: at a trillion (8, 1) leads, and the last
  change was at n = 970,015,695,444.
  the chains stay close: 3,744 apart at 1.18 billion each. If each pair picked its chain by a coin of three sides,
  the counts would sit about 28,000 apart (the square root of 2/3 of the count). And it is not that the next pair
  avoids its chain: to 10^9 the next pair is in the same chain 31.3% of the time, against 33.3% for the coin.
  So the counts are held together more tightly than chance -- the kind of thing the counts of primes in classes are
  known to do (their differences follow the zeros of L-functions; Rubinstein and Sarnak, "Chebyshev's bias", 1994),
  shown here for twin pairs in the owner's chains. Not found published in this form (searched 2026-10-25).
  the middle 2n by 37: 35 remainders (1 and 36 cannot happen), from 101,484,549 (at 24) to 101,523,192 (at 20) --
  38,643 apart, about what the coin gives (4 times the square root of 101.5 million).

29.53 (owner's number, no line with it): digits 2 9 5 3 -> 19 -> 10 -> 1; 2953 is prime -> 30 C3 (cousin with 2957);
  29 and 53 are both prime -- 29 C9, a twin with 31, Sophie Germain (59); 53 SA_ST_A, Sophie Germain (107).

FALSIFICATION: any assertion failing.
"""
import json
import pathlib

from sympy import isprime

ROOT = pathlib.Path(__file__).resolve().parents[2]
r = json.loads((ROOT / "records" / "owner_race_1e12.json").read_text())
w = json.loads((ROOT / "records" / "owner_walk_1e12.json").read_text())

table = {10 ** 6: [4979, 4978, 4913], 10 ** 7: [35876, 35811, 35719], 10 ** 8: [271509, 271038, 270823],
         10 ** 9: [2131202, 2127929, 2128909], 10 ** 10: [17172821, 17167372, 17168905],
         10 ** 11: [141364133, 141359928, 141360591], 10 ** 12: [1184255027, 1184257144, 1184258771]}
assert {int(k): v for k, v in r["checkpoints"].items()} == table
assert [max(v) - min(v) for v in table.values()] == [66, 157, 686, 3273, 5449, 4205, 3744]
assert r["chains"] == {"root3": 1184255027, "root6": 1184257144, "root9": 1184258771}
assert sum(r["chains"].values()) + r["pair_at_2"] == w["pairs"] == 3_552_770_943
assert all(sum(b) == x - (1 if i == 0 else 0) for i, (b, x) in enumerate(zip(r["per_billion"], w["per_billion"])))
assert (r["lead_changes"], r["last_change_n"], r["final_lead"]) == (69231, 970015695444, "root9 (8,1)")
assert round((r["chains"]["root3"] * 2 / 3) ** 0.5) == 28098
c37 = r["middle_by_37"]
assert c37[1] == 0 and c37[36] == 0 and sum(1 for x in c37 if x) == 35 and sum(c37) == 3_552_770_942
nz = [x for x in c37 if x]
assert (min(nz), max(nz), c37.index(min(nz)), c37.index(max(nz))) == (101484549, 101523192, 24, 20)

# 29.53
assert sum(map(int, "2953")) == 19 and isprime(2953) and isprime(2957) and 2953 % 37 == 30
assert isprime(29) and isprime(31) and isprime(59) and isprime(53) and isprime(107) and (29 % 37, 53 % 37) == (29, 16)

if __name__ == "__main__":
    print("race to 10^12: (5,7) 1,184,255,027  (2,4) 1,184,257,144  (8,1) 1,184,258,771; 69,231 lead changes, last at "
          "n = 970,015,695,444; 3,744 apart where a coin gives about 28,000")
