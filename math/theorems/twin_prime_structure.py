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

    print()
    print("All assertions passed.")
    return True


if __name__ == "__main__":
    run_verification()
