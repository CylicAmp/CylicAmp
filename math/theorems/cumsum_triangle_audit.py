"""
cumsum_triangle_audit.py

Audits the cumulative-sum triangle derived from L0 = [1,2,3,2,1]:

  L0   1   2   3   2   1     sum  9 = 3²
  L1   1   3   6   8   9     sum 27 = 3³ = 999/37
  L2   1   4  10  18  27     sum 60

Each level is the prefix-sum (running-total) of the level below.

Analyses:
  1.  Verify L0, L1, L2 as stated
  2.  Sum sequence 9, 27, 60, … — power-of-3 stops at L1
  3.  27 = 999/37  (37-family connection; 333 = 9×37)
  4.  Triangular numbers in L1: positions 0-2 = T₁,T₂,T₃
  5.  L2 first differences = L1[1:] = [3,6,8,9]
  6.  DR(L2[1:]) = [4,1,9,9], sum=23, DR=5
  7.  Closed-form sum: s(n) = C(n+4,4)+2C(n+3,3)+3C(n+2,2)+2(n+1)+1
  8.  L0 palindrome — fits exactly after folding in half
  9.  L0 = conv([1,1,1],[1,1,1]) — square of 3-step indicator
  10. Extended levels L0..L7, DR of sums
"""

import math
from itertools import accumulate

def dr(n):
    if n == 0: return 0
    r = n % 9
    return r if r != 0 else 9

def prefix_sum(seq):
    return list(accumulate(seq))

def comb(n, k):
    if k < 0 or k > n: return 0
    return math.comb(n, k)

def convolve(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            result[i + j] += ai * bj
    return result


# ============================================================
# 1. Build the triangle
# ============================================================
print("=" * 62)
print("1.  Cumulative-Sum Triangle")
print("=" * 62)

L0 = [1, 2, 3, 2, 1]
L1 = prefix_sum(L0)
L2 = prefix_sum(L1)
L3 = prefix_sum(L2)
L4 = prefix_sum(L3)

levels_4 = [L0, L1, L2, L3, L4]

print(f"\n  {'Level':>6}  {'values':>30}  {'sum':>6}  {'DR(sum)':>8}")
print(f"  {'-'*56}")
for i, L in enumerate(levels_4):
    s = sum(L)
    print(f"  L{i}     {str(L):>30}  {s:>6}  {dr(s):>8}")

assert L1 == [1, 3, 6, 8, 9],    f"L1 mismatch: {L1}"
assert L2 == [1, 4, 10, 18, 27], f"L2 mismatch: {L2}"
print(f"\n  L0, L1, L2 verified ✓")


# ============================================================
# 2. Sum sequence and power-of-3
# ============================================================
print()
print("=" * 62)
print("2.  Sum Sequence — power-of-3 analysis")
print("=" * 62)

sums = [sum(L) for L in levels_4]
print(f"\n  {'n':>4}  {'sum(Lₙ)':>10}  {'= 3^?':>8}  {'ratio vs prev':>14}  {'DR':>4}")
print(f"  {'-'*46}")
for i, s in enumerate(sums):
    log3 = math.log(s) / math.log(3)
    is_pow3 = abs(log3 - round(log3)) < 1e-9
    pow3_str = f"3^{round(log3)}" if is_pow3 else "—"
    ratio = f"{sums[i]/sums[i-1]:.4f}" if i > 0 else "—"
    print(f"  {i:>4}  {s:>10}  {pow3_str:>8}  {ratio:>14}  {dr(s):>4}")

print(f"\n  Power-of-3: n=0 (9=3²) and n=1 (27=3³). Breaks at n=2: 60 ≠ 81=3⁴.")


# ============================================================
# 3. 27 = 999/37
# ============================================================
print()
print("=" * 62)
print("3.  27 = 999/37  — 37-family connection")
print("=" * 62)

print(f"""
  999 / 37 = {999 // 37}  {'✓' if 999 // 37 == 27 else '✗'}
  999 = 10³ − 1 = 3³ × 37   (unique factorisation)
  333 = 9  × 37              (CRT modulus in emirp audit)
  111 = 3  × 37              (3-digit repunit R₃)
   27 = 3³ = sum(L1) = 999/37

  sum(L0) = 9  = 333/37 = DR_modulus
  sum(L1) = 27 = 999/37 = 3 × 9

  37 × 27 = 999 = 9 × R₃   where R₃ = 111 = 3 × 37
  The sum of L1 is the "37-quotient of 999", connecting the
  37-family CRT filter to the triangular prefix-sum structure.
""")
print(f"  sum(L1) = 27 = 999/37 ✓   sum(L0) = 9 = 333/37 ✓")


# ============================================================
# 4. Triangular numbers in L1
# ============================================================
print()
print("=" * 62)
print("4.  Triangular Numbers in L1")
print("=" * 62)

T = [k * (k + 1) // 2 for k in range(1, 8)]
print(f"\n  Triangular numbers T₁..T₇: {T}")
print(f"  L1 = {L1}")
print(f"\n  {'pos':>4}  {'L1[i]':>7}  {'T_(i+1)':>9}  {'match':>7}  {'deficit':>8}")
print(f"  {'-'*42}")
for i in range(5):
    tri = T[i]
    match = L1[i] == tri
    deficit = tri - L1[i]
    print(f"  {i:>4}  {L1[i]:>7}  {tri:>9}  {'✓' if match else '✗':>7}  {deficit:>8}")

print(f"""
  L1[0:3] = T₁,T₂,T₃ = 1,3,6  ✓
  L1[3] = 8 = T₄ − 2 = 10 − 2   (deficit from L0 descent: 2 instead of 4)
  L1[4] = 9 = T₅ − 6 = 15 − 6   (cumulative deficit)

  L0 vs ascending [1,2,3,4,5]:
""")
deficit_L0 = [L0[i] - (i + 1) for i in range(5)]
cum_deficit = list(accumulate(deficit_L0))
print(f"  L0 deficit from [1..5]:   {deficit_L0}")
print(f"  Cumulative deficit in L1: {cum_deficit}")
print(f"  (matches L1 − triangular: {[L1[i]-T[i] for i in range(5)]}  ✓)")


# ============================================================
# 5. L2 first differences = L1[1:]
# ============================================================
print()
print("=" * 62)
print("5.  L2 First Differences")
print("=" * 62)

L2_diffs = [L2[i] - L2[i - 1] for i in range(1, len(L2))]
print(f"\n  L2 = {L2}")
print(f"  L2 first differences: {L2_diffs}")
print(f"  L1[1:]              : {L1[1:]}")
print(f"  Equal: {'✓' if L2_diffs == L1[1:] else '✗'}")
print(f"""
  True by definition: S(a)[k] − S(a)[k−1] = a[k].
  So L2's differences at positions 1..4 are L1[1], L1[2], L1[3], L1[4].
  L1[0]=1 appears only as the "leftmost anchor" L2[0]=L1[0]=1.
""")


# ============================================================
# 6. DR analysis of L2[1:]
# ============================================================
print()
print("=" * 62)
print("6.  DR Analysis of L2[1:] = [4, 10, 18, 27]")
print("=" * 62)

L2_tail = L2[1:]   # [4, 10, 18, 27]
drs_tail = [dr(x) for x in L2_tail]
dr_sum = sum(drs_tail)

print(f"\n  L2[1:] = {L2_tail}")
print(f"\n  {'element':>10}  {'DR':>5}")
print(f"  {'-'*18}")
for x, d in zip(L2_tail, drs_tail):
    print(f"  {x:>10}  {d:>5}")
print(f"\n  Sum of DRs = {dr_sum}  (claimed: 23)  {'✓' if dr_sum == 23 else '✗'}")
print(f"  DR(sum)    = {dr(dr_sum)}        (claimed:  5)  {'✓' if dr(dr_sum) == 5 else '✗'}")

print(f"\n  Full L2 DRs incl. L2[0]=1:")
full_drs = [dr(x) for x in L2]
print(f"    DR({L2}) = {full_drs}")
print(f"    Sum = {sum(full_drs)}, DR = {dr(sum(full_drs))}")


# ============================================================
# 7. Closed-form sum formula
# ============================================================
print()
print("=" * 62)
print("7.  Closed-Form Sum Formula")
print("=" * 62)

def sum_formula(n):
    return (comb(n + 4, 4) + 2 * comb(n + 3, 3) + 3 * comb(n + 2, 2)
            + 2 * (n + 1) + 1)

print(f"""
  s(n) = Σⱼ L0[j] · C(n+4−j, n)
       = C(n+4,4) + 2·C(n+3,3) + 3·C(n+2,2) + 2·(n+1) + 1

  Derived from: L0[j] = {{1,2,3,2,1}} for j={{0,1,2,3,4}};
  each L0[j] contributes L0[j]·C(n+4−j, n) to the n-th level sum.
""")

print(f"  {'n':>4}  {'formula':>10}  {'actual':>10}  {'match':>7}")
print(f"  {'-'*35}")
for n in range(9):
    L = L0[:]
    for _ in range(n):
        L = list(accumulate(L))
    actual = sum(L)
    formula = sum_formula(n)
    print(f"  {n:>4}  {formula:>10}  {actual:>10}  {'✓' if formula == actual else '✗':>7}")


# ============================================================
# 8. L0 palindrome — fold structure
# ============================================================
print()
print("=" * 62)
print("8.  L0 Palindrome — Fits Exactly After Folding in Half")
print("=" * 62)

print(f"\n  L0          = {L0}")
print(f"  L0 reversed = {L0[::-1]}")
print(f"  Palindrome: {'✓' if L0 == L0[::-1] else '✗'}")
print(f"""
  Fold pairs at center (index 2, value 3):
    (L0[0], L0[4]) = (1, 1)  — equal ✓
    (L0[1], L0[3]) = (2, 2)  — equal ✓
    Center: L0[2] = 3

  "Fits exactly" here means left half = right half (palindrome),
  distinct from the origami fold where pairs sum to 10.
  The palindrome IS the fitting condition: each left value
  lands exactly on top of its mirror partner.

  Sum of fold pairs: 1+1=2, 2+2=4, center=3.  Sum=9=sum(L0) ✓
""")


# ============================================================
# 9. L0 = conv([1,1,1], [1,1,1])
# ============================================================
print()
print("=" * 62)
print("9.  L0 = [1,1,1] ★ [1,1,1]  (convolution / polynomial square)")
print("=" * 62)

base = [1, 1, 1]
conv_result = convolve(base, base)
print(f"\n  [1,1,1] ★ [1,1,1] = {conv_result}")
print(f"  = L0?  {'✓' if conv_result == L0 else '✗'}")
print(f"""
  As a polynomial: (1 + x + x²)² = 1 + 2x + 3x² + 2x³ + x⁴
  coefficients [1,2,3,2,1] = L0 ✓

  L0[k] = #{'{'}ways to choose 2 values from {{0,1,2}} summing to k{'}'}
         = self-convolution of the uniform 3-point measure.

  L0 sum = (1+1+1)² = 9 = 3²   — directly from the squaring ✓
  L1 sum = (prefix sums of L0) sum = 27 = 3³  (see section 2)

  Generating function of Lₙ: (1+x+x²)² · x^0 / (1−x)^n  (formal series)
  At x→1: indeterminate; resolved by the combinatorial formula in section 7.
""")


# ============================================================
# 10. Extended levels L0..L7
# ============================================================
print()
print("=" * 62)
print("10. Extended Levels and DR Survey")
print("=" * 62)

all_levels = [L0[:]]
for _ in range(7):
    all_levels.append(list(accumulate(all_levels[-1])))

print(f"\n  {'n':>4}  {'Lₙ':>40}  {'sum':>7}  {'DR(sum)':>8}")
print(f"  {'-'*64}")
for i, L in enumerate(all_levels):
    s = sum(L)
    print(f"  {i:>4}  {str(L):>40}  {s:>7}  {dr(s):>8}")

# Check powers of 3
print(f"\n  Sums that are powers of 3:")
found_any = False
for i, L in enumerate(all_levels):
    s = sum(L)
    log3 = math.log(s) / math.log(3)
    if abs(log3 - round(log3)) < 1e-9:
        print(f"    n={i}: sum={s} = 3^{round(log3)} ✓")
        found_any = True
if not found_any:
    print("    none found (beyond n=1)")

dr_of_sums = [dr(sum(L)) for L in all_levels]
print(f"\n  DR(sum(Lₙ)) for n=0..7: {dr_of_sums}")


# ============================================================
# Summary
# ============================================================
print()
print("=" * 62)
print("SUMMARY")
print("=" * 62)
print(f"""
  L0 = [1,2,3,2,1]  palindrome, sum=9=3², = [1,1,1]★[1,1,1]
  L1 = [1,3,6,8,9]  sum=27=3³=999/37
  L2 = [1,4,10,18,27]  sum=60

  ✓  L0, L1, L2 values correct
  ✓  sum=9=3², sum=27=3³; power-of-3 breaks at L2 (60 ≠ 81=3⁴)
  ✓  27 = 999/37; 9 = 333/37  (37-family: 333=9×37, 999=27×37)
  ✓  L1[0:3] = T₁,T₂,T₃ = 1,3,6; breaks at L1[3]=8 (deficit 2 from L0 descent)
  ✓  L2 first diffs = L1[1:] = [3,6,8,9] (by prefix-sum definition)
  ✓  DR(L2[1:]) = [4,1,9,9], sum=23, DR(23)=5
  ✓  Closed-form: s(n) = C(n+4,4)+2C(n+3,3)+3C(n+2,2)+2(n+1)+1
  ✓  L0 is a palindrome: folds exactly at center 3
  ✓  L0 = [1,1,1]★[1,1,1] = (1+x+x²)²

  Why power-of-3 stops at L1:
    sum(L0) = 3² because L0 = [1,1,1]²; sum of square = (sum of base)² = 3² = 9.
    sum(L1) = Σⱼ L0[j]·(5−j) = 1·5+2·4+3·3+2·2+1·1 = 27 = 3³.
    sum(L2) = Σⱼ L0[j]·C(6−j,2) = 1·15+2·10+3·6+2·3+1·1 = 60 ≠ 3⁴=81.
    The degree-4 polynomial s(n) is not exponential: no further 3-powers.
""")
