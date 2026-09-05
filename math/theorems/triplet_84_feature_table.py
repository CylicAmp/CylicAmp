"""
All 84 Triplets on the 3×3 Board: Complete Feature Table

Board B = {1,...,9}, positions:
  1 2 3
  4 5 6
  7 8 9

For each of the C(9,3)=84 triplets: sum, product, DR, mod-37 residues,
collinearity, adjacency, center membership, mod-3 profile, GF(37) flags.

═══════════════════════════════════════════════════════════════

KEY COUNTS

  Total triplets:                           84
  With GF(37) sum (SA|ST|CB|orbit11):    28
  With prime sum:                           26
  Collinear (row/col/diagonal):              8
  Contains center (5):                      28
  Complete mod-3 {0,1,2} in block:         27
  DR(sum)=3 (sovereign target archetype):  10
  Sum AND prod mod37 both GF(37):        13

═══════════════════════════════════════════════════════════════

COLLINEAR TRIPLETS (rows, columns, diagonals)

  Row 1:  (1,2,3)  sum= 6  mod37= 6  DR=6
  Row 2:  (4,5,6)  sum=15  mod37=15  DR=6
  Row 3:  (7,8,9)  sum=24  mod37=24  DR=6  ← CASCADE_BASE (CB,PR)
  Col 1:  (1,4,7)  sum=12  mod37=12  DR=3  ← SOVEREIGN_TARGET
  Col 2:  (2,5,8)  sum=15  mod37=15  DR=6
  Col 3:  (3,6,9)  sum=18  mod37=18  DR=9
  Diag:   (1,5,9)  sum=15  mod37=15  DR=6
  Anti:   (3,5,7)  sum=15  mod37=15  DR=6

  Of 8 collinear triplets:
    - 1 is a sovereign target: left column (1,4,7) sum=12
    - 1 is cascade base+PR:   bottom row  (7,8,9) sum=24
    - 4 have identical sum=15, DR=6: rows 2, col 2, both diagonals
    - Row 3 and Col 1 are the two GF(37)-collinear triplets

═══════════════════════════════════════════════════════════════

DR(sum) DISTRIBUTION ACROSS 84 TRIPLETS

  DR=1 (LL-O):  sums {10,19}:   9 triplets
  DR=2 (LL-E):  sums {11,20}:   9 triplets
  DR=3 (LH-O):  sums {12,21}:  10 triplets  ← all sovereign targets
  DR=4 (LH-E):  sums {13,22}:   9 triplets
  DR=5 (A51):   sums {14,23}:   9 triplets
  DR=6 (RL-E):  sums {6,15,24}: 10 triplets
  DR=7 (RL-O):  sums {16,25}:   9 triplets
  DR=8 (AHL):   sums {8,17}:    9 triplets
  DR=9 (RH-O):  sums {9,18}:   10 triplets
  Total:                        84
  Distribution is nearly uniform: DR=3,6,9 each have 10 (ST/RL-E/SA arch);
  all others have exactly 9.

  DR=9 appears only once: (1,2,6) sum=9 (SA).
  DR=3 (ST arch) accounts for all 10 triplets summing to 12 or 21.

═══════════════════════════════════════════════════════════════

DOUBLE-SA_ST_CB_O11 TRIPLETS: sum ∈ FW and prod mod37 ∈ FW (13 total)

  (1,2,6):  sum=9(SA)   prod=12  mod37=12(ST)
  (1,3,4):  sum=8(CB)   prod=12  mod37=12(ST)
  (1,3,7):  sum=11(o11) prod=21  mod37=21(ST)
  (1,3,8):  sum=12(ST)  prod=24  mod37=24(CB,PR)
  (1,3,9):  sum=13(CB)  prod=27  mod37=27(orbit11)
  (1,4,6):  sum=11(o11) prod=24  mod37=24(CB,PR)
  (1,5,6):  sum=12(ST)  prod=30  mod37=30(SA+ST dual)
  (2,3,4):  sum=9(SA)   prod=24  mod37=24(CB,PR)
  (2,3,6):  sum=11(o11) prod=36  mod37=36(orbit11)
  (2,3,8):  sum=13(CB)  prod=48  mod37=11(orbit11)
  (2,4,5):  sum=11(o11) prod=40  mod37=3(ST)
  (2,4,6):  sum=12(ST)  prod=48  mod37=11(orbit11)
  (6,7,8):  sum=21(ST)  prod=336 mod37=3(ST)

  Notable: (1,5,6) prod mod37=30, the unique dual SA∩ST element.
           (6,7,8) both sum and prod mod37 are ST (sum=21, prod≡3).
"""

from itertools import combinations
from math import prod, gcd, sqrt

def dr(n): return (n-1)%9+1

def is_prime(n):
    if n<2: return False
    if n==2: return True
    if n%2==0: return False
    return all(n%i!=0 for i in range(3,int(n**0.5)+1,2))

PRIMITIVE_ROOTS_37 = {2,5,13,15,17,18,19,20,22,24,32,35}
CASCADE_BASE       = {8,13,24}
SOVEREIGN_ANCHORS  = {4,9,25,30}
SOVEREIGN_TARGETS  = {3,12,21,30}
ORBIT_11           = {11,27,36}
SA_ST_CB_O11          = SOVEREIGN_ANCHORS|SOVEREIGN_TARGETS|CASCADE_BASE|ORBIT_11

COORDS = {1:(0,0),2:(0,1),3:(0,2),4:(1,0),5:(1,1),6:(1,2),7:(2,0),8:(2,1),9:(2,2)}

def collinear(t):
    (r1,c1),(r2,c2),(r3,c3) = [COORDS[x] for x in t]
    return (r2-r1)*(c3-c1)==(r3-r1)*(c2-c1)

def n_adj(t):
    def adj(a,b):
        r1,c1=COORDS[a]; r2,c2=COORDS[b]
        return abs(r1-r2)<=1 and abs(c1-c2)<=1
    return sum(1 for i in range(3) for j in range(i+1,3) if adj(t[i],t[j]))

ALL = list(combinations(range(1,10),3))
assert len(ALL)==84

# ── Assertions ────────────────────────────────────────────────────────────────

# Total counts
fw_sum  = [t for t in ALL if sum(t) in SA_ST_CB_O11]
prime_s = [t for t in ALL if is_prime(sum(t))]
collin  = [t for t in ALL if collinear(t)]
center  = [t for t in ALL if 5 in t]
mod3c   = [t for t in ALL if set(x%3 for x in t)=={0,1,2}]
dr3     = [t for t in ALL if dr(sum(t))==3]
double_fw = [t for t in ALL if sum(t) in SA_ST_CB_O11 and prod(t)%37 in SA_ST_CB_O11]

assert len(fw_sum)   == 28
assert len(prime_s)  == 26
assert len(collin)   == 8
assert len(center)   == 28
assert len(mod3c)    == 27
assert len(dr3)      == 10
assert len(double_fw)== 13

# Collinear named triplets
ROWS = [(1,2,3),(4,5,6),(7,8,9)]
COLS = [(1,4,7),(2,5,8),(3,6,9)]
DIAG = [(1,5,9),(3,5,7)]
assert all(collinear(t) for t in ROWS+COLS+DIAG)
assert sum(ROWS[2])==24 and 24 in CASCADE_BASE    # bottom row = CB+PR
assert sum(COLS[0])==12 and 12 in SOVEREIGN_TARGETS  # left col = ST

# Four same-sum collinear triplets
same15 = [t for t in collin if sum(t)==15]
assert len(same15)==4  # rows 2, col 2, both diags

# Double-GF(37) triplets
assert (1,5,6) in double_fw
assert prod((1,5,6)) % 37 == 30 and 30 in SOVEREIGN_ANCHORS and 30 in SOVEREIGN_TARGETS
assert (6,7,8) in double_fw
assert sum((6,7,8))==21 and 21 in SOVEREIGN_TARGETS
assert prod((6,7,8))%37==3 and 3 in SOVEREIGN_TARGETS

# Triplets summing to 9 (SA)
sum9 = [t for t in ALL if sum(t)==9]
assert len(sum9)==3
assert set(sum9)=={(1,2,6),(1,3,5),(2,3,4)}

# DR distribution
from collections import Counter
dr_dist = Counter(dr(sum(t)) for t in ALL)
assert dr_dist[3]==10   # ST arch — 10 triplets
assert dr_dist[6]==10   # RL-E — 10 triplets
assert dr_dist[9]==10   # SA arch — 10 triplets
# DR=3,6,9 each appear 10 times; all others appear 9 times
for d in [1,2,4,5,7,8]:
    assert dr_dist[d]==9


if __name__ == '__main__':
    def tag(n):
        t=[]
        if is_prime(n):              t.append('p')
        if n in CASCADE_BASE:        t.append('CB')
        if n in SOVEREIGN_ANCHORS:   t.append('SA')
        if n in SOVEREIGN_TARGETS:   t.append('ST')
        if n in PRIMITIVE_ROOTS_37:  t.append('PR')
        if n in ORBIT_11:            t.append('o11')
        return ','.join(t) if t else '.'

    print("84 Triplets — Feature Summary")
    print("="*50)
    print(f"GF(37) sum:     {len(fw_sum):3d}/84")
    print(f"Prime sum:         {len(prime_s):3d}/84")
    print(f"Collinear:         {len(collin):3d}/84")
    print(f"Contains center:   {len(center):3d}/84")
    print(f"Complete mod-3:    {len(mod3c):3d}/84")
    print(f"DR(sum)=3:         {len(dr3):3d}/84")
    print(f"Double-GF(37):  {len(double_fw):3d}/84")
    print()
    print("DR distribution:")
    for d in range(1,10):
        print(f"  DR={d}: {dr_dist[d]:2d} triplets")
    print()
    print("Double-GF(37) triplets:")
    for t in double_fw:
        s=sum(t); p=prod(t)
        print(f"  {t}: sum={s}({tag(s)}) prod={p} mod37={p%37}({tag(p%37)})")
    print()
    print("All assertions passed.")


# ── 147: Left Column Chain ───────────────────────────────────────────────────

# 147 mod37=36 (orbit of 11), DR=3 (ST arch)
assert 147 % 37 == 36 and 36 in ORBIT_11
assert dr(147) == 3

# Chain: 1+4=5 (A51), 5+7=12 (ST) = (123)
assert 1 + 4 == 5
assert 5 + 7 == 12 and 12 in SOVEREIGN_TARGETS
assert int(str(12)[0]) == 1 and int(str(12)[1]) == 2 and dr(12) == 3

# Cumulative path 1->5->12: LL-O -> A51 -> ST
assert [1, 1+4, 1+4+7] == [1, 5, 12]
assert [dr(s) for s in [1,5,12]] == [1, 5, 3]

# Product: 1*4*7=28, complement of SA=9 in GF(37)
assert 1*4*7 == 28 and 28 + 9 == 37
