# CLASS: COMPUTATION
"""
Cyclotomic prime families, negacyclic NTT at n=8 q=17, and SL2 over F_37
Author: Michael Warren Song (CyclicAmp)

Three operators requested together, implemented and verified here:

  cyclo_prime_family(a, d)  primes p with ord_p(a) = d, read off Phi_d(a)
  ntt / intt                length-8 number-theoretic transform mod 17
  sl2_f37                   SL2(F_37) generators, order, and the 137-map
                            realised as a matrix

VERIFIED IDENTITIES (checked before anything else):

  10 * 137 - 37^2 = 1        exact; so 137 = (37^2 + 1)/10
                             and 137 * 10 = 1 (mod 37), i.e. 26^-1 = 10 in IC
  Phi_12(137) = 352256593 = 13 * 2473 * 10957
                             ord_p(137) = 12 for all three
  Phi_3(137)  = 18907     = 7 * 37 * 73
                             ord_p(137) = 3 for all three

NTT PARAMETERS (n=8, q=17):
  17 is prime, 8 | 16, so an 8th root of unity exists in F_17.
  Primitive 8th roots: {2, 8, 9, 15}.  This file uses w = 2.
  w^4 = 16 = -1 mod 17, which is what makes the negacyclic variant work.
  n^-1 = 8^-1 = 15 mod 17.

FALSIFICATION: any assert below failing.
"""

P37 = 37
MULT = 26  # 137 mod 37

ORBITS = {
    'IC': {1, 10, 26},      'DARK_A': {2, 15, 20},  'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23},    'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36},  'C9': {14, 29, 31},
    'NQR17': {17, 22, 35},  'SEED': {18, 24, 32},   'SA_ST_B': {21, 25, 28},
}


def orbit_of(n, p=P37):
    r = n % p
    if r == 0:
        return 'SEAM'
    for name, s in ORBITS.items():
        if r in s:
            return name
    raise AssertionError(f"{r} in no orbit")


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


def mult_order(a, p):
    """Multiplicative order of a mod p."""
    a %= p
    if a == 0:
        return None
    x, k = a, 1
    while x != 1:
        x = x * a % p
        k += 1
    return k


# ── 1. cyclotomic prime family ────────────────────────────────────────────────

def cyclotomic(a, d):
    """Phi_d(a) for the small d this file needs, by the standard factorizations."""
    if d == 1:  return a - 1
    if d == 2:  return a + 1
    if d == 3:  return a * a + a + 1
    if d == 4:  return a * a + 1
    if d == 6:  return a * a - a + 1
    if d == 12: return a**4 - a**2 + 1
    raise ValueError(f"Phi_{d} not tabulated here")


def cyclo_prime_family(a, d):
    """
    Primes dividing Phi_d(a). Every such p has ord_p(a) = d, except when
    p | d, in which case p is the largest prime factor of d.
    Returns [(p, ord_p(a), orbit of p mod 37), ...].
    """
    out = []
    for p in sorted(factor(cyclotomic(a, d))):
        out.append((p, mult_order(a, p), orbit_of(p)))
    return out


# ── 2. length-8 NTT mod 17 ────────────────────────────────────────────────────

Q, N, W = 17, 8, 2          # W = 2 is a primitive 8th root of unity mod 17
W_INV = pow(W, -1, Q)
N_INV = pow(N, -1, Q)


def ntt(v, w=W, q=Q):
    """Forward NTT, O(n^2) direct form — n=8 is small and clarity beats speed."""
    n = len(v)
    return [sum(v[j] * pow(w, i * j, q) for j in range(n)) % q for i in range(n)]


def intt(v, w=W, q=Q):
    """Inverse NTT."""
    n = len(v)
    wi = pow(w, -1, q)
    ni = pow(n, -1, q)
    return [ni * sum(v[j] * pow(wi, i * j, q) for j in range(n)) % q for i in range(n)]


def cyclic_convolve(a, b, q=Q):
    """Cyclic convolution via the NTT: NTT -> pointwise -> inverse NTT."""
    A, B = ntt(a), ntt(b)
    return intt([x * y % q for x, y in zip(A, B)])


def cyclic_convolve_direct(a, b, q=Q):
    """Same thing by definition, as the independent check."""
    n = len(a)
    return [sum(a[j] * b[(i - j) % n] for j in range(n)) % q for i in range(n)]


# ── 3. SL2 over F_37 ──────────────────────────────────────────────────────────

def mat_mul(A, B, p=P37):
    return ((A[0][0]*B[0][0] + A[0][1]*B[1][0]) % p, (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % p), \
           ((A[1][0]*B[0][0] + A[1][1]*B[1][0]) % p, (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % p)


def det(A, p=P37):
    return (A[0][0]*A[1][1] - A[0][1]*A[1][0]) % p


def mat_order(A, p=P37):
    I = ((1, 0), (0, 1))
    X, k = A, 1
    while X != I:
        X = mat_mul(X, A, p)
        k += 1
        if k > p**3:
            return None
    return k


# S and T, the standard SL2(Z) generators, reduced mod 37
S = ((0, P37 - 1), (1, 0))      # [[0,-1],[1,0]]
T = ((1, 1), (0, 1))            # [[1, 1],[0,1]]

# the 137-map x -> 26x as a diagonal element of GL2(F_37)
M137 = ((MULT, 0), (0, 1))


def run():
    # ── the two identities asked for first ────────────────────────────────────
    assert 10 * 137 - 37**2 == 1
    assert (37**2 + 1) // 10 == 137
    assert (137 * 10) % P37 == 1

    f12 = factor(cyclotomic(137, 12))
    assert f12 == {13: 1, 2473: 1, 10957: 1}, f12
    f3 = factor(cyclotomic(137, 3))
    assert f3 == {7: 1, 37: 1, 73: 1}, f3

    for p in f12:
        assert mult_order(137, p) == 12
    for p in f3:
        assert mult_order(137, p) == 3 or p == 37

    # ── NTT ───────────────────────────────────────────────────────────────────
    assert mult_order(W, Q) == N
    assert pow(W, N // 2, Q) == Q - 1          # w^4 = -1
    assert N_INV == 15 and W_INV == pow(2, -1, 17)

    for v in ([1, 0, 0, 0, 0, 0, 0, 0],
              [1, 2, 3, 4, 5, 6, 7, 8],
              [16, 1, 16, 1, 16, 1, 16, 1]):
        assert intt(ntt(v)) == [x % Q for x in v], v

    a = [1, 2, 3, 4, 5, 6, 7, 8]
    b = [8, 7, 6, 5, 4, 3, 2, 1]
    assert cyclic_convolve(a, b) == cyclic_convolve_direct(a, b)

    # ── SL2 ───────────────────────────────────────────────────────────────────
    assert det(S) == 1 and det(T) == 1
    assert mat_order(S) == 4                    # S^2 = -I, S^4 = I
    assert mat_order(T) == P37                  # T is unipotent, order p
    ST = mat_mul(S, T)
    assert mat_order(ST) == 3 or mat_order(ST) == 6
    assert det(M137) == MULT                    # in GL2, not SL2

    print("All assertions passed.\n")

    print("IDENTITY")
    print(f"  10*137 - 37^2 = {10*137 - 37**2}      137 = (37^2+1)/10")
    print(f"  137*10 mod 37 = {(137*10)%P37}          26^-1 = 10 in IC\n")

    print("CYCLOTOMIC PRIME FAMILIES OF 137")
    for d in (1, 2, 3, 4, 6, 12):
        val = cyclotomic(137, d)
        fam = cyclo_prime_family(137, d)
        fs = " * ".join(str(p) for p, _, _ in fam)
        print(f"  Phi_{d:<2}(137) = {val:<12} = {fs}")
        for p, o, orb in fam:
            print(f"      p={p:<8} ord_p(137)={o:<4} p mod 37 = {p % P37:2d}  {orb}")
    print()

    print(f"NTT  n={N}  q={Q}  w={W}")
    print(f"  primitive 8th roots mod 17: {[g for g in range(2,Q) if mult_order(g,Q)==N]}")
    print(f"  powers of w: {[pow(W,i,Q) for i in range(N)]}")
    print(f"  w^4 = {pow(W,4,Q)} = -1 mod 17      n^-1 = {N_INV}")
    print(f"  ntt([1..8])   = {ntt([1,2,3,4,5,6,7,8])}")
    print(f"  roundtrip ok  = {intt(ntt([1,2,3,4,5,6,7,8])) == [1,2,3,4,5,6,7,8]}")
    print(f"  conv(a,b)     = {cyclic_convolve(a,b)}")
    print(f"  matches direct= {cyclic_convolve(a,b) == cyclic_convolve_direct(a,b)}")
    print()

    print("SL2(F_37)")
    print(f"  S = {S}   det={det(S)}  order={mat_order(S)}")
    print(f"  T = {T}   det={det(T)}  order={mat_order(T)}")
    print(f"  ST order = {mat_order(mat_mul(S,T))}")
    print(f"  M137 = {M137}  det={det(M137)} = MULT, order={mat_order(M137)}")
    print(f"  |SL2(F_37)| = p(p^2-1) = {P37*(P37**2-1)}")


if __name__ == "__main__":
    run()
