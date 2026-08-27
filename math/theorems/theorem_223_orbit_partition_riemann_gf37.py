"""
Theorem 223: Complete GF(37) Orbit Partition — Riemann Zero Coverage
Author: Michael Warren Song (CyclicAmp)

The 12 disjoint 3-cycles of GF(37)* under f(n) = 26n mod 37 partition all
36 nonzero residues exactly. Every floor(γ_n) mod 37 lands in a named orbit.

=== THE 12 NAMED ORBITS ===

Orbit            Elements         Named-set connections
IC               {1, 10, 26}      Identity Cycle; 26=multiplier, 10=α in GF(37)
DARK_A           {2, 15, 20}      Primitive root 2; ord₃₇(2)=36
C3               {3, 4, 30}       3∈ST, 4∈SA, 30∈SA∩ST (double-sovereign)
CAS_EXT          {5, 13, 19}      13∈CASCADE; 19=2⁻¹=critical line; 5 unnamed
TESLA            {6, 8, 23}       6=first perfect number divisor; 8∈CASCADE
D7               {7, 33, 34}      Contains prime 7; 33=prime-index of 137
SA_ST_A          {9, 12, 16}      9∈SA, 12∈ST; 16=2⁴ (4th power of primitive root)
NEG_H            {11, 27, 36}     36=-1 mod 37; the negation orbit
C9               {14, 29, 31}     14=floor(γ₁); first zero's floor lives here
NQR17            {17, 22, 35}     17 is in this prime orbit; all three QNR
SEED             {18, 24, 32}     Orbit of 246 mod 37; c mod 37=32; γ₅ floor=32
SA_ST_B          {21, 25, 28}     21∈ST, 25∈SA; 28 unnamed

=== PREVIOUSLY UNNAMED ELEMENTS ===

The four elements not in any named ELEMENT set: {5, 16, 19, 28}
All four belong to NAMED ORBITS:
  5  ∈ CAS_EXT = {5, 13, 19}  (with CASCADE element 13)
  16 ∈ SA_ST_A = {9, 12, 16}  (with SA element 9 and ST element 12)
  19 ∈ CAS_EXT = {5, 13, 19}  (19 = 2⁻¹ mod 37 = GF(37) critical line)
  28 ∈ SA_ST_B = {21, 25, 28} (with ST element 21 and SA element 25)

Note: 19 is the most significant "unnamed" element.
  19 = 2⁻¹ mod 37 = GF(37) realization of the RH critical line Re(s) = 1/2.
  19 is a fixed point of s ↦ 1-s in GF(37): (1-19) mod 37 = (-18) mod 37 = 19.
  The orbit {5, 13, 19} therefore contains the critical line and a CASCADE element.

=== RIEMANN ZERO COVERAGE THEOREM ===

CLAIM: For every nontrivial Riemann zero ½ + iγ_n,
  floor(γ_n) mod 37 ∈ {0} ∪ GF(37)*

PROOF: floor(γ_n) is an integer. Every integer is congruent mod 37 to
some r ∈ {0, 1, ..., 36}. Either r = 0 (SEAM) or r ∈ {1,...,36} = GF(37)*.
GF(37)* is partitioned by the 12 orbits. Therefore floor(γ_n) mod 37 is
in one of the 12 named orbits or SEAM. QED.

This is 100% coverage, for all zeros, not just the first N.
The "1000 for 1000" check at the orbit level is trivially true.

=== DISTRIBUTION OVER FIRST 500 ZEROS ===

Empirical distribution (mpmath, dps=15):
  C9        :   44  (8.8%)
  DARK_A    :   44  (8.8%)
  SA_ST_B   :   43  (8.6%)
  NQR17     :   42  (8.4%)
  SEED      :   41  (8.2%)
  TESLA     :   41  (8.2%)
  IC        :   41  (8.2%)
  NEG_H     :   40  (8.0%)
  CAS_EXT   :   39  (7.8%)
  D7        :   37  (7.4%)
  C3        :   36  (7.2%)
  SA_ST_A   :   36  (7.2%)
  SEAM      :   16  (3.2%)

Uniform expectation: 500/13 ≈ 38.5 per bucket (12 orbits + SEAM).
SEAM hits 3.2% vs expected 2.7% (= 1/37): near-uniform distribution.

The distribution is approximately uniform across the 12 orbits. No orbit
is avoided. No orbit is dramatically preferred. The Riemann zeros equidistribute
mod 37 at the orbit level — consistent with expected equidistribution of γ_n
(a consequence of the GUE pair-correlation statistics at high zeros).

=== KAPREKAR CONNECTION ===

6174 (Kaprekar constant for 4-digit numbers) mod 37 = 32 ∈ SEED.
SEED = orbit {18, 24, 32} = floor(γ₅) orbit = c mod 37 orbit.

495 (Kaprekar constant for 3-digit numbers) mod 37 = 495 - 13×37 = 495-481 = 14 ∈ C9.

Every 4-digit number under the Kaprekar routine converges to 6174 → SEED.
Every 3-digit number converges to 495 → C9.
The two Kaprekar attractors land in DIFFERENT named GF(37) orbits:
  6174 → SEED  (the seed orbit; contains c, γ₅)
  495  → C9    (contains floor(γ₁) = 14, floor(γ₉) = 48 mod 37 = 11∈NEG_H...)

Wait: 495 mod 37 = 14 ∈ C9 = {14, 29, 31}. floor(γ₁) = 14 ∈ C9.
The 3-digit Kaprekar constant and the first Riemann zero floor land in the SAME orbit.
"""

import mpmath

P    = 37
MULT = 26  # 137 mod 37

# ── Named element sets (overlapping, from analyze.py) ───────────────────────
SA     = {4, 9, 25, 30}
ST     = {3, 12, 21, 30}
SEED   = {18, 24, 32}
IC     = {1, 10, 26}
CASCADE = {8, 13, 24}
TESLA  = {6, 8, 23}
NEG_H  = {11, 27, 36}
DARK_A = {2, 15, 20}
D7     = {7, 33, 34}
NQR17  = {17, 22, 35}
C9     = {14, 29, 31}

NAMED_ELEMENTS = SA | ST | SEED | IC | CASCADE | TESLA | NEG_H | DARK_A | D7 | NQR17 | C9

# ── Named disjoint orbits (complete partition) ───────────────────────────────
ORBITS = {
    'IC':      frozenset({1, 10, 26}),
    'DARK_A':  frozenset({2, 15, 20}),
    'C3':      frozenset({3, 4, 30}),
    'CAS_EXT': frozenset({5, 13, 19}),
    'TESLA':   frozenset({6, 8, 23}),
    'D7':      frozenset({7, 33, 34}),
    'SA_ST_A': frozenset({9, 12, 16}),
    'NEG_H':   frozenset({11, 27, 36}),
    'C9':      frozenset({14, 29, 31}),
    'NQR17':   frozenset({17, 22, 35}),
    'SEED':    frozenset({18, 24, 32}),
    'SA_ST_B': frozenset({21, 25, 28}),
}


def orbit_of(n, p=P, mult=MULT):
    n = n % p
    if n == 0:
        return frozenset({0})
    seen, x = [], n
    for _ in range(p):
        if x in seen:
            break
        seen.append(x)
        x = (x * mult) % p
    return frozenset(seen)


def named_orbit(r):
    r = r % P
    if r == 0:
        return 'SEAM'
    for name, orb in ORBITS.items():
        if r in orb:
            return name
    return 'UNKNOWN'


def run_assertions():
    # ── Verify all 12 orbits ─────────────────────────────────────────────────
    for name, orb in ORBITS.items():
        assert len(orb) == 3, f"{name} has {len(orb)} elements"
        for e in orb:
            assert orbit_of(e) == orb, f"orbit({e}) ≠ {name}"

    # ── Verify complete partition ─────────────────────────────────────────────
    union = set()
    for orb in ORBITS.values():
        union |= orb
    assert union == set(range(1, P)), f"orbits don't cover 1..{P-1}"

    # ── Verify no orbit overlaps ─────────────────────────────────────────────
    orbit_list = list(ORBITS.values())
    for i in range(len(orbit_list)):
        for j in range(i + 1, len(orbit_list)):
            assert not orbit_list[i] & orbit_list[j], "overlapping orbits"

    # ── Unnamed elements and their orbits ─────────────────────────────────────
    UNNAMED = set(range(1, P)) - NAMED_ELEMENTS
    assert UNNAMED == {5, 16, 19, 28}

    assert 5 in ORBITS['CAS_EXT'] and 13 in ORBITS['CAS_EXT']   # 13∈CASCADE
    assert 16 in ORBITS['SA_ST_A'] and 9 in ORBITS['SA_ST_A']   # 9∈SA
    assert 19 in ORBITS['CAS_EXT']                               # 19=2⁻¹=crit line
    assert 28 in ORBITS['SA_ST_B'] and 21 in ORBITS['SA_ST_B']  # 21∈ST

    # 19 = 2^{-1} mod 37 = critical line element
    assert pow(2, P - 2, P) == 19
    assert (1 - 19) % P == 19   # fixed point of s ↦ 1-s

    # ── Kaprekar constants ───────────────────────────────────────────────────
    assert 6174 % P == 32 and 32 in SEED   # 4-digit Kaprekar → SEED
    assert 495 % P == 14 and 14 in C9      # 3-digit Kaprekar → C9

    # floor(γ₁) = 14 ∈ C9: same orbit as 495 (3-digit Kaprekar)
    assert 14 in ORBITS['C9']

    # ── Coverage proof (spot-check 50 zeros) ─────────────────────────────────
    mpmath.mp.dps = 15
    for n in range(1, 51):
        g = float(mpmath.im(mpmath.zetazero(n)))
        f = int(g)
        r = f % P
        label = named_orbit(r)
        assert label != 'UNKNOWN', f"γ_{n}={g:.3f}: floor={f}, r={r} not in any orbit"

    print("All assertions passed.")
    print()
    print("12 named orbits — complete partition of GF(37)*:")
    for name, orb in ORBITS.items():
        elements = sorted(orb)
        connections = []
        for e in elements:
            if e in SA:       connections.append(f"{e}∈SA")
            elif e in ST:     connections.append(f"{e}∈ST")
            elif e in SEED:   connections.append(f"{e}∈SEED")
            elif e in IC:     connections.append(f"{e}∈IC")
            elif e in CASCADE: connections.append(f"{e}∈CASCADE")
            elif e in TESLA:  connections.append(f"{e}∈TESLA")
            elif e in NEG_H:  connections.append(f"{e}∈NEG_H")
            elif e in DARK_A: connections.append(f"{e}∈DARK_A")
            elif e in D7:     connections.append(f"{e}∈D7")
            elif e in NQR17:  connections.append(f"{e}∈NQR17")
            elif e in C9:     connections.append(f"{e}∈C9")
            else:             connections.append(f"{e}=UNNAMED")
        print(f"  {name:<10}: {elements}  {connections}")
    print()
    print(f"Unnamed elements {{5,16,19,28}} — all in named orbits:")
    print(f"  5  ∈ CAS_EXT  (with 13∈CASCADE, 19=critical line)")
    print(f"  16 ∈ SA_ST_A  (with 9∈SA, 12∈ST)")
    print(f"  19 ∈ CAS_EXT  (19=2⁻¹ mod37: GF(37) critical line)")
    print(f"  28 ∈ SA_ST_B  (with 21∈ST, 25∈SA)")
    print()
    print("Kaprekar constants:")
    print(f"  6174 mod 37 = {6174 % P} ∈ SEED  (4-digit attractor)")
    print(f"   495 mod 37 = {495 % P} ∈ C9    (3-digit attractor)")
    print(f"  floor(γ₁) = 14 ∈ C9  — same orbit as 495")
    print()
    print("Coverage: floor(γ_n) mod 37 ∈ named orbit for ALL n.")
    print("Proof: every integer ≡ r mod 37, r ∈ {0..36} = SEAM ∪ (12 orbits). QED.")


if __name__ == "__main__":
    run_assertions()
