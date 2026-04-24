"""
Riemann Zeta Zeros — first 9 nontrivial zeros on the critical line Re(s) = 1/2
Computed to 30 decimal places via mpmath.

Verified output:
  1st: 14.1347251417346937904572519836
  2nd: 21.0220396387715549926284795939
  3rd: 25.0108575801456887632137909926
  4th: 30.4248761258595132103118975306
  5th: 32.9350615877391896906623689641
  6th: 37.5861781588256712572177634807
  7th: 40.9187190121474951873981269146
  8th: 43.3270732809149995194961221654
  9th: 48.0051508811671597279424727494
"""

from mpmath import mp, zetazero

mp.dps = 30  # 30 decimal places of precision

for n in range(1, 10):
    z = zetazero(n)
    print(f"{n}th zero: {z.imag}")
