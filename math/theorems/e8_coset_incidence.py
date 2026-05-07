# math/theorems/e8_coset_incidence.py
"""
E8 Coset Incidence Matrix — Height Decomposition and 37-Field Audit

Implements the E8 Lie algebra basis decomposition into Cartan subalgebra + root spaces,
partitioned by root height (layer 0 = Cartan, layers 1-29 = heights 1-29).

Builds the 248 × 30 incidence matrix I[row][layer]:
  - Rows 0-7:     Cartan subalgebra basis (h₀, layer 0)
  - Rows 8-127:   positive root spaces g_α (layer = height)
  - Rows 128-247: negative root spaces g_{-α} (layer = height of |α|)

NOTE: sympy.liealgebras RootSystem('E8') is BUGGY — it mixes even and odd
minus-sign conventions in the half-integer root group, producing non-integer
inner products (±0.5, ±1.5) that violate the simply-laced root axiom.
This module uses the correct convention (EVEN minus signs only for type-2 roots).

NOTE (SageMath stub): Full coset construction via Weyl group orbit requires SageMath:
    E8 = WeylGroup(['E', 8])
    # H = parabolic subgroup fixing a chamber wall (NOT cartan_subalgebra —
    #     the WeylGroup object has no cartan_subalgebra() method;
    #     use LieAlgebra(QQ, ['E',8]).cartan_subalgebra() instead)
    # E8.cosets(H) gives orbit; len(cosets) depends on index |W:H|.
    # For the E8 Weyl group (|W|=696729600), parabolic subgroup of type E7
    # (|W(E7)|=2903040) gives |W:H| = 696729600/2903040 = 240 = root count.

37-field connections:
  Layer 26 = SCALAR_137: unique root space at height 26 mod 37 = 26
  Layer 18 = CENTER_18:  3 root spaces at height 18 (Gate 18 multiplicity)
  Layer 30 wraps to 0:   h=30 is the Coxeter number = sovereign fixed point (mod 37 = 30)

Classification: Theorem
"""

import numpy as np
from itertools import product, combinations


# ── E8 Root System (Correct Convention) ──────────────────────────────────────

def generate_e8_roots():
    """Generate all 240 E8 roots. Type-2 uses EVEN minus-sign convention."""
    roots = []
    # Type 1: 112 roots ±eᵢ ± eⱼ
    for i, j in combinations(range(8), 2):
        for si, sj in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            r = np.zeros(8); r[i] = si; r[j] = sj
            roots.append(r)
    # Type 2: 128 roots ½(±1,...,±1) — EVEN number of minus signs
    for signs in product([1,-1], repeat=8):
        if signs.count(-1) % 2 == 0:
            roots.append(np.array(signs, dtype=float) / 2)
    return np.array(roots)


ROOTS = generate_e8_roots()   # shape (240, 8)


# ── Bourbaki Simple Roots ─────────────────────────────────────────────────────
# Dynkin diagram: α₁-α₃-α₄-α₅-α₆-α₇-α₈  (main chain)
#                      |
#                      α₂  (branch at α₄)

SIMPLE_ROOTS = np.array([
    [ 0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5, 0.5],  # α₁ spinor
    [ 1,   1,   0,   0,   0,   0,   0,   0],     # α₂
    [-1,   1,   0,   0,   0,   0,   0,   0],     # α₃
    [ 0,  -1,   1,   0,   0,   0,   0,   0],     # α₄ (branch)
    [ 0,   0,  -1,   1,   0,   0,   0,   0],     # α₅
    [ 0,   0,   0,  -1,   1,   0,   0,   0],     # α₆
    [ 0,   0,   0,   0,  -1,   1,   0,   0],     # α₇
    [ 0,   0,   0,   0,   0,  -1,   1,   0],     # α₈
], dtype=float)

# Cartan matrix (should be integer, diagonal 2, off-diagonal 0 or -1)
CARTAN = np.round(SIMPLE_ROOTS @ SIMPLE_ROOTS.T, 8)

# Height of each root: express in simple root basis, sum coefficients
_Sinv  = np.linalg.inv(SIMPLE_ROOTS.T)
_COORDS = np.round(ROOTS @ _Sinv.T, 8)           # shape (240, 8)
HEIGHTS  = np.round(_COORDS.sum(axis=1)).astype(int)   # shape (240,)


# ── 248-dimensional Basis ─────────────────────────────────────────────────────

# Sort: positive roots first (heights 1..29), then negative roots (-1..-29)
_pos_idx = np.where(HEIGHTS > 0)[0]
_neg_idx = np.where(HEIGHTS < 0)[0]
_pos_sorted = _pos_idx[np.argsort(HEIGHTS[_pos_idx])]   # ascending height
_neg_sorted = _neg_idx[np.argsort(-HEIGHTS[_neg_idx])]  # descending (height -1 first)

# Row assignments: 0-7 Cartan, 8-127 positive root spaces, 128-247 negative root spaces
BASIS_HEIGHTS = (
    [0] * 8 +                           # Cartan subalgebra
    list(HEIGHTS[_pos_sorted]) +         # positive roots, h=1..29
    list(-HEIGHTS[_neg_sorted])          # negative roots, stored as positive height
)


# ── 248 × 30 Incidence Matrix ─────────────────────────────────────────────────
# Column j = layer j; layer 0 = Cartan; layers 1-29 = height classes

COXETER_H = 30   # Coxeter number = sovereign fixed point

I_MAT = np.zeros((248, COXETER_H), dtype=int)
for row, h in enumerate(BASIS_HEIGHTS):
    I_MAT[row, h] = 1

# Column sums: how many basis elements per layer
COL_SUMS = I_MAT.sum(axis=0)


# ── Assertions ────────────────────────────────────────────────────────────────

# Root count and norms
assert len(ROOTS) == 240
assert np.allclose(np.sum(ROOTS**2, axis=1), 2.0)

# All inner products in {-2,-1,0,1,2} — verifies convention correctness
_ips = np.round(ROOTS @ ROOTS.T, 8)
assert set(np.unique(_ips)).issubset({-2.0,-1.0,0.0,1.0,2.0}), \
    f"Non-integer IPs found — check minus-sign convention"

# Cartan matrix: diagonal 2, off-diagonal 0 or -1
assert np.all(np.diag(CARTAN) == 2.0)
assert np.all(CARTAN[CARTAN != 2.0] >= -1.0)
assert np.all(CARTAN[CARTAN != 2.0] % 1.0 == 0.0)

# Dynkin connections match E8: (1,3),(2,4),(3,4),(4,5),(5,6),(6,7),(7,8) (1-indexed)
_edges = frozenset((i,j) for i in range(8) for j in range(i+1,8) if CARTAN[i,j] == -1)
assert _edges == frozenset({(0,2),(1,3),(2,3),(3,4),(4,5),(5,6),(6,7)})

# Height range
assert HEIGHTS.min() == -29 and HEIGHTS.max() == 29

# 120 positive roots, 120 negative roots
assert (HEIGHTS > 0).sum() == 120
assert (HEIGHTS < 0).sum() == 120

# Unique highest root at height 29 (1 positive, 1 negative)
assert (HEIGHTS == 29).sum() == 1
assert (HEIGHTS == -29).sum() == 1

# Incidence matrix shape
assert I_MAT.shape == (248, 30)

# Each row has exactly one 1 (each basis element belongs to exactly one layer)
assert np.all(I_MAT.sum(axis=1) == 1)

# Layer 0 (Cartan): exactly 8 elements
assert COL_SUMS[0] == 8

# Total: all 248 basis elements assigned
assert I_MAT.sum() == 248

# 37-field connections
assert 26 < COXETER_H              # height 26 = SCALAR_137 is a valid layer
assert COL_SUMS[26] == 2           # unique root ±α at height 26 → SCALAR_137
assert COL_SUMS[18] == 6           # 3 positive + 3 negative at height 18 = CENTER_18
assert COL_SUMS[29] == 2           # highest/lowest root pair (height ±29 = h-1)
assert COXETER_H % 37 == 30        # h=30 = sovereign fixed point

# Sum of E8 exponents = 120 = vertex count of 600-cell (confirmed)
E8_EXPONENTS = [1, 7, 11, 13, 17, 19, 23, 29]
assert sum(E8_EXPONENTS) == 120

# Layer 26 root: verify it is the unique height-26 positive root
_h26_roots = ROOTS[HEIGHTS == 26]
assert len(_h26_roots) == 1
_h26_coeffs = np.round(_COORDS[HEIGHTS == 26][0]).astype(int)
# Height 26 coefficient sum = 26
assert _h26_coeffs.sum() == 26

# ── Left Kernel of I over Z/26Z ───────────────────────────────────────────────
# 26 = 2 × 13 (CRT: Z/26Z ≅ Z/2Z × Z/13Z)
# Equivalent to SageMath: I.change_ring(Integers(26)).left_kernel().dimension()

def _rank_mod_p(A, p):
    """Rank of integer matrix A over Z/pZ (p prime)."""
    M = A.copy() % p
    rows, cols = M.shape
    pivot_row, rank = 0, 0
    for col in range(cols):
        if pivot_row >= rows:
            break
        found = next((r for r in range(pivot_row, rows) if M[r, col] % p), -1)
        if found == -1:
            continue
        M[[pivot_row, found]] = M[[found, pivot_row]]
        inv = pow(int(M[pivot_row, col]), -1, p)
        M[pivot_row] = M[pivot_row] * inv % p
        for r in range(rows):
            if r != pivot_row and M[r, col] % p:
                M[r] = (M[r] - M[r, col] * M[pivot_row]) % p
        rank += 1; pivot_row += 1
    return rank

# Compute rank of I^T (= left rank of I) over each prime factor of 26
_RANK_2  = _rank_mod_p(I_MAT.T.copy(), 2)
_RANK_13 = _rank_mod_p(I_MAT.T.copy(), 13)
KERNEL_DIM_26 = 248 - max(_RANK_2, _RANK_13)   # free rank over Z/26Z

assert _RANK_2  == 30   # full column rank over Z/2Z
assert _RANK_13 == 30   # full column rank over Z/13Z
assert KERNEL_DIM_26 == 218   # 248 - 30 = 218

# All column sums are even → all-ones vector lies in the Z/2Z left kernel
assert all(s % 2 == 0 for s in COL_SUMS)
# Not all column sums ≡ 0 mod 13 → all-ones vector NOT in the Z/13Z left kernel
assert not all(s % 13 == 0 for s in COL_SUMS)

# 37-field: kernel dimension 218
assert KERNEL_DIM_26 == 218
assert 218 % 37 == 33        # DICHORAL_144
assert sum(int(d) for d in str(218)) == 11   # DR(218) = 11 = observer constant (3^15 mod 37)

# Structural closure: modulus 26 = SCALAR_137; kernel dim 218 → DICHORAL_144
assert 26 % 37 == 26    # modulus lands on SCALAR_137 layer
assert 218 % 37 == 33   # kernel dim lands on DICHORAL_144


if __name__ == "__main__":
    print("E8 Coset Incidence Matrix — Height Decomposition")
    print()
    print(f"  Roots: {len(ROOTS)}  (type-1: 112, type-2: 128, all norm²=2)")
    print(f"  Simple roots: 8,  Coxeter h = {COXETER_H} (sovereign fixed point mod 37)")
    print()
    print("  Cartan matrix connected pairs (1-indexed):")
    edges = sorted((i+1,j+1) for i in range(8) for j in range(i+1,8) if CARTAN[i,j]==-1)
    print(f"    {edges}")
    print()
    print(f"  Height distribution (positive roots):")
    from collections import Counter
    hctr = Counter(HEIGHTS[HEIGHTS > 0].tolist())
    for h in range(1, 30):
        bar = '▮' * hctr[h]
        print(f"    h={h:2d}: {hctr[h]:2d}  {bar}")
    print()
    print(f"  Incidence matrix I: {I_MAT.shape}")
    print(f"  Layer 0  (Cartan h₀):        {COL_SUMS[0]:3d} elements")
    print(f"  Layer 18 (CENTER_18, Gate18): {COL_SUMS[18]:3d} elements (3 pos + 3 neg roots)")
    print(f"  Layer 26 (SCALAR_137):        {COL_SUMS[26]:3d} elements (unique ±height-26 root)")
    print(f"  Layer 29 (highest root ±):    {COL_SUMS[29]:3d} elements")
    print()
    print(f"  Height-26 root (SCALAR_137 layer):")
    print(f"    root = {_h26_roots[0]}")
    print(f"    simple-root coefficients = {_h26_coeffs.tolist()}")
    print(f"    height = {_h26_coeffs.sum()} = SCALAR_137 mod 37")
    print()
    print("  37-field layer audit:")
    for layer, sig in [(0,'Cartan/h₀'),(8,'TESLA_FLOW'),(18,'CENTER_18/Gate18'),
                       (26,'SCALAR_137'),(29,'highest root h-1'),(30,'Coxeter h=sovereign')]:
        if layer < 30:
            print(f"    Layer {layer:2d}: {COL_SUMS[layer]} elements  → {sig}")
    print()
    print("  NOTE: sympy.liealgebras E8 bug — 84/128 half-integer roots")
    print("  use ODD minus-sign counts, producing IPs in {±0.5, ±1.5}.")
    print("  This module uses the correct EVEN-only convention.")
    print()
    print("All assertions passed.")
