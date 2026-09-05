"""
PRIMITIVE ROOT TEST THEOREM
=========================================================================

Theorem:
  Let p be an odd prime and g an integer with gcd(g, p) = 1.
  Then g is a primitive root mod p (i.e., ord_p(g) = p − 1)
  if and only if:

      g^((p−1)/q) ≢ 1 (mod p)   for every prime q dividing p − 1.

Proof sketch:
  (⇒) Necessity: If ord_p(g) = p−1, then g^k ≡ 1 (mod p) only when
      (p−1) | k. Since (p−1)/q < p−1 for any prime q | (p−1), the
      condition g^((p−1)/q) ≢ 1 follows directly.

  (⇐) Sufficiency: Let d = ord_p(g). Since d | (p−1), write p−1 = d·m.
      If d < p−1, some prime q divides (p−1)/d, so d | (p−1)/q, giving
      g^((p−1)/q) ≡ 1 (mod p) — contradiction. Hence d = p−1.

Efficiency:
  Naive approach: check g^k ≢ 1 for all proper divisors of p−1.
  For p=37: p−1=36 has 8 proper divisors → 8 modular exponentiations.

  Theorem approach: check only prime factors of p−1.
  For p=37: prime factors of 36 are {2, 3} → 2 checks only.
  For p=2^64−2^32+1 (Goldilocks): p−1=2^32×3×5×17×257×65537 → 6 checks.

Verified examples:
  p=37, g=2:   2^18 ≡ 36 ≠ 1,  2^12 ≡ 26 ≠ 1  → primitive root ✓
  p=31, g=3:   3^15 ≡ 30 ≠ 1,  3^10 ≡ 25 ≠ 1,  3^6 ≡ 16 ≠ 1  → primitive root ✓

Connection to GF(37):
  This theorem is the certificate that the ×2 mod 37 orbit is complete.
  Without it, orbit completeness requires checking 35 divisors.
  With it, 2 checks suffice. The prime factorization of p−1 = 36 = 2²×3²
  is the algebraic bridge between the orbit (×2 mod 37) and the cascade
  ({8,13,24} → 37 elements): both are governed by the structure of 36.
"""


def prime_factors(n: int) -> set:
    """Return the set of distinct prime factors of n."""
    factors, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


def is_primitive_root(g: int, p: int) -> tuple:
    """
    Test whether g is a primitive root mod p using the theorem.
    Returns (True, None) if g is primitive, or (False, q) where q
    is the prime factor of p-1 that witnesses the failure.
    """
    pm1 = p - 1
    for q in prime_factors(pm1):
        if pow(g, pm1 // q, p) == 1:
            return False, q
    return True, None


def all_primitive_roots(p: int) -> list:
    """Return all primitive roots mod p in sorted order."""
    return [g for g in range(1, p) if is_primitive_root(g, p)[0]]


def verify_example(g: int, p: int):
    """Full verification with printed proof trace."""
    pm1   = p - 1
    pf    = sorted(prime_factors(pm1))
    print(f"\np={p}, g={g}")
    print(f"  p−1 = {pm1},  prime factors = {pf}")
    all_ok = True
    for q in pf:
        exp = pm1 // q
        val = pow(g, exp, p)
        ok  = val != 1
        print(f"  g^((p−1)/{q}) = {g}^{exp} mod {p} = {val}  {'✓' if ok else '✗ FAILS'}")
        if not ok:
            all_ok = False
    ok, _ = is_primitive_root(g, p)
    print(f"  → is_primitive_root({g}, {p}) = {ok}")
    return ok


# =============================================================================
# Summary
# =============================================================================

def summarise():
    print("=" * 60)
    print("PRIMITIVE ROOT TEST THEOREM — VERIFICATION")
    print("=" * 60)

    verify_example(2, 37)
    verify_example(3, 31)

    print("\n--- Efficiency comparison (p=37) ---")
    proper_divs = [d for d in range(1, 36) if 36 % d == 0]
    pf_36 = sorted(prime_factors(36))
    print(f"  Proper divisors of 36: {proper_divs}  ({len(proper_divs)} checks)")
    print(f"  Prime factors of 36:   {pf_36}  ({len(pf_36)} checks)")
    print(f"  Reduction: {len(proper_divs)} → {len(pf_36)}")

    print("\n--- All primitive roots mod 37 ---")
    roots_37 = all_primitive_roots(37)
    print(f"  {roots_37}")
    print(f"  Count: {len(roots_37)} = φ(φ(37)) = φ(36) = {sum(1 for g in roots_37)}")

    print("\n--- All primitive roots mod 31 ---")
    roots_31 = all_primitive_roots(31)
    print(f"  {roots_31}")

    print("\n--- Goldilocks prime (6 checks) ---")
    p_gold  = 2**64 - 2**32 + 1
    pf_gold = sorted(prime_factors(p_gold - 1))
    print(f"  p = 2^64 − 2^32 + 1")
    print(f"  p−1 prime factors: {pf_gold}  ({len(pf_gold)} checks)")
    g_gold, _ = 7, None
    ok, _   = is_primitive_root(g_gold, p_gold)
    print(f"  is_primitive_root(7, p) = {ok}  (smallest primitive root = 7)")


def run_assertions():
    assert is_primitive_root(2, 37)[0], "2 must be a primitive root mod 37"
    assert pow(2, 18, 37) == 36, "2^18 mod 37 must be 36 (≡ -1)"
    assert pow(2, 12, 37) == 26, "2^12 mod 37 must be 26 (≠ 1)"

    assert is_primitive_root(3, 31)[0], "3 must be a primitive root mod 31"
    assert pow(3, 15, 31) == 30, "3^15 mod 31 must be 30 (≡ -1)"
    assert pow(3, 10, 31) == 25, "3^10 mod 31 must be 25"
    assert pow(3,  6, 31) == 16, "3^6  mod 31 must be 16"

    from sympy import totient
    roots_37 = all_primitive_roots(37)
    assert len(roots_37) == totient(36) == 12, \
        f"|PR(37)| = {len(roots_37)}, expected φ(36)=12"
    assert roots_37 == [2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35]

    p_gold = 2**64 - 2**32 + 1
    assert is_primitive_root(7, p_gold)[0], "7 must be a primitive root mod Goldilocks prime"
    pf_gold = sorted(prime_factors(p_gold - 1))
    assert pf_gold == [2, 3, 5, 17, 257, 65537], \
        f"Goldilocks p-1 prime factors = {pf_gold}"


if __name__ == "__main__":
    run_assertions()
    summarise()
