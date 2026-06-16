"""
OddPerfect Zero-Decimal System: Comma Group Parity Analysis

n zeros split by standard thousands-grouping (from right, groups of 3).
Each group carries parity O (odd zero-count) or E (even zero-count).
Classification string interleaves parities with 'C' for comma.

Period-3 cycle on leftmost group size = (n-1) % 3 + 1:
  n ≡ 1 (mod 3) → leftmost = 1 (odd)  → all groups odd → OCO...CO
  n ≡ 2 (mod 3) → leftmost = 2 (even) → ECO...CO
  n ≡ 0 (mod 3) → leftmost = 3 (odd)  → all groups odd → OCO...CO

ECO occurs exactly when n ≡ 2 (mod 3).  All other n are OCO (all groups odd).

Mercenne count connection:
  n zeros → n+1 decimal slot positions → 2^(n+1)-1 placements (Mersenne)
  Digits of 137 = placement counts for n=0,1,2: 1, 3, 7 = 2^1-1, 2^2-1, 2^3-1

The sequence never terminates: n → n+3 appends one more group of 3 (odd),
preserving the parity class (OCO stays OCO, ECO stays ECO).
"""


def comma_groups(n):
    """Group n zeros by standard thousands format (rightmost groups of 3)."""
    if n <= 0:
        return []
    groups = []
    r = n
    while r > 3:
        groups.append(3)
        r -= 3
    groups.append(r)
    return list(reversed(groups))   # leftmost first


def zero_string(n):
    """Display n zeros with standard comma grouping."""
    groups = comma_groups(n)
    return ",".join("0" * g for g in groups)


def parity_class(n):
    """OCO/ECO/... classification string for n zeros."""
    groups = comma_groups(n)
    labels = ["O" if g % 2 == 1 else "E" for g in groups]
    return "C".join(labels)


def is_all_odd(n):
    """True when every group has an odd zero-count (OCO pattern)."""
    return all(g % 2 == 1 for g in comma_groups(n))


def comma_count(n):
    return max(0, len(comma_groups(n)) - 1)


def mersenne_placements(n):
    """Total decimal-slot placements for n zeros: 2^(n+1) - 1."""
    return 2 ** (n + 1) - 1


# ---------------------------------------------------------------------------
# Assertions: period-3 cycle rule
# ---------------------------------------------------------------------------

for n in range(1, 31):
    groups = comma_groups(n)
    leftmost = groups[0]
    if n % 3 == 2:          # ECO cases
        assert leftmost == 2, f"n={n}: expected leftmost=2, got {leftmost}"
        assert not is_all_odd(n), f"n={n}: ECO case should NOT be all-odd"
    else:                   # OCO cases (n%3==0 or 1)
        assert leftmost in (1, 3), f"n={n}: expected leftmost in {{1,3}}, got {leftmost}"
        assert is_all_odd(n), f"n={n}: should be all-odd but isn't"

# Mersenne connection: digits of 137 = placements for n=0,1,2
assert mersenne_placements(0) == 1    # 2^1-1 = 1
assert mersenne_placements(1) == 3    # 2^2-1 = 3
assert mersenne_placements(2) == 7    # 2^3-1 = 7

# n+3 preserves parity class (appends one more group of 3)
for n in range(1, 20):
    assert parity_class(n) == parity_class(n + 3)[: len(parity_class(n))], (
        f"n={n}: parity prefix not preserved after +3"
    )


# ---------------------------------------------------------------------------
# Enumeration: n = 1 .. 15
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("OddPerfect Zero-Decimal System")
    print("=" * 62)
    print(f"{'n':>3}  {'zeros':>18}  {'groups':<14}  {'class':<10}  {'#commas':>7}  {'all-odd':>7}")
    print("-" * 62)
    for n in range(1, 16):
        gs = comma_groups(n)
        zs = zero_string(n)
        pc = parity_class(n)
        nc = comma_count(n)
        ao = "OCO" if is_all_odd(n) else "ECO"
        print(f"{n:>3}  {zs:>18}  {str(gs):<14}  {pc:<10}  {nc:>7}  {ao:>7}")

    print()
    print("Period-3 rule: ECO iff n ≡ 2 (mod 3)")
    eco = [n for n in range(1, 31) if not is_all_odd(n)]
    oco = [n for n in range(1, 31) if is_all_odd(n)]
    print(f"ECO n in [1..30]: {eco}")
    print(f"OCO n in [1..30]: {oco}")

    print()
    print("Mersenne placement counts (2^(n+1)-1):")
    for n in range(6):
        print(f"  n={n}: {mersenne_placements(n)} placements")
    print("Digits of 137 = mersenne_placements(0,1,2) = 1, 3, 7")

    print()
    print("n+3 extension (OCO stays OCO, ECO stays ECO):")
    for n in [4, 5, 6, 7, 8, 9]:
        print(f"  n={n} → {parity_class(n):8s}  |  n+3={n+3} → {parity_class(n+3):10s}")

    print()
    print("All assertions passed.")
