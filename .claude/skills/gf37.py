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


def mod9(n):
    """Signed-safe residue mod 9. Defined for every integer."""
    return n % 9


def dr(n):
    """
    Digital root, defined only for n >= 0.

    Raises on negatives rather than taking abs(): DR is the repeated
    digit sum of a non-negative integer, and abs() makes it disagree with
    the modular class. DR(-8) via abs() is 8, while -8 = 1 (mod 9), and
    printing both columns for the same value is a contradiction, not a
    fact. For signed input use mod9().
    """
    if n < 0:
        raise ValueError(
            f"dr() is undefined for negative input ({n}); "
            f"use mod9({n}) = {mod9(n)} for the signed class")
    return 9 if n and n % 9 == 0 else n % 9


def dr_basin(n):
    """Basin of the digital root. Non-negative input only (see dr)."""
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


def order_mod(a, n, max_steps=None):
    """Multiplicative order of a mod n, by direct search.

    max_steps bounds the search and returns None when exceeded, instead of
    looping to n-1. The order of 10 mod 2^31-1 is 1073741823; a caller that
    asks for it unbounded simply hangs. Default stays unbounded so existing
    callers, all of which use small moduli, are unchanged.
    """
    from math import gcd
    a %= n
    if n <= 1 or gcd(a, n) != 1:
        return None
    k, v = 1, a
    while v != 1:
        v = v * a % n
        k += 1
        if max_steps is not None and k > max_steps:
            return None
    return k


def rule30(n, bits=8):
    s = format(n % (1 << bits), f'0{bits}b')
    out = ''
    for i in range(bits):
        L, C, R = int(s[(i - 1) % bits]), int(s[i]), int(s[(i + 1) % bits])
        out += str(L ^ (C | R))
    return int(out, 2)


def factor(n):
    """
    Prime factorization. A negative n carries a -1 key so the product of
    the returned factors equals n; abs() is not applied silently. Same
    rule as dr(): a function must not return something that disagrees
    with its input.
    """
    if n == 0:
        raise ValueError("factor(0) is undefined")
    f = {}
    if n < 0:
        f[-1] = 1
        n = -n
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def factor_str(n):
    """Human-readable factorization, e.g. 111 -> '3 x 37', 9 -> '3^2'."""
    if abs(n) < 2:
        return str(n)
    parts = []
    for b, e in sorted(factor(n).items()):
        parts.append(str(b) if e == 1 else f"{b}^{e}")
    return " x ".join(parts)


def factor_product(f):
    """Reconstruct n from factor(n). Used to assert round-tripping."""
    v = 1
    for b, e in f.items():
        v *= b ** e
    return v


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


# ── cyclotomic / decimal-period primitives (T301–T304) ─────────────────────

def phi_d(d, a):
    """Phi_d(a), the d-th cyclotomic polynomial evaluated at integer a.
    Computed by exact division: x^d - 1 = prod_{e | d} Phi_e(x)."""
    num = a ** d - 1
    for e in range(1, d):
        if d % e == 0:
            num //= phi_d(e, a)
    return num


def totient(n):
    """Euler phi, from the factorization. deg Phi_n = totient(n)."""
    t = n
    for q in factor(n):
        t = t // q * (q - 1)
    return t


def order_slot(a, d, max_digits=18):
    """Primes p with ord_p(a) = d: the factors of Phi_d(a), minus the
    exception p | d. Complete for that d (T301).

    Returns None when Phi_d(a) is too large to factor by trial division
    rather than hanging. Callers must handle None — a silent hang is worse
    than a stated refusal.
    """
    # deg Phi_d = totient(d), so Phi_d(a) has about totient(d)*log10(a)
    # digits. Check that BEFORE computing it — an earlier version built the
    # integer first, which for d = 1666665 means a 1.6-million-digit number.
    t = totient(d)
    if t * len(str(abs(a))) > max_digits:
        return None
    v = phi_d(d, a)
    if len(str(abs(v))) > max_digits:
        return None
    out = []
    for q in factor(v):
        if a % q and order_mod(a, q) == d:
            out.append(q)
    return sorted(out)


def period(n, base=10, max_steps=10 ** 7):
    """(pre-period, period) of 1/n in the given base.
    pre = max over p | base of ceil(v_p(n) / v_p(base)); period = ord_q(base)
    on the part of n coprime to the base. period 0 means it terminates;
    period -1 means the order search exceeded max_steps and is unknown."""
    if n <= 1:
        return (0, 0)
    q, pre = n, 0
    for p, vb in factor(base).items():
        vn = 0
        while q % p == 0:
            q //= p
            vn += 1
        pre = max(pre, -(-vn // vb))
    return (pre, (order_mod(base, q, max_steps) or -1) if q > 1 else 0)


def repetend(a, b, base=2, max_len=4096):
    """The repeating digit block of a/b in the given base, as a string.
    Empty string when the expansion terminates.

    Returns None when the period exceeds max_len rather than building a
    string of that length. 1/9999991 has period 1666665; a caller that
    asks for it without a bound simply hangs. Callers must handle None.
    """
    from math import gcd
    g = gcd(a, b)
    a, b = a // g, b // g
    pre, per = period(b, base)
    if not per:
        return ''
    if per > max_len:
        return None
    r = a % b
    for _ in range(pre):
        r = r * base % b
    out = []
    for _ in range(per):
        r *= base
        out.append(r // b)
        r %= b
    return ''.join(map(str, out))


def complement_halves(a, b, base=2):
    """True iff base^(L/2) = -1 mod q, so the repetend's halves are
    digit-complements (each pair summing to base-1)."""
    from math import gcd
    g = gcd(a, b)
    b //= g
    q = b
    for p in factor(base):
        while q % p == 0:
            q //= p
    if q <= 1:
        return None
    L = order_mod(base, q)
    if L % 2:
        return False
    return pow(base, L // 2, q) == q - 1


# The three complete lists that meet at 37 (T304). Each is proved complete
# in its own theorem; they are recorded here as data, not recomputed.
L1_ORD137 = [7, 37, 73]      # ord_p(137) = 3          | Phi_3(137) = 18907
L2_CM     = [5, 17, 37]      # p = n^2+1, n = |R*| in {2,4,6}
L3_ORD10  = [37]             # ord_p(10)  = 3          | Phi_3(10)  = 111


def lists_containing(p):
    """Which of the three complete lists hold this prime."""
    return [n for n, L in (('L1', L1_ORD137), ('L2', L2_CM), ('L3', L3_ORD10))
            if p in L]
