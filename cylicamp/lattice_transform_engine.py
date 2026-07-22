"""
Lattice Transform Engine
© 2026 Michael Warren Song. All Rights Reserved.

Generates all 1,680 ordered 3-partitions of {1..9} into groups of 3 digits.
Applies differential cascade {+8, +13, +24} to break the mod-37 degeneracy.
Filters for grids where adjacent block differences land in {8, 13, 24}.

Combinatorial count:
    C(9,3) × C(6,3) × C(3,3) = 84 × 20 × 1 = 1,680 partitions

Canonical degeneracy (all three resolve to residue 12):
    123 % 37 = 12
    456 % 37 = 12
    789 % 37 = 12
    → adjacent differences = 0, filter sees nothing

Cascade mutation breaks the symmetry by applying distinct offsets
to each block position, injecting asymmetric residues.
"""

from itertools import combinations
from collections import Counter


MOD      = 37
CASCADE  = (8, 13, 24)
ADJ_SET  = frozenset({8, 13, 24})
CANONICAL = (123, 456, 789)


# ── Partition generation ──────────────────────────────────────────────────────

def block_value(group: tuple) -> int:
    """Sorted-digit 3-digit number for a digit group, e.g. {3,1,2} → 123."""
    s = sorted(group)
    return s[0] * 100 + s[1] * 10 + s[2]


def generate_partitions() -> list:
    """
    All ordered 3-partitions of {1..9} into groups of 3 (internal order irrelevant).
    C(9,3) × C(6,3) × C(3,3) = 84 × 20 × 1 = 1,680.
    """
    digits = list(range(1, 10))
    partitions = []
    for g1 in combinations(digits, 3):
        rem1 = [d for d in digits if d not in g1]
        for g2 in combinations(rem1, 3):
            g3 = tuple(d for d in rem1 if d not in g2)
            b1, b2, b3 = block_value(g1), block_value(g2), block_value(g3)
            partitions.append({
                'groups':        (g1, g2, g3),
                'blocks':        (b1, b2, b3),
                'orig_residues': (b1 % MOD, b2 % MOD, b3 % MOD),
            })
    return partitions


# ── Cascade & adjacency ───────────────────────────────────────────────────────

def apply_cascade(blocks: tuple, cascade: tuple = CASCADE) -> tuple:
    """Differential mutation: block_i += cascade_i."""
    return tuple(b + c for b, c in zip(blocks, cascade))


def adjacency_check(blocks: tuple, circular: bool = False) -> dict:
    """
    Check adjacent block differences (mod 37) against ADJ_SET.
    Each pair passes if either direction (fwd or rev) lands in ADJ_SET.

    Linear: pairs (0,1) and (1,2).
    Circular: also pair (2,0).
    """
    res = [b % MOD for b in blocks]
    n   = len(res)
    pairs = [(i, (i + 1) % n) for i in range(n - 1 if not circular else n)]

    pair_results = []
    for i, j in pairs:
        fwd  = (res[j] - res[i]) % MOD
        rev  = (res[i] - res[j]) % MOD
        pair_results.append({
            'pair':   (i, j),
            'res_i':  res[i],
            'res_j':  res[j],
            'fwd':    fwd,
            'rev':    rev,
            'passed': fwd in ADJ_SET or rev in ADJ_SET,
        })

    return {
        'mut_residues': tuple(res),
        'pair_results': pair_results,
        'passed':       all(pr['passed'] for pr in pair_results),
    }


# ── Engine ────────────────────────────────────────────────────────────────────

class LatticeTransformEngine:
    def __init__(self, circular: bool = False):
        self.partitions = generate_partitions()
        self.circular   = circular
        assert len(self.partitions) == 1680, f"Expected 1680, got {len(self.partitions)}"

    # ── math constraints that must hold ──────────────────────────────────────

    def _constraint_analysis(self):
        """
        Derive which (r1, r2, r3) residue patterns survive the cascade filter.

        For linear adjacency with cascade (+8, +13, +24):
          Pair 0→1: (r2+13 - r1-8) % 37 = (r2-r1+5) % 37 must be in ADJ_SET
                 or (r1+8  - r2-13) % 37 = (r1-r2-5) % 37 must be in ADJ_SET
            → (r2-r1) % 37 ∈ {3, 8, 19} ∪ {13, 18, 29}  = {3,8,13,18,19,29}
              (both directions combined into: diff ∈ {3,8,13,18,19,29})

          Pair 1→2: (r3+24 - r2-13) % 37 = (r3-r2+11) % 37 must be in ADJ_SET
                 or (r2+13 - r3-24) % 37 = (r2-r3-11) % 37 must be in ADJ_SET
            → (r3-r2) % 37 ∈ {34,2,13} ∪ {18,13,2} = {2,13,18,34}
        """
        pair01_ok = set()
        pair12_ok = set()
        for delta in range(MOD):
            if (delta + 5) % MOD in ADJ_SET or (-(delta) - 5) % MOD in ADJ_SET:
                pair01_ok.add(delta)
            if (delta + 11) % MOD in ADJ_SET or (-delta - 11) % MOD in ADJ_SET:
                pair12_ok.add(delta)
        return pair01_ok, pair12_ok

    # ── main run ──────────────────────────────────────────────────────────────

    def run(self) -> tuple:
        survivors     = []
        orig_hist     = Counter()
        mut_hist      = Counter()

        for p in self.partitions:
            orig_hist[p['orig_residues']] += 1

            mut = apply_cascade(p['blocks'])
            adj = adjacency_check(mut, circular=self.circular)
            mut_hist[adj['mut_residues']] += 1

            if adj['passed']:
                survivors.append({
                    **p,
                    'mut_blocks': mut,
                    **adj,
                })

        return survivors, orig_hist, mut_hist

    # ── report ────────────────────────────────────────────────────────────────

    def report(self):
        survivors, orig_hist, mut_hist = self.run()
        mode = "circular" if self.circular else "linear"

        print("=" * 68)
        print("LATTICE TRANSFORM ENGINE — MOD-37 ADJACENCY FILTER")
        print("=" * 68)
        print(f"Partitions : 1,680  (C(9,3)×C(6,3)×C(3,3))")
        print(f"Cascade    : +{CASCADE[0]} / +{CASCADE[1]} / +{CASCADE[2]}")
        print(f"Target     : adjacent differences in {set(ADJ_SET)}")
        print(f"Adjacency  : {mode}")

        # ── canonical verification ──────────────────────────────────────────
        print("\n--- Canonical Block Degeneracy ---")
        for b in CANONICAL:
            print(f"  {b} % {MOD} = {b % MOD}")
        can_mut = apply_cascade(CANONICAL)
        can_adj = adjacency_check(can_mut, circular=self.circular)
        print(f"\n  After cascade {CASCADE} → {can_mut}")
        print(f"  Mutated residues : {can_adj['mut_residues']}")
        for pr in can_adj['pair_results']:
            flag = "PASS" if pr['passed'] else "FAIL"
            print(f"  [{pr['pair'][0]}→{pr['pair'][1]}] fwd={pr['fwd']:2d} rev={pr['rev']:2d}  {flag}")

        # ── constraint space ────────────────────────────────────────────────
        p01, p12 = self._constraint_analysis()
        print(f"\n--- Cascade Constraint Space ---")
        print(f"  (r2-r1) % 37 must be in : {sorted(p01)}")
        print(f"  (r3-r2) % 37 must be in : {sorted(p12)}")

        # ── original residue landscape ──────────────────────────────────────
        print(f"\n--- Original Residue Landscape ({len(orig_hist)} unique patterns) ---")
        for pat, cnt in orig_hist.most_common(10):
            print(f"  {pat}  →  {cnt} grids")

        # ── post-cascade landscape ──────────────────────────────────────────
        print(f"\n--- Post-Cascade Residue Landscape ({len(mut_hist)} unique patterns) ---")
        for pat, cnt in mut_hist.most_common(10):
            res   = list(pat)
            fwds  = [(res[i+1] - res[i]) % MOD for i in range(len(res)-1)]
            revs  = [(res[i] - res[i+1]) % MOD for i in range(len(res)-1)]
            ok    = all(f in ADJ_SET or r in ADJ_SET for f, r in zip(fwds, revs))
            flag  = "  ← PASSES" if ok else ""
            print(f"  {pat}  diffs fwd={tuple(fwds)} rev={tuple(revs)}{flag}  →  {cnt}")

        # ── survivors ───────────────────────────────────────────────────────
        print(f"\n--- Filter Results ---")
        print(f"Survivors : {len(survivors)} / 1,680")

        if survivors:
            print(f"\nFirst 10 surviving grids:")
            for s in survivors[:10]:
                print(f"  groups      : {s['groups']}")
                print(f"  orig blocks : {s['blocks']}  res: {s['orig_residues']}")
                print(f"  mut  blocks : {s['mut_blocks']}  res: {s['mut_residues']}")
                for pr in s['pair_results']:
                    print(f"    [{pr['pair'][0]}→{pr['pair'][1]}]  "
                          f"fwd={pr['fwd']:2d}  rev={pr['rev']:2d}  "
                          f"{'PASS' if pr['passed'] else 'FAIL'}")
                print()

            # DR distribution of survivor blocks
            all_blocks = [b for s in survivors for b in s['blocks']]
            dr_counts  = Counter()
            for b in all_blocks:
                dr = 1 + (b - 1) % 9 if b > 0 else 0
                dr_counts[dr] += 1
            flux = sum(dr_counts[d] for d in {3, 6, 9}) / len(all_blocks) if all_blocks else 0
            print(f"  DR distribution of survivor blocks: {dict(sorted(dr_counts.items()))}")
            print(f"  Spine FLUX ratio (3,6,9): {flux:.3f}  (natural ≈ 0.333)")

        else:
            print("\n  Zero grids survive.")
            print(f"\n  The cascade ({CASCADE}) does not route any partition")
            print(f"  into {{8, 13, 24}} adjacency under mod {MOD}.")
            print("\n  Closest misses — partitions where one pair passes:")
            near_misses = []
            for p in self.partitions:
                mb  = apply_cascade(p['blocks'])
                adj = adjacency_check(mb, circular=self.circular)
                passed_count = sum(1 for pr in adj['pair_results'] if pr['passed'])
                if passed_count > 0:
                    near_misses.append((passed_count, p, mb, adj))
            near_misses.sort(key=lambda x: -x[0])
            for pc, p, mb, adj in near_misses[:5]:
                fwds = tuple(pr['fwd'] for pr in adj['pair_results'])
                revs = tuple(pr['rev'] for pr in adj['pair_results'])
                print(f"    blocks: {p['blocks']} → {mb}  fwd={fwds}  rev={revs}")

        print("=" * 68)
        return survivors


# ── Execution ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    engine = LatticeTransformEngine(circular=False)
    survivors = engine.report()
