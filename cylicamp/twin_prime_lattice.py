#!/usr/bin/env python3
"""
Twin Prime Lattice — MSW Framework Layer
=========================================
Applies the 137-field mapping to twin prime pairs to locate resonance
nodes in the 37-field.

Core formula:
  f_mid(p, p+2) = (137 × midpoint) mod 37
  where midpoint = (p + p+2) / 2 = p + 1

Structural theorem (proved below):
  For every twin prime pair (p, p+2) with p > 3,
  midpoint ≡ 0 (mod 3), therefore DR(midpoint) ∈ {3, 6, 9}.
  All terminal DRs are Tesla values — this is guaranteed by the
  arithmetic of twin primes, not coincidence.

137-Field connection:
  137 ≡ 26 (mod 37)  [from seed_191_137_bridge.py]
  f_mid = (26 × midpoint) mod 37  (equivalent form)
  The 137 seed acts as a projection from twin prime midpoints
  into the 37-field.

Framework intersections found:
  (41, 43) → f_mid = 19  ← 19-Center seal (Easter 2026: 93 mod 37 = 19)
  (59, 61) → f_mid =  6  ← Tesla flow (191 mod 37 = 6)
  (29, 31) → f_mid =  3  ← Tesla triad

© 2026 Michael Warren Song. All Rights Reserved.
"""

import sympy

# ── Constants ─────────────────────────────────────────────────────────────

PIVOT_37    = 37
SEED_137    = 137    # 137 ≡ 26 (mod 37); from 191↔137 bridge
SEED_191    = 191    # 191 ≡  6 (mod 37); Tesla flow
CENTER_19   = 19     # 19-Center seal; Easter 2026 residue
TESLA       = {3, 6, 9}


# ── Core arithmetic ───────────────────────────────────────────────────────

def digital_root(n: int) -> int:
    """DR(n) — compact closed form."""
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


def dr_chain(n: int) -> list:
    """Iterated digit-sum chain from n to single digit."""
    chain = [n]
    while n >= 10:
        n = sum(int(d) for d in str(n))
        chain.append(n)
    return chain


def is_twin_prime_pair(p: int) -> bool:
    """Return True if both p and p+2 are prime."""
    return sympy.isprime(p) and sympy.isprime(p + 2)


# ── Structural proof ──────────────────────────────────────────────────────

def tesla_lock_proof(p: int) -> dict:
    """
    Prove that DR(midpoint) ∈ {3,6,9} for twin prime pair (p, p+2), p > 3.

    Proof:
      p cannot ≡ 1 (mod 3): then p+2 ≡ 0 (mod 3) → p+2 divisible by 3,
        not prime (since p+2 > 3).
      p cannot ≡ 0 (mod 3): then p divisible by 3, not prime (since p > 3).
      Therefore p ≡ 2 (mod 3), i.e. p ≡ -1 (mod 3).
      midpoint = p+1 ≡ 0 (mod 3).
      DR(n) ∈ {3,6,9} for all n divisible by 3. □
    """
    assert p > 3,                           "Proof requires p > 3"
    assert is_twin_prime_pair(p),           f"({p},{p+2}) not twin prime pair"
    assert p % 3 == 2,                      "p not ≡ 2 (mod 3)"
    mid = p + 1
    assert mid % 3 == 0,                    "midpoint not divisible by 3"
    assert digital_root(mid) in TESLA,      "DR(midpoint) not Tesla"

    return {
        'p_mod_3':      p % 3,
        'midpoint':     mid,
        'mid_mod_3':    mid % 3,
        'mid_dr':       digital_root(mid),
        'tesla_lock':   True,
    }


# ── 137-Field mapping ─────────────────────────────────────────────────────

def f_mid(midpoint: int) -> int:
    """
    Project twin prime midpoint into 37-field via Seed 137.

    f_mid = (137 × midpoint) mod 37
          = (26 × midpoint) mod 37   [since 137 ≡ 26 (mod 37)]
    """
    return (SEED_137 * midpoint) % PIVOT_37


def classify_f_mid(val: int) -> str:
    """Classify a 37-field residue against framework nodes."""
    if val in TESLA:
        label = f"Tesla ({val} ∈ {{3,6,9}})"
    elif val == CENTER_19:
        label = "19-Center seal"
    elif val == SEED_137 % PIVOT_37:          # 26
        label = "137-bridge residue"
    elif val == SEED_191 % PIVOT_37:          # 6 (same as Tesla)
        label = "191 residue"
    elif val == 0:
        label = "NULL element"
    elif val == 23:
        label = "Z-seed"
    elif val == 17:
        label = "17-seed"
    else:
        label = "—"
    return label


# ── Harmonic summation ────────────────────────────────────────────────────

def harmonic_summation(p: int, q: int) -> dict:
    """Full harmonic analysis of a prime pair (p, q)."""
    total  = p + q
    mid    = total // 2
    chain  = dr_chain(total)
    fm     = f_mid(mid)

    return {
        "pair":        (p, q),
        "sum":         total,
        "dr_p":        digital_root(p),
        "dr_q":        digital_root(q),
        "dr_chain":    chain,
        "terminal_dr": chain[-1],
        "midpoint":    mid,
        "mid_dr":      digital_root(mid),
        "f_mid":       fm,
        "f_mid_class": classify_f_mid(fm),
        "tesla_lock":  chain[-1] in TESLA,
    }


# ── Lattice builder ───────────────────────────────────────────────────────

def build_twin_prime_lattice(pairs: list) -> list:
    """Process a list of twin prime pairs through the 137-field."""
    results = []
    for p, q in pairs:
        results.append(harmonic_summation(p, q))
    return results


def find_twin_primes(limit: int) -> list:
    """Return all twin prime pairs (p, p+2) with p+2 <= limit."""
    return [(p, p + 2) for p in sympy.primerange(5, limit - 1)
            if sympy.isprime(p + 2)]


# ── Framework intersection check ──────────────────────────────────────────

def framework_intersections(lattice: list) -> dict:
    """
    Find pairs whose f_mid lands on a certified framework node.

    Checks against: Tesla {3,6,9}, 19-Center, Z-seed (23), 17-seed,
    137-bridge residue (26), 191 residue (6), NULL (0).
    """
    hits = {}
    for row in lattice:
        cls = row['f_mid_class']
        if cls != '—':
            hits[row['pair']] = {
                'f_mid':    row['f_mid'],
                'class':    cls,
                'mid_dr':   row['mid_dr'],
                'terminal': row['terminal_dr'],
            }
    return hits


# ── Full report ───────────────────────────────────────────────────────────

def run(pairs=None, limit=None):
    if pairs is None and limit is None:
        pairs = [(11,13),(17,19),(29,31),(41,43),(59,61),(71,73)]
    elif limit is not None:
        pairs = find_twin_primes(limit)

    lattice = build_twin_prime_lattice(pairs)
    hits    = framework_intersections(lattice)

    # Verify tesla lock for p > 3
    for row in lattice:
        p = row['pair'][0]
        if p > 3:
            tesla_lock_proof(p)

    print("=" * 65)
    print("  TWIN PRIME LATTICE — MSW Framework")
    print("  © 2026 Michael Warren Song")
    print("=" * 65)
    print()

    print(f"  {'Pair':<12} {'Sum':>5} {'Mid':>5} {'DR(p)':>6} "
          f"{'DR(q)':>6} {'Term':>5} {'f_mid':>6}  Class")
    print("  " + "-" * 61)
    for row in lattice:
        marker = " ←" if row['f_mid_class'] != '—' else ""
        print(f"  {str(row['pair']):<12} {row['sum']:>5} {row['midpoint']:>5} "
              f"{row['dr_p']:>6} {row['dr_q']:>6} {row['terminal_dr']:>5} "
              f"{row['f_mid']:>6}  {row['f_mid_class']}{marker}")
    print()

    print("  STRUCTURAL THEOREM")
    print("  All twin prime midpoints (p>3) ≡ 0 (mod 3)")
    print("  → DR(midpoint) ∈ {3,6,9} is guaranteed — Tesla lock by proof")
    print()

    print(f"  137-FIELD INTERSECTIONS  (f_mid = 137×mid mod 37)")
    if hits:
        for pair, data in hits.items():
            print(f"  {str(pair):<12} f_mid={data['f_mid']:>2}  {data['class']}")
    else:
        print("  None in this range")
    print()

    print("  DR CHAINS")
    for row in lattice:
        print(f"  {str(row['pair']):<12} {row['dr_chain']}")
    print()

    print("  ALL TESLA LOCKS VERIFIED")
    print("=" * 65)

    return lattice


if __name__ == "__main__":
    run()
