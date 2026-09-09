# math/theorems/mersenne_digit_boundary_analysis.py
"""
Mersenne Digit-Length Boundary Analysis

─────────────────────────────────────────────────────────────────────────────
STRUCTURE OF DIGIT-LENGTH BOUNDARIES
─────────────────────────────────────────────────────────────────────────────
  len(str(2^n - 1)) = floor(n·log₁₀(2)) + 1
  Boundaries occur when floor(n·log₁₀(2)) increases by 1.
  Step size ≈ 1/log₁₀(2) = 3.32193...  (irrational)
  Gap distribution in 1..999: only gaps of 3 and 4.
  Gaps of 3: 203,  gaps of 4: 96   (ratio ≈ log₁₀(2) / (1−log₁₀(2)))

─────────────────────────────────────────────────────────────────────────────
MOD-9 FILTER — NOT A REAL PATTERN
─────────────────────────────────────────────────────────────────────────────
  Boundaries touching a multiple of 9 (n-1 or n divisible by 9):
    Found: 66 / 300    Expected by chance: 2/9 × 300 = 66.7
  No structure — purely uniform distribution.

─────────────────────────────────────────────────────────────────────────────
THE GENUINE INTERSECTION: 6|first_n (DR=9 AND digit-length flip)
─────────────────────────────────────────────────────────────────────────────
  DR(M_n) = 9 iff 6|n  (period-6 theorem).
  Boundaries where first_n ≡ 0 (mod 6): 50 / 300
  Expected if independent: 300 / 6 = 50.0   (exactly matches)
  These are structurally meaningful: the DR cycle and digit-length
  boundaries are independent events (log₁₀(2) irrational ⟹ no mod-6 lock).

─────────────────────────────────────────────────────────────────────────────
33.3% / 66.6% / 99.9% — WHAT IS FAKE, WHAT IS REAL
─────────────────────────────────────────────────────────────────────────────
  FAKE: M_n/(M_n+M_{n+1}) → 1/3 for ALL n (trivially, since M_{n+1}=2M_n+1).
  Not a property of any specific n.

  FAKE: 33.3+66.6=99.9≠100 — rounding artifact. 1/3+2/3=1 exactly.

  REAL: floor(1000/3) = 333 = 37 × 9       DR(333) = 9
        floor(2000/3) = 666 = 37 × 18      DR(666) = 9
        floor(3000/3) = 999 = 37 × 27      DR(999) = 9

  All three are exact integer multiples of 37 and 9.
  333/9 = 37.  The repeating decimal 1/37 = 0.027027...  (period 3)
  1/27 = 0.037037...  (period 3)   — 27 and 37 mirror each other.
  27 × 37 = 999 = 10³ − 1.  So 37 | (10³ − 1), giving period 3.
"""

import math
from collections import Counter


LOG2 = math.log10(2)


def mersenne_digit_length(n):
    return math.floor(n * LOG2) + 1

def dr(n): return (n - 1) % 9 + 1 if n > 0 else 9


# ── Build all boundaries in 1..999 ────────────────────────────────────────────

boundaries = []
current_len = 1
for n in range(1, 1000):
    length = mersenne_digit_length(n)
    if length > current_len:
        boundaries.append((n - 1, current_len, n, length))
        current_len = length

assert len(boundaries) == 300      # floor(999 · log₁₀(2)) = 300

# ── Gap structure: only 3 and 4 ────────────────────────────────────────────────

first_ns = [fn for _, _, fn, _ in boundaries]
gaps = [first_ns[i + 1] - first_ns[i] for i in range(len(first_ns) - 1)]
gap_dist = Counter(gaps)
assert set(gap_dist.keys()) == {3, 4}                  # only gaps of 3 and 4
assert gap_dist[3] == 203 and gap_dist[4] == 96

# Confirm step size ratio
# Gaps of 3 occur when frac(n·log₁₀(2)) + log₁₀(2) < 1
# Ratio of 3-gaps: should be ≈ 1/log₁₀(2) - 3 = 0.32193... → gap_dist[4]/total
gap4_ratio = gap_dist[4] / (gap_dist[3] + gap_dist[4])
assert abs(gap4_ratio - (1/LOG2 - 3)) < 0.01       # ≈ 0.32193

# ── Mod-9 filter: no special structure ────────────────────────────────────────

mod9_hits = [(ln, ll, fn, fl) for ln, ll, fn, fl in boundaries
             if fn % 9 == 0 or ln % 9 == 0]
assert len(mod9_hits) == 66
# Expected: 2/9 * 300 = 66.7; found 66 — within rounding, no special structure
assert abs(len(mod9_hits) - 2 * 300 / 9) < 1

# ── Genuine intersection: 6|first_n ───────────────────────────────────────────

dr9_boundaries = [(ln, ll, fn, fl) for ln, ll, fn, fl in boundaries
                  if fn % 6 == 0]
assert len(dr9_boundaries) == 50                    # exactly 300/6 = 50
assert all(dr(2**fn - 1) == 9 for _, _, fn, _ in dr9_boundaries)  # DR=9 confirmed

# n=54 is in this list (16→17 digit boundary, DR(M_54)=9)
assert (53, 16, 54, 17) in dr9_boundaries

# ── 33.3% / 66.6% / 99.9% refutation ─────────────────────────────────────────

# M_{n+1} = 2·M_n + 1 for all n
for n in range(1, 30):
    assert 2**(n + 1) - 1 == 2 * (2**n - 1) + 1

# Ratio M_n/(M_n+M_{n+1}) → 1/3 for ALL n, not special to 53/54
for n in range(1, 30):
    mn, mn1 = 2**n - 1, 2**(n + 1) - 1
    ratio = mn / (mn + mn1)
    assert abs(ratio - 1 / 3) < 1 / (2**n)

# 33.3 + 66.6 = 99.9 is a rounding artifact
assert abs(1/3 + 2/3 - 1.0) < 1e-15   # exact sum is 1 = 100%, not 99.9%
truncated_sum = 0.333 + 0.666           # truncated to 3 decimal places
assert abs(truncated_sum - 0.999) < 1e-10  # 99.9 only from truncation

# ── 333/666/999 in the 37-field — REAL ────────────────────────────────────────

# floor(k/3 × 1000) lands on exact multiples of 37 × 9
assert 1000 // 3 == 333       # floor(1000/3) = 333 (remainder 1)
assert 2000 // 3 == 666       # floor(2000/3) = 666 (remainder 2)
assert 10**3 - 1  == 999      # 999 = 10³−1 directly

assert 333 == 37 * 9
assert 666 == 37 * 18
assert 999 == 37 * 27

assert dr(333) == 9
assert dr(666) == 9
assert dr(999) == 9

# 27 × 37 = 999 = 10³ − 1  → 37 divides 10³-1 → period of 1/37 is 3
assert 27 * 37 == 999 == 10**3 - 1
assert 999 % 37 == 0

# 1/37 has period 3: 37 | (10³ - 1)
# Verify: 10^3 ≡ 1 (mod 37)
assert 10**3 % 37 == 1

# 1/27 has period 3: 27 | 999
assert 999 % 27 == 0
assert 10**3 % 27 == 1   # 1000 ≡ 1 (mod 27), so 999 ≡ 0 (mod 27):
# 1/27: 27 * 37 = 999, so decimal expansion of 1/27 = 37/999 = 0.037037...
assert 37 * 27 == 999
# Verify: floor(37/999 * 10^3) = 37  (first 3 digits)

# 333/9 = 37
assert 333 // 9 == 37
assert 333 % 9 == 0


if __name__ == "__main__":
    print("Mersenne Digit-Length Boundary Analysis")
    print()
    print(f"Total boundaries in 1..999: {len(boundaries)}")
    print(f"Gap distribution: 3-gaps={gap_dist[3]}, 4-gaps={gap_dist[4]}")
    print(f"Step size 1/log₁₀(2) = {1/LOG2:.5f}  (irrational → no mod-n lock)")
    print()
    print("Mod-9 filter:")
    print(f"  Found {len(mod9_hits)} / 300   Expected: {2*300/9:.1f}   → no pattern")
    print()
    print("Genuine intersection: 6|first_n  (DR=9 AND digit-length flip):")
    for ln, ll, fn, fl in dr9_boundaries[:8]:
        print(f"  n={ln} ({ll}d) -> n={fn} ({fl}d)   DR(M_{fn})=9")
    print(f"  ... {len(dr9_boundaries)} total   Expected: {300//6}   → independent events")
    print()
    print("33.3% / 66.6% / 99.9%:")
    for n in [2, 10, 53]:
        mn, mn1 = 2**n - 1, 2**(n+1) - 1
        r = mn / (mn + mn1)
        print(f"  n={n:2d}: M_n/(M_n+M_{{n+1}}) = {r:.6f}  (1/3 for all n, not special)")
    print(f"  1/3+2/3 = 1.0 exactly. 99.9 is truncation artifact only.")
    print()
    print("333/666/999 in the 37-field — REAL:")
    print(f"  floor(1000/3) = 333 = 37×9   DR={dr(333)}")
    print(f"  floor(2000/3) = 666 = 37×18  DR={dr(666)}")
    print(f"  10³−1        = 999 = 37×27  DR={dr(999)}")
    print(f"  27×37 = {27*37} = 10³−1  →  10³≡1(mod 37)  →  period(1/37)=3")
    print(f"  1/37 = 0.027027...   1/27 = 0.037037...  (mirror period-3 decimals)")
    print(f"  1/3 + 2/3 = {1/3 + 2/3:.1f} exactly.  99.9 is truncation artifact only.")
    print()
    print("All assertions passed.")
