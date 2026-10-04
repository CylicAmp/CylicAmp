# CLASS: AUDIT
"""
Audit of supplied blocks (2026-10-04): the "fixed universal grip" for asymmetric pairs, and
three "disproof attempts". (The repeated acknowledgement block restates
rotation_3223_and_82_boundary_supplied_audit_2026_10_04.py correctly.) Mathematics only.

"FIXED UNIVERSAL GRIP" -- the bug it fixes does not exist
  F1 Its premise: for an asymmetric pair the forward root (23) and reverse root (32) are
     "structurally different" and must be tracked separately. A number and its reversal have
     the same digits, hence the same digital root, for EVERY pair -- checked for all 81. So
     root_forward and root_reverse are always the same number and the "fix" changes nothing
     about the anchors.
  F2 What it does change: the right half is no longer the mirror of the left, so the 8x8 loses
     the left-right palindrome symmetry every earlier grid had (row 1 for 2-3 becomes
     5 2 3 5 5 3 2 5 -> palindrome only by accident; row 2 becomes 2 1 2 2 3 1 3 3, not one).

DISPROOF TESTS
  T1 CORRECT (forced): 1 x 99,999,999 = 3 x 33,333,333 = 9 x 11,111,111 = 99,999,999; 8 x 9 = 72
     is the largest digit sum 8 digits can have; +1 gives 8 carries.
  T2 CORRECT result, sharper reason: in a cyclic stack row i is the base row p shifted by i, so
     entry (i, j) = p[(i + j) mod 4]. The anti-diagonal has i + j = 3 throughout, so it is
     4 x p[3] -- four copies of the LAST entry: 8 or 12, never 10, for any 2s-and-3s row.
     The main diagonal is p0, p2, p0, p2 = 2(p0 + p2): 10 only when p0 != p2. So "rows, columns
     AND main diagonals sum to 10" holds for 3223 and 2332 but fails for 2323 and 3232 (main
     diagonal 8 and 12).
  T3 NOT A TEST: "changing a node count would throw a symmetry error" was never run. The mod-5
     counts are a property of the seed rule; a different seed rule gives different counts.
  T4 "The system cannot be disproved": T1 and T2 are forced arithmetic (they cannot fail), and
     T3 did not run, so nothing here was put at risk.
NOT IN THE REPOSITORY: t325_fixed_universal_grip_2026_10_04.py was run locally only.
FALSIFICATION: any assertion failing.
"""
import itertools

dr = lambda n: 9 if n % 9 == 0 else n % 9
assert all(dr(int(f"{a}{b}")) == dr(int(f"{b}{a}")) for a in range(1, 10) for b in range(1, 10))  # F1


def fixed(d1, d2):                                         # the supplied "fix", verbatim logic
    f, r = dr(int(f"{d1}{d2}")), dr(int(f"{d2}{d1}"))
    L = [[f, d1, d2, f], [d1, 1, d1, d1], [d1, d1, 1, d1], [d2, d2, d1, r]]
    R = [[r, d2, d1, f], [d2, 1, d2, d2], [d2, d2, 1, d2], [d1, d1, d2, f]]
    top = [L[i] + R[i] for i in range(4)]
    return top + top[::-1]


g = fixed(2, 3)
assert g[0] == [5, 2, 3, 5, 5, 3, 2, 5] and g[1] == [2, 1, 2, 2, 3, 1, 3, 3]              # F2
assert g[1] != g[1][::-1]

assert 1 * 99_999_999 == 3 * 33_333_333 == 9 * 11_111_111 == 99_999_999 and 8 * 9 == 72   # T1
for p in set(itertools.permutations([2, 2, 3, 3])):                                        # T2
    m = [list(p[k:] + p[:k]) for k in range(4)]
    assert all(m[i][j] == p[(i + j) % 4] for i in range(4) for j in range(4))
    assert sum(m[i][3 - i] for i in range(4)) == 4 * p[3] in (8, 12)
    assert sum(m[i][i] for i in range(4)) == 2 * (p[0] + p[2])
assert 2 * (2 + 2) == 8 and 2 * (3 + 3) == 12          # 2323, 3232: main diagonal not 10
