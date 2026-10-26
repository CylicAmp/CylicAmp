# CLASS: COMPUTATION
"""
1 + 2 = 1|1 (owner_work #441, 2026-10-26). Process entry: owner_work/PROCESS.md, #441.

THE OWNER'S LINE, verbatim (#441):
    1+2=1|1=

CLEANED:  1 + 2 = 1|1 = ?

PROCESS: add 1 and 2; write it in the bars of #427 (Number + number of |): 1|1 is two 1s and one bar.

CHECKED:
    1 + 2 = 3
    1|1, number + number of |: the 1s add to 1 + 1 = 2, the bars count 1 -> 2 + 1 = 3 = 1 + 2   right
    the four readings of a row (#427):  digit and bars 1 1 -> 11;  count and digit 2 1 -> 21;
                                        bars over count 1/2;  count over bars 2/1 = 2
    1/2 and 2/1 are the first pair of the owner's 1 and 2 (#403): 1 ÷ 2 = 0.5 and 2 ÷ 1 = 2, which multiply to 1
    both ways: one bar between the 1s, none outside (|1| of #427 had two outside)

RESIDUES (gf37-audit): 3 C3; 11 NEG_H (prime, twin with 13); 21 SA_ST_B.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F

row = "1|1"
digits = [int(c) for c in row if c != "|"]
bars = row.count("|")
assert 1 + 2 == 3 == sum(digits) + bars and (sum(digits), bars) == (2, 1)
assert (f"{digits[0]}{bars}", f"{len(digits)}{digits[0]}") == ("11", "21")
assert (F(bars, len(digits)), F(len(digits), bars)) == (F(1, 2), F(2, 1))
assert F(1, 2) * F(2, 1) == 1 and F(1, 2) == F(1, 1 + 1) and F(2, 1) == F(2, 2 - 1)
assert [x % 37 for x in (3, 11, 21)] == [3, 11, 21]

if __name__ == "__main__":
    print("1 + 2 = 1|1 = 3: two 1s (2) and one bar (1); readings 11, 21, 1/2, 2/1")
