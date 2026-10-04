# math/theorems/e8_cartan_audit.py
"""
E8 Cartan Matrix — Verification

The Cartan matrix of a semisimple Lie algebra encodes inner products between
simple roots. For E8 (rank 8, simply-laced, trivial center):

  C_ii = 2   (all diagonal entries)
  C_ij ≤ 0  (off-diagonal entries)
  C_ij = 0  iff C_ji = 0  (symmetry for simply-laced)

─────────────────────────────────────────────────────────────────────────────
DYNKIN DIAGRAM — E8 (branch at node 3, 1-indexed)
─────────────────────────────────────────────────────────────────────────────
  1 — 2 — 3 — 4 — 5 — 6 — 7
          |
          8

  Arms from branch node 3: length 2 (toward 1), length 4 (toward 7), length 1 (node 8)
  Required for E8: arm lengths {1, 2, 4}  ✓
  (E6 would be {1,2,2}; E7 would be {1,2,3})

─────────────────────────────────────────────────────────────────────────────
DETERMINANT
─────────────────────────────────────────────────────────────────────────────
  For a simply-connected semisimple group with trivial center:
    |det(C)| = order of center = 1
  E8 has trivial center → det = 1  (exact integer)

─────────────────────────────────────────────────────────────────────────────
EIGENVALUES
─────────────────────────────────────────────────────────────────────────────
  For a simply-laced finite-type algebra with Coxeter number h and exponents mⱼ:
    λⱼ = 2 − 2cos(π mⱼ / h)

  E8: h = 30, exponents = {1, 7, 11, 13, 17, 19, 23, 29}

  λ_min = 2 − 2cos(π/30)  ≈ 0.010956
  λ_max = 2 + 2cos(π/30)  ≈ 3.989044

  All eigenvalues strictly positive → positive definite → finite-type  ✓

  Full spectrum (sorted):
    [0.010956, 0.51371, 1.186527, 1.584177,
     2.415823, 2.813473, 3.48629,  3.989044]

  Note: [0.05, 3.95] is WRONG — a previously circulated value that was not
  computed from the formula. Correct range is [0.011, 3.989].
"""

import numpy as np
import math

E8_CARTAN = np.array([
    [ 2, -1,  0,  0,  0,  0,  0,  0],
    [-1,  2, -1,  0,  0,  0,  0,  0],
    [ 0, -1,  2, -1,  0,  0,  0, -1],   # branch at node 3
    [ 0,  0, -1,  2, -1,  0,  0,  0],
    [ 0,  0,  0, -1,  2, -1,  0,  0],
    [ 0,  0,  0,  0, -1,  2, -1,  0],
    [ 0,  0,  0,  0,  0, -1,  2,  0],
    [ 0,  0, -1,  0,  0,  0,  0,  2],   # node 8 connected only to node 3
], dtype=int)

# ── Theoretical eigenvalue computation ────────────────────────────────────────

H = 30   # Coxeter number for E8
E8_EXPONENTS = [1, 7, 11, 13, 17, 19, 23, 29]

THEORETICAL_EIGENVALUES = sorted(
    2 - 2 * math.cos(math.pi * m / H) for m in E8_EXPONENTS
)

LAMBDA_MIN_THEORY = THEORETICAL_EIGENVALUES[0]   # ≈ 0.010956
LAMBDA_MAX_THEORY = THEORETICAL_EIGENVALUES[-1]  # ≈ 3.989044

# ── Numerical verification ─────────────────────────────────────────────────────

det_E8      = float(np.linalg.det(E8_CARTAN))
eigvals_E8  = sorted(np.linalg.eigvals(E8_CARTAN).real.tolist())
lambda_min  = eigvals_E8[0]
lambda_max  = eigvals_E8[-1]
pos_def     = all(e > 0 for e in eigvals_E8)

# ── Assertions ────────────────────────────────────────────────────────────────

# Determinant = 1 (trivial center)
assert abs(det_E8 - 1.0) < 1e-8, f"det = {det_E8}, expected 1.0"

# Positive definite
assert pos_def, f"Not positive definite; min eigenvalue = {lambda_min}"

# Eigenvalue range matches theory
assert abs(lambda_min - LAMBDA_MIN_THEORY) < 1e-6, \
    f"λ_min mismatch: numeric={lambda_min:.6f}, theory={LAMBDA_MIN_THEORY:.6f}"
assert abs(lambda_max - LAMBDA_MAX_THEORY) < 1e-6, \
    f"λ_max mismatch: numeric={lambda_max:.6f}, theory={LAMBDA_MAX_THEORY:.6f}"

# Previously circulated wrong range [0.05, 3.95] — verify it is wrong
assert lambda_min < 0.02,  "min eigenvalue is NOT in [0.05, ...]; it is ~0.011"
assert lambda_max > 3.98,  "max eigenvalue is NOT in [..., 3.95]; it is ~3.989"

# Symmetry (simply-laced: C is symmetric)
assert np.allclose(E8_CARTAN, E8_CARTAN.T), "Cartan matrix not symmetric"

# Diagonal entries all 2
assert all(E8_CARTAN[i, i] == 2 for i in range(8)), "Diagonal not all 2"

# Off-diagonal entries ≤ 0
for i in range(8):
    for j in range(8):
        if i != j:
            assert E8_CARTAN[i, j] <= 0, f"Off-diagonal entry [{i},{j}] = {E8_CARTAN[i,j]} > 0"

# Branch at node 3 (0-indexed: row/col 2): connected to nodes 2, 4, 8 (0-indexed: 1, 3, 7)
assert E8_CARTAN[2, 1] == -1
assert E8_CARTAN[2, 3] == -1
assert E8_CARTAN[2, 7] == -1
assert E8_CARTAN[7, 2] == -1   # symmetric

# Node 8 (0-indexed: 7) connected ONLY to node 3 (0-indexed: 2)
assert list(E8_CARTAN[7]) == [0, 0, -1, 0, 0, 0, 0, 2]


if __name__ == "__main__":
    print("E8 Cartan Matrix — Verification")
    print()
    print(f"  Determinant:       {det_E8:.10f}  (expected: 1.0)  ✓")
    print(f"  Positive definite: {pos_def}  ✓")
    print(f"  λ_min (numeric):   {lambda_min:.6f}")
    print(f"  λ_min (theory):    {LAMBDA_MIN_THEORY:.6f}  ✓")
    print(f"  λ_max (numeric):   {lambda_max:.6f}")
    print(f"  λ_max (theory):    {LAMBDA_MAX_THEORY:.6f}  ✓")
    print()
    print("  Full spectrum (sorted):")
    for i, (th, nu) in enumerate(zip(THEORETICAL_EIGENVALUES, eigvals_E8)):
        exp = E8_EXPONENTS[i]
        print(f"    m={exp:2d}: theory={th:.6f}  numeric={nu:.6f}  "
              f"diff={abs(th-nu):.2e}")
    print()
    print("  Dynkin diagram: 1-2-3-4-5-6-7 with 8 branching from 3")
    print("  Arm lengths from branch: 2 (toward 1), 4 (toward 7), 1 (node 8) → E8 ✓")
    print()
    print("All assertions passed.")
