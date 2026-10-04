# CLASS: AUDIT
"""
Audit of supplied text (2026-10-04): a "21-row block-rotation matrix" of the blocks
246 / 572 / 135, each rotated through its three cyclic shifts. Mathematics only.

CORRECT
  B1 The blocks use exactly the 7 digits 1..7 (2 and 5 twice); each block's rotations are
     246 462 624, 572 725 257, 135 351 513.
  B2 Every 9-digit row has digit sum 35, root 8. Forced: rotating a block keeps its digits.
  B3 Consecutive rows differ by a multiple of 9 (root 9). Forced by B2: equal digit sums
     mean equal residues mod 9. The three differences given (216,153,216; 161,532,162;
     -377,532,000) are computed correctly.
  B4 Products 462*725*351 = 117,567,450 and 624*257*513 = 82,268,784 are right, and every
     block product is 0 mod 9. Forced: 135, 351, 513 are all multiples of 27.

WRONG
  B5 "3 x 7 = 21 rows complete the full rotation": choosing one rotation per block gives
     3 x 3 x 3 = 27 rows. The number 7 (the count of distinct digits) does not enter.
  B6 The table is not 21 distinct rows: row 16 repeats row 2 (462 725 351), so it has 20,
     and 7 of the 27 combinations never appear:
       246 257 135, 246 572 351, 462 572 351, 462 725 135, 462 725 513, 624 257 351,
       624 725 513
  B7 "Identity return" after row 21: rotating all three blocks together returns to 246 572
     135 after 3 steps; stepping through all 27 combinations is the group Z3 x Z3 x Z3
     (order 27). No arrangement has period 21.
  B8 Row 1 product: 246 x 572 x 135 = 18,996,120, not 18,995,940.
FALSIFICATION: any assertion failing.
"""
import itertools
from collections import Counter

ROWS = """246 572 135|462 725 351|624 257 513|246 725 513|462 257 135|624 572 351|246 257 351|
462 572 513|624 725 135|462 572 135|624 725 351|246 257 513|462 257 513|624 572 135|
246 725 351|462 725 351|624 257 135|246 572 513|624 572 513|246 725 135|462 257 351"""
rows = [tuple(r.split()) for r in ROWS.replace("\n", "").split("|")]
rot = lambda s: [s, s[1:] + s[0], s[2:] + s[:2]]
B = [rot("246"), rot("572"), rot("135")]
assert B == [["246", "462", "624"], ["572", "725", "257"], ["135", "351", "513"]]        # B1
assert set("246572135") == set("1234567")
val = lambda r: int("".join(r))
assert all(sum(map(int, "".join(r))) == 35 for r in rows)                                 # B2
assert [val(rows[1]) - val(rows[0]), val(rows[2]) - val(rows[1]), val(rows[3]) - val(rows[2])] == \
       [216_153_216, 161_532_162, -377_532_000]                                           # B3
assert all((val(a) - val(b)) % 9 == 0 for a, b in zip(rows[1:], rows))
assert 462 * 725 * 351 == 117_567_450 and 624 * 257 * 513 == 82_268_784                   # B4
assert all(x % 27 == 0 for x in (135, 351, 513))
allrows = set(itertools.product(*B))
assert len(allrows) == 27 and 3 * 7 == 21                                                 # B5
assert len(rows) == 21 and len(set(rows)) == 20                                           # B6
assert [r for r, c in Counter(rows).items() if c > 1] == [("462", "725", "351")]
assert len(allrows - set(rows)) == 7
joint = [tuple(b[k % 3] for b in B) for k in range(4)]                                      # B7
assert joint[3] == joint[0] and joint[1] != joint[0]
assert 246 * 572 * 135 == 18_996_120 != 18_995_940                                         # B8
