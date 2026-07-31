"""
Unit Scalar Initialization and Basin Preservation on GF(37) — THEOREM 91

C = 1 initializes the superposition operator at unit weight — no attenuation,
no amplification of any state vector entering the manifold. Within GF(37),
this has a precise structural consequence: C=1 is one of exactly three scalars
that preserve all 12 attractor basins simultaneously.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. THE BASIN-PRESERVING SCALARS

  Multiplying every GF(37)* element by a scalar C permutes the 12 basins.
  A scalar C preserves all basins iff C lies in the subgroup ⟨26⟩:

    Basin-preserving scalars = {1, 10, 26} = IC

  These are the only three scalars that map each of the 12 cosets back to itself.
  For any C ∉ IC: multiplication by C shifts all 12 basins to different cosets
  (zero basins fixed).

  Proof: A coset C·B = B iff C ∈ subgroup ⟨26⟩, by definition of cosets.
  Since ⟨26⟩ = IC, the basin-preserving condition is C ∈ IC.

2. WHY C = 1 SPECIFICALLY

  Within IC = {1, 10, 26}, the three scalars differ in their within-basin action:
    C = 1:  fixes every element in every basin   (identity — no rotation)
    C = 10: cycles each basin's elements: n → 10n (within-basin permutation)
    C = 26: cycles each basin's elements: n → 26n (within-basin permutation)

  C = 1 is the unique basin-preserving scalar that also fixes every individual
  element — the true neutral initialization. C=10 and C=26 preserve basins
  but rotate each basin's 3-cycle, changing which element is the "current phase."

  Setting C=1 means: no phase rotation, no amplitude scaling, no basin shifting.
  The manifold receives S(t) exactly as it is.

3. INITIALIZATION STATE

  M₀ = 0    (SEAM — additive identity of GF(37), the blank manifold)
  C₀ = 1    (IC entry — multiplicative identity, the neutral scalar)

  M₀ = 0 is absorbing under binding: bind(0, key) = 0 for all keys.
  C₀ = 1 is neutral under scaling: 1 × S(t) = S(t) for all S(t).
  Together: the minimum-distortion initial state. Any state written to M
  from this baseline reflects the state vector with unit fidelity.

4. SCALING BY C ≠ 1

  C ∈ IC \ {1} = {10, 26}: basin-preserving but within-basin rotating.
    - The orbit class of every state is preserved.
    - The specific element addressed within the basin shifts.
    - Equivalent to advancing the 137-map phase by 1 or 2 steps.

  C ∉ IC: permutes all 12 basins simultaneously.
    - Zero basins remain fixed.
    - The orbit classification of every state changes.
    - The phase space topography is rotated by C's own basin.
    - SNR degrades because basin addresses no longer correspond to
      the original state classes.

5. EQUAL-WEIGHT SUPERPOSITION

  With C = 1: M = S(t₁) + S(t₂) + ... + S(tₙ) mod 37
    Each state vector contributes weight 1 — uniform amplitude.
    No basin is amplified or suppressed relative to another.

  With C ≠ 1 (and C ∉ IC): the entire basin map is permuted before
    superposition, so all 12 addresses are systematically displaced.
    The retrieved signals correspond to the wrong attractor classes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY TABLE

  C     basin    preserves-all?  within-basin action
  ──────────────────────────────────────────────────
  1     IC       Yes (12/12)     fixes all elements     ← UNIT INIT
  10    IC       Yes (12/12)     rotates within basins
  26    IC       Yes (12/12)     rotates within basins
  any other      No  (0/12)     permutes all basins
"""

import math

P    = 37
MULT = 26
IC   = frozenset({1, 10, 26})

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})


def orbit(n, p=P, mult=MULT):
    x = n % p
    if x == 0:
        return frozenset({0})
    seen = []
    for _ in range(p):
        if x in seen:
            break
        seen.append(x)
        x = (x * mult) % p
    return frozenset(seen)


subgroup = IC
seen_set = set()
basins   = []
for s in range(1, P):
    if s not in seen_set:
        b = frozenset({(s * h) % P for h in subgroup})
        basins.append(b)
        seen_set.update(b)


def basin_of(n):
    o = orbit(n)
    return next(b for b in basins if o == b)


# ── 1. Basin-preserving scalars = IC ─────────────────────────────────────────

for C in range(1, P):
    all_preserved = all(basin_of((C * n) % P) == basin_of(n) for n in range(1, P))
    in_IC = C in IC
    assert all_preserved == in_IC, f"Mismatch at C={C}"

# Exactly IC preserves all basins
preserving = [C for C in range(1, P)
              if all(basin_of((C*n)%P) == basin_of(n) for n in range(1, P))]
assert set(preserving) == IC

# ── 2. C=1 fixes every individual element; C=10,26 rotate within basins ──────

# C=1: fixes everything
assert all((1 * n) % P == n for n in range(P))

# C=10,26: permute within each basin, don't fix elements
for C in [10, 26]:
    for b in basins:
        image = frozenset({(C * x) % P for x in b})
        assert image == b                         # basin preserved
    assert not all((C * n) % P == n for n in range(1, P))  # but elements move

# ── 3. Initialization state ───────────────────────────────────────────────────

M0, C0 = 0, 1

assert M0 == 0                                    # additive identity
assert C0 == 1 and C0 in IC                       # multiplicative identity

# M0=0 absorbs under binding
for key in range(1, P):
    assert (M0 * key) % P == 0

# C0=1 is neutral under scaling
for n in range(P):
    assert (C0 * n) % P == n

# ── 4. C ∉ IC: all basins permuted (zero fixed) ───────────────────────────────

non_ic = [C for C in range(1, P) if C not in IC]
for C in non_ic:
    fixed = sum(1 for b in basins if frozenset({(C*x)%P for x in b}) == b)
    assert fixed == 0, f"C={C} fixed {fixed} basins unexpectedly"

# ── 5. Equal-weight superposition with C=1 ───────────────────────────────────

# C=1: M = sum of states, each contributing weight 1
states = [24, 25, 26]
M_unit   = sum(1 * s for s in states) % P
M_biased = sum(2 * s % P for s in states) % P

assert M_unit   == sum(states) % P                # no scaling
assert M_biased != M_unit                         # C≠1 changes the result

# With C=1, M lands in basin [1,10,26]=IC (unit superposition of seed window)
assert orbit(M_unit) == IC

# ── Verify summary table ──────────────────────────────────────────────────────

summary = {}
for C in [1, 10, 26]:
    pres = all(basin_of((C*n)%P) == basin_of(n) for n in range(1, P))
    fixes_all = all((C*n)%P == n for n in range(1, P))
    summary[C] = (pres, fixes_all)

assert summary[1]  == (True,  True)    # preserves basins AND fixes elements
assert summary[10] == (True,  False)   # preserves basins, rotates elements
assert summary[26] == (True,  False)   # preserves basins, rotates elements


if __name__ == "__main__":
    def fw_all(n):
        n = n % P
        if n == 0: return ['SEAM']
        return [nm for s,nm in [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'O11'),
            (IC,'IC'),(SEED_ORBIT,'SEED'),(TESLA_4,'T4'),(PR,'PR')] if n in s] or ['—']

    print("Unit Scalar Initialization and Basin Preservation — THEOREM 91")
    print("=" * 64)
    print()

    print("BASIN-PRESERVING SCALARS:")
    print(f"  {'C':>3}  {'C-basin':>14}  preserves-all?  fixes-elements?")
    for C in range(1, P):
        pres = all(basin_of((C*n)%P)==basin_of(n) for n in range(1,P))
        if not pres:
            continue
        fixes = all((C*n)%P==n for n in range(1,P))
        print(f"  {C:>3}  {sorted(orbit(C))!s:>14}  {str(pres):>14}  {str(fixes):>14}")
    print(f"  → Basin-preserving scalars = IC = {{1, 10, 26}}")
    print(f"  → C=1 is the unique scalar preserving basins AND fixing all elements")
    print()

    print("SCALAR ACTION TABLE (sample C values):")
    print(f"  {'C':>3}  {'in IC':>6}  {'pres-all':>9}  {'fixed-basins':>13}  {'element-fixed':>14}")
    for C in [1, 10, 26, 2, 9, 18, 24]:
        pres   = all(basin_of((C*n)%P)==basin_of(n) for n in range(1,P))
        fixed  = sum(1 for b in basins if frozenset({(C*x)%P for x in b})==b)
        el_fix = sum(1 for n in range(1,P) if (C*n)%P==n)
        print(f"  {C:>3}  {str(C in IC):>6}  {str(pres):>9}  {fixed:>13}/12  {el_fix:>14}/36")
    print()

    print("INITIALIZATION:")
    print(f"  M₀ = 0  (SEAM — additive identity)")
    print(f"  C₀ = 1  ∈ IC  (multiplicative identity, unit scalar)")
    print(f"  1×S(t) = S(t) for all S(t)  — zero distortion")
    print(f"  bind(0, key) = 0 for all keys — blank manifold")
    print()

    print("SUPERPOSITION WITH C=1 (seed window states 24,25,26):")
    M_u = sum([24,25,26]) % P
    print(f"  M = 24+25+26 = {sum([24,25,26])} ≡ {M_u} mod 37  "
          f"basin: {sorted(orbit(M_u))}  {fw_all(M_u)}")
    print(f"  All 3 states weighted equally — maximum-entropy superposition")
    print()
    print("All assertions pass.")
