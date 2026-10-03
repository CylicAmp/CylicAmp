# CLASS: AUDIT
"""
The owner's three repdigit lines (typed, 2026-10-03), decoded by notation-decode.

TRANSCRIPTION (exact)
  333=9×3~2+7=(9
  222=6×2~12÷2=(6
  111=3×1~1+2=(3

READING (each line: aaa -> s x a ~ op = (s, with s = digit sum of aaa = 3a)
  a  s=3a  s*a=3a^2  written op   value  op fits?
  3   9      27       2+7          9      digit sum of 27            yes
  2   6      12       12÷2         6      divide by a                yes
  1   3       3       1+2          3      see OPEN                   value yes
 The lines leave aaa, multiply its digit sum by a, and come back to the digit sum:
 every line ends at "(s". One rule fits all three VALUES: 3a^2 / a = 3a (forced by
 definition: it undoes the x a). The written operations differ per line.

WHY LINE 2 USES ÷ AND NOT A DIGIT SUM (forced, checked for a = 1..9)
  Digital roots: dr(3a^2) = dr(3a)  <=>  3a(a-1) = 0 (mod 9)  <=>  a = 0 or 1 (mod 3).
  So adding digits can return to s's digital root for a = 1, 3 and cannot for a = 2
  (dr 12 = 3, but s = 6). Of the three lines, 222 is the only one where a digit sum
  fails -- and it is the line written with ÷. Over a = 1..9 the digit-sum route works
  for a in {1, 3, 4, 6, 7, 9} at the digital-root level, and one-step digit sum of 3a^2
  equals 3a itself only for a = 1, 3 and 4 (48 -> 4+8 = 12).
  A first draft of this file said "only 1 and 3"; the assertion caught it.

FORCED, NOT FINDINGS
  aaa = 111a = 37 * 3a = 37 * s: every repdigit is its digit sum times 37
  (333 = 9*37, 222 = 6*37, 111 = 3*37). So the first number on each line (9, 6, 3)
  is also aaa's cofactor of 37. Same fact as repdigit_pf_page_2026_10_02.py item 1.

OPEN (not bent to fit)
  Line 1 "1+2": the value 3 is right, but 3a^2 = 3 has no "1" and "2" in it.
  Candidates, all giving 3:
    (a) digit sum of 12, line 2's product, carried down a line;
    (b) a + 2a = 3a (would read 2+4 on line 2 and 3+6 on line 3 -- not written there);
    (c) 1 + 2 = T(2), the triangular number.
  Settles it: what the 1 and the 2 in "1+2" are taken from.
  The "~" and the "(" are kept as markings ("goes to", "back to"); no value assigned.

PRIOR PAGE: repdigit_pf_page_2026_10_02.py writes 333 = x3, 222 = x2, 111 = 1x3.
 Here the multiplier after "×" is a itself (3, 2, 1). That agrees with the prior page
 for 333 and 222; for 999 and 666 (x3 there) it would not -- those lines are not here.

FALSIFICATION: any assertion failing.
"""


def ds(n):
    return sum(map(int, str(n)))


def dr(n):
    return 1 + (n - 1) % 9 if n else 0


LINES = {3: (9, 27, 9), 2: (6, 12, 6), 1: (3, 3, 3)}          # a: (s, s*a, value)
for a, (s, prod, val) in LINES.items():
    aaa = 111 * a
    assert ds(aaa) == s == 3 * a
    assert s * a == prod == 3 * a * a
    assert val == s and prod // a == s                           # one rule fits all values
    assert aaa == 37 * s                                         # forced
assert 2 + 7 == ds(27) == 9                                      # line 3 written op
assert 12 // 2 == 6 and 12 % 2 == 0                              # line 2 written op
assert ds(12) == 3 != 6                                          # digit sum fails on line 2
assert 1 + 2 == 3                                                # line 1 value only

# digital-root criterion over all digits
dr_ok = [a for a in range(1, 10) if dr(3 * a * a) == dr(3 * a)]
assert dr_ok == [a for a in range(1, 10) if a % 3 in (0, 1)] == [1, 3, 4, 6, 7, 9]
assert all((dr(3 * a * a) == dr(3 * a)) == ((3 * a * (a - 1)) % 9 == 0) for a in range(1, 100))
assert [a for a in range(1, 10) if ds(3 * a * a) == 3 * a] == [1, 3, 4]   # 48 -> 12 = 3*4 (an earlier draft said [1, 3])

if __name__ == "__main__":
    for a in (3, 2, 1):
        s, p, v = LINES[a]
        print(f"{111*a} = 37*{s};  {s}x{a} = {p};  {p}/{a} = {v};  dr({p}) = {dr(p)}  vs s = {s}")
    print("digit-sum route returns to s (digital root) for a =", dr_ok, "-- a = 2 is the exception here")
    print("OPEN: source of the 1 and 2 in line 1's '1+2'")
