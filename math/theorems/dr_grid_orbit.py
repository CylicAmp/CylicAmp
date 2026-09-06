"""
DR Grid Orbit Structure
========================
Standard 3×3 grid:
  1 2 3
  4 5 6
  7 8 9

Rule: pair (a, b) → sum s = a+b → orbit = [DR(s×n) for n in 1..9]

Nine orbit types (one per DR value 1-9):
  DR 1: 1,2,3,4,5,6,7,8,9   (identity cycle, period 9)
  DR 2: 2,4,6,8,1,3,5,7,9
  DR 3: 3,6,9               (period 3, sovereign)
  DR 4: 4,8,3,7,2,6,1,5,9
  DR 5: 5,1,6,2,7,3,8,4,9
  DR 6: 6,3,9               (period 3, sovereign)
  DR 7: 7,5,3,1,8,6,4,2,9
  DR 8: 8,7,6,5,4,3,2,1,9   (AHL carrier, descending)
  DR 9: 9                   (fixed point, infinite period)

Column groups of the 3×3 grid:
  COL1 = (1,4,7)   DS=12  DR=3   (sovereign)
  COL2 = (2,5,8)   DS=15  DR=6   (sovereign)
  COL3 = (3,6,9)   DS=18  DR=9   (fixed point)
  The three columns ENCODE the sovereign set {3,6,9}.

Column × Row(123) pairings:
  COL1 × 123: sums (2,6,1)  →  pair_sum DR = 9  (fixed point)
  COL2 × 123: sums (3,7,2)  →  pair_sum DR = 3  (sovereign)
  COL3 × 123: sums (4,8,3)  →  pair_sum DR = 6  (sovereign)
  → Pairing any column with 123 produces the fixed point or a sovereign.

Row × Row pairings (rows as top/bottom):
  R1×R3: (1+7,2+8,3+9) = (8,10,12) → DRs (8,1,3) → sum DR = 3 (sovereign)
  R1×R2: (1+4,2+5,3+6) = (5,7,9)   → DRs (5,7,9) → sum DR = 3 (sovereign)
  R2×R3: (4+7,5+8,6+9) = (11,13,15) → DRs (2,4,6) → sum DR = 3 (sovereign)
  → All row-pair sum DRs = 3 (sovereign invariant).

Self-pairings:
  COL1×COL1: sums (2,8,5)   → pair_sum DR = 6  (sovereign)
  COL2×COL2: sums (4,1,7)   → pair_sum DR = 3  (sovereign)
  COL3×COL3: sums (6,3,9)   → pair_sum DR = 9  (fixed point)
  R1×R1:     sums (2,4,6)   → pair_sum DR = 3  (sovereign)
  R2×R2:     sums (8,1,3)   → pair_sum DR = 3  (sovereign)
  R3×R3:     sums (5,7,9)   → pair_sum DR = 3  (sovereign)
  → ALL self-pairings reduce to sovereign set {3,6,9}.
"""


def dr(n: int) -> int:
    return (n - 1) % 9 + 1 if n > 0 else 0


def orbit(s: int, length: int = 9) -> list:
    return [dr(s * n) for n in range(1, length + 1)]


# Nine orbit types
ORBITS = {k: orbit(k) for k in range(1, 10)}

# Groups
ROW1, ROW2, ROW3 = [1, 2, 3], [4, 5, 6], [7, 8, 9]
COL1, COL2, COL3 = [1, 4, 7], [2, 5, 8], [3, 6, 9]

# Column DRs encode {3,6,9}
assert dr(sum(COL1)) == 3
assert dr(sum(COL2)) == 6
assert dr(sum(COL3)) == 9


def pair_sums(A, B):
    return [a + b for a, b in zip(A, B)]


def pair_sum_dr(A, B):
    return dr(sum(pair_sums(A, B)))


# Column × 123 pairings produce fixed point or sovereigns
assert pair_sum_dr(COL1, ROW1) == 9
assert pair_sum_dr(COL2, ROW1) == 3
assert pair_sum_dr(COL3, ROW1) == 6

# Row × Row pairings all reduce to DR=3
assert pair_sum_dr(ROW1, ROW3) == 3
assert pair_sum_dr(ROW1, ROW2) == 3
assert pair_sum_dr(ROW2, ROW3) == 3

# Self-pairings all land in {3,6,9}
self_dr = {
    "COL1×COL1": pair_sum_dr(COL1, COL1),
    "COL2×COL2": pair_sum_dr(COL2, COL2),
    "COL3×COL3": pair_sum_dr(COL3, COL3),
    "R1×R1": pair_sum_dr(ROW1, ROW1),
    "R2×R2": pair_sum_dr(ROW2, ROW2),
    "R3×R3": pair_sum_dr(ROW3, ROW3),
}
assert all(v in {3, 6, 9} for v in self_dr.values())


def show_grid(label, A, B):
    sums = pair_sums(A, B)
    sums_dr = [dr(s) for s in sums]
    total = sum(sums)
    print(f"{label}")
    print(f"  Top:    {A}  DS={sum(A)} DR={dr(sum(A))}")
    print(f"  Bottom: {B}  DS={sum(B)} DR={dr(sum(B))}")
    for a, b, s, r in zip(A, B, sums, sums_dr):
        orb = orbit(s)[:9]
        print(f"  {a}+{b} = {s:>2} → DR={r}  orbit: {orb}")
    print(f"  Total {sum(A)}+{sum(B)}={total} → DR={dr(total)}")
    print()


if __name__ == "__main__":
    print("DR GRID ORBIT STRUCTURE")
    print("=" * 50)
    print()

    print("── NINE ORBIT TYPES ──")
    for k, orb in ORBITS.items():
        period = 3 if k in (3, 6) else (1 if k == 9 else 9)
        tag = " (period 3, sovereign)" if k in (3, 6) else \
              " (fixed point)" if k == 9 else \
              " (AHL)" if k == 8 else ""
        print(f"  DR {k}: {orb}{tag}")
    print()

    print("── COLUMN GROUPS ──")
    print(f"  COL1=(1,4,7)  DS=12  DR={dr(12)}  (sovereign)")
    print(f"  COL2=(2,5,8)  DS=15  DR={dr(15)}  (sovereign)")
    print(f"  COL3=(3,6,9)  DS=18  DR={dr(18)}  (fixed point)")
    print()

    print("── COLUMN × ROW(1,2,3) ──")
    show_grid("COL1 × 123", COL1, ROW1)
    show_grid("COL2 × 123", COL2, ROW1)
    show_grid("COL3 × 123", COL3, ROW1)

    print("── ROW × ROW ──")
    show_grid("R1 × R2", ROW1, ROW2)
    show_grid("R1 × R3", ROW1, ROW3)
    show_grid("R2 × R3", ROW2, ROW3)

    print("── SELF-PAIRINGS ──")
    show_grid("COL1 × COL1", COL1, COL1)
    show_grid("COL2 × COL2", COL2, COL2)
    show_grid("COL3 × COL3", COL3, COL3)

    print("── SOVEREIGN INVARIANT ──")
    print("  Every pairing within or across the 3×3 grid")
    print("  reduces to pair_sum DR ∈ {3,6,9}.")
    print(f"  Self-pairing DRs: {list(self_dr.values())}")
    print()
    print("All assertions passed.")
