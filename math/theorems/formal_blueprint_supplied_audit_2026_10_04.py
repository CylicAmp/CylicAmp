# CLASS: AUDIT
"""
Audit of supplied text (2026-10-04): "The Official Architectural Blueprint" -- formal names for
the owner's operations, the 82 boundary, and the 3223 matrix, with a validation script.
Mathematics only.

CORRECT
  B1 Casting out nines = arithmetic mod 9; casting out fives = mod 5 (Z/5Z, cyclic of order 5);
     draining = carrying in base 10.
  B2 Carry counts by T432's identity c = (s(A) + s(B) - s(A+B)) / 9: 81+1 -> 0, 89+1 -> 1,
     99+1 -> 2. 3223 stack: rows and columns 10, main diagonal 10, anti-diagonal 12.
     The supplied script runs and its assertions hold.

WRONG NAMES (each one would mislead a reader who looked it up)
  B3 "Circulant matrix": a circulant shifts each row one place RIGHT, c_ij = p[(j - i) mod n];
     with first row 3223 it is 3223 / 3322 / 2332 / 2233. The owner's stack shifts LEFT,
     c_ij = p[(i + j) mod n] -- a LEFT circulant (a symmetric Hankel matrix): 3223 / 2233 /
     2332 / 3322, which is symmetric (c_ij = c_ji); a circulant generally is not.
  B4 "Dihedral group D4" for mirroring: one mirror is a reflection of order 2; the left-right and
     top-bottom mirrors together generate Z2 x Z2 (order 4, the Klein group), not D4 (order 8,
     which needs the quarter turns and the diagonal mirrors too).
  B5 "Finite field of pairs {1..9} x {1..9}": that is a set of 81 pairs, not a field.
  B6 "Kummer's Congruence Theorem": Kummer's congruences are about Bernoulli numbers. The carry
     count is Kummer's THEOREM on binomial coefficients (carries in base p), i.e. the digit-sum
     identity filed as T432.
  B7 "R_10" for base-10 radix arithmetic: R conventionally denotes the real numbers.
NOT IN THE REPOSITORY: t325_formal_blueprint_core.py was run locally only.
FALSIFICATION: any assertion failing.
"""
s = lambda n: sum(map(int, str(n)))
carries = lambda a, b: (s(a) + s(b) - s(a + b)) // 9
assert (carries(81, 1), carries(89, 1), carries(99, 1)) == (0, 1, 2)                   # B2

p = [3, 2, 2, 3]
left = [[p[(i + j) % 4] for j in range(4)] for i in range(4)]
circ = [[p[(j - i) % 4] for j in range(4)] for i in range(4)]
assert left == [[3, 2, 2, 3], [2, 2, 3, 3], [2, 3, 3, 2], [3, 3, 2, 2]]                  # the owner's stack
assert {sum(r) for r in left} == {10} == {sum(c) for c in zip(*left)}
assert sum(left[i][i] for i in range(4)) == 10 and sum(left[i][3 - i] for i in range(4)) == 12
assert circ == [[3, 2, 2, 3], [3, 3, 2, 2], [2, 3, 3, 2], [2, 2, 3, 3]] and circ != left  # B3
assert all(left[i][j] == left[j][i] for i in range(4) for j in range(4))
q = [1, 2, 3, 4]
assert any(q[(j - i) % 4] != q[(i - j) % 4] for i in range(4) for j in range(4))       # circulants need not be symmetric

# B4: left-right flip L and top-bottom flip T on an n x n index grid generate a group of order 4
n = 4
L = lambda ij: (ij[0], n - 1 - ij[1])
T = lambda ij: (n - 1 - ij[0], ij[1])
cells = [(i, j) for i in range(n) for j in range(n)]
maps = {tuple(cells)}
frontier = [tuple(cells)]
while frontier:
    cur = frontier.pop()
    for g in (L, T):
        nxt = tuple(g(c) for c in cur)
        if nxt not in maps:
            maps.add(nxt)
            frontier.append(nxt)
assert len(maps) == 4 != 8
