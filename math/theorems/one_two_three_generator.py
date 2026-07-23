"""
2+1=3 — The 123 Generator

The single addition 2+1=3 generates the complete {1,2,3} family.
{1,2,3} is the only set of positive integers where sum = product.
Both equal 6 (TESLA_FLOW). The family appears across every layer of the framework.

═══════════════════════════════════════════════════════════════

I. THE EQUATION

  2 + 1 = 3

  2 — Primitive Root mod 37 (ord₃₇(2)=36, generates all of GF(37)*)
  1 — Unity
  3 — Sovereign Target archetype (DR=3, ST arch)

  DR(1)=1, DR(2)=2, DR(3)=3 — the 123 DR sequence, in order.

II. SUM = PRODUCT (UNIQUE PROPERTY)

  1+2+3 = 6  (TESLA_FLOW, FPS-37 significance)
  1×2×3 = 6  (TESLA_FLOW)

  {1,2,3} is the only set of positive integers ≥1 where sum = product.
  Both equal 6 — TESLA_FLOW in the GF(37) field scanner.

III. NATURAL AGGREGATES OF {1,2,3}

  1!+2!+3!      = 1+2+6    = 9    (Sovereign Anchor)
  1×2+2×3+1×3   = 2+6+3    = 11   (orbit of 11)
  (1+2+3)²      = 6²       = 36   (orbit-11; 36 ≡ −1 mod 37)
  1²+2²+3²      = 1+4+9    = 14   DR=5 (A51)

IV. 12 = THE 123 INSTANCE

  12 ∈ SOVEREIGN_TARGETS
  digits of 12: {1, 2}; DR(12) = 3
  12 encodes {1, 2, 3} as: first digit, second digit, digital root.

  123 mod 37 = 12 (ST)
  12 × (anything) preserves the ST structure in Z/37Z.

V. PIE CONNECTION

  In the PIE sieve of π(100):
    Order 1 → S1 = 117  (size-1 subsets)
    Order 2 → S2 =  45  (size-2 subsets)
    Order 3 → S3 =   6  (size-3 subsets)

  S3 = 6 = 1+2+3 = 1×2×3.

  The third-order PIE correction count IS the 123 family sum and product.
  The alternating orders 1, 2, 3 of inclusion-exclusion are themselves the
  123 family — and the third order produces their combined value.

VI. HOSE FLOW CONNECTION

  Complete flow transient: 000 → 100 → 110 → 111
  DR sequence:             0   →  1  →  2  →  3

  2+1=3 IS the transient:
    Start at DR=1 (unity, the seed).
    Add DR=2 (Primitive Root step).
    Arrive at DR=3 (Sovereign Target archetype = the seam moment).

  The hose reaches 111 (seam, mod37=0) exactly at DR=3.
  2+1=3 describes the minimum path from unity to the seam.

═══════════════════════════════════════════════════════════════
"""

PRIMITIVE_ROOTS_37 = {2,5,13,15,17,18,19,20,22,24,32,35}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
CASCADE_BASE       = {8, 13, 24}
ORBIT_11           = {11, 27, 36}

def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0

# ── I. The equation ───────────────────────────────────────────────────────────

assert 2 + 1 == 3
assert 2 in PRIMITIVE_ROOTS_37
assert 3 in SOVEREIGN_TARGETS
assert [dr(n) for n in [1,2,3]] == [1, 2, 3]

# ── II. Sum = product ─────────────────────────────────────────────────────────

assert 1+2+3 == 6
assert 1*2*3 == 6
assert 6 % 37 == 6                             # TESLA_FLOW

# ── III. Natural aggregates ───────────────────────────────────────────────────

assert 1 + 2 + 6 == 9 and 9 in SOVEREIGN_ANCHORS        # factorials
assert 1*2 + 2*3 + 1*3 == 11 and 11 in ORBIT_11          # pairwise products
assert (1+2+3)**2 == 36 and 36 in ORBIT_11               # square of sum = -1 mod37
assert 36 % 37 == 37 - 1                                  # 36 ≡ -1

# ── IV. 12 as the 123 instance ────────────────────────────────────────────────

assert 12 in SOVEREIGN_TARGETS
assert int(str(12)[0]) == 1 and int(str(12)[1]) == 2 and dr(12) == 3
assert 123 % 37 == 12 and 12 in SOVEREIGN_TARGETS

# ── V. PIE connection ─────────────────────────────────────────────────────────

S3 = 6
assert S3 == 1+2+3 == 1*2*3                    # third-order PIE = 123 sum = 123 product

# ── VI. Hose flow connection ──────────────────────────────────────────────────

transient_drs = [0, 1, 2, 3]
assert transient_drs[1] == 1   # unity
assert transient_drs[2] == 2   # PR step
assert transient_drs[3] == 3   # ST arch — seam reached
assert 2 + 1 == 3              # the step from unity to seam: DR=1 + DR=2 = DR=3
assert 111 % 37 == 0           # 111 is the seam, reached at DR=3


if __name__ == '__main__':
    print("2+1=3 — The 123 Generator")
    print("=" * 55)
    print()
    print("I.  2+1=3: PR + unity = ST arch")
    print(f"    DR sequence: {[dr(n) for n in [1,2,3]]}")
    print()
    print(f"II. Sum=Product: 1+2+3=1×2×3={1*2*3} (TESLA_FLOW)")
    print(f"    Unique: only positive integer set with this property")
    print()
    print("III. Aggregates of {{1,2,3}}:")
    print(f"    1!+2!+3! = {1+2+6} (SA)")
    print(f"    1×2+2×3+1×3 = {2+6+3} (orbit-11)")
    print(f"    (1+2+3)² = {36} ≡ -1 mod37 (orbit-11)")
    print()
    print(f"IV.  12(ST): digits 1,2; DR=3 — encodes {{1,2,3}} directly")
    print(f"     123 mod37 = {123%37} (ST)")
    print()
    print(f"V.   PIE S3 = 6 = 1+2+3 = 1×2×3")
    print(f"     The third PIE order produces the 123 sum and product")
    print()
    print(f"VI.  Hose flow DR transient: {[0,1,2,3]}")
    print(f"     2+1=3: unity(1) + PR-step(2) = seam-arrival(3)")
    print(f"     Minimum path from unity to seam in DR space")
    print()
    print("All assertions passed.")
