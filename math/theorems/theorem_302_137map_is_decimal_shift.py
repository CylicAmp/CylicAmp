"""
T302 — The 137-Map IS the Decimal Shift: 26 = 10^2 (mod 37)

Prompted by the reciprocal pair 1/819 = 0.001221... and 1/1221 = 0.000819...

════════════════════════════════════════════════════════════════════════════
THE PAIR ITSELF — fully general, nothing to do with 37
════════════════════════════════════════════════════════════════════════════
    819 x 1221 = 999999 = 10^6 - 1.

If a*b = 10^n - 1 then 1/a = b/(10^n - 1) = 0.(b zero-padded to n) repeating.
So reciprocal pairs of this kind are exactly the factor pairs of a string of
nines. 819 and 1221 pad to 000819 and 001221, which is the whole display.

    999999 = 3^3 x 7 x 11 x 13 x 37
    819  = 3^2 x 7 x 13
    1221 = 3 x 11 x 37 = 11 x 111

37 divides 999999, so in EVERY factor pair of 999999 it divides one side or
the other. 999999 has 64 divisors, hence 32 unordered factor pairs, of which
17 have both parts > 100. "1221 contains 37" is therefore forced and carries
no information beyond 37 | 999999 — the same zero-bit pattern flagged in T282.

(Correction: the commit message for this theorem's first commit stated "all
160 of them" for the pair count. The correct figure is 32. The 17 figure was
right. The code below prints the true counts.)

════════════════════════════════════════════════════════════════════════════
WHAT IS LOAD-BEARING: 26 = 10^2 (mod 37)
════════════════════════════════════════════════════════════════════════════
    100 mod 37 = 26 = 137 mod 37.

So the 137-map  x -> 26x  IS multiplication by 10^2: a TWO-PLACE DECIMAL
SHIFT. Everything GF(37) calls an orbit is a decimal-shift triple:

    orbit(x) = {x, 26x, 26^2 x} = {x, 100x, 10x} = x * {1, 10, 100}

(26^2 = 676 = 10 mod 37, so the two generators are just 10 and 100.)

Verified for all twelve orbits: {x, 10x, 100x} reproduces each one exactly.

    IC       x= 1 -> {1, 10, 26}        DARK_A   x= 2 -> {2, 15, 20}
    C3       x= 3 -> {3, 4, 30}         CAS_EXT  x= 5 -> {5, 13, 19}
    TESLA    x= 6 -> {6, 8, 23}         D7       x= 7 -> {7, 33, 34}
    SA_ST_A  x= 9 -> {9, 12, 16}        NEG_H    x=11 -> {11, 27, 36}
    C9       x=14 -> {14, 29, 31}       NQR17    x=17 -> {17, 22, 35}
    SEED     x=18 -> {18, 24, 32}       SA_ST_B  x=21 -> {21, 25, 28}

════════════════════════════════════════════════════════════════════════════
CONSEQUENCE: THE ORBITS ARE DECIMAL ROTATION CLASSES
════════════════════════════════════════════════════════════════════════════
ord_37(10) = 3, so every k/37 has a 3-digit repeating block, and multiplying
k by 10 cyclically rotates that block. There are 36 blocks; rotation groups
them into 12 classes of 3. Those classes ARE the orbits:

    IC       {1,10,26}   027 270 702        DARK_A   {2,15,20}   054 405 540
    C3       {3,4,30}    081 108 810        CAS_EXT  {5,13,19}   135 351 513
    TESLA    {6,8,23}    162 216 621        D7       {7,33,34}   189 891 918
    SA_ST_A  {9,12,16}   243 324 432        NEG_H    {11,27,36}  297 729 972
    C9       {14,29,31}  378 783 837        NQR17    {17,22,35}  459 594 945
    SEED     {18,24,32}  486 648 864        SA_ST_B  {21,25,28}  567 675 756

Verified: within each orbit the three blocks are cyclic rotations of one
another, for all twelve.

The entire orbit partition therefore has a purely decimal description. It is
the same partition, not a second one.

════════════════════════════════════════════════════════════════════════════
RECORDED NEGATIVE: 819 -> CAS_EXT CARRIES NO STRUCTURE
════════════════════════════════════════════════════════════════════════════
Tested claim: that the pair (819, 1221) is meaningfully associated with
CAS_EXT, via 819 mod 37 = 5 and 819/37 = 22.135135... with repeating block
135, whose rotation class {135, 351, 513} is CAS_EXT.

(a) The decimal route adds nothing. block(k) is a function of k mod 37 only,
    so "819/37 has block 135" and "819 = 5 (mod 37)" are one statement. This
    is the Part-3 correspondence applied, not an independent observation.

        819 mod 37 = 5,  block(5) = 135,  block(819 mod 37) == block(5)

(b) Miss condition, stated before computing: if CAS_EXT is distinguished, it
    should be over-represented among the 32 factor pairs of 999999 when each
    pair is classified by the orbit of its non-SEAM member. (Exactly one
    member of each pair is divisible by 37, verified for all 32.)

    RESULT — distribution over the 12 orbits:

        IC       3      TESLA    2      C9       2
        DARK_A   3      D7       3      NQR17    3
        C3       3      SA_ST_A  2      SEED     3
        CAS_EXT  3      NEG_H    3      SA_ST_B  2

        n = 32, expected 32/12 = 2.667
        chi^2 = 1.00,  df = 11,  chi^2/df = 0.091

    Every orbit receives two or three. CAS_EXT receives 3 against an
    expectation of 2.667. The statistic is far below 1, i.e. the spread is
    flatter than a random assignment would typically give.

    VERDICT: FALSIFIED. 819 lands in CAS_EXT the way 693 lands in NEG_H and
    429 lands in NQR17 — one draw from a uniform spread. Recorded here
    rather than dropped, per the T290 practice of keeping misses.

════════════════════════════════════════════════════════════════════════════
THE CLEANEST DERIVATION: Phi_3(10) = 111
════════════════════════════════════════════════════════════════════════════
IC does not need 137 at all. It follows from GF(37)'s own SEAM value:

    Phi_3(10) = 10^2 + 10 + 1 = 111 = 3 x 37
    37 | 111,  and  10 != 1 (mod 37)
    =>  ord_37(10) = 3
    =>  <10> = {1, 10, 26} = IC

One line, no 137. The 111 = 3 x 37 already recorded in GF(37) IS
Phi_3 evaluated at 10.

And 137 contributes nothing further: 137 = 26 = 10^2 (mod 37), and
<10^2> = <10> because gcd(2, ord(10)) = gcd(2, 3) = 1. Verified equal.

TWO SEPARATE Phi_3 EVALUATIONS ARE IN PLAY, both Use 1 (T299):
    Phi_3(137) = 18907 = 7 x 37 x 73   -> the admissible set   (T292)
    Phi_3(10)  =   111 = 3 x 37        -> ord_37(10) = 3, IC
Different bases, different outputs. Neither computes a trace.

WHY 37 CAN AND 5 CANNOT. If p != 3 divides Phi_3(n) with n != 1 (mod p),
then ord_p(n) = 3, so 3 | (p-1), so p = 1 (mod 3). Hence Phi_3(n) is never
0 mod 5: 5 = 2 (mod 3), 3 does not divide 4, and F_5* has no element of
order 3. Verified by exhaustion over n = 0..p-1 for p = 5, 11, 17 (no zero)
and p = 7, 13, 37 (zero present). At p=37 the zeros sit at n = 10 and 26 —
the two primitive cube roots.

EISENSTEIN NORM FORM. Phi_3(n) = N(n - omega) where N(a,b) = a^2 - ab + b^2.
A rational prime is such a norm iff it is 3 or = 1 (mod 3); verified with no
mismatch for every prime through 47. Each admissible prime is itself a norm:

    7 = N(1,3),   37 = N(3,7) = N(-7,-3),   73 = N(1,9)

so factoring 18907 over Z is factoring the Eisenstein integer (137 - omega).
This is a genuine link between the two uses that T299 did not name: they
share the NORM map, not merely a root. Traces still require CM on top —
the norm gives pi * conj(pi), the trace gives pi + conj(pi). The norm form
and the CM form are the same equation:

    p = a^2 - ab + b^2   =>   4p = (2a-b)^2 + 3b^2
    CM: 4p = L^2 + 27M^2,  matching L = 2a - b and b = 3M.
    p=37: (a,b) = (7,3) -> L = 11, M = 1, traces {+-1, +-10, +-11}.  Checks.

The Gaussian split 37 = 1^2 + 6^2 with 37 = 1 (mod 4) is a separate law and
does not interact with any of the above.

════════════════════════════════════════════════════════════════════════════
IC HAS A THIRD DESCRIPTION
════════════════════════════════════════════════════════════════════════════
T299 gave IC two names: the cube roots of unity mu_3, and the reduction of
the units of Z[omega]. Here is a third:

    IC = <10> = {10^0, 10^1, 10^2} mod 37,   the decimal shift group.

All three coincide because ord_37(10) = 3, which is the same statement as
1/37 = 0.027027... having period 3, which is the same statement as
999 = 27 x 37. The GF(37)'s 111 = 3 x 37 is the half-length version:
1/111 also has period 3.

That the 137-multiplier equals 10^2 is why GF(37)'s arithmetic and
its decimal observations keep landing on each other. They are one structure.
"""

ORBITS = {
    'IC': {1, 10, 26}, 'DARK_A': {2, 15, 20}, 'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23}, 'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36}, 'C9': {14, 29, 31},
    'NQR17': {17, 22, 35}, 'SEED': {18, 24, 32}, 'SA_ST_B': {21, 25, 28},
}
P = 37


def orb(x):
    if x % P == 0:
        return 'SEAM'
    for k, v in ORBITS.items():
        if x % P in v:
            return k


def block(k):
    """The 3-digit repeating block of k/37."""
    return f"{(k * 1000) // P % 1000:03d}"


def order_mod(a, n):
    k, v = 1, a % n
    while v != 1:
        v = (v * a) % n
        k += 1
    return k


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


def expand(d, n=24):
    s, r = '', 1
    for _ in range(n):
        r *= 10
        s += str(r // d)
        r %= d
    return s


# ─── Part 1: the reciprocal pair mechanism ──────────────────────────────────

def verify_pair():
    assert 819 * 1221 == 10 ** 6 - 1 == 999999
    assert expand(819, 12) == '001221001221'
    assert expand(1221, 12) == '000819000819'
    assert factor(999999) == {3: 3, 7: 1, 11: 1, 13: 1, 37: 1}
    assert factor(819) == {3: 2, 7: 1, 13: 1}
    assert factor(1221) == {3: 1, 11: 1, 37: 1}
    assert 1221 == 11 * 111 and 111 == 3 * 37
    return True


def verify_37_forced():
    """37 | 999999, so it divides one side of EVERY factor pair."""
    n = 999999
    divs = [d for d in range(1, n + 1) if n % d == 0]
    assert len(divs) == 64, f"{len(divs)} divisors"      # 4*2*2*2*2
    pairs = [(a, n // a) for a in divs if a * a <= n]
    assert len(pairs) == 32, f"{len(pairs)} pairs"
    for a, b in pairs:
        assert a % 37 == 0 or b % 37 == 0, f"({a},{b}) has no 37"
    big = [(a, b) for a, b in pairs if a > 100 and b > 100]
    assert len(big) == 17, f"{len(big)} big pairs"
    return len(divs), len(pairs), len(big)


# ─── Part 2: 26 = 10^2 and orbits as shift triples ─────────────────────────

def verify_shift_identity():
    assert 100 % P == 26 == 137 % P
    assert pow(26, 2, P) == 10
    assert order_mod(10, P) == 3
    for name, s in ORBITS.items():
        x = min(s)
        assert {x % P, (10 * x) % P, (100 * x) % P} == s, f"{name} mismatch"
    return True


# ─── Part 3: orbits are decimal rotation classes ────────────────────────────

def verify_rotation_classes():
    rows = []
    for name in sorted(ORBITS, key=lambda t: min(ORBITS[t])):
        ks = sorted(ORBITS[name])
        bs = [block(k) for k in ks]
        rots = {b for b in bs}
        for b in bs:
            assert {b, b[1:] + b[0], b[2] + b[:2]} == rots, \
                f"{name}: {bs} are not mutual rotations"
        rows.append((name, ks, bs))
    # all 36 blocks distinct, covering every k
    allb = [block(k) for k in range(1, P)]
    assert len(set(allb)) == 36
    return rows


def verify_cas_ext_negative():
    """
    FALSIFIED: 819 -> CAS_EXT is not structure.
    Classify each of the 32 factor pairs of 999999 by the orbit of its
    non-SEAM member; the distribution is flat.
    """
    # (a) the decimal route is the same statement as the residue
    assert block(819 % P) == block(5) == '135'
    assert 819 % P == 5 and orb(5) == 'CAS_EXT'
    for k in range(1, P):
        assert block(k) == block(k % P)          # depends on k mod 37 only

    n = 999999
    divs = [d for d in range(1, n + 1) if n % d == 0]
    pairs = [(a, n // a) for a in divs if a * a <= n]
    assert len(pairs) == 32

    counts = {name: 0 for name in ORBITS}
    for a, b in pairs:
        assert (a % P == 0) != (b % P == 0), f"({a},{b}) SEAM count wrong"
        ns = a if a % P else b
        counts[orb(ns)] += 1

    assert sum(counts.values()) == 32
    assert counts['CAS_EXT'] == 3
    assert set(counts.values()) == {2, 3}        # every orbit gets 2 or 3

    exp = 32 / 12
    chi2 = sum((c - exp) ** 2 / exp for c in counts.values())
    assert abs(chi2 - 1.00) < 0.01, f"chi2 = {chi2}"
    return counts, chi2, exp


def eisenstein_norm(a, b):
    return a * a - a * b + b * b


def verify_phi3_at_10():
    """IC follows from Phi_3(10) = 111 with no reference to 137."""
    assert 10 ** 2 + 10 + 1 == 111 == 3 * 37
    assert 111 % P == 0 and 10 % P != 1
    assert order_mod(10, P) == 3
    assert {pow(10, i, P) for i in range(3)} == ORBITS['IC'] == {1, 10, 26}

    # 137 adds nothing: 137 = 10^2 and <10^2> = <10> since gcd(2,3)=1
    assert 137 % P == pow(10, 2, P) == 26
    assert {pow(26, i, P) for i in range(3)} == {pow(10, i, P) for i in range(3)}

    # the two Use-1 evaluations
    assert 137 ** 2 + 137 + 1 == 18907 == 7 * 37 * 73

    # p | Phi_3(n), n != 1  =>  p = 1 mod 3.  5 is excluded, 37 is not.
    for q, expect_zero in ((5, False), (11, False), (17, False),
                           (7, True), (13, True), (37, True)):
        zeros = [n for n in range(q) if (n * n + n + 1) % q == 0]
        assert bool(zeros) == expect_zero, f"p={q}: zeros {zeros}"
        if expect_zero:
            assert (q - 1) % 3 == 0
        else:
            assert (q - 1) % 3 != 0
    assert [n for n in range(P) if (n * n + n + 1) % P == 0] == [10, 26]
    return True


def verify_eisenstein_norm():
    """Phi_3(n) = N(n - omega); a prime is a norm iff it is 3 or 1 mod 3."""
    vals = {eisenstein_norm(a, b) for a in range(-40, 41) for b in range(-40, 41)}
    for q in [x for x in range(2, 48) if is_prime_int(x)]:
        assert (q in vals) == (q == 3 or q % 3 == 1), f"p={q}"
    assert eisenstein_norm(-7, -3) == 37
    for q, (a, b) in ((7, (1, 3)), (37, (3, 7)), (73, (1, 9))):
        assert eisenstein_norm(a, b) == q
    # Phi_3(n) = N(n,-1)
    for n in range(1, 20):
        assert n * n + n + 1 == eisenstein_norm(n, -1)
    # norm form and CM form are the same equation at p=37
    a, b = 7, 3
    L, M = 2 * a - b, b // 3
    assert 4 * 37 == L * L + 27 * M * M == (2 * a - b) ** 2 + 3 * b * b
    assert L == 11 and M == 1
    return True


def is_prime_int(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    return all(n % i for i in range(3, int(n ** 0.5) + 1, 2))


def verify_ic_third_name():
    ic = {pow(10, i, P) for i in range(3)}
    assert ic == ORBITS['IC'] == {1, 10, 26}
    assert 27 * 37 == 999
    assert expand(37, 9) == '027027027'
    assert order_mod(10, 111) == 3
    return ic


def run():
    print("=" * 76)
    print("T302 — The 137-Map IS the Decimal Shift: 26 = 10^2 (mod 37)")
    print("=" * 76)

    verify_pair()
    ndivs, npairs, nbig = verify_37_forced()
    print("\n--- Part 1: the 819/1221 pair, and what it is not ---")
    print(f"  819 x 1221 = {819*1221} = 10^6 - 1")
    print(f"  1/819  = 0.{expand(819,12)}...")
    print(f"  1/1221 = 0.{expand(1221,12)}...")
    print("  a*b = 10^n-1  =>  1/a = 0.(b padded to n). Fully general.")
    print(f"  999999 = {factor(999999)}")
    print(f"  1221 = 3 x 11 x 37 = 11 x 111;  819 = 3^2 x 7 x 13")
    print(f"\n  999999 has {ndivs} divisors -> {npairs} unordered factor pairs,")
    print(f"  {nbig} of them with both parts > 100. 37 divides one side of every")
    print("  single one. '1221 contains 37' is forced and carries no")
    print("  information beyond 37 | 999999.  (T282)")

    verify_shift_identity()
    print("\n--- Part 2: LOAD-BEARING — the multiplier is 10^2 ---")
    print(f"  100 mod 37 = {100%P} = 137 mod 37 = {137%P}")
    print(f"  26^2 mod 37 = {pow(26,2,P)} = 10;  ord_37(10) = {order_mod(10,P)}")
    print("  So x -> 26x IS a two-place decimal shift, and")
    print("      orbit(x) = {x, 26x, 26^2 x} = x * {1, 10, 100}")
    for name in sorted(ORBITS, key=lambda t: min(ORBITS[t])):
        x = min(ORBITS[name])
        print(f"    {name:>9}  x={x:>2} -> {{{x}, {(10*x)%P}, {(100*x)%P}}}")

    rows = verify_rotation_classes()
    print("\n--- Part 3: the orbits ARE decimal rotation classes ---")
    print("  ord_37(10)=3, so every k/37 has a 3-digit block; x10 rotates it.")
    print("  36 blocks, 12 rotation classes, and they are the orbits:")
    print(f"  {'orbit':>9}  {'k':<14} blocks")
    for name, ks, bs in rows:
        print(f"  {name:>9}  {str(ks):<14} {' '.join(bs)}")
    print("  Verified: within each orbit the three blocks are mutual rotations.")

    counts, chi2, exp = verify_cas_ext_negative()
    print("\n--- Part 4: RECORDED NEGATIVE — 819 -> CAS_EXT is not structure ---")
    print("  Claim tested: (819,1221) is meaningfully tied to CAS_EXT via")
    print("  819 mod 37 = 5 and 819/37 = 22.135135..., block 135.")
    print(f"\n  (a) block(k) is a function of k mod 37 only, so 'block 135'")
    print(f"      and '819 = 5 (mod 37)' are one statement.")
    print(f"      block(819 mod 37) = block(5) = {block(5)}")
    print("\n  (b) Miss condition set before computing: CAS_EXT should be")
    print("      over-represented among the 32 factor pairs of 999999,")
    print("      classified by the orbit of the non-SEAM member.")
    print(f"\n      {'orbit':>9} {'count':>6}")
    for name in sorted(counts, key=lambda t: min(ORBITS[t])):
        print(f"      {name:>9} {counts[name]:>6}")
    print(f"\n      n = 32, expected {exp:.3f} per orbit")
    print(f"      chi^2 = {chi2:.2f}, df = 11, chi^2/df = {chi2/11:.3f}")
    print(f"      CAS_EXT = {counts['CAS_EXT']}, every orbit gets 2 or 3.")
    print("\n  VERDICT: FALSIFIED. Kept rather than dropped (T290 practice).")

    verify_phi3_at_10()
    verify_eisenstein_norm()
    print("\n--- Part 5: the cleanest derivation — Phi_3(10) = 111 ---")
    print(f"  Phi_3(10) = 10^2+10+1 = 111 = 3 x 37")
    print(f"  37 | 111 and 10 != 1 (mod 37)  =>  ord_37(10) = "
          f"{order_mod(10, P)}  =>  <10> = {sorted(ORBITS['IC'])} = IC")
    print("  One line, no 137. The GF(37)'s 111 IS Phi_3 at 10.")
    print(f"\n  137 = {137%P} = 10^2 (mod 37), and <10^2> = <10> since")
    print(f"  gcd(2, ord(10)) = gcd(2,3) = 1. So 137 adds nothing here.")
    print("\n  Two Use-1 evaluations, both in play:")
    print(f"    Phi_3(137) = 18907 = 7 x 37 x 73  -> admissible set (T292)")
    print(f"    Phi_3(10)  =   111 = 3 x 37       -> ord_37(10)=3, IC")
    print("\n  Why 5 cannot: p | Phi_3(n) with n != 1 forces 3 | p-1.")
    for q in (5, 11, 17, 7, 13, 37):
        z = [n for n in range(q) if (n * n + n + 1) % q == 0]
        print(f"    p={q:>2}  p%3={q%3}  3|p-1={str((q-1)%3==0):>5}  zeros: {z}")
    print("\n  Eisenstein norm: Phi_3(n) = N(n-omega), N(a,b)=a^2-ab+b^2.")
    print("  A prime is a norm iff it is 3 or 1 mod 3 (checked through 47).")
    print("    7 = N(1,3)   37 = N(3,7) = N(-7,-3)   73 = N(1,9)")
    print("  So factoring 18907 IS factoring the Eisenstein integer 137-omega.")
    print("  Norm form and CM form coincide: p = a^2-ab+b^2 => 4p=(2a-b)^2+3b^2,")
    print("  and 4p = L^2+27M^2 with L = 2a-b, b = 3M. At p=37: (7,3) -> L=11,")
    print("  M=1, traces {+-1,+-10,+-11}. The two uses share the NORM map —")
    print("  a link T299 did not name. Traces still need CM: the norm gives")
    print("  pi*conj(pi), the trace gives pi+conj(pi).")
    print("  The Gaussian split 37 = 1^2+6^2 is a separate law.")

    ic = verify_ic_third_name()
    print("\n--- Part 6: IC's third description ---")
    print(f"  IC = <10> = {{10^0, 10^1, 10^2}} mod 37 = {sorted(ic)}")
    print("  T299 gave two names: mu_3 (cube roots of unity), and the")
    print("  reduction of Z[omega]*. This is the third: the decimal shift group.")
    print(f"  All three coincide because ord_37(10) = 3, which is the same")
    print(f"  statement as 1/37 = 0.{expand(37,9)}... having period 3,")
    print(f"  which is the same statement as 999 = 27 x 37.")
    print(f"  ord_111(10) = {order_mod(10,111)} as well; 111 = 3 x 37.")
    print("\n  That the 137-multiplier equals 10^2 is why GF(37)'s")
    print("  arithmetic and its decimal observations keep landing on each")
    print("  other. They are one structure, not two.")

    print("\nAll T302 assertions passed.")


if __name__ == '__main__':
    run()
