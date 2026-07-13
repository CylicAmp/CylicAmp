"""
Euler's Totient Function φ(n).

φ(n) counts the positive integers up to n that are relatively prime to n.
i.e. the count of k in [1..n] where gcd(k, n) = 1.

Key properties:
  - Prime p:          φ(p) = p − 1
  - Prime power p^k:  φ(p^k) = p^k − p^(k−1)
  - Multiplicative:   φ(mn) = φ(m)φ(n)  when gcd(m,n) = 1
  - General formula:  φ(n) = n ∏_{p|n} (1 − 1/p)

φ(37) = 36  — the 37-field has 36 non-zero residues (37 is prime).

RSA connection:
  n = p·q  →  φ(n) = (p−1)(q−1)
  Private key d = e⁻¹ mod φ(n)
"""

import math
import sympy


def totient_table(start: int = 1, end: int = 40) -> list:
    """Return list of (n, φ(n)) for n in [start, end]."""
    return [(n, sympy.totient(n)) for n in range(start, end + 1)]


def totient_values(start: int = 1, end: int = 40) -> list:
    """Return φ(n) values only, for n in [start, end]."""
    return [sympy.totient(n) for n in range(start, end + 1)]


def demonstrate() -> None:
    table = totient_table(1, 40)
    values = [phi for _, phi in table]

    print("=" * 56)
    print("  EULER'S TOTIENT FUNCTION φ(n) — n = 1 to 40")
    print("=" * 56)

    # Per-line output
    for n, phi in table:
        marker = ""
        if sympy.isprime(n):
            marker = f"  (prime: φ = n−1 = {n-1})"
        print(f"  φ({n:2d}) = {int(phi):2d}{marker}")

    print()
    print(f"Values list: {values}")

    # Key structural notes
    print()
    print("Key values:")
    print(f"  φ(37) = {sympy.totient(37)}  — 37 is prime; 36 non-zero residues in the 37-field")
    print(f"  sum φ(1..36) = {sum(sympy.totient(n) for n in range(1, 37))}")
    print(f"  φ(36) = {sympy.totient(36)}   — 12 coprimes to 36")

    # Verify multiplicativity example
    print()
    print("Multiplicativity checks (gcd(m,n)=1 → φ(mn)=φ(m)φ(n)):")
    for m, n in [(3, 5), (4, 9), (7, 8)]:
        lhs = int(sympy.totient(m * n))
        rhs = int(sympy.totient(m)) * int(sympy.totient(n))
        print(f"  φ({m}×{n}) = φ({m*n}) = {lhs}  |  φ({m})×φ({n}) = {rhs}  {'✓' if lhs == rhs else '✗'}")


def totient_product_formula(n: int) -> int:
    """
    Compute φ(n) using the product formula without sympy:
      φ(n) = n · ∏_{p|n} (1 − 1/p)
    """
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def rsa_demo(p: int = 61, q: int = 53) -> None:
    """
    Demonstrate RSA key generation using φ(n) = (p−1)(q−1).

    Steps:
      1. n = p·q
      2. φ(n) = (p−1)(q−1)
      3. Choose public exponent e coprime to φ(n)
      4. Private key d = e⁻¹ mod φ(n)
    """
    print("\n--- RSA Key Generation Demo ---")
    print(f"  Primes: p={p}, q={q}")
    n = p * q
    phi_n = (p - 1) * (q - 1)
    print(f"  n = p·q = {n}")
    print(f"  φ(n) = (p−1)(q−1) = {p-1}·{q-1} = {phi_n}")

    # Choose e: common choice is 65537; find smallest valid e otherwise
    for e_candidate in [65537, 17, 13, 7, 5, 3]:
        if math.gcd(e_candidate, phi_n) == 1:
            e = e_candidate
            break

    d = pow(e, -1, phi_n)
    print(f"  Public key:  (e={e}, n={n})")
    print(f"  Private key: (d={d}, n={n})")

    # Verify: e·d ≡ 1 (mod φ(n))
    check = (e * d) % phi_n
    print(f"  Verify e·d mod φ(n) = {check} (should be 1): {'✓' if check == 1 else '✗'}")

    # Mini encrypt/decrypt
    m = 42
    c = pow(m, e, n)
    m2 = pow(c, d, n)
    print(f"  Encrypt m={m}: c = m^e mod n = {c}")
    print(f"  Decrypt c={c}: m = c^d mod n = {m2}  {'✓' if m2 == m else '✗'}")


if __name__ == "__main__":
    demonstrate()

    # Product formula cross-check
    print("\n--- Product formula vs sympy cross-check ---")
    mismatches = []
    for n in range(1, 41):
        pf = totient_product_formula(n)
        sp = int(sympy.totient(n))
        if pf != sp:
            mismatches.append((n, pf, sp))
    if mismatches:
        for n, pf, sp in mismatches:
            print(f"  MISMATCH φ({n}): product={pf}, sympy={sp}")
    else:
        print("  All φ(1..40) match between product formula and sympy ✓")

    rsa_demo()
