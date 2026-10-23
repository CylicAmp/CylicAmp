# CLASS: COMPUTATION
"""
The owner's lines of #426 (2026-10-23): pairs that make 10 and so 1, the ones 1 = 11 = 111, "map this to my work",
and the pasted pieces with them (a tool's sum-to-10 / repunit printout, a "Your paths" table, a weak-links script).
Process entry: owner_work/PROCESS.md, #426. The NameError and calculus parts of the same message:
pasted_unified_frame_brun_name_error_audit_2026_10_23.py.

THE OWNER'S LINES, verbatim (#426):
    112(3|1)1|2(31)1
    1234|56|78910-11

    19 = 1, 2+8 = 1, 3+7 = 1, 4+6 = 1, 5+5 = 1 = 11, 111

    map this to my work

CLEANED:
    1 + 9 = 10 -> 1    2 + 8 = 10 -> 1    3 + 7 = 10 -> 1    4 + 6 = 10 -> 1    5 + 5 = 10 -> 1   -> 11 -> 111
    1234 | 56 | 78910 -> 11
    112(3|1)1|2(31)1      (kept as typed)

CHECKED:
    every pair that makes 10 has root 1 -- right (10 = 9 + 1)
    1234 | 56 | 78910:  1+2+3+4 = 10 -> 1;  5+6 = 11 -> 2;  7+8+9+10 = 34 -> 7 (or with the digits 7+8+9+1+0 = 25 -> 7:
      the same root both ways);  all of 1 to 10 = 55 -> 10 -> 1;  then 11
    112(3|1)1|2(31)1: the digits 1 1 2 3 1 1 2 3 1 1 add to 16 -> 7

MAPPED TO THE WORK (each part already has a file):
    pairs to 10 -> root 1: the "+9 changes nothing" rule (framework part 1,
      owner_framework_flips_halves_moves_2026_10_20.py) -- 10 is one more than 9; and T111 Lemma 111.4
      (theorem_111_ascending_descending_gf37.py): 123456789 + 987654321 puts a 10 in every column.
      Next to adding 8 (#400): + 8 takes 1 off, a pair to 10 leaves 1, a pair to 9 leaves 9.
    1, 11, 111: the ones. 111 = 3 x 37 and 10 x 10 + 10 + 1 = 111 (#423, pasted_order6_subgroup_x2x1_audit);
      "37 brings 111" (#390). Their roots go 1 2 3 ... 9 and round again: the root of n ones is n.
    1, 11, 111 read in twos (the tool's line): 1, 3, 7, 15, 31 = 2^n - 1, the Mersenne numbers -- the 7-4-9 triad work
      (#391-#393, owner_749_triad_*): the root of 2^n - 1 runs 1 3 7 6 4 9 and round again (every 6), so a prime
      exponent leaves root 1 when it is one more than a multiple of 6, and root 4 when it is one less -- the triad rule
      (exponent root 1, 4, 7 -> root 1; 2, 5, 8 -> root 4).
    the multiplication pairs to root 1 (1 x 1, 2 x 5, 4 x 7, 8 x 8): the doubling and halving chain (#382): 5 is the
      half of 2 (2 x 5 = 10 -> 1), 7 the half of 4 (4 x 7 = 28 -> 1), 8 its own (8 x 8 = 64 -> 1).

THE PASTED PIECES, re-run: the sum-to-10 list, the repunit roots (root of n ones = n, every 9), the binary list
  (2^n - 1) and the "Your paths" table (5+5, 6+4, 9+1 -> 1; 3 x 3 = 9; 3 + 1 = 4) are right.

THE WEAK-LINKS SCRIPT: run as given, it prints
    M = 10 19 28 | 5 14 0 | 58 8 12     roots 1 1 1 | 5 5 0 | 4 8 3     weak link (1, 2) (the 0)
    C = -9 14 50                        M' = the 0 replaced by 5
  One line does not do what its comment says (it changes a value): the comment says C takes M[i,0] - M[i,1] in every
  row, the code takes M[1,1] - M[1,2] in row 1. By the comment C = -9 -9 50: rows 0 and 1 both step by 9
  (10 -> 19 -> 28, 5 -> 14), the +9 that changes no root. The reconstruction value 5 is right as "the inverse of 2":
  2 x 5 = 10 -> 1 -- the halving rule (halving multiplies the root by 5).

RESIDUES mod 37 (gf37-audit): 19 CAS_EXT, 11 NEG_H, 111 -> 0, 1234 -> 13 CAS_EXT, 56 -> 19 CAS_EXT, 78910 -> 26 IC.

FALSIFICATION: any assertion failing.
"""
import numpy as np


def root(m):
    while m > 9:
        m = sum(map(int, str(m)))
    return m


def dr(n):                       # the script's own
    return 0 if n == 0 else (n - 1) % 9 + 1


pairs = [(1, 9), (2, 8), (3, 7), (4, 6), (5, 5)]
assert all(a + b == 10 and root(a + b) == 1 for a, b in pairs) and root(19) == 1
assert [root(int("1" * k)) for k in range(1, 13)] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3]
assert 1 + 2 + 3 + 4 == 10 and 5 + 6 == 11 and 7 + 8 + 9 + 10 == 34 and 7 + 8 + 9 + 1 + 0 == 25
assert root(34) == root(25) == 7 and sum(range(1, 11)) == 55 and root(55) == 1 and root(12345678910) == 1
assert sum(map(int, "1123112311")) == 16 and root(16) == 7
assert 111 == 3 * 37 == 10 * 10 + 10 + 1
assert [int("1" * k, 2) for k in range(1, 6)] == [1, 3, 7, 15, 31] == [2 ** k - 1 for k in range(1, 6)]
assert [root(2 ** k - 1) for k in range(1, 13)] == [1, 3, 7, 6, 4, 9] * 2
from sympy import primerange  # noqa: E402
for p in primerange(5, 3000):
    assert root(2 ** p - 1) == (1 if p % 6 == 1 else 4)
    assert (root(p) in (1, 4, 7)) == (p % 6 == 1)
assert all(root(a * b) == 1 for a, b in ((1, 1), (2, 5), (4, 7), (8, 8)))
assert (5 + 5, 6 + 4, 9 + 1, 3 * 3, 3 + 1) == (10, 10, 10, 9, 4)

# the weak-links script, as given
V = [10, 19, 28, 5, 14, 0, 58, 8, 12]
M = np.array(V).reshape(3, 3)
drm = np.array([[dr(int(v)) for v in r] for r in M])
assert drm.tolist() == [[1, 1, 1], [5, 5, 0], [4, 8, 3]]
weak = [(i, j) for i in range(3) for j in range(3) if M[i, j] == 0 or dr(int(M[i, j])) == 0]
assert weak == [(1, 2)]
C_code = [M[0, 0] - M[0, 1], M[1, 1] - M[1, 2], M[2, 0] - M[2, 1]]
C_comment = [M[i, 0] - M[i, 1] for i in range(3)]
assert C_code == [-9, 14, 50] and C_comment == [-9, -9, 50]
Mp = M.copy()
Mp[1, 2] = 5
assert Mp.tolist() == [[10, 19, 28], [5, 14, 5], [58, 8, 12]]
assert (2 * 5) % 9 == 1

assert [x % 37 for x in (19, 11, 111, 1234, 56, 78910)] == [19, 11, 0, 13, 19, 26]

if __name__ == "__main__":
    print("#426: pairs to 10 -> 1 right; 1, 11, 111 roots 1 2 3; in twos they are 2^n - 1, the Mersenne numbers of the "
          "7-4-9 triad; weak-links script runs, but row 1 of C uses columns 1, 2 (14) where its comment says 0, 1 (-9)")
