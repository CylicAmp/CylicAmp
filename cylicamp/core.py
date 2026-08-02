import itertools
from collections import defaultdict


def digital_root(n):
    """Reduce a non-negative integer to its digital root (0 maps to 0)."""
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


def build_full_lattice(d1, d2, d3, d4):
    """Build a 3x3 lattice of pair-sums from four core digits.

    Every cell is a sum of two inputs; no raw inputs are stored in the lattice.
    Returns (lattice, center) where center = d1+d2+d3+d4.
    """
    row1  = d1 + d2
    row2  = d3 + d4
    col1  = d1 + d3
    col2  = d2 + d4
    diag1 = d1 + d4
    diag2 = d2 + d3
    center = row1 + row2

    lattice = [
        [diag1, row1,  diag2],
        [col1,  diag1, col2],
        [diag2, row2,  diag1],
    ]
    return lattice, center


def generate_all_lattices(digit_set=(0, 1, 2)):
    """Generate every lattice over digit_set^4 and group by digital root of center."""
    groups = defaultdict(list)
    for core in itertools.product(digit_set, repeat=4):
        d1, d2, d3, d4 = core
        lattice, center = build_full_lattice(d1, d2, d3, d4)
        dr = digital_root(center)
        groups[dr].append({
            "core": core,
            "lattice": lattice,
            "center": center,
            "digital_root": dr,
        })
    return groups
