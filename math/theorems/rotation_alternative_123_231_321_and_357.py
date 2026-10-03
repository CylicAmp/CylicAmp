# CLASS: COMPUTATION
"""
The owner's rotation stacks of 2026-10-03, against the filed rotation work.
Author: Michael Warren Song (CyclicAmp)

    A (filed: T325)     B (new: the alternative)     C (new)
    123                 123                          357
    312                 231                          573
    231                 321                          735
    123                 123                          357

=== A IS ALREADY FILED ===
theorem_325_rotation_walk_shapes_gf37.py: 123 -> 312 -> 231 -> 123, each step the
rotation abc -> cab (last digit to the front). A cyclic Latin square: every digit once in
every row and column; column sums 6, 6, 6; total 666 = 18 x 37.

=== B: THE ALTERNATIVE -- THREE DIFFERENT MOVES, NOT ONE ===
    123 -> 231   rotation the OTHER way (abc -> bca, first digit to the back)
    231 -> 321   swap the first two digits
    321 -> 123   reversal
It closes (back to 123) like A, but by three different moves instead of one move three
times. What changes:
  - It visits BOTH rotation classes. 123 and 231 are rotations of each other; 321 is not a
    rotation of 123 -- it is in the other class {321, 213, 132}. A never leaves its class.
    The way back from 321 is reversal, the move T325 identified as the bridge between the
    two classes (123 <-> 321, 312 <-> 213, 231 <-> 132).
  - It is NOT a Latin square: column 2 reads 2, 3, 2 and column 3 reads 3, 1, 1.
  - Column sums 6, 7, 5 (A: 6, 6, 6); total 675 = 27 x 25, not a multiple of 37
    (A: 666 = 18 x 37). Mod 37 the rows are 12, 9, 25 (A: 12, 16, 9).
  - As moves on the three positions: rotation (order 3), swap (order 2), reversal (order 2);
    composed in order they give the identity, which is why the walk closes.

=== C: 357 / 573 / 735 ===
Rotations of 357, stepping abc -> bca -- the direction of B's first step, opposite to A.
  - Latin square; column sums 15, 15, 15; total 1665 = 45 x 37.
  - 357 is the arithmetic progression 3, 5, 7 (step 2). By T326 (theorem_326_all_roads_ap_
    triples_gf37.py) every step-2 triple is 24 mod 37, and 357 = 246 + 111 with
    111 = 3 x 37: 357 sits on the same residue as 246.
  - Its rotations are 24, 18, 32 mod 37 = {18, 24, 32}, the seed-246 orbit. Forced: a
    rotation of a 3-digit number multiplies its residue by 10 (999 = 27 x 37, T403
    cyclic_permutation_coset.py), and {24, 24*10, 24*100} mod 37 = {24, 18, 32}.
  - 357 = 3*7*17, 573 = 3*191, 735 = 3*5*7^2: all divisible by 3 (digit sum 15).
FALSIFICATION: any assertion failing.
"""
from sympy import factorint

rot_back = lambda s: s[-1] + s[:-1]        # abc -> cab   (A)
rot_fwd = lambda s: s[1:] + s[0]           # abc -> bca   (B step 1, C)
swap12 = lambda s: s[1] + s[0] + s[2]
rev = lambda s: s[::-1]

A = ["123"]
for _ in range(3):
    A.append(rot_back(A[-1]))
assert A == ["123", "312", "231", "123"]

B = ["123", rot_fwd("123")]
B.append(swap12(B[-1]))
B.append(rev(B[-1]))
assert B == ["123", "231", "321", "123"]

C = ["357"]
for _ in range(3):
    C.append(rot_fwd(C[-1]))
assert C == ["357", "573", "735", "357"]


def latin(rows):
    return all(len(set(col)) == 3 for col in zip(*rows)) and all(len(set(r)) == 3 for r in rows)


def colsums(rows):
    return [sum(int(r[i]) for r in rows) for i in range(3)]


rot_class = {"123", "312", "231"}
assert latin(A[:3]) and colsums(A[:3]) == [6, 6, 6] and sum(map(int, A[:3])) == 666 == 18 * 37
assert not latin(B[:3]) and colsums(B[:3]) == [6, 7, 5]
assert sum(map(int, B[:3])) == 675 == 27 * 25 and 675 % 37 != 0
assert set(B[:2]) <= rot_class and B[2] not in rot_class
assert {rev(x) for x in rot_class} == {"321", "213", "132"}
assert [int(x) % 37 for x in A[:3]] == [12, 16, 9] and [int(x) % 37 for x in B[:3]] == [12, 9, 25]

# B's three moves compose to the identity on any 3-letter word
for w in ("123", "abc", "xyz"):
    assert rev(swap12(rot_fwd(w))) == w

assert latin(C[:3]) and colsums(C[:3]) == [15, 15, 15] and sum(map(int, C[:3])) == 1665 == 45 * 37
assert 357 == 111 * 3 + 12 * 2 and 357 - 246 == 111 == 3 * 37
assert [int(x) % 37 for x in C[:3]] == [24, 18, 32] and {24, 24 * 10 % 37, 24 * 100 % 37} == {18, 24, 32}
assert [factorint(int(x)) for x in C[:3]] == [{3: 1, 7: 1, 17: 1}, {3: 1, 191: 1}, {3: 1, 5: 1, 7: 2}]

if __name__ == "__main__":
    print("A (T325):", A, "Latin, 666 = 18*37")
    print("B (new): ", B, "rotate, swap, reverse; not Latin; 675; visits both classes")
    print("C (new): ", C, "Latin, 1665 = 45*37; residues {18,24,32} = seed-246 orbit; 357 = 246 + 111")
