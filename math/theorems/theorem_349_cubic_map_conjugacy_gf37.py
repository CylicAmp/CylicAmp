# CLASS: THEOREM
"""
Theorem 349: T(x) = x^3+33 has the twelve named orbits as its fibres, and
its 6-cycle is a cycle of orbits -- confirming a supplied conjugacy analysis
in full
Author: Michael Warren Song (CyclicAmp)

An analysis distinguishing three things that get conflated -- the cubic
POLYNOMIAL, the CYCLE TYPE of the map, and the CONJUGACY CLASS in
Maps(F_37) -- was supplied and is correct throughout.  Everything in it is
reproduced here, and two facts it does not name are added.

=== EVERY SUPPLIED CLAIM, VERIFIED ===

    T   = x^3 + 33                        poly (1, 0, 0, 33)
    CTC = C o T o C^-1                    poly (33, 12, 25, 30)
    f_a = T o C                           poly (27, 27, 9, 34)
    f_b = C o T                           poly (3, 0, 0, 26)

    map    image chain           cycles          basins      max tail
    T      13 10  8  6           one 6-cycle     37          4
    CTC    13 10  8  6           one 6-cycle     37          4
    f_a    13  9  6  5  4        3-cycle + fix   31 + 6      5
    f_b    13  9  6  5  4        3-cycle + fix   31 + 6      5

    All exact, including the 31 + 6 basin split and the tail bounds.

    THE SEPARATION IS RIGHT.  f_b = C o T is serial composition with no
    C^-1, so it is not similar to T; it IS similar to f_a, and the witness
    is C itself: C o f_a o C^-1 = C o (T o C) o C^-1 = C o T = f_b, checked
    pointwise over all 37.  T and f_a cannot be conjugate by ANY bijection
    because their cycle types differ (6 against 1+3), and cycle type is a
    conjugacy invariant.  Two classes: {T, CTC} and {f_a, f_b}.

=== NOT NAMED IN THE ANALYSIS (1): THE FIBRES ARE THE ORBITS ===

    The analysis says "every other triple fibre of T is a multiplicative
    coset of that subgroup."  True, and those cosets have a name here.

        x^3 = y^3  <=>  x/y is a cube root of 1  <=>  x/y in <10> = IC

    so the fibres of x -> x^3 are the cosets of <10> -- which are exactly
    the twelve 137-orbits the whole corpus is built on.  Verified: every
    one of the twelve nonzero fibres of T equals a named orbit, on the nose.

        T(x) =  2  <-  {14,29,31}  C9
        T(x) =  4  <-  { 2,15,20}  DARK_A
        T(x) =  6  <-  { 7,33,34}  D7
        T(x) =  7  <-  {21,25,28}  SA_ST_B      ... twelve in all

    And the image size 13 is forced, not observed: (p-1)/3 cubes plus zero
    = 12 + 1.  The first collapse in the chain is the index of the cube
    subgroup.

=== NOT NAMED IN THE ANALYSIS (2): THE HEXAGON IS ON THE QUOTIENT ===

    T sends an entire orbit to a single point, so a 6-cycle of points is a
    6-cycle of ORBITS.  The cycle is

        6 -> 27 -> 32 -> 19 -> 10 -> 34 -> 6

    and its orbits are

        TESLA -> NEG_H -> SEED -> CAS_EXT -> IC -> D7 -> TESLA
        idx 3      6       5       11       0     8

    six DISTINCT orbits of the twelve, three from each of the 37-sum and
    74-sum halves (T331).  So the "one wheel" is not a wheel in F_37; it is
    a hexagon in the quotient, and the tails of length <= 4 are the
    approach through the collapsing fibres.

=== WHAT ONE-STEP SUMS CANNOT SEE ===

    The analysis's closing point stands and is worth keeping: a one-step
    Weil sum sees the 3-to-1 fold, since that is a statement about the
    fibres.  It does not see which of the two functional-graph types you
    land in after iterating, because that depends on the additive shift
    composed with the fold, not on the fold alone.  T and f_a share the
    fold exactly and differ in graph type.

=== FALSIFICATION ===
    A nonzero fibre of T that is not a named orbit; a conjugacy between T
    and f_a; or an image chain differing from those above.
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

T = lambda x: (pow(x, 3, P) + 33) % P
C = lambda x: (3 * x + 1) % P
Ci = lambda y: ((y - 1) * pow(3, P - 2, P)) % P
FA = lambda x: T(C(x))
FB = lambda x: C(T(x))
CTC = lambda x: C(T(Ci(x)))


def fit_cubic(f):
    for a in range(P):
        for b in range(P):
            for c in range(P):
                d = f(0)
                if all((a * x ** 3 + b * x ** 2 + c * x + d) % P == f(x)
                       for x in range(P)):
                    return (a, b, c, d % P)
    return None


def image_chain(f):
    S, out = set(range(P)), []
    while True:
        S = {f(x) for x in S}
        out.append(len(S))
        if len(out) > 1 and out[-1] == out[-2]:
            return out[:-1]


def graph(f):
    per = set()
    for x in range(P):
        seen, y = {}, x
        i = 0
        while y not in seen:
            seen[y] = i
            y = f(y)
            i += 1
        z, cy = y, [y]
        while f(z) != y:
            z = f(z)
            cy.append(z)
        per |= set(cy)
    lens, done, basins, tails = [], set(), {}, []
    for x in sorted(per):
        if x in done:
            continue
        cy, y = [x], f(x)
        while y != x:
            cy.append(y)
            y = f(y)
        done |= set(cy)
        lens.append(len(cy))
    for x in range(P):
        y, t = x, 0
        while y not in per:
            y = f(y)
            t += 1
        tails.append(t)
        cy, z = [y], f(y)
        while z != y:
            cy.append(z)
            z = f(z)
        basins[frozenset(cy)] = basins.get(frozenset(cy), 0) + 1
    return sorted(lens), sorted(basins.values(), reverse=True), max(tails)


def run():
    # --- polynomials ---
    assert fit_cubic(T) == (1, 0, 0, 33)
    assert fit_cubic(CTC) == (33, 12, 25, 30)
    assert fit_cubic(FA) == (27, 27, 9, 34)
    assert fit_cubic(FB) == (3, 0, 0, 26)

    # --- graphs ---
    assert image_chain(T) == [13, 10, 8, 6] == image_chain(CTC)
    assert image_chain(FA) == [13, 9, 6, 5, 4] == image_chain(FB)
    assert graph(T) == ([6], [37], 4)
    assert graph(CTC) == ([6], [37], 4)
    assert graph(FA) == ([1, 3], [31, 6], 5)
    assert graph(FB) == ([1, 3], [31, 6], 5)

    # --- conjugacy, checked ---
    assert all(C(FA(Ci(x))) == FB(x) for x in range(P))
    assert graph(T)[0] != graph(FA)[0]          # cycle type is an invariant

    # --- fibres ARE the orbits ---
    fib = {}
    for x in range(1, P):
        fib.setdefault(T(x), set()).add(x)
    assert len(fib) == 12
    for v, pre in fib.items():
        assert pre == set(ORBITS[BY[min(pre)]]), (v, pre)
    assert [x for x in range(P) if T(x) == 34] == [1, 10, 26]
    assert (P - 1) // 3 + 1 == 13 == image_chain(T)[0]
    assert {x for x in range(P) if T(x) == T(0)} == {0}

    # --- the 6-cycle is a cycle of orbits ---
    cy = [6]
    while T(cy[-1]) != cy[0]:
        cy.append(T(cy[-1]))
    assert cy == [6, 27, 32, 19, 10, 34]
    names = [BY[x] for x in cy]
    assert names == ['TESLA', 'NEG_H', 'SEED', 'CAS_EXT', 'IC', 'D7']
    assert len(set(names)) == 6
    half37 = {'IC', 'DARK_A', 'C3', 'CAS_EXT', 'TESLA', 'SA_ST_A'}
    assert sum(n in half37 for n in names) == 3      # three from each half

    print("All assertions passed.\n")
    print("THEOREM 349.  The cubic map's fibres are the orbits.\n")
    print("  SUPPLIED ANALYSIS, VERIFIED IN FULL")
    for nm, f in (("T", T), ("C o T o C^-1", CTC),
                  ("f_a = T o C", FA), ("f_b = C o T", FB)):
        L, B, t = graph(f)
        print(f"   {nm:14s} poly {fit_cubic(f)}  image {image_chain(f)}"
              f"  cycles {L}  basins {B}  tail {t}")
    print("\n   C o f_a o C^-1 = f_b, checked pointwise: conjugate.")
    print("   T and f_a have different cycle types, so no bijection")
    print("   conjugates them. Two classes, exactly as stated.\n")
    print("  ADDED (1): THE FIBRES ARE THE TWELVE NAMED ORBITS")
    print("   x^3 = y^3 iff x/y is a cube root of 1 iff x/y in <10> = IC,")
    print("   so the fibres of the cube are the cosets of <10> -- the orbits.")
    print(f"   verified for all {len(fib)} nonzero fibres.")
    for v in sorted(fib)[:4]:
        print(f"     T(x) = {v:2d}  <-  {sorted(fib[v])}  {BY[min(fib[v])]}")
    print(f"   image size 13 is forced: (p-1)/3 + 1 = {(P-1)//3} + 1.\n")
    print("  ADDED (2): THE HEXAGON IS ON THE QUOTIENT")
    print(f"   {' -> '.join(map(str,cy))} -> {cy[0]}")
    print(f"   {' -> '.join(names)} -> {names[0]}")
    print(f"   indices {[IDX[n] for n in names]}")
    print("   six distinct orbits, three from each half of T331's 37/74 split.")
    print("   T collapses a whole orbit to a point, so a 6-cycle of points is")
    print("   a 6-cycle of ORBITS -- the wheel lives in the quotient.")


if __name__ == "__main__":
    run()
