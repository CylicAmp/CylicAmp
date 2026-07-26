"""
Digit Sequence DR Coverage and the DR=2 Gap — GF(37)

THE BASE: {1,2,3,4}
  Sum = 10.  DR(10) = 1.  Literal sum written as 10 in notation.

REMOVAL FROM {1,2,3,4} — four 3-element subsets:
  Remove 1: {2,3,4} → sum=9,  DR=9   mod37=12∈ST
  Remove 2: {1,3,4} → sum=8,  DR=8   mod37=23∈{6,8,23}=TESLA_FLOW_orbit
  Remove 3: {1,2,4} → sum=7,  DR=7   mod37=13∈CB
  Remove 4: {1,2,3} → sum=6,  DR=6   mod37=12∈ST
  Removing digit d reduces sum by exactly d.
  DR values covered by removal: {6,7,8,9}

FIBONACCI TRIPLE RULE: (a, b, a+b)
  Sum = 2(a+b).  DR = DR(2(a+b)).
  The third element is the sum of the first two — three slots.

SINGLE-DIGIT CONSTRAINT (a+b ≤ 9, all three numbers ≤ 9):
  Possible triple sums: 2×{2,...,9} = {4,6,8,10,12,14,16,18}
  DR values:  {4, 6, 8, 1, 3,  5,  7,  9}
  Covered: {1,3,4,5,6,7,8,9}
  MISSING: DR=2

THE DR=2 GAP:
  For DR(2(a+b))=2: need a+b ≡ 1 (mod 9).
  Minimum with a,b ≥ 1: a+b = 10  (c=10 is TWO digits).
  Minimum with a ≥ 0, b ≥ 0: a+b = 1 → requires a=0 (SEAM element).
  With 0: (0,1,1) → sum=2, DR=2.  SEAM completes the coverage.
  With two-digit c: (1,9,10) or (4,6,10) → sum=20, DR=2.

  The OUTLIER_SOV connection:
    a+b = 28 (OUTLIER_SOV element, the SEAM-exit node):
    Triple sum = 2×28 = 56.  DR(56)=DR(11)=2.
    Any triple (a,b,28) with a+b=28 gives DR=2.
    But 28 = -9 mod 37: the SEAM-exit node from THEOREM 65.

MOD 37 OF USER SEQUENCES:
  212 → mod37=27∈ORBIT_11;  DR=5
  123 → mod37=12∈ST;        DR=6
  124 → mod37=13∈CB;        DR=7
  134 → mod37=23∈TF_orbit;  DR=8
  1234→ mod37=13∈CB;        DR=1 (literal sum 10)
  234 → mod37=12∈ST;        DR=9
  235 → mod37=13∈CB;        DR=1   (Fibonacci triple 2+3=5)
  246 → mod37=24∈CB∩SEED;  DR=3   (Fibonacci triple 2+4=6; PIPELINE SEED)
  325 → mod37=29∈PM_orbit;  DR=1   (Fibonacci triple 3+2=5)
  347 → mod37=14∈PM_orbit;  DR=5   (Fibonacci triple 3+4=7)
  426 → mod37=19∈PR_orbit;  DR=3   (Fibonacci triple 4+2=6)
  437 → mod37=30∈SA∩ST;    DR=5   (Fibonacci triple 4+3=7)

MOD 37 COINCIDENCES (via SEAM stride 111=3×37):
  124 ≡ 1234 ≡ 235 ≡ 13∈CB   (differences 1110=30×37 and 111=3×37)
  123 ≡ 234  ≡ 12∈ST          (difference 111=3×37)
  Adding 111 (SEAM stride) preserves mod 37 residue.

POWERS OF 10 MOD 37:
  10^1 ≡ 10 = DECADE_ANCHOR ∈ IC
  10^2 ≡ 26 = SCALAR_137 ∈ IC
  10^3 ≡ 1 ∈ IC  (period 3 = ord₃₇(10) = 3)
  All powers of 10 stay in IDENTITY_CYCLE.

PIPELINE SEED CONNECTION:
  246 = Fibonacci triple (2,4,6).  2+4=6.  Sum=12.  DR=3.
  246 mod 37 = 24 ∈ CB ∩ SEED_ORBIT — the pipeline seed maps to CB∩SEED.
  437 mod 37 = 30 ∈ SA∩ST — the (4,3,7) Fibonacci triple lands on sovereign intersection.
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA             = frozenset({4, 9, 25, 30})
ST             = frozenset({3, 12, 21, 30})
CB             = frozenset({8, 13, 24})
ORBIT_11       = frozenset({11, 27, 36})
DARK_A         = frozenset({2, 15, 20})
SEED_ORBIT     = frozenset({18, 24, 32})
IDENTITY_CYCLE = frozenset({1, 10, 26})
OUTLIER_SOV    = frozenset({21, 25, 28})
TESLA_FLOW     = 6
TESLA_FLOW_ORB = frozenset({6, 8, 23})
PRIME_MIRROR   = 31
PM_ORB         = frozenset({14, 29, 31})
PR_5_13_19     = frozenset({5, 13, 19})
SCALAR_137     = 26
DECADE_ANCHOR  = 10
SEAM           = 0
SEAM_STRIDE    = 111   # = 3×37


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


# ── BASE {1,2,3,4} ────────────────────────────────────────────────────────────

BASE = [1, 2, 3, 4]
assert sum(BASE) == 10


# ── REMOVAL MAP ───────────────────────────────────────────────────────────────

# Remove d: sum = 10-d; DR = 10-d (since 10-d ∈ {6,7,8,9} for d=1,2,3,4)
assert dr(10 - 1) == 9
assert dr(10 - 2) == 8
assert dr(10 - 3) == 7
assert dr(10 - 4) == 6

# mod 37 of the 4 three-digit removal sequences
assert 234 % 37 == 12 and 12 in ST       # remove 1
assert 134 % 37 == 23 and 23 in TESLA_FLOW_ORB   # remove 2
assert 124 % 37 == 13 and 13 in CB       # remove 3
assert 123 % 37 == 12 and 12 in ST       # remove 4

# Removing d reduces DR by exactly d (for d=1..4)
for d in [1, 2, 3, 4]:
    removed_sum = 10 - d
    assert dr(removed_sum) == removed_sum   # no further DR collapse needed


# ── FIBONACCI TRIPLE RULE: (a, b, a+b) ───────────────────────────────────────

def fib_triple_dr(a, b):
    return dr(a + b + (a + b))   # = dr(2(a+b))

# Single-digit triples (a+b ≤ 9): DR coverage
covered = set()
for a in range(1, 10):
    for b in range(1, 10):
        if a + b <= 9:
            covered.add(fib_triple_dr(a, b))

assert covered == frozenset({1, 3, 4, 5, 6, 7, 8, 9})   # DR=2 missing

# User's specific Fibonacci triples
assert dr(2+3+5) == 1   # 235
assert dr(2+4+6) == 3   # 246
assert dr(3+2+5) == 1   # 325
assert dr(3+4+7) == 5   # 347
assert dr(4+2+6) == 3   # 426
assert dr(4+3+7) == 5   # 437


# ── THE DR=2 GAP ─────────────────────────────────────────────────────────────

# Minimum a+b for DR=2 with a,b ≥ 1: a+b = 10
assert fib_triple_dr(1, 9) == 2   # (1,9,10): sum=20, DR=2
assert fib_triple_dr(4, 6) == 2   # (4,6,10): sum=20, DR=2

# With 0 (SEAM element): (0,1,1)
assert dr(0 + 1 + 1) == 2   # sum=2, DR=2

# OUTLIER_SOV(28) connection: any triple (a,b,28) with a+b=28 gives DR=2
assert dr(2 * 28) == 2   # DR(56) = 2
assert 28 in OUTLIER_SOV
assert (28 + 9) % 37 == 0   # 28 is the SEAM-exit node


# ── MOD 37 OF USER SEQUENCES ─────────────────────────────────────────────────

assert 212 % 37 == 27 and 27 in ORBIT_11      # DR=5
assert 123 % 37 == 12 and 12 in ST            # DR=6
assert 124 % 37 == 13 and 13 in CB            # DR=7
assert 134 % 37 == 23 and 23 in TESLA_FLOW_ORB  # DR=8
assert 1234 % 37 == 13 and 13 in CB           # sum=10, DR=1
assert 234 % 37 == 12 and 12 in ST            # DR=9
assert 235 % 37 == 13 and 13 in CB            # fib triple, DR=1
assert 246 % 37 == 24 and 24 in CB and 24 in SEED_ORBIT  # fib triple, DR=3
assert 325 % 37 == 29 and 29 in PM_ORB        # fib triple, DR=1
assert 347 % 37 == 14 and 14 in PM_ORB        # fib triple, DR=5
assert 426 % 37 == 19 and 19 in PR_5_13_19    # fib triple, DR=3
assert 437 % 37 == 30 and 30 in SA and 30 in ST  # fib triple, DR=5


# ── MOD 37 COINCIDENCES (SEAM STRIDE 111=3×37) ───────────────────────────────

assert SEAM_STRIDE == 3 * 37

# 111 is SEAM stride: adding 111 preserves mod 37
assert 235 % 37 == 124 % 37 == 13   # differ by 111 = 3×37
assert 234 % 37 == 123 % 37 == 12   # differ by 111 = 3×37
assert 1234 % 37 == 124 % 37 == 13  # differ by 1110 = 30×37

assert 235 - 124 == 111 and 111 % 37 == 0
assert 234 - 123 == 111 and 111 % 37 == 0
assert 1234 - 124 == 1110 and 1110 % 37 == 0


# ── POWERS OF 10 MOD 37 ──────────────────────────────────────────────────────

assert pow(10, 1, 37) == DECADE_ANCHOR and DECADE_ANCHOR in IDENTITY_CYCLE
assert pow(10, 2, 37) == SCALAR_137 and SCALAR_137 in IDENTITY_CYCLE
assert pow(10, 3, 37) == 1 and 1 in IDENTITY_CYCLE
assert pow(10, 3, 37) == 1   # period 3: ord₃₇(10) = 3


# ── PIPELINE SEED ────────────────────────────────────────────────────────────

assert 246 % 37 == 24
assert 24 in CB and 24 in SEED_ORBIT   # CB ∩ SEED_ORBIT ∩ Fibonacci triple


if __name__ == "__main__":
    print("Digit Sequence DR Coverage and the DR=2 Gap — GF(37)")
    print("=" * 60)
    print()
    print("{1,2,3,4} base: sum=10")
    print()
    print("Removal subsets (3-element):")
    for d in [1,2,3,4]:
        seq = int(''.join(str(x) for x in [1,2,3,4] if x!=d))
        print(f"  Remove {d}: sum={10-d}  DR={dr(10-d)}  mod37={seq%37}")
    print()
    print("Fibonacci triple coverage (single-digit a+b ≤ 9):")
    print(f"  DR values covered: {sorted(covered)}")
    print(f"  Missing: [2]")
    print(f"  DR=2 requires a+b≡1 (mod 9): min a+b=10 (two-digit c) or a=0 (SEAM)")
    print()
    print("User sequences mod 37:")
    for seq, kind, note in [
        (212,'','→ORBIT_11'), (123,'','→ST'), (124,'','→CB'), (134,'','→TF_orbit'),
        (1234,'four','→CB (sum=10)'), (234,'','→ST'),
        (235,'fib','→CB'), (246,'fib','→CB∩SEED [PIPELINE SEED]'),
        (325,'fib','→PM_orbit'), (347,'fib','→PM_orbit'),
        (426,'fib','→PR_orbit'), (437,'fib','→SA∩ST'),
    ]:
        print(f"  {seq:5d} {kind:4s}: mod37={seq%37:2d}  DR={dr(sum(int(d) for d in str(seq)))}  {note}")
    print()
    print("Coincidences via SEAM stride 111=3×37:")
    print(f"  124≡235≡1234 ≡ 13∈CB (mod 37)")
    print(f"  123≡234 ≡ 12∈ST (mod 37)")
    print()
    print("Powers of 10 mod 37: 1→10→26→1 (period 3; all in IC)")
    print()
    print(f"OUTLIER_SOV(28): any triple (a,b,28) with a+b=28 gives DR=2")
    print(f"  28 = -9 mod 37 = SEAM-exit node; 2×28=56, DR(56)=2")
    print()
    print("All assertions pass.")
