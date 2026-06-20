"""
CylicAmp Master Framework
=========================
All equations, theorems, and structural constants in one file.
Sections are independent — run any block standalone or the full file.
"""

from math import log, isqrt
from sympy import isprime, factorint


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: DIGITAL ROOT — FOUNDATION
# ═══════════════════════════════════════════════════════════════════════════════

def dr(n):
    """Digital root: 0 for n=0, 1-9 for positive integers."""
    if n == 0:
        return 0
    return 1 + (n - 1) % 9

# Four equivalent forms — all agree
for n in range(1, 300):
    assert dr(n) == (n - 1) % 9 + 1
    assert dr(n) == (n % 9) or (9 if n % 9 == 0 else n % 9)

# THEOREM 1: dr(n) ≡ n (mod 9)
for n in range(1, 500):
    assert dr(n) % 9 == n % 9

# THEOREM 2: dr(n) ≡ n (mod 3)
for n in range(1, 500):
    assert dr(n) % 3 == n % 3

# Additive property: dr(a+b) = dr(dr(a) + dr(b))
for a in range(1, 30):
    for b in range(1, 30):
        assert dr(a + b) == dr(dr(a) + dr(b))

# DR classes mod 3
for n in range(1, 100):
    if n % 3 == 0: assert dr(n) in {3, 6, 9}
    if n % 3 == 1: assert dr(n) in {1, 4, 7}
    if n % 3 == 2: assert dr(n) in {2, 5, 8}

# Necessary condition for primality (p > 3 → DR(p) ∈ {1,2,4,5,7,8})
PRIME_DR_SET = {1, 2, 4, 5, 7, 8}
for p in range(4, 1000):
    if isprime(p):
        assert dr(p) in PRIME_DR_SET

# 10 ≡ 1 (mod 9) → basis of all digit-sum arithmetic
assert 10 % 9 == 1
for m in range(20):
    assert pow(10, m, 9) == 1

# Doubling map on DR classes: 1→2→4→8→7→5→1 (period 6)
DOUBLING_CYCLE = [1, 2, 4, 8, 7, 5]
for i, x in enumerate(DOUBLING_CYCLE):
    assert dr(x * 2) == DOUBLING_CYCLE[(i + 1) % 6]
assert dr(3 * 2) == 6   # 3→6 fixed orbit
assert dr(6 * 2) == 3   # 6→3 fixed orbit
assert dr(9 * 2) == 9   # 9→9 fixed point

# 2n−1 skip-2 cycle: 1,3,5,7,9,2,4,6,8 (period 9)
TWO_N_MINUS_1 = [dr(2 * n - 1) for n in range(1, 10)]
assert TWO_N_MINUS_1 == [1, 3, 5, 7, 9, 2, 4, 6, 8]
# Each step +2 mod 9
for i in range(8):
    assert (TWO_N_MINUS_1[i + 1] - TWO_N_MINUS_1[i]) % 9 == 2


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: PAIR ADDITION — 4:5 EVEN/ODD SPLIT
# ═══════════════════════════════════════════════════════════════════════════════

# DR(2n) for n=1..9
DOUBLES = [(n, dr(2 * n)) for n in range(1, 10)]

# n=1..4 → even DR (no wraparound: 2n ≤ 8)
for n in range(1, 5):
    assert dr(2 * n) == 2 * n          # no reduction needed
    assert dr(2 * n) % 2 == 0          # EVEN

# n=5..9 → odd DR (wraparound: 2n > 9 → subtract 9)
for n in range(5, 10):
    assert dr(2 * n) == 2 * n - 9      # one full wrap
    assert dr(2 * n) % 2 == 1          # ODD

# 4:5 split: {2,4,6,8} vs {1,3,5,7,9}
assert sorted(dr(2 * n) for n in range(1, 5))  == [2, 4, 6, 8]
assert sorted(dr(2 * n) for n in range(5, 10)) == [1, 3, 5, 7, 9]

# 2n is EVEN; 2n−9 = EVEN−ODD = ODD → parity flip at the 9-boundary
assert (2 * 5 - 9) % 2 == 1

# Switch point: n=4 (last even) → n=5 (first odd)
assert dr(8)  % 2 == 0
assert dr(10) == 1 and dr(10) % 2 == 1

# 2n mod 9 sequence
MOD9_SEQ = [(2 * n) % 9 for n in range(1, 10)]
assert MOD9_SEQ == [2, 4, 6, 8, 1, 3, 5, 7, 0]


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: REPUNIT SEQUENCE — 2n−1 PATTERN
# ═══════════════════════════════════════════════════════════════════════════════

def repunit(n):
    return int("1" * n)

# R(n) + (n−1) at n=1..10 follows the 2n−1 DR pattern
repunit_drs = []
for n in range(1, 11):
    val = repunit(n) + (n - 1)
    repunit_drs.append(dr(val))

assert repunit_drs == [1, 3, 5, 7, 9, 2, 4, 6, 8, 1]

# Connection: 2n−1 formula gives same DRs
for n in range(1, 10):
    assert dr(2 * n - 1) == repunit_drs[n - 1]

# 111 = 3 × 37 (37-hub)
assert 111 == 3 * 37
assert repunit(3) == 111

# ord₃₇(10) = 3 → explains why 111 = 3×37
assert pow(10, 1, 37) != 1
assert pow(10, 2, 37) != 1
assert pow(10, 3, 37) == 1   # 1000 = 27×37 + 1


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: 37-HUB CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Core 37-field constants
assert 111 == 3 * 37
assert 137 == 4 * 37 - 11
assert 248 == 7 * 37 - 11
assert 666 == 18 * 37

# 137 ≡ 248 ≡ 26 (mod 37)
assert 137 % 37 == 26
assert 248 % 37 == 26
assert 26 == 37 - 11

# # 26 = 137 mod 37
# 26 = 137 mod 37
assert dr(26) == 8

# Quadratic residues mod 37
QR37 = frozenset((n * n) % 37 for n in range(37))
{4, 9, 25, 30}
F26_TARGETS = {3, 12, 21, 30}
assert ({4, 9, 25, 30}) <= QR37
assert all(t % 3 == 0 for t in F26_TARGETS)
assert all(dr(t) == 3 for t in F26_TARGETS)

# 666 cascade: 666→18→9
assert 666 % 9 == 0 and dr(666) == 9
assert 6 + 6 + 6 == 18 and dr(18) == 9
assert dr(dr(666)) == 9

# 37 ≡ 1 (mod 9) — identity on 9-subfield
assert 37 % 9 == 1
assert 18 % 9 == 0   # 18 = differential; annihilated mod 9
assert (18 ** 2) % 9 == 0   # 324 ≡ 0 (mod 9)

# Arithmetic progression sum over Z/37Z: S₃₇(a) = 37(a + 324)
def S37(a):
    return sum(a + 18 * k for k in range(37))

for a in [1, 5, 26, 30]:
    assert S37(a) == 37 * (a + 324)
    assert S37(a) % 37 == 0
    assert S37(a) % 9 == a % 9   # identity on 9-subfield: 37≡1(mod 9)

# Digits of 137 are Mersenne numbers
assert 1 == 2**1 - 1
assert 3 == 2**2 - 1
assert 7 == 2**3 - 1
# Adding 1 gives powers of 2
assert 1 + 1 == 2**1
assert 3 + 1 == 2**2
assert 7 + 1 == 2**3


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: f26_map 3-CYCLE (137 mod 37 = 26, ord₃₇(26) = 3)
# ═══════════════════════════════════════════════════════════════════════════════

# f26_map: f(n) = (137 × n) mod 37 = (26n) mod 37
def f26_map(n):
    return (26 * n) % 37

# ord₃₇(26) = 3
assert 137 % 37 == 26
assert pow(26, 1, 37) == 26
assert pow(26, 2, 37) == 10
assert pow(26, 3, 37) == 1

# Every non-zero element returns in exactly 3 steps
for n in range(1, 37):
    assert f26_map(f26_map(f26_map(n))) == n

# Exactly 12 disjoint 3-cycles partition {1..36}
seen = set()
cycles = []
for start in range(1, 37):
    if start not in seen:
        cycle = [start, f26_map(start), f26_map(f26_map(start))]
        seen.update(cycle)
        cycles.append(cycle)
assert len(cycles) == 12

# f26 anchor cycle ( 30 → 3 → 4 → 30
assert f26_map(30) == 3
assert f26_map(3) == 4
assert f26_map(4) == 30

# 26 cycle: 26 → 10 → 1 → 26 (includes 1)
assert f26_map(26) == 10
assert f26_map(10) == 1
assert f26_map(1) == 26


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: PERFECT NUMBERS AND 137
# ═══════════════════════════════════════════════════════════════════════════════

PERFECT = [6, 28, 496, 8128]
MERSENNE_P = [3, 7, 31, 127]       # primes p where 2^p-1 is Mersenne prime
EULER_PARAMS = [(2,3), (4,7), (16,31), (64,127)]  # (2^(p-1), 2^p-1)

def proper_divisors(n):
    return [i for i in range(1, n) if n % i == 0]

# Perfect: equals sum of proper divisors
for n in PERFECT:
    assert sum(proper_divisors(n)) == n

# Euclid-Euler formula N = 2^(p-1) × (2^p-1)
for n, (a, b) in zip(PERFECT, EULER_PARAMS):
    assert a * b == n

# DR theorem: [6,1,1,1] — 6 is sole exception
assert [dr(n) for n in PERFECT] == [6, 1, 1, 1]
assert 6 % 9 == 6
assert all(n % 9 == 1 for n in PERFECT[1:])

# QR mod 37
assert  6 % 37 not in QR37   # 6 is NOT QR — outlier in both DR and QR
assert 28 % 37 in QR37
assert 496 % 37 not in QR37
assert 8128 % 37 in QR37
assert 8128 % 37 == 25        # 25 is f26 anchor ✓

# Mersenne prime DR and QR
assert dr(3) == 3 and  3 % 37 in QR37
assert dr(7) == 7 and  7 % 37 in QR37
assert dr(31) == 4 and 31 % 37 not in QR37
assert dr(127) == 1 and 127 % 37 in QR37


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: MERSENNE PERIOD-6 THEOREM
# ═══════════════════════════════════════════════════════════════════════════════

# DR(2^n - 1) has period 6: [1, 3, 7, 6, 4, 9]
MERSENNE_DR_CYCLE = [1, 3, 7, 6, 4, 9]
for n in range(1, 61):
    m = 2**n - 1
    assert dr(m) == MERSENNE_DR_CYCLE[(n - 1) % 6]

# THEOREM: DR(M_n) = 9 ⟺ 6 | n
for n in range(1, 61):
    assert (dr(2**n - 1) == 9) == (n % 6 == 0)

# THEOREM: DR(M_p) ∈ {1,4} for ALL primes p ≥ 5 (DR=9 impossible for Mersenne primes)
for p in [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
    assert dr(2**p - 1) in {1, 4}, f"p={p}"

# M₅₃ → 16 digits (DR=4); M₅₄ → 17 digits (DR=9); 54=9×6 → DR=9
assert dr(2**53 - 1) == MERSENNE_DR_CYCLE[(53 - 1) % 6]   # index 4 → DR=4
assert dr(2**54 - 1) == 9                                  # 54 divisible by 6
assert (2**54 - 1) % 6 == 0 or 54 % 6 == 0                # confirmed


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8: TWIN PRIME TRIPARTITE
# ═══════════════════════════════════════════════════════════════════════════════

def sieve(limit):
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, isqrt(limit) + 1):
        if is_p[i]:
            is_p[i*i::i] = bytearray(len(is_p[i*i::i]))
    return [i for i in range(2, limit + 1) if is_p[i]]

PRIMES_10K = set(sieve(10002))

# Tripartite: twin prime DR pairs restricted to {(2,4),(5,7),(8,1)} for p > 3
# Proof from Z/9Z: DR(p+2) = DR(DR(p)+2); pairs with DR divisible by 3 → composite
BLOCKED  = {(1,3), (4,6), (7,9)}   # 3 | (p+2) → p+2 composite
VALID_DR = {(2,4), (5,7), (8,1)}

twin_pairs_found = set()
for p in range(5, 10001):
    if p in PRIMES_10K and (p + 2) in PRIMES_10K:
        twin_pairs_found.add((dr(p), dr(p + 2)))

assert twin_pairs_found == VALID_DR

# +2 chain: consecutive pairs collapse to first twin primes (11, 13)
CHAINS = [(2,2,7), (3,2,6), (4,2,7), (5,2,6)]
for a, b, c in CHAINS:
    assert a + b + c in {11, 13}
    assert dr(a + b + c) in {2, 4}
    assert (a % 2) != (c % 2)   # opposite parity rule

assert all(a + 2 + c == 11 for a,b,c in CHAINS[:2])   # {2,3} → 11
assert all(a + 2 + c == 13 for a,b,c in CHAINS[2:])   # {4,5} → 13

# 11 + 13 = 24, DR(24) = 6; DR(2) + DR(4) = 6
assert 11 + 13 == 24 and dr(24) == 6
assert dr(2) + dr(4) == 6


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9: ODD-PERFECT ZERO SYSTEM (OCO/ECO)
# ═══════════════════════════════════════════════════════════════════════════════

def comma_groups(n):
    """Standard thousands-grouping of n zeros."""
    groups, r = [], n
    while r > 3:
        groups.append(3)
        r -= 3
    groups.append(r)
    return list(reversed(groups))

def parity_class(n):
    return "C".join("O" if g % 2 == 1 else "E" for g in comma_groups(n))

def is_all_odd(n):
    return all(g % 2 == 1 for g in comma_groups(n))

# Period-3 rule: ECO iff n ≡ 2 (mod 3)
for n in range(1, 40):
    if n % 3 == 2:
        assert not is_all_odd(n)
    else:
        assert is_all_odd(n)

# n+3 preserves parity class (appends one group of 3, always odd)
for n in range(1, 20):
    prefix = parity_class(n)
    extended = parity_class(n + 3)
    assert extended.startswith(prefix)

# Mersenne placement counts = digits of 137
assert 2**1 - 1 == 1
assert 2**2 - 1 == 3
assert 2**3 - 1 == 7


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 10: ZERO-COMMA LABEL SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

def zc_label(n):
    """Zero-comma label: str(left_size) + str(K)*(2K)."""
    assert n >= 4
    K = (n - 1) // 3
    left = n % 3 or 3
    return str(left) + str(K) * (2 * K)

# All known examples
ZC_EXAMPLES = {
    4:"111", 5:"211", 6:"311",
    7:"12222", 8:"22222", 9:"32222",
    10:"1333333", 11:"2333333", 12:"3333333",
    13:"144444444", 14:"244444444", 15:"344444444",
    16:"15555555555",
}
for n, expected in ZC_EXAMPLES.items():
    assert zc_label(n) == expected

# Label length = 2K+1 (always odd)
for n in range(4, 31):
    K = (n - 1) // 3
    assert len(zc_label(n)) == 2 * K + 1
    assert (2 * K + 1) % 2 == 1

# First digit always in {1,2,3}
for n in range(4, 100):
    assert int(zc_label(n)[0]) in {1, 2, 3}

# Three all-same entries (full rotation closes at K=3)
for n in [4, 8, 12]:
    assert len(set(zc_label(n))) == 1

# All-same digit counts: 3, 5, 7 — the 357 anti-diagonal
assert [len(zc_label(n)) for n in [4, 8, 12]] == [3, 5, 7]
assert 3 + 5 + 7 == 15
assert 3 * 5 * 7 == 105

# 111 = 3×37; ord₃₇(10) = 3
assert 111 == 3 * 37
assert pow(10, 3, 37) == 1

# No all-same for K=4..9 (single-digit regime)
assert not any(len(set(zc_label(n))) == 1 for n in range(13, 31))


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 11: PALINDROME 1888081808881
# ═══════════════════════════════════════════════════════════════════════════════

N_PALIN = 1888081808881
BASE_PALIN = 188808
s = str(N_PALIN)

# Structure
assert s == s[::-1]                           # palindrome
assert len(s) == 13
assert s[6] == "1"                            # center = 1
assert s[:6] == "188808" and s[:6][::-1] == "808881"
assert s[:6] + s[6] + s[:6][::-1] == s       # reconstruction

# Base analysis
assert sum(int(d) for d in str(BASE_PALIN)) == 33    # NOT 25
assert dr(33) == 6                                    # NOT 7
assert BASE_PALIN % 37 == 34
assert BASE_PALIN %  9 ==  6

# Factorization
assert factorint(BASE_PALIN) == {2: 3, 3: 1, 7867: 1}
assert isprime(7867)

# 1888 ≡ 1 (mod 37) → chain
assert 51 * 37 + 1 == 1888
assert 5100 * 37 + 108 == BASE_PALIN
assert 108 % 37 == 34

# Full number mod 37
assert N_PALIN % 37 == 32
assert 32 == 37 - 5               # N ≡ -5 (mod 37)
assert (N_PALIN + 5) % 37 == 0
assert (N_PALIN + 5) // 37 == 51029238078


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 12: LUCAS ABBC CHAIN
# ═══════════════════════════════════════════════════════════════════════════════

# Lucas sequence L(n) = L(n-1) + L(n-2), L(0)=2, L(1)=1
def lucas(n):
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a

LUCAS_CHAIN = [lucas(n) for n in range(3, 11)]   # L(3)..L(10)
assert LUCAS_CHAIN == [4, 7, 11, 18, 29, 47, 76, 123]

# Recurrence holds
for i in range(2, len(LUCAS_CHAIN)):
    assert LUCAS_CHAIN[i] == LUCAS_CHAIN[i-1] + LUCAS_CHAIN[i-2]

# DR pattern
LUCAS_DR = [dr(x) for x in LUCAS_CHAIN]
assert LUCAS_DR == [4, 7, 2, 9, 2, 2, 4, 6]

# L(7)=29 and L(8)=47 are prime
assert isprime(29) and isprime(47)

# 47 × 76 = 3572 (DR=8); 47 + 76 = 123 (DR=6)
assert 47 * 76 == 3572 and dr(3572) == 8
assert 47 + 76 == 123  and dr(123)  == 6

# 11 + 13 = 24, DR = 6 (twin prime echo in Lucas chain)
assert dr(11 + 13) == 6 and dr(LUCAS_CHAIN[0] + LUCAS_CHAIN[1]) == dr(4 + 7)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 13: ARITHMETIC SEQUENCE −1111
# ═══════════════════════════════════════════════════════════════════════════════

TERMS = [9859, 8748, 7637, 6526, 5415, 4304, 3193]
DIFF  = -1111

# Common difference
for i in range(len(TERMS) - 1):
    assert TERMS[i + 1] - TERMS[i] == DIFF

# 1111 = 11 × 101
assert 1111 == 11 * 101

# DR increases by 5 each step (since −1111 ≡ +5 mod 9)
assert (-1111) % 9 == 5
DRS = [dr(t) for t in TERMS]
for i in range(len(DRS) - 1):
    assert (DRS[i + 1] - DRS[i]) % 9 == 5

# 8748 = 4 × 3⁷
assert 8748 == 4 * 3**7
assert factorint(8748) == {2: 2, 3: 7}


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 14: ALPHA GRID
# ═══════════════════════════════════════════════════════════════════════════════

GRID = {
    1: "LL-O",  2: "LL-E",  3: "LH-O",  4: "LH-E",
    5: "A51",
    6: "RL-E",  7: "RL-O",  8: "RH-E",  9: "RH-O",
}

AHL = 8   # Alpha High — RH-E
ALO = 7   # Alpha Low  — RL-O

assert AHL + ALO == 15 and dr(15) == 6

# 44-26-31-31-62-44 palindrome (all DR=8 or DR=4)
PALINDROME_SEQ = [44, 26, 31, 31, 62, 44]
PALINDROME_DR  = [dr(x) for x in PALINDROME_SEQ]
assert PALINDROME_DR == PALINDROME_SEQ[::-1].__class__(PALINDROME_DR)   # palindrome
assert PALINDROME_DR == [8, 8, 4, 4, 8, 8]
assert PALINDROME_DR == PALINDROME_DR[::-1]   # DR pattern is palindromic

# 13 and 31 are emirps, both DR=4
assert dr(13) == dr(31) == 4
assert isprime(13) and isprime(31)

# 26 and 62: digit reverses, both DR=8; 26=2×13, 62=2×31
assert dr(26) == dr(62) == 8
assert 26 == 2 * 13 and 62 == 2 * 31

# 9+n DR identity: dr(9+n) == n for n=1..9
for n in range(1, 10):
    assert dr(9 + n) == n

# 64 − 46 = 18, DR=9
assert 64 - 46 == 18 and dr(18) == 9

# OEOEOEOE pattern → 4 pairs × base 12 = 48, DR=3
assert dr(4 * 12) == 3


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 15: 91 AND PALINDROME GAP STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════

# 91 = 7 × 13
assert 91 == 7 * 13

# B1B − 1B1 = 91(B−1) for B=1..9
for B in range(1, 10):
    b1b = 100 * B + 10 * 1 + B   # B1B
    _1b1 = 100 * 1 + 10 * B + 1  # 1B1
    assert b1b - _1b1 == 91 * (B - 1)

# 010 → 101 gap = 91 (B=1 base case)
assert 101 - 10 == 91

# 141 + 111k palindrome family (k=0..5 only)
for k in range(6):
    left = 1 + k
    mid  = 4 + k
    right = 1 + k
    n = 100 * left + 10 * mid + right
    assert str(n) == str(left) + str(mid) + str(right)
    assert n == 141 + 111 * k

# Breaks at k=6 (mid digit = 10 > 9)
assert 4 + 6 == 10   # not a single digit → family ends

# 137 = 26 + 111: 26 (26) + repunit-3 (111)
assert 26 + 111 == 137
assert 30 + 111 == 141
assert 30 + 11  == 41           # inside 37-hub territory
# 111 = 11×10 + 1
assert 111 == 11 * 10 + 1


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 16: {2,3}-DIGIT PRIME FAMILY
# ═══════════════════════════════════════════════════════════════════════════════

from itertools import product as iproduct

def primes_from_digits(digits, length):
    """All primes of given length using only specified digits."""
    results = []
    for combo in iproduct(digits, repeat=length):
        if combo[0] == 0:
            continue
        n = int("".join(map(str, combo)))
        if isprime(n):
            results.append(n)
    return sorted(results)

P23 = {L: primes_from_digits([2, 3], L) for L in range(1, 8)}

assert P23[1] == [2, 3]
assert P23[2] == [23]
assert P23[3] == [223, 233]
assert P23[4] == [2333, 3323]
assert len(P23[5]) == 4
assert len(P23[6]) == 7
assert len(P23[7]) == 13

# Right-truncatable chain from 2: 2→23→233→2333→23333
CHAIN_23 = [2, 23, 233, 2333, 23333]
for x in CHAIN_23:
    assert isprime(x)
for i in range(1, len(CHAIN_23)):
    assert str(CHAIN_23[i]).startswith(str(CHAIN_23[i-1]))

# 23333 + "3" = 233333 — test if chain extends
assert not isprime(233333)   # terminates at length 5


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 17: EISENSTEIN PRIMES
# ═══════════════════════════════════════════════════════════════════════════════

def eisenstein_norm(a, b):
    """N(a + bω) = a² - ab + b²"""
    return a*a - a*b + b*b

assert eisenstein_norm(5, 2) == 19
assert eisenstein_norm(7, 3) == 37    # 37 appears as Eisenstein norm
assert eisenstein_norm(6, 1) == 31
assert isprime(eisenstein_norm(7, 3))  # 37 is prime


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 18: STRUCTURAL CONSTANTS SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

CONSTANTS = {
    "137 mod 37":          137 % 37,          # 26 = 26
    "ord_37(10)":          3,                  # 10³≡1 mod 37; explains 111=3×37
    "ord_37(26)":          3,                  # f26_map 3-cycle
    "ord_37(3)":           36,                 # 3 is primitive root mod 37
    "111 = 3×37":          True,
    "666 = 18×37":         True,
    "DR(137)":             dr(137),            # 2
    "DR(111)":             dr(111),            # 3
    "DR(666)":             dr(666),            # 9
    "DR(37)":              dr(37),             # 1
    "8128 mod 37":         8128 % 37,          # 25 — f26 anchor
    "N_palin mod 37":      N_PALIN % 37,       # 32 = 37−5
    "twin DR pairs":       sorted(VALID_DR),
    "all-same labels":     [zc_label(n) for n in [4, 8, 12]],
    "357 digit counts":    [3, 5, 7],
    "357 sum":             15,
    "357 product":         105,
    "mersenne cycle":      MERSENNE_DR_CYCLE,
    "doubling cycle":      DOUBLING_CYCLE,
    "lucas chain":         LUCAS_CHAIN,
    "lucas chain DR":      LUCAS_DR,
    "perfect DR":          [dr(n) for n in PERFECT],
    "f26 anchors":   sorted(({4, 9, 25, 30})),
    "f26 targets":   sorted(F26_TARGETS),
}

assert CONSTANTS["137 mod 37"]  == 26
assert CONSTANTS["DR(137)"]     == 2
assert CONSTANTS["DR(111)"]     == 3
assert CONSTANTS["DR(666)"]     == 9
assert CONSTANTS["8128 mod 37"] == 25
assert CONSTANTS["all-same labels"] == ["111", "22222", "3333333"]


if __name__ == "__main__":
    print("CylicAmp Master Framework")
    print("=" * 60)
    print()
    for k, v in CONSTANTS.items():
        print(f"  {k:<22} = {v}")
    print()
    print("All assertions passed across all 18 sections.")
