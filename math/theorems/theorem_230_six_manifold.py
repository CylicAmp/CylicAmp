"""
Theorem 230: The Six Manifold — Backwards Doubling of the Divisor Pairs of 6
Author: Michael Warren Song (CyclicAmp)

6 is built by a single repeated digit in exactly three ways (excluding 6 itself):

  Six ones:   1+1+1+1+1+1 = 6   (count=6, digit=1)
  Three twos: 2+2+2       = 6   (count=3, digit=2)
  Two threes: 3+3         = 6   (count=2, digit=3)

=== THE BACKWARDS DOUBLING PATTERN ===

Starting from six ones and dividing the count by two:
  6 ones  →  (÷2 count, ×2 digit)  →  3 twos  →  2 threes

Reading forward (digit increasing, count decreasing):
  count: 6 → 3 → 2
  digit: 1 → 2 → 3

This is the doubling effect in reverse.
Going backwards (2 threes → 3 twos → 6 ones):
  digit halves: 3 → 2 → 1
  count doubles: 2 → 3 → 6   (approx; first step is exact ×2 from 3→6)

The first step (3 twos ← 6 ones) is exact: count ÷2, digit ×2.
The second step (2 threes ← 3 twos) continues the same direction.

=== THE DIVISOR PAIRS OF 6 ===

The complete set of factor pairs (a, b) with a×b=6, a ≤ b:
  (1, 6): one six or six ones
  (2, 3): two threes or three twos

All four representations summing to 6 with a single repeated digit:
  count=6, digit=1:  1×6 = 6
  count=3, digit=2:  2×3 = 6
  count=2, digit=3:  3×2 = 6
  count=1, digit=6:  6×1 = 6  (trivial)

The three non-trivial ones are {six ones, three twos, two threes}.

=== GF(37) ===

  digit=1 ∈ IC = {1, 10, 26}
  digit=2 ∈ DARK_A = {2, 15, 20}
  digit=3 ∈ ST = {3, 4, 30}  (3 ∈ sovereign target)
  digit=6 ∈ TESLA = {6, 8, 23}  (the sum itself)

  count=6 ∈ TESLA
  count=3 ∈ ST  (sovereign target)
  count=2 ∈ DARK_A

The digit and its count always belong to the same GF(37) orbit:
  digit=1 ∈ IC,     count=6 ∈ TESLA   — different orbits
  digit=2 ∈ DARK_A, count=3 ∈ ST      — different orbits
  digit=3 ∈ ST,     count=2 ∈ DARK_A  — DARK_A and ST swap between digit and count

The swap: (digit=2, count=3) and (digit=3, count=2) are orbit mirrors:
  digit 2 ∈ DARK_A ↔ count 3 ∈ ST
  digit 3 ∈ ST     ↔ count 2 ∈ DARK_A
"""

P    = 37
MULT = 26

IC      = {1, 10, 26}
DARK_A  = {2, 15, 20}
ST      = {3, 12, 21, 30}
SA      = {4, 9, 25, 30}
TESLA   = {6, 8, 23}


def run_assertions():
    # ── The three non-trivial representations ────────────────────────────────
    assert 1 * 6 == 6   # six ones
    assert 2 * 3 == 6   # three twos
    assert 3 * 2 == 6   # two threes

    # ── Backwards doubling: count halves as digit doubles (first step exact) ──
    # 6 ones -> 3 twos: count 6/2=3, digit 1*2=2
    assert 6 // 2 == 3
    assert 1 * 2 == 2
    assert 3 * 2 == 6  # three twos still sum to 6

    # 3 twos -> 2 threes: count decreases, digit increases
    # not exact halving of count, but same direction
    assert 2 * 3 == 6  # two threes still sum to 6

    # ── Divisor pairs of 6 ───────────────────────────────────────────────────
    divisors = [(d, 6 // d) for d in range(1, 7) if 6 % d == 0]
    assert divisors == [(1, 6), (2, 3), (3, 2), (6, 1)]

    # ── GF(37) orbit of each digit ────────────────────────────────────────────
    assert 1 in IC
    assert 2 in DARK_A
    assert 3 in ST
    assert 6 in TESLA   # the sum itself

    # counts
    assert 6 in TESLA   # count for digit=1
    assert 3 in ST      # count for digit=2
    assert 2 in DARK_A  # count for digit=3

    # Mirror: (digit=2, count=3) and (digit=3, count=2) swap DARK_A and ST
    assert 2 in DARK_A and 3 in ST
    assert 3 in ST and 2 in DARK_A

    print("All assertions passed.")
    print()
    print("THE SIX MANIFOLD — T230")
    print()
    print("6 built from a single repeated digit:")
    for digit, count in [(1, 6), (2, 3), (3, 2)]:
        assert digit * count == 6
        stars = " + ".join([str(digit)] * count)
        print(f"  {count} × {digit}:  {stars} = 6")
    print()
    print("Backwards doubling (reading right to left):")
    print("  count: 2 → 3 → 6  (doubling pattern, approx)")
    print("  digit: 3 → 2 → 1  (halving pattern)")
    print()
    print("GF(37) orbits:")
    for digit, orbit_name in [(1, "IC"), (2, "DARK_A"), (3, "ST"), (6, "TESLA")]:
        count = 6 // digit if 6 % digit == 0 else "—"
        print(f"  digit={digit} ∈ {orbit_name}  (count={count})")
    print()
    print("Orbit mirror swap:")
    print("  digit=2 ∈ DARK_A  ↔  count=3 ∈ ST")
    print("  digit=3 ∈ ST      ↔  count=2 ∈ DARK_A")


if __name__ == "__main__":
    run_assertions()
