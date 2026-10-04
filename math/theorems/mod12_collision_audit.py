"""
mod12_collision_audit.py

Audits claims from the categorical operator / reflective lattice framework:

  1. f(node) = node mod 12 — collision condition
  2. State count formula: 2k - c
  3. Axis 2310 = P₅# fold map
  4. 12-cycle motif structure and primorial axis invariant
  5. Categorical functor framing
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'primes'))
from prime_engine import is_prime, digital_root
from math import gcd

# ---------------------------------------------------------------------------
# 1.  f(node) = node mod 12: collision condition
# ---------------------------------------------------------------------------
print("="*62)
print("1.  Collision condition: d ≡ 0 (mod 6)")
print("="*62)
print("""
  f(a-d) = f(a+d)
  ↔ (a-d) ≡ (a+d)  (mod 12)
  ↔ -2d ≡ 0         (mod 12)
  ↔ 2d ≡ 0          (mod 12)
  ↔ d ≡ 0           (mod 6)

  PROVEN ✓  Collision occurs exactly when 6 | d.
""")

# Verify to d=99
mismatches = [(d, (30-d)%12==(30+d)%12, d%6==0)
              for d in range(1, 100)
              if ((30-d)%12==(30+d)%12) != (d%6==0)]
print(f"  Verification d=1..99: mismatches = {len(mismatches)}  (expected 0)")

# Show collision table at axis=30
print(f"\n  Collision map at axis=30, d=1..13:")
print(f"  {'d':>3}  {'a-d':>4}  {'(a-d)%12':>9}  {'a+d':>4}  {'(a+d)%12':>9}  collision  6|d")
for d in range(1, 14):
    lo, hi = 30-d, 30+d
    fl, fh = lo%12, hi%12
    coll = fl == fh
    d6 = d%6==0
    print(f"  {d:>3}  {lo:>4}  {fl:>9}  {hi:>4}  {fh:>9}  {str(coll):>9}  {str(d6):>3}")

# ---------------------------------------------------------------------------
# 2.  State count formula 2k - c
# ---------------------------------------------------------------------------
print()
print("="*62)
print("2.  State count formula: 2k - c")
print("="*62)
print("""
  Formula: unique axiom states = 2k - c
  where k = number of folds, c = number of INTRA-PAIR collisions.

  An intra-pair collision: f(a-d) = f(a+d), i.e., d ≡ 0 (mod 6).
  These are the collisions the formula accounts for.

  LIMITATION: the formula omits CROSS-FOLD collisions,
  where different folds d_i ≠ d_j produce the same label.
  These further reduce unique states and are not counted by c.
""")

# Demonstrate with P3#=30 triple fold
axis = 30
folds_d = [1, 11, 13]
nodes = [(axis - d, axis + d) for d in folds_d]
all_nodes = [n for pair in nodes for n in pair]
labels = [n % 12 for n in all_nodes]
k = len(folds_d)
intra_c = sum(1 for lo, hi in nodes if lo%12 == hi%12)
unique_actual = len(set(labels))
formula_val = 2*k - intra_c

print(f"  Axis=30, folds d={folds_d}:")
for (lo, hi), d in zip(nodes, folds_d):
    print(f"    d={d:>2}: ({lo},{hi}) labels ({lo%12},{hi%12})")
print(f"  k={k}, intra-collisions c={intra_c}")
print(f"  Formula 2k-c = {formula_val}")
print(f"  Actual unique labels = {unique_actual}  (labels = {sorted(set(labels))})")
print(f"  DISCREPANCY = {formula_val - unique_actual}  (from cross-fold collisions)")

cross = [(all_nodes[i], all_nodes[j], labels[i])
         for i in range(len(all_nodes))
         for j in range(i+1, len(all_nodes))
         if labels[i]==labels[j] and i//2 != j//2]
print(f"  Cross-fold collisions: {[(a,b) for a,b,l in cross]}  all at labels {sorted(set(l for _,_,l in cross))}")

print(f"""
  CORRECTED FORMULA:
  Unique states = 2k - c_intra - c_cross
  where c_cross = number of additional label merges from cross-fold hits.

  For the P₃#=30 triple: c_intra=0, c_cross=4 → unique = 6 - 0 - 4 = 2.
  Confirmed: only labels {{5,7}} appear (all six nodes map to just two axioms).

  INTERNAL DOCUMENT NOTE:
  The "collision at axiom 5" for the pair (17,43) is a cross-fold collision:
    17 mod 12 = 5 = 29 mod 12 = 41 mod 12  (three nodes → one label).
    43 mod 12 = 7 = 31 mod 12 = 19 mod 12  (three nodes → one label).
  Not an intra-pair collision — (17,43) give labels 5 and 7 (no intra-collision).

  STATUS: Formula valid for intra-pair collisions only.
          Cross-fold collisions require inclusion-exclusion over all pairs.
""")

# ---------------------------------------------------------------------------
# 3.  Axis 2310 = P₅#
# ---------------------------------------------------------------------------
print("="*62)
print("3.  Axis 2310 = P₅# = 2×3×5×7×11")
print("="*62)

axis = 2310
print(f"\n  2310 mod 12 = {axis % 12}")
print(f"\n  THEOREM: All primorials Pₙ# ≥ P₃# have axis ≡ 6 (mod 12).")
print(f"  PROOF: P₃# = 30. For n≥3: Pₙ# = 30 × m (m odd, since 2 and 5")
print(f"  are already in P₃# but the additional primes 7,11,... are odd).")
print(f"  30m mod 12 = 6m mod 12. m odd → 6m ≡ 6 (mod 12). ∎")
print()

primorials = [(30,'P3#'),(210,'P4#'),(2310,'P5#'),(30030,'P6#')]
for p, name in primorials:
    m = p // 30
    parity = 'odd' if m%2 else 'even'
    print(f"  {name} = 30×{m} (m {parity}) → mod12 = {p%12}")

print(f"\n  Fold distances d=1,11,13 at axis 2310:")
print(f"  {'d':>4}  {'lo':>6}  {'hi':>6}  {'prime(lo)':>10}  {'prime(hi)':>10}  {'twin?':>6}  {'lo%12':>6}  {'hi%12':>6}  DR")
for d in [1, 11, 13]:
    lo, hi = axis - d, axis + d
    pl, ph = is_prime(lo), is_prime(hi)
    twin = pl and ph
    dr1, dr2 = digital_root(lo), digital_root(hi)
    print(f"  {d:>4}  {lo:>6}  {hi:>6}  {str(pl):>10}  {str(ph):>10}  {str(twin):>6}  {lo%12:>6}  {hi%12:>6}  ({dr1},{dr2})")

print(f"""
  d=1: (2309, 2311) — TWIN PRIME PAIR, DR=(5,7), mod12=(5,7) ✓
  d=11: (2299, 2321) — neither prime
  d=13: (2297, 2323) — 2297 prime, 2323=23×101 composite

  P₅# does NOT reproduce the full P₃# 6-element constellation.
  Only the d=1 fold (twin prime center) works at 2310.
  The d=11 and d=13 folds fail.

  This matches the earlier finding: P₃# is a special cluster,
  not a pattern that scales to all primorials.
""")

# Twin prime pairs near 2310
print(f"  Twin prime pairs within d ≤ 30 of axis 2310:")
for d in range(1, 31):
    lo, hi = axis-d, axis+d
    if is_prime(lo) and is_prime(hi):
        print(f"    d={d:>3}: ({lo},{hi})  DR=({digital_root(lo)},{digital_root(hi)})  mod12=({lo%12},{hi%12})")

# ---------------------------------------------------------------------------
# 4.  12-cycle motif
# ---------------------------------------------------------------------------
print()
print("="*62)
print("4.  12-cycle motif: (Z/12Z)× and primorial axis")
print("="*62)
print(f"""
  Positions in Z/12Z that are prime-allowed: gcd(r,12) = 1
    (Z/12Z)× = {{1, 5, 7, 11}}   φ(12) = 4 positions

  All other positions are composite-forced:
    {{0,2,3,4,6,8,9,10}} — divisible by 2 or 3.

  Primorial axis: always at position 6 (non-prime, gcd(6,12)=6).
  The ±1 fold from any primorial axis always lands at positions 5 and 7
  — both in (Z/12Z)×, both prime-allowed.

  The 12-cycle and the 9-cycle (Z/9Z from DR) both classify the same
  set of prime-allowed integers. Their intersection:
""")

z9_prime = {1,2,4,5,7,8}   # (Z/9Z)×
z12_prime = {r for r in range(12) if gcd(r,12)==1}  # (Z/12Z)×

print(f"  (Z/9Z)×  = {sorted(z9_prime)}")
print(f"  (Z/12Z)× = {sorted(z12_prime)}")
print()
print(f"  Combined filter (mod 36 = lcm(9,12)):")
print(f"  n prime-possible ↔ gcd(n,36)=1 ↔ gcd(n,9)=1 AND gcd(n,12)=1")
allowed_36 = [r for r in range(36) if gcd(r,36)==1]
print(f"  (Z/36Z)× = {allowed_36}  (φ(36) = {len(allowed_36)} positions out of 36)")

# ---------------------------------------------------------------------------
# 5.  Categorical functor
# ---------------------------------------------------------------------------
print()
print("="*62)
print("5.  Categorical operator framework")
print("="*62)
print("""
  CLAIM: The reflective lattice is a functor F: Lat → Lat.
  Objects: lattices with 12-cycle motif and primorial axis labels.
  Morphisms: reflection rules (lattice state → next state).
  F(L) = one step of the reflective operator.
  Composition of morphisms = iterated reflection.

  IS THIS WELL-DEFINED?

  Yes, IF morphisms are total functions L → L (which they are
  if the reflection rule is explicitly defined for every state).
  The categorical language is correctly applied.

  THE FIXED POINT:
  F(L*) = L* requires:
    v* (state vector) generates overlap O* = overlap(v*, motif)
    O* generates coupling λ* = coupling_rule(O*)
    λ* applied to v* regenerates v* (self-sustaining)

  This is a FIXED POINT EQUATION, not a theorem.
  It asserts existence of a self-sustaining state — unproven here.
  In dynamical systems this is a fixed point of the iteration map.
  Existence requires either a contraction mapping argument (Banach)
  or explicit construction.

  WHAT IS VERIFIED:
    The categorical language is correctly applied.
    The composition F∘F∘...∘F = Fⁿ is well-defined iterated reflection.
    The fixed point equation is correctly stated.

  WHAT IS NOT PROVEN:
    Existence of the fixed point (v*, O*, λ*).
    Whether the iteration converges to this fixed point.
    What the fixed point represents physically or number-theoretically.

  STATUS: Framework correctly formulated; fixed point existence unproven.
""")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("="*62)
print("SUMMARY")
print("="*62)
print(f"""
  Claim                                       Status
  ----------------------------------------------------------------
  f(n) = n mod 12                             WELL-DEFINED ✓
  Collision ↔ d ≡ 0 (mod 6)                  PROVEN ✓
  State count = 2k - c (intra-pair c)         PROVEN for intra-pair only
    Cross-fold collisions omitted             CORRECTION NEEDED
    Example: P₃# triple → formula says 6,
             actual unique labels = 2
  "Collision at axiom 5 for (17,43)"          MISIDENTIFIED
    (17,43) give labels 5 and 7 — no pair collision
    Actual: 3-way cross-fold: 17,29,41 → all label 5
  All primorials P3#+ have axis ≡ 6 (mod 12) PROVEN ✓
    (Z/12Z)× = {{1,5,7,11}}, axis at 6, ±1 fold at 5,7 ✓
  P₅# = 2310 has d=1 twin pair (2309,2311)   CORRECT ✓  DR=(5,7)
  P₅# does NOT reproduce full 6-element
    P₃# constellation at d=11,13             CONFIRMED ✗
  Categorical functor correctly stated        CORRECT FORMULATION ✓
  Fixed point (v*, O*, λ*) exists             UNPROVEN — needs existence proof
""")
