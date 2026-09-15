# CLASS: THEOREM
"""
Theorem 339: the orbit INDEX -- F_37*/<10> is Z/12, and it explains every
hit and miss in this run
Author: Michael Warren Song (CyclicAmp)

Safe primes and semiprimes, asked together, turn out to need one tool, and
building it retroactively collapses T331 and T332 into arithmetic mod 12.

=== THE INDEX ===

    The twelve orbits are the cosets of H = <10>, so they form a GROUP --
    F_37*/H, cyclic of order 36/3 = 12.  Since 2 is a primitive root, index
    each orbit by the power of 2 that lands in it:

        j   0    1      2   3     4       5    6     7     8  9  10     11
            IC DARK_A  C3 TESLA SA_ST_A SEED NEG_H NQR17 D7 C9 SA_ST_B CAS_EXT

    and then, with zero counterexamples over all 36 x 36 pairs,

        idx(xy) = idx(x) + idx(y)   (mod 12)

    THE ORBIT OF A PRODUCT IS THE SUM OF THE INDICES.  That single line is
    why multiplicative objects can see this structure and additive ones
    cannot -- which is exactly the T336 twin-prime null, restated as a
    reason rather than a measurement.

    GRADE: TIER A, DEFINITIONAL.  This is not a discovery and must not be
    ranked as one.  H is a subgroup of the abelian group F_37*, so F_37*/H
    is a quotient GROUP and the coset map is a homomorphism BY
    CONSTRUCTION; indexing by powers of a primitive root is the discrete
    log, which is the canonical isomorphism F_p*/H = Z/[F_p*:H].  The
    homomorphism IS that isomorphism.  Verified with zero counterexamples
    for p = 13, 37, 41, 61, 101 across subgroups of order 1, 2, 3, 4.
    The 36 x 36 check below confirms that the INDEXING TABLE is correct;
    it is not evidence for a theorem and carries no information about 37.

    The 37-specific content of this thread is not here.  It is in T333:
    that base 10 is admissible because 10 generates IC, the roots of
    Phi_3 mod 37 being exactly 10 and 26.

=== IT COLLAPSES T331 AND T332 ===

    orbit(-1) = NEG_H has index 6, so negation is  j -> j + 6.  T331's six
    dual pairs are just the six pairs {j, j+6}:

        IC 0 <-> NEG_H 6      DARK_A 1 <-> NQR17 7    C3 2 <-> D7 8
        TESLA 3 <-> C9 9      SA_ST_A 4 <-> SA_ST_B 10  SEED 5 <-> CAS_EXT 11

    T332 proved exactly two orbits are inversion-closed by a quotient-group
    argument.  In the index that is the two solutions of 2j == 0 (mod 12):
    j = 0 and j = 6, i.e. IC and NEG_H.  Same fact, now visible.

    T331's 37-half has indices {11, 0, 1, 2, 3, 4} -- a CONTIGUOUS ARC, and
    the 74-half is the opposite arc {5,...,10}.  Graded, not asserted: a
    split must take one of each pair {j, j+6}, giving 2^6 = 64 possibilities,
    of which 12 are arcs.  So p = 12/64 = 3/16, 2.42 bits, n = 1, post hoc.
    Suggestive only -- weaker than the 1-in-6 of T334.

=== SAFE PRIMES: TWO FORCED EXCLUSIONS, THEN A PREDICTED MISS ===

    A safe prime is q = 2p+1 with p prime -- the image of a Sophie Germain
    prime under T337's sigma.  Two residues are forced out:

        q == 1 needs p == 0, i.e. p = 37, and 2(37)+1 = 75 = 3 x 25
        q == 0 needs q = 37 = 2(18)+1, and 18 is composite

    So NO safe prime is 0 or 1 mod 37.  Residue 1 is in IC, so IC carries
    two admissible members instead of three -- the mirror of SEED losing one
    for Sophie Germain primes in T337.  Measured: exactly 0 safe primes at
    residue 1, as forced.

    Beyond that, PREDICTED MISS, and predicted rather than measured: sigma
    is a bijection on residues, so T337's equidistribution transports
    exactly.  Measured chi-square 4.94 on 56,031 safe primes below 2x10^7,
    against 24.72.  MISS.

=== SEMIPRIMES SPLIT INTO A MISS AND A HIT ===

    Squarefree, n = pq with p != q:  idx(n) = idx(p) + idx(q), and a
    convolution of two uniforms on Z/12 is uniform.  PREDICTED MISS.
    Measured chi-square 2.42 over the 12 indices on 206,905 semiprimes
    below 10^6.  MISS.

    Squares, n = p^2:  idx(n) = 2 idx(p), which is ALWAYS EVEN.  So prime
    squares are confined to the six even-index orbits

        IC, C3, SA_ST_A, NEG_H, D7, SA_ST_B

    and never touch the other six.  Measured: 167 of 167 prime squares
    below 10^6, zero odd indices.  A HIT, with no exceptions possible.

    The even-index orbits are exactly the six QR orbits, and all three
    sovereign orbits -- C3, SA_ST_A, SA_ST_B, at indices 2, 4, 10 -- are
    among them, matching the "3 of the 6 QR orbits" note already in
    CLAUDE.md.

=== WHAT THIS THEOREM CONTAINS, GRADED ===

    Ranked by evidential weight, every item is definitional or null:

      1. the index homomorphism      TIER A, definitional (see above)
      2. prime squares 167/167       TIER A, algebraically forced
      3. squarefree semiprimes       predicted null, chi-square 2.42
      4. safe primes                 predicted null, chi-square 4.94
      5. T331/T332 collapse          consequences of 1, not evidence

    So T339 contains NO 37-specific positive result.  Its instrument
    detects known multiplicative structure exactly and finds nothing else.
    That is the honest summary, and it is a stronger statement than a
    ranking that places the homomorphism first as a discovery.

=== GRADING THE HIT HONESTLY ===

    This is TIER A.  "Squares land in squares" holds for every prime
    modulus; nothing here is special to 37.  Its value is diagnostic, not
    evidential: it is the control that shows the index machinery detects
    real structure when real structure exists, which is what makes the
    misses in T336, T337 and above informative rather than merely negative.

    What IS 37-specific is only the labelling -- that the even-index half
    contains all three sovereign orbits.  Since the sovereign orbits were
    identified by containing anchors and targets, and those sets are
    themselves QR-flavoured, this is close to circular and is not counted.

=== FALSIFICATION ===
    idx(xy) != idx(x) + idx(y) for some pair; a prime square at an odd
    index; a safe prime congruent to 0 or 1 mod 37.
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
BY = {r: n for n, o in ORBITS.items() for r in o}
IDX = {BY[pow(2, j, P)]: j for j in range(12)}


def sieve(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b'\0\0'
    for i in range(2, int(n ** .5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return s


def run():
    import math
    from collections import Counter

    # --- the index is a group isomorphism ---
    assert len(IDX) == 12 and sorted(IDX.values()) == list(range(12))
    assert IDX['IC'] == 0 and IDX['NEG_H'] == 6
    for x in range(1, P):
        for y in range(1, P):
            assert (IDX[BY[x]] + IDX[BY[y]]) % 12 == IDX[BY[(x * y) % P]]

    # --- it collapses T331 and T332 ---
    for n, j in IDX.items():
        dual = next(m for m, k in IDX.items() if k == (j + 6) % 12)
        assert {(P - x) % P for x in ORBITS[n]} == set(ORBITS[dual])
    assert [j for j in range(12) if (2 * j) % 12 == 0] == [0, 6]
    inv = {x: pow(x, P - 2, P) for x in range(1, P)}
    closed = sorted(n for n, o in ORBITS.items()
                    if {inv[x] for x in o} == set(o))
    assert closed == ['IC', 'NEG_H']
    h37 = {n for n, o in ORBITS.items() if sum(o) == 37}
    assert sorted(IDX[n] for n in h37) == [0, 1, 2, 3, 4, 11]
    arc = {(11 + k) % 12 for k in range(6)}
    assert {IDX[n] for n in h37} == arc                 # contiguous
    assert abs(math.log2(64 / 12) - 2.415) < 0.01       # the grade

    # --- safe primes: forced exclusions ---
    N = 10 ** 7
    s = sieve(2 * N + 2)
    safe = [2 * p + 1 for p in range(3, N) if s[p] and s[2 * p + 1]]
    n = len(safe)
    assert n == 56031, n
    assert all(q % P not in (0, 1) for q in safe)       # FORCED
    assert 2 * 37 + 1 == 75 == 3 * 25                   # why 1 is impossible
    assert 37 == 2 * 18 + 1 and 18 % 2 == 0             # why 0 is impossible
    w = {o: sum(1 for r in ORBITS[o] if r not in (0, 1)) for o in ORBITS}
    assert w['IC'] == 2 and all(w[o] == 3 for o in ORBITS if o != 'IC')
    c = Counter(BY[q % P] for q in safe)
    tot = sum(w.values())
    chi = sum((c[o] - n * w[o] / tot) ** 2 / (n * w[o] / tot) for o in ORBITS)
    assert chi < 24.72, chi                             # MISS, as predicted

    # --- semiprimes ---
    M = 10 ** 6
    t = sieve(M)
    pr = [p for p in range(2, M) if t[p]]
    sqfree, squares = [], []
    for i, p in enumerate(pr):
        if p * p > M:
            break
        if p != 37:
            squares.append(p * p)
        for q in pr[i + 1:]:
            if p * q > M:
                break
            if p != 37 and q != 37:
                sqfree.append(p * q)
    assert len(sqfree) == 206905 and len(squares) == 167

    cs = Counter(IDX[BY[x % P]] for x in sqfree)
    chi_s = sum((cs[j] - len(sqfree) / 12) ** 2 / (len(sqfree) / 12)
                for j in range(12))
    assert chi_s < 24.72, chi_s                         # MISS, as predicted

    cq = Counter(IDX[BY[x % P]] for x in squares)
    assert all(j % 2 == 0 for j in cq)                  # THE HIT
    assert sorted(cq) == [0, 2, 4, 6, 8, 10]
    assert sum(v for j, v in cq.items() if j % 2) == 0
    for p in pr[:200]:                                  # and it is forced
        if p != 37:
            assert IDX[BY[(p * p) % P]] == (2 * IDX[BY[p % P]]) % 12

    # --- even index == quadratic residue ---
    qr = {(x * x) % P for x in range(1, P)}
    even = {n for n, j in IDX.items() if j % 2 == 0}
    assert all(set(ORBITS[n]) <= qr for n in even)
    assert all(not (set(ORBITS[n]) & qr) for n in ORBITS if n not in even)
    assert {'C3', 'SA_ST_A', 'SA_ST_B'} <= even         # the sovereign three

    print("All assertions passed.\n")
    print("THEOREM 339.  The orbit INDEX: F_37*/<10> = Z/12.\n")
    print("   j   orbit      residues")
    for nm, j in sorted(IDX.items(), key=lambda kv: kv[1]):
        print(f"  {j:2d}   {nm:9s}  {sorted(ORBITS[nm])}")
    print("\n   idx(xy) = idx(x) + idx(y) mod 12   -- 0 counterexamples")
    print("   the orbit of a PRODUCT is the SUM of the indices.  That is why")
    print("   multiplicative objects see this structure and the additive +2")
    print("   twin gap (T336) cannot.\n")
    print("  COLLAPSES T331 AND T332")
    print("   negation is j -> j+6, so T331's dual pairs are {j, j+6}")
    print("   T332's two inversion-closed orbits are the two solutions of")
    print(f"   2j == 0 (mod 12): {[j for j in range(12) if (2*j)%12==0]}"
          f" = IC and NEG_H\n")
    print(f"   T331's 37-half has indices {sorted(IDX[n] for n in h37)} --")
    print(f"   a contiguous arc.  p = 12/64 = 3/16 = {math.log2(64/12):.2f}"
          f" bits, n=1,")
    print( "   post hoc.  Suggestive only; weaker than T334's 1-in-6.\n")
    print("  SAFE PRIMES  q = 2p+1")
    print(f"   {n:,} below {2*N+1:,}")
    print( "   FORCED: no safe prime is 0 or 1 mod 37 (75 = 3x25; 18 even).")
    print( "   residue-1 count measured: 0.  IC carries 2 members, not 3 --")
    print( "   the mirror of SEED losing one in T337.")
    print(f"   chi-square {chi:.2f} vs 24.72  MISS, and PREDICTED: sigma is a")
    print( "   residue bijection, so T337's equidistribution transports.\n")
    print("  SEMIPRIMES SPLIT")
    print(f"   squarefree pq  {len(sqfree):,}   chi-square {chi_s:.2f}  MISS")
    print( "     predicted: idx(pq) = idx(p)+idx(q), convolution of uniforms")
    print(f"   prime squares  {len(squares):,}   indices {sorted(cq)}   HIT")
    print( "     idx(p^2) = 2 idx(p) is always EVEN -- confined to the six")
    print( "     even-index orbits, which are exactly the six QR orbits,")
    print( "     and contain all three sovereign orbits (indices 2, 4, 10).")
    print(f"     odd-index count: 0 of {len(squares)}.  No exception possible.\n")
    print("  GRADING THE HIT: TIER A.  'Squares land in squares' holds for")
    print("  every prime modulus -- nothing here is special to 37.  Its value")
    print("  is diagnostic: it is the control showing the index detects real")
    print("  structure when it exists, which is what makes the misses in")
    print("  T336, T337 and above informative rather than merely negative.")


if __name__ == "__main__":
    run()
