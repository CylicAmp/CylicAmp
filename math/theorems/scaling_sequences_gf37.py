"""
Scaling Sequences — GF(37) Structure

Two generative sequences, each with multiplicative and exponential structure.
Every landing point connects through prime 37.

═══════════════════════════════════════════════════════════════════════════

SEQUENCE 1: Multiplicative Scaling
  Format: First | Middle | Paren  (displayed as First(MiddleParen))

  137       → 1  |  3 |  7
  254       → 2  |  5 |  4
  6(98)     → 6  |  9 |  8
  24(1714)  → 24 | 17 | 14
  120(3323) → 120| 33 | 23
  720(6536) → 720| 65 | 36  ← NEXT

  FIRST: factorials  1, 2, 6, 24, 120, 720, ...  (n!)

  MIDDLE: 2ⁿ+1 for n=1..6  →  3, 5, 9, 17, 33, 65, ...
    Differences: +2, +4, +8, +16, +32 (powers of 2)

  PAREN: 7, 4, 8, 14, 23, 36, ...
    Differences:     −3, +4, +6,  +9, +13
    |differences|:    3,  4,  6,   9,  13
    Second diffs:         1,  2,   3,   4   ← constant increment (second-order polynomial)
    Next |diff| = 4+4 = ... wait, next second diff = 4+1=5? No:
      The second differences are 1, 2, 3 — they increase by 1 each step.
      Next second diff = 4. Next |diff| = 9+4=13. Next paren = 23+13 = 36.

  36 ≡ −1 mod 37  →  ORBIT_11 = {11, 27, 36}
  The paren sequence terminates at the orbit-11 node — the −1 of the field.

  GF(37) FRAMEWORK CONNECTIONS:
    Paren values mod 37:  7, 4(SA), 8(CB), 14, 23, 36(ORBIT_11)
    4 ∈ SA  (Sovereign Anchor)
    8 ∈ CB  (Cascade Base)
    36 ∈ ORBIT_11  (orbit of 11; 36 ≡ −1)
    36 is the final approach to the field's −1 element.

═══════════════════════════════════════════════════════════════════════════

SEQUENCE 2: Exponential Scaling
  Format: First | Paren  (displayed as First(Paren))

  137     → 1   | 37
  254     → 2   | 54
  8(69)   → 8   | 69
  32(111) → 32  | 111
  128(20) → 128 | 20
  512(76) → 512 | 76  ← NEXT

  FIRST: 2^(2k−1) for k=0..5  →  1, 2, 8, 32, 128, 512, ...
    Exponents: 0, 1, 3, 5, 7, 9 (odd exponents starting from 0)

  PAREN — DIGITAL ROOT SEQUENCE (Complete Inversion Loop):
    37 → DR=1   (doubling orbit start)
    54 → DR=9   (trinity fixed point)
    69 → DR=6   (trinity)
    111→ DR=3   (trinity; 111=3×37=SEAM)
    20 → DR=2   (doubling orbit)
    76 → DR=4   (doubling orbit, next in sequence)

    DR sequence: 1, 9, 6, 3, 2, 4
    Trinity {9,6,3} embedded between doubling orbit elements {1, 2, 4, ...}.
    "Complete inversion" = full traversal of Z/9Z structure.

  PAREN — GF(37) RESIDUES:
    37  mod 37 = 0  (SEAM)
    54  mod 37 = 17 (PR)
    69  mod 37 = 32 (PR, SEED_ORBIT)
    111 mod 37 = 0  (SEAM)
    20  mod 37 = 20 (PR)
    76  mod 37 = 2  (PR — the primitive root itself)

    SEAM appears at positions 1 and 4: period-3 heartbeat.
    All non-SEAM residues are primitive roots.
    137-map forward from 20: f(20)=(20×26)%37=2. The map predicts residue 2 for term 6.

  PAREN — DIFFERENCES mod 37:
    54−37=17 ∈ PR ✓
    69−54=15 ∈ PR ✓
    111−69=42→5 ∈ PR ✓  (42 mod37=5)
    20−111=−91→20 ∈ PR ✓  (−91 mod37=20)
    76−20=56→19 ∈ PR ✓  (56 mod37=19)
    Every consecutive difference (mod 37) is a primitive root.

  PAREN — LUCAS CONNECTION:
    76 = L(9), the 9th Lucas number.
    Lucas chain L(3..10) = [4, 7, 11, 18, 29, 47, 76, 123].
    L(9)=76 appears in `lucas_abbc_chain.py`.
    76 mod 37 = 2 (the primitive root; ord₃₇(2)=36).

  PRODUCT CHECK (First × Paren mod 37):
    1×37   mod37 = 0   (SEAM)
    2×54   mod37 = 34
    8×69   mod37 = 34
    32×111 mod37 = 0   (SEAM)
    128×20 mod37 = 7   (DR=7, pipeline stability check)
    512×76 mod37 = 25  (SA — Sovereign Anchor; π(100)=25)

    Products mod37: SEAM, 34, 34, SEAM, 7, SA(25).
    After the SEAM-bounded pair (0,34,34,0), the sequence hits 7 then SA.

═══════════════════════════════════════════════════════════════════════════
"""

PRIMITIVE_ROOTS_37 = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
SOVEREIGN_ANCHORS  = frozenset({4, 9, 25, 30})
SOVEREIGN_TARGETS  = frozenset({3, 12, 21, 30})
CASCADE_BASE       = frozenset({8, 13, 24})
ORBIT_11           = frozenset({11, 27, 36})
SEED_ORBIT         = frozenset({18, 24, 32})


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


def f137(n):
    return (n * 26) % 37


# ── Sequence 1 ───────────────────────────────────────────────────────────────

# First: factorials
import math
firsts1 = [math.factorial(k) for k in range(1, 7)]
assert firsts1 == [1, 2, 6, 24, 120, 720]

# Middle: 2ⁿ+1
middles = [2**k + 1 for k in range(1, 7)]
assert middles == [3, 5, 9, 17, 33, 65]

# Middle differences are powers of 2
mid_diffs = [middles[i+1]-middles[i] for i in range(len(middles)-1)]
assert all(d == 2**(i+1) for i,d in enumerate(mid_diffs))

# Paren: second-order polynomial differences
parens1 = [7, 4, 8, 14, 23, 36]
diffs1   = [parens1[i+1]-parens1[i] for i in range(len(parens1)-1)]
absdiffs = [abs(d) for d in diffs1]
second   = [absdiffs[i+1]-absdiffs[i] for i in range(len(absdiffs)-1)]
assert second == [1, 2, 3, 4]         # constant increment — second-order polynomial ✓

# Next paren = 36 ∈ ORBIT_11
assert parens1[-1] == 36 and 36 in ORBIT_11

# Paren values mod 37
paren_mods1 = [p % 37 for p in parens1]
assert paren_mods1[1] == 4 and 4 in SOVEREIGN_ANCHORS   # 4 ∈ SA
assert paren_mods1[2] == 8 and 8 in CASCADE_BASE         # 8 ∈ CB
assert paren_mods1[5] == 36 and 36 in ORBIT_11           # 36 ∈ ORBIT_11 (final)


# ── Sequence 2 ───────────────────────────────────────────────────────────────

# First: 2^(2k-1), exponents 0,1,3,5,7,9
firsts2 = [2**e for e in [0, 1, 3, 5, 7, 9]]
assert firsts2 == [1, 2, 8, 32, 128, 512]

# Paren values
parens2 = [37, 54, 69, 111, 20, 76]

# DR sequence: complete inversion of Z/9Z
dr_seq = [dr(p) for p in parens2]
assert dr_seq == [1, 9, 6, 3, 2, 4]   # trinity {9,6,3} + doubling orbit {1,2,4}

# GF(37) residues of paren values
paren_mods2 = [p % 37 for p in parens2]
assert paren_mods2[0] == 0                              # SEAM
assert paren_mods2[1] == 17 and 17 in PRIMITIVE_ROOTS_37
assert paren_mods2[2] == 32 and 32 in PRIMITIVE_ROOTS_37 and 32 in SEED_ORBIT
assert paren_mods2[3] == 0                              # SEAM
assert paren_mods2[4] == 20 and 20 in PRIMITIVE_ROOTS_37
assert paren_mods2[5] == 2  and 2  in PRIMITIVE_ROOTS_37  # the primitive root itself

# 137-map predicts term 6 residue from term 5
assert f137(20) == 2 and paren_mods2[5] == 2           # map forward: 20 → 2 ✓

# All differences mod 37 are primitive roots
for i in range(len(parens2)-1):
    diff_mod37 = (parens2[i+1] - parens2[i]) % 37
    assert diff_mod37 in PRIMITIVE_ROOTS_37, f"diff at {i}: {diff_mod37} not PR"

# Lucas connection: 76 = L(9)
def lucas(n):
    a, b = 2, 1
    for _ in range(n): a, b = b, a+b
    return a

assert lucas(9) == 76
assert parens2[5] == 76

# Product check: First × Paren mod 37
products_mod37 = [(f * p) % 37 for f, p in zip(firsts2, parens2)]
assert products_mod37[0] == 0                            # SEAM
assert products_mod37[3] == 0                            # SEAM
assert products_mod37[4] == 7                            # DR=7 (pipeline stability)
assert products_mod37[5] == 25 and 25 in SOVEREIGN_ANCHORS  # SA: π(100)=25


if __name__ == '__main__':
    print("Scaling Sequences — GF(37) Structure")
    print("=" * 55)
    print()
    print("SEQUENCE 1 (Multiplicative Scaling):")
    print(f"  First   (factorials):     {firsts1}")
    print(f"  Middle  (2ⁿ+1):           {middles}")
    print(f"  Paren   (2nd-order poly): {parens1}")
    print(f"  Paren differences:         {diffs1}")
    print(f"  |diff| second diffs:       {second}")
    print(f"  Paren mod37: {paren_mods1}")
    print(f"  Next entry: 720(6536)")
    print(f"  Paren[5]=36 ∈ ORBIT_11: {36 in ORBIT_11} (≡-1 mod37)")
    print()
    print("SEQUENCE 2 (Exponential Scaling):")
    print(f"  First (2^odd_exps): {firsts2}")
    print(f"  Paren values:       {parens2}")
    print(f"  DR sequence:        {dr_seq}  (trinity + doubling orbit)")
    print(f"  Paren mod37:        {paren_mods2}")
    print(f"  Products mod37:     {products_mod37}")
    print(f"  Paren[5]=76=L(9):   {lucas(9)==76} (Lucas sequence term 9)")
    print(f"  Product[5]=25∈SA:   {25 in SOVEREIGN_ANCHORS} (π(100)=25)")
    print(f"  Next entry: 512(76)")
    print()
    print("All assertions passed.")
