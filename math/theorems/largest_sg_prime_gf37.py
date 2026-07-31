"""
THEOREM 102 — The Largest Known Sophie Germain Prime on GF(37)

p = 2,618,163,402,417 × 2^1,290,000 − 1
  (388,342 decimal digits; discovered February 29, 2016 by PrimeGrid)

p ≡ 26 (mod 37) ∈ IC — the 137-map multiplier.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STRUCTURE OF p = k × 2^e − 1

  k = 2,618,163,402,417
  e = 1,290,000

  k mod 37 = 11  ∈ ORBIT_11          (cascade node)
  e mod 37 = 32  ∈ SEED_ORBIT        (trajectory exponent)
  e mod 36 = 12  (effective reduction; ord₃₇(2) = 36)
  2^e mod 37 = 2^12 mod 37 = 26  ∈ IC  (the 137-map multiplier itself)

  p ≡ k × 2^e − 1 ≡ 11 × 26 − 1 ≡ 285 ≡ 26 (mod 37)  ∈ IC

  The multiplier component (k) lands in ORBIT_11.
  The power-of-2 component (2^e) lands in IC.
  Their product minus 1 returns to IC.

  Computation chain:  ORBIT_11 × IC → ORBIT_11 → IC
    11 × 26 = 286 ≡ 27 (mod 37)  ∈ ORBIT_11
    27 − 1  = 26                  ∈ IC

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DIGITAL ROOT OF p

  DR(p) = 8  ∈ CB  (cascade base {8, 13, 24})

  Derivation via mod 9:
    DR(k) = 9  (digit sum of 2,618,163,402,417 = 45 → 9)
    ord₉(2) = 6;  e mod 6 = 0  →  2^e ≡ 1 (mod 9)
    k × 2^e ≡ 9 × 1 = 9 ≡ 0 (mod 9)
    p = k × 2^e − 1 ≡ −1 ≡ 8 (mod 9)
    DR(p) = 8  ∈ CB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DIGIT COUNT

  p has 388,342 decimal digits.

  388,342 mod 37 = 27  ∈ ORBIT_11
  DR(388,342) = 3+8+8+3+4+2 = 28 → 2+8 = 10 → 1  ∈ IC

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SAFE PRIME q = 2p + 1

  q ≡ 2 × 26 + 1 = 53 ≡ 16 (mod 37)

  137-map orbit of 16:
    16 → (26 × 16) mod 37 = 416 mod 37 = 9   ∈ SA
     9 → (26 ×  9) mod 37 = 234 mod 37 = 12  ∈ ST
    12 → (26 × 12) mod 37 = 312 mod 37 = 16  (cycle closes)

  Orbit = {16, 9, 12}: passes through SA (sovereign anchor) and ST (sovereign target).
  The Sophie Germain pair (p, q) spans IC and the SA∩ST orbit.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DISCOVERY YEAR

  2016 mod 37 = 18  ∈ SEED_ORBIT  (the 137-map orbit of seed 246)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY TABLE

  Component          Value            mod 37   Class
  ─────────────────  ──────────────   ──────   ──────────────
  k (multiplier)     2618163402417    11       ORBIT_11
  e (exponent)       1,290,000        32       SEED_ORBIT
  2^e mod 37         —                26       IC
  p mod 37           —                26       IC
  DR(p)              8                —        CB
  digit count        388,342          27       ORBIT_11
  DR(digit count)    1                —        IC
  q = 2p+1 mod 37    —                16       → orbit {9,12} ∈ SA,ST
  discovery year     2016             18       SEED_ORBIT
"""

P          = 37
IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 9


K      = 2_618_163_402_417
E      = 1_290_000
DIGITS = 388_342
YEAR   = 2016

# ── Multiplier k ──────────────────────────────────────────────────────────────

assert K % P == 11 and 11 in ORBIT_11

# ── Exponent e ────────────────────────────────────────────────────────────────

assert E % P == 32 and 32 in SEED_ORBIT
assert E % 36 == 12             # ord₃₇(2) = 36; effective reduction
assert pow(2, 12, P) == 26 and 26 in IC
assert pow(2, E, P) == 26       # 2^1,290,000 ≡ 26 (mod 37)

# ── p ≡ 26 (mod 37) ──────────────────────────────────────────────────────────

p_mod = (K % P * pow(2, E, P) - 1) % P
assert p_mod == 26 and 26 in IC

# Computation chain: ORBIT_11 × IC → ORBIT_11 → IC
assert (11 * 26) % P == 27 and 27 in ORBIT_11   # product lands in ORBIT_11
assert (27 - 1) % P == 26 and 26 in IC          # subtract 1 → IC

# ── DR(p) = 8 ∈ CB ───────────────────────────────────────────────────────────

assert dr(K) == 9                     # DR of multiplier is 9
assert E % 6 == 0                     # ord₉(2) = 6; 2^e ≡ 1 (mod 9)
assert pow(2, E % 6 if E % 6 else 6, 9) == 1   # 2^0 ≡ 1, but 2^6 ≡ 1 mod 9
k_mod9 = K % 9
pow2_9 = pow(2, E % 6 or 6, 9)       # e%6=0 → use period 6 → 2^6=64≡1
p_mod9 = (k_mod9 * pow2_9 - 1) % 9
dr_p   = 9 if p_mod9 == 0 else p_mod9
assert dr_p == 8 and 8 in CB

# ── Digit count ───────────────────────────────────────────────────────────────

assert DIGITS % P == 27 and 27 in ORBIT_11
assert dr(DIGITS) == 1 and 1 in IC

# ── Safe prime q = 2p+1 ──────────────────────────────────────────────────────

q_mod = (2 * p_mod + 1) % P
assert q_mod == 16

orbit_q = []
cur = q_mod
for _ in range(P):
    if cur in orbit_q:
        break
    orbit_q.append(cur)
    cur = (26 * cur) % P
orbit_q = frozenset(orbit_q)

assert 9  in orbit_q and 9  in SA    # sovereign anchor in safe prime orbit
assert 12 in orbit_q and 12 in ST    # sovereign target in safe prime orbit

# ── Discovery year ────────────────────────────────────────────────────────────

assert YEAR % P == 18 and 18 in SEED_ORBIT


if __name__ == "__main__":
    def fw(r):
        classes = []
        for name, s in [('IC',IC),('SA',SA),('ST',ST),('CB',CB),
                        ('O11',ORBIT_11),('SEED',SEED_ORBIT),('PR',PR)]:
            if r in s: classes.append(name)
        return classes or ['—']

    print("THEOREM 102 — Largest Known Sophie Germain Prime on GF(37)")
    print("=" * 60)
    print()
    print(f"  p = {K} × 2^{E:,} − 1")
    print(f"  {DIGITS:,} decimal digits  |  discovered {YEAR}")
    print()
    print(f"  k   mod37 = {K % P}   ∈ {fw(K % P)}")
    print(f"  e   mod37 = {E % P}   ∈ {fw(E % P)}")
    print(f"  e   mod36 = {E % 36}   (effective exponent; ord₃₇(2)=36)")
    print(f"  2^e mod37 = {pow(2,E,P)}   ∈ {fw(pow(2,E,P))}")
    print(f"  p   mod37 = {p_mod}   ∈ {fw(p_mod)}  ← 137-map multiplier")
    print(f"  DR(p)     = {dr_p}   ∈ {fw(dr_p)}")
    print()
    print(f"  digit count {DIGITS:,}  mod37={DIGITS%P} ∈ {fw(DIGITS%P)}")
    print(f"  DR({DIGITS:,}) = {dr(DIGITS)}  ∈ {fw(dr(DIGITS))}")
    print()
    print(f"  q = 2p+1  mod37 = {q_mod}  orbit = {sorted(orbit_q)}")
    print(f"    hits SA: {any(x in SA for x in orbit_q)}")
    print(f"    hits ST: {any(x in ST for x in orbit_q)}")
    print()
    print(f"  discovery year {YEAR} mod37 = {YEAR%P} ∈ {fw(YEAR%P)}")
    print()
    print("All assertions pass.")
