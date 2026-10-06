# CLASS: LEMMA
"""
M and W from pyramids (owner, 2026-10-06): "two pyramids next to each other
would be the M. If I were to put two pyramids in the creases that they
created, that would be our W."

Built the T325 way (theorem_325_rotation_walk_shapes_gf37.py,
rotation_shapes_new_stacks_2026_10_03.py): a pyramid is the chevron walk
0 1 2 1 0 on three columns, and the X is a chevron crossed with its mirror.

  M = two pyramids sharing a foot:        0 1 2 1 0 1 2 1 0
  W = pyramids sitting in M's creases,
      pointing down (W = 2 - M):          2 1 0 1 2 1 0 1 2

Reading taken: the pyramids in the creases point down, so W is M turned
over. Only this reading is built here.

M OVER W (both walks drawn on one grid):
  - The arms meet at every odd step (both at column 1), and each meeting is
    an X: one arm goes 0 -> 1 -> 2 while the other goes 2 -> 1 -> 0.
  - Between two meetings the arms open to opposite edges and close again,
    enclosing a diamond.
  So M over W = X, diamond, X, diamond, X, diamond, X: 4 X's, 3 diamonds. It
  is the T325 X picture (3.3 / .3. / 3.3) repeated.
  M + W = 2 in every row: the two walks are mirror images about the middle
  column.

FALSIFICATION: any assertion below failing.
"""
M = [0, 1, 2, 1, 0, 1, 2, 1, 0]
W = [2 - h for h in M]
assert W == [2, 1, 0, 1, 2, 1, 0, 1, 2]

# each pyramid is the T325 chevron
assert M[0:5] == [0, 1, 2, 1, 0] and M[4:9] == [0, 1, 2, 1, 0]

# meetings: exactly the odd steps, all in the middle column
meet = [t for t in range(9) if M[t] == W[t]]
assert meet == [1, 3, 5, 7] and all(M[t] == 1 for t in meet)

# every meeting is an X: the arms swap sides through it
for t in meet:
    assert (M[t - 1] - W[t - 1]) * (M[t + 1] - W[t + 1]) < 0

# between consecutive meetings the arms reach opposite edges: a diamond
diamonds = [(a, b) for a, b in zip(meet, meet[1:])
            if {M[(a + b) // 2], W[(a + b) // 2]} == {0, 2}]
assert len(meet) == 4 and len(diamonds) == 3

# mirror about the middle column
assert all(m + w == 2 for m, w in zip(M, W))

for t in range(9):
    row = ["."] * 3
    row[M[t]] = "M"
    row[W[t]] = "X" if M[t] == W[t] else "W"
    print(" ".join(row))
print("M over W: 4 X's, 3 diamonds. All assertions pass.")
