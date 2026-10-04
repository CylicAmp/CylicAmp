# CLASS: AUDIT
"""
Audit of supplied text and script (2026-10-04): "t325_billion_pyramid_matrix" -- a 10-row
1-2 pyramid (row r has r digits), mirrored into 4 panels, "up to the 1 billion boundary".
Mathematics only.

CORRECT
  P1 Mirroring each row about the centre line makes every combined row a palindrome. Forced.
  P2 1,000,000,000 = 10^9 has 10 digits.

WRONG
  P3 The script's own rule (2 where r + c is even, else 1) gives a quadrant of 55 digits
     summing to 80 -- not 15. Its `assert quadrant_sum == 15` FAILS, so it never reaches
     "verified and locked". Four panels: 320, root 5.
  P4 The grid printed in the text is a different rule (every row starts with 2 at the centre):
     row 1 is "2", but the script's row 1 is "1". That printed grid sums to 85 per quadrant,
     340 over four panels, root 7. Neither version gives 15 / 60 / root 6. (55 digits can
     never sum to 15: each digit is at least 1.)
  P5 "Column 2 alternates 1-2-1-2": in the printed grid the column next to the centre is all
     2s and the second column is all 1s; columns alternate, rows do not repeat down a column.
  P6 The pyramid rows are not place values, so the 10th row does not "reach 1 billion"; it is
     a 10-digit string, 2121212121 or 1212121212 depending on the rule.
NOT IN THE REPOSITORY: the script was not pushed (the text says "run locally").
FALSIFICATION: any assertion failing.
"""
script_rule = [[2 if (r + c) % 2 == 0 else 1 for c in range(r)] for r in range(1, 11)]
printed = [[2 if c % 2 == 0 else 1 for c in range(r)] for r in range(1, 11)]
root = lambda n: n % 9 or 9

full = lambda q: [row[::-1] + row for row in q]
assert all(r == r[::-1] for r in full(script_rule) + full(printed))                   # P1
assert len(str(10 ** 9)) == 10                                                        # P2
assert sum(map(len, script_rule)) == 55 and sum(map(sum, script_rule)) == 80 != 15    # P3
assert 4 * 80 == 320 and root(320) == 5
assert script_rule[0] == [1] and printed[0] == [2]                                    # P4
assert sum(map(sum, printed)) == 85 and 4 * 85 == 340 and root(340) == 7
assert 55 > 15
assert all(row[0] == 2 for row in printed) and all(row[1] == 1 for row in printed[1:])  # P5
assert "".join(map(str, printed[-1])) == "2121212121"                                 # P6
