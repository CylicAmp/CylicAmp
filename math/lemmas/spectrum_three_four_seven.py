# CLASS: COMPUTATION
"""
Seven colours = three (red, green, blue) + four (orange, yellow, indigo,
violet). Owner, 2026-10-06. The numbers 3, 4, 7 run through the frameworks
(.claude/skills/gf37-audit/audit.py).

ORBITS:
  - 3 and 4 are in the same orbit: C3 = {3, 4, 30}, since 3 * 26 = 78 = 4
    (mod 37). The three and the four are one orbit.
  - 7 is in D7 = {7, 33, 34}, the negative of C3:
      37 - 3 = 34, 37 - 4 = 33, 37 - 30 = 7.
    So the whole (7) sits in the mirror of its two parts (3, 4).
  - Red 700 nm is also D7 (rgb_wavelengths_frameworks.py).
  - Z/12 classes: 3 and 4 are class 2, 7 is class 8, and 8 - 2 = 6 is the
    half turn (negation).

PRIMES:
  - 3 -> 7 is a Sophie Germain chain: 2*3 + 1 = 7. 3 is Sophie Germain and 7
    is safe.
  - 3 and 7 are both twin primes (3,5) and (5,7), sharing 5.
  - 4 = 2^2 is the only one of the three that is not prime.

DIGITS:
  - 3 + 4 = 7 and 3 * 4 = 12 (DR 3).
  - 34 (the three then the four) = 2 * 17, mod 37 = 34, D7: the same orbit
    as 7.
  - 43 (the four then the three) is prime, twin (41, 43), mod 37 = 6, TESLA.
  - 347 is prime, twin (347, 349), safe (173 -> 347), mod 37 = 14, C9. C9 is
    also blue's orbit (4358).

FALSIFICATION: any assertion below failing.
"""
from sympy import isprime, factorint

C3, D7 = {3, 4, 30}, {7, 33, 34}
assert 3 in C3 and 4 in C3 and 7 in D7
assert (3 * 26) % 37 == 4 and (4 * 26) % 37 == 30 and (30 * 26) % 37 == 3
assert {(37 - a) for a in C3} == D7

assert 2 * 3 + 1 == 7 and isprime(3) and isprime(7)
assert isprime(5) and not isprime(4)
assert 3 + 4 == 7 and (3 * 4) % 9 == 3

assert factorint(34) == {2: 1, 17: 1} and 34 % 37 in D7
assert isprime(43) and isprime(41) and 43 % 37 == 6
assert isprime(347) and isprime(349) and isprime(173) and 347 == 2 * 173 + 1
assert 347 % 37 == 14 and 4358 % 37 in {14, 29, 31}

print("3, 4 in C3; 7 in D7 = -C3; 3 -> 7 Sophie Germain. All assertions pass.")
