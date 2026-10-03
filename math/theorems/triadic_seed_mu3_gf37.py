# CLASS: COMPUTATION
"""
Breathing triadic seed, indexed by mu_3(GF(37)) rather than by bare k
Author: Michael Warren Song (CyclicAmp)

Fills in the formula a spec left undefined, and indexes the three vertices by
the cube roots of unity IN GF(37) instead of by an abstract 0,1,2.

    P_k(t) = r(t) * ( cos(2*pi*k/3), sin(2*pi*k/3), 0 )
    r(t)   = 1 + A * sin(omega*t) * exp(-tau*t)

=== WHY mu_3(GF(37)) AND NOT JUST k ===

    3 divides 36 = |F_37*|, so GF(37) contains cube roots of unity:

        mu_3 = { x : x^3 = 1 mod 37 } = {1, 10, 26}

    26 = 137 mod 37, the 137-map multiplier.
    10 = 26^-1 mod 37, the base of the notation.
    So mu_3(GF(37)) = {1, 10, 26} = IC: identity, base, 137.

    Vertex k therefore carries residue 26^k mod 37, giving
        k=0 -> 1,  k=1 -> 26,  k=2 -> 10
    which is the group isomorphism mu_3(GF(37)) -> mu_3(C), not a labelling
    chosen for convenience.

=== WHAT IS FORCED (carries no information; stated so it is not mistaken
    for a result) ===

    - The three points stay equilateral at every t. Forced: they share one
      radius r(t), so the triangle only scales.
    - The centroid stays at the origin for every t. Forced: the cube roots of
      unity sum to zero, and scaling preserves that.
    - r(t) -> 1 as t -> infinity. Forced by the exp(-tau*t) envelope for any
      tau > 0.

    None of these three is evidence of anything. They are properties of
    "scale a symmetric figure by a decaying oscillation".

=== WHAT IS NOT FORCED ===

    - mu_3(GF(37)) = {1, 10, 26} specifically. This follows from
      ord_37(26) = 3, the same fact that makes every 137-orbit a 3-cycle.
      A different prime gives a different triple, or none at all when
      3 does not divide p-1.
    - The two generators of mu_3 are 26 and 10, and they induce the two
      opposite ORIENTATIONS of the triangle. Choosing 26 walks the vertices
      counter-clockwise, choosing 10 walks them clockwise. The inverse pair
      (26, 10) and the mirror pair are the same fact.

=== SCOPE ===

    mu_3 in C and mu_3 in GF(37) share a cyclic group of order 3. Z/3 is
    ubiquitous, so that correspondence by itself is level-1 and claims
    nothing. What is specific is WHICH triple GF(37) supplies.

    This file does not claim the continuous triangle "is" the GF(37)
    structure. It claims only that if you are going to index three vertices
    in this repo, {1, 26, 10} is the indexing the field already provides.

=== FALSIFICATION ===
    Any assert below failing.
"""

import math

P = 37
MULT = 26                     # 137 mod 37
A = 0.35                      # breath amplitude
OMEGA = 2.0 * math.pi         # one breath per unit t
TAU = 0.25                    # decay rate


def mu3():
    """Cube roots of unity in GF(37), as a set."""
    return {x for x in range(1, P) if pow(x, 3, P) == 1}


def residue(k, gen=MULT):
    """Residue carried by vertex k: gen^k mod 37."""
    return pow(gen, k, P)


def radius(t):
    return 1.0 + A * math.sin(OMEGA * t) * math.exp(-TAU * t)


def vertex(k, t, gen=MULT):
    """P_k(t). Returns (x, y, z, residue)."""
    r = radius(t)
    a = 2.0 * math.pi * k / 3.0
    return (r * math.cos(a), r * math.sin(a), 0.0, residue(k, gen))


def frame(t, gen=MULT):
    return [vertex(k, t, gen) for k in (0, 1, 2)]


def run():
    # --- mu_3 in GF(37) ---
    assert 36 % 3 == 0                       # why cube roots exist at all
    assert mu3() == {1, 10, 26}
    assert pow(MULT, 3, P) == 1 and pow(10, 3, P) == 1
    assert MULT == 137 % P
    assert MULT * 10 % P == 1                # 10 = 26^-1
    assert pow(MULT, 1, P) == 26 and pow(MULT, 2, P) == 10
    assert {residue(k) for k in (0, 1, 2)} == mu3()

    # --- both generators, opposite orientations ---
    assert [residue(k, 26) for k in (0, 1, 2)] == [1, 26, 10]
    assert [residue(k, 10) for k in (0, 1, 2)] == [1, 10, 26]
    assert [residue(k, 26) for k in (0, 1, 2)] == \
           [residue(k, 10) for k in (0, 2, 1)]     # one is the other reversed
    # a non-generator cannot index the triangle
    assert [residue(k, 1) for k in (0, 1, 2)] == [1, 1, 1]

    # --- the geometry, over many t ---
    ts = [i * 0.037 for i in range(400)]
    for t in ts:
        f = frame(t)
        r = radius(t)
        # centroid at origin (forced: roots sum to zero)
        cx = sum(v[0] for v in f) / 3.0
        cy = sum(v[1] for v in f) / 3.0
        assert abs(cx) < 1e-12 and abs(cy) < 1e-12, t
        # equilateral (forced: common radius)
        d = [math.dist(f[i][:2], f[j][:2]) for i, j in ((0, 1), (1, 2), (2, 0))]
        assert max(d) - min(d) < 1e-12, t
        assert abs(d[0] - r * math.sqrt(3)) < 1e-12, t
        # every vertex on the circle of radius r
        for v in f:
            assert abs(math.hypot(v[0], v[1]) - r) < 1e-12, t

    # --- decay envelope ---
    assert abs(radius(0.0) - 1.0) < 1e-12
    assert abs(radius(200.0) - 1.0) < 1e-9          # settles to the unit circle
    late = max(abs(radius(t) - 1.0) for t in (60, 70, 80, 90))
    early = max(abs(radius(t) - 1.0) for t in (0.2, 0.3, 0.4))
    assert late < early                              # it really decays

    # --- t=0 reproduces the static triad exactly ---
    f0 = frame(0.0)
    assert abs(f0[0][0] - 1.0) < 1e-12 and abs(f0[0][1]) < 1e-12
    assert abs(f0[1][0] + 0.5) < 1e-12 and abs(f0[1][1] - math.sqrt(3)/2) < 1e-12
    assert abs(f0[2][0] + 0.5) < 1e-12 and abs(f0[2][1] + math.sqrt(3)/2) < 1e-12

    print("All assertions passed.\n")
    print(f"mu_3(GF(37)) = {sorted(mu3())}   "
          f"26 = 137 mod 37,  10 = 26^-1 mod 37")
    print(f"vertex indexing k -> 26^k mod 37: "
          f"{[residue(k) for k in (0,1,2)]}   (the mu_3 isomorphism)\n")
    print("P_k(t) = r(t)*(cos(2pi k/3), sin(2pi k/3), 0),  "
          f"r(t) = 1 + {A}*sin({OMEGA/math.pi:.0f}pi t)*exp(-{TAU} t)\n")
    print(f"  {'t':>6} {'r(t)':>9}   " +
          "  ".join(f"{'V'+str(k)+' (res)':>18}" for k in (0, 1, 2)))
    # sampled OFF the zeros of sin(2pi t) -- integer and half-integer t
    # all give r = 1 exactly, which makes the breath look static
    for t in (0.0, 0.25, 1.25, 2.25, 4.25, 8.25, 16.25, 32.25):
        f = frame(t)
        cells = "  ".join(f"({v[0]:+.3f},{v[1]:+.3f}) {v[3]:>2}" for v in f)
        print(f"  {t:>6.2f} {radius(t):>9.6f}   {cells}")
    print("\nFORCED, so not evidence: equilateral at all t (common radius),")
    print("centroid at origin (roots sum to zero), r -> 1 (decay envelope).")
    print("NOT forced: that GF(37)'s mu_3 is {1,10,26}, which follows from")
    print("ord_37(26) = 3 -- the same fact that makes every 137-orbit a 3-cycle.")


if __name__ == "__main__":
    run()
