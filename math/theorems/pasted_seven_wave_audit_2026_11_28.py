# CLASS: AUDIT
"""
Pasted "Reset & Redo: Pure Mathematical Mechanics of the 7-Wave" (2026-11-28), built on equations it attributes to the
owner. Audit on arrival.

THE EQUATIONS (as relayed in the paste), each RIGHT:
    7 x 2 = 14 -> 1 + 4 = 5      7 x 3 = 21 -> 2 + 1 = 3 (and its flip 12, #259)      7 x 5 = 35 -> 3 + 5 = 8
    7 x 7 = 49 -> 4 + 9 = 13 -> 1 + 3 = 4      (1 + 8) + (1 + 8) = 9 + 9 = 18 -> 1 + 8 = 9,  3 + 6 = 9
RIGHT:
  x -> 7x by 9 on 1..9: two 3-cycles 1 -> 7 -> 4 -> 1 and 2 -> 5 -> 8 -> 2, and 3, 6, 9 fixed (7 leaves 1 by 3 and
    7 x 7 x 7 = 343 leaves 1 by 9). Its 3-cycle {1, 4, 7} is the x4 orbit of owner_369_729_189_rotations_flips_2026_11_19.py.
  7^k by 37: 7, 12, 10, 33, 9, 26, 34, 16, 1 -- order 9 (7 = 2^32 by 37, and 36 / 4 = 9); ord_37(33) = 9; pi(137) = 33;
    94801 leaves 7 by 37; 7^7 passes through 26 x 7 = 182, which leaves 34.
  |12 - 21| = 9, |182 - 281| = 99, |94801 - 10849| = 83952 -> 27 -> 9 (forced: a number minus its flip divides by 9).
WRONG (each changes a statement):
  "multiplying by 7 is the inverse doubling operator": 7 leaves -2 by 9, so x7 is doubling with the sign flipped; the
    inverse of doubling is x5 (2 x 5 = 10 leaves 1).
  tau(75) = tau(48) = 12 again: tau(75) = 6, tau(48) = 10.

FALSIFICATION: any assertion failing.
"""
from sympy import divisor_count, n_order, primepi

dr = lambda n: 1 + (n - 1) % 9
assert [(7 * k, dr(7 * k)) for k in (2, 3, 5, 7)] == [(14, 5), (21, 3), (35, 8), (49, 4)] and dr(13) == 4 and 3 * 7 == 21
assert (1 + 8) + (1 + 8) == 18 and (1 + 1) + (8 + 8) == 18 and dr(18) == 9 and 3 + 6 == 9
m7 = {x: (7 * x) % 9 or 9 for x in range(1, 10)}
assert m7[1] == 7 and m7[7] == 4 and m7[4] == 1 and m7[2] == 5 and m7[5] == 8 and m7[8] == 2 and all(m7[x] == x for x in (3, 6, 9))
assert pow(7, 3, 9) == 1 and 7 % 3 == 1 and {pow(4, k, 9) for k in range(3)} == {1, 4, 7}
assert [pow(7, k, 37) for k in range(1, 10)] == [7, 12, 10, 33, 9, 26, 34, 16, 1] and n_order(7, 37) == 9
assert pow(2, 32, 37) == 7 and 36 // 4 == 9 and n_order(33, 37) == 9 and primepi(137) == 33 and 94801 % 37 == 7
assert 26 * 7 == 182 and 182 % 37 == 34
assert 21 - 12 == 9 and 281 - 182 == 99 and 94801 - 10849 == 83952 and dr(83952) == 9
assert all((n - int(str(n)[::-1])) % 9 == 0 for n in range(1, 100000))
assert (-2) % 9 == 7 and pow(2, -1, 9) == 5 and (2 * 5) % 9 == 1
assert (divisor_count(75), divisor_count(48)) == (6, 10)

if __name__ == "__main__":
    print("7-wave: equations, the x7 cycles, ord_37(7) = 9 right; x7 is minus doubling (inverse is x5); tau(75) = 6")
