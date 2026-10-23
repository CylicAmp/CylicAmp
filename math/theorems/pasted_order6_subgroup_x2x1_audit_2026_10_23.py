# CLASS: AUDIT
"""
The pasted program output on the subgroup of order 6 mod 37 and the roots of x x + x + 1 (owner_work #423,
2026-10-23). Audit on arrival. Text from another tool's run, relayed by the owner.

PRIOR ART: theorem_111_ascending_descending_gf37.py, Lemma 111.7 (every 3-cycle of the 137-map adds to 0, because
26 is a cube root of 1); CLAUDE.md constants (ord of 26 = 3, 2 a primitive root); the orbits IC = {1, 10, 26} and
NEG_H = {11, 27, 36}.

RIGHT (re-run), every line:
  2 is a primitive root mod 37 (order 36)
  2^6 = 64 = 37 + 27 -> 27, and 27 has order 6
  the powers of 27: 27, 26, 36, 10, 11, 1 -> the subgroup {1, 10, 11, 26, 27, 36} (= IC and NEG_H together)
  x x + x + 1: 1 - 4 = -3 -> 34;  16 x 16 = 256 = 6 x 37 + 34, so 16 is a square root of 34 (21 is the other)
  roots (-1 + 16) / 2 and (-1 - 16) / 2 -> 26 and 10;  both in the order-6 subgroup
  the subgroup is the only one of order 6 (the group is cyclic, order 36); inside it the order-3 part is {1, 10, 26},
  and 10, 26 are the two cube roots of 1 other than 1 -- the roots of x x + x + 1

NEW LINES, owner's notation:
  x = 10:  10 x 10 + 10 + 1 = 111 = 3 x 37     (this is why 37 divides 111, and why 1000 = 27 x 37 + 1)
  x = 26:  26 x 26 + 26 + 1 = 703 = 19 x 37    (26 = 137 by 37: the 137-map multiplier is the other root)
  10 x 26 = 260 = 7 x 37 + 1 -> 1;  10 + 26 = 36 -> -1   (the two roots multiply to 1 and add to -1)
  the order-6 subgroup is the cube roots and their negatives: 37 - 1 = 36, 37 - 10 = 27, 37 - 26 = 11

FALSIFICATION: any assertion failing.
"""
P = 37


def order(a):
    return next(k for k in range(1, P) if pow(a, k, P) == 1)


assert order(2) == 36
assert pow(2, 6, P) == 27 and 64 == 37 + 27 and order(27) == 6
assert [pow(27, k, P) for k in range(1, 7)] == [27, 26, 36, 10, 11, 1]
sub6 = sorted({pow(27, k, P) for k in range(6)})
assert sub6 == [1, 10, 11, 26, 27, 36] and set(sub6) == {1, 10, 26} | {11, 27, 36}
assert [a for a in range(1, P) if order(a) == 6] == [11, 27] and sorted(a for a in range(1, P) if 6 % order(a) == 0) == sub6
assert (1 - 4) % P == 34 and 16 * 16 == 256 == 6 * 37 + 34 and 21 * 21 % P == 34
inv2 = pow(2, -1, P)
roots = sorted({(-1 + 16) * inv2 % P, (-1 - 16) * inv2 % P})
assert roots == [10, 26] and all((r * r + r + 1) % P == 0 for r in roots) and set(roots) <= set(sub6)
assert [a for a in range(1, P) if order(a) == 3] == [10, 26] and sorted(a for a in sub6 if 3 % order(a) == 0) == [1, 10, 26]

assert 10 * 10 + 10 + 1 == 111 == 3 * 37 and 1000 == 27 * 37 + 1
assert 26 * 26 + 26 + 1 == 703 == 19 * 37 and 137 % 37 == 26
assert 10 * 26 == 260 == 7 * 37 + 1 and (10 + 26) % P == P - 1
assert sorted(P - r for r in (1, 10, 26)) == [11, 27, 36]

if __name__ == "__main__":
    print("#423 subgroup output: every line right; 10 x 10 + 10 + 1 = 111 = 3 x 37 and 26 x 26 + 26 + 1 = 703 = 19 x 37 "
          "-- 10 and 26 (= 137 by 37) are the two roots")
