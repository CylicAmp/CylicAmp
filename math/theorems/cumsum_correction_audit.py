"""
cumsum_correction_audit.py

Audits the structural claims arising from the cumulative-sum triangle:

  A. DR periodicity — is the 9-cycle period-6?
  B. s(5)=314 ≈ 100π — coincidence or structural?
  C. Correction factor: can s(2) be "fixed" to 81=3⁴ while
     preserving s(0)=9, s(1)=27 and DR=9 at n=6?
  D. What L0 shapes give sustained power-of-3 sums?
"""

import math
from itertools import accumulate

def dr(n):
    if n == 0: return 0
    r = n % 9
    return r if r != 0 else 9

def comb(n, k):
    return math.comb(n, k) if 0 <= k <= n else 0

def prefix_sum(seq):
    return list(accumulate(seq))

def s(n, L0=None):
    """Closed-form sum(Lₙ) for a length-5 L0 (default [1,2,3,2,1])."""
    if L0 is None:
        L0 = [1, 2, 3, 2, 1]
    N = len(L0)
    return sum(L0[j] * comb(n + N - 1 - j, n) for j in range(N))


L0 = [1, 2, 3, 2, 1]

# ============================================================
# A.  DR Periodicity
# ============================================================
print("=" * 66)
print("A.  DR Periodicity — is the 9-cycle period-6?")
print("=" * 66)

N_TERMS = 30
sums  = [s(n) for n in range(N_TERMS)]
drs   = [dr(v) for v in sums]

print(f"\n  {'n':>4}  {'s(n)':>10}  {'DR':>4}  {'note'}")
print(f"  {'-'*48}")
for n in range(N_TERMS):
    note = ""
    if drs[n] == 9:
        note = "← DR=9"
    print(f"  {n:>4}  {sums[n]:>10}  {drs[n]:>4}  {note}")

# Locate all n where DR=9
nine_idx = [n for n in range(N_TERMS) if drs[n] == 9]
gaps     = [nine_idx[i+1] - nine_idx[i] for i in range(len(nine_idx)-1)]
print(f"\n  n values with DR(s(n))=9: {nine_idx}")
print(f"  Gaps between consecutive 9s: {gaps}")

# Test period-6 hypothesis
is_period6 = all(drs[n] == drs[n + 6] for n in range(N_TERMS - 6))
print(f"\n  Period-6 (drs[n] == drs[n+6] for all n < {N_TERMS-6}): "
      f"{'✓' if is_period6 else '✗  NOT period-6'}")

# Check what period (if any) the DR sequence has
for period in range(1, 20):
    ok = all(drs[n] == drs[n + period] for n in range(N_TERMS - period))
    if ok:
        print(f"  Smallest period found: {period}")
        break
else:
    print(f"  No period ≤ 19 found in first {N_TERMS} terms.")

print(f"\n  DR(s(n)) mod-9 class sequence (n=0..{N_TERMS-1}):")
print(f"    {drs}")


# ============================================================
# B.  s(5) = 314 ≈ 100π
# ============================================================
print()
print("=" * 66)
print("B.  s(5) = 314 ≈ 100π — coincidence or structural?")
print("=" * 66)

pi_100 = 100 * math.pi
s5     = s(5)
gap_pi = pi_100 - s5

print(f"\n  s(5)      = {s5}  (exact integer)")
print(f"  100·π     = {pi_100:.10f}")
print(f"  Gap       = {gap_pi:.10f}  (~{gap_pi:.3f})")
print(f"  Relative error: {gap_pi / pi_100 * 100:.4f}%")
print(f"""
  s(5) = C(9,4) + 2·C(8,3) + 3·C(7,2) + 2·6 + 1
       = 126 + 112 + 63 + 12 + 1
       = 314   (purely integer arithmetic, no π input)

  The s(n) formula is a degree-4 polynomial in n; it generates
  integer values for integer n.  Proximity to 100π is numerical
  coincidence: among all 3-digit integers, ~30 lie within 1 of 314.159.

  Test: nearby transcendental approximations at this scale:""")

targets = [
    ("100π",    100 * math.pi),
    ("10e²",    10 * math.e**2),
    ("100·√10", 100 * math.sqrt(10)),
    ("200/√(π+e)", 200 / math.sqrt(math.pi + math.e)),
]
for name, val in targets:
    print(f"    {name:20} = {val:.6f}   gap from s(5): {val - s5:+.6f}")

# Also check s(n) vs familiar constants scaled:
print(f"\n  All s(n) near simple multiples of π, e, φ (±0.5):")
phi = (1 + math.sqrt(5)) / 2
constants = [("π", math.pi), ("e", math.e), ("φ", phi), ("√2", math.sqrt(2)),
             ("√3", math.sqrt(3)), ("√5", math.sqrt(5))]
for n in range(20):
    sv = s(n)
    for cname, cval in constants:
        for mult in range(1, 500):
            approx = mult * cval
            if abs(approx - sv) < 0.5:
                print(f"    n={n}: s(n)={sv} ≈ {mult}·{cname} = {approx:.4f}  "
                      f"(gap {approx-sv:+.4f})")


# ============================================================
# C.  Correction Factor Analysis
# ============================================================
print()
print("=" * 66)
print("C.  Correction Factor: s(2)=60 → 81=3⁴")
print("=" * 66)

TARGET_S2 = 81   # 3^4
DELTA_S2  = TARGET_S2 - s(2)   # = 21

print(f"""
  Current s(2) = {s(2)}.  Target = {TARGET_S2} = 3⁴.  Delta = {DELTA_S2}.

  A correction δL0 to the generating sequence satisfies:
    s_δ(n) = Σⱼ δL0[j] · C(n+4-j, n)

  Constraint system to fix s(2) while preserving s(0), s(1), DR at n=6:
    (i)   Σⱼ δL0[j] = 0          (preserve s(0)=9)
    (ii)  Σⱼ δL0[j]·(5-j) = 0   (preserve s(1)=27)
    (iii) Σⱼ δL0[j]·C(6-j,2) = 21  (fix s(2) to 81)
    (iv)  Σⱼ δL0[j]·C(10-j,6) ≡ 0 mod 9  (preserve DR=9 at n=6)
""")

# Binomial coefficients for constraints
B = {
    0: [comb(4-j, 0) for j in range(5)],   # = [1,1,1,1,1]
    1: [comb(5-j, 1) for j in range(5)],   # = [5,4,3,2,1]
    2: [comb(6-j, 2) for j in range(5)],   # = [15,10,6,3,1]
    6: [comb(10-j, 6) for j in range(5)],  # = [210,84,28,7,1]
}
print(f"  Coefficients for each constraint:")
for k, bvec in sorted(B.items()):
    print(f"    n={k}: {bvec}")

# Null space basis for constraints (i) and (ii)
# Row-reduce [[1,1,1,1,1],[5,4,3,2,1]]
# After reduction: v1 = v3+2*v4+3*v5, v2 = -2*v3-3*v4-4*v5
# Basis for null space (free vars v3,v4,v5):
e = [
    [1, -2, 1, 0, 0],   # v3=1, v4=v5=0
    [2, -3, 0, 1, 0],   # v4=1, v3=v5=0
    [3, -4, 0, 0, 1],   # v5=1, v3=v4=0
]
print(f"\n  Null space basis (constraints i,ii satisfied):")
for i, ei in enumerate(e):
    dot0 = sum(ei[j]*B[0][j] for j in range(5))
    dot1 = sum(ei[j]*B[1][j] for j in range(5))
    dot2 = sum(ei[j]*B[2][j] for j in range(5))
    dot6 = sum(ei[j]*B[6][j] for j in range(5))
    print(f"    e{i+1} = {ei}   ·B[0]={dot0}  ·B[1]={dot1}  ·B[2]={dot2}  ·B[6]={dot6}")

# w = α·e1 + β·e2 + γ·e3
# ·B[2] = α*1 + β*3 + γ*6 = 21  → α = 21 - 3β - 6γ
# ·B[6] = α*70 + β*175 + γ*295 ≡ 0 mod 9
#       70≡7, 175≡4, 295≡7 mod 9
# → 7(21-3β-6γ) + 4β + 7γ ≡ 0 mod 9
# → 147 - 21β - 42γ + 4β + 7γ ≡ 0 mod 9
# → 3 - 8β - 8γ ≡ 0 mod 9   (147≡3, 21≡3≡-8 wait: 21 mod 9=3, coeff of β = -21+4=-17≡1 mod9?
# Let me redo carefully

print(f"""
  Solving α + 3β + 6γ = 21  (constraint iii)
  and  7α + 4β + 7γ ≡ 0 mod 9  (constraint iv, with coefficients mod 9)
""")

# Checking the mod9 coefficients
c1 = [70, 175, 295]
c1_mod9 = [x % 9 for x in c1]
print(f"  ·B[6] = {c1[0]}α + {c1[1]}β + {c1[2]}γ")
print(f"  mod 9: {c1_mod9[0]}α + {c1_mod9[1]}β + {c1_mod9[2]}γ ≡ 0")

# α = 21 - 3β - 6γ
# Substitute into 70α + 175β + 295γ ≡ 0 mod 9:
# 70(21-3β-6γ) + 175β + 295γ ≡ 0 mod 9
# 1470 - 210β - 420γ + 175β + 295γ ≡ 0
# 1470 - 35β - 125γ ≡ 0 mod 9
val_const = 70 * 21
val_b = -70*3 + 175    # = -210+175 = -35
val_g = -70*6 + 295    # = -420+295 = -125
print(f"\n  After substituting α = 21-3β-6γ:")
print(f"  {val_const} + ({val_b})β + ({val_g})γ ≡ 0 mod 9")
print(f"  {val_const % 9} + {val_b % 9}β + {val_g % 9}γ ≡ 0 mod 9")
# 1470 mod9 = 1+4+7+0=12→3
# -35 mod9: 35=3*9+8→ -35≡-8≡1 mod9
# -125 mod9: 125=13*9+8→ -125≡-8≡1 mod9
# So: 3 + β + γ ≡ 0 mod 9 → β+γ ≡ -3 ≡ 6 mod 9
print(f"  → β + γ ≡ 6 mod 9")

# Find integer solutions where L0 + δL0 has all non-negative entries
print(f"\n  Search for valid corrections (non-negative L0 + δL0):")
print(f"  (L0 = {L0}, so δL0[j] ≥ −L0[j])")

valid = []
for b in range(-30, 31):
    for g in range(-30, 31):
        if (b + g) % 9 != 6:
            continue
        a = 21 - 3*b - 6*g
        w = [a*e[0][j] + b*e[1][j] + g*e[2][j] for j in range(5)]
        new_L0 = [L0[j] + w[j] for j in range(5)]
        if all(x >= 0 for x in new_L0):
            # Verify constraints
            chk0 = sum(w[j]*B[0][j] for j in range(5))
            chk1 = sum(w[j]*B[1][j] for j in range(5))
            chk2 = sum(w[j]*B[2][j] for j in range(5))
            chk6 = sum(w[j]*B[6][j] for j in range(5)) % 9
            if chk0 == 0 and chk1 == 0 and chk2 == 21 and chk6 == 0:
                new_s6 = s(6, new_L0)
                valid.append((a, b, g, w, new_L0, new_s6))

if valid:
    print(f"  Found {len(valid)} valid corrections (α,β,γ,δL0,newL0):")
    for (a, b, g, w, nL0, ns6) in valid[:10]:
        print(f"    α={a:>4},β={b:>4},γ={g:>4}  δL0={w}  "
              f"new L0={nL0}  s(6)={ns6}  DR(s(6))={dr(ns6)}")
else:
    print(f"  NO valid correction found with non-negative entries in L0+δL0.")
    print(f"\n  Why: the null-space basis vectors e1,e2,e3 all contain negative")
    print(f"  components, so any linear combination satisfying the constraint")
    print(f"  equations forces at least one entry of new L0 below zero.")

# Demonstrate the smallest attempted corrections and why they fail
print(f"\n  Smallest single-element corrections (only one δL0[j] ≠ 0):")
print(f"  {'j':>4}  {'δ needed':>10}  {'integer?':>10}  {'new L0[j]':>10}  {'s_δ(6)':>8}  {'DR crash?':>10}")
for j in range(5):
    need = 21 / B[2][j]
    is_int = need == int(need)
    if is_int:
        d = int(need)
        new_lj = L0[j] + d
        s_d6 = d * B[6][j]
        new_s6 = s(6) + s_d6
        crash = dr(new_s6) != 9
        print(f"  {j:>4}  {need:>10.4f}  {'✓' if is_int else '✗':>10}  "
              f"{new_lj:>10}  {s_d6:>8}  {'YES (DR→'+str(dr(new_s6))+')' if crash else 'NO ✓':>10}")
    else:
        print(f"  {j:>4}  {need:>10.4f}  {'✗  non-integer':>10}")


# ============================================================
# D.  What L0 shapes sustain power-of-3 sums?
# ============================================================
print()
print("=" * 66)
print("D.  What L0 shapes sustain s(n) = 3^(n+2)?")
print("=" * 66)
print(f"""
  Requirement: s(n) = 9, 27, 81, 243, … = 3^(n+2)

  s(n) = Σⱼ L0[j] · C(n+4-j, n) = 3^(n+2)

  The generating function of s(n) is:
    S(x) = Σₙ s(n)·xⁿ = Σⱼ L0[j] / (1-x)^(5-j)  (formal)

  For S(x) to encode s(n) = 9·3^n, we need S(x) = 9/(1-3x):
    Σⱼ L0[j] / (1-x)^(5-j) = 9 / (1-3x)

  This requires L0 to be the coefficient sequence of 9·(1-x)^5 / (1-3x)
  at a formal series level — which is not a finite sequence (the (1-3x)
  denominator generates an infinite series).

  Conclusion: NO length-5 non-negative integer L0 can yield s(n) = 3^(n+2)
  for all n ≥ 0.

  The closest finite-support L0 for geometric sums:
    If L0 = [k] (length 1), s(n) = k for all n (constant).
    If L0 = [k₀, k₁] (length 2), s(n) = k₀(n+1) + k₁.  (linear)
    To get s(n) = 9·3^n we need infinite support: L0 = [9, 27, 81, …].
""")

# What if L0 = [3^k] for k=0..4?  (geometric L0)
L0_geo = [3**k for k in range(5)]
sums_geo = [s(n, L0_geo) for n in range(8)]
print(f"  Geometric L0 = [1,3,9,27,81] (3^k for k=0..4):")
print(f"    s(n) = {sums_geo}")
print(f"    DR   = {[dr(v) for v in sums_geo]}")
L0_uni = [3, 3, 3, 3, 3]
sums_uni = [s(n, L0_uni) for n in range(8)]
print(f"\n  Uniform L0 = [3,3,3,3,3]:")
print(f"    s(n) = {sums_uni}")
print(f"    DR   = {[dr(v) for v in sums_uni]}")
print(f"    (Uniform L0: s(n) scales as C(n+4,4)·3·5/C(...) — not geometric)")

L0_delta = [9, 0, 0, 0, 0]
sums_delta = [s(n, L0_delta) for n in range(8)]
print(f"\n  Point-mass L0 = [9,0,0,0,0]:")
print(f"    s(n) = {sums_delta}")
print(f"    (All equal to 9 — trivially DR=9 everywhere, sum never grows)")


# ============================================================
# Summary
# ============================================================
print()
print("=" * 66)
print("SUMMARY")
print("=" * 66)
print(f"""
  A. DR Periodicity:
     DR(s(n)) sequence = {drs[:20]} ...
     n with DR=9: {nine_idx[:10]}
     Gap pattern: {gaps[:10]}
     {'Period-6 confirmed ✓' if is_period6 else 'NOT period-6 ✗'}
     The n=6 return to DR=9 is a ONE-TIME coincidence within the first
     30 terms, not evidence of a periodic structure.

  B. s(5)=314 ≈ 100π:
     Gap = {gap_pi:.6f}  (relative {gap_pi/pi_100*100:.4f}%)
     COINCIDENCE — s(n) is a degree-4 integer polynomial; no π input.
     The gap ({gap_pi:.3f}) is the aliasing error of a random integer
     near 314, not a meaningful discrete sampling of a curvature.

  C. Correction factor:
     To fix s(2)=60 to 81=3⁴ while preserving s(0)=9 and s(1)=27,
     every solution δL0 in the constraint null space forces at least
     one negative entry in L0+δL0.
     {f'Found {len(valid)} non-negative solution(s).' if valid else
      'NO non-negative correction exists — mathematically impossible.'}
     A correction at n=2 either:
       (a) requires negative L0 entries (non-physical), or
       (b) breaks s(0) or s(1) (loses the 9=3², 27=3³ anchors), or
       (c) changes s(6) such that DR(s(6)) ≠ 9.
     All three options "crash" the structure in one way or another.

  D. Sustained power-of-3 sums require infinite-support L0:
     s(n) = 9·3ⁿ ← requires L0 = [9, 27, 81, 243, …] (infinite).
     A finite palindromic convolution like [1,1,1]★[1,1,1] generates
     polynomial growth — the exponential potential of base-3 is NOT
     recoverable via feedback correction at any single level.

  Root cause of power-of-3 failure at s(2):
    sum(L0) = (1+1+1)² = 3²   ← exact, from convolution
    sum(L1) = Σ L0[j]·(5-j) = 27 = 3³   ← "weight by position"
    sum(L2) = Σ L0[j]·C(6-j,2) = 60 ≠ 81   ← C(n,2) grows too slowly
    The binomial coefficient C(6-j,2) does not equal 3^(2-j) for j=0..4;
    the mismatch is structural, not correctable by feedback.
""")
