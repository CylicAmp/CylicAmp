"""
Sequence 146, 257, 368 — GF(37) Structure

Three numbers separated by 111 = 3×37. Step is a seam triple;
all three share the same GF(37) residue.

  146 + 111 = 257 + 111 = 368

═══════════════════════════════════════════════════════════════

I. SEAM TRIPLE STEP

  111 = 3 × 37 ≡ 0 mod 37  (three full laps around the field)

  146 mod 37 = 35 (PR, ≡ −2)
  257 mod 37 = 35 (PR, ≡ −2)   ← Fermat prime 2⁸+1
  368 mod 37 = 35 (PR, ≡ −2)

  All three land at 35 — the primitive root that is −2 in GF(37).
  Step = seam triple → residue is invariant. The field sees one point.

  DR: 2(PR), 5(PR), 8(CB)

II. DIGIT STRUCTURE

  Each number: first digit + step 3, step 2.
    146: 1, 1+3=4, 1+5=6
    257: 2, 2+3=5, 2+5=7
    368: 3, 3+3=6, 3+5=8

  Digit split — outer (first+last) and middle:
    146: (1+6, 4) = (7,    4=SA) → 11  (orbit-11)
    257: (2+7, 5) = (9=SA, 5=PR) → 14  (DR=5=PR)
    368: (3+8, 6) = (11,   6)    → 17  (DR=8)

  Outer sums [7, 9, 11]: step=2; sum=27(orbit-11)
    7 → RL-O, 9 → SA, 11 → orbit-11

  Middle values [4, 5, 6]: step=1(unity); sum=15(PR)
    4=SA, 5=PR, 6=TESLA_FLOW
    The middle column walks through SA → PR → TESLA_FLOW.

  Digit sums [11, 14, 17]: step=3(ST arch)
    11 ∈ orbit-11
    14: DR=5(PR)
    17: prime, DR=8
    11 + 14 = 25(SA)    ← intermediate partial sum = Sovereign Anchor
    11 + 14 + 17 = 42 mod 37 = 5(PR)

III. DOUBLING

  35 × 2 = 70 = 37 + 33  →  70 mod 37 = 33 (DICHORAL_144)

  Every element doubled lands on DICHORAL_144:
    146 × 2 = 292 mod 37 = 33
    257 × 2 = 514 mod 37 = 33
    368 × 2 = 736 mod 37 = 33

  The sequence lives at PR=35(≡−2); doubling maps the entire sequence to DICHORAL_144(33).

IV. FACTOR STRUCTURE

  146 = 2 × 73
    73 mod 37 = 36 (orbit-11, ≡ −1)
    146 ≡ 2 × (−1) = −2 ≡ 35(PR)  ✓

  257 = 2⁸ + 1  (Fermat prime)
    2⁸ mod 37 = 34 ≡ −3
    257 ≡ −3 + 1 = −2 ≡ 35(PR)  ✓
    The Fermat prime sits at −2 in GF(37).

  368 = 2⁴ × 23
    23 doubling chain under ×2 mod 37:
      23 × 1  = 23   mod 37 = 23  (.)
      23 × 2  = 46   mod 37 = 9   (SA)
      23 × 4  = 92   mod 37 = 18  (PR, SEED_ORBIT)
      23 × 8  = 184  mod 37 = 36  (orbit-11, ≡ −1)
      23 × 16 = 368  mod 37 = 35  (PR) ← arrives at sequence residue
    The 23-doubling chain visits SA → SEED_ORBIT → orbit-11 before landing at 35.

V. PARTIAL SUMS

  146 + 257 = 403  mod 37 = 33 (DICHORAL_144)
  146 + 257 + 368 = 771  mod 37 = 31 (PRIME_MIRROR)
  DR(771) = 6 (TESLA_FLOW)

  The two-element sum lands at DICHORAL (same as the doubled sequence).
  The three-element sum lands at PRIME_MIRROR.

VI. 5 × 11 = 55 → SEED ORBIT

  5  ∈ PRIMITIVE_ROOTS_37
  11 ∈ ORBIT_11

  5 × 11 = 55  mod 37 = 18  (PR, SEED_ORBIT)
  DR(55) = 1  (unity)

  The product of the PR-representative and the orbit-11 anchor
  lands at node 18 of the seed orbit {18, 24, 32}.
  DR collapses to unity — the multiplication reaches the seed and stops.

  In the digit structure above: middle values start at 4(SA) and 5(PR) appears at 257.
  First digit sum = 11(orbit-11). DR(257's middle=5) × first_digit_sum(11) = 55 → SEED.

VII. 124 = 4 × 31  AND  23

  124 = 4 × 31
    4  ∈ SA (Sovereign Anchor)
    31 = PRIME_MIRROR
    124 mod 37 = 13 (CB, PR)
    124 = 123 + 1  →  123 mod 37 = 12(ST);  DR(124) = 7

  DR(23) = 5(PR), DR(124) = 7
    DR(23) × DR(124) = 5 × 7 = 35(PR) = mod 37 residue of the sequence.
  DR(23) + DR(124) = 5 + 7 = 12(ST)

  23 is the prime factor of 368 (= 16 × 23).
  124 = 4 × 31:  the SA and PRIME_MIRROR whose DRs combine to 35 — the sequence residue.

  23 × 2 = 46:  46 mod 37 = 9(SA),  DR(46) = 1(unity)

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
SEED_ORBIT         = {18, 24, 32}

SEQ = [146, 257, 368]

# ── I. Seam triple step ───────────────────────────────────────────────────────

assert 111 == 3 * 37                           # step is three field laps
assert 146 + 111 == 257 and 257 + 111 == 368

assert all(n % 37 == 35 for n in SEQ)         # all ≡ −2 ≡ 35(PR) mod 37
assert 35 in PRIMITIVE_ROOTS_37
assert 35 == 37 - 2                            # 35 ≡ −2

assert [dr(n) for n in SEQ] == [2, 5, 8]
assert 2 in PRIMITIVE_ROOTS_37
assert 5 in PRIMITIVE_ROOTS_37
assert 8 in CASCADE_BASE

# ── II. Digit structure ───────────────────────────────────────────────────────

# digit generation rule: first=N, second=N+3, third=N+5
for i, n in enumerate(SEQ, start=1):
    d = [int(c) for c in str(n)]
    assert d == [i, i+3, i+5]

# digit split: outer = first+last, middle = center
splits = [(1+6, 4), (2+7, 5), (3+8, 6)]
sums   = [s[0]+s[1] for s in splits]
assert sums == [11, 14, 17]

outer_vals  = [s[0] for s in splits]   # [7, 9, 11]
middle_vals = [s[1] for s in splits]   # [4, 5, 6]

assert outer_vals == [7, 9, 11]
assert outer_vals[1] in SOVEREIGN_ANCHORS    # 9=SA
assert outer_vals[2] in ORBIT_11             # 11=orbit-11
assert sum(outer_vals) % 37 == 27 and 27 in ORBIT_11   # outer sum = 27(orbit-11)

assert middle_vals == [4, 5, 6]
assert 4 in SOVEREIGN_ANCHORS                # 4=SA
assert 5 in PRIMITIVE_ROOTS_37              # 5=PR
# 6 = TESLA_FLOW
assert sum(middle_vals) % 37 == 15 and 15 in PRIMITIVE_ROOTS_37

assert sums[0] in ORBIT_11                   # 11=orbit-11
assert dr(sums[1]) == 5 and 5 in PRIMITIVE_ROOTS_37   # DR(14)=5(PR)
assert (sums[0]+sums[1]) == 25 and 25 in SOVEREIGN_ANCHORS   # 11+14=25(SA)
assert sum(sums) % 37 == 5 and 5 in PRIMITIVE_ROOTS_37       # total=42 mod37=5(PR)

# ── III. Doubling ─────────────────────────────────────────────────────────────

assert 35 * 2 == 70 and 70 % 37 == 33        # −2 doubled → DICHORAL_144
for n in SEQ:
    assert (n * 2) % 37 == 33

# ── IV. Factor structure ──────────────────────────────────────────────────────

assert 146 == 2 * 73 and is_prime(73)
assert 73 % 37 == 36 and 36 in ORBIT_11      # 73 ≡ −1

assert 257 == 2**8 + 1 and is_prime(257)      # Fermat prime
assert 2**8 % 37 == 34                        # 2⁸ ≡ −3 mod 37
assert (2**8 + 1) % 37 == 35                  # 2⁸+1 ≡ −2 ≡ 35(PR)

assert 368 == 16 * 23 and is_prime(23)
chain = {1:23, 2:9, 4:18, 8:36, 16:35}
for k, r in chain.items():
    assert (23 * k) % 37 == r
assert chain[2]  in SOVEREIGN_ANCHORS         # SA
assert chain[4]  in SEED_ORBIT                # SEED_ORBIT
assert chain[8]  in ORBIT_11                  # orbit-11
assert chain[16] in PRIMITIVE_ROOTS_37        # PR

# ── V. Partial sums ───────────────────────────────────────────────────────────

assert (146 + 257) % 37 == 33                 # DICHORAL_144
assert (146 + 257 + 368) % 37 == 31          # PRIME_MIRROR
assert dr(146 + 257 + 368) == 6              # TESLA_FLOW

# ── VI. 5 × 11 = 55 → seed orbit ─────────────────────────────────────────────

assert 5 in PRIMITIVE_ROOTS_37 and 11 in ORBIT_11
assert 5 * 11 == 55
assert 55 % 37 == 18 and 18 in SEED_ORBIT and 18 in PRIMITIVE_ROOTS_37
assert dr(55) == 1                            # unity

# the 5 from middle_vals[1] (257's middle digit) × 11 (first digit sum)
assert middle_vals[1] == 5
assert sums[0] == 11
assert middle_vals[1] * sums[0] == 55

# ── VII. 124 and 23 ───────────────────────────────────────────────────────────

assert 124 == 4 * 31
assert 4 in SOVEREIGN_ANCHORS                # SA
assert 31 % 37 == 31                         # PRIME_MIRROR
assert 124 % 37 == 13 and 13 in CASCADE_BASE and 13 in PRIMITIVE_ROOTS_37
assert 123 % 37 == 12 and 12 in SOVEREIGN_TARGETS  # 124-1=123(ST)
assert dr(124) == 7

assert is_prime(23) and dr(23) == 5 and 5 in PRIMITIVE_ROOTS_37
assert dr(23) * dr(124) == 35 and 35 in PRIMITIVE_ROOTS_37   # product of DRs = sequence residue
assert dr(23) + dr(124) == 12 and 12 in SOVEREIGN_TARGETS    # sum of DRs = ST

assert 23 * 2 == 46
assert 46 % 37 == 9 and 9 in SOVEREIGN_ANCHORS
assert dr(46) == 1                            # unity


if __name__ == '__main__':
    def tag(n):
        t = []
        if n == 0:       return 'SEAM'
        if n in CASCADE_BASE:      t.append('CB')
        if n in SOVEREIGN_ANCHORS: t.append('SA')
        if n in SOVEREIGN_TARGETS: t.append('ST')
        if n in PRIMITIVE_ROOTS_37: t.append('PR')
        if n in ORBIT_11:          t.append('orb11')
        if n in SEED_ORBIT:        t.append('SEED')
        sig = {6:'TESLA_FLOW',10:'DECADE_ANCHOR',31:'PRIME_MIRROR',33:'DICHORAL_144'}
        s = sig.get(n)
        if s: t.append(s)
        return ','.join(t) if t else '.'

    print("Sequence 146, 257, 368 — GF(37) Structure")
    print("=" * 55)
    print()
    print(f"I. Step 111=3×37 (seam triple); all ≡35(PR,≡−2) mod37")
    for n in SEQ:
        d = [int(c) for c in str(n)]
        outer = d[0]+d[2]
        mid   = d[1]
        print(f"  {n}: mod37={n%37}({tag(n%37)})  DR={dr(n)}  "
              f"digits({d[0]},{d[1]},{d[2]})  outer={outer}({tag(outer)}) mid={mid}({tag(mid)}) sum={outer+mid}({tag(outer+mid)})")
    print()
    print(f"II. Outer sums {outer_vals}: step=2; sum=27({tag(27)})")
    print(f"    Middle vals {middle_vals}: step=1(unity); sum=15({tag(15)})")
    print(f"    Digit sums {sums}: step=3(ST arch)")
    print(f"    11+14={11+14}({tag(25)})  total=42 mod37=5({tag(5)})")
    print()
    print(f"III. Doubling: 35×2=70 mod37=33({tag(33)})")
    print(f"     {[n*2 for n in SEQ]} all mod37=33")
    print()
    print(f"IV. 146=2×73: 73 mod37=36({tag(36)}≡−1)")
    print(f"    257=2⁸+1 (Fermat prime): 2⁸ mod37=34(≡−3); 257≡−2≡35({tag(35)})")
    print(f"    368=16×23: 23 doubling chain:")
    for k,r in chain.items():
        print(f"      23×{k:2d}={23*k:4d} mod37={r:2d}({tag(r)})")
    print()
    print(f"V. Partial sums:")
    print(f"   146+257=403 mod37=33({tag(33)})")
    print(f"   146+257+368=771 mod37=31({tag(31)})  DR=6({tag(6)})")
    print()
    print(f"VI. 5(PR)×11(orb11)=55 mod37=18({tag(18)})  DR=1(unity)")
    print(f"    middle[257]=5, first_digit_sum=11  →  5×11=55(SEED)")
    print()
    print(f"VII. 124=4(SA)×31(PRIME_MIRROR) mod37=13({tag(13)})")
    print(f"     DR(23)×DR(124)=5×7=35({tag(35)}) = sequence residue")
    print(f"     DR(23)+DR(124)=5+7=12({tag(12)})")
    print(f"     23×2=46({tag(46%37)})  DR=1(unity)")
    print()
    print("All assertions passed.")
