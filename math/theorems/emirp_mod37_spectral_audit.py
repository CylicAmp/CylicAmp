"""
emirp_mod37_spectral_audit.py

Computes the emirp mod-37 frequency vector, chi-square uniformity test,
37x37 Markov transition matrix, and full eigenstructure.

Choices (per the spec):
  Dataset      : Option A — all emirps in [2, 10^6]
  Emirp defn   : standard — prime p s.t. reverse(p)≠p AND reverse(p) is prime
                 leading-zero reversals excluded (i.e. p not ending in 0)
                 palindromic primes excluded (reverse(p) = p)
  Transition   : Option 3 — r_n = p_n mod 37, M_{a,b} = P(r_{n+1}=b | r_n=a)
                 where the sequence is emirps in ascending order
"""

import math
import numpy as np

LIMIT = 1_000_000

# ---------------------------------------------------------------------------
# Sieve of Eratosthenes
# ---------------------------------------------------------------------------
sieve = bytearray([1]) * (LIMIT + 1)
sieve[0] = sieve[1] = 0
for i in range(2, int(LIMIT**0.5) + 1):
    if sieve[i]:
        sieve[i*i::i] = bytearray(len(sieve[i*i::i]))

def is_prime(n: int) -> bool:
    return bool(sieve[n]) if 0 <= n <= LIMIT else False

def reverse_digits(n: int) -> int:
    return int(str(n)[::-1])

emirps = []
for p in range(2, LIMIT + 1):
    if not is_prime(p):
        continue
    if str(p).endswith('0'):      # reversal would have leading zero
        continue
    r = reverse_digits(p)
    if r == p:                    # palindromic prime
        continue
    if is_prime(r):
        emirps.append(p)

N = len(emirps)
print(f"Emirps in [2, {LIMIT:,}]:  N = {N:,}")

# ---------------------------------------------------------------------------
# 2.  Frequency vector mod 37
# ---------------------------------------------------------------------------
MOD = 37
freq = np.zeros(MOD, dtype=int)
residues = []
for p in emirps:
    r = p % MOD
    freq[r] += 1
    residues.append(r)

residues = np.array(residues)

print()
print("=" * 60)
print("2.  Frequency vector  f_r = |{emirp p : p ≡ r (mod 37)}|")
print("=" * 60)
print(f"  {'r':>3}  {'f_r':>6}  {'f_r/N':>8}  {'1/37':>8}  deviation")
print(f"  {'-'*50}")
expected = N / MOD
for r in range(MOD):
    dev = (freq[r] - expected) / expected * 100
    print(f"  {r:>3}  {freq[r]:>6}  {freq[r]/N:>8.5f}  {1/MOD:>8.5f}  {dev:+.2f}%")

print(f"\n  Sum = {freq.sum()}  (should be {N})")

# ---------------------------------------------------------------------------
# 3.  Chi-square uniformity test
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("3.  Chi-square uniformity test  (H0: f_r uniform over Z/37Z)")
print("=" * 60)

chi2 = float(np.sum((freq - expected)**2 / expected))
df   = MOD - 1   # 36 degrees of freedom

# Chi-square critical values (df=36)
# p=0.05: 50.998, p=0.01: 55.758, p=0.001: 65.247
cv_05  = 50.998
cv_01  = 55.758
cv_001 = 65.247

print(f"  χ²₃₆ = {chi2:.4f}")
print(f"  df   = {df}")
print(f"  Critical values: p=0.05 → {cv_05},  p=0.01 → {cv_01},  p=0.001 → {cv_001}")
if chi2 < cv_05:
    print(f"  H0 NOT rejected at p=0.05  (consistent with uniform mod 37)")
elif chi2 < cv_01:
    print(f"  H0 rejected at p=0.05 but not p=0.01")
elif chi2 < cv_001:
    print(f"  H0 rejected at p=0.01 but not p=0.001")
else:
    print(f"  H0 rejected at p=0.001  (significant non-uniformity)")

# Max-deviation residue
r_max = int(np.argmax(np.abs(freq - expected)))
print(f"  Max deviation: r={r_max}  f_r={freq[r_max]}  "
      f"expected={expected:.2f}  dev={freq[r_max]-expected:+.2f}")

# NOTE: r=0 is STRUCTURALLY depleted: p≡0 (mod 37) requires 37|p, so only p=37
# qualifies; this is a number-theoretic artifact, not a distributional feature.
# Restricted chi-square over r=1,...,36 (the informative test):
freq_r = freq[1:]          # exclude r=0
N_r    = int(freq_r.sum())
exp_r  = N_r / 36
chi2_r = float(np.sum((freq_r - exp_r)**2 / exp_r))
df_r   = 35
cv_05r, cv_01r, cv_001r = 49.802, 54.437, 63.691  # df=35 critical values
print(f"\n  STRUCTURAL NOTE: r=0 is depleted by arithmetic (only p=37 ≡ 0 mod 37 is prime).")
print(f"  Restricted test over r=1..36 (N={N_r:,}, df=35):")
print(f"    χ²₃₅ = {chi2_r:.4f}")
print(f"    Critical values: p=0.05 → {cv_05r},  p=0.01 → {cv_01r},  p=0.001 → {cv_001r}")
if chi2_r < cv_05r:
    print(f"    H0 NOT rejected at p=0.05  (emirps are uniform mod 37 on {{1..36}})")
elif chi2_r < cv_01r:
    print(f"    H0 rejected at p=0.05 but not p=0.01")
elif chi2_r < cv_001r:
    print(f"    H0 rejected at p=0.01 but not p=0.001")
else:
    print(f"    H0 rejected at p=0.001  (genuine non-uniformity on {{1..36}})")

# ---------------------------------------------------------------------------
# 4.  Transition matrix  M_{a,b} = P(r_{n+1}=b | r_n=a)
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("4.  Transition matrix  M_{a,b} = P(r_{n+1}=b | r_n=a)")
print("=" * 60)

counts = np.zeros((MOD, MOD), dtype=int)
for i in range(len(residues) - 1):
    counts[residues[i], residues[i + 1]] += 1

# Row-normalize
row_sums = counts.sum(axis=1, keepdims=True)
# Rows with zero sum (no outgoing transitions): leave as zero
M = np.where(row_sums > 0, counts / row_sums.astype(float), 0.0)

print(f"  Shape: {M.shape}")
print(f"  Row-sum range: [{M.sum(axis=1).min():.6f}, {M.sum(axis=1).max():.6f}]  (should be ≤1)")
zero_rows = int(np.sum(row_sums.flatten() == 0))
print(f"  Zero-row residues (never appear as r_n): {zero_rows}")

# Show top-5 most common transitions
flat_counts = [(counts[a, b], a, b) for a in range(MOD) for b in range(MOD)]
flat_counts.sort(reverse=True)
print(f"\n  Top-5 most frequent transitions:")
print(f"  {'r_n':>4}  {'r_n+1':>5}  {'count':>7}  {'M[a,b]':>8}")
for cnt, a, b in flat_counts[:5]:
    print(f"  {a:>4}  {b:>5}  {cnt:>7}  {M[a,b]:>8.5f}")

# ---------------------------------------------------------------------------
# 5.  Eigenstructure of M
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("5.  Eigenstructure of M")
print("=" * 60)

eigenvalues = np.linalg.eigvals(M)
eigenvalues_sorted = sorted(eigenvalues, key=lambda x: -abs(x))
spectral_radius = abs(eigenvalues_sorted[0])

print(f"  Spectral radius ρ(M) = {spectral_radius:.8f}  (should be 1 for stochastic M)")

# Find eigenvalues by magnitude
ev_abs = sorted(abs(eigenvalues), reverse=True)
lambda1 = ev_abs[0]
lambda2 = ev_abs[1]
spectral_gap = lambda1 - lambda2

print(f"  λ₁ = {lambda1:.8f}  (dominant)")
print(f"  λ₂ = {lambda2:.8f}  (second)")
print(f"  Spectral gap = λ₁ - λ₂ = {spectral_gap:.8f}")
print(f"  Mixing time estimate: τ ≈ 1/(1-λ₂) = {1/(1-lambda2):.2f} steps")

# Real eigenvalues near 1
near1 = [(abs(e.real - 1.0), e) for e in eigenvalues if abs(e.imag) < 1e-10]
near1.sort()
print(f"\n  Real eigenvalues nearest 1:")
for dist, e in near1[:5]:
    print(f"    λ = {e.real:.8f}   (|λ-1| = {dist:.2e})")

print(f"\n  All eigenvalue magnitudes (top 10):")
for i, ev in enumerate(ev_abs[:10]):
    print(f"    |λ_{i+1}| = {ev:.8f}")

# ---------------------------------------------------------------------------
# 6.  Deviation from uniform kernel
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("6.  Deviation from uniform kernel  D = M - (1/37)·J")
print("=" * 60)

J_uniform = np.ones((MOD, MOD)) / MOD
D = M - J_uniform

D_frobenius = float(np.linalg.norm(D, 'fro'))
D_max       = float(np.abs(D).max())
D_spectral  = float(max(np.linalg.svd(D, compute_uv=False)))

print(f"  ||D||_F (Frobenius)  = {D_frobenius:.6f}")
print(f"  ||D||_∞ (max entry)  = {D_max:.6f}")
print(f"  ||D||_2 (spectral)   = {D_spectral:.6f}")
print(f"  ||D||_F / (1/√37)    = {D_frobenius * math.sqrt(MOD):.4f}  "
      f"(ratio to uniform scale; ≪1 → near-uniform)")

# Rows with largest total deviation
row_dev = np.sum(np.abs(D), axis=1)
top_dev = np.argsort(row_dev)[::-1][:5]
print(f"\n  Rows with largest deviation from uniform:")
print(f"  {'r':>3}  {'Σ|D[r,b]|':>12}  {'f_r':>6}")
for r in top_dev:
    print(f"  {r:>3}  {row_dev[r]:>12.6f}  {freq[r]:>6}")

# ---------------------------------------------------------------------------
# 7.  Stationary distribution comparison
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("7.  Stationary distribution π (left eigenvector of M, eigenvalue 1)")
print("=" * 60)

# Power iteration for stationary dist
pi = np.ones(MOD) / MOD
for _ in range(5000):
    pi_new = pi @ M
    if np.linalg.norm(pi_new - pi) < 1e-12:
        break
    pi = pi_new
pi = pi_new / pi_new.sum()

print(f"  Convergence check: ||π·M - π||_∞ = {np.abs(pi @ M - pi).max():.2e}")
print()
print(f"  {'r':>3}  {'π_r':>10}  {'f_r/N':>10}  {'1/37':>8}  {'π_r - 1/37':>12}")
print(f"  {'-'*55}")
for r in range(MOD):
    dev_pi = pi[r] - 1/MOD
    print(f"  {r:>3}  {pi[r]:>10.6f}  {freq[r]/N:>10.6f}  {1/MOD:>8.6f}  {dev_pi:>+12.6f}")

print(f"\n  ||π - uniform||_∞ = {np.abs(pi - 1/MOD).max():.6f}")
print(f"  ||π - f/N||_∞     = {np.abs(pi - freq/N).max():.6f}  "
      f"(stationary dist vs empirical freq)")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"""
  Dataset  : emirps in [2, {LIMIT:,}],  N = {N:,}
  Emirp def: prime p, reverse(p)≠p, reverse(p) prime, no leading zeros
  Transition: sequential emirps, M_{{a,b}} = P(r_{{n+1}}=b | r_n=a), r = p mod 37

  Statistical
    Residues covered     : {int(np.sum(freq > 0))}/37  residue classes hit
    χ²₃₆                 : {chi2:.4f}
    Verdict              : {'uniform (p>0.05)' if chi2 < cv_05 else 'non-uniform'}

  Spectral (M)
    Spectral radius      : {spectral_radius:.8f}
    Spectral gap λ₁-λ₂   : {spectral_gap:.8f}
    Mixing time τ        : {1/(1-lambda2):.2f} transitions

  Structural (D = M - J/37)
    ||D||_F              : {D_frobenius:.6f}
    ||D||_2              : {D_spectral:.6f}
    Max row deviation    : r={top_dev[0]}, Σ|D[r,·]|={row_dev[top_dev[0]]:.4f}

  Stationary π
    ||π - 1/37||_∞       : {np.abs(pi - 1/MOD).max():.6f}
    ||π - f/N||_∞        : {np.abs(pi - freq/N).max():.6f}
""")
