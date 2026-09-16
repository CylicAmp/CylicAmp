"""
conic_lame_audit.py

Audits the five-column conic section table:
  eccentricity | Cartesian modifier s | B²-4AC discriminant
  | Lamé exponent n | degenerate row

Four claims to check:
  1. B²-4AC discriminant sign for each conic type
  2. Eccentricity ranges
  3. Lamé exponent assignments (the main claim)
  4. Internal consistency of "Cartesian modifier s"
"""

import math

# ---------------------------------------------------------------------------
# 1.  B²-4AC discriminant — standard projective discriminant
# ---------------------------------------------------------------------------
print("="*62)
print("1.  B²-4AC discriminant for general conic Ax²+Bxy+Cy²+Dx+Ey+F=0")
print("="*62)
print("""
  Standard result (e.g. Salmon 1879; any projective geometry text):
    B²-4AC < 0  →  ellipse or circle
    B²-4AC = 0  →  parabola
    B²-4AC > 0  →  hyperbola
    Degenerate conic: Δ = det of full 3×3 matrix = 0  (SEPARATE condition)
""")

def disc(A, B, C):
    return B**2 - 4*A*C

test_conics = [
    ("Circle  x²+y²=1",           1, 0, 1, 0, 0, -1),
    ("Ellipse x²/4+y²=1",         1, 0, 4, 0, 0, -4),
    ("Parabola y=x²",             1, 0, 0, 0, -1, 0),
    ("Hyperbola x²-y²=1",         1, 0,-1, 0, 0, -1),
    ("Degen: two lines x²-y²=0",  1, 0,-1, 0, 0,  0),
    ("Degen: point x²+y²=0",      1, 0, 1, 0, 0,  0),
    ("Degen: one line x²=0",      1, 0, 0, 0, 0,  0),
]

def matrix_det_3x3(A, B, C, D, E, F):
    """Determinant of the 3×3 symmetric matrix of the conic."""
    # M = [[A, B/2, D/2],
    #      [B/2, C, E/2],
    #      [D/2, E/2, F]]
    a, b, c = A, B/2, D/2
    d, e, f = B/2, C, E/2
    g, h, i = D/2, E/2, F
    return (a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g))

print(f"  {'Conic':35}  {'B²-4AC':>8}  {'sign':>6}  {'Δ(3×3)':>10}  {'degen?':>7}")
print(f"  {'-'*75}")
for label, A, B, C, D, E, F in test_conics:
    d = disc(A, B, C)
    sign = "<0" if d < 0 else ("=0" if d == 0 else ">0")
    delta = matrix_det_3x3(A, B, C, D, E, F)
    degen = "yes (Δ=0)" if abs(delta) < 1e-12 else "no"
    print(f"  {label:35}  {d:>8.1f}  {sign:>6}  {delta:>10.4f}  {degen:>9}")

print(f"""
  The B²-4AC column in the table is CORRECT for circle, ellipse,
  parabola, hyperbola.

  ISSUE — degenerate row: the table writes "N/A (det = 0)" in the
  B²-4AC column, but:
    • The condition det = 0 refers to Δ (the full 3×3 matrix determinant),
      NOT to B²-4AC.
    • B²-4AC CAN be evaluated for degenerate conics:
        Two intersecting lines (x²−y²=0): B²-4AC = 4 > 0
        Isolated point (x²+y²=0):        B²-4AC = -4 < 0
        Double line (x²=0):              B²-4AC =  0
    • Conflating the two determinants in one column is INCORRECT.
    • The degenerate condition is Δ=0, not B²-4AC undefined.
""")

# ---------------------------------------------------------------------------
# 2.  Eccentricity ranges
# ---------------------------------------------------------------------------
print("="*62)
print("2.  Eccentricity ranges")
print("="*62)
print("""
  Standard definitions:
    Circle:    e = 0          ✓ (table: e = 0)
    Ellipse:   0 < e < 1      ✓ (table: 0 < e < 1)
    Parabola:  e = 1          ✓ (table: e = 1)
    Hyperbola: e > 1          ✓ (table: e > 1)
    Degenerate: varies        ✓ (table: varies)

  All eccentricity entries CORRECT.
""")

# ---------------------------------------------------------------------------
# 3.  Lamé exponent n  — the main claim
# ---------------------------------------------------------------------------
print("="*62)
print("3.  Lamé exponent n: (x/a)^n + (y/b)^n = 1")
print("="*62)
print("""
  The Lamé curve (superellipse) is defined by  (x/a)^n + (y/b)^n = 1.
  Special cases:
    n = 1:   |x/a| + |y/b| = 1  →  rhombus / diamond  (NOT a conic)
    n = 2:   (x/a)² + (y/b)² = 1  →  ellipse (a=b: circle)
    n = ∞:   rectangle
    n = 2/3: astroid (hypocycloid)
""")

# Numerically verify: which Lamé curves are actual conics?
# A conic is a degree-2 algebraic curve.
# (x/a)^n + (y/b)^n = 1 is degree n (for integer n), degree-2 only when n=2.

def is_lame_conic(n, a=2.0, b=1.0, n_pts=200):
    """
    Check if (x/a)^n + (y/b)^n = 1 satisfies a degree-2 equation.
    Strategy: sample 6 points on the curve, fit the general conic
    Ax²+Bxy+Cy²+Dx+Ey+F=0 (5 free parameters), check residuals on
    additional points.
    Returns max residual on held-out points.
    """
    # Sample points on the upper arc x from -a to a
    pts = []
    for k in range(n_pts):
        x = a * (-1 + 2*k/(n_pts-1))
        inner = 1 - abs(x/a)**n
        if inner < 0: continue
        y = b * inner**(1.0/n)
        pts.append((x, y))
        pts.append((x, -y))  # lower arc

    if len(pts) < 10: return float('nan')

    # Build least-squares system for conic fit (6 coefficients, scale F=1)
    # Ax² + Bxy + Cy² + Dx + Ey = -1
    import sys
    try:
        # Simple least-squares via normal equations
        rows = []
        rhs = []
        for x, y in pts:
            rows.append([x*x, x*y, y*y, x, y])
            rhs.append(-1.0)

        # Solve via normal equations AtA v = At b
        m = len(rows)
        AtA = [[0.0]*5 for _ in range(5)]
        Atb = [0.0]*5
        for i in range(5):
            for j in range(5):
                AtA[i][j] = sum(rows[k][i]*rows[k][j] for k in range(m))
            Atb[i] = sum(rows[k][i]*rhs[k] for k in range(m))

        # Gaussian elimination
        import copy
        M = [AtA[i][:] + [Atb[i]] for i in range(5)]
        for col in range(5):
            pivot = max(range(col, 5), key=lambda r: abs(M[r][col]))
            M[col], M[pivot] = M[pivot], M[col]
            if abs(M[col][col]) < 1e-12: return float('nan')
            for row in range(5):
                if row != col:
                    factor = M[row][col] / M[col][col]
                    for j in range(6):
                        M[row][j] -= factor * M[col][j]
        coeffs = [M[i][5] / M[i][i] for i in range(5)]
        A_c, B_c, C_c, D_c, E_c = coeffs
        F_c = 1.0

        # Residuals on all points
        residuals = [abs(A_c*x**2 + B_c*x*y + C_c*y**2 + D_c*x + E_c*y + F_c)
                     for x, y in pts]
        return max(residuals)
    except:
        return float('nan')

print("  Testing whether Lamé curves are degree-2 (conic) for various n:")
print(f"  {'n':>6}  {'max conic residual':>20}  {'is a conic?':>12}  note")
print(f"  {'-'*60}")
test_n_values = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
for n_val in test_n_values:
    res = is_lame_conic(n_val, a=2.0, b=1.0)
    is_conic = res < 1e-8 if not math.isnan(res) else False
    if n_val == 1.0:
        note = "rhombus"
    elif n_val == 1.5:
        note = "superellipse (table: 'Ellipse')"
    elif n_val == 2.0:
        note = "true ellipse"
    elif n_val == 2.5:
        note = "superellipse"
    elif n_val == 3.0:
        note = "superellipse"
    else:
        note = "superellipse"
    res_str = f"{res:.2e}" if not math.isnan(res) else "N/A"
    print(f"  {n_val:>6.1f}  {res_str:>20}  {str(is_conic):>12}  {note}")

print(f"""
  RESULT: The Lamé curve (x/a)^n + (y/b)^n = 1 is a degree-2 algebraic
  curve (conic section) ONLY when n = 2.
  For n ≠ 2 (including n = 1 and 1 < n < 2), the curve is NOT a conic.

  Table errors in the Lamé column:
  ┌─────────────┬──────────────────────────────────────────────────────┐
  │ Row         │ Error                                                │
  ├─────────────┼──────────────────────────────────────────────────────┤
  │ Ellipse     │ Listed as 1 < n < 2. INCORRECT.                     │
  │             │ An ellipse is (x/a)²+(y/b)²=1, which is n=2.        │
  │             │ Lamé curves with 1<n<2 are NOT ellipses; they are   │
  │             │ superellipses interpolating between rhombus and      │
  │             │ ellipse shape. They are degree-n, not degree-2.      │
  ├─────────────┼──────────────────────────────────────────────────────┤
  │ Degenerate  │ Listed as n = 1. NONSTANDARD / INCORRECT.           │
  │             │ n=1 gives a rhombus |x/a|+|y/b|=1.                 │
  │             │ A degenerate conic (two lines, a point, a double    │
  │             │ line) is defined by Δ=0 on a degree-2 form.         │
  │             │ The rhombus is not a degenerate conic; it is a      │
  │             │ degree-1 piecewise-linear curve in each quadrant.   │
  └─────────────┴──────────────────────────────────────────────────────┘

  Correct Lamé assignments for actual conics:
    Circle:    n = 2, a = b      (Lamé circle)
    Ellipse:   n = 2, a ≠ b      (same family as circle, n=2)
    Parabola:  N/A               ✓ (open curve; not expressible as Lamé)
    Hyperbola: N/A               ✓ (open curve; not expressible as Lamé)
""")

# ---------------------------------------------------------------------------
# 4.  Cartesian modifier s
# ---------------------------------------------------------------------------
print("="*62)
print("4.  Cartesian modifier s")
print("="*62)
print("""
  'Cartesian modifier s' is not a standard term in conic geometry.
  The table assigns:
    Circle:    s = 1  (where a = b)
    Ellipse:   s > 0  (where a ≠ b)
    Parabola:  N/A
    Hyperbola: s < 0
    Degenerate: s = 0

  Testing hypothesis: s = 1 − e²
    Circle:    e=0  → s = 1    ✓ matches
    Ellipse:   0<e<1 → 0<s<1   ✓ s > 0 ✓ (consistent but not s=1)
    Parabola:  e=1  → s = 0    ✗ table says N/A, formula gives 0
    Hyperbola: e>1  → s < 0    ✓ matches
    Degenerate: e varies → N/A  (not s=0 in general)

  Note: if s = 1−e², the parabola gives s = 0, colliding with the
  degenerate row entry s = 0, and contradicting the N/A entry.

  Testing hypothesis: s = sign of (b² in standard form Ax²+By²=C)
    Circle:    A=B → s=1        ambiguous (both positive)
    Ellipse:   A>0, B>0 → s>0   ✓
    Parabola:  one term missing → N/A ✓
    Hyperbola: A>0, B<0 (or reverse) → s<0 ✓
    Degenerate: depends on type → s=0 iff both terms vanish

  VERDICT: Without a definition of s, the column is underdetermined.
  The two candidate interpretations above are partially consistent but
  both have at least one conflict (parabola s=0 vs N/A for s=1-e²).
  The column requires an explicit definition to be auditable.
""")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("="*62)
print("SUMMARY")
print("="*62)
print(f"""
  Column              Status
  -----------------------------------------------------------
  Eccentricity        ALL CORRECT ✓

  B²-4AC discriminant CORRECT for circle, ellipse, parabola,
                      hyperbola.
                      INCORRECT for degenerate row: "det = 0"
                      refers to Δ (3×3 matrix det), not B²-4AC.
                      B²-4AC is defined for degenerate conics and
                      can be <0, =0, or >0 depending on type.

  Lamé exponent n     Circle n=2: CORRECT ✓
                      Ellipse "1<n<2": INCORRECT — ellipses are
                        n=2. Values 1<n<2 are superellipses, not
                        conic sections.
                      Degenerate n=1: INCORRECT — n=1 Lamé curve
                        is a rhombus, not a degenerate conic.
                      Parabola/Hyperbola N/A: CORRECT ✓

  Cartesian modifier  Undefined term; no standard definition.
  s                   Partially consistent with s = 1−e² but
                      parabola creates a conflict (s=0 vs N/A).
                      Requires explicit definition to audit.

  The table conflates two distinct classification schemes:
    1. Classical conics (eccentricity, B²-4AC, projective geometry)
    2. Lamé / superellipse family ((x/a)^n + (y/b)^n = 1)
  These are different families. The Lamé family intersects the
  conic family only at n=2. Extending n away from 2 leaves conic
  geometry entirely.
""")
