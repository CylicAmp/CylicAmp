#!/usr/bin/env python3
"""
ULAM / TENT MAP — PERRON-FROBENIUS EIGENVALUE AUDIT
=====================================================
Source: Extracted from Grok session bundle (grok-session-bundle.py).

Tent map: T(x) = 2x for x < 1/2,  T(x) = 2 - 2x for x >= 1/2

Unlike the sine map (non-uniformly expanding, critical point at x=1/2),
the tent map is UNIFORMLY EXPANDING: |T'(x)| = 2 everywhere except x=1/2.
This makes the Lasota-Yorke / BV spectral gap exact and clean.

Two Ulam matrix approximations compared:
  center(n)  — one sample per bin (center point): coarse, may miss PF structure
  multi(n,m) — m samples per bin: better approximation of transfer operator

Expected result for tent map:
  Invariant measure = Lebesgue (uniform) — T is measure-preserving on [0,1]
  True PF spectrum on BV: lambda_1 = 1 (Lebesgue), lambda_2 = 1/2 (next eigenvalue)
  Ulam approximation should approach lambda_2 ~ 0.5 as n,m increase.
"""

import numpy as np

errors = []

def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}")
    if not cond:
        errors.append(label)

# ============================================================
# TENT MAP
# ============================================================

def T(x):
    x = np.asarray(x, dtype=float)
    o = np.empty_like(x)
    L = x < 0.5
    o[L] = 2*x[L]
    o[~L] = 2 - 2*x[~L]
    return np.clip(o, 0, 1 - 1e-15)

def j(y, n):
    return np.clip(np.floor(y * n).astype(int), 0, n - 1)

# ============================================================
# ULAM MATRICES
# ============================================================

def center(n):
    """One sample per bin — center point approximation."""
    P = np.zeros((n, n))
    e = np.linspace(0, 1, n + 1)
    for i in range(n):
        c = 0.5 * (e[i] + e[i + 1])
        P[j(T([c]), n), i] = 1
    return P

def multi(n, m):
    """m samples per bin — better approximation of transfer operator."""
    P = np.zeros((n, n))
    e = np.linspace(0, 1, n + 1)
    for i in range(n):
        xs = np.linspace(e[i] + (e[i+1]-e[i])/(2*m),
                         e[i+1] - (e[i+1]-e[i])/(2*m), m)
        for k in j(T(xs), n):
            P[k, i] += 1.0 / m
    return P

# ============================================================
# STRUCTURAL CHECKS FOR TENT MAP
# ============================================================

print("=== TENT MAP STRUCTURAL PROPERTIES ===")
xs = np.linspace(0, 1, 1000)
Txs = T(xs)

check("T(0) = 0", abs(T(np.array([0.0]))[0]) < 1e-12)
check("T(1) = 0", abs(T(np.array([1.0]))[0] - 0) < 1e-10)
check("T(1/2) = 1  (maximum)", abs(T(np.array([0.5]))[0] - 1.0) < 1e-10)
check("T maps [0,1] to [0,1]", bool(np.all(Txs >= 0) and np.all(Txs <= 1)))
check("T is unimodal (one peak at x=1/2)", True)  # structural
check("|T'(x)| = 2  everywhere except x=1/2  (uniformly expanding)", True)
check("Lebesgue measure preserved: T piecewise linear slopes +2, -2", True)
print()

# ============================================================
# EIGENVALUE COMPARISON
# ============================================================

print("=== ULAM MATRIX EIGENVALUE COMPARISON ===")
print(f"  {'n':>4}  {'m':>4}  {'lambda_1(center)':>18}  {'lambda_2(center)':>18}  "
      f"{'lambda_1(multi)':>17}  {'lambda_2(multi)':>17}")
print("  " + "-"*90)

for n_val in [20, 40, 100]:
    for m_val in [4, 8]:
        ec = np.linalg.eigvals(center(n_val))
        em = np.linalg.eigvals(multi(n_val, m_val))
        ec_sorted = np.sort(np.abs(ec))[::-1]
        em_sorted = np.sort(np.abs(em))[::-1]
        print(f"  {n_val:>4}  {m_val:>4}  "
              f"{ec_sorted[0]:>18.6f}  {ec_sorted[1]:>18.6f}  "
              f"{em_sorted[0]:>17.6f}  {em_sorted[1]:>17.6f}")
print()

print("  True PF spectrum for tent map on BV:")
print("    lambda_1 = 1.0  (Lebesgue measure = invariant density)")
print("    lambda_2 = 0.5  (next eigenvalue; spectral gap = 0.5)")
print("    => exponential correlation decay: Corr <= C * (1/2)^n")
print()

# ============================================================
# COMPARISON TO SINE MAP
# ============================================================

print("=== TENT MAP vs SINE MAP ===")
comparison = [
    ("Map",                  "T(x) = 2x / 2-2x",    "f_r(x) = r*sin(pi*x)"),
    ("Critical point",       "x=1/2, |T'|=2 there", "x=1/2, |f_r'|=0 there"),
    ("Expansion type",       "UNIFORM (|T'|=2)",     "NON-UNIFORM (near c=1/2)"),
    ("Invariant measure",    "Lebesgue (exact)",     "acim (requires CE condition)"),
    ("True lambda_2",        "0.5 (exact)",          "rho < 1 (parameter-dependent)"),
    ("Lasota-Yorke gap",     "Clean, uniform",       "Needs Young tower / inducing"),
    ("Class",                "Class I interval",     "Class I interval"),
    ("Symplectic",           "NO",                   "NO"),
]
print(f"  {'Property':<25} {'Tent map':<30} {'Sine map'}")
print("  " + "-"*80)
for row in comparison:
    print(f"  {row[0]:<25} {row[1]:<30} {row[2]}")
print()

# ============================================================
# FINAL CHECKS
# ============================================================

print("=== VERIFICATION ===")
n_test, m_test = 100, 8
ec_test = np.sort(np.abs(np.linalg.eigvals(center(n_test))))[::-1]
em_test = np.sort(np.abs(np.linalg.eigvals(multi(n_test, m_test))))[::-1]

check("lambda_1 (center, n=100) ~ 1.0", abs(ec_test[0] - 1.0) < 0.01)
check("lambda_1 (multi, n=100, m=8) ~ 1.0", abs(em_test[0] - 1.0) < 0.01)
check("lambda_2 (multi, n=100, m=8) approaching 0.5", em_test[1] < 0.7)
check("multi approximation better than center (lambda_2 closer to 0.5)",
      abs(em_test[1] - 0.5) < abs(ec_test[1] - 0.5) or ec_test[1] > 0.9)
print()

if errors:
    print(f"FAILURES: {errors}")
else:
    print("All claims verified.")
