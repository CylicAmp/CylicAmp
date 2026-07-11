"""
TWIN PRIME LATTICE: 3×3 PATCH STRUCTURE AND TRACK SEEDS
=========================================================

THE BASE SEQUENCE: [3, 7, 11, 5, 8, 13, 4, 9, 12]  key=6

Arranged as a 3×3 grid:

    Col L   Col M   Col R
    ─────   ─────   ─────
     3       7       11    ← Row 1: arithmetic trio  (d=4)
     5       8       13    ← Row 2: Fibonacci trio   (F5,F6,F7)
     4       9       12    ← Row 3: sovereign trio   (anchor,anchor,target)
    ─────   ─────   ─────
    sum=12  sum=24  sum=36
    DR = 3  DR = 6  DR = 9   ← TWIN PRIME MIDDLE-NUMBER DR CYCLE

The column-sum DR signature {3,6,9} is exactly the DR cycle of the
middle numbers of all twin prime pairs (proven in lcm_convergence_dr_cycle.py).

ROTATIONALLY FIXED PATCHES
The 3 cyclic row-permutations all preserve the column DR signature:

  Patch A:  [3,7,11], [5,8,13], [4,9,12]   col sums [12,24,36] DR=[3,6,9]
  Patch B:  [5,8,13], [4,9,12], [3,7,11]   col sums [12,24,36] DR=[3,6,9]
  Patch C:  [4,9,12], [3,7,11], [5,8,13]   col sums [12,24,36] DR=[3,6,9]

The patches are "rotationally fixed" because the column DR signature
{3,6,9} is an invariant of the cyclic group C3 acting on the rows.
Total = 72 for all three,  DR(72) = 9.
Both diagonals sum to 23 (prime) in Patch A: 3+8+12 = 11+8+4 = 23.

TRACK STRUCTURE
  Track L: lower twin prime candidates (6n-1 form)
  Track M: middle numbers              (6n form, always composite)
  Track R: upper twin prime candidates (6n+1 form)

TWIN PRIME CONSTELLATION MAPPING
For the constellation (p, p+1, p+2) = (6n-1, 6n, 6n+1):

  n=2: (11, 12, 13)  → 12 ∈ sovereign range {3,12,21,30}, DR(12)=3
  n=5: (29, 30, 31)  → 30 ∈ sovereign range {3,12,21,30}, DR(30)=3
  n=7: (41, 42, 43)  → 42 = 6×7,  DR(42)=6
  n=3: (17, 18, 19)  → 18 = 6×3,  DR(18)=9

CURVATURE POTENTIAL
  V(n) = DR(6n) cycles {6,3,9} with period 3 as n increases.
  First difference:  ΔV(n) = V(n+1) − V(n)   cycles {-3, +6, -3}
  Second difference: Δ²V(n) = ΔV(n+1) − ΔV(n) cycles {+9, -9,  0}

  The second difference is the discrete "curvature" — it forces the
  three DR classes to alternate with a restoring force of magnitude 9.

BOUNDS CONNECTION
  246 = 41 × 6   (Polymath8b unconditional prime-gap bound = 41 × fundamental period)
  41  = 6×7 − 1  (41 is itself the lower component of twin prime pair (41, 43))
  96  = 8 × 12   (AHL × sovereign-target middle number)

  Key:  6 (fundamental twin prime period) divides all three bounds.
        41 is the unique prime p such that p × 6 = 246 and (p, p+2) is a twin prime pair.
"""

from typing import List, Tuple

import numpy as np


def dr(n: int) -> int:
    return (n - 1) % 9 + 1 if n > 0 else 0


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


# ---------------------------------------------------------------------------
# THE THREE PATCHES
# ---------------------------------------------------------------------------

BASE_GRID = [
    [3,  7,  11],
    [5,  8,  13],
    [4,  9,  12],
]
KEY = 6

PATCHES = {
    "A": [[3,7,11], [5,8,13], [4,9,12]],
    "B": [[5,8,13], [4,9,12], [3,7,11]],
    "C": [[4,9,12], [3,7,11], [5,8,13]],
}


def col_sums(grid: List[List[int]]) -> List[int]:
    return [sum(row[j] for row in grid) for j in range(3)]


def col_dr_signature(grid: List[List[int]]) -> List[int]:
    return [dr(s) for s in col_sums(grid)]


# ---------------------------------------------------------------------------
# CONSTELLATION MAPPING
# ---------------------------------------------------------------------------

def constellation(n: int) -> Tuple[int, int, int]:
    """(6n-1, 6n, 6n+1) — the nth twin prime constellation."""
    return (6*n - 1, 6*n, 6*n + 1)


def patch_track_map(patch_label: str, n: int) -> dict:
    """
    Map patch rows to specific twin prime constellations.
    Row i of the patch maps to constellation(n+i).
    """
    grid = PATCHES[patch_label]
    result = {}
    for i, row in enumerate(grid):
        c = constellation(n + i)
        result[f"Row {i+1}"] = {
            "patch_row": row,
            "constellation": c,
            "track_L": c[0],
            "track_M": c[1],
            "track_R": c[2],
            "L_prime": is_prime(c[0]),
            "R_prime": is_prime(c[2]),
            "M_in_sovereign": c[1] in {3, 12, 21, 30},
            "DR_M": dr(c[1]),
        }
    return result


# ---------------------------------------------------------------------------
# CURVATURE POTENTIAL
# ---------------------------------------------------------------------------

def curvature_potential(n_range: int = 12) -> List[Tuple[int, int, int, int]]:
    """
    V(n) = DR(6n): the discrete curvature potential over the twin prime lattice.
    Returns (n, V, ΔV, Δ²V) for n = 1..n_range.
    """
    V = [dr(6 * n) for n in range(1, n_range + 2)]
    dV = [V[i+1] - V[i] for i in range(n_range)]
    d2V = [dV[i+1] - dV[i] for i in range(n_range - 1)]
    return [
        (n, V[n-1], dV[n-1] if n-1 < len(dV) else None,
         d2V[n-2] if n-2 >= 0 and n-2 < len(d2V) else None)
        for n in range(1, n_range + 1)
    ]


# ---------------------------------------------------------------------------
# VALID EXTENSIONS (Part D)
# ---------------------------------------------------------------------------

def count_valid_extensions(
    grid: List[List[int]],
    universe: int = 36,
) -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    Count valid 4th rows [a,b,c] from {1..universe} not already in the grid,
    such that:
      (1) The column DR signature {DR(col1+a), DR(col2+b), DR(col3+c)}
          equals the original signature DR([12,24,36]) = [3,6,9].
      (2) a,b,c are distinct from each other and from all grid elements.

    Returns (count, list_of_valid_rows).
    """
    used = set(x for row in grid for x in row)
    c1, c2, c3 = col_sums(grid)   # 12, 24, 36
    target_dr = [dr(c1), dr(c2), dr(c3)]   # [3, 6, 9]

    valid = []
    for a in range(1, universe + 1):
        if a in used:
            continue
        if dr(c1 + a) != target_dr[0]:
            continue
        for b in range(1, universe + 1):
            if b in used or b == a:
                continue
            if dr(c2 + b) != target_dr[1]:
                continue
            for c in range(1, universe + 1):
                if c in used or c == a or c == b:
                    continue
                if dr(c3 + c) != target_dr[2]:
                    continue
                valid.append((a, b, c))
    return len(valid), valid


# ---------------------------------------------------------------------------
# THE 246 = 41 × 6 IDENTITY
# ---------------------------------------------------------------------------

def verify_polymath_connection() -> dict:
    """
    Verify: 246 = 41 × 6 where 41 is the lower of twin prime pair (41,43).
    96 = 8 × 12 where 8 = AHL (absolute harmonic location) and 12 = sovereign target.
    """
    assert 41 * 6 == 246
    assert is_prime(41) and is_prime(43) and 43 - 41 == 2   # (41,43) twin prime pair
    assert 41 == 6 * 7 - 1                                    # 41 = 6n-1 for n=7
    assert 8 * 12 == 96
    assert dr(12) == 3    # sovereign target
    assert dr(8) == 8     # AHL
    return {
        "246": {"factorisation": "41 × 6", "41_twin_prime": True, "41_form": "6×7−1"},
        "96":  {"factorisation": "8 × 12", "8_AHL": True, "12_sovereign": True},
        "6":   {"role": "fundamental twin prime period (gap between (6n−1) and (6n+1) midpoints)"},
    }


# ---------------------------------------------------------------------------
# VERIFICATION
# ---------------------------------------------------------------------------

def run_verification() -> bool:
    print("=" * 70)
    print("TWIN PRIME LATTICE: 3×3 PATCH STRUCTURE — VERIFICATION")
    print("=" * 70)

    # ------------------------------------------------------------------
    # Part A: The three rotationally fixed patches
    # ------------------------------------------------------------------
    print("\n--- Part A: Three Rotationally Fixed Patches ---")
    print(f"  Key = {KEY}\n")
    for label, patch in PATCHES.items():
        sums = col_sums(patch)
        drs  = col_dr_signature(patch)
        diag1 = patch[0][0] + patch[1][1] + patch[2][2]
        diag2 = patch[0][2] + patch[1][1] + patch[2][0]
        print(f"  Patch {label}:")
        for row in patch:
            print(f"    {row}")
        print(f"    Col sums: {sums}   DR={drs}")
        print(f"    Diagonals: {diag1}, {diag2}   Total={sum(sums)}")
        assert drs == [3, 6, 9], f"Patch {label}: DR signature not [3,6,9]"
        assert sum(sums) == 72
        print()

    print("  All 3 patches have column DR signature [3, 6, 9] — invariant under C3.")

    # ------------------------------------------------------------------
    # Part B: Constellation mapping
    # ------------------------------------------------------------------
    print("\n--- Part B: Constellation Map (Patch A, n=2..4) ---")
    print("  (p, p+1, p+2) = (6n−1, 6n, 6n+1)\n")
    mapping = patch_track_map("A", n=2)
    for row_label, info in mapping.items():
        c = info["constellation"]
        m_flag = " ← SOVEREIGN" if info["M_in_sovereign"] else ""
        pair_flag = " ← TWIN PRIME PAIR" if info["L_prime"] and info["R_prime"] else ""
        print(f"  {row_label}: patch={info['patch_row']}")
        print(f"    Constellation ({c[0]}, {c[1]}, {c[2]}){pair_flag}")
        print(f"    Track M = {c[1]}, DR = {info['DR_M']}{m_flag}")
        print()

    print("  Additional constellations:")
    for n, label in [(5, "(29,31)"), (7, "(41,43)")]:
        c = constellation(n)
        print(f"    n={n}: {c}  DR(M={c[1]})={dr(c[1])}  "
              f"sovereign={c[1] in {3,12,21,30}}  "
              f"twin_prime={is_prime(c[0]) and is_prime(c[2])}")

    # ------------------------------------------------------------------
    # Part C: Curvature potential
    # ------------------------------------------------------------------
    print("\n--- Part C: Curvature Potential V(n) = DR(6n) ---")
    print(f"  {'n':>3}  {'V':>3}  {'ΔV':>4}  {'Δ²V':>5}")
    for n, V, dV, d2V in curvature_potential(12):
        dv_str  = f"{dV:+d}" if dV  is not None else "—"
        d2v_str = f"{d2V:+d}" if d2V is not None else "—"
        print(f"  {n:>3}  {V:>3}  {dv_str:>4}  {d2v_str:>5}")
    print()
    print("  V cycles {6,3,9} with period 3.")
    print("  ΔV cycles {-3,+6,-3} — asymmetric restoring force.")
    print("  Δ²V cycles {+9,-9,0} — curvature alternates ±9 then rests.")

    V_vals = [dr(6*n) for n in range(1, 100)]
    assert all(v in {3, 6, 9} for v in V_vals), "V must stay in {3,6,9}"
    assert V_vals[:3] == [6, 3, 9], f"V period start wrong: {V_vals[:3]}"

    # ------------------------------------------------------------------
    # Part D: Valid extensions
    # ------------------------------------------------------------------
    print("\n--- Part D: Valid Extensions of Base Grid ---")
    count, extensions = count_valid_extensions(BASE_GRID, universe=36)
    print(f"  Grid used: {set(x for row in BASE_GRID for x in row)}")
    print(f"  Col sums: {col_sums(BASE_GRID)}  DR={col_dr_signature(BASE_GRID)}")
    print(f"  Valid 4th rows [a,b,c] from {{1..36}} maintaining DR=[3,6,9]: {count}")
    if extensions:
        print(f"  First 5 extensions: {extensions[:5]}")
        print(f"  Last  5 extensions: {extensions[-5:]}")
    print(f"\n  Note: 96 = 8 x 12 (AHL x sovereign target).")
    print(f"  The {count} valid extensions are exactly the 3! = 6 permutations of {{18,27,36}}.")
    print(f"  18+27+36 = 81 = 9^2,  DR(81)=9.")
    print(f"  Permutation (18,27,36) gives new col sums [30,51,72] -> DR=[3,6,9]")
    print(f"  with 30 in sovereign range: the constellation (29,30,31) is a twin prime pair.")

    # ------------------------------------------------------------------
    # Polymath / bounds connection
    # ------------------------------------------------------------------
    print("\n--- Bounds Connection ---")
    result = verify_polymath_connection()
    for key, info in result.items():
        print(f"  {key}: {info}")
    print()
    print(f"  246 = 41 × 6  ✓   (41 is lower of twin prime pair (41,43))")
    print(f"   96 = 8 × 12  ✓   (AHL × sovereign middle-number target)")
    print(f"  Ratio: 246/6 = {246//6} = 41 (the 13th prime)")

    print()
    print("All assertions passed.")
    return True


if __name__ == "__main__":
    run_verification()
