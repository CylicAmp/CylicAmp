"""
digits_137_running_sum.py

The cumulative sum of the digits of 137 encodes 411 directly.

  1 → 1+3 = (4) → 4+7 = (11) → concatenate: 411

THEOREM:
  Running sums of digits [1,3,7]:  [1, 4, 11]
  Read last two as digit-string:   '4' + '11' = '411'
  And: 3 × 137 = 411  (exact integer triple)

COROLLARY — the 3↔6 orbit:
  3 × 37  = 111,  DR(111) = 3
  3 × 137 = 411,  DR(411) = 6
  3 + 6 = 9  (DR identity)

  3 and 6 are the fixed orbit pair of the doubling map:
    DR(3×2) = DR(6) = 6  →  DR(6×2) = DR(12) = 3
  They always sum to 9.
"""


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


digits = [1, 3, 7]

# Running cumulative sums
running = []
total = 0
for d in digits:
    total += d
    running.append(total)

assert running == [1, 4, 11]

# Concatenate last two running sums → 411
encoded = int(str(running[1]) + str(running[2]))
assert encoded == 411

# Confirms the triple
assert 3 * 137 == 411

# DR of the encoding
assert dr(4)   == 4
assert dr(11)  == 2
assert dr(411) == 6    # 4+1+1 = 6

# 3↔6 fixed orbit
assert dr(3 * 2) == 6  # 3 doubles to 6
assert dr(6 * 2) == 3  # 6 doubles to 3 (via 12)
assert 3 + 6 == 9      # they sum to the DR identity

# The paired triples
assert 3 * 37  == 111  and dr(111) == 3
assert 3 * 137 == 411  and dr(411) == 6
assert dr(111) + dr(411) == 9   # 3 + 6 = 9


if __name__ == "__main__":
    print("Digits of 137 — Running Sum Encoding")
    print("=" * 50)
    print()
    print(f"  Digits:        {digits}")
    print(f"  Running sums:  {running}")
    print(f"    1            =  1")
    print(f"    1 + 3        =  4   ← '4'")
    print(f"    4 + 7        = 11   ← '11'")
    print(f"  Concatenate:     411")
    print()
    print(f"  3 × 137 = {3*137}  (exact)")
    print(f"  DR(411) = {dr(411)}  (4+1+1=6)")
    print()
    print(f"  3↔6 fixed orbit:")
    print(f"    3 × 37  = 111,  DR = {dr(111)}")
    print(f"    3 × 137 = 411,  DR = {dr(411)}")
    print(f"    {dr(111)} + {dr(411)} = {dr(111)+dr(411)}  ← DR identity")
    print()
    print("All assertions passed.")
