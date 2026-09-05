# math/theorems/sphenic_191919919191_audit.py
"""
Structural Audit — 191919919191
================================
191919919191 = 3 × 7 × 11 × 13 × 37 × 167 × 10343
             = 111111 × 167 × 10343

Key facts:
  - 7 distinct prime factors, all exponent 1 (squarefree)
  - Divisor count = 2^7 = 128
  - 3×7×11×13×37 = 111111  (the 37-period lock)
  - n mod 37 = 0  (37 is a factor)
  - DR(n) = DR(digit_sum=60) = 6 = DR(111111)
  - S_d = S_p = 6  (Morowah pair impossible: a^r=6⟹a=6,r=1, but 1^6=1≠6)

Digit string 191919919191:
  Two halves — 191919 | 919191
  191919 + 919191 = 1111110 = 111111 × 10
"""

import math


def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


def analyze_number(n: int):
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            count = 0
            while temp % d == 0:
                count += 1
                temp //= d
            factors.append((d, count))
        d += 1
    if temp > 1:
        factors.append((temp, 1))
    divisors = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)
            if n // i != i:
                divisors.append(n // i)
    return factors, len(divisors)


N = 191919919191
P = 37
PRIMES = [3, 7, 11, 13, 37, 167, 10343]


def verify():
    factors, div_count = analyze_number(N)

    # ── Factorization ─────────────────────────────────────────────────────────
    assert factors == [(p, 1) for p in PRIMES]
    product = 1
    for p in PRIMES:
        product *= p
    assert product == N

    # 111111 = 3×7×11×13×37 (the 37-period lock)
    assert 3 * 7 * 11 * 13 * 37 == 111111
    assert 111111 * 167 * 10343 == N

    # Squarefree → divisor count = 2^7
    assert div_count == 2**7 == 128

    # ── 37-field ──────────────────────────────────────────────────────────────
    assert N % P == 0
    assert 111111 % P == 0

    # ── Digital structure ─────────────────────────────────────────────────────
    digit_sum = sum(int(c) for c in str(N))
    assert digit_sum == 60
    assert dr(digit_sum) == 6
    assert dr(N) == 6
    assert dr(111111) == 6    # DR inherited from the 111111 core

    # Two-half digit sum: 191919 + 919191 = 111111 × 10
    lo, hi = int(str(N)[:6]), int(str(N)[6:])
    assert lo == 191919
    assert hi == 919191
    assert lo + hi == 111111 * 10

    # ── Morowah ───────────────────────────────────────────────────────────────
    sp_total = sum(dr(p) for p in PRIMES)
    S_p = dr(sp_total)
    assert dr(N) == 6
    assert S_p == 6          # S_d = S_p = 6
    # No Morowah pair: a^r=6 requires a=6,r=1; then r^a=1^6=1≠6
    TARGETS = {(a**r, r**a): (a, r)
               for a in range(1, 10) for r in range(1, 10)
               if a != r and 1 <= a**r <= 9 and 1 <= r**a <= 9}
    assert (6, 6) not in TARGETS

    print("191919919191 Structural Audit")
    print()
    print(f"  Factorization: {' × '.join(str(p) for p in PRIMES)}")
    print(f"  = 111111 × 167 × 10343")
    print(f"  Squarefree, 7 distinct primes  ✓")
    print(f"  Divisor count: 2^7 = {div_count}  ✓")
    print()
    print(f"  37-field: n mod 37 = {N % P}  (37 | n)  ✓")
    print(f"  111111 = 3×7×11×13×37 (37-period lock)  ✓")
    print()
    print(f"  Digit sum = {digit_sum},  DR = {dr(digit_sum)}")
    print(f"  DR(111111) = {dr(111111)}  (same DR)  ✓")
    print()
    print(f"  Two-half split: {lo} | {hi}")
    print(f"  {lo} + {hi} = {lo+hi} = 111111 × 10  ✓")
    print()
    print(f"  Factor DRs: {[dr(p) for p in PRIMES]}  → sum={sp_total}  S_p={S_p}")
    print(f"  S_d = S_p = 6  →  Morowah pair impossible  ✓")
    print()
    print("All assertions passed.")


if __name__ == "__main__":
    verify()
