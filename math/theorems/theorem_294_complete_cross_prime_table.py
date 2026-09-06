"""
T294 — Complete Cross-Prime Structural Table for {7, 37, 73}

Full dump of every computed quantity across the complete admissible prime set
(T292). No summarizing. Everything computed is recorded.

════════════════════════════════════════════════════════════════════════════
BASIC DATA
════════════════════════════════════════════════════════════════════════════
    p     mult   p-1        factored   orbits  quotient   4p = L^2+27M^2
    7      4      6         2 x 3         2    Z/2Z       28  = 1^2 + 27*1^2
   37     26     36       2^2 x 3^2      12    Z/12Z      148 = 11^2 + 27*1^2
   73     64     72       2^3 x 3^2      24    Z/24Z      292 = 7^2 + 27*3^2

    traces:  p=7  {+-1, +-4, +-5}
             p=37 {+-1, +-10, +-11}
             p=73 {+-7, +-10, +-17}
    M=1 at p=7 and p=37;  M=3 at p=73.
    -1 is in <mult> at NONE of the three -> antipodal pairing exists at all three.

════════════════════════════════════════════════════════════════════════════
POWER SUBGROUPS
════════════════════════════════════════════════════════════════════════════
    p= 7: squares {1,2,4} (3)   cubes {1,6} (2)     6th {1} (1)
          squares == <mult> exactly. The multiplier orbit IS the QR set.
          6th powers trivial because x^6=1 for all x (Fermat, p-1=6).
    p=37: squares (18)  cubes (12)  6th (6)
          squares    = H_6 = {C3,D7,IC,NEG_H,SA_ST_A,SA_ST_B}
          cubes      = H_4 = {IC,TESLA,NEG_H,C9}
          6th powers = H_2 = {IC,NEG_H} = <11>  (T284 operator group)
          All three power subgroups are T286 lattice subgroups.
    p=73: squares (36)  cubes (24)  6th (12)

════════════════════════════════════════════════════════════════════════════
ISOMORPHISM CLASSES OF y^2=x^3+a  — ALWAYS EXACTLY 6
════════════════════════════════════════════════════════════════════════════
Classes are cosets of the 6th powers. Count = gcd(6,p-1) = 6 at all three.
Class SIZE and orbit content differ:

    p= 7:  6 classes x  1 element  = 0 whole orbits per class (orbits SPLIT)
    p=37:  6 classes x  6 elements = 2 orbits = 1 antipodal pair per class
    p=73:  6 classes x 12 elements = 4 orbits = 2 antipodal pairs per class

p=37 full class table:
    {1,10,11,26,27,36}  = IC + NEG_H          #E=48  t=-10
    {2,15,17,20,22,35}  = DARK_A + NQR17      #E=49  t=-11
    {3,4,7,30,33,34}    = C3 + D7             #E=39  t= -1
    {5,13,18,19,24,32}  = CAS_EXT + SEED      #E=37  t= +1   ANOMALOUS
    {6,8,14,23,29,31}   = TESLA + C9          #E=28  t=+10
    {9,12,16,21,25,28}  = SA_ST_A + SA_ST_B   #E=27  t=+11

p=73 full class table:
    {1,3,8,9,24,27,46,49,64,65,70,72}         #E=84  t=-10
    {2,6,16,18,19,25,48,54,55,57,67,71}       #E=81  t= -7
    {4,12,23,32,35,36,37,38,41,50,61,69}      #E=57  t=+17
    {5,11,15,26,28,33,40,45,47,58,62,68}      #E=91  t=-17
    {7,10,17,21,22,30,43,51,52,56,63,66}      #E=64  t=+10
    {13,14,20,29,31,34,39,42,44,53,59,60}     #E=67  t= +7

p=7 per-element (orbits split, no class contains a whole orbit):
    orbit {1,2,4}: a=1 #E=12 t=-4 | a=2 #E= 9 t=-1 | a=4 #E= 3 t=+5
    orbit {3,5,6}: a=3 #E=13 t=-5 | a=5 #E= 7 t=+1 | a=6 #E= 4 t=+4
    a=5 is the anomalous value (#E=7=p) but it sits alone inside its orbit.

════════════════════════════════════════════════════════════════════════════
TRACE MULTIPLICITY
════════════════════════════════════════════════════════════════════════════
    p= 7: counts vary within orbits — no trace is assignable to an orbit
    p=37: each of the 6 traces covers 2 orbits = 1 antipodal pair
    p=73: each of the 6 traces covers 4 orbits = 2 antipodal pairs

════════════════════════════════════════════════════════════════════════════
ANTIPODAL STRUCTURE
════════════════════════════════════════════════════════════════════════════
    p= 7:  1 antipodal pair.  The TWO orbits are antipodes of each other,
           and they are exactly {QRs} and {NQRs}: {1,2,4} <-> {3,5,6}.
    p=37:  6 antipodal pairs.
    p=73: 12 antipodal pairs.
    Count is always (p-1)/6.

════════════════════════════════════════════════════════════════════════════
ARITHMETIC AMONG THE THREE PRIMES
════════════════════════════════════════════════════════════════════════════
    7 x 37 x 73 = 18907 = 137^2 + 137 + 1     exactly
    137^3 - 1 = 2571352 = 2^3 x 17 x 7 x 37 x 73
    136 = 2^3 x 17    (the order-1 cofactor; 17 appears nowhere else)
    73 = 2*37 - 1
    37 mod 7 = 2      73 mod 37 = 36      73 mod 7 = 3
    In GF(37):  7 in D7,  73 = 36 in NEG_H,  137 = 26 in IC
    orbit counts 2, 12, 24;  ratios 12/2 = 6,  24/12 = 2
    p-1 2-adic valuations: v2(6)=1, v2(36)=2, v2(72)=3   (1,2,3 consecutive)
    p-1 3-adic valuations: v3(6)=1, v3(36)=2, v3(72)=2
"""

from math import gcd, isqrt

ADMISSIBLE = [7, 37, 73]

NAMES_37 = {
    frozenset({1, 10, 26}): 'IC', frozenset({2, 15, 20}): 'DARK_A',
    frozenset({3, 4, 30}): 'C3', frozenset({5, 13, 19}): 'CAS_EXT',
    frozenset({6, 8, 23}): 'TESLA', frozenset({7, 33, 34}): 'D7',
    frozenset({9, 12, 16}): 'SA_ST_A', frozenset({11, 27, 36}): 'NEG_H',
    frozenset({14, 29, 31}): 'C9', frozenset({17, 22, 35}): 'NQR17',
    frozenset({18, 24, 32}): 'SEED', frozenset({21, 25, 28}): 'SA_ST_B',
}


def orbits_of(p):
    m = 137 % p
    seen, out = set(), []
    for x in range(1, p):
        if x in seen:
            continue
        o = frozenset({x, (x * m) % p, (x * m * m) % p})
        seen |= o
        out.append(o)
    return sorted(out, key=lambda s: min(s))


def count_points(a, p):
    n = 1
    for x in range(p):
        r = (x ** 3 + a) % p
        for y in range(p):
            if (y * y) % p == r:
                n += 1
    return n


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def cm(p):
    M = 1
    while 27 * M * M < 4 * p:
        r = 4 * p - 27 * M * M
        s = isqrt(r)
        if s * s == r:
            L = s
            h1, h2 = (L + 9 * M) // 2, (L - 9 * M) // 2
            return L, M, sorted({L, -L, h1, -h1, h2, -h2})
        M += 1


def iso_classes(p):
    sixth = {pow(x, 6, p) for x in range(1, p)}
    cls, cov = [], set()
    for a in range(1, p):
        if a in cov:
            continue
        c = frozenset({(a * s) % p for s in sixth})
        cls.append(c)
        cov |= c
    return sorted(cls, key=lambda s: min(s)), sixth


def antipodal_pairs(p):
    O = orbits_of(p)
    pairs, used = [], set()
    for o in O:
        if o in used:
            continue
        no = frozenset({((p - 1) * e) % p for e in o})
        if no != o:
            pairs.append((o, no))
            used |= {o, no}
    return pairs


# ─── assertions ──────────────────────────────────────────────────────────────

def verify_all():
    assert 7 * 37 * 73 == 18907 == 137 ** 2 + 137 + 1
    assert factor(137 ** 3 - 1) == {2: 3, 17: 1, 7: 1, 37: 1, 73: 1}
    assert 73 == 2 * 37 - 1

    for p in ADMISSIBLE:
        m = 137 % p
        assert pow(m, 3, p) == 1 and m != 1
        O = orbits_of(p)
        assert len(O) == (p - 1) // 3
        assert (p - 1) not in {pow(m, i, p) for i in range(3)}
        assert len(antipodal_pairs(p)) == (p - 1) // 6

        cls, sixth = iso_classes(p)
        assert len(cls) == 6, f"p={p}: {len(cls)} classes"
        assert len(sixth) == (p - 1) // gcd(6, p - 1)

        L, M, tr = cm(p)
        emp = {p + 1 - count_points(a, p) for a in range(1, p)}
        assert emp == set(tr), f"p={p}: {sorted(emp)} != {tr}"

    # p=7 squares == <mult>
    assert {pow(x, 2, 7) for x in range(1, 7)} == {1, 2, 4} == {pow(4, i, 7) for i in range(3)}
    # p=37 power subgroups are T286 subgroups
    sq37 = {pow(x, 2, 37) for x in range(1, 37)}
    cb37 = {pow(x, 3, 37) for x in range(1, 37)}
    s6_37 = {pow(x, 6, 37) for x in range(1, 37)}
    assert {NAMES_37[o] for o in orbits_of(37) if o <= sq37} == \
        {'C3', 'D7', 'IC', 'NEG_H', 'SA_ST_A', 'SA_ST_B'}
    assert {NAMES_37[o] for o in orbits_of(37) if o <= cb37} == \
        {'IC', 'TESLA', 'NEG_H', 'C9'}
    assert {NAMES_37[o] for o in orbits_of(37) if o <= s6_37} == {'IC', 'NEG_H'}


def run():
    verify_all()
    print("=" * 78)
    print("T294 — Complete Cross-Prime Structural Table for {7, 37, 73}")
    print("=" * 78)

    print(f"\n{'p':>4} {'mult':>5} {'p-1':>4} {'factored':>12} {'orbits':>7} "
          f"{'quotient':>9} {'4p = L^2+27M^2':>22}")
    for p in ADMISSIBLE:
        L, M, tr = cm(p)
        f = factor(p - 1)
        fs = ' x '.join(f"{b}^{e}" if e > 1 else str(b) for b, e in sorted(f.items()))
        print(f"{p:>4} {137%p:>5} {p-1:>4} {fs:>12} {(p-1)//3:>7} "
              f"{'Z/'+str((p-1)//3)+'Z':>9} {f'{4*p} = {L}^2+27*{M}^2':>22}")

    print("\nTRACES")
    for p in ADMISSIBLE:
        L, M, tr = cm(p)
        print(f"  p={p:3d}: {tr}   (L={L}, M={M})   1 attainable: {1 in tr}")

    print("\nPOWER SUBGROUPS")
    for p in ADMISSIBLE:
        sq = sorted({pow(x, 2, p) for x in range(1, p)})
        cb = sorted({pow(x, 3, p) for x in range(1, p)})
        s6 = sorted({pow(x, 6, p) for x in range(1, p)})
        om = sorted({pow(137 % p, i, p) for i in range(3)})
        print(f"  p={p:3d}: squares({len(sq):2d}) cubes({len(cb):2d}) "
              f"6th({len(s6):2d})   <mult>={om}")
        if p == 7:
            print(f"        squares={sq} == <mult>  (multiplier orbit IS the QR set)")
            print(f"        6th powers={s6} trivial (x^6=1 for all x)")
        if p == 37:
            O = orbits_of(37)
            print(f"        squares    = H_6 = {sorted(NAMES_37[o] for o in O if o<=set(sq))}")
            print(f"        cubes      = H_4 = {sorted(NAMES_37[o] for o in O if o<=set(cb))}")
            print(f"        6th powers = H_2 = {sorted(NAMES_37[o] for o in O if o<=set(s6))}")

    print("\nISOMORPHISM CLASSES (always 6 = gcd(6,p-1))")
    for p in ADMISSIBLE:
        cls, sixth = iso_classes(p)
        O = orbits_of(p)
        print(f"\n  p={p}: 6 classes x {len(cls[0])} elements")
        for c in cls:
            inside = [sorted(o) for o in O if o <= c]
            E = sorted({count_points(a, p) for a in c})
            t = [p + 1 - e for e in E]
            tag = "  <<ANOMALOUS" if p in E else ""
            nm = ''
            if p == 37:
                nm = ' = ' + ' + '.join(sorted(NAMES_37[o] for o in O if o <= c))
            print(f"    {sorted(c)}{nm}")
            print(f"      {len(inside)} whole orbit(s), #E={E}, t={t}{tag}")

    print("\np=7 PER-ELEMENT (orbits split across classes)")
    for o in orbits_of(7):
        row = ' | '.join(f"a={a} #E={count_points(a,7):2d} t={8-count_points(a,7):+2d}"
                         for a in sorted(o))
        print(f"    orbit {sorted(o)}: {row}")

    print("\nTRACE MULTIPLICITY")
    for p in ADMISSIBLE:
        O = orbits_of(p)
        d = {}
        for o in O:
            cs = {count_points(a, p) for a in o}
            if len(cs) == 1:
                d.setdefault(p + 1 - cs.pop(), []).append(o)
        if d:
            for t in sorted(d):
                print(f"  p={p:3d} t={t:+3d}: {len(d[t])} orbits = "
                      f"{len(d[t])//2} antipodal pair(s)")
        else:
            print(f"  p={p:3d}: counts vary within orbits — no trace per orbit")

    print("\nANTIPODAL PAIRS")
    for p in ADMISSIBLE:
        ap = antipodal_pairs(p)
        print(f"  p={p:3d}: {len(ap)} pairs (= (p-1)/6)")
        if p == 7:
            for a, b in ap:
                print(f"        {sorted(a)} <-> {sorted(b)}  (= QRs <-> NQRs)")

    print("\nARITHMETIC AMONG THE THREE PRIMES")
    print(f"  7 x 37 x 73 = {7*37*73} = 137^2+137+1 = {137**2+137+1}")
    print(f"  137^3 - 1 = {137**3-1} = {factor(137**3-1)}")
    print(f"  136 = {factor(136)}  (order-1 cofactor; 17 appears nowhere else)")
    print(f"  73 = 2*37-1 = {2*37-1}")
    print(f"  37 mod 7 = {37%7}   73 mod 37 = {73%37}   73 mod 7 = {73%7}")
    print(f"  orbit counts 2, 12, 24;  12/2 = 6,  24/12 = 2")
    v2 = lambda n: (n & -n).bit_length() - 1
    print(f"  v2(p-1): {[v2(p-1) for p in ADMISSIBLE]}  (consecutive 1,2,3)")
    v3 = lambda n: next(k for k in range(99) if (n // 3**k) % 3)
    print(f"  v3(p-1): {[v3(p-1) for p in ADMISSIBLE]}")

    print("\nAll T294 assertions passed.")


if __name__ == '__main__':
    run()
