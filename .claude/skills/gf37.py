"""
Shared GF(37) library for the CylicAmp skills.

Single source of truth for orbits, classes, blocks, and the standard checks.
Import from any skill script:  sys.path.insert(0, <.claude/skills>) ; import gf37
"""

from math import gcd, isqrt

P = 37
MULT = 137 % P          # = 26
PRIMITIVE_ROOT = 2      # ord_37(2) = 36

ORBITS = {
    'IC':      {1, 10, 26},
    'DARK_A':  {2, 15, 20},
    'C3':      {3, 4, 30},
    'CAS_EXT': {5, 13, 19},
    'TESLA':   {6, 8, 23},
    'D7':      {7, 33, 34},
    'SA_ST_A': {9, 12, 16},
    'NEG_H':   {11, 27, 36},
    'C9':      {14, 29, 31},
    'NQR17':   {17, 22, 35},
    'SEED':    {18, 24, 32},
    'SA_ST_B': {21, 25, 28},
}

ANTIPODAL = [
    ('IC', 'NEG_H'), ('DARK_A', 'NQR17'), ('C3', 'D7'),
    ('TESLA', 'C9'), ('SA_ST_A', 'SA_ST_B'), ('SEED', 'CAS_EXT'),
]

# named sets from METHOD.md step 2 (distinct from the 12 orbits)
NAMED_SETS = {
    'SA':      {4, 9, 25, 30},          # sovereign anchors
    'ST':      {3, 12, 21, 30},         # sovereign targets, DR=3
    'CASCADE': {8, 13, 24},             # cascade base
}

_E2O = {}
for _n, _s in ORBITS.items():
    for _e in _s:
        _E2O[_e] = _n

_DLOG = {pow(PRIMITIVE_ROOT, k, P): k for k in range(P - 1)}

# the 12 Z/12Z class representatives, in class order
CLASS_ORDER = [_E2O[pow(PRIMITIVE_ROOT, m, P)] for m in range(12)]


def orbit(x):
    """Named orbit of x mod 37, or 'SEAM' when 37 | x."""
    return _E2O.get(x % P, 'SEAM')


def cls(x):
    """Z/12Z class of x (discrete log mod 12). None on SEAM."""
    r = x % P
    return None if r == 0 else _DLOG[r] % 12


def orbit_triple(x):
    """The 137-map orbit {x, 26x, 26^2 x} = {x, 100x, 10x} mod 37."""
    r = x % P
    return sorted({r, (r * MULT) % P, (r * MULT * MULT) % P})


def antipode(name):
    for a, b in ANTIPODAL:
        if a == name:
            return b
        if b == name:
            return a
    return None


def named_sets(x):
    r = x % P
    return sorted(n for n, s in NAMED_SETS.items() if r in s)


def block(k):
    """3-digit repeating block of k/37. Depends only on k mod 37."""
    return f"{(k % P * 1000) // P % 1000:03d}"


def dr(n):
    """Digital root."""
    n = abs(n)
    return 9 if n and n % 9 == 0 else n % 9


def dr_basin(n):
    d = dr(n)
    if d in (3, 6, 9):
        return 'Trinity'
    if d in (1, 4, 7):
        return 'Basin'
    return 'Valve'


def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    return all(n % i for i in range(3, isqrt(n) + 1, 2))


def prime_profile(n):
    """Primality and the neighbour types from METHOD.md step 6."""
    if not is_prime(n):
        return {'prime': False}
    return {
        'prime': True,
        'twin': is_prime(n - 2) or is_prime(n + 2),
        'cousin': is_prime(n - 4) or is_prime(n + 4),
        'sexy': is_prime(n - 6) or is_prime(n + 6),
        'sophie_germain': is_prime(2 * n + 1),
        'safe': n > 2 and (n - 1) % 2 == 0 and is_prime((n - 1) // 2),
        'chamber': n % 6,
    }


def order_mod(a, n):
    """Multiplicative order of a mod n, or None if not coprime."""
    a %= n
    if gcd(a, n) != 1:
        return None
    k, v = 1, a
    while v != 1:
        v = (v * a) % n
        k += 1
    return k


def rule30(n, bits=8):
    s = format(n % (1 << bits), f'0{bits}b')
    out = ''
    for i in range(bits):
        L, C, R = int(s[(i - 1) % bits]), int(s[i]), int(s[(i + 1) % bits])
        out += str(L ^ (C | R))
    return int(out, 2)


def factor(n):
    f, d = {}, 2
    n = abs(n)
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


# ── Riemann zeros: first 30 imaginary parts, for the standing RH check ──
GAMMA = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178,
    40.918719, 43.327073, 48.005151, 49.773832, 52.970321, 56.446248,
    59.347044, 60.831779, 65.112544, 67.079811, 69.546402, 72.067158,
    75.704691, 77.144840, 79.337375, 82.910381, 84.735493, 87.425275,
    88.809111, 92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
]


def rh_hits(r):
    """Indices n where floor(gamma_n) = r (mod 37)."""
    return [i for i, g in enumerate(GAMMA, 1) if int(g) % P == r % P]
