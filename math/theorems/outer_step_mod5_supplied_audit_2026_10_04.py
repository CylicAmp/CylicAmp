# CLASS: AUDIT
"""
Audit of supplied script and record WAV-010-MOD5 (2026-10-04): digit residues mod 5 along the
loop 12 23 34 45 56 67 78 89 91 12. Mathematics only.

CORRECT
  M1 Left residues 1 2 3 4 0 1 2 3 4 1 (sum 21); right 2 3 4 0 1 2 3 4 1 2 (sum 22). The script
     runs and its assertions hold.
CORRECTED
  M2 "Constant net variance -1": as with the parity record, the ten listed nodes count 12 twice.
     Over the 9-node loop the two residue sums are 20 and 20 -- difference 0.
  M3 "Unbroken cyclic progression": each column steps +1 mod 5 except at the 9 -> 1 wrap
     (residue 4 -> 1 on the left at 91 -> 12, on the right at 89 -> 91).
FALSIFICATION: any assertion failing.
"""
seq = [12, 23, 34, 45, 56, 67, 78, 89, 91, 12]
L = [x // 10 % 5 for x in seq]
R = [x % 10 % 5 for x in seq]
assert L == [1, 2, 3, 4, 0, 1, 2, 3, 4, 1] and R == [2, 3, 4, 0, 1, 2, 3, 4, 1, 2]       # M1
assert (sum(L), sum(R)) == (21, 22)
assert (sum(L[:9]), sum(R[:9])) == (20, 20)                                              # M2
stepsL = [(b - a) % 5 for a, b in zip(L, L[1:])]
stepsR = [(b - a) % 5 for a, b in zip(R, R[1:])]
assert [i for i, s in enumerate(stepsL) if s != 1] == [8] and [i for i, s in enumerate(stepsR) if s != 1] == [7]  # M3
