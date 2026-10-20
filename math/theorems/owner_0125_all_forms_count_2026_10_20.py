# CLASS: AUDIT
"""
Every form you can make from 0.125 by the owner's moves, counted exactly (owner_work #378, 2026-10-20). Process entry: owner_work/PROCESS.md, #378.

THE OWNER'S LINES, verbatim:
    0.125
    5-2
    0.12311
    0.1232
    11.123
    2.123
    0.323
    5-3
    0.122
    2.222
    1.313

    Yeah, I don't think you get it. I'm giving you examples of how to do what I'm doing. You can make a bunch of different things from this because you
    can reduce from any number or you can add to any number. You can add to the length of the number. You can add one way to the number, to the left side
    or to the right side. And there's only a certain amount of things that you can do like that, and I would like the exact number.

THE MOVES (as given): take units off any digit; put them onto any digit, or as new digits on the left or the right; the length can grow. In every
  example the 8 of 0.125 (1+2+5) is kept: 1+2+3+1+1, 1+2+3+2, 1+1+1+2+3, 2+1+2+3, 3+2+3, 2+2+2+2, 1+3+1+3 are all 8. 0.122 (sum 5) is the step with
  the 3 still out, not a finished form.
WHAT IS COUNTED: every number written with digits 1 to 9 (no 0 except the "0." in front) whose digits add to 8, with the point anywhere that leaves at least
  one digit after it (every example does). Zeros are left out because a 0 can be put anywhere any number of times (0.1025, 0.10025, ...), and then there
  is no end to the count.

THE EXACT NUMBER: 576.
  The digits, ignoring the point: the ways to split 8 into ordered parts, 2^7 = 128 (8 ; 17 71 26 62 35 53 44 ; ... ; 11111111).
  By length: 1 digit 1 way, 2 digits 7, 3 digits 21, 4 digits 35, 5 digits 35, 6 digits 21, 7 digits 7, 8 digits 1 (1+7+21+35+35+21+7+1 = 128).
  A form with k digits takes the point in k places (0.ddd, d.dd, dd.d for k = 3), so 1x1 + 2x7 + 3x21 + 4x35 + 5x35 + 6x21 + 7x7 + 8x1 = 576.
  If a whole number with nothing after the point also counts (125, 8, 2222), add the 128: 704.
  All of the owner's examples are in the 576.
FRAMEWORKS (gf37-audit): 576 = 24x24 = 21 SA_ST_B ; 704 = 64x11 = 1 IC ; 128 = 2^7 = 17 NQR17.

#379 (2026-10-20), verbatim: "very good with zero amd without... / seeing on how I covered this already before and either not saved or not made into part of
  the process of how I do.. / so totals are for both"
  The owner's standing way of counting: every count both ways, with and without (as with the comma and without, #269: "no comma count should be explored
  also because it creates a better understanding of the bigger picture"). Totals for both:
  WITHOUT ZERO: 576 (704 with whole numbers) -- as above; by length 1, 14, 63, 140, 175, 126, 49, 8.
  WITH ZERO (zeros allowed among the digits; the part before the point is "0" or does not start with 0; at least one digit after the point):
    there is no last length, so the total is given by length: 1, 17, 117, 525, 1815, 5247, 13299, 30459 for 1 to 8 digits -- 51480 up to 8 digits, the
    longest form without zero. For n digits: S(n) + (n-1)(S(n) - S(n-1)), where S(n) = C(n+7, 8) is the number of n-digit strings (zeros allowed) that add to 8.
    Example n = 2: 9 strings 08 17 26 35 44 53 62 71 80 ; 0.08 .. 0.80 gives 9, 1.7 .. 8.0 gives 8 ; 17.
  Frameworks: 51480 = 2x2x2x3x3x5x11x13 = 13 CAS_EXT.

FALSIFICATION: any assertion failing.
"""
from itertools import product
from math import comb


def compositions(n):
    if n == 0:
        yield ()
        return
    for first in range(1, n + 1):
        for rest in compositions(n - first):
            yield (first,) + rest


comps = list(compositions(8))
assert len(comps) == 128 == 2 ** 7 and all(max(c) <= 9 for c in comps)
by_len = {k: sum(1 for c in comps if len(c) == k) for k in range(1, 9)}
assert by_len == {k: comb(7, k - 1) for k in range(1, 9)} and list(by_len.values()) == [1, 7, 21, 35, 35, 21, 7, 1]


def forms(allow_whole=False):
    out = set()
    for c in comps:
        s = "".join(map(str, c))
        for cut in range(0, len(s) + (1 if allow_whole else 0)):
            left, right = s[:cut], s[cut:]
            out.add((left or "0") + ("." + right if right else ""))
    return out


F = forms()
assert len(F) == 576 == sum(k * comb(7, k - 1) for k in range(1, 9)) == 1 + 14 + 63 + 140 + 175 + 126 + 49 + 8
assert len(forms(allow_whole=True)) == 704 == 576 + 128
examples = ["0.125", "0.12311", "0.1232", "11.123", "2.123", "0.323", "2.222", "1.313"]
assert all(e in F for e in examples) and all(sum(int(ch) for ch in e if ch.isdigit()) == 8 for e in examples)
assert "0.122" not in F and sum(map(int, "0122")) == 5
assert all(sum(int(ch) for ch in f if ch.isdigit()) == 8 and "0" not in f.split(".")[1] for f in F)
assert 576 == 24 * 24 and (576 % 37, 704 % 37, 128 % 37) == (21, 1, 17) and 704 == 64 * 11

# #379: with zero, by length
def with_zero(n):
    total = 0
    for digs in product(range(9), repeat=n):
        if sum(digs) != 8:
            continue
        for cut in range(0, n):
            if cut >= 1 and digs[0] == 0:
                continue
            total += 1
    return total


S = lambda n: comb(n + 7, 8)
wz = [with_zero(n) for n in range(1, 9)]
assert wz == [1, 17, 117, 525, 1815, 5247, 13299, 30459] and sum(wz) == 51480
assert all(wz[n - 1] == S(n) + (n - 1) * (S(n) - S(n - 1)) for n in range(1, 9))
assert [k * comb(7, k - 1) for k in range(1, 9)] == [1, 14, 63, 140, 175, 126, 49, 8] and sum(k * comb(7, k - 1) for k in range(1, 9)) == 576
assert S(2) == 9 and wz[1] == 9 + 8 and 51480 % 37 == 13

if __name__ == "__main__":
    print("forms of 0.125 keeping the 8, digits 1-9, at least one digit after the point: 576 (704 if whole numbers count; 128 digit strings)")
