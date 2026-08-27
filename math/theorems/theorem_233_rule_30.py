"""
Theorem 233: Rule 30 — Wolfram's Cellular Automaton in GF(37)
Author: Michael Warren Song (CyclicAmp)

Rule 30 is Wolfram's elementary cellular automaton with rule number 30 = 0b00011110.
Update rule: new[i] = left XOR (center OR right).

=== 30 IN GF(37) ===

30 mod 37 = 30.  30 is the ONLY element in SA ∩ ST ∩ C3 simultaneously:
  SA  = {4, 9, 25, 30}   (sovereign anchors)
  ST  = {3, 12, 21, 30}  (sovereign targets)
  C3  = {3, 4, 30}       (C3 orbit under 26-map)

30 in binary: 00011110  (the rule descriptor is its own GF(37) element)
DR(30) = 3 ∈ ST.
30 × 137 mod 37 = 3 ∈ C3.  30 × 26 mod 37 = 3 ∈ C3.
Orbit of 30 under 26-map: 30 → 3 → 4 → 30 = C3 = {3, 4, 30}.
30 is orbit-stable: the 137-map keeps 30 inside C3.

=== F-HEXAD COLLAPSE ===

All three F-hexad orbit representatives (9∈SA_ST_A, 18∈SEED, 36∈NEG_H),
treated as 6-bit values and evolved one step under Rule 30, all yield 63:

  R30(9)  = 63  mod37 = 26 = MULT ∈ IC
  R30(18) = 63  mod37 = 26 = MULT ∈ IC
  R30(36) = 63  mod37 = 26 = MULT ∈ IC

Rule 30 collapses all three F-hexad orbit seeds to the 137-map multiplier.
63 = 0b00111111.  63 mod 37 = 26 = MULT = 137 mod 37.

=== FIXED POINTS MOD 37 UNDER RULE 30 (8-bit) ===

n and R30(n) share the same residue mod 37 for these residues:
  {0, 4, 8, 10, 11, 20, 22, 29, 31, 34}

Orbits: SEAM, C3, TESLA, IC, NEG_H, DARK_A, NQR17, C9, C9, D7.

The twin prime pair (29, 31) ∈ C9 = {14, 29, 31} are BOTH fixed points mod 37.
C9 is the only orbit with two fixed-point members.
4 ∈ C3 ∩ SA is a fixed point (sovereign anchor, orbit-triple member, and Rule 30 fixed).

=== CENTER COLUMN AT PRIME STEPS ===

Starting from a single ON cell, the Rule 30 center column at step n:

Active prime steps (bit=1): 3, 5, 13, 19, 23, 29, 37
  3  ∈ C3        5  ∈ CAS_EXT
  13 ∈ CAS_EXT   19 ∈ CAS_EXT   (complete CAS_EXT orbit {5,13,19} all active)
  23 ∈ TESLA     29 ∈ C9
  37 ∈ SEAM      (the GF field prime itself; 37 mod 37 = 0)

Inactive prime steps (bit=0): 2, 7, 11, 17, 31
  2  ∈ DARK_A    7  ∈ D7
  11 ∈ NEG_H     17 ∈ NQR17
  31 ∈ C9        (29 active, 31 inactive — C9 twin pair diverges)

The complete CAS_EXT orbit {5, 13, 19} consists entirely of active prime steps.
CAS_EXT = {5, 13, 19}: 5 is prime, 13 is prime, 19 is prime — CAS_EXT is the
only GF(37) orbit whose elements are all prime AND all active in the Rule 30
center column.

Step 37 (the GF prime p=37) is active.  At the field modulus the center is ON.

=== TWIN PRIMES ===

Fixed points (29,31): both in C9; C9 contains the twin prime pair (29,31).
Center column: step 29 active (bit=1), step 31 inactive (bit=0) — the twin pair
diverges in the center column even though both are mod-37 fixed points.

=== SOPHIE GERMAIN ===

Active prime steps include:
  3 → Sophie Germain (2×3+1=7∈D7); D7 is an inactive-step orbit.
  5 → Sophie Germain (2×5+1=11∈NEG_H); NEG_H is an inactive-step orbit.
  23 → Sophie Germain (2×23+1=47→10∈IC); the safe prime's orbit IC is not
       represented among active prime steps but appears as a fixed point (10∈IC).

Sophie Germain active steps map their safe primes to inactive-step orbits
(D7, NEG_H), or to orbits with fixed-point members (IC).

=== 1/137 ===

30 × 137 mod 37 = 3 ∈ C3 (orbit-stable).
R30 collapse target: 26 = 137 mod 37 = MULT = inverse of (1/137) in GF(37).
The F-hexad collapse under Rule 30 lands exactly at the 1/137 residue.

=== RIEMANN HYPOTHESIS ===

Active prime step 29: floor(γ₁) ≈ 14 ∈ C9 (same orbit as step 29∈C9).
Active prime step 23: floor(γ₈) ≈ 43, 43 mod 37 = 6 ∈ TESLA (same orbit).
Fixed point 29 ∈ C9; γ₁ floor = 14 ∈ C9: Riemann zero orbit matches R30 fixed point orbit.
"""

import mpmath

mpmath.mp.dps = 15

P    = 37
MULT = 26

SA      = {4, 9, 25, 30}
ST      = {3, 12, 21, 30}
SEED    = {18, 24, 32}
IC      = {1, 10, 26}
CASCADE = {8, 13, 24}
TESLA   = {6, 8, 23}
D7      = {7, 33, 34}
NEG_H   = {11, 27, 36}
SA_ST_A = {9, 12, 16}
DARK_A  = {2, 15, 20}
C3      = {3, 4, 30}
CAS_EXT = {5, 13, 19}
C9      = {14, 29, 31}
NQR17   = {17, 22, 35}
SA_ST_B = {21, 25, 28}

ORBITS = {
    'IC': IC, 'DARK_A': DARK_A, 'C3': C3, 'CAS_EXT': CAS_EXT,
    'TESLA': TESLA, 'D7': D7, 'SA_ST_A': SA_ST_A, 'NEG_H': NEG_H,
    'C9': C9, 'NQR17': NQR17, 'SEED': SEED, 'SA_ST_B': SA_ST_B,
}


def orb(n):
    r = n % P
    if r == 0: return 'SEAM'
    for name, s in ORBITS.items():
        if r in s: return name


def rule30_step(row):
    width = len(row)
    new = []
    for i in range(width):
        L = row[(i - 1) % width]
        C = row[i]
        R = row[(i + 1) % width]
        k = 4 * L + 2 * C + R
        new.append((30 >> k) & 1)
    return new


def r30_val(n, bits=8):
    row = [(n >> (bits - 1 - i)) & 1 for i in range(bits)]
    return int(''.join(map(str, rule30_step(row))), 2)


def center_col_steps(n_steps=74):
    width = 149
    center = 74
    row = [0] * width
    row[center] = 1
    col = {}
    for step in range(1, n_steps + 1):
        row = rule30_step(row)
        col[step] = row[center]
    return col


def run_assertions():
    # ── 30 in GF(37) ─────────────────────────────────────────────────────────
    assert 30 % P == 30
    assert 30 in SA and 30 in ST and 30 in C3
    # Only element in all three
    triple = SA & ST & C3
    assert triple == {30}

    # Orbit of 30 under 26-map = C3
    orb30 = set()
    x = 30
    for _ in range(3):
        orb30.add(x)
        x = (x * MULT) % P
    assert orb30 == C3

    # 30 × 137 mod 37 = 3 ∈ C3
    assert (30 * 137) % P == 3 and 3 in C3

    # ── F-hexad collapse ──────────────────────────────────────────────────────
    # All three orbit reps (6-bit R30) → 63 → 26 = MULT
    for v in [9, 18, 36]:
        assert r30_val(v, bits=6) == 63
    assert 63 % P == MULT and MULT in IC

    # ── Fixed points mod 37 (8-bit) ───────────────────────────────────────────
    fixed = sorted(set(n % P for n in range(256) if r30_val(n, 8) % P == n % P))
    assert set(fixed) == {0, 4, 8, 10, 11, 20, 22, 29, 31, 34}

    # Twin pair (29,31) both fixed
    assert 29 in fixed and 31 in fixed and 29 in C9 and 31 in C9

    # 4 in C3 ∩ SA is fixed
    assert 4 in fixed and 4 in C3 and 4 in SA

    # ── Center column at prime steps ──────────────────────────────────────────
    from sympy import isprime as _isp, primerange as _pr
    col = center_col_steps(37)

    active_primes   = [p for p in _pr(2, 38) if col[p] == 1]
    inactive_primes = [p for p in _pr(2, 38) if col[p] == 0]

    assert active_primes   == [3, 5, 13, 19, 23, 29, 37]
    assert inactive_primes == [2, 7, 11, 17, 31]

    # Complete CAS_EXT orbit {5,13,19} all active
    assert {5, 13, 19} == CAS_EXT
    assert all(p in active_primes for p in CAS_EXT)
    assert all(_isp(p) for p in CAS_EXT)   # all CAS_EXT elements are prime

    # Step 37 (GF prime) is active
    assert col[37] == 1

    # ── Riemann ───────────────────────────────────────────────────────────────
    g1 = float(mpmath.im(mpmath.zetazero(1)))
    assert int(g1) % P == 14 and 14 in C9   # same orbit as fixed point 29∈C9

    g8 = float(mpmath.im(mpmath.zetazero(8)))
    assert int(g8) % P == 6 and 6 in TESLA  # same orbit as active prime step 23∈TESLA

    print("All assertions passed.")
    print()
    print("RULE 30 IN GF(37) — T233")
    print()
    print(f"30 mod 37 = 30  ∈ SA ∩ ST ∩ C3 (unique triple-intersection element)")
    print(f"30 orbit under 26-map: {sorted(C3)} = C3")
    print(f"30 × 137 mod 37 = {(30*137)%P} ∈ C3 (orbit-stable)")
    print()
    print("F-hexad collapse (6-bit R30):")
    for v, name in [(9,'SA_ST_A'), (18,'SEED'), (36,'NEG_H')]:
        print(f"  R30({v}∈{name}) = {r30_val(v,6)} → {r30_val(v,6)%P} = MULT ∈ IC")
    print()
    print(f"R30 fixed points mod 37 (8-bit): {{0,4,8,10,11,20,22,29,31,34}}")
    print(f"  Twin pair (29,31) ∈ C9: both fixed")
    print(f"  4 ∈ C3 ∩ SA: fixed")
    print()
    print("Center column active prime steps: {3,5,13,19,23,29,37}")
    print("  CAS_EXT = {5,13,19}: complete orbit, all prime, all active")
    print("  Step 37 (GF prime p=37): active (bit=1)")
    print("Center column inactive prime steps: {2,7,11,17,31}")


if __name__ == "__main__":
    run_assertions()
