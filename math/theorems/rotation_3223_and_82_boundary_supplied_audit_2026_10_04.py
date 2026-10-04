# CLASS: AUDIT
"""
Audit of supplied text (2026-10-04): the 3223 / 2332 rotation grids with "every one of the 8
directions sums to 10", and the "81 -> 82 -> 10 master flush". Mathematics only.

CORRECT
  R1 Rows and columns of both rotation stacks sum to 10 (forced: each row is a rotation; each
     column holds every entry once). Main diagonals: 3+2+3+2 = 10 and 2+3+2+3 = 10.
  R2 9 x 9 = 81; 81 + 1 = 82; 8 + 2 = 10; 81 = 0 mod 9, 1 mod 5; 82 = 1 mod 9, 2 mod 5.

WRONG
  R3 "Every directional vector without exception sums to 10": the ANTI-diagonals do not.
     3223 stack (3223 / 2233 / 2332 / 3322): anti-diagonal 3+3+3+3 = 12 (root 3).
     2332 stack (2332 / 3322 / 3223 / 2233): anti-diagonal 2+2+2+2 = 8.
  R4 "At 82 the digits sum to 10, so the machine drains / flushes and logs a 1 in the next
     column": 81 + 1 = 82 has NO carry -- the units digit goes 1 -> 2. A drain in the owner's
     system happens when a column passes 9 (e.g. 89 + 1 = 90, 99 + 1 = 100); a DIGIT SUM of
     10 is not a carry. Kummer (T432): s(81+1) = s(81) + 1 - 9*0 = 10, zero carries.
FALSIFICATION: any assertion failing.
"""
ds = lambda n: sum(map(int, str(n)))


def stack(v):
    return [v[k:] + v[:k] for k in range(4)]


for base, anti in (([3, 2, 2, 3], 12), ([2, 3, 3, 2], 8)):
    m = stack(base)
    assert {sum(r) for r in m} == {10} == {sum(c) for c in zip(*m)}                     # R1
    assert sum(m[i][i] for i in range(4)) == 10
    assert sum(m[i][3 - i] for i in range(4)) == anti != 10                              # R3
assert 9 * 9 == 81 and ds(82) == 10 and (81 % 9, 81 % 5, 82 % 9, 82 % 5) == (0, 1, 1, 2)  # R2
carries = len(str(81)) - len(str(81).rstrip("9"))
assert carries == 0 and ds(82) == ds(81) + 1 - 9 * carries                               # R4
assert ds(90) == ds(89) + 1 - 9 * 1 and ds(100) == ds(99) + 1 - 9 * 2
