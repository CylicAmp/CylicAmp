# CLASS: AUDIT
"""
Audit of supplied text and script (2026-10-04): "compute_true_4d_shapes" -- digit paths
through all 24^4 = 331,776 four-row stacks of permutations of 1..4. Mathematics only.

CORRECT
  P1 1,536 uniform and 330,240 broken stacks (also in
     stack_count_digital_roots_supplied_audit_2026_10_03.py).
  P2 256 = 4^4 distinct digit paths occur among the broken stacks.

WRONG
  P3 "Top 5 most common paths" / "dominant trajectories: the zero-shift lock (0,0,0,0) and
     the direct pivot (0,1,0,1)". There is no dominant path. Every one of the 256 paths
     occurs EXACTLY 5,160 times in the broken stacks (and exactly 24 times in the uniform
     ones). Forced: each row puts a given digit in each of the 4 columns for 6 of its 24
     permutations, independently row by row, so over all stacks every path has the same
     count 4 * 24^4 / 256 = 5,184; the uniform stacks take 4 * 1,536 / 256 = 24 of each.
     A "top 5" of a 256-way tie is just the first five in iteration order.

NOT IN THE REPOSITORY
  P4 The text says the script was "computed, tested, and locked into branch all-work".
     No file named compute_true_4d_shapes_2026_10_03.py exists on all-work (checked
     2026-10-04 after fetching origin).
FALSIFICATION: any assertion failing.
"""
import collections
import itertools

P = list(itertools.permutations((1, 2, 3, 4)))
broken, unif = collections.Counter(), collections.Counter()
nu = nb = 0
for st in itertools.product(P, repeat=4):
    rots = {st[0][k:] + st[0][:k] for k in range(4)}
    u = all(r in rots for r in st)
    nu += u
    nb += not u
    for d in (1, 2, 3, 4):
        (unif if u else broken)[tuple(r.index(d) for r in st)] += 1

assert (nu, nb) == (1536, 330240)                                       # P1
assert len(broken) == 256 == 4 ** 4                                      # P2
assert set(broken.values()) == {5160} and set(unif.values()) == {24}     # P3
assert 4 * 24 ** 4 // 256 == 5184 == 5160 + 24 and 4 * 1536 // 256 == 24
assert broken[(0, 0, 0, 0)] == broken[(0, 1, 0, 1)] == broken[(3, 2, 1, 0)] == 5160

if __name__ == "__main__":
    print("all 256 paths occur exactly", broken[(0, 0, 0, 0)], "times in the broken stacks")
