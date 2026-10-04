# CLASS: AUDIT
"""
Audit of supplied records (2026-10-04): AUD-WAV-QDIST-C (row sums of squares of an 8x8 matrix C),
AUD-LEY-MOD5, and the mod-5 step. The script they cite, t325_world_record_overlay_expansion.py,
is not in this repository; C is rebuilt from the construction the record spells out.
Mathematics only.

CORRECT
  Q1 C: C[0,0] = 5; the eight cyclic edges (0,1) ... (6,7), (7,0) set to 2; +1 at (1,0) ... (6,5),
     (0,7) and the diagonal (1,1) ... (7,7). Total mass 35; row sums of squares
     [30, 6, 6, 6, 6, 6, 6, 5], total 71. The record is right that the script's asserted
     [31, 6, ..., 6] / 73 does not match its own matrix, and right that 73 would need mass 37.
  Q2 Mod 5: V_q -> [0, 1, 1, 1, 1, 1, 1, 0], residue sum 6 = 1; 71 = 1 mod 5; 35 x 71 = 2485 = 0.
     The last is forced, not a "preserved property": 35 is itself a multiple of 5.

PREMISE VOID
  Q3 AUD-LEY-MOD5: 41,080 = 0 mod 5 is true arithmetic, but 41,080 is not the digit count of
     10243^5100 + 5100^10243 (37,977 digits, = 2 mod 5), and that number is composite, divisible
     by 113 and 5101 (leyland_record_claim_supplied_audit_2026_10_04.py). The record describes a
     number that is neither a Leyland prime nor 41,080 digits long.
FALSIFICATION: any assertion failing.
"""
import numpy as np

C = np.zeros((8, 8), int)
C[0, 0] = 5
for i in range(8):
    C[i, (i + 1) % 8] = 2
for r, c in [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (0, 7)] + [(k, k) for k in range(1, 8)]:
    C[r, c] += 1
Vq = [int((row ** 2).sum()) for row in C]
assert C.sum() == 35 and Vq == [30, 6, 6, 6, 6, 6, 6, 5] and sum(Vq) == 71               # Q1
assert sum(Vq) + 2 == 73 and C.sum() + 2 == 37
assert [v % 5 for v in Vq] == [0, 1, 1, 1, 1, 1, 1, 0] and 71 % 5 == 1 and 35 * 71 % 5 == 0 and 35 % 5 == 0   # Q2
assert 41080 % 5 == 0 and 37977 % 5 == 2                                                 # Q3
assert (pow(10243, 5100, 113) + pow(5100, 10243, 113)) % 113 == 0
