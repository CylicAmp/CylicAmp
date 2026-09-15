# CLASS: THEOREM
"""
Theorem 347: the prime-gap chi bias and the orbit self-transition rate are
both measured against the wrong null
Author: Michael Warren Song (CyclicAmp)

An analysis of 664,567 primes below 10^7 read through T346's pair-invariant.
Every figure in it reproduces exactly.  Two of its three conclusions compare
against a baseline that is not the right one.

=== REPRODUCED, ALL OF IT ===

    primes < 10^7                664,579
    primes > 37                  664,567      (12 removed: 2..37)
    successive gaps              664,566
    min 2, max 154, mean         15.047
    gap 2 / 4 / 6                58,975 / 58,617 / 99,985
    QR gaps / NR gaps            290,196 / 374,150   ratio 0.7756
    orbit self-transitions       0.0577

    Independently recomputed here; every one matches.  The prime orbit
    distribution -- twelve counts near 55,380, all within 0.3% of 1/12 -- is
    a correct Dirichlet check and stands as reported.

=== CORRECTION 1: chi(g) IS NOT A MEASUREMENT ===

    chi(g) is a DETERMINISTIC function of g.  The QR/NR split of gaps is the
    gap histogram re-weighted by a fixed sign, and carries no information the
    histogram does not already have.  There is nothing about primes in it.

    Where the excess comes from, term by term:

        g       count    chi    running NR - QR
        6      99,985     -1          + 99,985
       12      65,513     +1          + 34,472
        2      58,975     -1          + 93,447
        4      58,617     +1          + 34,830
       10      54,431     +1          - 19,601
       18      43,851     -1          + 24,250
        8      42,352     -1          + 66,602
       14      35,394     -1          +101,996

        full NR - QR = +83,954

    Gap 6 alone contributes +99,985 -- 119% of the total, the other gaps
    partially cancelling it back.  And chi(6) = chi(2)chi(3) = (-1)(+1) = -1,
    because 2 is a primitive root so chi(2) = -1, while 3 = 2^26 has an even
    exponent so chi(3) = +1.

    So the entire bias is one sentence: the commonest prime gap happens to be
    a non-residue mod 37.  Not a fact about consecutive primes.

=== CORRECTION 2: THE SELF-TRANSITION BASELINE IS 1/18, NOT 1/12 ===

    orbit(p) = orbit(p+g) means (p+g)/p lies in <10> = {1,10,26}, i.e.
    1 + g/p is in the subgroup.  For a FIXED g not congruent to 0:

        h = 1   needs g == 0            excluded
        h = 10  needs p == g/9          one residue
        h = 26  needs p == g/25         one residue

    Exactly 2 of the 36 residues of p qualify.  Verified for all 36 nonzero
    g: every one admits exactly two.  So the null is 2/36 = 1/18 = 0.0556,
    not 1/12 = 0.0833.  (For g == 0 mod 37 the rate is 1; that is 0.033% of
    gaps.)

        predicted   0.00033 + (1 - 0.00033)/18  =  0.0559
        observed                                   0.0577
        ratio                                      1.032

    Against the correct baseline this is a 3% EXCESS, not a 31% deficit.
    "A prime's successor prefers a different orbit" inverts the sign of the
    effect by using 1/12.

    Worked case, g = 6: the two qualifying residues are 6/9 = 13 (CAS_EXT,
    and 13+6 = 19 is also CAS_EXT) and 6/25 = 18 (SEED, and 18+6 = 24 is
    also SEED).

=== THE 3-6-9 LADDER, FOR COMPLETENESS ===

    3+3=6, 6+3=9, 9+3=3      adding 3 cycles forward
    6+6=3, 3+6=9, 9+6=6      adding 6 cycles backward
    9+9=9                    adding 9 is the identity

    This is the ideal (3) = {3,6,9} in Z/9Z as a cyclic group of order 3
    under addition, with 9 == 0 as its neutral element.  Forced, and already
    the subject of T137 and T138 Part II.

=== FALSIFICATION ===
    A nonzero g mod 37 admitting other than exactly two qualifying p; or a
    QR/NR gap split not equal to the sign-weighted gap histogram.
"""

P = 37
ORBITS = {
    'IC': (1, 10, 26),      'DARK_A': (2, 15, 20),  'C3': (3, 4, 30),
    'CAS_EXT': (5, 13, 19), 'TESLA': (6, 8, 23),    'D7': (7, 33, 34),
    'SA_ST_A': (9, 12, 16), 'NEG_H': (11, 27, 36),  'C9': (14, 29, 31),
    'NQR17': (17, 22, 35),  'SEED': (18, 24, 32),   'SA_ST_B': (21, 25, 28),
}
BY = {r: n for n, o in ORBITS.items() for r in o}
QR = {(x * x) % P for x in range(1, P)}


def chi(d):
    d %= P
    return 0 if d == 0 else (1 if d in QR else -1)


def dr(n):
    return 1 + (n - 1) % 9


def run():
    from collections import Counter
    N = 10 ** 7
    s = bytearray([1]) * (N + 1)
    s[0:2] = b'\0\0'
    for i in range(2, int(N ** .5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    allp = [i for i in range(2, N) if s[i]]
    big = [p for p in allp if p > 37]
    assert len(allp) == 664579 and len(big) == 664567
    gaps = [b - a for a, b in zip(big, big[1:])]
    assert len(gaps) == 664566
    assert min(gaps) == 2 and max(gaps) == 154
    assert abs(sum(gaps) / len(gaps) - 15.047) < 0.001
    gc = Counter(gaps)
    assert (gc[2], gc[4], gc[6]) == (58975, 58617, 99985)

    # --- correction 1 ---
    qr = sum(1 for g in gaps if chi(g) == 1)
    nr = sum(1 for g in gaps if chi(g) == -1)
    assert (qr, nr) == (290196, 374150)
    assert abs(qr / nr - 0.7756) < 0.0001
    # the split IS the sign-weighted histogram, identically
    assert nr - qr == sum(c * (-chi(g)) for g, c in gc.items() if chi(g))
    assert gc[6] > nr - qr                       # gap 6 overshoots the total
    assert chi(2) == -1 and chi(3) == 1 and chi(6) == -1
    assert pow(2, 26, P) == 3                    # 3 = 2^26, even exponent

    # --- correction 2 ---
    for g in range(1, P):
        sol = [p for p in range(1, P)
               if (p + g) % P and BY[p] == BY[(p + g) % P]]
        assert len(sol) == 2, (g, sol)
    i9, i25 = pow(9, P - 2, P), pow(25, P - 2, P)
    assert sorted([(6 * i9) % P, (6 * i25) % P]) == [13, 18]
    assert BY[13] == BY[19] == 'CAS_EXT' and BY[18] == BY[24] == 'SEED'
    same = sum(1 for a, b in zip(big, big[1:]) if BY[a % P] == BY[b % P])
    rate = same / len(gaps)
    assert abs(rate - 0.0577) < 0.0002
    f0 = sum(1 for g in gaps if g % P == 0) / len(gaps)
    pred = f0 + (1 - f0) / 18
    assert abs(pred - 0.0559) < 0.0002
    assert 1.02 < rate / pred < 1.05             # excess, not deficit
    assert rate / (1 / 12) < 0.75                # the wrong null's "deficit"

    # --- the prime orbit distribution stands ---
    c = Counter(BY[p % P] for p in big)
    for o in ORBITS:
        assert abs(c[o] / (len(big) / 12) - 1) < 0.004, o

    # --- the 3-6-9 ladder ---
    assert dr(3 + 3) == 6 and dr(6 + 3) == 9 and dr(9 + 3) == 3
    assert dr(6 + 6) == 3 and dr(3 + 6) == 9 and dr(9 + 6) == 6
    assert dr(9 + 9) == 9
    assert all(dr(x + 9) == dr(x) for x in range(1, 37))

    print("All assertions passed.\n")
    print("THEOREM 347.  Two right numbers, two wrong nulls.\n")
    print(f"  reproduced: {len(allp):,} primes, {len(big):,} above 37,")
    print(f"  {len(gaps):,} gaps, mean {sum(gaps)/len(gaps):.3f}, max {max(gaps)},")
    print(f"  QR {qr:,} / NR {nr:,}, ratio {qr/nr:.4f}, self-trans {rate:.4f}")
    print("  every figure matches. The orbit distribution is a correct")
    print("  Dirichlet check and stands.\n")
    print("  CORRECTION 1 -- chi(g) is a deterministic function of g")
    print("    the QR/NR split is the gap histogram re-weighted by a sign;")
    print("    it holds no information the histogram lacks.")
    print(f"    gap 6 contributes {gc[6]:+,} of a total {nr-qr:+,} = "
          f"{gc[6]/(nr-qr)*100:.0f}%")
    print("    chi(6) = chi(2)chi(3) = (-1)(+1) = -1, since 2 is a primitive")
    print("    root and 3 = 2^26 has an even exponent.")
    print("    the bias is: the commonest gap is a non-residue.\n")
    print("  CORRECTION 2 -- the baseline is 1/18, not 1/12")
    print("    orbit(p) = orbit(p+g) needs 1 + g/p in <10>; for fixed g != 0")
    print("    that pins p to exactly 2 of 36 residues. Verified, all 36 g.")
    print(f"      predicted {pred:.4f}   observed {rate:.4f}   ratio {rate/pred:.3f}")
    print("    a 3% EXCESS against the right null, not a 31% deficit.")
    print("    g=6: the two are 13 (CAS_EXT, 13+6=19) and 18 (SEED, 18+6=24).")


if __name__ == "__main__":
    run()
