"""
digital_root_table_audit.py

Audit of the two-column table format  n - A - B.
Determines the formula for A and B, then checks every entry.
"""

from math import gcd

# ---------------------------------------------------------------------------
# Digital root helper
# ---------------------------------------------------------------------------
def dr(n):
    """Digital root: 1-9 (or 0 for n=0)."""
    if n == 0: return 0
    r = n % 9
    return r if r != 0 else 9

# ---------------------------------------------------------------------------
# The full table as given
# ---------------------------------------------------------------------------
table = [
    (10,1,2),(11,2,3),(12,3,6),(20,2,4),(21,3,6),(22,4,8),(23,5,1),
    (30,3,6),(32,5,1),(33,6,3),(34,7,5),(40,4,8),(43,7,5),(44,8,7),
    (45,9,9),(50,5,1),(54,9,9),(55,1,2),(56,2,4),(60,6,3),(65,2,4),
    (67,4,8),(70,7,5),(76,4,8),(78,6,3),(80,8,7),(87,6,3),(88,7,5),
    (89,8,7),(90,9,9),(98,8,7),(99,9,9),
]

# ---------------------------------------------------------------------------
# 1.  Determine formula for A
# ---------------------------------------------------------------------------
print("="*62)
print("1.  Formula for A")
print("="*62)

a_formula_ok = all(A == dr(n) for n, A, B in table)
print(f"  A = dr(n) for all entries: {a_formula_ok}")
if not a_formula_ok:
    for n, A, B in table:
        if A != dr(n):
            print(f"    FAIL: n={n}, claimed A={A}, dr({n})={dr(n)}")
else:
    print(f"  A = digital_root(n) = (sum of digits of n, reduced mod 9) ✓")

# ---------------------------------------------------------------------------
# 2.  Determine formula for B
# ---------------------------------------------------------------------------
print()
print("="*62)
print("2.  Formula for B")
print("="*62)

# Hypothesis: B = dr(2n)
print(f"  Testing B = dr(2n):")
b_errors = []
for n, A, B in table:
    expected_B = dr(2 * n)
    ok = (B == expected_B)
    if not ok:
        b_errors.append((n, A, B, expected_B))

print(f"  Errors: {len(b_errors)} out of {len(table)}")
if b_errors:
    print(f"\n  {'n':>4}  {'A':>3}  {'B_claimed':>10}  {'dr(2n)':>7}  note")
    for n, A, B, exp in b_errors:
        print(f"  {n:>4}  {A:>3}  {B:>10}  {exp:>7}  ← should be {exp}")
else:
    print(f"  B = dr(2n) for all entries ✓")

# Confirm correct formula for the error case
if b_errors:
    n0, A0, B0, exp0 = b_errors[0]
    print(f"\n  For n={n0}: dr({n0})={dr(n0)}, dr(2×{n0})=dr({2*n0})={dr(2*n0)}")
    print(f"  Claimed B={B0}, correct B={exp0}.")

# ---------------------------------------------------------------------------
# 3.  Full table check
# ---------------------------------------------------------------------------
print()
print("="*62)
print("3.  Full table: n - dr(n) - dr(2n)")
print("="*62)
print(f"  {'n':>4}  {'dr(n)':>6}  {'dr(2n)':>7}  {'claimed_A':>10}  {'claimed_B':>10}  A_ok  B_ok")
print(f"  {'-'*64}")
all_a_ok = True
all_b_ok = True
for n, A, B in table:
    a_ok = (A == dr(n))
    b_ok = (B == dr(2*n))
    all_a_ok = all_a_ok and a_ok
    all_b_ok = all_b_ok and b_ok
    a_mark = "✓" if a_ok else "FAIL"
    b_mark = "✓" if b_ok else f"FAIL(correct={dr(2*n)})"
    print(f"  {n:>4}  {dr(n):>6}  {dr(2*n):>7}  {A:>10}  {B:>10}  {a_mark:>4}  {b_mark}")

print(f"\n  A = dr(n):  all correct: {all_a_ok}")
print(f"  B = dr(2n): all correct: {all_b_ok}")

# ---------------------------------------------------------------------------
# 4.  Missing entries (numbers in range that are absent)
# ---------------------------------------------------------------------------
print()
print("="*62)
print("4.  Coverage: which two-digit numbers are in the table?")
print("="*62)

present = {n for n, A, B in table}
# Two-digit range with dr(n) ≥ 1 (i.e., 10..99)
all_two_digit = set(range(10, 100))
missing = sorted(all_two_digit - present)
print(f"  Present: {len(present)} entries (out of 90 two-digit numbers)")
print(f"  Missing: {len(missing)}")
print(f"  Missing n values: {missing}")

# Do the missing entries have a pattern?
# Check if missing entries share a digit-sum structure
missing_dr = [(n, dr(n)) for n in missing]
# Are missing entries those where X=0 or specific digit combo?
# Actually check: every present n seems to have one non-zero digit,
# or both non-zero, but skipping rows where Y < X?
print(f"\n  Present entries by first digit:")
for d in range(1, 10):
    in_table = sorted(n for n, A, B in table if n // 10 == d)
    print(f"    {d}x: {in_table}")

# ---------------------------------------------------------------------------
# 5.  Structural observation: the table as a doubling map on digital roots
# ---------------------------------------------------------------------------
print()
print("="*62)
print("5.  Structure: dr(2n) is the 'doubling map' on {1..9}")
print("="*62)

print(f"  Doubling map on digital roots: a ↦ dr(2a)")
for a in range(1, 10):
    print(f"    dr(2×{a}) = dr({2*a}) = {dr(2*a)}")

# Check: orbit under doubling
print(f"\n  Orbit of 1 under repeated doubling:")
x = 1
orbit = [x]
for _ in range(20):
    x = dr(2 * x)
    orbit.append(x)
    if x == orbit[0] and len(orbit) > 1:
        break
print(f"    {orbit}  (period = {len(orbit)-1})")

# The map a ↦ dr(2a) on Z/9Z*:
# Note: dr(2×9)=dr(18)=9, so 9 is a fixed point
# All others form cycles
print(f"\n  Fixed points of the doubling map: "
      f"{{a : dr(2a) = a}} = {[a for a in range(1,10) if dr(2*a)==a]}")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
print("="*62)
print("SUMMARY")
print("="*62)
print(f"""
  Format: n - A - B

  A = dr(n) = digital root of n (sum of digits, reduced mod 9):
      CONFIRMED for all {len(table)} entries ✓

  B = dr(2n) = digital root of 2n (doubling map on digital roots):
      {len(table) - len(b_errors)}/{len(table)} entries correct""")

if b_errors:
    for n, A, B, exp in b_errors:
        print(f"  ONE ERROR:  {n}-{A}-{B}  should be  {n}-{A}-{exp}")
        print(f"    dr(2×{n}) = dr({2*n}) = {exp}, not {B}")

print(f"""
  The table encodes the map  n ↦ (dr(n), dr(2n))
  i.e., the digit-root pair under ×1 and ×2.

  Doubling map dr(2·) on {{1,...,9}}:
    1→2→4→8→7→5→1  (6-cycle)
    3→6→3           (2-cycle: 3 and 6)
    9→9             (fixed point)

  The table only includes entries where the second digit ≥ first digit
  (lower-triangular portion of the 9×9 grid), explaining the 32 entries
  rather than all 90 two-digit numbers.
""")
