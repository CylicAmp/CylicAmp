"""
Theorem: Infinite Resonances on Every 666-Track
(Promoted from Conjecture 1 — now a proved Theorem)

Sovereign triangle: sides 9, 10, 17 — area A0 = 36 = 6²
Scaling by m ∈ Z⁺: sides 9m, 10m, 17m — area A = 36m² = (6m)²

Properties preserved for all m:
  DR(A) = DR(36m²) = 9  (Absolute 9 Vacuum)
  semiperimeter s = 18m ≡ 0 (mod 18)
  coupling k = 6m

Six 666-tracks — all solved via 17m ≡ anchor (mod 666), gcd(17,666)=1:
  505-track: m0=539, step=666
  419-track: m0=103, step=666
  233-track: m0=523, step=666
   61-track: m0=317, step=666
  209-track: m0=169, step=666
   85-track: m0=5,   step=666

Since gcd(17,666)=1, every congruence 17m≡a (mod 666) has a unique
solution mod 666, giving an infinite arithmetic progression m=m0+666t.
Each distinct m gives a distinct triangle and distinct k=6m.
Therefore every 666-track contains infinitely many resonances. QED
"""

import ast
from math import gcd


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


# Syntax audit
_code = """
from math import gcd
def dr(n): return (n-1)%9+1 if n>0 else 0
triangle = (9,10,17)
area0 = 36
"""
ast.parse(_code)

# Sovereign triangle
SIDES = (9, 10, 17)
AREA0 = 36

# --- Assertions ---

# Base triangle: area via Heron's formula
a, b, c = SIDES
s0 = (a + b + c) // 2
area_check = (s0 * (s0-a) * (s0-b) * (s0-c)) ** 0.5
assert abs(area_check - AREA0) < 1e-9, f"Area {area_check} != 36"
assert dr(AREA0) == 9       # Absolute 9 Vacuum at base

# Scaling: area = 36m², DR = 9 for all m
for m in range(1, 50):
    assert dr(AREA0 * m * m) == 9, f"DR(36m²) != 9 at m={m}"
    assert (18 * m) % 18 == 0     # semiperimeter divisible by 18

# 666-track congruences — verify base solutions and step sizes
TRACKS = [
    (505, 539),
    (419, 103),
    (233, 523),
    ( 61, 317),
    (209, 169),
    ( 85,   5),
]
STEP = 666  # gcd(17,666)=1 → unique solution mod 666

# Verify all six tracks: 17*m0 ≡ anchor (mod 666), infinite progression
assert gcd(17, 666) == 1    # solvability guaranteed for all anchors
for anchor, m0 in TRACKS:
    assert (17 * m0) % 666 == anchor, f"Base solution fails for track {anchor}"
    for t in range(10):
        m = m0 + STEP * t
        assert (17 * m) % 666 == anchor
        assert dr(AREA0 * m * m) == 9
        assert (18 * m) % 18 == 0

# DR of 666
assert dr(666) == 9         # 666 itself is in the Absolute 9 Vacuum


if __name__ == "__main__":
    print("Theorem: Infinite Resonances on Every 666-Track")
    print()
    print(f"Sovereign triangle: sides {SIDES}, area={AREA0}, DR(area)={dr(AREA0)}")
    print(f"Scaling law: area=36m², DR=9 for all m (verified m=1..49)")
    print()
    print(f"{'Track':<6} {'m0':<8} {'17×m0 mod 666'}")
    print("-" * 35)
    for anchor, m0 in TRACKS:
        print(f"{anchor:<6} m0={m0:<6} {(17*m0)%666} ✓")
    print()
    print(f"DR(666) = {dr(666)}  (666-lattice in Absolute 9 Vacuum)")
    print(f"gcd(17,666)={gcd(17,666)} → all 6 tracks solvable via 17m≡anchor (mod 666)")
    print()
    print("Every track has infinite arithmetic progression of solutions.")
    print("Conjecture 1 → THEOREM. QED.")
    print()
    print("All assertions passed.")
