"""
Carmichael Numbers of Cyclotomic Type Divisible by 37
======================================================

Two families searched up to k = 20,000:

  Type A:  n = Φ₃(2k) = 4k² + 2k + 1   (3rd cyclotomic polynomial at 2k)
  Type B:  n = Φ₄(2k) = 4k² + 1         (4th cyclotomic polynomial at 2k)

DATA (Carmichaels found, k ≤ 20,000):
  Type B  k=108    n=46657     = 13 × 37 × 97
  Type B  k=780    n=2433601   = 17 × 37 × 53 × 73
  Type A  k=1152   n=5310721   = 13 × 37 × 61 × 181
  Type B  k=4104   n=67371265  = 5 × 13 × 37 × 109 × 257

WHY 37 DIVIDES ALL FOUR:

  Type B:  4k² + 1 ≡ 0 mod 37
    ↔ 4k² ≡ -1 ≡ 36 mod 37
    ↔ k² ≡ 9 mod 37
    ↔ k ≡ ±3 mod 37       (since 3² = 9, and 3 is a QR mod 37)

  Type A:  4k² + 2k + 1 ≡ 0 mod 37
    Discriminant: 4 - 16 = -12 ≡ 25 mod 37,  √25 = ±5 mod 37
    k = (-2 ± 5) / 8 mod 37  (8⁻¹ ≡ 14 mod 37)
    ↔ k ≡ 14×3 = 42 ≡ 5 mod 37   or   k ≡ 14×(-7) = -98 ≡ 13 mod 37

  Verified:
    k=108  ≡ -3 mod 37  (34 mod 37)  → Type B k²≡9 mod 37 ✓
    k=780  ≡  3 mod 37              → Type B k²≡9 mod 37 ✓
    k=4104 ≡ -3 mod 37  (34 mod 37)  → Type B k²≡9 mod 37 ✓
    k=1152 ≡  5 mod 37              → Type A ✓

PRIME FACTOR STRUCTURE (from cyclotomic polynomial theory):

  Type A (Φ₃): if p | Φ₃(2k) then ord_p(2k) = 3, so 3 | (p-1), so p ≡ 1 mod 3.
    All prime factors are in COL1 (chi_{-3} = +1).
    Verified: 13≡37≡61≡181≡1 mod 3 for n=5310721.

  Type B (Φ₄): if p | Φ₄(2k) then ord_p(2k) = 4, so 4 | (p-1), so p ≡ 1 mod 4.
    All prime factors ≡ 1 mod 4 (Gaussian split primes in Z[i]).
    Verified: 13≡17≡37≡53≡73≡97≡109≡257≡5≡1 mod 4  (5≡1 mod 4 ✓).
    COL2 factors (chi=-1) can appear but always in even count → n ∈ COL1.

DR AND χ₋₃ STRUCTURE:

  All four n have DR = 1 and chi_{-3} = +1 (COL1, identity).
  Reason: k ≡ 0 mod 3 for all cases → k² ≡ 0 mod 9 → 4k² ≡ 0 mod 9.
    Type B: n = 4k²+1 ≡ 1 mod 9 → DR = 1 ✓
    Type A: n = 4k²+2k+1 ≡ 0+0+1 = 1 mod 9 → DR = 1 ✓  (k≡0 mod 3 → 2k≡0 mod 9 only if k≡0 mod 9)
    For k=780: k≡6 mod 9 → k²≡36≡0 mod 9 → n≡1 mod 9. ✓
    For k=108,4104,1152: k≡0 mod 9 → n≡1 mod 9. ✓

  n-1 = 4k² (Type B) or 4k²+2k (Type A):
    DR(n-1) = DR(n-1 mod 9) = DR(0) = 9  (sovereign, as expected for Carmichael n-1)
    Verified: all n-1 have digit sum divisible by 9.

KORSELT CRITERION:
  n is Carmichael ↔ squarefree AND (p-1)|(n-1) for every prime p|n.
  For Type B: n-1 = 4k². Condition: (p-1) | 4k² for each prime p|n.
  For Type A: n-1 = 4k²+2k = 2k(2k+1). Condition: (p-1) | 2k(2k+1).

SPARSITY: only 4 Carmichaels found up to k=20,000 across both families.
  Type B: k = 108, 780, 4104  (3 examples)
  Type A: k = 1152             (1 example)
  The mod-37 condition on k is necessary but far from sufficient for Carmichaelhood.
"""

from math import gcd


def dr(n: int) -> int:
    return (n - 1) % 9 + 1 if n > 0 else 0


def chi_m3(n: int) -> int:
    r = n % 3
    return 1 if r == 1 else (-1 if r == 2 else 0)


def factor(n: int) -> list:
    fs = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            fs.append(d)
            n //= d
        d += 1
    if n > 1:
        fs.append(n)
    return fs


def phi3(k: int) -> int:
    return 4 * k * k + 2 * k + 1


def phi4(k: int) -> int:
    return 4 * k * k + 1


DATA = [
    ('B', 108, 46657),
    ('B', 780, 2433601),
    ('A', 1152, 5310721),
    ('B', 4104, 67371265),
]

KNOWN_FACTORS = {
    46657: [13, 37, 97],
    2433601: [17, 37, 53, 73],
    5310721: [13, 37, 61, 181],
    67371265: [5, 13, 37, 109, 257],
}

for typ, k, n in DATA:
    # Verify formula
    formula_val = phi4(k) if typ == 'B' else phi3(k)
    assert formula_val == n, f"Formula failed for type {typ}, k={k}"

    # Verify factorization
    fs = KNOWN_FACTORS[n]
    assert all(n % p == 0 for p in fs)
    check_product = 1
    for p in fs:
        check_product *= p
    assert check_product == n, f"Factor product mismatch for n={n}"

    # Korselt criterion
    n1 = n - 1
    assert len(set(fs)) == len(fs), f"n={n} not squarefree"
    for p in fs:
        assert n1 % (p - 1) == 0, f"Korselt failed: ({p}-1) ∤ ({n}-1)"

    # 37 divides n
    assert 37 in fs, f"37 not a factor of n={n}"

    # k mod 37 condition
    k37 = k % 37
    if typ == 'B':
        assert (4 * k * k) % 37 == 36, f"Type B: 4k^2 ≢ -1 mod 37 for k={k}"
    else:
        assert k37 in {5, 13}, f"Type A: k mod 37 should be 5 or 13, got {k37}"

    # All prime factors ≡ 1 mod 4 (both types) — from cyclotomic factorization
    for p in fs:
        assert p % 4 == 1, f"p={p} not ≡1 mod 4"

    # Type A: all factors ≡ 1 mod 3 (COL1)
    if typ == 'A':
        for p in fs:
            assert p % 3 == 1, f"Type A: p={p} not ≡1 mod 3"

    # n itself: DR=1, chi=+1 (COL1)
    assert dr(n) == 1, f"DR({n}) = {dr(n)}, expected 1"
    assert chi_m3(n) == 1, f"chi({n}) = {chi_m3(n)}, expected +1"

    # n ≡ 1 mod 9 (so DR = 1)
    assert n % 9 == 1, f"n={n} ≢ 1 mod 9"

    # n-1 is sovereign (DR=9)
    assert dr(n1) == 9, f"DR(n-1) = {dr(n1)}, expected 9"

    # Type B: COL2 factors come in pairs (chi product = +1)
    if typ == 'B':
        chi_prod = 1
        for p in fs:
            chi_prod *= chi_m3(p)
        assert chi_prod == 1, f"Type B: chi product of factors ≠ +1 for n={n}"

# Verify 37 mod-condition is equivalent to 37 | n:
# Type B: 4k^2+1 ≡ 0 mod 37 ↔ k ≡ ±3 mod 37
for k_test in range(37):
    if phi4(k_test) % 37 == 0:
        assert k_test in {3, 34}, f"Type B: unexpected k={k_test} with 37|Phi4(2k)"

# Type A: 4k^2+2k+1 ≡ 0 mod 37 ↔ k ≡ 5 or 13 mod 37
for k_test in range(37):
    if phi3(k_test) % 37 == 0:
        assert k_test in {5, 13}, f"Type A: unexpected k={k_test} with 37|Phi3(2k)"

# Type A factors ≡ 1 mod 3 by cyclotomic theory: verify using ord_p(2k)=3
for k in [1152]:
    n = phi3(k)
    fs = KNOWN_FACTORS[n]
    for p in fs:
        assert p % 3 == 1, f"Type A factor {p} not ≡1 mod 3"
        # ord_p(2k) divides p-1 and divides 3 (from Φ₃ theory): ord_p(2k) ∈ {1,3}
        two_k = (2 * k) % p
        cube = pow(two_k, 3, p)
        assert cube == 1, f"(2k)^3 ≢ 1 mod {p}"

# Type B factors ≡ 1 mod 4 by cyclotomic theory: verify ord_p(2k)=4
for typ, k, n in [('B', 108, 46657), ('B', 780, 2433601)]:
    fs = KNOWN_FACTORS[n]
    for p in fs:
        assert p % 4 == 1, f"Type B factor {p} not ≡1 mod 4"
        two_k = (2 * k) % p
        fourth = pow(two_k, 4, p)
        assert fourth == 1, f"(2k)^4 ≢ 1 mod {p}"


if __name__ == "__main__":
    print("CARMICHAEL NUMBERS OF CYCLOTOMIC TYPE DIVISIBLE BY 37")
    print("=" * 60)
    print()
    print("Type A: n = Φ₃(2k) = 4k²+2k+1  (3rd cyclotomic)")
    print("Type B: n = Φ₄(2k) = 4k²+1      (4th cyclotomic)")
    print()
    print("37|n condition:")
    print("  Type B: k ≡ ±3 mod 37  (since k²≡9 mod 37 ↔ 4k²≡36≡-1 mod 37)")
    print("  Type A: k ≡ 5 or 13 mod 37")
    print()
    print(f"{'Typ':4} {'k':>6}  {'n':>10}  {'k mod 37':>8}  {'DR':>2}  {'chi':>4}  Factors")
    print("-" * 70)
    for typ, k, n in DATA:
        fs = KNOWN_FACTORS[n]
        kmod = k % 37
        factors_str = " × ".join(
            f"{p}({'C1' if chi_m3(p)==1 else 'C2'})" for p in fs
        )
        print(f"  {typ}  {k:>6}  {n:>10}  {kmod:>8}  {dr(n):>2}  {chi_m3(n):>+3}  {factors_str}")

    print()
    print("All prime factors of Type B: p ≡ 1 mod 4 (split in Z[i])")
    print("All prime factors of Type A: p ≡ 1 mod 3 (split in Z[ω], ω = e^{2πi/3})")
    print()
    print("All n: DR=1 (COL1, chi=+1), n ≡ 1 mod 9")
    print("Reason: k ≡ 0 or 6 mod 9 → k² ≡ 0 mod 9 → n ≡ 1 mod 9")
    print()
    print("All assertions passed.")
