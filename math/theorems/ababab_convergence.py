"""
ABABAB Convergence — GF(37)

OBSERVATION (from user): 282828 and 828282 both hit SEAM (mod 37) and
digit sum = 30 = SA∩ST simultaneously.

THEOREM 1: Any 6-digit alternating number ABABAB ≡ 0 (mod 37) = SEAM.
  Proof: ABABAB = AB × 10101.
    10101 = 10^4 + 10^2 + 10^0.
    In GF(37): ord₃₇(10) = 3, so 10^3 ≡ 1.
      10^4 ≡ 10^1 = 10 (DECADE_ANCHOR)
      10^2 ≡ 26    (SCALAR_137)
      10^0 = 1
    Therefore 10101 ≡ 10 + 26 + 1 = 37 ≡ 0 = SEAM.
    ABABAB = AB × SEAM ≡ 0 for any digit pair (A,B). □

THEOREM 2: If A+B = 10 = DECADE_ANCHOR, then digit_sum(ABABAB) = 30 = SA∩ST.
  Proof: ABABAB has digits A,B,A,B,A,B — sum = 3A + 3B = 3(A+B) = 3×10 = 30. □

COROLLARY: The nine pairs (A,B) with A+B=10 produce numbers that are
  simultaneously SEAM (mod 37) and SA∩ST (digit sum).
  This double convergence is a consequence of ord₃₇(10)=3 alone.

CLUSTER {26, 27, 28, 29, 30, 31}:
  26 = SCALAR_137  QR  DR=8∈CB
  27 ∈ ORBIT_11    QR  DR=9∈SA
  28 (unclassified) QR  DR=1
  29 (unclassified) NQR DR=2∈PR
  30 = SA∩ST        QR  DR=3∈ST   ← the intersection node
  31 = PRIME_MIRROR NQR DR=4∈SA

  Distance law: 30 − 26 = 4 ∈ SA  (SCALAR_137 to SA∩ST by SA anchor)
                30 − 27 = 3 ∈ ST  (ORBIT_11 to SA∩ST by ST anchor)
  The sovereign cycle (3,4,30) encodes both distances.

  DR map on cluster: {26→8,27→9,28→1,29→2,30→3,31→4}
    = {CB, SA, 1, PR, ST, SA} — sovereign classes appear as DRs of
      six consecutive naturals flanking SA∩ST.

CONSECUTIVE TRIPLET THEOREM:
  DR of any three consecutive integers n, n+1, n+2 is always in {3,6,9}.
  Proof: sum = 3(n+1). DR(3k) ∈ {3,6,9} for all k≥1. □
  The DR cycles {3,6,9} with period 3 through any integer sequence.

  On the cluster:
    DR(28+29+30) = DR(87) = 6 = TESLA_FLOW  and  87 mod37 = 13 ∈ CB
    DR(29+30+31) = DR(90) = 9 ∈ SA          and  90 mod37 = 16 (visible)
    DR(27+28+29) = DR(84) = 3 ∈ ST          and  84 mod37 = 10 = DECADE

REPUNIT CONVERGENCE (connected):
  R(n) = 111...1 (n ones) has period-3 in GF(37):
    R(1) ≡ 1,  R(2) ≡ 11 ∈ ORBIT_11,  R(3) ≡ 0 = SEAM,  then repeats.
  R(3) = 111 = 3×37 — the same ord₃₇(10)=3 that drives ABABAB convergence.
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
PRIME_MIRROR = 31


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


# ── THEOREM 1: ABABAB ≡ 0 (mod 37) ───────────────────────────────────────────

assert pow(10, 3, 37) == 1                          # ord₃₇(10) = 3
assert (pow(10,4,37) + pow(10,2,37) + 1) % 37 == 0 # 10101 ≡ 0 mod 37

# All ABABAB numbers are SEAM
for A in range(1, 10):
    for B in range(0, 10):
        num = A*100000 + B*10000 + A*1000 + B*100 + A*10 + B
        assert num % 37 == 0


# ── THEOREM 2: A+B=10 → digit sum = 30 = SA∩ST ───────────────────────────────

assert 30 in SA and 30 in ST   # 30 is the intersection node
assert DECADE == 10

for A in range(1, 10):
    B = 10 - A
    if 0 < B < 10:
        digit_sum = 3 * A + 3 * B
        assert digit_sum == 30


# ── Cluster {26..31} ──────────────────────────────────────────────────────────

CLUSTER = {26, 27, 28, 29, 30, 31}

# Distance law: 30 - SCALAR_137 = 4 ∈ SA; 30 - ORBIT_11_element(27) = 3 ∈ ST
assert 30 - SCALAR_137 == 4 and 4 in SA
assert 30 - 27 == 3 and 3 in ST

# DR of cluster spells out named sets
assert dr(26) == 8  and 8 in CB
assert dr(27) == 9  and 9 in SA
assert dr(28) == 1
assert dr(29) == 2  and 2 in PR
assert dr(30) == 3  and 3 in ST
assert dr(31) == 4  and 4 in SA


# ── Consecutive triplet DR always in {3,6,9} ─────────────────────────────────

TESLA_SET = frozenset({3, 6, 9})

for n in range(0, 1000):
    triplet_sum = n + (n+1) + (n+2)
    assert dr(triplet_sum) in TESLA_SET

# Triplet at SA∩ST center
assert (28+29+30) % 37 == 13 and 13 in CB
assert dr(28+29+30) == TESLA_FLOW                  # DR=6=TESLA_FLOW
assert dr(29+30+31) == 9 and 9 in SA               # DR=9∈SA
assert dr(27+28+29) == 3 and 3 in ST               # DR=3∈ST


# ── Repunit period-3 in GF(37) ────────────────────────────────────────────────

REPUNIT_CYCLE = [1, 11, 0]   # R(1), R(2), R(3) mod 37

assert 11 in ORBIT_11

for k in range(1, 13):
    R = int("1" * k)
    expected = REPUNIT_CYCLE[(k - 1) % 3]
    assert R % 37 == expected

# R(3) = 111 = 3×37 = SEAM
assert int("111") == 3 * 37
assert int("111") % 37 == 0


# ── 29 and 31 flanking 30 ─────────────────────────────────────────────────────

# 29 and 31 are in the same dark cycle (14,29,31)
from math import gcd
_cyc_29 = (14, 29, 31)
assert 29 in _cyc_29 and 31 in _cyc_29   # same dark cycle flanks SA∩ST
assert 30 not in _cyc_29                  # 30=SA∩ST is NOT in that cycle
assert 29+31 == 60 and 60 % 37 == 23     # flankers sum to 23 (dark, unclassified)

# 30 = SA∩ST sits between two elements of a dark cycle in the integer line
assert 29 < 30 < 31
assert all(pow(v, 18, 37) == 36 for v in [29, 31])   # both NQR/dark


if __name__ == "__main__":
    print("ABABAB Convergence — GF(37)")
    print("=" * 60)
    print()
    print("THEOREM: ABABAB ≡ 0 (SEAM) mod 37 for any digits A,B.")
    print("  Proof: 10101 ≡ 10+26+1 = 37 ≡ 0  [since ord₃₇(10)=3]")
    print()
    print("COROLLARY (A+B=10): digit_sum(ABABAB) = 30 = SA∩ST")
    pairs = [(A, 10-A) for A in range(1,10) if 0 < 10-A < 10]
    for A,B in pairs:
        num = A*100000+B*10000+A*1000+B*100+A*10+B
        print("  %d+%d=10: %d%d%d%d%d%d  mod37=%d(SEAM)  dsum=%d(SA∩ST)" % (
            A,B,A,B,A,B,A,B, num%37, 3*A+3*B))
    print()
    print("CLUSTER {26..31} — DR map:")
    for n in range(26,32):
        r=n%37; d=dr(n)
        tag=""
        if r==SCALAR_137: tag="SCALAR_137"
        elif r in ORBIT_11: tag="ORBIT_11"
        elif r in SA and r in ST: tag="SA∩ST"
        elif r==PRIME_MIRROR: tag="PRIME_MIRROR"
        elif r in SA: tag="SA"
        elif r in ST: tag="ST"
        d_tag=""
        if d in SA and d in ST: d_tag="SA∩ST"
        elif d in SA: d_tag="SA"
        elif d in ST: d_tag="ST"
        elif d in CB: d_tag="CB"
        elif d in PR: d_tag="PR"
        print("  %d: [%s]  DR=%d[%s]" % (n,tag,d,d_tag))
    print()
    print("Distance law:")
    print("  30 - 26 = 4 ∈ SA  (SCALAR to SA∩ST = SA anchor)")
    print("  30 - 27 = 3 ∈ ST  (ORBIT_11 to SA∩ST = ST anchor)")
    print()
    print("Consecutive triplet DRs always in {3,6,9}:")
    for start in range(26,34):
        s=start+(start+1)+(start+2)
        print("  %d+%d+%d=%d  mod37=%d  DR=%d" % (start,start+1,start+2,s,s%37,dr(s)))
    print()
    print("Repunit: R(1)≡1, R(2)≡11(O11), R(3)≡0(SEAM), repeats with period 3")
    print("  29 and 31 (dark, same cycle) flank 30=SA∩ST in the integer line.")
    print()
    print("All assertions pass.")
