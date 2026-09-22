"""
Sovereign Matrix (DR form) — Characteristic Polynomial

The 9×9 Sovereign Matrix M (DR form) has column layout:

  Cols 1, 9    → v₁ = DR(r·1) = [1,2,3,4,5,6,7,8,9]
  Cols 2, 5, 8 → v₂ = DR(r·2) = [2,4,6,8,1,3,5,7,9]
  Cols 3, 7    → v₃ = DR(r·3) = [3,6,9,3,6,9,3,6,9]
  Cols 4, 6    → v₄ = DR(r·4) = [4,8,3,7,2,6,1,5,9]

Three groups of identical columns → M = V·Wᵀ (outer-product sum).
  V (9×4): [v₁ | v₂ | v₃ | v₄]  — rank 4 (verified algebraically)
  W (9×4): disjoint indicator columns  — rank 4

Structural results (verified below):
  rank(M) = 4   → null-space dimension 5  → ≥5 zero eigenvalues
  Wᵀ·V (4×4)    → rank 3 (rows 0 and 3 are identical: [10,11,12,13])
                → one additional zero eigenvalue
  Total zero eigenvalues: 6
  Characteristic polynomial: λ⁶ · p₃(λ)
"""

import numpy as np
import sympy as sp


def digital_root(n: int) -> int:
    return (n - 1) % 9 + 1 if n > 0 else 0


# --- Build M (user's construction verbatim) ---
M = np.zeros((9, 9), dtype=int)
for r in range(1, 10):
    for c in range(1, 10):
        if c == 5:
            val = digital_root(2 * r)
        else:
            m = c if c <= 4 else 10 - c
            val = digital_root(r * m)
        M[r - 1, c - 1] = val

# --- Rank check ---
rank = int(np.linalg.matrix_rank(M))
assert rank == 4, f"expected rank 4, got {rank}"

# --- Wᵀ·V cross-check for the outer-product decomposition ---
# Column vectors
v1 = M[:, 0].copy()   # DR(r·1), same as col 9
v2 = M[:, 1].copy()   # DR(r·2), same as cols 5 and 8
v3 = M[:, 2].copy()   # DR(r·3), same as col 7
v4 = M[:, 3].copy()   # DR(r·4), same as col 6

V = np.column_stack([v1, v2, v3, v4])   # 9×4
# Indicator weight vectors (1-indexed column → 0-indexed row in W)
# w₁ picks cols 1,9 → rows 0,8
# w₂ picks cols 2,5,8 → rows 1,4,7
# w₃ picks cols 3,7 → rows 2,6
# w₄ picks cols 4,6 → rows 3,5
W = np.zeros((9, 4), dtype=int)
for idx in (0, 8):      W[idx, 0] = 1
for idx in (1, 4, 7):   W[idx, 1] = 1
for idx in (2, 6):      W[idx, 2] = 1
for idx in (3, 5):      W[idx, 3] = 1

assert np.all(V @ W.T == M), "M ≠ V·Wᵀ"

WtV = W.T @ V   # 4×4
assert np.linalg.matrix_rank(WtV) == 3, "Wᵀ·V should have rank 3"
assert np.all(WtV[0] == WtV[3]), "rows 0 and 3 of Wᵀ·V should be equal"

# --- Characteristic polynomial (sympy, exact) ---
lam = sp.Symbol("lambda")
M_sp = sp.Matrix(M.tolist())
char_poly_raw = M_sp.charpoly(lam)
char_poly = sp.expand(char_poly_raw.as_expr())

# Assert λ⁶ divides the characteristic polynomial
# (coefficients of λ⁰ through λ⁵ must all be zero)
poly_obj = sp.Poly(char_poly, lam)
coeffs = poly_obj.all_coeffs()   # [a₉, a₈, ..., a₁, a₀]
assert len(coeffs) == 10, "expected degree-9 polynomial"
for power in range(6):           # check λ⁰ … λ⁵ coefficients
    assert coeffs[-(power + 1)] == 0, (
        f"coeff of λ^{power} should be 0, got {coeffs[-(power+1)]}"
    )

# Degree-3 cofactor p₃ such that char_poly = λ⁶ · p₃
cofactor_coeffs = coeffs[:4]     # a₉, a₈, a₇, a₆ → λ³, λ², λ¹, λ⁰ of cofactor
p3 = sp.Poly(cofactor_coeffs, lam).as_expr()

# Confirm: λ⁶ · p₃ == char_poly
assert sp.expand(lam**6 * p3 - char_poly) == 0

# The three non-zero eigenvalues are roots of p₃
nonzero_roots = sp.solve(p3, lam)


if __name__ == "__main__":
    print("Sovereign Matrix (DR form) — 9×9")
    print()
    print("M =")
    print(M)
    print()
    print(f"rank(M) = {rank}")
    print()
    print("Wᵀ·V =")
    print(WtV)
    print(f"  rank(Wᵀ·V) = {np.linalg.matrix_rank(WtV)}  "
          f"(rows 0 and 3 equal: {WtV[0].tolist()})")
    print()
    print("Characteristic polynomial (expanded):")
    print(f"  {char_poly}")
    print()
    print("Factored form:")
    print(f"  {sp.factor(char_poly)}")
    print()
    print("Degree-3 cofactor p₃  (char_poly = λ⁶ · p₃):")
    print(f"  p₃(λ) = {p3}")
    print()
    print("Non-zero eigenvalues of M (roots of p₃):")
    for r in nonzero_roots:
        print(f"  λ = {r}  ≈  {complex(r):.6f}")
    print()
    print("All assertions passed.")
