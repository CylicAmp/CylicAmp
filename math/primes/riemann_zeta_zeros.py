"""
Riemann Zeta Zeros — high-precision output + digit reduction analysis
First zero to 40 significant figures; zeros 1-8 with digital root table.
"""

import mpmath

mpmath.mp.dps = 50  # 50 dps internal precision

# ── High-precision first zero ──────────────────────────────────────────────
z1 = mpmath.zetazero(1)
t1 = mpmath.im(z1)
print("Zero 1 (40 sig figs):", mpmath.nstr(t1, 40))
print()

# ── Digital root helper ────────────────────────────────────────────────────
def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9

# ── Digit reduction table for zeros 1-8 ───────────────────────────────────
# For each zero: take first two significant digits d1, d2
# Compute: |d1-d2|, DR(d1+d2)
# Then apply the add-then-reduce chain: DR(d1+d2) + DR(|d1-d2|) → DR(...)
print(f"{'Zero':<6} {'t (40 s.f.)':<42} {'d1':>3} {'d2':>3} {'|diff|':>7} {'DR(sum)':>8} {'chain→':>8}")
print("─" * 82)

for n in range(1, 9):
    z = mpmath.zetazero(n)
    t = mpmath.im(z)
    s = mpmath.nstr(t, 40)
    digits = s.replace('.', '').lstrip('0')
    d1, d2 = int(digits[0]), int(digits[1])
    diff_val = abs(d1 - d2)
    sum_dr   = dr(d1 + d2)
    diff_dr  = dr(diff_val) if diff_val else 0
    chain    = dr(sum_dr + diff_dr)  # fold both reductions together
    print(f"{n:<6} {s:<42} {d1:>3} {d2:>3} {diff_val:>7} {sum_dr:>8} {chain:>8}")

# ── Zero 1 deep-digit table: 4 vs 7 cycle ─────────────────────────────────
# 14.134725...  →  digits at positions 3,4,6 are 4, 7
# 7 - 4 = 3
# 4 + 7 = 11 → DR = 2
# 3 + 7 = 10 → DR = 1
# DR(2) + DR(1) = 3  ← fixed point
print()
print("── Zero 1 inner digit cycle: 4 vs 7 ──────────────────────────────")
print(f"  14.13472514...  →  prominent digits: 4, 7")
print(f"  7  − 4  = 3          (difference)")
print(f"  4  + 7  = 11  → DR = {dr(11)}")
print(f"  3  + 7  = 10  → DR = {dr(10)}")
print(f"  DR(11) + DR(10) = {dr(11)} + {dr(10)} = {dr(11)+dr(10)}  → DR = {dr(dr(11)+dr(10))}  ← fixed point")
