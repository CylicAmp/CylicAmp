#!/usr/bin/env python3
"""
Decides whether a GF(37) claim is FORCED (carries no information) or
CONTINGENT (could have come back otherwise).

Four forcing mechanisms found across T237/T282/T285/T290/T297/T299/T302:

  partition    every residue lands in exactly one orbit
  homomorphism class positions always add; DR always multiplies
  tie          the "extreme" is not unique
  definition   the 137-map preserves every orbit, by definition

Usage:
  python3 forced.py factorization 246        # are the coset/DR checks forced?
  python3 forced.py tie <name> <json-counts> # is the extreme a tie?
  python3 forced.py tier <property>          # Tier A/B/C classification
  python3 forced.py orbit-claim <n> <ORBIT>  # information content of a hit
"""
import sys, os, json, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import gf37 as G


def check_factorization(n):
    """Coset-position and DR agreement across factorizations are forced."""
    out = [f"n = {n}, residue {n % G.P}, class {G.cls(n)}, DR {G.dr(n)}", ""]
    divs = [d for d in range(1, n + 1) if n % d == 0]
    pairs = [(a, n // a) for a in divs if a * a <= n
             and a % G.P and (n // a) % G.P]
    out.append(f"{'a':>7} {'b':>9} {'cls a':>6} {'cls b':>6} {'sum%12':>7} "
               f"{'cls n':>6} {'DR a':>5} {'DR b':>5} {'DRxDR':>6} {'DR n':>5}")
    bad = 0
    for a, b in pairs:
        cs = (G.cls(a) + G.cls(b)) % 12
        dd = G.dr(G.dr(a) * G.dr(b))
        if cs != G.cls(n) or dd != G.dr(n):
            bad += 1
        out.append(f"{a:>7} {b:>9} {G.cls(a):>6} {G.cls(b):>6} {cs:>7} "
                   f"{G.cls(n):>6} {G.dr(a):>5} {G.dr(b):>5} {dd:>6} {G.dr(n):>5}")
    out += ["",
            f"factorizations checked: {len(pairs)}, disagreements: {bad}",
            "",
            "VERDICT: FORCED (homomorphism).",
            "  class: F_37* -> Z/12Z is a group homomorphism (T285), so",
            "         positions add for every factorization of every integer",
            "         coprime to 37. No factorization could disagree.",
            "  DR:    Z -> Z/9Z is a ring homomorphism, so DRs multiply.",
            f"  The only fact with content is: {n} = {n % G.P} (mod 37), "
            f"class {G.cls(n)}, DR {G.dr(n)}.",
            "  Everything else on such a list follows from it.  (T215, T299)"]
    return "\n".join(out)


def check_tie(counts):
    """counts: dict label -> count. Are max/min unique?"""
    mx, mn = max(counts.values()), min(counts.values())
    top = sorted(k for k, v in counts.items() if v == mx)
    bot = sorted(k for k, v in counts.items() if v == mn)
    out = [f"max = {mx}, achieved by {len(top)}: {top}",
           f"min = {mn}, achieved by {len(bot)}: {bot}", ""]
    if len(top) > 1 or len(bot) > 1:
        out.append("VERDICT: TIE PRESENT — do NOT read an orbit off the extreme.")
        out.append("  Selecting one member of a tie and reporting its orbit is")
        out.append("  the T237 failure: the tie can span opposite ends of any")
        out.append("  scale you are testing, so no outcome counts as a miss.")
    else:
        out.append("VERDICT: extremes are unique. An orbit reading is admissible,")
        out.append("  provided the miss condition was stated before computing.")
    # uniformity
    n, k = sum(counts.values()), len(counts)
    exp = n / k
    chi2 = sum((v - exp) ** 2 / exp for v in counts.values())
    out += ["", f"n = {n} over {k} bins, expected {exp:.3f}",
            f"chi^2 = {chi2:.2f}, df = {k-1}, chi^2/df = {chi2/(k-1):.3f}",
            "  chi^2/df near or below 1 means the spread is consistent with",
            "  uniform: no bin is distinguished."]
    return "\n".join(out)


def check_tier(prop):
    """Which tier does a property live in? (T300)"""
    return "\n".join([
        f"property: {prop}", "",
        "TIER A — true for every prime p = 1 (mod 3). Not about 37.",
        "  mu_3 exists; orbits of size 3; (p-1)/3 of them; cyclic quotient;",
        "  fixed-point-free antipodal pairing; |P^1| = 2 + (p-1);",
        "  subgroup lattice above mu_3; gcd(6,p-1) j=0 classes; 4p=L^2+27M^2.",
        "",
        "TIER B — true for {7, 37, 73} only.  (T292)",
        "  ord_p(137) = 3, i.e. p | Phi_3(137) = 18907 = 7 x 37 x 73.",
        "  The ONLY tier where the number 137 does any work.",
        "",
        "TIER C — unique to 37 among all primes.  (T300)",
        "  p = n^2+1 for a CM unit count n: {5 (n=2), 17 (n=4), 37 (n=6)}.",
        "  Tier B and Tier C are INDEPENDENT lists meeting only at 37.",
        "",
        "Ask: does the property still hold at p=73? at p=101 (k=5)?",
        "  holds at both  -> Tier A, says nothing about 37",
        "  holds at 7,73  -> Tier B, a fact about 137",
        "  fails at both  -> candidate Tier C, verify against all primes",
    ])


def check_orbit_claim(n, name):
    """Information content of 'n lands in ORBIT'."""
    hit = G.orbit(n) == name
    out = [f"claim: {n} lands in {name}",
           f"actual orbit: {G.orbit(n)}   claim is {hit}", ""]
    out += ["information content:",
            "  P(a given residue lands in a given orbit) = 3/36 = 1/12",
            f"  log2(12) = {math.log2(12):.2f} bits IF the orbit was named in advance",
            "  0 bits if the orbit was read off after computing (T282)", "",
            "The orbit partition is COMPLETE: every residue lands somewhere.",
            "'n has an orbit' is never news. Only 'n has THIS orbit, predicted",
            "before computing' carries the 3.58 bits."]
    return "\n".join(out)


# ── mechanism 5: rendering ──────────────────────────────────────────────────

def check_digits(n):
    """Every forced base-10 fact about n. None of these carry information."""
    import numpy as np
    s = str(abs(n))
    d = [int(c) for c in s]
    L = ['-' * 68, f"rendering audit: {n}  ({len(s)} digits)", '-' * 68]
    A = L.append

    ds = sum(d)
    A(f"  digit sum {ds}, DR {(ds - 1) % 9 + 1}   FORCED: DR(n) = DR(digit sum)")
    alt = sum(x * (-1) ** i for i, x in enumerate(d))
    A(f"  alternating sum {alt}")
    if len(d) % 2 == 0:
        A(f"    even length, so n = {-alt % 11} mod 11 and n mod 11 = {n % 11}"
          f"   agree: {(-alt) % 11 == n % 11}   FORCED (10 = -1 mod 11)")
    else:
        A(f"    odd length, so n = {alt % 11} mod 11 and n mod 11 = {n % 11}"
          f"   agree: {alt % 11 == n % 11}   FORCED")

    if len(s) == 2:
        a, b = d
        A(f"  mirror {10*b+a}:  sum = {11*(a+b)} = 11 x {a+b}   FORCED")
    if len(s) == 3 and d[0] == d[2]:
        a, b = d[0], d[1]
        A(f"  palindrome aba; swap to bab gives {91*(a-b)} = 91 x {a-b}"
          f"   FORCED (91 = Phi_6(10) = 7 x 13)")

    if len(set(d)) == 1:
        A(f"  repdigit: {len(d)} copies of {d[0]}, digit sum {len(d)*d[0]}"
          f"   FORCED = k*d")
    if len(set(d)) == 2 and all(d[i] == d[i % 2] for i in range(len(d))):
        A(f"  period-2 alternation, length {len(d)}")
        P = np.abs(np.fft.fft(d)) ** 2
        nz = [k for k in range(len(d)) if P[k] > 1e-9]
        if len(d) % 2 == 0:
            A(f"    even length -> DFT nonzero only at {nz} (DC + Nyquist)  FORCED")
        else:
            A(f"    odd length -> DFT nonzero at {len(nz)} of {len(d)} bins;"
              f" 2 does not divide {len(d)}  FORCED")

    # comma grouping runs right to left, so slice from the right
    grp = [s[max(0, len(s) - i - 3):len(s) - i] for i in range(0, len(s), 3)][::-1]
    A(f"  comma groups (right to left, as printed): {','.join(grp)}")
    A(f"    substring occurrence is a rendering fact. Test divisibility:")
    for t in (37, 137, 111, 1001):
        A(f"      {t} | n : {n % t == 0}   (n mod {t} = {n % t})")

    A("  every line above is determined by the numeral's shape.")
    A("  substitute other digits in the same arrangement and each still holds.")
    return "\n".join(L)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(1)
    cmd = a[0]
    if cmd == 'factorization':
        print(check_factorization(int(a[1])))
    elif cmd == 'tie':
        print(check_tie(json.loads(a[1])))
    elif cmd == 'tier':
        print(check_tier(' '.join(a[1:]) or '(unnamed)'))
    elif cmd == 'orbit-claim':
        print(check_orbit_claim(int(a[1]), a[2]))
    elif a[0] == 'digits':
        print(check_digits(int(a[1])))
    else:
        print(__doc__); sys.exit(1)


