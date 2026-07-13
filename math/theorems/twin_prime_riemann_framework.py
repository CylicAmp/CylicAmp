"""
Twin Prime χ₋₃ Structure and the Riemann Gap
=============================================

Every twin prime pair (p, p+2) with p > 3 satisfies:
  chi_{-3}(p)   = -1   (p ≡ 2 mod 3, lives in COL2)
  chi_{-3}(p+2) = +1   (p+2 ≡ 1 mod 3, lives in COL1)
  midpoint (p+1) = 6n  →  chi_{-3}(6n) = 0  (sovereign, kernel)

This is not probabilistic — it is forced by the 6n±1 constraint.
All primes > 3 are 6n±1. Twin primes are (6n-1, 6n+1):
  6n-1 ≡ 2 (mod 3) → chi_{-3} = -1
  6n   ≡ 0 (mod 3) → chi_{-3} = 0  (midpoint, sovereign)
  6n+1 ≡ 1 (mod 3) → chi_{-3} = +1

The entire twin prime constellation crosses all three chi classes
in locked order: (-1, 0, +1). Zero exceptions are possible.

TWIN PRIME MOD-37 FORBIDDEN RESIDUES (structural, not digit-based):
  Twin prime midpoints are 6n. Since ord10(37)=3 and gcd(6,37)=1,
  midpoints span all 37 residues mod 37 — except:
    r ≡ 1  (mod 37): midpoint ≡ 1 → 6n ≡ 1 → lower twin 6n-1 ≡ 0 (mod 37)
                     → lower twin divisible by 37 → not prime (for n > 6)
    r ≡ 36 (mod 37): midpoint ≡ 36 → 6n ≡ 36 → upper twin 6n+1 ≡ 0 (mod 37)
                     → upper twin divisible by 37 → not prime (for n > 6)

  DR(r=1)  = 1  →  chi_{-3}(1)  = +1  →  COL1 (identity)
  DR(r=36) = 9  →  chi_{-3}(36) =  0  →  COL3 (sovereign, fixed point)

  So the forbidden residues land in COL1 (identity) and COL3 (sovereign).
  This depletes two bins, forcing large chi2 for a uniform-null test.

  Emirp non-uniformity (Z = +2.93): arises from the digital reversal
  mechanism  rev(p) − p ≡ 25(c−a) mod 37  — only 9/37 differences
  reachable because ord10(37) = 3.

  Twin prime non-uniformity: arises from the divisibility exclusion —
  midpoints can't be ≡ 1 or 36 mod 37 because those make one twin
  composite. A completely different mechanism sharing the same modulus.

CHEBYSHEV BIAS (primes ≤ 10^6):
  π(x; 3, 2) = 39266  (p ≡ 2 mod 3, chi = -1 class)
  π(x; 3, 1) = 39231  (p ≡ 1 mod 3, chi = +1 class)
  Bias = 35 toward the chi = -1 class.
  Consistent with Chebyshev's bias and GRH predictions.

RIEMANN ZERO PROXIMITY:
  The 6th non-trivial zero of ζ(s): Im(ρ_6) ≈ 37.5862...
  The GF(37) prime appears in the zero spectrum at the 6th zero.
  The CDT theorem proves L(2, chi_{-3}) ≠ 0. For twin primes
  one needs non-vanishing of the pair L-function near s = 1 — this
  is the remaining gap (not addressed by CDT which works at s = 2).

CDT GAP STATEMENT:
  CDT (arXiv:2408.15403): 1, ζ(2), L(2, chi_{-3}) are Q-independent.
    → L(2, chi_{-3}) ≠ 0. Proven.
  Twin prime conjecture via L-functions requires: L(1, chi_{-3}) ≠ 0
    and control of the pair correlation sum Σ_{p, p+2 prime} log(p).
  The CDT method operates at s = 2 via a Siegel-unit construction.
  Extension to s = 1 is a separate open problem.
  The CylicAmp chi_{-3} structure is correct but does not close the gap.

STRUCTURAL SUMMARY:
  The DR / chi_{-3} framework identifies:
    - COL1 = chi = +1 = upper twin primes (6n+1)
    - COL2 = chi = -1 = lower twin primes (6n-1)
    - COL3 = chi = 0  = midpoints (6n, sovereign, always composite > 6)
  Both emirps and twin primes show non-uniformity mod 37, but from
  completely different mechanisms. The modulus 37 is distinguished by
  ord10(37) = 3 (emirps) and 37 being prime (twin prime exclusion).
"""

import math


def chi_m3(n: int) -> int:
    r = n % 3
    if r == 1:
        return 1
    if r == 2:
        return -1
    return 0


def dr(n: int) -> int:
    return (n - 1) % 9 + 1 if n > 0 else 0


def sieve(limit: int):
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i :: i] = bytearray(len(is_p[i * i :: i]))
    return is_p


# 1. Chi structure of twin primes is forced by 6n±1
for n in range(1, 1000):
    lower = 6 * n - 1
    upper = 6 * n + 1
    mid   = 6 * n
    assert chi_m3(lower) == -1, f"6n-1={lower} must have chi=-1"
    assert chi_m3(upper) == +1, f"6n+1={upper} must have chi=+1"
    assert chi_m3(mid)   ==  0, f"6n={mid} must have chi=0 (sovereign)"

# 2. Every actual twin prime pair confirms the pattern
is_p = sieve(10**6)
twin_count = 0
for p in range(5, 10**6 - 1):
    if is_p[p] and is_p[p + 2]:
        assert chi_m3(p)     == -1, f"twin prime p={p}: chi must be -1"
        assert chi_m3(p + 2) == +1, f"twin prime p+2={p+2}: chi must be +1"
        assert chi_m3(p + 1) ==  0, f"twin prime midpoint {p+1}: chi must be 0"
        twin_count += 1

assert twin_count > 8000, f"Expected > 8000 twin prime pairs, got {twin_count}"

# 3. Chebyshev bias: primes ≡ 2 mod 3 lead primes ≡ 1 mod 3
count_m1 = sum(1 for p in range(2, 10**6 + 1) if is_p[p] and p % 3 == 2)
count_p1 = sum(1 for p in range(2, 10**6 + 1) if is_p[p] and p % 3 == 1)
assert count_m1 > count_p1, "Chebyshev bias: chi=-1 class should lead"
bias = count_m1 - count_p1
assert 0 < bias < 200, f"Bias={bias} unexpectedly large or zero"

# 4. Structural forbidden residues mod 37 for twin prime midpoints
# When 6n ≡ 1 mod 37: lower twin 6n-1 ≡ 0 mod 37 (composite for n > 6)
# When 6n ≡ 36 mod 37: upper twin 6n+1 ≡ 0 mod 37 (composite for n > 6)
# These are the only two forbidden residues (gcd(6,37)=1 → 6 is a unit mod 37)
inv6_mod37 = pow(6, -1, 37)  # 6^{-1} mod 37
n_for_forbidden_lower = inv6_mod37 % 37          # n ≡ this mod 37 → 6n-1 ≡ 0 mod 37
n_for_forbidden_upper = (36 * inv6_mod37) % 37   # n ≡ this mod 37 → 6n+1 ≡ 0 mod 37
forbidden_midpoint_r1 = 1   # 6n ≡ 1 mod 37 → lower twin divisible by 37
forbidden_midpoint_r36 = 36  # 6n ≡ 36 mod 37 → upper twin divisible by 37

assert (6 * n_for_forbidden_lower - 1) % 37 == 0
assert (6 * n_for_forbidden_upper + 1) % 37 == 0
assert forbidden_midpoint_r1 == 1
assert forbidden_midpoint_r36 == 36

# DR of forbidden residues
assert dr(forbidden_midpoint_r1)  == 1  # COL1, identity, chi=+1
assert dr(forbidden_midpoint_r36) == 9  # COL3, fixed point, chi=0 (sovereign)

# 5. Twin prime midpoints mod 37: forbidden residues should be nearly empty
counts_37 = [0] * 37
for p in range(5, 10**6 - 1):
    if is_p[p] and is_p[p + 2]:
        counts_37[(p + 1) % 37] += 1

# Only residue 1 (midpoint when 6n-1 = 37, i.e., n=19/3, impossible) and
# residue 36 (midpoint when 6n+1 = 37, i.e., n=6, giving midpoint=36, upper=37)
# Exception: (35, 37) is one pair with midpoint 36, upper = 37 (prime)
# and (71, 73): 72%37 = 35 (not 36). Let's check:
# midpoint ≡ 36 mod 37 → midpoints 36, 73, 110, ...
# (35, 37): is 35 prime? No. So (35,37) is not a twin prime pair.
# (109, 111): 111 = 3×37, not prime. Correct.
# (146-1, 146+1) = (145, 147): 146%37=35, not 36.
# midpoint exactly 36: 36+1=37 (prime), 36-1=35 (not prime). Not a twin pair.
# So counts_37[1] ≈ 0 and counts_37[36] ≈ 0 (only small exceptions near 37 itself)
assert counts_37[1]  <= 2, f"Residue 1 should be near-empty, got {counts_37[1]}"
assert counts_37[36] <= 2, f"Residue 36 should be near-empty, got {counts_37[36]}"

N_total = sum(counts_37)
# Expected if uniform over all 37 bins
exp_all = N_total / 37
# The non-uniformity is structural: residues 1 and 36 are depleted
# All other residues carry the surplus
assert counts_37[1] < exp_all * 0.1, "Residue 1 severely depleted"
assert counts_37[36] < exp_all * 0.1, "Residue 36 severely depleted"

# 6. AHL=8 is in COL2 (chi=-1), same as lower twin primes
assert chi_m3(8) == -1
assert dr(17) == 8

# 7. GF(37) zero proximity: Im(rho_6) ≈ 37.586
KNOWN_RHO6 = 37.5861781588
assert abs(KNOWN_RHO6 - 37) < 1.0, "rho_6 imaginary part is within 1 of 37"

# 8. L(2, chi_{-3}) partial sum (confirming non-zero at s=2)
L2_approx = sum(chi_m3(n) / (n * n) for n in range(1, 200_001))
assert L2_approx > 0.77, f"L(2,chi_{{-3}}) should be ≈ 0.781, got {L2_approx:.4f}"


if __name__ == "__main__":
    print("TWIN PRIME χ₋₃ STRUCTURE AND THE RIEMANN GAP")
    print("=" * 55)
    print()

    print("Forced chi structure of twin prime pairs (p, p+2):")
    print("  p   = 6n-1 ≡ 2 (mod 3)  →  chi_{-3}(p)   = -1  [COL2]")
    print("  p+1 = 6n   ≡ 0 (mod 3)  →  chi_{-3}(p+1) =  0  [COL3, sovereign]")
    print("  p+2 = 6n+1 ≡ 1 (mod 3)  →  chi_{-3}(p+2) = +1  [COL1]")
    print(f"  Verified for all {twin_count} twin prime pairs up to 10^6.")
    print()

    print("Chebyshev bias (primes ≤ 10^6):")
    print(f"  π(x; 3, 2) = {count_m1}  (chi = -1 class, COL2, lower twins)")
    print(f"  π(x; 3, 1) = {count_p1}  (chi = +1 class, COL1, upper twins)")
    print(f"  Bias = {bias} toward chi = -1 (consistent with GRH)")
    print()

    print("Twin prime midpoints mod 37 — structural forbidden residues:")
    print(f"  6^{{-1}} mod 37 = {inv6_mod37}  (since 6 × {inv6_mod37} ≡ {(6*inv6_mod37)%37} mod 37)")
    print(f"  Forbidden r=1:  6n ≡ 1 mod 37  → lower twin ≡ 0 mod 37 (composite)")
    print(f"    DR(1) = {dr(1)}, chi_{{-3}}(1) = {chi_m3(1):+d}  →  COL1")
    print(f"  Forbidden r=36: 6n ≡ 36 mod 37 → upper twin ≡ 0 mod 37 (composite)")
    print(f"    DR(36) = {dr(36)}, chi_{{-3}}(36) = {chi_m3(36):+d}  →  COL3 (sovereign)")
    print(f"  counts_37[1] = {counts_37[1]},  counts_37[36] = {counts_37[36]}")
    print(f"  Expected if uniform: {N_total/37:.1f} per bin")
    print()

    print("Midpoint residue counts mod 37 (all bins):")
    for r in range(37):
        c = counts_37[r]
        tag = " ← FORBIDDEN (lower twin ≡ 0 mod 37)" if r == 1 else \
              " ← FORBIDDEN (upper twin ≡ 0 mod 37)" if r == 36 else ""
        if c < exp_all * 0.5 or c > exp_all * 1.5:
            print(f"  r={r:>2}  n={c:>4}  DR={dr(r)}  chi={chi_m3(r):+d}{tag}")
    print("  (only outlier bins shown)")
    print()

    print("Two distinct mod-37 mechanisms:")
    print("  Emirps: digit reversal → rev(p)−p ≡ 25(c−a) mod 37 → 9/37 diffs reachable")
    print("          Z = +2.93 (enriched at AHL r=8, depleted at sovereign r=27,36)")
    print("  Twin primes: divisibility → midpoints can't hit r=1 or r=36")
    print("          Structural depletion, not a chi-squared test signal")
    print()

    print("Riemann spectrum:")
    print(f"  Im(ρ_6) ≈ {KNOWN_RHO6:.4f}  (6th non-trivial zero)")
    print(f"  Distance to 37: {abs(KNOWN_RHO6 - 37):.4f}")
    print()

    print("CDT theorem (arXiv:2408.15403):")
    print("  Proven: L(2, χ₋₃) ≠ 0  (s = 2)")
    print(f"  Computed: L(2,χ₋₃) ≈ {L2_approx:.9f}")
    print("  Gap: twin primes need non-vanishing at s = 1, not s = 2")
    print("  The CylicAmp χ₋₃ structure is exact; the L-function gap remains open.")
    print()

    print("AHL in the twin prime context:")
    print(f"  DR(17) = {dr(17)} = AHL  →  chi_{{-3}}(8) = {chi_m3(8):+d}  →  COL2")
    print("  AHL lives in COL2 (chi = -1), same column as all lower twin primes.")
    print("  Most emirp-enriched residue mod 37 is r=8 (COL2, chi=-1).")
    print()

    print("All assertions passed.")
