"""
3×3 Triplet Partition Framework — GF(37) Connection

The board B = {1,2,...,9} has exactly 280 unordered 3-block partitions.
Of these, 14 have all three block sums inside the framework sets
  SA ∪ ST ∪ CB ∪ orbit(11) = {4,9,25,30} ∪ {3,12,21,30} ∪ {8,13,24} ∪ {11,27,36}.

These 14 partitions fall into exactly four sum-multiset types:

  Type I   — {8,13,24}  = CASCADE_BASE exactly:          2 partitions
  Type II  — {9,12,24}  = {SA, ST, CB+PR}:              3 partitions
  Type III — {11,13,21} = {orbit(11), CB+PR, ST}:       6 partitions
  Type IV  — {12,12,21} = {ST, ST, ST} (all sovereign): 3 partitions

═══════════════════════════════════════════════════════════════

I. THE TARGET PARTITION: {1,3,5}, {2,4,6}, {7,8,9}

  Block structure:
    T1 = {1,3,5}  — all odd:   sum = 9  (SA, RH-O)
    T2 = {2,4,6}  — all even:  sum = 12 (ST, LH-E ... actually sum of odds)
    L  = {7,8,9}  — "large":   sum = 24 (CB, PR)

  Block sums: 9(SA), 12(ST), 24(CB+PR) — one node from each major class.

  Pairwise sums of block sums:
    9 + 12 = 21   (ST, sovereign target)
    12 + 24 = 36  (orbit of 11: {11,27,36})
    9 + 24 = 33   (= 3 × 11 = ST_arch × 123-family-rep, complement of 4=SA)

  Block products mod 37:
    prod(T1) = 15  mod 37 = 15  (PR)
    prod(T2) = 48  mod 37 = 11  (orbit of 11!)
    prod(L)  = 504 mod 37 = 23  (prime)

  Sum of all block products mod 37:
    (15 + 48 + 504) mod 37 = 567 mod 37 = 12  (ST)

  Mod-3 structure:
    T1 = {1,0,2} mod 3  — complete residue system {0,1,2}
    T2 = {2,1,0} mod 3  — complete residue system
    L  = {1,2,0} mod 3  — complete residue system
  Each block is a complete residue system mod 3.

═══════════════════════════════════════════════════════════════

II. TYPE I — CASCADE_BASE PARTITIONS: block sums {8,13,24}

  The three block sums are exactly the cascade base {8,13,24}.

  Partition A: {1,2,5} | {3,4,6} | {7,8,9}
    sums: 8(CB), 13(CB+PR), 24(CB+PR)
  Partition B: {1,3,4} | {2,5,6} | {7,8,9}
    sums: 8(CB), 13(CB+PR), 24(CB+PR)

  Both have {7,8,9} as the 24-sum block.

═══════════════════════════════════════════════════════════════

III. TYPE II — {9,12,24} PARTITIONS: one SA, one ST, one CB+PR

  Three partitions achieving {SA, ST, CB+PR}:

  A: {1,2,6} | {3,4,5} | {7,8,9}   sums: 9(SA), 12(ST), 24(CB+PR)
  B: {1,3,5} | {2,4,6} | {7,8,9}   sums: 9(SA), 12(ST), 24(CB+PR)  ← target
  C: {1,5,6} | {2,3,4} | {7,8,9}   sums: 12(ST), 9(SA), 24(CB+PR)

  Partition C products: prod({1,5,6})=30 (dual SA+ST), prod({2,3,4})=24 (CB+PR).
  All three include {7,8,9} as the large block.

═══════════════════════════════════════════════════════════════

IV. TYPE IV — ALL-SOVEREIGN-TARGET PARTITIONS: block sums {12,12,21}

  Three partitions where every block sum is a sovereign target:

  A: {1,2,9} | {3,4,5} | {6,7,8}   sums: 12(ST), 12(ST), 21(ST)
  B: {1,3,8} | {2,4,6} | {5,7,9}   sums: 12(ST), 12(ST), 21(ST)
  C: {1,5,6} | {2,3,7} | {4,8,9}   sums: 12(ST), 12(ST), 21(ST)

  Every block has DR=3 (sovereign target archetype).
  Partition B shares T2={2,4,6} (sum=12) with the target partition.

═══════════════════════════════════════════════════════════════

V. 137-SPACE FINITE VOID

  A board |B|=137 positions with alphabet |A|=k has k^137 raw states.

  137 mod 37 = 26  — the 137-map multiplier.

  The 137-position board encodes the multiplier in its own cardinality:
  the number of positions, reduced mod 37, IS the map that defines the
  framework's 3-cycles.

  ord₃₇(26) = 3: every element's orbit under this multiplier has length 3.

═══════════════════════════════════════════════════════════════

VI. COUNTING SUMMARY (3×3 BOARD)

  Total 3-block partitions:             280
  Framework-special (all sums in FW):    14
  By type:
    Type I  {8,13,24}  = CASCADE_BASE:  2
    Type II {9,12,24}  = SA+ST+CB:      3
    Type III{11,13,21} = orb11+CB+ST:   6
    Type IV {12,12,21} = all-ST:        3
  Total:                                14

  Proportion: 14/280 = 1/20.
"""

from itertools import combinations
from math import prod

def dr(n):
    return (n - 1) % 9 + 1

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

PRIMITIVE_ROOTS_37 = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}
CASCADE_BASE       = {8, 13, 24}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
ORBIT_11           = {11, 27, 36}
FRAMEWORK          = SOVEREIGN_ANCHORS | SOVEREIGN_TARGETS | CASCADE_BASE | ORBIT_11

B = list(range(1, 10))

def all_partitions(board):
    seen = set()
    result = []
    for t1 in combinations(board, 3):
        rest1 = [x for x in board if x not in t1]
        for t2 in combinations(rest1, 3):
            t3 = tuple(x for x in rest1 if x not in t2)
            key = tuple(sorted([tuple(sorted(t1)), tuple(sorted(t2)), tuple(sorted(t3))]))
            if key not in seen:
                seen.add(key)
                result.append(key)
    return result

PARTS = all_partitions(B)

# ── Assertions ────────────────────────────────────────────────────────────────

# I. Target partition
T1, T2, L = (1,3,5), (2,4,6), (7,8,9)
assert sum(T1) == 9  and 9 in SOVEREIGN_ANCHORS
assert sum(T2) == 12 and 12 in SOVEREIGN_TARGETS
assert sum(L)  == 24 and 24 in CASCADE_BASE and 24 in PRIMITIVE_ROOTS_37

# Pairwise sums of block sums
assert sum(T1) + sum(T2) == 21 and 21 in SOVEREIGN_TARGETS
assert sum(T2) + sum(L)  == 36 and 36 in ORBIT_11
assert sum(T1) + sum(L)  == 33 and 33 == 3 * 11

# Block products mod 37
assert prod(T1) % 37 == 15 and 15 in PRIMITIVE_ROOTS_37
assert prod(T2) % 37 == 11 and 11 in ORBIT_11
assert (prod(T1) + prod(T2) + prod(L)) % 37 == 12 and 12 in SOVEREIGN_TARGETS

# Complete residue system mod 3 in each block
for block in [T1, T2, L]:
    assert set(x % 3 for x in block) == {0, 1, 2}

# Total partitions
assert len(PARTS) == 280

# Framework-special partitions
fw_special = [p for p in PARTS if all(sum(b) in FRAMEWORK for b in p)]
assert len(fw_special) == 14

# Type I: {8,13,24} = CASCADE_BASE
type1 = [p for p in fw_special if frozenset(sum(b) for b in p) == frozenset(CASCADE_BASE)]
assert len(type1) == 2
for p in type1:
    assert frozenset(sum(b) for b in p) == {8, 13, 24}

# Type II: {9,12,24}
type2 = [p for p in fw_special if frozenset(sum(b) for b in p) == {9,12,24}]
assert len(type2) == 3
# Target partition is in type2
target_key = tuple(sorted([tuple(sorted(T1)), tuple(sorted(T2)), tuple(sorted(L))]))
assert target_key in type2

# Type IV: {12,12,21} — all sovereign targets
type4 = [p for p in fw_special
         if sorted(sum(b) for b in p) == [12,12,21]]
assert len(type4) == 3
for p in type4:
    for b in p:
        assert sum(b) in SOVEREIGN_TARGETS
        assert dr(sum(b)) == 3

# 137 mod 37 = 26 = 137-map multiplier
assert 137 % 37 == 26

# Total summary
type3 = [p for p in fw_special if frozenset(sum(b) for b in p) == {11,13,21}]
assert len(type3) == 6
assert len(type1) + len(type2) + len(type3) + len(type4) == 14
assert 14 * 20 == 280    # 14/280 = 1/20


if __name__ == '__main__':
    def tag(n):
        t = []
        if is_prime(n):              t.append('p')
        if n in CASCADE_BASE:        t.append('CB')
        if n in SOVEREIGN_ANCHORS:   t.append('SA')
        if n in SOVEREIGN_TARGETS:   t.append('ST')
        if n in PRIMITIVE_ROOTS_37:  t.append('PR')
        if n in ORBIT_11:            t.append('orb11')
        return ','.join(t) if t else '.'

    print("3×3 Triplet Partition Framework")
    print("=" * 55)
    print()
    print("I. Target partition {1,3,5},{2,4,6},{7,8,9}:")
    for name, block in [('T1',T1),('T2',T2),('L',L)]:
        s = sum(block)
        print(f"   {name}={block}: sum={s}({tag(s)})  prod={prod(block)} mod37={prod(block)%37}({tag(prod(block)%37)})")
    print(f"   Pairwise: 9+12=21(ST), 12+24=36(orb11), 9+24=33=3×11")
    print(f"   Sum of products mod37: {(prod(T1)+prod(T2)+prod(L))%37} (ST)")
    print()
    print(f"II–IV. Framework-special partitions: {len(fw_special)}/280 = 1/20")
    for label, grp in [('Type I  {8,13,24}=CASCADE_BASE', type1),
                       ('Type II {9,12,24}=SA+ST+CB',     type2),
                       ('Type III{11,13,21}=orb11+CB+ST', type3),
                       ('Type IV {12,12,21}=all-ST',      type4)]:
        print(f"   {label}: {len(grp)} partitions")
    print()
    print(f"V. 137 mod 37 = {137%37} = 137-map multiplier")
    print()
    print("All assertions passed.")
