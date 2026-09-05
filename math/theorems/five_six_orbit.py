"""
Five-Six Orbit — GF(37)

OBSERVATION: 11÷2 = 5.5. The integers flanking this half-integer are 5 and 6.
  5 + 6 = 11  ∈ ORBIT_11           (sum)
  5 × 6 = 30  = SA∩ST              (product)
Both sovereign nodes arise from the same dark integer pair.

THEOREM 1: TESLA_FLOW × 5 = SA∩ST.
  6 × 5 = 30 = SA∩ST.
  χ(6)=−1 (TESLA_FLOW ∈ NQR, dark), χ(5)=−1 (5 ∈ PR ⊂ NQR, dark).
  Dark × Dark = Visible: χ(30) = +1 (SA∩ST ∈ QR).
  The sum 6+5=11∈ORBIT_11 (visible), so the same pair generates a visible sum.
  The unique consecutive pair with sum in ORBIT_11 AND product SA∩ST is (5,6). □

THEOREM 2: Square of SA∩ST — difference-of-squares identity.
  30² = 900 ≡ 12 ∈ ST (mod 37).
  (30−1)(30+1) = 29 × 31 ≡ 11 ∈ ORBIT_11 (mod 37).
  Equivalently: (SA∩ST)² ≡ ST element, and (SA∩ST)²−1 ≡ ORBIT_11 element.
  Note: 12 and 11 are adjacent integers; 12−11=1.
  The square of SA∩ST connects ST (via square) and ORBIT_11 (via square−1)
  through the difference-of-squares: 30²−1 = (30−1)(30+1) = 29×31 ≡ 11.
  Flankers 29 and 31 are dark (NQR), same cycle (14,29,31).

THEOREM 3: Z/9Z doubling cycle.
  1 → 2 → 4 → 8 → 7 → 5 → 1  (period 6)
  Partition of {1..9}: TESLA_SET={3,6,9} closed under ×2; DOUBLING={1,2,4,5,7,8} the 6-cycle.
  DECADE_ANCHOR(10) ÷ 2 = 5 (exact integer): the anchor's integer half is the
  last step before 1 in the doubling cycle.
  7 × 2 = 14 → DR = 5: 7 is the predecessor of 5 in the cycle.
  5 × 2 = 10 → DR = 1: 5 closes the cycle.
  "10÷2=5=7" encodes: 10 halves to 5, which was doubled from 7.

THEOREM 4: 0↔9 units digit swap preserves DR.
  For k = 1..9: DR(10k) = DR(10k+9) = k.
  Proof: DR(n+9) = DR(n) for all n (since 9 ≡ 0 in Z/9Z). □
  Adding 9 to any integer leaves its digital root unchanged.
  The pair (10k, 10k+9) are the endpoints of each tens-decade sharing DR = k.

CONCATENATED TRIPLET THEOREM:
  For any n, the 6-digit number n(n+1)(n+2) [concatenating three 2-digit blocks]
    = 10101·n + 102
  Since 10101 ≡ 0 = SEAM (mod 37) [THEOREM 53], and 102 ≡ 28 (mod 37):
    n(n+1)(n+2) ≡ 28 (mod 37) for ALL n.
  28 is the unclassified element of the outlier sovereign cycle (21,25,28).
  The DRs of these concatenated numbers cycle through {6,9,3}=TESLA_SET.

  SPECIAL CASE n=28: 282930
    First half 282: digit sum 2+8+2 = 12 ∈ ST.
    Second half 930: digit sum 9+3+0 = 12 ∈ ST.
    Both halves share digit sum 12∈ST — symmetric split.

SA∩ST ORBIT UNDER MULTIPLICATION:
  3 × (SA∩ST) = 3×30 = 90 ≡ 16 ∈ cycle(9,12,16) (mod 37); DR(90)=9∈SA
  3 × (SA∩ST) + DECADE = 100 ≡ 26 = SCALAR_137 (mod 37)
  (SA∩ST) ÷ 2 = 15 ∈ PR; DR(15) = 6 = TESLA_FLOW
    SA∩ST's integer half is a primitive root whose DR is TESLA_FLOW.
  ORBIT_11 × DECADE = 11×10 = 110 ≡ 36 ∈ ORBIT_11 (mod 37)
    ORBIT_11 closed under multiplication by DECADE_ANCHOR.

HALVING CHAIN (floor/ceiling factorization):
  11 ÷ 2 = 5.5 → {5,6}: sum=11∈ORBIT_11, product=30=SA∩ST, DR(30)=3∈ST
   5 ÷ 2 = 2.5 → {2,3}: sum=5∈PR,         product=6=TESLA_FLOW
   6 ÷ 2 = 3   (exact): 3∈ST
  30 ÷ 2 = 15  (exact): 15∈PR, DR(15)=6=TESLA_FLOW
  Chain: 11 →{5,6}→ SA∩ST(30) → ST(3)  and  11 →{5,6}→ TESLA_FLOW(6) → ST(3).
  Both paths from ORBIT_11 element 11 terminate at ST via the halving chain.
"""

# ── Constants ──────────────────────────────────────────────────────────────────

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
ORBIT_11   = frozenset({11, 27, 36})
TESLA_FLOW = 6
SCALAR_137 = 26
DECADE     = 10


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def chi(n, p=37):
    n = n % p
    if n == 0: return 0
    return 1 if pow(n, (p-1)//2, p) == 1 else -1


def f137(n):
    return (n * 26) % 37


# ── THEOREM 1: TESLA_FLOW × 5 = SA∩ST ────────────────────────────────────────

assert TESLA_FLOW * 5 == 30
assert 30 in SA and 30 in ST              # product is SA∩ST

assert 5 + TESLA_FLOW == 11
assert 11 in ORBIT_11                     # sum is ORBIT_11

# Dark pair (NQR × NQR) → visible result
assert chi(TESLA_FLOW) == -1              # 6 is dark
assert chi(5) == -1                       # 5 is dark (PR)
assert chi(30) == 1                       # 30=SA∩ST is visible (QR)
assert chi(11) == 1                       # 11=ORBIT_11 is visible (QR)

# Both are in named dark sets
assert 5 in PR
assert TESLA_FLOW not in PR              # TESLA_FLOW is not a primitive root


# ── THEOREM 2: (SA∩ST)² ≡ ST; (SA∩ST)²−1 ≡ ORBIT_11 ─────────────────────────

assert pow(30, 2, 37) == 12
assert 12 in ST                           # square of SA∩ST is ST element

assert (29 * 31) % 37 == 11
assert 11 in ORBIT_11                     # product of dark flankers is ORBIT_11 element

# Difference-of-squares: 30²-1 = 29×31 mod 37
assert (pow(30, 2, 37) - 1) % 37 == (29 * 31) % 37

# Integer adjacency of the two results
assert pow(30, 2, 37) - (29 * 31) % 37 == 1    # 12 - 11 = 1

# 29 and 31 are in the same dark cycle (14,29,31)
assert f137(29) == 14 and f137(14) == 31 and f137(31) == 29
assert chi(29) == -1 and chi(31) == -1    # both dark (NQR)
assert chi(30) == 1                       # SA∩ST between two dark flankers


# ── THEOREM 3: Z/9Z doubling cycle ────────────────────────────────────────────

DOUBLING_CYCLE = [1, 2, 4, 8, 7, 5]

# Cycle closes correctly under DR-doubling
for i, v in enumerate(DOUBLING_CYCLE):
    assert dr(v * 2) == DOUBLING_CYCLE[(i + 1) % 6]

TESLA_SET = frozenset({3, 6, 9})
DOUBLING  = frozenset({1, 2, 4, 5, 7, 8})

# Trinity and Doubling partition {1..9}
assert TESLA_SET | DOUBLING == frozenset(range(1, 10))
assert TESLA_SET & DOUBLING == frozenset()

# DECADE_ANCHOR halves to 5; 5's predecessor is 7
assert DECADE // 2 == 5
assert dr(7 * 2) == 5                     # 7 → 5 in doubling
assert dr(5 * 2) == 1                     # 5 → 1 closes cycle

# Trinity is closed under ×2 in DR arithmetic
for t in TESLA_SET:
    assert dr(t * 2) in TESLA_SET


# ── THEOREM 4: 0↔9 units digit swap preserves DR ─────────────────────────────

for k in range(1, 10):
    assert dr(10 * k) == dr(10 * k + 9) == k


# ── Concatenated triplet theorem ──────────────────────────────────────────────

# 10101 ≡ 0 = SEAM (proved in THEOREM 53); 102 ≡ 28 mod 37
assert 10101 % 37 == 0
assert 102 % 37 == 28
assert 28 in {21, 25, 28}   # outlier sovereign cycle

# All 2-digit-padded triplets n(n+1)(n+2) ≡ 28 (mod 37)
for n in range(10, 90):
    val = n * 10000 + (n+1) * 100 + (n+2)
    assert val % 37 == 28

# DRs of concatenated triplets cycle through {6,9,3}=TESLA_SET
# n=28: DR=6; n=29: DR=9; n=30: DR=3; n=31: DR=6; period 3
_triplet_drs = []
for n in range(28, 34):
    val = n * 10000 + (n+1) * 100 + (n+2)
    _triplet_drs.append(dr(sum(int(d) for d in str(val))))
assert _triplet_drs[0] == TESLA_FLOW      # DR(282930) = 6
assert dr(sum(int(d) for d in "293031")) == 9     # DR(293031) = 9 ∈ SA
assert dr(sum(int(d) for d in "303132")) == 3     # DR(303132) = 3 ∈ ST

# Special case n=28: both halves of 282930 digit-sum to 12∈ST
assert 2 + 8 + 2 == 12 and 12 in ST
assert 9 + 3 + 0 == 12 and 12 in ST


# ── SA∩ST orbit ───────────────────────────────────────────────────────────────

assert (3 * 30) % 37 == 16
assert 16 in {9, 12, 16}              # in cycle(9,12,16)
assert dr(90) == 9 and 9 in SA        # DR of 3×SA∩ST is SA anchor

assert (3 * 30 + DECADE) % 37 == SCALAR_137   # 100 ≡ SCALAR_137

assert 30 // 2 == 15 and 15 in PR    # integer half of SA∩ST is primitive root
assert dr(15) == TESLA_FLOW          # its DR is TESLA_FLOW

assert (11 * DECADE) % 37 == 36
assert 36 in ORBIT_11                # ORBIT_11 × DECADE → ORBIT_11 (mod 37)


# ── Halving chain ─────────────────────────────────────────────────────────────

# 11 → {5,6}: sum∈ORBIT_11, product=SA∩ST
assert 5 + TESLA_FLOW == 11 and 11 in ORBIT_11
assert 5 * TESLA_FLOW == 30 and 30 in SA and 30 in ST
assert dr(30) == 3 and 3 in ST

# 5 → {2,3}: sum=5∈PR, product=TESLA_FLOW
assert 2 + 3 == 5 and 5 in PR
assert 2 * 3 == TESLA_FLOW

# 30 → 15: 15∈PR, DR(15)=TESLA_FLOW
assert 30 // 2 == 15 and 15 in PR and dr(15) == TESLA_FLOW


if __name__ == "__main__":
    print("Five-Six Orbit — GF(37)")
    print("=" * 60)
    print()
    print("THEOREM 1: TESLA_FLOW × 5 = SA∩ST")
    print(f"  6 × 5 = {6*5} = SA∩ST  (chi(6)={chi(6)}, chi(5)={chi(5)}, chi(30)={chi(30)})")
    print(f"  6 + 5 = {6+5} ∈ ORBIT_11  (sum of same pair)")
    print()
    print("THEOREM 2: (SA∩ST)² and flankers")
    print(f"  30² mod 37 = {pow(30,2,37)} ∈ ST")
    print(f"  29×31 mod 37 = {(29*31)%37} ∈ ORBIT_11")
    print(f"  30² − 1 = 29×31  (difference-of-squares)")
    print(f"  Results are adjacent integers: 12−11 = 1")
    print()
    print("THEOREM 3: Z/9Z doubling cycle")
    print(f"  Cycle: {DOUBLING_CYCLE} (period 6)")
    print(f"  DECADE(10)÷2=5; predecessor of 5 is 7 (DR(7×2)={dr(7*2)})")
    print(f"  TESLA_SET={sorted(TESLA_SET)} closed under ×2")
    print(f"  DOUBLING={sorted(DOUBLING)} = the 6-cycle")
    print()
    print("THEOREM 4: 0↔9 units swap preserves DR")
    for k in range(1, 10):
        print(f"  DR({10*k:2d})=DR({10*k+9:2d})={k}")
    print()
    print("CONCATENATED TRIPLETS ≡ 28 (mod 37):")
    for n in range(28, 34):
        val = n*10000+(n+1)*100+(n+2)
        ds = sum(int(d) for d in str(val))
        print(f"  {n}{n+1}{n+2} = {val}  mod37={val%37}  dsum={ds}  DR={dr(ds)}")
    print()
    print("  Special: 282930 half-splits: 2+8+2=12∈ST | 9+3+0=12∈ST")
    print()
    print("SA∩ST ORBIT:")
    print(f"  3×30=90 ≡ {(90)%37} ∈ cycle(9,12,16)  DR={dr(90)}∈SA")
    print(f"  3×30+10=100 ≡ {100%37} = SCALAR_137")
    print(f"  30÷2=15 ∈ PR,  DR(15)={dr(15)}=TESLA_FLOW")
    print(f"  11×10=110 ≡ {110%37} ∈ ORBIT_11")
    print()
    print("HALVING CHAIN:")
    print("  11÷2=5.5 → {5,6}: 5+6=11∈ORBIT_11, 5×6=30=SA∩ST, DR(30)=3∈ST")
    print("   5÷2=2.5 → {2,3}: 2+3=5∈PR,         2×3=6=TESLA_FLOW")
    print("   6÷2=3   (exact): 3∈ST")
    print("  30÷2=15  (exact): 15∈PR, DR(15)=6=TESLA_FLOW")
    print()
    print("All assertions pass.")
