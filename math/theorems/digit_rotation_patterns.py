"""
3-DIGIT ROTATION PATTERNS AND D4 DIRECTIONAL VARIATIONS
============================================================

VALID NUMBERS: 127, 137, 147, 157, 167, 187, 197
  Range 117–197, no zeros, no repeated digits.
  117 excluded (two 1s), 177 excluded (two 7s).
  Seven numbers total.

  Sum = 1119   DR(1119) = 3
  Digital roots: 1, 2, 3, 4, 5, 7, 8
  First three (127, 137, 147) have DR 1, 2, 3  → 1+2+3 = 6

PARTITION GROUPS — each trio covers all of {1,2,...,9} exactly once:
  {127, 349, 568}  sum = 1044
  {137, 268, 594}  sum =  999
  {147, 258, 369}  sum =  774
  {147, 258, 369} = partition by residue mod 3: {1,4,7}∣{2,5,8}∣{3,6,9}

3×3 GRID OF PERMUTATIONS OF {1,6,7}:
  167 / 617 / 671
  as a digit matrix:
      1 6 7
      6 1 7
      6 7 1

D4 DIRECTIONAL VARIATIONS (8 orientations = 4 rotations × 2 mirrors):
  R0          167 / 617 / 671  ✓ valid
  R0+FH       761 / 716 / 176  ✓ valid
  R90         661 / 716 / 177  ✗ repeated digits
  R90+FH      166 / 617 / 771  ✗ repeated digits
  R180        176 / 716 / 761  ✓ valid
  R180+FH     671 / 617 / 167  ✓ valid
  R270        771 / 617 / 166  ✗ repeated digits
  R270+FH     177 / 716 / 661  ✗ repeated digits

  Total D4 orientations: 8
  Valid (all rows have distinct digits): 4

  The 4 valid orientations form {e, R180, FH, R180·FH} — the Klein
  four-group K4, a subgroup of D4 of index 2.

  The 6 permutations of {1,6,7} split into two complementary triples:
    A = {167, 617, 671}   (used by R0 and R180+FH)
    B = {176, 716, 761}   (used by R0+FH and R180)
  Each valid orientation uses exactly one triple for its rows.
"""

from typing import List, Tuple


VALID_1X7 = [127, 137, 147, 157, 167, 187, 197]

BASE_GRID = [
    [1, 6, 7],
    [6, 1, 7],
    [6, 7, 1],
]

PARTITION_GROUPS = [
    [127, 349, 568],
    [137, 268, 594],
    [147, 258, 369],
]


def digital_root(n: int) -> int:
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def _rot90cw(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    return [[g[n - 1 - j][i] for j in range(n)] for i in range(n)]


def _flip_h(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    return [[g[i][n - 1 - j] for j in range(n)] for i in range(n)]


def d4_orientations(grid: List[List[int]]) -> List[Tuple[str, List[List[int]]]]:
    """Return all 8 D4 orientations of a square grid."""
    result = []
    g = [row[:] for row in grid]
    for k in range(4):
        deg = k * 90
        result.append((f"R{deg}", [row[:] for row in g]))
        result.append((f"R{deg}+FH", _flip_h([row[:] for row in g])))
        g = _rot90cw(g)
    return result


def row_number(row: List[int]) -> int:
    return row[0] * 100 + row[1] * 10 + row[2]


def has_distinct_digits(row: List[int]) -> bool:
    return len(set(row)) == len(row)


def run_verification() -> bool:
    print("=" * 66)
    print("DIGIT ROTATION PATTERNS — VERIFICATION")
    print("=" * 66)

    # 1. Valid numbers and sum
    total = sum(VALID_1X7)
    drs = [digital_root(n) for n in VALID_1X7]
    assert total == 1119, f"sum mismatch: {total}"
    assert digital_root(total) == 3, f"DR(sum) mismatch: {digital_root(total)}"
    assert drs == [1, 2, 3, 4, 5, 7, 8], f"DR sequence mismatch: {drs}"
    assert 1 + 2 + 3 == 6
    print(f"  Valid numbers: {VALID_1X7}")
    print(f"  Sum = {total}  DR = {digital_root(total)}")
    print(f"  DRs = {drs}  (first three: 1+2+3 = 6)")

    # 2. Partition groups
    print()
    all_digits_ok = True
    for grp in PARTITION_GROUPS:
        digits = sorted("".join(str(n) for n in grp))
        ok = digits == list("123456789")
        if not ok:
            all_digits_ok = False
        mark = "✓" if ok else "✗"
        print(f"  {mark} {grp}  sum={sum(grp)}  covers {{1..9}}: {ok}")
    assert all_digits_ok

    # 3. D4 orientations
    print()
    print("  D4 ORIENTATIONS OF 167/617/671:")
    orientations = d4_orientations(BASE_GRID)
    valid_labels = []
    for label, orient in orientations:
        rows = [row_number(row) for row in orient]
        ok = all(has_distinct_digits(row) for row in orient)
        mark = "✓" if ok else "✗"
        if ok:
            valid_labels.append(label)
        print(f"    {mark} {label:8s}  {rows[0]} / {rows[1]} / {rows[2]}")

    valid_count = len(valid_labels)
    assert valid_count == 4, f"expected 4 valid orientations, got {valid_count}"
    assert set(valid_labels) == {"R0", "R0+FH", "R180", "R180+FH"}, (
        f"valid set mismatch: {valid_labels}"
    )

    print()
    print(f"  Total D4 orientations: 8")
    print(f"  Valid (distinct digits): {valid_count}  — form Klein four-group K4 < D4")
    print()
    print("  Complementary triples of {1,6,7} permutations:")
    print("    A = {167, 617, 671}  (R0, R180+FH)")
    print("    B = {176, 716, 761}  (R0+FH, R180)")

    print()
    print("All assertions passed.")
    return True


if __name__ == "__main__":
    run_verification()
