#!/usr/bin/env python3
"""
Runs METHOD.md's fixed sequence plus CLAUDE.md's standing analysis on any
number. Reports everything without filtering.

    python3 audit.py 246 [more numbers...]

Improvements over v1, each prompted by a gap found while auditing:
  - antipodal residue and block shown, with the 999 block-sum check
  - block-map position (T303): B(k)=27k, cycles are the antipodal pairs
  - RH reported at BOTH residue and orbit level (v1 gave residue only,
    which read as "no hit" when the orbit had hits elsewhere)
  - named-set line no longer prints UNNAMED for numbers that do have an
    orbit name; SA/ST/CASCADE membership is stated separately
  - Sophie Germain chain, not just the boolean
  - orbit chamber profile (chi_-3 splits inside an orbit)
  - QR status mod 37
  - SEAM numbers get cofactor and 10^d-1 analysis instead of a blank
  - repeat residues across one invocation are flagged

Caught a v1-era error on first run: at 13 the orbit chambers are
{5:5, 13:1, 19:1}, not "5 and 19 chamber 5". The orbit-level view makes
that visible where the single-number view did not.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import gf37 as G

QR = {(i * i) % G.P for i in range(1, G.P)}
B_MULT = 27          # T303: block(k) = 27k, B = x27 mod 37


def block_cycle(r):
    """T303 block-map cycle containing r, in order from r."""
    c, x = [r], (B_MULT * r) % G.P
    while x != r:
        c.append(x)
        x = (B_MULT * x) % G.P
    return c


def sg_chain(n):
    """Sophie Germain chain through n: ... -> (n-1)/2 -> n -> 2n+1 -> ..."""
    down = []
    x = n
    while x % 2 == 1 and G.is_prime((x - 1) // 2) and (x - 1) // 2 > 1:
        x = (x - 1) // 2
        down.append(x)
    up = []
    x = n
    while G.is_prime(2 * x + 1):
        x = 2 * x + 1
        up.append(x)
    return list(reversed(down)) + [n] + up


def audit(n, seen_residues=None):
    r = n % G.P
    o = G.orbit(n)
    L = []
    A = L.append

    A("=" * 70)
    A(f"n = {n}")
    A("=" * 70)

    # ── Steps 1-3 ───────────────────────────────────────────────────────
    A(f"  [1] n mod 37          = {r}")
    if seen_residues is not None and r in seen_residues:
        A(f"      (same residue as {seen_residues[r]} audited above — all")
        A(f"       mod-37 rows below will be identical)")

    sets = G.named_sets(n)
    A(f"  [2] SA/ST/CASCADE     = {sets if sets else 'none'}")
    if r:
        A(f"      orbit name        = {o}")
    A(f"  [3] orbit             = {o}" + (f"  {G.orbit_triple(n)}" if r else ""))

    if r:
        t = G.orbit_triple(n)
        anti_r = (-r) % G.P
        anti_o = G.antipode(o)
        A(f"      position          = {t.index(r)} of 3")
        A(f"      Z/12Z class       = {G.cls(n)}")
        A(f"      QR mod 37         = {'yes' if r in QR else 'no'}")
        A(f"      block             = {G.block(r)}   (= 27 x {r})")
        A(f"      orbit blocks      = {[G.block(x) for x in t]}")
        A(f"      antipode          = {anti_r} ({anti_o}), block {G.block(anti_r)}")
        bs = int(G.block(r)) + int(G.block(anti_r))
        A(f"      block sum         = {G.block(r)} + {G.block(anti_r)} = {bs}"
          f"  {'(= 999, forced)' if bs == 999 else '(EXPECTED 999)'}")
        cyc = block_cycle(r)
        A(f"      block-map cycle   = {cyc}   (T303, length {len(cyc)})")
        A(f"                          orbits {[G.orbit(v) for v in cyc]}")

    # ── Step 4 ──────────────────────────────────────────────────────────
    if n >= 0:
        A(f"  [4] DR                = {G.dr(n)}   basin = {G.dr_basin(n)}")
        A(f"      DR mod 3 = {G.dr(n)%3}, n mod 3 = {n%3}  "
          f"(equal: {G.dr(n)%3 == n%3})")
    else:
        A(f"  [4] DR                = undefined for n < 0")
        A(f"      mod 9             = {G.mod9(n)}   "
          f"(signed class; DR is not defined here)")

    # ── Step 5 ──────────────────────────────────────────────────────────
    A(f"  [5] mod 2,3,6,9       = {n%2}, {n%3}, {n%6}, {n%9}")

    # ── Step 6 ──────────────────────────────────────────────────────────
    p = G.prime_profile(n)
    if p['prime']:
        A(f"  [6] prime             = True   twin={p['twin']} "
          f"cousin={p['cousin']} sexy={p['sexy']}")
        A(f"      Sophie Germain    = {p['sophie_germain']} (2n+1={2*n+1})   "
          f"safe = {p['safe']}")
        ch = sg_chain(n)
        if len(ch) > 1:
            A(f"      SG chain          = {' -> '.join(map(str, ch))}")
        A(f"      chamber (mod 6)   = {p['chamber']}  "
          f"(chi_-3 = {'+1' if p['chamber']==1 else '-1'})")
    else:
        A(f"  [6] prime             = False   factorization = {G.factor(n)}")

    if r:
        chambers = {x: x % 6 for x in G.orbit_triple(n)}
        A(f"      orbit chambers    = {chambers}")

    # ── standing analysis ───────────────────────────────────────────────
    A("  --- standing analysis ---")
    if r:
        hits_r = G.rh_hits(r)
        hits_o = sorted(i for x in G.orbit_triple(n) for i in G.rh_hits(x))
        A(f"  RH   residue {r}: gamma_n = {hits_r or 'none in first 30'}")
        A(f"       orbit {o}: gamma_n = {hits_o or 'none in first 30'}")
        inv = pow(26, -1, G.P)
        A(f"  137  n x137 = {(n*137)%G.P} ({G.orbit(n*137)}),  "
          f"n /137 = {(r*inv)%G.P} ({G.orbit(r*inv)})")
        A(f"       n mod 137 = {n%137}")
        r30 = G.rule30(n)
        same = ' <- stays in orbit' if G.orbit(r30) == o else ''
        A(f"  R30  {n%256:08b} -> {r30:08b} = {r30}, mod 37 = {r30%G.P} "
          f"({G.orbit(r30)}){same}")
    else:
        cof = n // G.P
        A(f"  SEAM: 37 | {n}. No orbit, no class. Rotation axis (T302).")
        A(f"  cofactor n/37 = {cof} = {G.factor(cof) if cof > 1 else '1'}")
        for d in (3, 6, 9):
            if (10 ** d - 1) % n == 0:
                A(f"  n divides 10^{d}-1 = {10**d-1}")
        if n % 111 == 0:
            A(f"  n = {n//111} x 111, and 111 = Phi_3(10) = 3 x 37 (T302)")

    # ── decimal / cyclotomic (T301-T304) ────────────────────────────────
    A("  --- decimal period and cyclotomic slot (T301-T304) ---")
    if n > 1:
        pre10, per10 = G.period(n, 10)
        pre2,  per2  = G.period(n, 2)
        def _p(x):
            return 'terminates' if x == 0 else ('unknown (search bound)' if x < 0 else x)
        A(f"  1/{n}  base 10: pre={pre10} period={_p(per10)}"
          f"   base 2: pre={pre2} period={_p(per2)}")
        for base, per in ((10, per10), (2, per2)):
            if per <= 0:
                continue
            comp = "  (halves complementary)" if G.complement_halves(1, n, base) else ""
            rp = G.repetend(1, n, base, max_len=240)
            if rp is None:
                A(f"       block base {base:>2} = period {per}, not printed{comp}")
            else:
                A(f"       block base {base:>2} = {rp}{comp}")
        if per10 > 0:
            slot = G.order_slot(10, per10)
            if slot is None:
                A(f"       Phi_{per10}(10) has degree {G.totient(per10)} — "
                  f"too large to factor here, slot not computed")
            else:
                A(f"       Phi_{per10}(10) = {G.phi_d(per10, 10)} = "
                  f"{G.factor_str(G.phi_d(per10, 10))}"
                  f"   -> primes of period {per10}: {slot}")
            if slot == [n]:
                A(f"       {n} is the ONLY prime with decimal period {per10}")
            elif slot is not None and not G.is_prime(n):
                q = n
                for pp in G.factor(10):
                    while q % pp == 0:
                        q //= pp
                A(f"       n = {G.factor_str(n)}; part coprime to 10 is {q}"
                  f" = {G.factor_str(q)}, and ord_{q}(10) = {per10}")
    if G.is_prime(n):
        ls = G.lists_containing(n)
        A(f"  complete lists containing {n}: {ls or 'none'}"
          f"   (L1 ord_p(137)=3 {G.L1_ORD137}, L2 p=n^2+1 {G.L2_CM}, "
          f"L3 ord_p(10)=3 {G.L3_ORD10})")
        for d in (1, 2, 3, 4, 6, 8):
            if G.phi_d(d, 137) % n == 0 and 137 % n:
                A(f"  n | Phi_{d}(137) = {G.phi_d(d,137)}  -> ord_{n}(137) = "
                  f"{G.order_mod(137, n)}")

    # ── forced facts ────────────────────────────────────────────────────
    A("  --- forced, carries no information (T282) ---")
    A("  * orbit membership: the partition is complete")
    A("  * the 137-map preserves every orbit, by definition")
    if r:
        A("  * class(a)+class(b) = class(ab) for EVERY factorization (T285)")
        A("  * DR(a)*DR(b) = DR(ab) mod 9 for EVERY factorization")
        A(f"  * block({r}) = 27 x {r}; the decimal route adds nothing (T303)")
        A("  * the block sum with the antipode is 999 for every pair")
    return "\n".join(L)


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    seen = {}
    for a in args:
        n = int(a)
        print(audit(n, seen))
        print()
        seen.setdefault(n % G.P, n)
