#!/usr/bin/env python3
"""
prime_delta23_audit.py

Audit of the signed delta distribution for primes ≤ 5000 under the shift +23.

Stated claims:
  Total primes ≤ 5000: 669
  delta(p) = DR(p+23) - DR(p) ∈ {+5, -4}  for all p
  +5 count: 333 (49.78%),  -4 count: 336 (50.22%)
  DR counts: 1→109, 2→114, 3→1, 4→109, 5→112, 7→112, 8→112
  First 20 primes: specific (p, DR, p+23, DR(p+23), delta)
  Delta sequence first 30: [5,5,-4,-4,5,5,-4,5,-4,5,5,5,-4,-4,5,-4,-4,-4,5,-4,5,-4,5,-4,-4,5,5,-4,5,-4]
  Max +5 run: 5,  Max -4 run: 6
  For primes > 3: DR ∈ {1,2,4,5,7,8} (no DR ∈ {3,6,9})

Underlying law:
  For any integer n: DR(n+23) - DR(n) = +5 if DR(n) ∈ {1,2,3,4},
                                         -4 if DR(n) ∈ {5,6,7,8,9}.
  Proof: 23 ≡ 5 (mod 9). Adding 5 (mod 9) either stays ≤ 9 (+5) or
  wraps through the 9→1 boundary (-4 = +5 - 9).
"""

import sys
from math import isqrt

FAIL = []

def check(cond, label, actual, stated):
    if not cond:
        FAIL.append(f"{label}: actual={actual}, stated={stated}")
    return cond

def dr(n):
    """Digital root, 1-9 convention (multiples of 9 → 9, not 0)."""
    if n == 0: return 9
    r = n % 9
    return r if r != 0 else 9

def sieve(limit):
    """Sieve of Eratosthenes."""
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, isqrt(limit) + 1):
        if is_p[i]:
            is_p[i*i::i] = bytearray(len(is_p[i*i::i]))
    return [i for i in range(2, limit + 1) if is_p[i]]

# ── Universal law verification ────────────────────────────────────────────────
print("=== Universal Law: DR(n+23) - DR(n) ∈ {+5, -4} ===")
print("  23 ≡ 5 (mod 9); adding 5 (mod 9) to any DR value:")
print()
print(f"  {'DR(n)':>8} {'DR(n+23)':>10} {'delta':>7} {'rule':>12}")
print(f"  {'-'*8} {'-'*10} {'-'*7} {'-'*12}")

for d in range(1, 10):
    dnew = dr(d + 23)          # equivalent to (d + 5) in the 1-9 ring
    delta = dnew - d
    rule = "+5" if d <= 4 else "-4"
    check(delta == (5 if d <= 4 else -4),
          f"law DR={d}", delta, 5 if d <= 4 else -4)
    print(f"  DR(n)={d:>2}  DR(n+23)={dnew:>2}  delta={delta:>+3}  [{rule}]")

print()
print("  Verified: DR(n) ∈ {1,2,3,4} → delta=+5; DR(n) ∈ {5,6,7,8,9} → delta=-4")

# ── Prime sieve and delta computation ────────────────────────────────────────
print("\n=== Prime δ-Distribution (primes ≤ 5000) ===")

primes = sieve(5000)
n_primes = len(primes)
check(n_primes == 669, "π(5000)", n_primes, 669)
print(f"  Total primes ≤ 5000: {n_primes}  (stated 669: {'PASS' if n_primes==669 else 'FAIL'})")

deltas  = [dr(p + 23) - dr(p) for p in primes]
count_p5 = sum(1 for d in deltas if d == +5)
count_m4 = sum(1 for d in deltas if d == -4)
check(count_p5 == 333, "+5 count",  count_p5, 333)
check(count_m4 == 336, "-4 count",  count_m4, 336)
check(count_p5 + count_m4 == n_primes, "total check", count_p5+count_m4, n_primes)

pct_p5 = count_p5 / n_primes * 100
pct_m4 = count_m4 / n_primes * 100
print(f"  +5 count: {count_p5} ({pct_p5:.2f}%)  (stated 333, 49.78%)")
print(f"  -4 count: {count_m4} ({pct_m4:.2f}%)  (stated 336, 50.22%)")

# All deltas must be +5 or -4
invalid = [p for p, d in zip(primes, deltas) if d not in (5, -4)]
check(len(invalid) == 0, "no invalid deltas", invalid, [])
print(f"  All deltas in {{+5,-4}}: {'PASS' if not invalid else 'FAIL'}")

# ── Per-DR count table ────────────────────────────────────────────────────────
print("\n=== DR(p) Distribution ===")
stated_counts = {1: 109, 2: 114, 3: 1, 4: 109, 5: 112, 7: 112, 8: 112}

dr_counts = {}
for p in primes:
    d = dr(p)
    dr_counts[d] = dr_counts.get(d, 0) + 1

print(f"  {'DR':>4} {'Stated':>7} {'Actual':>7} {'Delta sign':>11} {'OK':>4}")
print(f"  {'-'*4} {'-'*7} {'-'*7} {'-'*11} {'-'*4}")
for d in sorted(stated_counts):
    actual  = dr_counts.get(d, 0)
    stated  = stated_counts[d]
    sign    = "+5" if d <= 4 else "-4"
    ok      = actual == stated
    check(ok, f"DR={d} count", actual, stated)
    print(f"  {d:>4} {stated:>7} {actual:>7} {sign:>11} {'✓' if ok else '✗':>4}")

# Verify no DR ∈ {6, 9} among primes (divisible by 3)
for d in (6, 9):
    count_d = dr_counts.get(d, 0)
    if d == 6:
        check(count_d == 0, f"DR={d} absent", count_d, 0)
    else:
        check(count_d == 0, f"DR={d} absent", count_d, 0)
print(f"  DR ∈ {{6,9}} absent from primes: {'PASS'}")

# ── First 20 primes verification ──────────────────────────────────────────────
print("\n=== First 20 Primes (p, DR(p), p+23, DR(p+23), delta) ===")

stated_20 = [
    ( 2, 2, 25, 7, +5), ( 3, 3, 26, 8, +5), ( 5, 5, 28, 1, -4),
    ( 7, 7, 30, 3, -4), (11, 2, 34, 7, +5), (13, 4, 36, 9, +5),
    (17, 8, 40, 4, -4), (19, 1, 42, 6, +5), (23, 5, 46, 1, -4),
    (29, 2, 52, 7, +5), (31, 4, 54, 9, +5), (37, 1, 60, 6, +5),
    (41, 5, 64, 1, -4), (43, 7, 66, 3, -4), (47, 2, 70, 7, +5),
    (53, 8, 76, 4, -4), (59, 5, 82, 1, -4), (61, 7, 84, 3, -4),
    (67, 4, 90, 9, +5), (71, 8, 94, 4, -4),
]
print(f"  {'p':>5} {'DR(p)':>6} {'p+23':>6} {'DR(p+23)':>9} {'δ':>4} {'OK':>4}")
print(f"  {'-'*5} {'-'*6} {'-'*6} {'-'*9} {'-'*4} {'-'*4}")
for p_s, drp_s, p23_s, drp23_s, delta_s in stated_20:
    p23   = p_s + 23
    drp   = dr(p_s)
    drp23 = dr(p23)
    delta = drp23 - drp
    ok = (p23 == p23_s and drp == drp_s and drp23 == drp23_s and delta == delta_s)
    check(ok, f"p={p_s}", (drp, p23, drp23, delta), (drp_s, p23_s, drp23_s, delta_s))
    print(f"  {p_s:>5} {drp:>6} {p23:>6} {drp23:>9} {delta:>+4} {'✓' if ok else '✗':>4}")

# ── Delta sequence first 30 ───────────────────────────────────────────────────
print("\n=== Delta Sequence (first 30) ===")
stated_seq30 = [5,5,-4,-4,5,5,-4,5,-4,5,5,5,-4,-4,5,-4,-4,-4,5,-4,5,-4,5,-4,-4,5,5,-4,5,-4]
actual_seq30 = deltas[:30]
check(actual_seq30 == stated_seq30, "delta seq[0:30]", actual_seq30, stated_seq30)
print(f"  Stated: {stated_seq30}")
print(f"  Actual: {actual_seq30}")
print(f"  Match: {'PASS' if actual_seq30 == stated_seq30 else 'FAIL'}")

# ── Run lengths ───────────────────────────────────────────────────────────────
print("\n=== Run Lengths ===")

def run_lengths(seq):
    if not seq: return []
    runs = []
    cur_val, cur_len = seq[0], 1
    for v in seq[1:]:
        if v == cur_val:
            cur_len += 1
        else:
            runs.append((cur_val, cur_len))
            cur_val, cur_len = v, 1
    runs.append((cur_val, cur_len))
    return runs

runs = run_lengths(deltas)
runs_p5 = [r for v, r in runs if v == +5]
runs_m4 = [r for v, r in runs if v == -4]
max_p5 = max(runs_p5)
max_m4 = max(runs_m4)

check(max_p5 == 5, "max +5 run", max_p5, 5)
check(max_m4 == 6, "max -4 run", max_m4, 6)
print(f"  Max +5 run: {max_p5}  (stated 5: {'PASS' if max_p5==5 else 'FAIL'})")
print(f"  Max -4 run: {max_m4}  (stated 6: {'PASS' if max_m4==6 else 'FAIL'})")

# Show first 20 runs
print(f"\n  First 20 run lengths (stated):")
runs_20 = runs[:20]
for v, r in runs_20:
    sign = "+5" if v == 5 else "-4"
    print(f"    {sign} run: {r} primes")

# ── Theoretical context ───────────────────────────────────────────────────────
print("\n=== Theoretical Basis ===")
print("  The +5/-4 dichotomy follows from 23 ≡ 5 (mod 9).")
print("  For any n: DR(n) + 5 stays in {6,...,9} if DR(n) ≤ 4 → delta = +5")
print("             DR(n) + 5 wraps mod 9 (→ {1,...,5}) if DR(n) ≥ 5 → delta = -4")
print()
print("  For primes > 3: DR(p) ∈ {1,2,4,5,7,8}  [no multiples of 3]")
print("  Threshold DR=4/5 divides this set into equal halves: {1,2,4} and {5,7,8}")
print()
print("  Dirichlet equidistribution: primes are asymptotically equidistributed")
print("  across the φ(9)=6 residue classes {1,2,4,5,7,8} mod 9.")
print("  Equal split 3+3 → asymptotic +5 : -4 ratio → 1 : 1 (50% / 50%).")
print(f"  Empirical at N=5000: {count_p5}/{n_primes} = {pct_p5:.3f}% vs {count_m4}/{n_primes} = {pct_m4:.3f}%")

# Verify the equal split of {1,2,4,5,7,8} into {1,2,4} and {5,7,8}
plus_set  = {d for d in range(1,9) if 9 % d != 0 and d <= 4 and d in (1,2,4,5,7,8)}
minus_set = {d for d in range(1,9) if 9 % d != 0 and d >= 5 and d in (1,2,4,5,7,8)}
# The valid DR values for primes > 3,5 are {1,2,4,5,7,8}:
valid_drs = {1,2,4,5,7,8}
plus_drs  = {d for d in valid_drs if d <= 4}   # {1,2,4}
minus_drs = {d for d in valid_drs if d >= 5}   # {5,7,8}
assert plus_drs == {1,2,4} and minus_drs == {5,7,8}
assert len(plus_drs) == len(minus_drs) == 3
print(f"  +5 DR set: {sorted(plus_drs)} ({len(plus_drs)} classes)")
print(f"  -4 DR set: {sorted(minus_drs)} ({len(minus_drs)} classes)")
print(f"  Equal partition confirmed → Dirichlet → asymptotic 50/50.")

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n=== Summary ===")
if FAIL:
    print(f"FAILED ({len(FAIL)}):")
    for f in FAIL:
        print(f"  ✗  {f}")
    sys.exit(1)
else:
    print("ALL CLAIMS VERIFIED")

if __name__ == "__main__":
    pass
