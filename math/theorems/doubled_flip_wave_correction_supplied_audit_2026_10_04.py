# CLASS: AUDIT
"""
Audit of a supplied correction (2026-10-04) to the doubled-flip wave
(doubled_flip_wave_supplied_audit_2026_10_04.py). Mathematics only.

CORRECT
  C1 28 two-digit coordinates have digits differing by at most 1 (10 doubles + 9 + 9); the
     corrected path visits 25 of them and misses exactly 01, 10 and 23.
  C2 Doubles have equal parity on both sides; every a(a+1) or (a+1)a has mixed parity (forced:
     consecutive digits differ in parity).

WRONG
  C3 "The right array has 27 terms summing to 126": that 27-entry list is not the one in the
     earlier text, whose right column had 26 entries summing to 125.
  C4 The corrected path 00 11 12 21 22 32 33 ... 77 78 87 88 89 98 99 00 does NOT give 125 / 125.
     It gives left 123, right 122 (drift +1) -- the unpaired 32 contributes the +1. (These are
     the original text's 123 / 122, so the original totals belonged to this path, not to the
     columns it listed.)
  C5 "Skipping 23 is what forces the balance": the opposite. Putting 23 back (27 terms) gives
     125 / 125, drift 0 -- every term then has its flip.
FALSIFICATION: any assertion failing.
"""
fix = "00 11 12 21 22 32 33 34 43 44 45 54 55 56 65 66 67 76 77 78 87 88 89 98 99 00".split()
near = {f"{a}{b}" for a in range(10) for b in range(10) if abs(a - b) <= 1}
assert len(near) == 28 and len(set(fix)) == 25 and sorted(near - set(fix)) == ["01", "10", "23"]  # C1
assert all((int(s[0]) % 2 == int(s[1]) % 2) == (s[0] == s[1]) for s in near)                     # C2
R27 = [0, 1, 2, 1, 2, 3, 2, 3, 4, 3, 4, 5, 4, 5, 6, 5, 6, 7, 6, 7, 9, 7, 8, 9, 8, 9, 0]
R_earlier = [0, 1, 2, 2, 3, 2, 3, 4, 3, 4, 5, 4, 5, 6, 5, 6, 7, 6, 7, 9, 7, 8, 9, 8, 9, 0]
assert (len(R27), sum(R27), len(R_earlier), sum(R_earlier)) == (27, 126, 26, 125)               # C3
col = lambda seq, i: sum(int(s[i]) for s in seq)
assert (len(fix), col(fix, 0), col(fix, 1)) == (26, 123, 122)                                    # C4
with23 = fix[:5] + ["23"] + fix[5:]
assert (len(with23), col(with23, 0), col(with23, 1)) == (27, 125, 125)                           # C5
