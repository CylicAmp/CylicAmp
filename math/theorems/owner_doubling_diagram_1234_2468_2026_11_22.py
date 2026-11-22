# CLASS: AUDIT
"""
The owner's diagram of 2026-11-22 (an image made with Grok, the owner's tool): two columns of nodes joined row by row,
    1 - 2
    2 - ?      (the right node of row 2 is covered by the hexagon)
    3 - 6
    4 - 8
with red/green and blue links down each column, orange staircases stepping down to the right (from 1, from 2, from 3 to
8), a triangle from 1 and 4 to a point on the right, and a hexagon with a red web inside it at the centre.

RIGHT (what the numbers show):
  each right node is twice the left: 1 -> 2, 3 -> 6, 4 -> 8, so row 2 reads 2 -> 4 if the covered node is 4 (asked)
  row sums n + 2n = 3n: 3, 6, 9, 12 -> roots 3, 6, 9, 3 -- every row lands in 3, 6, 9 (forced: 3n)
  columns 1 + 2 + 3 + 4 = 10 and 2 + 4 + 6 + 8 = 20, total 30 -> 3
  the four corners are 1, 2, 4, 8 -- the doubling chain, 1 + 2 + 4 + 8 = 15 -> 6
CONNECTIONS:
  owner_work/TERMS.md "DOUBLE EVEN BY 4" (#270): "1248 / 751". By 9 the doubling chain runs 1 2 4 8 7 5 and back to 1
    (16 -> 7, 32 -> 5, 64 -> 1): the corners are its first four, and 751 is the rest of it.
  owner_369_729_189_rotations_flips_2026_11_19.py (What's not 369): the row sums are all 3, 6 or 9.
ASKED (each blocks a check): the number under the hexagon at row 2 on the right; what the hexagon with its web, the
  triangle, and the staircases stand for.
Frameworks: records/gf37_audit_doubling_diagram_2026_11_22.txt.

FALSIFICATION: any assertion failing.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
dr = lambda n: 1 + (n - 1) % 9
left, right = [1, 2, 3, 4], [2, None, 6, 8]
assert all(r == 2 * l for l, r in zip(left, right) if r is not None)
full = [2 * l for l in left]
assert [l + r for l, r in zip(left, full)] == [3, 6, 9, 12] and [dr(l + r) for l, r in zip(left, full)] == [3, 6, 9, 3]
assert sum(left) == 10 and sum(full) == 20 and dr(30) == 3
corners = [left[0], right[0], left[-1], right[-1]]
assert sorted(corners) == [1, 2, 4, 8] and sum(corners) == 15 and dr(15) == 6
chain = [pow(2, k, 9) for k in range(7)]
assert chain == [1, 2, 4, 8, 7, 5, 1] and chain[:4] == [1, 2, 4, 8] and chain[4:6] + [chain[6]] == [7, 5, 1]
assert "DOUBLE EVEN BY 4" in (ROOT / "owner_work" / "TERMS.md").read_text()
assert (ROOT / "records" / "gf37_audit_doubling_diagram_2026_11_22.txt").exists()

if __name__ == "__main__":
    print("diagram: right = 2 x left; rows 3 6 9 12 -> 3 6 9 3; corners 1 2 4 8 (doubling chain 1 2 4 8 7 5)")
