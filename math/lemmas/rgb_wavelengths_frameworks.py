# CLASS: COMPUTATION
"""
The CIE 1931 RGB primaries run through the repo's frameworks (owner, 2026-10-06).
    red 700 nm, green 546.1 nm, blue 435.8 nm
The decimal point is dropped (546.1 -> 5461, 435.8 -> 4358).

UNITS DO NOT MATTER for the orbit or the digital root (forced):
  - Changing units by a power of 10 (nm, angstrom, dropping the decimal point)
    multiplies by 10^k.
  - 10 is in the orbit {1, 10, 26} = IC, so every multiplication by 10 stays
    in the same orbit.
  - 10 = 1 (mod 9), so the digital root does not change either.
  - Example: 700 nm = 7000 angstrom; residues 34 and 7, both D7.

RESULTS (.claude/skills/gf37-audit/audit.py):
          n     mod 37  orbit   class  DR  factorization
  red     700   34      D7       8     7   2^2 * 5^2 * 7
  green   5461  22      NQR17    7     7   43 * 127      (127 = 2^7 - 1)
  blue    4358  29      C9       9     2   2 * 2179
  - Red and green share digital root 7. Blue is 2.
  - Prime factors in twin pairs: 5 and 7 (red), 43 (green; 41, 43).
  - 127 is a Mersenne prime. 2179 is in no twin pair and is neither Sophie
    Germain nor safe.
  - Orbit classes 8, 7, 9: three different orbits, no two antipodal.

SCOPE: 546.1 and 435.8 nm are mercury emission lines; 700 nm was a chosen
value. These are conventions, so nothing here is a property of light.

FALSIFICATION: any assertion below failing.
"""
from sympy import factorint, isprime

dr = lambda n: n % 9 or 9
IC = {1, 10, 26}
ORB = {"D7": {7, 33, 34}, "NQR17": {17, 22, 35}, "C9": {14, 29, 31}}
orbit = lambda n: next(k for k, v in ORB.items() if n % 37 in v)

RGB = {"red": 700, "green": 5461, "blue": 4358}
assert {k: v % 37 for k, v in RGB.items()} == {"red": 34, "green": 22, "blue": 29}
assert {k: orbit(v) for k, v in RGB.items()} == {"red": "D7", "green": "NQR17", "blue": "C9"}
assert {k: dr(v) for k, v in RGB.items()} == {"red": 7, "green": 7, "blue": 2}
assert factorint(700) == {2: 2, 5: 2, 7: 1}
assert factorint(5461) == {43: 1, 127: 1} and 127 == 2**7 - 1
assert factorint(4358) == {2: 1, 2179: 1} and isprime(2179)

# units: powers of 10 keep orbit and DR
assert 10 in IC and 10 % 9 == 1
for n in RGB.values():
    for k in range(1, 6):
        assert orbit(n * 10**k) == orbit(n) and dr(n * 10**k) == dr(n)
assert 7000 % 37 == 7 and orbit(7000) == "D7"

# twin / Sophie Germain profile of the prime factors
twin = lambda p: isprime(p - 2) or isprime(p + 2)
assert [p for p in (2, 5, 7, 43, 127, 2179) if twin(p)] == [5, 7, 43]
assert not isprime(2 * 2179 + 1) and not isprime((2179 - 1) // 2)

print("RGB: red 700 D7 DR7 | green 5461 NQR17 DR7 | blue 4358 C9 DR2. Units-invariant. All assertions pass.")
