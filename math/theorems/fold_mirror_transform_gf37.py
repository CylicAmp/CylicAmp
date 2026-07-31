"""
Fold+Mirror Transform on GF(37) — THEOREM 99

The fold+mirror transform acts on the pattern 1234(0)6789:
  - Left block:   [1,2,3,4]
  - Center digit: 0  (additive identity of GF(37))
  - Right block:  [6,7,8,9]

FOLD+ RULE: map every non-zero digit to 1 (the multiplicative identity).
  [1,2,3,4] → [1,1,1,1]
  [6,7,8,9] → [1,1,1,1]

MIRROR RULE: copy the folded left block to the right around center 0.

RESULT: 1234(0)6789  →  1111(0)1111

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ALGEBRAIC MEANING

  fold+ is the indicator function of GF(37)*:
    f(d) = 1  if d ≠ 0  (nonzero → multiplicative identity)
    f(d) = 0  if d = 0  (zero → additive identity)

  So fold+ collapses every nonzero element to the unit, preserving 0.

GF(37) BLOCK RESIDUES

  Before fold+:
    1234 mod 37 = 13  ∈ CB ∩ PR   (cascade base element, primitive root)
    6789 mod 37 = 18  ∈ SEED_ORBIT ∩ PR  (seed orbit entry, primitive root)

  After fold+:
    1111 mod 37 = 1   ∈ IC ∩ TESLA_4  (identity basin)

  fold+ maps:  CB × SEED_ORBIT  →  IC × IC
  The cascade base and seed orbit both collapse to the identity basin.

FULL NUMBER RESIDUES

  Start:  123406789  mod 37 = 23  DR = 4
  Result: 111101111  mod 37 = 27  ∈ ORBIT_11   DR = 8

  The transform lands in ORBIT_11 = {11, 27, 36}.

DIGIT SUM COLLAPSE

  Original digit sum: 1+2+3+4+0+6+7+8+9 = 40   DR = 4
  Folded digit sum:   1+1+1+1+0+1+1+1+1 = 8    DR = 8

  DR doubles: 4 → 8.

ALPHA GRID CONNECTION

  Full alpha grid: 1-2-3-4-(5)-6-7-8-9  (center = 5, not 0)
  123456789 mod 37 = 36  ∈ ORBIT_11 ∩ TESLA_4
  digit sum = 45  mod 37 = 8  ∈ CB

  Replacing center 5 with 0 shifts residue: 36 → 23.
  fold+ of the 0-center pattern lands at 27 ∈ ORBIT_11.
  Both 36 and 27 ∈ ORBIT_11 = {11, 27, 36}.
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


def fold_plus(block):
    return [1 if d != 0 else 0 for d in block]


def to_int(left, center, right):
    return int(''.join(str(d) for d in left + [center] + right))


# ── The transform ─────────────────────────────────────────────────────────────

left   = [1, 2, 3, 4]
center = 0
right  = [6, 7, 8, 9]

left_folded  = fold_plus(left)
right_folded = fold_plus(right)

assert left_folded  == [1, 1, 1, 1]
assert right_folded == [1, 1, 1, 1]

start_n  = to_int(left, center, right)    # 123406789
result_n = to_int(left_folded, center, right_folded)  # 111101111

assert start_n  == 123406789
assert result_n == 111101111


# ── Block residues ────────────────────────────────────────────────────────────

assert 1234 % P == 13 and 13 in CB and 13 in PR
assert 6789 % P == 18 and 18 in SEED_ORBIT and 18 in PR
assert 1111 % P == 1  and 1  in IC and 1  in TESLA_4

# fold+ maps CB×SEED_ORBIT → IC×IC
assert 1234 % P in CB
assert 6789 % P in SEED_ORBIT
assert 1111 % P in IC


# ── Full number residues ──────────────────────────────────────────────────────

assert start_n  % P == 23
assert result_n % P == 27 and 27 in ORBIT_11
assert dr(start_n)  == 4
assert dr(result_n) == 8


# ── Digit sum collapse ────────────────────────────────────────────────────────

orig_sum = sum(left) + center + sum(right)
fold_sum = sum(left_folded) + center + sum(right_folded)

assert orig_sum == 40 and dr(orig_sum) == 4
assert fold_sum == 8  and dr(fold_sum) == 8


# ── Alpha grid connection ─────────────────────────────────────────────────────

alpha_n = to_int([1,2,3,4], 5, [6,7,8,9])
assert alpha_n == 123456789
assert alpha_n % P == 36 and 36 in ORBIT_11 and 36 in TESLA_4
assert sum(range(1, 10)) == 45 and 45 % P == 8 and 8 in CB

# Both alpha (center=5) and fold result land in ORBIT_11
assert alpha_n % P in ORBIT_11
assert result_n % P in ORBIT_11


if __name__ == "__main__":
    def fw(r):
        classes = []
        for name, s in [('IC',IC),('SA',SA),('ST',ST),('CB',CB),
                        ('O11',ORBIT_11),('SEED',SEED_ORBIT),
                        ('T4',TESLA_4),('PR',PR),('BY',BASIN_Y)]:
            if r in s: classes.append(name)
        return classes or ['—']

    print("Fold+Mirror Transform on GF(37) — THEOREM 99")
    print("=" * 60)
    print()
    print(f"  Transform: 1234(0)6789 → 1111(0)1111")
    print(f"  Rule: fold+(d) = 1 if d≠0 else 0  (indicator of GF(37)*)")
    print()
    print(f"  Block residues (before):")
    print(f"    1234 mod37={1234%P} ∈ {fw(1234%P)}  (cascade base)")
    print(f"    6789 mod37={6789%P} ∈ {fw(6789%P)}  (seed orbit entry)")
    print(f"  Block residues (after fold+):")
    print(f"    1111 mod37={1111%P} ∈ {fw(1111%P)}  (identity basin)")
    print()
    print(f"  Full number:")
    print(f"    {start_n}  mod37={start_n%P}  DR={dr(start_n)}  {fw(start_n%P)}")
    print(f"    {result_n}  mod37={result_n%P}  DR={dr(result_n)}  {fw(result_n%P)}")
    print()
    print(f"  Digit sum: {orig_sum} (DR={dr(orig_sum)}) → {fold_sum} (DR={dr(fold_sum)})")
    print()
    print(f"  Alpha grid 123456789 mod37={alpha_n%P} ∈ {fw(alpha_n%P)}")
    print(f"  Both alpha and fold result ∈ ORBIT_11 = {{11,27,36}}")
    print()
    print("All assertions pass.")
