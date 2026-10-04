# CLASS: AUDIT
"""
Audit of four supplied blocks (2026-10-04): the 81-combination grip engine, the "total tensor
collapse", the 1-X grid for 13/14, and the 1-1..1-9 expansion. The two complete scripts were
run here exactly as written (their seed rule rebuilt below). Mathematics only.

81-COMBINATION ENGINE -- the script's OWN output contradicts the text
  T1 Text: "4 shape groups of 20, 40, 20 and 1". The script finds 8 distinct parity fields,
     of sizes 6, 10, 10, 10, 10, 10, 10, 15. (And the text's own basis fails: pairs of two
     even digits number 4 x 4 = 16, two odd digits 5 x 5 = 25, mixed 40 -- not 20/40/20.)

TOTAL TENSOR COLLAPSE -- the script's OWN output contradicts the text
  T2 Text: total weight 34,992. The script computes 23,328 (root 9).
  T3 Text: "34,992 = 0 mod 5 (6,998 remainder 0)". 34,992 ends in 2: 5 x 6,998 = 34,990,
     remainder 2. The script's real total 23,328 is 3 mod 5, so its own
     `assert master_fives == 0` FAILS -- the script stops with AssertionError.
  T4 Text: roots 3 and 6 have 576 nodes each, root 9 has 1,152; mod-5 tracks flat at
     1,036 / 1,044. The script counts: root 1 = 1,152 (from the many 1 entries), every other
     root 504; mod 5: 0 -> 504, 1 -> 1,656, 2/3/4 -> 1,008 each. Not flat.
  T5 The T432 carry check inside it is correct (Kummer's identity holds for every n).

1-X GRID FOR 13 / 14
  T6 CORRECT: roots 4, 5, 5, 4; gaps +1, +27, -10, -18 summing to 0 -- forced: the gaps of any
     closed loop of numbers sum to 0.
  T7 WRONG: the parity table marks the anchors 4 as Odd (row "4 = 1 3 = 4" is E | O O | E),
     and the prime table marks the anchors 5 as Composite (5 is prime).
  T8 The 1-X stepping script is cut off in the paste and cannot run.

1-1 .. 1-9 EXPANSION -- CORRECT, and forced
  T9 Roots 2, 3, ..., 9, 1; gaps 0, 9, 18, ..., 72: x1 - 1x = 9(x - 1). The reversal keeps the
     digit sum, so `assert root_v1 == root_v4` always holds.

NOT IN THE REPOSITORY: none of t325_all_81_combinations_engine.py, t325_total_tensor_collapse_
  2026_10_03.py, t325_one_x_stepping_engine.py, t325_onex_full_expansion_2026_10_03.py exists on
  all-work (checked 2026-10-04 after fetching origin).
FALSIFICATION: any assertion failing.
"""
import itertools
from collections import Counter

dr = lambda n: 9 if n % 9 == 0 else n % 9
par = lambda n: "e" if n % 2 == 0 else "o"


def seed(d1, d2):                                    # the supplied scripts' seed rule
    r1, r4 = dr(int(f"{d1}{d2}")), dr(int(f"{d2}{d1}"))
    return [[r1, d1, d2, r1], [d1, 1, d1, d1], [d1, d1, 1, d1], [d2, d2, d1, r4]]


def field(s):
    top = [r[::-1] + r for r in s]
    return top + top[::-1]


groups, total, m9, m5 = Counter(), 0, Counter(), Counter()
for d1, d2 in itertools.product(range(1, 10), repeat=2):
    s = seed(d1, d2)
    groups["".join("".join(r) for r in field([[par(x) for x in row] for row in s]))] += 1
    total += 4 * sum(map(sum, s))
    for row in s:
        for v in row:
            m9[dr(v)] += 4
            m5[v % 5] += 4
assert sorted(groups.values()) == [6, 10, 10, 10, 10, 10, 10, 15]                       # T1
assert (4 * 4, 5 * 5, 2 * 4 * 5) == (16, 25, 40)
assert total == 23328 != 34992 and dr(total) == 9                                       # T2
assert 34992 % 5 == 2 and 5 * 6998 == 34990 and total % 5 == 3                          # T3
assert m9[1] == 1152 and all(m9[r] == 504 for r in range(2, 10))                         # T4
assert dict(m5) == {0: 504, 1: 1656, 2: 1008, 3: 1008, 4: 1008}
s = lambda n: sum(map(int, str(n)))
assert all(s(n + 1) == s(n) + 1 - 9 * (len(str(n)) - len(str(n).rstrip("9"))) for n in range(10 ** 5))  # T5

V = [13, 14, 41, 31]
assert [dr(v) for v in V] == [4, 5, 5, 4]                                                # T6
gaps = [V[(i + 1) % 4] - V[i] for i in range(4)]
assert gaps == [1, 27, -10, -18] and sum(gaps) == 0
assert par(4) == "e" and 5 in (2, 3, 5, 7)                                               # T7

assert [dr(int(f"1{x}")) for x in range(1, 10)] == [2, 3, 4, 5, 6, 7, 8, 9, 1]           # T9
assert [int(f"{x}1") - int(f"1{x}") for x in range(1, 10)] == [9 * (x - 1) for x in range(1, 10)]
assert all(dr(int(f"1{x}")) == dr(int(f"{x}1")) for x in range(1, 10))
