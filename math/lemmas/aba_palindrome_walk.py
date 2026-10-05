# CLASS: LEMMA
"""
Owner's page (2026-10-05):
    growing mirrors  7, 78, 878 / 7, 87, 787 / 8, 78, 878 / 8, 87, 787   and  SIT787
    walk  121 212 191 919 989 898 878 787 878 787 676 767 676 767 656 565 656
          545 454 545 454 343 434 343 232 323 232 323 212 121 212 121
Context: growing mirrors 4, 94, 494 (rotation_grids_x.py); the torus-787 audit
(torus787_clusters_supplied_audit_2026_10_04.py).

THE MIRRORS: from 7 or 8, adding a digit on alternate sides gives 878 and 787,
both reading the same backwards. 787 is prime; 878 = 2 x 439.

THE WALK: three-digit mirrors aba / bab on neighbouring digits, stepping round
the circle 1-2, then 1-9 (the wrap), 9-8, 8-7, 7-6, 6-5, 5-4, 4-3, 3-2, 2-1 --
back to where it began.
  CLOSED FORMS (known: digit-chain skill): aba + bab = 111(a+b) and
  aba - bab = 91(a-b). So every neighbouring pair differs by exactly 91 = 7 x 13
  (878 - 787 = 91, ..., 323 - 232 = 91), and the pair sums run
  1887, 1665, 1443, 1221, 999, 777, 555, 333 = 111 x 17, 15, ..., 3 -- down by
  222 each step, ending in the repdigits 999, 777, 555, 333. The wrap pair 1-9
  is 8 apart: 919 - 191 = 728 = 8 x 91, and 191 + 919 = 1110 = 111 x 10.
  COUNTS: 1-2, 1-9 and 9-8 appear twice at the start; 8-7, 7-6, 5-4, 3-2 and
  2-1 four times (aba, bab, aba, bab); 6-5 (656 565 656) and 4-3 (343 434 343)
  three times each.

THE GRID AS INTENDED (owner, 2026-10-05: "it starts at 1,2,1 and ends with
  2,1,2 -- each row should be like that"): every pair is one doubled block,
  aba bab aba bab --
      121 212 121 212 / 323 232 323 232 / 434 343 434 343 / 545 454 545 454 /
      656 565 656 565 / 767 676 767 676 / 878 787 878 787 / 989 898 989 898
  The pasted list had uneven blocks (6-5 and 4-3 three entries, the first
  three pairs two). Each row totals 2 x 111(a+b) = 222(a+b): 666, 1110, 1554,
  1998, 2442, 2886, 3330, 3774. Open: whether the wrap 191 919 191 919 closes
  the grid back to 1.

FALSIFICATION: any assertion below failing.
"""
from itertools import groupby
from sympy import isprime, factorint

assert all(x == x[::-1] for x in ("878", "787")) and isprime(787) and factorint(878) == {2: 1, 439: 1}

WALK = [121, 212, 191, 919, 989, 898, 878, 787, 878, 787, 676, 767, 676, 767, 656, 565, 656,
        545, 454, 545, 454, 343, 434, 343, 232, 323, 232, 323, 212, 121, 212, 121]
assert all(str(x) == str(x)[::-1] for x in WALK)
PAIRS = [(k, len(list(g))) for k, g in groupby(tuple(sorted(set(str(x)))) for x in WALK)]
assert [p for p, _ in PAIRS] == [("1", "2"), ("1", "9"), ("8", "9"), ("7", "8"), ("6", "7"), ("5", "6"),
                                  ("4", "5"), ("3", "4"), ("2", "3"), ("1", "2")]
assert [c for _, c in PAIRS] == [2, 2, 2, 4, 4, 3, 4, 3, 4, 4]
for a in range(1, 10):
    for b in range(1, 10):
        x, y = int(f"{a}{b}{a}"), int(f"{b}{a}{b}")
        assert x + y == 111 * (a + b) and x - y == 91 * (a - b)
SUMS = [int(f"{a}{a-1}{a}") + int(f"{a-1}{a}{a-1}") for a in range(9, 2, -1)] + [121 + 212]
assert SUMS == [1887, 1665, 1443, 1221, 999, 777, 555, 333]
assert 919 - 191 == 728 == 8 * 91 and 191 + 919 == 1110

GRID = [[121, 212, 121, 212]] + [[int(f"{k+1}{k}{k+1}"), int(f"{k}{k+1}{k}")] * 2 for k in range(2, 9)]
assert GRID[1] == [323, 232, 323, 232] and GRID[-1] == [989, 898, 989, 898]
assert [sum(r) for r in GRID] == [666, 1110, 1554, 1998, 2442, 2886, 3330, 3774]
assert all(abs(r[0] - r[1]) == 91 for r in GRID)

if __name__ == "__main__":
    print("all assertions pass")
