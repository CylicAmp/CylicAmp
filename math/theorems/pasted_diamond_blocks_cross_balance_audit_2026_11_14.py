# CLASS: AUDIT
"""
Pasted text (2026-11-14), from another tool working on the owner's blocks of the digits 1 .. 8, relayed by the owner:
four diamonds (outer pair, inner pair) -- Evens 2,8 | 4,6; Odds 1,7 | 3,5; Primes 2,7 | 3,5; Non-primes 1,8 | 4,6 --
the Prime / Non-prime imbalances +1 and -1 cancel, outer 18 = inner 18, unique up to swapping outer and inner; and
the owner's chain as quoted: 36/2 = 18, 17 + 18 = 35 -> 3 + 5 = 8.

RIGHT (checked below):
  sums 10|10, 8|8, 9|8, 9|10; imbalances 0, 0, +1, -1; combined outer 9 + 9 = 18, inner 8 + 10 = 18;
  unique: over the 3 x 3 pairings of the primes and non-primes with either pair outside, only primes 2,7 + non-primes
    1,8 outside (or the swap, 3,5 + 4,6 outside) give 18 | 18;
  shared cores: Odds and Primes both have 3,5 inside; Evens and Non-primes both have 4,6 inside;
  the chain: 1 + ... + 8 = 36, 36/2 = 18; 2 + 3 + 5 + 7 = 17, 17 + 18 = 35, 3 + 5 = 8.

WHAT IT ADDS, AND WHY: both cuts have the SAME outside and inside -- outer 2,8 + 1,7 = 2,7 + 1,8 = {1, 2, 7, 8}, inner
  4,6 + 3,5 = {3, 4, 5, 6}: the four end digits around the four middle ones. They balance because the digits pair to 9
  (1 + 8 = 2 + 7 = 3 + 6 = 4 + 5 = 9): two pairs each side, 18 each. The Prime / Non-prime cut is the Even / Odd cut
  with 7 and 8 traded between blocks.

NOT SHOWN: "the digits of 35 are not incidental" (3,5 = the shared core; 18 -> 1,8 = the Non-prime outer pair): those
  are readings of how 35 and 18 are written in base 10; nothing in the blocks produces them.

FALSIFICATION: any assertion failing.
"""
from itertools import combinations

blocks = {"evens": ((2, 8), (4, 6)), "odds": ((1, 7), (3, 5)), "primes": ((2, 7), (3, 5)), "nonprimes": ((1, 8), (4, 6))}
assert {k: (sum(o), sum(i), sum(o) - sum(i)) for k, (o, i) in blocks.items()} == {
    "evens": (10, 10, 0), "odds": (8, 8, 0), "primes": (9, 8, 1), "nonprimes": (9, 10, -1)}
assert 9 + 9 == 18 == 8 + 10


def splits(s):
    s = tuple(s)
    out = []
    for a in combinations(s, 2):
        b = tuple(x for x in s if x not in a)
        out.append((a, b))                       # a outside, b inside (both orders appear)
    return out


hits = [(po, no) for po, pi in splits((2, 3, 5, 7)) for no, ni in splits((1, 4, 6, 8)) if sum(po) + sum(no) == sum(pi) + sum(ni)]
assert sorted(hits) == sorted([((2, 7), (1, 8)), ((3, 5), (4, 6))])          # unique up to swapping outside/inside

assert blocks["odds"][1] == blocks["primes"][1] == (3, 5) and blocks["evens"][1] == blocks["nonprimes"][1] == (4, 6)
assert set(blocks["evens"][0] + blocks["odds"][0]) == set(blocks["primes"][0] + blocks["nonprimes"][0]) == {1, 2, 7, 8}
assert set(blocks["evens"][1] + blocks["odds"][1]) == set(blocks["primes"][1] + blocks["nonprimes"][1]) == {3, 4, 5, 6}
assert 1 + 8 == 2 + 7 == 3 + 6 == 4 + 5 == 9

assert sum(range(1, 9)) == 36 and 36 // 2 == 18 and 2 + 3 + 5 + 7 == 17 and 17 + 18 == 35 and 3 + 5 == 8

if __name__ == "__main__":
    print("diamonds right; Prime/Non-prime 18 | 18 unique up to swap; both cuts are ends {1,2,7,8} | middle {3,4,5,6}")
