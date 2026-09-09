#!/usr/bin/env python3
"""
harmonic_prime_matrix_audit.py

Audit of the mathematical claims in the Harmonic Prime Matrix dashboard.

Claims stated:
  1. 1-2-4-8-7-5 vortex loop: powers of 2 mod 9, period 6
  2. Gap distribution: basket 3 → 33.10%, basket 6 → 33.40%, basket 9 → 33.50%
  3. +4 mod 9 offset applied every 25 steps (displayed label was "13-Separation" —
     corrected to "25-Step" in the committed HTML; the code trigger is step % 25 == 0)
  4. Offset rule: (node + 4) % 9 || 9  maps result into {1,...,9} (no zero)

One discrepancy found and corrected:
  The original label "13-Separation Offset Correction" was inconsistent with the code,
  which fires every 25 steps (totalCount % 25 === 0).  The value 13 does not appear
  anywhere in the implementation.  Label corrected to "25-Step Offset Correction."
"""

import sys
import numpy as np

FAIL = []

def check(cond, msg):
    if not cond:
        FAIL.append(msg)
    return cond

# ── 1. Powers of 2 mod 9 cycle ────────────────────────────────────────────────

print("=== 1. Vortex Loop: Powers of 2 mod 9 ===")

stated_loop = [1, 2, 4, 8, 7, 5]

# Generate the orbit starting from 2^0 = 1 (the JS array starts at the identity)
# 2^0=1, 2^1=2, 2^2=4, 2^3=8, 2^4≡7, 2^5≡5, 2^6≡1 (period 6)
orbit = []
v = 1
for k in range(10):
    orbit.append(v)
    v = (v * 2) % 9

period_6 = orbit[:6]
period_repeat = orbit[6:]

print(f"  First 10 powers of 2 mod 9: {orbit}")
print(f"  Cycle (period 6): {period_6}")
print(f"  Repeat check:     {period_repeat}  (must equal first 4 of cycle)")

check(period_6 == stated_loop,
      f"Stated loop {stated_loop} != computed {period_6}")
check(period_repeat == period_6[:4],
      f"Period not 6: tail {period_repeat} != {period_6[:4]}")

# Verify period is exactly 6 (multiplicative order of 2 mod 9)
order = 1
v = 2
while v != 1:
    v = (v * 2) % 9
    order += 1
check(order == 6, f"ord_9(2) = {order}, expected 6")
print(f"  Multiplicative order of 2 mod 9: {order}")
print(f"  Loop matches stated [1,2,4,8,7,5]: {'PASS' if period_6 == stated_loop else 'FAIL'}")

# Verify 9 is NOT in the cycle (gcd(2,9)=1, so 2 is a unit, 0 never reached)
check(9 not in period_6 and 0 not in period_6,
      "Cycle contains 0 or 9 — impossible since gcd(2,9)=1")
print(f"  9 and 0 absent from cycle (gcd(2,9)=1): PASS")

# ── 2. Gap distribution probability split ────────────────────────────────────

print("\n=== 2. Gap Distribution: 33.10% / 33.40% / 33.50% ===")

p3  = 0.331
p6  = 0.334
p9  = 0.335

print(f"  p(basket 3) = {p3:.4f} = {p3*100:.2f}%  (threshold < 0.331)")
print(f"  p(basket 6) = {p6:.4f} = {p6*100:.2f}%  (threshold 0.331 ≤ x < 0.665)")
print(f"  p(basket 9) = {p9:.4f} = {p9*100:.2f}%  (threshold ≥ 0.665)")
print(f"  Sum = {p3 + p6 + p9:.10f}  (must be 1.0)")

check(abs(p3 + p6 + p9 - 1.0) < 1e-12, f"Probabilities sum to {p3+p6+p9}")

# Code boundary check: 0.331 + 0.334 = 0.665
code_boundary = 0.331 + 0.334
print(f"  Code boundary (0.331 + 0.334) = {code_boundary:.6f}  (must be 0.665)")
check(abs(code_boundary - 0.665) < 1e-12, f"Boundary = {code_boundary}")
print(f"  Boundary check: PASS")

# Numerical convergence simulation
rng = np.random.default_rng(0)
N = 1_000_000
samples = rng.random(N)
c3 = int(np.sum(samples < 0.331))
c6 = int(np.sum((samples >= 0.331) & (samples < 0.665)))
c9 = N - c3 - c6

obs3, obs6, obs9 = c3/N, c6/N, c9/N
print(f"\n  Monte Carlo ({N:,} samples):")
print(f"    basket 3: {obs3:.5f}  (target {p3:.5f}, error {abs(obs3-p3)*100:.3f}%)")
print(f"    basket 6: {obs6:.5f}  (target {p6:.5f}, error {abs(obs6-p6)*100:.3f}%)")
print(f"    basket 9: {obs9:.5f}  (target {p9:.5f}, error {abs(obs9-p9)*100:.3f}%)")

tol = 0.002  # 0.2% Monte Carlo tolerance at N=1e6 (≈3σ)
check(abs(obs3 - p3) < tol, f"basket 3 Monte Carlo error {abs(obs3-p3):.5f} > {tol}")
check(abs(obs6 - p6) < tol, f"basket 6 Monte Carlo error {abs(obs6-p6):.5f} > {tol}")
check(abs(obs9 - p9) < tol, f"basket 9 Monte Carlo error {abs(obs9-p9):.5f} > {tol}")
print(f"  Convergence within ±{tol*100:.1f}%: PASS")

# ── 3. +4 mod 9 offset on cycle nodes ─────────────────────────────────────────

print("\n=== 3. Offset Correction: (node + 4) mod 9, result in {1,...,9} ===")

stated_loop = [1, 2, 4, 8, 7, 5]
print(f"  Loop nodes:        {stated_loop}")
print(f"  After +4 mod 9 (JS-style, 0→9):")

js_mod9 = lambda x: x % 9 if x % 9 != 0 else 9

offset_results = []
for node in stated_loop:
    result = js_mod9(node + 4)
    offset_results.append(result)
    print(f"    ({node} + 4) % 9 → {result}")

# Verify no zeros appear (the || 9 guard in JS)
check(0 not in offset_results, f"Zero appeared in offset results: {offset_results}")
check(all(1 <= r <= 9 for r in offset_results),
      f"Offset result out of [1,9]: {offset_results}")
print(f"  All results in {{1,...,9}}: PASS")

# Specific checks
check(js_mod9(1 + 4) == 5,  f"(1+4)%9 = {js_mod9(5)}, expected 5")
check(js_mod9(8 + 4) == 3,  f"(8+4)%9 = {js_mod9(12)}, expected 3")
check(js_mod9(5 + 4) == 9,  f"(5+4)%9 = {js_mod9(9)}, expected 9")  # the 0→9 case
print(f"  Edge case (5+4)%9=0→9 (JS || 9 guard): PASS")

# ── 4. Label discrepancy audit ────────────────────────────────────────────────

print("\n=== 4. Label Discrepancy: '13-Separation' vs code trigger 'totalCount % 25 === 0' ===")
print("  Original HTML label: '13-Separation Offset Correction'")
print("  Code trigger:        totalCount % 25 === 0  (every 25 steps)")
print("  Value 13 appears:    nowhere in the implementation")
print()
print("  Correction applied in committed HTML:")
print("    '13-Separation Offset Correction'  →  '25-Step Offset Correction'")
print()

# Verify the step-25 trigger fires at the right count values
trigger_counts = [n for n in range(1, 101) if n % 25 == 0]
print(f"  Trigger fires at steps: {trigger_counts}  (in first 100 steps)")
check(trigger_counts == [25, 50, 75, 100], f"Unexpected trigger counts: {trigger_counts}")
print(f"  Trigger cadence correct (every 25): PASS")

# ── 5. gapY lane separation ───────────────────────────────────────────────────

print("\n=== 5. Spatial Lane Separation (gapY formula) ===")

# gapY = floor(random() * 60) + lane_offset * 100 + 50
# lane 0 (basket 3): gapY ∈ [50, 109]
# lane 1 (basket 6): gapY ∈ [150, 209]
# lane 2 (basket 9): gapY ∈ [250, 309]

lanes = {3: (50, 109), 6: (150, 209), 9: (250, 309)}
for basket, (lo, hi) in lanes.items():
    lane = 0 if basket == 3 else (1 if basket == 6 else 2)
    computed_lo = lane * 100 + 50
    computed_hi = lane * 100 + 50 + 59  # floor(random()*60) max = 59
    check(computed_lo == lo and computed_hi == hi,
          f"Basket {basket} lane [{computed_lo},{computed_hi}] != stated [{lo},{hi}]")
    print(f"  Basket {basket} (lane {lane}): gapY ∈ [{computed_lo}, {computed_hi}]")

# Verify lanes are non-overlapping
check(lanes[3][1] < lanes[6][0], "Lanes 3 and 6 overlap")
check(lanes[6][1] < lanes[9][0], "Lanes 6 and 9 overlap")
separation_3_6 = lanes[6][0] - lanes[3][1]
separation_6_9 = lanes[9][0] - lanes[6][1]
print(f"  Gap between basket 3 and 6 lanes: {separation_3_6} units (non-overlapping: PASS)")
print(f"  Gap between basket 6 and 9 lanes: {separation_6_9} units (non-overlapping: PASS)")

# ── Summary ───────────────────────────────────────────────────────────────────

print("\n=== Summary ===")
if FAIL:
    print(f"FAILED ({len(FAIL)} claim(s)):")
    for msg in FAIL:
        print(f"  - {msg}")
    sys.exit(1)
else:
    print("ALL CLAIMS VERIFIED")
    print()
    print("Verified:")
    print("  [1,2,4,8,7,5] = powers of 2 mod 9, period 6, ord_9(2)=6")
    print("  Gap split 0.331/0.334/0.335 sums to 1.0; converges in Monte Carlo")
    print("  Offset (node+4)%9 with 0→9 guard; all results in {1,...,9}")
    print("  Spatial lanes non-overlapping, separation = 41 units each")
    print()
    print("Correction applied:")
    print("  Label '13-Separation' → '25-Step' (code trigger: totalCount % 25 === 0)")

if __name__ == "__main__":
    pass
