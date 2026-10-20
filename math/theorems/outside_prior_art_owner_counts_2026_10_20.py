# CLASS: AUDIT
"""
Outside prior art for two of the owner's sequences (owner_work #396, 2026-10-20). Replies on 2026-10-20 said "most of these are true facts that number
theory already has" without checking any of them; the owner asked why. This file is the check, done on OEIS (oeis.org, searched 2026-10-20).

1. The with-zero counts of the forms of 0.125 (owner's moves, #378-#379): 1, 17, 117, 525, 1815, 5247, 13299, 30459.
   OEIS: A056117, "Expansion of (1+8*x)/(1-x)^9" -- the same numbers. OEIS gives them as a power series; the owner reached them by counting every way to
   write 0.125 with its 8 moved between digit places, zeros allowed (owner_0125_all_forms_count_2026_10_20.py). Checked here: the series (1+8x)/(1-x)^9
   gives these terms, and so does the owner's count, (9n-1)/8 x C(n+6, 7).
2. How many n of each length have 37 dividing n + its flip (the owner's flips, framework file): 45, 225, 2405, 34867 for 3, 4, 5, 6 digits.
   OEIS: no match ("Sorry, but the terms do not match anything in the table").
Rule taken from this: nothing is called "known" without the place it is published; when it is published, the reply names it and shows how the owner's
route differs (the owner's instruction of 2026-09-29, skill outside-prior-art).

FALSIFICATION: any assertion failing.
"""
from math import comb

import sympy as sp

x = sp.symbols("x")
series = sp.series((1 + 8 * x) / (1 - x) ** 9, x, 0, 8).removeO()
terms = [series.coeff(x, k) for k in range(8)]
assert terms == [1, 17, 117, 525, 1815, 5247, 13299, 30459]
assert terms == [(9 * n - 1) * comb(n + 6, 7) // 8 for n in range(1, 9)]


def flip(n):
    return int(str(n)[::-1])


assert [sum(1 for n in range(10 ** (L - 1), 10 ** L) if (n + flip(n)) % 37 == 0) for L in (3, 4, 5, 6)] == [45, 225, 2405, 34867]

if __name__ == "__main__":
    print("owner's with-zero counts = OEIS A056117 (as a series); the 37 flip counts 45, 225, 2405, 34867 are not in OEIS")
