# math/theorems/field_55_mirror_structure.py
"""
55-Field Mirror Structure — Verified Arithmetic

Seven seeds, palindrome pair-sum analysis, 3025 kernel,
modular locks, Gauss construction, zero migration pattern.

─────────────────────────────────────────────────────────────────────────────
SEEDS AND PAIR SUMS
─────────────────────────────────────────────────────────────────────────────
  Seed       P0  P1  P2  P3  P0+P3  P1+P2
  32500523   32  50  05  23    55     55
  32055023   32  05  50  23    55     55
  30255203   30  25  52  03    33     77
  30255203   30  25  52  03    33     77
  32055023   32  05  50  23    55     55
  32500533   32  50  05  33    65     55   ← outer lock broken
  32400524   32  40  05  24    56     45   ← extra term

─────────────────────────────────────────────────────────────────────────────
ZERO MIGRATION PATTERN
─────────────────────────────────────────────────────────────────────────────
  Row  Seed      Zero positions (0-indexed)
  R0   32500523  3, 4   (center pair)
  R1   32055023  2, 5   (step out)
  R2   30255203  1, 6   (outer pair)
  R3   30255203  1, 6   (mirror of R2)
  R4   32055023  2, 5   (mirror of R1)
  R5   32500533  3, 4   (mirror of R0, last digit ≠ R0)

  Zeros migrate: (3,4) → (2,5) → (1,6) → (1,6) → (2,5) → (3,4)
  Each step: zero columns move outward by 1 position.
  R0-R4 are palindromes. R5 is NOT (32500533: last digit 3,3 ≠ R0's 2,3).

─────────────────────────────────────────────────────────────────────────────
ANTI-SYMMETRY OF DIFFERENCES
─────────────────────────────────────────────────────────────────────────────
  [0→1]: −445500
  [1→2]: −1799820
  [2→3]:        0    ← exact
  [3→4]: +1799820    ← [1→2]+[3→4] = 0 exactly
  [4→5]: +445510     ← NOT +445500: broken by 10 (seed[5]≠seed[0] by 10)

  Inner 3 pairs: exact odd symmetry.
  Outer pair: broken by 10 (7th digit 2→3 in seed[5]).

─────────────────────────────────────────────────────────────────────────────
GAUSS: 55² = 3025
─────────────────────────────────────────────────────────────────────────────
  (10n+5)² = 100·n(n+1) + 25,  n=5:  100·30 + 25 = 3025
  30 = 7 + 23,  25 = 5²
"""

SEEDS = [
    '32500523',  # [0]
    '32055023',  # [1]
    '30255203',  # [2]
    '30255203',  # [3]
    '32055023',  # [4]
    '32500533',  # [5]
    '32400524',  # ext
]

ZERO_POSITIONS = [(3,4),(2,5),(1,6),(1,6),(2,5),(3,4)]  # [0]..[5]

def pair_sums(s):
    P = [int(s[0:2]), int(s[2:4]), int(s[4:6]), int(s[6:8])]
    return P[0]+P[3], P[1]+P[2]

def dr(n): return 1 + (n-1)%9 if n>0 else 9


# ── Pair sum verification ──────────────────────────────────────────────────────

EXPECTED_PAIR_SUMS = [(55,55),(55,55),(33,77),(33,77),(55,55),(65,55),(56,45)]
for s, exp in zip(SEEDS, EXPECTED_PAIR_SUMS):
    assert pair_sums(s) == exp, f"Pair sum mismatch for {s}"

# ── Zero migration ─────────────────────────────────────────────────────────────

for i, (s, (z1, z2)) in enumerate(zip(SEEDS[:6], ZERO_POSITIONS)):
    assert s[z1] == '0', f"Seed[{i}] pos {z1} is not zero"
    assert s[z2] == '0', f"Seed[{i}] pos {z2} is not zero"

# Migration: positions step outward 3→2→1 then back 1→2→3
zpos = [p[0] for p in ZERO_POSITIONS]
assert zpos == [3,2,1,1,2,3]

# R0-R4 are palindromes, R5 is not
for i in range(5):
    assert SEEDS[i] == SEEDS[i][::-1], f"Seed[{i}] not palindrome"
assert SEEDS[5] != SEEDS[5][::-1]   # R5 breaks palindrome

# ── Anti-symmetry of differences ──────────────────────────────────────────────

vals = [int(s) for s in SEEDS[:6]]
diffs = [vals[i+1]-vals[i] for i in range(5)]

assert diffs[2] == 0                             # [2→3] = 0
assert diffs[1] + diffs[3] == 0                  # [1→2]+[3→4] = 0
assert diffs[0] == -445500
assert diffs[4] == +445510
assert diffs[4] + diffs[0] == 10                 # outer shell broken by 10
assert int(SEEDS[5]) - int(SEEDS[0]) == 10       # source of asymmetry

# ── 3025 kernel: 55² ──────────────────────────────────────────────────────────

assert 55**2 == 3025
prefixes = [int(s[:4]) for s in SEEDS]
offsets = [p - 3025 for p in prefixes]
assert offsets == [225, 180, 0, 0, 180, 225, 215]
assert 225 == 15**2
# Note: 180 = 4×45 = 36×5 (not a perfect square)
# Offsets [0..5] are symmetric: [225,180,0,0,180,225]; ext=215 breaks

# ── Modular locks ─────────────────────────────────────────────────────────────

EXPECTED_MODS = [
    (19,11,16, 3),  # 32500523
    (36,11, 9, 0),  # 32055023
    ( 7,11, 2, 4),  # 30255203
    ( 7,11, 2, 4),  # 30255203
    (36,11, 9, 0),  # 32055023
    (29, 3, 7, 0),  # 32500533
    (31, 2,14, 0),  # 32400524
]
for s, (m37,m18,m19,m13) in zip(SEEDS, EXPECTED_MODS):
    n = int(s)
    assert n%37==m37 and n%18==m18 and n%19==m19 and n%13==m13

# mod 18 = 11 for seeds [0]..[4] (digit sum ≡ 2 mod 9 and odd)
for s in SEEDS[:5]:
    assert int(s) % 18 == 11

# ── Gauss construction ─────────────────────────────────────────────────────────

n = 5
assert (10*n+5)**2 == 100*n*(n+1)+25 == 3025
assert n*(n+1) == 30 == 7+23     # 30 = LAMED-30 = 7+23
assert 25 == 5**2

# ── 55 modular ────────────────────────────────────────────────────────────────

assert 55 % 37 == 18
assert 55 % 18 ==  1
assert 55 % 19 == 17
assert 55 == 37 + 18

# ── Extra term: 32400524 ──────────────────────────────────────────────────────

assert int(SEEDS[0]) - int(SEEDS[6]) == 99999   # five 9s
assert 3240 % 18 == 0     # center-aligned
assert 3240 % 55 == 50


if __name__ == "__main__":
    print("55-Field Mirror Structure")
    print()
    print("Pair sums:")
    for s, (a,b) in zip(SEEDS, EXPECTED_PAIR_SUMS):
        flag = "" if a in (33,55,77) and b in (33,55,77) else "  ← LOCK BROKEN"
        print(f"  {s}: P0+P3={a:2d}  P1+P2={b:2d}{flag}")
    print()
    print("Zero migration (0-indexed positions):")
    for i, (s, (z1,z2)) in enumerate(zip(SEEDS[:6], ZERO_POSITIONS)):
        pal = "palindrome" if s==s[::-1] else "NOT palindrome"
        print(f"  R{i}: {s}  zeros at ({z1},{z2})  {pal}")
    print()
    print("Anti-symmetry:")
    for i, d in enumerate(diffs):
        sym = " ✓" if i in (1,2,3) else f"  (asymmetry={diffs[4]+diffs[0]})"
        print(f"  [{i}→{i+1}]: {d:+}{sym}")
    print()
    print(f"55² = 3025  (n=5: 100·30+25, 30=7+23, 25=5²)")
    print(f"55 mod 37={55%37}, mod 18={55%18}, mod 19={55%19}")
    print(f"32500523 − 32400524 = {int(SEEDS[0])-int(SEEDS[6])}  (five 9s)")
    print(f"3240 mod 18={3240%18}, mod 55={3240%55}")
    print()
    print("All assertions passed.")
