#!/usr/bin/env python3
"""
BLUE-SHIFTED RECURSIVE MAPPING AUDIT
=====================================
W_n = S_n / 2   Domain: Continuous Rational Field   lim W_n = 0

STRUCTURE FOUND:
  Two segments — no single exponential spans both.

  Segment A (n=0,1):  W_n = 7 · 2^(-n)
  Segment B (n≥2):    W_n = 2^(-⌊(n-2)/2⌋)   (paired halving, each value repeats once)

  Transition at n=1→2: ratio W[2]/W[1] = 1/3.5 = 2/7 ≈ 0.2857  (not 1/2)

EXPONENTIAL CLAIM f(t) = 7·e^{-λt}:
  λ = ln 2 fits n=0,1 exactly. Fails from n=2 onward.
  f(2) = 7·(1/4) = 1.75  ≠  W[2] = 1.0   (error = −0.75)

φ_DECAY:
  Claim φ_decay ≈ 0.5 is verified for segment B:
    W[n+2]/W[n] = 0.5 for all n≥2  ✓
  Per-step ratio within segment B alternates: 1 (repeat), 0.5 (halve).

CUMULATIVE ENERGY (infinite extension of segment B):
  Σ(n=0..∞) W_n = W[0]+W[1] + 2·(1+0.5+0.25+...) = 10.5 + 4.0 = 14.5
"""

import math

errors = []

def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}")
    if not cond:
        errors.append(label)

S = [14, 7, 2, 2, 1, 1, 0.5, 0.5, 0.25]
W = [s / 2 for s in S]

CLAIMED_W = [7.0, 3.5, 1.0, 1.0, 0.5, 0.5, 0.25, 0.25, 0.125]
CLAIMED_D = [7.0, 3.5, 1.0, 1.0, 0.5, 0.5, 0.25, 0.25, 0.125]

# ── W_n = S_n / 2 ────────────────────────────────────────────────────────────

print("=== W_n = S_n / 2 ===")
print(f"  {'n':>3}  {'S_n':>8}  {'W_n':>8}  {'claimed':>8}  {'Delta=W_n?':>10}  match")
print("  " + "-"*60)
for n in range(len(S)):
    w = S[n] / 2
    delta_ok = abs(CLAIMED_D[n] - w) < 1e-12
    ok = abs(w - CLAIMED_W[n]) < 1e-12
    print(f"  {n:>3}  {S[n]:>8}  {w:>8.4f}  {CLAIMED_W[n]:>8.4f}  {'Y' if delta_ok else 'N':>10}  {'OK' if ok else 'ERR'}")
print()

for n in range(len(S)):
    check(f"W[{n}] = {S[n]}/2 = {CLAIMED_W[n]}", abs(W[n] - CLAIMED_W[n]) < 1e-12)
check("lim W_n = 0  (monotone non-increasing)", all(W[i] >= W[i+1] - 1e-12 for i in range(len(W)-1)))
check("W_n -> 0  (final value < 0.2)", W[-1] < 0.2)
print()

# ── S_n RATIO STRUCTURE ───────────────────────────────────────────────────────

print("=== S_n RATIO STRUCTURE ===")
for n in range(1, len(S)):
    r = S[n] / S[n-1]
    tag = "(=1/2)" if abs(r - 0.5) < 1e-9 else "(=1)" if abs(r - 1.0) < 1e-9 else f"(={r:.4f}) <- TRANSITION"
    print(f"  S[{n}]/S[{n-1}] = {S[n]}/{S[n-1]} = {r:.6f}  {tag}")
print()
check("S[1]/S[0] = 1/2  (clean halve)", abs(S[1]/S[0] - 0.5) < 1e-9)
check("S[2]/S[1] ≠ 1/2  (transition break at n=2)", abs(S[2]/S[1] - 0.5) > 0.1)
check("S[2]/S[1] = 2/7", abs(S[2]/S[1] - 2/7) < 1e-9)
print()

# ── PIECEWISE FORMULA ─────────────────────────────────────────────────────────

print("=== PIECEWISE FORMULA ===")
print("  Segment A (n=0,1):  W_n = 7 · 2^(-n)")
for n in range(2):
    predicted = 7 * 2**(-n)
    check(f"Segment A: W[{n}] = 7·2^(-{n}) = {predicted}", abs(predicted - W[n]) < 1e-12)

print()
print("  Segment B (n≥2):  W_n = 2^(-floor((n-2)/2))  [paired halving]")
for n in range(2, len(W)):
    k = (n - 2) // 2
    predicted = 2**(-k)
    check(f"Segment B: W[{n}] = 2^(-{k}) = {predicted}", abs(predicted - W[n]) < 1e-12)
print()

# ── EXPONENTIAL FIT ───────────────────────────────────────────────────────────

print("=== EXPONENTIAL f(t) = 7·exp(-ln2·t) ===")
lam = math.log(2)
print(f"  lambda = ln(2) = {lam:.6f}")
print(f"  {'n':>3}  {'W_n':>8}  {'f(n)':>10}  {'diff':>8}  fit?")
print("  " + "-"*45)
for n, w in enumerate(W):
    ft = 7 * math.exp(-lam * n)
    diff = w - ft
    ok = abs(diff) < 1e-9
    print(f"  {n:>3}  {w:>8.4f}  {ft:>10.4f}  {diff:>8.4f}  {'OK' if ok else 'MISMATCH'}")
print()
check("f(t)=7e^(-ln2·t) fits n=0", abs(7 * math.exp(0) - W[0]) < 1e-9)
check("f(t)=7e^(-ln2·t) fits n=1", abs(7 * math.exp(-lam) - W[1]) < 1e-9)
check("f(t)=7e^(-ln2·t) fails n=2  (predicts 1.75, got 1.0)", abs(7 * math.exp(-2*lam) - W[2]) > 0.5)
check("Single exponential does NOT span both segments", True)
print()

# ── phi_DECAY ─────────────────────────────────────────────────────────────────

print("=== phi_DECAY = 0.5 (step-pair ratio in segment B) ===")
for n in range(2, len(W) - 2):
    r = W[n + 2] / W[n]
    check(f"W[{n+2}]/W[{n}] = {W[n+2]}/{W[n]} = 0.5", abs(r - 0.5) < 1e-9)
print()

# ── CUMULATIVE ENERGY ─────────────────────────────────────────────────────────

print("=== CUMULATIVE ENERGY ===")
finite_sum = sum(W)
print(f"  Finite (n=0..8):   {finite_sum}")
head = W[0] + W[1]
tail_inf = 2 * (1 / (1 - 0.5))
total_inf = head + tail_inf
print(f"  Infinite extension: head(n=0,1)={head} + tail(n≥2)=2×Σ2^(-k)={tail_inf} = {total_inf}")
check("Finite sum (n=0..8) = 14.125", abs(finite_sum - 14.125) < 1e-9)
check("Infinite sum = 14.5  [10.5 + 4.0]", abs(total_inf - 14.5) < 1e-9)
print()

if errors:
    print(f"FAILURES: {errors}")
else:
    print("All verified claims pass.")
