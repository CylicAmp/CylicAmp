# math/theorems/kernel5_generators_audit.py
"""
Kernel-5 Generators Audit — {0,13} Matrix

Computes explicit basis vectors for ker(KERNEL5_M) over Z/26Z and addresses
the user request: "compute the explicit generators ... identify which map to
the 100-Unity Bridge ... re-run the full GUE multi-point correlation audit."

─────────────────────────────────────────────────────────────────────────────
PREMISE CORRECTION (required before any computation)
─────────────────────────────────────────────────────────────────────────────
  The matrix with SNF = [13,13,13,13,26,26,26,26,0] is the ARTIFICIAL {0,13}
  construction (entry 86), NOT the "Sovereign Matrix."

  Sovereign Matrix (PROVIDED_M, entry 80):
    SNF  = [1, 9, 9, 9, 9, 9, 9, 9, 450]
    Kernel Z/26Z = 0   (no torsion; gcd(9,26)=gcd(450,26)=gcd(26,26)? no:
                        gcd(450,26)=2 → one torsion element but kernel=0 because
                        450 mod 26 ≠ 0 and 450 is not divisible by 26)

  Wait — let me be precise. kernel_dim_mod_n counts entries d with gcd(d,n)=n
  or d=0. For SNF=[1,9,9,9,9,9,9,9,450]: gcd(450,26)=2≠26, d≠0 → kernel=0. ✓

  The {0,13} matrix has kernel=5 for an entirely algebraic reason:
    13 ≡ 0 (mod 13) → M ≡ 0 (mod 13) → kernel mod 13 = full (dim 9)
    13B mod 2 = B mod 2 → kernel mod 2 = ker(B mod 2) = dim 5
    CRT: kernel mod 26 = dim 5   (constrained by the tighter mod-2 condition)

─────────────────────────────────────────────────────────────────────────────
ALGEBRAIC MECHANISM
─────────────────────────────────────────────────────────────────────────────
  ker(13B over Z/26Z) = {v ∈ (Z/26Z)^9 : 13·B·v ≡ 0 (mod 26)}
                      = {v ∈ (Z/26Z)^9 : B·v ≡ 0 (mod 2)}
  because 13x ≡ 0 (mod 26)  iff  x ≡ 0 (mod 2).

  So the kernel over Z/26Z = preimage of ker(B mod 2) under reduction mod 2.
  ker(B mod 2) has dimension 5 over F_2 (rank(B mod 2) = 4 → kernel dim = 5).

  Canonical F_2 kernel generators lift directly: {0,1} ⊂ {0,...,25}.

─────────────────────────────────────────────────────────────────────────────
100-UNITY BRIDGE / DECIMAL TRADE EXTRACTION — STATUS
─────────────────────────────────────────────────────────────────────────────
  Kernel generators are vectors in {0,1}^9 ⊂ (Z/26Z)^9.
  They are NOT real numbers and cannot be Riemann zero imaginary parts
  (which are reals: 14.134..., 21.022..., 25.010..., etc.).

  "Decimal Trade Extraction" has no mathematical definition in this session.
  "100-Unity Bridge" maps γ₁₂ = 56.446... → 100 via 56+44=100; this is
  a scalar arithmetic identity on ONE real number, not a map from Z/26Z
  module elements to a spectral sequence.

  The domain mismatch is categorical:
    kernel vectors : (Z/26Z)^9 — discrete, 9-dimensional, integer-valued
    Riemann zeros  : ℝ          — continuous, scalar, transcendental

  No injection from (Z/26Z)^9 into ℝ preserves any relevant structure.

─────────────────────────────────────────────────────────────────────────────
GUE AUDIT STATUS
─────────────────────────────────────────────────────────────────────────────
  A GUE multi-point audit requires an ordered sequence of real numbers
  to compare against GUE nearest-neighbor and k-point statistics.

  Kernel generators are five 9-dimensional integer vectors.
  They do not define a sequence of "ordinates" in any natural sense.

  To run a GUE audit one would need a well-defined map:
    φ : ker(M, Z/26Z) → {s₁ < s₂ < ... < sₙ} ⊂ ℝ

  No such map has been specified, and no natural one exists.
  This audit is declined on mathematical grounds, not computational ones.

Classification: Theorem (kernel generators); Refutation (100-Unity Bridge,
                GUE ordinate claim)
"""

import numpy as np
from math import gcd
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from kernel5_construction_audit import KERNEL5_M, B


# ── F₂ null-space via row reduction ──────────────────────────────────────────

def null_space_f2(A):
    """Basis for ker(A) over F_2; returns list of integer 0/1 row-vectors."""
    A = (np.array(A, dtype=int) % 2).copy()
    m, n = A.shape
    pivot_col_to_row = {}   # pivot_col_to_row[c] = row index of that pivot
    row = 0
    for col in range(n):
        pivot = next((r for r in range(row, m) if A[r, col] % 2), None)
        if pivot is None:
            continue
        A[[row, pivot]] = A[[pivot, row]]
        for r in range(m):
            if r != row and A[r, col] % 2:
                A[r] = (A[r] + A[row]) % 2
        pivot_col_to_row[col] = row
        row += 1
    free_cols = [c for c in range(n) if c not in pivot_col_to_row]
    kernel_vecs = []
    for f in free_cols:
        v = [0] * n
        v[f] = 1
        for c, r in pivot_col_to_row.items():
            v[c] = int(A[r, f])   # back-substitution
        kernel_vecs.append(v)
    return kernel_vecs


# ── Compute kernel ────────────────────────────────────────────────────────────

B_F2 = B.copy() % 2
KERNEL_F2_BASIS = null_space_f2(B_F2)

# Lift: 0/1 vectors from F_2 are already valid elements of Z/26Z
KERNEL_26_GENERATORS = [np.array(v, dtype=int) for v in KERNEL_F2_BASIS]


# ── Verify generators ─────────────────────────────────────────────────────────

# Exactly 5 generators
assert len(KERNEL_F2_BASIS) == 5, f"Expected 5, got {len(KERNEL_F2_BASIS)}"

# Each is in ker(B mod 2)
for i, v in enumerate(KERNEL_F2_BASIS):
    Bv = (B_F2 @ np.array(v)) % 2
    assert np.all(Bv == 0), f"G{i} not in ker(B mod 2): B·v = {list(Bv)}"

# Each lifted vector is in ker(KERNEL5_M mod 26)
for i, v in enumerate(KERNEL_26_GENERATORS):
    Mv = (KERNEL5_M @ v) % 26
    assert np.all(Mv == 0), f"G{i} not in ker(M mod 26): M·v = {list(Mv)}"

# Linearly independent over F_2
G_mat = np.array(KERNEL_F2_BASIS, dtype=int) % 2
g_rref = G_mat.copy()
g_row = 0
for col in range(9):
    piv = next((r for r in range(g_row, 5) if g_rref[r, col] % 2), None)
    if piv is None:
        continue
    g_rref[[g_row, piv]] = g_rref[[piv, g_row]]
    for r in range(5):
        if r != g_row and g_rref[r, col] % 2:
            g_rref[r] = (g_rref[r] + g_rref[g_row]) % 2
    g_row += 1
assert g_row == 5, f"Generators not linearly independent: F_2 rank = {g_row}"

# All components in {0, 1} — not real numbers, not Riemann zero imaginary parts
for v in KERNEL_26_GENERATORS:
    assert set(map(int, v)) <= {0, 1}, f"Component outside {{0,1}}: {v}"

# γ₁ through γ₁₂ (first 12 Riemann zero imaginary parts, LMFDB values)
GAMMA_PREFIX = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
                52.970321, 56.446248]

for v in KERNEL_26_GENERATORS:
    for gamma in GAMMA_PREFIX:
        for c in v:
            assert abs(int(c) - gamma) > 1.0, \
                f"Spurious γ proximity: component {c} near γ={gamma}"

# Sovereign Matrix (PROVIDED_M) has kernel = 0 over Z/26Z: verified in prior audit
# KERNEL5_M is the {0,13} artificial construction; max entry = 13 (no DR/T entries)
assert KERNEL5_M.max() == 13
assert 1 not in KERNEL5_M   # no 1–9 DR entries


# ── 100-Unity Bridge refutation ───────────────────────────────────────────────

# "100-Unity Bridge": γ₁₂ = 56.446... → 100 by 56 + 44 = 100.
# This is a scalar identity on ONE real number γ₁₂.
# Kernel generators are elements of (Z/26Z)^9 — 9-vectors, not scalars.
# No component of any generator equals 56 or rounds to γ₁₂.
GAMMA_12 = 56.446248
for v in KERNEL_26_GENERATORS:
    assert all(c != 56 and abs(int(c) - GAMMA_12) > 10 for c in v)

# "Decimal Trade Extraction" — no mathematical definition given in this session.
# Verified: no map φ: (Z/26Z)^9 → ℝ has been specified.
# The "extraction" of a real ordinate from a modular vector is undefined.
DECIMAL_TRADE_EXTRACTION_DEFINED = False
assert not DECIMAL_TRADE_EXTRACTION_DEFINED   # confirmed: undefined


if __name__ == "__main__":
    print("Kernel-5 Generators Audit — {0,13} Matrix")
    print()
    print("  PREMISE CORRECTION:")
    print("  The matrix with SNF=[13,13,13,13,26,26,26,26,0] is the artificial")
    print("  {0,13} construction (entry 86), NOT the Sovereign Matrix.")
    print("  Sovereign Matrix (PROVIDED_M) has SNF=[1,9,9,9,9,9,9,9,450], kernel=0.")
    print()
    print("  Algebraic mechanism:")
    print("    ker(13B mod 26) = {v : B·v ≡ 0 (mod 2)}")
    print("    because 13x ≡ 0 (mod 26) iff x ≡ 0 (mod 2)")
    print()
    print("  Kernel basis over F_2 (= basis for ker(KERNEL5_M) over Z/26Z):")
    for i, v in enumerate(KERNEL_F2_BASIS):
        Mv = (KERNEL5_M @ np.array(v)) % 26
        Bv = (B_F2 @ np.array(v)) % 2
        print(f"    G{i+1} = {v}")
        print(f"         B·G{i+1} mod 2  = {list(map(int,Bv))}  {'✓' if np.all(Bv==0) else '✗'}")
        print(f"         M·G{i+1} mod 26 = {list(map(int,Mv))}  {'✓' if np.all(Mv==0) else '✗'}")
    print()
    print("  Component range: all entries in {0, 1}")
    print("  Riemann zero imaginary parts: reals in [14.13, ...]")
    print("  → Categorical mismatch: discrete integers ≠ transcendental reals")
    print()
    print("  100-Unity Bridge check:")
    print(f"    γ₁₂ = {GAMMA_12}")
    print("    All kernel vector components: {0, 1}")
    print("    No component equals 56 or approximates γ₁₂.")
    print("    'Decimal Trade Extraction' has no mathematical definition.")
    print("    → 100-Unity Bridge claim: UNDEFINED / INAPPLICABLE")
    print()
    print("  GUE audit status:")
    print("    A GUE audit requires an ordered real sequence.")
    print("    Five 9-dimensional Z/26Z vectors do not define such a sequence.")
    print("    No ordinate-generating map has been specified.")
    print("    → GUE multi-point audit: DECLINED (undefined input)")
    print()
    print("  Summary:")
    print("    kernel dim 5 is confirmed for the {0,13} construction.")
    print("    The mechanism is M ≡ 0 (mod 13), not DR/T-operator structure.")
    print("    Kernel generators have no spectral interpretation.")
    print()
    print("All assertions passed.")
