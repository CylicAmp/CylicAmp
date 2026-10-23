# CLASS: AUDIT
"""
The pasted reading of the run-together string 8.702.634,456.9313,159.56 as money with two-digit cents
(owner_work #428, 2026-10-23). Audit on arrival. Text from another tool, relayed by the owner; the same message asks
for the walk to a trillion (owner_engine_walk_1t_2026_10_23.py).

RIGHT:
  "8.702.63" + "4,456.93" + "13,159.56" put back together is the string, character for character.
  8,702.63 + 4,456.93 = 13,159.56 -- the third amount is the sum of the first two, to the cent
  (the paste leaves "Balance / Sum:" blank; this is the number that goes there).

WRONG (changes the numbers the string is read as): "completely unambiguous". The paste reads the first point,
  in 8.702, as a thousands mark and every other point as the cents point. Reading every point as the cents point
  (the same two-digit rule) splits the string into four amounts instead:
      8.70 | 2.63 | 4,456.93 | 13,159.56
  and 8.70 + 2.63 + 4,456.93 = 4,468.26 -- no balance. So the two-digit rule leaves two readings; the sum is what
  picks the paste's one: only 8,702.63 + 4,456.93 lands exactly on 13,159.56.

NEW LINES, owner's notation (in cents):
  870263 + 445693 = 1315956
  roots: 8+7+0+2+6+3 = 26 -> 8;  4+4+5+6+9+3 = 31 -> 4;  8 + 4 = 12 -> 3;  1+3+1+5+9+5+6 = 30 -> 3   right
  by 37: 870263 -> 23 TESLA, 445693 -> 28 SA_ST_B, 1315956 -> 14 C9 (23 + 28 = 51 = 37 + 14)

FALSIFICATION: any assertion failing.
"""
import re
from decimal import Decimal as D

s = "8.702.634,456.9313,159.56"
assert "8.702.63" + "4,456.93" + "13,159.56" == s
a, b, c = D("8702.63"), D("4456.93"), D("13159.56")
assert a + b == c


def split_all_points_cents(text):
    """every '.' is a cents point; each amount ends two digits after its point"""
    out, cur, i = [], "", 0
    while i < len(text):
        ch = text[i]
        if ch == ".":
            out.append(cur + text[i:i + 3])
            cur, i = "", i + 3
        else:
            cur += ch
            i += 1
    return out


four = split_all_points_cents(s)
assert four == ["8.70", "2.63", "4,456.93", "13,159.56"] and "".join(four) == s
vals = [D(x.replace(",", "")) for x in four]
assert sum(vals[:3]) == D("4468.26") != vals[3]
# in the paste's reading only the last amount is the sum of the others
assert a + b == c and a != b + c and b != a + c

ca, cb, cc = 870263, 445693, 1315956


def root(m):
    while m > 9:
        m = sum(map(int, str(m)))
    return m


assert ca + cb == cc and (root(ca), root(cb), root(cc)) == (8, 4, 3) and root(8 + 4) == 3
assert (ca % 37, cb % 37, cc % 37) == (23, 28, 14) and (23 + 28) % 37 == 14
assert re.fullmatch(r"[\d.,]+", s)

if __name__ == "__main__":
    print("cents string: 8,702.63 + 4,456.93 = 13,159.56 right; not the only split under the two-digit rule "
          "(8.70 | 2.63 | 4,456.93 | 13,159.56 also fits, with no balance) -- the sum picks the reading")
