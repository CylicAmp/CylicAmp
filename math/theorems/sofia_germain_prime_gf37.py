"""
Sofia Germain Prime in GF(37) — THEOREM 69

THE PRIME:  p = 2618163402417 × 2^1290000 − 1  (largest known Sofia Germain prime)
            q = 2p + 1                            (safe prime; ~388,342 digits)

THE KEY FACT: p ≡ SCALAR_137 = 26 mod 37 — the prime itself sits at the 137-map
multiplier position in GF(37).
One-line reason: ORBIT_11 × SCALAR_137 − 1 ≡ SCALAR_137 (11×26−1=285≡26 mod 37).

HAND-CHECKABLE:
  k = 2618163402417 ≡ 11 mod 37           (ORBIT_11)
  n = 1290000;  n mod 36 = 12;  2^12 ≡ 26 mod 37   (= SCALAR_137 ∈ IC)
  k × 2^n ≡ 11 × 26 = 286 ≡ 27 mod 37
  p ≡ 27 − 1 = 26 mod 37                 (= SCALAR_137 ∈ IDENTITY_CYCLE)
  q ≡ 2 × 26 + 1 = 53 ≡ 16 mod 37       (∈ O2 = {9,12,16}, sovereign orbit 2)

ORBIT CHAIN (mod 37):
  k ∈ ORBIT_11    ×   2^n ∈ IC(SCALAR_137)   − 1  →  p ∈ IC(SCALAR_137)
  p ∈ IC          ×2  +1                       →  q ∈ O2

  Fixed point: the 137-map multiplier multiplies by itself (ORBIT_11 × IC → IC).

CONNECTIONS TO THE FRAMEWORK:
  • 2^1290000 ≡ 26 = SCALAR_137 ∈ IC: the power-of-2 in the prime formula is
    EXACTLY the 137-map multiplier. Because ord₃₇(2)=36 and 1290000 mod 36=12,
    and 2^12 ≡ 26 mod 37.
  • p ≡ 26 = SCALAR_137: the prime ITSELF is the 137-map multiplier mod 37.
    The world-record Sophie Germain prime is fixed at the most fundamental
    constant in GF(37).
  • q ≡ 16 ∈ O2 = {9,12,16}: the safe prime lands in the second sovereign orbit,
    the orbit of the sovereign targets minus the SA∩ST pivot.
  • n mod 37 = 1290000 mod 37: let's compute — 1290000/37 = 34864.8...,
    34864×37=1289968, 1290000-1289968=32 → n mod 37 = 32 ∈ SEED_ORBIT!
  • DR(p) = DR(q) = 8 ∈ CB: both prime and safe prime share digital root in CB.

DIGITAL ROOT:
  k ≡ 0 mod 9  (digit sum = 45)
  2^1290000 ≡ 1 mod 9  (period 6; 1290000 mod 6 = 0; 2^0 = 1)
  k × 2^n ≡ 0 mod 9  →  p ≡ −1 ≡ 8 mod 9  →  DR(p) = 8 ∈ CB
  q = 2p+1 ≡ 17 ≡ 8 mod 9  →  DR(q) = 8 ∈ CB
"""

# ── Constants ──────────────────────────────────────────────────────────────────

SA             = frozenset({4, 9, 25, 30})
ST             = frozenset({3, 12, 21, 30})
CB             = frozenset({8, 13, 24})
ORBIT_11       = frozenset({11, 27, 36})
SEED_ORBIT     = frozenset({18, 24, 32})
IDENTITY_CYCLE = frozenset({1, 10, 26})
O2             = frozenset({9, 12, 16})
SCALAR_137     = 26


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


# ── PRIME PARAMETERS ─────────────────────────────────────────────────────────

k = 2618163402417   # coefficient
n = 1290000         # exponent  (NOT 21290 — that form is composite)

k37    = k % 37
n36    = n % 36     # ord₃₇(2) = 36
pow2n  = pow(2, n, 37)


# ── KEY CHECKS ────────────────────────────────────────────────────────────────

# Coefficient ∈ ORBIT_11
assert k37 == 11 and 11 in ORBIT_11

# Exponent: 1290000 mod 36 = 12; 2^12 ≡ 26 = SCALAR_137 ∈ IC
assert n36 == 12
assert pow2n == SCALAR_137 and SCALAR_137 in IDENTITY_CYCLE

# n mod 37 ∈ SEED_ORBIT
assert n % 37 == 32 and 32 in SEED_ORBIT

# k × 2^n ≡ 11 × 26 = 286 ≡ 27 mod 37
kpow = (k37 * pow2n) % 37
assert kpow == 27

# p ≡ SCALAR_137 ∈ IC  — the prime is the 137-map multiplier mod 37
p37 = (kpow - 1) % 37
assert p37 == SCALAR_137 and SCALAR_137 in IDENTITY_CYCLE

# Hand-check: 11×26 = 286; 286 mod 37 = 286 − 7×37 = 286 − 259 = 27; 27−1=26=SCALAR_137
assert 11 * 26 == 286 and 286 % 37 == 27 and 27 - 1 == 26

# Safe prime q ≡ 16 ∈ O2
q37 = (2 * p37 + 1) % 37
assert q37 == 16 and 16 in O2

# DR of p and q (via mod 9 arithmetic)
k9       = sum(int(d) for d in str(k)) % 9   # digit sum 45 ≡ 0 mod 9
pow2n_9  = pow(2, n, 9)                       # 2^1290000 mod 9
p9       = (k9 * pow2n_9 - 1) % 9
q9       = (2 * p9 + 1) % 9

assert k9 == 0              # digit sum 45
assert n % 6 == 0           # 1290000 divisible by 6 → 2^n ≡ 1 mod 9
assert pow2n_9 == 1
assert p9 == 8 and 8 in CB  # DR(p) = 8 ∈ CB
assert q9 == 8 and 8 in CB  # DR(q) = 8 ∈ CB

# n mod 37 = 32 ∈ SEED_ORBIT
assert n % 37 == 32 and 32 in SEED_ORBIT

# The SCALAR_137 self-reference: 11 × SCALAR_137 − 1 ≡ SCALAR_137 mod 37
assert (11 * SCALAR_137 - 1) % 37 == SCALAR_137   # fixed-point identity


if __name__ == "__main__":
    print("Sofia Germain Prime in GF(37) — THEOREM 69")
    print("=" * 60)
    print()
    print(f"p = {k} × 2^{n} − 1  (~388,342 digits)")
    print()
    print(f"k = {k}")
    print(f"  k mod 37 = {k37}  ∈ ORBIT_11  ✓")
    print()
    print(f"n = {n}")
    print(f"  n mod 36 = {n36}  (ord₃₇(2)=36)")
    print(f"  2^n mod 37 = 2^12 = {pow2n} = SCALAR_137  ∈ IC  ✓")
    print(f"  n mod 37 = {n%37}  ∈ SEED_ORBIT  ✓")
    print()
    print(f"k × 2^n ≡ 11×26 = 286 ≡ {kpow} mod 37")
    print(f"p ≡ {kpow}−1 = {p37} = SCALAR_137  ∈ IC  ✓")
    print(f"  (the prime IS the 137-map multiplier mod 37)")
    print()
    print(f"q = 2p+1  ≡ 2×{p37}+1 = {2*p37+1} ≡ {q37} mod 37  ∈ O2={{9,12,16}}  ✓")
    print()
    print(f"DR(p) = {p9 if p9>0 else 9}  ∈ CB  ✓")
    print(f"DR(q) = {q9 if q9>0 else 9}  ∈ CB  ✓")
    print()
    print(f"Fixed-point identity: 11 × 26 − 1 ≡ 26 mod 37  (ORBIT_11 × IC − 1 = IC)")
    print()
    print("All assertions pass.")
