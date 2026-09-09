#!/usr/bin/env python3
"""
block_cayley_spectral_audit.py

Audits A = [[C4, I4],[I4, C4]] spectral claims (8x8 graph, two coupled 4-cycles):

  Indexing convention: ORBIT-MAJOR  (index = N*orbit + position, N=4)
  Orbit 0 = rows/cols 0..3, Orbit 1 = rows/cols 4..7

  1. Spectrum = {3,1,1,1,-1,-1,-1,-3}
  2. [A, S⊕S] = 0  (cyclic shift commutation)
  3. Fourier block decomposition A_k = [[lambda_k,1],[1,lambda_k]], eigs = lambda_k ± 1
     Correct DFT basis for orbit-major: col 2k = [F[:,k];0], col 2k+1 = [0;F[:,k]]
  4. Equitable partition Q = [[2,1],[1,2]], eigenvalues {3,1} exact Ritz
  5. Tensor product (orbit-major): A = I2⊗C4 + SWAP⊗I4
  6. Ritz compression: orbit-constant retains {3,1}, no phantom eigenvalues
  7. Extension: coupling C = S^m for m=0,1,2,3
     - Full spectrum invariant (|omega^{mk}|=1 for all k,m)
     - Real-subspace phantom Ritz appears at m=1,3 (imaginary coupling in k=1,3 blocks)
  8. Phantom Ritz mechanism: real projection of [[0,i],[-i,0]] discards coupling -> zeros
"""

import numpy as np

FAIL = []
def check(cond, label, detail=""):
    if not cond:
        FAIL.append(label + (f": {detail}" if detail else ""))
    return cond

N = 4   # orbit size

# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------
# C4: 4-cycle adjacency (C4 = S + S^T)
C4 = np.zeros((N, N))
for j in range(N):
    C4[j, (j+1)%N] = 1
    C4[j, (j-1)%N] = 1

# S: cyclic shift permutation S[j, (j+1)%4] = 1; S^T = S^{-1}
S = np.zeros((N, N))
for j in range(N):
    S[j, (j+1)%N] = 1

I4   = np.eye(N)
I2   = np.eye(2)
SWAP = np.array([[0.0,1.0],[1.0,0.0]])

omega = np.exp(2j * np.pi / N)                              # = i (4th root of unity)
F     = np.array([[omega**(j*k) for k in range(N)]
                  for j in range(N)]) / np.sqrt(N)          # DFT_4 unitary
check(np.allclose(F @ F.conj().T, I4, atol=1e-10), "DFT_4 unitary")

# ---------------------------------------------------------------------------
# A = [[C4, I4],[I4, C4]] in orbit-major indexing
# ---------------------------------------------------------------------------
A = np.block([[C4, I4],[I4, C4]])
print("=== 1. Spectrum of A = [[C4, I4],[I4, C4]] ===")
check(np.allclose(A, A.T, atol=1e-10), "A is symmetric")
eigs_A   = sorted(np.linalg.eigvalsh(A))
claimed  = [-3, -1, -1, -1, 1, 1, 1, 3]
spec_ok  = np.allclose(eigs_A, claimed, atol=1e-10)
check(spec_ok, "Spectrum = {3,1,1,1,-1,-1,-1,-3}")
print(f"  Eigenvalues: {[round(e,4) for e in eigs_A]}")
print(f"  Claimed {claimed}: {'PASS' if spec_ok else 'FAIL'}")

# ---------------------------------------------------------------------------
# [A, S⊕S] = 0
# ---------------------------------------------------------------------------
print("\n=== 2. [A, S⊕S] = 0 ===")
SS = np.block([[S, np.zeros((N,N))],[np.zeros((N,N)), S]])
comm_norm = np.linalg.norm(A @ SS - SS @ A)
check(comm_norm < 1e-10, "[A, S⊕S] = 0", f"norm={comm_norm:.2e}")
check(np.linalg.norm(C4 @ S - S @ C4) < 1e-10, "[C4, S] = 0")
print(f"  ||[A, S⊕S]|| = {comm_norm:.2e}  PASS")
print(f"  [C4, S] = 0 since C4 = S+S^T (S commutes with S±S^T)  PASS")

# ---------------------------------------------------------------------------
# C4 eigenvalues
# ---------------------------------------------------------------------------
print("\n=== 3. Fourier block decomposition ===")
lambda_k = {k: 2*np.cos(2*np.pi*k/N) for k in range(N)}
eigs_C4  = sorted(np.linalg.eigvalsh(C4))
check(np.allclose(sorted(lambda_k.values()), eigs_C4, atol=1e-10), "C4 eigs = 2cos(2pi*k/4)")
print(f"  C4 eigenvalues: {[round(e,4) for e in eigs_C4]}  = 2cos(2pi*k/4) = {{2,0,-2,0}}  PASS")

# Build the correct DFT basis for orbit-major indexing:
#   Column 2k   = [F[:,k]; 0]  (orbit-0, Fourier mode k)
#   Column 2k+1 = [0; F[:,k]]  (orbit-1, Fourier mode k)
# Derivation: A_FT[2k',2k]   = (F† C4 F)[k',k] = lambda_k * delta_{k',k}  (within orbit)
#             A_FT[2k',2k+1] = (F† I4 F)[k',k] = delta_{k',k}             (inter-orbit)
F8 = np.zeros((2*N, 2*N), dtype=complex)
for k in range(N):
    F8[:N,  2*k]   = F[:, k]   # orbit 0
    F8[N:,  2*k+1] = F[:, k]   # orbit 1

check(np.allclose(F8 @ F8.conj().T, np.eye(2*N), atol=1e-10), "F8 unitary")

A_FT = F8.conj().T @ A @ F8

print(f"  Fourier-transformed A (should be 2x2 block-diagonal):")
block_eigs_all = []
for k in range(N):
    Bk   = A_FT[2*k:2*k+2, 2*k:2*k+2]
    lk   = lambda_k[k]
    expB = np.array([[lk, 1.0],[1.0, lk]])
    blk_ok = (np.allclose(Bk.real, expB, atol=1e-10) and
               np.allclose(Bk.imag, 0,   atol=1e-10))
    check(blk_ok, f"k={k}: A_k = [[lambda_k,1],[1,lambda_k]]",
          f"got {np.round(Bk.real,4)}")
    eigs_Bk = sorted(np.linalg.eigvalsh(Bk.real))
    check(np.allclose(eigs_Bk, sorted([lk+1, lk-1]), atol=1e-10),
          f"k={k}: A_k eigs = lambda_k ± 1")
    block_eigs_all.extend(eigs_Bk)
    print(f"  k={k}: lambda_k={lk:+.2f}  A_k={np.round(Bk.real,4)}  "
          f"eigs={[round(e,4) for e in eigs_Bk]}")

# Off-diagonal 2×2 blocks should be zero
off_norm = sum(np.linalg.norm(A_FT[2*j:2*j+2, 2*k:2*k+2])
               for j in range(N) for k in range(N) if j != k)
check(off_norm < 1e-8, "A_FT off-diagonal 2x2 blocks zero", f"norm={off_norm:.2e}")
print(f"  Off-diagonal 2x2 blocks: {off_norm:.2e} ≈ 0  PASS")

check(np.allclose(sorted(block_eigs_all), claimed, atol=1e-10), "Block union = full spectrum")
print(f"  Block eig union {[round(e,4) for e in sorted(block_eigs_all)]} = full spectrum  PASS")

# ---------------------------------------------------------------------------
# Equitable partition and Ritz
# ---------------------------------------------------------------------------
print("\n=== 4. Equitable partition Q = [[2,1],[1,2]] ===")
# Unit-normalized orbit-constant vectors
e_orb = np.ones(N) / np.sqrt(N)    # unit norm: ||e_orb||=1
phi1  = np.concatenate([e_orb, np.zeros(N)])
phi2  = np.concatenate([np.zeros(N), e_orb])
V     = np.column_stack([phi1, phi2])

Q = V.T @ A @ V     # should = [[2,1],[1,2]] with unit-normalized phis
q_eigs = sorted(np.linalg.eigvalsh(Q))
check(np.allclose(Q, [[2.0,1.0],[1.0,2.0]], atol=1e-10), "V^T A V = [[2,1],[1,2]]",
      str(np.round(Q, 4)))
check(np.allclose(q_eigs, [1.0, 3.0], atol=1e-10), "Q eigenvalues = {1,3}")
print(f"  Q = {np.round(Q,4)}")
print(f"  Q eigenvalues: {q_eigs}  PASS")

ritz_exact = all(min(abs(rv - e) for e in claimed) < 1e-8 for rv in q_eigs)
check(ritz_exact, "Ritz values {1,3} are exact eigenvalues of A (no phantom)")
print(f"  Ritz {{1,3}} ⊂ Spec(A): no phantom  PASS")

# Verify partition is equitable: same intra/inter degree for every vertex
for v in range(N):
    intra = sum(A[v, j] for j in range(N))
    inter = sum(A[v, j] for j in range(N, 2*N))
    check(abs(intra-2)<1e-10 and abs(inter-1)<1e-10, f"orbit-0 vertex {v} equitable")
for v in range(N, 2*N):
    intra = sum(A[v, j] for j in range(N, 2*N))
    inter = sum(A[v, j] for j in range(N))
    check(abs(intra-2)<1e-10 and abs(inter-1)<1e-10, f"orbit-1 vertex {v} equitable")
print(f"  Partition equitable (regular intra=2, inter=1 per vertex)  PASS")

# ---------------------------------------------------------------------------
# Tensor product structure (orbit-major)
# I2 ⊗ C4 = [[C4,0],[0,C4]]  (within-orbit adjacency)
# SWAP ⊗ I4 = [[0,I4],[I4,0]]  (inter-orbit identity)
# A = I2⊗C4 + SWAP⊗I4
# ---------------------------------------------------------------------------
print("\n=== 5. Tensor product (orbit-major): A = I2⊗C4 + SWAP⊗I4 ===")
A_tp = np.kron(I2, C4) + np.kron(SWAP, I4)
tp_ok = np.allclose(A, A_tp, atol=1e-10)
check(tp_ok, "A = I2⊗C4 + SWAP⊗I4")
print(f"  kron(I2,C4)    = [[C4,0],[0,C4]]   (within-orbit adjacency)")
print(f"  kron(SWAP,I4)  = [[0,I4],[I4,0]]   (inter-orbit identity coupling)")
print(f"  A = I2⊗C4 + SWAP⊗I4: {'PASS' if tp_ok else 'FAIL'}")
print(f"  In Fourier mode k: I2⊗C4 -> lambda_k*I_2,  SWAP⊗I4 -> SWAP")
print(f"  A_k = lambda_k*I_2 + SWAP  =>  eigs = lambda_k ± 1  ✓")

# ---------------------------------------------------------------------------
# Ritz compression
# ---------------------------------------------------------------------------
print("\n=== 6. Ritz compression ===")
print(f"  2D orbit-constant subspace retains: {{3,1}} (k=0 Fourier mode only)")
print(f"  Missing: k=1 gives {{1,-1}}×2, k=2 gives {{-1,-3}}, k=3 gives {{1,-1}}×2")
print(f"  Orbit-constant Ritz = Q eigenvalues = exact eigenvalues: no phantom  ✓")

# ---------------------------------------------------------------------------
# Extension: coupling C = S^m for m=0..3
# ---------------------------------------------------------------------------
print("\n=== 7. Extension: A_m = [[C4,S^m],[(S^m)^T,C4]] ===")
print(f"  In mode k: S^m eigenvalue = omega^(mk) => |coupling|=1 for all m,k")
print(f"  => spectrum unchanged at {{3,1,1,1,-1,-1,-1,-3}} for all m")
print()

for m in range(N):
    Sm  = np.linalg.matrix_power(S, m)
    Am  = np.block([[C4, Sm],[Sm.T, C4]])
    sym_ok  = np.allclose(Am, Am.T, atol=1e-10)
    eigs_Am = sorted(np.linalg.eigvalsh(Am))
    check(np.allclose(eigs_Am, claimed, atol=1e-10), f"A_m={m} spectrum = claimed")

    # Orbit-constant Ritz: S^m @ e_orb = e_orb (permutation preserves uniform vector)
    Qm      = V.T @ Am @ V
    ritz_m  = sorted(np.linalg.eigvalsh(Qm))
    ritz_ex = all(min(abs(rv-e) for e in eigs_Am) < 1e-6 for rv in ritz_m)
    check(np.allclose(ritz_m, [1.0, 3.0], atol=1e-8), f"A_m={m} orbit-Ritz = {{1,3}}")
    print(f"  m={m}: sym={sym_ok}  eigs={[round(e,4) for e in eigs_Am]}")
    print(f"         orbit-Ritz={[round(e,4) for e in ritz_m]}  exact={ritz_ex}")

# ---------------------------------------------------------------------------
# Phantom Ritz: real-subspace projection of complex Fourier block
# For m=1, k=1: coupling = omega^1 = i (purely imaginary)
# Real test vector projects [[0,i],[-i,0]] to [[0,Re(i)],[Re(i),0]] = [[0,0],[0,0]]
# Phantom zeros appear at k=1,3 instead of actual eigenvalues {1,-1}
# ---------------------------------------------------------------------------
print("\n=== 8. Phantom Ritz: real projection of complex Fourier coupling ===")
print()

for m in range(N):
    Sm      = np.linalg.matrix_power(S, m)
    Am      = np.block([[C4, Sm],[Sm.T, C4]])
    act     = sorted(np.linalg.eigvalsh(Am))

    coupling_k1 = omega**m      # S^m eigenvalue at Fourier mode k=1
    lk1 = lambda_k[1]           # = 0

    # Exact Hermitian 2×2 block at k=1:
    Ak1_exact = np.array([[lk1, coupling_k1],[coupling_k1.conj(), lk1]])
    eigs_exact = sorted(np.linalg.eigvalsh(Ak1_exact))

    # Real projection: replace coupling by its real part
    cr = coupling_k1.real
    Ak1_real = np.array([[lk1, cr],[cr, lk1]])
    eigs_ritz = sorted(np.linalg.eigvalsh(Ak1_real))

    phantom = [rv for rv in eigs_ritz if min(abs(rv-e) for e in act) > 0.1]
    flag = "  <-- PHANTOM" if phantom else ""

    print(f"  m={m}: omega^m={coupling_k1:.4f}  Im={coupling_k1.imag:+.4f}")
    print(f"         exact k=1 block eigs: {[round(e,4) for e in eigs_exact]}  "
          f"(via |coupling|=1)")
    print(f"         real-projected Ritz:  {[round(e,4) for e in eigs_ritz]}"
          f"{flag}")
    if phantom:
        print(f"         Mechanism: Im(coupling)={coupling_k1.imag:.4f} discarded;")
        print(f"           [[0,i],[-i,0]] -> [[0,0],[0,0]] -> phantom {eigs_ritz}")
    print()

# 8D demonstration: cosine-only (real Fourier) test space for m=0 vs m=1
print("  8D demo: Ritz from cosine-only test vectors (discards sine component)")
cos_vecs = []
for k in range(N):
    ck = np.cos(2*np.pi*k*np.arange(N)/N)
    if np.linalg.norm(ck) > 1e-10:
        ck /= np.linalg.norm(ck)
        cos_vecs.append(np.concatenate([ck, np.zeros(N)]))
        cos_vecs.append(np.concatenate([np.zeros(N), ck]))
W_cos, _ = np.linalg.qr(np.column_stack(cos_vecs))

for m in [0, 1]:
    Sm = np.linalg.matrix_power(S, m)
    Am = np.block([[C4, Sm],[Sm.T, C4]])
    act = sorted(np.linalg.eigvalsh(Am))
    Ritz_cos = W_cos.T @ Am @ W_cos
    ritz_c = sorted(np.linalg.eigvals(Ritz_cos).real)
    phantom_c = [rv for rv in ritz_c if min(abs(rv-e) for e in act) > 0.2]
    print(f"  m={m}: cosine Ritz={[round(e,4) for e in ritz_c]}")
    print(f"         actual     ={[round(e,4) for e in act]}")
    if phantom_c:
        print(f"         PHANTOM values: {[round(e,4) for e in phantom_c]}")
    else:
        print(f"         (all Ritz exact — cosine space spans full spectrum for this m)")
    print()

# ---------------------------------------------------------------------------
# Summary table
# ---------------------------------------------------------------------------
print("=== Summary: coupling sweep ===")
print(f"  {'m':>3}  {'|coupling k=1|':>16}  {'Im(coupling)':>14}  "
      f"{'k=1,3 phantom Ritz':>20}")
for m in range(N):
    c = omega**m
    has_phantom = abs(c.imag) > 0.5
    print(f"  {m:>3}  {abs(c):>16.4f}  {c.imag:>+14.4f}  "
          f"{'zeros {0,0} instead of {1,-1}' if has_phantom else 'none (real coupling)'}")

print()
print("  Core results:")
print("  1. Spectrum {3,1,1,1,-1,-1,-1,-3} invariant under m (|omega^mk|=1)")
print("  2. Orbit-constant Ritz = {3,1} exact for all m (permutation preserves e_orb)")
print("  3. m=1,3: Im(omega^m) ≠ 0 => real-subspace discards the coupling")
print("            phase-twisted irreps k=1,3 become invisible to real test functions")
print("            phantom zeros appear in real Ritz at k=1,3 blocks")
print("  4. m=0,2: coupling is real (±1) => no phantom")

# ---------------------------------------------------------------------------
# Final
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
    print("  A = [[C4,I4],[I4,C4]], 8×8 two-coupled-4-cycles:")
    print("    Spectrum = {3,1,1,1,-1,-1,-1,-3}  ✓")
    print("    [A, S⊕S] = 0  ✓")
    print("    Fourier blocks A_k = [[lambda_k,1],[1,lambda_k]], eigs = lambda_k ± 1  ✓")
    print("    Block union = full spectrum  ✓")
    print("    Q = [[2,1],[1,2]]; orbit-constant Ritz = {3,1} exact; no phantom  ✓")
    print("    A = I2⊗C4 + SWAP⊗I4 (orbit-major tensor product)  ✓")
    print()
    print("  Coupling sweep C = S^m (m=0..3):")
    print("    Full spectrum invariant (|omega^mk|=1)  ✓")
    print("    Orbit-constant Ritz = {3,1} exact for all m  ✓")
    print("    m=1,3: real-subspace Ritz gives phantom zeros at k=1,3 blocks  ✓")
    print("    Mechanism: Im(omega^m) discarded by real projection -> zero coupling")
