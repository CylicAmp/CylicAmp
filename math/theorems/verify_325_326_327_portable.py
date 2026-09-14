# CLASS: VERIFICATION
"""
Portable verifier for T325 / T326 / T327 -- no imports, no repo, real orbit
names.  Copy this single file anywhere and run it.

    python3 verify_325_326_327_portable.py

Written because an independent check of these three theorems had to stub
orbit_of() as "r{n%37}" for lack of the theorems module.  No stub is needed:
the twelve 137-orbits are 60 lines of arithmetic and are rebuilt below from
the definition rather than pasted, so the names are checked, not trusted.

Every numeric claim in T325, T326 and T327 is re-derived here.  This file is
a CHECK, not a source: if it disagrees with the theorem files, the
disagreement is the finding.
"""

P, MULT = 37, 26                       # 137 mod 37 = 26

# --- the twelve orbits, BUILT from the 137-map, not pasted ----------------
def build_orbits():
    """Orbits of x -> 26x on F_37*.  ord_37(26) = 3, so all are 3-cycles."""
    seen, out = set(), []
    for s in range(1, P):
        if s in seen:
            continue
        o = frozenset((s * MULT ** k) % P for k in range(3))
        seen |= o
        out.append(o)
    return out

NAMES = {                              # the names used throughout the repo
    frozenset({1, 10, 26}): 'IC',        frozenset({2, 15, 20}): 'DARK_A',
    frozenset({3, 4, 30}): 'C3',         frozenset({5, 13, 19}): 'CAS_EXT',
    frozenset({6, 8, 23}): 'TESLA',      frozenset({7, 33, 34}): 'D7',
    frozenset({9, 12, 16}): 'SA_ST_A',   frozenset({11, 27, 36}): 'NEG_H',
    frozenset({14, 29, 31}): 'C9',       frozenset({17, 22, 35}): 'NQR17',
    frozenset({18, 24, 32}): 'SEED',     frozenset({21, 25, 28}): 'SA_ST_B',
}
ORB = build_orbits()
assert pow(MULT, 3, P) == 1 and pow(MULT, 1, P) != 1, "ord_37(26) must be 3"
assert len(ORB) == 12 and all(len(o) == 3 for o in ORB), "twelve 3-cycles"
assert set(ORB) == set(NAMES), "built orbits must equal the named ones"
_BY_R = {r: NAMES[o] for o in ORB for r in o}
ANCHORS, TARGETS = {4, 9, 25, 30}, {3, 12, 21, 30}


def orbit_of(n):
    return _BY_R.get(n % P, 'SEAM')


def is_prime(m):
    return m > 1 and all(m % k for k in range(2, int(m ** .5) + 1))


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def check(label, cond):
    assert cond, "FAILED: " + label
    print(f"  ok  {label}")


# ==========================================================================
def t325():
    print("T325  rotation stack 123 / 312 / 231")
    S = ["123", "312", "231"]

    def latin(g):                      # symbol-set check included
        n = len(g)
        return (len({c for r in g for c in r}) == n
                and all(len(set(r)) == n for r in g)
                and all(len({g[r][c] for r in range(n)}) == n
                        for c in range(n)))

    check("is a Latin square on {1,2,3}", latin(S))
    check("the multiplication table is NOT (six symbols)",
          not latin(["123", "246", "369"]))
    check("every digit on a broken diagonal, +1 per row",
          all(all((r[i + 1].index(d) - r[i].index(d)) % 3 == 1
                  for i in range(2)) for d in "123" for r in [S]))
    # rotation IS the 137-map, over every 3-digit word
    def rotr(n):
        w = f"{n:03d}"
        return int(w[-1] + w[:-1])

    def rotl(n):
        w = f"{n:03d}"
        return int(w[1:] + w[0])
    check("abc -> cab == x26 for all 1000 words",
          all(rotr(n) % P == (MULT * n) % P for n in range(1000)))
    check("abc -> bca == x10 for all 1000 words",
          all(rotl(n) % P == (10 * n) % P for n in range(1000)))
    check("10 = 26^-1 mod 37", (MULT * 10) % P == 1)
    check("rotation class of 123 is exactly SA_ST_A",
          {int(r) % P for r in S} == {9, 12, 16}
          and orbit_of(123) == 'SA_ST_A')
    check("reversal class is exactly SA_ST_B",
          {int(r[::-1]) % P for r in S} == {21, 25, 28})
    check("SA_ST_A has anchor 9 / target 12; SA_ST_B has 25 / 21",
          {9, 12, 16} & ANCHORS == {9} and {9, 12, 16} & TARGETS == {12}
          and {21, 25, 28} & ANCHORS == {25}
          and {21, 25, 28} & TARGETS == {21})
    check("full rotation sums to the SEAM for every 3-digit word",
          all((n + rotr(n) + rotr(rotr(n))) % P == 0 for n in range(100, 1000))
          and 111 == 3 * P)
    # chevron and mirror arm are column reflections, not list reverses
    chev, xarm = ["231", "312", "123", "312", "231"], \
                 ["123", "312", "231", "312", "123"]
    tc = [r.index("1") for r in chev]
    tx = [r.index("1") for r in xarm]
    check("chevron / mirror arm: c -> 2-c, and each is its own reverse",
          tx == [2 - v for v in tc] and chev[::-1] == chev
          and xarm[::-1] == xarm and xarm != chev)
    check("marked rows 3,5,7: (3,5) and (5,7) twin pairs sharing 5",
          all(is_prime(v) for v in (3, 5, 7)) and is_prime(3) and is_prime(5)
          and is_prime(7))
    check("3,5 Sophie Germain (7,11); 7 is not (15); 3 -> 7 is a marked row",
          is_prime(2 * 3 + 1) and is_prime(2 * 5 + 1)
          and not is_prime(2 * 7 + 1) and 2 * 3 + 1 == 7)


def t326():
    print("\nT326  AP triples: residue = 12 x step")
    APS = [(a, d, int(f"{a}{a+d}{a+2*d}"))
           for d in range(10) for a in range(1, 10)
           if a + d <= 9 and a + 2 * d <= 9]
    check("25 AP triples with digits 0-9", len(APS) == 25)
    check("n = 111a + 12d for every one",
          all(n == 111 * a + 12 * d for a, d, n in APS))
    check("residue is 12d, start digit invisible (111 = 3 x 37)",
          all(n % P == (12 * d) % P for a, d, n in APS) and 111 == 3 * P)
    check("the seven ascending roads are ONE POINT, 12",
          {int(f"{a}{a+1}{a+2}") % P for a in range(1, 8)} == {12}
          and 12 in TARGETS)
    by_d = {}
    for a, d, n in APS:
        by_d.setdefault(d, set()).add(n % P)
    check("d -> residue: 0/12/24/36/11",
          by_d == {0: {0}, 1: {12}, 2: {24}, 3: {36}, 4: {11}})
    for d, r in ((0, 0), (1, 12), (2, 24), (3, 36), (4, 11)):
        print(f"       d={d}  asc {r:2d} {orbit_of(r):8s}"
              f"   desc {(25*d)%P:2d} {orbit_of(25*d)}")
    check("reversal is negation; 12 + 25 = 37; abc+cba = 222b = 6x37xb",
          all((n + int(f"{a+2*d}{a+d}{a}")) % P == 0 for a, d, n in APS)
          and 12 + 25 == P and 222 == 6 * P)
    check("descending d=3,4 land on 1 and 26 = 137 mod 37, both IC",
          orbit_of(25 * 3) == orbit_of(25 * 4) == 'IC'
          and (25 * 4) % P == 137 % P)
    check("every AP triple has DR in the trinity {3,6,9}",
          {dr(n) for _, _, n in APS} <= {3, 6, 9})
    check("246 is the d=2 road; 24 = 12x2; DR 3; both T316 conditions",
          (2, 2, 246) in APS and 246 % P == 24 and dr(246) == 3
          and orbit_of(246) == 'SEED' and 333 == 9 * P)
    check("d=2 class is 135,246,357,468,579, all == 24",
          [n for _, d, n in APS if d == 2] == [135, 246, 357, 468, 579]
          and {n % P for _, d, n in APS if d == 2} == {24})
    check("rotation-class sums are 333(a+d), 333 = 9 x 37",
          all(sum(int(f"{n:03d}"[k:] + f"{n:03d}"[:k]) for k in (0, 2, 1))
              == 333 * (a + d) for a, d, n in APS))
    check("wrap-around roads are not APs: 891 == 3 in C3, 912 == 24 in SEED",
          891 % P == 3 and orbit_of(891) == 'C3' and 3 in TARGETS
          and 912 % P == 24 and orbit_of(912) == 'SEED'
          and 891 not in [n for _, _, n in APS]
          and 912 not in [n for _, _, n in APS])
    check("only primes among {0,1,11,12,13,24,25,26,36} are 11,13, a twin pair",
          {v for v in (0, 1, 11, 12, 13, 24, 25, 26, 36) if is_prime(v)}
          == {11, 13} and is_prime(2 * 11 + 1) and not is_prime(2 * 13 + 1)
          and is_prime((11 - 1) // 2))


def t327():
    print("\nT327  counting stack 123 / 246 / 369")
    STACK = [123 * k for k in (1, 2, 3)]
    grid = [[i * j for j in (1, 2, 3)] for i in (1, 2, 3)]
    check("stack is 123,246,369 with digits d,2d,3d",
          STACK == [123, 246, 369]
          and all(123 * d == int(f"{d}{2*d}{3*d}") for d in (1, 2, 3)))
    check("it is T326's a=d diagonal: 111d + 12d = 123d",
          all(111 * d + 12 * d == 123 * d for d in (1, 2, 3)))
    check("three rows because a=d forces 3d <= 9", 3 * 3 == 9 and 3 * 4 > 9)
    check("d=4 breaks the digit AP (492 = 4,9,2) but not the law (== 11)",
          123 * 4 == 492 and [int(c) for c in "492"] != [4, 8, 12]
          and 492 % P == (12 * 4) % P == 11)
    for d in (1, 2, 3):
        print(f"       123 x {d} = {123*d}  == {123*d%P:2d} = 12x{d}"
              f"   {orbit_of(123*d)}")
    check("three rows, THREE orbits (T325's three sat in one)",
          len({orbit_of(n) for n in STACK}) == 3
          and len({orbit_of(int(r)) for r in ("123", "312", "231")}) == 1)
    check("369 == 36 == -1 mod 37", 369 % P == P - 1)
    check("123 + 246 = 369 -- row3 = row1 + row2, a two-term Lucas step",
          123 + 246 == 369 and (12 + 24) % P == 36)
    check("stack sum 738 == 35 in NQR17, and does NOT vanish "
          "(6 x 123 has no factor 37)",
          sum(STACK) == 738 and 738 % P == 35
          and orbit_of(738) == 'NQR17' and 6 * 123 == 738)
    check("grid symmetric; row sums 6,12,18 -> TESLA, SA_ST_A, SEED",
          all(grid[i][j] == grid[j][i] for i in range(3) for j in range(3))
          and [sum(r) for r in grid] == [6, 12, 18]
          and [orbit_of(s) for s in (6, 12, 18)]
          == ['TESLA', 'SA_ST_A', 'SEED'])
    check("grand total (1+2+3)^2 = 36 == -1",
          sum(map(sum, grid)) == 36 == (1 + 2 + 3) ** 2
          and 36 % P == P - 1)
    main = int("".join(str(grid[i][i]) for i in range(3)))
    anti = int("".join(str(grid[i][2 - i]) for i in range(3)))
    check("main 149 == 1 (148 = 4x37); anti 343 = 7^3 == 10 (333 = 9x37)",
          main == 149 and anti == 343 == 7 ** 3
          and main % P == 1 and 148 == 4 * P
          and anti % P == 10 and 333 == 9 * P)
    check("both diagonals in IC; product == 10, stays in IC",
          orbit_of(main) == orbit_of(anti) == 'IC'
          and (main * anti) % P == 10 and orbit_of(main * anti) == 'IC')
    check("diagonals plus 137 fill IC = {1,10,26} exactly",
          {main % P, anti % P, 137 % P} == {1, 10, 26})
    check("149 prime, (149,151) twin, 151 == 3 in C3 (a target)",
          is_prime(149) and is_prime(151) and 151 % P == 3
          and orbit_of(151) == 'C3' and 3 in TARGETS)
    road = [(123 * k) % P for k in range(1, P + 1)]
    check("123k sweeps all 37 residues once; seam only at k=37",
          sorted(road) == list(range(P)) and road.index(0) == P - 1
          and 123 * 37 == 4551 == 3 * 37 * 41)


if __name__ == "__main__":
    print(f"orbits rebuilt from x -> {MULT}x on F_{P}*, "
          f"{len(ORB)} of them, names verified against the build\n")
    t325()
    t326()
    t327()
    print("\nAll checks passed.  No imports, no repo, real orbit names.")
