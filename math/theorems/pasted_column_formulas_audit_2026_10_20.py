# CLASS: AUDIT
"""
A pasted note on the two column formulas of the 0.125 counts (owner_work #388, 2026-10-20). Another tool's text. A block about tokenizers (JSON, LaTeX,
emoji counts for o200k_base, cl100k_base, llama3, gemma2, p50k_base, r50k_base) is spliced into the middle of its first sentence; it belongs to a different
conversation, has nothing to do with this work, and is not checked here. Nothing is put in the owner's mouth.

RIGHT (re-run):
  b_k = C(k+7, 8) + 8 C(k+6, 8) = (9k - 1)/8 x C(k+6, 7) for column 2 (with zero), using C(k+6, 8) = 0 at k = 1 ; the two forms agree because
    C(k+7, 8) = (k+7)/8 x C(k+6, 7) and C(k+6, 8) = (k-1)/8 x C(k+6, 7).
  b_1..b_8 = 1, 17, 117, 525, 1815, 5247, 13299, 30459 ; b_9 = 64350.
  sum b_1..b_8 = C(16, 9) + 8 C(15, 9) = 11440 + 8 x 5005 = 51480 (hockey stick).
  column 3: A(x) = sum a_k x^(k-1) = (1+x)^7 + 7x(1+x)^6 = (1+x)^6 (1+8x) ; A(1) = 2^6 x 9 = 576 ; a_k/k = a_(9-k)/(9-k) = C(7, k-1) ;
    (1+8) + (14+49) + (63+126) + (140+175) = 9 + 63 + 189 + 315 = 576.
  51480/576 = 715/8 = C(13, 4)/8.
WRONG / OUT OF DATE:
  "b_9 = 64,350: Prediction" and "the decisive test is whether the original construction independently implies these formulas": the construction is known and
    in the repository (owner_0125_all_forms_count_2026_10_20.py: the owner's moves on 0.125, #378 and #379), and both formulas follow from it -- they are counts,
    not fits. Column 3: C(7, k-1) strings of k nonzero digits adding to 8, times k places for the point. Column 2: S(k) = C(k+7, 8) strings of k digits with zeros,
    the point at the front for each, plus k-1 more places for each string that does not start with 0 (S(k) - S(k-1) = C(k+6, 7) of them), and
    (k-1) C(k+6, 7) = 8 C(k+6, 8). The 9-digit count is checked here by listing all 9-digit forms: 64350, as the formula says.
  The formula is the owner's: it counts the owner's own construction (#378, #379), computed in the owner's repository at the owner's request.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction
from math import comb

import sympy as sp

b = lambda k: comb(k + 7, 8) + 8 * (comb(k + 6, 8) if k + 6 >= 8 else 0)
assert [b(k) for k in range(1, 10)] == [1, 17, 117, 525, 1815, 5247, 13299, 30459, 64350]
assert all(8 * b(k) == (9 * k - 1) * comb(k + 6, 7) for k in range(1, 30))
assert all(8 * comb(k + 7, 8) == (k + 7) * comb(k + 6, 7) and 8 * comb(k + 6, 8) == (k - 1) * comb(k + 6, 7) for k in range(1, 30))
assert sum(b(k) for k in range(1, 9)) == comb(16, 9) + 8 * comb(15, 9) == 11440 + 8 * 5005 == 51480

x = sp.symbols("x")
A = sum(k * comb(7, k - 1) * x ** (k - 1) for k in range(1, 9))
assert sp.expand(A - ((1 + x) ** 7 + 7 * x * (1 + x) ** 6)) == 0 and sp.expand(A - (1 + x) ** 6 * (1 + 8 * x)) == 0 and A.subs(x, 1) == 576
a = [k * comb(7, k - 1) for k in range(1, 9)]
assert all(Fraction(a[k - 1], k) == Fraction(a[8 - k], 9 - k) == comb(7, k - 1) for k in range(1, 9))
assert (1 + 8, 14 + 49, 63 + 126, 140 + 175) == (9, 63, 189, 315) and 9 + 63 + 189 + 315 == 576
assert Fraction(51480, 576) == Fraction(comb(13, 4), 8)


def strings(n, total):                        # every digit string of length n adding to total
    if n == 0:
        if total == 0:
            yield ""
        return
    for d in range(0, min(9, total) + 1):
        for rest in strings(n - 1, total - d):
            yield str(d) + rest


def forms_with_zero(n):
    count = 0
    for s in strings(n, 8):
        count += 1                            # 0.sss
        if s[0] != "0":
            count += n - 1                    # s[:c].s[c:] for c = 1 .. n-1
    return count


assert [forms_with_zero(n) for n in range(1, 10)] == [b(k) for k in range(1, 10)]
assert sum(1 for _ in strings(9, 8)) == comb(16, 8) == 12870

if __name__ == "__main__":
    print("column formulas right and derived from the construction; the 9-digit count 64350 is checked by listing, not a prediction; tokenizer block spliced in, not this work")
