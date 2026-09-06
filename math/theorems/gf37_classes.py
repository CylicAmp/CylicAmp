"""
GF(37) Class Definitions — Canonical Single Source of Truth

All named classes, orbits, and cross-orbit sets for the GF(37).
Import from this file instead of redefining sets per-theorem.

    from gf37_classes import SA, ST, CB, IC, SEED_ORB, TESLA_ORB, QR37, PR37
    from gf37_classes import ALL_ORBITS, classify_residue, orbit137

STRUCTURE
=========

GF(37) = (ℤ/37ℤ)× has order φ(37) = 36.
The 137-map f(n) = 26n mod 37 has ord₃₇(26) = 3, so every orbit is a 3-cycle.
There are exactly 12 orbits: 6 QR (visible) and 6 NQR (dark).

THE 12 ORBITS
=============

QR orbits (quadratic residues mod 37):
  IC             = {1,  10, 26}   identity class; orbit of 1
  SOVEREIGN_SPIRAL = {3, 4,  30}  unique orbit intersecting SA, ST, and SA∩ST
  D7             = {7,  33, 34}   orbit of 7; anti-sovereign dual
  SA_ORB         = {9,  12, 16}   orbit of 9; contains SA-step Δ=9
  ORBIT_11       = {11, 27, 36}   orbit of 11; 36=φ(37)
  OUTLIER_ORB    = {21, 25, 28}   orbit of 21; 28 is the outlier node (28+9≡0)

NQR orbits (non-quadratic-residues mod 37):
  DARK_A         = {2,  15, 20}   all primitive roots in this orbit
  NQR_5          = {5,  13, 19}   orbit of 5
  TESLA_ORB      = {6,  8,  23}   TESLA_FLOW=6; 6²≡−1; ord₃₇(6)=4
  NQR_14         = {14, 29, 31}   orbit of 14
  NQR_17         = {17, 22, 35}   orbit of 17
  SEED_ORB       = {18, 24, 32}   orbit of seed 246 mod 37 = 24

CROSS-ORBIT NAMED SETS
=======================

These sets each take exactly one element from three different orbits —
they are transversals, not 137-map orbits themselves.

SA (Sovereign Anchors):
  {4, 9, 25, 30}
  4  ∈ SOVEREIGN_SPIRAL,  30 ∈ SOVEREIGN_SPIRAL  (two from same orbit)
  9  ∈ SA_ORB
  25 ∈ OUTLIER_ORB
  QR sector; DR=4 or 9

ST (Sovereign Targets):
  {3, 12, 21, 30}
  3  ∈ SOVEREIGN_SPIRAL,  30 ∈ SOVEREIGN_SPIRAL  (two from same orbit)
  12 ∈ SA_ORB
  21 ∈ OUTLIER_ORB
  QR sector; DR=3 for all; DR(3)=DR(12)=DR(21)=DR(30)=3
  SA ∩ ST = {30}

CB (Cascade Base):
  {8, 13, 24}
  8  ∈ TESLA_ORB
  13 ∈ NQR_5
  24 ∈ SEED_ORB
  NQR sector; one element from each of three distinct NQR orbits

SPECIAL VALUES
==============

SEAM        = 0    absorbing element; fixed point of all ×a maps; chi(0)=0
TESLA_FLOW  = 6    6²≡−1 mod 37; ord₃₇(6)=4; counts QR and NQR orbits (6 each)
SA_STEP     = 9    Op(+−) delta; drives sovereign chain 3→12→21→30
OUTLIER     = 28   28+SA_STEP ≡ 0 mod 37; final step before SEAM
"""

P = 37

# ── 12 orbits under f(n) = 26n mod 37 ─────────────────────────────────────────

# QR orbits
IC               = frozenset({1,  10, 26})
SOVEREIGN_SPIRAL = frozenset({3,  4,  30})
D7               = frozenset({7,  33, 34})
SA_ORB           = frozenset({9,  12, 16})
ORBIT_11         = frozenset({11, 27, 36})
OUTLIER_ORB      = frozenset({21, 25, 28})

QR_ORBITS = [IC, SOVEREIGN_SPIRAL, D7, SA_ORB, ORBIT_11, OUTLIER_ORB]

# NQR orbits
DARK_A           = frozenset({2,  15, 20})
NQR_5            = frozenset({5,  13, 19})
TESLA_ORB        = frozenset({6,  8,  23})
NQR_14           = frozenset({14, 29, 31})
NQR_17           = frozenset({17, 22, 35})
SEED_ORB         = frozenset({18, 24, 32})

NQR_ORBITS = [DARK_A, NQR_5, TESLA_ORB, NQR_14, NQR_17, SEED_ORB]

ALL_ORBITS = QR_ORBITS + NQR_ORBITS

# ── Cross-orbit named sets (transversals) ─────────────────────────────────────

SA = frozenset({4,  9,  25, 30})   # Sovereign Anchors
ST = frozenset({3,  12, 21, 30})   # Sovereign Targets; DR=3 for all
CB = frozenset({8,  13, 24})       # Cascade Base; NQR transversal

# ── Computed sets ──────────────────────────────────────────────────────────────

QR37 = frozenset(n for n in range(1, P) if pow(n, (P-1)//2, P) == 1)
NQR37 = frozenset(range(1, P)) - QR37
PR37  = frozenset(g for g in range(2, P)
                  if all(pow(g, 36//q, P) != 1 for q in [2, 3]))

# ── Special scalars ────────────────────────────────────────────────────────────

SEAM       = 0
TESLA_FLOW = 6
SA_STEP    = 9
OUTLIER    = 28

# ── Orbit label map (residue → orbit name) ─────────────────────────────────────

_ORBIT_NAMES = {
    'IC': IC, 'SOVEREIGN_SPIRAL': SOVEREIGN_SPIRAL, 'D7': D7,
    'SA_ORB': SA_ORB, 'ORBIT_11': ORBIT_11, 'OUTLIER_ORB': OUTLIER_ORB,
    'DARK_A': DARK_A, 'NQR_5': NQR_5, 'TESLA_ORB': TESLA_ORB,
    'NQR_14': NQR_14, 'NQR_17': NQR_17, 'SEED_ORB': SEED_ORB,
}

_CROSS_NAMES = {'SA': SA, 'ST': ST, 'CB': CB}


def orbit_of(r: int) -> str:
    """Return the 137-map orbit name for residue r (0 → 'SEAM')."""
    r = r % P
    if r == 0:
        return 'SEAM'
    for name, s in _ORBIT_NAMES.items():
        if r in s:
            return name
    return '?'


def cross_classes(r: int) -> list:
    """Return cross-orbit class names (SA/ST/CB) that contain residue r."""
    r = r % P
    return [name for name, s in _CROSS_NAMES.items() if r in s]


def classify_residue(r: int) -> dict:
    """Full classification of a residue 0..36."""
    r = r % P
    orb = orbit_of(r)
    cross = cross_classes(r)
    qr = r in QR37
    pr = r in PR37
    return {
        'residue':   r,
        'orbit':     orb,
        'sector':    'SEAM' if r == 0 else ('QR' if qr else 'NQR'),
        'cross':     cross,
        'primitive': pr,
    }


def orbit137(n: int) -> tuple:
    """137-map 3-cycle of n mod 37."""
    r = n % P
    path = []
    for _ in range(3):
        path.append(r)
        r = (26 * r) % P
    return tuple(path)


def verify_structure():
    """Assert all class definitions are internally consistent."""

    # Exactly 12 orbits, each size 3, covering {1..36}
    all_elements = set()
    for orb in ALL_ORBITS:
        assert len(orb) == 3
        assert not orb & all_elements, f"orbit overlap: {orb & all_elements}"
        all_elements |= orb
    assert all_elements == set(range(1, P))

    # Each orbit is closed under ×26
    for orb in ALL_ORBITS:
        for r in orb:
            assert (26 * r) % P in orb, f"{r}×26 not in same orbit"

    # QR/NQR orbit split correct
    assert all(any(r in QR37 for r in o) for o in QR_ORBITS)   # all QR have QR members
    assert all(not any(r in QR37 for r in o) for o in NQR_ORBITS)  # NQR have none

    # SA: four elements from three QR orbits
    assert SA == frozenset({4,9,25,30})
    assert {orbit_of(r) for r in SA} == {'SOVEREIGN_SPIRAL', 'SA_ORB', 'OUTLIER_ORB'}

    # ST: four elements from three QR orbits; all DR=3
    assert ST == frozenset({3,12,21,30})
    assert {orbit_of(r) for r in ST} == {'SOVEREIGN_SPIRAL', 'SA_ORB', 'OUTLIER_ORB'}
    assert all((r-1)%9+1 == 3 for r in ST if r > 0)  # DR=3

    # SA ∩ ST = {30}
    assert SA & ST == frozenset({30})
    assert orbit_of(30) == 'SOVEREIGN_SPIRAL'

    # CB: one from TESLA_ORB, NQR_5, SEED_ORB
    assert CB == frozenset({8,13,24})
    assert {orbit_of(r) for r in CB} == {'TESLA_ORB', 'NQR_5', 'SEED_ORB'}
    assert all(r in NQR37 for r in CB)

    # Special scalars
    assert TESLA_FLOW in TESLA_ORB and pow(TESLA_FLOW, 2, P) == P - 1
    assert SA_STEP in SA and SA_STEP in SA_ORB
    assert (OUTLIER + SA_STEP) % P == SEAM

    # Primitive roots
    assert len(PR37) == 12          # φ(φ(37)) = φ(36) = 12
    assert PR37 <= NQR37            # all primitive roots are NQR
    assert all(p in DARK_A for p in PR37 & DARK_A)

    # ord₃₇(26) = 3
    assert pow(26, 3, P) == 1 and pow(26, 1, P) != 1 and pow(26, 2, P) != 1 \
        and pow(26, 3, P) == 1

    # 137 mod 37 = 26
    assert 137 % P == 26

    print(f"Structure verified: 12 orbits, {len(QR37)} QR, {len(NQR37)} NQR, "
          f"{len(PR37)} primitive roots")


if __name__ == "__main__":
    verify_structure()

    print()
    print("GF(37) Named Classes")
    print("=" * 60)
    print(f"  Prime: {P}   Map multiplier: 137%37=26   ord₃₇(26)=3")
    print()
    print("  QR ORBITS (visible sector):")
    for name, orb in [('IC', IC), ('SOVEREIGN_SPIRAL', SOVEREIGN_SPIRAL),
                      ('D7', D7), ('SA_ORB', SA_ORB),
                      ('ORBIT_11', ORBIT_11), ('OUTLIER_ORB', OUTLIER_ORB)]:
        print(f"    {name:<20} {sorted(orb)}")
    print()
    print("  NQR ORBITS (dark sector):")
    for name, orb in [('DARK_A', DARK_A), ('NQR_5', NQR_5),
                      ('TESLA_ORB', TESLA_ORB), ('NQR_14', NQR_14),
                      ('NQR_17', NQR_17), ('SEED_ORB', SEED_ORB)]:
        print(f"    {name:<20} {sorted(orb)}")
    print()
    print("  CROSS-ORBIT TRANSVERSALS:")
    print(f"    SA (Sovereign Anchors)   {sorted(SA)}")
    print(f"    ST (Sovereign Targets)   {sorted(ST)}  DR=3 all")
    print(f"    CB (Cascade Base)        {sorted(CB)}  NQR transversal")
    print(f"    SA ∩ ST                  {{30}}")
    print()
    print(f"  SEAM=0  TESLA_FLOW=6  SA_STEP=9  OUTLIER=28")
    print(f"  QR37: {len(QR37)} elements   NQR37: {len(NQR37)}   PR37: {len(PR37)}")
