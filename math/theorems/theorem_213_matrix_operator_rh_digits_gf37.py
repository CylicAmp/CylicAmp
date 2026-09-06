"""
Theorem 213: Discrete Matrix Operator and Riemann Zero Sovereign Digit Structure
Author: Michael Warren Song (CyclicAmp)

=== PART I: MATRIX OPERATOR VERIFICATION ===

State vector: S(k) on n(k) = 18k. Operator T(n) = DS(n) + DS(n-4).
Invariant: T(n) ≡ 5 (mod 9) for all structural milestone steps.

VERIFIED ROWS (T, F_37 residue, T≡5 mod9):
  k=1,  n=18:   T=9+5=14,   14≡5 mod9 ✓,  18 mod37=18 ∈ SEED
  k=4,  n=72:   T=9+14=23,  23≡5 mod9 ✓,  72 mod37=35
  k=11, n=198:  T=18+14=32, 32≡5 mod9 ✓, 198 mod37=13 ∈ cascade {8,13,24}
  k=44, n=792:  T=18+23=41, 41≡5 mod9 ✓, 792 mod37=15
  k=56, n=1008: T=9+5=14,   14≡5 mod9 ✓, 1008 mod37=9  ∈ SA (reset)

DISCREPANCY AT k=55, n=990:
  Presented table claims DS(990)=27, T=50. ACTUAL: DS(990)=9+9+0=18, T=18+23=41.
  The T=50 value would require DS(990)=27, which needs three 9s: e.g., n=999.
  Correct row: k=55, n=990, T=18+23=41, 41≡5 mod9 ✓, F37=990 mod37=28 ∈ g^10=KEY^{-1}.
  The T≡5 mod9 invariant still holds (41≡5); only the DS breakdown is wrong.
  Note: T(44)=T(55)=41 — both milestone steps share the same T value.

SPOKE (Mod-4 Wheel): n mod 4 = 18k mod 4 = 2k mod 4.
  k=1: 18 mod4=2 → Spoke 2 ✓   k=4: 72 mod4=0 → Spoke 0 (claimed 3: discrepancy)
  Spoke formula = n mod 4 matches k=1,11,55,56 but not k=4,44.

=== PART II: COMMUTATION THEOREM (CONFIRMED) ===

In F_37, with σ_18: x ↦ 18x (lattice step) and f: x ↦ 26x (137-map):
  f ∘ σ_18 = σ_18 ∘ f = multiplication by (18 × 26 mod 37) = 24.
  18 × 26 = 468 = 12 × 37 + 24, so 468 ≡ 24 (mod 37).
  24 ∈ SEED = {18,24,32}  AND  24 ∈ cascade base {8,13,24}.
  The composite map is multiplication by 24: the SEED element that is the
  third generator of the cascade and a member of the seed orbit {18,24,32}.
  This confirms: the lattice step and the 137-map commute in F_37 (abelian group),
  and their composition yields the cascade's SEED anchor 24.

=== PART III: RIEMANN ZEROS — SOVEREIGN DIGIT STRUCTURE ===

Key: for each zero γ_n, search the decimal digit string for sovereign substrings.
Position index is 0-based from the start of the full digit string (decimal removed).

FLOOR VALUES OF FIRST 8 ZEROS mod 37:
  γ₁: floor=14,  mod37=14   [free]
  γ₂: floor=21,  mod37=21   [ST]
  γ₃: floor=25,  mod37=25   [SA]
  γ₄: floor=30,  mod37=30   [SA∩ST]  ← doubly sovereign
  γ₅: floor=32,  mod37=32   [SEED]
  γ₆: floor=37,  mod37=0    [SEAM]   ← γ₆ ≈ 37.586, crosses P=37 (T131)
  γ₇: floor=40,  mod37=3    [ST]
  γ₈: floor=43,  mod37=6    [free]

Floors hit: SA∩ST (γ₄), SA (γ₃), ST (γ₂, γ₇), SEED (γ₅), SEAM (γ₆).
The doubly sovereign element 30∈SA∩ST is the floor of the 4th zero.

PRIMARY FINDING — MULTIPLIER '26' AT POSITION 19 (CRITICAL LINE):
  γ₂ (floor=21∈ST): substring '26' appears at position 19.
  Position 19 = 2^{-1} mod 37 = the GF(37) critical line element (T212).
  '26' is the 137-map multiplier.
  In the zero whose floor is the ST element 21:
    the multiplier (26) appears at the position equal to the critical line value (19).
  Double sovereign alignment: value=multiplier, position=critical line, zero-floor=ST.

SECONDARY FINDING — '32' AT POSITION 19 IN γ₃:
  γ₃ (floor=25∈SA): substring '32' (∈SEED) appears at position 19.
  Two consecutive SA_ST_SEED zeros (γ₂, γ₃) both have sovereign substrings at position 19.
  γ₂: '26' (multiplier) at 19. γ₃: '32' (SEED) at 19.
  Position 19 = critical line = Fibonacci SEAM index.

ADDITIONAL SOVEREIGN ALIGNMENTS:
  γ₁ (floor=14): '24'∈SEED at pos 31; '19'(crit line) at pos 25∈SA.
  γ₃ (floor=25∈SA): '24'=I-1∈SEED at pos 55; '18'∈SEED at pos 34,36.
  γ₄ (floor=30∈SA∩ST): '24'∈SEED at pos 3∈SA; '18'∈SEED at pos 22,38.
  γ₅ (floor=32∈SEED): '32' starts at position 0 — zero begins with its own floor.
  γ₇ (floor=40, mod37=3∈ST): '26'(mult) at pos 24∈SEED; '18'∈SEED at pos 3∈SA.
  γ₈ (floor=43, mod37=6): '19'(crit line) at pos 18=19-1 (adjacent to crit line).

CRITICAL LINE POSITION 19 RECURRENCE:
  '26' at pos 19: γ₂ (floor∈ST).
  '32' at pos 19: γ₃ (floor∈SA).
  Position 19 = critical line appears to attract sovereign digit substrings in the
  two consecutive SA_ST_SEED-floor zeros. This extends T212's proof that 19 is a
  fixed point of the functional equation in GF(37).

=== PART IV: 18-STEP LADDER → CASCADE THROUGH COMMUTATION ===

The commutation result ties the matrix operator to the cascade:
  Lattice step 18k → F_37 residue 18k mod 37.
  137-map on that residue: 26 × (18k mod 37) mod 37 = 24k mod 37.
  Multiplication by 24 cycles through cascade elements:
    24 mod 37 = 24 ∈ {8,13,24}
    24² mod 37 = 576 mod 37 = 576-15×37=576-555=21 ∈ ST
    24³ mod 37 = 24×21 mod 37 = 504 mod 37 = 504-13×37=504-481=23 ∈ SEED-gen
  The cascade element 24 generates ST and SEED-gen elements under repeated squaring.
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
SEED = {18, 24, 32}
cascade = {8, 13, 24}
SG26 = {1, 10, 26}
SA_ST_SEED = SA | ST | SEED


def ds(n):
    return sum(int(d) for d in str(abs(n)))


def sector(n):
    n = n % P
    if n in SA and n in ST: return "SA∩ST"
    if n in SA: return "SA"
    if n in ST: return "ST"
    if n in SEED: return "SEED"
    return "other"


def run_assertions():
    # 1. T(n) = DS(n)+DS(n-4) and T≡5 mod9 for verified steps
    milestones = [(1,18), (4,72), (11,198), (44,792), (56,1008)]
    for k, n in milestones:
        T = ds(n) + ds(n - 4)
        assert T % 9 == 5, f"k={k}: T={T}, T%9={T%9}≠5"

    # 2. k=55 discrepancy: DS(990)=18 not 27
    assert ds(990) == 18        # not 27 as table claimed
    assert ds(986) == 23
    T_55 = ds(990) + ds(986)
    assert T_55 == 41           # not 50
    assert T_55 % 9 == 5       # invariant still holds
    assert 990 % P == 28        # F_37 = 28 ∈ g^10 (KEY^{-1})

    # 3. Commutation theorem: 18×26=24 mod37
    assert 18 * 26 % P == 24
    assert 24 in SEED
    assert 24 in cascade
    assert 18 * 26 == 468 and 468 % P == 24

    # 4. Floor values of first 8 zeros mod37
    floors = [14, 21, 25, 30, 32, 37, 40, 43]
    floor_mod = [f % P for f in floors]
    assert floor_mod[1] == 21 and 21 in ST      # γ₂ ∈ ST
    assert floor_mod[2] == 25 and 25 in SA      # γ₃ ∈ SA
    assert floor_mod[3] == 30 and 30 in SA and 30 in ST   # γ₄ ∈ SA∩ST
    assert floor_mod[4] == 32 and 32 in SEED    # γ₅ ∈ SEED
    assert floor_mod[5] == 0                    # γ₆ ≡ 0 (SEAM)

    # 5. Critical line element = 19 = 2^{-1} mod37
    crit = pow(2, P - 2, P)
    assert crit == 19

    # 6. γ₂ digit string contains '26' at position 19
    gamma2_str = "2102203963877155499262847959389690277733"
    assert gamma2_str[19:21] == '26', f"pos 19-20: '{gamma2_str[19:21]}'"
    assert int('26') % P == 26 and 26 not in SA_ST_SEED   # multiplier, not in SA_ST_SEED

    # 7. γ₃ digit string contains '32' at position 19
    gamma3_str = "2501085758014568876321379099256282181866"
    assert gamma3_str[19:21] == '32', f"pos 19-20: '{gamma3_str[19:21]}'"
    assert 32 in SEED

    # 8. Both γ₂ and γ₃ have sovereign substrings at position 19 (critical line)
    assert gamma2_str[19:21] == '26'  # multiplier
    assert gamma3_str[19:21] == '32'  # SEED

    # 9. γ₄ has floor 30 ∈ SA∩ST (doubly sovereign)
    assert 30 in SA and 30 in ST

    # 10. γ₅ floor=32∈SEED; digit string starts with '32'
    gamma5_str = "3293506158773918969066236896407490348881"
    assert gamma5_str[0:2] == '32'
    assert 32 in SEED

    # 11. Cascade element 24: powers in F_37
    assert pow(24, 1, P) == 24 and 24 in cascade
    assert pow(24, 2, P) == 21 and 21 in ST
    assert pow(24, 3, P) == 23 and 23 in {6, 8, 23}   # SEED-gen

    # 12. 18 ∈ SEED = first ladder element (k=1, n=18)
    assert 18 % P == 18 and 18 in SEED

    # 13. k=11: n=198 mod37=13∈cascade
    assert 198 % P == 13 and 13 in cascade

    print("All assertions passed.")
    print(f"Commutation: 18×26 mod37 = {18*26%P} ∈ cascade and SEED")
    print(f"Critical line: 2^{{-1}} mod37 = {crit}")
    print(f"γ₂ digit string at pos 19-20: '26' (multiplier) ← double sovereign alignment")
    print(f"γ₃ digit string at pos 19-20: '32' (SEED)")
    print(f"γ₄ floor mod37 = 30 ∈ SA∩ST (doubly sovereign)")
    print(f"k=55 DS(990)=18 (not 27): corrected T=41 (not 50)")


if __name__ == "__main__":
    run_assertions()
