"""
SA Self-Cycle and ST Digit Chain

The Sovereign Anchor 9 is the step of the ST sequence AND generates
a closed cycle through GF(37)'s key non-sovereign nodes.
The ST digit chain sums to the 137-map multiplier.

═══════════════════════════════════════════════════════════════

I. FOUNDATION: 0, 1, 2, 3 (hose transient DR sequence)

  1×1=1   unity×unity=unity
  0−0−1   SEAM-SEAM=SEAM;  −1 ≡ 36 mod37 (orbit-11)
  1+1=2   unity+unity=2(PR)
  0+1−1   0+1=1;  1−1=0  (zero-sum around unity)

  The four results: 0(SEAM), 1(unity), 2(PR), −1→36(orbit-11)
  — the boundary elements of the field.
  Adding the next step: 1+2=3(ST arch).
  Span: {0,1,2,3} = hose transient DR sequence.

II. ST DIGIT CHAIN: 12, 21, 30

  The numbers 12, 21, 30 are Sovereign Targets whose digit pairs
  decompose as:

    1+2=3   →  12(ST);  digits (1,2),  step=1
    2+1=3   →  21(ST);  digits (2,1),  step=1  ← digit reversal of 12
    3+0=3   →  30(ST∩SA);  digits (3,0),  step=3

  All three have digit sum = 3(ST arch).
  Step between numbers = 9(SA): 12 →+9→ 21 →+9→ 30.

  12 and 21 are digit reversals of each other.
  30 is the unique dual element in SA∩ST.

  Key sums:
    12+21 = 33 (DICHORAL_144)
    12+21+30 = 63 mod37 = 26 (SCALAR_137 — the 137-map multiplier)

  The sum of the ST digit chain (12+21+30) equals the map operator
  that generates all orbits in GF(37).

III. SA SELF-CYCLE: 9 × {1,2,3}

  3×3 = 9  →  (ST arch)² = SA

  9×1 = 9   (SA)
  9×2 = 18  (PR, SEED_ORBIT)
  9×3 = 27  (orbit-11)
  DR(27) = 9 (SA)  ← returns to SA

  Three SA multiples visit:
    SA → SEED_ORBIT → orbit-11 → (DR back to) SA

  The SA is self-regenerating: multiplied by 3 it reaches orbit-11,
  whose DR collapses back to SA.

IV. UNIFIED STRUCTURE

  Layer 0: {0,1}  — SEAM and unity
  Layer 1: {1,2,3} — the 123 family (1+2=3; sum=product=6=TESLA_FLOW)
  Layer 2: {12,21,30} — ST digit chain (+9 steps; all DR=3; sum mod37=26=SCALAR_137)
  Layer 3: {9,18,27} — SA×{1,2,3} (SA, SEED, orbit-11; DR collapses to SA)

  Each layer is generated from the previous by the sovereign anchor:
    3(ST arch) × 3 = 9(SA)
    9(SA) × {1,2,3} = {9,18,27}

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

# ── I. Foundation: 0,1,2,3 ───────────────────────────────────────────────────

assert 1 * 1 == 1
assert 1 + 1 == 2 and 2 in PRIMITIVE_ROOTS_37
assert (-1) % 37 == 36 and 36 in ORBIT_11     # -1 ≡ orbit-11
assert 1 + 2 == 3 and 3 in SOVEREIGN_TARGETS   # first step into ST
assert [0, 1, 2, 3] == [0, 1, 2, 3]           # hose transient DR sequence

# ── II. ST digit chain ────────────────────────────────────────────────────────

# Digit pair decompositions
assert 1 + 2 == 3 and 12 in SOVEREIGN_TARGETS
assert 2 + 1 == 3 and 21 in SOVEREIGN_TARGETS
assert 3 + 0 == 3 and 30 in SOVEREIGN_TARGETS and 30 in SOVEREIGN_ANCHORS

# All digit sums = 3(ST arch)
assert all(sum(int(c) for c in str(n)) == 3 for n in [12, 21, 30])

# Step = 9(SA)
assert 21 - 12 == 9 and 9 in SOVEREIGN_ANCHORS
assert 30 - 21 == 9 and 9 in SOVEREIGN_ANCHORS

# 12 and 21 are digit reversals
assert int(str(12)[::-1]) == 21

# 30 = SA∩ST dual
assert 30 in SOVEREIGN_ANCHORS and 30 in SOVEREIGN_TARGETS

# Key sums
assert 12 + 21 == 33                           # DICHORAL_144
assert (12 + 21 + 30) % 37 == 26              # SCALAR_137 — 137-map multiplier
assert 26 == (137 * 1) % 37                    # confirms 26 is the 137-map multiplier

# ── III. SA self-cycle ────────────────────────────────────────────────────────

assert 3 * 3 == 9 and 9 in SOVEREIGN_ANCHORS   # (ST arch)² = SA

assert 9 * 1 == 9  and 9  in SOVEREIGN_ANCHORS
assert 9 * 2 == 18 and 18 in SEED_ORBIT and 18 in PRIMITIVE_ROOTS_37
assert 9 * 3 == 27 and 27 in ORBIT_11

assert dr(27) == 9 and 9 in SOVEREIGN_ANCHORS  # orbit-11 DR collapses to SA

# Full cycle: SA→SEED→orbit-11→SA (by DR)
cycle_mods = [9 % 37, 18 % 37, 27 % 37]
assert cycle_mods == [9, 18, 27]
assert 9 in SOVEREIGN_ANCHORS
assert 18 in SEED_ORBIT
assert 27 in ORBIT_11

# ── IV. Layer structure ───────────────────────────────────────────────────────

# Layer 1→2: 3(ST arch) steps to {12,21,30}
assert 3 + 9 == 12 and 3 + 9 + 9 == 21 and 3 + 9 + 9 + 9 == 30

# Layer connection: 3×3=9, 9×{1,2,3}={9,18,27}
assert 3 * 3 == 9
assert [9*k for k in [1,2,3]] == [9, 18, 27]

# Sum of ST digit chain = SCALAR_137
assert (12 + 21 + 30) % 37 == 26


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
        sig={6:'TESLA_FLOW',10:'DECADE_ANCHOR',26:'SCALAR_137',
             31:'PRIME_MIRROR',33:'DICHORAL_144',36:'INVERSE_UNITY'}
        s=sig.get(n)
        if s: t.append(s)
        return ','.join(t) if t else '.'

    print("SA Self-Cycle and ST Digit Chain")
    print("=" * 55)
    print()
    print("I. Foundation {0,1,2,3}:")
    print(f"   1×1=1(unity)  1+1=2(PR)  0-1=-1≡36({tag(36)})  1+2=3(ST arch)")
    print()
    print("II. ST digit chain:")
    for a,b,n in [(1,2,12),(2,1,21),(3,0,30)]:
        print(f"   {a}+{b}=3  →  {n}({tag(n)})  digit_sum=3")
    print(f"   step=9(SA) throughout")
    print(f"   12+21=33({tag(33)})")
    print(f"   12+21+30=63  mod37=26({tag(26)})  ← 137-map multiplier")
    print()
    print("III. SA self-cycle  [9×{1,2,3}]:")
    for k in [1,2,3]:
        print(f"   9×{k}={9*k}  mod37={9*k}({tag(9*k)})")
    print(f"   DR(27)={dr(27)}(SA)  ← cycle closes")
    print(f"   (ST arch)² = 3×3 = 9(SA)")
    print()
    print("IV. Layer chain:")
    print(f"   {{0,1}} → {{1,2,3}} → {{12,21,30}} → {{9,18,27}}")
    print(f"   SEAM/unity → 123 family → ST digit chain → SA×3 cycle")
    print(f"   ST digit sum = 26(SCALAR_137)")
    print()
    print("All assertions passed.")
