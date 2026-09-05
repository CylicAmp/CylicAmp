"""
GF(37) Runner — Feed any input through every theorem module.

Takes a number, sequence, or string and runs it through the GF(37)
GF(37): orbit classification, DR, mod-37 residue, mirror detection,
layer accumulation, and connections to theorems.
"""

import sys
import os

P = 37

ORBITS = {
    'IC':               frozenset({1, 10, 26}),
    'SOVEREIGN_SPIRAL': frozenset({3, 4, 30}),
    'D7':               frozenset({7, 33, 34}),
    'SA_ORB':           frozenset({9, 12, 16}),
    'ORBIT_11':         frozenset({11, 27, 36}),
    'OUTLIER_ORB':      frozenset({21, 25, 28}),
    'DARK_A':           frozenset({2, 15, 20}),
    'NQR_5':            frozenset({5, 13, 19}),
    'TESLA_ORB':        frozenset({6, 8, 23}),
    'NQR_14':           frozenset({14, 29, 31}),
    'NQR_17':           frozenset({17, 22, 35}),
    'SEED_ORB':         frozenset({18, 24, 32}),
}

ORBIT_137_MAP = {
    'IC':               'multiplicative identity cluster',
    'SOVEREIGN_SPIRAL': 'sovereign anchors and targets',
    'D7':               '414-palindrome orbit',
    'SA_ORB':           'self-averaging orbit',
    'ORBIT_11':         'orbit of 11',
    'OUTLIER_ORB':      'outlier sector',
    'DARK_A':           'dark sector A',
    'NQR_5':            'non-quadratic residue, pivot 5',
    'TESLA_ORB':        'Tesla orbit (period anchor 8)',
    'NQR_14':           'non-quadratic residue 14',
    'NQR_17':           'non-quadratic residue 17',
    'SEED_ORB':         'seed orbit (246 mod 37 = 24)',
}


def orbit_of(v):
    v = v % P
    if v == 0:
        return 'SEAM'
    return next((name for name, s in ORBITS.items() if v in s), '?')


def dr(n):
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def map_137(n):
    """Apply the 137-map: f(n) = 137n mod 37 = 26n mod 37"""
    return (26 * n) % P


def orbit_cycle(n):
    """Full 3-cycle under the 137-map"""
    a = n % P
    if a == 0:
        return [0, 0, 0]
    b = map_137(a)
    c = map_137(b)
    return [a, b, c]


def digit_sum(n):
    return sum(int(d) for d in str(abs(n)))


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return all(n % i != 0 for i in range(3, int(n**0.5) + 1, 2))


def find_mirrors(numbers):
    """Find subsets of a list that produce the same sum."""
    from itertools import combinations
    subset_sums = {}
    for r in range(1, len(numbers) + 1):
        for combo in combinations(range(len(numbers)), r):
            s = sum(numbers[i] for i in combo)
            nums = tuple(numbers[i] for i in combo)
            if s not in subset_sums:
                subset_sums[s] = []
            subset_sums[s].append(nums)
    return {s: groups for s, groups in subset_sums.items() if len(groups) > 1}


def run(n):
    """Run a single integer through the full GF(37)."""
    print("=" * 62)
    print(f"INPUT: {n}")
    print("=" * 62)

    residue = n % P
    o = orbit_of(n)
    d = dr(n)
    ds = digit_sum(n)
    cyc = orbit_cycle(residue)

    print(f"\n  mod 37     = {residue}  →  {o}")
    if o != 'SEAM':
        print(f"               {ORBIT_137_MAP.get(o, '')}")
    print(f"  DR         = {d}  →  {orbit_of(d)}")
    print(f"  digit sum  = {ds}  →  {orbit_of(ds)}")
    print(f"  prime?     = {is_prime(n)}")

    print(f"\n  137-map 3-cycle from {residue}:")
    print(f"    {cyc[0]} ({orbit_of(cyc[0])}) → {cyc[1]} ({orbit_of(cyc[1])}) → {cyc[2]} ({orbit_of(cyc[2])}) → {cyc[0]}")
    print(f"    cycle sum = {sum(cyc)} = {sum(cyc) // P} × 37" if sum(cyc) % P == 0 else f"    cycle sum = {sum(cyc)}")

    neg = (-n) % P
    print(f"\n  negation: -{n} mod 37 = {neg}  →  {orbit_of(neg)}")
    print(f"    {n} + (-{n}) = 0 mod 37 = SEAM")
    print(f"    {orbit_of(n)} ↔ {orbit_of(neg)}")

    # SEAM check
    if residue == 0:
        print(f"\n  SEAM: {n} is an exact multiple of 37")
        print(f"  {n} / 37 = {n // P}, residue of quotient = {(n // P) % P} → {orbit_of(n // P)}")

    # Complement to 37
    comp = P - residue if residue != 0 else 0
    print(f"\n  complement: {residue} + {comp} = 37")
    print(f"    {orbit_of(residue)} + {orbit_of(comp)} = SEAM")

    print()


def run_sequence(numbers):
    """Run a sequence through GF(37) — layers, mirrors, accumulations."""
    print("=" * 62)
    print(f"SEQUENCE: {numbers}")
    print("=" * 62)

    print("\n  INDIVIDUAL ELEMENTS:")
    print(f"  {'n':>6}  mod37  orbit              DR")
    print(f"  {'-'*50}")
    for n in numbers:
        print(f"  {n:>6}  {n%P:>5}  {orbit_of(n):<20} {dr(n)}")

    print("\n  ADJACENT PAIR SUMS:")
    for i in range(len(numbers) - 1):
        s = numbers[i] + numbers[i+1]
        print(f"  {numbers[i]}+{numbers[i+1]}={s}  mod37={s%P}  {orbit_of(s)}  DR={dr(s)}")

    print("\n  ALL PAIR SUMS:")
    from itertools import combinations
    for a, b in combinations(numbers, 2):
        s = a + b
        print(f"  {a}+{b}={s}  mod37={s%P}  {orbit_of(s)}  DR={dr(s)}")

    print("\n  DR ACCUMULATION:")
    drs = [dr(n) for n in numbers]
    print(f"  DRs: {drs}")
    cumsum = 0
    for i, d in enumerate(drs):
        cumsum += d
        print(f"  +{d} → cumsum={cumsum}  {orbit_of(cumsum)}")

    print(f"\n  TOTAL SUM: {sum(numbers)}  mod37={sum(numbers)%P}  {orbit_of(sum(numbers))}")

    print("\n  MIRRORS (different subsets, same sum):")
    mirrors = find_mirrors(numbers)
    if mirrors:
        for s, groups in sorted(mirrors.items()):
            print(f"  sum={s}  mod37={s%P}  {orbit_of(s)}  DR={dr(s)}")
            for g in groups:
                print(f"    {' + '.join(str(x) for x in g)}")
    else:
        print("  none")

    print()


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print("Usage:")
        print("  python3 framework_runner.py 260")
        print("  python3 framework_runner.py 98 76 54 32 12")
        sys.exit(0)

    numbers = [int(a) for a in args]

    if len(numbers) == 1:
        run(numbers[0])
    else:
        run_sequence(numbers)
        print("\nINDIVIDUAL BREAKDOWNS:")
        for n in numbers:
            run(n)
