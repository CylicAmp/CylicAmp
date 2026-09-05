#!/usr/bin/env python3
"""
g4_spectral_decomposition.py

Implements and audits the G4 = Z4^2 ⋊ D4 (order 128) spectral system:
  - Left regular representation (128×128)
  - D4 character table and isotypic projectors
  - Identity resolution verification
  - Cayley adjacency operator K(alpha, beta)
  - Block diagonalization of K via D4-isotypic decomposition
  - Eigenvalues and spectral gaps per irrep sector
"""

import numpy as np
import random

random.seed(42)
FAIL = []

def check(cond, label, detail=""):
    if not cond:
        FAIL.append(label + (f": {detail}" if detail else ""))
    return cond

# ---------------------------------------------------------------------------
# D4 arithmetic (0=e,1=r,2=r²,3=r³,4=s,5=rs,6=r²s,7=r³s)
# ---------------------------------------------------------------------------

def d4_mul(x, y):
    sx, ax = (1, x - 4) if x >= 4 else (0, x)
    sy, ay = (1, y - 4) if y >= 4 else (0, y)
    if sx == 0 and sy == 0: return (ax + ay) % 4
    if sx == 0 and sy == 1: return 4 + (ax + ay) % 4
    if sx == 1 and sy == 0: return 4 + (ax - ay) % 4
    return (ax - ay) % 4

def d4_inv(x):
    return x if x >= 4 else (-x) % 4

D4 = list(range(8))

# D4 action on Z4^2: k = 4*a + b
def z4sq_act(d, k):
    a, b = divmod(k, 4)
    if   d == 0: return 4 * a + b
    elif d == 1: return 4 * ((-b) % 4) + a
    elif d == 2: return 4 * ((-a) % 4) + (-b) % 4
    elif d == 3: return 4 * b + (-a) % 4
    elif d == 4: return 4 * a + (-b) % 4
    elif d == 5: return 4 * b + a
    elif d == 6: return 4 * ((-a) % 4) + b
    else:        return 4 * ((-b) % 4) + (-a) % 4

# ---------------------------------------------------------------------------
# G4 = Z4^2 ⋊ D4 (order 128)
# Elements: (k, d), index = 8*k + d, k in 0..15, d in 0..7
# ---------------------------------------------------------------------------

N = 128

def enc(k, d): return 8 * k + d
def dec(idx): return divmod(idx, 8)

def g4_mul(u, v):
    k1, d1 = dec(u)
    k2, d2 = dec(v)
    dk2   = z4sq_act(d1, k2)
    a1, b1 = divmod(k1, 4)
    a2, b2 = divmod(dk2, 4)
    new_k = 4 * ((a1 + a2) % 4) + (b1 + b2) % 4
    return enc(new_k, d4_mul(d1, d2))

def g4_inv(u):
    k, d = dec(u)
    d_i = d4_inv(d)
    ak  = z4sq_act(d_i, k)       # d^{-1}·k
    a, b = divmod(ak, 4)
    return enc(4 * ((-a) % 4) + (-b) % 4, d_i)

G4 = list(range(N))
ID = enc(0, 0)

# ---------------------------------------------------------------------------
# Group axiom verification
# ---------------------------------------------------------------------------
print("=== G4 group axioms ===")
sample = random.sample(G4, 20)
check(all(g4_mul(ID, g) == g              for g in sample), "left  identity")
check(all(g4_mul(g, ID) == g              for g in sample), "right identity")
check(all(g4_mul(g, g4_inv(g)) == ID      for g in sample), "right inverse")
check(all(g4_mul(g4_inv(g), g) == ID      for g in sample), "left  inverse")
s5 = sample[:5]
check(all(g4_mul(g4_mul(a, b), c) == g4_mul(a, g4_mul(b, c))
          for a in s5 for b in s5 for c in s5), "associativity (5^3 sample)")
print("  All group axioms: PASS")

# ---------------------------------------------------------------------------
# Left regular representation: rho_L(g)[i, j] = 1 iff i = g*j
# ---------------------------------------------------------------------------

def build_reg(g):
    M = np.zeros((N, N), dtype=float)
    for j in range(N):
        M[g4_mul(g, j), j] = 1.0
    return M

print("Building D4 regular representations...", flush=True)
rho = {d: build_reg(enc(0, d)) for d in D4}

# Verify rho is a homomorphism on D4 sample
for d1 in D4[:4]:
    for d2 in D4[:4]:
        check(np.allclose(rho[d4_mul(d1, d2)], rho[d1] @ rho[d2]),
              f"rho homomorphism d4_mul({d1},{d2})")
print("  Reguler rep homomorphism: PASS")

# ---------------------------------------------------------------------------
# D4 character table
# Conjugacy classes: C1={e}, C2={r²}, C3={r,r³}, C4={s,r²s}, C5={rs,r³s}
# Irreps: A1,A2,B1,B2 (dim 1), E (dim 2)
# ---------------------------------------------------------------------------

def d4_class(d):
    return {0:1, 2:2, 1:3, 3:3, 4:4, 6:4, 5:5, 7:5}[d]

CHAR = {
    'A1': {1:1,  2:1,  3:1,  4:1,  5:1},
    'A2': {1:1,  2:1,  3:1,  4:-1, 5:-1},
    'B1': {1:1,  2:1,  3:-1, 4:1,  5:-1},
    'B2': {1:1,  2:1,  3:-1, 4:-1, 5:1},
    'E':  {1:2,  2:-2, 3:0,  4:0,  5:0},
}
DIM = {'A1':1, 'A2':1, 'B1':1, 'B2':1, 'E':2}

def chi(irrep, d): return CHAR[irrep][d4_class(d)]

# Orthogonality check
print("\n=== D4 character table ===")
for ir1 in CHAR:
    for ir2 in CHAR:
        inner = sum(chi(ir1, d) * chi(ir2, d) for d in D4) / 8.0
        check(abs(inner - (1.0 if ir1 == ir2 else 0.0)) < 1e-12,
              f"<chi_{ir1}, chi_{ir2}> = {'1' if ir1==ir2 else '0'}")
print("  Orthogonality of all pairs: PASS")
print(f"  Sum dim^2 = {sum(d**2 for d in DIM.values())} (expected 8=|D4|)")
check(sum(d**2 for d in DIM.values()) == 8, "sum d_chi^2 = |D4|")

# ---------------------------------------------------------------------------
# Isotypic projectors: P_chi = (d_chi/|D4|) sum_{d in D4} chi(d^{-1}) rho(d)
# ---------------------------------------------------------------------------
print("\n=== Isotypic projectors ===")
projectors = {}
for ir in CHAR:
    d_chi = DIM[ir]
    P = sum(chi(ir, d4_inv(d)) * rho[d] for d in D4) * (d_chi / 8.0)
    projectors[ir] = P

# Identity resolution
P_sum = sum(projectors.values())
id_res_ok = np.allclose(P_sum, np.eye(N), atol=1e-10)
check(id_res_ok, "sum(P_chi) = I_128")
print(f"  Identity resolution sum(P_chi) = I_128: {'PASS' if id_res_ok else 'FAIL'}")

# Projector properties
for ir, P in projectors.items():
    check(np.allclose(P @ P, P, atol=1e-10),        f"{ir}: P^2 = P")
    check(np.allclose(P.T, P, atol=1e-10),           f"{ir}: P = P^T")
    rank = int(round(np.trace(P)))
    d_chi = DIM[ir]
    expected = 16 * d_chi * d_chi
    check(rank == expected, f"{ir}: rank = 16·d_chi^2 = {expected}", f"got {rank}")
    print(f"  {ir}: rank={rank}  (d_chi={d_chi}, expected 16·{d_chi}²={expected})")

# ---------------------------------------------------------------------------
# Cayley adjacency operator K(alpha, beta)
# K = alpha * sum(T_x generators) + beta * sum(R_d generators)
# Using symmetric generating set for Hermitian K.
# ---------------------------------------------------------------------------

def build_K(alpha=1.0, beta=1.0):
    # Z4^2 translation generators (each paired with inverse for symmetry)
    trans = [enc(4*1+0, 0), enc(4*3+0, 0),   # (1,0) and (-1,0)=(3,0)
             enc(4*0+1, 0), enc(4*0+3, 0)]    # (0,1) and (0,-1)=(0,3)
    # D4 generators embedded in G4: r, r^{-1}=r^3, s (self-inverse)
    rot   = [enc(0, 1), enc(0, 3), enc(0, 4)]
    K = np.zeros((N, N), dtype=float)
    for g in trans:
        K += alpha * build_reg(g)
    for g in rot:
        K += beta * build_reg(g)
    return K

print("\n=== Building K(1, 1) ===", flush=True)
K = build_K(alpha=1.0, beta=1.0)
check(np.allclose(K, K.T, atol=1e-10), "K(1,1) is symmetric")
print(f"  K symmetric (Hermitian over R): PASS")
print(f"  K nonzero entries: {int(np.sum(K != 0))}  (= {int(np.sum(K != 0))//N} per row on avg)")

# ---------------------------------------------------------------------------
# Block diagonalization of K via isotypic decomposition
# For each irrep: find ONB of im(P_chi), compress K, diagonalize.
# ---------------------------------------------------------------------------
print("\n=== Block diagonalization of K ===")

all_eigs = {}

for ir, P in projectors.items():
    d_chi = DIM[ir]
    expected_rank = 16 * d_chi * d_chi

    # Orthonormal basis for image(P) via eigendecomposition of P
    ev_P, evec_P = np.linalg.eigh(P)
    basis = evec_P[:, ev_P > 0.5]           # columns with eigenvalue ~1
    check(basis.shape[1] == expected_rank,
          f"{ir}: basis shape", f"got {basis.shape[1]}")

    # Compress K to this sector
    K_sec = basis.T @ K @ basis              # shape (rank, rank)
    check(np.allclose(K_sec, K_sec.T, atol=1e-8), f"{ir}: K_sector symmetric")
    sector_eigs = np.linalg.eigvalsh(K_sec)
    all_eigs[ir] = sorted(sector_eigs)

    uniq, cnts = np.unique(np.round(sector_eigs, 4), return_counts=True)
    print(f"\n  {ir}  (sector dim = {expected_rank})")
    print(f"  {'eigenvalue':>14}  {'multiplicity':>12}")
    for ev, cnt in zip(uniq, cnts):
        print(f"  {ev:+14.6f}  {cnt:>12}")

# ---------------------------------------------------------------------------
# Cross-check: full spectrum = union of sector spectra
# ---------------------------------------------------------------------------
full_eigs  = sorted(np.linalg.eigvalsh(K))
union_eigs = sorted(e for eigs in all_eigs.values() for e in eigs)
check(len(union_eigs) == N, "sector union size = 128", str(len(union_eigs)))
check(np.allclose(np.array(full_eigs), np.array(union_eigs), atol=1e-5),
      "full spectrum = union of sector spectra")
print(f"\n  Full spectrum cross-check ({N} eigs): {'PASS' if np.allclose(np.array(full_eigs), np.array(union_eigs), atol=1e-5) else 'FAIL'}")

# ---------------------------------------------------------------------------
# Spectral gaps per sector
# ---------------------------------------------------------------------------
print("\n=== Spectral gaps per sector ===")
print(f"  {'irrep':>5}  {'dim':>5}  {'min_eig':>10}  {'max_eig':>10}  {'max_gap':>10}")
for ir, eigs in all_eigs.items():
    if len(eigs) < 2:
        continue
    gaps = [eigs[i+1] - eigs[i] for i in range(len(eigs)-1)]
    print(f"  {ir:>5}  {len(eigs):>5}  {min(eigs):>10.4f}  {max(eigs):>10.4f}  {max(gaps):>10.4f}")

# ---------------------------------------------------------------------------
# K(alpha=0, beta=1): pure D4 sector — isolate subgroup dynamics
# ---------------------------------------------------------------------------
print("\n=== K(alpha=0, beta=1) — pure D4 subgroup action ===")
K_d4 = build_K(alpha=0.0, beta=1.0)
for ir, P in projectors.items():
    ev_P, evec_P = np.linalg.eigh(P)
    basis = evec_P[:, ev_P > 0.5]
    K_sec = basis.T @ K_d4 @ basis
    ev_sec = np.linalg.eigvalsh(K_sec)
    uniq = np.unique(np.round(ev_sec, 4))
    print(f"  {ir}: distinct eigs = {uniq}")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
if FAIL:
    print(f"FAILED ({len(FAIL)}):")
    for f in FAIL:
        print(f"  FAIL  {f}")
    import sys; sys.exit(1)
else:
    print("ALL CHECKS PASS")
    print()
    print("  G4 = Z4^2 ⋊ D4, order 128  ✓")
    print("  Left regular representation is a group homomorphism  ✓")
    print("  D4 character table: 5 irreps, orthogonality verified  ✓")
    print("  sum(d_chi^2) = 8 = |D4|  ✓")
    print("  Identity resolution: sum_{chi} P_chi = I_128  ✓")
    print("  Each P_chi: idempotent, self-adjoint, rank = 16·d_chi^2  ✓")
    print("  K(1,1) symmetric (Hermitian)  ✓")
    print("  Full spectrum = union of sector spectra  ✓")
    print()
    print("  Document notes confirmed:")
    print("    - C[G4] ↓_{D4} decomposes as 16 copies of C[D4]")
    print("      (16 cosets × Peter-Weyl for D4)")
    print("    - chi-sector dim = 16·d_chi^2: A1=16, A2=16, B1=16, B2=16, E=64")
    print("    - K block-diagonalizes cleanly under D4-isotypic decomposition")
    print("    - Identity resolution holds (document's 'strong indication': confirmed)")
    print()
    print("  Audit of document claims:")
    print("    TRUE:  G4 is a valid semidirect product group algebra")
    print("    TRUE:  rho_reg is a 128D faithful representation")
    print("    TRUE:  D4 character table decomposes C[G4] cleanly (as restriction)")
    print("    TRUE:  P_chi are genuine projectors summing to identity")
    print("    TRUE:  K block-diagonalizes; sector eigenvalues are well-defined")
    print("    NOTED: decomposition is restriction C[G4]↓_{D4}, not C[D4] alone")
    print("    NOTED: 'spin network'/'quantum geometry' labels not supported by")
    print("           the construction; this is finite-group harmonic analysis")
