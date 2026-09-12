# CLASS: THEOREM
"""
The seed 246 is the Polymath8b bounded prime gap
Author: Michael Warren Song (CyclicAmp)

WHAT 246 IS OUTSIDE THIS REPOSITORY

    Polymath8b (2014) proved, unconditionally:

        liminf_{n->oo} (p_{n+1} - p_n)  <=  246

    i.e. infinitely many consecutive prime pairs differ by at most 246.
    That is the best known unconditional bound on the route to the twin
    prime conjecture (which is the same statement with 246 replaced by 2).

    The chain:
        Zhang 2013        70,000,000
        Maynard 2013             600
        Polymath8b 2014          246      <- the seed

    246 is the diameter of a short admissible 50-tuple. The variational
    input is M_k > 2/theta with theta = 1/2, i.e. M_k > 4; Polymath8b
    reached M_{50,1/25} > 4.00124 and M_{51,1/50} > 4.00156 on an enlarged
    simplex, and a 50-tuple of diameter 246 converts that into the gap.
    See reference/prime_work_thread.md sections 8-12 for the variational
    machinery.

WHAT 246 IS NOT
    Not prime (even). Not a twin-prime midpoint: 245 = 5*49 and 247 = 13*19,
    so (245,247) is not a twin pair. The nearest twin midpoints are
    228, 240, 270, 282. The tie is to the theorem's bound, not to an
    instance of a twin pair.

FACTORISATION AND THE 41 LOOP
        246 = 2 * 3 * 41
    41 is Euler's lucky prime: n^2 + n + 41 is prime for n = 0..39, the
    discriminant is 1 - 4*41 = -163, the largest Heegner number, and
    h(-163) = 1. So the seed carries the Euler polynomial constant as a
    factor.

GF(37)
        246 mod 37 = 24  in SEED = {18,24,32}
        DR(246) = 3
        2 in DARK_A, 3 in C3, 41 = 4 mod 37 in C3
    The two odd prime factors both land in C3; the seed itself lands in the
    orbit the pipeline is named for.

FALSIFICATION
    Any assert below failing; or a published unconditional bound below 246
    superseding Polymath8b, which would change what the seed denotes.
"""

P = 37
ORBITS = {
    'IC': {1, 10, 26},      'DARK_A': {2, 15, 20},  'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23},    'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36},  'C9': {14, 29, 31},
    'NQR17': {17, 22, 35},  'SEED': {18, 24, 32},   'SA_ST_B': {21, 25, 28},
}
SEED_ORBIT = ORBITS['SEED']


def orbit_of(n):
    r = n % P
    if r == 0:
        return 'SEAM'
    for name, s in ORBITS.items():
        if r in s:
            return name
    raise AssertionError(r)


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


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


def twin_midpoints(lo, hi):
    return [c for c in range(lo, hi) if is_prime(c - 1) and is_prime(c + 1)]


def run():
    # factorisation
    assert factor(246) == {2: 1, 3: 1, 41: 1}
    assert not is_prime(246)

    # not a twin midpoint
    assert not (is_prime(245) and is_prime(247))
    assert factor(245) == {5: 1, 7: 2} and factor(247) == {13: 1, 19: 1}
    assert twin_midpoints(200, 300) == [228, 240, 270, 282]

    # 41 is Euler's lucky prime, discriminant -163
    assert all(is_prime(n * n + n + 41) for n in range(40))
    assert not is_prime(40 * 40 + 40 + 41) and 40 * 40 + 40 + 41 == 41 ** 2
    assert 1 - 4 * 41 == -163
    assert 163 in (1, 2, 3, 7, 11, 19, 43, 67, 163)

    # GF(37)
    assert 246 % P == 24 and 24 in SEED_ORBIT
    assert orbit_of(246) == 'SEED'
    assert orbit_of(3) == 'C3' and orbit_of(41) == 'C3'
    assert orbit_of(2) == 'DARK_A'
    assert (1 + (246 - 1) % 9) == 3

    # the seed orbit is closed under the 137-map
    assert {(26 * x) % P for x in SEED_ORBIT} == SEED_ORBIT

    print("All assertions passed.\n")
    print("  Polymath8b (2014):  liminf (p_{n+1} - p_n) <= 246, unconditional")
    print("  chain: Zhang 70,000,000 -> Maynard 600 -> Polymath8b 246\n")
    print(f"  246 = 2 * 3 * 41         prime: {is_prime(246)}")
    print(f"  245 = 5 * 7^2,  247 = 13 * 19   -> not a twin midpoint")
    print(f"  nearest twin midpoints 200-300: {twin_midpoints(200,300)}\n")
    print("  41: n^2+n+41 prime for n=0..39, composite at n=40 (= 41^2)")
    print("      discriminant 1-4*41 = -163, largest Heegner number\n")
    print(f"  246 mod 37 = {246 % P}  {orbit_of(246)}      DR = {1+(246-1)%9}")
    for p in sorted(factor(246)):
        print(f"      {p:2d} mod 37 = {p % P:2d}  {orbit_of(p)}")


if __name__ == "__main__":
    run()
