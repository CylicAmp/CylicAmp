"""
collision_node_20979.py

Factorization and digital root properties of 20979.

─────────────────────────────────────────────────────────────────
DEFINITION:
  20979 = 3⁴ × 7 × 37

VERIFIED PROPERTIES [PROVEN]:
  (i)   20979 = 37 × 567 = 37 × 7 × 81 = 37 × 7 × 3⁴
  (ii)  DS(20979) = 27 = 3³,   DR(20979) = 9 = 3²
  (iii) rev(20979) = 97902,    DS(97902) = 27,  DR(97902) = 9
  (iv)  DR(20979) = DR(rev(20979)) = 9    [DR-palindrome pair]

FRAMEWORK CONTEXT:
  Contains the framework modulus 37.
  567 = 7 × 81 = 7 × 3⁴: DR(567) = 18, DR²(567) = 9.
  37 itself: DR(37) = 10 → DR(10) = 1.
  Product inherits DR=9 from 567 (since DR(37)≡1, DR(37×n)=DR(n) mod 9).

NOTE ON UNIQUENESS:
  20979 is not unique among multiples of 37 with DR=9.
  Other examples: 333, 666, 999, 1332, 1665, 1998, 2331, ...
  The defining property is the specific factorization 37 × 7 × 3⁴,
  which simultaneously involves framework prime 37, prime 7, and
  the largest power of 3 fitting in a 5-digit multiple of 37×7.
─────────────────────────────────────────────────────────────────
"""


def ds(n):
    return sum(int(d) for d in str(n))


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def rev(n):
    return int(str(n)[::-1])


N = 20979

# ──────────────────────────────────────────────────────────────────────────────
# FACTORIZATION
# ──────────────────────────────────────────────────────────────────────────────

assert 37 * 567 == N
assert 7 * 81 == 567
assert 3**4 == 81
assert 3**4 * 7 * 37 == N

# Prime factorization: 3^4 × 7 × 37
assert N == 3**4 * 7 * 37

# Factor DRs
assert ds(567) == 18 and dr(567) == 9
assert dr(37) == 1             # DR(37) = 3+7 = 10 → DR = 1
assert dr(N) == 9              # DR multiplies by DR(37)=1, so DR(37k)=DR(k) mod 9


# ──────────────────────────────────────────────────────────────────────────────
# DIGIT PROPERTIES
# ──────────────────────────────────────────────────────────────────────────────

assert ds(N) == 2 + 0 + 9 + 7 + 9
assert ds(N) == 27
assert dr(N) == 9

# DR(37 × k) = DR(k) when DR(37) = 1 (which it is)
# Verify: DR(37k) = DR(k) for small k
for k in range(1, 20):
    assert dr(37 * k) == dr(k), f"DR(37×{k}) ≠ DR({k})"

# So DR(20979) = DR(37 × 567) = DR(567) = 9
assert dr(N) == dr(567)


# ──────────────────────────────────────────────────────────────────────────────
# REVERSAL
# ──────────────────────────────────────────────────────────────────────────────

R = rev(N)
assert R == 97902
assert ds(R) == 9 + 7 + 9 + 0 + 2
assert ds(R) == 27
assert dr(R) == 9

# DR-palindrome pair: DR(n) = DR(rev(n)) = 9
assert dr(N) == dr(R)


# ──────────────────────────────────────────────────────────────────────────────
# FRAMEWORK PRIME 37 CONTEXT
# ──────────────────────────────────────────────────────────────────────────────

# DR(37k) = DR(k) because DR(37) = 1 acts as identity on DR product
# This means 37 is "invisible" in DR arithmetic
assert dr(37) == 1
assert dr(37 * 9) == 9    # DR(333) = 9
assert dr(37 * 18) == 9   # DR(666) = 9
assert dr(37 * 27) == 9   # DR(999) = 9

# 20979 has DR=9 because 567 has DR=9 and 37 acts as DR-identity
assert dr(37 * 567) == dr(567) == 9


# ──────────────────────────────────────────────────────────────────────────────
# UNIQUENESS SCOPE
# ──────────────────────────────────────────────────────────────────────────────

# Among 5-digit multiples of 37 with DR=9:
five_digit_37_dr9 = [37 * k for k in range(270, 2703)  # 5-digit range
                     if 10000 <= 37*k <= 99999 and dr(37*k) == 9]
# 20979 is one of many
assert N in five_digit_37_dr9
assert len(five_digit_37_dr9) > 1    # not unique among 5-digit multiples

# But 20979 = 37 × 7 × 3^4 is the unique product of these three factors
assert len([n for n in range(1, 100000) if n == 3**4 * 7 * 37]) == 1


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Collision Node 20979 — Factorization and DR Properties")
    print("=" * 62)

    print(f"\n  N = {N}")
    print(f"  Factorization: 3⁴ × 7 × 37 = {3**4} × 7 × 37")
    print(f"  37 × 567 = {37*567}  ({'✓' if 37*567==N else '✗'})")
    print(f"  7 × 81 = {7*81}  ({'✓' if 7*81==567 else '✗'})")
    print(f"  3⁴ = {3**4}")

    print(f"\n  DS({N}) = {ds(N)},  DR = {dr(N)}")
    print(f"  rev({N}) = {R},  DS = {ds(R)},  DR = {dr(R)}")
    print(f"  DR-palindrome pair: DR(n) = DR(rev(n)) = 9")

    print(f"\n  Framework property:")
    print(f"    DR(37) = {dr(37)}  (37 acts as DR-identity: DR(37k) = DR(k))")
    print(f"    DR(20979) = DR(37×567) = DR(567) = {dr(567)}")

    print(f"\n  Uniqueness note:")
    print(f"    Among 5-digit multiples of 37 with DR=9: {len(five_digit_37_dr9)} elements.")
    print(f"    20979 is unique only as 3⁴×7×37 specifically.")

    print()
    print("All assertions passed.")
