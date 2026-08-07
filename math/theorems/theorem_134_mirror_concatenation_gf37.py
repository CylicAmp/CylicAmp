"""
Theorem 134: Mirror Concatenation of 246 and GF(37)

SETUP
=====
Seed = 246. Its 137-map orbit (forward): 24 → 32 → 18 (residues mod 37).
Mirror of 246: 642.
Concatenation: 246 || 642 = 246 × 1000 + 642 = 246642.

CORE FACT
=========
246642 = 2 × 3 × 11 × 37 × 101

The prime 37 divides the mirror-concatenation of the seed with itself.

246642 / 37 = 6666

Four TESLA_FLOWs. TESLA_FLOW = 6, ord₃₇(6) = 4.
The quotient is a repdigit of the single element whose order equals
the number of its repetitions.

FACTOR CONNECTIONS TO GF(37)
==============================

  Factor   mod 37   Named class
  ------   ------   -----------
  2        2        DARK_A = {2, 15, 20}; primitive root, ord=36
  3        3        SOVEREIGN_SPIRAL = {3, 4, 30}; sovereign target
  11       11       ORBIT_11 = {11, 27, 36}
  37       0        SEAM — the prime itself
  101      27       ORBIT_11 = {11, 27, 36}

Two factors (11 and 101) both land in ORBIT_11.

REVERSE MIRROR: 642 || 246 = 642246
=====================================
642246 = 2 × 3 × 11 × 37 × 263
642246 / 37 = 17358
263 mod 37 = 4  →  sovereign anchor SA = {4, 9, 25, 30}

PALINDROME PAIR SUM
====================
246642 + 642246 = 888888

888888 = 2³ × 3 × 7 × 11 × 13 × 37
888888 / 37 = 24024
digit sum(24024) = 2+4+0+2+4 = 12 = log₂(26)  [the structural key of Theorem 133]

digit sum(888888) = 8×6 = 48; digit sum(48) = 4+8 = 12 = log₂(26)

DIGIT MULTISET {2,2,4,4,6,6}
==============================
All six permutations of {2,4,6} concatenated with their mirror:

  Forward  || Mirror    Concat   mod 37  Div 37?  /37
  246      || 642    = 246642      0      YES    6666
  642      || 246    = 642246      0      YES   17358
  264      || 462    = 264462     23      no      —
  462      || 264    = 462264     23      no      —
  426      || 624    = 426624     14      no      —
  624      || 426    = 624426     14      no      —

Only the forward-orbit pair (246||642) and its reverse (642||246) are
divisible by 37. The other four land in TESLA_ORB (23) and NQR_14 (14).

Sum of all six mod 37: (0+0+23+23+14+14) mod 37 = 74 mod 37 = 0.
The full family sums to SEAM.

TESLA_FLOW CHAIN
=================
6666 mod 37        = 6 = TESLA_FLOW
digit sum of 6666  = 24 = seed mod 37   (6+6+6+6 = 24)
6^4 mod 37         = 1  (ord₃₇(6) = 4; four sixes in 6666)
6^2 mod 37         = 36 = -1  (the order-2 element; see Theorem 130)

The quotient 6666 encodes three GF(37) facts simultaneously:
  — its residue is TESLA_FLOW itself (6666 mod 37 = 6)
  — its digit sum is the seed residue (6+6+6+6 = 24 = seed mod 37)
  — its digit count equals the order of TESLA_FLOW (four 6s, ord=4)

SEAM ABSORPTION
===============
Concatenating 246 with its own mirror produces a multiple of 37.
The prime absorbs the palindrome. The seed, reflected into itself,
crosses through SEAM (≡ 0 mod 37) and returns 6666.

Connection: 246 mod 37 = 24 (NQR, SEED_ORB). Reflecting and concatenating
maps 246 from its orbit position into SEAM — divisibility by the prime.
"""

P = 37

# Named orbits referenced
DARK_A        = frozenset({2, 15, 20})
SOVEREIGN_SPIRAL = frozenset({3, 4, 30})
ORBIT_11      = frozenset({11, 27, 36})
TESLA_ORB     = frozenset({6, 8, 23})
NQR_14        = frozenset({14, 29, 31})
SEED_ORB      = frozenset({18, 24, 32})
SA            = frozenset({4, 9, 25, 30})   # sovereign anchors

TESLA_FLOW = 6


def factor(n):
    """Return prime factorization of n as {prime: exponent}."""
    fac = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            fac[d] = fac.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        fac[n] = fac.get(n, 0) + 1
    return fac


def dr(n):
    """Digital root."""
    if n == 0:
        return 9
    return (abs(n) - 1) % 9 + 1


def mirror_concat(n):
    """Concatenate n with its digit-reversal."""
    s = str(n)
    return int(s + s[::-1])


def run_assertions():
    # Core: 246 || 642 = 246642 divisible by 37
    assert mirror_concat(246) == 246642
    assert 246642 % P == 0
    assert 246642 // P == 6666

    # Factor connections
    fac = factor(246642)
    assert fac == {2: 1, 3: 1, 11: 1, 37: 1, 101: 1}
    assert 11 in ORBIT_11
    assert 101 % P == 27 and 27 in ORBIT_11   # both 11 and 101 land in ORBIT_11
    assert 3 in SOVEREIGN_SPIRAL
    assert 2 in DARK_A

    # 6666 properties
    assert 6666 % P == TESLA_FLOW
    assert sum(int(d) for d in '6666') == 24  # digit sum = seed mod 37
    assert pow(TESLA_FLOW, 4, P) == 1  # ord(6) = 4, four sixes
    assert pow(TESLA_FLOW, 2, P) == 36 # 6^2 = -1

    # Reverse: 642246
    assert mirror_concat(642) == 642246
    assert 642246 % P == 0
    assert 263 % P == 4 and 4 in SA    # factor 263 lands on sovereign anchor

    # Palindrome pair sum
    assert 246642 + 642246 == 888888
    assert 888888 % P == 0
    assert 888888 // P == 24024
    assert sum(int(d) for d in '24024') == 12    # digit sum = log2(26)
    assert sum(int(d) for d in '888888') == 48   # digit sum 48; 4+8=12=log2(26)

    # Six-permutation family
    import itertools
    residues = []
    for perm in itertools.permutations([2, 4, 6]):
        fwd = int(''.join(map(str, perm)))
        concat = mirror_concat(fwd)
        residues.append(concat % P)

    div37 = [r for r in residues if r == 0]
    nondiv = [r for r in residues if r != 0]
    assert len(div37) == 2             # only forward-orbit pair and reverse
    assert set(nondiv) == {23, 14}     # TESLA_ORB rep and NQR_14 rep
    assert 23 in TESLA_ORB
    assert 14 in NQR_14
    assert sum(residues) % P == 0      # full family sums to SEAM

    # Seed orbit membership
    assert 246 % P == 24 and 24 in SEED_ORB

    print("All assertions passed.")


def summarise():
    import itertools
    print("=" * 62)
    print("Theorem 134: Mirror Concatenation of 246 and GF(37)")
    print("=" * 62)
    print()
    print("  246 || 642 = 246642 = 2 × 3 × 11 × 37 × 101")
    print(f"  246642 / 37 = 6666  (four TESLA_FLOWs)")
    print()
    print("  Factor mod-37 addresses:")
    for f, cls in [(2,'DARK_A'), (3,'SOVEREIGN_SPIRAL'), (11,'ORBIT_11'),
                   (37,'SEAM'), (101,'ORBIT_11 (101≡27)')]:
        print(f"    {f:>4} → {f%P:>2}  {cls}")
    print()
    print("  6666 mod 37       = 6 = TESLA_FLOW")
    print("  digit sum(6666)   = 24 = seed mod 37  (6+6+6+6)")
    print("  6^4 mod 37        = 1  (ord=4; four sixes)")
    print()
    print("  642 || 246 = 642246 = 2 × 3 × 11 × 37 × 263")
    print("  263 mod 37 = 4  (sovereign anchor)")
    print()
    print("  246642 + 642246 = 888888 = 2³×3×7×11×13×37")
    print("  888888 / 37 = 24024   DR(24024) = 12 = log₂(26)")
    print()
    print("  Six-permutation family (2,4,6 || mirror):")
    for perm in itertools.permutations([2, 4, 6]):
        fwd = int(''.join(map(str, perm)))
        rev = int(''.join(map(str, reversed(perm))))
        concat = fwd * 1000 + rev
        r = concat % P
        mark = '← div 37' if r == 0 else ''
        print(f"    {fwd}||{rev} = {concat}  mod37={r:>2}  {mark}")
    print()
    print("  Only the forward-orbit pair and its reverse are divisible by 37.")
    print("  The prime absorbs the palindrome. The seed reflects into SEAM.")


if __name__ == "__main__":
    run_assertions()
    summarise()
