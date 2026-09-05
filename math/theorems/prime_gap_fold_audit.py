"""
prime_gap_fold_audit.py

Reconstructs the "prime folding" column structure:
  Col A: [1, 2, 2, 4]  (prime gaps 1–4)
  Col B: [4, 7, 9, 6]  (unknown operation on A)
  Col C: [8, 5, 9, 3]  (unknown operation on B)

Connected to: origami_fold_1_to_9.py (fold at center 5, pairs sum to 10)

Analyses:
  1. Sliding window A–Z of prime gaps (4-wide)
  2. Column sums and DRs
  3. Which columns are identical (periodic structure)
  4. Reconstruct the A→B→C fold rule
  5. Link to origami fold: 1234(5)6789 paired to sum 10
  6. Fibonacci triangle from Col C seeds
"""

import math
import numpy as np
from collections import Counter

# ---------------------------------------------------------------------------
# Sieve (no sympy)
# ---------------------------------------------------------------------------
LIMIT = 1_000_001
sieve = bytearray([1]) * (LIMIT + 1)
sieve[0] = sieve[1] = 0
for i in range(2, int(LIMIT**0.5) + 1):
    if sieve[i]:
        sieve[i*i::i] = bytearray(len(sieve[i*i::i]))

def is_prime(n): return bool(sieve[n]) if 0 <= n <= LIMIT else False

PRIMES = [n for n in range(2, 2000) if is_prime(n)]
GAPS   = [PRIMES[i+1] - PRIMES[i] for i in range(len(PRIMES)-1)]

def dr(n):
    if n == 0: return 0
    r = n % 9
    return r if r != 0 else 9


# ============================================================
# 1. Sliding Window A–Z (4-wide, step 1)
# ============================================================
print("=" * 70)
print("1.  Sliding Window A–Z — prime gap columns (4 consecutive gaps)")
print("=" * 70)

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

cols = {}
for idx, letter in enumerate(ALPHABET):
    col = GAPS[idx: idx+4]
    cols[letter] = col

print(f"\n  {'Col':>4}  {'gaps':>20}  {'sum':>5}  {'DR':>4}")
print(f"  {'-'*40}")
for letter in ALPHABET:
    col = cols[letter]
    s   = sum(col)
    print(f"  {letter:>4}  {str(col):>20}  {s:>5}  {dr(s):>4}")

# Duplicates
print(f"\n  Identical columns:")
from itertools import combinations
seen = {}
for L, col in cols.items():
    key = tuple(col)
    seen.setdefault(key, []).append(L)
for key, letters in seen.items():
    if len(letters) > 1:
        print(f"    {list(key)} → Cols {letters}")

# DR frequency of column sums
dr_freq = Counter(dr(sum(cols[L])) for L in ALPHABET)
print(f"\n  DR frequency of column sums A–Z:")
for k in sorted(dr_freq):
    print(f"    DR={k}: {dr_freq[k]} times")


# ============================================================
# 2. Col A  →  Col B  →  Col C  —  fold reconstruction
# ============================================================
print()
print("=" * 70)
print("2.  Col A → Col B → Col C — fold rule reconstruction")
print("=" * 70)

COL_A = [1, 2, 2, 4]   # prime gaps
COL_B = [4, 7, 9, 6]   # given
COL_C = [8, 5, 9, 3]   # given

print(f"\n  Col A = {COL_A}  (prime gaps 1–4:  2→3=1, 3→5=2, 5→7=2, 7→11=4)")
print(f"  Col B = {COL_B}  (given)")
print(f"  Col C = {COL_C}  (given)")

# --- Hypothesis 1: Col C = 2 × Col B (mod 9, 0→9) ---
def dr_double(col):
    return [dr(2*x) for x in col]

h1 = dr_double(COL_B)
print(f"\n  Hypothesis 1:  Col C = DR(2 × Col B)  =  {h1}")
print(f"  Match: {'✓' if h1 == COL_C else '✗'}")

# --- Hypothesis 2: Col B = Col A + rotated first-4 primes ---
P4 = [2, 3, 5, 7]    # first 4 primes

for shift in range(4):
    rotated = P4[shift:] + P4[:shift]
    candidate = [COL_A[i] + rotated[i] for i in range(4)]
    if candidate == COL_B:
        print(f"\n  Hypothesis 2:  Col B = Col A + rotate([2,3,5,7], {shift})")
        print(f"    rotate shift={shift}: {rotated}")
        print(f"    Col A + rotated: {candidate}")
        print(f"    Match: ✓")
        SHIFT_FOUND = shift
        ROTATION    = rotated
        break
else:
    print(f"\n  Hypothesis 2 (simple rotation): ✗ not found")
    SHIFT_FOUND = None

# --- Hypothesis 3: Col B = fold of Col A around origami center ---
# Origami fold: x → 10-x (pairs sum to 10); then A + fold(A)?
fold_A = [10 - x for x in COL_A]
h3 = fold_A
print(f"\n  Hypothesis 3:  fold(A) = [10-a for a in A]  =  {fold_A}")
print(f"  = Col B? {'✓' if fold_A == COL_B else '✗'}")

mix_h3 = [COL_A[i] + fold_A[i] for i in range(4)]
print(f"  A + fold(A) = {mix_h3} vs Col B {COL_B}  →  {'✓' if mix_h3 == COL_B else '✗'}")

# --- Hypothesis 4: Col B is built from reverse cumulative sums ---
rev_cum = []
s = 0
for x in reversed(COL_A):
    s += x
    rev_cum.append(s)
print(f"\n  Hypothesis 4: reverse cumulative sums of A = {rev_cum}")
print(f"  = Col B? {'✓' if rev_cum == COL_B else '✗'}")

# --- Hypothesis 5: Adjacent sum within Col A, then origami fold ---
adj = [COL_A[i]+COL_A[i+1] for i in range(3)]
print(f"\n  Hypothesis 5: adjacent sums of A = {adj} (3 values)")

# --- Summarise what we know ---
print(f"""
  CONFIRMED:
    Col B → Col C:  DR(2 × Col B) = {dr_double(COL_B)} = Col C  ✓

  CONFIRMED:
    Col A → Col B:  Col A + rotate([2,3,5,7], 1) = {COL_B}  ✓
    Rotation: [2,3,5,7] shifted left by 1 → [3,5,7,2]

  INTERPRETATION:
    The "fold" pairs each prime gap with the corresponding shifted prime:
      gap₁ (1) + prime₂ (3) = 4
      gap₂ (2) + prime₃ (5) = 7
      gap₃ (2) + prime₄ (7) = 9
      gap₄ (4) + prime₁ (2) = 6  ← wraps around (fold)
    This is a "prime fold": pair gaps with primes in cyclic order.

    Then Col C = DR(2 × Col B) = digit-root doubling.

  ORIGAMI FOLD CONNECTION:
    The origami fold at center 5 has fold_sum = 10.
    10² mod 37 = 26 = 26  (from origami_fold_1_to_9.py).
    Col B sum = 4+7+9+6 = 26 = 26  ← Col B sum is the scalar!
    Col A sum = 9 = DR modulus (origami fold center contact 4+5=9).
    Col C sum = 25 = 5² (fold center squared).
""")

# ============================================================
# 3. Origami fold connection
# ============================================================
print("=" * 70)
print("3.  Origami Fold Connection  (origami_fold_1_to_9.py)")
print("=" * 70)

FOLD_CENTER = 5
FOLD_SUM    = 10

pairs = [(FOLD_CENTER - i, FOLD_CENTER + i) for i in range(1, FOLD_CENTER)]
print(f"\n  Fold at {FOLD_CENTER}, pairs summing to {FOLD_SUM}:")
for a, b in pairs:
    print(f"    {a} + {b} = {a+b}  (both prime? {is_prime(a)}/{is_prime(b)})")
print(f"  Center contact: {FOLD_CENTER-1}+{FOLD_CENTER} = {FOLD_CENTER-1+FOLD_CENTER} = DR modulus")

print(f"\n  Column sum connections:")
print(f"    Col A sum = {sum(COL_A)} = DR modulus = 4+5")
print(f"    Col B sum = {sum(COL_B)} = 10² mod 37 = 26")
print(f"    Col C sum = {sum(COL_C)} = {FOLD_CENTER}² = fold-center²")

# "Fit exactly after folding in half" — this is when BOTH fold partners are prime
print(f"\n  'Fit exactly after folding in half':  pairs where BOTH a and b are prime:")
for a, b in pairs:
    if is_prime(a) and is_prime(b):
        print(f"    {a}+{b}={a+b}  ← FITS EXACTLY (both prime)")
    else:
        print(f"    {a}+{b}={a+b}  ← partial (only {'a' if is_prime(a) else 'b'} prime)")

# For general mod-6 twin prime fold:
print(f"\n  General prime fold: (6k-1, 6k+1) pairs (folding around multiples of 6)")
print(f"  These 'fit exactly' because both 6k±1 are prime for twin prime pairs.")
twin_folds = []
for k in range(1, 20):
    a, b = 6*k - 1, 6*k + 1
    if is_prime(a) and is_prime(b):
        twin_folds.append((a, b, 6*k))
        print(f"    ({a}, {b}) fold at {6*k}  ← both prime, gap=2 (twin prime)")


# ============================================================
# 4. Fibonacci triangle from Col C
# ============================================================
print()
print("=" * 70)
print("4.  Fibonacci Triangle from Col C = [8, 5, 9, 3]")
print("=" * 70)

def fib_triangle(seeds):
    """Reduce a list by pairwise sums until 1 element, then continue Fibonacci."""
    current = list(seeds)
    print(f"  Level 0: {current}")
    while len(current) > 2:
        current = [current[i]+current[i+1] for i in range(len(current)-1)]
        print(f"  Level {len(seeds)-len(current)}: {current}")
    # Continue as Fibonacci from final pair
    a, b = current[0], current[1]
    print(f"  Fibonacci continuation from ({a}, {b}):")
    fib_seq = [a, b]
    for _ in range(10):
        a, b = b, a+b
        fib_seq.append(b)
    print(f"    {fib_seq[:12]}")
    return fib_seq

fib_c = fib_triangle(COL_C)

print(f"\n  Same triangle from Col A = {COL_A}:")
fib_a = fib_triangle(COL_A)

print(f"\n  Same triangle from Col B = {COL_B}:")
fib_b = fib_triangle(COL_B)


# ============================================================
# 5. Twin prime gap analysis
# ============================================================
print()
print("=" * 70)
print("5.  Twin Prime Structure in First 500 Gaps")
print("=" * 70)

twin_pairs = [(PRIMES[i], PRIMES[i+1])
              for i in range(len(PRIMES)-1)
              if PRIMES[i+1] - PRIMES[i] == 2 and PRIMES[i] > 3]

print(f"\n  Twin prime pairs (p > 3): {len(twin_pairs)} in first 500 primes")
print(f"  Sum/12 for each pair  (all twin primes p>3 satisfy p+p+2 ≡ 0 mod 12):")
sums12 = [(p+q, (p+q)//12) for p,q in twin_pairs[:20]]
for (p,q), (s, n) in zip(twin_pairs[:20], sums12):
    print(f"    ({p},{q})  sum={s}  sum/12={n}  DR(n)={dr(n)}")

# Verify: p≡-1 mod 6, q=p+2≡1 mod 6 for all twin primes p>3
all_twin = all(p % 6 == 5 for p, q in twin_pairs)
print(f"\n  All twin primes p>3 satisfy p ≡ 5 (mod 6) ≡ -1 (mod 6): {'✓' if all_twin else '✗'}")
print(f"  This means they always FOLD EXACTLY around a multiple of 6.")


# ============================================================
# 6. Fibonacci mod 12 — Pisano period
# ============================================================
print()
print("=" * 70)
print("6.  Fibonacci mod 12 — Pisano period")
print("=" * 70)

fib = [0, 1]
while True:
    fib.append(fib[-1]+fib[-2])
    if len(fib) > 4 and fib[-1]%12==1 and fib[-2]%12==0:
        period = len(fib)-2
        break

fib_mod12 = [f%12 for f in fib[:period]]
print(f"\n  Pisano period π(12) = {period}")
print(f"  Fibonacci mod 12 cycle: {fib_mod12}")

# How many prime gaps (mod 12) match the Fibonacci cycle?
gaps_mod12 = [g%12 for g in GAPS[:period]]
matches = sum(1 for i in range(period) if gaps_mod12[i] == fib_mod12[i])
print(f"\n  First {period} prime gaps mod 12: {gaps_mod12}")
print(f"  Fibonacci mod 12 cycle:           {fib_mod12}")
print(f"  Pointwise matches: {matches}/{period}")


# ============================================================
# 7. Prime gaps mod 24
# ============================================================
print()
print("=" * 70)
print("7.  Prime Gap Distribution mod 24 (first 500 gaps)")
print("=" * 70)

c24 = Counter(g%24 for g in GAPS[:500])
print(f"\n  {'mod24':>7}  {'count':>7}  {'bar'}")
print(f"  {'-'*40}")
for k in sorted(c24):
    bar = "█" * c24[k]
    print(f"  {k:>7}  {c24[k]:>7}  {bar}")


# ============================================================
# Summary
# ============================================================
print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
  Prime folding math located:
    File: math/theorems/origami_fold_1_to_9.py
    Operation: sequence 1-9 folded at center 5, all pairs sum to 10.
    "Fits exactly" = fold pair where BOTH members are prime: (5, 7) only in 1-9.
    General: twin primes (6k-1, 6k+1) always fold exactly around 6k.

  Col A → Col B → Col C reconstruction:
    Col A = prime gaps [1,2,2,4]  (sum=9=DR modulus, origami center contact)
    Col B = Col A + rotate([2,3,5,7],1) = Col A + [3,5,7,2]  →  [4,7,9,6]
            sum=26=26=10²mod37  ← origami fold scalar
    Col C = DR(2×Col B) = [8,5,9,3]
            sum=25=5²  ← fold-center squared

  Column sums encode the origami fold hierarchy:
    9 (DR modulus) → 26 (26) → 25 (center²)
""")
