"""
THE GOLDILOCKS PRIME: p = 2^64 - 2^32 + 1
=========================================================================

p = 0xffffffff00000001 = 18,446,744,069,414,584,321

This prime is used in real ZK proof systems (Plonky2, Starky) because:
1. Arithmetic mod p fits in 64-bit registers with cheap reduction
2. p - 1 = 2^32 × (3 × 5 × 17 × 257 × 65537), so NTT up to size 2^32
3. The odd factor 3 × 5 × 17 × 257 × 65537 = product of Fermat primes F1–F4

Connection to this framework: the same structure of "multiplicative group
with primitive roots enabling large orbits" applies here as in (Z/37Z)*.
- ord_37(2) = 36 = φ(37): 2 generates (Z/37Z)* of size 36
- For Goldilocks: any primitive root mod p generates (Z/pZ)* of size p-1

Verified facts:
- p is prime (Miller-Rabin, deterministic witnesses)
- p-1 = 2^32 × 3 × 5 × F2 × F3 × F4 where Fi = 2^(2^i) + 1
- v_2(p-1) = 32 → NTT (number-theoretic transform) supports size 2^32
- INT16 lookup table: 65536 entries × 4 bytes = 256 KB
"""


P = 2**64 - 2**32 + 1


# =============================================================================
# Primality
# =============================================================================

def miller_rabin(n, a):
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(r - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
    return False


def is_prime_deterministic(n):
    """Deterministic Miller-Rabin for n < 3.3 × 10^24 using 12 witnesses."""
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    return all(miller_rabin(n, a) for a in witnesses)


# =============================================================================
# Factorization of p-1
# =============================================================================

FERMAT_PRIMES = {
    "F1": 5,       # 2^2 + 1
    "F2": 17,      # 2^4 + 1
    "F3": 257,     # 2^8 + 1
    "F4": 65537,   # 2^16 + 1
}

def verify_pm1_factorization():
    """
    p-1 = 2^32 × 3 × 5 × 17 × 257 × 65537
         = 2^32 × 3 × F1 × F2 × F3 × F4
    Note: F0=3=2^1+1 is not a Fermat prime (not a power of 2 exponent),
    but F1=5, F2=17, F3=257, F4=65537 are.
    """
    product = 2**32 * 3 * 5 * 17 * 257 * 65537
    return product == P - 1


def two_adic_valuation(n):
    """Return v such that 2^v | n but 2^(v+1) does not."""
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v


# =============================================================================
# NTT (Number-Theoretic Transform) structure
# =============================================================================

def ntt_max_size():
    """Max NTT size = largest power of 2 dividing p-1."""
    return 2 ** two_adic_valuation(P - 1)


def ntt_generator():
    """Find a primitive 2^32-th root of unity mod p."""
    # Any primitive root g mod p gives g^((p-1)/2^32) as a 2^32-th root of unity.
    # We search for the smallest generator.
    odd_part = (P - 1) >> 32
    for g in range(2, P):
        # Check g is a primitive root: g^((p-1)/q) != 1 for each prime q | p-1
        primes = [2, 3, 5, 17, 257, 65537]
        if all(pow(g, (P - 1) // q, P) != 1 for q in primes):
            omega = pow(g, odd_part, P)
            return g, omega
    return None, None


# =============================================================================
# Lookup table size (INT16 activation tables for ZK-ML)
# =============================================================================

def lookup_table_stats():
    """
    An INT16 lookup table for an activation function (softmax, GeLU, etc.)
    maps each of the 2^16 possible INT16 inputs to a single INT16 output.
    Each entry is 4 bytes (2-byte key + 2-byte value).
    """
    entries = 2**16
    bytes_per_entry = 4
    total_bytes = entries * bytes_per_entry
    return {
        "entries":       entries,
        "bytes_per_entry": bytes_per_entry,
        "total_bytes":   total_bytes,
        "total_kb":      total_bytes // 1024,
    }


# =============================================================================
# Connection to mod-37 framework
# =============================================================================

def goldilocks_mod37():
    """
    Goldilocks prime p mod 37 and its relation to the mod-37 orbit work.
    Not a deep connection — just documenting the residue.
    """
    return {
        "p mod 37":   P % 37,
        "(p-1) mod 37": (P - 1) % 37,
        "note": "No structural relation to ord_37(2)=36; both involve"
                " primitive roots but in independent settings.",
    }


# =============================================================================
# Summary
# =============================================================================

def summarise():
    print("=" * 60)
    print("GOLDILOCKS PRIME: p = 2^64 - 2^32 + 1")
    print("=" * 60)

    print(f"\np = {P:,}")
    print(f"p = {hex(P)}")
    print(f"is_prime: {is_prime_deterministic(P)}")

    print(f"\np-1 = 2^32 × 3 × 5 × 17 × 257 × 65537:")
    print(f"  factorization correct: {verify_pm1_factorization()}")
    print(f"  17 = F2 = 2^4+1: {17 == 2**4+1}")
    print(f"  257 = F3 = 2^8+1: {257 == 2**8+1}")
    print(f"  65537 = F4 = 2^16+1: {65537 == 2**16+1}")

    v = two_adic_valuation(P - 1)
    print(f"\n2-adic valuation v_2(p-1) = {v}")
    print(f"Max NTT size = 2^{v} = {ntt_max_size():,}")
    print(f"2^32 | (p-1): {(P-1) % 2**32 == 0}")
    print(f"2^33 | (p-1): {(P-1) % 2**33 == 0}")

    g, omega = ntt_generator()
    print(f"\nSmallest primitive root mod p: {g}")
    print(f"2^32-th root of unity: {g}^((p-1)/2^32) mod p = {omega}")
    print(f"  omega^(2^32) mod p = 1: {pow(omega, 2**32, P) == 1}")
    print(f"  omega^(2^31) mod p = {pow(omega, 2**31, P)}  (should be ≠ 1)")

    stats = lookup_table_stats()
    print(f"\nINT16 lookup table stats:")
    print(f"  entries:    {stats['entries']:,}  (= 2^16)")
    print(f"  bytes/entry: {stats['bytes_per_entry']}")
    print(f"  total:      {stats['total_kb']} KB per table")
    print(f"  24 tables:  {24 * stats['total_kb']} KB = {24 * stats['total_kb'] // 1024} MB")

    m37 = goldilocks_mod37()
    print(f"\nMod-37 residues (connection to orbit framework):")
    print(f"  p mod 37 = {m37['p mod 37']}")
    print(f"  (p-1) mod 37 = {m37['(p-1) mod 37']}")
    print(f"  {m37['note']}")


def run_assertions():
    assert is_prime_deterministic(P), "Goldilocks prime p = 2^64 - 2^32 + 1 must be prime"
    assert verify_pm1_factorization(), \
        "p-1 must factor as 2^32 × 3 × 5 × 17 × 257 × 65537"
    assert two_adic_valuation(P - 1) == 32, \
        f"v_2(p-1) = {two_adic_valuation(P-1)}, expected 32"

    from math import prod
    assert 3 * 5 * 17 * 257 * 65537 == prod(FERMAT_PRIMES.values()) * 3

    # Primitive root g=7
    def is_prim_root_goldilocks(g):
        pm1 = P - 1
        for q in {2, 3, 5, 17, 257, 65537}:
            if pow(g, pm1 // q, P) == 1:
                return False
        return True
    assert is_prim_root_goldilocks(7), "7 must be a primitive root mod Goldilocks prime"

    # Fermat prime identities
    for name, val in FERMAT_PRIMES.items():
        exp = 2 ** (2 ** (["F1","F2","F3","F4"].index(name) + 1))
        assert val == exp + 1, f"{name} = {val}, expected {exp}+1"


if __name__ == "__main__":
    run_assertions()
    summarise()
