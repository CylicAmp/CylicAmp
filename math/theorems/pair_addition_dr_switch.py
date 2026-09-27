"""
Pair Addition: Even Sum → Odd Digital Root Switch at n=5

For n in 1..9, doubling n gives 2n. The DR of 2n shows a clean 4:5 split:
  n=1..4 → DR(2n) ∈ {2,4,6,8}   (EVEN)  — 2n fits in [1..9], no wraparound
  n=5..9 → DR(2n) ∈ {1,3,5,7,9} (ODD)   — 2n > 9, subtract one full cycle

WHY the parity flips:
  DR(2n) = 2n       when n ≤ 4   (2n ≤ 8 ≤ 9)
  DR(2n) = 2n - 9   when n ≥ 5   (2n ≥ 10 > 9)

  2n is always EVEN.
  2n - 9 = EVEN - ODD = ODD.

  So the 9-wraparound converts even DR → odd DR.
  The boundary is n=4 (last pre-wrap) vs n=5 (first post-wrap).

4:5 split:
  Even DRs in {1..9}: {2,4,6,8}       — 4 values
  Odd  DRs in {1..9}: {1,3,5,7,9}     — 5 values
  4 + 5 = 9 = full cycle

Connection to zero-decimal comma system:
  Groups of 4 (even): produce ECO pattern when they are the leftmost group
  Groups of 3 (odd) : produce OCO — and 5 of the 9 DRs are odd
  The 4:5 split mirrors the 4 even / 5 odd digit count in {1..9}
"""


def dr(n):
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


# ---------------------------------------------------------------------------
# Table
# ---------------------------------------------------------------------------

ROWS = [(n, n + n, dr(n + n)) for n in range(1, 10)]

# ---------------------------------------------------------------------------
# Assertions
# ---------------------------------------------------------------------------

# n=1..4: DR(2n) is even (no wraparound)
for n in range(1, 5):
    assert dr(2 * n) == 2 * n,          f"n={n}: expected dr(2n)=2n={2*n}"
    assert dr(2 * n) % 2 == 0,          f"n={n}: DR should be even"

# n=5..9: DR(2n) is odd (wraparound: 2n-9)
for n in range(5, 10):
    assert dr(2 * n) == 2 * n - 9,      f"n={n}: expected dr(2n)=2n-9={2*n-9}"
    assert dr(2 * n) % 2 == 1,          f"n={n}: DR should be odd"

# Switch point
assert dr(8)  % 2 == 0   # n=4: last even DR
assert dr(10) % 2 == 1   # n=5: first odd DR
assert dr(10) == 1        # 10 → 1 (subtract 9)

# 4:5 split
even_drs = [dr(2 * n) for n in range(1, 5)]
odd_drs  = [dr(2 * n) for n in range(5, 10)]
assert sorted(even_drs) == [2, 4, 6, 8]
assert sorted(odd_drs)  == [1, 3, 5, 7, 9]
assert len(even_drs) + len(odd_drs) == 9

# 2n mod 9 sequence: 2,4,6,8,1,3,5,7,0  (dr treats 0 as 9)
mod9_seq = [(2 * n) % 9 for n in range(1, 10)]
assert mod9_seq == [2, 4, 6, 8, 1, 3, 5, 7, 0]


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 70)
    print("PAIR ADDITION: Even Sum vs Odd Digital Root Switch")
    print("=" * 70)

    print(f"\n  {'n':>3} | {'n+n':>4} | {'dr(2n)':>8} | {'dr parity':>9} | {'2n mod 9':>8}")
    print(f"  {'─' * 50}")

    for n, s, d in ROWS:
        parity = "odd" if d % 2 == 1 else "even"
        mod9 = s % 9
        print(f"  {n:>3} | {s:>4} | {d:>8} | {parity:>9} | {mod9:>8}")

    print()
    print("─" * 50)
    print("KEY OBSERVATION:")
    print("  n = 1,2,3,4: dr(2n) = 2,4,6,8 → ALL EVEN")
    print("  n = 5,6,7,8,9: dr(2n) = 1,3,5,7,9 → ALL ODD")
    print()
    print("  The switch happens at n = 5.")
    print("  2*4 = 8 (dr=8, even) → 2*5 = 10 (dr=1, odd)")
    print()
    print("  WHY: 2n mod 9 for n=1..9 gives:")
    print("  2,4,6,8,1,3,5,7,0(→9)")
    print("  These are the 9 values mod 9, relabeled by dr.")
    print()
    print("  The even digital roots {2,4,6,8} come from n=1,2,3,4")
    print("  The odd digital roots {1,3,5,7,9} come from n=5,6,7,8,9")
    print()
    print("  4 even drs + 5 odd drs = 9 total")
    print("  This is the 4:5 split.")
    print()
    print("PROOF:")
    print("  DR(2n) = 2n      for n ≤ 4  (2n ≤ 8, fits in cycle)")
    print("  DR(2n) = 2n - 9  for n ≥ 5  (2n ≥ 10, wraps once)")
    print("  2n is EVEN; 2n - 9 is EVEN - ODD = ODD.")
    print("  The 9-wraparound converts even → odd. QED.")
    print()
    print("All assertions passed.")
