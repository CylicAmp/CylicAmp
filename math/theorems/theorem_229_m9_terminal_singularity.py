"""
Theorem 229: M_9 — Terminal Singularity Operator on ℂ⁹
Author: Michael Warren Song (CyclicAmp)

The multiplication-by-9 operator M_9 acts on the 9-dimensional space ℂ⁹ (or ℤ⁹).
M_3 is the multiplication-by-3 operator.  Their matrix structure and composition
are verified, and every dimensional parameter connects through GF(37).

=== OPERATOR DEFINITIONS ===

Index convention: basis vectors e_1,...,e_9; stored as 0-indexed (e_9 = index 8).
Modular convention: (9j mod 9) = 0 is identified with 9 (i.e., index 8).

M_3:  e_j → e_{3j mod 9}   (triadic collapse; 0→9 convention)
  Row 2 (e_3):  columns 0,3,6 = 1  (j=1,4,7 map here)
  Row 5 (e_6):  columns 1,4,7 = 1  (j=2,5,8 map here)
  Row 8 (e_9):  columns 2,5,8 = 1  (j=3,6,9 map here)
  All other entries = 0.

M_9:  e_j → e_{9j mod 9} = e_9   (every basis vector collapses to e_9)
  Row 8 (e_9):  all nine columns = 1
  All other entries = 0.

=== PROPERTIES ===

RANK AND KERNEL:
  rank(M_9) = 1   → image = span{e_9} (one-dimensional Spine)
  dim(ker M_9) = 8  → 8-dimensional null space
  rank(M_3) = 3   → image = span{e_3, e_6, e_9}
  dim(ker M_3) = 6  → 6-dimensional null space

EIGENSTRUCTURE OF M_9:
  Eigenvalues: {0, 1}  (rank-1 projection: spec(M_9) = {0,1})
  Eigenspace for λ=1: span{e_9}       (1-dimensional)
  Eigenspace for λ=0: ker(M_9)        (8-dimensional)

NIL-IDEMPOTENT CHAIN:
  M_3 is a 2-step path to idempotency:
    M_3²  = M_9    (two doublings of the triadic collapse = total collapse)
    M_9²  = M_9    (idempotent: applying M_9 twice = applying it once)

  This is NOT nilpotency (M_3^k ≠ 0).  It is:
    Step 1 (M_3):  collapse from 9 directions into 3 (ranks 3, 6, 9)
    Step 2 (M_9):  collapse from 3 directions into 1 (rank 9 only)

ACTION ON A VECTOR:
  M_9 · v = (Σᵢ vᵢ) · e_9    — sums all amplitudes onto e_9.

ABSORBING PROPERTY (column-stochastic T):
  For any matrix T with each column summing to a constant c:
    M_9 · T = c · M_9
  In particular: for any permutation matrix or column-stochastic T with c=1:
    M_9 · T = M_9   (M_9 is a right absorbing element)
  This includes the identity I, all permutation matrices, M_3, and M_9 itself.

=== GF(37) DIMENSIONAL STRUCTURE ===

Every dimensional parameter of the M_9 / M_3 system is a named GF(37) element:

Parameter        Value   GF(37) classification
Space dimension    9     ∈ SA (sovereign anchor)  — SA_ST_A orbit {9, 12, 16}
rank(M_9)          1     ∈ IC (identity cycle)    — orbit {1, 10, 26}
dim(ker M_9)       8     ∈ CASCADE ∩ TESLA        — orbit {6, 8, 23} = TESLA
rank(M_3)          3     ∈ ST (sovereign target)  — orbit {3, 4, 30} = C3
dim(ker M_3)       6     ∈ TESLA                  — orbit {6, 8, 23} = TESLA

The rank of M_3 is a sovereign target (3∈ST).
The kernel of M_3 is a TESLA element (6∈TESLA).
The kernel of M_9 is a CASCADE/TESLA element (8∈CASCADE∩TESLA).

=== COLLAPSE CHAIN IN GF(37) ===

The cascade 3 → 6 → 9 (digital root chain) corresponds to:
  Step 1 (×3 operator): rank 3∈ST, image in {e_3, e_6, e_9}
  Step 2 (×9 terminal): rank 1∈IC, image in {e_9}

GF(37) orbits of the chain nodes under the 26-map:
  3 → orbit C3 = {3, 4, 30}   (3∈ST, 4∈SA, 30∈SA∩ST)
  6 → orbit TESLA = {6, 8, 23}  (6∈TESLA, 8∈CASCADE∩TESLA)
  9 → orbit SA_ST_A = {9, 12, 16}  (9∈SA, 12∈ST)

The terminal image axis 9 generates the SA_ST_A orbit.
The intermediate image set {3,6,9} is not closed under the 26-map; it reaches
{C3, TESLA, SA_ST_A}, three distinct named orbits.

=== IDEMPOTENCY AND PROJECTION THEORY ===

M_9 satisfies M_9² = M_9: it is a PROJECTION onto span{e_9}.
By the spectral theorem for projections:
  spec(M_9) ⊆ {0, 1}  ✓
  trace(M_9) = rank(M_9) = 1  ✓
  Any vector v decomposes as v = (M_9·v) + (v - M_9·v)
    where M_9·v ∈ image(M_9) and (v - M_9·v) ∈ ker(M_9).

M_9 is NOT an orthogonal projection (M_9 ≠ M_9ᵀ):
  M_9ᵀ has all 1s in the last COLUMN (not row).
  Orthogonal projection onto span{e_9} = e_9·e_9ᵀ / ||e_9||² = diag(0,...,0,1).

M_9 is an oblique projection: it collapses along directions NOT orthogonal to
the image span{e_9}.  The kernel and image are complementary but not orthogonal.
"""

import numpy as np
from numpy.linalg import matrix_rank, eigvals

# ── GF(37) constants ──────────────────────────────────────────────────────────
P    = 37
MULT = 26

SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
SEED    = {18, 24, 32}
IC      = {1, 10, 26}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}
D7      = {7, 33, 34}
SA_ST_A = {9, 12, 16}
C3      = {3, 4, 30}


def build_M9(n=9) -> np.ndarray:
    """M_9: e_j -> e_n (last basis vector).  Row n-1 all ones."""
    M = np.zeros((n, n), dtype=int)
    M[n - 1, :] = 1
    return M


def build_M3(n=9) -> np.ndarray:
    """M_3: e_j -> e_{3j mod n} (with 0 -> n convention)."""
    M = np.zeros((n, n), dtype=int)
    for j in range(1, n + 1):
        dest = (3 * j) % n or n   # 0 mod n -> n
        M[dest - 1, j - 1] = 1
    return M


def orbit_26(x: int) -> list:
    """Three-cycle of x under f(n) = 26n mod 37."""
    orb = []
    for _ in range(3):
        orb.append(x)
        x = (x * MULT) % P
    return orb


def run_assertions():
    n = 9
    M9 = build_M9(n)
    M3 = build_M3(n)

    # ── M_9 structure ─────────────────────────────────────────────────────────
    # All-ones in last row, zeros elsewhere
    for i in range(n):
        for j in range(n):
            expected = 1 if i == n - 1 else 0
            assert M9[i, j] == expected

    # ── Rank-Nullity ─────────────────────────────────────────────────────────
    assert matrix_rank(M9) == 1
    assert n - matrix_rank(M9) == 8   # dim(ker M_9)
    assert matrix_rank(M3) == 3
    assert n - matrix_rank(M3) == 6   # dim(ker M_3)

    # ── GF(37) classification of dimensions ──────────────────────────────────
    assert n == 9 and 9 in SA
    assert matrix_rank(M9) == 1 and 1 in IC
    assert (n - matrix_rank(M9)) == 8 and 8 in CASCADE and 8 in TESLA
    assert matrix_rank(M3) == 3 and 3 in ST
    assert (n - matrix_rank(M3)) == 6 and 6 in TESLA

    # ── Nil-idempotent chain: M_3^2 = M_9, M_9^2 = M_9 ──────────────────────
    assert np.array_equal(M3 @ M3, M9),  "M_3^2 must equal M_9"
    assert np.array_equal(M9 @ M9, M9),  "M_9 must be idempotent"

    # ── Eigenvalues of M_9: {0, 1} ───────────────────────────────────────────
    evals = sorted(set(round(e.real, 8) for e in eigvals(M9.astype(float))))
    assert evals == [0.0, 1.0], f"eigenvalues of M_9 = {evals}"

    # ── trace(M_9) = rank(M_9) = 1 ───────────────────────────────────────────
    assert int(np.trace(M9)) == 1

    # ── Action: M_9·v = sum(v)·e_9 ───────────────────────────────────────────
    v = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    result = M9 @ v
    expected = np.zeros(n, dtype=int)
    expected[n - 1] = sum(v)
    assert np.array_equal(result, expected)

    # ── Absorbing property for column-stochastic T ────────────────────────────
    # Permutation matrices
    I = np.eye(n, dtype=int)
    assert np.array_equal(M9 @ I, M9)
    assert np.array_equal(M9 @ M3, M9)
    assert np.array_equal(M9 @ M9, M9)   # also M_9 itself

    # ── GF(37) orbits of chain nodes ─────────────────────────────────────────
    assert set(orbit_26(9)) == SA_ST_A
    assert set(orbit_26(3)) == C3
    assert set(orbit_26(6)) == TESLA

    # 9 ∈ SA: sovereign anchor
    assert 9 in SA
    assert 3 in ST    # sovereign target
    assert 6 in TESLA

    # ── Projection theory: oblique (M_9 ≠ M_9^T) ─────────────────────────────
    assert not np.array_equal(M9, M9.T)   # oblique, not orthogonal
    # Orthogonal projection onto span{e_9} would be diag(0,...,0,1)
    ortho = np.zeros((n, n), dtype=int)
    ortho[n - 1, n - 1] = 1
    assert not np.array_equal(M9, ortho)

    print("All assertions passed.")
    print()
    print("M_9 — TERMINAL SINGULARITY OPERATOR (T229)")
    print()
    print(f"  Space dimension:   9  ∈ SA (sovereign anchor); orbit SA_ST_A = {sorted(SA_ST_A)}")
    print(f"  rank(M_9):         1  ∈ IC;  dim(ker M_9) = 8 ∈ CASCADE∩TESLA")
    print(f"  rank(M_3):         3  ∈ ST;  dim(ker M_3) = 6 ∈ TESLA")
    print()
    print(f"  Nil-idempotent chain:")
    print(f"    M_3^2 = M_9  ✓")
    print(f"    M_9^2 = M_9  ✓  (idempotent)")
    print()
    print(f"  Eigenvalues of M_9: {{0, 1}}  (oblique rank-1 projection)")
    print(f"  trace(M_9) = {int(np.trace(M9))} = rank(M_9)  ✓")
    print()
    print(f"  Absorbing: M_9 ∘ T = M_9 for all column-stochastic T")
    print()
    print(f"  GF(37) cascade chain:")
    print(f"    3 (rank M_3) ∈ ST  → orbit C3 = {sorted(C3)}")
    print(f"    6 (ker M_3)  ∈ TESLA → orbit TESLA = {sorted(TESLA)}")
    print(f"    9 (image axis) ∈ SA → orbit SA_ST_A = {sorted(SA_ST_A)}")
    print(f"    The 3→6→9 digital-root chain maps to ST→TESLA→SA in GF(37).")


if __name__ == "__main__":
    run_assertions()
