# CLASS: AUDIT
"""
Audit of a supplied script (2026-10-04): parity alternation along the corrected wave
00 11 12 21 22 32 33 ... 77 78 87 88 89 98 99 00, and its projection onto an 8x8 grid with
values (row + col) mod 8. Run here with the same logic. Mathematics only.

RESULTS
  W1 Parity change between neighbours is 1 or 2, never 0: the path is not a strict alternation.
     Inside each stage aa -> a(a+1) -> (a+1)a -> (a+1)(a+1) the changes are 1, 2, 1 (the flip
     changes both digits' parity; stepping on or off a double changes one). The skipped 23
     makes 22 -> 32 a single change.
  W2 The 8x8 grid (row + col) mod 8 has 32 even and 32 odd cells.
  W3 Wave values: 0 2 3 3 4 5 6 7 7 0 1 1 2 3 3 4 5 5 6 7 7 0 1 1 2 0; sum 85, root 4;
     11 even, 15 odd. Forced: a double aa lands on 2a mod 8 (even); every other node has
     digits a, a+1 and lands on 2a + 1 mod 8 (odd).
  W4 Defect in the projection: "digit mod 8" folds 8 -> 0 and 9 -> 1, so 88, 89, 98, 99 land on
     the same cells as 00, 01, 10, 11. The 8x8 grid cannot distinguish the top of the wave from
     its start; any shape read off it for digits 8 and 9 is an artefact of the fold.
FALSIFICATION: any assertion failing.
"""
seq = [0, 11, 12, 21, 22, 32, 33, 34, 43, 44, 45, 54, 55, 56, 65, 66, 67, 76, 77, 78, 87, 88, 89, 98, 99, 0]
d = lambda x: (x // 10, x % 10)
ch = [sum(abs(p % 2 - q % 2) for p, q in zip(d(a), d(b))) for a, b in zip(seq, seq[1:])]
assert set(ch) == {1, 2}                                                                  # W1
i = seq.index(33)
assert ch[i:i + 3] == [1, 2, 1] and ch[seq.index(22)] == 1
m = [[(r + c) % 8 for c in range(8)] for r in range(8)]
assert sum(v % 2 == 0 for row in m for v in row) == 32                                    # W2
vals = [m[a % 8][b % 8] for a, b in map(d, seq)]
assert vals == [0, 2, 3, 3, 4, 5, 6, 7, 7, 0, 1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 7, 0, 1, 1, 2, 0]  # W3
assert sum(vals) == 85 and (85 - 1) % 9 + 1 == 4
assert all((v % 2 == 0) == (d(x)[0] == d(x)[1]) for x, v in zip(seq, vals))
assert [(a % 8, b % 8) for a, b in map(d, (88, 89, 98, 99))] == [(0, 0), (0, 1), (1, 0), (1, 1)]  # W4
