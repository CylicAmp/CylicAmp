# CLASS: AUDIT
"""
A pasted "energy profile curve for the cyclic pathway" (another tool's text; "plotted above", but no plot is in the message) and the owner's two lines after it
(owner_work #399, 2026-10-20). Process entry for the owner's lines: owner_work/PROCESS.md, #399.

THE OWNER'S LINES, verbatim:
    1+7=8

    eight is the barrier to and cost 1
  Cleaned: 1 + 7 = 8 ; 8 is the barrier, and it costs 1 to get past it: 8 + 1 = 9.
  Checked: 1 + 7 = 8 right. In the owner's chain 9 is where everything resets (adding 9 changes nothing, framework B1), and 8 is the last stop before it:
    8 + 1 = 9. It is every term of the A056117 driver: 9k - 1 = 8, 17, 26, 35, ... each adds up to 8 (17 → 1+7 = 8), and each is one short of a multiple of 9:
    9k - 1 + 1 = 9k (8 + 1 = 9, 17 + 1 = 18, 26 + 1 = 27). So the 1 the owner says the barrier costs is exactly the 1 in 9k - 1.

THE PASTE, checked:
  RIGHT: the points (0,0), (1,4.0), (2,1.5), (3,3.0), (4,1.5), (5,2.5), (6,1.0), (7,5.0), (8,1.5), (9,3.5), (10,0): the highest is 5.0 at x = 7, start and end are both 0
    (so the change over the cycle is 0). The climbs out of each low point: 4.0, 1.5, 1.0, 4.0, 2.0.
    1 + 5 + 0 = 6 ; 246 x 1.5 = 369 ; 246 = 6 x 41 ; 369 = 9 x 41 ; 123,456,789 leaves 369 by 999 ; 5 + 5 = 10 → 1 ; 4 x 7 = 28 → 2 + 8 = 10 → 1.
  The label "intermediate 3" is used twice, at x = 4 and at x = 8 (both at 1.5).
MISSING (asked): the plot ("plotted above" -- not in the message), and what the pathway and its energies are: no source, units or rule gives the numbers 4.0, 1.5,
  3.0, 2.5, 5.0, 3.5, so beyond adding them up they can't be checked.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F

chain = lambda n: n if n < 10 else chain(sum(map(int, str(n))))
assert 1 + 7 == 8 and 8 + 1 == 9 and chain(17) == 8
assert all(chain(9 * k - 1) == 8 and (9 * k - 1 + 1) % 9 == 0 for k in range(1, 300))
assert [9 * k - 1 + 1 for k in (1, 2, 3)] == [9, 18, 27]

pts = [(0, 0), (1, F(4)), (2, F(3, 2)), (3, F(3)), (4, F(3, 2)), (5, F(5, 2)), (6, F(1)), (7, F(5)), (8, F(3, 2)), (9, F(7, 2)), (10, 0)]
ys = [y for _, y in pts]
assert max(ys) == 5 and pts[ys.index(5)][0] == 7 and ys[0] == ys[-1] == 0
lows, peaks = ys[0::2], ys[1::2]
assert [p - l for p, l in zip(peaks, lows)] == [4, F(3, 2), 1, 4, 2]
assert 1 + 5 + 0 == 6 and 246 * F(3, 2) == 369 and 246 == 6 * 41 and 369 == 9 * 41 and 123456789 % 999 == 369
assert (5 + 5) % 9 == 1 and (4 * 7) % 9 == 1 and 4 * 7 == 28

if __name__ == "__main__":
    print("#399: 1+7=8; 8 is one short of 9 and costs 1 -- every 9k-1 is that barrier (9k-1+1 = 9k). Paste: arithmetic right; plot and energy source missing")
