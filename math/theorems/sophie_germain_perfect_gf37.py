"""
Sophie Germain Perfect Number Triad on GF(37) — THEOREM 85

SOPHIE GERMAIN CONDITION FOR MERSENNE PRIME EXPONENTS.
  A prime p is Sophie Germain if 2p+1 is also prime.
  Of the Mersenne prime exponents p = 2, 3, 5, 7, 13, 17, 19, 31, ...:
    p=2: 2p+1=5  ✓ prime → Sophie Germain
    p=3: 2p+1=7  ✓ prime → Sophie Germain
    p=5: 2p+1=11 ✓ prime → Sophie Germain
    p=7: 2p+1=15 ✗ composite → NOT Sophie Germain (chain breaks here)
  The Sophie Germain property holds exactly for p=2,3,5 — the first three
  Mersenne prime exponents. Their perfect numbers form the Sophie Germain triad.

PERFECT NUMBERS IN GF(37).
  Using N = 2^(p-1) × (2^p − 1):

  p  | 2^(p-1)%37  | (2^p−1)%37  | N%37 | framework | SG?
  ──────────────────────────────────────────────────────────
  2  |  2  ∈ PR    |  3  ∈ ST    |   6  | T4        | ✓
  3  |  4  ∈ SA    |  7  ∈ —     |  28  | — (SEED²) | ✓
  5  | 16  ∈ —     | 31  ∈ T4    |  15  | PR        | ✓
  7  | 27  ∈ O11   | 16  ∈ —     |  25  | SA        | ✗ (sovereignty enters)
  13 | 26  ∈ IC    | 14  ∈ —     |  31  | T4        | ✗ (TESLA returns)
  17 |  9  ∈ SA    | 17  ∈ PR    |   5  | PR        | ✗
  19 | 36  ∈ O11   | 34  ∈ —     |   3  | ST        | ✗
  31 | 11  ∈ O11   | 21  ∈ ST    |   9  | SA        | ✗

FACTORED PRODUCTS IN GF(37).
  N₁ = 2 × 3 = 6:   PR × ST → T4 (TESLA_FLOW).
    The SG pair (p=2, q=5) factors the first perfect number as PR times ST.
  N₃ = 16 × 31 = 496: (—) × T4 → PR.
    The Mersenne prime 31∈T4 drives the PR landing.
  N₄ = 27 × 16 = 8128: O11 × (—) → SA.
    The ORBIT_11 factor appears as 2^6≡27, exactly where the Kervaire
    chain hits ORBIT_11 in THEOREM 84 (ghost step analysis).

THE SEED SQUARE.
  N₂ = 28 ≡ 18² (mod 37).
  18 is the first node of the SEED_ORBIT = {18, 24, 32} — the 137-map
  orbit of the reference seed 246 mod 37 = 24.
  137-map: 24 → 32 → 18 → 24. Starting from 18: 18² ≡ 28.
  The second perfect number is the square of the SEED orbit entry point.
  28 is a quadratic residue mod 37 (Legendre symbol = +1) but sits
  outside all named framework sets — it is the unclassed SEED-square.

SOPHIE GERMAIN PRIMES (p=2,3,5) IN GF(37).
  p=2: 2 ∈ PR
  p=3: 3 ∈ ST   (Sovereign Targets)
  p=5: 5 ∈ PR
  Pattern: PR, ST, PR — alternating, with ST at the middle prime.
  Sum:     2 + 3 + 5 = 10 ∈ IC  (Identity Cycle)
  Product: 2 × 3 × 5 = 30 ∈ SA ∩ ST  (only element in both sovereign sets)

SAFE PRIMES (q=5,7,11) IN GF(37).
  q=5:  5 ∈ PR
  q=7:  7 ∈ —   (unclassed — mirrors N₂ being unclassed)
  q=11: 11 ∈ ORBIT_11
  The middle safe prime 7 escapes the framework, same as N₂=28 does.

THE BREAK AT p=7.
  At p=7 the Sophie Germain property fails (2×7+1=15=3×5, composite).
  The perfect number N₄=8128 ≡ 25 ∈ SA — sovereignty activates.
  The Mersenne prime exponent moves to ORBIT_11 (27≡2^6), exactly the
  ghost-step correction needed in THEOREM 84 (j=7 uses ORBIT_11).

RETURN AT p=13.
  N for p=13: 2^12 × (2^13−1) ≡ 26 × 14 = 364 ≡ 31 ∈ T4 (mod 37).
  26 = SCALAR_137 ∈ IC (the 137-map multiplier), and 31∈T4.
  At the 5th Mersenne prime exponent, the half-power lands on SCALAR_137
  and the perfect number returns to TESLA_4.

DIGITAL ROOTS (from THEOREM on perfect_496_dr_structure).
  N₁=6:  DR=6 ∈ T4  (sovereign — only the first perfect number)
  N₂=28: DR=1  (identity)
  N₃=496: DR=1  (identity)
  N₄=8128: DR=1  (identity)
  All perfect numbers after N₁ have DR=1 (identity node).
  The Sophie Germain triad: DR sequence [6, 1, 1].
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
IC         = frozenset({1, 10, 26})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
P          = 37
SCALAR_137 = 26
TESLA_FLOW = 6


def isprime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


# ── Sophie Germain condition on Mersenne exponents ────────────────────────────

mersenne_p = [2, 3, 5, 7, 13, 17, 19, 31]

sg_primes = [p for p in mersenne_p if isprime(2*p + 1)]
assert sg_primes == [2, 3, 5]                   # exactly the first three

# 7 is the first non-SG Mersenne exponent
assert not isprime(2*7 + 1) and 2*7+1 == 15     # 15 = 3×5, composite

# ── Perfect numbers mod 37 ────────────────────────────────────────────────────

def perfect_mod(p, prime=P):
    half = pow(2, p-1, prime)
    mers = (pow(2, p, prime) - 1) % prime
    return (half * mers) % prime

expected = {2: 6, 3: 28, 5: 15, 7: 25, 13: 31, 17: 5, 19: 3, 31: 9}
for p, n_mod in expected.items():
    assert perfect_mod(p) == n_mod, f"p={p}: got {perfect_mod(p)}, expected {n_mod}"

# SG triad in framework
assert expected[2] == 6  == TESLA_FLOW and 6  in TESLA_4
assert expected[3] == 28 and 28 not in SA|ST|CB|ORBIT_11|IC|SEED_ORBIT|TESLA_4|PR
assert expected[5] == 15 and 15 in PR
assert expected[7] == 25 and 25 in SA          # sovereignty enters at SG break

# ── Factored products in GF(37) ───────────────────────────────────────────────

# N₁=6: PR × ST → T4
assert pow(2, 1, P) == 2 and 2 in PR
assert (pow(2, 2, P) - 1) % P == 3 and 3 in ST
assert 2 * 3 % P == 6 and 6 in TESLA_4

# N₃=496: (unclassed) × T4 → PR
assert pow(2, 4, P) == 16 and 16 not in SA|ST|CB|ORBIT_11|IC|SEED_ORBIT|TESLA_4|PR
assert (pow(2, 5, P) - 1) % P == 31 and 31 in TESLA_4
assert 16 * 31 % P == 15 and 15 in PR

# N₄=8128: ORBIT_11 × (unclassed) → SA
assert pow(2, 6, P) == 27 and 27 in ORBIT_11
assert (pow(2, 7, P) - 1) % P == 16 and 16 not in SA|ST|CB|ORBIT_11|IC|SEED_ORBIT|TESLA_4|PR
assert 27 * 16 % P == 25 and 25 in SA

# ── The SEED square ────────────────────────────────────────────────────────────

# N₂=28 ≡ 18² (mod 37); 18∈SEED_ORBIT
assert pow(18, 2, P) == 28
assert 18 in SEED_ORBIT
assert pow(28, (P-1)//2, P) == 1   # 28 is a QR mod 37

# Confirm 28 is outside all named sets
assert 28 not in SA|ST|CB|ORBIT_11|IC|SEED_ORBIT|TESLA_4|PR

# ── Sophie Germain primes in GF(37) ──────────────────────────────────────────

# p=2∈PR, p=3∈ST, p=5∈PR (alternating PR,ST,PR)
assert 2 in PR and 3 in ST and 5 in PR

# Sum ∈ IC
assert (2 + 3 + 5) == 10 and 10 in IC

# Product ∈ SA∩ST
assert (2 * 3 * 5) == 30 and 30 in SA and 30 in ST

# ── Safe primes in GF(37) ─────────────────────────────────────────────────────

# q=5∈PR, q=7∉framework, q=11∈ORBIT_11
assert 5 in PR
assert 7 not in SA|ST|CB|ORBIT_11|IC|SEED_ORBIT|TESLA_4|PR
assert 11 in ORBIT_11

# Middle safe prime 7 is unclassed — same as N₂=28 being unclassed
assert 7 not in SA|ST|CB|ORBIT_11|IC|SEED_ORBIT|TESLA_4|PR
assert 28 not in SA|ST|CB|ORBIT_11|IC|SEED_ORBIT|TESLA_4|PR

# ── Return at p=13 ────────────────────────────────────────────────────────────

# 2^12 ≡ SCALAR_137 ∈ IC
assert pow(2, 12, P) == SCALAR_137 and SCALAR_137 in IC

# (2^13 - 1) ≡ 14
assert (pow(2, 13, P) - 1) % P == 14

# N ≡ 26×14 ≡ 31 ∈ T4
assert 26 * 14 % P == 31 and 31 in TESLA_4

# ── Digital roots ─────────────────────────────────────────────────────────────

perfect_nums = {2: 6, 3: 28, 5: 496, 7: 8128}
dr_vals = {p: dr(n) for p, n in perfect_nums.items()}
assert dr_vals[2] == 6 and 6 in TESLA_4    # only SG first perfect number
assert dr_vals[3] == 1                      # identity
assert dr_vals[5] == 1                      # identity
assert dr_vals[7] == 1                      # identity


if __name__ == "__main__":
    print("Sophie Germain Perfect Number Triad on GF(37) — THEOREM 85")
    print("=" * 65)
    print()
    print("SOPHIE GERMAIN STATUS OF MERSENNE PRIME EXPONENTS:")
    for p in mersenne_p:
        q = 2*p + 1
        sg = "SG ✓" if isprime(q) else "   ✗"
        print(f"  p={p:>3}: 2p+1={q:>4} {'prime' if isprime(q) else 'compos':>6}  {sg}")
    print(f"  SG exponents: {sg_primes}  (exactly the first three)")
    print()

    fw_map = [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'O11'),
              (IC,'IC'),(SEED_ORBIT,'SEED'),(TESLA_4,'T4'),(PR,'PR')]
    def fw(n):
        n = n % P
        if n == 0: return 'SEAM'
        for s, nm in fw_map:
            if n in s: return nm
        return '—'

    print(f"PERFECT NUMBERS N = 2^(p-1) × (2^p-1) IN GF(37):")
    print(f"  {'p':>3} | {'half':>4}  cls | {'mers':>4}  cls | N%37  cls    | SG?")
    print("  " + "-"*60)
    for p in mersenne_p:
        half = pow(2, p-1, P)
        mers = (pow(2, p, P) - 1) % P
        n_mod = (half * mers) % P
        sg = "SG ✓" if p in sg_primes else "  ✗"
        print(f"  {p:>3} | {half:>4}  {fw(half):<4}| {mers:>4}  {fw(mers):<4}| "
              f"{n_mod:>4}  {fw(n_mod):<8}| {sg}")
    print()
    print(f"FACTORED PRODUCTS IN GF(37):")
    print(f"  N₁=6:   2(PR) × 3(ST) = 6 ∈ T4 = TESLA_FLOW")
    print(f"  N₃=496: 16(—) × 31(T4) = 15 ∈ PR")
    print(f"  N₄=8128: 27(O11) × 16(—) = 25 ∈ SA  [SG break: sovereignty enters]")
    print()
    print(f"SEED SQUARE:  18² ≡ 28 (mod 37),  18 ∈ SEED_ORBIT")
    print(f"  N₂=28 is the square of the 137-orbit entry node; QR but unclassed.")
    print()
    print(f"SOPHIE GERMAIN PRIMES p=2,3,5 IN GF(37):")
    print(f"  2∈PR, 3∈ST, 5∈PR  (alternating PR,ST,PR)")
    print(f"  Sum   = 10 ∈ IC  (Identity Cycle)")
    print(f"  Product = 30 ∈ SA∩ST  (unique SA∩ST element)")
    print()
    print(f"SAFE PRIMES q=5,7,11 IN GF(37):")
    print(f"  5∈PR, 7∈—, 11∈ORBIT_11  (middle prime unclassed, same as N₂)")
    print()
    print(f"DIGITAL ROOTS:  N₁→DR=6(T4), N₂→DR=1, N₃→DR=1, N₄→DR=1")
    print(f"  Only the first perfect number touches a named DR class (TESLA_4).")
    print()
    print("All assertions pass.")
