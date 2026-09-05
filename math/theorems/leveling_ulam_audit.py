"""
leveling_ulam_audit.py

Verifies six leveling phenomena and the Ulam diagonal prime pools.

─────────────────────────────────────────────────────────────────
VERIFIED:
  Seeds/factors/DR for {26,27,28,29,30,7777}
  Harmonic leveling H_n − ln(n) → γ
  Prime density π(x)/x vs 1/ln(x)
  Modular flatness: max deviation mod 9 and mod 28 up to 100000
  Perfect balance points (perfect numbers): 6, 28, 496
  Collatz global convergence to 1 for all seeds
  Ulam diagonal prime counts (A=SW, B=NW, C=NE) for k-windows

Ulam diagonal formulas (k=1,2,...):
  A (SW): 4k² + 2k + 1
  B (NW): 4k² + 1
  C (NE): 4k² − 2k + 1
  SE    : (2k+1)²  — all composite for k ≥ 1
─────────────────────────────────────────────────────────────────
"""

import math
from sympy import factorint, isprime, primepi

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = abs(n) % 9
    return r if r else 9


# ── Seeds: factors and digital roots ─────────────────────────────────────────

SEEDS = {
    26:   ({2: 1, 13: 1}, 8,  False),
    27:   ({3: 3},        9,  False),
    28:   ({2: 2, 7: 1},  1,  False),
    29:   ({29: 1},       2,  True),
    30:   ({2: 1, 3: 1, 5: 1}, 3, False),
    7777: ({7: 1, 11: 1, 101: 1}, 1, False),
}

for n, (factors, dr_val, prime) in SEEDS.items():
    check(factorint(n) == factors,
          f"factors({n})", factorint(n), factors)
    check(dr(n) == dr_val,
          f"dr({n})", dr(n), dr_val)
    check(isprime(n) == prime,
          f"isprime({n})", isprime(n), prime)

# 7777 = 7 × 11 × 101 explicit
check(7 * 11 * 101 == 7777, "7 × 11 × 101 = 7777", 7 * 11 * 101, 7777)
check(dr(7777) == 1, "DR(7777) = 1", dr(7777), 1)


# ── Harmonic leveling: H_n − ln(n) → γ ───────────────────────────────────────

EULER_GAMMA = 0.5772156649015328606065120900824024310421593359

def H(n):
    return sum(1 / k for k in range(1, n + 1))

TARGET = [
    (100,   0.58220733),
    (1000,  0.57771558),
    (10000, 0.57726566),
]

for n, expected_diff in TARGET:
    diff = H(n) - math.log(n)
    check(abs(diff - expected_diff) < 1e-7,
          f"H({n}) − ln({n}) ≈ {expected_diff}", round(diff, 8), expected_diff)
    check(diff > EULER_GAMMA,
          f"H({n}) − ln({n}) > γ (convergence from above)", diff > EULER_GAMMA, True)


# ── Prime density leveling ────────────────────────────────────────────────────

DENSITY = [
    (1000,   0.168000, 0.144765),
    (10000,  0.122900, 0.108574),
    (100000, 0.095920, 0.086859),
]

for x, pi_ratio, inv_ln in DENSITY:
    pi_x = primepi(x)
    check(abs(pi_x / x - pi_ratio) < 1e-5,
          f"π({x})/x ≈ {pi_ratio}", round(pi_x / x, 6), pi_ratio)
    check(abs(1 / math.log(x) - inv_ln) < 1e-5,
          f"1/ln({x}) ≈ {inv_ln}", round(1 / math.log(x), 6), inv_ln)
    # π(x)/x > 1/ln(x) for these x (prime race offset)
    check(pi_x / x > 1 / math.log(x),
          f"π({x})/x > 1/ln({x})", pi_x / x > 1 / math.log(x), True)


# ── Modular flatness ──────────────────────────────────────────────────────────

# Mod 9, integers 1..100000
# 100000 = 11111×9 + 1  →  residue 1 has 11112, all others 11111
expected_9 = 100000 / 9
counts_9 = [sum(1 for n in range(1, 100001) if n % 9 == r) for r in range(9)]
# Faster: analytic
counts_9_analytic = []
for r in range(9):
    start = r if r > 0 else 9
    count = (100000 - start) // 9 + 1 if start <= 100000 else 0
    counts_9_analytic.append(count)
max_dev_9 = max(abs(c - expected_9) for c in counts_9_analytic)
rel_dev_9 = max_dev_9 / expected_9

check(abs(max_dev_9 - 0.89) < 0.01,
      "mod 9 max dev ≈ 0.89", round(max_dev_9, 2), 0.89)
check(abs(rel_dev_9 - 0.000080) < 1e-5,
      "mod 9 relative dev ≈ 0.000080", round(rel_dev_9, 6), 0.000080)

# Mod 28, integers 1..100000
# 100000 = 3571×28 + 12  →  residues 1..12 have 3572, residues 0,13..27 have 3571
expected_28 = 100000 / 28
counts_28_analytic = []
for r in range(28):
    start = r if r > 0 else 28
    count = (100000 - start) // 28 + 1 if start <= 100000 else 0
    counts_28_analytic.append(count)
max_dev_28 = max(abs(c - expected_28) for c in counts_28_analytic)
rel_dev_28 = max_dev_28 / expected_28

check(abs(max_dev_28 - 0.57) < 0.01,
      "mod 28 max dev ≈ 0.57", round(max_dev_28, 2), 0.57)
check(abs(rel_dev_28 - 0.000160) < 1e-5,
      "mod 28 relative dev ≈ 0.000160", round(rel_dev_28, 6), 0.000160)


# ── Perfect balance points ────────────────────────────────────────────────────

def proper_divisor_sum(n):
    return sum(d for d in range(1, n) if n % d == 0)

for p in [6, 28, 496]:
    check(proper_divisor_sum(p) == p,
          f"σ_proper({p}) = {p} (perfect number)", proper_divisor_sum(p), p)

# Factor structures
check(6   == 2 * 3,          "6 = 2 × 3",           2 * 3,      6)
check(28  == 4 * 7,          "28 = 4 × 7 = 2² × 7", 4 * 7,      28)
check(496 == 16 * 31,        "496 = 2⁴ × 31",        16 * 31,    496)
check(isprime(3),            "3 prime", isprime(3), True)
check(isprime(7),            "7 prime", isprime(7), True)
check(isprime(31),           "31 prime", isprime(31), True)

# Euler's formula: perfect = 2^(p-1)(2^p - 1) for Mersenne prime 2^p-1
check(2**(2-1) * (2**2-1) == 6,   "2^1 × (2²-1) = 6",   2**(2-1)*(2**2-1), 6)
check(2**(3-1) * (2**3-1) == 28,  "2^2 × (2³-1) = 28",  2**(3-1)*(2**3-1), 28)
check(2**(5-1) * (2**5-1) == 496, "2^4 × (2⁵-1) = 496", 2**(5-1)*(2**5-1), 496)


# ── Collatz convergence ───────────────────────────────────────────────────────

def collatz_reaches_1(n, limit=10000):
    seen = set()
    while n != 1 and n not in seen and limit > 0:
        seen.add(n)
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        limit -= 1
    return n == 1

for seed in [26, 27, 28, 29, 30, 7777]:
    check(collatz_reaches_1(seed),
          f"Collatz({seed}) reaches 1", collatz_reaches_1(seed), True)


# ── Ulam diagonal prime pools ─────────────────────────────────────────────────

# Diagonal formulas (k=1,2,...):
# A (SW): 4k² + 2k + 1
# B (NW): 4k² + 1
# C (NE): 4k² - 2k + 1
# SE    : (2k+1)² — all composite for k ≥ 1

def diag_A(k): return 4*k*k + 2*k + 1
def diag_B(k): return 4*k*k + 1
def diag_C(k): return 4*k*k - 2*k + 1

def prime_count_window(formula, k_start, k_end):
    return sum(1 for k in range(k_start, k_end + 1) if isprime(formula(k)))

# SE diagonal: all composite for k ≥ 1
for k in range(1, 51):
    check(not isprime((2*k+1)**2),
          f"SE k={k}: (2k+1)²={(2*k+1)**2} composite",
          isprime((2*k+1)**2), False)

# Verified prime counts per window
WINDOWS = [
    ("A", diag_A,  1, 10,  6),
    ("A", diag_A, 10, 19,  3),
    ("A", diag_A, 20, 29,  2),
    ("A", diag_A, 40, 49,  2),
    ("B", diag_B,  1, 10,  7),
    ("B", diag_B, 10, 19,  4),
    ("B", diag_B, 20, 29,  3),
    ("B", diag_B, 40, 49,  3),
    ("C", diag_C,  1, 10,  5),
    ("C", diag_C, 10, 19,  3),
    ("C", diag_C, 20, 29,  2),
    ("C", diag_C, 40, 49,  1),
]

for name, fn, k0, k1, expected_count in WINDOWS:
    count = prime_count_window(fn, k0, k1)
    check(count == expected_count,
          f"Diag {name} k={k0}-{k1}: {expected_count} primes", count, expected_count)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Leveling and Ulam Diagonal Audit")
    print("=" * 66)

    print(f"\n── Seeds: factors and DR ──")
    print(f"  {'n':>5}  {'factors':<22}  {'DR':>3}  {'prime':>6}")
    for n, (factors, dr_val, prime) in SEEDS.items():
        print(f"  {n:5d}  {str(factors):<22}  {dr_val:3d}  {str(prime):>6}")

    print(f"\n── Harmonic leveling: H_n − ln(n) → γ ──")
    print(f"  γ = {EULER_GAMMA:.10f}")
    for n, expected_diff in TARGET:
        diff = H(n) - math.log(n)
        print(f"  n={n:6d}: {diff:.8f}  (target {expected_diff})")

    print(f"\n── Prime density ──")
    for x, pi_ratio, inv_ln in DENSITY:
        print(f"  x={x:6d}: π(x)/x={pi_ratio:.6f}  1/ln(x)={inv_ln:.6f}")

    print(f"\n── Modular flatness (integers 1..100000) ──")
    print(f"  mod 9:  max dev={max_dev_9:.2f}  relative={rel_dev_9:.6f}")
    print(f"  mod 28: max dev={max_dev_28:.2f}  relative={rel_dev_28:.6f}")

    print(f"\n── Perfect numbers ──")
    for p in [6, 28, 496]:
        print(f"  σ_proper({p}) = {proper_divisor_sum(p)}  ✓")

    print(f"\n── Collatz convergence ──")
    for seed in [26, 27, 28, 29, 30, 7777]:
        print(f"  {seed} → 1: {collatz_reaches_1(seed)}")

    print(f"\n── Ulam diagonals (A=4k²+2k+1, B=4k²+1, C=4k²-2k+1) ──")
    print(f"  {'diag':<2}  {'k-window':<10}  {'primes':>6}")
    for name, fn, k0, k1, expected_count in WINDOWS:
        count = prime_count_window(fn, k0, k1)
        print(f"  {name}   k={k0:2d}..{k1:2d}      {count:6d}")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
