# CLASS: AUDIT
"""
Audit of supplied text and script (2026-10-04): 12346789 vs 12345678 -- "dual matrix",
gap 1111, roots, fives, digit products. Mathematics only.

CORRECT (every number)
  H1 12346789 - 12345678 = 1111; slots 5-8 each step by 1 (6-5, 7-6, 8-7, 9-8), and the
     place values of those four slots are 1000, 100, 10, 1, so the gap is 1111. Forced.
  H2 Roots 4 (digit sum 40), 9 (digit sum 36), gap 4; 9 + 4 = 13 -> 4. Forced: digital
     roots add mod 9, so root(a) = root(b) + root(a - b).
  H3 Mod 5: 4, 3, gap 1, and 4 - 3 = 1. Forced the same way (mod 5 is additive).
  H4 Digit products 72,576 (= 9!/5) and 40,320 (= 8!), digit sums 27 and 9, both root 9.
     Forced: both products contain 3 x 6 = 18, a multiple of 9.

NOT IN THE REPOSITORY
  H5 The text says t325_half_split_sync_2026_10_03.py "is pushed to branch all-work". No
     such file exists on all-work (checked 2026-10-04 after fetching origin). The checks it
     contained are the assertions below.
FALSIFICATION: any assertion failing.
"""
from math import factorial, prod

a, b = 12346789, 12345678
ds = lambda n: sum(map(int, str(n)))
root = lambda n: n % 9 or 9

assert a - b == 1111 == 1000 + 100 + 10 + 1                                            # H1
assert [x - y for x, y in zip((6, 7, 8, 9), (5, 6, 7, 8))] == [1, 1, 1, 1]
assert (ds(a), ds(b), root(a), root(b), root(1111)) == (40, 36, 4, 9, 4)                 # H2
assert root(root(b) + root(a - b)) == root(a)
assert (a % 5, b % 5, (a - b) % 5) == (4, 3, 1) and (a % 5 - b % 5) % 5 == (a - b) % 5   # H3
pa, pb = prod((1, 2, 3, 4, 6, 7, 8, 9)), prod(range(1, 9))                              # H4
assert (pa, pb) == (72576, 40320) == (factorial(9) // 5, factorial(8))
assert (ds(pa), ds(pb), root(pa), root(pb)) == (27, 9, 9, 9) and pa % 18 == pb % 18 == 0
