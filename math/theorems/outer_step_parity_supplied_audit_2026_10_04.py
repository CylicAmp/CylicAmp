# CLASS: AUDIT
"""
Audit of supplied script and record (2026-10-04): parity along the outer step loop
12 23 34 45 56 67 78 89 91 12 -- the 2-digit version of the owner's roads (add 1 to each
digit, 9 wraps to 1; period 9, cf. theorem_326 and next_term_sequences_index.py).
Mathematics only.

CORRECT
  O1 Left parities O E O E O E O E O O; right E O E O E O E O O E; node parities = right parities
     (forced: a number's parity is its last digit's). Counts: left 4 E / 6 O, right 5 / 5,
     nodes 5 / 5. The script runs and its assertions hold.
  O2 The alternation breaks only at the 9 -> 1 wrap: right column at 89 -> 91, left column at
     91 -> 12. Mod-5 pairs in the table are right.
CORRECTED
  O3 "Net drift locks at -1": the ten listed nodes count 12 twice. The loop itself has 9 nodes:
     eight steps of -1 and one +8 (at 91) sum to 0. The -1 is the repeated 12.
  O4 "Mod 5 variance locks at -1" is not defined anywhere in the record.
FALSIFICATION: any assertion failing.
"""
seq = [12, 23, 34, 45, 56, 67, 78, 89, 91, 12]
L = [x // 10 % 2 for x in seq]
R = [x % 2 for x in seq]
assert L == [1, 0, 1, 0, 1, 0, 1, 0, 1, 1] and R == [0, 1, 0, 1, 0, 1, 0, 1, 1, 0]       # O1
assert [x % 2 for x in seq] == R and (L.count(0), R.count(0)) == (4, 5)
breaks_R = [(seq[i], seq[i + 1]) for i in range(9) if R[i] == R[i + 1]]
breaks_L = [(seq[i], seq[i + 1]) for i in range(9) if L[i] == L[i + 1]]
assert breaks_R == [(89, 91)] and breaks_L == [(91, 12)]                                 # O2
road = lambda n: int("".join(str(int(c) % 9 + 1) for c in str(n)))
assert all(road(a) == b for a, b in zip(seq, seq[1:]))
drift = [x // 10 - x % 10 for x in seq]
assert sum(drift) == -1 and sum(drift[:9]) == 0 and drift[8] == 8                        # O3
