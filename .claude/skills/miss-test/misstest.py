#!/usr/bin/env python3
"""
T282 miss-test harness. Refuses to evaluate a claim until a miss condition
has been declared, then measures whether that condition could actually fire.

  python3 misstest.py declare "<claim>" "<miss condition>"
  python3 misstest.py sweep <expr> <domain>    # what fraction of the domain passes?
  python3 misstest.py orbit-uniform '<json counts>'

sweep example — is "x^3+5 is QR" selective over F_37*?
  python3 misstest.py sweep "pow(x,3,37)+5" qr
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import gf37 as G

QR = {(i * i) % G.P for i in range(1, G.P)}


def declare(claim, miss):
    return "\n".join([
        "=" * 66,
        "MISS-TEST DECLARATION  (T282)",
        "=" * 66,
        f"  CLAIM: {claim}",
        f"  MISS:  {miss}",
        "",
        "Before computing, answer these. If any answer is 'no', the test is",
        "vacuous and the result carries 0 bits regardless of how it comes out.",
        "",
        "  1. Is there a concrete outcome that would count as a miss?",
        "  2. Was the target named BEFORE the computation ran?",
        "  3. Would the claim survive at p=73 (Tier A) or is it specific?",
        "  4. Is the claim forced by a homomorphism, a complete partition,",
        "     a definition, or a tie?   (run forced-check)",
        "  5. If it fails, will the failure be recorded rather than dropped?",
        "",
        "Known vacuous patterns:",
        "  - 'n lands in an orbit'            partition is complete",
        "  - 'the 137-map preserves orbit X'  true of every orbit by definition",
        "  - 'factorizations agree on class'  homomorphism, always true",
        "  - 'DRs multiply correctly'         homomorphism, always true",
        "  - 'the extreme block maps to X'    check for ties first (T237)",
        "  - 'n + reverse(n) = repdigit'      true for every 2-digit n",
    ])


def sweep(expr, domain):
    """Fraction of F_37* for which expr(x) satisfies the domain predicate."""
    pred = {
        'qr':     lambda v: v % G.P in QR,
        'nqr':    lambda v: v % G.P not in QR and v % G.P != 0,
        'seam':   lambda v: v % G.P == 0,
        'prime':  lambda v: G.is_prime(v),
    }.get(domain)
    if pred is None:
        return f"unknown domain '{domain}'. use qr|nqr|seam|prime"
    hits, tot, byorb = [], 0, {}
    for x in range(1, G.P):
        v = eval(expr, {'x': x, 'pow': pow, 'G': G})
        tot += 1
        if pred(v):
            hits.append(x)
            byorb[G.orbit(x)] = byorb.get(G.orbit(x), 0) + 1
    frac = len(hits) / tot
    L = [f"expr   : {expr}",
         f"domain : {domain}",
         f"hits   : {len(hits)}/{tot} = {frac:.4f}",
         f"by orbit: {dict(sorted(byorb.items()))}", ""]
    if frac > 0.95:
        L.append("VERDICT: VACUOUS — almost everything passes. Not a test.")
    elif frac < 0.05:
        L.append("VERDICT: near-empty — check the predicate is what you meant.")
    else:
        L.append(f"VERDICT: SELECTIVE. A hit carries about "
                 f"{-__import__('math').log2(frac):.2f} bits,")
        L.append("         but only if the target was named in advance.")
    # orbit-uniformity of the hit set
    if byorb:
        full = [o for o in G.ORBITS if o in byorb and byorb[o] == 3]
        L.append(f"orbits fully inside the hit set: {sorted(full)} "
                 f"({len(full)}/12)")
        L.append("  a hit set that is a union of whole orbits is orbit-invariant;")
        L.append("  that is a real structural property (cf. T287).")
    return "\n".join(L)


def orbit_uniform(counts):
    """Chi-square a distribution over the 12 orbits."""
    c = {o: counts.get(o, 0) for o in G.ORBITS}
    n = sum(c.values())
    exp = n / 12
    chi2 = sum((v - exp) ** 2 / exp for v in c.values())
    L = [f"{'orbit':>9} {'count':>6}"]
    for o in G.CLASS_ORDER:
        L.append(f"{o:>9} {c[o]:>6}")
    L += ["", f"n = {n}, expected {exp:.3f} per orbit",
          f"chi^2 = {chi2:.2f}, df = 11, chi^2/df = {chi2/11:.3f}", ""]
    if chi2 / 11 < 1.5:
        L.append("VERDICT: consistent with uniform. No orbit is distinguished.")
        L.append("  Reporting one orbit from this spread is post-hoc selection.")
    else:
        L.append("VERDICT: deviates from uniform. Identify the mechanism before")
        L.append("  claiming structure — check ties, then check p=73.")
    return "\n".join(L)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(1)
    if a[0] == 'declare':
        print(declare(a[1], a[2] if len(a) > 2 else '(NONE GIVEN — test is vacuous)'))
    elif a[0] == 'sweep':
        print(sweep(a[1], a[2]))
    elif a[0] == 'orbit-uniform':
        print(orbit_uniform(json.loads(a[1])))
    else:
        print(__doc__); sys.exit(1)
