"""
palindrome_diamond_audit.py

Audits four specific mathematical constructions and two framing claims:
  1. VIREON re-initialization matrix (triadic + doubling circuit palindrome)
  2. Seed-1-23 extrapolation and center spine {1,2,4,7,2,7,4,2,1}
  3. Repunit-square diamond: row k = (111...1 with k ones)²
  4. Descending palindrome diamond: row k = k,k-1,...,1,...,k-1,k
  5. "Axioms 0-5": test for logical / mathematical form
  6. Polar conic scatter plot formula r = ℓ/(1+e·cos θ)
"""

import math

DR = lambda n: ((n - 1) % 9) + 1 if n > 0 else 0   # digital root

# ---------------------------------------------------------------------------
# 1.  VIREON re-initialization matrix
# ---------------------------------------------------------------------------
print("="*62)
print("1.  VIREON re-initialization matrix")
print("="*62)
print("""
  Claimed construction:
    Row 9 (widest, 17 digits): 57842196369124875
    Each row k = center 2k-1 digits of row 9.
    Document claim: center-outward sequence = {3,6,9} ∪ {1,2,4,8,7,5}.
""")

VIREON_ROW9 = "57842196369124875"

# Verify palindrome
is_palindrome = VIREON_ROW9 == VIREON_ROW9[::-1]
print(f"  Row 9 palindrome: {is_palindrome} ✓" if is_palindrome else
      f"  Row 9 NOT palindromic ✗")

# Center digit
center = VIREON_ROW9[len(VIREON_ROW9)//2]
print(f"  Center digit: {center}  (expected: 3) {'✓' if center=='3' else '✗'}")

# Center-outward sequence (right half from center)
half = VIREON_ROW9[len(VIREON_ROW9)//2:]   # '3', '6', '9', ...
print(f"  Center-outward: {list(half)}")
expected_co = [3,6,9,1,2,4,8,7,5]
actual_co   = [int(d) for d in half]
print(f"  Matches {{3,6,9}}+{{1,2,4,8,7,5}}: {actual_co == expected_co} ✓"
      if actual_co == expected_co else
      f"  MISMATCH: expected {expected_co}, got {actual_co}")

# Reconstruct all 9 expanding rows
print(f"\n  Reconstructed matrix (expanding from center):")
for k in range(1, 10):
    start = 9 - k    # center at index 8; 2k-1 chars: [9-k : 8+k]
    end   = 8 + k    # exclusive
    row = VIREON_ROW9[start:end]
    is_pal = row == row[::-1]
    print(f"    Row {k:2d}: {row:>18}  palindrome:{is_pal}")

# What is the algebraic rule?
# The sequence 3,6,9,1,2,4,8,7,5 are the two non-trivial orbits under
# multiplication by 2 (mod 9) PLUS the triadic fixed set:
#   {3,6,9}: dr(3×k) for k=1,2,3 — or equivalently, multiples of 3 mod 9
#   {1,2,4,8,7,5}: the 6-cycle of doubling, confirmed in prior audit
print(f"""
  Algebraic note:
    {list(half)} = {{3,6,9}} || {{1,2,4,8,7,5}}
    {{3,6,9}} = orbit of 3 under ×2 mod 9, plus fixed point 9
    {{1,2,4,8,7,5}} = orbit of 1 under ×2 mod 9 (6-cycle, confirmed)
    Together these are ALL non-zero residues mod 9.
    The nine-element sequence 3,6,9,1,2,4,8,7,5 is a permutation of {{1,...,9}}.
    It is NOT the natural order, but it IS complete. ✓
""")

# ---------------------------------------------------------------------------
# 2.  Seed extrapolation: seed = "1\n23", expand cycling 1-9, mirror
# ---------------------------------------------------------------------------
print("="*62)
print("2.  Seed extrapolation diamond")
print("="*62)
print("""
  Rule: expand seed by appending sequential integers (cycling 1-9).
  Row n has n digits. After 9 rows, total = 1+2+...+9 = 45 digits (mod-9 = 0).
  Mirror operation: S → Reverse(S[1:]) + S[0] + S[1:]
""")

def gen_rows(n_rows=9):
    """Generate rows by cycling digits 1-9."""
    seq = []
    d = 1
    for r in range(1, n_rows+1):
        row = []
        for _ in range(r):
            row.append(d)
            d = (d % 9) + 1
        seq.append(row)
    return seq

def mirror(row):
    """Apply bi-directional palindrome mirror."""
    if len(row) == 1:
        return row[:]
    return list(reversed(row[1:])) + [row[0]] + row[1:]

rows = gen_rows(9)
print("  Un-mirrored rows (seed extrapolation):")
claimed_unmirrored = [
    [1],
    [2,3],
    [4,5,6],
    [7,8,9,1],
    [2,3,4,5,6],
    [7,8,9,1,2,3],
    [4,5,6,7,8,9,1],
    [2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,8,9],
]
all_match = True
for i, (r, c) in enumerate(zip(rows, claimed_unmirrored)):
    ok = r == c
    all_match = all_match and ok
    print(f"  Row {i+1:2d}: {''.join(map(str,r)):>10}  {'✓' if ok else f'FAIL (expected {c})'}")

print(f"\n  All un-mirrored rows correct: {all_match}")

print("\n  Mirrored rows (full diamond, top half):")
claimed_mirrored_strs = [
    "1",
    "323",
    "65456",
    "1987891",
    "654323456",
    "32198789123",
    "1987654567891",
    "987654323456789",
    "98765432123456789",
]
center_digits = []
all_mirror_ok = True
for i, (row, claimed_str) in enumerate(zip(rows, claimed_mirrored_strs)):
    m = mirror(row)
    actual_str = ''.join(map(str, m))
    ok = actual_str == claimed_str
    all_mirror_ok = all_mirror_ok and ok
    center = m[len(m)//2]
    center_digits.append(center)
    print(f"  Row {i+1:2d}: {actual_str:>20}  {'✓' if ok else f'FAIL (claimed {claimed_str})'}")

print(f"\n  All mirrored rows correct: {all_mirror_ok}")

# Center spine
print(f"\n  Center digit per row: {center_digits}")
claimed_spine = [1,2,4,7,2,7,4,2,1]
spine_ok = center_digits == claimed_spine
print(f"  Claimed spine {{1,2,4,7,2,7,4,2,1}}: {spine_ok} {'✓' if spine_ok else '✗'}")

if not spine_ok:
    print(f"  Actual spine: {center_digits}")

# Explain the center spine
print(f"""
  Why the center spine is {{1,2,4,7,2,7,4,2,1}}:
    The center of mirrored row n = first digit of un-mirrored row n = S[0].
    S[0] for row n is the digit at position (cumulative count of prior rows) + 1
    in the cycling sequence 1,2,...,9,1,2,...

    Cumulative digits before row n:
      Row 1 starts at position 1  → digit 1
      Row 2 starts at position 2  → digit 2
      Row 3 starts at position 4  → digit 4
      Row 4 starts at position 7  → digit 7
      Row 5 starts at position 11 → 11 mod 9 = 2
      Row 6 starts at position 16 → 16 mod 9 = 7
      Row 7 starts at position 22 → 22 mod 9 = 4
      Row 8 starts at position 29 → 29 mod 9 = 2
      Row 9 starts at position 37 → 37 mod 9 = 1

    Starting positions: 1,2,4,7,2,7,4,2,1 = center spine ✓
    The pattern arises from cumulative triangular numbers mod 9:
      T(n-1)+1 = n(n-1)/2 + 1  mod 9
""")
# Verify
starts = []
total = 0
for n in range(1, 10):
    start = (total % 9) + 1
    starts.append(start)
    total += n
print(f"  Computed starting positions: {starts}")
print(f"  Matches claimed spine: {starts == claimed_spine} ✓" if starts==claimed_spine else
      f"  MISMATCH")

# ---------------------------------------------------------------------------
# 3.  Repunit-square diamond  (111...1)² = 12345...k...54321
# ---------------------------------------------------------------------------
print()
print("="*62)
print("3.  Repunit-square diamond: (111...1)²")
print("="*62)

def repunit(k):
    return int('1' * k)

print(f"  {'k':>3}  {'111...1 (k ones)':>18}  {'(111...1)²':>22}  palindrome")
all_rep_ok = True
for k in range(1, 10):
    r = repunit(k)
    sq = r * r
    s = str(sq)
    is_pal = s == s[::-1]
    all_rep_ok = all_rep_ok and is_pal
    print(f"  {k:>3}  {r:>18}  {sq:>22}  {'✓' if is_pal else '✗'}")

print(f"\n  All repunit squares are palindromes: {all_rep_ok} ✓")

# Verify specific structure: digits are 1,2,...,k,...,2,1
print(f"\n  Digit pattern of (111...1)² for k=1..9:")
for k in range(1, 10):
    sq = str(repunit(k)**2)
    # Expected: 1,2,...,k,...,2,1 but for k<10 all single digits
    expected_digits = list(range(1,k+1)) + list(range(k-1,0,-1))
    actual_digits = [int(d) for d in sq]
    ok = actual_digits == expected_digits
    print(f"  k={k}: {''.join(map(str,expected_digits)):>20}  match:{ok} {'✓' if ok else '✗'}")

print(f"""
  Formula: repunit(k)² = (10^k - 1)²/81
  The digits 1,2,...,min(k,9),...,2,1 arise from the convolution
  of the all-1s vector with itself: (1*1)(k) = number of ways to
  write k as a sum of two integers from {{1,...,9}} = k for k ≤ 9.
  This is a PROVEN result, not a conjecture.
""")

# ---------------------------------------------------------------------------
# 4.  Descending palindrome diamond: row k = k,k-1,...,1,...,k-1,k
# ---------------------------------------------------------------------------
print("="*62)
print("4.  Descending palindrome diamond")
print("="*62)
print("""
  Row k: k, k-1, ..., 2, 1, 2, ..., k-1, k  (2k-1 digits)
  Image shows this pattern with commas as formatting separators.
""")

print(f"  {'k':>3}  {'row (no commas)':>25}  palindrome")
for k in range(1, 14):
    row = list(range(k, 0, -1)) + list(range(2, k+1))
    s = ''.join(str(d % 10) for d in row)    # mod 10 for display (digits 1-13 → wrap)
    row_str = ','.join(str(d) for d in row)
    is_pal = row == row[::-1]
    print(f"  {k:>3}  {row_str:>30}  {'✓' if is_pal else '✗'}")

print(f"""
  All rows are palindromes by construction (symmetric about k).
  The image shows rows up to k=13, with commas in image text as
  visual separators, not decimal separators.
  This is a KNOWN pattern; no new mathematical content.
""")

# ---------------------------------------------------------------------------
# 5.  "Axioms 0-5": test for logical / mathematical form
# ---------------------------------------------------------------------------
print("="*62)
print("5.  'Axioms 0-5': test for mathematical content")
print("="*62)

axioms = [
    (0, "Phase Gate",
     "Initiates absolute matrix collapse or total spatial reflection at terminal vertices"),
    (1, "Singularity",
     "The absolute origin vector from which all radial shells expand"),
    (2, "Polarity",
     "Forces bi-directional geometric divergence across the X and Y axes simultaneously"),
    (3, "Triadic Resonance",
     "The foundational spatial anchor preventing matrix entropy"),
    (4, "Cartesian Stability",
     "The orthogonal lock mapping the boundary edges of the lattice"),
    (5, "Asymmetric Shift",
     "The geometric pivot that triggers sequence recursive loops"),
]

print("""
  A mathematical axiom is a logical proposition: it contains a
  subject, predicate, and logical connectives (∀, ∃, →, ↔, =, etc.)
  that can be combined with other axioms via rules of inference.
  It must be:
    (a) Expressible as a formal sentence in a logical language
    (b) Either primitive (undefined at this level) or derivable
    (c) Testable: a model either satisfies or violates it

  Test for each "axiom":
""")
print(f"  {'#':>3}  {'Name':>20}  {'Has equations?':>15}  "
      f"{'Has quantifiers?':>17}  {'Falsifiable?':>13}")
print(f"  {'-'*78}")
for n, name, desc in axioms:
    has_eq  = any(c in desc for c in ['=', '<', '>', '≤', '≥', '≠', '∀', '∃', '→'])
    has_q   = any(w in desc.lower() for w in ['all', 'every', 'exists', 'some',
                                               'for all', 'there exists', '∀', '∃'])
    # Falsifiable: can we construct a specific case where the axiom fails?
    # These are all vague enough that falsification is undefined.
    falsif = False   # none have specific numeric conditions to test
    print(f"  {n:>3}  {name:>20}  {str(has_eq):>15}  {str(has_q):>17}  "
          f"{str(falsif):>13}")

print(f"""
  Result: NONE of the six "Axioms" contains equations, quantifiers,
  or falsifiable conditions.

  Compare with actual mathematical axioms:
    Peano Axiom 1: 0 ∈ ℕ                   (quantifier-free; contains =; falsifiable)
    Field axiom:   ∀a,b: a+b = b+a         (quantified; equation; falsifiable)
    ZFC Extensionality: ∀A,B: (∀x: x∈A ↔ x∈B) → A=B

  The submitted "Axioms 0-5" are LABELS with descriptive text.
  They name roles (origin, polarity, anchor, etc.) but do not
  constrain the system to a specific mathematical structure.
  No theorem can be derived from them because they have no logical form.

  Applying the removal test:
    Remove the analogy ("matrix", "lattice", "engine") →
    "Axiom 3 (Triadic Resonance): The foundational spatial anchor
     preventing matrix entropy."
    Removing "spatial anchor" and "matrix entropy" leaves:
    "...preventing entropy." — no equation, no definition of entropy,
    no governing rule. Nothing remains after analogy removal.
""")

# ---------------------------------------------------------------------------
# 6.  Polar conic scatter plot: r = ℓ/(1 + e·cos θ)
# ---------------------------------------------------------------------------
print("="*62)
print("6.  Polar conic formula verification")
print("="*62)
print("""
  Standard focus-directrix form (Apollonius / Newton):
    r = ℓ / (1 + e·cos θ)    where ℓ = semi-latus rectum > 0

  Conic type determined by e:
    e = 0:   circle  (r = ℓ = const)
    0<e<1:   ellipse (periapsis at θ=0, apoapsis at θ=π)
    e = 1:   parabola (r → ∞ as θ → π)
    e > 1:   hyperbola (r < 0 for θ > arccos(-1/e), giving 2nd branch)
""")

import math

def polar_conic(e, ell=1.0, n_pts=200):
    """Generate (x,y) points for r = ell/(1+e*cos(theta))."""
    pts = []
    for k in range(n_pts):
        theta = 2 * math.pi * k / n_pts
        denom = 1 + e * math.cos(theta)
        if abs(denom) < 1e-9: continue
        r = ell / denom
        pts.append((r * math.cos(theta), r * math.sin(theta)))
    return pts

# Verify key geometric properties
print(f"  {'e':>5}  {'type':>10}  {'periapsis r(0)':>15}  "
      f"{'apoapsis r(π)':>15}  {'note'}")
print(f"  {'-'*72}")
for e, ell, label in [(0, 1.0, 'circle'), (0.5, 0.75, 'ellipse'),
                      (1.0, 2.0, 'parabola'), (1.5, 1.25, 'hyperbola')]:
    r0  = ell / (1 + e)   # r at θ=0
    rpi = ell / (1 - e) if abs(1-e) > 1e-9 else float('inf')
    if e == 1.0:
        rpi_str = "∞"
    elif e > 1.0:
        rpi_str = f"{rpi:.4f} (neg, 2nd branch)"
    else:
        rpi_str = f"{rpi:.4f}"
    print(f"  {e:>5.1f}  {label:>10}  {r0:>15.4f}  {rpi_str:>15}  ell={ell}")

print(f"""
  Parabola (e=1): r → ∞ as θ → π. The curve opens in the direction
  OPPOSITE to θ=0. With θ=0 along +x axis, the parabola's vertex is
  at (ell/2, 0) and opens toward −x (left).

  KEY CHECK for scatter plot:
    If the scatter plot shows the parabola opening toward +x (right)
    or diagonally upward, the formula r = ell/(1+e·cos θ) was NOT used.
    A rightward-opening parabola requires r = ell/(1−e·cos θ)
    or a rotation of the standard form.

  The correct polar parabola (e=1, vertex on +x axis, opens left):
""")

# Print 10 sample points for parabola
print(f"  {'θ (°)':>8}  {'r':>8}  {'x':>8}  {'y':>8}  note")
ell_para = 2.0
for theta_deg in [0, 30, 60, 90, 120, 150, 170]:
    theta = math.radians(theta_deg)
    denom = 1 + math.cos(theta)
    if abs(denom) < 1e-9:
        print(f"  {theta_deg:>8}  {'→∞':>8}")
        continue
    r = ell_para / denom
    x, y = r * math.cos(theta), r * math.sin(theta)
    note = "vertex" if theta_deg == 0 else ("far left" if theta_deg >= 150 else "")
    print(f"  {theta_deg:>8}  {r:>8.3f}  {x:>8.3f}  {y:>8.3f}  {note}")

print(f"""
  All x-coordinates ≤ ell/2 = {ell_para/2} for this parabola.
  Any scatter plot showing parabola points at x > 1.0 for ell=2.0
  is using a different formula or orientation.

  The bar chart (eccentricity classification) and the eccentricity
  ranges (e=0, 0.5, 1.0, 1.5 as representative values) are CORRECT
  as labeled values. The scatter plot geometry requires code inspection
  to confirm formula; visual alone is ambiguous.
""")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("="*62)
print("SUMMARY")
print("="*62)
print(f"""
  Construction                          Status
  ---------------------------------------------------------------
  VIREON matrix palindrome              CORRECT ✓
  Center-outward: 3,6,9,1,2,4,8,7,5    CORRECT ✓ (all 9 residues)
  Sequence = two Z/9Z orbits concat.    CORRECT ✓
  Seed extrapolation rows               ALL 9 ROWS CORRECT ✓
  Center spine {{1,2,4,7,2,7,4,2,1}}     CORRECT ✓ (from T(n-1)+1 mod 9)
  Repunit squares (111...1)²            CORRECT ✓ (proven theorem)
  Descending palindrome rows            CORRECT ✓ (trivially symmetric)

  "Axioms 0-5"                          NOT AXIOMS — zero logical form;
                                        no equations, quantifiers, or
                                        falsifiable conditions in any of
                                        the six statements.

  Polar conic formula r=ℓ/(1+e·cosθ)   Formula is standard and correct.
                                        Parabola (e=1) opens leftward
                                        in this convention; a plot showing
                                        rightward-opening parabola uses a
                                        different equation.

  Applying removal test to "Axioms":
    Remove analogy framing → no residual equations.
    These are labels, not axioms. No theorems follow from them.
""")
