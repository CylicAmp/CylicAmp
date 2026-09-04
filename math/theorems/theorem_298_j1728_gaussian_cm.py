"""
T298 — j=1728 over F_37: Gaussian CM, and a Clean Case of the T297 Seam

The j=0 family (T288-T295) has Eisenstein CM: End = Z[omega], disc -3, six
units, six traces, sextic twists. The j=1728 family is its Gaussian partner:
End = Z[i], disc -4, four units, four traces, quartic twists.

════════════════════════════════════════════════════════════════════════════
THE FAMILY
════════════════════════════════════════════════════════════════════════════
    E_a : y^2 = x^3 + a x,   a != 0,   j = 1728,   Aut(E_a) = mu_4

    E_a ≅ E_a'  over K  iff  a'/a in (K*)^4.

TWIST CLASS COUNT — the number of classes is the INDEX, not the subgroup order:

    #classes = |F_p* / (F_p*)^4| = gcd(4, p-1)
    class size = (p-1)/gcd(4, p-1)

At p=37: gcd(4,36) = 4 classes of 9 elements each.
(Not 9 classes of 4. Compare j=0: gcd(6,36) = 6 classes of 6, per T288/T294.)

Verified by direct enumeration:
    a in {1,7,9,10,12,16,26,33,34}    #E=36   t= +2
    a in {2,14,15,18,20,24,29,31,32}  #E=50   t=-12
    a in {3,4,11,21,25,27,28,30,36}   #E=40   t= -2
    a in {5,6,8,13,17,19,22,23,35}    #E=26   t=+12

Four classes, four traces, and the correspondence is a BIJECTION — unlike
j=0 at p=37, where six classes carried six traces but each trace covered a
whole antipodal orbit pair (T288).

════════════════════════════════════════════════════════════════════════════
THE CM INPUT
════════════════════════════════════════════════════════════════════════════
p > 2 splits in Q(i) iff p = 1 (mod 4). Then p = L^2 + M^2 = pi*conj(pi),
and the four associates +-pi, +-i*pi give traces +-2L, +-2M.

    37 = 1^2 + 6^2   ->   traces {+-2, +-12}
    #E = 38 - t   ->   {26, 36, 40, 50}
    Hasse: 2*sqrt(37) = 12.166..., so |t| = 12 sits just inside the bound.
    Equivalently 4p = t^2 + 4s^2:  148 = 2^2+4*36 = 12^2+4*1.

If p = 3 (mod 4), p stays inert in Z[i], the curve is supersingular, t = 0,
#E = p+1. Verified at p = 7, 11, 19, 23.

Across the framework's admissible set (T292):
    p= 7 (3 mod 4)  SUPERSINGULAR   t = 0
    p=37 (1 mod 4)  ordinary        37 = 1^2+6^2   t in {+-2, +-12}
    p=73 (1 mod 4)  ordinary        73 = 3^2+8^2   t in {+-6, +-16}

The switch is the splitting law in Q(i), exactly the job Q(sqrt(-3)) did for
j=0. Z/36Z does not produce 37 = 1^2 + 6^2.

════════════════════════════════════════════════════════════════════════════
A CLEAN CASE OF THE T297 SEAM
════════════════════════════════════════════════════════════════════════════
The order-4 endomorphism is  phi(x,y) = (-x, i*y)  with i^2 = -1.
At p=37, sqrt(-1) = 6 or 31. Those sit in TESLA and C9.

Which Z/12Z classes CAN contain a square root of -1 is BLOCK 1:
    -1 = 36 has class 6.  x^2 = -1  =>  2*class(x) = 6 (mod 12)
    =>  class(x) in {3, 9}  =  TESLA and C9.
Pure Z/12Z arithmetic. This is also exactly the "imaginary unit orbit"
property T285 recorded for TESLA and C9.

That those same elements furnish an ORDER-4 CURVE ENDOMORPHISM is BLOCK 2.
Nothing in Z/12Z says a group element of order 4 acts on a curve.

So the two blocks touch here without either being a corollary of the other:
block 1 says WHERE sqrt(-1) lives; block 2 says WHAT it does to a curve.

════════════════════════════════════════════════════════════════════════════
SIDE BY SIDE
                          j = 0                    j = 1728
    model            y^2 = x^3 + a            y^2 = x^3 + a x
    End              Z[omega]                 Z[i]
    discriminant     -3                       -4
    Aut              mu_6                     mu_4
    twists           a'/a in (K*)^6           a'/a in (K*)^4
    #classes at 37   gcd(6,36) = 6            gcd(4,36) = 4
    ordinary when    p = 1 mod 3              p = 1 mod 4
    norm identity    4p = L^2 + 27M^2         p = L^2 + M^2
    traces at p=37   {+-1, +-10, +-11}        {+-2, +-12}
    anomalous?       yes, t=1 (T288/T293)     no, t=1 not attainable
    GLV uses         beta, cube root of 1     i, square root of -1
════════════════════════════════════════════════════════════════════════════
"""

from math import gcd, isqrt

P = 37
ORBITS = {
    'IC': {1, 10, 26}, 'DARK_A': {2, 15, 20}, 'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23}, 'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36}, 'C9': {14, 29, 31},
    'NQR17': {17, 22, 35}, 'SEED': {18, 24, 32}, 'SA_ST_B': {21, 25, 28},
}
DLOG = {pow(2, k, 37): k for k in range(36)}


def orb(x):
    for n, s in ORBITS.items():
        if x % 37 in s:
            return n
    return 'SEAM'


def count_points(a, p):
    """#E for y^2 = x^3 + a x over F_p, including the point at infinity."""
    n = 1
    for x in range(p):
        r = (x ** 3 + a * x) % p
        for y in range(p):
            if (y * y) % p == r:
                n += 1
    return n


def twist_classes(p):
    fourth = {pow(x, 4, p) for x in range(1, p)}
    cls, cov = [], set()
    for a in range(1, p):
        if a in cov:
            continue
        c = frozenset({(a * f) % p for f in fourth})
        cls.append(c)
        cov |= c
    return sorted(cls, key=min), fourth


def gaussian_rep(p):
    for L in range(1, isqrt(p) + 1):
        M2 = p - L * L
        M = isqrt(M2)
        if M * M == M2:
            return L, M
    return None


# ─── Part 1: class count is the index ───────────────────────────────────────

def verify_class_count():
    cls, fourth = twist_classes(P)
    assert len(fourth) == (P - 1) // gcd(4, P - 1) == 9
    assert len(cls) == gcd(4, P - 1) == 4, f"got {len(cls)} classes"
    assert all(len(c) == 9 for c in cls)
    # bijection classes <-> traces
    tr = {}
    for c in cls:
        ts = {P + 1 - count_points(a, P) for a in c}
        assert len(ts) == 1, f"class {sorted(c)} has traces {ts}"
        t = ts.pop()
        assert t not in tr, "two classes share a trace"
        tr[t] = sorted(c)
    assert len(tr) == 4
    return cls, tr


# ─── Part 2: CM prediction ──────────────────────────────────────────────────

def verify_cm():
    L, M = gaussian_rep(P)
    assert (L, M) == (1, 6), f"37 = {L}^2+{M}^2"
    pred = sorted({2 * L, -2 * L, 2 * M, -2 * M})
    obs = sorted({P + 1 - count_points(a, P) for a in range(1, P)})
    assert pred == obs == [-12, -2, 2, 12]
    assert max(abs(t) for t in obs) < 2 * P ** 0.5     # Hasse
    for t in obs:                                       # 4p = t^2+4s^2
        s2 = (4 * P - t * t)
        assert s2 % 4 == 0 and isqrt(s2 // 4) ** 2 == s2 // 4
    return L, M, obs


def verify_supersingular():
    out = {}
    for q in (7, 11, 19, 23):
        ts = {q + 1 - count_points(a, q) for a in range(1, q)}
        assert ts == {0}, f"p={q}: traces {ts}"
        out[q] = sorted(ts)
    return out


# ─── Part 3: the seam ───────────────────────────────────────────────────────

def verify_seam():
    roots = [x for x in range(1, P) if (x * x) % P == P - 1]
    assert sorted(roots) == [6, 31]
    assert {orb(x) for x in roots} == {'TESLA', 'C9'}
    # BLOCK 1: which Z/12Z classes can hold sqrt(-1)
    cls_of_neg1 = DLOG[36] % 12
    assert cls_of_neg1 == 6
    solutions = [m for m in range(12) if (2 * m) % 12 == cls_of_neg1]
    assert solutions == [3, 9]
    assert [DLOG[x] % 12 for x in sorted(roots)] == [3, 9]
    # BLOCK 2: the endomorphism actually works
    a, i = 1, 6
    for x in range(P):
        r = (x ** 3 + a * x) % P
        for y in range(P):
            if (y * y) % P == r:
                assert ((i * y) % P) ** 2 % P == ((-x) ** 3 + a * (-x)) % P
    return roots, solutions


def run():
    print("=" * 76)
    print("T298 — j=1728 over F_37: Gaussian CM and the T297 Seam")
    print("=" * 76)

    cls, tr = verify_class_count()
    print("\n--- Part 1: twist classes = INDEX gcd(4,p-1), not subgroup order ---")
    print(f"  |(F_37*)^4| = (p-1)/gcd(4,p-1) = 36/4 = 9   <- subgroup size")
    print(f"  #classes    = gcd(4,p-1)       = 4          <- what we want")
    print("  4 classes of 9, not 9 classes of 4.")
    print("  (j=0 comparison: gcd(6,36) = 6 classes of 6, per T288/T294)")
    print(f"\n  {'trace':>6}  {'#E':>4}  class")
    for t in sorted(tr):
        print(f"  {t:>+6}  {38-t:>4}  {tr[t]}")
    print("  4 classes <-> 4 traces is a BIJECTION.")

    L, M, obs = verify_cm()
    print("\n--- Part 2: Gaussian CM input ---")
    print(f"  37 = {L}^2 + {M}^2  ->  traces +-2*{L}, +-2*{M} = {obs}")
    print(f"  #E = 38 - t = {sorted(38-t for t in obs)}")
    print(f"  Hasse 2*sqrt(37) = {2*P**0.5:.3f}; |t|=12 sits just inside")
    print(f"  4p = t^2+4s^2:  148 = 2^2+4*6^2 = 12^2+4*1^2")
    ss = verify_supersingular()
    print(f"  p = 3 mod 4 -> inert in Z[i] -> supersingular, t=0: {ss}")
    print("\n  Across the admissible set (T292):")
    for p in (7, 37, 73):
        r = gaussian_rep(p)
        ts = sorted({p + 1 - count_points(a, p) for a in range(1, p)})
        kind = "ordinary" if p % 4 == 1 else "SUPERSINGULAR"
        extra = f"  {p} = {r[0]}^2+{r[1]}^2" if r else ""
        print(f"    p={p:3d} ({p%4} mod 4, {kind:13s}) traces={ts}{extra}")

    roots, solutions = verify_seam()
    print("\n--- Part 3: a clean case of the T297 seam ---")
    print(f"  endomorphism phi(x,y) = (-x, i*y),  i^2 = -1")
    print(f"  sqrt(-1) mod 37 = {roots}  ->  orbits {[orb(x) for x in roots]}")
    print("\n  BLOCK 1 (pure Z/12Z) — where sqrt(-1) CAN live:")
    print(f"    -1 = 36 has class {DLOG[36]%12}")
    print(f"    x^2 = -1  =>  2*class(x) = 6 (mod 12)  =>  class in {solutions}")
    print(f"    class 3 = TESLA, class 9 = C9 — T285's imaginary unit orbits")
    print("\n  BLOCK 2 — what those elements DO:")
    print("    (x,y) -> (-x, 6y) is an order-4 automorphism of y^2 = x^3+x.")
    print("    Verified on every point. Nothing in Z/12Z implies this.")
    print("\n  The blocks touch without either being a corollary of the other:")
    print("  block 1 says WHERE sqrt(-1) lives; block 2 says WHAT it does.")

    print("\n" + "=" * 76)
    print(f"  {'':16} {'j = 0':<26} j = 1728")
    for lab, a, b in (
        ('model', 'y^2 = x^3 + a', 'y^2 = x^3 + a x'),
        ('End', 'Z[omega]', 'Z[i]'),
        ('discriminant', '-3', '-4'),
        ('Aut', 'mu_6', 'mu_4'),
        ('#classes at 37', 'gcd(6,36) = 6', 'gcd(4,36) = 4'),
        ('ordinary when', 'p = 1 mod 3', 'p = 1 mod 4'),
        ('norm identity', '4p = L^2 + 27M^2', 'p = L^2 + M^2'),
        ('traces at p=37', '{+-1, +-10, +-11}', '{+-2, +-12}'),
        ('anomalous?', 'yes, t=1', 'no, t=1 unattainable'),
        ('GLV uses', 'beta, cube root of 1', 'i, square root of -1'),
    ):
        print(f"  {lab:16} {a:<26} {b}")
    print("=" * 76)
    print("\nAll T298 assertions passed.")


if __name__ == '__main__':
    run()
