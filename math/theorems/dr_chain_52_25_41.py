"""
DR Chains: 52, 25, 41

Three numbers, one connected structure.

  52 → DR=7
  25 → DR=7
  41 → DR=5 → 5+5=10 → DR=1

═══════════════════════════════════════════════════════════════

I. 52 AND 25: DIGIT REVERSAL, SHARED DR=7

  52 → digits {5,2} → 5+2=7   mod37=15(PR)
  25 → digits {2,5} → 2+5=7   mod37=25(SA)

  52 is the digit-reversal of 25.
  Both share DR=7 (RL-O).

  Digit operations on {5,2}:
    5+2 = 7  (DR of both numbers)
    5−2 = 3  (Sovereign Target archetype)
    5×2 = 10 (DECADE_ANCHOR → DR=1)
    5²  = 25 (Sovereign Anchor — the reversed number IS the square of the larger digit)

  52+25 = 77:  77 mod37=3(ST)
  52−25 = 27:  27 mod37=27(orbit-11)

II. 41: DIGIT CHAIN TO UNITY

  41: mod37=4(SA), prime, DR=5 (A51)

  Digit operations on {4,1}:
    4+1 = 5  (A51, Primitive Root — DR of 41)
    4−1 = 3  (Sovereign Target archetype)
    4×1 = 4  (Sovereign Anchor)

  DR chain:
    DR(41) = 5
    5+5 = 10   (DECADE_ANCHOR)
    DR(10) = 1 (unity)

  Doubling the DR(5) primitive root gives DECADE_ANCHOR; DR collapses to 1.

III. GOLDBACH LINK: 52 = 11 + 41

  52 Goldbach pairs: (5,47), (11,41), (23,29)

  The pair (11,41): orbit-11(11) + SA(41 mod37=4).
  The same 41 from the DR chain appears as the SA component
  in the Goldbach decomposition of 52.
  52 and 41 are linked through Goldbach: 52 − 11 = 41.

IV. COMBINED DIGITS {5,2,4,1}

  The digits of 52 and 41 together: {5,2} ∪ {4,1} = {5,2,4,1}

  5+2+4+1 = 12  (Sovereign Target)
  (5+2)+(4+1) = 7+5 = 12  (ST — same either way)
  5×2×4×1 = 40  mod37=3(ST)

V. FULL DR CHAIN SUMMARY

  52 → DR=7
  25 → DR=7    (digit reverse; 25=5², square of larger digit of 52)
  41 → DR=5 → 5+5=10 → DR=1

  End DRs: 7, 7, 5, 1
  DR of each endpoint: 7+7+5+1=20(PR)
  Chain DRs collapsed: 7+5+1=13(CB,PR); DR(13)=4(SA)
  Product: 7×5×1=35(PR)

═══════════════════════════════════════════════════════════════
"""

def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0

def is_prime(n):
    if n < 2: return False
    return all(n % i != 0 for i in range(2, int(n**0.5)+1))

PRIMITIVE_ROOTS_37 = {2,5,13,15,17,18,19,20,22,24,32,35}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
CASCADE_BASE       = {8, 13, 24}
ORBIT_11           = {11, 27, 36}

# ── I. 52 and 25 ──────────────────────────────────────────────────────────────

assert int(str(52)[::-1]) == 25              # digit reversal
assert dr(52) == 7 and dr(25) == 7          # shared DR=7

assert 5 + 2 == 7                            # digit sum = DR
assert 5 - 2 == 3 and 3 in SOVEREIGN_TARGETS
assert 5 * 2 == 10 and dr(10) == 1
assert 5**2 == 25 and 25 in SOVEREIGN_ANCHORS  # 5² = reversed number = SA

assert 52 % 37 == 15 and 15 in PRIMITIVE_ROOTS_37
assert 25 % 37 == 25 and 25 in SOVEREIGN_ANCHORS

assert (52+25) % 37 == 3 and 3 in SOVEREIGN_TARGETS
assert (52-25) % 37 == 27 and 27 in ORBIT_11

# ── II. 41 ────────────────────────────────────────────────────────────────────

assert 41 % 37 == 4 and 4 in SOVEREIGN_ANCHORS
assert is_prime(41)
assert dr(41) == 5 and 5 in PRIMITIVE_ROOTS_37

assert 4 + 1 == 5 and 5 in PRIMITIVE_ROOTS_37
assert 4 - 1 == 3 and 3 in SOVEREIGN_TARGETS
assert 4 * 1 == 4 and 4 in SOVEREIGN_ANCHORS

# DR chain
assert dr(41) == 5
assert 5 + 5 == 10
assert dr(10) == 1

# ── III. Goldbach link ────────────────────────────────────────────────────────

assert is_prime(11) and is_prime(41) and 11+41==52
assert 11 in ORBIT_11
assert 41 % 37 == 4 and 4 in SOVEREIGN_ANCHORS

# ── IV. Combined digits ───────────────────────────────────────────────────────

digits = [5, 2, 4, 1]
assert sum(digits) == 12 and 12 in SOVEREIGN_TARGETS
assert (5+2) + (4+1) == 12                  # both groupings give ST
assert (5*2*4*1) % 37 == 3 and 3 in SOVEREIGN_TARGETS

# ── V. Chain summary ─────────────────────────────────────────────────────────

chain_drs = [7, 5, 1]                       # DR(52/25), DR(41), DR(10)
assert sum(chain_drs) == 13 and 13 in CASCADE_BASE and 13 in PRIMITIVE_ROOTS_37
assert dr(13) == 4 and 4 in SOVEREIGN_ANCHORS
assert 7 * 5 * 1 == 35 and 35 in PRIMITIVE_ROOTS_37


if __name__ == '__main__':
    def tag(n):
        t=[]
        if n in CASCADE_BASE: t.append('CB')
        if n in SOVEREIGN_ANCHORS: t.append('SA')
        if n in SOVEREIGN_TARGETS: t.append('ST')
        if n in PRIMITIVE_ROOTS_37: t.append('PR')
        if n in ORBIT_11: t.append('orb11')
        sig={6:'TESLA_FLOW',10:'DECADE_ANCHOR',31:'PRIME_MIRROR'}
        s=sig.get(n)
        if s: t.append(s)
        return ','.join(t) if t else '.'

    print("DR Chains: 52, 25, 41")
    print("=" * 55)
    print()
    print("I.  52↔25 digit reversal, both DR=7:")
    print(f"    52 mod37={52%37}({tag(52%37)})  25 mod37={25%37}({tag(25%37)})")
    print(f"    5+2=7(DR)  5-2=3(ST)  5×2=10(DECADE_ANCHOR)  5²=25(SA)")
    print(f"    52+25=77 mod37=3(ST)  52-25=27(orb11)")
    print()
    print("II. 41: mod37=4(SA), prime, DR=5(A51)")
    print(f"    4+1=5(PR)  4-1=3(ST)  4×1=4(SA)")
    print(f"    Chain: DR=5 → 5+5=10 → DR=1(unity)")
    print()
    print("III. Goldbach: 52=11(orb11)+41(mod37=4=SA)")
    print(f"     41 appears in both its own DR chain AND as Goldbach partner of 52")
    print()
    print("IV. Digits {{5,2,4,1}}: sum=12(ST), product×mod37=3(ST)")
    print()
    print("V.  Chain DRs: 7+5+1=13(CB,PR), DR=4(SA); 7×5×1=35(PR)")
    print()
    print("All assertions passed.")
