# math/theorems/sphenic_happy_371113.py
"""
Structural Audit — 371113 (Sphenic + Happy)
============================================
371113 = 29 × 67 × 191

Properties verified:
  - Sphenic: exactly 3 distinct prime factors
  - Happy:   digit-square iteration reaches 1
  - Digit sequence: [3,7,1,1,1,3] — starts "37", outer pair (3,3)
  - DR = 7,  n mod 37 = 3
  - Morowah: S_d=7, S_p=8 — no pair (7^1=7 but 1^7=1≠8)
"""

import math


def factorize(n: int) -> list[int]:
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def is_happy(num: int) -> bool:
    seen = set()
    while num != 1 and num not in seen:
        seen.add(num)
        num = sum(int(c)**2 for c in str(num))
    return num == 1


def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


N = 371113
P = 37


def verify():
    factors = factorize(N)

    # ── Factorization ─────────────────────────────────────────────────────────
    assert factors == [29, 67, 191]
    assert 29 * 67 * 191 == N

    # All three factors are prime (no further factorization)
    for p in factors:
        assert factorize(p) == [p], f"{p} is not prime"

    # Sphenic: exactly 3 distinct primes
    assert len(factors) == 3 and len(set(factors)) == 3

    # ── Happy sequence ────────────────────────────────────────────────────────
    assert is_happy(N)
    # Trace: 371113 → 70 → 49 → 97 → 130 → 10 → 1
    expected_seq = [371113, 70, 49, 97, 130, 10, 1]
    seq = []
    x = N
    seen: set = set()
    while x != 1 and x not in seen:
        seen.add(x); seq.append(x)
        x = sum(int(c)**2 for c in str(x))
    seq.append(x)
    assert seq == expected_seq, f"Unexpected happy sequence: {seq}"

    # ── Digital structure ─────────────────────────────────────────────────────
    assert dr(N) == 7
    assert N % P == 3
    assert str(N)[:2] == "37"           # opens with the 37-signature
    assert "11" in str(N)               # contains the run of ones
    assert str(N)[0] == str(N)[-1]      # outer digits both 3

    # ── Morowah (no pair) ─────────────────────────────────────────────────────
    sp_total = sum(dr(p) for p in factors)   # dr(29)+dr(67)+dr(191) = 2+4+2 = 8
    S_p = dr(sp_total)
    assert S_p == 8
    # S_d=7, S_p=8: need a^r=7 and r^a=8. 7 = 7^1 only, then 1^7=1≠8. No pair.
    TARGETS = {(a**r, r**a): (a, r)
               for a in range(1,10) for r in range(1,10)
               if a!=r and 1<=a**r<=9 and 1<=r**a<=9}
    assert (dr(N), S_p) not in TARGETS

    print("371113 Structural Audit")
    print()
    print(f"  Factorization: 371113 = {' × '.join(str(p) for p in factors)}")
    print(f"  Sphenic:       True  ✓")
    print(f"  Happy:         True  ✓  (sequence: {expected_seq})")
    print()
    print(f"  Digit sequence: {list(str(N))}  (outer pair: 3,3)")
    print(f"  Starts '37':    True  ✓")
    print(f"  DR(371113):     {dr(N)}")
    print(f"  mod 37:         {N % P}")
    print()
    print(f"  Morowah: S_d={dr(N)}, S_p={S_p}  →  no (a,r) pair  ✓")
    print()
    print("  Factor mod-37 residues:")
    for p in factors:
        print(f"    {p}: DR={dr(p)}  mod37={p%P}")
    print()
    print("All assertions passed.")


if __name__ == "__main__":
    verify()
