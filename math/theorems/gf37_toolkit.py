"""
GF(37) Toolkit — fast classification and connection lookup for any integer.

Usage:
    from gf37_toolkit import classify, analyze, batch, orbit, dr

    classify(336)     # full class report
    analyze(248)      # all framework connections
    batch([1728, 744, 196883, 196884])  # table
    orbit(3)          # 137-map 3-cycle
    dr(336)           # digital root with chain
"""

P = 37

# ── Named classes ──────────────────────────────────────────────────────────────
IC        = frozenset({1,  10, 26})
SA        = frozenset({4,  9,  25, 30})
ST        = frozenset({3,  12, 21, 30})
CB        = frozenset({8,  13, 24})
SEED_ORB  = frozenset({18, 24, 32})
ORBIT_11  = frozenset({11, 27, 36})
D7        = frozenset({7,  33, 34})
SA_ORB    = frozenset({9,  12, 16})
NQR_17    = frozenset({17, 22, 35})
TESLA_ORB = frozenset({6,  8,  23})
DARK_A    = frozenset({2,  15, 20})

_QR37 = frozenset(n for n in range(1, P) if pow(n, (P-1)//2, P) == 1)
_PR37 = frozenset(g for g in range(2, P)
                  if all(pow(g, 36//q, P) != 1 for q in [2, 3]))

_CLASSES = [
    ('IC',        IC),
    ('SA',        SA),
    ('ST',        ST),
    ('CB',        CB),
    ('SEED_ORB',  SEED_ORB),
    ('ORBIT_11',  ORBIT_11),
    ('D7',        D7),
    ('SA_ORB',    SA_ORB),
    ('NQR_17',    NQR_17),
    ('TESLA_ORB', TESLA_ORB),
    ('DARK_A',    DARK_A),
]

# Framework constants for near-miss detection
_CONSTANTS = {
    'phi_37':    36,
    '137-map':   26,
    'SA-step':   9,
    'TESLA':     6,
    'seed_246':  246,
    'seed_mod':  24,
    '111=3x37':  111,
    '504=sig246':504,
    '137':       137,
}


# ── Core functions ──────────────────────────────────────────────────────────────

def dr(n: int) -> int:
    """Digital root (1-9 convention; 0 maps to 9)."""
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def dr_chain(n: int) -> str:
    """Digital root with reduction chain shown."""
    steps = [str(abs(n))]
    cur = abs(n)
    while cur >= 10:
        cur = sum(int(d) for d in str(cur))
        steps.append(str(cur))
    return ' → '.join(steps)


def orbit(n: int) -> tuple:
    """137-map 3-cycle of n mod 37."""
    r = n % P
    path = []
    for _ in range(3):
        path.append(r)
        r = (26 * r) % P
    return tuple(path)


def _named_classes(r: int) -> list:
    """Return list of all named-class labels that contain r."""
    names = []
    for label, s in _CLASSES:
        if r in s:
            names.append(label)
    if r == 0:
        names.append('SEAM')
    return names


def classify(n: int, verbose: bool = True) -> dict:
    """
    Full GF(37) classification of n.
    Returns dict; prints report if verbose=True.
    """
    r = n % P
    names = _named_classes(r)
    qr = r != 0 and r in _QR37
    pr = r in _PR37
    orb = orbit(n)
    d = dr(n)
    chain = dr_chain(n)

    # Overlaps with special sets
    flags = []
    if r in SA and r in ST:  flags.append('SA∩ST')
    if r in CB and r in SEED_ORB: flags.append('CB∩SEED_ORB')
    if r == 0: flags.append('SEAM')

    result = {
        'n':        n,
        'mod37':    r,
        'classes':  names,
        'flags':    flags,
        'QR':       qr,
        'PR':       pr,
        'orbit':    orb,
        'dr':       d,
        'dr_chain': chain,
    }

    if verbose:
        cls_str = ', '.join(names) if names else '(unclassed)'
        flag_str = '  [' + ', '.join(flags) + ']' if flags else ''
        print(f"  n = {n}")
        print(f"    mod 37  : {r}  →  {cls_str}{flag_str}")
        print(f"    sector  : {'QR' if qr else 'NQR' if r != 0 else 'SEAM'}  "
              f"{'primitive root' if pr else ''}")
        print(f"    orbit   : {orb[0]} → {orb[1]} → {orb[2]} → {orb[0]}")
        print(f"    DR      : {chain}  =  {d}")

    return result


def analyze(n: int) -> dict:
    """
    Deep analysis: classify + check divisibility, factoring, and proximity
    to framework constants.
    """
    print(f"\n{'='*52}")
    print(f"  ANALYZE  {n}")
    print(f"{'='*52}")

    result = classify(n)
    r = result['mod37']

    # Divisibility by small framework primes
    divs = []
    for p in [2, 3, 7, 37, 41, 43]:
        if n % p == 0:
            divs.append(f"{p}×{n//p}")
    if divs:
        print(f"    divides : {', '.join(divs)}")

    # n mod 9 and Z/9Z class
    mod9 = n % 9
    trinity = mod9 in {3, 6, 0}  # 0 here means 9 in DR convention
    print(f"    mod 9   : {mod9}  {'(trinity {3,6,9})' if trinity else '(doubling chain)'}")

    # Proximity to framework constants
    close = []
    for name, val in _CONSTANTS.items():
        if abs(n - val) <= 5:
            close.append(f"{name}={val} (Δ={n-val:+d})")
    if close:
        print(f"    near    : {', '.join(close)}")

    # Does n = a×37 + r for notable a?
    q = n // P
    if q in _QR37:
        print(f"    factor  : {n} = {q}×37 + {r}  ({q} ∈ QR₃₇)")
    elif q > 0:
        print(f"    factor  : {n} = {q}×37 + {r}")

    # DR chain
    print(f"    DR chain: {dr_chain(n)}")

    # Orbit classes
    orb = result['orbit']
    orb_classes = [', '.join(_named_classes(x)) or '—' for x in orb]
    print(f"    orbit classes: {orb[0]}({orb_classes[0]}) → "
          f"{orb[1]}({orb_classes[1]}) → {orb[2]}({orb_classes[2]})")

    return result


def batch(numbers, labels=None):
    """
    Print a compact table for a list of numbers.
    labels: optional list of name strings, same length as numbers.
    """
    if labels is None:
        labels = [str(n) for n in numbers]

    w = max(len(l) for l in labels)
    header = f"  {'label':<{w}}  {'n':>10}  {'mod37':>5}  {'class':<20}  {'DR':>3}  {'sector'}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for label, n in zip(labels, numbers):
        r = n % P
        names = _named_classes(r)
        cls = '+'.join(names) if names else f'{r}?'
        sector = 'QR' if (r and r in _QR37) else ('NQR' if r else 'SEAM')
        print(f"  {label:<{w}}  {n:>10}  {r:>5}  {cls:<20}  {dr(n):>3}  {sector}")


# ── Quick-check wrappers ───────────────────────────────────────────────────────

def check(*args):
    """Classify one or more numbers, compact output."""
    for n in args:
        classify(n)
        print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # CLI: python3 gf37_toolkit.py 336 248 1728 ...
        nums = []
        for arg in sys.argv[1:]:
            try:
                nums.append(int(arg))
            except ValueError:
                print(f"  skipping non-integer: {arg}")
        if len(nums) == 1:
            analyze(nums[0])
        else:
            batch(nums)
    else:
        # Demo
        print("GF(37) Toolkit — demo\n")
        print("── batch: j-function values ──────────────────")
        batch([1728, 744, 196883, 196884, 163, 640320],
              ['j(i)', 'j-const', 'Monster-rep', 'McKay', 'Heegner', '640320'])

        print("\n── analyze: 336 hours ────────────────────────")
        analyze(336)

        print("\n── classify: E8 invariants ───────────────────")
        check(248, 8, 240)

        print("── usage ─────────────────────────────────────")
        print("  python3 gf37_toolkit.py 336          # deep analysis")
        print("  python3 gf37_toolkit.py 248 8 240    # batch table")
