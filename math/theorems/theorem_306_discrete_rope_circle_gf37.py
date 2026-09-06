"""
T306 — The Discrete Rotation Group over F_37 Is F_37* Itself, and Its Order-3
        Subgroup Is IC

Written to replace a false claim: that "an F_37 positional step hits a strict
maximum cycle length of 3 before wrapping." Three is the order of ONE element.
The rotation group has order 36 and its maximum element order is 36.

════════════════════════════════════════════════════════════════════════════
THE OBJECT
════════════════════════════════════════════════════════════════════════════
The norm-1 circle over F_p is

    S(p) = { (a,b) in F_p^2 : a^2 + b^2 = 1 }

with the rotation product (a,b)(c,d) = (ac - bd, ad + bc). At p = 37,

    |S(37)| = 36.

════════════════════════════════════════════════════════════════════════════
IT IS F_37*, NOT SOMETHING NEW
════════════════════════════════════════════════════════════════════════════
37 = 1 (mod 4), so -1 is a quadratic residue and x^2 + 1 splits over F_37:
sqrt(-1) = 6 and 31. Then a^2 + b^2 = (a + bi)(a - bi) factors, and norm 1
says the two factors are inverse. So

    phi(a,b) = a + 6b   is a GROUP ISOMORPHISM  S(37) --> F_37*

Verified: homomorphic on all 36 x 36 pairs, bijective, phi(1,0) = 1.

Consequence — the order histograms are identical, which they must be:

    order    1  2  3  4  6  9 12 18 36
    S(37)    1  1  2  2  2  6  4  6 12
    F_37*    1  1  2  2  2  6  4  6 12

    MAXIMUM ROTATION ORDER = 36. There are 12 generators, e.g. (2,16).
    Achievable cycle lengths are the divisors of 36: 1,2,3,4,6,9,12,18,36.

════════════════════════════════════════════════════════════════════════════
THE ORDER-3 ROTATIONS ARE EXACTLY IC
════════════════════════════════════════════════════════════════════════════
    { r in S(37) : r^3 = 1 } = { (1,0), (18,11), (18,26) }
    phi of those             = { 1, 10, 26 } = IC = mu_3

So the 3-cycle does exist inside the rotation group — it is one subgroup of
order 3 out of a group of order 36, and it is the 137-map orbit of 1. That is
the correct statement. "Maximum cycle length 3" replaces a subgroup with the
whole group.

════════════════════════════════════════════════════════════════════════════
TRANSLATION INVARIANCE IS EXACT HERE, NOT NUMERICAL
════════════════════════════════════════════════════════════════════════════
With R_m = g^m for a generator g, the bilinear form is invariant under a
simultaneous shift:

    <R_m q, R_n k> = <R_(m+t) q, R_(n+t) k>     for all q, k, m, n, t

3000 random cases, zero failures, exact in F_37. The float RoPE trace reports
this same identity as 8.882e-16; over F_37 the residual is 0, because the
group is finite and the arithmetic is exact.

The proof is one line: rotations preserve the form and the group is abelian,
so <R_m q, R_n k> = <q, R_(n-m) k> depends only on n - m.

════════════════════════════════════════════════════════════════════════════
WHAT IS FORCED, AND WHERE IT STOPS
════════════════════════════════════════════════════════════════════════════
TIER A for p = 1 (mod 4), nothing to do with 37:
    |S(p)| = p-1 and S(p) ~ F_p*, because -1 is a QR and x^2+1 splits.
TIER A generally:
    a cyclic group of order n has exactly one subgroup of each order d | n.
    The order-3 subgroup being mu_3 is that fact, not a discovery.
NOT GENERIC — the split depends on p mod 4:
    p = 3 (mod 4) gives |S(p)| = p+1 and S(p) is NOT isomorphic to F_p*.
    p= 5,13,17,29,37,41: |S| = p-1   (1 mod 4, splits)
    p= 7,11,19,23,31,43: |S| = p+1   (3 mod 4, non-split)
This separates the admissible primes of T292:
    p= 7: 3 mod 4, |S| =  8 = p+1   NOT isomorphic to F_7*
    p=37: 1 mod 4, |S| = 36 = p-1   isomorphic
    p=73: 1 mod 4, |S| = 72 = p-1   isomorphic
So {7,37,73} is split by this property, and 7 is the odd one out — a
different reason from the two failures in T293.

════════════════════════════════════════════════════════════════════════════
GRADED UNDER T305
════════════════════════════════════════════════════════════════════════════
Cut 1  STRUCTURAL, not literal. SO(2) over R is compact and connected; S(37)
       is finite cyclic of order 36. They are not the same object.
Cut 2  LEVEL 2 as a correspondence to RoPE: Phi sends a real rotation by
       angle m*w to g^m, and the preserved relation is named — the bilinear
       form is invariant under simultaneous shift. Within F_37 the invariance
       is LEVEL 3: proved above, and checked on 3000 cases.
Cut 3  NATIVE rigor here is a theorem. The identification with RoPE as used
       in transformers is not, and the theorem does not upgrade it. Nothing
       here says a transformer computes anything in F_37.
Cut 4  Not a functor. No categories are named and none are needed.

FALSIFICATION: exhibit an element of S(37) of order greater than 36, or a
pair (q,k) and shift t with <R_m q, R_n k> != <R_(m+t) q, R_(n+t) k>. Either
breaks the file.
"""

from collections import Counter

P = 37
I = 6                      # sqrt(-1) mod 37; the other root is 31


def circle():
    return [(a, b) for a in range(P) for b in range(P) if (a * a + b * b) % P == 1]


def mul(p, q):
    a, b = p
    c, d = q
    return ((a * c - b * d) % P, (a * d + b * c) % P)


def order(g):
    x, n = (1, 0), 0
    while True:
        x = mul(x, g)
        n += 1
        if x == (1, 0):
            return n
        if n > P + 2:
            raise AssertionError(f"order of {g} exceeds {P+2}")


def phi(p):
    a, b = p
    return (a + I * b) % P


def dot(u, v):
    return (u[0] * v[0] + u[1] * v[1]) % P


# ─── Part 1: the circle has p-1 elements because -1 is a QR ─────────────────

def verify_size():
    S = circle()
    assert len(S) == P - 1 == 36
    assert P % 4 == 1
    assert pow(P - 1, (P - 1) // 2, P) == 1              # -1 is a QR
    assert sorted(x for x in range(P) if (x * x) % P == P - 1) == [6, 31]
    assert (I * I) % P == P - 1
    return S


# ─── Part 2: phi is a group isomorphism onto F_37* ─────────────────────────

def verify_isomorphism():
    S = circle()
    for p in S:
        for q in S:
            assert phi(mul(p, q)) == (phi(p) * phi(q)) % P, (p, q)
    assert len({phi(p) for p in S}) == 36
    assert {phi(p) for p in S} == set(range(1, P))
    assert phi((1, 0)) == 1
    return True


# ─── Part 3: identical order histograms; maximum order is 36, not 3 ────────

def verify_orders():
    S = circle()
    hc = Counter(order(p) for p in S)
    hf = Counter(next(k for k in range(1, P) if pow(x, k, P) == 1)
                 for x in range(1, P))
    assert hc == hf, (hc, hf)
    assert max(hc) == 36, "maximum rotation order must be 36"
    assert hc[36] == 12                                   # phi(36) generators
    assert order((2, 16)) == 36
    assert (2 * 2 + 16 * 16) % P == 1                     # (2,16) is on the circle
    divisors = sorted(d for d in range(1, 37) if 36 % d == 0)
    assert sorted(hc) == divisors
    return hc, divisors


# ─── Part 4: the order-3 rotations are IC ──────────────────────────────────

def verify_mu3_is_IC():
    S = circle()
    o3 = [p for p in S if order(p) in (1, 3)]
    assert sorted(o3) == [(1, 0), (18, 11), (18, 26)], o3
    assert sorted(phi(p) for p in o3) == [1, 10, 26]       # IC
    assert {pow(26, k, P) for k in range(3)} == {1, 10, 26}
    return o3


# ─── Part 5: exact translation invariance ──────────────────────────────────

def verify_invariance(trials=3000, seed=37):
    import random
    rnd = random.Random(seed)
    g = (2, 16)
    pw = [(1, 0)]
    for _ in range(35):
        pw.append(mul(pw[-1], g))

    def R(v, n):
        a, b = pw[n % 36]
        x, y = v
        return ((a * x - b * y) % P, (a * y + b * x) % P)

    for _ in range(trials):
        q = (rnd.randrange(P), rnd.randrange(P))
        k = (rnd.randrange(P), rnd.randrange(P))
        m, n, t = (rnd.randrange(36) for _ in range(3))
        assert dot(R(q, m), R(k, n)) == dot(R(q, (m + t) % 36), R(k, (n + t) % 36))
        # and it depends only on the difference
        assert dot(R(q, m), R(k, n)) == dot(q, R(k, (n - m) % 36))
    return trials


# ─── Part 6: p mod 4 decides, and it splits {7, 37, 73} ────────────────────

def verify_p_mod_4():
    rows = []
    for p in (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
        n = sum(1 for a in range(p) for b in range(p) if (a * a + b * b) % p == 1)
        assert n == (p - 1 if p % 4 == 1 else p + 1), (p, n)
        rows.append((p, p % 4, n))
    for p, want in ((7, 8), (37, 36), (73, 72)):
        n = sum(1 for a in range(p) for b in range(p) if (a * a + b * b) % p == 1)
        assert n == want, (p, n)
    return rows


def run():
    print("=" * 76)
    print("T306 — The Discrete Rotation Group over F_37 Is F_37*; Its mu_3 Is IC")
    print("=" * 76)

    S = verify_size()
    print(f"\n--- Part 1: |S(37)| = {len(S)} = p - 1 ---")
    print(f"  37 = 1 mod 4, so -1 is a QR and x^2+1 splits; sqrt(-1) = 6, 31")

    verify_isomorphism()
    print("\n--- Part 2: (a,b) -> a + 6b is an isomorphism onto F_37* ---")
    print("  homomorphic on all 36 x 36 products, bijective, phi(1,0) = 1")
    print("  a^2+b^2 = (a+bi)(a-bi); norm 1 makes the factors inverse")

    hc, divs = verify_orders()
    print("\n--- Part 3: order histograms are identical ---")
    print(f"  {'order':<8}" + "".join(f"{d:>4}" for d in divs))
    print(f"  {'S(37)':<8}" + "".join(f"{hc[d]:>4}" for d in divs))
    print(f"  MAXIMUM ROTATION ORDER = {max(hc)}, with {hc[36]} generators, e.g. (2,16)")
    print("  NOT 3. Three is the order of one subgroup.")

    o3 = verify_mu3_is_IC()
    print("\n--- Part 4: the order-3 rotations are exactly IC ---")
    print(f"  {{r : r^3 = 1}} = {o3}")
    print(f"  phi of those  = {sorted(phi(p) for p in o3)} = IC = mu_3")

    n = verify_invariance()
    print(f"\n--- Part 5: translation invariance, exact ---")
    print(f"  <R_m q, R_n k> = <R_(m+t) q, R_(n+t) k> = <q, R_(n-m) k>")
    print(f"  {n} random cases, zero failures, exact in F_37 (float RoPE: 8.88e-16)")

    rows = verify_p_mod_4()
    print("\n--- Part 6: p mod 4 decides; it splits the admissible primes ---")
    for p, m4, sz in rows:
        print(f"  p={p:>3} ({m4} mod 4): |S| = {sz:>3} = p{'-1, ~ F_p*' if m4==1 else '+1, NOT ~ F_p*'}")
    print("  among {7,37,73}:  7 is 3 mod 4 (|S|=8, non-split);")
    print("                   37 and 73 are 1 mod 4 (|S| = 36, 72, split)")
    print("  A different separation from T293's two failures.")

    print("\n--- graded under T305 ---")
    print("  Cut 1 STRUCTURAL: SO(2)/R is compact connected; S(37) is finite cyclic")
    print("  Cut 2 LEVEL 2 to RoPE (Phi and the preserved relation are named);")
    print("        LEVEL 3 inside F_37 — the invariance is proved")
    print("  Cut 3 native = theorem; the RoPE identification is not upgraded by it")
    print("  Cut 4 not a functor; no categories named or needed")

    print("\nAll T306 assertions passed.")


if __name__ == '__main__':
    run()
