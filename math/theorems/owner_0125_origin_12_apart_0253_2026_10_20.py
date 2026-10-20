# CLASS: AUDIT
"""
Where 0.125 came from, 0.125 and 0.137 twelve apart, and 0.253 (owner_work #381, 2026-10-20). Process entry: owner_work/PROCESS.md, #381.

THE OWNER'S LINES, verbatim:
    0.125 i got by dividing what times what? Its a important detail.

    because

    0125+
    0.012=0137 are exactly 12 apart

    0.253 all prime building blocks

WHERE 0.125 CAME FROM (the record, #368 and #375):
  #368: "1 +3 twos / 9÷2÷2÷2=" and "1.125+0.012=1.137" -- 9 divided by 2, three times: 9 ÷ 2 = 4.5 → ÷ 2 = 2.25 → ÷ 2 = 1.125, which is 9 ÷ (2x2x2) = 9 ÷ 8.
  1.125 = 1 + 0.125, and 0.125 = 1 ÷ 2 ÷ 2 ÷ 2 = 1 ÷ 8 (the "1 + 3 twos"). #375 wrote the same halving as 8 ÷ 2 ÷ 2 ÷ 2 = 1.
CHECKED:
  0.125 + 0.012 = 0.137                                                          right
  137 - 125 = 12 (they are 12 thousandths apart)                                 right
  0.253: 2, 5 and 3 are all prime                                                right
  and 253 = 11 x 23, two primes (11 and 23: 2x11+1 = 23, a Sophie Germain pair); also 253 = 125 + 128 = 5x5x5 + 2x2x2x2x2x2x2.
MISSING (asked): how 0.253 was made from 0.125 / 0.137 / 0.012.
FRAMEWORKS (gf37-audit): 125 = 5x5x5 = 14 C9 ; 253 = 11x23 = 31 C9 -- the same orbit, and 26 x 14 = 364 = 9x37 + 31, so 253's residue is the 137-map of 125's ;
  137 = 26 IC ; 12 SA_ST_A.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as Q

from sympy import factorint, isprime

assert Q(9) / 2 / 2 / 2 == Q(9, 8) == Q(1125, 1000) and [Q(9) / 2, Q(9) / 4] == [Q(45, 10), Q(225, 100)]
assert Q(9, 8) - 1 == Q(125, 1000) == Q(1) / 2 / 2 / 2 == Q(1, 8) and Q(8) / 2 / 2 / 2 == 1
assert Q(125, 1000) + Q(12, 1000) == Q(137, 1000) and 137 - 125 == 12
assert all(isprime(d) for d in (2, 5, 3)) and factorint(253) == {11: 1, 23: 1} and 2 * 11 + 1 == 23
assert 253 == 125 + 128 == 5 ** 3 + 2 ** 7
assert (125 % 37, 253 % 37, 137 % 37, 12 % 37) == (14, 31, 26, 12) and 26 * 14 == 364 == 9 * 37 + 31 and (26 * 125) % 37 == 253 % 37

if __name__ == "__main__":
    print("0.125 = 9/2/2/2 - 1 = 1/2/2/2 (#368); 0.125 + 0.012 = 0.137, 12 apart; 0.253: digits 2 5 3 prime, 253 = 11 x 23 = 125 + 128")
