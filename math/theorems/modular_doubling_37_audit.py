"""
modular_doubling_37_audit.py

The sequence  Cₖ = (g · 2ᵏ mod 37) mod 9  and its structure in DR-space.

─────────────────────────────────────────────────────────────────
FRAMEWORK LINK:
  37 is the prime factor of 111 = 3 × 37.
  mod 9 = the DR reduction (digital root for 1–9).
  Combining them: project the doubling orbit mod 37 into DR-space.

KEY FACTS:
  (M1) 2 is the smallest primitive root mod 37.
       ord₃₇(2) = 36 = φ(37).
       The orbit {2ᵏ mod 37 : k=0..35} = {1, 2, …, 36} exactly.

  (M2) 37 ≡ 1 (mod 9).
       Therefore {1,…,36} mod 9 = 4 copies of {0,1,2,3,4,5,6,7,8}:
       each residue class appears exactly 4 times.

  (M3) For gcd(g, 9) = 1 (g ∈ {1,2,4,5,7,8}):
       Cₖ is perfectly equidistributed — each of {0,…,8} appears 4 times.

  (M4) For gcd(g, 9) = 3 (g ∈ {3, 6}):
       Cₖ takes only values {0, 3, 6} (12 times each).

  (M5) For g = 9 (gcd = 9):  Cₖ = 0 for all k.

  (M6) First 6 terms of Cₖ (g=1) match the DR doubling sequence exactly:
       [1, 2, 4, 8, 7, 5].  Divergence begins at k=6 where the
       mod-37 reduction first fires: 2⁶=64 ≡ 27 (mod 37); 27 mod 9 = 0,
       but 64 mod 9 = 1 (the pure DR cycle would give 1 here).

  (M7) Zeros of Cₖ (g=1) at k = 6, 16, 17, 18.
       These are exactly the four positions where 2ᵏ mod 37 is a multiple
       of 9: {27, 9, 18, 36}.  Spacing: [10, 1, 1].

SEQUENCE (g=1, k=0..35):
  [1, 2, 4, 8, 7, 5, 0, 8, 7, 4, 7, 4, 8, 6, 3, 5,
   0, 0, 0, 8, 6, 2, 3, 5, 1, 2, 3, 6, 3, 6, 2, 4, 7, 5, 1, 1]
─────────────────────────────────────────────────────────────────
"""

from sympy import isprime, primitive_root, factorint
from collections import Counter
from math import gcd

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = n % 9
    return r if r else 9


# ── Framework link: 37 in 111 ─────────────────────────────────────────────────

check(factorint(111) == {3: 1, 37: 1}, "111=3×37", factorint(111), {3: 1, 37: 1})
check(37 % 9 == 1, "37 ≡ 1 mod 9", 37 % 9, 1)
check(isprime(37), "37 is prime", isprime(37), True)


# ── M1: 2 is a primitive root mod 37, order = 36 ─────────────────────────────

check(primitive_root(37) == 2, "prim root mod 37 = 2", primitive_root(37), 2)

orbit = [pow(2, k, 37) for k in range(36)]
check(sorted(orbit) == list(range(1, 37)), "orbit = {1..36}", sorted(orbit), list(range(1, 37)))
check(len(set(orbit)) == 36, "orbit length = 36", len(set(orbit)), 36)


# ── M2: uniform distribution of {1..36} mod 9 ────────────────────────────────

residues_mod9 = [x % 9 for x in range(1, 37)]
counts_mod9 = Counter(residues_mod9)
check(all(counts_mod9[r] == 4 for r in range(9)), "{1..36} mod 9 uniform (4 each)",
      dict(sorted(counts_mod9.items())), {r: 4 for r in range(9)})


# ── Sequences Cₖ = (g · 2ᵏ mod 37) mod 9 for g=1..9 ─────────────────────────

SEQ = {}
for g in range(1, 10):
    SEQ[g] = [(g * pow(2, k, 37)) % 9 for k in range(36)]


# ── M3: equidistribution when gcd(g, 9) = 1 ──────────────────────────────────

uniform_g = [1, 2, 4, 5, 7, 8]
for g in uniform_g:
    c = Counter(SEQ[g])
    check(all(c[r] == 4 for r in range(9)),
          f"equidist g={g}", dict(sorted(c.items())), {r: 4 for r in range(9)})
    check(gcd(g, 9) == 1, f"gcd({g},9)=1", gcd(g, 9), 1)


# ── M4: three-value collapse when gcd(g, 9) = 3 ──────────────────────────────

for g in [3, 6]:
    c = Counter(SEQ[g])
    check(set(c.keys()) == {0, 3, 6}, f"g={g} values={{0,3,6}}", set(c.keys()), {0, 3, 6})
    check(all(c[r] == 12 for r in [0, 3, 6]),
          f"g={g} counts=12 each", dict(sorted(c.items())), {0: 12, 3: 12, 6: 12})
    check(gcd(g, 9) == 3, f"gcd({g},9)=3", gcd(g, 9), 3)


# ── M5: all-zero when g = 9 ───────────────────────────────────────────────────

check(all(v == 0 for v in SEQ[9]), "g=9 all zeros", set(SEQ[9]), {0})
check(gcd(9, 9) == 9, "gcd(9,9)=9", gcd(9, 9), 9)


# ── M6: first 6 terms match DR doubling sequence ──────────────────────────────

DR_DOUBLING = [1, 2, 4, 8, 7, 5]   # DR(2^k) mod 9 for k=0..5, pure mod 9
check(SEQ[1][:6] == DR_DOUBLING, "first 6 terms = DR doubling", SEQ[1][:6], DR_DOUBLING)

# Divergence at k=6: 2^6 mod 37 = 27; 27 mod 9 = 0; but 64 mod 9 = 1
check(pow(2, 6, 37) == 27, "2^6 mod 37 = 27", pow(2, 6, 37), 27)
check(27 % 9 == 0, "27 mod 9 = 0", 27 % 9, 0)
check(pow(2, 6) % 9 == 1, "64 mod 9 = 1 (pure DR cycle)", pow(2, 6) % 9, 1)
check(SEQ[1][6] == 0, "C₆ = 0 (diverges from DR cycle)", SEQ[1][6], 0)


# ── M7: zeros at k = 6, 16, 17, 18 ──────────────────────────────────────────

zero_ks = [k for k, v in enumerate(SEQ[1]) if v == 0]
check(zero_ks == [6, 16, 17, 18], "zero positions", zero_ks, [6, 16, 17, 18])

# Values: 27, 9, 18, 36 — all multiples of 9 in {1..36}
zero_vals = [orbit[k] for k in zero_ks]
check(zero_vals == [27, 9, 18, 36], "zero values in orbit", zero_vals, [27, 9, 18, 36])
check(all(v % 9 == 0 for v in zero_vals), "all are multiples of 9", True, True)
check(sorted(zero_vals) == [9, 18, 27, 36], "= {9,18,27,36}", sorted(zero_vals), [9, 18, 27, 36])

# Spacing: [10, 1, 1]
spacings = [zero_ks[i + 1] - zero_ks[i] for i in range(len(zero_ks) - 1)]
check(spacings == [10, 1, 1], "zero spacings", spacings, [10, 1, 1])

# Consecutive triple 16,17,18: 9,18,36 are 9·1, 9·2, 9·4 in Z
check(9 * 1 == 9 and 9 * 2 == 18 and 9 * 4 == 36, "triple = 9·{1,2,4}", True, True)


# ── Full sequence g=1 ─────────────────────────────────────────────────────────

EXPECTED_SEQ = [1, 2, 4, 8, 7, 5, 0, 8, 7, 4, 7, 4, 8, 6, 3, 5,
                0, 0, 0, 8, 6, 2, 3, 5, 1, 2, 3, 6, 3, 6, 2, 4, 7, 5, 1, 1]
check(SEQ[1] == EXPECTED_SEQ, "full sequence g=1", SEQ[1], EXPECTED_SEQ)


# ── Connection to DR function ─────────────────────────────────────────────────

# 37 ≡ 1 mod 9 → DR(37) = 1 = DR(1)
check(dr(37) == 1, "DR(37)=1", dr(37), 1)
check(dr(37) == dr(1), "DR(37)=DR(1)", dr(37), dr(1))

# DR(111) = 3 = DR(3); 111 = 3×37
check(dr(111) == 3, "DR(111)=3", dr(111), 3)
check(dr(3 * 37) == dr(3) * dr(37) % 9 or dr(3 * 37) == 3, "DR(3×37)=3",
      dr(3 * 37), 3)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Modular Doubling Sequence: Cₖ = (g·2ᵏ mod 37) mod 9")
    print("=" * 62)

    print(f"\n── Framework: 37 in DR-space ──")
    print(f"  111 = 3×37    DR(37) = {dr(37)}  37 ≡ 1 (mod 9)")
    print(f"  37 is prime; 2 is its smallest primitive root")
    print(f"  ord₃₇(2) = 36 = φ(37)")

    print(f"\n── Full sequence g=1, k=0..35 ──")
    print(f"  {SEQ[1]}")

    print(f"\n── Equidistribution ──")
    for g in range(1, 10):
        c = Counter(SEQ[g])
        d = gcd(g, 9)
        vals = sorted(c.keys())
        print(f"  g={g}  gcd(g,9)={d}  values={vals}  counts={[c[v] for v in vals]}")

    print(f"\n── First 6 terms vs DR doubling sequence ──")
    print(f"  C₀..C₅ = {SEQ[1][:6]}")
    print(f"  DR 2ᵏ  = {DR_DOUBLING}  (pure mod 9, period 6)")
    print(f"  Match. Divergence at k=6: 2⁶≡27 mod 37, 27 mod 9 = 0 (not 1).")

    print(f"\n── Zeros of Cₖ (g=1) ──")
    print(f"  Positions: {zero_ks}  spacing: {spacings}")
    print(f"  Orbit values: {zero_vals}")
    print(f"  = multiples of 9 in {{1..36}}: 27=3×9, 9=1×9, 18=2×9, 36=4×9")
    print(f"  Triple at k=16,17,18: 2^16≡9, 2^17≡18, 2^18≡36 (mod 37)")

    print(f"\n── 2ᵏ mod 37, k=0..35 ──")
    for k, v in enumerate(orbit):
        mark = " ← mult of 9" if v % 9 == 0 else ""
        print(f"  k={k:2d}: {v:2d}  mod 9 = {v%9}{mark}")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
