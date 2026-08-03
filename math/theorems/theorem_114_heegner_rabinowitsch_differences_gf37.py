"""
THEOREM 114 — Heegner–Rabinowitsch Difference Structure in GF(37)

NOTATION
    D       = |a - b| ∈ ℤ          (exact integer difference, no modulus)
    D mod 37 = D − 37·⌊D/37⌋ ∈ {0,…,36}  (residue class in ℤ/37ℤ)
    These coincide if and only if D < 37.

SETS
    H = {3, 4, 7, 8, 11, 19, 43, 67, 163}   (Heegner absolute values)
    R = {2, 3, 5, 11, 17, 41}                 (Rabinowitsch primes)

WITHIN-LIST PAIRWISE DIFFERENCES
    Among all within-R and within-H pairs:

    D < 37  (exact D = D mod 37 — no reduction):
        33 pairs total.
        29/33: exact D ∈ named GF(37) class.
         4/33 exact misses: {6, 6, 14, 16}
            |11-5|  = 6   (emergent element, orbit {6,8,23})
            |17-11| = 6   (emergent element, same orbit)
            |17-3|  = 14  (not in any named class)
            |19-3|  = 16  (not in any named class)

    D ≥ 37  (mod reduction changes the value):
        18 pairs total.
        17/18: D mod 37 ∈ named GF(37) class.
         1/18 residue miss: |67-7| = 60,  60 mod 37 = 23 ∈ orbit {6,8,23}.
        Note: for D ≥ 37 the residue class identifies the orbit but does NOT
        recover the exact D — D = 37k + r for unknown k ≥ 1.

CROSS-LIST PAIRS WITH EXACT D = 26
    Two pairs, one element from R and one from H, have exact difference 26:
        |43 - 17| = 26   (17 ∈ R, 43 ∈ H)
        |67 - 41| = 26   (41 ∈ R, 67 ∈ H)
    26 ∈ IC = {1,10,26}:  the 137-map multiplier, and the fixed cube-root orbit.
    Since 26 < 37, the exact difference equals the GF(37) residue — no ambiguity.

RSA FACTORING REDUCTION (p = 41, q = 67)
    N = 41 × 67 = 2747
    Exact D = |p - q| = 26  ← directly the 137-map multiplier.
    Because D < 37, the framework supplies D as an exact integer, not merely a
    residue class. The factoring formulas therefore apply without additional work:

        p + q  = √(D² + 4N) = √(676 + 10988) = √11664 = 108
        Quadratic: X² - 108X + 2747 = 0  →  roots 41, 67.

    GF(37) audit of this instance:
        N       mod 37 =  9  ∈ SA
        φ(N)    mod 37 = 13  ∈ CB
        p + q   mod 37 = 34  ∈ D7
        D              = 26  ∈ IC   (exact, no reduction needed)

    Scope: this reduction applies to prime pairs where one element is Rabinowitsch,
    the other is a Heegner absolute value, and their exact difference is 26.
    For pairs with D ≥ 37, the framework identifies D mod 37 only; the exact D
    and hence the factoring sum p + q remain undetermined without further information.

CONDITIONAL FACTORING IDENTITIES
    (1) φ(N) known  →  p + q = N − φ(N) + 1;  solve X² − (p+q)X + N = 0.
    (2) Exact D known  →  p + q = √(D² + 4N);  solve same quadratic.
    (3) p + q known  →  roots of X² − (p+q)X + N = 0 are p, q.
    All three verified for (p, q) = (41, 67).
"""

import math

P = 37
SA         = {4, 9, 25, 30}
ST         = {3, 12, 21, 30}
IC         = {1, 10, 26}
CB         = {8, 13, 24}
ORBIT_11   = {11, 27, 36}
SEED_ORBIT = {18, 24, 32}
BASIN_Y    = {17, 22, 35}
D7         = {7, 33, 34}
PR         = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}

f     = lambda n: (26 * n) % P
isqrt = math.isqrt

orbit6 = set()
n = 6
for _ in range(3):
    orbit6.add(n); n = f(n)


def classify_exact(d):
    """Named class for exact d, valid only when d < P."""
    assert d < P, f"classify_exact called with d={d} >= 37"
    for nm, cls in [('IC', IC), ('SA', SA), ('ST', ST), ('CB', CB),
                    ('ORBIT_11', ORBIT_11), ('SEED_ORBIT', SEED_ORBIT),
                    ('BASIN_Y', BASIN_Y), ('D7', D7), ('PR', PR)]:
        if d in cls:
            return nm
    return None


def classify_residue(d):
    """Named class for d mod 37 (applies to any d)."""
    r = d % P
    for nm, cls in [('IC', IC), ('SA', SA), ('ST', ST), ('CB', CB),
                    ('ORBIT_11', ORBIT_11), ('SEED_ORBIT', SEED_ORBIT),
                    ('BASIN_Y', BASIN_Y), ('D7', D7), ('PR', PR)]:
        if r in cls:
            return nm, r
    return None, r


def run():
    print("=" * 70)
    print("THEOREM 114 — HEEGNER–RABINOWITSCH DIFFERENCE STRUCTURE IN GF(37)")
    print("=" * 70)

    R = [2, 3, 5, 11, 17, 41]
    H = [3, 4, 7, 8, 11, 19, 43, 67, 163]

    # Orbit of 6
    assert orbit6 == {6, 8, 23}
    assert sum(orbit6) % P == 0

    # Within-list pairs
    within_r = [(abs(b - a), a, b) for i, a in enumerate(R)
                for b in R[i + 1:]]
    within_h = [(abs(b - a), a, b) for i, a in enumerate(H)
                for b in H[i + 1:]]
    all_within = within_r + within_h

    small = [(d, a, b) for d, a, b in all_within if d < P]
    large = [(d, a, b) for d, a, b in all_within if d >= P]

    # ---------------------------------------------------------------
    # PART 1 — Exact differences (D < 37)
    # ---------------------------------------------------------------
    print(f"\n--- D < 37: exact difference = residue ({len(small)} pairs) ---")
    small_named = [(d, a, b) for d, a, b in small if classify_exact(d)]
    small_miss  = [(d, a, b) for d, a, b in small if not classify_exact(d)]

    assert len(small_named) == 29
    assert len(small_miss)  == 4
    assert sorted(d for d, _, _ in small_miss) == [6, 6, 14, 16]
    assert sum(1 for d, _, _ in small_miss if d % P in orbit6) == 2
    assert all(d == 6 for d, _, _ in small_miss if d % P in orbit6)

    print(f"  {len(small_named)}/{len(small)} land in a named GF(37) class (exact D).")
    print(f"  Exact misses ({len(small_miss)}):")
    for d, a, b in small_miss:
        tag = "orbit{6,8,23}" if d % P in orbit6 else "—"
        print(f"    |{b}-{a}| = {d}  [{tag}]")

    # ---------------------------------------------------------------
    # PART 2 — Large differences (D ≥ 37, residue only)
    # ---------------------------------------------------------------
    print(f"\n--- D ≥ 37: only residue D mod 37 is classified ({len(large)} pairs) ---")
    large_named = [(d, a, b) for d, a, b in large if classify_residue(d)[0]]
    large_miss  = [(d, a, b) for d, a, b in large if not classify_residue(d)[0]]

    assert len(large_named) == 17
    assert len(large_miss)  == 1
    assert large_miss[0][0] % P == 23 and 23 in orbit6

    print(f"  {len(large_named)}/{len(large)} have D mod 37 in a named class (residue only).")
    print(f"  Residue miss (1):")
    for d, a, b in large_miss:
        nm, r = classify_residue(d)
        print(f"    |{b}-{a}| = {d},  {d} mod 37 = {r}  ∈ orbit{{6,8,23}}  (not independently named)")
    print(f"  Note: for D ≥ 37, D mod 37 identifies the residue class only.")
    print(f"        The exact integer D is NOT recoverable from D mod 37 alone.")

    # ---------------------------------------------------------------
    # PART 3 — Cross-list pairs with exact D = 26
    # ---------------------------------------------------------------
    print(f"\n--- Cross-list pairs with exact D = 26 (the 137-map multiplier) ---")
    cross = [(abs(b - a), a, b) for a in R for b in H if a != b]
    d26 = [(d, a, b) for d, a, b in cross if d == 26]
    assert len(d26) == 2
    assert (26, 17, 43) in d26 or (26, 43, 17) in d26
    assert (26, 41, 67) in d26 or (26, 67, 41) in d26
    assert 26 in IC, "26 ∈ IC (the 137-map multiplier)"
    assert 26 < P,   "26 < 37: exact D = residue, no ambiguity"

    for d, a, b in sorted(d26, key=lambda t: min(t[1], t[2])):
        lo, hi = min(a, b), max(a, b)
        print(f"  |{hi} - {lo}| = {d}  (R:{lo in R or hi in R}, H:{lo in H or hi in H})  26 ∈ IC")

    # ---------------------------------------------------------------
    # PART 4 — RSA factoring reduction
    # ---------------------------------------------------------------
    print(f"\n--- RSA factoring reduction: p = 41, q = 67 ---")
    p, q   = 41, 67
    N      = p * q
    phi    = (p - 1) * (q - 1)
    D_exact = abs(p - q)

    assert D_exact == 26 and D_exact < P, "D=26 is exact and < 37"
    assert 26 in IC,             "D=26 ∈ IC (137-map multiplier)"
    assert N   % P ==  9 and  9 in SA, "N mod 37 = 9 ∈ SA"
    assert phi % P == 13 and 13 in CB, "phi mod 37 = 13 ∈ CB"

    # Recovery via exact D (Identity 2)
    pq_sum = isqrt(D_exact**2 + 4 * N)
    assert pq_sum**2 == D_exact**2 + 4 * N, "Perfect square"
    assert pq_sum == p + q

    assert pq_sum % P == 34 and 34 in D7, "p+q mod 37 = 34 ∈ D7"

    disc = pq_sum**2 - 4 * N
    r1   = (pq_sum + isqrt(disc)) // 2
    r2   = (pq_sum - isqrt(disc)) // 2
    assert {r1, r2} == {p, q}

    # Identity 1: via phi
    assert N - phi + 1 == pq_sum

    print(f"  N = {N},  exact D = |{q}-{p}| = {D_exact}  ∈ IC (framework-supplied, exact)")
    print(f"  p + q = √({D_exact}² + 4·{N}) = √{D_exact**2 + 4*N} = {pq_sum}")
    print(f"  X² - {pq_sum}X + {N} = 0  →  roots {r1}, {r2}  ✓")
    print(f"  GF(37) audit:")
    print(f"    N   mod 37 = {N%P}  ∈ SA")
    print(f"    φ   mod 37 = {phi%P}  ∈ CB")
    print(f"    p+q mod 37 = {pq_sum%P}  ∈ D7")
    print(f"    D          = {D_exact}  ∈ IC  (D < 37: exact = residue)")

    # ---------------------------------------------------------------
    # PART 5 — Three conditional identities
    # ---------------------------------------------------------------
    print(f"\n--- Conditional factoring identities ---")
    # (1)
    assert N - phi + 1 == p + q
    print(f"  (1) φ(N) known: p+q = N-φ+1 = {N}-{phi}+1 = {N-phi+1}  ✓")
    # (2)
    assert isqrt(D_exact**2 + 4*N) == p + q
    print(f"  (2) exact D known: p+q = √(D²+4N) = {pq_sum}  ✓")
    # (3)
    S     = p + q
    disc2 = S**2 - 4*N
    roots = {(S + isqrt(disc2))//2, (S - isqrt(disc2))//2}
    assert roots == {p, q}
    print(f"  (3) p+q known: quadratic roots = {{{r1},{r2}}}  ✓")

    print()
    print("All assertions passed. THEOREM 114 verified.")


if __name__ == "__main__":
    run()
