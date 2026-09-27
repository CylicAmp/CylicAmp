# math/theorems/one_zeros_nine_pattern.py
"""
Pattern: 1[0^n]9  — Comma Count and mod-37 Period

Construction: take n zeros, place 1 on the left and 9 on the right.
n=0: 19  |  n=1: 109  |  n=2: 1,009  |  n=6: 10,000,009  |  ...

─────────────────────────────────────────────────────────────────────────────
RIGHT COLUMN = COMMA COUNT in standard number formatting
─────────────────────────────────────────────────────────────────────────────
  The right column is floor((n+1)/3), the number of thousands-separators
  when the resulting number is written with commas:

  n zeros → number             → commas
  1  → 109                     → 0
  2  → 1,009                   → 1
  3  → 10,009                  → 1
  4  → 100,009                 → 1
  5  → 1,000,009               → 2
  6  → 10,000,009              → 2
  7  → 100,000,009             → 2
  8  → 1,000,000,009           → 3
  ...
  Formula: floor((n+1)/3).  Increases by 1 every 3 zeros.

─────────────────────────────────────────────────────────────────────────────
DIGIT SUM AND DIGITAL ROOT
─────────────────────────────────────────────────────────────────────────────
  DS(1[0^n]9) = 1+9 = 10  for ALL n.
  DR(1[0^n]9) = 1          for ALL n.
  Zeros contribute nothing to the digit sum.

─────────────────────────────────────────────────────────────────────────────
mod-37 PERIOD: cycle [19, 35, 10] with period 3
─────────────────────────────────────────────────────────────────────────────
  1[0^n]9 = 10^(n+1) + 9.
  10^3 ≡ 1 (mod 37)  because 999 = 27 × 37.
  So 10^(n+1) mod 37 cycles [10, 26, 1] with period 3.
  → 1[0^n]9 mod 37 cycles [19, 35, 10] with period 3:

    n ≡ 0 (mod 3): mod 37 = 19
    n ≡ 1 (mod 3): mod 37 = 35 = −2 (mod 37)
    n ≡ 2 (mod 3): mod 37 = 10

  The comma count (floor((n+1)/3)) and the mod-37 value both have period 3,
  but they change at different offsets.

  Comma count increases at n=2,5,8,11,...  (n ≡ 2 mod 3)
  mod-37 cycle restarts at n=0,3,6,9,...   (n ≡ 0 mod 3)
  The two period-3 structures are offset by 2.

─────────────────────────────────────────────────────────────────────────────
WHY: 1000 ≡ 1 (mod 37)
─────────────────────────────────────────────────────────────────────────────
  Comma groupings work in powers of 1000. Since 1000 ≡ 1 (mod 37),
  adding three more zeros (one comma group) is invisible in mod 37.
  The scale of the number is irrelevant to its 37-residue — only
  n mod 3 determines it.

─────────────────────────────────────────────────────────────────────────────
10,000,009 = 23 × 434,783
─────────────────────────────────────────────────────────────────────────────
  The n=6 example from the construction.
  23 is a recurring factor: 1449=9×7×23, 1541=23×67, palindrome seeds
  32500523 and 32055023 both end in suffix 23.

─────────────────────────────────────────────────────────────────────────────
NOTE: last table entry typo
─────────────────────────────────────────────────────────────────────────────
  n=13: should be 100,000,000,000,009 (the 9 was dropped in display).
  floor(14/3) = 4 commas ✓.
"""

def dr(n): return (n - 1) % 9 + 1 if n > 0 else 9
def ds(n): return sum(int(d) for d in str(n))

def make(n):
    return int('1' + '0' * n + '9')

def comma_count(num):
    return (len(str(num)) - 1) // 3


# ── Comma count formula ────────────────────────────────────────────────────────

for n in range(0, 14):
    num = make(n)
    cc = comma_count(num)
    formula = (n + 1) // 3
    assert cc == formula, f"n={n}: comma_count={cc} ≠ formula={formula}"

# Specific values from user's table (n=number of zeros)
assert make(1) == 109         and comma_count(109) == 0
assert make(2) == 1_009       and comma_count(1_009) == 1
assert make(3) == 10_009      and comma_count(10_009) == 1
assert make(4) == 100_009     and comma_count(100_009) == 1
assert make(5) == 1_000_009   and comma_count(1_000_009) == 2
assert make(6) == 10_000_009  and comma_count(10_000_009) == 2
assert make(7) == 100_000_009 and comma_count(100_000_009) == 2
assert make(8) == 1_000_000_009 and comma_count(1_000_000_009) == 3
assert make(11) == 1_000_000_000_009 and comma_count(1_000_000_000_009) == 4

# Typo check: last entry (n=13) with the 9 preserved
assert make(13) == 100_000_000_000_009
assert comma_count(100_000_000_000_009) == 4

# ── Digit sum and DR: always 10 and 1 ─────────────────────────────────────────

for n in range(0, 14):
    num = make(n)
    assert ds(num) == 10, f"n={n}: DS={ds(num)}"
    assert dr(num) == 1,  f"n={n}: DR={dr(num)}"

# ── mod-37 period-3 cycle ─────────────────────────────────────────────────────

# 10^3 ≡ 1 (mod 37) because 999 = 27 × 37
assert 10**3 % 37 == 1
assert 999 == 27 * 37

# Cycle [19, 35, 10]
MOD37_CYCLE = [19, 35, 10]
for n in range(0, 12):
    num = make(n)
    expected = MOD37_CYCLE[n % 3]
    assert num % 37 == expected, f"n={n}: {num} mod 37 = {num%37} ≠ {expected}"

# Explicitly
assert make(0) % 37 == 19   # n≡0: 19
assert make(1) % 37 == 35   # n≡1: 35=-2
assert make(2) % 37 == 10   # n≡2: 10
assert make(6) % 37 == 19   # n=6 example

# 1000 ≡ 1 (mod 37): comma grouping is invisible to mod 37
assert 1000 % 37 == 1
# Adding 3 zeros (one comma group) doesn't change mod-37 residue
for n in range(0, 9):
    assert make(n) % 37 == make(n + 3) % 37, f"n={n}: period-3 violated"

# ── The two period-3 structures are offset by 2 ───────────────────────────────

# Comma count increases at n=2,5,8,11 (n≡2 mod 3)
# mod-37 cycle restarts at n=0,3,6,9 (n≡0 mod 3)
for n in range(1, 12):
    if n % 3 == 2:  # comma count increases here
        assert comma_count(make(n)) == comma_count(make(n - 1)) + 1
        assert make(n) % 37 == 10   # at this point mod37=10 (not the cycle start)

# ── 10,000,009 = 23 × 434,783 ─────────────────────────────────────────────────

assert 23 * 434_783 == 10_000_009
assert 10_000_009 % 23 == 0

# 23 in framework context
assert '32500523'.endswith('23')
assert '32055023'.endswith('23')
assert 1449 % 23 == 0    # 1449 = 9×7×23
assert 1541 % 23 == 0    # 1541 = 23×67


if __name__ == "__main__":
    print("Pattern: 1[0^n]9")
    print()
    print(f"{'n':>3}  {'number':>22}  commas  DS  DR  mod37")
    for n in range(0, 14):
        num = make(n)
        print(f"{n:>3}  {num:>22,d}  {comma_count(num)}       {ds(num):2d}   {dr(num)}   {num%37:2d}")
    print()
    print(f"Comma count formula: floor((n+1)/3)  — increases every 3 zeros")
    print(f"DS = 10, DR = 1 for all n  (zeros contribute nothing)")
    print(f"mod 37 cycle [19,35,10] period 3  (10^3≡1 mod 37, 999=27×37)")
    print(f"Two period-3 structures offset by 2:")
    print(f"  comma count  steps at n≡2(mod 3): {[n for n in range(12) if n%3==2]}")
    print(f"  mod37 cycle resets at n≡0(mod 3): {[n for n in range(12) if n%3==0]}")
    print()
    print(f"10,000,009 = 23×434783  (23 connects palindrome seeds, 1449, 1541)")
    print(f"1000≡1(mod 37): comma scale is invisible to the 37-field")
    print()
    print("All assertions passed.")
