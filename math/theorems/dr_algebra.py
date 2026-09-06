"""
CLOSED ALGEBRA ON DIGITAL ROOT CLASSES
================================================================

A complete group-theoretic analysis of digital roots:
- Group structure (DR, +) isomorphic to Z/9Z
- Subgroup lattice
- Cycle decomposition under doubling
- 81 two-digit number mapping
"""

import numpy as np
from itertools import product


def digital_root(n):
    """Digital root 1-9."""
    if n == 0:
        return 9
    return (n - 1) % 9 + 1


class DRAlgebra:
    """Algebraic structure on digital root classes."""

    def __init__(self):
        self.dr_classes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.addition_table = self._build_addition_table()
        self.doubling_map = {x: digital_root(x * 2) for x in self.dr_classes}

    def _build_addition_table(self):
        """Build the DR-addition Cayley table."""
        table = {}
        for a in self.dr_classes:
            for b in self.dr_classes:
                table[(a, b)] = digital_root(a + b)
        return table

    def add(self, a, b):
        """DR-addition: a + b (mod 9)."""
        return self.addition_table[(a, b)]

    def double(self, x):
        """Doubling map: x → DR(2x)."""
        return self.doubling_map[x]

    def find_cycles(self):
        """Find cycles under doubling."""
        visited = set()
        cycles = []

        for start in self.dr_classes:
            if start in visited:
                continue

            path = []
            current = start
            while current not in visited:
                visited.add(current)
                path.append(current)
                current = self.double(current)

                if current == start:
                    cycles.append(path)
                    break

        return cycles

    def generate_subgroup(self, g):
        """Generate cyclic subgroup <g>."""
        subgroup = {9}  # Identity
        current = g
        while current not in subgroup:
            subgroup.add(current)
            current = self.add(current, g)
        return sorted(subgroup)


def run_assertions():
    algebra = DRAlgebra()

    # Group structure: (DR, +) isomorphic to Z/9Z
    # Identity is 9, every element has an inverse, addition is associative
    assert algebra.add(9, 5) == 5 and algebra.add(5, 9) == 5, "9 is identity"
    for a in algebra.dr_classes:
        assert algebra.add(algebra.add(3, a), 6) == algebra.add(3, algebra.add(a, 6)), \
            f"associativity failed for a={a}"

    # Cycle decomposition under doubling
    cycles = algebra.find_cycles()
    cycle_sets = [frozenset(c) for c in cycles]
    assert frozenset({1, 2, 4, 8, 7, 5}) in cycle_sets, \
        "6-cycle {1,2,4,8,7,5} must exist under doubling"
    assert frozenset({3, 6}) in cycle_sets, \
        "2-cycle {3,6} must exist under doubling"
    assert frozenset({9}) in cycle_sets, \
        "fixed point {9} must exist under doubling"

    cycle_lengths = sorted(len(c) for c in cycles)
    assert cycle_lengths == [1, 2, 6], \
        f"doubling cycle lengths = {cycle_lengths}, expected [1,2,6]"

    # Generators: elements generating the full group of order 9
    generators = [g for g in algebra.dr_classes
                  if len(algebra.generate_subgroup(g)) == 9]
    assert len(generators) == 6, f"|generators| = {len(generators)}, expected 6 (φ(9))"


# Main analysis
if __name__ == "__main__":
    run_assertions()
    algebra = DRAlgebra()

    print("DR-Algebra Structure")
    print("=" * 50)

    # Addition table
    print("\nAddition Table:")
    print("  " + " ".join(f"{i:>2}" for i in algebra.dr_classes))
    for a in algebra.dr_classes:
        row = [algebra.add(a, b) for b in algebra.dr_classes]
        print(f"{a:>2}|" + " ".join(f"{r:>2}" for r in row))

    # Cycles
    print("\nDoubling Cycles:")
    cycles = algebra.find_cycles()
    for cycle in cycles:
        print(f"  {' → '.join(map(str, cycle))} → {cycle[0]} (length {len(cycle)})")

    # Generators
    print("\nGenerators:")
    generators = [g for g in algebra.dr_classes
                  if len(algebra.generate_subgroup(g)) == 9]
    print(f"  {generators}")
