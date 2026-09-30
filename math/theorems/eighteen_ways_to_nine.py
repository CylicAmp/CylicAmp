# CLASS: IDENTITY
"""
"18 ways to add up 9" (2026-09-30): of the usual ways to count sums equal to 9,
exactly one gives 18 -- partitions of 9 into parts no bigger than 4, which by
conjugation equals partitions of 9 into at most 4 parts. All 30 partitions of 9
exist; these are the 18 with every part <= 4.

Other counts (none is 18): all partitions 30, exactly 3 parts 7, distinct parts 8,
odd parts 8, ordered sums 256, ordered positive pairs 8, digit pairs a+b = 9: 10.

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

if __name__ == "__main__":
    for p in SMALL:
        print(" + ".join(map(str, p)))
