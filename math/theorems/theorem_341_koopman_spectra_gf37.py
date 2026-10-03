# CLASS: THEOREM
"""
Theorem 341: Koopman spectra of the 137-map and the Sophie Germain map --
and the upgrade this forces on T340's grading
Author: Michael Warren Song (CyclicAmp)

Koopman theory studies a dynamical system T by the LINEAR operator it
induces on observables:

        (U f)(x) = f(T(x))

On an infinite space that is a trade -- linearity bought with infinite
dimension.  Here the space is 37 points, so U is an exact 37 x 37 matrix
and nothing is approximated.  For a bijection it is a permutation matrix,
and its spectrum is fixed by the cycle type: a cycle of length L
contributes the L-th roots of unity, once each.

=== THE TWO SPECTRA ===

    mu(x) = 26x       cycle type  1 + 12x3       (T331/T339)
    sigma(x) = 2x+1   cycle type  1 + 36         (T337)

    mu     spectrum {1, w, w^2}, multiplicities 13, 12, 12
    sigma  spectrum ALL 36th roots of unity, each once, plus a second 1

    The two are maximally opposed: mu's spectrum has three points, sigma's
    has thirty-six.  That is the operator statement of what T337 found
    element-wise -- mu is a union of 3-cycles, sigma is one long cycle.

=== THE CHARACTERS DIAGONALISE MU EXACTLY ===

    chi(26x) = chi(26) chi(x), so EVERY multiplicative character is an
    eigenfunction of U_mu with eigenvalue chi(26), and chi(26)^3 =
    chi(26^3) = chi(1) = 1 forces that eigenvalue to be a cube root of
    unity.  With 2 a primitive root and 26 = 2^12 (T339),

        chi_k(26) = exp(2 pi i * 12k / 36) = exp(2 pi i k / 3)

    so the eigenvalue depends only on k mod 3, giving 12 characters at each
    cube root.  The 12 with eigenvalue 1 are exactly the characters trivial
    on <10> -- the characters of the quotient F_37*/<10> = Z/12.

    THE INVARIANT OBSERVABLES OF THE 137-MAP ARE EXACTLY T339's ORBIT-INDEX
    FUNCTIONS.  The index was introduced there as bookkeeping; it is the
    eigenvalue-1 eigenspace.

=== T338 IN OPERATOR LANGUAGE ===

    dim of the invariant-observable space (eigenvalue 1):

        mu alone              13     12 orbits + the fixed point 0
        sigma alone            2     1 cycle + the fixed point 36
        both simultaneously    1     constants only

    The last line is T338.  <sigma, mu> = AGL(1,37) acts transitively, so
    no nonconstant observable survives both maps.  T338 said this as
    primitivity forbidding a joint partition; here it is a rank
    computation, and the two agree.

=== THE UPGRADE TO T340 ===

    T340 graded the correspondence

        1 + w + w^2 = 0  in C        1 + 10 + 26 = 0  in GF(37)

    as LEVEL 1 -- "a shared algebraic identity, nothing more".  That grade
    is too low, and Koopman theory says why.  The complex cube roots of
    unity are not merely analogous to the orbit multipliers: they ARE the
    spectrum of the operator induced by the map whose multipliers those
    are.  Both facts descend from one input, ord_37(26) = 3:

        ord = 3  =>  Phi_3(10) = 0  =>  the multipliers sum to 0 in GF(37)
        ord = 3  =>  all cycles length 3  =>  spectrum {1, w, w^2} in C

    Same cause, two consequences.  That is a LEVEL-2 correspondence -- a
    shared MECHANISM, not a shared formula.  Upgraded here.

    It remains TIER A.  Any order-3 bijection has cube-root-of-unity
    spectrum, so this says nothing about 37 in particular; what 37 supplies
    is that 10 -- the base we write in -- is the order-3 element (T333).
    And it still does not say GF(37) models interference.  The upgrade is
    from coincidence to common cause, not from mathematics to physics.

=== FALSIFICATION ===
    A cycle type for mu or sigma other than 1+12x3 and 1+36; a character
    that is not an eigenfunction; a joint invariant dimension above 1.
"""

P = 37


def mu(x):
    return (26 * x) % P


def sigma(x):
    return (2 * x + 1) % P


def cycle_type(f):
    from collections import Counter
    seen, out = set(), []
    for x in range(P):
        if x in seen:
            continue
        c, y = 0, x
        while y not in seen:
            seen.add(y)
            c += 1
            y = f(y)
        out.append(c)
    return Counter(out)


def run():
    import cmath
    import numpy as np
    from collections import Counter

    # --- cycle types ---
    cm, cs = cycle_type(mu), cycle_type(sigma)
    assert dict(cm) == {1: 1, 3: 12} and sum(k * v for k, v in cm.items()) == P
    assert dict(cs) == {1: 1, 36: 1} and sum(k * v for k, v in cs.items()) == P

    # --- spectra from the cycle type ---
    def spectrum(ct):
        s = Counter()
        for L, m in ct.items():
            for j in range(L):
                s[round(j / L, 9)] += m
        return s
    sm, ss = spectrum(cm), spectrum(cs)
    assert sorted(sm) == [0.0, round(1 / 3, 9), round(2 / 3, 9)]
    assert sorted(sm.values(), reverse=True) == [13, 12, 12]
    assert len(ss) == 36 and ss[0.0] == 2
    assert sum(sm.values()) == sum(ss.values()) == P

    # --- confirm numerically from the actual matrices ---
    def U(f):
        M = np.zeros((P, P))
        for x in range(P):
            M[x, f(x)] = 1
        return M
    Um, Us = U(mu), U(sigma)
    ang = sorted({round(float(np.angle(e) / (2 * np.pi)) % 1, 4)
                  for e in np.linalg.eigvals(Um)})
    assert ang == [0.0, 0.3333, 0.6667]
    assert len({round(float(np.angle(e) / (2 * np.pi)) % 1, 4)
                for e in np.linalg.eigvals(Us)}) == 36

    # --- characters diagonalise mu ---
    g = 2
    dlog = {pow(g, k, P): k for k in range(36)}
    assert dlog[26] == 12 and pow(2, 12, P) == 26
    z = lambda t: cmath.exp(2j * cmath.pi * t)
    for k in range(36):
        chi = {x: z(k * dlog[x] / 36) for x in range(1, P)}
        lam = z(k * dlog[26] / 36)
        for x in range(1, P):                       # chi(26x) = chi(26)chi(x)
            assert abs(chi[(26 * x) % P] - lam * chi[x]) < 1e-9
        assert abs(lam ** 3 - 1) < 1e-9             # a cube root of unity
        assert abs(lam - z((k % 3) / 3)) < 1e-9     # depends on k mod 3
    triv = [k for k in range(36) if abs(z(k * dlog[26] / 36) - 1) < 1e-9]
    assert len(triv) == 12 and triv == [k for k in range(36) if k % 3 == 0]

    # --- T338 as a rank computation ---
    I = np.eye(P)
    def fixdim(*Ms):
        A = np.vstack([M - I for M in Ms])
        return P - np.linalg.matrix_rank(A, tol=1e-9)
    assert fixdim(Um) == 13                          # 12 orbits + {0}
    assert fixdim(Us) == 2                           # 1 cycle + {36}
    assert fixdim(Um, Us) == 1                       # constants only = T338

    # --- the upgrade: one cause, two consequences ---
    assert pow(26, 3, P) == 1 and pow(26, 1, P) != 1
    assert (1 + 10 + 26) % P == 0                    # GF(37) side
    w = cmath.exp(2j * cmath.pi / 3)
    assert abs(1 + w + w * w) < 1e-12                # C side
    assert 100 % P == 26                             # 26 = 10^2, so Phi_3(10)
    assert 10 ** 2 + 10 + 1 == 111 == 3 * P
    # Tier A: any order-3 bijection does this
    for n in (5, 6, 9):
        ct = Counter({3: n})
        s = spectrum(ct)
        assert sorted(s) == [0.0, round(1 / 3, 9), round(2 / 3, 9)]

    print("All assertions passed.\n")
    print("THEOREM 341.  Koopman spectra on 37 points.\n")
    print("   (U f)(x) = f(T(x)).  37 points, so U is an exact 37x37 matrix.")
    print("   For a bijection it is a permutation matrix and the spectrum is")
    print("   fixed by the cycle type.\n")
    print(f"   mu    = 26x    cycle type {dict(cm)}")
    print(f"     spectrum {{1, w, w^2}}, multiplicities 13, 12, 12")
    print(f"   sigma = 2x+1   cycle type {dict(cs)}")
    print(f"     spectrum: all 36 roots of unity, plus a second 1")
    print( "   maximally opposed -- three eigenvalues against thirty-six.\n")
    print("  THE CHARACTERS DIAGONALISE MU")
    print( "   chi(26x) = chi(26)chi(x), and chi(26)^3 = 1, so every character")
    print(f"   is an eigenfunction at a cube root of unity.  26 = 2^{dlog[26]},")
    print( "   so chi_k(26) = exp(2 pi i k/3): the eigenvalue is k mod 3.")
    print(f"   the {len(triv)} characters at eigenvalue 1 are exactly those")
    print( "   trivial on <10> -- the characters of F*/<10> = Z/12.")
    print( "   T339's orbit index IS the eigenvalue-1 eigenspace.\n")
    print("  T338 AS A RANK COMPUTATION")
    print(f"   invariant observables:  mu {fixdim(Um)},  sigma {fixdim(Us)},"
          f"  both {fixdim(Um,Us)}")
    print( "   dimension 1 = constants only: transitivity of <sigma,mu>,")
    print( "   i.e. T338's primitivity, as a rank.\n")
    print("  THE UPGRADE TO T340")
    print( "   T340 graded 1+w+w^2 = 0 against 1+10+26 = 0 as LEVEL 1,")
    print( "   'a shared algebraic identity'.  Too low.  Both descend from")
    print( "   ord_37(26) = 3:")
    print( "     ord 3 -> Phi_3(10) = 0      -> multipliers sum to 0 in GF(37)")
    print( "     ord 3 -> all cycles length 3 -> spectrum {1,w,w^2} in C")
    print( "   One cause, two consequences: LEVEL 2, a shared MECHANISM.\n")
    print( "   Still TIER A -- any order-3 bijection has this spectrum, so it")
    print( "   says nothing about 37; what 37 supplies is that 10, the base we")
    print( "   write in, is the order-3 element (T333).  And it still does not")
    print( "   say GF(37) models interference.  Coincidence to common cause,")
    print( "   not mathematics to physics.")


if __name__ == "__main__":
    run()
