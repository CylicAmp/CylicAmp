# math/theorems/liouville_parity_audit.py
"""
Liouville Parity Domain n=1..37
=================================
λ(n) = (−1)^Ω(n), where Ω(n) = total prime factors with multiplicity.

Claims:
  1. Domain cardinality |{1..37}| = 37
  2. |λ⁺| = 17  (λ = +1, even Ω)
  3. |λ⁻| = 20  (λ = −1, odd Ω)
  4. λ(37) = −1  (37 is prime, Ω=1)
  5. Partition sets: perfect squares, biprimes, triprimes, etc.

All claims verified by direct computation of Ω(n).
"""

import math


def Omega(n: int) -> int:
    """Total number of prime factors of n with multiplicity."""
    if n == 1:
        return 0
    count = 0
    d = 2
    while d * d <= n:
        while n % d == 0:
            count += 1
            n //= d
        d += 1
    if n > 1:
        count += 1
    return count


def liouville(n: int) -> int:
    return 1 if Omega(n) % 2 == 0 else -1


def verify():
    print("Liouville Parity Domain n=1..37\n")

    domain = list(range(1, 38))
    assert len(domain) == 37

    # ── Compute Ω and λ for entire domain ─────────────────────────────────────
    omega = {n: Omega(n) for n in domain}
    lam   = {n: liouville(n) for n in domain}

    # ── Claim 1: domain cardinality ───────────────────────────────────────────
    print("=" * 60)
    print("CLAIM 1: |{1..37}| = 37")
    print("=" * 60)
    assert len(domain) == 37
    print(f"  Cardinality = {len(domain)}  ✓")

    # ── Claim 2: |λ⁺| = 17 ───────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("CLAIM 2: 17 elements with λ = +1")
    print("=" * 60)

    lambda_plus  = [n for n in domain if lam[n] == +1]
    lambda_minus = [n for n in domain if lam[n] == -1]
    assert len(lambda_plus) == 17
    assert len(lambda_minus) == 20
    print(f"  λ=+1: {lambda_plus}  count={len(lambda_plus)}  ✓")

    # ── Claim 3: |λ⁻| = 20 ───────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("CLAIM 3: 20 elements with λ = −1")
    print("=" * 60)
    print(f"  λ=−1: {lambda_minus}  count={len(lambda_minus)}  ✓")

    # ── Claim 4: λ(37) = −1 ──────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("CLAIM 4: λ(37) = −1  (37 is prime, Ω=1)")
    print("=" * 60)
    assert omega[37] == 1
    assert lam[37] == -1
    print(f"  Ω(37) = {omega[37]},  λ(37) = {lam[37]}  ✓")

    # ── Claim 5a: λ⁺ partition — perfect squares ──────────────────────────────
    print()
    print("=" * 60)
    print("CLAIM 5a: λ⁺ partition — perfect squares with Ω listed")
    print("=" * 60)

    perfect_squares = {
        1:  0,   # 1
        4:  2,   # 2²
        9:  2,   # 3²
        16: 4,   # 2⁴
        25: 2,   # 5²
        36: 4,   # 2²×3²
    }
    for n, expected_omega in perfect_squares.items():
        assert omega[n] == expected_omega, f"Ω({n}) = {omega[n]}, expected {expected_omega}"
        assert lam[n] == 1
        sq = math.isqrt(n)
        assert sq * sq == n, f"{n} is not a perfect square"
        print(f"  {n:2d}: Ω={omega[n]}, λ=+1  ✓")

    # ── Claim 5b: λ⁺ partition — biprimes (Ω=2, squarefree) ─────────────────
    print()
    print("=" * 60)
    print("CLAIM 5b: λ⁺ partition — biprimes (Ω=2, squarefree)")
    print("=" * 60)

    biprimes = [6, 10, 14, 15, 21, 22, 26, 33, 34, 35]
    for n in biprimes:
        assert omega[n] == 2, f"Ω({n}) = {omega[n]}, expected 2"
        # Squarefree: no perfect square divisor > 1
        sq = math.isqrt(n)
        assert sq * sq != n   # not a perfect square itself
        assert lam[n] == 1
        print(f"  {n:2d}: Ω={omega[n]}, λ=+1  ✓")

    # ── Claim 5c: λ⁺ partition — 24 = 2³×3, Ω=4 ─────────────────────────────
    print()
    print("=" * 60)
    print("CLAIM 5c: 24 = 2³×3, Ω = 3+1 = 4, λ = +1")
    print("=" * 60)
    assert 24 == 8 * 3
    assert omega[24] == 4
    assert lam[24] == 1
    print(f"  24: Ω={omega[24]}, λ=+1  ✓")

    # Verify λ⁺ is exactly these three groups
    computed_plus = set(lambda_plus)
    declared_plus = set(perfect_squares) | set(biprimes) | {24}
    assert computed_plus == declared_plus, (
        f"λ⁺ mismatch: computed={sorted(computed_plus)}, declared={sorted(declared_plus)}"
    )
    print(f"\n  λ⁺ = squares ∪ biprimes ∪ {{24}} = exactly {sorted(declared_plus)}  ✓")

    # ── Claim 5d: λ⁻ partition — primes (Ω=1) ────────────────────────────────
    print()
    print("=" * 60)
    print("CLAIM 5d: λ⁻ partition — primes in 1..37 (Ω=1)")
    print("=" * 60)

    primes_37 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in primes_37:
        assert omega[p] == 1, f"Ω({p}) = {omega[p]}, expected 1"
        assert lam[p] == -1
    assert len(primes_37) == 12
    print(f"  Primes: {primes_37}  count=12  ✓")

    # ── Claim 5e: λ⁻ partition — triprimes (Ω=3) ────────────────────────────
    print()
    print("=" * 60)
    print("CLAIM 5e: λ⁻ partition — triprimes (Ω=3)")
    print("=" * 60)

    triprimes = {
        8:  "2³",
        12: "2²×3",
        18: "2×3²",
        20: "2²×5",
        27: "3³",
        28: "2²×7",
        30: "2×3×5",
    }
    for n, factored in triprimes.items():
        assert omega[n] == 3, f"Ω({n}) = {omega[n]}, expected 3"
        assert lam[n] == -1
        print(f"  {n:2d} = {factored}: Ω={omega[n]}, λ=−1  ✓")

    # ── Claim 5f: λ⁻ partition — 32 = 2⁵, Ω=5 ───────────────────────────────
    print()
    print("=" * 60)
    print("CLAIM 5f: 32 = 2⁵, Ω = 5, λ = −1")
    print("=" * 60)
    assert 32 == 2**5
    assert omega[32] == 5
    assert lam[32] == -1
    print(f"  32: Ω={omega[32]}, λ=−1  ✓")

    # Verify λ⁻ is exactly these three groups
    computed_minus = set(lambda_minus)
    declared_minus = set(primes_37) | set(triprimes) | {32}
    assert computed_minus == declared_minus, (
        f"λ⁻ mismatch: computed={sorted(computed_minus)}, declared={sorted(declared_minus)}"
    )
    print(f"\n  λ⁻ = primes ∪ triprimes ∪ {{32}} = exactly {sorted(declared_minus)}  ✓")

    # ── Full Ω table ──────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("Full Ω(n) and λ(n) table for n=1..37")
    print("=" * 60)
    print(f"\n  {'n':>3}  Ω  λ  |  {'n':>3}  Ω  λ")
    print(f"  {'─'*3}  ─  ─  |  {'─'*3}  ─  ─")
    for i in range(1, 20):
        j = i + 18
        row_j = f"{j:3d}  {omega[j]}  {lam[j]:+d}" if j <= 37 else ""
        print(f"  {i:3d}  {omega[i]}  {lam[i]:+d}  |  {row_j}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"""
  CLAIM 1: |{{1..37}}| = 37                   PASS  ✓
  CLAIM 2: |λ⁺| = 17                         PASS  ✓
  CLAIM 3: |λ⁻| = 20                         PASS  ✓
  CLAIM 4: λ(37) = −1  (37 prime, Ω=1)       PASS  ✓
  CLAIM 5a: 6 perfect squares, Ω even         PASS  ✓
  CLAIM 5b: 10 biprimes (Ω=2, squarefree)    PASS  ✓
  CLAIM 5c: 24 = 2³×3, Ω=4                   PASS  ✓
  CLAIM 5d: 12 primes, Ω=1                   PASS  ✓
  CLAIM 5e: 7 triprimes, Ω=3                 PASS  ✓
  CLAIM 5f: 32 = 2⁵, Ω=5                     PASS  ✓

  Partition check:
    λ⁺ = squares ∪ biprimes ∪ {{24}}           {sorted(lambda_plus)}
    λ⁻ = primes ∪ triprimes ∪ {{32}}           {sorted(lambda_minus)}
  Partitions are disjoint and exhaustive over {{1..37}}  ✓
    """)

    print("All assertions passed.")


if __name__ == "__main__":
    verify()
