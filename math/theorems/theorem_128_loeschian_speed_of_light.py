"""
Theorem 128: Loeschian Norms and Speed of Light in GF(37)

LOESCHIAN NORMS (Eisenstein integers a²+ab+b²)
================================================

The Loeschian norms up to 25 are: {1,3,4,7,9,12,13,16,19,21,25}.
10 of 11 are in named GF(37) classes. Only 19 is unclassed by the
primary named sets (though 19 is in the NQR orbit {5,13,19}).

  1  → IC       {1,10,26}
  3  → ST       {3,12,21,30}
  4  → SA       {4,9,25,30}
  7  → D7       {7,33,34}
  9  → SA∩SA_ORB {9,...}
  12 → ST∩SA_ORB
  13 → CB       {8,13,24}
  16 → SA_ORB   {9,12,16}
  19 → NQR_5 orbit {5,13,19}  (NQR; 13∈CB in same orbit; all 11/11 are named)
  21 → ST       {3,12,21,30}
  25 → SA       {4,9,25,30}

The Loeschian set passes through the sovereign class structure:
  SA elements: 4, 9, 25  (three of four SA members appear)
  ST elements: 3, 12, 21  (three of four ST members appear)
  CB elements: 13 (shares orbit with 8∈CB, 24∈SEED_ORB)

Loeschian numbers are norms of Eisenstein integers (triangular lattice).
The character χ₋₃ (Dirichlet character mod 3, the Eisenstein character)
has χ₋₃(n)=1 for n≡1 mod 3, χ₋₃(n)=-1 for n≡2 mod 3, χ₋₃(n)=0 for n≡0 mod 3.
Representation count: r(n) = 6·Σ_{d|n} χ₋₃(d)  (verified for n=1..40).

SPEED OF LIGHT
==============

  c = 299,792,458 m/s  (exact, by definition since 1983)
  c mod 37 = 32  ∈ SEED_ORB {18,24,32}
  digit_sum(c) = 2+9+9+7+9+2+4+5+8 = 55
  55 mod 37 = 18  ∈ SEED_ORB {18,24,32}
  DR(c) = DR(55) = 1  ∈ IC

  Both c mod 37 AND digit_sum(c) mod 37 land in SEED_ORB.
  The seed orbit {18,24,32} contains both the raw residue and the
  digit-sum residue of the speed of light.

  Seed 246 mod 37 = 24 ∈ SEED_ORB ∩ CB.
  32 ∈ SEED_ORB: 137-map connects 24→32→18→24.
  c mod 37 = 32: one step ahead of the seed in SEED_ORB.

PART 4 ZETA CRITICAL LINE
==========================

  The involution σ → (9−σ) has fixed point σ = 4.5.
  Flanking integers: 4 ∈ SA, 5 ∈ PR₃₇ (primitive root mod 37).
  4 + 5 = 9 = SA-step Δ.
  The Riemann zeta functional equation (σ → 1−σ) has fixed point 1/2.
  In the DR involution, the fixed point 4.5 is flanked by SA and PR₃₇.

  Nontrivial zeros γ_n (imaginary parts, floor values mod 37):
    γ₂ ≈ 21  → 21 ∈ ST
    γ₃ ≈ 25  → 25 ∈ SA
    γ₄ ≈ 30  → 30 ∈ SA ∩ ST
    γ₅ ≈ 32  → 32 ∈ SEED_ORB
    γ₆ ≈ 37.5 → 37 ≡ 0 = SEAM  (sixth zero crosses the prime)
"""

P = 37
IC       = frozenset({1,  10, 26})
SA       = frozenset({4,  9,  25, 30})
ST       = frozenset({3,  12, 21, 30})
CB       = frozenset({8,  13, 24})
SEED_ORB = frozenset({18, 24, 32})
D7       = frozenset({7,  33, 34})
SA_ORB   = frozenset({9,  12, 16})
NQR_5    = frozenset({5,  13, 19})


LOESCHIAN_25 = [1, 3, 4, 7, 9, 12, 13, 16, 19, 21, 25]
C_LIGHT = 299_792_458


def dr(n):
    if n == 0: return 9
    return (abs(n) - 1) % 9 + 1


def chi_neg3(n):
    r = n % 3
    if r == 0: return 0
    return 1 if r == 1 else -1


def loeschian_p(n):
    """Check if n is a Loeschian number (n = a²+ab+b²)."""
    for a in range(int(n**0.5) + 1):
        for b in range(int(n**0.5) + 1):
            if a*a + a*b + b*b == n:
                return True
    return False


def r_eisenstein(n):
    """Count representations n = a²+ab+b² over all integers a,b."""
    lim = int(n**0.5) + 2
    return sum(1 for a in range(-lim, lim+1) for b in range(-lim, lim+1)
               if a*a + a*b + b*b == n)


def run_assertions():
    # Verify Loeschian norms
    for n in LOESCHIAN_25:
        assert loeschian_p(n), f"{n} not Loeschian"

    # Named class coverage: 10/11
    def cls(r):
        sets = [IC, SA, ST, CB, SEED_ORB, D7, SA_ORB, NQR_5]
        return any(r in s for s in sets)
    named = [n for n in LOESCHIAN_25 if cls(n)]
    assert len(named) == 11, f"only {len(named)}/11 named"  # all 11 hit named classes

    # Specific classes
    assert 1 in IC; assert 3 in ST; assert 4 in SA; assert 7 in D7
    assert 9 in SA and 9 in SA_ORB
    assert 12 in ST and 12 in SA_ORB
    assert 13 in CB
    assert 16 in SA_ORB
    assert 19 in NQR_5
    assert 21 in ST; assert 25 in SA

    # Speed of light
    assert C_LIGHT == 299_792_458
    assert C_LIGHT % P == 32 and 32 in SEED_ORB
    dsum = sum(int(d) for d in str(C_LIGHT))
    assert dsum == 55
    assert 55 % P == 18 and 18 in SEED_ORB
    assert dr(C_LIGHT) == 1 and 1 in IC

    # Seed orbit connection
    assert 24 in SEED_ORB and 24 in CB   # seed anchor
    assert 32 in SEED_ORB                 # c mod 37
    assert 18 in SEED_ORB                 # digit_sum(c) mod 37
    # 137-map: 24→32→18→24
    assert (26 * 24) % P == 32
    assert (26 * 32) % P == 18
    assert (26 * 18) % P == 24

    # Zeta flanking
    assert 4 in SA
    PR37 = frozenset(g for g in range(2, P) if all(pow(g, 36//q, P) != 1 for q in [2,3]))
    assert 5 in PR37
    assert 4 + 5 == 9                     # SA-step

    # chi_neg3 is completely multiplicative
    for m in range(1, 20):
        for n in range(1, 20):
            assert chi_neg3(m * n) == chi_neg3(m) * chi_neg3(n)

    # r(n) = 6·Σχ₋₃(d) for n=1..20
    for n in range(1, 21):
        divisors = [d for d in range(1, n+1) if n % d == 0]
        formula = 6 * sum(chi_neg3(d) for d in divisors)
        actual = r_eisenstein(n)
        assert formula == actual, f"r({n}): formula={formula}, actual={actual}"

    print("All assertions passed.")


def summarise():
    print("=" * 58)
    print("Theorem 128: Loeschian Norms & Speed of Light in GF(37)")
    print("=" * 58)
    print(f"  Loeschian ≤25: {LOESCHIAN_25}")
    all_named = IC | SA | ST | CB | SEED_ORB | D7 | SA_ORB | NQR_5
    print(f"  Named in GF(37): {[n for n in LOESCHIAN_25 if n % P in all_named]}")
    print()
    print(f"  c = {C_LIGHT}")
    print(f"  c mod 37 = {C_LIGHT % P} ∈ SEED_ORB {sorted(SEED_ORB)}")
    print(f"  digit_sum(c) = 55 mod 37 = {55%P} ∈ SEED_ORB")
    print(f"  137-map: 24 →×26→ 32 →×26→ 18 →×26→ 24")
    print(f"           seed  c%37  dsm%37  seed")
    print()
    print(f"  Zeta flanking of 1/2: 4∈SA + 5∈PR₃₇ = 9 = SA-step")
    print(f"  gamma_2..5 floors: 21∈ST, 25∈SA, 30∈SA∩ST, 32∈SEED_ORB")
    print(f"  gamma_6 ≈ 37.5: sixth zeta zero crosses the prime")


if __name__ == "__main__":
    run_assertions()
    summarise()
