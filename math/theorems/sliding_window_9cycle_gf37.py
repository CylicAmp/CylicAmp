"""
Sliding Window 9-Cycle — GF(37) Structure

The digit sequence 1,2,3,4,5,6,7,8,9,1,2,... (cyclic, using DR arithmetic where 9+1=1)
generates a 9-element cycle of 3-digit windows under digit-wise +1.

Each window = 3 consecutive digits; step = 111 = 3×37 for windows 1–7.
At the wrap boundary (7→8→9) the arithmetic step changes.

═══════════════════════════════════════════════════════════════

I. THE 9-CYCLE

  123 → 234 → 345 → 456 → 567 → 678 → 789
  all ≡ 12 mod 37  (Sovereign Target)
  step = 111 = 3×37 = SEAM × 3  (each step is a seam multiple)

  789 → 891:  step = 102,  102 mod37 = 28  (no name)
  891 → 912:  step =  21,  21 mod37 = 21   (ST — Sovereign Target)
  912 → 123:  digit-wrap closes the cycle

  912 mod 37 = 24  (CB, PR, SEED_ORBIT)
  891 mod 37 =  3  (ST arch)

  Elements 1–7: all ≡ 12(ST) — the ST chain holds for seven steps.
  Element 8 (891): drops to 3(ST arch) — the archetype.
  Element 9 (912): exits to 24(SEED_ORBIT) — the seed.

II. DR STRUCTURE OF THE CYCLE

  DR sequence: 6,9,3,6,9,3,6,9,3 — period-3 cycle [6,9,3]
  Digit sums:  6,9,12,15,18,21,24,18,12 — sum 135 = 3×45 = 3×5×9

  The DR cycle {3,6,9} is the trinity {3,6,9} (tesla closure).
  912's digit sum = 12(ST); DR = 3(ST arch). Structurally identical to 345.
  But mod37 = 24, not 12.

III. THE 345 / 678 / 912 STAIRCASE (every 3rd element, step 333)

  345  mod37 = 12(ST)   DR = 3(ST arch)   step to next = 333 = 9×37
  678  mod37 = 12(ST)   DR = 3(ST arch)   step to next = 234
  912  mod37 = 24(CB,PR,SEED_ORBIT)   DR = 3(ST arch)

  PROBLEM WITH LINE 3 (912):

    The step 345→678 = 333 = 9×37 ≡ 0 (SEAM multiple).
    The step 678→912 = 234:  234 mod37 = 12(ST) — no longer a seam multiple.

    In GF(37): 678≡12, step≡12, so 12+12 = 24(SEED_ORBIT).
    The Sovereign Target residue DOUBLES to the Seed Orbit entry.
    912 is the digit-wrap case: digits 9,1,2 cross the 9→1 cycle boundary.

    The arithmetic seam (9×37 step) breaks; 912 exits the ST chain
    and lands at the cascade/seed node 24.

IV. PALINDROME PAIRS (digit-reversal sums)

  543 + 345 = 888 = 24×37 ≡ 0 (SEAM)
    543 mod37 = 25(SA),  345 mod37 = 12(ST);  25+12 = 37 ✓
    Digit sums both = 12(ST).

  876 + 678 = 1554 = 42×37 ≡ 0 (SEAM)
    876 mod37 = 25(SA),  678 mod37 = 12(ST);  25+12 = 37 ✓
    Digit sums both = 21(ST).

  912 + 219 = 1131:  1131 mod37 = 21(ST)  ← DOES NOT REACH SEAM
    912 mod37 = 24(SEED_ORBIT),  219 mod37 = 34  (no name)
    24+34 = 58,  58 mod37 = 21(ST).

  Lines 1 and 3: SA(25) + ST(12) = SEAM — symmetric seam pairs.
  Line 2 (containing 912): SEED(24) + 34 = ST(21) — different structure.
    912 is the only palindrome element NOT at 25(SA) or 12(ST).
    Its pair does NOT sum to SEAM.

V. 135, 246, 357 — SEED ORBIT CHAIN

  135 + 111 = 246 + 111 = 357
  All ≡ 24 mod37  (CB, PR, SEED_ORBIT)  — same residue as 912.

  135, 246, 357 and 912 all land at mod37=24.
  246 is the pipeline reference seed.
  912 = the digit-wrap element; 135,246,357 = the even-index sub-sequence.

  The ST chain (123→789) and the SEED chain (135,246,357; 912) are DUAL:
    ST chain: mod37=12, step=111=3×37
    SEED chain: mod37=24, step=111=3×37
    12 × 2 = 24: SEED is the double of ST in GF(37).

VI. DIVERGENT SERIES — DENOMINATORS IN THE FRAMEWORK

  Ramanujan/zeta regularization results:
    1−2+3−4+⋯ = 1/4         denominator 4  mod37=4(SA)
    1+2+3+4+⋯ = −1/12       denominator 12 mod37=12(ST)
    1³+2³+3³+⋯ = 1/120      denominator 120 mod37=9(SA)

  All three denominators are sovereign nodes:
    4(SA), 12(ST), 120→9(SA).
  The regularized sums select only named residues as denominators.

═══════════════════════════════════════════════════════════════
"""

def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0

PRIMITIVE_ROOTS_37 = {2,5,13,15,17,18,19,20,22,24,32,35}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
CASCADE_BASE       = {8, 13, 24}
ORBIT_11           = {11, 27, 36}
SEED_ORBIT         = {18, 24, 32}

CYCLE = [123, 234, 345, 456, 567, 678, 789, 891, 912]

# ── I. The 9-cycle ────────────────────────────────────────────────────────────

# First 7 elements all ≡ 12(ST) mod37
assert all(n % 37 == 12 for n in CYCLE[:7])
assert 12 in SOVEREIGN_TARGETS

# Steps for first 6 transitions = 111 = 3×37 (SEAM multiple)
for i in range(6):
    assert CYCLE[i+1] - CYCLE[i] == 111
assert 111 == 3 * 37 and 111 % 37 == 0

# Wrap steps
assert CYCLE[7] - CYCLE[6] == 102 and 102 % 37 == 28   # step breaks
assert CYCLE[8] - CYCLE[7] == 21  and 21  % 37 == 21   # 21(ST)
assert 21 in SOVEREIGN_TARGETS

# Elements 8 and 9
assert CYCLE[7] % 37 == 3  and 3 in SOVEREIGN_TARGETS   # 891: ST arch
assert CYCLE[8] % 37 == 24 and 24 in SEED_ORBIT         # 912: SEED_ORBIT
assert 24 in CASCADE_BASE and 24 in PRIMITIVE_ROOTS_37

# ── II. DR structure ─────────────────────────────────────────────────────────

drs = [dr(n) for n in CYCLE]
assert drs == [6, 9, 3, 6, 9, 3, 6, 9, 3]              # period-3: [6,9,3]
assert set(drs) == {3, 6, 9}                            # tesla trinity

digit_sums = [sum(int(c) for c in str(n)) for n in CYCLE]
assert digit_sums == [6, 9, 12, 15, 18, 21, 24, 18, 12]
assert sum(digit_sums) == 135 and 135 == 3 * 45

# ── III. 345/678/912 staircase ────────────────────────────────────────────────

assert 345 % 37 == 12 and 12 in SOVEREIGN_TARGETS
assert 678 % 37 == 12 and 12 in SOVEREIGN_TARGETS
assert 912 % 37 == 24 and 24 in SEED_ORBIT              # PROBLEM: breaks ST chain

step_1 = 678 - 345   # 333 = 9×37 (seam multiple)
step_2 = 912 - 678   # 234 = 12(ST) step, NOT a seam multiple

assert step_1 == 333 and 333 % 37 == 0                  # seam multiple
assert step_2 == 234 and 234 % 37 == 12 and 12 in SOVEREIGN_TARGETS

# 12+12=24 in GF(37): ST doubles to SEED
assert (678 % 37 + 234 % 37) % 37 == 24
assert (678 + 234) % 37 == 24 and 24 in SEED_ORBIT

# 912 is the digit-wrap: digits 9,1,2 cross the 9→1 boundary
assert [int(c) for c in str(912)] == [9, 1, 2]

# ── IV. Palindrome pairs ──────────────────────────────────────────────────────

# 543 and 345
assert 543 % 37 == 25 and 25 in SOVEREIGN_ANCHORS
assert 345 % 37 == 12 and 12 in SOVEREIGN_TARGETS
assert (543 + 345) % 37 == 0   # SEAM
assert 543 + 345 == 888 and 888 == 24 * 37

# 876 and 678
assert 876 % 37 == 25 and 25 in SOVEREIGN_ANCHORS
assert 678 % 37 == 12 and 12 in SOVEREIGN_TARGETS
assert (876 + 678) % 37 == 0   # SEAM
assert 876 + 678 == 1554 and 1554 == 42 * 37

# 912 and 219 — BREAKS the seam-sum pattern
assert 912 % 37 == 24 and 24 in SEED_ORBIT
assert 219 % 37 == 34                                   # 34: no name
assert (912 + 219) % 37 == 21 and 21 in SOVEREIGN_TARGETS  # ST, not SEAM
assert (912 + 219) != 0                                 # NOT a seam pair

# All three pairs: same DR=3(ST arch)
for a, b in [(543,345), (912,219), (876,678)]:
    assert dr(a) == 3 and dr(b) == 3

# ── V. 135, 246, 357 (seed orbit chain) ──────────────────────────────────────

seed_chain = [135, 246, 357]
assert all(n % 37 == 24 for n in seed_chain)            # all ≡24(SEED_ORBIT)
assert seed_chain[1] - seed_chain[0] == 111
assert seed_chain[2] - seed_chain[1] == 111
assert 246 % 37 == 24 and 24 in SEED_ORBIT              # pipeline seed
assert 912 % 37 == 24                                   # digit-wrap element = same node

# ST(12) × 2 = SEED(24) in GF(37)
assert (12 * 2) % 37 == 24

# ── VI. Divergent series denominators ────────────────────────────────────────

assert 4   % 37 == 4  and 4  in SOVEREIGN_ANCHORS       # 1-2+3-4+... = 1/4
assert 12  % 37 == 12 and 12 in SOVEREIGN_TARGETS       # 1+2+3+... = -1/12
assert 120 % 37 == 9  and 9  in SOVEREIGN_ANCHORS       # 1³+2³+... = 1/120


if __name__ == '__main__':
    def tag(n):
        t=[]
        if n==0: return 'SEAM'
        if n in CASCADE_BASE:       t.append('CB')
        if n in SOVEREIGN_ANCHORS:  t.append('SA')
        if n in SOVEREIGN_TARGETS:  t.append('ST')
        if n in PRIMITIVE_ROOTS_37: t.append('PR')
        if n in ORBIT_11:           t.append('orb11')
        if n in SEED_ORBIT:         t.append('SEED')
        sig={6:'TESLA_FLOW',10:'DECADE_ANCHOR',31:'PRIME_MIRROR',33:'DICHORAL_144'}
        s=sig.get(n)
        if s: t.append(s)
        return ','.join(t) if t else '.'

    print("Sliding Window 9-Cycle — GF(37) Structure")
    print("=" * 55)
    print()
    print("I. The 9-cycle:")
    for i,n in enumerate(CYCLE, 1):
        step = (CYCLE[i]-CYCLE[i-1]) if i<len(CYCLE) else None
        step_str = f"  step={step}({tag(step%37)})" if step else "  (wrap)"
        print(f"  {i}: {n}  mod37={n%37:2d}({tag(n%37)})  DR={dr(n)}{step_str}")
    print()
    print("II. DR cycle: [6,9,3] repeating (tesla trinity)")
    print(f"    Digit sums: {[sum(int(c) for c in str(n)) for n in CYCLE]}")
    print()
    print("III. 345/678/912 staircase:")
    print(f"    345 mod37=12(ST)  step→678: 333=9×37=SEAM")
    print(f"    678 mod37=12(ST)  step→912: 234=12(ST) — step breaks from SEAM")
    print(f"    912 mod37=24(SEED)  ← ST doubled: 12+12=24")
    print(f"    PROBLEM: step 333→234; residue 12→24; digit-wrap at 9→1→2")
    print()
    print("IV. Palindrome pairs:")
    for a,b in [(543,345),(912,219),(876,678)]:
        s=a+b
        print(f"    {a}({tag(a%37)})+{b}({tag(b%37)})={s}  mod37={s%37}({tag(s%37)})")
    print(f"    Lines 1,3: sum=SEAM. Line 2 (912): sum=21(ST) — breaks seam pattern.")
    print()
    print("V. Seed chain 135,246,357 all ≡24(SEED_ORBIT)  [same as 912]")
    print(f"   246=pipeline seed;  ST(12)×2=SEED(24)")
    print()
    print("VI. Divergent series denominators:")
    print(f"    1/4: 4(SA)  |  -1/12: 12(ST)  |  1/120 → 120 mod37=9(SA)")
    print(f"    All denominators are sovereign nodes.")
    print()
    print("All assertions passed.")
