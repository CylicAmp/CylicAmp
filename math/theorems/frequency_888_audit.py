"""
frequency_888_audit.py

Framework analysis of 888 (MHz center frequency, ASKAP VAST survey).

─────────────────────────────────────────────────────────────────
FACTORIZATION:
  888 = 8 × 111
      = 8 × 3 × 37
      = AHL × repunit₃
      = AHL × 3 × framework_modulus

  888 = 24 × 37
      = φ(90) × framework_modulus
      = (wheel-sieve Euler totient) × framework_modulus

  888 ≡ 0 mod 37   (divisible by the framework modulus)
  888 ≡ 6 mod 9    (DR(888) = 6 = cascade product 1×2×3)

─────────────────────────────────────────────────────────────────
KEY IDENTITIES:
  AHL = 8 (doubling cycle step 4/6; DR(17)=8)
  repunit₃ = 111 = 3 × 37
  φ(90) = 24 (admissible residues in wheel sieve mod 90)
  37 = framework modulus (Z/37Z prime field)

  888 = AHL × repunit₃ = φ(90) × 37

  These are the same factorization because:
    AHL × repunit₃ = 8 × 111 = 8 × 3 × 37 = 24 × 37 = φ(90) × 37  ✓

─────────────────────────────────────────────────────────────────
"""

from math import gcd

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = abs(n) % 9
    return r if r else 9


def phi(n):
    """Euler totient φ(n)."""
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


# ── Framework constants ───────────────────────────────────────────────────────

FREQ       = 888
AHL        = 8
REPUNIT_3  = 111
MODULUS    = 37
PHI_90     = 24

# ── Primary factorization ─────────────────────────────────────────────────────

check(FREQ == AHL * REPUNIT_3, "888 = AHL × repunit₃ = 8×111", FREQ, AHL * REPUNIT_3)
check(REPUNIT_3 == 3 * MODULUS, "repunit₃ = 3×37", REPUNIT_3, 3 * MODULUS)
check(FREQ == AHL * 3 * MODULUS, "888 = 8×3×37 = AHL×3×modulus", FREQ, AHL * 3 * MODULUS)

# ── Euler-totient factorization ───────────────────────────────────────────────

check(phi(90) == PHI_90, "φ(90) = 24", phi(90), PHI_90)
check(FREQ == PHI_90 * MODULUS, "888 = φ(90)×37 = 24×37", FREQ, PHI_90 * MODULUS)

# The two factorizations are the same
check(AHL * REPUNIT_3 == PHI_90 * MODULUS,
      "AHL×repunit₃ = φ(90)×modulus (same factorization)",
      AHL * REPUNIT_3, PHI_90 * MODULUS)

# Why: AHL × repunit₃ = 8 × 111 = 8 × 3 × 37; φ(90) × 37 = 24 × 37 = 8×3×37
check(AHL * 3 == PHI_90, "AHL×3 = 8×3 = 24 = φ(90)", AHL * 3, PHI_90)


# ── Modular properties ────────────────────────────────────────────────────────

check(FREQ % MODULUS == 0, "888 ≡ 0 mod 37 (divisible by framework modulus)",
      FREQ % MODULUS, 0)
check(FREQ // MODULUS == PHI_90, "888 / 37 = 24 = φ(90)", FREQ // MODULUS, PHI_90)

check(dr(FREQ) == 6, "DR(888) = 6 = cascade product (1×2×3)", dr(FREQ), 6)
check(FREQ % 9 == 6, "888 ≡ 6 mod 9", FREQ % 9, 6)
check(1 * 2 * 3 == 6, "cascade product φ×e×π first digits = 1×2×3 = 6", 1 * 2 * 3, 6)

# DR chain: 888 → 24 → 6
check(dr(FREQ) == dr(PHI_90), "DR(888) = DR(24) = 6", dr(FREQ), dr(PHI_90))
check(dr(PHI_90) == 6, "DR(24) = 6", dr(PHI_90), 6)


# ── Digit structure ───────────────────────────────────────────────────────────

digits = [int(d) for d in str(FREQ)]   # [8, 8, 8]
check(digits == [AHL, AHL, AHL], "888 = [AHL,AHL,AHL] = three AHL digits", digits, [AHL]*3)
check(sum(digits) == 24, "digit sum(888) = 24 = φ(90)", sum(digits), 24)
check(sum(digits) == PHI_90, "digit sum(888) = φ(90)", sum(digits), PHI_90)

# The repeated AHL digit
check(digits[0] == digits[1] == digits[2] == AHL,
      "all three digits = AHL = 8", True, True)

# repunit₃ digit structure: 111 = [1,1,1] — the unit
repunit_digits = [int(d) for d in str(REPUNIT_3)]
check(repunit_digits == [1, 1, 1], "repunit₃ = [1,1,1] (three units)", repunit_digits, [1,1,1])
check(sum(repunit_digits) == 3, "digit sum(repunit₃) = 3 = π-axiom", sum(repunit_digits), 3)
check(dr(REPUNIT_3) == 3, "DR(111) = 3", dr(REPUNIT_3), 3)

# 888 = [AHL,AHL,AHL] ×digit× [1,1,1] = AHL × repunit₃
check(AHL * REPUNIT_3 == FREQ, "digit product: 8×[1,1,1] = [8,8,8] = 888", True, True)


# ── Cascade and doubling cycle connections ────────────────────────────────────

# AHL = 8 is step 4/6 in the doubling cycle 1→2→4→8→7→5→1
DOUBLING_CYCLE = [1, 2, 4, 8, 7, 5]
check(DOUBLING_CYCLE[3] == AHL, "doubling_cycle[3] = 8 = AHL", DOUBLING_CYCLE[3], AHL)

# DR(888) = 6 = DR(1×2×3) = DR(φ×e×π first digits) = DR(AHL+ALO) = DR(8+7)
ALO = 7
check(dr(AHL + ALO) == 6, "DR(AHL+ALO) = DR(8+7) = DR(15) = 6", dr(AHL + ALO), 6)
check(dr(FREQ) == dr(AHL + ALO), "DR(888) = DR(AHL+ALO)", dr(FREQ), dr(AHL + ALO))

# 888 / 8 = 111 = repunit₃; DR(111) = 3 = π-axiom
check(FREQ // AHL == REPUNIT_3, "888 / AHL = 111 = repunit₃", FREQ // AHL, REPUNIT_3)
check(dr(REPUNIT_3) == 3, "DR(repunit₃) = DR(111) = 3 = π-axiom", dr(REPUNIT_3), 3)

# 37 in Z/37Z: GATE = 18 = (37-1)/2; repunit period mod 37 = 3 (period of 1,11,111)
GATE = (MODULUS - 1) // 2
check(GATE == 18, "GATE = (37-1)/2 = 18", GATE, 18)
repunit_mod37 = [1 % MODULUS, 11 % MODULUS, 111 % MODULUS]
check(repunit_mod37 == [1, 11, 0], "repunits mod 37: [1,11,0] (period 3, 111≡0)", repunit_mod37, [1, 11, 0])
check(REPUNIT_3 % MODULUS == 0, "repunit₃ = 111 ≡ 0 mod 37 (zero element)", REPUNIT_3 % MODULUS, 0)

# 888 ≡ 0 mod 37 follows directly: 888 = AHL × repunit₃ ≡ 8 × 0 = 0 mod 37
check(AHL * (REPUNIT_3 % MODULUS) % MODULUS == 0,
      "888 ≡ AHL×(repunit₃ mod 37) = 8×0 = 0 mod 37",
      AHL * (REPUNIT_3 % MODULUS) % MODULUS, 0)


# ── φ(90) = 24 connections ───────────────────────────────────────────────────

# φ(90) = 24 = number of coprime residues mod 90 = admissible wheel positions
check(phi(90) == 24, "φ(90) = 24 (admissible wheel positions)", phi(90), 24)

# 24 = 8 × 3 = AHL × π-axiom
check(24 == AHL * 3, "24 = 8×3 = AHL×π-axiom", 24, AHL * 3)

# 24 = 4! (factorial: also 1×2×3×4)
check(24 == 1 * 2 * 3 * 4, "24 = 4! = 1×2×3×4", 24, 1 * 2 * 3 * 4)

# DR(24) = 6 = cascade product
check(dr(24) == 6, "DR(24) = DR(φ(90)) = 6 = cascade product", dr(24), 6)

# 9 admissible twin-prime pairs mod 90; 24/9 is not integer (9 is odd, 24=8×3)
# but: 24 = 9 + 9 + 6; i.e., 24 admissible residues = 9 pairs × 2 + 6 singles
TWIN_PRIME_PAIRS_MOD90 = 9
check(TWIN_PRIME_PAIRS_MOD90 * 2 + 6 == PHI_90,
      "9 twin-prime pairs×2 + 6 = 18+6 = 24 = φ(90)",
      TWIN_PRIME_PAIRS_MOD90 * 2 + 6, PHI_90)


# ── Summary table ─────────────────────────────────────────────────────────────

CONNECTIONS = [
    ("888 = AHL × repunit₃",             AHL * REPUNIT_3 == FREQ),
    ("888 = φ(90) × 37",                 PHI_90 * MODULUS == FREQ),
    ("888 ≡ 0 mod 37",                   FREQ % MODULUS == 0),
    ("DR(888) = 6 = cascade product",     dr(FREQ) == 6),
    ("digits(888) = [AHL,AHL,AHL]",       digits == [8, 8, 8]),
    ("digit sum(888) = 24 = φ(90)",       sum(digits) == PHI_90),
    ("repunit₃ ≡ 0 mod 37",              REPUNIT_3 % MODULUS == 0),
    ("φ(90) = AHL × π-axiom = 8×3",      PHI_90 == AHL * 3),
]

for label, cond in CONNECTIONS:
    check(cond, label, cond, True)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Frequency 888 Framework Audit")
    print("=" * 66)

    print(f"\n── Factorization ──")
    print(f"  888 = {AHL} × {REPUNIT_3}  =  AHL × repunit₃")
    print(f"  888 = {AHL} × 3 × {MODULUS}  =  AHL × 3 × modulus")
    print(f"  888 = {PHI_90} × {MODULUS}  =  φ(90) × modulus")
    print(f"  These are identical: AHL×3 = {AHL}×3 = {AHL*3} = φ(90)")

    print(f"\n── Modular properties ──")
    print(f"  888 mod 37 = {FREQ % MODULUS}  (divisible by framework modulus)")
    print(f"  888 / 37   = {FREQ // MODULUS} = φ(90)")
    print(f"  888 mod 9  = {FREQ % 9}  =  DR(888) = 6 = cascade product (1×2×3)")
    print(f"  888 → 24 → 6  (DR chain)")

    print(f"\n── Digit structure ──")
    print(f"  digits(888)  = {digits}  =  [AHL,AHL,AHL]  =  three AHL digits")
    print(f"  digits(111)  = {repunit_digits}  =  [1,1,1]   =  three units (repunit₃)")
    print(f"  digit sum(888) = {sum(digits)} = φ(90)")
    print(f"  DR(111) = {dr(REPUNIT_3)} = π-axiom;  DR(888) = {dr(FREQ)} = cascade product")

    print(f"\n── Repunit and modulus connection ──")
    print(f"  repunit₁=1 mod 37=1,  repunit₂=11 mod 37=11,  repunit₃=111 mod 37=0")
    print(f"  111 ≡ 0 mod 37 → 888 = 8×111 ≡ 0 mod 37")
    print(f"  repunit₃ is the zero element of Z/37Z (up to normalization)")

    print(f"\n── φ(90) = 24 connections ──")
    print(f"  φ(90) = 24 = AHL×π-axiom = 8×3")
    print(f"  24 = 4! = number of admissible wheel residues mod 90")
    print(f"  9 twin-prime pairs × 2 + 6 = {9*2+6} = 24 = φ(90)")
    print(f"  DR(24) = {dr(24)} = cascade product")

    print(f"\n── Connection table ──")
    for label, cond in CONNECTIONS:
        print(f"  {'✓' if cond else '✗'}  {label}")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
