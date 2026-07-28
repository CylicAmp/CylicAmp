"""
c0_emirp_class.py — emirp DR classes are reversal-closed; C0 = DR 1.

THEOREM T2 (identity). Digit reversal preserves the digit sum, hence
  rev(n) ≡ n (mod 9). Therefore every emirp pair (p, rev p) shares its
  digital root, hence its chi_{-3} value, hence its splitting behavior in
  Z[omega]: both split (DR ∈ {1,4,7}) or both inert (DR ∈ {2,5,8}).
  In particular every C0 pair (DR = 1) is split–split, so BOTH members are
  representable as p = x^2 + xy + y^2 (Eisenstein/Loeschian norm form).
  DR = 1 means p ≡ 1 (mod 9): trivial Frobenius at level 9, i.e. C0 primes
  split completely in Q(zeta_9).

THEOREM T2' (mod-11 frame). With L = digit count,
  rev(n) ≡ (-1)^(L-1) · n (mod 11):
  odd-length emirp pairs share their mod-11 residue; even-length pairs negate it.
PROOF. n ≡ alternating digit sum (mod 11) since 10 ≡ -1; reversal multiplies
  the alternating sum by (-1)^(L-1). QED.

NO ANALOGUE MOD 37. Reversal obeys no uniform twist mod 37 (e.g. 100 ≡ 26 but
  rev(100)=1), and by CRT the mod-37 residue is independent of DR. Identities
  live on the 9/11 side; the 37 frame carries empirical content only.

BASELINE. The correct null for emirp DR statistics is not "all primes" but
  candidates: non-palindromic primes with leading digit in {1,3,7,9}
  (the trailing digit of any prime > 5 is automatically in that set).
"""
import math, sys
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

def eisenstein_witness(p):
    """p prime, p ≡ 1 mod 3  ->  (x, y) with x^2 + xy + y^2 = p."""
    for x in range(math.isqrt(p) + 1):
        d = 4 * p - 3 * x * x
        if d < 0:
            break
        s = math.isqrt(d)
        if s * s == d and (s - x) % 2 == 0:
            return (x, (s - x) // 2)
    return None

S = sieve(LIMIT)
LEAD = set('1379')
cand, edr, pair_mat = Counter(), Counter(), Counter()
v_dr = v_chi = v_11 = 0
Ne = 0
c0 = []

for p in range(11, LIMIT + 1):
    if not S[p]:
        continue
    s = str(p)
    if s[0] not in LEAD:
        continue
    r = int(s[::-1])
    if r == p:
        continue
    cand[dr(p)] += 1
    if r <= LIMIT and S[r]:
        Ne += 1
        edr[dr(p)] += 1
        pair_mat[(dr(p), dr(r))] += 1
        if dr(p) != dr(r):            v_dr += 1   # provably unreachable
        if chi3(p) != chi3(r):        v_chi += 1  # provably unreachable
        if len(s) % 2 == 1:
            if (p - r) % 11: v_11 += 1            # provably unreachable
        else:
            if (p + r) % 11: v_11 += 1            # provably unreachable
        if dr(p) == 1 and p < r:
            c0.append((p, r))

Nc = sum(cand.values())
classes = (1, 2, 4, 5, 7, 8)
chi2_base = sum((edr[k] - Ne * cand[k] / Nc) ** 2 / (Ne * cand[k] / Nc) for k in classes)
off_diag = sum(v for (a, b), v in pair_mat.items() if a != b)

print(f"LIMIT = {LIMIT}")
print(f"candidates = {Nc}, emirps = {Ne}")
print(f"violations: DR = {v_dr}, chi3 = {v_chi}, mod-11 law = {v_11}, "
      f"off-diagonal (DRp, DRrev) mass = {off_diag}   (theorems predict all 0)")
print("emirp DR shares vs candidate baseline:")
for k in classes:
    print(f"  DR {k}: {edr[k]:>8}  {edr[k]/Ne:.4f}   baseline {cand[k]/Nc:.4f}")
print(f"chi2 vs baseline = {chi2_base:.2f} on df = 5")
print(f"C0 class (DR = 1): {edr[1]} emirps, {len(c0)} unordered pairs")
print("first C0 pairs with Eisenstein witnesses (both members split, both Loeschian):")
for a, b in c0[:6]:
    wa, wb = eisenstein_witness(a), eisenstein_witness(b)
    print(f"  ({a}, {b}):  {a} = {wa[0]}^2+{wa[0]}*{wa[1]}+{wa[1]}^2 ,  "
          f"{b} = {wb[0]}^2+{wb[0]}*{wb[1]}+{wb[1]}^2")
sys.exit(0 if v_dr == v_chi == v_11 == 0 else 1)
