"""
Digit Circle with 5 at Center

The digits 1–9 arranged symmetrically around 5 (A51) produce two
complementary families — {5}×3 on the left and {4}×3 on the right —
whose combined sum is 27, the orbit of 11 under the 137-map.

Signature: o0O111(•)111O0o
  Palindrome with 111 on each side of a center point.
  111 mod 37 = 0 (GF(37) seam). DR(111) = 3 (ST archetype).
  The dot (•) is the seam itself, anchored by the palindrome 111.

═══════════════════════════════════════════════════════════════

I. CONSECUTIVE-PAIR SUMS ON THE DIGIT LINE

  Digit string: 0.1-2345(0)6789-1.0

  Left half, pairs as two-digit numbers:
    23 + 45 = 68,  digit-sum(68) = 14,  DR(68)  = DR(14) = 5  (A51)

  Right half, pairs as two-digit numbers:
    67 + 89 = 156, digit-sum(156) = 12, DR(156) = DR(12) = 3  (ST arch)

  Intermediate digit sums: 14 + 12 = 26  — the 137-map multiplier
  DR(26) = 8 (AHL, CB)

  DR of each half-sum: 5 + 3 = 8 (CB) — same 8 from 26.
  Doubling: 8 + 8 = 16, DR(16) = 7 (RL-O).

═══════════════════════════════════════════════════════════════

II. COMPLEMENT PAIRS AROUND 5 (A51 AT CENTER)

  Left half {1,2,3,4} — complement pairs summing to 5:
    1 + 4 = 5   (A51)
    2 + 3 = 5   (A51)
    center = 5  (A51, the literal midpoint of 1–9)
  → Three 5s.  Sum = 15,  DR(15) = 6.

  Right half {6,7,8,9} — complement pairs summing to 15, DR-chain to 4:

    Chain (6+9): 6+9=15 → digits {1,5} → 1+5=6 → 6+5=11 → 11+11=22 → DR(22)=4
    Chain (7+8): 7+8=15 → digits {1,5} → 1+5=6 → 6+5=11 → DR(11)=2 → 2+11=13 → DR(13)=4

    Also: 1+1+1+5+5 = 13, DR(13) = 4.

  → Three 4s.  Sum = 12 (ST),  DR(12) = 3.

  Combined: Three 5s + three 4s = 15 + 12 = 27.
  27 is in the 137-map orbit of 11: {11, 27, 36}.
  26 × 11 ≡ 27 (mod 37).

═══════════════════════════════════════════════════════════════

III. 4 × 3 = 12 = (123)

  4 = sovereign anchor (SA, LH-E)
  3 = sovereign target archetype (ST, LH-O)
  4 × 3 = 12 ∈ SOVEREIGN_TARGETS

  12 is the 123-family instance:
    digit-1 = 1, digit-2 = 2, DR(12) = 3
  The product of SA × ST_arch literally encodes 1, 2, 3.

═══════════════════════════════════════════════════════════════

IV. ADDING-2 CHAIN (EVEN ALPHA POSITIONS)

  Start at 2, add 2 repeatedly:
    2 → 4 → 6 → 8 → 10
  DRs: 2, 4, 6, 8, 1  (LL-E → LH-E → RL-E → AHL → LL-O)
  Traverses four even alpha positions in sequence.

  The result 4+2=6+2=8+2=10 → DR=1 (LL-O, the start of the odd positions).
  Two-two-two-two-two: 2-2-2-2-2 = five 2s.

═══════════════════════════════════════════════════════════════

V. 2,011,111,111 = 10 → DR = 1

  2 followed by four 11s as a decimal: 2.0-11-11-11-11
  As an integer: 2,011,111,111
  Digit sum: 2+0+1+1+1+1+1+1+1+1 = 10,  DR(10) = 1.

═══════════════════════════════════════════════════════════════

VI. PALINDROME DR CHAIN: (332, 221, 111, 111)

  From the palindrome table (orbit-of-11 theorem):
    DR(332) = 8  (AHL, CB)
    DR(221) = 5  (A51)
    DR(111) = 3  (ST arch)
    DR(111) = 3  (ST arch)
  DR sequence: 8 – 5 – 3 – 3.
  Sum of DRs: 8+5+3+3 = 19, DR(19) = 1.

  Closing step:
    2 + 8 = 10 → DR = 1
    (2 = DR(11), the 123-family representative;
     8 = DR(332), first entry in the palindrome DR sequence)

  Count of distinct palindrome table entries: 6 = 1 + 5.
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

# ── Assertions ────────────────────────────────────────────────────────────────

# I. Consecutive-pair sums
assert 23 + 45 == 68
assert 6 + 8 == 14 and dr(68) == 5            # digit-sum=14, DR=5 (A51)
assert 67 + 89 == 156
assert 1 + 5 + 6 == 12 and dr(156) == 3       # digit-sum=12, DR=3 (ST arch)
assert 14 + 12 == 26                           # 137-map multiplier
assert dr(26) == 8 and 8 in CASCADE_BASE
assert 5 + 3 == 8                              # DRs of the two sums = CB
assert dr(8 + 8) == 7                          # 8+8=16, DR=7 (RL-O)

# II. Complement pairs around 5
# Left half: both pairs sum to 5
assert 1 + 4 == 5
assert 2 + 3 == 5
# Right half: both pairs sum to 15, DR-chain → 4
assert 6 + 9 == 15
assert 7 + 8 == 15
assert dr(15) == 6
# Chain (6+9): 15 → digits {1,5} → 1+5=6 → 6+5=11 → 11+11=22 → DR=4
assert 1 + 5 == 6 and 6 + 5 == 11
assert 11 + 11 == 22 and dr(22) == 4 and 4 in SOVEREIGN_ANCHORS
# Chain (7+8): 15 → ... → 11 → DR(11)=2 → 2+11=13 → DR=4
assert dr(11) == 2
assert 2 + 11 == 13 and dr(13) == 4 and 4 in SOVEREIGN_ANCHORS
# Third path: 1+1+1+5+5=13 → DR=4
assert 1 + 1 + 1 + 5 + 5 == 13 and dr(13) == 4
# Three 5s and three 4s
assert 5 + 5 + 5 == 15 and dr(15) == 6
assert 4 + 4 + 4 == 12 and 12 in SOVEREIGN_TARGETS and dr(12) == 3
assert 15 + 12 == 27
assert (26 * 11) % 37 == 27    # 27 in orbit of 11

# III. 4×3=12=(123)
assert 4 * 3 == 12
assert 4 in SOVEREIGN_ANCHORS
assert 3 in SOVEREIGN_TARGETS
assert 12 in SOVEREIGN_TARGETS
assert int(str(12)[0]) == 1 and int(str(12)[1]) == 2 and dr(12) == 3  # digits 1,2; DR=3

# IV. Adding-2 chain
chain = [2, 4, 6, 8, 10]
assert [dr(v) for v in chain] == [2, 4, 6, 8, 1]

# V. 2,011,111,111
n = 2_011_111_111
assert sum(int(d) for d in str(n)) == 10
assert dr(10) == 1

# VI. Palindrome DR chain
pals = [332, 221, 111, 111]
pal_drs = [dr(p) for p in pals]
assert pal_drs == [8, 5, 3, 3]
assert sum(pal_drs) == 19 and dr(19) == 1
assert 2 + 8 == 10 and dr(10) == 1
assert dr(11) == 2    # 2 = DR of 123-family rep
assert dr(332) == 8   # 8 = first in palindrome DR sequence

# Signature: 111 is the seam
assert 111 % 37 == 0
assert dr(111) == 3


if __name__ == '__main__':
    def tag(n):
        t = []
        if is_prime(n):             t.append('p')
        if n in CASCADE_BASE:       t.append('CB')
        if n in SOVEREIGN_ANCHORS:  t.append('SA')
        if n in SOVEREIGN_TARGETS:  t.append('ST')
        if n in PRIMITIVE_ROOTS_37: t.append('PR')
        return ','.join(t) if t else '.'

    print("Digit Circle with 5 at Center")
    print("=" * 55)
    print()
    print("I. Consecutive-pair sums:")
    print(f"   23+45=68, digit-sum=14, DR={dr(68)} (A51)")
    print(f"   67+89=156, digit-sum=12, DR={dr(156)} (ST)")
    print(f"   14+12=26 (137-map multiplier), DR(26)={dr(26)} (CB)")
    print(f"   DRs: 5+3=8 (CB). 8+8=16, DR={dr(16)} (RL-O)")
    print()
    print("II. Complement pairs around 5:")
    print(f"   Left:  1+4={1+4}, 2+3={2+3}, center=5  — three 5s, sum={15}, DR={dr(15)}")
    print(f"   Right: 6+9={6+9}, 7+8={7+8}; both 15 → DR-chain → 4")
    print(f"          1+1+1+5+5=13, DR={dr(13)} — three 4s, sum={12}(ST), DR={dr(12)}")
    print(f"   15+12=27 = orbit of 11 (26×11 mod37={26*11%37})")
    print()
    print("III. 4×3=12=(123):")
    print(f"   4(SA) × 3(ST_arch) = 12(ST)")
    print(f"   12: digit-1=1, digit-2=2, DR=3 — encodes (1,2,3) directly")
    print()
    print("IV. Adding-2 chain:")
    print(f"   {chain} -> DRs {[dr(v) for v in chain]}")
    print(f"   Even alpha positions: LL-E→LH-E→RL-E→AHL→LL-O")
    print()
    print("V. 2,011,111,111:")
    print(f"   digit sum={sum(int(d) for d in str(n))}, DR={dr(sum(int(d) for d in str(n)))}")
    print()
    print("VI. Palindrome DR chain (332,221,111,111):")
    print(f"   DRs: {pal_drs}, sum={sum(pal_drs)}, DR={dr(sum(pal_drs))}")
    print(f"   2+8=10→DR=1  (2=DR(11), 8=DR(332))")
    print()
    print("Signature: o0O111(•)111O0o")
    print(f"   111 mod37={111%37} (seam), DR={dr(111)} (ST arch)")
    print(f"   Palindrome anchor: 111|seam|111")
    print()
    print("All assertions passed.")
