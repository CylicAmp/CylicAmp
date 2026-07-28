"""
Sofia Germain Prime in GF(37) — THEOREM 69

THE PRIME:  p = 2618163402417 × 2^21290 − 1  (largest known Sofia Germain prime)
            q = 2p + 1                          (safe prime)

THE KEY FACT: q ≡ 30 mod 37 = SA∩ST, the unique sovereign intersection.
One-line reason: ORBIT_11 × SA∩ST − 1 ≡ ANTI_SOV, then 2×ANTI_SOV + 1 ≡ SA∩ST.

HAND-CHECKABLE:
  k = 2618163402417 ≡ 11 mod 37    (ORBIT_11)
  n = 21290;  n mod 36 = 14;  2^14 ≡ 30 mod 37   (SA∩ST = {30} element)
  p ≡ 11 × 30 − 1 = 329 ≡ 33 mod 37              (ANTI_SOV = {7,33,34})
  q ≡ 2 × 33 + 1 = 67  ≡ 30 mod 37               (SA∩ST = {30})

ORBIT CHAIN (mod 37):
  k ∈ ORBIT_11    ×   2^n ∈ SA∩ST   −1  →  p ∈ ANTI_SOV
  p ∈ ANTI_SOV    ×2  +1             →  q ∈ SA∩ST

CONNECTIONS TO THE FRAMEWORK:
  • 2^21290 ≡ 30 ∈ SA∩ST:  the power-of-2 in the prime formula hits the sovereign
    intersection because ord₃₇(2)=36 and 21290 mod 36 = 14, and 2^14 ≡ 30.
  • p ∈ ANTI_SOV = {7,33,34}:  ANTI_SOV is the squaring image of O3=OUTLIER_SOV
    (THEOREM 64 squaring map), and the tripling map sends ORBIT_11 → ANTI_SOV
    after 3 steps (THEOREM 68 Cycle 1).
  • q ≡ 30 = SA∩ST: the safe prime sits at the unique element shared by both
    sovereign sets — the sovereign intersection, which is also SA∩ST pivot in
    the ST chain 3→12→21→30 (THEOREM 65).
  • DR(p) = DR(q) = 8 ∈ CB: both prime and safe prime share the same digital root,
    landing in the Cascade Base orbit {8,13,24}.
  • 21290 mod 37 = 15 ∈ DARK_A: the exponent itself lives in DARK_A = {2,15,20},
    the primitive-root orbit.

DIGITAL ROOT PATH:
  k ≡ 0 mod 9  (digit sum = 45)
  2^21290 ≡ 4 mod 9  (period 6; 21290 mod 6 = 2; 2^2 = 4)
  k × 2^n ≡ 0 mod 9  →  p = k×2^n − 1 ≡ 8 mod 9  →  DR(p) = 8 ∈ CB
  q = 2p+1 ≡ 17 ≡ 8 mod 9  →  DR(q) = 8 ∈ CB

  Both prime and safe prime have DR = 8 ∈ CB = {8,13,24}.
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA             = frozenset({4, 9, 25, 30})
ST             = frozenset({3, 12, 21, 30})
CB             = frozenset({8, 13, 24})
ORBIT_11       = frozenset({11, 27, 36})
DARK_A         = frozenset({2, 15, 20})
ANTI_SOV       = frozenset({7, 33, 34})
IDENTITY_CYCLE = frozenset({1, 10, 26})
OUTLIER_SOV    = frozenset({21, 25, 28})


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


# ── PRIME PARAMETERS ─────────────────────────────────────────────────────────

k = 2618163402417   # coefficient
n = 21290           # exponent

k37 = k % 37
n36 = n % 36        # ord₃₇(2) = 36
pow2n = pow(2, n, 37)


# ── KEY CHECKS ────────────────────────────────────────────────────────────────

# Coefficient in ORBIT_11
assert k37 == 11 and 11 in ORBIT_11

# Exponent: 21290 mod 36 = 14; 2^14 ≡ 30 ∈ SA∩ST
assert n36 == 14
assert pow2n == 30 and 30 in SA and 30 in ST

# n mod 37 ∈ DARK_A
assert n % 37 == 15 and 15 in DARK_A

# p ≡ k×2^n − 1 ≡ ANTI_SOV
p37 = (k37 * pow2n - 1) % 37
assert p37 == 33 and 33 in ANTI_SOV

# Hand-check: 11×30 − 1 = 329 ≡ 33 mod 37
assert 11 * 30 - 1 == 329 and 329 % 37 == 33

# Safe prime q = 2p+1 ≡ SA∩ST = {30}
q37 = (2 * p37 + 1) % 37
assert q37 == 30 and 30 in SA and 30 in ST

# DR of p and q (using mod 9 arithmetic)
k9       = sum(int(d) for d in str(k)) % 9   # 45 % 9 = 0
pow2n_9  = pow(2, n, 9)                       # 2^21290 mod 9
p9       = (k9 * pow2n_9 - 1) % 9
q9       = (2 * p9 + 1) % 9

assert k9 == 0              # digit sum 45 ≡ 0 mod 9
assert n % 6 == 2           # 21290 mod 6 = 2 → 2^n ≡ 4 mod 9
assert pow2n_9 == 4
assert p9 == 8 and 8 in CB  # DR(p) = 8 ∈ CB
assert q9 == 8 and 8 in CB  # DR(q) = 8 ∈ CB

# SA∩ST is a singleton {30}; q lands there
SA_ST = SA & ST
assert SA_ST == frozenset({30})
assert q37 in SA_ST

# ANTI_SOV is the squaring image of OUTLIER_SOV (THEOREM 64)
assert frozenset(pow(x, 2, 37) for x in OUTLIER_SOV) == ANTI_SOV

# 21290 mod 36 = 14, confirming 2^14 anchors the power
assert pow(2, 14, 37) == 30


if __name__ == "__main__":
    print("Sofia Germain Prime in GF(37) — THEOREM 69")
    print("=" * 60)
    print()
    print(f"p = {k} × 2^{n} − 1")
    print()
    print(f"k = {k}")
    print(f"  k mod 37 = {k37}  ∈ ORBIT_11  {'✓' if k37 in ORBIT_11 else '✗'}")
    print(f"  DR(k) = {dr(sum(int(d) for d in str(k)))} ∈ SA: {dr(sum(int(d) for d in str(k))) in SA}")
    print()
    print(f"n = {n}")
    print(f"  n mod 36 = {n36}  (since ord₃₇(2)=36)")
    print(f"  2^n mod 37 = 2^14 mod 37 = {pow2n}  ∈ SA∩ST  {'✓' if pow2n in SA and pow2n in ST else '✗'}")
    print(f"  n mod 37 = {n%37}  ∈ DARK_A  {'✓' if n%37 in DARK_A else '✗'}")
    print()
    print(f"p ≡ {k37}×{pow2n}−1 = {k37*pow2n-1} ≡ {p37} mod 37")
    print(f"  p mod 37 = {p37}  ∈ ANTI_SOV  {'✓' if p37 in ANTI_SOV else '✗'}")
    print(f"  DR(p) = {p9 if p9 > 0 else 9}  ∈ CB  {'✓' if p9 in CB or p9==8 else '✗'}")
    print()
    print(f"q = 2p+1  ≡ 2×{p37}+1 = {2*p37+1} ≡ {q37} mod 37")
    print(f"  q mod 37 = {q37}  ∈ SA∩ST = {{30}}  {'✓' if q37 in SA and q37 in ST else '✗'}")
    print(f"  DR(q) = {q9 if q9 > 0 else 9}  ∈ CB  {'✓' if q9 in CB or q9==8 else '✗'}")
    print()
    print("Sovereign intersection SA∩ST = {30}.")
    print("The safe prime of the world-record Sofia Germain prime")
    print("sits at the unique sovereign intersection node.")
    print()
    print("All assertions pass.")
