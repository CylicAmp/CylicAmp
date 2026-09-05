"""
Open/Closed System Grid Theorem — THEOREM 72

SOURCE: Observation that closed systems (same digit repeating) cannot generate
complexity beyond their own factor, while open systems (sequential digit filling)
naturally produce 37.

THE GRID:
  A 3×3 grid begins as a closed system: nine 1s.
  Open filling proceeds sequentially — each new digit takes its place:

    121    123    123    123    123    123    1-23    1-2345678-1
    111 -> 111 -> 411 -> 451 -> 456 -> 456 -> 456 ->
    111    111    111    111    111    711    78-1

  The open sequence: 1, 2, 3, 4, 5, 6, 7, 8, 1 (boundary 1s at each end)
  Collapse: 1-2345678-1

THEOREM (Closed System Bound).
  The closed system (nine 1s, digit sum=9) can only produce multiples of 11
  within itself: 11, 22, 33, ..., 99. Its DR cycles {2,4,6,8,1,3,5,7,9}
  but never escapes the 11-family. Complexity is bounded by self-interaction.

THEOREM (Open System Sum = 37).
  The complete open filling 1-2345678-1 has digit sum:
    1+2+3+4+5+6+7+8+1 = 37 = THE PRIME.
  The interior digits 1+2+...+8 = 36 ∈ ORBIT_11 (the antipode -1 mod 37).
  Adding one boundary 1: 36+1 = 37. The open system's signature IS the prime.

GF(37) CONNECTIONS:
  • Closed system sum = 9 ∈ SA: the sovereign anchor — locked, cannot evolve.
  • Interior sum = 36 ∈ ORBIT_11: 36 ≡ -1 mod 37, the maximum before reset.
  • Open system sum = 37 = THE PRIME: the complete sequence generates GF(37).
  • SEAM = 0 = 37 mod 37: the prime collapses to SEAM — completion, not origin.
  • The boundary 1s are not walls. They are the bookends that make expansion possible.

THE THIRD BODY:
  Two closed systems (1s and 2s segregated) cannot reach 3 by interaction.
  The third element is not a problem — it is the mechanism of growth.
  28 × 2 = 56, not 57. The gap of 1 forces the system to open (28.05 + 28.05 = 57).
  The closed doubling always lands one short. The outside factor is inevitable.

  "Open / Closed / Third body — which isn't the problem, it's the solution."

NATURAL LAW:
  The sequential filling 1→2→3→...→8 cannot be stopped at any intermediate step
  without violating the natural order of integers. Attempting to hold the grid
  at 111/111/111 produces a sum of 9 — sovereign but frozen. The prime 37
  only appears when the full sequence is permitted to complete.
"""

# ── Constants ──────────────────────────────────────────────────────────────────

SA         = frozenset({4, 9, 25, 30})
ORBIT_11   = frozenset({11, 27, 36})
SEAM       = 0


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


# ── Key checks ─────────────────────────────────────────────────────────────────

# Closed system: nine 1s
_closed_sum = 9 * 1
assert _closed_sum == 9 and 9 in SA              # closed sum ∈ SA — locked

# Open sequence: 1,2,3,4,5,6,7,8,1
_open_seq = [1, 2, 3, 4, 5, 6, 7, 8, 1]
_open_sum = sum(_open_seq)
assert _open_sum == 37                            # open sum = THE PRIME

# Interior: 1+2+...+8
_interior = sum(range(1, 9))
assert _interior == 36 and 36 in ORBIT_11        # interior ∈ ORBIT_11 (-1 mod 37)
assert _interior + 1 == 37                        # one boundary 1 → prime

# SEAM: the prime collapses to SEAM mod 37
assert 37 % 37 == SEAM                            # completion = SEAM

# 11-family stays closed: 11n for n=1..9 never leaves 11-multiples
for n in range(1, 10):
    assert (11 * n) % 11 == 0                     # always multiple of 11

# The gap of 1 in doubling: 28×2=56, need 57
assert 28 * 2 == 56 and 56 + 1 == 57            # closed doubling lands one short

# DR of closed system = 9
assert dr(9) == 9 and 9 in SA

# DR of open sum = DR(37) = DR(3+7) = 10 → 1 ∈ IC (identity cycle)
IC = frozenset({1, 10, 26})
assert dr(37) == 1 and 1 in IC                   # open system DR ∈ IC


if __name__ == "__main__":
    print("Open/Closed System Grid Theorem — THEOREM 72")
    print("=" * 60)
    print()
    print("CLOSED system (nine 1s):")
    print(f"  digit sum = {_closed_sum}  ∈ SA (sovereign anchor, frozen)")
    print()
    print("OPEN sequence (1-2345678-1):")
    print(f"  digits: {_open_seq}")
    print(f"  digit sum = {_open_sum} = THE PRIME 37")
    print(f"  interior 1+2+...+8 = {_interior}  ∈ ORBIT_11 (≡ -1 mod 37)")
    print(f"  36 + 1 boundary = 37")
    print()
    print("The gap of 1:")
    print(f"  28 × 2 = {28*2}  (one short of 57)")
    print(f"  closed doubling always lands one short — the outside factor is forced")
    print()
    print("GF(37):")
    print(f"  closed sum 9 ∈ SA: {9 in SA}")
    print(f"  interior 36 ∈ ORBIT_11: {36 in ORBIT_11}")
    print(f"  open sum 37 mod 37 = {37%37} = SEAM (completion)")
    print(f"  DR(37) = {dr(37)} ∈ IC (identity cycle)")
    print()
    print("All assertions pass.")
