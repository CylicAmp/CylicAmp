# CLASS: AUDIT
"""
The owner's diagram of 2026-10-18 (a picture, no text; saved as owner_work/images/2026-10-18_diagram_43_26_36.jpg).

THE OWNER'S DIAGRAM, transcribed:
      |4|3|
     4|-1-|3
      |2+3|
     2-----3
     6-----6

     26+36=5+2=(7)

WHAT IT IS (reading; every piece is checked below):
  Row 1-2 is the neighbor-difference step of 43: between the neighbours 4 and 3 goes |4 - 3| = 1, giving 4 1 3. This is the owner's own
  picture of the rule used in neighbor_difference_43_vs_seed45_2026_10_17.py (which assumed it). The next step puts |4 - 1| = 3 and
  |1 - 3| = 2 between the neighbours of 4 1 3, giving 4 3 1 2 3; the diagram's "2+3" is these two inserted digits, sum 5.
  Rows 4-5: the 2 and the 3 become 6 and 6. Two readings give exactly that: each inserted digit times the other (2 x 3 = 6, 3 x 2 = 6), or each
  outer digit of 43 plus the digit under it (4 + 2 = 6, 3 + 3 = 6). The picture does not say which.
  Read down, the left column is 2 over 6 = 26 and the right column is 3 over 6 = 36.
  26 + 36 = 62, digit root 8 (26 -> 8, 36 -> 9, 8 + 9 = 17 -> 8). The line says 5+2 = (7): that is the sum done column by column with no carry,
  tens 2 + 3 = 5 (the "5" of "2+3"), units 6 + 6 = 12 written as 2 -> 52 -> 5 + 2 = 7. With the carry kept it is 62 -> 8. The 7 is the digital
  root of the starting 43 (4 + 3 = 7).

FRAMEWORKS (gf37-audit): 26 IC; 36 NEG_H; 52 DARK_A; 62 SA_ST_B; 413 TESLA; 43123 SEED.
FALSIFICATION: any assertion failing.
"""


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def step(digits):
    out = [digits[0]]
    for a, b in zip(digits, digits[1:]):
        out += [abs(a - b), b]
    return out


s1 = step([4, 3])
s2 = step(s1)
assert s1 == [4, 1, 3] and s2 == [4, 3, 1, 2, 3]
inserted2 = [abs(4 - 1), abs(1 - 3)]               # the digits inserted into 4 1 3
assert inserted2 == [3, 2] and sum(inserted2) == 5 == 2 + 3
assert 2 * 3 == 6 == 3 * 2 and 4 + 2 == 6 == 3 + 3                                   # both readings of rows 4-5
assert 26 + 36 == 62 and dr(26) == 8 and dr(36) == 9 and dr(dr(26) + dr(36)) == 8 and dr(62) == 8
assert (2 + 3, (6 + 6) % 10) == (5, 2) and 5 + 2 == 7 and dr(52) == 7 and 6 + 6 == 12    # no-carry sum
assert dr(43) == 7 and 4 + 3 == 7 and 62 - 52 == 10
assert [n % 37 for n in (26, 36, 52, 62, 413, 43123)] == [26, 36, 15, 25, 6, 18]

if __name__ == "__main__":
    print("diagram: 43 -> 413 (|4-3| = 1) -> 43123 (3 and 2, sum 5); 26 and 36 down the columns; 26+36 = 62 (root 8), no-carry 52 -> 7 = root of 43")
