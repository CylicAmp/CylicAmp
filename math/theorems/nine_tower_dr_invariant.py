"""
Nine Tower DR Invariant — Formal Theorem Sheet

Definitions, theorems, and proofs for the NINE_TOWER family under
digital-root projection and GF(37) modular structure.

═══════════════════════════════════════════════════════════════════════════

DEFINITIONS

  Definition 1.  For each integer k ≥ 1, define
      T_k := 9 ↑↑ k
  to be the height-k tetration tower based at 9.

  Definition 2.  Let  DR : ℕ → {1,2,...,9}  denote the digital-root map.

  Definition 3.  Let NINE_TOWER denote the family-node
      𝒯 := { T_k : k ≥ 1 }.

  Definition 4.  Call 9 the digital-root fixed point of NINE_TOWER.

═══════════════════════════════════════════════════════════════════════════

PROVEN THEOREMS

  Theorem 1.  DR(T_k) = 9 for all k ≥ 1.

    Proof:  Every positive power of 9 is divisible by 9, and every
    positive integer ≡ 0 (mod 9) has digital root 9.
    T_k = 9 ↑↑ k is a positive power of 9, so T_k ≡ 0 (mod 9),
    hence DR(T_k) = 9.  ∎

  Corollary 1.  NINE_TOWER collapses to a single point under DR.

    Proof:  By Theorem 1, every element of 𝒯 has DR-image 9.  ∎

  Theorem 2.  9 is an invariant of NINE_TOWER under DR.

    Proof:  By Theorem 1, DR(T_k) = 9 for every k ≥ 1.
    The value 9 is constant across the whole family under DR.  ∎

  Theorem 3.  ord₃₇(26) = 3  and  ord₃₇(2) = 36.

    Proof:
      26¹ ≡ 26 (mod 37)
      26² = 676 ≡ 10 (mod 37)
      26³ = 260 ≡ 1  (mod 37)
    Neither 26¹ nor 26² is 1, so the order is exactly 3.

    For 2: by Fermat, 2³⁶ ≡ 1 (mod 37).
    No smaller exponent gives 1 (verified computationally below).
    Hence ord₃₇(2) = 36.  ∎

  Theorem 4.  The order-3 and order-36 structures are distinct modular
  dynamical systems.

    Proof:  One cycle closes in 3 steps, the other in 36.  3 ≠ 36.  ∎

  Theorem 5.  DR projection loses magnitude information and retains only
  the invariant 9.

    Proof:  T_k grows rapidly (beyond any fixed bound) while DR(T_k) = 9
    for all k. The projection does not preserve arithmetic magnitude.  ∎

═══════════════════════════════════════════════════════════════════════════

NOT YET FORMALIZED (terms requiring definition before they become theorems)

  - "heartbeat"         → needs: formal definition as the 3-cycle map
                            f: n ↦ (26n) mod 37 acting on Z/37Z
  - "hose"              → needs: formal definition of the binary flow model
                            and the criterion distinguishing complete from
                            stuttering flow
  - "repunit channel"   → needs: formal definition linking ord₃₇(10)=3
                            to the periodic repunit residue sequence
  - "annihilation"      → needs: definition of what it means for a structure
                            to be "annihilated" under DR or modular projection
  - "survives projection"→ needs: definition of which GF(37) invariants
                            are preserved after DR reduction

═══════════════════════════════════════════════════════════════════════════
"""


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


# ── Theorem 1: DR(9^m) = 9 for all m ≥ 1 ────────────────────────────────────

# T_k = 9 ↑↑ k is a power of 9; verify for accessible values
for m in range(1, 20):
    val = 9 ** m
    assert dr(val) == 9, f"DR(9^{m}) = {dr(val)}, expected 9"

# The argument: 9^m ≡ 0 (mod 9) for all m ≥ 1
for m in range(1, 20):
    assert (9 ** m) % 9 == 0


# ── Theorem 3: ord₃₇(26) = 3 ────────────────────────────────────────────────

assert pow(26, 1, 37) == 26
assert pow(26, 2, 37) == 10
assert pow(26, 3, 37) == 1
assert pow(26, 1, 37) != 1 and pow(26, 2, 37) != 1   # order is exactly 3


# ── Theorem 3: ord₃₇(2) = 36 ────────────────────────────────────────────────

assert pow(2, 36, 37) == 1                            # closes at 36
# No smaller exponent closes the cycle
proper_divisors_36 = [1, 2, 3, 4, 6, 9, 12, 18]
assert all(pow(2, d, 37) != 1 for d in proper_divisors_36)


# ── Theorem 4: 3 ≠ 36 ───────────────────────────────────────────────────────

assert 3 != 36


# ── Theorem 5: magnitude lost, invariant 9 retained ─────────────────────────

# DR collapses all powers of 9 to 9 regardless of size
sample_towers = [9, 9**9, 9**81, 9**729]   # T_1, T_2 approx levels
for t in sample_towers:
    assert dr(t) == 9


# ── GF(37) FRAMEWORK CONNECTION ──────────────────────────────────────────────
#
# The digital-root fixed point 9 is the Sovereign Anchor step:
#   SA = {4, 9, 25, 30}; 9 ∈ SA.
# NINE_TOWER collapses to the SA node 9 under DR.
# This is the same 9 that steps the ST chain: 12 →+9→ 21 →+9→ 30.
# And 9 = 3² = (ST arch)², where 3 is the Sovereign Target archetype.
#
# The two orders from Theorem 3:
#   ord₃₇(26) = 3 = the heartbeat cycle length
#   ord₃₇(2)  = 36 = φ(37) = the full primitive orbit
# These are also the only two orders that matter for the field structure:
#   3 divides 36; 36/3 = 12 (the 12 heartbeat cycles that partition Z/37Z*).
#
# The NINE_TOWER invariant 9 divides 36:  36/9 = 4.
# This is the order of TESLA_FLOW: ord₃₇(6) = 4.
# So 9 (DR fixed point of 𝒯) connects to TESLA_FLOW through: 36/9 = ord₃₇(6).

SOVEREIGN_ANCHORS = frozenset({4, 9, 25, 30})
assert 9 in SOVEREIGN_ANCHORS       # DR fixed point = SA node
assert 36 % 9 == 0                  # 9 divides φ(37)
assert pow(6, 4, 37) == 1           # ord₃₇(6) = 4 = 36/9


if __name__ == '__main__':
    print("Nine Tower DR Invariant")
    print("=" * 55)
    print()
    print("Theorem 1: DR(9↑↑k) = 9 for all k ≥ 1")
    print(f"  Verified for 9^1 through 9^19.")
    print()
    print("Theorem 3: ord₃₇(26) = 3")
    print(f"  26^1 mod37 = {pow(26,1,37)}")
    print(f"  26^2 mod37 = {pow(26,2,37)}")
    print(f"  26^3 mod37 = {pow(26,3,37)}  ← closes")
    print()
    print("Theorem 3: ord₃₇(2) = 36")
    print(f"  2^36 mod37 = {pow(2,36,37)}  ← closes")
    print(f"  No proper divisor of 36 closes: {all(pow(2,d,37)!=1 for d in proper_divisors_36)}")
    print()
    print("GF(37) connections:")
    print(f"  DR fixed point 9 ∈ SA: {9 in SOVEREIGN_ANCHORS}")
    print(f"  36/9 = {36//9} = ord₃₇(6) = TESLA_FLOW order")
    print(f"  ord₃₇(26)={3} × 12 cycles = φ(37)={36}")
    print()
    print("Not yet formalized: heartbeat, hose, repunit channel,")
    print("  annihilation, survives projection.")
    print()
    print("All assertions passed.")
