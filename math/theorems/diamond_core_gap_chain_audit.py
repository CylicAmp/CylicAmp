#!/usr/bin/env python3
"""
diamond_core_gap_chain_audit.py

Diamond Core [8,3,7; 2,6,1; 5,9,4] gap-chain analysis.

READ ORDER (1-indexed): chain[1..9] = [8, 3, 7, 2, 6, 1, 5, 9, 4]
GAPS (1-indexed):        gap[1..8]  = [5, 4, 5, 4, 5, 4, 4, 5]

FINDINGS:
  - Only gaps 4 and 5 appear; four of each
  - 4×5 + 4×4 = 20 + 16 = 36 = φ(37)
  - Expected alternation [5,4,5,4,5,4,5,4] vs actual [5,4,5,4,5,4,4,5]:
    swap at gap positions 7-8 around pivot chain[8]=9 (≡ 0 mod 9)
  - 5* [chain[7]=5]: flanked (4,4) — compression node; net −1 vs alternation
  - 4* [chain[9]=4]: preceded by gap(5) — extension terminus; net +1 vs alternation
  - Swap preserves total: compression −1, extension +1, net 0

  8 + 9 = 17; digits of 17 are {1, 7} = {chain[6], chain[3]}

  3261⅞ = 26095/8:
    3261  ≡ 5  (mod 37)  = chain[7] = 5*  [compression node]
    26095 ≡ 10 (mod 37)  = chain[6]+chain[8] = 1+9
    DR(26095) = 4        = chain[9] = 4*  [terminal]
    Fractional numerator 7  = chain[3]
    Denominator 8           = chain[1]
    Factorization 26095 = 5 × 17 × 307:
      5        = chain[7]              (5* compression node)
      17       = chain[1] + chain[8]  (8+9, the observed sum)
      DR(307)  = 1 = chain[6]         (digit 1 of 17 = digit 1 of 8+9)
"""

errors = []

def check(label, cond):
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {label}")
    if not cond:
        errors.append(label)

def digital_root(n):
    if n == 0:
        return 0
    return 1 + (abs(int(n)) - 1) % 9

# ── DIAMOND CORE ─────────────────────────────────────────────────────────────

core = [
    [8, 3, 7],
    [2, 6, 1],
    [5, 9, 4],
]
# Row-by-row read order. 1-indexed: chain[1]=8, chain[9]=4
chain = [8, 3, 7, 2, 6, 1, 5, 9, 4]

print("=== DIAMOND CORE [8,3,7; 2,6,1; 5,9,4] ===")
for i, row in enumerate(core, 1):
    print(f"  Row {i}: {row}  sum={sum(row)}")
print(f"  Chain (row order): {chain}")
print()

# ── GAP CHAIN ────────────────────────────────────────────────────────────────

print("=== GAP CHAIN ===")
gaps = [abs(chain[i+1] - chain[i]) for i in range(8)]
print(f"  Gaps: {gaps}")
print()

check("gaps = [5,4,5,4,5,4,4,5]",      gaps == [5,4,5,4,5,4,4,5])
check("only values 4 and 5 appear",     set(gaps) == {4, 5})

fours = gaps.count(4)
fives = gaps.count(5)
check("four gaps of value 4",           fours == 4)
check("four gaps of value 5",           fives == 4)
check("4 × 5 = 20",                     fives * 5 == 20)
check("4 × 4 = 16",                     fours * 4 == 16)
check("4×5 + 4×4 = 36 = φ(37)",        fives*5 + fours*4 == 36)
check("sum(gaps) = 36",                  sum(gaps) == 36)
print()

# ── ALTERNATION ANOMALY ──────────────────────────────────────────────────────

print("=== ALTERNATION ANOMALY ===")
alt_exp = [5,4,5,4,5,4,5,4]
alt_act = [5,4,5,4,5,4,4,5]

check("expected alternation [5,4,5,4,5,4,5,4] sums to 36", sum(alt_exp) == 36)
check("actual sequence      [5,4,5,4,5,4,4,5] sums to 36", sum(alt_act) == 36)
check("totals equal — global invariant preserved",           sum(alt_exp) == sum(alt_act))

# Gap 7 and gap 8 (0-indexed: positions 6 and 7)
check("gap[7] anomaly: expected 5, actual 4  [compression]",
      alt_exp[6] == 5 and alt_act[6] == 4)
check("gap[8] anomaly: expected 4, actual 5  [extension]",
      alt_exp[7] == 4 and alt_act[7] == 5)

pivot = chain[7]   # chain[8] in 1-indexed = 9
check("pivot chain[8] = 9",             pivot == 9)
check("9 ≡ 0 (mod 9)  [absorptive in Z₉]", 9 % 9 == 0)
print("  Swap gaps 7-8 around pivot 9: compression(−1) + extension(+1) = 0")
print()

# ── COMPRESSION NODE 5* ──────────────────────────────────────────────────────

print("=== COMPRESSION NODE 5* [chain[7]=5] ===")
node_5 = chain[6]           # 0-indexed 6 = 1-indexed 7
check("chain[7] = 5  (5*)",             node_5 == 5)
left_gap  = gaps[5]         # |chain[6] − chain[7]| = |1 − 5|
right_gap = gaps[6]         # |chain[7] − chain[8]| = |5 − 9|
check("|chain[6]−chain[7]| = |1−5| = 4  (left gap of 5*)",  left_gap  == 4)
check("|chain[7]−chain[8]| = |5−9| = 4  (right gap of 5*)", right_gap == 4)
check("5* flanked by (4,4) — double compression",
      left_gap == 4 and right_gap == 4)
print()

# ── EXTENSION TERMINUS 4* ────────────────────────────────────────────────────

print("=== EXTENSION TERMINUS 4* [chain[9]=4] ===")
node_4  = chain[8]          # 0-indexed 8 = 1-indexed 9
pre_gap = gaps[7]           # |chain[8] − chain[9]| = |9 − 4|
check("chain[9] = 4  (4*)",             node_4 == 4)
check("|chain[8]−chain[9]| = |9−4| = 5  (extension gap)", pre_gap == 5)
check("4* is terminal (no following gap)", len(gaps) == len(chain) - 1)
print()

# ── 8 + 9 = 17 ──────────────────────────────────────────────────────────────

print("=== 8 + 9 = 17 ===")
c1, c8 = chain[0], chain[7]
check("chain[1] = 8",                   c1 == 8)
check("chain[8] = 9",                   c8 == 9)
check("chain[1] + chain[8] = 17",       c1 + c8 == 17)
check("17 is prime",                    all(17 % d != 0 for d in range(2, 17)))
check("digit 1 of 17 = chain[6] = 1",  chain[5] == 1)
check("digit 7 of 17 = chain[3] = 7",  chain[2] == 7)
check("{1,7} ⊂ chain",                  {1, 7}.issubset(set(chain)))
print()

# ── 3261⅞ = 26095/8 ─────────────────────────────────────────────────────────

print("=== 3261⅞ = 26095/8 ===")
W, fn, fd = 3261, 7, 8
N = W * fd + fn
check("3261×8 + 7 = 26095",            N == 26095)
check("26095/8 = 3261.875",            N / fd == 3261.875)
check("denominator 8 = chain[1]",      fd == chain[0])
check("fractional numerator 7 = chain[3]", fn == chain[2])
print()

# Integer part mod 37
check("3261 ≡ 5 (mod 37)  [= chain[7] = 5*]", W % 37 == 5)
check("chain[7] = 5  [5* compression node]",   chain[6] == 5)
print()

# Full numerator mod 37
check("26095 ≡ 10 (mod 37)",                   N % 37 == 10)
check("chain[6]+chain[8] = 1+9 = 10",          chain[5] + chain[7] == 10)
check("26095 ≡ chain[6]+chain[8] (mod 37)",    N % 37 == chain[5] + chain[7])
print()

# DR of full numerator
check("DR(26095) = 4  [= chain[9] = 4*]",      digital_root(N) == 4)
check("chain[9] = 4  [4* extension terminus]",  chain[8] == 4)
print()

# Prime factorization
check("26095 = 5 × 17 × 307",                  5 * 17 * 307 == 26095)
check("factor 5 = chain[7]  (5*)",             chain[6] == 5)
check("factor 17 = chain[1]+chain[8]  (8+9)",  chain[0] + chain[7] == 17)
check("DR(307) = 1 = chain[6]",                digital_root(307) == 1 and chain[5] == 1)
print("  DR(307)=1=chain[6] — third prime factor maps via DR to digit-1-of-17")
print()

# Whole-part factorization
check("3261 = 3 × 1087",                       3 * 1087 == 3261)
check("DR(3261) = 3 = chain[2]",               digital_root(3261) == 3 and chain[1] == 3)
check("DR(1087) = 7 = chain[3]",               digital_root(1087) == 7 and chain[2] == 7)
print("  3261 = chain[2] × (prime with DR=chain[3])")
print()

# ── CLOSURE: (8+9)×9 ≡ 5* (mod 37) ─────────────────────────────────────────

print("=== CLOSURE: (chain[1]+chain[8]) × chain[8] ≡ 5* (mod 37) ===")
check("17 × 9 = 153",                          17 * 9 == 153)
check("153 ≡ 5 (mod 37)  [= 5*]",             153 % 37 == 5)
check("DR(17 × 37) = 8 = chain[1]",           digital_root(17 * 37) == 8)
print("  (8+9) × 9 mod 37 = 5* — the sum×pivot collapses to the compression node")
print()

# ── ROW / COLUMN / DIAGONAL SUMS ────────────────────────────────────────────

print("=== DIAMOND CORE SUMS ===")
row_sums = [sum(r) for r in core]
col_sums = [sum(core[r][c] for r in range(3)) for c in range(3)]
diag_tl  = core[0][0] + core[1][1] + core[2][2]   # 8+6+4
diag_tr  = core[0][2] + core[1][1] + core[2][0]   # 7+6+5
col2_num = core[0][1]*100 + core[1][1]*10 + core[2][1]  # 369

check("row 1: 8+3+7 = 18",             row_sums[0] == 18)
check("row 2: 2+6+1 = 9  [middle]",    row_sums[1] == 9)
check("row 3: 5+9+4 = 18",             row_sums[2] == 18)
check("outer rows = 2×middle  [18=2×9]", row_sums[0] == 2*row_sums[1])
check("col 1: 8+2+5 = 15",             col_sums[0] == 15)
check("col 2: 3+6+9 = 18",             col_sums[1] == 18)
check("col 3: 7+1+4 = 12",             col_sums[2] == 12)
check("col 2 read as 369 ≡ −1 (mod 37)", col2_num == 369 and 369 % 37 == 36)
check("diagonal TL→BR: 8+6+4 = 18",   diag_tl == 18)
check("diagonal TR→BL: 7+6+5 = 18",   diag_tr == 18)
check("both main diagonals = 18",      diag_tl == diag_tr == 18)
check("grand sum = 45 = 1+2+...+9",    sum(chain) == 45)
print()

# ── SUMMARY ──────────────────────────────────────────────────────────────────

print("=== SUMMARY ===")
print("  Chain [8,3,7,2,6,1,5,9,4]: gaps [5,4,5,4,5,4,4,5]")
print("  4×5 + 4×4 = 20+16 = 36 = φ(37)")
print("  Anomaly: swap at gap positions 7-8 around pivot 9 ≡ 0 (mod 9)")
print("  5* [chain[7]]: flanked (4,4) — compression −1")
print("  4* [chain[9]]: preceded by 5  — extension +1   net = 0")
print()
print("  8+9=17;  digits {1,7} = {chain[6], chain[3]}")
print()
print("  3261  ≡ 5  (mod 37) = 5*  [compression node]")
print("  26095 ≡ 10 (mod 37) = 1+9 [chain[6]+chain[8]]")
print("  DR(26095) = 4 = 4*  [extension terminus]")
print("  26095 = 5 × 17 × 307:")
print("    5      = chain[7]")
print("    17     = chain[1]+chain[8]")
print("    DR(307)= 1 = chain[6]")
print()

if errors:
    print(f"FAILURES: {errors}")
else:
    print("All verified claims pass.")
