# CLASS: THEOREM
"""
T_33 is constant on mu_3-cosets, and its 6-cycle is a transversal of six named orbits
Author: Michael Warren Song (CyclicAmp)

THEOREM (T_33 is a class function on the 12 named orbits)
    mu_3 = {1,10,26} = ker(x -> x^3). For any x in F_37* and m in mu_3,
    (xm)^3 = x^3 m^3 = x^3 (since m^3=1). So x^3, hence T_33(x)=x^3+33,
    depends only on the coset x*mu_3 -- exactly the 12 named orbits of
    this repository (they are the cosets of mu_3, since 26 generates
    mu_3 and the 137-map is x -> 26x). T_33 collapses each 3-element
    orbit to a single value. Verified for all 12 orbits, no exceptions.

THEOREM (the 6-cycle is a transversal of six named orbits)
    C_6 = (6 -> 27 -> 32 -> 19 -> 10 -> 34 -> 6), T_33's unique cycle
    (cubic_shift_33_gf37.py), contains exactly one element from each of
    six named orbits:
        6  in TESLA     27 in NEG_H     32 in SEED
        10 in IC        19 in CAS_EXT   34 in D7
    The other six orbits (DARK_A, C3, SA_ST_A, C9, NQR17, SA_ST_B) contain
    no cycle element.

CONSEQUENCE (transient is NOT orbit-constant on the six touching orbits)
    "Transient" = steps to reach C_6. Because T_33 is orbit-constant, all
    three elements of an orbit share the same image after one step. But
    an orbit that itself contains a cycle element has one member with
    transient 0 (the cycle element) and two members with transient 1
    (one step to the shared image, which is a cycle node) -- transient
    set {0,1}, not a single value.
    The six non-touching orbits have no such ambiguity: each has a
    single, well-defined transient in {2,3,4}.
    This is a correction to a proposed geometric layout that assumed
    transient was orbit-constant like T_33 is; it is not, on exactly
    the six orbits that intersect C_6.

TRANSIENT DISTRIBUTION (all 36 nonzero elements)
    {0: 6, 1: 12, 2: 6, 3: 6, 4: 6}   sums to 36, max transient 4,
    all five bands (0..4) populated -- confirms cubic_shift_33_gf37.py's
    exhaustive max-4 result from the orbit-level view.

FALSIFICATION
    Any assert below failing.
"""

P = 37
MU3 = frozenset({1, 10, 26})
CYCLE = [6, 27, 32, 19, 10, 34]

NAMED_ORBITS = {
    'IC': {1, 10, 26}, 'DARK_A': {2, 15, 20}, 'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23}, 'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36}, 'C9': {14, 29, 31},
    'NQR17': {17, 22, 35}, 'SEED': {18, 24, 32}, 'SA_ST_B': {21, 25, 28},
}


def cube(x):
    return pow(x, 3, P)


def T33(x):
    return (cube(x) + 33) % P


def transient(x):
    k = 0
    while x not in CYCLE:
        x = T33(x)
        k += 1
    return k


def cosets_of_mu3():
    seen, out = set(), []
    for x in range(1, P):
        if x in seen:
            continue
        c = sorted({(x * m) % P for m in MU3})
        out.append(c)
        seen.update(c)
    return out


def run():
    cosets = cosets_of_mu3()
    assert len(cosets) == 12
    assert sorted(map(sorted, cosets)) == sorted(map(sorted, NAMED_ORBITS.values()))

    # T_33 constant on every coset
    for c in cosets:
        assert len({T33(x) for x in c}) == 1
        assert len({cube(x) for x in c}) == 1

    # cycle touches exactly these six orbits, one element each
    touching = {name for c in CYCLE for name, s in NAMED_ORBITS.items() if c in s}
    assert touching == {'TESLA', 'NEG_H', 'SEED', 'CAS_EXT', 'IC', 'D7'}
    non_touching = set(NAMED_ORBITS) - touching
    assert non_touching == {'DARK_A', 'C3', 'SA_ST_A', 'C9', 'NQR17', 'SA_ST_B'}

    # transient ambiguity exactly on the touching orbits
    for name, s in NAMED_ORBITS.items():
        ts = {transient(x) for x in s}
        if name in touching:
            assert ts == {0, 1}, (name, ts)
        else:
            assert len(ts) == 1, (name, ts)

    # full distribution
    from collections import Counter
    dist = Counter(transient(x) for x in range(1, P))
    assert dict(dist) == {0: 6, 1: 12, 2: 6, 3: 6, 4: 6}
    assert max(dist) == 4
    assert set(dist) == {0, 1, 2, 3, 4}

    print("All assertions passed.\n")
    print("T_33 value and transient per named orbit:")
    for name, s in sorted(NAMED_ORBITS.items()):
        el = sorted(s)
        v = T33(el[0])
        ts = sorted({transient(x) for x in s})
        flag = "  <- touches C_6" if name in touching else ""
        print(f"  {name:<9} {el}  T_33={v:2d}  transient={ts}{flag}")
    print()
    print(f"C_6 = {CYCLE}")
    print(f"touching orbits (one cycle element each): {sorted(touching)}")
    print(f"non-touching orbits: {sorted(non_touching)}")
    print()
    print(f"transient distribution over all 36 nonzero elements: {dict(sorted(dist.items()))}")


if __name__ == "__main__":
    run()
