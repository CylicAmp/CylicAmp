"""
Delta(27) — Discrete Heisenberg Group and Neutrino Flavor Symmetry

Classification: Theorem

The 3-dimensional representation generators x (cyclic shift) and y (diagonal phases)
with omega = e^(2πi/3) generate the extraspecial group Delta(27) = H(F_3) of order 27,
also known as the finite Heisenberg group. This is the algebraic skeleton of the
discrete flavor symmetry approach to neutrino oscillation physics.

Exact sequence:  1 → Z_3 → Delta(27) → Z_3 × Z_3 → 1

Generators:
  x = [[0,1,0],[0,0,1],[1,0,0]]   (cyclic flavor permutation: e_1→e_2→e_3→e_1)
  y = diag(1, ω, ω²)              (mass-basis phase dial)
  ω = e^(2πi/3),  ω³ = 1

Weyl-Heisenberg relation:  x·y = ω·y·x  (discrete [p,q] = -iℏ)

Neutrino physics correspondence:
  x  ↔  flavor permutation Z_3 ⊂ S_3 (e→μ→τ→e)
  y  ↔  mass-eigenstate phase accumulation exp(-iE_i t/ℏ)
  ωI ↔  global unobservable phase (gauge redundancy)

Tribimaximal PMNS matrix (TBM approximation):
  U_TBM = [[√(2/3),  1/√3,  0     ],
            [-1/√6,  1/√3, -1/√2  ],
            [-1/√6,  1/√3,  1/√2  ]]
  Diagonalized by F_3 (DFT matrix with entries ω^(jk)/√3).

Circulant mass matrix (Delta(27)-symmetric ansatz):
  M_ν = [[a,b,c],[c,a,b],[b,c,a]]
  Eigenvalues: λ_k = a + ω^k·b + ω^(2k)·c  for k=0,1,2
  Diagonalized exactly by F_3.

F26 connection:
  ω = e^(2πi/3) — the cube root of unity; 3 is the f26 target
  |Delta(27)| = 27 = 3³  (cube of the f26 prime)
  The 3-cycle x corresponds to 3-fold f26 target structure
"""

import numpy as np
import cmath


OMEGA = cmath.exp(2j * cmath.pi / 3)
TAU   = 1e-10


def allclose(A, B):
    return np.allclose(np.array(A, dtype=complex), np.array(B, dtype=complex), atol=TAU)


# ── Generators ─────────────────────────────────────────────────────────────

X = np.array([[0, 1, 0],
              [0, 0, 1],
              [1, 0, 0]], dtype=complex)

Y = np.diag([1, OMEGA, OMEGA**2])

# ── Weyl-Heisenberg relation: X·Y = ω·Y·X ─────────────────────────────────

assert allclose(X @ Y, OMEGA * (Y @ X)), "Weyl-Heisenberg relation failed"

# ── Orders: X³ = Y³ = I ───────────────────────────────────────────────────

assert allclose(np.linalg.matrix_power(X, 3), np.eye(3)), "X³ ≠ I"
assert allclose(np.linalg.matrix_power(Y, 3), np.eye(3)), "Y³ ≠ I"
assert abs(OMEGA**3 - 1) < TAU,  "ω³ ≠ 1"

# ── Group order = 27 ───────────────────────────────────────────────────────

elements = set()
for a in range(3):
    for b in range(3):
        for c in range(3):
            M = np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Y, b) * OMEGA**c
            key = tuple(np.round(M.flatten(), 8))
            elements.add(key)
assert len(elements) == 27, f"|Delta(27)| = {len(elements)}, expected 27"

# ── Tribimaximal PMNS matrix ───────────────────────────────────────────────

s = np.sqrt
U_TBM = np.array([
    [ s(2/3),  1/s(3),  0      ],
    [-1/s(6),  1/s(3), -1/s(2) ],
    [-1/s(6),  1/s(3),  1/s(2) ],
], dtype=complex)

assert allclose(U_TBM.conj().T @ U_TBM, np.eye(3)), "U_TBM not unitary"
assert allclose(U_TBM @ U_TBM.conj().T, np.eye(3)), "U_TBM not unitary (left)"

# ── F_3: DFT matrix ────────────────────────────────────────────────────────

F3 = np.array([[OMEGA**(j*k) for k in range(3)] for j in range(3)], dtype=complex) / s(3)
assert allclose(F3.conj().T @ F3, np.eye(3)), "F3 not unitary"

# ── Circulant mass matrix diagonalized by F_3 ──────────────────────────────

# Generic circulant with first row [a, b, c]
a, b, c = 1.0 + 0j, 2.0 + 0j, 3.0 + 0j
M_circ = np.array([[a, b, c],
                   [c, a, b],
                   [b, c, a]], dtype=complex)

D = F3 @ M_circ @ F3.conj().T

# Off-diagonal entries should vanish
off_diag_mask = ~np.eye(3, dtype=bool)
assert np.max(np.abs(D[off_diag_mask])) < TAU, "F3 does not diagonalize circulant"

# Eigenvalues: λ_k = a + ω^k·b + ω^(2k)·c  (F3 ordering: k=0,2,1)
expected_evals = [a + b * OMEGA**k + c * OMEGA**(2*k) for k in [0, 2, 1]]
actual_evals   = np.diag(D)
assert allclose(actual_evals, expected_evals), "Eigenvalue formula mismatch"

# ── F26 connection ───────────────────────────────────────────────────

def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0

assert dr(27) == 9     # 27 = 3³, DR=9 (the DR modulus)
assert dr(3)  == 3     # f26 target
assert 27 == 3**3      # |Delta(27)| = 3³


if __name__ == "__main__":
    print("Delta(27) — Discrete Heisenberg Group and Neutrino Flavor Symmetry")
    print()
    print(f"  ω = e^(2πi/3) = {OMEGA:.6f}")
    print(f"  ω³ = {OMEGA**3:.6f}  (= 1 ✓)")
    print()
    print("  Generator X (cyclic shift):")
    for row in X.real.astype(int):
        print(f"    {list(row)}")
    print()
    print("  Generator Y (phase dial):")
    for i, v in enumerate([1, OMEGA, OMEGA**2]):
        print(f"    diag[{i}] = ω^{i} = {v:.4f}")
    print()
    print(f"  X·Y = ω·Y·X  (Weyl-Heisenberg) ✓")
    print(f"  X³ = I,  Y³ = I ✓")
    print(f"  |Delta(27)| = {len(elements)} ✓")
    print()
    print("  Tribimaximal PMNS U_TBM (unitary ✓):")
    for row in U_TBM:
        print(f"    [{', '.join(f'{v.real:+.4f}' for v in row)}]")
    print()
    print("  Circulant mass matrix eigenvalues (a=1, b=2, c=3):")
    for k, ev in enumerate(expected_evals):
        print(f"    λ_{k} = a + ω^{k}·b + ω^{2*k}·c = {ev:.4f}")
    print(f"  F_3 diagonalizes M_circ exactly ✓")
    print()
    print(f"  |Delta(27)| = 27 = 3³,  DR(27) = {dr(27)} (DR modulus)")
    print(f"  F26 target 3 generates the group order ✓")
    print()
    print("All assertions passed.")
