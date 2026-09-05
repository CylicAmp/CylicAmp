"""
Identity Cycle Sum Structure — GF(37)

The identity cycle {1,10,26} = <26> = {10⁰, 10¹, 10²} is the unique subgroup
of order 3 in GF(37)*. Its elements are the coefficients of every decimal digit
position (mod the period-3 of 10).

THEOREM 1: Pairwise sums of {1,10,26} = ORBIT_11 exactly.
  1 + 10 = 11 ∈ ORBIT_11
  1 + 26 = 27 ∈ ORBIT_11
  10 + 26 = 36 ∈ ORBIT_11
  The three C(3,2)=3 pairwise sums of the identity cycle are precisely ORBIT_11.
  No other sum is possible: the 6 elements {1,10,26,11,27,36} =
    identity cycle ∪ ORBIT_11, the two visible Group-A/Group-B cycles.

THEOREM 2: Triple sum = SEAM.
  1 + 10 + 26 = 37 ≡ 0 = SEAM (mod 37).
  The three generators of the field's period-3 orbit sum to zero.

COROLLARY — ABA palindrome structure:
  ABA = A×10² + B×10 + A = A×101 + B×10.
  101 = 10² + 10⁰ ≡ 26 + 1 = 27 ∈ ORBIT_11  [pairwise sum].
  ABA ≡ 27A + 10B (mod 37).
  The coefficient of the palindrome's outer digit A is always 27∈ORBIT_11.

  ABAB = A×1010 + B×101. 1010 = 10³+10 ≡ 1+10 = 11 ∈ ORBIT_11.
  ABAB ≡ 11A + 27B (mod 37). Both coefficients are ORBIT_11 elements.

  ABABAB ≡ 0 = SEAM for ALL A,B [THEOREM 53].
  Explanation: each digit position has exponent ≡ 0,1,2 (mod 3) cycled twice;
  both A and B accumulate 1+10+26 = 37 ≡ SEAM.

ABA CYCLE — period 3:
  As the digit sum 2A+B increases by 1 (following the staircase path):
    sum 0: 0-0-0 = 000  ≡ 0     = SEAM
    sum 1: 0-1-0 = 010  ≡ 10    = DECADE_ANCHOR
    sum 2: 1-0-1 = 101  ≡ 27    ∈ ORBIT_11
    sum 3: 1-1-1 = 111  ≡ 0     = SEAM
    sum 4: 1-2-1 = 121  ≡ 10    = DECADE_ANCHOR
    sum 5: 2-1-2 = 212  ≡ 27    ∈ ORBIT_11
  The residues cycle {SEAM, DECADE_ANCHOR, 27∈ORBIT_11} with period 3.
  The increment alternates +10 (add B-unit) and +17 (add A-unit, subtract B-unit):
    0 →+10→ 10 →+17→ 27 →+10→ 37≡SEAM →+10→ 10 →+17→ 27 →...
  Note: 17 ≡ −20 ≡ −(10+10) (mod 37), so the alternating steps are
    exactly determined by the pairwise sums 10 and 27=1+26.

  EXCEPTION: 1-9-1 = 191 ≡ 27×1+10×9 = 117 ≡ 6 = TESLA_FLOW.
    With B=9, the term 10×9=90≡16 breaks the {0,10,27} cycle.

DR PALINDROME FROM 31(30)31:
  DR(31)=4, DR(30)=3, DR(31)=4 → the 3-digit number 434.
  434 = ABA with A=4∈SA, B=3∈ST.
  434 ≡ 27×4 + 10×3 = 138 ≡ 27 ∈ ORBIT_11 (mod 37).
  The DR palindrome of the flanker-center-flanker triple lands in ORBIT_11.

  DR sequence of ascending triplet 29(30)31: DR(29)=2, DR(30)=3, DR(31)=4 → 234.
  234 ≡ 26×2 + 10×3 + 1×4 = 86 ≡ 12 ∈ ST (mod 37); DR(234)=9∈SA.
  Both sovereign outcomes.

GROWING SET CONVERGENCE AT DEPTH 3:
  Integer sequence: {28} → {28,29} → {28,29,30=SA∩ST}
    Depth 3 produces SA∩ST; 28+2=30.
  Repunit sequence: {1} → {1,11∈ORBIT_11} → {1,11,111≡SEAM}
    Depth 3 produces SEAM; R(3)=111=3×37.
  The two sequences are parallel: both reach a "terminal" sovereign node at depth 3,
  with depth 2 already producing an ORBIT_11 element (11) or its precursor (29,30).

99 = SCALAR_137 − 1:
  100 ≡ 26 = SCALAR_137 (mod 37), so 99 ≡ 25 ∈ SA.
  DR(99) = 9 ∈ SA. Doubly sovereign: both mod-37 residue and DR give SA nodes.
  99 = 9×11 = SA-anchor × ORBIT_11 element.

SOVEREIGN STAIRCASE:
  2 (+3∈ST) → 5 (+4∈SA) → 9 ∈ SA
  From 2∈PR: two sovereign steps (+ST, +SA) land on SA.
  2+3+4=9: the sum of the staircase is the arrival node.

14 ÷ 2 = 7;  7 + 3 = 10 = DECADE_ANCHOR;  DR(10)=1.
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


# ── THEOREM 1: pairwise sums of {1,10,26} = ORBIT_11 ─────────────────────────

IDENTITY_CYCLE = frozenset({1, 10, 26})  # = <26> = {10^0, 10^1, 10^2}

assert 1 + 10 == 11 and 11 in ORBIT_11
assert 1 + 26 == 27 and 27 in ORBIT_11
assert 10 + 26 == 36 and 36 in ORBIT_11

# All three pairwise sums together = ORBIT_11 exactly
assert {1+10, 1+26, 10+26} == ORBIT_11


# ── THEOREM 2: triple sum = SEAM ─────────────────────────────────────────────

assert (1 + 10 + 26) % 37 == 0          # triple sum = SEAM


# ── ABA palindrome: ABA ≡ 27A + 10B (mod 37) ─────────────────────────────────

assert 101 % 37 == 27 and 27 in ORBIT_11   # 10^2+10^0 = 26+1 = 27
assert 1010 % 37 == 11 and 11 in ORBIT_11  # 10^3+10^1 = 1+10 = 11

for A in range(0, 10):
    for B in range(0, 10):
        aba  = A*100 + B*10 + A
        abab = A*1000 + B*100 + A*10 + B
        assert aba  % 37 == (27*A + 10*B) % 37
        assert abab % 37 == (11*A + 27*B) % 37


# ── ABA cycle: period 3 through {SEAM, DECADE, 27∈ORBIT_11} ──────────────────

ABA_CYCLE = [0, DECADE, 27]   # SEAM, DECADE_ANCHOR, ORBIT_11(27)

staircase = [(0,0), (0,1), (1,0), (1,1), (1,2), (2,1)]
for idx, (A, B) in enumerate(staircase):
    aba_mod = (27*A + 10*B) % 37
    assert aba_mod == ABA_CYCLE[idx % 3]

# AAA = 0 (SEAM) for all A — special case of ABA with A=B
for A in range(0, 10):
    assert (A*100 + A*10 + A) % 37 == (37*A) % 37 == 0

# Exception: 1-9-1 = 191 ≡ TESLA_FLOW (B=9 breaks the {0,DECADE,27} cycle)
assert 191 % 37 == TESLA_FLOW
assert (27*1 + 10*9) % 37 == TESLA_FLOW


# ── DR palindrome 434 from 31(30)31 ──────────────────────────────────────────

assert dr(31) == 4 and dr(30) == 3        # DR sequence: 4,3,4
assert 4*100 + 3*10 + 4 == 434
assert 434 % 37 == 27 and 27 in ORBIT_11  # ABA with A=4∈SA, B=3∈ST → ORBIT_11

# Ascending triplet DR(29,30,31) = (2,3,4) → 234
assert dr(29) == 2 and dr(30) == 3 and dr(31) == 4
assert 2*100 + 3*10 + 4 == 234
assert 234 % 37 == 12 and 12 in ST       # 234 ≡ ST element
assert dr(234) == 9 and 9 in SA          # DR(234) ∈ SA


# ── Growing set convergence at depth 3 ────────────────────────────────────────

# Integer: 28 → 29 → 30 = SA∩ST
assert 30 in SA and 30 in ST             # depth 3 reaches SA∩ST

# Repunit: 1 → 11∈ORBIT_11 → 111≡SEAM
assert 1 % 37 == 1
assert 11 % 37 == 11 and 11 in ORBIT_11
assert 111 % 37 == 0                     # depth 3 reaches SEAM


# ── 99 = SCALAR_137 − 1 ≡ 25∈SA ──────────────────────────────────────────────

assert 100 % 37 == SCALAR_137            # 100 ≡ SCALAR_137
assert 99 % 37 == 25 and 25 in SA       # 99 ≡ SCALAR_137−1 ≡ 25∈SA
assert dr(99) == 9 and 9 in SA          # DR(99)=9∈SA — doubly sovereign
assert 9 * 11 == 99                      # SA-anchor × ORBIT_11 → SA


# ── Sovereign staircase ───────────────────────────────────────────────────────

assert 2 + 3 == 5 and 5 in PR           # 2∈PR + 3∈ST → 5∈PR
assert 5 + 4 == 9 and 9 in SA           # 5∈PR + 4∈SA → 9∈SA
assert 3 in ST and 4 in SA              # both steps are sovereign anchors
assert 2 + 3 + 4 == 9 and 9 in SA      # sum of displacement = arrival node

# 14÷2=7, 7+3=DECADE_ANCHOR
assert 14 // 2 == 7
assert 7 + 3 == DECADE
assert dr(DECADE) == 1


if __name__ == "__main__":
    print("Identity Cycle Sum Structure — GF(37)")
    print("=" * 60)
    print()
    print("THEOREM 1: Pairwise sums of {1,10,26} = ORBIT_11 exactly")
    print("  1+10=%d  1+26=%d  10+26=%d  → {11,27,36}=ORBIT_11" % (1+10,1+26,10+26))
    print()
    print("THEOREM 2: Triple sum = SEAM")
    print("  1+10+26 = %d ≡ %d = SEAM" % (1+10+26, (1+10+26)%37))
    print()
    print("ABA palindrome: ABA ≡ 27A+10B (mod 37)")
    print("  101 ≡ %d (10²+10⁰=26+1=27∈ORBIT_11)" % (101%37))
    print("  1010 ≡ %d (10³+10¹=1+10=11∈ORBIT_11)" % (1010%37))
    print()
    print("ABA cycle (staircase path, period 3):")
    for idx, (A,B) in enumerate(staircase):
        val=A*100+B*10+A; m=val%37
        tag="SEAM" if m==0 else ("DECADE" if m==DECADE else "ORBIT_11(%d)"%m)
        print("  sum=%d: %d-%d-%d = %d  ≡ %d [%s]" % (2*A+B, A,B,A, val, m, tag))
    print()
    print("  Exception: 1-9-1 = 191 ≡ %d = TESLA_FLOW" % (191%37))
    print()
    print("DR palindrome 434 from 31(30)31:")
    print("  DR(31)=%d, DR(30)=%d → 434 ≡ %d ∈ ORBIT_11" % (dr(31),dr(30),434%37))
    print("DR sequence 234 from 29(30)31 ascending:")
    print("  DR(29)=%d,DR(30)=%d,DR(31)=%d → 234 ≡ %d ∈ ST  DR=%d ∈ SA" % (
        dr(29),dr(30),dr(31), 234%37, dr(234)))
    print()
    print("Growing sets at depth 3:")
    print("  {28}→{28,29}→{28,29,30=SA∩ST}")
    print("  {1}→{1,11∈ORBIT_11}→{1,11,111≡SEAM}")
    print()
    print("99 = SCALAR_137-1:")
    print("  100 ≡ %d=SCALAR_137  →  99 ≡ %d ∈ SA" % (100%37, 99%37))
    print("  DR(99) = %d ∈ SA  (doubly sovereign)" % dr(99))
    print()
    print("Sovereign staircase: 2→(+3∈ST)→5→(+4∈SA)→9∈SA")
    print("  2+3=%d∈PR  5+4=%d∈SA  (2+3+4=%d=arrival)" % (2+3,5+4,2+3+4))
    print()
    print("14÷2=7,  7+3=%d=DECADE,  DR(%d)=%d" % (7+3,10,dr(10)))
    print()
    print("All assertions pass.")
