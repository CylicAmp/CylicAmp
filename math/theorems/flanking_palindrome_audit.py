"""
flanking_palindrome_audit.py

Centers drawn from digits {1, 5, 6}. Flanking digit = the member of {1,5,6}
absent from the center's digit set.

  555  → uses {5}       → missing {1,6} → DR(555)=6  → flank = 6
  1661 → uses {1,6}     → missing {5}   → DR(1661)=5 → flank = 5
  5115 → uses {1,5}     → missing {6}   → flank = 6
  6556 → uses {5,6}     → missing {1}   → flank = 1

All four centers are palindromes.

10-DIGIT CONSTRUCTIONS:
  5115 | flank(5115)=6 | flank(6556)=1 | 6556  =  5115616556
  reverse(5115616556) = 6556165115  =  6556 | 1 | 6 | 5115

  1661 | flank(1661)=5 | flank(1661)=5 | 1661  =  1661551661
  reverse(1661551661) = 1661551661  (palindrome)

FLANKED REPRESENTATIONS:
  6 ~ 555  ~ 6   DR(555)=6   ✓
  5 ~ 1661 ~ 5   DR(1661)=5  ✓
  6 ~ 5115 ~ 6   flank=6     ✓
  1 ~ 6556 ~ 1   flank=1     ✓

CROSS-SUMS:
  2561 + 2516 = 5077   DR(5077): 5+0+7+7=19→10→1
  251  + 256  = 507    DR(507):  5+0+7=12→3
─────────────────────────────────────────────────────────────────
"""

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = n % 9
    return r if r else 9


def digit_set(n):
    return set(int(d) for d in str(n))


FULL_SET = {1, 5, 6}

CENTERS = [
    (555,  6),
    (1661, 5),
    (5115, 6),
    (6556, 1),
]

# Flanking digit = missing member of {1,5,6}
for center, flank in CENTERS:
    ds = digit_set(center)
    missing = FULL_SET - ds
    check(flank in missing, f"{center} flank={flank} in missing={missing}", flank, missing)

# All centers are palindromes
for center, _ in CENTERS:
    s = str(center)
    check(s == s[::-1], f"{center} is palindrome", s, s[::-1])

# DR checks for 555 and 1661
check(dr(555)  == 6, "DR(555)=6",  dr(555),  6)
check(dr(1661) == 5, "DR(1661)=5", dr(1661), 5)

# 10-digit constructions
n1 = 5115616556
n1_rev = int(str(n1)[::-1])
check(n1_rev == 6556165115, "reverse(5115616556)=6556165115", n1_rev, 6556165115)

n2 = 1661551661
n2_rev = int(str(n2)[::-1])
check(n2_rev == n2, "1661551661 is palindrome", n2_rev, n2)

# Cross-sums
check(2561 + 2516 == 5077, "2561+2516=5077", 2561 + 2516, 5077)
check(dr(5077) == 1, "DR(5077)=1", dr(5077), 1)
check(251 + 256 == 507, "251+256=507", 251 + 256, 507)
check(dr(507) == 3, "DR(507)=3", dr(507), 3)

if __name__ == "__main__":
    print("Flanking Palindrome Audit — digit set {1,5,6}")
    print("=" * 62)
    print(f"\n  {'center':>10}  {'digits':>10}  {'missing':>8}  {'flank':>5}  {'DR':>3}")
    print("  " + "-" * 45)
    for center, flank in CENTERS:
        ds = digit_set(center)
        missing = FULL_SET - ds
        print(f"  {center:>10}  {str(sorted(ds)):>10}  {str(sorted(missing)):>8}  {flank:>5}  {dr(center):>3}")
    print(f"\n  10-digit constructions:")
    print(f"    5115|6|1|6556 = {5115616556}  reverse = {6556165115}")
    print(f"    1661|5|5|1661 = {1661551661}  (palindrome)")
    print(f"\n  Cross-sums:")
    print(f"    2561+2516 = 5077  DR=1")
    print(f"    251+256   = 507   DR=3")
    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
