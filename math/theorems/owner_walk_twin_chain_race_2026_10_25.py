# CLASS: COMPUTATION
"""
What the walk can show that is neither forced nor in A007508: the race between the owner's three twin chains
(owner_work #439, 2026-10-25: "Well, what can it show?").

THE THREE CHAINS (owner_framework_flips_halves_moves_2026_10_20.py, part 8): every twin pair after (3, 5) folds to
(2, 4), (5, 7) or (8, 1). In the walk the pair is 2n - 1, 2n + 1, and which chain it falls in is decided by the root
of n -- the owner's 3 6 9:
    n -> 3:  2n - 1 -> 5,  2n + 1 -> 7     (5, 7)
    n -> 6:  2n - 1 -> 2,  2n + 1 -> 4     (2, 4)
    n -> 9:  2n - 1 -> 8,  2n + 1 -> 1     (8, 1)

NOT FORCED: nothing makes the three counts equal or unequal; the usual expectation (twin pairs spread evenly over the
classes they can be in -- a conjecture) says even, with a race in the small differences. Which chain leads, and how
often the lead changes, can come out either way.

TO 1,000,000,000 (computed here):
    n up to         root 3 (5,7)    root 6 (2,4)    root 9 (8,1)
    10^6               4979            4978            4913
    10^7              35876           35811           35719
    10^8             271509          271038          270823
    10^9            2131202         2127929         2128909
  the lead changed 496 times; root 3, the (5, 7) chain, has led since n = 8,648,940.
  The differences are about 1 to 2 times the square root of the counts, so this is the size a race of chance gives --
  a longer walk is what tells whether the lead holds.

ALSO: the middle 2n by 37 takes 35 of the 37 remainders (1 and 36 cannot happen: one of 2n - 1, 2n + 1 would be a
  multiple of 37); to 10^9 the 35 counts run from 181,855 to 183,122 around the even share 182,515.

OUTSIDE: biases of twin primes in residue classes are studied in general -- S. Sahoo, "On twin prime distribution and
  associated biases", arXiv:2111.09053 (Chebyshev-type and Oliver-Soundararajan-type biases for twin primes). The
  mod 9 race of the three chains to 10^13 was not found there or in OEIS (searched 2026-10-25).

FALSIFICATION: any assertion failing.
"""
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
import owner_walk_big as B  # noqa: E402


def root(m):
    while m > 9:
        m = sum(map(int, str(m)))
    return m


# the chain is decided by the root of n
for n in range(3, 3000, 3):
    pair = (root(2 * n - 1), root(2 * n + 1))
    assert pair == {3: (5, 7), 6: (2, 4), 9: (8, 1)}[root(n)]

w = B.walk_big(10 ** 9, block=10_000_000)
n = w["pairs"]
n = n[n > 2]
assert len(n) == 6_388_040 and np.all(n % 3 == 0)
cls = n % 9
table = {N: [int(((cls == c) & (n <= N)).sum()) for c in (3, 6, 0)] for N in (10 ** 6, 10 ** 7, 10 ** 8, 10 ** 9)}
assert table == {10 ** 6: [4979, 4978, 4913], 10 ** 7: [35876, 35811, 35719], 10 ** 8: [271509, 271038, 270823],
                 10 ** 9: [2131202, 2127929, 2128909]}
c = np.stack([np.cumsum(cls == 3), np.cumsum(cls == 6), np.cumsum(cls == 0)])
lead = np.argmax(c, axis=0)
changes = np.nonzero(lead[1:] != lead[:-1])[0]
assert len(changes) == 496 and lead[-1] == 0 and int(n[changes[-1] + 1]) == 8_648_940
d = table[10 ** 9]
assert 1 < (d[0] - d[1]) / np.sqrt(d[0]) < 3

mid = (2 * n) % 37
counts = np.bincount(mid, minlength=37)
assert counts[1] == 0 and counts[36] == 0 and int((counts > 0).sum()) == 35
assert (int(counts[counts > 0].min()), int(counts.max())) == (181_855, 183_122) and round(len(n) / 35) == 182_515

if __name__ == "__main__":
    print("chains to 10^9: (5,7) 2,131,202  (2,4) 2,127,929  (8,1) 2,128,909; 496 lead changes, (5,7) leads since "
          "n = 8,648,940; middle by 37: 35 classes, 181,855 .. 183,122")
