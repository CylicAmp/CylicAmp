# math/theorems/mirror_set_generator.py
"""
Mirror Set Generator — 9-Invariant Permutation Theorem

THEOREM: For any integer n ≡ 0 (mod 9), every digit permutation of n
also ≡ 0 (mod 9), i.e. has digital root 9.

PROOF: Digit sum is invariant under permutation. Since DR(n) ≡ n (mod 9)
(dr_modular_foundation.py, Theorem 1), and permuting digits preserves
the digit sum, the DR class is preserved across the entire mirror set.

Classification: Theorem
"""

from itertools import permutations
from typing import List


class MirrorSetGenerator:
    @staticmethod
    def get_invariant_permutations(n: int) -> List[int]:
        """
        Generate all unique digit permutations of n.
        Verifies that every permutation maintains the 9-Invariant.
        """
        digits = list(str(abs(n)))
        unique_perms = sorted(set(int("".join(p)) for p in permutations(digits)))

        for p in unique_perms:
            root = 1 + (p - 1) % 9 if p != 0 else 0
            if root != 9 and n % 9 == 0:
                raise ArithmeticError(f"Phase Shift detected in permutation {p}")

        return unique_perms


# --- Assertions ---

# 198 = abs(143 - 341); digit sum = 1+9+8 = 18 → DR = 9
assert 198 % 9 == 0
mirror_198 = MirrorSetGenerator.get_invariant_permutations(198)
assert set(mirror_198) == {189, 198, 819, 891, 918, 981}
assert len(mirror_198) == 6
assert all(p % 9 == 0 for p in mirror_198)

# 198-orbit mod 37 forensic audit
# Residue set {3,4,5,13,19,30} — all six are framework landmarks:
#   3=TRINITY, 4=sovereign anchor, 5=PIVOT/G'5 void,
#   13=GATE_13, 19=CENTER_19, 30=sovereign fixed point
_orbit_residues = {n % 37 for n in mirror_198}
assert _orbit_residues == {3, 4, 5, 13, 19, 30}
assert len(_orbit_residues) == 6                    # all distinct
assert 198 % 37 == 13                               # GATE_13
assert 891 % 37 == 3                                # TRINITY (sovereign target)
assert 918 % 37 == 30                               # sovereign fixed point
assert 819 % 37 == 5                                # PIVOT_PRIME / G'5 void marker
assert 189 % 37 == 4                                # sovereign anchor
assert 981 % 37 == 19                               # CENTER_19

# Broader invariant: any multiple of 9 produces a mirror set of multiples of 9
for base in [9, 18, 27, 36, 45, 99, 108, 117, 126, 135, 144, 162, 189, 198, 234, 279]:
    perms = MirrorSetGenerator.get_invariant_permutations(base)
    assert all(p % 9 == 0 for p in perms), f"Invariant failed for base={base}"

# Non-multiples of 9: DR class is still preserved (just not DR=9)
for base in [100, 137, 191, 232]:
    perms = MirrorSetGenerator.get_invariant_permutations(base)
    expected_dr = 1 + (base - 1) % 9
    for p in perms:
        if p == 0:
            continue
        assert 1 + (p - 1) % 9 == expected_dr, f"DR class broken for base={base}, perm={p}"


if __name__ == "__main__":
    source_val = 198  # abs(143 - 341)
    mirror_set = MirrorSetGenerator.get_invariant_permutations(source_val)

    print(f"Source: {source_val} (DR=9, Root 9)")
    print(f"Verified Mirror Set: {mirror_set}")
    print(f"Total Unique Paths: {len(mirror_set)}")
    print()

    # Show DR class preservation for non-9 examples
    for val in [137, 191, 232]:
        perms = MirrorSetGenerator.get_invariant_permutations(val)
        dr = 1 + (val - 1) % 9
        print(f"  {val} (DR={dr}): {perms}")

    print()
    print("All assertions passed.")
