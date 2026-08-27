"""
Universal analyzer: paste any number, get the full GF(37) framework answer.
Usage:  python3 cylicamp/analyze.py 137
        python3 cylicamp/analyze.py 17 19
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, "..")
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.join(_ROOT, "math", "primes"))
sys.path.insert(0, os.path.join(_ROOT, "math", "theorems"))

P = 37
MULT = 26  # 137 mod 37

SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
SEED    = {18, 24, 32}
IC      = {1, 10, 26}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}
NEG_H   = {11, 27, 36}
DARK_A  = {2, 15, 20}
D7      = {7, 33, 34}
NQR17   = {17, 22, 35}
C3      = {3, 4, 30}
C6      = {1, 6, 36}
C9      = {14, 29, 31}

NAMED = {
    "SA":      SA,
    "ST":      ST,
    "SEED":    SEED,
    "IC":      IC,
    "CASCADE": CASCADE,
    "TESLA":   TESLA,
    "NEG_H":   NEG_H,
    "DARK_A":  DARK_A,
    "D7":      D7,
    "NQR17":   NQR17,
    "C3":      C3,
    "C6":      C6,
    "C9":      C9,
}

ZETA_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
              37.586178, 40.918719, 43.327073, 48.005151, 49.773832]


def dr(n):
    n = abs(int(n))
    r = n % 9
    return 9 if r == 0 else r


def orbit_137(n):
    n = n % P
    if n == 0:
        return [0]
    seen, o = [], n
    for _ in range(P):
        if o in seen:
            break
        seen.append(o)
        o = (MULT * o) % P
    return seen


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def prime_index(n):
    """Return k such that n is the k-th prime (1-indexed). None if not prime."""
    if not is_prime(n):
        return None
    count, candidate = 0, 2
    while candidate <= n:
        if is_prime(candidate):
            count += 1
        candidate += 1
    return count


def prime_type(n):
    types = []
    if is_prime(n):
        types.append("PRIME")
        if is_prime(n + 2):
            types.append("twin-left")
        if is_prime(n - 2):
            types.append("twin-right")
        if is_prime(n + 4):
            types.append("cousin-left")
        if is_prime(n - 4):
            types.append("cousin-right")
        if is_prime(n + 6):
            types.append("sexy-left")
        if is_prime(n - 6):
            types.append("sexy-right")
        if is_prime(n + 6) and is_prime(n + 12):
            types.append("prime-triple-left")
        # Chamber (6n-1 / 6n+1)
        if n % 6 == 5:
            types.append("chamber-5 (χ₋₃=-1)")
        elif n % 6 == 1:
            types.append("chamber-1 (χ₋₃=+1)")
    return types


def membership(r):
    hits = [name for name, s in NAMED.items() if r in s]
    return hits if hits else ["—"]


def chi3(n):
    r = n % 3
    if r == 0:
        return 0
    return 1 if r == 1 else -1


def nearest_zeta(n):
    diffs = [(abs(n - z), i+1, z) for i, z in enumerate(ZETA_ZEROS)]
    diffs.sort()
    d, idx, z = diffs[0]
    return idx, z, d


def holonomy_class(n):
    r = n % P
    o = tuple(sorted(orbit_137(r)))
    # Named holonomy classes
    if set(o) == SEED:
        return "SEED holonomy class {18,24,32}"
    if set(o) == IC:
        return "IC holonomy class {1,10,26}"
    if set(o) == CASCADE:
        return "CASCADE holonomy class {8,13,24}"
    return f"orbit {list(o)}"


def analyze(n):
    r = n % P
    orb = orbit_137(r)
    orb_len = len(orb)
    members = membership(r)
    ptypes = prime_type(n)
    pidx  = prime_index(n)
    c3 = chi3(n)
    zn, zv, zd = nearest_zeta(n)
    hol = holonomy_class(n)

    print(f"\n{'='*60}")
    print(f"  n = {n}")
    print(f"{'='*60}")
    print(f"  DR(n)          = {dr(n)}")
    print(f"  n mod 37       = {r}")
    print(f"  Named sets     = {', '.join(members)}")
    print(f"  137-map orbit  = {orb}  (period {orb_len})")
    print(f"  Holonomy class = {hol}")
    print(f"  χ₋₃(n)        = {c3:+d}")
    prime_str = ', '.join(ptypes) if ptypes else 'composite'
    if pidx:
        prime_str += f'  [prime #{pidx}]'
    print(f"  Primality      = {prime_str}")
    print(f"  Nearest ζ zero = γ_{zn} = {zv:.6f}  (distance {zd:.6f})")

    # DR symmetric pair check (center 34)
    center = 34
    pair_sum = dr(center + n) + dr(center - n) if n <= center else None
    if pair_sum is not None:
        print(f"  DR(34+n)+DR(34-n) = {pair_sum} ≡ {pair_sum%9} mod9  (invariant=5: {pair_sum%9==5})")

    # Gauge holonomy connection (T215)
    print(f"  Gauge holonomy: Z/3Z class = {orb_len % 3}  (0=trivial, closes in {orb_len} steps)")

    print()
    return {
        "n": n, "dr": dr(n), "mod37": r, "sets": members,
        "orbit": orb, "chi3": c3, "prime_types": ptypes,
        "nearest_zero": (zn, zv, zd), "holonomy": hol
    }


def analyze_pair(a, b):
    print(f"\n{'='*60}")
    print(f"  PAIR: ({a}, {b})")
    print(f"{'='*60}")
    gap = b - a
    center = (a + b) / 2
    dr_a, dr_b = dr(a), dr(b)
    ra, rb = a % P, b % P

    print(f"  Gap            = {gap}")
    print(f"  Center         = {center}")
    print(f"  DR({a})        = {dr_a}")
    print(f"  DR({b})        = {dr_b}")
    print(f"  DR sum         = {dr_a + dr_b} → DR = {dr(dr_a + dr_b)}")
    print(f"  {a} mod 37     = {ra}  {membership(ra)}")
    print(f"  {b} mod 37     = {rb}  {membership(rb)}")
    print(f"  χ₋₃({a})      = {chi3(a):+d}")
    print(f"  χ₋₃({b})      = {chi3(b):+d}")

    if gap == 2:
        print(f"  Type: TWIN PRIME pair")
        mid = int(center)
        print(f"  Center {mid}: DR={dr(mid)}, mod37={mid%P}, χ₋₃={chi3(mid)}")
        print(f"  Chamber: {a}={'5-chamber' if a%6==5 else '1-chamber'}, "
              f"{b}={'5-chamber' if b%6==5 else '1-chamber'}")
    elif gap == 4:
        print(f"  Type: COUSIN PRIME pair")
    elif gap == 6:
        print(f"  Type: SEXY PRIME pair")
        print(f"  Sexy prime DR law: DR({a})+DR({b}) = {dr_a}+{dr_b} = {dr_a+dr_b} → {dr(dr_a+dr_b)}")

    print()


if __name__ == "__main__":
    args = [int(x) for x in sys.argv[1:] if x.lstrip('-').isdigit()]
    if not args:
        print("Usage: python3 cylicamp/analyze.py <n>  OR  <a> <b>")
        print("Examples:")
        print("  python3 cylicamp/analyze.py 137")
        print("  python3 cylicamp/analyze.py 11 17   # sexy prime pair")
        print("  python3 cylicamp/analyze.py 17 19   # twin prime pair")
        sys.exit(0)

    if len(args) == 1:
        analyze(args[0])
    elif len(args) == 2:
        analyze(args[0])
        analyze(args[1])
        analyze_pair(args[0], args[1])
    else:
        for a in args:
            analyze(a)
