# CLASS: AUDIT
"""
Pasted "Sharpened Operational Taxonomy: Canonical Metrics & Exact Quantities" (2026-11-17), from another tool,
relayed by the owner. Eight rows; checked below (Langton's ant re-simulated from an all-white grid, heading up).

RIGHT:
  1. drift: the highway moves (-2, -2) every 104 steps, so (-1/52, -1/52) cells per step for the start heading
     used in langton_ant_highway_2026_10_14.py (other start headings turn the vector: (-2, 2), (2, 2), (2, -2)).
  2. 58 - 46 = 12: in each 104-step period of the highway the ant stands on a white cell 58 times and on a black cell
     46 times; every visit flips the cell, so black cells grow by 58 - 46 = 12. (This settles the "58 - 46" asked
     about with the ledger's Lemma 11. The repo's 23 - 11 counts the cells flipped an odd number of times in a
     period -- the same net 12. The window starting exactly at the onset 9976 gives 57 - 47 = 10; from 9977 on, 12.)
  3. NPCR critical value at 512 x 512, alpha 0.05: 99.5893% (pasted_tmc_manuscript_pages_11_13_audit_2026_11_17.py).
  4. mu_UACI = (F + 2)/(3(F + 1)) = 257/768 = 33.4635% -- right as the value.
  5. tau = digit sum; tau(n) = n - 9 sum floor(n/10^k) holds (checked for every n below 100,000); 17 -> 8.
  6. root = 1 + (n - 1) mod 9 (for n >= 1); kept by every cut, as in owner_3333_cuts_and_repeats.
  7. pi(17) = 7, pi(23) = 9.

FAULTS THAT CHANGE A NUMBER:
  4'. The integral given for mu, (1/255) int int |x - y| / 255^2 dx dy over [0, 255]^2, equals 1/3 = 33.333%, not
      257/768. 257/768 is the average of |x - y| / 255 over the 256 x 256 grey-level pairs (a sum, not an integral).
  8.  "G(w) = sum of ord(w_i)": ord is the computer character code; read that way "I AM" gives 247 (215 without the
      space). The 23 needs the alphabet position, ord - 64.
  (Edge: 1 + (n - 1) mod 9 gives 9 at n = 0; the root of 0 is 0.)

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction

from sympy import primepi


def ant(n_steps, heading=(0, 1)):
    black, x, y = set(), 0, 0
    dx, dy = heading
    pos, col, nb, B = [(0, 0)], [], 0, [0]
    for _ in range(n_steps):
        k = (x, y)
        if k in black:
            col.append(1)
            dx, dy = -dy, dx
            black.discard(k)
            nb -= 1
        else:
            col.append(0)
            dx, dy = dy, -dx
            black.add(k)
            nb += 1
        x += dx
        y += dy
        pos.append((x, y))
        B.append(nb)
    return pos, col, B


pos, col, B = ant(11000)
assert all((pos[t + 104][0] - pos[t][0], pos[t + 104][1] - pos[t][1]) == (-2, -2) for t in range(9976, 11000 - 104))
assert pos[9975 + 104][0] - pos[9975][0] != -2 or pos[9975 + 104][1] - pos[9975][1] != -2
assert (Fraction(-2, 104), Fraction(-2, 104)) == (Fraction(-1, 52), Fraction(-1, 52))
for start in range(9977, 10800, 37):
    white = col[start:start + 104].count(0)
    assert (white, 104 - white) == (58, 46) and B[start + 104] - B[start] == 12
assert col[9976:9976 + 104].count(0) == 57 and B[9976 + 104] - B[9976] == 10
for h, s in (((1, 0), (-2, 2)), ((0, -1), (2, 2)), ((-1, 0), (2, -2))):
    p2, _, _ = ant(10200, h)
    assert (p2[10100][0] - p2[9996][0], p2[10100][1] - p2[9996][1]) == s

N, F = 256, 255
mean = Fraction(sum(abs(a - b) for a in range(N) for b in range(N)), N * N * F)
assert mean == Fraction(257, 768) == Fraction(F + 2, 3 * (F + 1)) and round(float(mean) * 100, 4) == 33.4635
assert Fraction(F ** 3, 3) / F ** 2 / F == Fraction(1, 3)                 # the integral as written

assert all(sum(map(int, str(n))) == n - 9 * sum(n // 10 ** k for k in range(1, 12)) for n in range(1, 100_000))
assert primepi(17) == 7 and primepi(23) == 9
assert sum(map(ord, "I AM")) == 247 and sum(map(ord, "IAM")) == 215 and sum(ord(c) - 64 for c in "IAM") == 23
assert 1 + (0 - 1) % 9 == 9

if __name__ == "__main__":
    print("taxonomy: drift -1/52, 58 white / 46 black visits per period (+12), values right; the UACI integral gives 1/3")
