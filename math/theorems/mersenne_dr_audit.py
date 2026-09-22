"""
mersenne_dr_audit.py

Digital root structure of the 51 known Mersenne prime exponents.

─────────────────────────────────────────────────────────────────
OBJECT:
  M_p = 2^p − 1  (Mersenne prime, p = Mersenne prime exponent)

CLAIMS UNDER TEST:
  (D1) DR(M_p) is determined entirely by p mod 6.
  (D2) For p > 3:  DR(M_p) = 1 iff p ≡ 1 (mod 6);
                   DR(M_p) = 4 iff p ≡ 5 (mod 6).
  (D3) DR(M_p) ∈ {1, 3, 4, 7} for all known Mersenne primes.
  (D4) DR ∈ {2, 5, 6, 8, 9} is structurally excluded.
  (D5) Among p > 3: split DR=1 vs DR=4 is near 1:1.

STRUCTURAL PROOF OF D2:
  DR(M_p) ≡ M_p (mod 9) = (2^p − 1) mod 9
  Powers of 2 mod 9 cycle with period 6:
    p mod 6:  1 → 2,   2 → 4,   3 → 8,   4 → 7,   5 → 5,   0 → 1
  For prime p > 3:  p ≡ 1 (mod 6)  or  p ≡ 5 (mod 6)  only.
    p ≡ 1 (mod 6):  2^p ≡ 2 (mod 9)  →  M_p ≡ 1 (mod 9)  →  DR = 1
    p ≡ 5 (mod 6):  2^p ≡ 5 (mod 9)  →  M_p ≡ 4 (mod 9)  →  DR = 4
  For p = 2: 2^2 ≡ 4 (mod 9) → DR = 3.
  For p = 3: 2^3 ≡ 8 (mod 9) → DR = 7.

PROOF OF D4 (exclusions):
  DR ∈ {6, 9}: would require p ≡ 4 or 0 (mod 6); no prime p > 3
               satisfies either (4 is even; 0 requires 6|p).
  DR ∈ {2, 5}: would require 2^p ≡ 3 or 6 (mod 9); neither 3 nor 6
               appears in the period-6 cycle {2,4,8,7,5,1}.
  DR = 8:      would require 2^p ≡ 0 (mod 9); impossible since gcd(2,9)=1.

CONSISTENCY WITH PRIME DR VOID:
  Primes p > 3 satisfy DR(p) ∉ {3, 6, 9}.
  Mersenne primes M_p with p > 3 satisfy DR(M_p) ∈ {1, 4} ⊂ {1,2,4,5,7,8}.
  Both p=2 (DR=3) and p=3 (DR=7) satisfy the void since neither is > 3.
  → No Mersenne prime violates the prime DR void.

EMPIRICAL RESULTS (all 51 known exponents):
  DR values present:  {1, 3, 4, 7}
  DR values absent:   {2, 5, 6, 8, 9}
  p > 3:  DR=1: 24 exponents  |  DR=4: 25 exponents  (near 1:1)
─────────────────────────────────────────────────────────────────
"""

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


# ── Known Mersenne prime exponents (51 total, ordered) ────────────────────────

EXPONENTS = [
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127,
    521, 607, 1279, 2203, 2281, 3217, 4253, 4423,
    9689, 9941, 11213, 19937, 21701, 23209, 44497,
    86243, 110503, 132049, 216091, 756839, 859433,
    1257787, 1398269, 2976221, 3021377, 6972593,
    13466917, 20996011, 24036583, 25964951, 30402457,
    32582657, 37156667, 42643801, 43112609, 57885161,
    74207281, 77232917, 82589933,
]

check(len(EXPONENTS) == 51, "exponent count", len(EXPONENTS), 51)
check(EXPONENTS[0]  == 2,        "first exponent",  EXPONENTS[0],  2)
check(EXPONENTS[-1] == 82589933, "last exponent",   EXPONENTS[-1], 82589933)


# ── DR functions ──────────────────────────────────────────────────────────────

def dr(n):
    if n == 0:
        return 0
    r = n % 9
    return r if r else 9


# 2^p mod 9 by p mod 6
_POW2_MOD9 = {1: 2, 2: 4, 3: 8, 4: 7, 5: 5, 0: 1}


def dr_mersenne(p):
    """DR(2^p - 1) via modular arithmetic — O(1), works for any exponent."""
    r = (_POW2_MOD9[p % 6] - 1) % 9
    return r if r else 9


def dr_mersenne_direct(p):
    """DR(2^p - 1) by full digit-sum — O(p) digits, use only for small p."""
    return dr(sum(int(d) for d in str((1 << p) - 1)))


# ── Verify analytic = direct for all computable exponents (p ≤ 607) ──────────

SMALL = [p for p in EXPONENTS if p <= 607]

for p in SMALL:
    analytic = dr_mersenne(p)
    direct   = dr_mersenne_direct(p)
    check(
        analytic == direct,
        f"analytic==direct p={p}",
        analytic,
        direct,
    )

check(len(SMALL) == 14, "small exponent count (p ≤ 607)", len(SMALL), 14)


# ── CLAIM D1 / D2: DR determined by p mod 6 ──────────────────────────────────

for p in EXPONENTS:
    expected = dr_mersenne(p)
    if p == 2:
        check(expected == 3, f"D1 p=2 DR=3",  expected, 3)
    elif p == 3:
        check(expected == 7, f"D1 p=3 DR=7",  expected, 7)
    elif p % 6 == 1:
        check(expected == 1, f"D2 p={p} ≡1(6) DR=1", expected, 1)
    elif p % 6 == 5:
        check(expected == 4, f"D2 p={p} ≡5(6) DR=4", expected, 4)
    else:
        FAIL.append(f"Unexpected p%6={p%6} for prime p={p}")


# ── CLAIM D3: DR set ──────────────────────────────────────────────────────────

all_dr = {dr_mersenne(p) for p in EXPONENTS}
check(all_dr == {1, 3, 4, 7}, "D3 DR set", all_dr, {1, 3, 4, 7})


# ── CLAIM D4: exclusion of {2, 5, 6, 8, 9} ───────────────────────────────────

excluded = set(range(1, 10)) - all_dr
check(excluded == {2, 5, 6, 8, 9}, "D4 excluded DRs", excluded, {2, 5, 6, 8, 9})


# ── CLAIM D5: near 1:1 split for p > 3 ───────────────────────────────────────

big = [p for p in EXPONENTS if p > 3]
n_dr1 = sum(1 for p in big if dr_mersenne(p) == 1)
n_dr4 = sum(1 for p in big if dr_mersenne(p) == 4)

check(len(big)  == 49, "p > 3 count",   len(big),  49)
check(n_dr1     == 24, "DR=1 count",    n_dr1,     24)
check(n_dr4     == 25, "DR=4 count",    n_dr4,     25)
check(n_dr1 + n_dr4 == 49, "DR=1+DR=4=49", n_dr1 + n_dr4, 49)
# 24/49 ≈ 48.98% — consistent with primes being ~equidistributed mod 6.
check(abs(n_dr1 / len(big) - 0.5) < 0.02, "DR=1 fraction near 1/2", round(n_dr1/len(big),4), "≈0.5")


# ── Prime DR void consistency ─────────────────────────────────────────────────

# For any Mersenne prime M_p with p > 3, DR must not be in {3, 6, 9}.
for p in big:
    d = dr_mersenne(p)
    check(d not in {3, 6, 9}, f"void check p={p}", d, "not in {3,6,9}")


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Mersenne Prime Digital Root Audit")
    print("=" * 62)

    print(f"\n51 known Mersenne prime exponents; first={EXPONENTS[0]}, last={EXPONENTS[-1]}")

    print(f"\n── DR table (all 51) ──")
    print(f"  {'p':>10}  {'p%6':>4}  {'DR':>3}")
    for p in EXPONENTS:
        print(f"  {p:>10}  {p%6:>4}  {dr_mersenne(p):>3}")

    print(f"\n── Analytic vs direct (p ≤ 607, {len(SMALL)} exponents) ──")
    for p in SMALL:
        a = dr_mersenne(p)
        d = dr_mersenne_direct(p)
        print(f"  p={p:4d}  analytic={a}  direct={d}  {'✓' if a==d else '✗'}")

    print(f"\n── CLAIM D3: DR set ──")
    print(f"  Present:  {sorted(all_dr)}")
    print(f"  Absent:   {sorted(excluded)}")

    print(f"\n── CLAIM D5: split for p > 3 ──")
    print(f"  DR=1: {n_dr1} / {len(big)}  ({100*n_dr1/len(big):.2f}%)  [p ≡ 1 mod 6]")
    print(f"  DR=4: {n_dr4} / {len(big)}  ({100*n_dr4/len(big):.2f}%)  [p ≡ 5 mod 6]")

    print(f"\n── Structural reasons for D4 (exclusions) ──")
    print("  DR ∈ {6,9}: require p ≡ 4 or 0 (mod 6); no prime p > 3")
    print("  DR ∈ {2,5}: require 2^p ≡ 3 or 6 (mod 9); 3,6 ∉ {2,4,8,7,5,1}")
    print("  DR = 8:     requires 2^p ≡ 0 (mod 9); impossible since gcd(2,9)=1")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
