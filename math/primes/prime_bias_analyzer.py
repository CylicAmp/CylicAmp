"""
Twin Prime Bias Analyzer — GF(37) connections

Chebyshev's bias: twin primes p≡3 (mod 4) outnumber p≡1 (mod 4) at finite limits,
though both densities are asymptotically equal (Hardy-Littlewood).

GF(37) mirror:
  NQR (dark sector) outnumber QR in twin-prime-index sense?
  Mod-37 residues of twin prime pairs cluster in specific orbits:
  Twin primes avoid multiples of 37, so p mod 37 ∈ {1..36}.
  Those residues map through the 137-map f(n) = 26n mod 37.

Specific connection:
  37 is NOT a member of any twin prime pair (37+2=39=3×13, 37-2=35=5×7).
  The nearest twin pair: (41,43). 41 mod 37 = 4 ∈ SA; 43 mod 37 = 6 ∈ TESLA_ORB.
  Second nearest: (29,31). 29 mod 37 = 29; 31 mod 37 = 31.
"""

P = 37
SA = frozenset({4, 9, 25, 30})
TESLA_ORB = frozenset({6, 8, 23})
CB = frozenset({8, 13, 24})


def sieve(limit: int) -> list:
    is_prime = bytearray([1]) * (limit + 1)
    is_prime[0] = is_prime[1] = 0
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = bytearray(len(is_prime[i*i::i]))
    return is_prime


def analyze_twin_primes(limit: int = 1_000_000):
    print(f"  [prime_bias_analyzer]: Running sieve up to {limit:,}...")

    is_prime = sieve(limit)

    twin_count = 0
    mod4 = {1: 0, 3: 0}
    mod37_hits = {n: 0 for n in range(P)}

    for p in range(3, limit - 1, 2):
        if is_prime[p] and is_prime[p + 2]:
            twin_count += 1
            mod4[p % 4] += 1
            mod37_hits[p % P] += 1

    print(f"  [+] Twin prime pairs found: {twin_count:,}")
    print("  [+] Chebyshev bias (mod 4):")
    print(f"      p ≡ 1 (mod 4): {mod4[1]:,}")
    print(f"      p ≡ 3 (mod 4): {mod4[3]:,}")
    bias = mod4[3] - mod4[1]
    print(f"      bias (3 - 1):  {bias:,}  ({'NQR-analog leads' if bias > 0 else 'QR-analog leads'})")

    # GF(37) residue mapping
    sa_hits  = sum(mod37_hits[n] for n in SA)
    tsl_hits = sum(mod37_hits[n] for n in TESLA_ORB)
    cb_hits  = sum(mod37_hits[n] for n in CB)
    print("  [+] GF(37) orbit hits for twin prime residues (p mod 37):")
    print(f"      SA {sorted(SA)}:        {sa_hits:,}")
    print(f"      TESLA_ORB {sorted(TESLA_ORB)}: {tsl_hits:,}")
    print(f"      CB {sorted(CB)}:        {cb_hits:,}")
    print(f"      41 mod 37 = {41 % P} ∈ SA: {41 % P in SA}")
    print(f"      43 mod 37 = {43 % P} ∈ TESLA_ORB: {43 % P in TESLA_ORB}")

    return {
        'twin_count': twin_count,
        'mod4_bias': mod4,
        'mod37_sa': sa_hits,
        'mod37_tesla': tsl_hits,
    }
