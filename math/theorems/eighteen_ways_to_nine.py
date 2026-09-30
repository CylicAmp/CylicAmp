# CLASS: IDENTITY
"""
"18 ways to add up 9" (2026-09-30): of the usual ways to count sums equal to 9,
exactly one gives 18 -- partitions of 9 into parts no bigger than 4, which by
conjugation equals partitions of 9 into at most 4 parts. All 30 partitions of 9
exist; these are the 18 with every part <= 4.

Other counts (none is 18): all partitions 30, exactly 3 parts 7, distinct parts 8,
odd parts 8, ordered sums 256, ordered positive pairs 8, digit pairs a+b = 9: 10.

THE OWNER'S COUNT (2026-09-30): 9 ways, one per starting digit a = 1..9 with
partner b = 9 - a: 1+8, 2+7, 3+6, 4+5, 5+4, 6+3, 7+2, 8+1, 9+0. Each digit has
exactly one partner reaching 9; the ninth pair is 9+0, and under the collapse
0 and 9 are the same class, so 9 pairs with itself. Reversal pairs the other
eight into four swaps (1+8 <-> 8+1, ...): 4 * 2 + 1 = 9. Counting 0+9 as well
gives 10.

FALSIFICATION: any assertion failing.
"""


def partitions(n, largest):
    if n == 0:
        return [[]]
    return [[k] + rest for k in range(min(n, largest), 0, -1) for rest in partitions(n - k, k)]


ALL = partitions(9, 9)
SMALL = partitions(9, 4)
assert len(ALL) == 30 and len(SMALL) == 18
assert len([p for p in ALL if len(p) <= 4]) == 18                 # conjugate count agrees
assert len([p for p in ALL if len(p) == 3]) == 7
assert len([p for p in ALL if len(set(p)) == len(p)]) == 8
assert len([p for p in ALL if all(k % 2 for k in p)]) == 8

PAIRS = [(a, 9 - a) for a in range(1, 10)]
assert len(PAIRS) == 9 and PAIRS[-1] == (9, 0) and all(a + b == 9 for a, b in PAIRS)
assert all(sum(1 for b in range(0, 10) if a + b == 9) == 1 for a in range(1, 10))     # one partner each
swaps = {frozenset(p) for p in PAIRS if p[0] != p[1] and (p[1], p[0]) in PAIRS}
assert len(swaps) == 4 and (9, 0) not in [(b, a) for a, b in PAIRS]
assert len([(a, 9 - a) for a in range(0, 10)]) == 10

if __name__ == "__main__":
    for p in SMALL:
        print(" + ".join(map(str, p)))
