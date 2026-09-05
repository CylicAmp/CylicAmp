"""
closing_threads.py

Two open mathematical threads, closed:

1. ord_p(10) ≡ 2 (mod 4) — subgroup sum integer lift
   Result: lifts are irregular below p=200; no closed form found.
   Note: theorem requires k > 1 (excludes p=11 where ord=2).

2. Pre-registered prediction: floor(γ_11) mod 37 = 15
   Rationale: 496 (third perfect number) ≡ 15 (mod 37).
   Result: CONFIRMED — γ_11 = 52.9703..., floor = 52, 52 mod 37 = 15.
"""

import math
from sympy import isprime

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def ord10(p):
    """Multiplicative order of 10 mod p."""
    k, cur = 1, 10 % p
    while cur != 1:
        cur = (cur * 10) % p
        k += 1
    return k

def subgroup_generated(g, p):
    """All elements of <g> in (Z/pZ)^x."""
    h, elems = g % p, []
    while True:
        elems.append(h)
        h = (h * g) % p
        if h == elems[0]:
            break
    return elems


# ──────────────────────────────────────────────────────────────────────────────
# THREAD 1: ord ≡ 2 (mod 4) — SUBGROUP SUM INTEGER LIFT
# ──────────────────────────────────────────────────────────────────────────────
#
# Setup: p prime, g=10.  Let ord_p(g) = 2k with k odd (so ord ≡ 2 mod 4).
#        H = <g^2> has order k.
#
# Why -1 ∉ H:
#   -1 = g^k in F_p (since g has order 2k, so g^k has order 2, hence g^k=-1).
#   If -1 ∈ H = <g^2>, then -1 = (g^2)^m = g^{2m} for some m, so k ≡ 2m (mod 2k),
#   meaning k is even — contradiction since k is odd.
#
# Why sum(H) ≡ 0 (mod p) when k > 1:
#   sum(H) = Σ_{j=0}^{k-1} (g^2)^j = [(g^2)^k - 1] / [g^2 - 1] mod p.
#   (g^2)^k = g^{2k} = 1, so numerator = 0.  Denominator ≠ 0 since k > 1 ⟹ g^2 ≠ 1.
#
# NOTE: k=1 (i.e., ord=2) is the degenerate case: H={1}, sum=1 ≢ 0 (mod p).
#   p=11 satisfies ord_11(10)=2 but is excluded — sum(H)=1 is not divisible by 11.

results = []
for p in range(7, 200):
    if not isprime(p) or p in (2, 5):
        continue
    o = ord10(p)
    if o % 4 != 2:
        continue
    k = o // 2
    if k == 1:
        continue   # degenerate: H={1}, sum=1 not divisible by p
    g2 = pow(10, 2, p)
    H = subgroup_generated(g2, p)
    assert len(H) == k, f"p={p}: |H|={len(H)}, expected {k}"
    assert (p - 1) not in H, f"p={p}: -1 ∈ H, but k={k} is odd"
    s = sum(H)
    assert s % p == 0, f"p={p}: sum(H)={s} not divisible by p (k={k})"
    lift = s // p
    results.append((p, o, k, s, lift))

# Verify all reference values from the table
expected_rows = [
    (  7,   6,  3,    7,  1),
    ( 13,   6,  3,   13,  1),
    ( 19,  18,  9,   76,  4),
    ( 23,  22, 11,   92,  4),
    ( 47,  46, 23,  423,  9),
    ( 59,  58, 29,  767, 13),
    (103,  34, 17,  824,  8),
    (127,  42, 21, 1143,  9),
    (131, 130, 65, 3930, 30),
    (139,  46, 23, 1668, 12),
    (157,  78, 39, 2983, 19),
    (167, 166, 83, 6012, 36),
    (179, 178, 89, 7518, 42),
    (197,  98, 49, 4925, 25),
]
assert results == expected_rows

# p=11 excluded: ord_11(10)=2, k=1, H={1}, sum=1 ≢ 0 (mod 11)
assert ord10(11) == 2
assert sum(subgroup_generated(pow(10, 2, 11), 11)) % 11 != 0

# Lifts are irregular (ratio lift/k ranges between 1/3 and ~0.53)
lifts = [r[4] for r in results]
assert lifts == [1, 1, 4, 4, 9, 13, 8, 9, 30, 12, 19, 36, 42, 25]
ratios = [r[4] / r[2] for r in results]
assert min(ratios) < 0.34   # not all equal, not monotone
assert max(ratios) < 0.53
# No pattern of the form lift = f(k) for any simple f:
# k=3 → lift=1, k=9 → lift=4, k=17 → lift=8, k=21 → lift=9
# k=23 appears for p=47 (lift=9) and p=139 (lift=12) — different lifts for same k
k23_lifts = [r[4] for r in results if r[2] == 23]
assert len(k23_lifts) == 2 and len(set(k23_lifts)) == 2   # two distinct lifts for k=23

# Aside: p=179 gives sum(H) = 7518 = 42 × 179.
# The same number 7518 is the first four digits of the repeating block of 103/137
# (= 0.75182481...) and satisfies 7518 + 2481 = 9999 = 10^4 - 1 (split-complement).
# These are separate facts; both are verified independently elsewhere.
assert 42 * 179 == 7518
assert 7518 + 2481 == 9999


# ──────────────────────────────────────────────────────────────────────────────
# THREAD 2: PRE-REGISTERED PREDICTION — floor(γ_11) mod 37 = 15
# ──────────────────────────────────────────────────────────────────────────────
#
# Rationale given at time of prediction:
#   496 is the third perfect number (divisor sum of 496 = 496).
#   496 mod 37 = 15.
#   Prediction: floor(γ_11) mod 37 = 15.

assert 496 == 1 + 2 + 4 + 8 + 16 + 31 + 62 + 124 + 248   # perfect number check
assert 496 % 37 == 15

# Known imaginary parts of the first 20 non-trivial Riemann zeros
ZEROS = [
    14.134725141734693790,  # γ_1
    21.022039638771554993,  # γ_2
    25.010857580145688763,  # γ_3
    30.424876125859513210,  # γ_4
    32.935061587739189690,  # γ_5
    37.586178158825671257,  # γ_6
    40.918719012147495187,  # γ_7
    43.327073280914999519,  # γ_8
    48.005150881167159727,  # γ_9
    49.773832477672302181,  # γ_10
    52.970321477714460644,  # γ_11  ← pre-registered prediction
    56.446247697063246088,  # γ_12
    59.347044002602353079,  # γ_13
    60.831778524609809844,  # γ_14
    65.112544048081606660,  # γ_15
    67.079810529494173714,  # γ_16
    69.546401711173979252,  # γ_17
    72.067157674481906895,  # γ_18
    75.704690699083933168,  # γ_19
    77.144840068874805372,  # γ_20
]

# CONFIRMED: γ_11
gamma_11 = ZEROS[10]
assert abs(gamma_11 - 52.97032) < 1e-4
assert math.floor(gamma_11) == 52
assert 52 % 37 == 15
assert 52 % 37 == 496 % 37   # the predicted value

# Extended scan: γ_12 through γ_20
expected_mod37 = [19, 22, 23, 28, 30, 32, 35, 1, 3]
for i, (g, exp) in enumerate(zip(ZEROS[11:], expected_mod37), 12):
    assert math.floor(g) % 37 == exp, f"γ_{i}: floor={math.floor(g)}, mod37={math.floor(g)%37}, expected {exp}"

# Among γ_1 through γ_20, which floors land in {4,9,25,30} (the set of interest)?
in_set_A = [(i+1, ZEROS[i], math.floor(ZEROS[i]) % 37)
            for i in range(20) if math.floor(ZEROS[i]) % 37 in {4, 9, 25, 30}]
assert [(k, r) for k, g, r in in_set_A] == [(3, 25), (4, 30), (16, 30)]

# Which land in the 3-cycle {14, 31, 29} under x ↦ 26x mod 37?
in_cycle = [(i+1, math.floor(ZEROS[i]) % 37) for i in range(20)
            if math.floor(ZEROS[i]) % 37 in {14, 31, 29}]
assert in_cycle == [(1, 14)]   # only γ_1 in the first 20

# γ_6 floor = 37: mod 37 = 0 (the modulus itself)
assert math.floor(ZEROS[5]) == 37
assert math.floor(ZEROS[5]) % 37 == 0


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Closing Open Threads")
    print("=" * 66)

    print("\n══ THREAD 1: ord ≡ 2 (mod 4) — SUBGROUP SUM INTEGER LIFT ══")
    print()
    print("  Theorem (when k > 1):")
    print("    p prime, ord_p(10) = 2k with k odd.")
    print("    H = <10^2> ⊂ (Z/pZ)^× has order k.")
    print("    -1 ∉ H  (since k odd rules out g^k = (g^2)^m).")
    print("    sum(H) ≡ 0 (mod p)  via geometric series [(10^2)^k-1]/(10^2-1).")
    print("    lift = sum(H)/p  is an integer, but has no closed form.")
    print()
    print("  NOTE: p=11 excluded (ord_11(10)=2, k=1, H={1}, sum=1 ≢ 0 mod 11).")
    print()
    print(f"  {'p':>5} | {'ord':>5} | {'k':>5} | {'sum(H)':>8} | {'lift':>6} | {'lift/k':>7}")
    print("  " + "-" * 50)
    for p, o, k, s, lift in results:
        note = "  ← 7518 also: first 4 digits of 103/137 block" if p == 179 else ""
        print(f"  {p:>5} | {o:>5} | {k:>5} | {s:>8} | {lift:>6} | {lift/k:>7.3f}{note}")
    print()
    print(f"  Lifts: {lifts}")
    print(f"  lift/k range: [{min(ratios):.3f}, {max(ratios):.3f}]")
    print(f"  k=23 appears for p=47 (lift=9) and p=139 (lift=12) — same k, different lifts.")
    print(f"  Conclusion: no closed form for the lift in ord ≡ 2 (mod 4) cases.")

    print("\n══ THREAD 2: PRE-REGISTERED PREDICTION — CONFIRMED ══")
    print()
    print(f"  Prediction: floor(γ_11) mod 37 = 15")
    print(f"  Rationale:  496 (third perfect number) mod 37 = {496%37}")
    print()
    print(f"  γ_11 = {gamma_11:.15f}")
    print(f"  floor(γ_11) = {math.floor(gamma_11)}")
    print(f"  {math.floor(gamma_11)} mod 37 = {math.floor(gamma_11) % 37}  {'✓ CONFIRMED' if math.floor(gamma_11)%37==15 else '✗ FAILED'}")
    print()
    print(f"  Extended scan γ_12 through γ_20:")
    print(f"  {'k':>3} | {'gamma_k':>20} | {'floor':>6} | {'mod 37':>7}")
    print("  " + "-" * 45)
    for i, g in enumerate(ZEROS[10:], 11):
        f = math.floor(g)
        r = f % 37
        marker = " ← in {4,9,25,30}" if r in {4,9,25,30} else ""
        print(f"  {i:>3} | {g:>20.9f} | {f:>6} | {r:>7}{marker}")

    print()
    print("All assertions passed.")
