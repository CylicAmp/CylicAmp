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

    propagate_theme(n)
    full_spectrum(n)

    return {
        'n': n, 'digits': ds, 'mirror': mir, 'complement': comp,
        'mod37': mod37, 'dr': dr_val, 'digit_sum': digit_sum,
    }


def find_themes(ds):
    """All arithmetic rules satisfied by ordered triple ds=[a,b,c]."""
    a, b, c = ds[0], ds[1], ds[2]
    themes = []
    if a + b == c: themes.append(('sum',  f"{a}+{b}={c}"))
    if b + c == a: themes.append(('sum',  f"{b}+{c}={a}"))
    if a + c == b: themes.append(('sum',  f"{a}+{c}={b}"))
    if a - b == c > 0: themes.append(('diff', f"{a}-{b}={c}"))
    if b - a == c > 0: themes.append(('diff', f"{b}-{a}={c}"))
    if c - b == a > 0: themes.append(('diff', f"{c}-{b}={a}"))
    if a * b == c: themes.append(('prod', f"{a}×{b}={c}"))
    if b * c == a: themes.append(('prod', f"{b}×{c}={a}"))
    return themes


def full_spectrum(n):
    """
    Score ALL complement arrangements by deviation from the original theme.
    deviation = |a+b−c| for sum theme (or analogous for diff/prod).
    Range: 0 (perfect — same rule as original) → max (maximally opposed).
    """
    from itertools import permutations
    from collections import defaultdict, Counter

    ds = digits_of(n)
    comp = complement_9(ds)
    themes = find_themes(ds)

    if not themes or len(comp) < 3:
        return

    # Prefer a sum theme; fall back to whatever is present
    primary = next((t for t in themes if t[0] == 'sum'), themes[0])
    theme_type, theme_label = primary

    print(f"\n  {'─'*54}")
    print(f"  FULL SPECTRUM [{theme_label}]")

    entries = []
    for perm in permutations(comp, 3):
        a, b, c = perm
        if theme_type == 'sum':
            dev = abs(a + b - c)
        elif theme_type == 'diff':
            dev = abs(abs(a - b) - c)
        else:  # prod
            dev = abs(a * b - c)
        num = int(''.join(map(str, perm)))
        r = num % P
        orb = orbit_of(r)
        cross = cross_classes(r)
        entries.append((dev, perm, num, r, orb, cross))

    by_dev = defaultdict(list)
    for e in entries:
        by_dev[e[0]].append(e)

    max_dev = max(by_dev)

    print(f"  dev=0 aligned [{theme_label}]  →  dev={max_dev} maximally opposed")
    print(f"\n  {'dev':>4}  {'n':>5}  {'SA':>4}  {'ST':>4}  {'CB':>4}  top orbit")
    print(f"  {'─'*52}")

    for dev in sorted(by_dev):
        group = by_dev[dev]
        sa = sum(1 for e in group if e[3] in SA)
        st = sum(1 for e in group if e[3] in ST)
        cb = sum(1 for e in group if e[3] in CB)
        top = Counter(e[4] for e in group).most_common(1)[0][0]
        tag = '  ◀ ALIGNED' if dev == 0 else ('  ◀ OPPOSED' if dev == max_dev else '')
        print(f"  {dev:>4}  {len(group):>5}  {sa:>4}  {st:>4}  {cb:>4}  {top:<24}{tag}")

    # Detail: perfect alignment only
    if 0 in by_dev:
        print(f"\n  ── Perfect alignment ──")
        for dev, perm, num, r, orb, cross in sorted(by_dev[0], key=lambda x: x[2]):
            cs = '+'.join(cross) if cross else '—'
            rule = (f"{perm[0]}+{perm[1]}={perm[2]}" if theme_type == 'sum'
                    else f"{perm[0]}-{perm[1]}={perm[2]}")
            print(f"    {num:>8}  mod37={r:>2}  {orb:<22}  {cs:<10}  {rule}")

    return by_dev


def propagate_theme(n):
    """
    Find all numbers from the complement of n's digits (in {1..9})
    that satisfy the same arithmetic themes as n.
    Returns dict of theme_label → list of matching (triple, number, mod37, orbit).
    """
    from itertools import permutations
    ds = digits_of(n)
    comp = complement_9(ds)
    themes = find_themes(ds)

    print(f"\n  {'─'*54}")
    print(f"  THEME PROPAGATION: {n} → complement {comp}")
    print(f"  Themes: {[t[1] for t in themes]}")

    all_matches = []
    for theme_type, label in themes:
        matches = []
        for perm in permutations(comp, 3):
            a, b, c = perm
            hit = (
                (theme_type == 'sum'  and a + b == c) or
                (theme_type == 'diff' and a - b == c > 0) or
                (theme_type == 'prod' and a * b == c)
            )
            if hit:
                num = int(''.join(map(str, perm)))
                r = num % P
                orb = orbit_of(r)
                cross = cross_classes(r)
                matches.append((perm, num, r, orb, cross))

        if matches:
            print(f"\n  Theme [{label}] — {len(matches)} neighbors:")
            print(f"    {'number':>8}  {'mod37':>5}  {'orbit':<20}  {'cross'}")
            for perm, num, r, orb, cross in matches:
                cs = '+'.join(cross) if cross else '—'
                rule = f"{perm[0]}+{perm[1]}={perm[2]}" if theme_type=='sum' else f"{perm[0]}-{perm[1]}={perm[2]}"
                print(f"    {num:>8}  {r:>5}  {orb:<20}  {cs:<14}  {rule}")
            all_matches.extend(matches)

    # Summary
    if all_matches:
        from collections import Counter
        orbit_freq = Counter(m[3] for m in all_matches)
        sa_hits = [(m[1], m[2]) for m in all_matches if m[2] in SA]
        st_hits = [(m[1], m[2]) for m in all_matches if m[2] in ST]
        print(f"\n  SA hits: {sa_hits}")
        print(f"  ST hits: {st_hits}")
        print(f"  Orbit freq: {dict(orbit_freq.most_common())}")

    return all_matches


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
