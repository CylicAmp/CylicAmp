# CLASS: AUDIT
"""
The pasted "Comprehensive Mathematical Corpus: Axiomatic Model and Integrated Framework" (owner_work #432,
2026-10-24): axioms I-V, Lemma 1 (+6 = -3), Lemma 2 (123453 and 378921 repeated), Theorem 1 (the 4 x 5 lattice
35..54, pairs to 89), Theorem 2 (the 9 x 9 "Delta 99" matrix, eigenvalues in pairs to 1010 around 505), the S3 / S4
words, the 1-5-9 split, the 30-step wave, and the zeros gamma_6 .. gamma_11. Audit on arrival.

THE PASTE: text from another tool, relayed by the owner. It closes "This synthesis brings together your axioms,
proofs, matrix operators ..."; nothing below puts a claim of it in the owner's mouth. The same message asks for the
walk to 1,000,000: re-run, it gives the numbers of owner_work #418 again (333,334 predicted, 14,871 pairs, 0 missed;
dashboards/owner_engine/check_owner_engine.py).

RIGHT (re-run), every number:
  the root operator C(n) = 1 + (n - 1 by 9); C of a sum and of a product follow the roots; {3, 6, 9} and
    {1, 2, 4, 5, 7, 8}; anything times a multiple of 3 is a multiple of 3; 3 x 3, 3 x 6, 3 x 9 -> 9
  a matrix with Q M Q^-1 = -M has its eigenvalues in +/- pairs; with an odd size, 0 is one of them
  Lemma 1: +6 is -3 by 9; 3 -> 6 -> 9 -> 3 and 6 -> 3 -> 9 -> 6
  Lemma 2: 123 + 453 = 576 -> 21 by 37; 378 + 921 = 1299 -> 4; repeated k times -> 21k and 4k (10^6 -> 1);
    digit totals 18 and 30, so the pair adds to 48k -> 3k by 9; both 37 | and root 9 first at k = 111 = 3 x 37
  Theorem 1: 35 + 5r + c over r = 0..3, c = 0..4 is 35..54; every cell plus its opposite = 89 -> 17 -> 8;
    the 20 cells add to 890 -> 8
  Theorem 2: diagonal 109 208 307 406 505 604 703 802 901, neighbours 99: the eigenvalues come in pairs adding to
    1010, 505 is one of them, and the gaps read the same both ways (computed below to 1e-9)
  S3 of 3 5 7 -> 15 -> 6; S3 of 1 2 4 -> 7; S4 of 2 3 5 7: 24 words, -> 17 -> 8; the period of the Fibonacci
    numbers by 9 is 24
  1 2 3 / 4 5 6 / 7 8 9: the diagonal 1 5 9 -> 15 -> 6, above it 2 3 6 -> 11 -> 2, below it 4 7 8 -> 19 -> 1;
    1 + 2 + 6 = 9
  F12 = 144 -> 9; flipping 191 inside out gives 919
  the zeros: gamma_6 .. gamma_11 = 37.586178, 40.918719, 43.327073, 48.005151, 49.773832, 52.970321 (the repo's
    zero table), nearest whole numbers 38 41 43 48 50 53, distances 0.413822 0.081281 0.327073 0.005151 0.226168
    0.029679, roots 2 5 7 3 5 8; 3 + 5 = 8; 48 and 41 are opposite cells of the lattice (48 + 41 = 89);
    48 + 50 = 98 -> 8
  N(T) = T/2pi ln(T/2pi) - T/2pi + O(ln T) is the count of zeros up to height T (the error O(ln T) covers S(T))

THE ONE CHECK LEFT: "the 30-step palindromic wave ... the global cycle sum = 144" -- the 30 states are not listed
  (only 121, 919, 555, 212 ... 989), so the sum 144 needs them. Can I get the 30 states?

TIED TO THE OWNER'S WORK:
  the diagonal of Theorem 2 is 109 and its flips: 109 <-> 901, 208 <-> 802, 307 <-> 703, 406 <-> 604, 505 <-> 505;
    each entry and its flip add to 1010, and each is a pair to 10 with a 0 between (1|0|9, 2|0|8, ...), root 1 --
    the pairs to 10 of #426 and the flips of #358. The eigenvalue pairs to 1010 are the same pairs.
    109 is the step of the pasted 891 -> 128 rows (#401); 901 - 109 = 792 = 8 x 99, a flip moves by 9s.
  Lemma 1's +6 = -3 is the same rule as adding 8 takes 1 off (#400) and taking 4 adds 5 (#415).
  Lemma 2's 10^3 -> 1 by 37 is 1000 = 27 x 37 + 1, behind "37 brings 111" (#390).
  the S3 words are those of #422 (pasted_s3_permutations_123_audit_2026_10_23.py).

FALSIFICATION: any assertion failing.
"""
import json
import pathlib
from itertools import permutations

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]


def C(n):
    return 1 + (n - 1) % 9


def root(m):
    while m > 9:
        m = sum(map(int, str(m)))
    return m


# axioms
assert all(C(n) == root(n) for n in range(1, 5000))
assert all(C(a + b) == C(C(a) + C(b)) and C(a * b) == C(C(a) * C(b)) for a in range(1, 80) for b in range(1, 80))
assert all(C(x * y) in (3, 6, 9) for x in (3, 6, 9) for y in range(1, 10)) and all(C(3 * x) == 9 for x in (3, 6, 9))
assert all(C(x * k) == 9 for x in (3, 6, 9) for k in (3, 6, 9))

# Lemma 1
assert (6 + 3) % 9 == 0
seq3, seq6 = [3], [6]
for _ in range(3):
    seq3.append(C(seq3[-1] + 3))
    seq6.append(C(seq6[-1] + 6))
assert seq3 == [3, 6, 9, 3] and seq6 == [6, 3, 9, 6]

# Lemma 2
A, B = 123453, 378921
assert (123 + 453, 576 % 37, 378 + 921, 1299 % 37) == (576, 21, 1299, 4)
assert all(int(str(A) * k) % 37 == 21 * k % 37 and int(str(B) * k) % 37 == 4 * k % 37 for k in range(1, 60))
assert sum(map(int, str(A))) == 18 and sum(map(int, str(B))) == 30
first = next(k for k in range(1, 500) if int(str(A) * k) % 37 == 0 and int(str(B) * k) % 37 == 0
             and C(int(str(A) * k) + int(str(B) * k)) == 9)
assert first == 111 == 3 * 37

# Theorem 1
L = [[35 + 5 * r + c for c in range(5)] for r in range(4)]
assert sorted(v for row in L for v in row) == list(range(35, 55))
assert all(L[r][c] + L[3 - r][4 - c] == 89 for r in range(4) for c in range(5)) and C(89) == 8
assert sum(map(sum, L)) == 890 and C(890) == 8

# Theorem 2
H = np.zeros((9, 9))
for i in range(9):
    H[i, i] = 109 + 99 * i
for i in range(8):
    H[i, i + 1] = H[i + 1, i] = 99
lam = np.sort(np.linalg.eigvalsh(H))
assert all(abs(lam[j] + lam[8 - j] - 1010) < 1e-9 for j in range(9)) and abs(lam[4] - 505) < 1e-9
gaps = np.diff(lam)
assert all(abs(gaps[j] - gaps[7 - j]) < 1e-9 for j in range(8))
R = np.fliplr(np.eye(9))
D = np.diag([(-1) ** i for i in range(9)])
Q = D @ R
M = H - 505 * np.eye(9)
assert np.allclose(Q @ M @ np.linalg.inv(Q), -M)
diag = [int(H[i, i]) for i in range(9)]
assert diag == [109, 208, 307, 406, 505, 604, 703, 802, 901]
assert all(int(str(d)[::-1]) == diag[8 - i] and d + diag[8 - i] == 1010 for i, d in enumerate(diag))
assert all(root(d) == 1 and int(str(d)[0]) + int(str(d)[2]) == 10 and str(d)[1] == "0" for d in diag)
assert 901 - 109 == 792 == 8 * 99

# S3, S4, 1-5-9
for digits, r in (("357", 6), ("124", 7)):
    words = ["".join(p) for p in permutations(digits)]
    assert len(words) == 6 and all(C(int(w)) == r for w in words)
w4 = ["".join(p) for p in permutations("2357")]
assert len(w4) == 24 and all(C(int(w)) == 8 for w in w4)
f, pis = (0, 1), 0
while True:
    f = (f[1], (f[0] + f[1]) % 9)
    pis += 1
    if f == (0, 1):
        break
assert pis == 24
assert (C(1 + 5 + 9), C(2 + 3 + 6), C(4 + 7 + 8)) == (6, 2, 1) and 1 + 2 + 6 == 9
assert sorted([1, 5, 9] + [2, 3, 6] + [4, 7, 8]) == list(range(1, 10))

# the wave pieces that are given
fib = [0, 1]
while len(fib) < 13:
    fib.append(fib[-1] + fib[-2])
assert fib[12] == 144 and C(144) == 9
assert "191"[1] + "191"[0] + "191"[1] == "919"

# the zeros
zeros = json.loads((ROOT / "math" / "lemmas" / "data" / "zeta_zeros_gamma_1_1000.json").read_text())
g = zeros[5:11]
assert [round(x, 6) for x in g] == [37.586178, 40.918719, 43.327073, 48.005151, 49.773832, 52.970321]
near = [round(x) for x in g]
assert near == [38, 41, 43, 48, 50, 53]
assert [round(abs(x - n), 6) for x, n in zip(g, near)] == [0.413822, 0.081281, 0.327073, 0.005151, 0.226168, 0.029679]
assert [C(n) for n in near] == [2, 5, 7, 3, 5, 8] and C(48) + C(50) == C(53)
assert L[2][3] == 48 and L[1][1] == 41 and 48 + 41 == 89 and C(48 + 50) == 8

if __name__ == "__main__":
    print("#432 corpus: every number right (Lemma 2 first at k = 111; lattice pairs 89; eigenvalues pair to 1010 "
          "around 505; zeros 48 50 53 roots 3 + 5 = 8); the 30 wave states are needed for its 144; the diagonal "
          "109 ... 901 is 109 and its flips, each a pair to 10")
