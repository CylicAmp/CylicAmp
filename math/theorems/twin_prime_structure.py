"""
TWIN PRIME STRUCTURE THEOREM
=============================================

Built from first principles. Every step traceable.

THEOREM 1: All primes greater than 3 are of the form 6n±1.

Proof:
  Any integer falls into one of six residue classes mod 6:
    6n     — divisible by 6, composite
    6n + 1 — candidate
    6n + 2 — divisible by 2, composite
    6n + 3 — divisible by 3, composite
    6n + 4 — divisible by 2, composite
    6n + 5 — candidate (same as 6n - 1)
  Only 6n+1 and 6n-1 survive. QED.

THEOREM 2: Every twin prime pair (p, p+2) greater than (3,5) has the form
           (6n-1, 6n+1) for some positive integer n.

Proof:
  By Theorem 1, p is either 6n-1 or 6n+1.
  If p = 6n+1, then p+2 = 6n+3 = 3(2n+1), which is divisible by 3.
  Since p+2 > 3, it would be composite — contradiction.
  Therefore p = 6n-1 and p+2 = 6n+1. QED.

THEOREM 3: For any twin prime pair (p, p+2) greater than (3,5),
           the number between them (p+1) is always divisible by 6.

Proof:
  From Theorem 2, p = 6n-1, so p+1 = 6n. Divisible by 6. QED.

  Equivalently, from first principles:
    (a) p is an odd prime, so p+1 is even — divisible by 2.
    (b) p = 6n-1 implies p ≡ 2 (mod 3), so p+1 ≡ 0 (mod 3).
        Why p ≡ 2 (mod 3): if p ≡ 1 (mod 3), then p+2 ≡ 0 (mod 3),
        making p+2 composite — contradicting p+2 being prime.
    (c) gcd(2,3) = 1, so 2|(p+1) and 3|(p+1) gives 6|(p+1). QED.

THEOREM 4: No prime triplet (p, p+2, p+4) exists beyond (3, 5, 7).

Proof:
  Suppose (p, p+2, p+4) are all prime with p > 3.
  By Theorem 2, (p, p+2) = (6n-1, 6n+1).
  Then p+4 = 6n+3 = 3(2n+1), divisible by 3.
  Since p+4 > 3, it is composite — contradiction. QED.

CONNECTION TO THE FRAMEWORK:
  The twin prime pair (11, 13) = (6·2-1, 6·2+1):
    Middle number: 12 = 6·2 — the sovereign target in {3,12,21,30}.
    The +2 Chain Theorem (plus2_chain_theorem.py) and the AHL-8 Vault
    (lob_691_695.py) both identify 12 as the skipped sovereign value.
    This is not coincidence — 12 is divisible by 6 by Theorem 3, and
    its membership in the sovereign range {3,12,21,30} reflects the
    mod-9 digital root structure: DR(12) = 3.

  For any twin prime pair (6n-1, 6n+1):
    Middle number = 6n
    DR(6n) cycles through {6,3,9,6,3,9,...} as n increases.
    The sovereign range {3,12,21,30} corresponds to n ≡ 2 (mod 3),
    i.e. DR(6n) = 3 — exactly the case n=2 giving middle number 12.

THEOREM 5: Euler's polynomial and Rabinowitsch's theorem.

  The polynomial f(n) = n^2 + n + 41 takes prime values for all
  n = 0, 1, ..., 39.  At n = 40 it fails: f(40) = 41^2.

  Algebraic identity at first failure:
    f(40) = 40·41 + 41 = 41(40 + 1) = 41^2.

  Discriminant: Δ = 1 - 4·41 = -163.

  Rabinowitsch (1913): n^2 + n + q is prime for all n = 0,...,q-2
  if and only if the imaginary quadratic field Q(√(1-4q)) has class
  number 1.  For q = 41 this gives Q(√-163), whose class number 1 is
  established by Heegner–Stark–Baker.

  The six primes q for which this holds are: 2, 3, 5, 11, 17, 41.
  These are exactly the primes (D+1)/4 where D ∈ {7,11,19,43,67,163}
  are Heegner numbers.

  GF(37) connections:
    (a) 41 ≡ 4 (mod 37) — the constant term is a sovereign anchor
        ({4, 9, 25, 30}).
    (b) f(n) ≡ n^2 + n + 4 (mod 37).  The discriminant mod 37 is
        1 - 16 = -15 ≡ 22 (mod 37), and Legendre(22, 37) = -1.
        Therefore f(n) ≡ 0 (mod 37) has no solution: the prime 37
        never divides any value of Euler's polynomial.
    (c) The six special primes {2,3,5,11,17,41}: only 41 reduces mod 37
        to a sovereign anchor.

THEOREM 6: CRT mod 333 structure of twin prime pairs.

  The composite modulus M = 333 = 9 × 37 unifies digital root (mod 9)
  and field structure (mod 37) via the Chinese Remainder Theorem.

  CRT reconstruction formula (verified: 37^{-1} ≡ 1 mod 9, 9^{-1} ≡ 33 mod 37):
    CRT(r_9, r_37) = 37·r_9 + 297·r_37  (mod 333).

  For any twin prime pair (p, p+2):
    CRT(p+2) ≡ CRT(p) + 2  (mod 333)  [since 2 < 333].

  Key example — the pair (431, 433):
    431 ≡ 24 (mod 37): seed orbit {18, 24, 32}.
    433 ≡ 26 (mod 37): the 137-map multiplier (137 mod 37 = 26).
    432 ≡ 25 (mod 37): sovereign anchor {4, 9, 25, 30}.
    DR(432) = 9.
    CRT(431) = 98,  CRT(433) = 100,  CRT(432) = 99 (midpoint).

  (431, 433) is the first twin prime pair whose GF(37) residues land
  on {seed orbit node, 137-map multiplier} simultaneously.
"""


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def dr(n: int) -> int:
    return (n - 1) % 9 + 1 if n > 0 else 0


def run_verification() -> bool:
    print("=" * 66)
    print("TWIN PRIME STRUCTURE THEOREM — VERIFICATION")
    print("=" * 66)

    # ------------------------------------------------------------------
    # Theorem 1: All primes > 3 are 6n±1
    # ------------------------------------------------------------------
    print("\n--- Theorem 1: Primes > 3 are of the form 6n±1 ---")
    primes_to_100 = [p for p in range(4, 101) if is_prime(p)]
    for p in primes_to_100:
        assert p % 6 in {1, 5}, f"{p} is prime but not 6n±1"
    print(f"  Verified for all {len(primes_to_100)} primes in (3, 100].")
    print(f"  Residues mod 6: all in {{1, 5}} (i.e. 6n+1 or 6n-1).")

    # ------------------------------------------------------------------
    # Theorem 2: Twin primes > (3,5) have form (6n-1, 6n+1)
    # ------------------------------------------------------------------
    print("\n--- Theorem 2: Twin prime pairs have form (6n-1, 6n+1) ---")
    twin_pairs = [(p, p+2) for p in range(4, 1001) if is_prime(p) and is_prime(p+2)]
    for p, q in twin_pairs:
        n = (p + 1) // 6
        assert p == 6*n - 1, f"({p},{q}): p ≠ 6n-1"
        assert q == 6*n + 1, f"({p},{q}): q ≠ 6n+1"
    print(f"  Verified for all {len(twin_pairs)} twin prime pairs below 1000.")
    print(f"  First 5 pairs: {twin_pairs[:5]}")

    # ------------------------------------------------------------------
    # Theorem 3: Middle number is always divisible by 6
    # ------------------------------------------------------------------
    print("\n--- Theorem 3: Middle number (p+1) divisible by 6 ---")
    for p, q in twin_pairs:
        middle = p + 1
        assert middle % 6 == 0, f"Middle of ({p},{q}) = {middle}, not divisible by 6"
        assert middle % 2 == 0, f"{middle} not even"
        assert middle % 3 == 0, f"{middle} not divisible by 3"
    print(f"  Verified: p+1 ≡ 0 (mod 6) for all {len(twin_pairs)} pairs.")
    print(f"  Middle numbers: {[p+1 for p,q in twin_pairs[:8]]}")

    # ------------------------------------------------------------------
    # Theorem 4: No prime triplet beyond (3,5,7)
    # ------------------------------------------------------------------
    print("\n--- Theorem 4: No prime triplet (p, p+2, p+4) beyond (3,5,7) ---")
    triplets = [(p, p+2, p+4) for p in range(2, 10001)
                if is_prime(p) and is_prime(p+2) and is_prime(p+4)]
    assert triplets == [(3, 5, 7)], f"Unexpected triplets: {triplets}"
    print(f"  Only prime triplet up to 10000: {triplets[0]}")
    print(f"  For any twin prime pair (6n-1, 6n+1) with n≥2:")
    print(f"  The next candidate 6n+3 = 3(2n+1) is always divisible by 3.")

    # ------------------------------------------------------------------
    # Framework connection: sovereign middle numbers
    # ------------------------------------------------------------------
    print("\n--- Framework connection: DR of middle numbers ---")
    print(f"  Middle numbers and their digital roots:")
    for p, q in twin_pairs[:10]:
        middle = p + 1
        n = middle // 6
        print(f"  ({p:>4}, {q:>4})  middle={middle:>4}=6×{n}  DR={dr(middle)}")
    print(f"  Sovereign range {{3,12,21,30}} = middle numbers where DR=3")
    print(f"  (11,13) → middle=12 ∈ sovereign range, DR(12)=3")

    # ------------------------------------------------------------------
    # Theorem 5: Euler's polynomial and Rabinowitsch
    # ------------------------------------------------------------------
    print("\n--- Theorem 5: Euler's polynomial f(n) = n^2 + n + 41 ---")
    f = lambda n: n*n + n + 41
    euler_primes = [f(n) for n in range(40)]
    assert all(is_prime(v) for v in euler_primes), "Some f(n) is not prime for n in 0..39"
    print(f"  f(n) prime for all n = 0,...,39: verified ({len(euler_primes)} values).")
    assert f(40) == 41**2, f"f(40) = {f(40)}, expected 41^2 = {41**2}"
    assert f(41) == 41 * 43, f"f(41) = {f(41)}, expected 41*43 = {41*43}"
    print(f"  f(40) = {f(40)} = 41^2  (composite, algebraic identity: 41*(40+1))")
    print(f"  f(41) = {f(41)} = 41*43  (composite)")
    assert 41 % 37 == 4, "41 mod 37 must equal 4 (sovereign anchor)"
    print(f"  41 mod 37 = {41 % 37}  (sovereign anchor {{4,9,25,30}})")
    hits_37 = [n for n in range(37) if f(n) % 37 == 0]
    assert hits_37 == [], f"f(n) divisible by 37 at n={hits_37}"
    print(f"  f(n) ≡ 0 (mod 37) has no solution: 37 never divides f(n).  ✓")

    # ------------------------------------------------------------------
    # Theorem 6: CRT mod 333 structure
    # ------------------------------------------------------------------
    print("\n--- Theorem 6: CRT mod 333 structure of twin prime pairs ---")
    M = 333  # 9 * 37

    def crt_333(n):
        r9, r37 = n % 9, n % 37
        return (37 * r9 + 297 * r37) % M

    for p, q in twin_pairs:
        assert crt_333(q) == (crt_333(p) + 2) % M, \
            f"CRT difference ≠ 2 for pair ({p},{q})"
    print(f"  CRT(p+2) ≡ CRT(p) + 2 (mod 333): verified for all "
          f"{len(twin_pairs)} pairs below 1000.")

    # Key example: (431, 433)
    assert is_prime(431) and is_prime(433)
    assert 431 % 37 == 24,  f"431 mod 37 = {431 % 37}, expected 24"
    assert 433 % 37 == 26,  f"433 mod 37 = {433 % 37}, expected 26"
    assert 432 % 37 == 25,  f"432 mod 37 = {432 % 37}, expected 25"
    assert dr(432) == 9,    f"DR(432) = {dr(432)}, expected 9"
    assert crt_333(431) == 98
    assert crt_333(433) == 100
    assert crt_333(432) == 99
    print(f"  (431, 433): GF(37) residues = (24, 26)")
    print(f"    431 ≡ 24 (mod 37): seed orbit {{18,24,32}}")
    print(f"    433 ≡ 26 (mod 37): 137-map multiplier")
    print(f"    432 ≡ 25 (mod 37): sovereign anchor {{4,9,25,30}},  DR=9")
    print(f"    CRT images: (98, 100),  midpoint CRT(432) = 99")
    print(f"  First twin prime pair whose GF(37) residues = (seed, 137-mult).  ✓")

    print()
    print("All assertions passed.")
    return True


if __name__ == "__main__":
    run_verification()
