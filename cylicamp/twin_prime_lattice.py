#!/usr/bin/env python3
"""
Twin Prime Lattice — MSW Framework Layer
=========================================
Applies the 137-field mapping to twin prime pairs to locate resonance
nodes in the 37-field.

Core formula:
  f_mid(p, p+2) = (137 × midpoint) mod 37
  where midpoint = (p + p+2) / 2 = p + 1

Note on terminal_dr: terminal_dr = DR(p + q) = DR(p + p+2) = DR(2p+2).
  This is the iterated digit sum of the pair sum, reduced to one digit.

Structural laws (proved — not observed):

  Law 1: mid_dr = dr_p + 1  for all twin prime pairs (p, p+2)
    Proof: p > 3 → p ≡ 2 (mod 3) → DR(p) ∈ {2,5,8} (never 9)
           DR(p+1) = DR(p)+1 holds whenever DR(p) ≠ 9. □
    Verified: holds for all 20 pairs including (3,5).

  Law 2: terminal_dr + dr_q = 10  for all twin prime pairs with p ≥ 5
    Proof: p = 6k−1 for integer k ≥ 1 (all primes > 3 are ≡ ±1 mod 6;
           p ≡ 1 would make p+2 ≡ 0 mod 3, not prime).
           terminal_dr = DR(12k),  dr_q = DR(6k+1).
           k≡1(mod 3): DR(3k)=3, DR(6k+1)=7 → sum=10 ✓
           k≡2(mod 3): DR(3k)=6, DR(6k+1)=4 → sum=10 ✓
           k≡0(mod 3): DR(3k)=9, DR(6k+1)=1 → sum=10 ✓  □
    Exception: (3,5) → sum=13 (p=3 does not fit 6k−1 form).

  Law 3: last digit of p×q ∈ {3, 9}  for all twin prime pairs with p > 5
    Proof: p > 5 prime ⟹ p ends in {1,3,7,9}.
           If last(p)=3 then last(p+2)=5, so p+2 divisible by 5 — not prime.
           If last(p)=5 then p divisible by 5 — not prime (p>5).
           So last(p) ∈ {1, 7, 9} for p > 5 twin primes.
           last(p)=1 ⟹ last(q)=3 ⟹ last(p×q) = 1×3 mod 10 = 3
           last(p)=7 ⟹ last(q)=9 ⟹ last(p×q) = 7×9 mod 10 = 3
           last(p)=9 ⟹ last(q)=1 ⟹ last(p×q) = 9×1 mod 10 = 9
           ∴ last(p×q) ∈ {3,9} ⊂ Tesla {3,6,9}. Tesla lock on product. □
    Exception: (3,5) last=5; (5,7) last=5.

137-Field connection:
  137 ≡ 26 (mod 37)  [from seed_191_137_bridge.py]
  f_mid = (26 × midpoint) mod 37  (equivalent form)
  The 137 seed acts as a projection from twin prime midpoints
  into the 37-field.

Framework intersections (first 20 pairs):
  (29,  31) → f_mid =  3  ← Tesla triad
  (41,  43) → f_mid = 19  ← 19-Center seal (Easter 2026: 93 mod 37 = 19)
  (59,  61) → f_mid =  6  ← Tesla flow (191 mod 37 = 6)
  (137,139) → f_mid = 36  ← inverse unity (36 ≡ −1 mod 37); self-referential
  (191,193) → f_mid = 34  ← Seed 191 appears as its own twin prime

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

def verify_laws(p: int) -> dict:
    """
    Verify all three structural laws for twin prime pair (p, p+2).

    Law 1: DR(midpoint) = DR(p) + 1  (all p)
    Law 2: DR(sum) + DR(p+2) = 10    (p ≥ 5)
    Law 3: last digit of p×(p+2) ∈ {3,9}  (p > 5)
    """
    assert is_twin_prime_pair(p), f"({p},{p+2}) not twin prime pair"
    q     = p + 2
    mid   = p + 1
    total = p + q
    chain = dr_chain(total)
    term  = chain[-1]
    dp    = digital_root(p)
    dq    = digital_root(q)
    dm    = digital_root(mid)

    law1 = dm == dp + 1
    law2 = (term + dq == 10) if p >= 5 else None   # (3,5) is exception
    last_prod = (p * q) % 10
    law3 = (last_prod in {3, 9}) if p > 5 else None  # (3,5),(5,7) exceptions

    assert law1, f"Law 1 failed for p={p}: mid_dr={dm}, dr_p+1={dp+1}"
    if law2 is not None:
        assert law2, f"Law 2 failed for p={p}: term={term}, dr_q={dq}"
    if law3 is not None:
        assert law3, f"Law 3 failed for p={p}: last(p×q)={last_prod} not in {{3,9}}"

    return {
        'p_mod_3':       p % 3,
        'mid_dr':        dm,
        'dr_p_plus1':    dp + 1,
        'law1':          law1,
        'term_plus_drq': term + dq if p >= 5 else None,
        'law2':          law2,
        'last_p':        p % 10,
        'last_q':        q % 10,
        'last_pxq':      last_prod,
        'law3':          law3,
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
    chain  = dr_chain(total)   # terminal_dr = DR(p+q)
    fm     = f_mid(mid)
    prod   = p * q

    return {
        "pair":        (p, q),
        "sum":         total,
        "dr_p":        digital_root(p),
        "dr_q":        digital_root(q),
        "dr_chain":    chain,
        "terminal_dr": chain[-1],      # DR(p+q) = DR(2p+2)
        "midpoint":    mid,
        "mid_dr":      digital_root(mid),
        "f_mid":       fm,
        "f_mid_class": classify_f_mid(fm),
        "tesla_lock":  chain[-1] in TESLA,
        "last_p":      p % 10,
        "last_q":      q % 10,
        "last_pxq":    prod % 10,
        "product_tesla": prod % 10 in TESLA,
    }


def last_digit_analysis(lattice: list) -> dict:
    """
    Tabulate last-digit patterns across the lattice.

    Law 3 proved: for p > 5, last(p×q) ∈ {3,9} ⊂ Tesla {3,6,9}.

    Pattern key:
      last(p)=1 → last(q)=3 → last(p×q)=3
      last(p)=7 → last(q)=9 → last(p×q)=3
      last(p)=9 → last(q)=1 → last(p×q)=9
    """
    counts = {}
    for row in lattice:
        pattern = (row['last_p'], row['last_q'], row['last_pxq'])
        counts[pattern] = counts.get(pattern, 0) + 1

    all_tesla = all(row['product_tesla'] or row['pair'][0] <= 5
                    for row in lattice)
    return {
        'pattern_counts':     counts,
        'all_product_tesla':  all_tesla,
        'law3_verified':      all_tesla,
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

    lattice  = build_twin_prime_lattice(pairs)
    hits     = framework_intersections(lattice)
    ld_stats = last_digit_analysis(lattice)

    # Verify all three structural laws
    for row in lattice:
        p = row['pair'][0]
        verify_laws(p)

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

    print("  STRUCTURAL THEOREMS")
    print("  All twin prime midpoints (p>3) ≡ 0 (mod 3)")
    print("  → DR(midpoint) ∈ {3,6,9} is guaranteed — Tesla lock by proof")
    print("  terminal_dr = DR(p+q) = DR(2p+2)")
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

    print("  LAST DIGIT ANALYSIS (Law 3)")
    print(f"  {'Pair':<12} {'last_p':>6} {'last_q':>6} {'last_p×q':>9}  Tesla?")
    print("  " + "-" * 42)
    for row in lattice:
        tesla = "Tesla ✓" if row['product_tesla'] else ("exception" if row['pair'][0] <= 5 else "✗")
        print(f"  {str(row['pair']):<12} {row['last_p']:>6} {row['last_q']:>6} "
              f"{row['last_pxq']:>9}  {tesla}")
    print()
    print("  Pattern table (last_p, last_q) → last(p×q):")
    for (lp, lq, lpq), cnt in sorted(ld_stats['pattern_counts'].items()):
        tesla = "Tesla" if lpq in TESLA else ""
        print(f"    ({lp},{lq}) → {lpq}  {tesla}  [×{cnt}]")
    print(f"  All products Tesla (p>5): {ld_stats['law3_verified']}")
    print()

    print("  STRUCTURAL LAWS VERIFIED")
    print("  Law 1: mid_dr = dr_p + 1  — holds for all pairs")
    print("  Law 2: terminal_dr + dr_q = 10  — holds for all p ≥ 5")
    print("  Law 3: last(p×q) ∈ {3,9} ⊂ Tesla  — holds for all p > 5")
    print("  Exceptions: (3,5) Law 2; (3,5),(5,7) Law 3 — small primes only")
    print("=" * 65)

    return lattice


if __name__ == "__main__":
    run()
