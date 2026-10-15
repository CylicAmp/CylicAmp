# CylicAmp -- the work of Michael Warren Song, checked
#
# One file, everything in it. Copy all of it, paste it into any Python 3 (3.9 or
# newer) and press run: an online Python site on a phone or in a browser works
# (search "online python", paste, Run). Nothing to install: standard library only.
# It runs in about a second and prints every result as
#     PASS  <title>        or        FAIL  <title>: <what went wrong>
# with the lines it checks quoted above each one, then "N of M checks passed".
#
# Built 2026-10-14 from the repository github.com/CylicAmp/CylicAmp
# (branch claude/add-torus-animation-6Ey5Z).
#
# How it is laid out:
#   - Each result opens with the lines it checks, word for word. Michael Warren Song's
#     own messages are quoted with their number (#n) in owner_work/messages/; that
#     record starts 2026-10-05. Earlier work is quoted from the owner's file in the
#     repository that holds it, named above the quote. "..." marks skipped lines.
#   - Text that arrived pasted inside a message (another tool's output) is labelled
#     "pasted", never as the owner's words.
#   - The owner's names for operations are kept: drip cycle, count commas with 1 /
#     with out, +1 to begin again, cap plus new beginning, equal odds compress, ...
#   - Every check computes. Where a line of the work needs a correction, the check
#     says so in its detail; where something is open (a conjecture), it says open.

import math
import time
from collections import Counter
from decimal import Decimal, getcontext
from fractions import Fraction

# ----------------------------------------------------------------------------------
# Shared helpers (written once, used by every part)
# ----------------------------------------------------------------------------------


def dr(n):
    """Digital root, the repository convention: dr(0) = 0, otherwise 1..9."""
    n = abs(int(n))
    return 0 if n == 0 else 1 + (n - 1) % 9


def digit_sum(n):
    return sum(int(c) for c in str(abs(int(n))))


def dr_slow(n):
    """Digital root by adding digits until one digit is left (cross-check of dr)."""
    n = abs(int(n))
    while n > 9:
        n = digit_sum(n)
    return n


def is_prime(n):
    """Miller-Rabin with the first 13 prime bases: exact for every n < 3.3 * 10**24."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in small:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _rho(n):
    if n % 2 == 0:
        return 2
    c = 1
    while True:
        x = y = 2
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d
        c += 1


def factor(n):
    """Prime factorization as a dict {prime: exponent}."""
    out = Counter()
    for p in (2, 3, 5, 7, 11, 13):
        while n % p == 0:
            out[p] += 1
            n //= p
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if is_prime(m):
            out[m] += 1
            continue
        d = _rho(m)
        stack += [d, m // d]
    return dict(sorted(out.items()))


def sieve(N):
    """bytearray s with s[k] = 1 exactly when k is prime, 0 <= k <= N."""
    s = bytearray([1]) * (N + 1)
    s[0] = s[1] = 0
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(range(i * i, N + 1, i)))
    return s


def mult_order(a, m):
    k, x = 1, a % m
    while x != 1:
        x = x * a % m
        k += 1
    return k


def divisor_count(n):
    return math.prod(e + 1 for e in factor(n).values()) if n > 1 else 1


# GF(37): the 137-map f(n) = 137 n mod 37 = 26 n mod 37, and the twelve named orbits.
P = 37
MULT = 137 % P                      # = 26


def orbit(n):
    """The 137-map orbit (3-cycle) of n mod 37, as a sorted tuple."""
    r = n % P
    return tuple(sorted({r, r * MULT % P, r * MULT * MULT % P}))


ORBIT_NAMES = {
    (1, 10, 26): "IC", (3, 4, 30): "C3", (7, 33, 34): "D7", (6, 8, 23): "TESLA",
    (18, 24, 32): "SEED", (5, 13, 19): "CAS_EXT", (9, 12, 16): "SA_ST_A",
    (21, 25, 28): "SA_ST_B", (2, 15, 20): "DARK_A", (14, 29, 31): "C9",
    (11, 27, 36): "NEG_H", (17, 22, 35): "NQR17", (0,): "SEAM",
}


def orbit_name(n):
    return ORBIT_NAMES[orbit(n)]


def rotations(s):
    return [s[i:] + s[:i] for i in range(len(s))]


def owner_equations_hold(text):
    """Check every line of the owner's form 'a=b' (two-digit number = its digit sum's
    root), e.g. '12=3'. Returns the list of (line, ok)."""
    out = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        left, right = line.split("=")
        out.append((line, dr(int(left)) == int(right)))
    return out


CHECKS = []


def check(bucket, title, source, owner):
    """Register one result: bucket name, title, where the owner's lines come from,
    the owner's lines verbatim. The function returns (ok, detail)."""
    def reg(fn):
        CHECKS.append((bucket, title, source, owner, fn))
        return fn
    return reg


# ==================================================================================
# 1/137 and the 137-map in GF(37)
# ==================================================================================
B_GF37 = "1/137 and the 137-map in GF(37)"


@check(B_GF37, "The 137-map: every nonzero residue comes back in exactly 3 steps; 12 three-cycles; 246 -> 24 -> 32 -> 18",
       "the owner's file math/lemmas/heartbeat_3cycle.py",
       """The map  f(n) = (n × 137) mod 37  is equivalent to  f(n) = (26n) mod 37
since 137 mod 37 = 26.
...
Consequence: EVERY non-zero node returns to itself in exactly 3 steps.
...
The 36 non-zero residues partition into exactly 12 disjoint 3-cycles.""")
def _():
    f = lambda n: n * 137 % 37
    first_return = []
    for n in range(1, 37):
        x, k = f(n), 1
        while x != n:
            x, k = f(x), k + 1
        first_return.append(k)
    cycles = {orbit(n) for n in range(1, 37)}
    seed = [246 % 37, f(246 % 37), f(f(246 % 37)), f(f(f(246 % 37)))]
    ok = (137 % 37 == 26 and set(first_return) == {3} and len(cycles) == 12
          and all(len(c) == 3 for c in cycles) and seed == [24, 32, 18, 24])
    return ok, f"137 mod 37 = {137 % 37}; first return for n = 1..36: always {set(first_return)}; {len(cycles)} cycles; 246 -> {seed}"


@check(B_GF37, "137 and 139 are twin primes; 137 = 26 (mod 37); the cube roots of 1 mod 37 are exactly 1, 10, 26; 2^137 = 24 and 2^12 = 26 (mod 37)",
       "the owner's file math/theorems/theorem_109_137_twin_prime_gf37.py",
       """The prime 137 has residue 26 mod 37, which is exactly the multiplier used to
define the 137-map: f(n) = 137·n (mod 37) = 26·n (mod 37).
...
IC = {1, 10, 26} is the complete set of cube roots of unity in GF(37).
...
The primitive root 2 raised to the power 137 gives the seed residue:
2^137 ≡ 24 (mod 37).""")
def _():
    roots = [x for x in range(1, 37) if pow(x, 3, 37) == 1]
    ok = (is_prime(137) and is_prime(139) and roots == [1, 10, 26]
          and pow(2, 137, 37) == 24 == 246 % 37 and pow(2, 12, 37) == 26)
    return ok, f"137, 139 prime: {is_prime(137)}, {is_prime(139)}; x^3 = 1: {roots}; 2^137 = {pow(2, 137, 37)}; 2^12 = {pow(2, 12, 37)} (mod 37)"


@check(B_GF37, "Each 3-cycle adds up to 37 or 74 -- six of each -- and the twelve sums total 666",
       "the owner's file math/theorems/basin_sum_wraparound_gf37.py (2026-07-31)",
       """S(a) ∈ [3, 108]. The only multiples of 37 in this range are
{37, 74} — because 3 × 37 = 111 > 108. Therefore S(a) ∈ {37, 74},
...
Exactly 6 of the 12 basins satisfy S(a) = 1 × 37 (single period):""")
def _():
    sums = [sum(c) for c in {orbit(n) for n in range(1, 37)}]
    wrap_ok = all(a + 10 * a % 37 + 26 * a % 37 == 37 * (a - 10 * a // 37 - 26 * a // 37) for a in range(1, 37))
    ok = sorted(Counter(sums).items()) == [(37, 6), (74, 6)] and sum(sums) == 666 == sum(range(1, 37)) and wrap_ok
    return ok, f"cycle sums: {dict(Counter(sums))}; total {sum(sums)}; S(a) = 37(a - k1 - k2) for every a: {wrap_ok}"


@check(B_GF37, "The 12 cycles are the cosets of {1, 10, 26}; the discrete log base 2, mod 12, labels each cycle",
       "the owner's file math/theorems/theorem_118_coset_structure_gf37.py (2026-08-03)",
       """The 12 left cosets of H_3 are exactly the 12 orbits of the 137-map.""")
def _():
    dlog = {pow(2, k, 37): k for k in range(36)}
    cosets = {tuple(sorted(a * h % 37 for h in (1, 10, 26))) for a in range(1, 37)}
    cycles = {orbit(n) for n in range(1, 37)}
    labels = {c: {dlog[x] % 12 for x in c} for c in cycles}
    ok = cosets == cycles and all(len(v) == 1 for v in labels.values()) and len({min(v) for v in labels.values()}) == 12
    return ok, f"cosets == cycles: {cosets == cycles}; dlog mod 12 constant on each cycle and different across the 12: {ok}"


@check(B_GF37, "ABCABC = 2 x ABC (mod 37) for every 3-digit block; 2 has order 36 mod 37 (a primitive root); 2^-1 = 19",
       "the owner's file math/lemmas/abcabc_mod37_orbit.py",
       """ABCABC = ABC × 1001,  and  1001 ≡ 2 (mod 37)
→ ABCABC ≡ 2 · ABC (mod 37)
...
- ord_37(2) = 36  (2 is a primitive root mod 37)
...
- 2^{-1} ≡ 19 (mod 37)  (since 2·19 = 38 ≡ 1)""")
def _():
    bad = [a for a in range(1000) if int(f"{a:03d}" * 2) % 37 != 2 * a % 37]
    prim = [g for g in range(1, 37) if mult_order(g, 37) == 36]
    ok = not bad and 1001 % 37 == 2 and mult_order(2, 37) == 36 and 2 * 19 % 37 == 1
    ok = ok and prim == [2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35]
    return ok, f"blocks 000-999 failing: {len(bad)}; order of 2 = {mult_order(2, 37)}; all primitive roots: {prim}"


@check(B_GF37, "The 137-map keeps squares with squares (26 = 10^2); anchors and targets are all squares; 5 is not, so x^2 - x - 1 has no root mod 37",
       "the owner's file math/theorems/sovereign_qr_closure.py",
       """The 137/37 multiplier 26 = 137 mod 37 is itself QR (10² ≡ 26 mod 37).
Therefore the map f(n) = 26n mod 37 preserves QR membership:
...
PIVOT (residue 5): Legendre(5|37) = -1  — non-residue, no sqrt mod 37""")
def _():
    qr = {n * n % 37 for n in range(1, 37)}
    keeps = all((26 * n % 37 in qr) == (n in qr) for n in range(1, 37))
    golden = [x for x in range(37) if (x * x - x - 1) % 37 == 0]
    ok = (10 * 10 % 37 == 26 and keeps and {4, 9, 25, 30} <= qr and {3, 12, 21, 30} <= qr
          and 5 not in qr and pow(5, 18, 37) == 36 and golden == [])
    return ok, f"squares mod 37: {len(qr)}; map keeps them: {keeps}; 5^18 = {pow(5, 18, 37)} (= -1); roots of x^2-x-1: {golden}"


@check(B_GF37, "The 3x+1 map mod 37: one fixed point (18) and two 18-cycles; 3 has order 18. (The Collatz conjecture itself is open; below, a measurement only)",
       "the owner's line in the Egor screenshot attached to #276 (as recorded in math/theorems/langton_ant_highway_2026_10_14.py), and the owner's file math/theorems/theorem_346_collatz_137_proper_subgroup_gf37.py",
       """I know no more of my Langdon ants or my collaze conjectures 3+1 proves no even mentions
...
C(x)     = 3x+1     1 fixed point + TWO 18-cycles""")
def _():
    C = lambda x: (3 * x + 1) % 37
    seen, cyc = set(), []
    for s in range(37):
        if s in seen:
            continue
        x, path = s, []
        while x not in seen:
            seen.add(x)
            path.append(x)
            x = C(x)
        cyc.append(len(path))
    fixed = [x for x in range(37) if C(x) == x]
    # measurement: every start up to 100,000 reaches 1 under n -> n/2, 3n+1
    reach = {1: True}

    def reaches(n):
        path = []
        while n not in reach:
            if len(path) > 5000:          # give up: report it instead of looping for ever
                return False
            path.append(n)
            n = n // 2 if n % 2 == 0 else 3 * n + 1
        for m in path:
            reach[m] = True
        return True
    all_reach = all(reaches(n) for n in range(1, 100001))
    ok = sorted(cyc) == [1, 18, 18] and fixed == [18] and mult_order(3, 37) == 18 and all_reach
    return ok, (f"cycle lengths {sorted(cyc)}, fixed point {fixed}, order of 3 = {mult_order(3, 37)}; "
                f"every n <= 100,000 reaches 1: {all_reach} (typo: 'Langdon ants' for Langton's ant, 'collaze' for Collatz)")


# ==================================================================================
# Twin primes
# ==================================================================================
B_TWIN = "Twin primes"
TWIN_LIMIT = 10 ** 6
_SIEVE = None


def primes_flags():
    global _SIEVE
    if _SIEVE is None:
        _SIEVE = sieve(TWIN_LIMIT + 2)
    return _SIEVE


@check(B_TWIN, "Every twin pair above (3, 5) is (6m-1, 6m+1), and its digital roots are (2,3,4), (5,6,7) or (8,9,1) -- below 10^6: 2651, 2788, 2729 (whether they even out is open)",
       "#189, 2026-10-06; then the owner's file twin_ramified_axis.py",
       """So you're telling me that my twin prime work, I did not advance that fucking field at all. To where there's new ways to look at it.
...
and mod 9 the pair has exactly one of three types:
(2,3,4), (5,6,7), (8,9,1)  — midpoint DR always in {3,6,9}.""")
def _():
    s = primes_flags()
    types, not_6m, total = Counter(), 0, 0
    for p in range(5, TWIN_LIMIT - 1):
        if s[p] and s[p + 2]:
            total += 1
            if (p + 1) % 6:
                not_6m += 1
            types[(dr(p), dr(p + 1), dr(p + 2))] += 1
    want = {(2, 3, 4): 2651, (5, 6, 7): 2788, (8, 9, 1): 2729}
    ok = dict(types) == want and not_6m == 0
    return ok, f"{total} twin pairs with 5 <= p < 10^6; not of the form 6m+-1: {not_6m}; types {dict(types)}"


@check(B_TWIN, "A twin midpoint is never 1 or 36 mod 37 (either would put a twin on a multiple of 37); a midpoint of 0 mod 37 is allowed and occurs",
       "the owner's file math/theorems/theorem_345_twin_midpoint_forbidden_gf37.py",
       """6n == 1  (mod 37)  =>  6n-1 == 0  =>  lower twin divisible by 37
6n == 36 (mod 37)  =>  6n+1 == 0  =>  upper twin divisible by 37""")
def _():
    s = primes_flags()
    mids = Counter((p + 1) % 37 for p in range(3, TWIN_LIMIT - 1) if s[p] and s[p + 2])
    ok = mids[1] == 0 and mids[36] == 0 and mids[0] > 0 and len(mids) == 35
    return ok, f"below 10^6: midpoints on 1: {mids[1]}, on 36: {mids[36]}, on 0: {mids[0]}; residues used: {len(mids)} of 37"


# ==================================================================================
# Seed 246, the pair 0.007 / 0.008, and the drip cycle on 246
# ==================================================================================
B_SEED = "Seed 246, 0.007 / 0.008, and the drip cycle on 246"


@check(B_SEED, "0.007 and 0.008: DR(7+8) + (8-7) = 6 + 1 = 7 closes back on 7, and (-3) mod 9 = 6 = DR(7+8)",
       "the owner's files math/theorems/theorem_120_digit_algebra_007_008.py and theorem_121_scientific_notation_007_008.py",
       """Synthesis:  6 + 1 = 7   ← closes back to A
This closure is specific to the pair (7, 8): DR(A+B) + (B-A) = A
...
(-s) mod 9 = 6 = DR(m1 + m2)   [exponent residue equals DR of mantissa sum]""")
def _():
    closes = [(a, b) for a in range(1, 10) for b in range(a + 1, 10) if dr(a + b) + (b - a) == a]
    neighbours = [(a, b) for a, b in closes if b == a + 1]
    ok = dr(7 + 8) + (8 - 7) == 7 and (-3) % 9 == 6 == dr(7 + 8) and neighbours == [(7, 8)]
    return ok, (f"6 + 1 = {dr(15) + 1}; (-3) mod 9 = {(-3) % 9}. Pairs A < B that close: {closes} -- "
                f"(7, 8) is the only neighbouring pair; (5, 7) closes too (DR(12) + 2 = 5), so 'specific to (7, 8)' holds for neighbours")


@check(B_SEED, "The reference check passes for exactly the seeds 246 mod 333 (333 = 9 x 37): 246, 579, 912, ...",
       "the owner's file math/theorems/theorem_316_t120_seed_class_mod_333_gf37.py",
       """The three are 246, 579, 912 -- an arithmetic progression of common
difference 333 = 9 x 37 = lcm(9, 37).""")
def _():
    hits = [s for s in range(1, 4000) if dr(s) == 3 and s % 37 == 24]
    ok = hits == list(range(246, 4000, 333)) and 333 == 9 * 37 and math.lcm(9, 37) == 333
    return ok, f"seeds below 4000 with root 3 and = 24 (mod 37): {hits}"


@check(B_SEED, "Drip cycle on 246: its rotations 246, 462, 624 stay in one 137-map cycle (SEED), the mirror's rotations 642, 426, 264 in the opposite one (CAS_EXT); 264 is on the mirror's rotation",
       "#228, 2026-10-12 (the drip cycle example); #252 and #262, 2026-10-13; the owner's rotations of 2026-10-04 in math/lemmas/rotation_grids_x.py",
       """1
12

1
21

2
12

2
21
That right there is just a fucking small example. That is not all of them. Find all of them.
...
run my full drip cycle on 246
...
264 is on the 246 rotation
...
426 -> 642 -> 264 -> 426   (=1, =2, =3: back on the third turn)
246 -> 624 -> 462 -> 246""")
def _():
    rot, mir = rotations("246"), rotations("642")
    every = all(int(r) % 37 == 10 * int(s) % 37
                for a in range(1000) for s in [f"{a:03d}"] for r in [s[1:] + s[0]])
    names = ({orbit_name(int(x)) for x in rot}, {orbit_name(int(x)) for x in mir})
    ok = (names == ({"SEED"}, {"CAS_EXT"}) and every and "264" in mir and "264" not in rot
          and 246 + 642 == 888 == 24 * 37 and sorted(rot + mir) == sorted({"246", "264", "426", "462", "624", "642"}))
    return ok, (f"246's rotations {rot} -> {names[0]}; the mirror's {mir} -> {names[1]}; "
                f"a rotation multiplies by 10 (mod 37) for all 1000 three-digit blocks (999 = 27 x 37): {every}; "
                f"246 + 642 = 888 = 24 x 37. 264 is in the mirror cycle, as the owner wrote it 2026-10-04 (426 -> 642 -> 264), not in 246 -> 462 -> 624")


# ==================================================================================
# Phi_3 / Phi_12 at 137 and the tape 113115117167 (the owner's handoff, #241)
# ==================================================================================
B_PHI = "Phi_3 / Phi_12 at 137 and the tape 113115117167 (#241)"
SRC_241 = "#241, 2026-10-13: the owner's handoff (\"Author of the work: Michael Warren Song\"), compiled 2026-09-12"
TAPE = 113115117167
P3 = 137 ** 2 + 137 + 1
P12 = 137 ** 4 - 137 ** 2 + 1


@check(B_PHI, "Phi_3(137) = 18907 = 7 x 37 x 73 and Phi_12(137) = 352256593 = 13 x 2473 x 10957; each of 13, 2473, 10957 is prime, = 1 mod 12, and 137 has order 12 modulo it",
       SRC_241,
       """Φ₃(137) = 137² + 137 + 1 = 18907 = 7 · 37 · 73
...
Φ₁₂(137) = 137⁴ − 137² + 1 = 352256593 = 13 · 2473 · 10957""")
def _():
    f3, f12 = factor(P3), factor(P12)
    each = [(p, is_prime(p), mult_order(137, p), p % 12) for p in (13, 2473, 10957)]
    ok = (P3 == 18907 and f3 == {7: 1, 37: 1, 73: 1} and P12 == 352256593
          and f12 == {13: 1, 2473: 1, 10957: 1} and all(e[1:] == (True, 12, 1) for e in each))
    return ok, f"Phi_3(137) = {P3} = {f3}; Phi_12(137) = {P12} = {f12}; (p, prime, order of 137, p mod 12): {each}"


@check(B_PHI, "The tape S = 113115117167 = 13 x 8701162859 (prime); gcd(S, Phi_3) = 1 and gcd(S, Phi_12) = 13",
       SRC_241,
       """S = 113115117167 = 13 · 8701162859     (8701162859 is prime)
gcd(S, Φ₃(137))  = 1
gcd(S, Φ₁₂(137)) = 13""")
def _():
    fs = factor(TAPE)
    ok = fs == {13: 1, 8701162859: 1} and math.gcd(TAPE, P3) == 1 and math.gcd(TAPE, P12) == 13
    return ok, f"S = {fs}; gcd with Phi_3: {math.gcd(TAPE, P3)}; with Phi_12: {math.gcd(TAPE, P12)}"


@check(B_PHI, "1/137 repeats every 8 digits: 0.(00729927); 10^4 = -1 (mod 137)",
       SRC_241,
       """Correct value: **the period is 8.** ord₁₀(137) = 8, since 10⁴ ≡ −1 (mod 137).""")
def _():
    digits, r = [], 1
    for _ in range(24):
        r *= 10
        digits.append(r // 137)
        r %= 137
    d = "".join(map(str, digits))
    ok = mult_order(10, 137) == 8 and pow(10, 4, 137) == 136 and d == "00729927" * 3
    return ok, f"1/137 = 0.{d}...; order of 10 mod 137 = {mult_order(10, 137)}; 10^4 mod 137 = {pow(10, 4, 137)}"


@check(B_PHI, "New from the framework run: the tape's prime 8701162859 is a twin prime (8701162861 prime) and a Sophie Germain prime (17402325719 prime); the chain stops there; it is not a safe prime",
       SRC_241,
       """S = 113115117167 = 13 · 8701162859     (8701162859 is prime)""")
def _():
    q = 8701162859
    ok = (is_prime(q) and is_prime(q + 2) and not is_prime(q - 2) and is_prime(2 * q + 1)
          and not is_prime(2 * (2 * q + 1) + 1) and not is_prime((q - 1) // 2))
    return ok, (f"q+2 prime: {is_prime(q + 2)}; 2q+1 = {2 * q + 1} prime: {is_prime(2 * q + 1)}; "
                f"2(2q+1)+1 prime: {is_prime(4 * q + 3)}; (q-1)/2 prime: {is_prime((q - 1) // 2)}")


@check(B_PHI, "Correction to section 4: the residual 0.035999... is about 1.7 million times the CODATA uncertainty -- six orders of magnitude, not ten",
       SRC_241,
       """- Constraint on any future connection: the residual is 0.035999, roughly 2.6 × 10⁻⁴
relative — about ten orders of magnitude larger than the CODATA uncertainty on α⁻¹.""")
def _():
    out = []
    for name, v in (("CODATA 2018 137.035999084(21)", 137035999084), ("CODATA 2022 137.035999177(21)", 137035999177)):
        resid = v - 137 * 10 ** 9            # in units of 10^-9
        ratio = resid / 21                   # uncertainty 0.000000021
        out.append((name, round(ratio), round(math.log10(ratio), 2), resid / v))
    ok = all(1.6e6 < o[1] < 1.8e6 and 2.62e-4 < o[3] < 2.63e-4 for o in out)
    return ok, "; ".join(f"{n}: residual / uncertainty = {r:,} (10^{e}), relative residual {rel:.4g}" for n, r, e, rel in out)


# ==================================================================================
# Langton's ant (the owner's results, computed in the owner's Egor project)
# ==================================================================================
B_ANT = "Langton's ant (the owner's Egor results, #276)"
SRC_ANT = ("the owner's Egor results (egor_v18_project, igor_langton_mask_v18.py), in the screenshot attached "
           "to #276, 2026-10-14; transcribed in math/theorems/langton_ant_highway_2026_10_14.py")
ANT_TABLE = """Highway onset                  Step 9,976
Highway movement period        104 steps
Displacement per period        (-2, +2)
Odd-flip mask                  34 cells
Black-cell growth              +12 per completed cycle
Simulation horizon             5,000,000 steps
Black cells at 5,000,000       576,486"""
ONSET, PERIOD = 9976, 104
RUN_FULL_LANGTON = False      # set to True to also run all 5,000,000 moves (slower on a phone)
_ANT = {}


def ant(n_steps, y_down=False):
    """Langton's ant on an all-white grid: on white turn right, on black turn left; flip; step.
    Starts at (0,0) heading north. Returns xs, ys (position after t moves), B (black cells
    after t moves), col (colour read before move t+1, 1 = black)."""
    key = (n_steps, y_down)
    if key in _ANT:
        return _ANT[key]
    black = set()
    x = y = 0
    dx, dy = (0, -1) if y_down else (0, 1)
    xs, ys, B, col = [0] * (n_steps + 1), [0] * (n_steps + 1), [0] * (n_steps + 1), [0] * n_steps
    nb = 0
    for t in range(n_steps):
        k = (x, y)
        if k in black:
            col[t] = 1
            dx, dy = (dy, -dx) if y_down else (-dy, dx)
            black.discard(k)
            nb -= 1
        else:
            dx, dy = (-dy, dx) if y_down else (dy, -dx)
            black.add(k)
            nb += 1
        x += dx
        y += dy
        xs[t + 1], ys[t + 1], B[t + 1] = x, y, nb
    _ANT[key] = (xs, ys, B, col)
    return _ANT[key]


ANT_N = ONSET + PERIOD * 60


def onset_and_shift(xs, ys, q):
    N = len(xs) - 1
    sx, sy = xs[N] - xs[N - q], ys[N] - ys[N - q]
    t = N - q
    while t >= 0 and xs[t + q] - xs[t] == sx and ys[t + q] - ys[t] == sy:
        t -= 1
    return t + 1, (sx, sy)


@check(B_ANT, "Highway from step 9,976 with least period 104; +12 black cells per cycle; B(9976 + 104n) = 714 + 12n holds from n = 1 (so 'n >= 2' is not sharp); 5,000,000 = 9,976 + 104 x 47,981 gives 576,486",
       SRC_ANT, ANT_TABLE + """
"The conditional formula for completed highway cycles is
B(n) = 714 + 12n,   n >= 2.\"""")
def _():
    xs, ys, B, col = ant(ANT_N)
    t0, shift = onset_and_shift(xs, ys, PERIOD)
    least = all(onset_and_shift(xs, ys, q)[0] > ANT_N - 3 * PERIOD for q in range(1, PERIOD) if PERIOD % q == 0)
    t = ANT_N - PERIOD
    while t >= 0 and B[t + PERIOD] - B[t] == 12:
        t -= 1
    plus12_from = t + 1
    nmax = (ANT_N - ONSET) // PERIOD
    formula = all(B[ONSET + PERIOD * n] == 714 + 12 * n for n in range(1, nmax + 1))
    n5 = (5_000_000 - ONSET) // PERIOD
    xd, yd, _, _ = ant(ANT_N, y_down=True)
    shift_screen = onset_and_shift(xd, yd, PERIOD)[1]
    ok = (t0 == ONSET and least and plus12_from == 9977 and formula and B[ONSET] == 716
          and (5_000_000 - ONSET) % PERIOD == 0 and n5 == 47981 and 714 + 12 * n5 == 576486
          and shift == (-2, -2) and shift_screen == (-2, 2))
    detail = (f"periodic from step {t0}; 104 is the least period: {least}; +12 every cycle from t = {plus12_from}; "
              f"B = 714 + 12n for n = 1..{nmax}: {formula}; at n = 0, B(9976) = {B[ONSET]}; "
              f"n = {n5} -> {714 + 12 * n5}; shift {shift} heading north with y up, {shift_screen} with y down "
              f"(screen rows) -- the (-2, +2) of the table")
    if RUN_FULL_LANGTON:
        black, x, y, dx, dy = set(), 0, 0, 0, 1
        for _ in range(5_000_000):
            k = (x, y)
            if k in black:
                dx, dy = -dy, dx
                black.discard(k)
            else:
                dx, dy = dy, -dx
                black.add(k)
            x += dx
            y += dy
        ok = ok and len(black) == 576486
        detail += f"; direct run of 5,000,000 moves: {len(black)} black cells"
    return ok, detail


def flip_window(xs, ys, col, start):
    p = (xs[start], ys[start])
    c, first = Counter(), {}
    for t in range(start, start + PERIOD):
        o = (xs[t] - p[0], ys[t] - p[1])
        c[o] += 1
        first.setdefault(o, col[t])
    odd = {o for o, m in c.items() if m % 2}
    return c, odd, sum(1 for o in odd if first[o] == 0)


@check(B_ANT, "Odd-flip mask: in each 104-move window from the onset, 34 of the 41 cells visited flip an odd number of times; 22 white-to-black / 12 back in the first window, 23 / 11 in every later one (23 - 11 = 12)",
       SRC_ANT, "Odd-flip mask                  34 cells\nBlack-cell growth              +12 per completed cycle")
def _():
    xs, ys, B, col = ant(ANT_N)
    c0, m0, w0 = flip_window(xs, ys, col, ONSET)
    later = [flip_window(xs, ys, col, ONSET + PERIOD * k) for k in range(1, 50)]
    ok = (len(c0) == 41 and len(m0) == 34 and w0 == 22
          and all(c == c0 and m == m0 and w == 23 for c, m, w in later))
    return ok, f"cells visited {len(c0)}, odd-flip {len(m0)}, first window {w0}/{34 - w0}, later windows {later[0][2]}/{34 - later[0][2]} (same 34 offsets each time)"


@check(B_ANT, "For this start (the all-white grid) the highway never ends: once the window has moved past every cell the early walk touched, each period repeats the one before -- shown by induction from periods 0..5. (That EVERY start builds a highway is open.)",
       SRC_ANT, "\"Infinite continuation remains unproved.\"")
def _():
    xs, ys, B, col = ant(ANT_N)
    s = (-2, -2)
    dot = lambda a, b: a[0] * b[0] + a[1] * b[1]
    p0 = (xs[ONSET], ys[ONSET])
    C = {(xs[t], ys[t]) for t in range(ONSET)}
    U = [(xs[ONSET + j] - p0[0], ys[ONSET + j] - p0[1]) for j in range(PERIOD)]
    Us, s2 = set(U), dot(s, s)
    maxC = max(dot(c, s) for c in C)
    minW = min(dot((p0[0] + u[0], p0[1] + u[1]), s) for u in Us)
    Kd = 0
    while minW + Kd * s2 <= maxC:        # from period Kd on, the window projects past all of C
        Kd += 1
    D = 0
    for u in Us:
        for v in Us:
            d = (u[0] - v[0], u[1] - v[1])
            if d[0] * s[1] == d[1] * s[0] and dot(d, s) > 0 and dot(d, s) % s2 == 0:
                D = max(D, dot(d, s) // s2)
    K = max(1, Kd, D)
    flips = Counter(U)
    f = {v: sum(flips[(v[0] + i * s[0], v[1] + i * s[1])] for i in range(1, D + 1)) % 2 for v in Us}
    # the predicted colours must match the simulated ones for 41 periods from K on
    control = all(col[ONSET + PERIOD * k + j] == f[U[j]]
                  for k in range(K, K + 41) for j in range(PERIOD) if U.index(U[j]) == j)
    base = all(xs[ONSET + PERIOD * k + j] - xs[ONSET + PERIOD * k] == U[j][0]
               and ys[ONSET + PERIOD * k + j] - ys[ONSET + PERIOD * k] == U[j][1]
               for k in range(K + 1) for j in range(PERIOD))
    ok = (Kd, D, K) == (5, 2, 5) and len(C) == 1376 and control and base
    return ok, (f"cells touched before the onset: {len(C)}; the window clears them from period {Kd}; "
                f"a cell is re-read at most {D} periods later; base periods 0..{K} match: {base}; "
                f"predicted colours match the run for periods {K}..{K + 40}: {control}. "
                f"So for this start the 'unproved' line can be closed; for other starts the highway question stays open")


# ==================================================================================
# 0.25: the drip cycle on 0.25, x^(x^x), and the 1/4 power tower
# ==================================================================================
B_QUARTER = "0.25: the drip cycle on 0.25, x^(x^x) = (1/2)^sqrt2, the 1/4 power tower"
OWNER_255 = """run my full drip cycle on 0.25


01
00=23/6
0=+1
00=23/6
0=+1
00=23/6
0=+1
00=23/6



0
00=36
0+1
00=66
0+1
00=99
0+1=
12


6+1=7
6+1=7
6+1=7
9+3=12+21=(3+4=7)

36+66=102
9+12=21"""


@check(B_QUARTER, "Drip cycle on 0.25: every ordering of 0, 2, 5 has root 7; the owner's lines 6+1=7, 9+3=12, (3+4=7), 36+66=102, 9+12=21 hold; 36+66 = 102 is 1/4 mod 37 (102 x 4 = 408 = 11 x 37 + 1); 23 and 6 are one 137-map cycle {6, 8, 23}",
       "#255, 2026-10-13", OWNER_255)
def _():
    orders = sorted({a + b + c for a in "025" for b in "025" for c in "025" if sorted(a + b + c) == ["0", "2", "5"]})
    roots = {dr(int(o)) for o in orders}
    lines = (6 + 1 == 7 and 9 + 3 == 12 and 3 + 4 == 7 and 36 + 66 == 102 and 9 + 12 == 21
             and digit_sum(36) == 9 and digit_sum(66) == 12 and digit_sum(102) == 3)
    quarter = Fraction(1, 4)
    inv4 = pow(4, -1, 37)
    ok = (roots == {7} and lines and 102 % 37 == inv4 == 28 and 408 == 11 * 37 + 1
          and orbit(23) == orbit(6) == (6, 8, 23) and quarter == Fraction(25, 100) and digit_sum(25) == 7)
    return ok, (f"orderings {orders} all root {roots}; 9 and 12 are the digit sums of 36 and 66; 12+21 = {12 + 21}; "
                f"1/4 mod 37 = {inv4} = 102 mod 37 = {102 % 37}; orbit of 23 = orbit of 6 = {orbit(6)}")


@check(B_QUARTER, "x = 1/4 solves x^(x^x) = (1/2)^sqrt2 -- the only positive solution -- and 0.25 -> 2 + 5 = 7",
       "#255, 2026-10-13 (the owner's 0.25); Cliff Pickover's equation, sent by the owner 2026-10-13 with \"=7\" (math/theorems/pickover_tetration_x_quarter_2026_10_13.py)",
       "run my full drip cycle on 0.25")
def _():
    x = 0.25
    lhs, rhs = x ** (x ** x), 0.5 ** math.sqrt(2)
    getcontext().prec = 50
    q = Decimal(1) / 4
    exact = abs(q ** (q ** q) - (Decimal(1) / 2) ** Decimal(2).sqrt()) < Decimal(10) ** -45
    g = [k / 10000 for k in range(1, 10000)]
    vals = [t ** (t ** t) for t in g]
    rising = all(a < b for a, b in zip(vals, vals[1:]))       # f increases on (0, 1) ...
    above = all(t ** (t ** t) >= 1 for t in (1 + k / 100 for k in range(300)))   # ... and f >= 1 for x >= 1
    ok = abs(lhs - rhs) < 1e-15 and exact and rising and above and rhs < 1 and digit_sum(25) == 7
    return ok, (f"(1/4)^((1/4)^(1/4)) = {lhs!r}, (1/2)^sqrt2 = {rhs!r} (equal to 45 places); "
                f"x^(x^x) rises on (0,1) (checked at 9,999 points; the owner's file has the derivative proof) and is >= 1 for x >= 1; 2 + 5 = 7")


@check(B_QUARTER, "The 1/4 power tower: heights swing below and above 1/2 and close in on 1/2, each gap shrinking by ln(1/2) = -0.6931...; height 2 = 1/sqrt2, height 3 = 2^-sqrt2; at a 15-digit cut the roots end up 5, 4, 5, 4, ... for ever (they never settle on one)",
       "#257, 2026-10-13",
       "Do all that this algorithm can do in every direction allowed to go by numbers")
def _():
    getcontext().prec = 60
    x = Decimal(1) / 4
    half = Decimal(1) / 2
    t = [None, x]
    for _ in range(130):
        t.append(x ** t[-1])
    swing = all((t[k] < half) == (k % 2 == 1) for k in range(1, 131))
    ln_half = -math.log(2)
    ratios = [float((t[k + 1] - half) / (t[k] - half)) for k in range(30, 35)]
    contract = all(abs(r - ln_half) < 1e-5 for r in ratios)
    h23 = (abs(t[2] - 1 / Decimal(2).sqrt()) < Decimal(10) ** -50
           and abs(t[3] - Decimal(2) ** -Decimal(2).sqrt()) < Decimal(10) ** -50)
    first = next(k for k in range(1, 131) if abs(t[k] - half) < Decimal(10) ** -15)

    def cut_root(v):
        s = format(v, "f").split(".")[1][:15]
        return dr(digit_sum(int(s)))
    tail = [cut_root(t[k]) for k in range(first, 131)]
    alternate = all(r == (5 if k % 2 == 0 else 4) for r, k in zip(tail, range(first, 131)))
    ok = swing and contract and h23 and first == 92 and alternate
    return ok, (f"odd heights below 1/2, even above: {swing}; gap ratios at heights 30-34: {[round(r, 6) for r in ratios]} "
                f"vs ln(1/2) = {ln_half:.6f}; first height within 10^-15 of 1/2: {first}; roots from there: {tail[:8]}... "
                f"(t -> (1/4)^t is decreasing, so every height lands on the other side of 1/2 from the one before: the 5, 4 swing never stops)")


@check(B_QUARTER, "Pasted summary checked: 1/sqrt2 -> 6 and 2^-sqrt2 -> 8 hold only when the digits are cut at 4 places (the digits never end); 171 = 9 x 19 splits to 9 both ways; 23/6 = 3.8333... has roots cycling 2, 5, 8 and +1 sends them to 3, 6, 9",
       "#256, 2026-10-13 -- the owner's words; the summary between them was pasted (another tool's output) and is what is checked",
       """check
...
What do you see in my git hub that this needs""")
def _():
    getcontext().prec = 60

    def roots(v, k):
        s = format(v, "f").split(".")[1]
        return [dr(digit_sum(int(s[:j]))) for j in range(1, k + 1)]
    r2 = roots(1 / Decimal(2).sqrt(), 8)
    t3 = roots(Decimal(2) ** -Decimal(2).sqrt(), 8)
    q = format(Decimal(23) / 6, "f").replace(".", "")
    lad = [dr(digit_sum(int(q[:j]))) for j in range(1, 12)]
    ok = (r2[3] == 6 and t3[3] == 8 and len(set(r2)) > 1 and len(set(t3)) > 1
          and 171 == 9 * 19 and dr(1 + 71) == 9 == dr(17 + 1)
          and lad[2:] == [5, 8, 2] * 3 and {dr(v + 1) for v in (2, 5, 8)} == {3, 6, 9})
    return ok, f"1/sqrt2 roots at 1..8 places: {r2}; 2^-sqrt2: {t3}; 23/6 roots: {lad}"


# ==================================================================================
# The owner's lines of 2026-10-13, #258-#264
# ==================================================================================
B_1013 = "The owner's lines of 2026-10-13 (#258-#264)"


@check(B_1013, "76637196617697: the lines 7+6=1+3=4, 4+6=1+0=1, 1+3=4 are its running digital root (7, 4, 1, 4, ...), which ends on 9 because the digits add to 81; 7663 = 79 x 97, a prime and its reversal. The pasted '74 engine': all ten products right, but iterations 5 and 6 have their digit sums swapped, iteration 10 sums to 117 (not 126), and V mod 7 is 2 (not 1)",
       "#258, 2026-10-13 (the owner's lines; the '74 engine' block after them was pasted)",
       """7663,7196,6176,(97)
76,637,196,617,697




7+6=1+3=4
4+6=1+0=1
1+3=4""")
def _():
    V = 76637196617697
    same = "7663719661769" + "7" == str(V) == "76637196617697"
    walk, r = [], 0
    for c in str(V):
        r = dr(r + int(c))
        walk.append(r)
    sums, p = [], V
    for _ in range(10):
        p *= 74
        sums.append(digit_sum(p))
    pasted = [81, 99, 72, 81, 99, 108, 90, 144, 162, 126]
    wrong = [i + 1 for i in range(10) if sums[i] != pasted[i]]
    ok = (same and walk[:4] == [7, 4, 1, 4] and walk[-1] == 9 and digit_sum(V) == 81
          and 7663 == 79 * 97 and is_prime(79) and is_prime(97)
          and p == 377360820225814352692011083523072 and wrong == [5, 6, 10] and sums[9] == 117 and V % 7 == 2
          and 1 + 44 + 14 + 11 + 4 == 74 == 2 * 37)
    return ok, f"walk {walk}; digit sums of V x 74^k: {sums} (pasted differs at iterations {wrong}); V mod 7 = {V % 7}; V = {factor(V)}"


@check(B_1013, "The 1-9 grid split: every equation holds; (1)2(3)2(1) = 12321 = 111^2 = 3^2 x 37^2; 12121 and 22222 are both 22 mod 37 (they differ by 10101 = 3 x 7 x 13 x 37); 23 over 6 with 6+2 = 8 is one 137-map cycle {6, 8, 23}; rows 123, 456, 789 are all 12 mod 37 (steps of 333 = 9 x 37)",
       "#259, 2026-10-13",
       """(3x7=12 and 21)
(1)2(3)2(1)
(1)2(1)2(1)
(2)2(2)2(2)=3 twos or 2 thress

1-23
456
789
34
2+6=8+9=(1+7=8)""" + "\n...\n" + """1---|23
45--|6×2=1+2=(3+8=11)+45=5+6=11
789
346""")
def _():
    eqs = (3 * 7 == 21 and str(21)[::-1] == "12" and 2 + 6 == 8 and 8 + 9 == 17 and dr(17) == 8
           and 6 * 2 == 12 and dr(12) == 3 and 3 + 8 == 11 and 11 + 45 == 56 and 5 + 6 == 11 and 3 * 2 == 2 * 3)
    ok = (eqs and 12321 == 111 ** 2 == 3 ** 2 * 37 ** 2 and factor(12121) == {17: 1, 23: 1, 31: 1}
          and factor(22222) == {2: 1, 41: 1, 271: 1} and 12121 % 37 == 22222 % 37 == 22
          and 22222 - 12121 == 10101 == 3 * 7 * 13 * 37 and orbit(6) == orbit(8) == orbit(23)
          and [n % 37 for n in (123, 456, 789)] == [12, 12, 12] and 456 - 123 == 789 - 456 == 333 == 9 * 37)
    return ok, (f"12321 = {factor(12321)}; 12121 = {factor(12121)}, 22222 = {factor(22222)}, both 22 mod 37; "
                f"orbit of 6 = {orbit(6)}; 123, 456, 789 mod 37 = 12, 12, 12. typo: 'thress' for threes")


@check(B_1013, "3+4=7+9=7+2=9+3=1+2=3 is a running digital root (adding 9 never changes it); the block 159-7 / 48-84 / 7-951 reads the same backwards and uses six digits twice each (6 x 2 = 12 -> 3); 159 + 951 = 1110 = 30 x 37 and 159 - 48 = 111 = 3 x 37",
       "#260 and #261, 2026-10-13",
       """1---------------2-----3
4|5
7|8|9
3+4=7+9=7+2=9+3=1+2=3

...
159-7
48-84
7-951


block of 6×2=1+2=3""")
def _():
    walk, r = [], 0
    for a in (3, 4, 9, 2, 3):
        r = dr(r + a)
        walk.append(r)
    nine = all(dr(n + 9) == dr(n) for n in range(1, 10000))
    blk = ["159-7", "48-84", "7-951"]
    cnt = Counter(ch for l in blk for ch in l if ch.isdigit())
    ok = (walk == [3, 7, 7, 9, 3] and nine and blk[2] == blk[0][::-1] and blk[1] == blk[1][::-1]
          and len(cnt) == 6 and set(cnt.values()) == {2} and dr(6 * 2) == 3
          and 159 + 951 == 1110 == 30 * 37 and 159 - 48 == 111 == 3 * 37 and sum(range(1, 10)) - 6 == 39 and dr(39) == 3)
    return ok, f"running roots {walk}; digits used {sorted(cnt)} twice each, left out {sorted(set('123456789') - set(cnt))}; without its 6 the grid adds to 39 -> 3"


@check(B_1013, "6 and 2 both ways round: 6+2 = 8; the '6+2=12' is 6 x 2 = 12 (as #263 writes it: 6x2=(1+2=3)); 6/2 and 2/6 are reciprocal; 6-2 = 4 and 2-6 = -4 (the signs in the two lines are swapped; 4 + (-4) = 0 holds either way); x% of y = y% of x always, so 2% of 6 = 6% of 2 = 0.12; 8-12-16-20 have roots 8, 3, 7, 2",
       "#262 and #263, 2026-10-13",
       """6+2=8
6+2=12
6÷2
2÷6
6-2=-4
2-6=4+(-4)=0
...
2% of 6
6% of 2


2--3--7--2
8-12-16-20
...
6x2=(1+2=3)""")
def _():
    pct = all(Fraction(a, 100) * b == Fraction(b, 100) * a for a in range(1, 50) for b in range(1, 50))
    ok = (6 + 2 == 8 and 6 * 2 == 12 and dr(12) == 3 and Fraction(6, 2) * Fraction(2, 6) == 1
          and 6 - 2 == 4 and 2 - 6 == -4 and 4 + (-4) == 0 and pct and Fraction(2, 100) * 6 == Fraction(12, 100)
          and [dr(v) for v in (8, 12, 16, 20)] == [8, 3, 7, 2] and dr(8 + 12) == 2)
    return ok, ("6 - 2 = 4, 2 - 6 = -4 (written -4 and 4: swapped); 2% of 6 = 6% of 2 = 3/25 = 0.12; "
                "roots of 8, 12, 16, 20: 8, 3, 7, 2 -- the row 2--3--7--2 matches at 3, 7, 2; 8 + 12 = 20 -> 2 (#263) gives the first 2")


@check(B_1013, "Halving strings: 8 -> 44|2222|11111111 = 44222211111111 exactly as written; 6 -> 33|2211|111111 = 332211111111 (3322111 is its first 7 digits: open which was meant); every level adds back to the number. The chain 3+4=7+9=16+14=30+23 = 53 -> 5+3 = 8, and 14 + 23 = 37",
       "#263, 2026-10-13",
       """1=1
2=11
6=3322111
8 =44222211111111

6x2=(1+2=3)
6+2=(8+12=20)
3+4=7+9=16+14=30+23=5+3=8""")
def _():
    def halving(v):
        rows, row = [], [v]
        while any(x > 1 for x in row):
            row = [p for x in row for p in ((x // 2, x - x // 2) if x > 1 else (x,))]
            rows.append(sorted(row, reverse=True))
        return rows
    string = lambda v: "".join("".join(map(str, r)) for r in halving(v))
    run, acc = [], 0
    for a in (3, 4, 9, 14, 23):
        acc += a
        run.append(acc)
    ok = (string(2) == "11" and string(8) == "44222211111111" and string(6) == "332211111111"
          and string(6)[:7] == "3322111" and all(sum(r) == v for v in range(2, 40) for r in halving(v))
          and run == [3, 7, 16, 30, 53] and dr(53) == 8 and 14 + 23 == 37 and 53 % 37 == 16)
    return ok, f"8 -> {string(8)}; 6 -> {string(6)}; running sums {run}; 53 -> {dr(53)}; 16 and 53 share residue 16 mod 37 (14 + 23 = 37)"


@check(B_1013, "+1 to begin again: 123+1 -> 7 and 456+1 -> 7 hold; 789+1 = 790 -> 7 (789 has root 6 like the other rows; it is 9 alone that gives 9+1 -> 1); 7+7 = 14 -> 5, +1 = 6 holds; the rows 123, 456, 789 are all 12 mod 37 and after +1 all 13",
       "#264, 2026-10-13",
       """one short because everything needs +1 after downloading to begin again

123+1=1+6=7
456+1=1+6=7
789+1=1+9=1

7+7=1+4=5+1=6""")
def _():
    rows = (123, 456, 789)
    ok = ([dr(v) for v in rows] == [6, 6, 6] and [dr(v + 1) for v in rows] == [7, 7, 7]
          and digit_sum(789) == 24 and dr(9 + 1) == 1 and dr(790) == 7 and 7 + 7 == 14 and dr(14) + 1 == 6
          and [v % 37 for v in rows] == [12] * 3 and [(v + 1) % 37 for v in rows] == [13] * 3)
    return ok, "roots 6, 6, 6 -> +1 -> 7, 7, 7; mod 37: 12, 12, 12 -> 13, 13, 13 (CAS_EXT); 789 + 1 = 790 -> 7"


# ==================================================================================
# Counting the commas: with 1 / with out (#265-#269)
# ==================================================================================
B_COMMA = "Counting the commas: count commas with 1 / with out (#265-#269)"


def count_commas(commas, with1):
    """#266: lead 1, then each comma and its group of 3; with 1 the commas count on from the 1."""
    out = [1]
    for c in range(1, commas + 1):
        out += [c + 1 if with1 else c, 3]
    return int("".join(map(str, out)))


@check(B_COMMA, "Comma sets: 0,000 = 1+3 = 4, 00,000 = 2+3 = 5, 000,000 = 3+3 = 6, 0,000,000 = 1+6 = 7 (lead group plus groups of 3). +111 adds 1 to every digit and never changes the residue mod 37 (111 = 3 x 37); 336 - 167 = 169 = 13^2; 167 is a safe prime; 11323 = 169 x 67",
       "#265, 2026-10-13",
       """a set can be
0,000=1+3=4
00,000=2+3=5
000,000=3+3=6
0+1=0,000,000=1+6=7

...
134+111
235+111
336-167
167=cap plus new beginning""")
def _():
    sets = [(s, len(s.split(",")[0]), sum(map(len, s.split(",")))) for s in ("0,000", "00,000", "000,000", "0,000,000")]
    groups = all(len(g) == 3 for s, _, _ in sets for g in s.split(",")[1:])
    plus111 = all((n + 111) % 37 == n % 37 for n in range(1000))
    ok = ([t for _, _, t in sets] == [4, 5, 6, 7] and groups and plus111 and 134 + 111 == 245 and 235 + 111 == 346
          and 336 - 167 == 169 == 13 ** 2 and is_prime(167) and is_prime(83) and 11323 == 169 * 67 and 134 == 2 * 67
          and 6 + 1 == 7)
    return ok, ("digits per set 4, 5, 6, 7; 134 + 111 = 245, 235 + 111 = 346 (the 346 under the #259 grid); "
                "167 = 2 x 83 + 1 with 83 prime; 'cap plus new beginning': 6 + 1 = 7, written 1, 6, 7")


@check(B_COMMA, "Count commas with 1 gives 12333, with out gives 11323 -- both come out of the #266 rule for 0,000,000; the same rule gives 123 / 113 for 0,000 and 1233343 / 1132333 for 0,000,000,000; with minus with out = 1010",
       "#265 and #266, 2026-10-13",
       """or 12333 count commas with 1
or 11323 count commas with out
...
If I start at 1, I count the comma as 2. And then I continue to count those commas from there. Then I will get to a 3. If I start at 1, I don't count the comma as adding 2. Then I get 1, 1 at the beginning of my count. Then I get 3. We get another comma, that's 2. And then 3 again.""")
def _():
    w, wo = count_commas(2, True), count_commas(2, False)
    ok = (w == 12333 and wo == 11323 and (count_commas(1, True), count_commas(1, False)) == (123, 113)
          and (count_commas(3, True), count_commas(3, False)) == (1233343, 1132333) and w - wo == 1010
          and "0,000,000".count(",") == 2 and 12333 % 37 == 123 % 37 == 12)
    return ok, f"with 1: {w}; with out: {wo}; difference {w - wo}; 12333 and 123 are both 12 mod 37 (12333 - 123 = 37 x 330)"


@check(B_COMMA, "The pairs 12=3, 21=3, 34=7, 43=7, 46=1, 64=1, 33=6, 77=5, 11=2 all hold; 12+34 = 46 and 21+43 = 64; 12+21 = 33, 34+43 = 77, 46+64 = 110 = 33+77; a two-digit number plus its reversal is always 11 x its digit sum; 24+13 = 37 -> 3+7 = 10, +1 = 11",
       "#267, 2026-10-13",
       """0,------000=1+3=4
00,------00=2+2=4
000,------0=3+1=4

4×3=12
3×4=12==(2+4=6)
7×7=4+9=(1+3=4)

6+4=10
24+13=3+7=(10+1)=11


12=3
21=3


34=7
43=7

46=1
64=1

33=6
77=5
11=2""")
def _():
    pairs = owner_equations_hold("12=3\n21=3\n34=7\n43=7\n46=1\n64=1\n33=6\n77=5\n11=2")
    slide = [(len(s.split(",")[0]), len(s.split(",")[1].replace("-", ""))) for s in ("0,------000", "00,------00", "000,------0")]
    rev11 = all(n + int(str(n)[::-1]) == 11 * digit_sum(n) for n in range(10, 100) if n % 10)
    ok = (all(o for _, o in pairs) and slide == [(1, 3), (2, 2), (3, 1)] and 4 * 3 == 3 * 4 == 12 and dr(24) == 6
          and 7 * 7 == 49 and digit_sum(49) == 13 and digit_sum(13) == 4 and 12 + 34 == 46 and 21 + 43 == 64
          and 12 + 21 == 33 and 34 + 43 == 77 and 46 + 64 == 110 == 33 + 77 and rev11
          and 24 + 13 == 37 and 3 + 7 + 1 == 11 and 6 + 4 == 10 and dr(24) + dr(13) == 10)
    return ok, f"each pair line: {[l for l, o in pairs if o]}; comma splits {slide}; n + reversal = 11 x digit sum for all 81 two-digit n with no 0: {rev11}"


@check(B_COMMA, ",000 three times: 3, 6, 9 -> 18 -> 9; with the three commas 18+3 = 21 and 9+3 = 12 -- both root 3, reversals of each other; 'this section goes by 369': 369 = 3 x 123",
       "#268, 2026-10-13",
       """this section goes by 369
like this
23
123
1123

when we count the comma


also with a comma we get 369

,000=3
,000=6
,000=9=18
1+8=9
and if we add the commas
=18+3=21
=9+3=12""")
def _():
    run = [len(",000,000,000".split(",")[1]) * k for k in (1, 2, 3)]
    ok = (run == [3, 6, 9] and sum(run) == 18 and dr(18) == 9 and 18 + 3 == 21 and 9 + 3 == 12
          and dr(21) == dr(12) == 3 and str(21)[::-1] == "12" and 369 == 3 * 123
          and [digit_sum(n) for n in (23, 123, 1123)] == [5, 6, 7] and is_prime(23) and is_prime(1123))
    return ok, "3, 6, 9 -> 18 -> 9; +3 -> 21 and 12; 23, 123, 1123 have digit sums 5, 6, 7 (how they go by 3, 6, 9 is still open)"


@check(B_COMMA, "10-20-30 over 11-22-33: the columns add to 21, 42, 63 -> 3, 6, 9; 3+6+9 = 18 -> 9, and with the 3 zeros 9+3 = 12 -> 3; 123 written twice digit by digit is 112233 = 3 x 11 x 19 x 179",
       "#269, 2026-10-13",
       """because
123
112233

10-20-30
11-22-33
3---6--9+3 zeros =1+2=3
...
no comma count should be explored also because it creates a better understanding of the bigger picture..""")
def _():
    tens, twins = [10, 20, 30], [11, 22, 33]
    cols = [a + b for a, b in zip(tens, twins)]
    ok = (cols == [21, 42, 63] and [dr(c) for c in cols] == [3, 6, 9]
          and "".join(map(str, tens)).count("0") == 3 and dr(3 + 6 + 9) == 9 and 9 + 3 == 12 and dr(12) == 3
          and int("".join(d * 2 for d in "123")) == 112233 and factor(112233) == {3: 1, 11: 1, 19: 1, 179: 1})
    return ok, f"columns {cols} -> {[dr(c) for c in cols]}; 112233 = {factor(112233)}"


# ==================================================================================
# Odd and even, the doubling, and 181 (#270); the July cipher (2026-07-16)
# ==================================================================================
B_DOUBLE = "Odd and even, the doubling, 181 (#270), and the cipher 123 of 2026-07-16"


@check(B_DOUBLE, "The doubling roots 1, 2, 4, 8, 7, 5, 1 (written 1248 / 751): the 7th is the second 1, because 2^6 = 64 = 1 (mod 9), so the roots repeat every 6 for ever and never touch 3, 6, 9",
       "#270, 2026-10-13",
       """DOUBLE EVEN BY 4
1248
751

NOTICE AT THE 7 NUMBER I GET MY SECOND 1""")
def _():
    roots = [dr(2 ** k) for k in range(7)]
    forever = all(dr(2 ** k) == dr(2 ** (k + 6)) for k in range(300))
    never369 = all(dr(2 ** k) not in (3, 6, 9) for k in range(300))
    ok = (roots == [1, 2, 4, 8, 7, 5, 1] and "".join(map(str, roots[:4])) == "1248" and "".join(map(str, roots[4:])) == "751"
          and pow(2, 6, 9) == 1 and forever and never369 and all(dr(2 ** k) == dr_slow(2 ** k) for k in range(300)))
    return ok, f"roots of 2^0..2^6: {roots}; period 6 checked to 2^305; dr formula = repeated digit sum on all of them"


@check(B_DOUBLE, "In rows of 3 the roots are 124 / 875 / 1, and the first column reads 181 up or down; 124 + 875 = 999 because each root plus the one 3 places later is 9 (2^3 = 8 = -1 mod 9) -- so the columns run 1,8,1,8 / 2,7,2,7 / 4,5,4,5 for ever. My build out of 181: 1+8+1 = 10, 10/2 = 5 -> 55 (equal odds compress)",
       "#270, 2026-10-13",
       """because if not by sets of 4

124
875
1

see that 181? firsr row up or down

which is

18+1=1+9=1
1+18=1+9=1+1=2)0


my build out of 181
55=equal odds compress 
because 10÷2=5

1÷2=0.5+0.5=1.""")
def _():
    r = [dr(2 ** k) for k in range(7)]
    rows = [r[0:3], r[3:6], r[6:]]
    col1 = "".join(str(x[0]) for x in rows)
    nine = all(dr(2 ** k) + dr(2 ** (k + 3)) == 9 for k in range(1000))
    ok = (rows == [[1, 2, 4], [8, 7, 5], [1]] and col1 == "181" == col1[::-1] and 124 + 875 == 999 == 27 * 37
          and pow(2, 3, 9) == 8 and nine and 18 + 1 == 1 + 18 == 19 and dr(19) == 1 and is_prime(181) and is_prime(179)
          and digit_sum(181) == 10 and Fraction(10, 2) == 5 and Fraction(1, 2) + Fraction(1, 2) == 1)
    return ok, (f"rows {rows}; column 1 = {col1}; root + root 3 later = 9 for k < 1000: {nine}; 181 is prime, twin with 179; "
                f"my build out of 181: 1 + 8 + 1 = 10, 10 / 2 = 5 and 5 (55), 1 / 2 = 0.5 + 0.5 = 1. typo: 'firsr' for first")


@check(B_DOUBLE, "Odd and even: 1+1 = 2 (odd+odd even), 2+3 = 5 (mixed is odd); 3+4 = 7 halves to 3.5 + 3.5 and 3+5+3+5 = 16, 16/2 = 8, 8+8 = 16. 248 + 510 = 758: roots 5 + 6 = 11 -> 2 and 758 -> 20 -> 2 (digital roots add). 8 = 44,222,211,111,111 is the halving string of 8 with commas: 14 digits, digit sum 24",
       "#270, 2026-10-13",
       """It may boil down to this

1+1=2(odd+odd=( thats even)
2+3=5(even,odd=(mix uneven)
3+4=7(3.5+3.5=16÷2=(8+8)
...
8=44,222,211,111,111=
...
EEE=Doubling SETS OF 3
248+  5
510=+6+5=(1+1=2)
758+20=2""")
def _():
    parity = all((a + b) % 2 == (a % 2 + b % 2) % 2 for a in range(20) for b in range(20))
    adds = all(dr(dr(a) + dr(b)) == dr(a + b) for a in range(1, 300) for b in range(1, 300))
    s = "44222211111111"
    ok = (parity and (1 + 1) % 2 == 0 and (2 + 3) % 2 == 1 and Fraction(7, 2) * 2 == 7 and 3 + 5 + 3 + 5 == 16
          and 16 // 2 == 8 and 248 + 510 == 758 and (dr(248), dr(510), dr(758)) == (5, 6, 2) and digit_sum(758) == 20
          and adds and f"{int(s):,}" == "44,222,211,111,111" and len(s) == 14 and digit_sum(int(s)) == 24
          and all(int(c) % 2 == 0 for c in "248"))
    return ok, "roots of 248, 510, 758: 5, 6, 2; dr(a) + dr(b) reduces to dr(a + b) for all a, b < 300; 44222211111111 with commas = 44,222,211,111,111"


@check(B_DOUBLE, "The cipher of 2026-07-16 and the lines of 2026-10-13 are the same structure: the unity pairs (3,7), (6,4), (9,1) are exactly the trinity + doubling pairs adding to 1 mod 9, and #267 (6+4, 24+13 = 3+7), #268 (369) and #270 (1248 / 751, 18+1) write all three",
       "the owner's file math/theorems/cipher_123_1234.py (2026-07-16), then #267, #268, #270",
       """CIPHER 1: 123 → 6 + 4 = 1
...
Trinity kernel (multiples of 3): {3, 6, 9}
Doubling orbit:                   {1, 2, 4, 5, 7, 8}
...
(3,7), (6,4), (9,1) — exactly 3 of 18 possible pairs
...
6+4=10
24+13=3+7=(10+1)=11
...
this section goes by 369
...
18+1=1+9=1""")
def _():
    T, Dd = {3, 6, 9}, {1, 2, 4, 5, 7, 8}
    unity = sorted((t, d) for t in T for d in Dd if (t + d) % 9 == 1)
    orbit9 = [pow(2, k, 9) or 9 for k in range(7)]
    ok = (unity == [(3, 7), (6, 4), (9, 1)] and len(T) * len(Dd) == 18 and T | Dd == set(range(1, 10))
          and dr(1 + 2 + 3) == 6 and dr(6 + 4) == 1 and dr(24) == 6 and dr(13) == 4 and 24 + 13 == 37
          and set(orbit9) == Dd and dr(18) == 9 and dr(18 + 1) == 1 and 1234 % 37 == 13)
    return ok, f"unity pairs {unity} of 18; doubling orbit {orbit9}; 24 + 13 = 37 -> 3 + 7; 18 + 1 -> 1; 1234 mod 37 = {1234 % 37}"


# ==================================================================================
# Earlier pages: 2026-09-23 to 2026-10-06
# ==================================================================================
B_EARLY = "Earlier pages, 2026-09-23 to 2026-10-06"


@check(B_EARLY, "The draining system (casting out tens): 1+...+9 = 45 and 45+1 = 46 -> 4+6 = 10, one drain; the k-th nine is 9k counting nines and 10k-1 counting tens (27 / 29, 36 / 39); k nines drain with +k (9k + k = 10k); 99 needs only +1; the O/E code is n-1 in three binary places",
       "the owner's message of 2026-09-23, filed verbatim in math/theorems/casting_out_tens_drain_system.py; #196, 2026-10-06",
       """Show me who did casting out fives. Show me who did casting out tens, because the only thing I heard about is casting out fucking nines.
...
"10 isnt tens its a marker meaning 1 zero has been drained...
...
45+1=4+6=10
...
but at 18 which is 9+9 =18 is our true second 9 not 19...19 is based on counting 10s..
...
second 9+9 needs +1+1 +2=20=(27 nines)(29 tens)
third =9+9+9=27 needs +1+1+1 +3=30-(36)(39
...
what's interesting is when I get to 99 i only need +1
...
1=LLO 2=LLE 3=LRO 4=LRE 5=RLO 6=RLE 7=RRO 8=RRO\"""")
def _():
    code = []
    for n in range(1, 9):
        b = n - 1
        code.append(("R" if b & 4 else "L") + ("R" if b & 2 else "L") + ("E" if b & 1 else "O"))
    owner = "LLO LLE LRO LRE RLO RLE RRO RRO".split()
    nth = [(9 * k, 10 * k - 1) for k in range(1, 5)]
    ok = (sum(range(1, 10)) == 45 and digit_sum(45 + 1) == 10 and nth == [(9, 9), (18, 19), (27, 29), (36, 39)]
          and all(9 * k + k == 10 * k for k in range(1, 1000)) and 99 + 1 == 100
          and code[:7] == owner[:7] and code[7] == "RRE")
    return ok, f"k-th nine (nines, tens): {nth}; the code from n-1 in binary: {code} -- 1..7 as written; typo: RRO for RRE at 8"


@check(B_EARLY, "The field around 12: 12 - 9 = 3 = 1+2 and 12 + 9 = 21 (the flip); 12 is the only two-digit number that does both. In the chain, 32 - 9 = 23 holds and 23 - 9 is 14 (reaching 12 from 23 takes -11: open)",
       "the owner's lines of 2026-10-04, recorded in math/lemmas/center_out_x.py",
       """OWNER'S CHAIN (2026-10-04): (1+2) = 32-9 = 23-9 = 12-9 = 3-(2 = 1).""")
def _():
    both = [n for n in range(10, 100) if n % 10 and n - 9 == digit_sum(n) and n + 9 == int(str(n)[::-1])]
    down = all(dr(n + 9 * j) == dr(n) for n in range(1, 500) for j in range(1, 20))
    ok = both == [12] and 32 - 9 == 23 and 23 - 9 == 14 and 12 - 9 == 3 == 1 + 2 and 3 - 2 == 1 and down
    return ok, f"two-digit numbers with n - 9 = digit sum and n + 9 = flip: {both}; adding 9 never changes the root: {down}"


@check(B_EARLY, "The window lines of 246: 24~62, 46~24, 62~46 give 5, 7, 9 -- the owner's '795 new set of 3' -- and for EVERY row abc the new set is the digits shifted by the digit sum: dr(a+b+c+a), dr(a+b+c+b), dr(a+b+c+c)",
       "the owner's lines of 2026-10-04, recorded in math/lemmas/rotation_grids_x.py",
       """24~62 = 6+8 = (1+(4 = 5) = 10 = 1
46~24 = (1+(6 = 7) = 1+6 = 7+7 = 1+4 = 5
62~46 = (8+(1 = 9) = 8+1+9 = 1+8 = 9
795 new set of 3 / 861 / 618""")
def _():
    def new_set(a, b, c):
        w = [10 * a + b, 10 * b + c, 10 * c + a]
        return [dr(digit_sum(w[i]) + digit_sum(w[i - 1])) for i in range(3)]
    v = new_set(2, 4, 6)
    rule = all(new_set(a, b, c) == [dr(a + b + c + x) for x in (a, b, c)]
               for a in range(1, 10) for b in range(1, 10) for c in range(1, 10))
    win = [dr(digit_sum(w)) for w in (24, 46, 62)]
    ok = (v == [5, 7, 9] and "795" in rotations("579") and rule and win == [6, 1, 8]
          and "861" in rotations("186") and "618" in rotations("186") and [dr(2 * x) for x in v] == [1, 5, 9])
    return ok, f"246 -> {v} (795 is a turn of 579); window roots {win} (861, 618: turns of 186); rule holds for all 729 rows of digits 1-9: {rule}"


@check(B_EARLY, "The infinite growth cycle: FILL (put the missing number next to the larger end) and ONES (a 1 between every pair) reproduce the owner's lines 246 -> 23456 -> 213141516 -> 2123213431454156 exactly; each cycle about doubles the length (measured over nine cycles, ratio 2.07; the limit 2 is read from the pattern, not proved)",
       "the owner's lines of 2026-10-04, recorded in math/lemmas/infinite_growth_cycle.py",
       """"I continuously add the missing numbers in between that create a space for
new gaps that need to be filled in"
246
23456
213141516        "after 3 we get ones"
2123213431454156 "make sure I did right"
0 / 00 / 000 / 0000 = double""")
def _():
    def fill(s):
        out = [s[0]]
        for a, b in zip(s, s[1:]):
            if abs(a - b) >= 2:
                out.append(max(a, b) - 1)
            out.append(b)
        return out

    def ones(s):
        out = [s[0]]
        for b in s[1:]:
            out += [1, b]
        return out
    show = lambda s: "".join(map(str, s))
    s1 = fill([2, 4, 6])
    s2 = ones(s1)
    s3 = fill(s2)
    s, lengths = [2, 3, 4, 5, 6], [5]
    for _ in range(9):
        s = ones(s)
        while fill(s) != s:
            s = fill(s)
        lengths.append(len(s))
    ok = ((show(s1), show(s2), show(s3)) == ("23456", "213141516", "2123213431454156")
          and lengths == [5, 25, 93, 281, 741, 1785, 4045, 8793, 18581, 38521])
    return ok, f"{show(s1)} -> {show(s2)} -> {show(s3)}; gap-free lengths {lengths}; last ratio {lengths[-1] / lengths[-2]:.2f}"


@check(B_EARLY, "Building 4 from 1, 2, 3 has 7 ways -- the list had 5 and is missing 2+2 and 1+2+1; by the owner's rule (the next number made only from the numbers before it) n has 2^(n-1) - 1 ways: 1, 3, 7, 15, 31, ...",
       "the owner's lines of 2026-10-04, recorded in math/lemmas/compositions_of_n.py",
       """2 = 1+1
3 = 111, 2+1, 1+2
4 = 1+3, 3+1, 11+2, 2+11, 1111   "at 4 it gets way more complicated"
"double check I am not missing any combinations of 123 to make 4\"""")
def _():
    def comps(n, parts):
        if n == 0:
            return [[]]
        return [[p] + r for p in parts if p <= n for r in comps(n - p, parts)]
    four = sorted("+".join(map(str, c)) for c in comps(4, (1, 2, 3)))
    given = {"1+3", "3+1", "1+1+2", "2+1+1", "1+1+1+1"}
    counts = [len(comps(n, range(1, n))) for n in range(2, 13)]
    ok = (len(four) == 7 and sorted(set(four) - given) == ["1+2+1", "2+2"]
          and counts == [2 ** (n - 1) - 1 for n in range(2, 13)])
    return ok, f"the 7 ways: {four}; counts for n = 2..12: {counts}"


@check(B_EARLY, "M and W from pyramids: on the pyramid line 0 1 2 1 0 1 2 1 0 ..., moving half a pyramid (2 steps) turns it over: h(t+2) = 2 - h(t). So every M carries a W, M + W = 2 everywhere, and turning over twice gives back the start",
       "#7, #8 and #9, 2026-10-06",
       """One of the things that you can make is two pyramids next to each other. That would be the M. If I were to put two pyramids in the creases that they created, that would be our W.
...
Whenever you create an M, you also create a W. So think about it this way. Half of the M is M, and the other half of it is W.
...
Because whenever I make an M, I'm making an upside down W. And whenever I make a W, I'm making an upside M.""")
def _():
    h = lambda t: (0, 1, 2, 1)[t % 4]
    M = [h(t) for t in range(9)]
    W = [2 - x for x in M]
    shift = all(h(t + 2) == 2 - h(t) for t in range(1000))
    ok = (M == [0, 1, 2, 1, 0, 1, 2, 1, 0] and W == [h(t + 2) for t in range(9)] and shift
          and all(a + b == 2 for a, b in zip(M, W)) and [2 - x for x in W] == M)
    return ok, f"M = {M}; W = {W} = the same line 2 steps later; h(t+2) = 2 - h(t) for t < 1000: {shift}"


@check(B_EARLY, "Seven colours = 3 + 4: 3 and 4 are in one 137-map cycle {3, 4, 30}; 7 is in {7, 33, 34} = its negative (37-3, 37-4, 37-30); 2 x 3 + 1 = 7 (a Sophie Germain step); 3 and 7 are both twin primes, sharing 5",
       "#15, 2026-10-06",
       """So, we have three things. How many are on, how many are in the spectrum? That's three, red, green, and blue. How many colors are there?""")
def _():
    neg = tuple(sorted(37 - x for x in orbit(3)))
    ok = (orbit(3) == orbit(4) == (3, 4, 30) and orbit(7) == neg == (7, 33, 34) and 2 * 3 + 1 == 7
          and is_prime(3) and is_prime(7) and is_prime(5) and 3 + 4 == 7 and dr(3 * 4) == 3)
    return ok, f"orbit of 3 and 4: {orbit(3)}; orbit of 7: {orbit(7)} = 37 minus {orbit(3)}"


# ==================================================================================
# The multiples-of-9 block brought in #291 (pasted text, checked)
# ==================================================================================
B_NINE = "The multiples-of-9 block brought in #291 (pasted, checked)"
SRC_291 = "pasted in #291, 2026-10-14 (the block inside the command the owner sent)"


@check(B_NINE, "All twelve factorizations 342 ... 441 are right, and each has root 9 (forced: 9 divides n); 333 = 3^2 x 37; 19 = 2^-1 mod 37; 369 - 351 = 18; det [8 1 6; 3 5 7; 4 9 2] = -360; 378 = 370 + 8; 387 = 10 x 37 + 17; 396 = 36 x 11; 405 = 45 x 9; 23 divides 133,860; 441 = 21^2",
       SRC_291,
       """n = 342 = 2 · 3² · 19          → dr = 9    (19 = 2⁻¹ mod 37 ray multiplicity)
n = 351 = 3³ · 13              → dr = 9    (13 connects to N(1,7) = 4·13·37)
n = 360 = 2³ · 3² · 5          → dr = 9    (360 = Lo Shu determinant magnitude)
n = 369 = 3² · 41              → dr = 9    (41 connects to N(5,6) = 2·41·37)
...
n = 441 = 3² · 7² = 21²        → dr = 9    (Square of the 21 anchor: 1776 → 21)""")
def _():
    claimed = {342: {2: 1, 3: 2, 19: 1}, 351: {3: 3, 13: 1}, 360: {2: 3, 3: 2, 5: 1}, 369: {3: 2, 41: 1},
               378: {2: 1, 3: 3, 7: 1}, 387: {3: 2, 43: 1}, 396: {2: 2, 3: 2, 11: 1}, 405: {3: 4, 5: 1},
               414: {2: 1, 3: 2, 23: 1}, 423: {3: 2, 47: 1}, 432: {2: 4, 3: 3}, 441: {3: 2, 7: 2}}
    m = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
    det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
           + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    ok = (list(claimed) == list(range(342, 442, 9)) and all(factor(n) == f for n, f in claimed.items())
          and all(dr(n) == 9 for n in claimed) and factor(333) == {3: 2, 37: 1} and 2 * 19 % 37 == 1
          and 369 - 351 == 18 and det == -360 and 370 + 8 == 378 and 10 * 37 + 17 == 387 and 36 * 11 == 396
          and 45 * 9 == 405 and 133860 % 23 == 0 and 21 ** 2 == 441 and digit_sum(1776) == 21
          and 4 * 13 * 37 == 1924 and 2 * 41 * 37 == 3034)
    return ok, (f"all 12 factorizations match; Lo Shu det = {det}; 133,860 = 23 x {133860 // 23}. "
                "I don't have enough information on N(a, b), 'isotropic class', 'Sigma N' or 'ray multiplicity': "
                "the paste does not define them (the numbers given for them, 1924 and 3034, multiply out right)")


@check(B_NINE, "Correction: 432 is not highly composite -- it has 20 divisors and the smaller 360 has 24; 360 is highly composite (more divisors than every smaller number)",
       SRC_291,
       """n = 432 = 2⁴ · 3³              → dr = 9    (Highly composite base-12/base-9 node)""")
def _():
    dc = [0] + [divisor_count(n) for n in range(1, 433)]
    hc = lambda n: all(dc[m] < dc[n] for m in range(1, n))
    ok = dc[432] == 20 and dc[360] == 24 and hc(360) and not hc(432)
    return ok, f"divisors: 432 -> {dc[432]}, 360 -> {dc[360]}; 360 highly composite: {hc(360)}; 432: {hc(432)}"


@check(B_NINE, "Correction: on the multiples of 9 the digital root is 9 every time, so it keeps no information about n -- 'zero information loss' is the opposite of what happens: everything but '9 divides n' is lost",
       SRC_291,
       """Every multiple of 9 sits permanently on the attractor horizon f(n) \\equiv 9, with zero information loss between steps.""")
def _():
    values = {dr(9 * k) for k in range(1, 100001)}
    ok = values == {9} and dr_slow(9 * 123456789) == 9
    return ok, f"distinct roots over the first 100,000 multiples of 9: {sorted(values)}"


# ==================================================================================
# Run everything
# ==================================================================================

def main():
    start = time.time()
    passed = 0
    bucket = None
    for b, title, source, owner, fn in CHECKS:
        if b != bucket:
            bucket = b
            print()
            print("=" * 78)
            print(bucket)
            print("=" * 78)
        print()
        if source.startswith("#"):
            head = f"Michael Warren Song, {source}"          # the owner's own message
        elif source.startswith("pasted"):
            head = "Pasted (not the owner's words): " + source[len("pasted "):]
        else:
            head = source[0].upper() + source[1:]               # the owner's file or recorded lines
        print(f"  {head}:")
        blank = False
        for line in owner.splitlines():
            if not line.strip():
                if not blank:
                    print("    |")
                blank = True
                continue
            blank = False
            print("    | " + line.rstrip())
        try:
            ok, detail = fn()
        except Exception as exc:          # a crash is a FAIL, never a silent skip
            ok, detail = False, f"error: {exc!r}"
        if ok:
            passed += 1
            print(f"PASS  {title}")
            print(f"      {detail}")
        else:
            print(f"FAIL  {title}: {detail}")
    print()
    print(f"({time.time() - start:.1f} seconds)")
    print(f"{passed} of {len(CHECKS)} checks passed")
    return passed == len(CHECKS)


if __name__ == "__main__":
    main()
