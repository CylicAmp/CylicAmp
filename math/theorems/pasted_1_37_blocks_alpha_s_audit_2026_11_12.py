# CLASS: AUDIT
"""
The output block that arrived with the owner's message of 2026-11-12 (program output, relayed):

    1/37 = 0.02702702702702703  block: 027  37*27 = 999  1/27 block: 037
    ord_37(10): 3
    k=1,10,26 blocks: ['027', '270', '702']
    rotation families: 12
    all block digit sums multiple of 9: True
    g^2 needed for 8g^2/3 = 1/37: 3/296 = 0.010135135135135136
    1/alpha_s(mt) one-loop = 9.253;  alpha_s = 1/37 at Q ~ 1.13e+13 GeV (one-loop)

RIGHT, every line (recomputed below):
  1/37 = 0.027 027 ..., 37 x 27 = 999, 1/27 = 0.037 037 ...;  10 has order 3 by 37;
  k/37 for k = 1, 10, 26 has blocks 027, 270, 702 -- the block of k/37 is 27 x k, so the three are rotations;
  36 nonzero remainders in groups of 3 = 12 rotation families;  every block is 27 x k, so its digits add to a
    multiple of 9 (forced);  8 g^2 / 3 = 1/37 gives g^2 = 3/296 = 0.0101351351...;
  one-loop running: 1/alpha_s(mt) = 1/0.1180 + (23/3)/(2 pi) x ln(mt/mZ) = 9.252 .. 9.254 for mt = 172.5 .. 172.76
    GeV (mZ = 91.1876; inputs not printed in the block, these reproduce it); then with 6 quark flavours
    (b0 = 11 - 2 x 6/3 = 7), 1/alpha_s(Q) = 9.253 + (7/(2 pi)) ln(Q/mt) = 37 at Q = 1.131 x 10^13 GeV.

PRIOR ART (repo): 999 = 27 x 37 and IC = {1, 10, 26} = <10> are in T302; the 12 families are the Z/12 orbit
  quotient (T118, T138, ...). The one-loop scale where alpha_s = 1/37 is not in the repo before this file.

SCOPE: one-loop only, as the block says; Q barely moves with the top mass (it goes as mt^(-2/21)).

FALSIFICATION: any assertion failing.
"""
import math
from fractions import Fraction

assert repr(1 / 37) == "0.02702702702702703" and 37 * 27 == 999 and f"{1000 // 27:03d}" == "037"
assert [pow(10, e, 37) for e in (1, 2, 3)] == [10, 26, 1]
assert {k: f"{k * 1000 // 37:03d}" for k in (1, 10, 26)} == {1: "027", 10: "270", 26: "702"}
assert all(k * 1000 // 37 == 27 * k for k in range(1, 37))
assert 36 // 3 == 12 and len({frozenset(k * m % 37 for m in (1, 10, 26)) for k in range(1, 37)}) == 12
assert all(sum(map(int, f"{27 * k:03d}")) % 9 == 0 for k in range(1, 37))
g2 = Fraction(3, 296)
assert Fraction(8, 3) * g2 == Fraction(1, 37) and repr(float(g2)) == "0.010135135135135136"

a_mz, mz = 0.1180, 91.1876
for mt in (172.5, 172.57, 172.76):
    inv_mt = 1 / a_mz + (23 / 3) / (2 * math.pi) * math.log(mt / mz)
    assert round(inv_mt, 2) in (9.25,) and 9.252 <= inv_mt <= 9.2545
    Q = mt * math.exp((37 - inv_mt) * 2 * math.pi / 7)
    assert 1.12e13 < Q < 1.14e13 and f"{Q:.2e}" == "1.13e+13"

if __name__ == "__main__":
    print("1/37 blocks, ord 3, 12 families, 3/296, 1/alpha_s(mt) = 9.253, Q = 1.13e13 GeV: all right")
