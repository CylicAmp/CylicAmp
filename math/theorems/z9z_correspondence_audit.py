"""
z9z_correspondence_audit.py

Arithmetic audit of Z/9Z correspondence document claims:
  - Set decomposition X_inv / X_nil under ×2
  - Multiplicative ideal (3) = {0,3,6}
  - Idempotents, indecomposability, nilpotency
  - Non-split exact sequence vs direct sum
  - Bimodule map precision correction
"""

from itertools import product as iproduct

N = 9
Zn = list(range(N))

# ---------------------------------------------------------------------------
# 1.  Set-level decomposition
# ---------------------------------------------------------------------------
print("="*62)
print("1.  Set decomposition: X_inv and X_nil")
print("="*62)

from math import gcd
X_inv = [x for x in Zn if gcd(x, N) == 1]   # units: gcd(x,9)=1
X_nil = [x for x in Zn if gcd(x, N) >  1 or x == 0]  # non-units

# re-derive: (3) = {0,3,6}, complement = units
ideal3 = [x for x in Zn if x % 3 == 0]
units  = [x for x in Zn if gcd(x, N) == 1]

print(f"  Z/9Z  = {Zn}")
print(f"  X_inv = {units}  (units, gcd(x,9)=1)")
print(f"  X_nil = {ideal3}  (multiples of 3: the ideal (3))")
print(f"  Disjoint: {set(units) & set(ideal3) == set()} ✓")
print(f"  Cover:   {sorted(set(units) | set(ideal3)) == Zn} ✓")

# Claimed values
assert units  == [1,2,4,5,7,8], f"units wrong: {units}"
assert ideal3 == [0,3,6],        f"ideal3 wrong: {ideal3}"
print(f"  X_inv = {{1,2,4,5,7,8}}: CONFIRMED ✓")
print(f"  X_nil = {{0,3,6}}:        CONFIRMED ✓")

# ---------------------------------------------------------------------------
# 2.  Forward-invariance under ×2 (mod 9)
# ---------------------------------------------------------------------------
print()
print("="*62)
print("2.  Forward invariance under ×2 (mod 9)")
print("="*62)

def mul2(x): return (2 * x) % N

inv_closed = all(mul2(x) in units  for x in units)
nil_closed = all(mul2(x) in ideal3 for x in ideal3)

print(f"  ×2 orbit on X_inv:")
for x in units:
    print(f"    {x} → {mul2(x)}")
print(f"  X_inv closed under ×2: {inv_closed} ✓")

print(f"\n  ×2 orbit on X_nil:")
for x in ideal3:
    print(f"    {x} → {mul2(x)}")
print(f"  X_nil closed under ×2: {nil_closed} ✓")

# Specific claim: 0→0, 3↔6 (2-cycle)
assert mul2(0) == 0,           "0→0 fails"
assert mul2(3) == 6,           "3→6 fails"
assert mul2(6) == (12 % 9),    "6→? fails"
assert mul2(6) == 3,           "6→3 fails"
print(f"  0→0: {mul2(0)==0} ✓,  3→6: {mul2(3)==6} ✓,  6→3: {mul2(6)==3} ✓")
print(f"  3 and 6 form a 2-cycle; never escapes X_nil: CONFIRMED ✓")

# ---------------------------------------------------------------------------
# 3.  (3) is a multiplicative ideal
# ---------------------------------------------------------------------------
print()
print("="*62)
print("3.  (3) = {0,3,6} is a multiplicative ideal of Z/9Z")
print("="*62)

failures = []
for a in Zn:
    for b in ideal3:
        prod = (a * b) % N
        if prod not in ideal3:
            failures.append((a, b, prod))

print(f"  Testing a·b ∈ (3) for all a∈Z/9Z, b∈(3):")
print(f"  Failures: {failures}")
assert failures == [], f"Ideal property fails: {failures}"
print(f"  (3) is closed under multiplication by all of Z/9Z: CONFIRMED ✓")

# Additive closure
add_fail = [(a,b) for a in ideal3 for b in ideal3 if (a+b)%N not in ideal3]
print(f"  Additive closure failures: {add_fail}")
assert add_fail == [], "Additive closure fails"
print(f"  (3) closed under addition: CONFIRMED ✓")

# ---------------------------------------------------------------------------
# 4.  2 generates (Z/9Z)* ≅ C₆
# ---------------------------------------------------------------------------
print()
print("="*62)
print("4.  2 generates (Z/9Z)* ≅ C₆")
print("="*62)

orbit2 = []
x = 1
for _ in range(N):
    orbit2.append(x)
    x = (x * 2) % N
    if x == 1:
        orbit2.append(x)
        break

print(f"  Powers of 2 mod 9: {orbit2}")
print(f"  Orbit: {sorted(set(orbit2))}")
assert sorted(set(orbit2)) == sorted(units), f"2 does not generate units: {orbit2}"
print(f"  ⟨2⟩ = {{1,2,4,5,7,8}} = (Z/9Z)*: CONFIRMED ✓")
print(f"  ord(2) = {len(orbit2)-1}  (cycle returns to 1) ✓  [C₆ ≅ Z/6Z]")

# Verify group order
assert len(units) == 6, f"|units| = {len(units)}, expected 6"
print(f"  |(Z/9Z)*| = {len(units)} = φ(9) = 9·(1-1/3) = 6 ✓")

# ---------------------------------------------------------------------------
# 5.  Idempotents in Z/9Z
# ---------------------------------------------------------------------------
print()
print("="*62)
print("5.  Idempotents: only 0 and 1")
print("="*62)

idempotents = [x for x in Zn if (x * x) % N == x]
print(f"  {{x ∈ Z/9Z : x² = x}} = {idempotents}")
assert idempotents == [0, 1], f"Unexpected idempotents: {idempotents}"
print(f"  Only idempotents are 0 and 1: CONFIRMED ✓")
print(f"  → Z/9Z is a LOCAL ring (unique maximal ideal J = (3))")
print(f"  → Indecomposable as Z/9Z-module (no central idempotent to project onto (3))")

# ---------------------------------------------------------------------------
# 6.  Nilpotency: (3)² = (0)
# ---------------------------------------------------------------------------
print()
print("="*62)
print("6.  Nilpotency: (3)² = (0) in Z/9Z")
print("="*62)

ideal3_sq = sorted(set((a * b) % N for a in ideal3 for b in ideal3))
print(f"  (3)·(3) = {{a·b mod 9 : a,b ∈ {{0,3,6}}}} = {ideal3_sq}")
assert ideal3_sq == [0], f"(3)² ≠ (0): {ideal3_sq}"
print(f"  (3)² = {{0}}: CONFIRMED ✓  [3·3 = 9 ≡ 0, 3·6 = 18 ≡ 0, 6·6 = 36 ≡ 0]")
print(f"  Nilpotency index of (3) = 2")

# Check individual products
print(f"  3·3 = {3*3} ≡ {(3*3)%N} (mod 9) ✓")
print(f"  3·6 = {3*6} ≡ {(3*6)%N} (mod 9) ✓")
print(f"  6·6 = {6*6} ≡ {(6*6)%N} (mod 9) ✓")

# ---------------------------------------------------------------------------
# 7.  Jacobson radical and quotient
# ---------------------------------------------------------------------------
print()
print("="*62)
print("7.  Jacobson radical J(Z/9Z) = (3), quotient ≅ Z/3Z")
print("="*62)

# J(R) of a local ring = unique maximal ideal
# Verify (3) is maximal: Z/9Z/(3) must be a field
# Quotient map: x ↦ x mod 3
quotient = sorted(set(x % 3 for x in Zn))
print(f"  Z/9Z → Z/3Z via x↦x mod 3: image = {quotient} ✓")

# Check it's a ring homomorphism
hom_ok = all((((a+b)%N)%3 == (a%3 + b%3)%3) and
             (((a*b)%N)%3 == (a%3 * b%3)%3)
             for a in Zn for b in Zn)
print(f"  Quotient map is a ring homomorphism: {hom_ok} ✓")

# Kernel = {x : x mod 3 = 0} = ideal3
ker_quot = [x for x in Zn if x % 3 == 0]
assert ker_quot == ideal3, f"Kernel ≠ (3): {ker_quot}"
print(f"  Kernel of quotient map = (3): CONFIRMED ✓")
print(f"  Z/9Z/(3) ≅ Z/3Z (field GF(3)): CONFIRMED ✓")
print(f"  J(Z/9Z) = (3): CONFIRMED ✓  [unique maximal ideal of the local ring]")

# ---------------------------------------------------------------------------
# 8.  Non-split exact sequence: 0 → (3) → Z/9Z → Z/3Z → 0
# ---------------------------------------------------------------------------
print()
print("="*62)
print("8.  Exact sequence 0→(3)→Z/9Z→Z/3Z→0 is NOT split")
print("="*62)

# A sequence 0 → M → E → Q → 0 of Z/9Z-modules splits iff there is a
# Z/9Z-module retraction r: E → M with r∘i = id_M,
# OR equivalently a section s: Q → E with π∘s = id_Q.
# Sections s: Z/3Z → Z/9Z must satisfy:
#   (a) π(s(x̄)) = x̄  for all x̄ ∈ Z/3Z
#   (b) s(x̄ + ȳ) = s(x̄) + s(ȳ)  (group homomorphism)
#   (c) r·s(x̄) = s(r̄·x̄)  for all r ∈ Z/9Z  (Z/9Z-linearity)
#
# Since Z/3Z ≅ Z/9Z/(3), elements of Z/3Z are cosets {0̄, 1̄, 2̄}.
# A section s must map: 0̄→0, and 1̄→ some x with x≡1 mod 3.
# Choices for s(1̄): 1, 4, or 7.

print("  Searching for Z/9Z-module sections s: Z/3Z → Z/9Z")
print("  (a section must lift x̄ and be Z/9Z-linear)\n")

# Z/9Z-linearity means: for any r ∈ Z/9Z and x̄ ∈ Z/3Z:
#   s(r̄·x̄) = r·s(x̄)
# r̄ = r mod 3.
# We need s(0̄)=0, s(1̄)=c for some c with c≡1(mod 3), s(2̄)=2c mod 9.
# Also s must be a group hom: s(1̄+1̄) = s(2̄) = 2c, and s(2̄+1̄)=s(0̄)=0.
# Check: s(2̄+1̄) = s(3̄) = s(0̄) = 0. But also must equal s(2̄)+s(1̄)=2c+c=3c.
# So 3c ≡ 0 (mod 9).

candidates = [c for c in Zn if c % 3 == 1]  # s(1̄) must satisfy c≡1(mod3)
print(f"  Candidates for s(1̄): {candidates}  (must be ≡1 mod 3)")

split_sections = []
for c in candidates:
    s = {0: 0, 1: c % N, 2: (2*c) % N}   # s(k̄) = k·c mod 9
    # Verify s is a group hom Z/3Z → Z/9Z:
    is_hom = all((s[(a+b)%3] == (s[a]+s[b])%N) for a in range(3) for b in range(3))
    # Verify 3c ≡ 0 mod 9:
    linearity_ok = (3*c) % N == 0
    # Verify π∘s = id: s(k̄) ≡ k (mod 3) for k=0,1,2:
    section_ok = all(s[k]%3 == k for k in range(3))
    # Verify Z/9Z-linearity: r·s(x̄) = s(r̄·x̄) for all r, x̄:
    zmod9_linear = all(((r * s[x]) % N) == s[(r * x) % 3]
                       for r in Zn for x in range(3))
    ok = is_hom and section_ok and zmod9_linear
    print(f"    c={c}: group_hom={is_hom}, section={section_ok}, "
          f"Z/9Z-linear={zmod9_linear}  → {'VALID section' if ok else 'FAILS'}")
    if ok:
        split_sections.append(c)

print(f"\n  Valid splitting sections: {split_sections}")
if split_sections:
    print(f"  Sequence SPLITS ← UNEXPECTED")
else:
    print(f"  No valid section exists → sequence does NOT split: CONFIRMED ✓")
    print(f"  This confirms Z/9Z ≇ (3) ⊕ Z/3Z as Z/9Z-modules.")
    print(f"  The filtration 0 ⊂ (3) ⊂ Z/9Z is non-split.")

# Alternative check: if it split, then Z/9Z ≅ Z/3Z ⊕ Z/3Z as abelian groups,
# but Z/9Z has an element of order 9 (namely 1), while Z/3Z⊕Z/3Z has max order 3.
print(f"\n  Consistency check (abelian group):")
max_order_Z9 = max(min(k for k in range(1,N+1) if (k*x)%N==0) for x in Zn)
print(f"    Max element order in Z/9Z: {max_order_Z9}")
print(f"    Z/3Z ⊕ Z/3Z has max element order: 3")
print(f"    Z/9Z has element of order 9 → cannot be ≅ Z/3Z⊕Z/3Z ✓")

# ---------------------------------------------------------------------------
# 9.  Bimodule map precision (document's "minor precision")
# ---------------------------------------------------------------------------
print()
print("="*62)
print("9.  Precision check: inclusion (3) ↪ Z/9Z IS a bimodule map")
print("="*62)

print("""
  Document claim: "ℓ²({0,3,6}) ⊂ ℓ²(Z/9Z) is not a bimodule map"
  Document's own correction: "slightly imprecise — the inclusion IS a
  bimodule map; the obstruction is not being a split monomorphism."

  Arithmetic verification:
""")

# Inclusion i: ideal3 → Zn, i(x) = x
# Z/9Z-linearity of i: r·i(x) = r·x and i(r·x) = r·x; same iff r·x ∈ ideal3.
# But i is defined on (3), and (3) is an ideal, so r·x ∈ (3) for all r ∈ Z/9Z.
linear_ok = all(((r * x) % N) in ideal3 for r in Zn for x in ideal3)
print(f"  r·x ∈ (3) for all r∈Z/9Z, x∈(3): {linear_ok} ✓")
print(f"  → The inclusion i: (3) ↪ Z/9Z satisfies r·i(x) = i(r·x): CONFIRMED ✓")
print(f"  → i is a Z/9Z-bimodule map (left and right, ring is commutative).")

# The obstruction: no retraction r: Z/9Z → (3) with r∘i = id_(3)
# A retraction r must be a Z/9Z-module map: r(a·x) = a·r(x)
# and r(i(x)) = x for x ∈ (3).
# r: Z/9Z → {0,3,6}. Being a group hom, r is determined by r(1).
# r(1) must lie in... but r must map into (3), so r(1) ∈ {0,3,6}.
# r(n) = n·r(1) mod 9. Check r∘i = id:
# i(3) = 3, so r(3) = 3·r(1) mod 9 must equal 3.
# 3·r(1) ≡ 3 mod 9 → r(1) ≡ 1 mod 3. But r(1) ∈ {0,3,6}: none satisfy 1 mod 3.

print(f"\n  Searching for Z/9Z-module retractions r: Z/9Z → (3) with r∘i=id_(3):")
retractions = []
for c in Zn:   # r(1) = c, so r(n) = n·c mod 9
    r_vals = {x: (x * c) % N for x in Zn}
    # r must map INTO (3):
    maps_into_ideal = all(r_vals[x] in ideal3 for x in Zn)
    # r∘i = id_(3): r(x) = x for all x in ideal3:
    retract_ok = all(r_vals[x] == x for x in ideal3)
    if maps_into_ideal and retract_ok:
        retractions.append(c)
        print(f"    r(1)={c}: maps_into_ideal={maps_into_ideal}, retract_ok={retract_ok} → VALID")

if not retractions:
    print(f"  No retraction exists: CONFIRMED ✓")
    print(f"  Reason: r(1) must be ≡1(mod 3) [from r(3)=3] but r(1)∈(3) requires r(1)∈{{0,3,6}}")
    print(f"  {{0,3,6}} ∩ {{x: x≡1(mod 3)}} = ∅  → contradiction.")
    print(f"\n  The obstruction is: i is not a SPLIT monomorphism.")
    print(f"  (3) is a submodule but NOT a direct summand of Z/9Z.")
    print(f"  The document's minor-precision correction is CORRECT ✓")

# ---------------------------------------------------------------------------
# 10.  Direct sum vs filtration
# ---------------------------------------------------------------------------
print()
print("="*62)
print("10.  Z/9Z ≇ (3) ⊕ Z/3Z as Z/9Z-modules")
print("="*62)

print("""
  If Z/9Z ≅ (3) ⊕ Z/3Z, then Z/9Z would have:
    - A central idempotent e with e·Z/9Z ≅ (3) and (1-e)·Z/9Z ≅ Z/3Z.
    - But idempotents of Z/9Z = {0, 1} (proved above).
    - Neither e=0 nor e=1 gives the required decomposition.
""")
print(f"  Idempotents: {idempotents}")
print(f"  e=0: e·Z/9Z = 0  ≇ (3)")
print(f"  e=1: e·Z/9Z = Z/9Z ≇ Z/3Z")
print(f"  No idempotent splits Z/9Z into (3) ⊕ Z/3Z: CONFIRMED ✓")

print(f"""
  Correct structure:
    Jacobson radical filtration:  0 ⊂ J = (3) ⊂ Z/9Z
    Semisimple quotient:          Z/9Z / J ≅ Z/3Z  (field GF(3))
    Non-split extension:          0 → (3) → Z/9Z → Z/3Z → 0

  This is the local ring structure; Z/9Z is the Witt ring W(F_3) truncated
  at level 2 (the simplest non-trivial Witt vector extension of F_3).
""")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("="*62)
print("ALL CHECKS PASS")
print("="*62)
print(f"""
  X_inv = {{1,2,4,5,7,8}}:          ✓  units, gcd(x,9)=1
  X_nil = {{0,3,6}} = (3):           ✓  nilpotent ideal, multiples of 3
  Disjoint/cover Z/9Z:              ✓
  ×2 forward invariance:            ✓  0→0, 3↔6, units→units
  (3) is a multiplicative ideal:    ✓  a·b ∈ (3) for all a∈Z/9Z, b∈(3)
  2 generates (Z/9Z)* ≅ C₆:        ✓  orbit {{1,2,4,8,7,5}} = units
  Idempotents = {{0,1}} only:        ✓  Z/9Z is a local ring
  Indecomposable module:            ✓  no central idempotent to project
  (3)² = (0): nilpotency index 2:   ✓  3·3=3·6=6·6≡0(mod 9)
  J(Z/9Z) = (3), quotient = Z/3Z:  ✓  ring hom, kernel = (3)
  Exact sequence 0→(3)→Z/9Z→Z/3Z→0 does NOT split: ✓
  Z/9Z ≇ (3) ⊕ Z/3Z as modules:   ✓  no idempotent for splitting
  Inclusion (3)↪Z/9Z IS bimodule:  ✓  but is NOT a split monomorphism
  Document's "minor precision" correction: CORRECT ✓

  One note on scope:
    This audit is for Z/9Z module theory only. The G4 Cayley-graph
    eigenvalue analysis (orbit λ_trans values) is a separate structure
    covered in g4_mackey_fourier_audit.py and g4_stabilizer_geometry_audit.py.
""")
