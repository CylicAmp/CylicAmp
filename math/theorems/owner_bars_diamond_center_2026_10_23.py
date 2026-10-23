# CLASS: COMPUTATION
"""
The owner's bars: a diamond of repeated digits split by |, and "Number + number of |" (owner_work #427, 2026-10-23).
Process entry: owner_work/PROCESS.md, #427.

THE OWNER'S LINES, verbatim (#427):
    |1|
    2|2
    3|3|3
    44|44
    55|5|55
    666|666
    777|7|777
    8|888|888|8
    9|999|9|999|9
    1|111|111|1
    222|2|222
    333|333
    44|4|44
    55|55
    6|6|6
    7|7
    8

    here we see
    how the center is influenced by the numbers abd spacing

    |1|=
    2|2=41(2/1
    3|3|3=92(2/3
    4|4|4|4=33(3/4
    5|5|5|5|5=54(4/5
    6|6|6|6|6|6=65(5/6
    7|7|7|7|7|7|7=76(6/7
    8|8|8|8|8|8|8|8=87(7/8
    9|9|9|9|9|9|9|9|9=98
    1|1|1|1|1|1|1|1=17
    2|2|2|2|2|2|2=26,72,6/7,7/6
    3|3|3|3|3|3=36
    4|4|4|4|4=44
    5|5|5|5=54
    6|6|6=62
    7|7=71
    8=8

    2|2|2|2|2|2|2=26,72,6/7,7/6
    each row has a 4 count

    Number +number of |

    so
    222|22   I identify as 3/2
    22|222  or 2/3
    22|2|22 or 42.4  4.24 4•24 4•2•4
    2|2|2|2|2=5/4 or 4/5

PROCESS: lay the digits 1 to 9 and back down in rows, the row length going 1 -> 9 -> 1, split by bars; watch the
center. Then one bar between every two digits, and read each row as the number with the number of bars after it;
each row gives four readings (26, 72, 6/7, 7/6 for seven 2s); then groups: 222|22 as 3/2, 22|2|22 as 4 2 4.

CHECKED -- THE DIAMOND:
    the row lengths go 1 2 3 4 5 6 7 8 9 8 7 6 5 4 3 2 1: 81 digits in all = 9 x 9
    every row reads the same both ways
    the spacing depends only on the row length: going down, each length gets the same groups as going up
      (8: 1 3 3 1   7: 3 1 3   6: 3 3   5: 2 1 2   4: 2 2   3: 1 1 1   2: 1 1); only the ends differ (|1| has bars
      outside, 8 has none)
    the center: an odd length puts a digit in the middle, an even length puts a bar there.
      Going up the digit is the length, so the odd digits take the center: 1 3 5 7 9.
      Going down the digit and the length add to 9, so the even digits take it: 2 4 6 8.
      The center digits are 1 3 5 7 9 2 4 6 8 -- every digit once.
    the row totals: going up the squares 1 4 9 16 25 36 49 64 81; going down the digit x (9 - digit):
      8 14 18 20 20 18 14 8 -- the same read both ways.

CHECKED -- NUMBER + NUMBER OF | (one bar between every two digits: bars = digits - 1):
    by the rule:  5|5|5|5|5 -> 54, 6|... -> 65, 76, 87, 98, 1 x 8 -> 17, 2 x 7 -> 26, 4 x 5 -> 44, 6 x 3 -> 62,
                  7 x 2 -> 71, 8 -> 8:  right
    2|2 = 41 and 3|3|3 = 92: the total with the bars (2+2 = 4 and 1 bar; 3+3+3 = 9 and 2 bars); by the digit
      they are 21 and 32.
    3 x 6 = 36 and 5 x 4 = 54: the digit with the count (six 3s, four 5s); by the bars they are 35 and 53.
    4|4|4|4 = 33: typo: 33 for 43 (4 and 3 bars).
    the four readings of 2|2|2|2|2|2|2 (26, 72, 6/7, 7/6): right -- digit and bars, count and digit, bars over count,
      count over bars.
    the fractions: bars over count = 1/2 2/3 3/4 4/5 5/6 6/7 7/8 8/9 -- the owner's 1 of #403, n ÷ (n + 1);
      count over bars = n ÷ (n - 1), the owner's 2; each pair multiplies to 1 (6/7 x 7/6 = 1).
    222|22 = 3/2: right (3 twos and 2 twos; the totals 6 and 4 give the same 3/2); 22|222 = 2/3 right.
    22|2|22 -> 4 2 4 (2+2, 2, 2+2): 42.4 and 4.24 are 424 with the point moved; with • as times, 4 x 24 = 96 and
      4 x 2 x 4 = 32. 424 reads the same both ways, like the row.
    2|2|2|2|2 = 5/4 or 4/5: right (5 twos, 4 bars).

  both ways: |1| has 2 bars counting the outer ones, 0 between digits.

RESIDUES mod 37 (gf37-audit): 41 C3, 17 NQR17, 71 D7 -- all three prime and twins (41 43, 17 19, 71 73);
  26 IC (137 by 37); 92 and 98 SEED; 54 72 424 NQR17; 33 44 D7; 36 NEG_H; 65 62 SA_ST_B; 76 DARK_A; 87 CAS_EXT.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F

from sympy import isprime


def root(m):
    while m > 9:
        m = sum(map(int, str(m)))
    return m


# --- the diamond ---
dia = ["|1|", "2|2", "3|3|3", "44|44", "55|5|55", "666|666", "777|7|777", "8|888|888|8", "9|999|9|999|9",
       "1|111|111|1", "222|2|222", "333|333", "44|4|44", "55|55", "6|6|6", "7|7", "8"]
lengths = [len(r.replace("|", "")) for r in dia]
digits = [int(r.replace("|", "")[0]) for r in dia]
assert lengths == list(range(1, 10)) + list(range(8, 0, -1)) and sum(lengths) == 81 == 9 * 9
assert digits == list(range(1, 10)) + list(range(1, 9))
assert all(r == r[::-1] for r in dia)
groups = {r: [len(g) for g in r.split("|") if g] for r in dia}
for i in range(9, 17):
    up = 16 - i                                  # the row going up with the same length
    assert lengths[i] == lengths[up] and groups[dia[i]] == groups[dia[up]] or (lengths[i] == 1)
assert groups["8|888|888|8"] == groups["1|111|111|1"] == [1, 3, 3, 1]


def center(r):
    s = r.strip("|")
    return s[len(s) // 2] if len(s) % 2 else "|"


centers = [center(r) for r in dia]
assert all((c != "|") == (n % 2 == 1) for c, n in zip(centers, lengths))
center_digits = [int(c) for c in centers if c != "|"]
assert center_digits == [1, 3, 5, 7, 9, 2, 4, 6, 8] and sorted(center_digits) == list(range(1, 10))
assert all(d == n for d, n in zip(digits[:9], lengths[:9])) and all(d + n == 9 for d, n in zip(digits[9:], lengths[9:]))
totals = [d * n for d, n in zip(digits, lengths)]
assert totals[:9] == [k * k for k in range(1, 10)] and totals[9:] == [8, 14, 18, 20, 20, 18, 14, 8] == totals[9:][::-1]
assert [r.count("|") for r in dia][0] == 2 and "|1|".strip("|") == "1"

# --- number + number of | ---
rows = [(2, 2, "41"), (3, 3, "92"), (4, 4, "33"), (5, 5, "54"), (6, 6, "65"), (7, 7, "76"), (8, 8, "87"), (9, 9, "98"),
        (1, 8, "17"), (2, 7, "26"), (3, 6, "36"), (4, 5, "44"), (5, 4, "54"), (6, 3, "62"), (7, 2, "71"), (8, 1, "8")]


def forms(d, k):
    b = k - 1
    return {"digit+bars": f"{d}{b}" if b else f"{d}", "count+digit": f"{k}{d}", "total+bars": f"{d * k}{b}",
            "digit+count": f"{d}{k}"}


match = {}
for d, k, wrote in rows:
    f = forms(d, k)
    match[(d, k)] = [name for name, v in f.items() if v == wrote]
by_rule = [(d, k) for d, k, w in rows if "digit+bars" in match[(d, k)]]
assert by_rule == [(5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (1, 8), (2, 7), (4, 5), (6, 3), (7, 2), (8, 1)]
assert match[(2, 2)] == ["total+bars"] and match[(3, 3)] == ["total+bars"]
assert match[(3, 6)] == ["digit+count"] and match[(5, 4)] == ["digit+count"]
assert match[(4, 4)] == [] and forms(4, 4)["digit+bars"] == "43"                  # typo: 33 for 43
assert (forms(2, 2)["digit+bars"], forms(3, 3)["digit+bars"], forms(3, 6)["digit+bars"], forms(5, 4)["digit+bars"]) == \
    ("21", "32", "35", "53")
# the four readings of seven 2s
assert (forms(2, 7)["digit+bars"], forms(2, 7)["count+digit"], F(6, 7), F(7, 6)) == ("26", "72", F(6, 7), F(7, 6))
# the fractions are the owner's 1 and 2 (#403)
assert [F(k - 1, k) for k in range(2, 10)] == [F(n, n + 1) for n in range(1, 9)]
assert all(F(k - 1, k) * F(k, k - 1) == 1 for k in range(2, 10))
# groups
assert F(3, 2) == F(6, 4) and F(2, 3) == F(4, 6)
assert [sum(map(int, g)) for g in "22|2|22".split("|")] == [4, 2, 4]
assert (F(424, 10), F(424, 100), 4 * 24, 4 * 2 * 4) == (F(212, 5), F(106, 25), 96, 32) and str(424) == str(424)[::-1]
assert (5, 4) == ("2|2|2|2|2".count("2"), "2|2|2|2|2".count("|"))

# residues
written = [41, 92, 33, 54, 65, 76, 87, 98, 17, 26, 72, 36, 44, 62, 71, 424]
assert [x % 37 for x in written] == [4, 18, 33, 17, 28, 2, 13, 24, 17, 26, 35, 36, 7, 25, 34, 17]
assert [x for x in written if isprime(x)] == [41, 17, 71] and all(isprime(p + 2) for p in (41, 17, 71))

if __name__ == "__main__":
    print("#427: the center digits run 1 3 5 7 9 2 4 6 8, every digit once (odd lengths put a digit in the middle); "
          "spacing depends only on the length; by 'number + number of |' 11 rows right, 41 and 92 use the total, "
          "36 and 54 the count, 33 is 43; bars/count = the owner's 1 (n ÷ (n+1))")
