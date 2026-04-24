"""
Riemann Zeta Zeros — first 8 nontrivial zeros on the critical line Re(s) = 1/2
Computed to 50 decimal places of internal precision via mpmath; printed to 10 d.p.

Verified output:
  Zero 1: 14.1347251417
  Zero 2: 21.0220396388
  Zero 3: 25.0108575801
  Zero 4: 30.4248761259
  Zero 5: 32.9350615877
  Zero 6: 37.5861781588
  Zero 7: 40.9187190121
  Zero 8: 43.3270732809
"""

import mpmath

mpmath.mp.dps = 50  # 50 decimal places of internal precision

for n in range(1, 9):
    z = mpmath.zetazero(n)
    t = mpmath.im(z)
    print(f"Zero {n}: {float(t):.10f}")
