# CLASS: AUDIT
"""
Audit of supplied text (2026-10-03, another assistant's reading of the repdigit lines):
"nnn / 37 = n x 3, and the PF reduction is path-dependent".

CORRECT
  S1 nnn / 37 = 3n for n = 1..9 (forced: nnn = 111n = 3*37*n).
  S2 Every arithmetic step in the three "paths from 21" is computed correctly.

NOT ESTABLISHED / WRONG
  S3 "Path-dependent PF": the paths add and subtract numbers that come from no stated
     rule (+3, +3, -2, +1 ...). With free operands EVERY digit 1..9 is reachable from 21
     (checked below with one step of +-k), so "three different foundations" carries no
     information: a test that cannot fail. A path system needs a rule for its operands.
  S4 The PF table contradicts the owner's pages:
     - The 2026-10-02 page marks PF only on 111, 444, 888 (PF-13, PF-23, PF-33); 222 and
       555 are x2 lines, 333/666/999 are x3 lines. The table gives PF values to all nine.
     - 777 is not on any page; the table's "777 -> PF 1" has no source.
     - The owner's line of 2026-10-03, "111=3×1~1+2=(3", ends at 3. The table says
       111 -> PF 1 via "3-2=1", a step the owner did not write.
  S5 The table is internally inconsistent: 12 -> 3 and 15 -> 6 by digit sum, but 18 is
     left "?" (digit sum gives 9), 21 is reduced by 2-1 (digit sum gives 3), and 24, 27
     are left unreduced. No single rule produces its PF column.
  S6 "24 = 4!, 27 = 3^3": both true, offered as a guess for why they are unreduced;
     nothing on the pages says so.

OWNER'S DEFINITION (2026-10-03, verbatim): "I didn't put path dependent. ... one of these
algorithms changed what PF means. PF has always stood for prime foundational, which is
numbers that equal 12."  The "path-dependent" reading came from the supplied text, not
the owner, and it redefines PF; under the owner's definition it is set aside.
Checked against the PF lines of the 2026-10-02 page (111, 444, 888):
  444: digit sum 12 and 444/37 = 12          -- equals 12
  888: digit sum 24 and 888/37 = 24 = 2 x 12 -- a multiple of 12, not 12
  111: digit sum 3 and 111/37 = 3            -- how 111 equals 12 is not on the page yet
Among all nine repdigits, only 444 gives exactly 12 by digit sum or by /37.

What stands from the owner's own lines: repdigit_return_lines_2026_10_03.py.
FALSIFICATION: any assertion failing.
"""
for n in range(1, 10):
    assert int(str(n) * 3) // 37 == 3 * n and int(str(n) * 3) % 37 == 0          # S1

P1 = [(2, '-', 1, 1), (1, '+', 2, 3), (3, '-', 2, 1)]
P2 = [(2, '-', 1, 1), (1, '+', 1, 2), (2, '+', 2, 4), (4, '+', 3, 7), (7, '+', 3, 10), (1, '+', 1, 2)]
P3 = [(2, '-', 1, 1), (1, '+', 1, 2), (2, '+', 2, 4), (4, '+', 3, 7), (7, '+', 3, 10), (10, '-', 2, 8), (8, '+', 1, 9)]
for path in (P1, P2, P3):                                                         # S2
    for x, op, y, r in path:
        assert (x + y if op == '+' else x - y) == r

# S3: with a free operand, one step reaches every digit from either digit of 21
reach = {d + k for d in (2, 1) for k in range(-9, 10)} | {21 - k for k in range(12, 21)}
assert set(range(1, 10)) <= reach

# S4: owner's page markings (repdigit_pf_page_2026_10_02.py) vs the supplied PF table
PAGE_PF = {1, 4, 8}
TABLE_PF = {1: 1, 2: 6, 3: 9, 4: 3, 5: 6, 6: None, 7: 1, 8: 24, 9: 27}
assert set(TABLE_PF) - PAGE_PF == {2, 3, 5, 6, 7, 9}
assert TABLE_PF[1] == 1 and 1 + 2 == 3        # owner's line 111 ends at 3, table says 1

# S5: digit sum would give 18 -> 9, 21 -> 3, 24 -> 6, 27 -> 9 -- table does not follow it
ds = lambda m: sum(map(int, str(m)))
assert [ds(3 * n) for n in (4, 5)] == [TABLE_PF[4], TABLE_PF[5]]
assert [ds(3 * n) for n in (6, 7, 8, 9)] == [9, 3, 6, 9]
assert (TABLE_PF[7], TABLE_PF[8], TABLE_PF[9]) == (1, 24, 27)

DS = lambda m: sum(map(int, str(m)))
assert [n for n in range(1, 10) if 111 * n // 37 == 12 or DS(111 * n) == 12] == [4]
assert (DS(888), 888 // 37, DS(111), 111 // 37) == (24, 24, 3, 3)

import math
assert math.factorial(4) == 24 and 3 ** 3 == 27                                 # S6

if __name__ == "__main__":
    print("S1, S2 correct; S3 untestable as stated; S4 contradicts owner's pages; S5 no single rule; S6 true but unsupported")
