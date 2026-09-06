"""
Pattern (1-4)(5)(1-4) — 16 Numbers on GF(37) — THEOREM 98

All 3-digit numbers with middle digit 5 and first/last digits in {1,2,3,4}.
16 total numbers. Parity classification uses o/e/O/E system:
  odd digit → o, even digit → e, 9 → O (Big O), 8 → E (Big E)
  (no Big O or Big E appear here — all digits ∈ {1,2,3,4,5})

Parity classes (4 groups of 4):
  ooo: 151, 153, 351, 353
  oeo: 152, 154, 352, 354     (note: 5 is odd → o; middle always o)
  eoo: 251, 253, 451, 453
  eeo: 252, 254, 452, 454

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GF(37) RESIDUE STRUCTURE

  The 16 mod-37 residues form three consecutive runs:
    {3,4,5,6,7,8,9,10}   — 8 values  (covers ST,SA,PR,T4,CB,IC)
    {18,19,20,21}         — 4 values  (SEED_ORBIT entry + PR cluster)
    {29,30,31,32}         — 4 values  (SA∩ST + T4 + SEED_ORBIT)

  Sum of all 16 numbers: 4840
    4840 mod 37 = 30  ∈ SA ∩ ST  (sovereign anchor AND sovereign target)
    DR(4840) = 7

  Notable residue hits:
    151 mod 37 = 3   ∈ ST
    152 mod 37 = 4   ∈ SA
    252 mod 37 = 30  ∈ SA ∩ ST
    254 mod 37 = 32  ∈ SEED_ORBIT ∩ PR
    351 mod 37 = 18  ∈ SEED_ORBIT ∩ PR  (seed orbit entry)
    452 mod 37 = 8   ∈ CB  (cascade base)
    453 mod 37 = 9   ∈ SA
    454 mod 37 = 10  ∈ IC
"""

P          = 37
IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
BASIN_Y    = frozenset({17, 22, 35})


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 9


def parity(d):
    if d == 9: return 'O'
    if d == 8: return 'E'
    return 'o' if d % 2 == 1 else 'e'


# ── Build all 16 numbers ──────────────────────────────────────────────────────

NUMS = [100 * a + 50 + b for a in range(1, 5) for b in range(1, 5)]
assert len(NUMS) == 16
assert NUMS == [151,152,153,154,251,252,253,254,351,352,353,354,451,452,453,454]


# ── Parity classification ─────────────────────────────────────────────────────

def pat(n):
    d1, d2, d3 = n // 100, (n // 10) % 10, n % 10
    return parity(d1) + parity(d2) + parity(d3)

assert [pat(n) for n in NUMS] == [
    'ooo','ooe','ooo','ooe',
    'eoo','eoe','eoo','eoe',
    'ooo','ooe','ooo','ooe',
    'eoo','eoe','eoo','eoe',
]

parity_groups = {
    'ooo': [151, 153, 351, 353],
    'ooe': [152, 154, 352, 354],
    'eoo': [251, 253, 451, 453],
    'eoe': [252, 254, 452, 454],
}
for label, members in parity_groups.items():
    assert all(pat(n) == label for n in members)


# ── GF(37) residues ───────────────────────────────────────────────────────────

residues = [n % P for n in NUMS]
assert sorted(set(residues)) == [3,4,5,6,7,8,9,10,18,19,20,21,29,30,31,32]

# Three consecutive runs
run1 = set(range(3, 11))    # {3..10}
run2 = set(range(18, 22))   # {18..21}
run3 = set(range(29, 33))   # {29..32}
assert set(residues) == run1 | run2 | run3

# Named hits
assert 151 % P == 3  and 3  in ST
assert 152 % P == 4  and 4  in SA
assert 252 % P == 30 and 30 in SA and 30 in ST
assert 254 % P == 32 and 32 in SEED_ORBIT and 32 in PR
assert 351 % P == 18 and 18 in SEED_ORBIT and 18 in PR
assert 452 % P == 8  and 8  in CB
assert 453 % P == 9  and 9  in SA
assert 454 % P == 10 and 10 in IC


# ── Sum properties ────────────────────────────────────────────────────────────

total = sum(NUMS)
assert total == 4840
assert total % P == 30
assert 30 in SA and 30 in ST    # SA ∩ ST
assert dr(total) == 7


if __name__ == "__main__":
    def fw(r):
        classes = []
        for name, s in [('IC',IC),('SA',SA),('ST',ST),('CB',CB),
                        ('O11',ORBIT_11),('SEED',SEED_ORBIT),
                        ('T4',TESLA_4),('PR',PR),('BY',BASIN_Y)]:
            if r in s: classes.append(name)
        return classes or ['—']

    print("Pattern (1-4)(5)(1-4) — 16 Numbers on GF(37) — THEOREM 98")
    print("=" * 64)
    print()
    print(f"  {'n':>4}  {'pat':>4}  {'mod37':>5}  {'DR':>3}  classes")
    for n in NUMS:
        r = n % P
        print(f"  {n:>4}  {pat(n):>4}  {r:>5}  {dr(n):>3}  {fw(r)}")
    print()
    print(f"  Sum: {total}  mod37={total%P} ∈ SA∩ST  DR={dr(total)}")
    print()
    print("  Residue runs:")
    print(f"    {{3..10}}  : {sorted(run1)}")
    print(f"    {{18..21}} : {sorted(run2)}")
    print(f"    {{29..32}} : {sorted(run3)}")
    print()
    print("All assertions pass.")
