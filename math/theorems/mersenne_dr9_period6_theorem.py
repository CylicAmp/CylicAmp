# math/theorems/mersenne_dr9_period6_theorem.py
"""
DR(M_n) Period-6 Theorem and the DR=9 Constraint

─────────────────────────────────────────────────────────────────────────────
THEOREM 1 — PERIOD-6 CYCLE
─────────────────────────────────────────────────────────────────────────────
  2^n mod 9 cycles with period 6: [2, 4, 8, 7, 5, 1]
  → DR(M_n) = DR(2^n − 1) cycles:

    n mod 6 = 1 → DR = 1
    n mod 6 = 2 → DR = 3
    n mod 6 = 3 → DR = 7
    n mod 6 = 4 → DR = 6
    n mod 6 = 5 → DR = 4   ← n=53 (53 mod 6 = 5)
    n mod 6 = 0 → DR = 9   ← n=54 (54 mod 6 = 0)

─────────────────────────────────────────────────────────────────────────────
THEOREM 2 — DR=9 IFF 6∣n
─────────────────────────────────────────────────────────────────────────────
  DR(M_n) = 9  ⟺  6 ∣ n
  Proof: DR(M_n) = 9 ↔ M_n ≡ 0 (mod 9) ↔ 2^n ≡ 1 (mod 9) ↔ 6 ∣ n.

─────────────────────────────────────────────────────────────────────────────
THEOREM 3 — DR=9 IS IMPOSSIBLE FOR MERSENNE PRIMES (p ≥ 5)
─────────────────────────────────────────────────────────────────────────────
  If 6∣p and p is prime, then p = 2 or p = 3 (since 6∣p ⟹ 2∣p and 3∣p).
  For p ≥ 5: p ≡ 1 or 5 (mod 6).
  Therefore DR(M_p) is only ever 1 or 4 for any prime p ≥ 5.

─────────────────────────────────────────────────────────────────────────────
THE TRIVIAL 33.3% CLAIM — REFUTED
─────────────────────────────────────────────────────────────────────────────
  M_{n+1} = 2·M_n + 1 for all n.
  So M_n / (M_n + M_{n+1}) = M_n / (3·M_n + 1) → 1/3 for all n.
  This is NOT a property of n=53/54. It holds for every consecutive pair.

─────────────────────────────────────────────────────────────────────────────
1/3 IN THE 37-FIELD
─────────────────────────────────────────────────────────────────────────────
  3^{−1} mod 37 = 25   (3 × 25 = 75 = 2×37 + 1)
  25 = 5²  — appears in Gauss kernel: 55² = 3025 = 100×30 + 25
  So 1/3 (mod 37) = 25 = 5² — connects the 1/3 structure to the Gauss kernel.
"""

import math


def dr(n): return (n - 1) % 9 + 1 if n > 0 else 9

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True


# ── Period-6 cycle ─────────────────────────────────────────────────────────────

pow2_mod9 = [(2**k) % 9 for k in range(1, 7)]
assert pow2_mod9 == [2, 4, 8, 7, 5, 1]

dr_cycle = [dr(2**k - 1) for k in range(1, 7)]
assert dr_cycle == [1, 3, 7, 6, 4, 9]

# Cycle verified for n=1..60
for n in range(1, 61):
    assert dr(2**n - 1) == dr_cycle[(n - 1) % 6]

# ── Theorem 2: DR=9 iff 6∣n ────────────────────────────────────────────────────

# All n≡0(mod 6) in 1..60 give DR=9
n9_list = [n for n in range(1, 61) if dr(2**n - 1) == 9]
assert n9_list == [6, 12, 18, 24, 30, 36, 42, 48, 54, 60]
assert all(n % 6 == 0 for n in n9_list)

# All n≢0(mod 6) in 1..60 give DR≠9
assert all(dr(2**n - 1) != 9 for n in range(1, 61) if n % 6 != 0)

# ── Theorem 3: DR=9 impossible for Mersenne primes p≥5 ────────────────────────

# For prime p≥5: p mod 6 is only 1 or 5
primes_to_100 = [p for p in range(5, 101) if is_prime(p)]
assert all(p % 6 in (1, 5) for p in primes_to_100)

# DR(M_p) is only ever 1 or 4 for prime p≥5
for p in primes_to_100:
    d = dr(2**p - 1)
    assert d in (1, 4), f"prime p={p}: DR(M_p)={d} — expected 1 or 4"

# Exactly: p≡1(mod 6)→DR=1, p≡5(mod 6)→DR=4
for p in primes_to_100:
    if p % 6 == 1:
        assert dr(2**p - 1) == 1
    else:  # p%6==5
        assert dr(2**p - 1) == 4

# n=53 and n=54 fit the cycle
assert 53 % 6 == 5 and dr(2**53 - 1) == 4
assert 54 % 6 == 0 and dr(2**54 - 1) == 9

# ── Trivial 33.3% refutation ───────────────────────────────────────────────────

# M_{n+1} = 2·M_n + 1  always
for n in range(1, 20):
    assert 2**(n+1) - 1 == 2*(2**n - 1) + 1

# Ratio M_n/(M_n+M_{n+1}) → 1/3 for all n — not special to 53/54
for n in range(1, 20):
    mn, mn1 = 2**n - 1, 2**(n+1) - 1
    ratio = mn / (mn + mn1)
    assert abs(ratio - 1/3) < 1/(2**n)   # converges to 1/3 for all n

# ── 1/3 in the 37-field ────────────────────────────────────────────────────────

assert 3 * 25 % 37 == 1          # 3^{-1} mod 37 = 25
assert 25 == 5**2                 # 25 = 5²
assert 55**2 == 3025              # Gauss kernel
assert 3025 % 100 == 25          # 3025 ends in 25 = 5² = 3^{-1} mod 37


if __name__ == "__main__":
    print("DR(M_n) Period-6 Theorem")
    print()
    print("Cycle (n mod 6 = 1..6):")
    labels = ["n≡1", "n≡2", "n≡3", "n≡4", "n≡5", "n≡0"]
    for label, d in zip(labels, dr_cycle):
        marker = "  ← DR=9 iff 6∣n" if d == 9 else ""
        print(f"  {label}(mod 6): DR(M_n) = {d}{marker}")
    print()
    print("Mersenne primes p≥5:")
    primes_sample = [p for p in range(5, 60) if is_prime(p)]
    for p in primes_sample:
        print(f"  p={p:2d}  p%6={p%6}  DR(M_p)={dr(2**p-1)}")
    print()
    print("Theorem: DR(M_p) ∈ {1,4} for all prime p≥5. DR=9 is impossible.")
    print()
    print("Trivial 33.3% refutation:")
    for n in [2, 5, 10, 53]:
        mn, mn1 = 2**n-1, 2**(n+1)-1
        r = mn/(mn+mn1)
        print(f"  n={n:2d}: M_n/(M_n+M_{{n+1}}) = {r:.6f}  (→1/3 for all n)")
    print()
    print(f"1/3 mod 37 = 25 = 5²  (appears in Gauss kernel: 55²=3025, last two digits=25)")
    print()
    print("All assertions passed.")
