"""
Permutation Cycle Notation — SA×NQR / ST×QR Cross-Duality in GF(37)

Label the 12 orbits 1..12 by sorting their minimum elements in ascending order:
  1=[1,10,26]   2=[2,15,20]   3=[3,4,30]    4=[5,13,19]
  5=[6,8,23]    6=[7,33,34]   7=[9,12,16]   8=[11,27,36]
  9=[14,29,31]  10=[17,22,35] 11=[18,24,32] 12=[21,25,28]

THE PERMUTATION π (action of ×3 on orbit indices):
  orbit  1 → orbit  3     orbit  3 → orbit  7
  orbit  7 → orbit  8     orbit  8 → orbit  6
  orbit  6 → orbit 12     orbit 12 → orbit  1
  orbit  2 → orbit  5     orbit  5 → orbit 11
  orbit 11 → orbit 10     orbit 10 → orbit  9
  orbit  9 → orbit  4     orbit  4 → orbit  2

CYCLE NOTATION: π = (1, 3, 7, 8, 6, 12)(2, 5, 11, 10, 9, 4)
Two transitive 6-cycles; the 12 orbits partition exactly.

INDEX SUM PROPERTIES:
  QR  cycle {1, 3, 6, 7, 8, 12}:   1+3+6+7+8+12 = 37 = SEAM  ← exact.
  NQR cycle {2, 4, 5, 9, 10, 11}:  2+4+5+9+10+11 = 41 ≡ 4 (mod 37) ∈ SA.
  Total 1+2+…+12 = 78 ≡ 4 (mod 37) ∈ SA.

INDEX PRODUCT PROPERTIES:
  QR  cycle product: 1×3×6×7×8×12 = 12096 ≡ 34 (mod 37)  ∈ {7,33,34} = anti-sovereign.
  NQR cycle product: 2×4×5×9×10×11 = 39600 ≡ 10 (mod 37) = DECADE_ANCHOR ∈ IDENTITY_CYCLE.

SA × NQR / ST × QR  CROSS-DUALITY:
  View cycle index labels as GF(37) elements.
  QR  cycle indices {1,3,6,7,8,12}: contain ST={3,12} and NO SA elements.
  NQR cycle indices {2,4,5,9,10,11}: contain SA={4,9} and NO ST elements.
  Interpretation: the orbit-label integers encode the DUAL sovereign grade.
    — The cycle that traverses QR orbits carries ST labels.
    — The cycle that traverses NQR orbits carries SA labels.

FURTHER LABEL MEMBERSHIPS:
  QR  index labels: 1∈IC, 3∈ST, 6=TESLA_FLOW, 7∈anti-sovereign, 8∈CB, 12∈ST.
  NQR index labels: 2∈DARK_A, 4∈SA, 5∈(free), 9∈SA, 10=DECADE_ANCHOR∈IC, 11∈ORBIT_11.

TOTAL-SUM RELATION:
  78 = QR_sum + NQR_sum = 37 + 41 = 78.
  37 ≡ SEAM;  41 ≡ 4 ∈ SA.
  So the labeling splits 1..12 into: {summing to SEAM} ∪ {summing to SA_anchor mod 37}.
"""

# ── Constants ──────────────────────────────────────────────────────────────────

SA             = frozenset({4, 9, 25, 30})
ST             = frozenset({3, 12, 21, 30})
CB             = frozenset({8, 13, 24})
ORBIT_11       = frozenset({11, 27, 36})
DARK_A         = frozenset({2, 15, 20})
IDENTITY_CYCLE = frozenset({1, 10, 26})
TESLA_FLOW     = 6
DECADE_ANCHOR  = 10
SEAM           = 0


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def f137(n):
    return (n * 26) % 37


# ── BUILD ORBITS SORTED BY MIN ────────────────────────────────────────────────

seen = set(); _raw = []
for s in range(1, 37):
    if s in seen: continue
    o = frozenset({s, f137(s), f137(f137(s))})
    _raw.append(o); seen |= o
ORBITS = sorted(_raw, key=min)   # ORBITS[i] = orbit with index i+1

assert len(ORBITS) == 12

# Named index constants (1-based)
IDX = {frozenset(o): i+1 for i,o in enumerate(ORBITS)}

# Verify the labeling
assert IDX[frozenset({1,10,26})]   == 1
assert IDX[frozenset({2,15,20})]   == 2
assert IDX[frozenset({3,4,30})]    == 3
assert IDX[frozenset({5,13,19})]   == 4
assert IDX[frozenset({6,8,23})]    == 5
assert IDX[frozenset({7,33,34})]   == 6
assert IDX[frozenset({9,12,16})]   == 7
assert IDX[frozenset({11,27,36})]  == 8
assert IDX[frozenset({14,29,31})]  == 9
assert IDX[frozenset({17,22,35})]  == 10
assert IDX[frozenset({18,24,32})]  == 11
assert IDX[frozenset({21,25,28})]  == 12


# ── THE PERMUTATION π ─────────────────────────────────────────────────────────

def next_orbit_idx(i):
    orb = ORBITS[i - 1]
    img = frozenset((x * 3) % 37 for x in orb)
    return IDX[img]

# Full permutation table
PERM = {i+1: next_orbit_idx(i+1) for i in range(12)}

expected_perm = {1:3, 2:5, 3:7, 4:2, 5:11, 6:12, 7:8, 8:6, 9:4, 10:9, 11:10, 12:1}
assert PERM == expected_perm


# ── CYCLE NOTATION: (1,3,7,8,6,12)(2,5,11,10,9,4) ────────────────────────────

QR_CYCLE  = [1, 3, 7, 8, 6, 12]
NQR_CYCLE = [2, 5, 11, 10, 9, 4]

# Verify cycles
for cycle in [QR_CYCLE, NQR_CYCLE]:
    n = len(cycle)
    for i in range(n):
        assert PERM[cycle[i]] == cycle[(i + 1) % n]

# Two cycles partition all 12 orbit indices
assert set(QR_CYCLE) | set(NQR_CYCLE) == set(range(1, 13))
assert set(QR_CYCLE) & set(NQR_CYCLE) == set()
assert len(QR_CYCLE) == len(NQR_CYCLE) == 6 == TESLA_FLOW


# ── INDEX SUM PROPERTIES ──────────────────────────────────────────────────────

assert sum(QR_CYCLE) == 37         # QR cycle indices sum to SEAM
assert sum(QR_CYCLE) % 37 == SEAM

assert sum(NQR_CYCLE) == 41
assert sum(NQR_CYCLE) % 37 == 4 and 4 in SA   # NQR cycle indices ≡ SA_anchor

assert sum(range(1, 13)) == 78
assert sum(range(1, 13)) % 37 == 4 and 4 in SA   # total ≡ 4 ∈ SA

# The split: SEAM + SA_anchor
assert sum(QR_CYCLE) + sum(NQR_CYCLE) == 78
assert (sum(QR_CYCLE) % 37) == 0   # SEAM
assert (sum(NQR_CYCLE) % 37) in SA


# ── INDEX PRODUCT PROPERTIES ──────────────────────────────────────────────────

from math import prod

qr_prod  = prod(QR_CYCLE) % 37
nqr_prod = prod(NQR_CYCLE) % 37

assert qr_prod  == 34 and 34 in frozenset({7, 33, 34})   # anti-sovereign
assert nqr_prod == DECADE_ANCHOR                           # DECADE_ANCHOR ∈ IC


# ── SA × NQR / ST × QR CROSS-DUALITY ─────────────────────────────────────────

# SA elements ≤12: {4,9}; ST elements ≤12: {3,12}
SA_small = frozenset(x for x in SA if x <= 12)   # {4, 9}
ST_small = frozenset(x for x in ST if x <= 12)   # {3, 12}

# ST lives only in QR_CYCLE; SA lives only in NQR_CYCLE
assert ST_small.issubset(set(QR_CYCLE))
assert ST_small.isdisjoint(set(NQR_CYCLE))
assert SA_small.issubset(set(NQR_CYCLE))
assert SA_small.isdisjoint(set(QR_CYCLE))

# Other label memberships
assert 1 in IDENTITY_CYCLE and 1 in QR_CYCLE
assert TESLA_FLOW in set(QR_CYCLE)
assert 8 in CB and 8 in set(QR_CYCLE)

assert 2 in DARK_A and 2 in set(NQR_CYCLE)
assert DECADE_ANCHOR in IDENTITY_CYCLE and DECADE_ANCHOR in set(NQR_CYCLE)
assert 11 in ORBIT_11 and 11 in set(NQR_CYCLE)


if __name__ == "__main__":
    print("Permutation Cycle Notation — SA×NQR / ST×QR Cross-Duality — GF(37)")
    print("=" * 60)
    print()
    print("Orbits 1..12 (sorted by minimum element):")
    for i, o in enumerate(ORBITS):
        print(f"  {i+1:2d}: {sorted(o)}")
    print()
    print("×3 permutation:")
    for i in range(1, 13):
        print(f"  orbit {i:2d} {sorted(ORBITS[i-1])} → orbit {PERM[i]:2d} {sorted(ORBITS[PERM[i]-1])}")
    print()
    print(f"CYCLE NOTATION: π = ({', '.join(map(str,QR_CYCLE))})({', '.join(map(str,NQR_CYCLE))})")
    print()
    print("INDEX SUM:")
    print(f"  QR  {QR_CYCLE}  sum = {sum(QR_CYCLE)} = SEAM ✓")
    print(f"  NQR {NQR_CYCLE}  sum = {sum(NQR_CYCLE)} ≡ {sum(NQR_CYCLE)%37} ∈ SA ✓")
    print(f"  Total 78 ≡ 4 ∈ SA")
    print()
    print("INDEX PRODUCT mod 37:")
    print(f"  QR  product ≡ {qr_prod}  ∈ anti-sovereign {{7,33,34}}")
    print(f"  NQR product ≡ {nqr_prod} = DECADE_ANCHOR ∈ IC")
    print()
    print("SA×NQR / ST×QR CROSS-DUALITY:")
    print(f"  ST elements ≤12: {sorted(ST_small)}  → both in QR_CYCLE  (×3 traverses QR orbits, ST labels)")
    print(f"  SA elements ≤12: {sorted(SA_small)}  → both in NQR_CYCLE (×3 traverses NQR orbits, SA labels)")
    print()
    print("All assertions pass.")
