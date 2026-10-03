#!/usr/bin/env python3
"""
The chain a digit pair generates, with the closed forms that govern it.

    python3 chain.py pair 1 9
    python3 chain.py sweep [--primes]
    python3 chain.py grid 0 7 5
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import gf37 as G

ABBR = {'IC': 'IC', 'DARK_A': 'DKA', 'C3': 'C3', 'CAS_EXT': 'CAS',
        'TESLA': 'TSL', 'D7': 'D7', 'SA_ST_A': 'SAA', 'NEG_H': 'NGH',
        'C9': 'C9', 'NQR17': 'N17', 'SEED': 'SED', 'SA_ST_B': 'SAB',
        'SEAM': 'SEAM'}


def fac(n):
    if n < 2:
        return str(n)
    if G.is_prime(n):
        return "PRIME"
    return G.factor_str(n)


def pair(a, b):
    L, A = [], lambda s: L.append(s)
    ab, ba = 10*a + b, 10*b + a
    aba, bab = 101*a + 10*b, 101*b + 10*a
    abab, baba = 1010*a + 101*b, 1010*b + 101*a
    A("=" * 72)
    A(f"digit chain  a={a}  b={b}")
    A("=" * 72)
    A(f"  {'form':<6}{'value':>7}  {'factors':<20}{'mod37':>6}{'orbit':>7}"
      f"{'cls':>5}{'QR':>4}{'DR':>4}")
    for name, v in (('a', a), ('b', b), ('ab', ab), ('ba', ba),
                    ('aba', aba), ('bab', bab), ('abab', abab), ('baba', baba)):
        r = v % G.P
        qr = '-' if r == 0 else ('+' if pow(r, 18, G.P) == 1 else '-')
        A(f"  {name:<6}{v:>7}  {fac(v):<20}{r:>6}{ABBR[G.orbit(r)]:>7}"
          f"{(G.cls(r) if r else '-'):>5}{qr:>4}{G.dr(v):>4}")

    A("\n  closed forms (all forced):")
    A(f"    aba + bab  = {aba+bab:>6} = 111 x {a+b:<2} = 37 x {(aba+bab)//37}")
    A(f"    aba - bab  = {aba-bab:>6} =  91 x {a-b:<2} = 7 x 13 x {a-b}")
    ra, rb = aba % G.P, bab % G.P
    if a == b:
        A(f"    r_aba = r_bab = {ra}   both SEAM; no antipodal pair when a = b")
    else:
        A(f"    r_aba + r_bab = {ra} + {rb} = {ra+rb}"
          f"   antipodal: {G.antipode(G.orbit(ra)) == G.orbit(rb)}")
    A(f"    abab = 101 x {ab:<3} baba = 101 x {ba}")
    A(f"    abab + baba = {abab+baba:>6} = 1111 x {a+b}")
    A(f"    abab - baba = {abab-baba:>6} =  909 x {a-b}")
    if a == b:
        A(f"    a = b, so aba = 111a and the residue is SEAM")

    A("\n  contingent (not fixed by the forms):")
    pr = [(n, v) for n, v in (('ab', ab), ('ba', ba), ('aba', aba), ('bab', bab))
          if G.is_prime(v)]
    A(f"    primes among ab, ba, aba, bab: "
      f"{', '.join(f'{n}={v}' for n, v in pr) if pr else 'none'}")
    if G.is_prime(aba) and G.is_prime(bab):
        A(f"    BOTH palindromes prime — only 1,3 and 1,9 do this")
    for v in dict.fromkeys((aba, bab)):
        if v > 1:
            pre, per = G.period(v, 10)
            A(f"    1/{v}: pre {pre}, period {per}")
    tw = [(v, v+2) for v in (ab, aba, bab) if G.is_prime(v) and G.is_prime(v+2)]
    tw += [(v-2, v) for v in (ab, aba, bab) if G.is_prime(v) and G.is_prime(v-2)]
    if tw:
        A(f"    twin pairs: {tw}")
    return "\n".join(L)


def sweep(only_primes=False):
    L = []
    L.append(f"{'ab':>3} {'a,b':>4} {'aba':>4} {'bab':>4} {'aba factors':>13}"
             f" {'bab factors':>13} {'r':>3}{'orb':>5} {'r':>3}{'orb':>5} {'/37':>4} P")
    for n in range(10, 100):
        a, b = n // 10, n % 10
        aba, bab = 101*a + 10*b, 101*b + 10*a
        p = ("A" if G.is_prime(aba) else ".") + ("B" if G.is_prime(bab) else ".") \
            + ("n" if G.is_prime(n) else ".")
        if only_primes and p == "...":
            continue
        ra, rb = aba % G.P, bab % G.P
        L.append(f"{n:>3} {a},{b:<2} {aba:>4} {bab:>4} {fac(aba):>13} {fac(bab):>13}"
                 f" {ra:>3}{ABBR[G.orbit(ra)]:>5} {rb:>3}{ABBR[G.orbit(rb)]:>5}"
                 f" {(aba+bab)//37:>4} {p}")
    L.append("\nP: A = aba prime, B = bab prime, n = the two-digit ab prime")
    return "\n".join(L)


def grid(a, b, rows):
    import numpy as np
    L, A = [], lambda s: L.append(s)
    r1, r2 = f"{a}{b}{a}", f"{b}{a}{b}"
    A(f"alternating grid, digits {a} and {b}, {rows} rows")
    for i in range(rows):
        A("    " + (r1 if i % 2 == 0 else r2))
    A(f"\n  rows as numbers: {int(r1)} and {int(r2)}")
    A(f"  sum {int(r1)+int(r2)} = 111 x {a+b} = 37 x {(int(r1)+int(r2))//37}")
    M = [[int(c) for c in (r1 if i % 2 == 0 else r2)] for i in range(rows)]
    if rows >= 3 and rows % 2 == 1:
        A(f"  as a {rows}x3 matrix: row 1 = row 3, so rank <= 2 and det = 0")
        A(f"    forced for ANY two digits in this arrangement")
    for s, lab in ((r1*2, f"{r1}{r1}"), (r1+r2, f"{r1}{r2}")):
        v = [int(c) for c in s]
        P = np.abs(np.fft.fft(v))**2
        nz = [k for k in range(len(v)) if P[k] > 1e-9]
        A(f"  '{s}' length {len(v)}: DFT nonzero at {nz}"
          + ("  (DC + Nyquist only)" if len(nz) <= 2 else "  (full spectrum)"))
    A("  period-2 vectors are two-tone iff the length is even.")
    return "\n".join(L)


if __name__ == '__main__':
    v = sys.argv[1:]
    if not v:
        print(__doc__); sys.exit(1)
    if v[0] == 'pair':
        print(pair(int(v[1]), int(v[2])))
    elif v[0] == 'sweep':
        print(sweep('--primes' in v))
    elif v[0] == 'grid':
        print(grid(int(v[1]), int(v[2]), int(v[3]) if len(v) > 3 else 3))
    else:
        print(__doc__); sys.exit(1)
