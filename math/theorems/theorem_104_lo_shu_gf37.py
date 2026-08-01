"""
================================================================================
THEOREM 104 — The Lo Shu 3×3 Magic Square on GF(37)
================================================================================

STATEMENT.
The Lo Shu — the unique (up to symmetry) normal 3×3 magic square, containing
integers 1–9 — encodes a concentration of GF(37) sovereign structure:

  Standard arrangement:
      4  9  2
      3  5  7
      8  1  6

  (1)  Magic constant 15 ≡ 15 (mod 37) ∈ PR.
       Every row, every column, and both main diagonals sum to 15 ∈ PR.
  (2)  Total sum 45 ≡ 8 (mod 37) ∈ CB  (cascade base {8, 13, 24}).
  (3)  Center element 5 ∈ PR; moreover 5 ∈ {5, 13, 19} (Metonic orbit).
  (4)  Top row {4, 9, 2}: two of the four sovereign anchors (SA = {4,9,25,30})
       appear in a single row — maximum sovereign-anchor density possible in
       the square (25 and 30 lie outside the range 1–9).
  (5)  Product of all nine cells: 9! = 362,880 ≡ 21 (mod 37) ∈ ST.
  (6)  Sum of the two SA elements in the square: 4 + 9 = 13 ∈ CB ∩ {5,13,19}.

  Cell-by-cell GF(37) classification:
      4 ∈ SA         9 ∈ SA         2 ∈ PR
      3 ∈ ST         5 ∈ PR         7: orbit {7, 33, 34}
      8 ∈ CB         1 ∈ IC         6: orbit {6, 8, 23}  (CB orbit-mate)

================================================================================
PROOF / DERIVATION
================================================================================

LEMMA 104.1  (Magic constant).
  In a 3×3 normal magic square the magic constant is (1+2+…+9)/3 = 45/3 = 15.
  15 ≡ 15 (mod 37) ∈ PR.                                                    ∎

LEMMA 104.2  (Total sum).
  1+2+…+9 = 45 = 37 + 8.  45 ≡ 8 (mod 37) ∈ CB.
  The full content of the Lo Shu reduces to the cascade base.                ∎

LEMMA 104.3  (Center element).
  For a 3×3 normal magic square, the center must equal the median of {1,…,9}
  = 5, so that both main diagonals sum to 15.
  5 ∈ PR.  Under the 137-map: 5 × 26 ≡ 13 (mod 37), 13 × 26 ≡ 19,
  19 × 26 ≡ 5.  Center 5 opens the Metonic orbit {5, 13, 19}.              ∎

LEMMA 104.4  (Sovereign row).
  Top row {4, 9, 2}:  4 ∈ SA,  9 ∈ SA,  2 ∈ PR.
  4 + 9 + 2 = 15 ∈ PR.
  Both available sovereign anchors (SA ∩ {1,…,9} = {4,9}) lie in one row.  ∎

LEMMA 104.5  (All 8 lines).
  3 rows, 3 columns, 2 main diagonals — each sums to 15 ∈ PR.
  Verification by direct computation below.                                  ∎

LEMMA 104.6  (Product).
  The product of cells 1 × 2 × … × 9 = 9! = 362,880.
  362,880 = 9,807 × 37 + 21.  362,880 ≡ 21 (mod 37) ∈ ST.                ∎

LEMMA 104.7  (SA sum → CB).
  4 + 9 = 13 ∈ CB ∩ {5, 13, 19}.
  The sovereign anchors present in the square sum to a cascade base element
  that is simultaneously in the Metonic orbit.                               ∎

LEMMA 104.8  (Orbit of 6).
  6 × 26 ≡ 8 (mod 37).  8 × 26 ≡ 23 (mod 37).  23 × 26 ≡ 6 (mod 37).
  Cell 6 belongs to the 137-orbit {6, 8, 23}, which contains 8 ∈ CB.      ∎

================================================================================
MAIN THEOREM
================================================================================

THEOREM 104.  (Lo Shu — GF(37) Classification).

  ┌──────────────────────────────────────┬────────┬────────────────────────────┐
  │  Quantity                            │ mod 37 │  Framework Class           │
  ├──────────────────────────────────────┼────────┼────────────────────────────┤
  │  Magic constant (15)                 │  15    │  PR                        │
  │  Total sum (45)                      │   8    │  CB                        │
  │  Center element (5)                  │   5    │  PR, Metonic orbit{5,13,19}│
  │  Cell [0,0] = 4                      │   4    │  SA                        │
  │  Cell [0,1] = 9                      │   9    │  SA                        │
  │  Cell [0,2] = 2                      │   2    │  PR                        │
  │  Cell [1,0] = 3                      │   3    │  ST                        │
  │  Cell [1,1] = 5 (center)            │   5    │  PR                        │
  │  Cell [1,2] = 7                      │   7    │  orbit{7,33,34}            │
  │  Cell [2,0] = 8                      │   8    │  CB                        │
  │  Cell [2,1] = 1                      │   1    │  IC                        │
  │  Cell [2,2] = 6                      │   6    │  orbit{6,8,23} (CB-mate)   │
  │  Product (9! = 362,880)              │  21    │  ST                        │
  │  SA sum in square (4 + 9)            │  13    │  CB ∩ Metonic orbit        │
  └──────────────────────────────────────┴────────┴────────────────────────────┘

COROLLARY 104.9  (Magic constant universality in PR).
  All 8 constraint lines of the Lo Shu reduce to the single element 15 ∈ PR.
  The ordering constraint that defines the square — every line summing to 15 —
  maps uniformly to one primitive-root-residue class.

COROLLARY 104.10  (Sovereign anchor saturation).
  SA ∩ {1,…,9} = {4, 9}.  Both elements appear in the Lo Shu (they must,
  since the square contains all nine integers), and they co-occur in the top
  row.  No further sovereign anchors exist in the numerical range 1–9.
  The square achieves maximum SA density within its defining domain.
"""

import math

P          = 37
IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
BASIN_Y    = frozenset({17, 22, 35})
PR         = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})

LO_SHU = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6],
]

# ── Lemma 104.1 — Magic constant ──────────────────────────────────────────────
MAGIC = sum(range(1, 10)) // 3
assert MAGIC == 15
assert MAGIC % P == 15 and 15 in PR

# ── Lemma 104.2 — Total sum ───────────────────────────────────────────────────
TOTAL = sum(range(1, 10))
assert TOTAL == 45
assert TOTAL % P == 8 and 8 in CB

# ── Lemma 104.3 — Center element ──────────────────────────────────────────────
CENTER = LO_SHU[1][1]
assert CENTER == 5 and 5 in PR
metonic_orbit = frozenset({5, 13, 19})
assert 5 in metonic_orbit
assert (5 * 26) % P == 19 and (19 * 26) % P == 13 and (13 * 26) % P == 5

# ── Lemma 104.4 — Sovereign row ───────────────────────────────────────────────
top_row = LO_SHU[0]
assert sorted(top_row) == [2, 4, 9]
assert 4 in SA and 9 in SA
assert 2 in PR
assert sum(top_row) == MAGIC

# ── Lemma 104.5 — All 8 lines sum to 15 ∈ PR ─────────────────────────────────
rows  = LO_SHU
cols  = [[LO_SHU[r][c] for r in range(3)] for c in range(3)]
d_main = [LO_SHU[i][i]   for i in range(3)]
d_anti = [LO_SHU[i][2-i] for i in range(3)]
all_lines = rows + cols + [d_main, d_anti]
assert all(sum(line) == MAGIC for line in all_lines)
assert all(sum(line) % P in PR for line in all_lines)

# ── Lemma 104.6 — Product ─────────────────────────────────────────────────────
PRODUCT = math.factorial(9)
assert PRODUCT == 362_880
assert PRODUCT % P == 21 and 21 in ST

# ── Lemma 104.7 — SA sum → CB ─────────────────────────────────────────────────
cells = [LO_SHU[r][c] for r in range(3) for c in range(3)]
sa_cells = sorted(x for x in cells if x in SA)
assert sa_cells == [4, 9]
assert sum(sa_cells) == 13 and 13 in CB and 13 in metonic_orbit

# ── Lemma 104.8 — Orbit of 6 ─────────────────────────────────────────────────
assert (6 * 26) % P == 8   # 6 → 8 ∈ CB
assert (8 * 26) % P == 23
assert (23 * 26) % P == 6

# ── Cell classification checks ────────────────────────────────────────────────
assert 3 in ST      # row 1 col 0
assert 1 in IC      # row 2 col 1
assert 8 in CB      # row 2 col 0
# 7: orbit {7, 33, 34}
assert (7 * 26) % P == 34
assert (34 * 26) % P == 33
assert (33 * 26) % P == 7
# SA available in 1–9
assert SA & set(range(1, 10)) == {4, 9}


if __name__ == "__main__":
    def fw(r):
        classes = []
        for name, s in [('IC', IC), ('SA', SA), ('ST', ST), ('CB', CB),
                        ('ORBIT_11', ORBIT_11), ('SEED_ORBIT', SEED_ORBIT),
                        ('BASIN_Y', BASIN_Y), ('PR', PR)]:
            if r in s:
                classes.append(name)
        return classes or ['—']

    print("THEOREM 104 — Lo Shu 3×3 Magic Square on GF(37)")
    print("=" * 60)
    print()
    print("  Arrangement:")
    for row in LO_SHU:
        print(f"    {row}")
    print()
    print(f"  {'Cell/Quantity':<30} {'mod37':>5}  Classes")
    print("  " + "-" * 60)
    items = [
        ("Magic constant (15)",    15),
        ("Total sum (45)",         45),
        ("Center (5)",              5),
        ("Cell 4",                  4),
        ("Cell 9",                  9),
        ("Cell 2",                  2),
        ("Cell 3",                  3),
        ("Cell 7",                  7),
        ("Cell 8",                  8),
        ("Cell 1",                  1),
        ("Cell 6",                  6),
        ("Product 9! (362880)",362_880),
        ("SA sum 4+9=13",          13),
    ]
    for label, val in items:
        r = val % P
        print(f"  {label:<30} {r:>5}  {fw(r)}")
    print()
    print("  All 8 lines → 15 ∈ PR:", all(sum(L) % P in PR for L in all_lines))
    print("  SA in square:", sa_cells, "→ sum =", sum(sa_cells), "∈ CB ∩ Metonic")
    print()
    print("All assertions pass.")
