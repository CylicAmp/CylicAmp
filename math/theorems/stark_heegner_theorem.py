"""
STARK–HEEGNER THEOREM
=====================
There are exactly nine imaginary quadratic fields Q(√d) (d < 0 squarefree)
with class number 1. Their fundamental discriminants are:

    -3, -4, -7, -8, -11, -19, -43, -67, -163.

Historical notes:
  - Heegner (1952): published a proof; contained gaps not fully accepted.
  - Stark (1967): filled the gaps in Heegner's approach.
  - Baker (1966): independent proof via linear forms in logarithms.
  Combined result: Stark–Heegner theorem (also Heegner–Stark–Baker).

DISCRIMINANT STRUCTURE
  Of the nine fundamental discriminants, seven are ≡ 1 (mod 4):
    -3, -7, -11, -19, -43, -67, -163.

  The remaining two are ≡ 0 (mod 4):
    -4, -8.

RABINOWITSCH CORRESPONDENCE
  Rabinowitsch (1913): n²+n+q is prime for all n = 0,...,q-2 if and only if
  Q(√(1-4q)) has class number 1.

  The six discriminants d ≡ 1 (mod 4) for which q = (1-d)/4 is prime are:

    d = -7   ->  q = 2
    d = -11  ->  q = 3
    d = -19  ->  q = 5
    d = -43  ->  q = 11
    d = -67  ->  q = 17
    d = -163 ->  q = 41

  The seventh discriminant ≡ 1 (mod 4) is d = -3, giving q = (1+3)/4 = 1,
  which is not prime. It is correctly excluded from the Rabinowitsch list,
  but the selection criterion is "q prime", not "d ≡ 1 mod 4" alone.

CONSEQUENCE
  Because the Stark–Heegner list is finite and complete, the Rabinowitsch
  primes {2, 3, 5, 11, 17, 41} are also finite and complete. No further
  prime q exists for which n²+n+q is prime throughout 0 ≤ n ≤ q-2.

GF(37) CONNECTIONS
  - 41 ≡ 4 (mod 37): sovereign anchor {4, 9, 25, 30}.
  - f(n) = n²+n+41 ≡ n²+n+4 (mod 37). Discriminant mod 37: -15 ≡ 22.
    Legendre(22, 37) = -1: the prime 37 never divides any value of f(n).
  - The six Rabinowitsch primes mod 37:
      2 mod 37 = 2  (primitive root, ord=36)
      3 mod 37 = 3  (ord=18)
      5 mod 37 = 5
     11 mod 37 = 11
     17 mod 37 = 17
     41 mod 37 = 4  (sovereign anchor — unique among the six)
"""

from sympy import isprime, legendre_symbol


def fundamental_discriminant(d: int) -> bool:
    if d % 4 == 1:
        return True
    if d % 4 == 0 and (d // 4) % 4 in (2, 3):
        return True
    return False


def run_verification() -> bool:
    print("=" * 66)
    print("STARK–HEEGNER THEOREM — VERIFICATION")
    print("=" * 66)

    discs = [-3, -4, -7, -8, -11, -19, -43, -67, -163]

    # All nine are fundamental discriminants
    print("\n--- Nine fundamental discriminants ---")
    for d in discs:
        assert fundamental_discriminant(d), f"{d} is not a fundamental discriminant"
    print(f"  All nine confirmed as fundamental discriminants.")

    # Discriminants ≡ 1 (mod 4)
    print("\n--- Discriminants ≡ 1 (mod 4) ---")
    cong1 = [d for d in discs if d % 4 == 1]
    assert len(cong1) == 7, f"Expected 7, got {len(cong1)}: {cong1}"
    assert -3 in cong1, "-3 must be in the ≡1 mod 4 list"
    print(f"  Count: {len(cong1)}  (seven, not six)")
    print(f"  Values: {cong1}")

    # Discriminants ≡ 0 (mod 4)
    cong0 = [d for d in discs if d % 4 == 0]
    assert cong0 == [-4, -8]
    print(f"  Discriminants ≡ 0 (mod 4): {cong0}")

    # Rabinowitsch correspondence
    print("\n--- Rabinowitsch correspondence q = (1-d)/4 ---")
    rabinowitsch_primes = []
    for d in cong1:
        q = (1 - d) // 4
        prime = isprime(q)
        print(f"  d={d:>5}  ->  q={q:>3}  prime={prime}")
        if prime:
            rabinowitsch_primes.append(q)

    assert rabinowitsch_primes == [2, 3, 5, 11, 17, 41], \
        f"Rabinowitsch primes mismatch: {rabinowitsch_primes}"
    print(f"\n  Rabinowitsch primes: {rabinowitsch_primes}")

    # d=-3 gives q=1, excluded because 1 is not prime
    assert (1 - (-3)) // 4 == 1
    assert not isprime(1)
    print(f"  d=-3 -> q=1 (not prime): correctly excluded from Rabinowitsch list.")

    # Verify each Rabinowitsch prime polynomial
    print("\n--- Polynomial n²+n+q prime for n=0,...,q-2 ---")
    for q in rabinowitsch_primes:
        vals = [n*n + n + q for n in range(q - 1)]
        assert all(isprime(v) for v in vals), \
            f"n²+n+{q} fails primality for some n in 0..{q-2}"
        print(f"  q={q:>3}: n²+n+{q} prime for n=0,...,{q-2}  ✓")

    # GF(37) connections
    print("\n--- GF(37) connections ---")
    assert 41 % 37 == 4
    print(f"  41 mod 37 = {41 % 37}  (sovereign anchor {{4,9,25,30}})")

    f = lambda n: n*n + n + 41
    hits = [n for n in range(37) if f(n) % 37 == 0]
    assert hits == []
    print(f"  f(n) ≡ 0 (mod 37) has no solution: {hits}")

    disc_mod37 = (-163) % 37
    leg = legendre_symbol(-163, 37)
    assert disc_mod37 == 22
    assert leg == -1
    print(f"  -163 mod 37 = {disc_mod37},  Legendre(-163,37) = {leg}")
    print(f"  37 never divides any f(n).  ✓")

    sovereign_anchors = {4, 9, 25, 30}
    only_sovereign = [q for q in rabinowitsch_primes if q % 37 in sovereign_anchors]
    assert only_sovereign == [41]
    print(f"  Only Rabinowitsch prime ≡ sovereign anchor mod 37: {only_sovereign}")

    print()
    print("All assertions passed.")
    return True


if __name__ == "__main__":
    run_verification()
