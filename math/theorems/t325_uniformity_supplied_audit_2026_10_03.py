# CLASS: AUDIT
"""
Audit of supplied text (2026-10-03): "The Law of T325 Geometric Uniformity" -- over all
6^3 = 216 stacks of three rows (each a permutation of 1,2,3), the three digits draw the
same figure (column-shifted) iff consecutive rows are cyclic shifts; counts 54 / 54 / 0 / 162.
Mathematics only.

CORRECT
  U1 The counts: 54 uniform stacks, all 54 cyclic, 0 non-cyclic uniform, 162 not uniform.
     Reproduced below (the supplied script does not run as pasted: its line-continuation
     backslashes are followed by code on the same line -- a SyntaxError; repaired here
     without changing its logic).
  U2 The statement. It is forced, and shorter than the text makes it:
       the digits' tracks are shifts of one another, c_d(r) = c_1(r) + s_d, for every row r
       <=> each row r is row 0 rotated by the same amount t_r for every digit
       <=> every row is a rotation of row 0.
     So uniform stacks = 6 choices of row 0 x 3 x 3 rotations = 54. T325 already proves the
     forward direction ("each row is a rotation, so the three digits sit at rigid cyclic
     offsets"); what this adds is the converse and the count.
  U3 231 -> 321 swaps the first two positions; digit 1 stays in column 2. Correct.

WRONG
  U4 "The swapped elements (digits 2 and 3) experience an isolated directional bounce,
     forcing the zigzag." Only digit 2 zigzags. Digit 3 draws the CLEAN diagonal in
     123/231/321 (columns 2, 1, 0) and the clean chevron, diamond and X in every walk
     (rotation_shapes_new_stacks_2026_10_03.py). The notch of digit 1 also starts BEFORE
     the swap: the first step (123 -> 231, a rotation) moves digit 1 from column 0 to 2.
FALSIFICATION: any assertion failing.
"""
import itertools

PERMS = list(itertools.permutations((1, 2, 3)))


def cols(stack, d):
    return [row.index(d) for row in stack]


def shifted(a, b):
    return any(all((x + s) % 3 == y for x, y in zip(a, b)) for s in range(3))


def is_cyclic_shift(r1, r2):          # the supplied predicate, repaired syntax
    return ((r2[0] == r1[1] and r2[1] == r1[2] and r2[2] == r1[0]) or
            (r2[0] == r1[2] and r2[1] == r1[0] and r2[2] == r1[1]) or r1 == r2)


uni = cyc_uni = noncyc_uni = broken = 0
for stack in itertools.product(PERMS, repeat=3):
    u = shifted(cols(stack, 1), cols(stack, 2)) and shifted(cols(stack, 1), cols(stack, 3))
    c = is_cyclic_shift(stack[0], stack[1]) and is_cyclic_shift(stack[1], stack[2])
    rot0 = {stack[0][k:] + stack[0][:k] for k in range(3)}
    assert u == all(r in rot0 for r in stack) == c                    # U2: three conditions agree
    uni += u; cyc_uni += u and c; noncyc_uni += u and not c; broken += not u
assert (uni, cyc_uni, noncyc_uni, broken) == (54, 54, 0, 162)        # U1
assert 6 * 3 * 3 == 54

B = [(1, 2, 3), (2, 3, 1), (3, 2, 1)]
assert cols(B, 1) == [0, 2, 2] and cols(B, 2) == [1, 0, 1] and cols(B, 3) == [2, 1, 0]   # U3, U4
assert B[2] == (B[1][1], B[1][0], B[1][2])                           # 231 -> 321 swaps positions 0,1

if __name__ == "__main__":
    print(f"uniform {uni} (all cyclic {cyc_uni}), non-cyclic uniform {noncyc_uni}, broken {broken}")
    print("in 123/231/321: digit 3 diagonal", cols(B, 3), "digit 2 zigzag", cols(B, 2), "digit 1 notch", cols(B, 1))
