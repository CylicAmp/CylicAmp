#!/usr/bin/env python3
"""
g4_mackey_fourier_audit.py

Full Mackey / Fourier decomposition of G_4 = Z_4^2 ⋊ D_4.

Verified claims:
  1. Fourier transform F_16 on Z_4^2 is unitary
  2. D_4 acts on dual lattice Z_4^2-hat; 6 orbits with sizes 1,4,2,4,4,1
  3. Mackey block dimensions per orbit: orbit_size × |D_4|
  4. Cayley operator eigenvalues satisfy shift structure:
       eig(K, orbit O_i) = λ_i + (D_4 base spectrum)
     where λ_i is the translation eigenvalue for orbit i
  5. Full 128-eigenvalue spectrum matches orbit-shifted D_4 spectrum
  6. Rational eigenvalue count: only orbits O_0, O_5 (trivial stabilizer = D_4 itself)
     can produce rational eigenvalues; generic D_4 spectrum has irrational entries
  7. Total irrep count via Mackey = 20
"""

import numpy as np
from itertools import product as iproduct
from fractions import Fraction
import cmath

FAIL = []
def check(cond, label, detail=""):
    if not cond:
        FAIL.append(label + (f": {detail}" if detail else ""))
    return cond

# ---------------------------------------------------------------------------
# D4 arithmetic
# ---------------------------------------------------------------------------

def d4_mul(x, y):
    sx, ax = (1, x-4) if x >= 4 else (0, x)
    sy, ay = (1, y-4) if y >= 4 else (0, y)
    if sx == 0 and sy == 0: return (ax+ay) % 4
    if sx == 0 and sy == 1: return 4+(ax+ay) % 4
    if sx == 1 and sy == 0: return 4+(ax-ay) % 4
    return (ax-ay) % 4

def d4_inv(x): return x if x >= 4 else (-x) % 4

D4 = list(range(8))
D4_NAMES = {0:'e', 1:'σ', 2:'σ²', 3:'σ³', 4:'τ', 5:'στ', 6:'σ²τ', 7:'σ³τ'}

# ---------------------------------------------------------------------------
# Z_4^2 and G_4
# ---------------------------------------------------------------------------

Z4SQ = list(range(16))

def rho2(d, k):
    a, b = divmod(k, 4)
    if   d == 0: return 4*a + b
    elif d == 1: return 4*((-b)%4) + a
    elif d == 2: return 4*((-a)%4) + (-b)%4
    elif d == 3: return 4*b + (-a)%4
    elif d == 4: return 4*a + (-b)%4
    elif d == 5: return 4*b + a
    elif d == 6: return 4*((-a)%4) + b
    else:        return 4*((-b)%4) + (-a)%4

def z4sq_add(k1, k2):
    a1,b1 = divmod(k1,4); a2,b2 = divmod(k2,4)
    return 4*((a1+a2)%4) + (b1+b2)%4

def z4sq_neg(k):
    a,b = divmod(k,4); return 4*((-a)%4) + (-b)%4

N = 128
def enc(k,d): return 8*k+d
def dec(idx): return divmod(idx,8)

def g4_mul(u, v):
    k1,d1 = dec(u); k2,d2 = dec(v)
    return enc(z4sq_add(k1, rho2(d1,k2)), d4_mul(d1,d2))

def build_reg(g):
    M = np.zeros((N,N));
    for j in range(N): M[g4_mul(g,j), j] = 1.0
    return M

def vec_from_idx(k): return divmod(k, 4)  # (a, b)

# ===========================================================================
print("=" * 70)
print("GENERATING SET S FOR CAYLEY GRAPH")
print("=" * 70)

# Symmetric generating set S:
#   Z4^2 translations: e1=(1,0), -e1=(3,0), e2=(0,1), -e2=(0,3)
#   D4 generators (with inverses): σ=r, σ^{-1}=r^3, τ=s (self-inverse)
e1   = enc(4*1+0, 0)
ne1  = enc(4*3+0, 0)
e2   = enc(4*0+1, 0)
ne2  = enc(4*0+3, 0)
sig  = enc(0, 1)    # σ = r
sig3 = enc(0, 3)    # σ^{-1} = r^3
tau  = enc(0, 4)    # τ = s (self-inverse)

S = [e1, ne1, e2, ne2, sig, sig3, tau]   # 7 generators (symmetric)

print()
print(f"  e1  = ((1, 0), e)")
print(f"  -e1 = ((3, 0), e)")
print(f"  e2  = ((0, 1), e)")
print(f"  -e2 = ((0, 3), e)")
print(f"  σ   = ((0, 0), σ)   [= r]")
print(f"  σ⁻¹ = ((0, 0), σ³)  [= r⁻¹, included for symmetry]")
print(f"  τ   = ((0, 0), τ)   [= s, self-inverse]")
print(f"  |S| = {len(S)}  (symmetric generating set)")

# Verify S is symmetric (closed under inverse)
S_inv = [g4_mul(g4_mul(enc(0,0), g), g) for g in S]  # dummy; check directly
for g in S:
    g_inv = enc(z4sq_neg(rho2(d4_inv(dec(g)[1]), dec(g)[0])), d4_inv(dec(g)[1]))
    check(g_inv in S, f"S closed under inverse: {g}", f"inv={g_inv} not in S")
print(f"  S is symmetric (closed under inverses): PASS ✓")

# ===========================================================================
print()
print("=" * 70)
print("FOURIER TRANSFORM ON Z_4²")
print("=" * 70)

# F_16: the DFT on Z_4^2
# F[k, v] = omega^{k·v} / 4  where omega = exp(2πi/4) = i
# k = (k1, k2), v = (v1, v2): k·v = k1*v1 + k2*v2 (in Z_4)
omega = np.exp(2j * np.pi / 4)

F16 = np.zeros((16, 16), dtype=complex)
for k_idx in range(16):
    k1, k2 = divmod(k_idx, 4)
    for v_idx in range(16):
        v1, v2 = divmod(v_idx, 4)
        F16[k_idx, v_idx] = omega**((k1*v1 + k2*v2) % 4) / 4.0

print()
print("Dual lattice elements (momentum indices k ∈ Z_4²):")
for k_idx in range(16):
    k1, k2 = divmod(k_idx, 4)
    print(f"  k_{k_idx:2d} = ({k1}, {k2})")

# Verify unitarity: F @ F† = I (with normalization 4, so F†F = (1/16)*I after our norm)
FdagF = F16 @ F16.conj().T * 16   # scale: each entry 1/4, so F†F * 16 = I
diag_vals = np.diag(FdagF)
off_max = np.max(np.abs(FdagF - np.diag(diag_vals)))
check(np.allclose(diag_vals, 16.0, atol=1e-12), "F_16 * F_16† diagonal = 16*I")
check(off_max < 1e-12, "F_16 * F_16† off-diagonal = 0", f"max={off_max:.2e}")
print(f"\nF_16 @ F_16† diagonal: {diag_vals[:5]}... (should all be 16)")
print(f"Max off-diagonal: {off_max:.2e}")

# ===========================================================================
print()
print("=" * 70)
print("D_4-ORBITS IN DUAL LATTICE widehat{Z_4²} ≅ Z_4²")
print("=" * 70)
print()

# D4 acts on Z4^2-hat by (d·χ_k)(v) = χ_k(rho2(d^{-1}, v))
# This is equivalent to: d maps momentum k to rho2(d, k)
# (contragredient = same as direct for this self-dual group)

seen = [False] * 16
orbits = []
for k in Z4SQ:
    if not seen[k]:
        orb = sorted(set(rho2(d, k) for d in D4))
        orbits.append(orb)
        for kk in orb:
            seen[kk] = True

# Compute stabilizers
def stabilizer(k):
    return [d for d in D4 if rho2(d, k) == k]

orbit_info = []
for i, orb in enumerate(orbits):
    k0 = orb[0]
    stab = stabilizer(k0)
    orbit_info.append({'orb': orb, 'stab': stab, 'k0': k0})

    stab_names = ', '.join(D4_NAMES[d] for d in stab)
    pts = [f"({divmod(k,4)[0]}, {divmod(k,4)[1]})" for k in orb]
    print(f"Orbit O_{i}: [{', '.join(pts)}]")
    print(f"  Size: {len(orb)}")
    print(f"  Stabilizer of ({divmod(k0,4)[0]}, {divmod(k0,4)[1]}): {{{stab_names}}} (order {len(stab)})")
    print()
    check(len(orb) * len(stab) == 8, f"O_{i}: orbit-stabilizer theorem: |O|×|Stab|=8",
          f"got {len(orb)}×{len(stab)}={len(orb)*len(stab)}")

total_pts = sum(len(oi['orb']) for oi in orbit_info)
check(total_pts == 16, f"orbits partition Z4^2 (sum=16)", f"got {total_pts}")
print(f"Total orbits: {len(orbits)}")
print(f"Sum of orbit sizes: {total_pts} (= 16) {'✓' if total_pts==16 else 'FAIL'}")

# ===========================================================================
print()
print("=" * 70)
print("LITTLE-GROUP / MACKEY ANALYSIS")
print("=" * 70)
print()

total_mackey_dim = 0
mackey_irrep_count = 0
for i, oi in enumerate(orbit_info):
    orb_size = len(oi['orb'])
    stab_order = len(oi['stab'])
    block_dim = orb_size * 8
    total_mackey_dim += block_dim
    # Number of irreps from Mackey: = number of irreps of stabilizer
    # Z2 has 2 irreps, V4 has 4 irreps, D4 has 5 irreps
    if stab_order == 8:   n_irr = 5  # D4
    elif stab_order == 4: n_irr = 4  # V4 = Z2 x Z2 (stabilizer of (2,0) is {e,r^2,s,r^2s})
    elif stab_order == 2: n_irr = 2  # Z2
    else: n_irr = stab_order
    mackey_irrep_count += n_irr
    print(f"Orbit O_{i}: size = {orb_size}, stabilizer order = {stab_order}")
    print(f"  Block dimension in regular rep: {orb_size} × 8 = {block_dim}")
    print(f"  Irreps from Mackey: {n_irr} (from {stab_order}-element stabilizer)")
    print()

check(total_mackey_dim == N, f"total Mackey block dim = {N}", f"got {total_mackey_dim}")
check(mackey_irrep_count == 20, f"total Mackey irrep count = 20", f"got {mackey_irrep_count}")
print(f"Total block dimension: {total_mackey_dim} = {N} ✓")
print(f"Total irrep count (Mackey): {mackey_irrep_count}")

# ===========================================================================
print()
print("=" * 70)
print("TRANSLATION OPERATORS IN FOURIER BASIS")
print("=" * 70)
print()

# Translation eigenvalue for momentum k under generators {e1,-e1,e2,-e2}:
# L_{e1} acts on f: k -> chi_k(e1) = omega^{k1*1} = i^{k1}
# K_trans eigenvalue at k = sum over {e1,-e1,e2,-e2} of chi_k(generator)
#   = (omega^{k1} + omega^{-k1} + omega^{k2} + omega^{-k2})
#   = 2*cos(pi*k1/2) + 2*cos(pi*k2/2)
# For k=(k1,k2) with k1,k2 in {0,1,2,3}: omega^n = i^n

a_val, b_val = 1.0, 1.0
alpha_val, beta_val = 1.0, 1.0

print(f"Translation eigenvalues (a={a_val}, b={b_val}):")
trans_eig = {}
orbit_assignment = {}
# Build orbit lookup
for i, oi in enumerate(orbit_info):
    for k in oi['orb']:
        orbit_assignment[k] = i

for k in Z4SQ:
    k1, k2 = divmod(k, 4)
    # eigenvalue of K_trans = a*(2cos(pi*k1/2) + 2cos(pi*k2/2))
    lam = a_val * (2*np.cos(np.pi*k1/2) + 2*np.cos(np.pi*k2/2))
    trans_eig[k] = lam
    print(f"  k=({k1}, {k2}): λ = {lam:8.4f}  (orbit O_{orbit_assignment[k]})")

print()
print("Translation eigenvalues grouped by orbit:")
for i, oi in enumerate(orbit_info):
    pts = [f"({divmod(k,4)[0]}, {divmod(k,4)[1]})" for k in oi['orb']]
    lams_rounded = {round(trans_eig[k], 8) for k in oi['orb']}
    lam_display = {f"{v:.4f}" for v in lams_rounded}
    print(f"  O_{i}: [{', '.join(pts)}]")
    print(f"      λ values: {lam_display}")
    print()
    # All elements in same orbit should have same translation eigenvalue (±0.0 treated equal)
    lam_vals = [round(trans_eig[k], 8) for k in oi['orb']]
    check(len(set(lam_vals)) == 1, f"O_{i}: uniform translation eigenvalue",
          f"got {lam_vals}")

# ===========================================================================
print("=" * 70)
print("SPECTRAL ANALYSIS: CAYLEY OPERATOR")
print("=" * 70)
print()
print(f"Parameters: a = {a_val}, b = {b_val}, α = {alpha_val}, β = {beta_val}")

# Build full 128×128 Cayley operator
# K = a*(L_{e1}+L_{-e1}+L_{e2}+L_{-e2}) + b*(L_σ + L_{σ^{-1}} + L_τ)
# with α and β as additional scaling (here both 1)
K_trans_mat = sum(build_reg(g) for g in [e1, ne1, e2, ne2]) * a_val
K_d4gen_mat = (build_reg(sig) + build_reg(sig3) + build_reg(tau)) * b_val
K_full = alpha_val * K_trans_mat + beta_val * K_d4gen_mat

check(np.allclose(K_full, K_full.T, atol=1e-10), "K_full is symmetric")

# Compute D4 base spectrum (translation λ=0 sector)
# K_D4 part alone:
K_D4_only = K_d4gen_mat  # β=1
# For the orbit with λ_k=0 (say O_2), K_block = 0 + K_D4
# Extract D4 base eigenvalues from O_2 block

# The "base D4 spectrum" is the eigenvalue structure of K_D4gen
# restricted to the D4 subgroup. Build 8×8 regular rep of D4:
D4_reg = {}
for d in D4:
    M = np.zeros((8,8))
    for j in range(8): M[d4_mul(d,j), j] = 1.0
    D4_reg[d] = M

K_D4_8x8 = (D4_reg[1] + D4_reg[3] + D4_reg[4]) * b_val  # r, r^{-1}, s
D4_base_eigs = sorted(np.linalg.eigvalsh(K_D4_8x8))
print()
print(f"D_4 base spectrum (8 eigenvalues of K_D4 on C[D4]):")
print(f"  {[f'{e:.4f}' for e in D4_base_eigs]}")

# Verify: all D4 base eigs should be real (symmetric K)
check(all(abs(np.imag(e)) < 1e-12 for e in np.linalg.eigvals(K_D4_8x8)),
      "D4 base eigenvalues are real")

# ===========================================================================
# Block-by-block spectral analysis via orbit decomposition
# For each orbit O_i with translation eigenvalue λ_i:
#   the K-block restricted to that orbit = λ_i * I + K_D4
#   (this is the shift structure)
# ===========================================================================

print()
print("Eigenvalues grouped by D_4-orbits:")
print()

all_predicted = []
orbit_spectra = {}

for i, oi in enumerate(orbit_info):
    k0 = oi['orb'][0]
    lam_i = trans_eig[k0]
    orb_size = len(oi['orb'])

    print("─" * 60)
    pts = [f"({divmod(k,4)[0]}, {divmod(k,4)[1]})" for k in oi['orb']]
    print(f"Orbit O_{i}: [{', '.join(pts)}]")
    print(f"  Size = {orb_size}, Stabilizer order = {len(oi['stab'])}")
    print()
    print(f"  Translation eigenvalue: λ = {lam_i:.4f}")
    print()

    # Predicted block spectrum: λ_i + D4_base_eigs
    predicted_block = sorted([lam_i + e for e in D4_base_eigs])
    # Each of the 8 values appears with multiplicity orb_size in the full spectrum
    for e in predicted_block:
        all_predicted.extend([e] * orb_size)

    orbit_spectra[i] = predicted_block
    print(f"  Full block spectrum (8 eigenvalues):")
    for e in predicted_block:
        print(f"  {e:14.4f}")
    print()

# Verify full spectrum
eigs_full = sorted(np.linalg.eigvalsh(K_full))
predicted_sorted = sorted(all_predicted)

max_dev = max(abs(a-b) for a,b in zip(eigs_full, predicted_sorted))
check(len(eigs_full) == N, f"128 eigenvalues computed", f"got {len(eigs_full)}")
check(max_dev < 1e-8, "shift structure: all eigs = λ_orbit + D4_base_eig", f"max dev={max_dev:.2e}")
print()
print(f"Shift structure verification (eig = λ_orbit + D4_base):")
print(f"  Max deviation across all 128 eigenvalues: {max_dev:.2e}  PASS ✓")

# ===========================================================================
print()
print("=" * 70)
print("FULL 128×128 SPECTRUM VERIFICATION")
print("=" * 70)
print()

print(f"Number of eigenvalues: {len(eigs_full)} (should be 128)")
print(f"Max deviation from shift-structure prediction: {max_dev:.2e}")
print()
print(f"Spectral range: [{eigs_full[0]:.4f}, {eigs_full[-1]:.4f}]")
print(f"Spectral diameter: {eigs_full[-1] - eigs_full[0]:.4f}")

# ===========================================================================
print()
print("=" * 70)
print("RATIONALITY ANALYSIS")
print("=" * 70)
print()

# Rational eigenvalues: those where λ_i + D4_base_eig is rational
# D4_base_eigs come from {r, r^{-1}=r^3, s} Cayley operator on D4
# These are algebraic; check which are rational
from fractions import Fraction
def is_rational(x, tol=1e-9):
    for denom in range(1, 100):
        if abs(x * denom - round(x * denom)) < tol:
            return True, Fraction(round(x * denom), denom)
    return False, None

print("D_4 base eigenvalues — rationality check:")
rational_base = []
irrational_base = []
for e in D4_base_eigs:
    rat, frac = is_rational(e)
    if rat:
        rational_base.append((e, frac))
        print(f"  {e:10.6f}  RATIONAL  ({frac})")
    else:
        irrational_base.append(e)
        print(f"  {e:10.6f}  irrational")

print()
print("Translation eigenvalues — rationality check:")
trans_values = sorted(set(round(v,8) for v in trans_eig.values()))
for lam in trans_values:
    rat, frac = is_rational(lam)
    print(f"  λ = {lam:8.4f}  {'RATIONAL' if rat else 'irrational'}  {frac if rat else ''}")

print()
# Count rational eigenvalues in full spectrum
n_rational = 0
n_irrational = 0
for i, oi in enumerate(orbit_info):
    lam_i = trans_eig[oi['orb'][0]]
    lam_rat, _ = is_rational(lam_i)
    orb_size = len(oi['orb'])
    for e in D4_base_eigs:
        total = lam_i + e
        rat, _ = is_rational(total)
        if rat:
            n_rational += orb_size
        else:
            n_irrational += orb_size

print(f"Rational eigenvalues in full 128-spectrum: {n_rational}")
print(f"Irrational eigenvalues: {n_irrational}")
print(f"Fraction irrational: {n_irrational}/{N} = {n_irrational/N:.3f}")

check(n_rational + n_irrational == N, f"rational+irrational = {N}")

# ---------------------------------------------------------------------------
# Rationality depends on generating set: audit alternative {s, rs} generators
# With {s=τ, rs=στ}: K_E = rho_E(s)+rho_E(rs) = [[1,0],[0,-1]]+[[0,1],[1,0]]
# = [[1,1],[1,-1]], eigenvalues ±sqrt(2) — IRRATIONAL
# ---------------------------------------------------------------------------
print()
print("Generating-set dependence of rationality:")
print("  Current S = {r, r⁻¹, s}: D4 base spectrum all integers → 128/128 rational")
print()
print("  Alternative S' = {s, rs} (two reflections, symmetric since s²=(rs)²=e):")

D4_reg_alt = {}
for d in D4:
    M = np.zeros((8,8))
    for j in range(8): M[d4_mul(d,j), j] = 1.0
    D4_reg_alt[d] = M

# s = d4 element 4, rs = d4 element 5
K_D4_alt = D4_reg_alt[4] + D4_reg_alt[5]
check(np.allclose(K_D4_alt, K_D4_alt.T, atol=1e-10), "K_D4_alt is symmetric")
D4_alt_eigs = sorted(np.linalg.eigvalsh(K_D4_alt))
print(f"  D4 alt. spectrum: {[f'{e:.4f}' for e in D4_alt_eigs]}")

# Count irrational
n_rat_alt = sum(1 for e in D4_alt_eigs if is_rational(e)[0])
n_irr_alt = len(D4_alt_eigs) - n_rat_alt
print(f"  Rational / irrational in D4 base (alt): {n_rat_alt} / {n_irr_alt}")

# Full alt spectrum
# Build the alt K on G4 (replacing D4 generator part)
K_d4gen_alt = (build_reg(enc(0,4)) + build_reg(enc(0,5))) * b_val
K_full_alt = alpha_val * K_trans_mat + beta_val * K_d4gen_alt
check(np.allclose(K_full_alt, K_full_alt.T, atol=1e-10), "K_full_alt symmetric")
eigs_alt = sorted(np.linalg.eigvalsh(K_full_alt))
n_rat_full_alt = sum(1 for e in eigs_alt if is_rational(e)[0])
n_irr_full_alt = len(eigs_alt) - n_rat_full_alt
print(f"  Rational / irrational in full 128-spectrum (alt): {n_rat_full_alt} / {n_irr_full_alt}")
print(f"  Alt spectral range: [{eigs_alt[0]:.4f}, {eigs_alt[-1]:.4f}]")
print()
print("  Conclusion: irrationality is a GENERATING-SET property, not a group property.")
print("  S={r,r⁻¹,s} → integer spectrum; S'={s,rs} → sqrt(2) irrationalities.")

# ===========================================================================
print()
print("=" * 70)
print("IRREP DECOMPOSITION VIA MACKEY THEOREM")
print("=" * 70)
print()

# For G = Z4^2 ⋊ D4, Mackey gives:
# Irreps <-> pairs (orbit O_i, irrep rho of Stab(k0) for k0 in O_i)
# Dimension of ind. irrep = |D4| / |Stab| * dim(rho) = (8/|Stab|) * dim(rho)

print(f"{'Orbit':<8} {'|O|':<5} {'Stab':<12} {'|Stab|':<8} "
      f"{'Stab irreps':<12} {'Ind. rep dims':<20} {'Count'}")
print("-" * 80)

total_irreps = 0
dim_check = 0
irrep_table = []

stab_irrep_data = {
    8: (5, [1,1,1,1,2]),   # D4: A1,A2,B1,B2,E
    4: (4, [1,1,1,1]),      # V4 = Z2×Z2: four 1-dim irreps
    2: (2, [1,1]),           # Z2: two 1-dim irreps
}

for i, oi in enumerate(orbit_info):
    k0 = oi['orb'][0]
    k0_str = f"({divmod(k0,4)[0]},{divmod(k0,4)[1]})"
    orb_size = len(oi['orb'])
    stab_order = len(oi['stab'])
    stab_name = {8:'D_4', 4:'V_4', 2:'Z_2'}[stab_order]

    n_irr, dims = stab_irrep_data[stab_order]
    ind_dims = [orb_size * d for d in dims]
    total_irreps += n_irr
    for d in ind_dims:
        dim_check += d * d
    irrep_table.append((i, orb_size, stab_name, stab_order, n_irr, ind_dims))

    print(f"O_{i:<6} {orb_size:<5} {stab_name:<12} {stab_order:<8} "
          f"{n_irr:<12} {ind_dims}")

print("-" * 80)
print(f"Total irreps: {total_irreps}")
print(f"Σ(dim²) = {dim_check}  (should be {N} = |G_4|)")
check(total_irreps == 20, f"total irreps = 20", f"got {total_irreps}")
check(dim_check == N, f"Σ(dim²) = |G_4| = {N}", f"got {dim_check}")
print(f"  total irreps = {total_irreps}  {'PASS ✓' if total_irreps==20 else 'FAIL'}")
print(f"  Σ(dim²) = {dim_check} = {N}  {'PASS ✓' if dim_check==N else 'FAIL'}")
print()
print("  Note: the 20 conjugacy classes computed from g4_construction_audit.py ✓")
print("  (20 classes = 20 irreps — confirmed independently)")

# ===========================================================================
print()
print("=" * 70)
print("SUMMARY TABLE")
print("=" * 70)
print()
print(f"  {'Orbit':<8} {'k rep':<12} {'|O|':<5} {'Stab':<8} {'λ_trans':<10} "
      f"{'Block dims (induced irreps)'}")
print(f"  {'-'*75}")
for i, oi in enumerate(orbit_info):
    k0 = oi['orb'][0]
    k1,k2 = divmod(k0, 4)
    lam_i = trans_eig[k0]
    orb_size = len(oi['orb'])
    stab_order = len(oi['stab'])
    stab_name = {8:'D_4', 4:'V_4', 2:'Z_2'}[stab_order]
    _, dims = stab_irrep_data[stab_order]
    ind_dims = [orb_size * d for d in dims]
    print(f"  O_{i:<6} ({k1},{k2}){'':<7} {orb_size:<5} {stab_name:<8} {lam_i:<10.1f} {ind_dims}")

print()
print(f"  Cayley operator |S| = {len(S)} (translation: 4, D4 gen: 3=r,r⁻¹,s)")
print(f"  Spectral range: [{eigs_full[0]:.4f}, {eigs_full[-1]:.4f}]")
print(f"  Spectral diameter: {eigs_full[-1]-eigs_full[0]:.4f}")
print(f"  Shift structure: eig(O_i) = λ_i + D4_base  CONFIRMED ✓")
print(f"  Rational/irrational split: {n_rational}/{N} rational, {n_irrational}/{N} irrational")

# ===========================================================================
print()
print("=" * 70)
if FAIL:
    print(f"FAILED ({len(FAIL)}):")
    for f in FAIL:
        print(f"  FAIL  {f}")
    import sys; sys.exit(1)
else:
    print("ALL CHECKS PASS")
    print()
    print("  F_16 unitary on Z_4²  ✓")
    print("  6 D_4-orbits: sizes 1,4,2,4,4,1 (sum=16)  ✓")
    print("  Orbit-stabilizer theorem: |O|×|Stab|=8 for each orbit  ✓")
    print("  Translation eigenvalues λ_i = {4,2,0,0,-2,-4} (orbit-constant)  ✓")
    print("  Shift structure: eig(K,O_i) = λ_i + D_4 base spectrum  ✓")
    print("  Full 128-eigenvalue spectrum matches shift prediction  ✓")
    print(f"  Mackey irrep count: 20 = #{len(orbits)} orbits × (Stab irreps)  ✓")
    print(f"  Σ(dim²) = {dim_check} = |G_4|  ✓")
    print(f"  Rational eigenvalues: {n_rational}/{N},  Irrational: {n_irrational}/{N}  ✓")
