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
the other. There are 17 such pairs with both parts > 100. "1221 contains 37"
is therefore forced and carries no information beyond 37 | 999999 — the same
zero-bit pattern flagged in T282.

════════════════════════════════════════════════════════════════════════════
WHAT IS LOAD-BEARING: 26 = 10^2 (mod 37)
════════════════════════════════════════════════════════════════════════════
    100 mod 37 = 26 = 137 mod 37.

So the 137-map  x -> 26x  IS multiplication by 10^2: a TWO-PLACE DECIMAL
SHIFT. Everything the framework calls an orbit is a decimal-shift triple:

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
IC HAS A THIRD DESCRIPTION
════════════════════════════════════════════════════════════════════════════
T299 gave IC two names: the cube roots of unity mu_3, and the reduction of
the units of Z[omega]. Here is a third:

    IC = <10> = {10^0, 10^1, 10^2} mod 37,   the decimal shift group.

All three coincide because ord_37(10) = 3, which is the same statement as
1/37 = 0.027027... having period 3, which is the same statement as
999 = 27 x 37. The framework's 111 = 3 x 37 is the half-length version:
1/111 also has period 3.

That the 137-multiplier equals 10^2 is why the framework's arithmetic and
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
    pairs = [(a, n // a) for a in range(1, int(n ** 0.5) + 1) if n % a == 0]
    for a, b in pairs:
        assert a % 37 == 0 or b % 37 == 0, f"({a},{b}) has no 37"
    big = [(a, b) for a, b in pairs if a > 100 and b > 100]
    return len(pairs), len(big)


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
    npairs, nbig = verify_37_forced()
    print("\n--- Part 1: the 819/1221 pair, and what it is not ---")
    print(f"  819 x 1221 = {819*1221} = 10^6 - 1")
    print(f"  1/819  = 0.{expand(819,12)}...")
    print(f"  1/1221 = 0.{expand(1221,12)}...")
    print("  a*b = 10^n-1  =>  1/a = 0.(b padded to n). Fully general.")
    print(f"  999999 = {factor(999999)}")
    print(f"  1221 = 3 x 11 x 37 = 11 x 111;  819 = 3^2 x 7 x 13")
    print(f"\n  37 divides 999999, so it divides one side of all {npairs} factor")
    print(f"  pairs ({nbig} with both parts > 100). '1221 contains 37' is forced")
    print("  and carries no information beyond 37 | 999999.  (T282)")

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

    ic = verify_ic_third_name()
    print("\n--- Part 4: IC's third description ---")
    print(f"  IC = <10> = {{10^0, 10^1, 10^2}} mod 37 = {sorted(ic)}")
    print("  T299 gave two names: mu_3 (cube roots of unity), and the")
    print("  reduction of Z[omega]*. This is the third: the decimal shift group.")
    print(f"  All three coincide because ord_37(10) = 3, which is the same")
    print(f"  statement as 1/37 = 0.{expand(37,9)}... having period 3,")
    print(f"  which is the same statement as 999 = 27 x 37.")
    print(f"  ord_111(10) = {order_mod(10,111)} as well; 111 = 3 x 37.")
    print("\n  That the 137-multiplier equals 10^2 is why the framework's")
    print("  arithmetic and its decimal observations keep landing on each")
    print("  other. They are one structure, not two.")

    print("\nAll T302 assertions passed.")


if __name__ == '__main__':
    run()
