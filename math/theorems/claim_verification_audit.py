# math/theorems/claim_verification_audit.py
"""
Claim Verification Audit
=========================
Verifies claims from the JSON package (2026-05-15) and fixes two bugs
in claim_verification.py supplied with that package.

Bug fixes applied:
  BUG 1: phi_18 == 6 assertion fails in float arithmetic
          (18*(1-1/2)*(1-1/3) = 6.000000000000001 in float64)
          Fix: use integer arithmetic φ(18) = φ(2)×φ(9) = 1×6 = 6
  BUG 2 (from JSON): dr(444) was asserted as 9; correct value is 3
          (4+4+4=12 → 1+2=3)
  BUG 3 (from JSON): date digit sum 2026-05-02 was asserted as 9;
          correct value is 8 (2+0+2+6+0+5+0+2=17 → dr=8)

Claims audited:
  1. Bug fixes on dr(444) and date digit sum
  2. 17/20 = 0.85
  3. 37 mod 18 = 1
  4. 17 mod 18 = 17
  5. λ(37) = λ(17) = -1
  6. Binary λ-vector weight = 20
  7. φ(18) = 6  (integer, not float)
  8. 720 % 18 = 0; 14400 % 18 = 0
  9. Kaprekar 6174: distribution over 8991 four-digit numbers

Unverifiable as stated (logged, not asserted):
  — "Parity structure maps to Steane [7,1,3] code": no derivation supplied
  — "600-cell discrete vertices bridge to Z/18Z": divisibility 18|720 and
    18|14400 are arithmetic facts; no structural connection demonstrated
  — "Identity morphism {+1,-1} → {+1,-1}": tautological, not a claim
"""

import math


# ── helpers ───────────────────────────────────────────────────────────────────

def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


def Omega(n: int) -> int:
    if n == 1:
        return 0
    count = 0
    d = 2
    while d * d <= n:
        while n % d == 0:
            count += 1
            n //= d
        d += 1
    if n > 1:
        count += 1
    return count


def liouville(n: int) -> int:
    return 1 if Omega(n) % 2 == 0 else -1


def kaprekar_steps(n: int) -> int:
    """Steps to reach 6174 from a 4-digit number with ≥2 distinct digits."""
    if n == 6174:
        return 0
    for i in range(8):
        digits = sorted(str(n).zfill(4))
        desc = int(''.join(reversed(digits)))
        asc  = int(''.join(digits))
        n = desc - asc
        if n == 6174:
            return i + 1
    return 8  # should not occur for valid input


def verify():
    print("Claim Verification Audit\n")

    # ── Section 1: Bug fixes ──────────────────────────────────────────────────
    print("=" * 60)
    print("SECTION 1: Bug fixes from JSON package")
    print("=" * 60)

    # BUG 2: dr(444) ≠ 9
    assert dr(444) == 3    # 4+4+4=12 → 1+2=3
    assert 444 == 12 * 37
    print(f"\n  dr(444) = {dr(444)}  (4+4+4=12 → 1+2=3)  ✓")
    print(f"  444 = 12×37  ✓  (DR-3 class via 37-multiple)")
    print(f"  Original (wrong) assertion was dr(444)=9  → corrected to 3")

    # BUG 3: date digit sum 2026-05-02
    date_digits = [2, 0, 2, 6, 0, 5, 0, 2]   # 2026-05-02
    date_sum = sum(date_digits)
    assert date_sum == 17
    assert dr(date_sum) == 8
    print(f"\n  Digit sum of 2026-05-02: {date_sum}  →  dr = {dr(date_sum)}  ✓")
    print(f"  Original (wrong) assertion was dr=9  → corrected to 8")

    # ── Section 2: Arithmetic claims ─────────────────────────────────────────
    print()
    print("=" * 60)
    print("SECTION 2: Arithmetic claims")
    print("=" * 60)

    # CLAIM 2: 17/20 = 0.85  (float equality holds: both round to same IEEE 754 double)
    assert 17 / 20 == 0.85
    print(f"\n  17/20 = 0.85  ✓")

    # CLAIM 3: 37 mod 18 = 1
    assert 37 % 18 == 1
    print(f"  37 mod 18 = {37 % 18}  ✓")

    # CLAIM 4: 17 mod 18 = 17
    assert 17 % 18 == 17
    print(f"  17 mod 18 = {17 % 18}  ✓")

    # CLAIM 5 & 6: λ(37) = λ(17) = -1
    assert Omega(37) == 1 and Omega(17) == 1   # both prime
    assert liouville(37) == -1
    assert liouville(17) == -1
    print(f"  λ(37) = {liouville(37)},  λ(17) = {liouville(17)}  (both prime, Ω=1)  ✓")

    # CLAIM 6: binary λ-vector weight = 20 over n=1..37
    lambda_vec = [0 if liouville(n) == +1 else 1 for n in range(1, 38)]
    weight = sum(lambda_vec)
    assert weight == 20   # consistent with liouville_parity_audit.py
    assert len(lambda_vec) == 37
    print(f"  Binary λ-vector length={len(lambda_vec)}, weight (λ=−1 count)={weight}  ✓")

    # CLAIM 7: φ(18) = 6  — INTEGER arithmetic only
    # φ(18) = φ(2)×φ(3²) = 1×6 = 6  (since 18 = 2×3²)
    # Euler product: 18×(1−1/2)×(1−1/3) = 18×(1/2)×(2/3) = 6
    # BUG in supplied code: float gives 6.000000000000001 ≠ 6
    phi_18_float = 18 * (1 - 1/2) * (1 - 1/3)
    assert phi_18_float != 6                   # demonstrates the float bug
    phi_18_int = 18 * 1 * 2 // (2 * 3)        # integer: 18//2 × 2//3... better:
    phi_18_int = 18 // 2 * 2 // 3 * 1         # = 9 × 2//3 — also fragile
    # Clean: use multiplicativity φ(2)=1, φ(9)=6
    assert math.gcd(2, 9) == 1
    phi_2 = 1     # φ(p) = p-1 for prime p; φ(2)=1
    phi_9 = 6     # φ(3²) = 3²-3 = 6
    phi_18 = phi_2 * phi_9
    assert phi_18 == 6
    print(f"  φ(18) = φ(2)×φ(9) = 1×6 = {phi_18}  ✓  (integer arithmetic)")
    print(f"  FIXED: float formula gives {phi_18_float} ≠ 6  (rounding error)")

    # CLAIM 8: 600-cell / 120-cell symmetry group divisibilities
    # |H₄| = 14400 (symmetry group of 600-cell and 120-cell)
    # 720 = edge count of 600-cell = face count of 120-cell
    assert 720 % 18 == 0
    assert 14400 % 18 == 0
    print(f"\n  720 % 18 = {720 % 18}  ✓  (720 = 40×18; edges of 600-cell)")
    print(f"  14400 % 18 = {14400 % 18}  ✓  (14400 = 800×18; |H₄| symmetry group)")

    # ── Section 3: Kaprekar 6174 statistics ──────────────────────────────────
    print()
    print("=" * 60)
    print("SECTION 3: Kaprekar 6174 — step distribution over 4-digit numbers")
    print("=" * 60)

    dist = {}
    total = 0
    step_sum = 0
    for n in range(1000, 10000):
        if len(set(str(n))) == 1:
            continue   # skip repdigits (1111, 2222, ..., 9999)
        s = kaprekar_steps(n)
        dist[s] = dist.get(s, 0) + 1
        total += 1
        step_sum += s

    expected_dist = {0: 1, 1: 356, 2: 519, 3: 2124,
                     4: 1124, 5: 1379, 6: 1508, 7: 1980}
    assert total == 8991
    assert dist == expected_dist
    assert max(dist) == 7

    mean_steps = step_sum / total
    assert abs(mean_steps - 4.679) < 0.001

    print(f"\n  Numbers tested: {total}  ✓")
    print(f"  Max steps: {max(dist)}  ✓")
    print(f"  Mean steps: {mean_steps:.3f}  ✓")
    print(f"  Step distribution:")
    for k in sorted(dist):
        pct = dist[k] / total * 100
        print(f"    steps={k}: {dist[k]:5d}  ({pct:.2f}%)")

    assert dist[3] == 2124   # peak at steps=3
    assert dist[7] == 1980   # second peak at steps=7
    print(f"\n  Peak at steps=3: {dist[3]} numbers  ✓")
    print(f"  Second peak at steps=7: {dist[7]} numbers ({dist[7]/total*100:.2f}%)  ✓")
    print(f"  n=6174 itself: steps=0 (already fixed point)  ✓")

    # ── Section 4: Unverifiable claims (logged) ───────────────────────────────
    print()
    print("=" * 60)
    print("SECTION 4: Unverifiable claims")
    print("=" * 60)
    print("""
  STEANE CODE BRIDGE:
    Claim: λ-vector parity maps to Steane [7,1,3] code stabilizers.
    Status: UNVERIFIABLE as stated.
    The λ-vector has length 37, not 7. Encoding {+1,-1} as {0,1} over F₂
    is trivially possible for any function. No specific connection to the
    Steane code's [7,1,3] parameters or its stabilizer generators is
    supplied or derivable from the parity counts alone.

  600-CELL / Z/18Z BRIDGE:
    Claims: 720 and 14400 divisible by 18; connection to Z/18Z.
    Arithmetic: 18|720 and 18|14400 are correct (verified above).
    Status: DIVISIBILITY ONLY — no structural connection established.
    That 720 and 14400 are divisible by 18 does not constitute a bridge
    between the parity domain and 4D polytope geometry. Many numbers
    divisible by 18 have no connection to the 600-cell.

  IDENTITY MORPHISM {+1,−1} → {+1,−1}:
    Status: TAUTOLOGICAL. Every function on {+1,−1} is a self-map.
    Not a meaningful claim.
    """)

    # ── Summary ───────────────────────────────────────────────────────────────
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"""
  BUG FIXES:
    dr(444) = 3  (not 9)  ✓
    date_sum(2026-05-02) = 8  (not 9)  ✓
    phi_18 float assertion fails (6.000000000000001 ≠ 6) — fixed to int  ✓

  CLAIMS VERIFIED:
    17/20 = 0.85  ✓
    37 mod 18 = 1  ✓
    17 mod 18 = 17  ✓
    λ(37) = λ(17) = -1  ✓
    Binary λ-vector weight = 20  ✓
    φ(18) = 6  (integer arithmetic)  ✓
    720 % 18 = 0;  14400 % 18 = 0  ✓
    Kaprekar step distribution over 8991 numbers  ✓

  UNVERIFIABLE:
    Steane code bridge  — no derivation supplied
    600-cell bridge    — divisibility ≠ structural connection
    Identity morphism  — tautological
    """)

    print("All assertions passed.")


if __name__ == "__main__":
    verify()
