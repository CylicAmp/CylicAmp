"""
Alternating 1-2 Structures: sequences, palindromes, triples, tables

Seed digits are 1 and 2 — the first two members of the 123 family.

═══════════════════════════════════════════════════════════════

I. ALTERNATING SEQUENCES (period 6 mod 37)

  seq1 (starts 1): 1, 12, 121, 1212, 12121, 121212, ...
  seq2 (starts 2): 2, 21, 212, 2121, 21212, 212121, ...

  Both sequences have period 6 in GF(37):

  seq1 orbit mod 37: {1, 12, 10, 28, 22, 0}
  seq2 orbit mod 37: {2, 21, 27, 12, 11, 0}

  Both hit 0 (GF(37) seam) at digit-lengths 6, 12, 18, 24 (multiples of 6).
  12 (sovereign target) appears in BOTH orbits.

  10-digit pair: 1212121212 + 2121212121 ≡ 28+12 = 40 ≡ 3 (mod 37)
  — the sum of the two 10-digit alternating numbers is a sovereign target mod 37.

  seq2 orbit contains: 27 (in orbit of 11 under 137-map) and 11 itself.

═══════════════════════════════════════════════════════════════

II. 9+9+9 → 11 CONNECTION

  9+9+9 = 27 (DR=9)
  27 is in the 137-map orbit of 11: {11, 27, 36}
  Digits of 27: 2 and 7.
  9 + 2 = 11  (the 123-family representative)
  11 + 7 = 18  DR(18) = 9  (returns to 9)

  Chain: 9+9+9 = 27 → digits {2,7} → 9+2 = 11 → 11+7 = 18 → DR=9

═══════════════════════════════════════════════════════════════

III. 1221 / 2112 PALINDROMES

  1221 mod 37 = 0  (GF(37) seam)
  2112 mod 37 = 3  (sovereign target, LH-O)
  1221 + 2112 = 3333, DR(3333) = 3
  1221 × 2112 mod 37 = 0

  Structure:
    1221-2112  |  2112-1221
    2112-1221  |  1221-2112
    2112-1221  |  1221-2112
    1221-2112  |  2112-1221

═══════════════════════════════════════════════════════════════

IV. THREE-DIGIT PALINDROME → ALPHA GRID (digit sums)

  Digit-palindromes built from {1,2,3} map to alpha grid positions 3–9:
    111 → sum=3  (LH-O, sovereign target archetype)
    121 → sum=4  (LH-E, sovereign anchor)
    212 → sum=5  (A51, center)
    222 → sum=6  (RL-E)
    232 → sum=7  (RL-O / ALO)
    323 → sum=8  (RH-E / AHL, cascade base)
    333 → sum=9  (RH-O, sovereign anchor)

  Covers alpha positions 3–9. Positions 1 (LL-O) and 2 (LL-E)
  would require digits below 1.

═══════════════════════════════════════════════════════════════

V. TWO-DIGIT DR TABLE

  Two-digit numbers from digits {1,2,3} and their DRs:
    11 → (2)   mod37=11  (prime, 123-family representative)
    12 → 3     mod37=12  (sovereign target)
    21 → 3     mod37=21  (sovereign target)
    22 → (4)   mod37=22  (primitive root)
    23 → 5     mod37=23  (prime)
    32 → 5     mod37=32  (primitive root)
    33 → (6)   mod37=33  = -4 mod 37

  Parenthesized DRs (2, 4, 6) = even values from double-digit numbers (11,22,33).
  Non-parenthesized DRs (3, 3, 5, 5) = from mixed-digit pairs.

  33 + 4 = 37 ≡ 0 (mod 37) — boundary.
  4 is sovereign anchor (SA/LH-E). 33 = 3×11 = ST_archetype × 123-family-rep.

═══════════════════════════════════════════════════════════════

VI. ARITHMETIC TRIPLE TABLES

  Triples (a, middle, b) where the middle is the key number:

  Set 1 — outer sum = 6:
    2 - 24 - 4   product a×b=8  (CB)   mid mod37=24 (CB,PR)
    3 - 12 - 3   product a×b=9  (SA)   mid mod37=12 (ST)
    3 - 21 - 3   product a×b=9  (SA)   mid mod37=21 (ST)
    4 - 42 - 2   product a×b=8  (CB)   mid mod37= 5 (A51, PR)

  Set 2 — outer sum = 10:
    4 - 46 - 6   product a×b=24 (CB,PR) mid mod37= 9 (SA)
    5 - 23 - 5   product a×b=25 (SA)    mid mod37=23 (prime)
    5 - 32 - 5   product a×b=25 (SA)    mid mod37=32 (PR)
    6 - 64 - 4   product a×b=24 (CB,PR) mid mod37=27 (orbit of 11)

  Pattern:
    Set 1 products: 8(CB) or 9(SA)
    Set 2 products: 24(CB,PR) or 25(SA)
    Note: 5+32=37 (complement pair in GF(37), like 11+26=37)

═══════════════════════════════════════════════════════════════

VII. SOVEREIGN TARGET CHAIN

  1+2=3  →  3+9=12  →  12+9=21  →  21+9=30
  {3, 12, 21, 30} = sovereign targets (ST)
  30 is the ONLY element that is simultaneously SA and ST.
  All have DR=3. All in the 123 family.

  "2+1=3" gives the same starting point (style 3-2-1 of 123 family).

═══════════════════════════════════════════════════════════════

VIII. 1089 = 33² = (3 × 11)²

  3 = sovereign target archetype (LH-O)
  11 = 123-family representative, complement of 26 in GF(37)
  33 = 3×11, DR(33)=6, 33 ≡ -4 (mod 37), 33+4=37
  1089 = 33², DR(1089)=9, digit sum 1+0+8+9=18, DR(18)=9

  Palindrome families from digit rotations of 1089:
    {1089, 9108, 8910, 0891} — cyclic rotations, all DR=9
    {0189, 9018, 8901, 1890} — cyclic rotations of complementary arrangement
    Each rotation concatenated with its digit-reversal gives a palindrome.
"""

def dr(n):
    return (n - 1) % 9 + 1

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

PRIMITIVE_ROOTS_37 = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}
CASCADE_BASE       = {8, 13, 24}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}

def alt1(k):
    return int(''.join('1' if i % 2 == 0 else '2' for i in range(k)))

def alt2(k):
    return int(''.join('2' if i % 2 == 0 else '1' for i in range(k)))

# ── Assertions ───────────────────────────────────────────────────────────────

# I. Alternating sequences: period 6 mod 37
orbit1 = [alt1(k) % 37 for k in range(1, 7)]
orbit2 = [alt2(k) % 37 for k in range(1, 7)]
assert orbit1 == [1, 12, 10, 28, 22, 0]
assert orbit2 == [2, 21, 27, 12, 11, 0]
# Verify period
for k in range(1, 10):
    assert alt1(k) % 37 == alt1(k + 6) % 37
    assert alt2(k) % 37 == alt2(k + 6) % 37
# Seams at multiples of 6
for m in [6, 12, 18, 24]:
    assert alt1(m) % 37 == 0
    assert alt2(m) % 37 == 0
# 12 (ST) in both orbits
assert 12 in orbit1 and 12 in orbit2
# 10-digit sum ≡ 3 (ST) mod 37
assert (1212121212 + 2121212121) % 37 == 3
assert 3 in SOVEREIGN_TARGETS
# seq2 orbit contains 27 (orbit of 11) and 11
assert 27 in orbit2 and 11 in orbit2
assert (26 * 11) % 37 == 27       # 11->27 under 137-map

# II. 9+9+9 → 11
assert 9 + 9 + 9 == 27
assert (26 * 11) % 37 == 27       # 27 in orbit of 11
assert 9 + 2 == 11                 # 9 + tens-digit of 27
assert 11 + 7 == 18                # + units-digit
assert dr(18) == 9

# III. 1221 / 2112
assert 1221 % 37 == 0
assert 2112 % 37 == 3 and 3 in SOVEREIGN_TARGETS
assert 1221 + 2112 == 3333
assert dr(3333) == 3
assert (1221 * 2112) % 37 == 0

# IV. Three-digit palindromes
assert sum(int(d) for d in '111') == 3
assert sum(int(d) for d in '121') == 4
assert sum(int(d) for d in '212') == 5
assert sum(int(d) for d in '222') == 6
assert sum(int(d) for d in '232') == 7
assert sum(int(d) for d in '323') == 8
assert sum(int(d) for d in '333') == 9

# V. Two-digit DR table
assert dr(11) == 2
assert dr(12) == 3 == dr(21)
assert dr(22) == 4
assert dr(23) == 5 == dr(32)
assert dr(33) == 6
assert 33 + 4 == 37
assert (-4) % 37 == 33
assert 33 == 3 * 11

# VI. Triple tables
SET1 = [(2, 24, 4), (3, 12, 3), (3, 21, 3), (4, 42, 2)]
SET2 = [(4, 46, 6), (5, 23, 5), (5, 32, 5), (6, 64, 4)]
for a, mid, b in SET1:
    assert a + b == 6
for a, mid, b in SET2:
    assert a + b == 10
assert all(a * b in CASCADE_BASE or a * b in SOVEREIGN_ANCHORS
           for a, mid, b in SET1)  # products are 8(CB) or 9(SA)
assert 5 + 32 == 37                # complement pair like 11+26=37
assert 12 in SOVEREIGN_TARGETS and 21 in SOVEREIGN_TARGETS
assert 42 % 37 == 5                # 42 ≡ A51 (PR) mod 37

# VII. Sovereign target chain
assert 1 + 2 == 3 and 3 in SOVEREIGN_TARGETS
for v in [3, 12, 21, 30]:
    assert dr(v) == 3 and v in SOVEREIGN_TARGETS
assert 30 in SOVEREIGN_ANCHORS and 30 in SOVEREIGN_TARGETS  # dual element

# VIII. 1089 = 33^2 = (3*11)^2
assert 33 == 3 * 11
assert 33 ** 2 == 1089
assert dr(1089) == 9
assert (33 + 4) % 37 == 0
# Palindromic 8-digit strings from rotations of 1089
rotations_1089 = ['1089', '9108', '8910', '0891']
for r in rotations_1089:
    palindrome_str = r + r[::-1]
    assert palindrome_str == palindrome_str[::-1], f'{palindrome_str} not palindrome'
# Digit sum of each rotation = 18
for r in rotations_1089:
    dsum = sum(int(d) for d in r)
    assert dsum == 18 and dr(dsum) == 9


if __name__ == '__main__':
    def tag(n):
        t = []
        if is_prime(n):             t.append('p')
        if n in CASCADE_BASE:       t.append('CB')
        if n in SOVEREIGN_ANCHORS:  t.append('SA')
        if n in SOVEREIGN_TARGETS:  t.append('ST')
        if n in PRIMITIVE_ROOTS_37: t.append('PR')
        return ','.join(t) if t else '.'

    print("Alternating 1-2 Structures")
    print("=" * 55)
    print()
    print("I. Alternating sequence orbits mod 37:")
    print(f"   seq1: {orbit1}")
    print(f"   seq2: {orbit2}")
    print(f"   10-digit sum mod 37: {(1212121212+2121212121)%37} (ST)")
    print()
    print("II. 9+9+9=27 -> 11:")
    print(f"   27 in orbit of 11: {(26*11)%37}=27 -> {(26*27)%37}=36 -> {(26*36)%37}=11")
    print(f"   9+2=11, 11+7=18, DR(18)=9")
    print()
    print("III. 1221/2112:")
    print(f"   1221 mod37=0, 2112 mod37=3(ST), sum=3333 DR=3")
    print()
    print("IV. Palindromes -> alpha grid:")
    for p in [111,121,212,222,232,323,333]:
        s=sum(int(d) for d in str(p))
        print(f"   {p} -> {s}")
    print()
    print("V. Two-digit DR table:")
    for n in [11,12,21,22,23,32,33]:
        print(f"   {n}: DR={dr(n)}, mod37={n%37} ({tag(n%37)})")
    print(f"   33+4=37 (boundary)")
    print()
    print("VI. Triple tables:")
    for a,mid,b in SET1: print(f"   {a}-{mid}-{b}  a+b={a+b}  a*b={a*b}({tag(a*b)})  mid%37={mid%37}({tag(mid%37)})")
    for a,mid,b in SET2: print(f"   {a}-{mid}-{b}  a+b={a+b}  a*b={a*b}({tag(a*b)})  mid%37={mid%37}({tag(mid%37)})")
    print()
    print("VII. ST chain: 3->12->21->30 (+9 each step)")
    print()
    print("VIII. 1089=33^2=(3x11)^2, DR=9")
    print()
    print("All assertions passed.")
