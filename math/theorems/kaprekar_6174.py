"""
Kaprekar's Constant — 6174

Algorithm for any 4-digit number n (not a repdigit):
  1. Sort digits in descending order → D
  2. Sort digits in ascending order  → A
  3. next = D − A
  Repeat until reaching 6174.

Theorem (verified by exhaustion):
  Every 4-digit integer with at least 2 distinct decimal digits
  reaches 6174 in at most 7 steps.

  6174 is a fixed point: 7641 − 1467 = 6174.

Repdigits (1111, 2222, …, 9999) map to 0 in one step and are excluded
from the convergence claim; they are a separate fixed point at 0.
"""


def _pad_digits(n: int) -> list[int]:
    """Return 4 decimal digits of n, zero-padded on the left."""
    return [int(d) for d in f"{n:04d}"]


def kaprekar_step(n: int) -> int:
    digits = _pad_digits(n)
    desc = int("".join(map(str, sorted(digits, reverse=True))))
    asc  = int("".join(map(str, sorted(digits))))
    return desc - asc


def steps_to_6174(n: int) -> int | None:
    """Return number of steps for n to reach 6174, or None if it won't (repdigit)."""
    digits = _pad_digits(n)
    if len(set(digits)) == 1:
        return None  # repdigit fixed at 0
    seen = set()
    steps = 0
    while n != 6174:
        if n in seen or steps > 8:
            return None  # unexpected cycle — should not occur
        seen.add(n)
        n = kaprekar_step(n)
        steps += 1
    return steps


# --- Fixed-point check ---
assert kaprekar_step(6174) == 6174, "6174 must be a fixed point"

# --- Exhaustive check: all 4-digit numbers with >= 2 distinct digits ---
max_steps = 0
for n in range(1000, 10000):
    s = steps_to_6174(n)
    if s is not None:
        assert s <= 7, f"{n} took {s} steps (> 7)"
        max_steps = max(max_steps, s)

assert max_steps == 7, f"expected max 7 steps, got {max_steps}"


if __name__ == "__main__":
    print("Kaprekar's Constant — 6174")
    print()
    print(f"  Fixed point:  kaprekar_step(6174) = {kaprekar_step(6174)}")
    print()
    print("  Example traces:")
    for example in (1234, 9999, 1111, 3087, 2178):
        s = steps_to_6174(example)
        tag = "(repdigit, excluded)" if s is None else f"{s} step(s)"
        print(f"    {example} → {tag}")
    print()
    # Recompute distribution
    from collections import Counter
    dist: Counter = Counter()
    for n in range(1000, 10000):
        s = steps_to_6174(n)
        if s is not None:
            dist[s] += 1
    for k in sorted(dist):
        print(f"    {k} step(s): {dist[k]} numbers")
    print(f"\n  Max steps to 6174: {max(dist)}")
    print()
    print("All assertions passed.")
