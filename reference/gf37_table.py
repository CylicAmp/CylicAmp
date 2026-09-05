#!/usr/bin/env python3
"""Complete GF(37) reference table. Regenerates reference/gf37_table.txt."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '.claude', 'skills'))
import gf37 as G

QR = {(i * i) % 37 for i in range(1, 37)}

def build():
    L = []
    L.append("GF(37) COMPLETE REFERENCE TABLE")
    L.append("")
    L.append("r     residue 1..36")
    L.append("orbit 137-map orbit (T285)          cls   Z/12Z class")
    L.append("pos   position in orbit             blk   decimal block of r/37 = 27r (T303)")
    L.append("anti  antipode 37-r (T283)          ablk  antipode's block; blk+ablk = 999")
    L.append("QR    quadratic residue mod 37      DR    digital root")
    L.append("ch    chamber r mod 6               p?    prime")
    L.append("r30   Rule 30 image mod 37          RH    n with floor(gamma_n) = r, n <= 30")
    L.append("")
    L.append(f"{'r':>3} {'orbit':>8} {'cls':>4} {'pos':>4} {'blk':>4} {'anti':>5} "
             f"{'ablk':>5} {'QR':>3} {'DR':>3} {'ch':>3} {'p?':>3} {'r30':>4} {'RH':>10}")
    for r in range(1, 37):
        t = G.orbit_triple(r)
        a = (-r) % 37
        hits = G.rh_hits(r)
        L.append(f"{r:>3} {G.orbit(r):>8} {G.cls(r):>4} {t.index(r):>4} "
                 f"{G.block(r):>4} {a:>5} {G.block(a):>5} "
                 f"{('Y' if r in QR else 'n'):>3} {G.dr(r):>3} {r%6:>3} "
                 f"{('Y' if G.is_prime(r) else 'n'):>3} {G.rule30(r)%37:>4} "
                 f"{str(hits) if hits else '-':>10}")
    L.append("")
    L.append("SEAM: r = 0 (37 | n). No orbit, no class, no block.")
    L.append("")
    L.append("ORBITS")
    for name in G.CLASS_ORDER:
        s = sorted(G.ORBITS[name])
        L.append(f"  {name:>8}  cls {G.cls(s[0]):>2}  {s}  blocks "
                 f"{[G.block(x) for x in s]}  antipode {G.antipode(name)}")
    L.append("")
    L.append("ANTIPODAL PAIRS (T283) — class distance 6, blocks sum to 999")
    for a, b in G.ANTIPODAL:
        L.append(f"  {a:>8} <-> {b:<8}  cls {G.cls(min(G.ORBITS[a])):>2} / "
                 f"{G.cls(min(G.ORBITS[b])):>2}")
    L.append("")
    L.append("BLOCK-MAP CYCLES (T303) — B(k) = 27k, six 6-cycles = the antipodal pairs")
    seen = set()
    for s in range(1, 37):
        if s in seen:
            continue
        c, x = [s], (27 * s) % 37
        while x != s:
            c.append(x); x = (27 * x) % 37
        seen |= set(c)
        L.append(f"  {str(c):<28} {G.orbit(c[0])} / {G.orbit(c[1])}")
    L.append("")
    L.append("CONSTANTS")
    L.append(f"  137 mod 37 = {137%37} = 10^2 mod 37     ord_37(26) = 3")
    L.append(f"  ord_37(10) = 3   ord_37(2) = 36   ord_37(27) = 6")
    L.append(f"  Phi_3(10) = 111 = 3 x 37           Phi_3(137) = 18907 = 7 x 37 x 73")
    L.append(f"  999 = 27 x 37                      block(k) = 27k exactly")
    return "\n".join(L)

if __name__ == '__main__':
    out = build()
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gf37_table.txt')
    with open(path, 'w') as f:
        f.write(out + "\n")
    print(out)
