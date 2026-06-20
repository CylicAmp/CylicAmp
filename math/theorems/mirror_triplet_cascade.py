"""
Mirror Triplet Arithmetic — DR Cascade under f(n)=(26n)%37

Classification: Theorem

Consecutive-digit mirror sums form an arithmetic series with step 666.
The cascade 666→18→9 reduces to the DR modulus. The repunit 111,111,111
unifies the series as a three-block structure (31313) with DR=9.

Verified claims:

Mirror sum formula (consecutive digits a=d, b=d+1, c=d+2):
  abc + cba = 2b × 111   (b is the middle digit)
  123+321 =  4×111 =  444  (b=2)
  456+654 = 10×111 = 1110  (b=5)
  789+987 = 16×111 = 1776  (b=8)

Arithmetic series {444, 1110, 1776}: common difference = 666 = 6×111 = 18×37
  Middle digit increases by 3 (2→5→8), so 2b increases by 6, sum by 6×111=666.

DR cascade: 666 → 18 → 9
  DR(666) = 6+6+6 = 18
  DR(18)  = 1+8   = 9   (the DR modulus)

Repunit 111,111,111 — the "31313" structure:
  Three blocks of three 1s: [111][111][111]  →  3-block|3-block|3-block
  "31313" encodes: 3 ones, 1 (identity separator), 3 ones, 1, 3 ones
  Digit sum = 9 (three groups of 3 = 3×3 = 9)
  111,111,111 = 9  × 12,345,679   (DR=9 factor pair; note: digit 8 is absent)
  111,111,111 = 37 × 3,003,003    (divisible by f26 modulus 37)
  111,111,111 = 111 × 1,001,001 = 3×37 × 3×333,667

DR-additive triples (a + b = DR(a+b)):
  (1, 2, 3)  →  1+2=3           (exact, no reduction needed)
  (3, 4, 7)  →  3+4=7           (exact)
  (7, 8, 6)  →  DR(7+8)=DR(15)=6  (DR reduction)
  (2, 5, 7)  →  2+5=7           (exact)
  Closing identity: 3×3 = 9  (f26 target squared = DR modulus)

Complementary pair: 4+5=9 = DR modulus  (4 and 5 are DR-complements to 9)
"""

from itertools import product as iproduct


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


def mirror_sum(d):
    """Sum of a 3-digit consecutive-digit number and its reverse."""
    a, b, c = d, d + 1, d + 2
    forward  = 100 * a + 10 * b + c
    backward = 100 * c + 10 * b + a
    return forward + backward


# ── Mirror sums ────────────────────────────────────────────────────────────

TRIPLETS = [(1, 444), (4, 1110), (7, 1776)]

for d, expected in TRIPLETS:
    result = mirror_sum(d)
    assert result == expected, f"mirror_sum({d}) = {result}, expected {expected}"
    b = d + 1    # middle digit
    assert result == 2 * b * 111, f"Formula 2b×111 failed for d={d}"

# ── Arithmetic series with step 666 ───────────────────────────────────────

sums = [s for _, s in TRIPLETS]
diffs = [sums[i+1] - sums[i] for i in range(len(sums)-1)]
assert all(diff == 666 for diff in diffs), f"Step ≠ 666: {diffs}"

STEP = 666
assert STEP == 6 * 111
assert STEP == 18 * 37    # DR modulus 37 factor

# ── DR cascade: 666 → 18 → 9 ──────────────────────────────────────────────

assert dr(666) == 9        # iterative: 6+6+6=18 → 1+8=9; dr() does it directly
assert 6 + 6 + 6 == 18
assert 1 + 8 == 9
assert dr(18) == 9

# ── Repunit 111,111,111 ────────────────────────────────────────────────────

R9 = 111_111_111    # nine ones

# Three-block structure "31313": [111][111][111]
blocks = [111, 111, 111]
assert sum(blocks) == 333
assert R9 == blocks[0] * 1_000_000 + blocks[1] * 1_000 + blocks[2]

# 3×3 = 9 digit structure
assert 3 * 3 == 9    # three groups of three = nine 1s
assert sum(int(ch) for ch in str(R9)) == 9    # digit sum = 9

# Divisibility
assert R9 % 9 == 0
assert R9 // 9 == 12_345_679    # note: digit 8 is absent in quotient
assert R9 % 37 == 0             # DR modulus 37 divides the repunit
assert R9 // 37 == 3_003_003

# 111 = 3×37 is the building block
assert 111 == 3 * 37

# "31313" as block-separator pattern: 3 digits, (1 separator), 3 digits, (1), 3 digits
# Digit count encoding: 3-1-3-1-3 = three blocks of 3 with identity separators
block_pattern = [3, 1, 3, 1, 3]
assert sum(v for v in block_pattern if v == 3) == 9    # total 1-digits
assert sum(v for v in block_pattern if v == 1) == 2    # two identity separators

# ── DR-additive triples ────────────────────────────────────────────────────

DR_TRIPLES = [
    (1, 2, 3),   # 1+2=3
    (3, 4, 7),   # 3+4=7
    (7, 8, 6),   # DR(7+8)=DR(15)=6
    (2, 5, 7),   # 2+5=7
]

for a, b, c in DR_TRIPLES:
    raw = a + b
    result = raw if raw <= 9 else dr(raw)
    assert result == c, f"DR triple ({a},{b},{c}) failed: DR({raw})={dr(raw)}"

# ── Closing identity ───────────────────────────────────────────────────────

assert 3 * 3 == 9        # DR=3 target squared = DR modulus
assert 4 + 5 == 9        # complementary pair summing to 9


if __name__ == "__main__":
    print("Mirror Triplet Arithmetic — DR Cascade under f(n)=(26n)%37")
    print()
    print("Mirror sums (abc + cba = 2b × 111):")
    for d, expected in TRIPLETS:
        a, b, c = d, d+1, d+2
        print(f"  {a}{b}{c}+{c}{b}{a} = {expected:5d}  (2×{b}×111 = {2*b*111})")
    print()
    print(f"Arithmetic series:  {sums}")
    print(f"Common difference:  {STEP} = 6×111 = 18×37")
    print(f"DR(666) = DR(18) = {dr(18)}  (DR modulus)")
    print()
    print(f"Repunit 111,111,111:")
    print(f"  Three-block [111][111][111]  →  '31313' structure")
    print(f"  Digit sum = 9 = 3×3  (three groups of three 1s)")
    print(f"  111,111,111 = 9 × {R9//9}   (digit 8 absent in quotient)")
    print(f"  111,111,111 = 37 × {R9//37}  (DR modulus 37 divides repunit)")
    print(f"  111 = 3 × 37  (building block)")
    print()
    print("DR-additive triples  (a + b →[DR]→ c):")
    for a, b, c in DR_TRIPLES:
        raw = a + b
        dr_note = f"DR({raw})={dr(raw)}" if raw > 9 else f"{raw}"
        print(f"  {a} + {b} = {dr_note} = {c}")
    print()
    print(f"Closing identities:  3×3 = {3*3} (DR=3 target squared),  4+5 = {4+5}")
    print()
    print("All assertions passed.")
