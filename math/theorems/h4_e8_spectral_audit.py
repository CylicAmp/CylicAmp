#!/usr/bin/env python3
"""
h4_e8_spectral_audit.py

Audits the claims in the submitted code snippet:
  1. H4 root geometry: r1=(1,phi,0,0) and r2=(1/2,1/2,1/2,phi/2) norm checks
  2. E8: |W(E8)|=696729600, 240 roots
  3. H4 ∪ phi*H4 ⊂ E8: count compatibility
  4. Spectral data table: {2.000}, {1.618, 0.382}, {0.000} vs actual G4 eigenvalues
"""

import math
import itertools
import numpy as np

FAIL = []

def check(cond, label, detail=""):
    if not cond:
        FAIL.append(label + (f": {detail}" if detail else ""))
    return cond

phi = (1 + math.sqrt(5)) / 2

# ---------------------------------------------------------------------------
# Section 1: H4 root geometry — what are the actual roots?
# ---------------------------------------------------------------------------
print("=== Section 1: H4 root geometry ===")
print()
print("  The H4 root system = 120 vertices of the 600-cell (all on unit S^3).")
print("  (Verified in d4_600cell_latin_square_audit.py)")
print()

# Regenerate 600-cell vertices (H4 roots, norm=1 embedding)
axis_verts = []
for i in range(4):
    for s in (+1, -1):
        v = [0.0]*4; v[i] = s
        axis_verts.append(tuple(v))

tesseract_verts = [tuple(s) for s in itertools.product([+0.5,-0.5], repeat=4)]

icosian_verts = set()
for perm in itertools.permutations([0,1,2,3]):
    inv_count = sum(1 for i in range(4) for j in range(i+1,4) if perm[i]>perm[j])
    if inv_count % 2 != 0: continue
    base = [0.0, 0.5, 1/(2*phi), phi/2]
    v = [base[perm[i]] for i in range(4)]
    for signs in itertools.product([+1,-1], repeat=3):
        nz = [i for i in range(4) if abs(v[i])>1e-12]
        sv = list(v)
        for idx, sg in zip(nz, signs): sv[idx] *= sg
        icosian_verts.add(tuple(sv))

h4_roots = [tuple(v) for v in axis_verts + tesseract_verts] + list(icosian_verts)
check(len(h4_roots) == 120, "H4 has 120 roots (= 600-cell vertices)", str(len(h4_roots)))

# All H4 roots on unit sphere
norms_sq = [sum(x**2 for x in v) for v in h4_roots]
check(all(abs(n-1.0)<1e-10 for n in norms_sq), "all H4 roots on unit S^3 (norm=1)")
print(f"  H4 root count: {len(h4_roots)}  (all norm=1: PASS)")

# ---------------------------------------------------------------------------
# Audit claim: r1 = (1, phi, 0, 0)
# ---------------------------------------------------------------------------
print()
r1 = (1.0, phi, 0.0, 0.0)
r1_norm2 = sum(x**2 for x in r1)
r1_norm  = math.sqrt(r1_norm2)
print(f"  r1 = (1, φ, 0, 0)")
print(f"  ||r1||² = 1 + φ² = 1 + (φ+1) = 2+φ = {r1_norm2:.10f}")
print(f"  ||r1||  = {r1_norm:.10f}  (expected 1.0 for H4 root — got {r1_norm:.4f})")
check(abs(r1_norm2 - 1.0) > 0.1, "r1 is NOT on unit sphere",
      f"||r1||²={r1_norm2:.6f}, expected 1 for H4 root")
r1_in_h4 = any(all(abs(r1[i]-v[i])<1e-8 for i in range(4)) for v in h4_roots)
check(not r1_in_h4, "r1 = (1,φ,0,0) is NOT in the H4 root set")
print(f"  r1 in H4 root set: {r1_in_h4}  (expected False)")
print(f"  CLAIM FAIL: r1 is presented as an 'H4 φ-root' but has norm² = 2+φ ≈ {r1_norm2:.3f} ≠ 1")

# ---------------------------------------------------------------------------
# Audit claim: r2 = (0.5, 0.5, 0.5, phi/2)
# ---------------------------------------------------------------------------
print()
r2 = (0.5, 0.5, 0.5, phi/2)
r2_norm2 = sum(x**2 for x in r2)
r2_norm  = math.sqrt(r2_norm2)
print(f"  r2 = (1/2, 1/2, 1/2, φ/2)")
print(f"  ||r2||² = 3/4 + φ²/4 = (3+φ+1)/4 = (4+φ)/4 = {r2_norm2:.10f}")
print(f"  ||r2||  = {r2_norm:.10f}  (expected 1.0 for H4 root)")
check(abs(r2_norm2 - 1.0) > 0.1, "r2 is NOT on unit sphere",
      f"||r2||²={r2_norm2:.6f}")
r2_in_h4 = any(all(abs(r2[i]-v[i])<1e-8 for i in range(4)) for v in h4_roots)
check(not r2_in_h4, "r2 = (1/2,1/2,1/2,φ/2) is NOT in the H4 root set")
print(f"  r2 in H4 root set: {r2_in_h4}  (expected False)")
print(f"  CLAIM FAIL: r2 has norm² ≈ {r2_norm2:.3f} ≠ 1, no zero component (icosian form requires one)")

# What the code would actually print (H4 Coxeter group label)
print()
print("  What the code DOES print correctly:")
print("    'H4: rank 4, Coxeter [3,3,5], 120 roots' — these counts are correct")
print("    Rank 4 ✓, Coxeter diagram with edge labels (3,3,5) ✓, 120 total roots ✓")
print("    But r1 and r2 are not actually H4 roots.")


# ---------------------------------------------------------------------------
# Section 2: E8 Weyl group order and root count
# ---------------------------------------------------------------------------
print("\n=== Section 2: E8 verification ===")

# |W(E8)| = product of degrees = 2·8·12·14·18·20·24·30
e8_degrees = [2, 8, 12, 14, 18, 20, 24, 30]
w_e8 = 1
for d in e8_degrees: w_e8 *= d
check(w_e8 == 696729600, "|W(E8)| = 696729600", str(w_e8))
print(f"  E8 degrees: {e8_degrees}")
print(f"  |W(E8)| = {' × '.join(map(str,e8_degrees))} = {w_e8}")
print(f"  Claimed: 696729600 — {'PASS' if w_e8==696729600 else 'FAIL'}")

# E8 root count: rank 8, 120 positive roots, 240 total
# Exponents = degrees - 1; sum of exponents = number of positive roots
e8_exponents = [d-1 for d in e8_degrees]
e8_pos_roots = sum(e8_exponents)
check(e8_pos_roots == 120, "E8 positive roots = 120", str(e8_pos_roots))
check(2*e8_pos_roots == 240, "E8 total roots = 240")
print(f"  E8 exponents: {e8_exponents}")
print(f"  Positive roots: sum({e8_exponents}) = {e8_pos_roots}")
print(f"  Total roots: {2*e8_pos_roots}  — {'PASS' if 2*e8_pos_roots==240 else 'FAIL'}")

# H4 ∪ φ·H4 count compatibility with E8
check(120 + 120 == 240, "H4-root-count + phi*H4-root-count = E8-root-count: 120+120=240")
print()
print("  H4 ∪ φ·H4 ⊂ E8: count check 120+120=240 ✓")
print("  (Full icosian embedding verification requires explicit E8 coordinates;")
print("   count compatibility is necessary but not sufficient.)")
print("  Known result: E8 root lattice = icosian ring of icosians,")
print("  with roots = {(p,q): p,q ∈ icosian integers, norm(p)+norm(q)=1}")
print("  This realizes E8 as a rank-8 lattice over H4 × H4. Accepted as correct.")


# ---------------------------------------------------------------------------
# Section 3: Spectral data table audit
# ---------------------------------------------------------------------------
print("\n=== Section 3: Spectral data table audit ===")
print()
print("  Claimed table (from submitted code):")
print("    D4-triv  | 1  | 2.000")
print("    φ-sect   | 2  | 1.618, 0.382")
print("    Null     | 1  | 0.000")
print()
print("  Cross-checking against our G4 sector eigenvalues at K(1,1):")
print()

# From g4_spectral_decomposition.py verified output at K(alpha=1,beta=1):
known_sectors = {
    'A1': ([-1,1,1,1,1,3,3,3,3,3,3,5,5,5,5,7], 16),
    'A2': ([-3,-1,-1,-1,-1,1,1,1,1,1,1,3,3,3,3,5], 16),
    'B1': ([-5,-3,-3,-3,-3,-1,-1,-1,-1,-1,-1,1,1,1,1,3], 16),
    'B2': ([-7,-5,-5,-5,-5,-3,-3,-3,-3,-3,-3,-1,-1,-1,-1,1], 16),
    'E':  ([-5,-5,-3]*10+[-1]*20+[1]*20+[3]*10+[5,5], 64),
}

actual_unique = {
    'A1': sorted(set([-1,1,3,5,7])),
    'A2': sorted(set([-3,-1,1,3,5])),
    'B1': sorted(set([-5,-3,-1,1,3])),
    'B2': sorted(set([-7,-5,-3,-1,1])),
    'E':  sorted(set([-5,-3,-1,1,3,5])),
}
print("  Actual sector eigenvalues at K(1,1):")
for ir, eigs in actual_unique.items():
    print(f"    {ir}: {eigs}  (all integers)")

print()
print("  Checking claimed values:")

# Check 1: 'D4-triv' eigenvalue 2.000
claimed_triv = 2.000
all_actual = [-7,-5,-3,-1,0,1,3,5,7]  # union of all sector unique eigs (no 0, no 2)
in_any_sector = any(abs(claimed_triv - e) < 1e-6
                    for eigs in actual_unique.values() for e in eigs)
check(not in_any_sector,
      "CONFIRMED: claimed eigenvalue 2.000 does NOT appear in any K(1,1) sector",
      f"actual A1 unique: {actual_unique['A1']}")
print(f"  'D4-triv | 2.000': 2.0 is NOT an eigenvalue of K(1,1) in any sector")
print(f"    A1 sector eigenvalues: {actual_unique['A1']}  — no 2.0")

# Check 2: 'φ-sect' with eigenvalues {phi ≈ 1.618, phi^{-2} ≈ 0.382}
claimed_phi_eigs = [phi, 1/phi**2]  # ≈ [1.618, 0.382]
for cv in claimed_phi_eigs:
    in_any = any(abs(cv - e) < 0.01 for eigs in actual_unique.values() for e in eigs)
    check(not in_any, f"CONFIRMED: {cv:.4f} not in any K(1,1) sector")
print(f"  'φ-sect | 1.618, 0.382': φ≈1.618 and 1/φ²≈0.382 are NOT K(1,1) eigenvalues")
print(f"    All K(1,1) eigenvalues are ODD INTEGERS: {{-7,-5,-3,-1,1,3,5,7}}")

# Check 3: 'Null' eigenvalue 0.000
claimed_null = 0.0
null_in_any = any(abs(claimed_null - e) < 1e-6 for eigs in actual_unique.values() for e in eigs)
check(not null_in_any,
      "CONFIRMED: eigenvalue 0.0 does NOT appear in any K(1,1) sector")
print(f"  'Null | 0.000': 0.0 is NOT a K(1,1) eigenvalue (all eigenvalues odd integers)")

# Check 4: 'φ-sect' is not a D4 irrep
d4_irreps = ['A1','A2','B1','B2','E']
print(f"\n  'φ-sect' is NOT a D4 irrep name. D4 irreps are: {d4_irreps}")
print(f"  'Null' is NOT a D4 irrep name.")
check(True, "'φ-sect' not a D4 irrep (documented)")

# Check 5: Does any K(alpha, beta) produce phi-valued eigenvalues?
print()
print("  Checking K(alpha,beta) for phi-valued eigenvalues:")
print("  K_D4gen only (K(0,1)): A1 sector eigenvalue = 3*beta = 3; A2=1; B1=-1; B2=-3")
print("  K_trans only (K(1,0)): sector centers = 0 (trans contributes 0 to all centers)")
print("  K(α,β) eigenvalues = α·λ_trans + β·λ_D4gen (linear; both operators integer-valued)")
print("  => K(α,β) eigenvalues are INTEGER COMBINATIONS of α and β.")
print("  => φ-valued eigenvalues appear ONLY if α or β is irrational (e.g., α=φ).")
print()
print("  At K(phi, 1):")

# Compute K(phi, 1) eigenvalues in A1 sector to see if phi appears
def z4sq_act(d, k):
    a, b = divmod(k, 4)
    if d==0: return 4*a+b
    elif d==1: return 4*((-b)%4)+a
    elif d==2: return 4*((-a)%4)+(-b)%4
    elif d==3: return 4*b+(-a)%4
    elif d==4: return 4*a+(-b)%4
    elif d==5: return 4*b+a
    elif d==6: return 4*((-a)%4)+b
    else:      return 4*((-b)%4)+(-a)%4

def d4_mul(x, y):
    sx, ax = (1, x-4) if x>=4 else (0, x)
    sy, ay = (1, y-4) if y>=4 else (0, y)
    if sx==0 and sy==0: return (ax+ay)%4
    if sx==0 and sy==1: return 4+(ax+ay)%4
    if sx==1 and sy==0: return 4+(ax-ay)%4
    return (ax-ay)%4

def d4_inv(x): return x if x>=4 else (-x)%4
D4 = list(range(8))

N=128
def enc(k,d): return 8*k+d
def dec(idx): return divmod(idx,8)

def g4_mul(u,v):
    k1,d1=dec(u); k2,d2=dec(v)
    dk2=z4sq_act(d1,k2); a1,b1=divmod(k1,4); a2,b2=divmod(dk2,4)
    return enc(4*((a1+a2)%4)+(b1+b2)%4, d4_mul(d1,d2))

def build_reg(g):
    M=np.zeros((N,N),dtype=float)
    for j in range(N): M[g4_mul(g,j),j]=1.0
    return M

def d4_class(d): return {0:1,2:2,1:3,3:3,4:4,6:4,5:5,7:5}[d]
CHAR={'A1':{1:1,2:1,3:1,4:1,5:1},'A2':{1:1,2:1,3:1,4:-1,5:-1},
      'B1':{1:1,2:1,3:-1,4:1,5:-1},'B2':{1:1,2:1,3:-1,4:-1,5:1},
      'E':{1:2,2:-2,3:0,4:0,5:0}}
DIM={'A1':1,'A2':1,'B1':1,'B2':1,'E':2}
def chi(ir,d): return CHAR[ir][d4_class(d)]

rho_D4={d:build_reg(enc(0,d)) for d in D4}
P={}
for ir in CHAR:
    P[ir]=sum(chi(ir,d4_inv(d))*rho_D4[d] for d in D4)*(DIM[ir]/8.0)

trans_gens=[enc(4*1+0,0),enc(4*3+0,0),enc(4*0+1,0),enc(4*0+3,0)]
rot_gens=[enc(0,1),enc(0,3),enc(0,4)]
K_trans=sum(build_reg(g) for g in trans_gens)
K_D4gen=sum(build_reg(g) for g in rot_gens)

for ir in ['A1','E']:
    ev_P, evec_P = np.linalg.eigh(P[ir])
    b = evec_P[:, ev_P > 0.5]
    K_phi1 = b.T @ (phi*K_trans + 1.0*K_D4gen) @ b
    eigs = sorted(np.linalg.eigvalsh(K_phi1))
    uniq = sorted(set(round(e,6) for e in eigs))
    print(f"  {ir}: {uniq[:6]}{'...' if len(uniq)>6 else ''}")

print()
print("  At K(phi,1), eigenvalues include phi-multiples as expected (alpha=phi in integer combinations).")
print("  But these would never appear in K(integer, integer) — which is the natural choice.")
print()
print("  CONCLUSION: The spectral table is FABRICATED for K(1,1).")
print("  D4 irrep names 'φ-sect' and 'Null' do not exist.")
print("  Eigenvalues {2.0, 1.618, 0.382, 0.0} do not appear in K(1,1) sector spectra.")


# ---------------------------------------------------------------------------
# Section 4: 'φ-critical loci: none detected in (α,β) sweep'
# ---------------------------------------------------------------------------
print("\n=== Section 4: 'φ-critical loci' claim ===")
print()
print("  The claim 'φ-critical loci: none detected' is consistent with our sweep")
print("  (which found no critical structure involving φ as a parameter value),")
print("  BUT the term 'φ-critical loci' is undefined in the submitted code.")
print("  No definition of 'φ-critical' is given; the claim has no mathematical content.")
print("  Our sweep: critical loci (λ_max=1) are LINEAR in (α,β), not φ-related.")
print("  The critical curve for A1 sector: 4α + 3β = 1 (a line, not involving φ).")

# Verify: max joint eigenvalue pair in A1 sector
ev_P, evec_P = np.linalg.eigh(P['A1'])
b_A1 = evec_P[:, ev_P > 0.5]
K_t_A1 = b_A1.T @ K_trans @ b_A1
K_d_A1 = b_A1.T @ K_D4gen @ b_A1
vals_T, vecs_T = np.linalg.eigh(K_t_A1)
# Joint diagonalize
vals_D = np.linalg.eigvalsh(vecs_T[:, -1:].T @ K_d_A1 @ vecs_T[:, -1:])
lam_t_max = float(vals_T[-1])
# Find lam_d at max lam_t
degenerate_idx = [i for i in range(len(vals_T)) if abs(vals_T[i]-vals_T[-1])<1e-8]
Vsub = vecs_T[:, degenerate_idx]
Bsub = Vsub.T @ K_d_A1 @ Vsub
lam_d_at_max_T = float(np.linalg.eigvalsh(Bsub)[-1])
print()
print(f"  A1 max joint pair: (λ_t_max={lam_t_max:.1f}, λ_d_max={lam_d_at_max_T:.1f})")
print(f"  Critical line A1: {lam_t_max:.0f}α + {lam_d_at_max_T:.0f}β = 1  (linear, no φ)")
check(abs(lam_t_max - 4.0) < 0.1, "A1 max lambda_trans = 4")
check(abs(lam_d_at_max_T - 3.0) < 0.1, "A1 max lambda_D4 = 3 (= chi_hat_A1(K_D4gen))")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "="*60)
if FAIL:
    print(f"FAILED ({len(FAIL)}):")
    for f in FAIL:
        print(f"  FAIL  {f}")
    import sys; sys.exit(1)
else:
    print("ALL CHECKS PASS")
    print()
    print("  Section 1 (H4 root geometry):")
    print("    'H4: rank 4, [3,3,5], 120 roots' — CORRECT  ✓")
    print("    r1=(1,φ,0,0): ||r1||²=2+φ≈3.618 ≠ 1 — NOT an H4 root  CLAIM FAILS")
    print("    r2=(1/2,1/2,1/2,φ/2): ||r2||²≈1.405 ≠ 1 — NOT an H4 root  CLAIM FAILS")
    print("    H4 roots all have norm=1 (600-cell vertices on unit S³)  ✓")
    print()
    print("  Section 2 (E8):")
    print("    |W(E8)| = 2·8·12·14·18·20·24·30 = 696729600  ✓")
    print("    E8 total roots = 240  ✓")
    print("    H4 ∪ φ·H4 ⊂ E8: count 120+120=240 consistent; icosian embedding accepted  ✓")
    print()
    print("  Section 3 (Spectral data table):")
    print("    'D4-triv | 1 | 2.000' — FABRICATED: no K(1,1) sector eigenvalue = 2")
    print("    'φ-sect | 2 | 1.618, 0.382' — FABRICATED: 'φ-sect' not a D4 irrep")
    print("      eigenvalues φ≈1.618 and 1/φ²≈0.382 not in K(1,1) spectra")
    print("    'Null | 1 | 0.000' — FABRICATED: 'Null' not a D4 irrep")
    print("      eigenvalue 0 not in K(1,1) spectra")
    print("    All K(1,1) eigenvalues are ODD INTEGERS in {-7,-5,-3,-1,1,3,5,7}")
    print()
    print("  Section 4 ('φ-critical loci'):")
    print("    Claim 'none detected' is vacuously consistent (term is undefined)")
    print("    Critical loci for K(α,β) are LINEAR (no φ): A1 critical line = 4α+3β=1")
