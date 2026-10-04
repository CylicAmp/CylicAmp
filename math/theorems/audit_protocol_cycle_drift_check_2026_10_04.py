# CLASS: AUDIT
"""
Checks the mathematical claims inside the owner's Mathematical Audit Protocol (2026-10-04),
filed at .claude/skills/audit-supplied/PROTOCOL.md.

P1 CORRECT: the 2-digit cycle 12 23 34 45 56 67 78 89 91 has 9 distinct nodes and 9 edges; eight
   steps of -1 and one wrap of +8 give drift 0; appending 12 again adds a spurious -1.
P2 CORRECT, with the scope made exact: "for any permutation cycle of base-10 coordinates mapped
   Z9 -> Z9, the drift sums to 0". It holds when each node is (x, sigma(x)) and x runs over one
   cycle of a permutation sigma of the digits 1..9 -- then the left and right columns contain the
   same digits, so their sums agree. Checked for every permutation of 1..9 (362,880) and all of
   their cycles. It FAILS for a cycle of nodes whose right digits are not a rearrangement of the
   left ones -- e.g. the 26-node wave (left sum 128, right 129; wave26_gram audit), so the
   condition matters.
FALSIFICATION: any assertion failing.
"""
import itertools

cyc = [12, 23, 34, 45, 56, 67, 78, 89, 91]
d = [x // 10 - x % 10 for x in cyc]
assert len(set(cyc)) == 9 and d == [-1] * 8 + [8] and sum(d) == 0                       # P1
assert sum(d) + (1 - 2) == -1
for perm in itertools.permutations(range(1, 10)):                                        # P2
    sigma = dict(zip(range(1, 10), perm))
    seen = set()
    for start in range(1, 10):
        if start in seen:
            continue
        x, nodes = start, []
        while x not in seen:
            seen.add(x)
            nodes.append((x, sigma[x]))
            x = sigma[x]
        assert sum(a - b for a, b in nodes) == 0
wave = [77, 78, 87, 88, 89, 98, 99, 91, 19, 11, 12, 21, 22, 23, 32, 33, 34, 43, 44, 45, 54, 55, 56, 65, 66, 67]
assert sum(x // 10 - x % 10 for x in wave) == -1
