"""
Triple Grid Analysis — Odd/Even neighborhood technique.

For any number, extract digits, classify on the 1-9 O/E grid,
find complement neighbors, mirror, and compute the ET/EB/gap structure.

Usage:
    python3 triple_grid.py 246
    python3 triple_grid.py 135 789 246
"""

import sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from gf37_classes import (P, IC, SA, ST, CB, SEED_ORB, ORBIT_11, D7,
                           orbit_of, cross_classes, classify_residue)

# ── Constants ──────────────────────────────────────────────────────────────────

ALL9 = list(range(1, 10))  # 1..9
CENTER = 5                  # 5 is the center digit — neither O nor E in 8-grid

# ET and EB (top/bottom edges of the 1-9 grid)
ET = list(range(1, 10))   # 1,2,3,4,5,6,7,8,9
EB = list(range(9, 0, -1)) # 9,8,7,6,5,4,3,2,1
GAP = [abs(et - eb) for et, eb in zip(ET, EB)]  # 8,6,4,2,0,2,4,6,8


def oe(d):
    """Odd/Even/Center classification of digit d."""
    if d == CENTER: return '0'   # center / zero-space
    return 'E' if d % 2 == 0 else 'O'


def dr(n):
    if n == 0: return 9
    return (abs(n) - 1) % 9 + 1


def digits_of(n):
    return [int(d) for d in str(abs(n))]


def mirror(n):
    """Digit reversal."""
    return int(str(abs(n))[::-1])


def middle_digit(n):
    """Middle digit of a number (None if even length)."""
    s = str(abs(n))
    if len(s) % 2 == 1:
        return int(s[len(s)//2])
    return None


def complement_9(ds):
    """Digits from {1..9} not in ds."""
    return sorted(set(ALL9) - set(ds))


def sum_property(ds):
    """Check relationships like a+b=c within the digit set."""
    props = []
    for i in range(len(ds)):
        for j in range(len(ds)):
            if i == j: continue
            for k in range(len(ds)):
                if k in (i, j): continue
                if ds[i] + ds[j] == ds[k]:
                    props.append(f"{ds[i]}+{ds[j]}={ds[k]}")
    return props


def analyze(n):
    """Full triple-grid analysis of number n."""
    ds = digits_of(n)
    mir = mirror(n)
    mid = middle_digit(n)
    comp = complement_9(ds)
    dr_val = dr(n)
    mod37 = n % P

    print(f"\n{'='*56}")
    print(f"  TRIPLE GRID: {n}")
    print(f"{'='*56}")

    # ── Digit classification ───────────────────────────────────────
    print(f"\n  Digits: {ds}")
    print(f"  O/E:    {'  '.join(oe(d) for d in ds)}")
    evens   = [d for d in ds if d % 2 == 0]
    odds    = [d for d in ds if d % 2 != 0 and d != CENTER]
    centers = [d for d in ds if d == CENTER]
    print(f"  Evens:  {evens}   Odds: {odds}   Center(5): {centers}")

    # ── Complement ────────────────────────────────────────────────
    comp_e = [d for d in comp if d % 2 == 0]
    comp_o = [d for d in comp if d % 2 != 0 and d != CENTER]
    comp_c = [d for d in comp if d == CENTER]
    print(f"\n  Missing from {{1..9}}: {comp}  ({len(comp)} missing)")
    print(f"    Missing evens:  {comp_e}")
    print(f"    Missing odds:   {comp_o}")
    print(f"    Missing center: {comp_c if comp_c else 'none'}")

    # ── ET / EB / GAP grid ────────────────────────────────────────
    print(f"\n  ET (top):    {' '.join(str(x).rjust(2) for x in ET)}")
    print(f"  O/E:         {' '.join(oe(x).rjust(2) for x in ET)}")
    print(f"  GAP |ET-EB|: {' '.join(str(g).rjust(2) for g in GAP)}")
    print(f"  EB (bottom): {' '.join(str(x).rjust(2) for x in EB)}")

    # Highlight where our digits land on the grid
    markers = [('*' if (i+1) in ds else ' ').rjust(2) for i in range(9)]
    print(f"  Digit mark:  {''.join(markers)}")

    # ET positions for the actual digits
    print(f"\n  Grid positions of {ds}:")
    for d in ds:
        pos = d  # digit d is at position d on the ET grid (1-indexed)
        et_val = ET[pos-1]
        eb_val = EB[pos-1]
        gap_val = GAP[pos-1]
        print(f"    d={d}  ET={et_val}  EB={eb_val}  gap={gap_val}  O/E={oe(d)}")

    # ── Mirror and middle ─────────────────────────────────────────
    print(f"\n  Mirror:       {n} → {mir}")
    mid_sum = (n + mir) // 2
    mid_diff = abs(n - mir)
    print(f"  (n+mirror)/2: {mid_sum}")
    print(f"  |n-mirror|:   {mid_diff}")
    if mid is not None:
        print(f"  Middle digit: {mid}  O/E={oe(mid)}")

    # ── Sum / product properties ──────────────────────────────────
    props = sum_property(ds)
    if props:
        print(f"\n  Sum properties: {', '.join(props)}")
    digit_sum = sum(ds)
    digit_prod = 1
    for d in ds: digit_prod *= d
    print(f"  Digit sum:  {digit_sum}  DR={dr(digit_sum)}")
    print(f"  Digit prod: {digit_prod}")

    # ── GF(37) connections ─────────────────────────────────────────
    print(f"\n  GF(37):")
    print(f"    {n} mod 37 = {mod37}  orbit={orbit_of(mod37)}  cross={cross_classes(mod37)}")
    print(f"    DR({n}) = {dr_val}")
    print(f"    mirror {mir} mod 37 = {mir%P}  orbit={orbit_of(mir%P)}")
    if mid is not None:
        print(f"    middle digit {mid} → orbit={orbit_of(mid)}")
    # digit sum mod 37
    print(f"    digit sum {digit_sum} mod 37 = {digit_sum%P}  orbit={orbit_of(digit_sum%P)}")

    # Complement as a number (join digits)
    if len(comp) > 0:
        comp_n = int(''.join(map(str, comp)))
        print(f"    complement {comp} as number → {comp_n} mod 37 = {comp_n%P}  orbit={orbit_of(comp_n%P)}")

    return {
        'n': n, 'digits': ds, 'mirror': mir, 'complement': comp,
        'mod37': mod37, 'dr': dr_val, 'digit_sum': digit_sum,
    }


def batch_analyze(numbers):
    """Analyze multiple numbers and show a comparison table."""
    print("\n  COMPARISON TABLE")
    print(f"  {'n':>8}  {'digits':<10} {'O/E':<8} {'miss':<12} {'mirror':>8} {'mod37':>6} {'orbit':<16} {'DR':>3}")
    print("  " + "-"*80)
    for n in numbers:
        ds = digits_of(n)
        oe_str = ''.join(oe(d) for d in ds)
        comp = complement_9(ds)
        mir = mirror(n)
        r = n % P
        orb = orbit_of(r)
        print(f"  {n:>8}  {str(ds):<10} {oe_str:<8} {str(comp):<12} {mir:>8} {r:>6} {orb:<16} {dr(n):>3}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = [int(a) for a in sys.argv[1:] if a.isdigit()]

    if not args:
        # Default demo
        args = [246]

    if len(args) == 1:
        analyze(args[0])
    else:
        batch_analyze(args)
        for n in args:
            analyze(n)
