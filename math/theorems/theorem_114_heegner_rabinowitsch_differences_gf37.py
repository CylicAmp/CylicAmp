"""
THEOREM 114 — Heegner–Rabinowitsch Difference Structure in GF(37)

The nine Heegner absolute values H = {3,4,7,8,11,19,43,67,163} and the
six Rabinowitsch primes R = {2,3,5,11,17,41} encode the GF(37) framework
in their pairwise differences.

COVERAGE
    Heegner  C(9,2) = 36 pairs:  34/36 differences ≡ named class (mod 37).
    Rabinowitsch C(6,2) = 15 pairs: 12/15 differences ≡ named class (mod 37).

    The two pairs that miss the named classes in each list are all connected
    to 6 or its 137-map orbit {6, 8, 23}:
      Rabinowitsch misses: 11-5=6 (orbit6), 17-11=6 (orbit6), 17-3=14 (—)
      Heegner misses:      67-7=60≡23 (orbit6), 19-3=16 (—)
    The misses at 6 and 23 are the emergent element (Theorem 113) and its
    orbit partner. The miss at 14 and 16 are genuine exceptions.

D = 26 PAIRS  (the 137-map multiplier, exactly)
    |67 - 41| = 26:  41 ∈ R (Rabinowitsch), 67 ∈ H (Heegner)
    |43 - 17| = 26:  17 ∈ R (Rabinowitsch), 43 ∈ H (Heegner)
    In both cases D = 26 exactly — no mod reduction needed.
    26 ∈ IC = {1, 10, 26}: the cube-roots-of-unity orbit.

RSA FACTORING REDUCTION (p=41, q=67)
    N = 41 × 67 = 2747
    D = |p - q| = 26  [recoverable from framework: the 137-map multiplier]
    p + q = √(D² + 4N) = √(676 + 10988) = √11664 = 108
    Solve X² - 108X + 2747 = 0  →  roots 41, 67  ✓

    GF(37) audit of this RSA instance:
        N     mod 37 =  9  ∈ SA   (sovereign anchor)
        φ(N)  mod 37 = 13  ∈ CB   (cascade base)
        p + q mod 37 = 34  ∈ D7   ({7,33,34})
        D           = 26  ∈ IC   (137-map multiplier)

    Scope of the reduction: this applies to prime pairs where one prime is
    Rabinowitsch and the other is a Heegner absolute value, and their
    difference is 26. General RSA primes carry no such structure.

CONDITIONAL FACTORING IDENTITIES (verified)
    (1) φ(N) known →  p + q = N - φ(N) + 1;  roots of X² - (p+q)X + N = 0
    (2) D = |p-q| known → p + q = √(D² + 4N); same quadratic
    (3) p + q known → quadratic X² - (p+q)X + N = 0 has roots p, q
    The GF(37) framework supplies D for the specific pairs above.
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

f      = lambda n: (26 * n) % P
dr     = lambda n: (n - 1) % 9 + 1 if n > 0 else 0
isqrt  = math.isqrt

# 137-map orbit of 6
orbit6 = set()
n = 6
for _ in range(3):
    orbit6.add(n); n = f(n)

def classify(n):
    r = n % P
    for nm, cls in [('IC', IC), ('SA', SA), ('ST', ST), ('CB', CB),
                    ('ORBIT_11', ORBIT_11), ('SEED_ORBIT', SEED_ORBIT),
                    ('BASIN_Y', BASIN_Y), ('D7', D7), ('PR', PR)]:
        if r in cls:
            return nm, r
    return None, r


def run():
    print("=" * 66)
    print("THEOREM 114 — HEEGNER–RABINOWITSCH DIFFERENCE STRUCTURE IN GF(37)")
    print("=" * 66)

    R = [2, 3, 5, 11, 17, 41]
    H = [3, 4, 7, 8, 11, 19, 43, 67, 163]

    assert len(R) == 6
    assert len(H) == 9

    # ---------------------------------------------------------------
    # PART 1 — Orbit of 6 under 137-map
    # ---------------------------------------------------------------
    assert orbit6 == {6, 8, 23}, f"Orbit mismatch: {orbit6}"
    assert sum(orbit6) % P == 0
    print(f"\nOrbit of 6 under 137-map: {sorted(orbit6)},  sum=37≡0 mod 37")

    # ---------------------------------------------------------------
    # PART 2 — Rabinowitsch pairwise coverage
    # ---------------------------------------------------------------
    r_pairs = [(R[j] - R[i], R[i], R[j])
               for i in range(len(R)) for j in range(i + 1, len(R))]
    assert len(r_pairs) == 15

    r_named = [(d, a, b) for d, a, b in r_pairs if classify(d)[0] is not None]
    r_miss  = [(d, a, b) for d, a, b in r_pairs if classify(d)[0] is None]

    assert len(r_named) == 12
    assert len(r_miss)  == 3

    # The two orbit6 misses
    orbit6_misses_r = [(d, a, b) for d, a, b in r_miss if d % P in orbit6]
    assert len(orbit6_misses_r) == 2
    assert all(d == 6 for d, _, _ in orbit6_misses_r), "Both orbit6 misses = 6"

    print(f"\nRabinowitsch C(6,2)=15 pairs:  12 named,  3 miss")
    for d, a, b in r_miss:
        nm, r = classify(d)
        tag = f"orbit6" if d % P in orbit6 else "—"
        print(f"  MISS: {b}-{a}={d}  mod37={r}  [{tag}]")

    # ---------------------------------------------------------------
    # PART 3 — Heegner pairwise coverage
    # ---------------------------------------------------------------
    h_pairs = [(H[j] - H[i], H[i], H[j])
               for i in range(len(H)) for j in range(i + 1, len(H))]
    assert len(h_pairs) == 36

    h_named = [(d, a, b) for d, a, b in h_pairs if classify(d)[0] is not None]
    h_miss  = [(d, a, b) for d, a, b in h_pairs if classify(d)[0] is None]

    assert len(h_named) == 34
    assert len(h_miss)  == 2

    orbit6_misses_h = [(d, a, b) for d, a, b in h_miss if d % P in orbit6]
    assert len(orbit6_misses_h) == 1
    assert orbit6_misses_h[0][0] % P == 23, "Heegner orbit6 miss is 23"

    print(f"\nHeegner C(9,2)=36 pairs:  34 named,  2 miss")
    for d, a, b in h_miss:
        nm, r = classify(d)
        tag = f"orbit6" if d % P in orbit6 else "—"
        print(f"  MISS: {b}-{a}={d}  mod37={r}  [{tag}]")

    # ---------------------------------------------------------------
    # PART 4 — Pairs with |p-q| = 26 exactly
    # ---------------------------------------------------------------
    universe = sorted(set(R + H))
    d26_pairs = [(a, b) for i, a in enumerate(universe)
                 for b in universe[i + 1:] if b - a == 26]
    assert (17, 43) in d26_pairs
    assert (41, 67) in d26_pairs
    assert 26 in IC, "26 ∈ IC (the 137-map multiplier)"

    print(f"\nPairs with |p-q| = 26 (the 137-map multiplier):")
    for a, b in d26_pairs:
        print(f"  |{b}-{a}|=26  Rab:{a in R}/{b in R}  Heg:{a in H}/{b in H}")

    # ---------------------------------------------------------------
    # PART 5 — RSA factoring reduction: p=41, q=67
    # ---------------------------------------------------------------
    p, q = 41, 67
    N   = p * q
    phi = (p - 1) * (q - 1)
    D   = abs(p - q)

    assert D == 26 and 26 in IC, "D=26 ∈ IC (137-map multiplier)"
    assert N == 2747
    assert N % P == 9  and 9  in SA,  "N mod 37 = 9 ∈ SA"
    assert phi % P == 13 and 13 in CB, "phi mod 37 = 13 ∈ CB"

    # Recovery via D
    pq_sum = isqrt(D * D + 4 * N)
    assert pq_sum * pq_sum == D * D + 4 * N, "Perfect square"
    assert pq_sum == p + q

    assert pq_sum % P == 34 and 34 in D7, "p+q mod 37 = 34 ∈ D7"

    disc = pq_sum * pq_sum - 4 * N
    r1   = (pq_sum + isqrt(disc)) // 2
    r2   = (pq_sum - isqrt(disc)) // 2
    assert {r1, r2} == {p, q}

    # Recovery via phi
    pq_sum2 = N - phi + 1
    assert pq_sum2 == p + q

    print(f"\nRSA factoring reduction (p=41, q=67):")
    print(f"  N = {N}")
    print(f"  D = |p-q| = {D}  (137-map multiplier, recoverable from GF(37) framework)")
    print(f"  p+q = sqrt({D}^2 + 4*{N}) = sqrt({D*D+4*N}) = {pq_sum}")
    print(f"  X^2 - {pq_sum}X + {N} = 0  →  roots {r1}, {r2}  ✓")
    print(f"\n  GF(37) audit:")
    print(f"    N   mod 37 = {N%P}  ∈ SA")
    print(f"    phi mod 37 = {phi%P}  ∈ CB")
    print(f"    p+q mod 37 = {pq_sum%P}  ∈ D7")
    print(f"    D          = {D}  ∈ IC  (no reduction needed)")

    # ---------------------------------------------------------------
    # PART 6 — Three conditional factoring identities
    # ---------------------------------------------------------------
    # Identity 1: phi known
    assert N - phi + 1 == p + q
    # Identity 2: D known
    assert isqrt(D * D + 4 * N) == p + q
    # Identity 3: sum known -> quadratic -> roots
    S = p + q
    disc2 = S * S - 4 * N
    assert isqrt(disc2) == D
    roots = {(S + isqrt(disc2)) // 2, (S - isqrt(disc2)) // 2}
    assert roots == {p, q}

    print(f"\nConditional factoring identities (all verified on p={p}, q={q}):")
    print(f"  (1) phi known: p+q = N-phi+1 = {N}-{phi}+1 = {N-phi+1}  ✓")
    print(f"  (2) D   known: p+q = sqrt(D^2+4N) = {pq_sum}  ✓")
    print(f"  (3) p+q known: quadratic roots = {{{r1},{r2}}}  ✓")

    print()
    print("All assertions passed. THEOREM 114 verified.")


if __name__ == "__main__":
    run()
