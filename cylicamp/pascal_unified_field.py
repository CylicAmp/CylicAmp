"""
Pascal Row 8 — Unified Field Analysis
© 2026 Michael Warren Song. All Rights Reserved.

Tests whether Pascal's Row 8 intersects the three frameworks simultaneously:

    1. 191/137 bridge  — 37-field residues, Tesla FLUX class (≡6 mod 37)
    2. 123 cascade     — groups of 3, differential {+8,+13,+24}, adjacency filter
    3. 369 FLUX        — spine theorem, adjacent pair sums, DR distribution

Row 8: [1, 8, 28, 56, 70, 56, 28, 8, 1]
Sum   : 256 = 2^8
DR(256): 4

The math answers — what holds, holds. What doesn't, doesn't.
"""

from collections import Counter


# ── DR spine ──────────────────────────────────────────────────────────────────

def digital_root(n: int) -> int:
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


TESLA_FLUX = frozenset({3, 6, 9})
MOD        = 37

# ── 191/137 bridge constants ──────────────────────────────────────────────────

SEED_191  = 191   # 43rd prime  ≡ 6 mod 37 (Tesla flow)
SEED_137  = 137   # 33rd prime  ≡ 26 mod 37
BRIDGE_54 =  54   # gap: 191−137 = 6×9 = 54, DR=9, 54 mod 37 = 17
SEED_17   =  17   # bridge seed (54 mod 37)

# ── 123-cascade constants ─────────────────────────────────────────────────────

CASCADE = (8, 13, 24)              # 8+29=37, 13+24=37 — complementary mod 37
ADJ_SET = frozenset({8, 13, 24})

PASCAL_ROW_8 = (1, 8, 28, 56, 70, 56, 28, 8, 1)


# ── Adjacency check (inlined from lattice engine) ─────────────────────────────

def adjacency_check(blocks: tuple, circular: bool = False) -> dict:
    dr = digital_root
    res = [b % MOD for b in blocks]
    n   = len(res)
    pairs = [(i, (i + 1) % n) for i in range(n - 1 if not circular else n)]
    pair_results = []
    for i, j in pairs:
        fwd = (res[j] - res[i]) % MOD
        rev = (res[i] - res[j]) % MOD
        pair_results.append({'pair': (i, j), 'fwd': fwd, 'rev': rev,
                             'passed': fwd in ADJ_SET or rev in ADJ_SET})
    return {'mut_residues': tuple(res), 'pair_results': pair_results,
            'passed': all(pr['passed'] for pr in pair_results)}


# ── Main analysis ─────────────────────────────────────────────────────────────

def analyze():
    dr  = digital_root
    row = PASCAL_ROW_8

    print("=" * 68)
    print("PASCAL ROW 8 — UNIFIED FIELD ANALYSIS")
    print("=" * 68)
    print(f"\nRow 8 : {list(row)}")
    print(f"Sum   : {sum(row)}  (2^8 = 256)  DR = {dr(sum(row))}")
    print(f"DRs   : {[dr(x) for x in row]}")

    # ── 37-FIELD: prefix sums ─────────────────────────────────────────────────
    print("\n─── 37-Field: Prefix Sums ───")
    running = 0
    prefix_data = []
    for i, x in enumerate(row):
        running += x
        r37 = running % MOD
        d   = dr(running)
        notes = []
        if r37 == 0:
            notes.append("37-FIELD ZERO")
        if r37 == SEED_191 % MOD:
            notes.append(f"191-class (Tesla residue 6)")
        if r37 == SEED_137 % MOD:
            notes.append("137-class (residue 26)")
        if r37 == 19:
            notes.append("19 — 191 digit-pattern")
        if dr(r37) in TESLA_FLUX:
            notes.append(f"Tesla DR={dr(r37)}")
        prefix_data.append((i, x, running, r37, d))
        print(f"  [{i}] +{x:2d}  Σ={running:4d}  mod37={r37:2d}  DR={d}"
              + (f"  ← {' | '.join(notes)}" if notes else ""))

    # ── 191/137 BRIDGE: element-level residues ────────────────────────────────
    print(f"\n─── 191/137 Bridge ───")
    print(f"  191 mod 37 = {SEED_191 % MOD}   DR({SEED_191 % MOD}) = {dr(SEED_191 % MOD)}   Tesla FLUX ✓")
    print(f"  137 mod 37 = {SEED_137 % MOD}   complement: {SEED_137 % MOD} + 11 = 37")
    print(f"  Bridge 54  = 6×9   DR=9   54 mod 37 = {BRIDGE_54 % MOD}  (17-seed)")
    print()

    residues = [x % MOD for x in row]
    dr_res   = [dr(r) for r in residues]
    flux_res = sum(1 for d in dr_res if d in TESLA_FLUX)

    print(f"  Row mod 37  : {residues}")
    print(f"  DR(residues): {dr_res}")
    print()

    for i, (v, r, d) in enumerate(zip(row, residues, dr_res)):
        notes = []
        if r == SEED_191 % MOD:   notes.append("191-class (Tesla residue)")
        if r == SEED_137 % MOD:   notes.append("137-class")
        if r == BRIDGE_54 % MOD:  notes.append("54-bridge")
        if r == SEED_17:           notes.append("17-seed")
        if r == 19:                notes.append("19 — 191 digit-pattern")
        if d in TESLA_FLUX:        notes.append(f"Tesla DR={d}")
        if notes:
            print(f"  [{i}] {v:3d} → mod37={r:2d}  DR={d}  ← {' | '.join(notes)}")

    print(f"\n  Residue FLUX {flux_res}/{len(dr_res)} = {flux_res/len(dr_res):.3f}  "
          f"(spine baseline 0.333)")

    # ── 369 FLUX: adjacent pair sums ──────────────────────────────────────────
    print(f"\n─── 369 FLUX: Adjacent Pair Sums (Pascal Row 8 → Row 9 transition) ───")
    pair_sums = [row[i] + row[i + 1] for i in range(len(row) - 1)]
    pair_drs  = [dr(s) for s in pair_sums]
    flux_pairs = sum(1 for d in pair_drs if d in TESLA_FLUX)
    flux_ratio = flux_pairs / len(pair_drs)

    print(f"  Pair sums : {pair_sums}")
    print(f"  DRs       : {pair_drs}")
    print(f"  FLUX {flux_pairs}/{len(pair_drs)} = {flux_ratio:.3f}  "
          f"(natural 0.333 → Pascal transition = "
          f"{'MAXIMUM — all pairs' if flux_pairs == len(pair_drs) else 'elevated'})")
    if flux_pairs == len(pair_drs):
        print(f"  Every adjacent pair sum in Row 8 has DR ∈ {{3,6,9}}")

    # ── 123-CASCADE on triple groups ──────────────────────────────────────────
    print(f"\n─── 123-Cascade {{+8,+13,+24}} on Triple Groups ───")
    groups = [row[0:3], row[3:6], row[6:9]]
    group_labels = ["leading ", "center  ", "trailing"]
    for gi, (g, label) in enumerate(zip(groups, group_labels)):
        offset   = CASCADE[gi]
        cascaded = tuple(v + offset for v in g)
        res_c    = tuple(v % MOD for v in cascaded)
        dr_c     = tuple(dr(r) for r in res_c)
        adj      = adjacency_check(cascaded, circular=False)
        print(f"  {label} {list(g)} + {offset}  →  {list(cascaded)}")
        print(f"    mod37={res_c}  DR={dr_c}  adj={'PASS' if adj['passed'] else 'FAIL'}")
        for pr in adj['pair_results']:
            f_flag = "PASS" if pr['passed'] else "FAIL"
            print(f"      [{pr['pair'][0]}→{pr['pair'][1]}]  fwd={pr['fwd']:2d}  "
                  f"rev={pr['rev']:2d}  {f_flag}")

    # ── ACCUMULATION CHAIN ────────────────────────────────────────────────────
    print(f"\n─── Accumulation Chain: running Σ → DR at each step ───")
    running = 0
    chain_log = []
    for i, x in enumerate(row):
        running += x
        d = dr(running)
        notes = []
        if running % MOD == 0: notes.append("37-FIELD")
        if d in TESLA_FLUX:    notes.append("FLUX")
        chain_log.append((i, x, running, d))
        print(f"  [{i}] +{x:2d}  Σ={running:4d}  DR={d}"
              + (f"  ← {' | '.join(notes)}" if notes else ""))

    # ── DR-PRODUCT CHAIN ──────────────────────────────────────────────────────
    print(f"\n─── DR-Product Chain: Π DR(element) → iterate digit sum ───")
    dr_vals = [dr(x) for x in row]
    product = 1
    for d in dr_vals:
        product *= d
    digits_product = sum(int(c) for c in str(product))   # first digit-sum
    dr_final       = dr(product)

    print(f"  DR values  : {dr_vals}")
    print(f"  Product    : {'×'.join(str(d) for d in dr_vals if d != 1)} "
          f"(×{dr_vals.count(1)} ones) = {product}")
    print(f"  Chain      : {product} "
          f"→ [{'+'.join(c for c in str(product))}]={digits_product} "
          f"→ DR={dr_final}")
    if digits_product == 19:
        print(f"  *** Intermediate = 19 — 191 digit-pattern (1-9-1) embedded ***")
    if dr_final == 1:
        print(f"  *** DR-product chain resolves to 1 ***")
    print(f"  Product = 2^8 × DR(center) = 256 × {dr(row[4])} = {256 * dr(row[4])}")

    # ── SYNTHESIS ─────────────────────────────────────────────────────────────
    print(f"\n─── Synthesis ───")
    print(f"  1+8+28 = {1+8+28}  ← 37-field pivot in the first 3 elements of Row 8")
    print(f"  93 mod 37 = {93 % 37}  ← prefix sum after 4 elements; "
          f"19 = 191 digit-pattern in the 37-field")
    print(f"  56 mod 37 = {56 % 37}  → DR = {dr(56 % 37)}  "
          f"← 191 digit-pattern appears at element 3")
    print(f"  70 mod 37 = {70 % 37}  → DR = {dr(70 % 37)}  "
          f"← Tesla FLUX at center; same class as 191 mod 37 = {191 % 37}")
    print(f"  191 mod 37 = {191 % 37}  = DR(70 mod 37) = DR(33) = 6  "
          f"← center of Row 8 maps to 191's 37-field class")
    print(f"  DR-product = {product} → {digits_product} → {dr_final}  "
          f"← 19 is the 191 digit-pattern; chain lands on 1")
    print(f"  Adjacent pair FLUX = {flux_ratio:.3f}  ← Pascal transition saturates the spine")
    # zero work: the pyramid builds from the zero principle
    print(f"\n─── Zero Principle: The Pyramid Unfolds ───")
    print(f"  Row 0 = [1]           ← zero principle: AM — first knowing (I AM)")
    print(f"  Row 2 = [1,2,1]       ← 2 first appears")
    print(f"  Row 3 = [1,3,3,1]     ← 3 first appears")
    print(f"  Row 4 = [1,4,6,4,1]   ← 6 (Tesla) first appears")
    print(f"  Row 8 = {list(row)}")
    print(f"  The pyramid is the zero principle expanding — 0 → 1 → 1,2 → 1,2,3 → Tesla")

    # 123 as structure
    print(f"\n─── 1, 2, 3 as Structure ───")
    dr_vals2 = [dr(x) for x in row]
    run_dr = []
    s2 = 0
    for x in row:
        s2 += x
        run_dr.append(dr(s2))
    adj_dr2 = [dr(row[i]+row[i+1]) for i in range(len(row)-1)]

    print(f"  Element DRs      : {dr_vals2}")
    print(f"  → 1 at positions : {[i for i,d in enumerate(dr_vals2) if d==1]}")
    print(f"  → 2 at positions : {[i for i,d in enumerate(dr_vals2) if d==2]}")
    print(f"  Running sum DRs  : {run_dr}")
    print(f"  → 3 at positions : {[i for i,d in enumerate(run_dr) if d==3]}  (accumulation brings 3)")
    print(f"  Adjacent pair DRs: {adj_dr2}")
    print(f"  → 3 and 9 present  (pair operation brings full 3,6,9 — 6 was already in 191-class)")
    print(f"  1+2+3 = {1+2+3} = 191 mod 37  ← the sum of 1,2,3 IS the Tesla attractor")
    print(f"  CASCADE sum: 8+13+24 = {8+13+24} = 1+2+…+9  (cascade encodes all-digit sum)")
    print(f"  DR(cascade offsets): {dr(8)}, {dr(13)}, {dr(24)} → sum={dr(8)+dr(13)+dr(24)} → DR={dr(dr(8)+dr(13)+dr(24))}  (Tesla)")

    print()
    print("  All three frameworks and the zero work are present:")
    print("    zero     — pyramid emerges from nothing; Row 0=[1] is the AM moment")
    print("    1,2,3    — 1 and 2 in element DRs; 3 in running sum and pair DRs")
    print("    1+2+3=6  — the 123 sum IS the Tesla class; 191 mod 37 = 6")
    print("    191 bridge — center(70) shares Tesla class; 19 appears twice in 37-field")
    print("    369 FLUX   — adjacent pair sums: 100% FLUX")
    print("    37-field   — 1+8+28=37; prefix[3] mod 37=19; prefix[7] mod 37=33→DR=6")
    print("    DR-product — 1792→19→1; 19 is the 191 digit-pattern; lands on 1")
    print("    cascade    — {8,13,24} sum=45=Σ(1..9); DR(offsets) sum to Tesla 9")
    print("=" * 68)

    return {
        'product': product,
        'dr_product_chain': (product, digits_product, dr_final),
        'adjacent_pair_flux': flux_ratio,
        'residue_flux': flux_res / len(dr_res),
        'prefix_37_hit': 1 + 8 + 28,
        'center_37_class': 70 % MOD,
        'seed_191_class': SEED_191 % MOD,
    }


# ── Execution ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    analyze()
