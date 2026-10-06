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

ONE LINE HOLDS BOTH (owner, 2026-10-06: "Whenever you create an M, you also
create a W ... Half of the M is M, and the other half of it is W", with a
drawing of one zigzag run between two digit rows).
  - Run the pyramid line on: 0 1 2 1 0 1 2 1 0 1 2 ...
  - Moving it over by half a pyramid (2 steps) gives exactly the turned-over
    line: h(t+2) = 2 - h(t).
  - So W is not a second line. It is the same line read from half a pyramid
    later, and every M carries a W.
  - Inside M = /\/\, the middle strokes \/ are half a W. Inside W = \/\/,
    the middle strokes /\ are half an M.

THE TWO DIGIT ROWS IN THE DRAWING:
      top     -0-00-0-00     zero groups 1, 2, 1, 2
      bottom  00-0-00-0-0    zero groups 2, 1, 2, 1 (then a 1 that starts the next 2)
  - The bottom row's first ten marks are the top row read backwards: the
    mirror.
  - Top is the 1-2 alternation and bottom the 2-1 alternation. These are the
    12 / 21 strings of left_anchor_and_four_panel_shapes_supplied_audit_2026_10_04.py.

UPSIDE DOWN (owner, 2026-10-06: "whenever I make an M, I'm making an upside
down W. And whenever I make a W, I'm making an upside M").
  - Turning W over gives M, and turning M over gives W.
  - Turning over twice returns the start.
  - M and W each read the same backwards, so turning upside down, rotating a
    half turn and moving half a pyramid all give the same line.

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

# one line holds both: shifting by half a pyramid = turning over
line = [(0, 1, 2, 1)[t % 4] for t in range(40)]
assert all(line[t + 2] == 2 - line[t] for t in range(38))
assert line[2:11] == W
# every M carries a W in its middle, and every W an M
assert M[2:7] == W[0:5] and W[2:7] == M[0:5]

flip = lambda h: [2 - v for v in h]
assert flip(W) == M and flip(M) == W and flip(flip(M)) == M
assert M == M[::-1] and W == W[::-1]                       # each reads the same backwards
assert flip(M)[::-1] == W == line[2:11]                     # half turn = turn over = half-pyramid shift

top, bot = "-0-00-0-00", "00-0-00-0-0"
assert bot[:10] == top[::-1]
assert [len(g) for g in top.split("-") if g] == [1, 2, 1, 2]
assert [len(g) for g in bot.split("-") if g] == [2, 1, 2, 1, 1]

for t in range(9):
    row = ["."] * 3
    row[M[t]] = "M"
    row[W[t]] = "X" if M[t] == W[t] else "W"
    print(" ".join(row))
print("M over W: 4 X's, 3 diamonds. All assertions pass.")
