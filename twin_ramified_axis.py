"""
twin_ramified_axis.py — twin prime midpoints and the chi_{-3} = 0 axis.

THEOREM (identity, zero degrees of freedom).
  For every twin pair (p, p+2) with p > 3:
    chi_{-3}(p) = -1  (inert in Z[omega]),
    chi_{-3}(p+1) = 0  (midpoint in the chi=0 residue class),
    chi_{-3}(p+2) = +1 (split in Z[omega]);
  and mod 9 the pair has exactly one of three types:
    (2,3,4), (5,6,7), (8,9,1)  — midpoint DR always in {3,6,9}.
PROOF. p > 3 twin lower forces p ≡ 5 (mod 6), so p mod 9 ∈ {2,5,8};
  add 1 and 2. Mod 3 this reads p ≡ 2, p+1 ≡ 0, p+2 ≡ 1. QED.
NOTE ON TERMINOLOGY. Only the prime 3 ramifies in Z[omega]; midpoints are
  composite. The correct statement is that midpoints lie in the chi = 0
  ("ramified-type") residue class, not that they ramify.

EMPIRICAL CONTENT. The only open question is whether the three types are
  equidistributed. Hardy–Littlewood predicts yes (the mod-9 obstruction acts
  identically on all three); this script measures it.
"""
import sys
from collections import Counter

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 10**6

def sieve(n):
    S = bytearray([1]) * (n + 1); S[0] = S[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if S[i]:
            S[i*i::i] = bytearray(len(S[i*i::i]))
    return S

dr   = lambda n: (n - 1) % 9 + 1
chi3 = lambda n: 0 if n % 3 == 0 else (1 if n % 3 == 1 else -1)

S = sieve(LIMIT)
types = Counter()
violations = 0
for p in range(5, LIMIT - 1):
    if S[p] and S[p + 2]:
        m = p + 1
        types[dr(m)] += 1
        if (chi3(p), chi3(m), chi3(p + 2)) != (-1, 0, 1):
            violations += 1                     # provably unreachable
        if dr(m) not in (3, 6, 9):
            violations += 1                     # provably unreachable

N = sum(types.values())
exp = N / 3
chi2 = sum((types[k] - exp) ** 2 / exp for k in (3, 6, 9))

print(f"LIMIT = {LIMIT}")
print(f"twin pairs (p > 3): N = {N}")
print(f"identity violations: {violations}   (theorem predicts 0)")
print(f"type (2,3,4) [mid DR 3]: {types[3]}")
print(f"type (5,6,7) [mid DR 6]: {types[6]}")
print(f"type (8,9,1) [mid DR 9]: {types[9]}")
print(f"equidistribution: chi2 = {chi2:.2f} on df = 2")
sys.exit(0 if violations == 0 else 1)
