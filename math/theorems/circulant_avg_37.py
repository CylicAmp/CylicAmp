"""
circulant_avg_37.py

Eigenvalue analysis of the circulant averaging operator on Z/37Z
with window size N=10.

Operator:  (Af)(x) = (1/10) sum_{j=0}^{9} f(x+j mod 37)

As a 37×37 circulant matrix, its eigenvalues are complex:
  lambda_k = (1/10) sum_{j=0}^{9} exp(2*pi*i*j*k/37)
           = exp(9*pi*i*k/37) * sin(10*pi*k/37) / (10 * sin(pi*k/37))

The CLOSED-FORM formula gives the SQUARED magnitude:
  |lambda_k|^2 = [sin(10*pi*k/37) / (10 * sin(pi*k/37))]^2

This is real and non-negative for all k.

Dominant nontrivial eigenvalue (by squared magnitude):
  lambda_* = |lambda_1|^2 = |lambda_36|^2  ~= 0.7835

Spectral gap:
  gamma = 1 - lambda_*  ~= 0.2165

Note on notation: k=1 and k=36 are the dominant nontrivial modes.
In sorted order, |lambda_1|^2 is the SECOND-LARGEST squared magnitude
(after |lambda_0|^2 = 1). It is not "lambda_2" in the Fourier-index
sense — that refers to k=2, which gives |lambda_2|^2 ~= 0.3445.
"""

import numpy as np
from math import gcd

n = 37   # Z/37Z  (prime)
N = 10   # window size


def lam_sq_closed(k, N=N, n=n):
    """Squared magnitude |lambda_k|^2 via closed form. L'Hopital at k=0."""
    if k % n == 0:
        return 1.0
    return (np.sin(N * np.pi * k / n) / (N * np.sin(np.pi * k / n))) ** 2

def lam_complex(k, N=N, n=n):
    """Complex eigenvalue lambda_k of the circulant averaging operator."""
    return sum(np.exp(2j * np.pi * j * k / n) for j in range(N)) / N


# ──────────────────────────────────────────────────────────────────────────────
# VERIFY CLOSED FORM AGAINST DIRECT COMPUTATION
# ──────────────────────────────────────────────────────────────────────────────

for k in range(n):
    lc  = lam_sq_closed(k)
    ldk = lam_complex(k)
    assert abs(lc - abs(ldk)**2) < 1e-12, f"k={k}: closed={lc}, |direct|^2={abs(ldk)**2}"

# lambda_0 = 1 (trivial eigenvalue)
assert abs(lam_sq_closed(0) - 1.0) < 1e-15
assert abs(lam_complex(0) - 1.0) < 1e-14

# lambda_k = lambda_{n-k}  (symmetry: k and -k give conjugate complex eigenvalues)
for k in range(1, n):
    assert abs(lam_sq_closed(k) - lam_sq_closed(n - k)) < 1e-14

# Dominant nontrivial squared magnitude is at k=1 (and k=36 = -1 mod 37)
sq_mags = [lam_sq_closed(k) for k in range(n)]
lam_star = max(sq_mags[1:])
k_star = sq_mags.index(lam_star)

assert abs(lam_star - 0.7835169601) < 1e-9
assert k_star == 1
assert abs(lam_sq_closed(1) - lam_sq_closed(36)) < 1e-14

# Spectral gap
gamma = 1.0 - lam_star
assert abs(gamma - 0.2164830399) < 1e-9

# The complex eigenvalue at k=1 is NOT real
lam1_complex = lam_complex(1)
assert abs(lam1_complex.imag) > 0.5   # imaginary part is significant
assert abs(abs(lam1_complex)**2 - lam_star) < 1e-12   # |lambda_1|^2 = lambda_*

# |lambda_1| (operator norm contribution) != lambda_* (squared magnitude)
lam1_abs = abs(lam1_complex)
assert abs(lam1_abs - np.sqrt(lam_star)) < 1e-12
assert abs(lam1_abs - 0.8851649338) < 1e-9


# ──────────────────────────────────────────────────────────────────────────────
# ALL 37 SQUARED MAGNITUDES
# ──────────────────────────────────────────────────────────────────────────────

# Sorted (descending) squared magnitudes, deduplicated by symmetry
unique_sq = sorted(set(round(lam_sq_closed(k), 13) for k in range(n)), reverse=True)
# k=0 gives 1.0 (trivial), the rest appear in pairs {k, 37-k}

# Check against reference values from the verified output
assert abs(lam_sq_closed(1) - 0.7835169601) < 1e-9
assert abs(lam_sq_closed(2) - 0.3444756564) < 1e-9
assert abs(lam_sq_closed(3) - 0.0493868679) < 1e-9
assert abs(lam_sq_closed(4) - 0.0057210064) < 1e-9
assert abs(lam_sq_closed(5) - 0.0469942349) < 1e-9

# Max discrepancy across all k
max_disc = max(abs(lam_sq_closed(k) - abs(lam_complex(k))**2) for k in range(n))
assert max_disc < 1e-13


# ──────────────────────────────────────────────────────────────────────────────
# CONNECTION TO ord_37(10) = 3
# ──────────────────────────────────────────────────────────────────────────────

# The window size N=10, modulus n=37.
# 10 mod 37 = 10 = first non-trivial element of <10> in (Z/37Z)^x.
# ord_37(10) = 3  (the 3-cycle {1, 10, 26} under multiplication).
assert pow(10, 3, 37) == 1
assert pow(10, 1, 37) == 10   # N mod n = N itself

# gcd(N, n) = gcd(10, 37) = 1: the window has no common factor with the period.
assert gcd(N, n) == 1


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Circulant Averaging Operator on Z/37Z, Window Size N=10")
    print("=" * 66)

    print(f"\nOperator: (Af)(x) = (1/{N}) sum_{{j=0}}^{{{N-1}}} f(x+j mod {n})")
    print(f"Eigenvalues are complex; formula gives squared magnitudes |lambda_k|^2")

    print("\n── EIGENVALUE TABLE ──")
    print(f"  {'k':>3} | {'|lambda_k|^2 closed':>20} | {'|lambda_k|^2 direct':>20} | {'Re(lambda_k)':>14} | {'Im(lambda_k)':>14}")
    print("  " + "-"*80)
    for k in list(range(6)) + [35, 36]:
        lc  = lam_sq_closed(k)
        ldk = lam_complex(k)
        print(f"  {k:>3} | {lc:>20.10f} | {abs(ldk)**2:>20.10f} | {ldk.real:>14.10f} | {ldk.imag:>14.10f}")

    print(f"\n  Max discrepancy (closed vs direct): {max_disc:.2e}")

    print("\n── SPECTRAL GAP ──")
    print(f"  lambda_* = max_{{k!=0}} |lambda_k|^2 = {lam_star:.10f}")
    print(f"           attained at k=1 and k=36 (= -1 mod 37)")
    print(f"  |lambda_1| = sqrt(lambda_*) = {lam1_abs:.10f}  (complex eigenvalue magnitude)")
    print(f"  gamma = 1 - lambda_* = {gamma:.10f}")

    print("\n── NOTATION NOTE ──")
    print(f"  lambda_* is NOT 'lambda_2' in the Fourier-index sense.")
    print(f"  k=1 gives the dominant nontrivial mode; k=2 gives {lam_sq_closed(2):.10f}.")
    print(f"  In sorted order, lambda_* = |lambda_1|^2 is the second-largest squared")
    print(f"  magnitude (after |lambda_0|^2 = 1).")
    print(f"  The complex eigenvalue lambda_1 = {lam1_complex.real:.6f} + {lam1_complex.imag:.6f}i (not real).")

    print("\n── CONNECTION TO THE MODULUS ──")
    print(f"  N={N}, n={n}: gcd({N},{n}) = {gcd(N,n)}")
    print(f"  ord_37(10) = 3  (10^3 mod 37 = {pow(10,3,37)})")
    print(f"  The window size N=10 is the generator of the order-3 subgroup of (Z/37Z)^x")

    print()
    print("All assertions passed.")
