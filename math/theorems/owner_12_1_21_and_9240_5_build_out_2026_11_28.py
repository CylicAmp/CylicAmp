# CLASS: AUDIT
"""
The owner's lines of 2026-11-28 and the owner's correction of the first build-out.

THE OWNER'S LINES, verbatim:
    1)12|1|21(8
    9240.5|5.0429
    94801|10849
    build out how I taught
THE OWNER'S CORRECTION (the method): "it's where we take something we cut it in half. We added up, we make it a mirror
    image. I showed you how to add things up when there's more than two lines" -- the adding is the column stack of
    2026-11-17 (owner_5151_1515_column_stack_2026_11_17.py): lay the lines one under another and add down each column,
    keeping each column's root.

THE PROCESS, step by step (each checked RIGHT):
    take something, cut it in half:   18481 -> 9240.5            (9240.5 + 9240.5 = 18481)
    make it a mirror image:           9240.5 | 5.0429            (5.0429 is 9240.5 read backwards)
    add it up, column by column, the half laid on itself, keeping each column's root:
          9 2 4 0 5          5 0 4 2 9
        + 9 2 4 0 5        + 5 0 4 2 9
          18 4 8 0 10        10 0 8 4 18
       -> 9 4 8 0 1       -> 1 0 8 4 9
    the mirror again:                 94801 | 10849              (each is the other read backwards)
    adding the two halves of a line down the columns gives a mirror image itself:
        12 over 21          -> 3 3         = 33
        9240.5 over 5.0429  -> 5 2 8 2 5   = 52825
        94801 over 10849    -> 1 4 7 4 1   = 14741        and 52825 laid on itself -> 14741 again
    (forced: column k and column (n+1-k) add the same two digits, so the result always reads the same both ways)
ASKED: the 1) and the (8) of line 1 -- what each one is in the steps.
Superseded reading (2026-11-28, first reply): splits and flips in place of the column add; the owner marked it incorrect.
Frameworks: records/gf37_audit_12_1_21_9240_2026_11_28.txt.

FALSIFICATION: any assertion failing.
"""
import pathlib
from fractions import Fraction as F

TH = pathlib.Path(__file__).resolve().parent
root = lambda n: 0 if n == 0 else 1 + (n - 1) % 9


def column_add(*rows):
    return "".join(str(root(sum(int(r[i]) for r in rows))) for i in range(len(rows[0])))


assert F(92405, 10) * 2 == 18481 and "9240.5"[::-1] == "5.0429" and "94801"[::-1] == "10849"
assert column_add("92405", "92405") == "94801" and column_add("50429", "50429") == "10849"
assert column_add("12", "21") == "33" and column_add("92405", "50429") == "52825" and column_add("94801", "10849") == "14741"
assert column_add("52825", "52825") == "14741"
assert all(column_add(s, s[::-1]) == column_add(s, s[::-1])[::-1] for s in ("12", "92405", "94801", "123456", "70718"))
assert "column" in (TH / "owner_5151_1515_column_stack_2026_11_17.py").read_text()

if __name__ == "__main__":
    print("cut in half 18481 -> 9240.5, mirror 5.0429, add up by columns -> 94801, mirror 10849; halves stack to 52825, 14741")
