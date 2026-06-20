"""
Pisano Period Modulo 333 — CRT Decomposition

Theorem (Pisano period for coprime moduli):
  If gcd(m,n) = 1, then π(mn) = lcm(π(m), π(n)).

Proof sketch (CRT):
  By CRT, Z/mnZ ≅ Z/mZ × Z/nZ.
  State (F_k, F_{k+1}) mod mn returns to (0,1) iff it returns
  to (0,1) mod m AND mod n simultaneously.
  Therefore π(mn) = lcm(π(m), π(n)).

Application — 333 = 9 × 37, gcd(9,37) = 1:
  π(9)   = 24   (Pisano period mod 9, proven in Layer 58)
  π(37)  = 76   (Pisano period mod 37, verified here)
  π(333) = lcm(24, 76) = 24×76 / gcd(24,76) = 1824/4 = 456

Framework connections:
  333 = 9 × 37  — joins both core moduli of the 1/137 framework
  456 mod 9  = 6  (DR=6, coupling signature, matches all k-DR values)
  456 mod 37 = 456 - 12×37 = 456 - 444 = 12  (f26 target)
  456 mod 24 = 0  (exact multiple of Lucas/Fib period)
  456 mod 76 = 0  (exact multiple of π(37))
  gcd(24, 76) = 4  (the shared factor binding the two periods)

Pisano period mod 37: π(37) = 76 = 2×38 = 2×(37+1)
  Note: for prime p ≡ ±1 mod 5, π(p) | p-1 or p+1.
  37 ≡ 2 mod 5, and 37+1=38, 2×38=76. ✓

Sealed output:
  pi(9)   = 24
  pi(37)  = 76
  pi(333) = 456
  lcm(24,76) = 456
  Theorem confirmed: True
"""

import ast
from math import gcd


def pisano(m):
    a, b = 0, 1
    for i in range(1, m * m + 1):
        a, b = b, (a + b) % m
        if a == 0 and b == 1:
            return i


# Syntax audit
_code = """
from math import gcd
def pisano(m):
    a, b = 0, 1
    for i in range(1, m*m+1):
        a, b = b, (a+b)%m
        if a==0 and b==1: return i
pi9=pisano(9); pi37=pisano(37); pi333=pisano(333)
lcm_val=(pi9*pi37)//gcd(pi9,pi37)
print("Pisano 333 audit successful.")
"""
ast.parse(_code)

# --- Compute ---
pi9   = pisano(9)
pi37  = pisano(37)
pi333 = pisano(333)
lcm_val = (pi9 * pi37) // gcd(pi9, pi37)

# --- Assertions ---

# Base values
assert pi9  == 24,  f"pi(9) = {pi9}"
assert pi37 == 76,  f"pi(37) = {pi37}"

# CRT theorem: lcm gives the combined period
assert gcd(9, 37) == 1               # coprimality required
assert 333 == 9 * 37
assert gcd(24, 76) == 4
assert lcm_val == 456
assert pi333 == 456                   # direct computation confirms

# Framework connections
assert 456 % 9  == 6    # DR=6, coupling signature
assert 456 % 37 == 12   # DR=3 target set {3,12,21,30}
assert 456 % 24 == 0    # exact multiple of Layer 58 period
assert 456 % 76 == 0    # exact multiple of pi(37)

# 456 DR
def dr(n): return (n-1)%9+1 if n>0 else 0
assert dr(456) == 6     # DR=6 matches unified k coupling signature

# pi(37) structure: 76 = 2×38 = 2×(37+1)
assert pi37 == 2 * (37 + 1)

# Higher composites (bonus)
pi18  = pisano(18)   # 18 = 2×9
pi74  = pisano(74)   # 74 = 2×37 (phase-lock number)
assert pi74 == (pi37 * pisano(2)) // gcd(pi37, pisano(2))


if __name__ == "__main__":
    print("Pisano Period Modulo 333 — CRT Decomposition")
    print()
    print(f"pi(9)   = {pi9}")
    print(f"pi(37)  = {pi37}")
    print(f"pi(333) = {pi333}")
    print(f"lcm(24,76) = {lcm_val}  [gcd={gcd(24,76)}]")
    print(f"Theorem confirmed: {pi333 == lcm_val}")
    print()
    print("Framework connections:")
    print(f"  456 mod 9  = {456%9}  (DR=6, coupling signature)")
    print(f"  456 mod 37 = {456%37}  (DR=3 target)")
    print(f"  456 mod 24 = {456%24}  (exact multiple of pi(9))")
    print(f"  456 mod 76 = {456%76}  (exact multiple of pi(37))")
    print(f"  DR(456)    = {dr(456)}  (unified k-coupling)")
    print(f"  pi(37)=76=2×(37+1): {pi37==2*(37+1)}")
    print()
    print(f"  pi(18) = {pi18}  pi(74) = {pi74}")
    print()
    print("All assertions passed.")
