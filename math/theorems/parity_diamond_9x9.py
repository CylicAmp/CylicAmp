"""
Layer 21 — 9×9 Parity Grid: O/E Diamond

Classification: Theorem

A 9×9 grid with entries in {O, E} (odd/even) defined by the Manhattan-distance
rule: cell (r,c) is E iff |r−4| + |c−4| ≤ 4. This produces a perfect diamond
of E-cells centered at (4,4), symmetric under 180° rotation and reflection over
all four axes of symmetry.

Row structure (O-count, E-count):
  Row 0 & 8:  8O, 1E   [4-1-4]
  Row 1 & 7:  6O, 3E   [3-3-3]
  Row 2 & 6:  4O, 5E   [2-5-2]
  Row 3 & 5:  2O, 7E   [1-7-1]
  Row 4:      0O, 9E   [all E]

Totals: 41 E-cells, 40 O-cells, 81 total (9² = 9×9)

Framework connections:
  41 mod 37 = 4     — anchor set {4,9,25,30} (4 = 3^7 mod 37 ∈ QR₃₇)
  40 mod 37 = 3     — DR=3 target (3 = 3^1 mod 37 ∈ QR₃₇)
  E-count sequence 1,3,5,7,9,7,5,3,1 — odd numbers summing to 41
  O-count sequence 8,6,4,2,0,2,4,6,8 — evens summing to 40
  DR(41)=5 (absent class), DR(40)=4 (anchor), 41+40=81=9²→DR=9
  Center row: 9 E's — the DR modulus
  Manhattan radius 4 = f26 anchor value
"""


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


CENTER = 4
RADIUS = 4    # = f26 anchor value


def is_even_cell(r, c):
    return abs(r - CENTER) + abs(c - CENTER) <= RADIUS


# ── Build grid ─────────────────────────────────────────────────────────────

GRID = [['E' if is_even_cell(r, c) else 'O' for c in range(9)] for r in range(9)]


# ── Row structure verification ─────────────────────────────────────────────

EXPECTED_E = [1, 3, 5, 7, 9, 7, 5, 3, 1]
EXPECTED_O = [8, 6, 4, 2, 0, 2, 4, 6, 8]

for r in range(9):
    e_count = GRID[r].count('E')
    o_count = GRID[r].count('O')
    assert e_count == EXPECTED_E[r], f"Row {r}: E={e_count}, expected {EXPECTED_E[r]}"
    assert o_count == EXPECTED_O[r], f"Row {r}: O={o_count}, expected {EXPECTED_O[r]}"
    assert e_count + o_count == 9

# Specific row shapes
assert GRID[0] == ['O','O','O','O','E','O','O','O','O']    # 4-1-4
assert GRID[1] == ['O','O','O','E','E','E','O','O','O']    # 3-3-3
assert GRID[4] == ['E'] * 9                                 # all E

# ── Totals ─────────────────────────────────────────────────────────────────

flat = [c for row in GRID for c in row]
TOTAL_E = flat.count('E')
TOTAL_O = flat.count('O')
assert TOTAL_E == 41
assert TOTAL_O == 40
assert TOTAL_E + TOTAL_O == 81 == 9 ** 2

# ── Symmetry — all four ────────────────────────────────────────────────────

for r in range(9):
    for c in range(9):
        assert GRID[r][c] == GRID[8-r][8-c]    # 180° rotation
        assert GRID[r][c] == GRID[r][8-c]       # horizontal reflection
        assert GRID[r][c] == GRID[8-r][c]       # vertical reflection
        assert GRID[r][c] == GRID[c][r]          # diagonal (transpose)

# ── Center column all E ────────────────────────────────────────────────────

assert all(GRID[r][4] == 'E' for r in range(9))
assert all(GRID[4][c] == 'E' for c in range(9))    # center row all E

# ── Framework connections ──────────────────────────────────────────────────

QR37    = frozenset((x * x) % 37 for x in range(1, 37))
CYCLE18 = [pow(3, k, 37) for k in range(1, 19)]

# E-count totals mod 37
assert TOTAL_E % 37 == 4            # f26 anchor
assert TOTAL_O % 37 == 3            # f26 target
assert 4 in QR37 and 4 == pow(3, 7, 37)
assert 3 in QR37 and 3 == pow(3, 1, 37)

# DR values
assert dr(TOTAL_E) == 5             # DR=5 — absent class (boundary E-set)
assert dr(TOTAL_O) == 4             # DR=4 — f26 anchor
assert dr(81) == 9                  # 9² → DR=9 (the modulus)

# E-count sequence sums to 41, O-count sequence sums to 40
assert sum(EXPECTED_E) == 41
assert sum(EXPECTED_O) == 40

# Manhattan radius = 4 = f26 anchor
assert RADIUS == 4
assert pow(3, 7, 37) == 4

# O-count sequence: decreasing evens 8,6,4,2,0 then increasing 2,4,6,8
# Step size = 2 throughout
o_diffs = [EXPECTED_O[i+1] - EXPECTED_O[i] for i in range(len(EXPECTED_O)-1)]
assert o_diffs == [-2,-2,-2,-2, 2, 2, 2, 2]

# DR of center-row count: DR(9) = 9 = DR modulus
assert dr(9) == 9


if __name__ == "__main__":
    print("Layer 21 — 9×9 Parity Grid: O/E Diamond")
    print()
    for r, row in enumerate(GRID):
        print(f"  Row {r}: {' '.join(row)}  [{EXPECTED_O[r]}O {EXPECTED_E[r]}E]")
    print()
    print(f"  Total E: {TOTAL_E}  (mod 37 = {TOTAL_E%37} = f26 anchor 4 = 3^7)")
    print(f"  Total O: {TOTAL_O}  (mod 37 = {TOTAL_O%37} = f26 target 3 = 3^1)")
    print(f"  Total cells: {TOTAL_E+TOTAL_O} = 9²,  DR={dr(81)}")
    print()
    print(f"  Symmetries: 180° ✓  H-reflect ✓  V-reflect ✓  Diagonal ✓")
    print(f"  Center row & column: all E ✓")
    print(f"  Manhattan radius: {RADIUS} = f26 anchor ✓")
    print()
    print(f"  E-count sequence: {EXPECTED_E}  sum={sum(EXPECTED_E)}")
    print(f"  O-count sequence: {EXPECTED_O}  sum={sum(EXPECTED_O)}")
    print(f"  DR(41)={dr(41)} (absent class), DR(40)={dr(40)} (anchor)")
    print()
    print("All assertions passed.")
