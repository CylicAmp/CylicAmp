# CLASS: AUDIT
"""
Audit of supplied text (2026-10-04): "the 21-row block-rotation matrix collapses the RSA
defense". Mathematics only.

WRONG
  R1 Everything the matrix tracks -- digital roots (N mod 9), block rotations of 3-digit
     groups (N mod 999 = 27 x 37), the "8-root track" and "9-root intervals" -- is N reduced
     modulo a small fixed number m. For any m coprime to N, the units mod m form a group,
     so for EVERY residue p0 there is exactly one q0 with p0 * q0 = N (mod m): no candidate
     prime is ever excluded. Checked below for m = 9, 37, 999 on a 256-bit semiprime.
  R2 Two different semiprimes can share N mod 999 and their digital root while having
     completely different factors (constructed below), so these quantities cannot
     determine the factors even in principle.
  R3 The "3 x 7 = 21 row grid" is 3 x 3 x 3 = 27 rows (block_rotation_21_row_supplied_audit_
     2026_10_04.py); "net drift of the spatial gaps is exactly 0" is not defined anywhere in
     the supplied material, so it cannot be tested.
  R4 The text's own source [4] (osandamalith.com, 2026-07-17, "I thought I found a prime
     pattern that breaks RSA") tested the digital-root version and concluded, verbatim:
     "No candidate p is ever excluded, because a valid partner q always exists" and "the very
     group structure that makes the pattern elegant is what guarantees it's useless."
     R1 is the same group argument, extended to mod 999.
FALSIFICATION: any assertion failing -- or a factorization of the N below that uses only
its residues mod 9, 37 and 999.
"""
from math import gcd

from sympy import nextprime

p = nextprime(2 ** 127 + 12345)
q = nextprime(2 ** 128 + 67890)
N = p * q
assert N.bit_length() >= 255

for m in (9, 37, 999):                                                     # R1
    assert gcd(N, m) == 1
    units = [r for r in range(1, m) if gcd(r, m) == 1]
    partners = {r: (N * pow(r, -1, m)) % m for r in units}
    assert all(gcd(s, m) == 1 for s in partners.values())                  # every p0 has a valid q0
    assert len(partners) == len(units)                                     # none excluded
    assert partners[p % m] == q % m                                        # the true pair is one of them

# R2: two semiprimes, same N mod 999 (so same digital root and same block rotations mod 37),
# different factors
a1, b1 = 1009, 1013
target = (a1 * b1) % 999
a2 = 1019
b2 = next(b for b in range(1020, 10 ** 6) if (a2 * b) % 999 == target and all(b % d for d in range(2, int(b ** 0.5) + 1)))
assert (a1 * b1) % 999 == (a2 * b2) % 999 and {a1, b1} != {a2, b2}
assert (a1 * b1) % 9 == (a2 * b2) % 9

if __name__ == "__main__":
    print(f"256-bit N: every unit residue of p mod 9, 37, 999 has a partner -- 0 excluded")
    print(f"{a1}*{b1} and {a2}*{b2}: same residue mod 999 ({target}), different factors")
