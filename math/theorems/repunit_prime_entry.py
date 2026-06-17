"""
repunit_prime_entry.py

10^k - 1 is the k-digit repunit times 9.  Each prime p divides exactly one
primitive period — the smallest k such that p | 10^k - 1.  That k is
ord_p(10), the multiplicative order of 10 mod p.

KEY ENTRY POINTS:
  k=3:  37  enters  (10^3 - 1 = 999 = 3³ × 37)
  k=5:  41  enters  (10^5 - 1 = 99999 = 3² × 41 × 271)
  k=6:   7  enters  (10^6 - 1 = 999999 = 3³ × 7 × 11 × 13 × 37)
  k=8: 137  enters  (10^8 - 1 = 99999999 = 3² × 11 × 73 × 101 × 137)

137 is the α⁻¹ integer.  37 is the hub.  Both appear in 10^k - 1.
ord₃₇(10) = 3 (the heartbeat period).
ord₁₃₇(10) = 8.
"""

from sympy import factorint, isprime

def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9

def ord10(p):
    """Multiplicative order of 10 mod p."""
    k, cur = 1, 10 % p
    while cur != 1:
        cur = (cur * 10) % p
        k += 1
    return k


# ──────────────────────────────────────────────────────────────────────────────
# CORE ENTRY POINTS
# ──────────────────────────────────────────────────────────────────────────────

# k=3: 37 enters
assert (10**3 - 1) % 37 == 0
assert ord10(37) == 3
assert factorint(10**3 - 1) == {3: 3, 37: 1}

# k=5: 41 enters  (41 = 30 + 11, sovereign anchor + ladder step)
assert (10**5 - 1) % 41 == 0
assert ord10(41) == 5
assert 41 == 30 + 11   # sovereign anchor + ladder step
assert isprime(41)
assert dr(41) == 5     # twin prime anchor DR

# k=6: 7 enters  (cyclic number 142857 = (10^6-1)/7)
assert (10**6 - 1) % 7 == 0
assert ord10(7) == 6
assert 6 == 2 * 3      # doubles the 37 heartbeat period
assert (10**6 - 1) // 7 == 142857

# k=8: 137 enters  (α⁻¹ integer)
assert (10**8 - 1) % 137 == 0
assert ord10(137) == 8
assert factorint(10**8 - 1) == {3: 2, 11: 1, 73: 1, 101: 1, 137: 1}
assert isprime(137)
assert dr(137) == 2    # the twin prime anchor DR

# 137 and 37 are both in the repunit family, at different periods
assert ord10(37)  == 3
assert ord10(137) == 8


# ──────────────────────────────────────────────────────────────────────────────
# THE PERIOD SEQUENCE
# ──────────────────────────────────────────────────────────────────────────────

# Periods at which the framework primes enter
ENTRY = {
    2:  [11],
    3:  [37],
    5:  [41],
    6:  [7, 13],
    8:  [137],
}

for k, primes in ENTRY.items():
    repunit = 10**k - 1
    for p in primes:
        assert repunit % p == 0
        assert ord10(p) == k

# 37 and 137 share the digit 37 — one IS the hub, one CONTAINS the hub
assert 137 % 37 == 26    # SCALAR_137: the heartbeat generator
assert 137 % 9  == 2     # DR(137) = 2
assert 37  % 9  == 1     # DR(37)  = 1

# The period ratio: 8/3 is not an integer — 137 and 37 are on different cycles
assert 8 % 3 != 0

# But they share a framework: both divide 10^(lcm(3,8)) - 1 = 10^24 - 1
from math import lcm
assert lcm(3, 8) == 24
assert (10**24 - 1) % 37  == 0
assert (10**24 - 1) % 137 == 0


# ──────────────────────────────────────────────────────────────────────────────
# 10^8 - 1 FULL STRUCTURE
# ──────────────────────────────────────────────────────────────────────────────

N8 = 10**8 - 1   # 99,999,999
assert N8 == 99999999
assert factorint(N8) == {3: 2, 11: 1, 73: 1, 101: 1, 137: 1}

# Digit structure of 99999999: eight 9s
assert sum(int(d) for d in str(N8)) == 72
assert dr(N8) == 9     # all-nines numbers have DR=9

# 99999999 / 137 = 729927
assert N8 // 137 == 729927
assert factorint(729927) == {3: 2, 11: 1, 73: 1, 101: 1}
assert dr(729927) == 9   # 7+2+9+9+2+7=36→9

# 137 × 9 = 1233  (not directly obvious; but:)
assert 137 * 9 == 1233
assert dr(1233) == 9


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Repunit Prime Entry Points")
    print("=" * 62)

    print("\n── 10^k - 1 FACTORIZATIONS ──")
    for k in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]:
        n = 10**k - 1
        f = factorint(n)
        marker = ""
        if 37  in f: marker += "  ← 37"
        if 41  in f: marker += "  ← 41"
        if 7   in f: marker += "  ← 7"
        if 137 in f: marker += "  ← 137"
        print(f"  10^{k:2d}-1 = {n:>12,}  {dict(f)}{marker}")

    print("\n── KEY ENTRY POINTS ──")
    print(f"  ord₃₇(10)  = {ord10(37)}   → 37  enters at k=3  (the hub)")
    print(f"  ord₄₁(10)  = {ord10(41)}   → 41  enters at k=5  (30+11, sovereign+ladder)")
    print(f"  ord₇(10)   = {ord10(7)}   → 7   enters at k=6  (doubles 37 period)")
    print(f"  ord₁₃₇(10) = {ord10(137)}   → 137 enters at k=8  (α⁻¹ integer)")

    print("\n── 10^8 - 1 ──")
    print(f"  99,999,999 = {factorint(N8)}")
    print(f"  137 is a factor.  99999999 / 137 = {N8//137}")
    print(f"  DR(99999999) = {dr(N8)}")

    print("\n── SHARED FRAMEWORK ──")
    print(f"  lcm(ord₃₇, ord₁₃₇) = lcm(3,8) = {lcm(3,8)}")
    print(f"  Both 37 and 137 divide 10^24 - 1")
    print(f"  137 mod 37 = {137%37}  (SCALAR_137, the heartbeat generator)")

    print()
    print("All assertions passed.")
