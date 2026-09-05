"""
digit_cycles_1_9.py

Three digit cycles partition {1,...,9} completely.
Each cycle is defined by chaining pairs XY where the last digit
of one pair becomes the first digit of the next.

CYCLE A — digits {2, 5, 6}
  2=(26)=6=(65)=5=(56)=6=(62)=2  (palindromic 4-step, pivot: 6)

CYCLE B — digits {1, 3, 7}
  1=(13)=3=(37)=7=(73)=3=(31)=1  (palindromic 4-step, pivot: 3)
  All four pairs — 13, 37, 73, 31 — are prime.
  They form two emirp pairs: 13↔31 and 37↔73.
  Digits {1,3,7} are the digits of 137.

CYCLE C — digits {4, 8, 9}
  4=(48)=8=(89)=9=(94)=4  (pure 3-cycle)

Each cycle contains exactly one element of {3,6,9}:
  Cycle A pivot: 6
  Cycle B pivot: 3
  Cycle C close: 9
"""

from sympy import isprime

# ── CHAIN RULE ────────────────────────────────────────────────────────────────

cycles = {
    'A': [(2,6),(6,5),(5,6),(6,2)],
    'B': [(1,3),(3,7),(7,3),(3,1)],
    'C': [(4,8),(8,9),(9,4)],
}

for name, pairs in cycles.items():
    for i in range(len(pairs)):
        _, y = pairs[i]
        nx, _ = pairs[(i+1) % len(pairs)]
        assert y == nx, f'Cycle {name}: chain broken at step {i}'

# ── PARTITION ─────────────────────────────────────────────────────────────────

all_digits = set(d for pairs in cycles.values() for x,y in pairs for d in (x,y))
assert all_digits == set(range(1, 10))

# ── CYCLE B: ALL PAIRS PRIME, TWO EMIRP PAIRS ─────────────────────────────────

b_pairs = [13, 37, 73, 31]
assert all(isprime(n) for n in b_pairs)
assert isprime(13) and isprime(31) and int(str(13)[::-1]) == 31
assert isprime(37) and isprime(73) and int(str(37)[::-1]) == 73

# ── {3,6,9} PIVOTS ────────────────────────────────────────────────────────────

assert {2,5,6} & {3,6,9} == {6}   # Cycle A pivot
assert {1,3,7} & {3,6,9} == {3}   # Cycle B pivot
assert {4,8,9} & {3,6,9} == {9}   # Cycle C close

# ── DIGIT SUMS ────────────────────────────────────────────────────────────────

def dr(n): return 0 if n == 0 else 1+(n-1)%9

assert sum({2,5,6}) == 13 and dr(13) == 4
assert sum({1,3,7}) == 11 and dr(11) == 2   # dr=2 = dr(137)
assert sum({4,8,9}) == 21 and dr(21) == 3
assert sum(range(1,10)) == 45

# ── OUTPUT ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Digit Cycles — Partition of {1,...,9}")
    print("=" * 50)
    for name, pairs in cycles.items():
        nums = [int(f'{x}{y}') for x,y in pairs]
        digits = sorted(set(d for x,y in pairs for d in (x,y)))
        print(f"  Cycle {name}: digits={digits}, pairs={nums}, all prime={all(isprime(n) for n in nums)}")
    print()
    print("  {3,6,9} pivots: A→6, B→3, C→9")
    print("  Cycle B pairs {13,37,73,31}: all prime, emirp pairs 13↔31 and 37↔73")
    print("  Digits of 137 = {1,3,7} = Cycle B")
    print()
    print("All assertions passed.")
