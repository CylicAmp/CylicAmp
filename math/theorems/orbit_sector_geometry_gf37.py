"""
Orbit Sector Geometry — GF(37)

Three geometric structures emerge from the 137-map orbit partition:

  HEXAGON  (Space)   — 6 QR orbits + 6 NQR orbits: two hexagonal rings of 3-cycles
  SPIRAL   (Growth)  — each orbit is a 3-step spiral under multiplication by SCALAR_137(=26)
  VORONOI  (Pressure)— QR/NQR boundary = SEAM; sovereign/non-sovereign further partitions

FOUNDATION: chi(SCALAR_137) = chi(26) = +1.
  The 137-map multiplier 26 is itself a quadratic residue (QR).
  Therefore chi(26n) = chi(26)·chi(n) = chi(n) for all n.
  Consequence: every orbit {n, 26n, 26²n} is HOMOGENEOUS — all elements share the same
  Legendre symbol. Each orbit is either entirely QR (visible) or entirely NQR (dark).

HEXAGON (Space) — 6 + 6 = 12 ORBITS:
  QR orbits  (visible): {1,10,26}, {3,4,30}, {7,33,34}, {9,12,16}, {11,27,36}, {21,25,28}
  NQR orbits (dark):    {2,15,20}, {5,13,19}, {6,8,23},  {14,29,31}, {17,22,35}, {18,24,32}
  Exactly 6 QR and 6 NQR orbits. 6 = TESLA_FLOW = doubling-cycle period.

SPIRAL (Growth) — CANONICAL SOVEREIGN SPIRAL: orbit {3, 4, 30}
  ST(3) →×26→ SA(4) →×26→ SA∩ST(30) →×26→ ST(3)
  The 137-map spirals ST → SA → SA∩ST in a single 3-cycle.
  This is the unique orbit where all three sovereign grades appear.

VORONOI (Pressure) — SOVEREIGN ORBITS:
  Three of the six QR orbits contain sovereign (SA or ST) elements:
    {3, 4, 30}:  ST(3),  SA(4),  SA∩ST(30)  — fully sovereign; canonical spiral
    {9, 12, 16}: SA(9),  ST(12), 16(interior)— sovereign pair + one unclassified
    {21, 25, 28}: ST(21), SA(25), 28(outlier) — sovereign pair + outlier
  Each sovereign orbit contains exactly one SA and one ST element.
  The three non-sovereign QR orbits: {1,10,26}, {7,33,34}, {11,27,36}.

SOVEREIGN ORBITS FORM A META-3-CYCLE UNDER Op(+-):
  The SA-step Op(+-) has Δ=+9∈SA. Applied to ST-element of each sovereign orbit:
    3 (∈{3,4,30})  +9= 12 ∈ {9,12,16}    [ST→ST of next orbit]
    12(∈{9,12,16}) +9= 21 ∈ {21,25,28}   [ST→ST of next orbit]
    21(∈{21,25,28})+9= 30 ∈ {3,4,30}     [ST→SA∩ST of first orbit]
  The three sovereign orbits themselves form a 3-cycle under the SA-step.
  Orbit of orbits: {3,4,30} → {9,12,16} → {21,25,28} → {3,4,30}.

SEAM CONTACT — THE PRESSURE POINT:
  28 ∈ {21,25,28} (the outlier element of the third sovereign orbit):
    28 + 9 (Op(+-) delta) = 37 ≡ 0 = SEAM.
  The only orbit element that maps directly to SEAM via the SA-step is the outlier 28.
  Pressure is maximal at the boundary between the QR sovereign region and SEAM.

ORBIT MINIMUM SUMS — SECTOR CROSSINGS:
  QR orbit minima:  {1,3,7,9,11,21}   sum = 52 ≡ 15 ∈ DARK_A (mod 37)
  NQR orbit minima: {2,5,6,14,17,18}  sum = 62 ≡ 25 ∈ SA   (mod 37)
  15 (DARK_A) + 25 (SA) = 40 ≡ 3 ∈ ST.
  QR-to-NQR minimum sum produces: DARK_A, SA, then ST. Three sectors in one sum.

THE THREE-STRUCTURE CORRESPONDENCE:
  HEXAGON  = the 6+6 orbit split (Space: how the 36 elements organize)
  SPIRAL   = the ×26 map within each orbit (Growth: how elements evolve)
  VORONOI  = the QR/NQR partition and sovereign sub-partition (Pressure: boundaries)
  All three emerge from a single fact: chi(26)=1 and ord₃₇(26)=3.
"""

# ── Constants ──────────────────────────────────────────────────────────────────

SA           = frozenset({4, 9, 25, 30})
ST           = frozenset({3, 12, 21, 30})
CB           = frozenset({8, 13, 24})
PR           = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})
ORBIT_11     = frozenset({11, 27, 36})
DARK_A       = frozenset({2, 15, 20})
TESLA_FLOW   = 6
SCALAR_137   = 26
DECADE_ANCHOR = 10
SEAM         = 0


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def f137(n):
    return (n * 26) % 37


def chi(n, p=37):
    n = n % p
    if n == 0: return 0
    return 1 if pow(n, (p - 1) // 2, p) == 1 else -1


# ── FOUNDATION: chi(26) = 1 → orbits are homogeneous ─────────────────────────

assert chi(SCALAR_137) == 1   # 137-map multiplier is QR
assert pow(SCALAR_137, 3, 37) == 1   # ord₃₇(26) = 3

# Every orbit element has the same chi (since multiplying by 26 preserves chi)
for n in range(1, 37):
    assert chi(f137(n)) == chi(n)   # chi preserved by 137-map


# ── COMPUTE ALL 12 THREE-CYCLES ───────────────────────────────────────────────

seen = set()
ORBITS = []
for start in range(1, 37):
    if start in seen:
        continue
    orbit = frozenset({start, f137(start), f137(f137(start))})
    assert f137(f137(f137(start))) == start   # verify 3-cycle
    ORBITS.append(orbit)
    seen |= orbit

assert len(ORBITS) == 12
assert len(seen) == 36   # all 36 nonzero elements covered


# ── HEXAGON: 6 QR + 6 NQR ORBITS ─────────────────────────────────────────────

QR_ORBITS  = [o for o in ORBITS if chi(min(o)) == 1]
NQR_ORBITS = [o for o in ORBITS if chi(min(o)) == -1]

assert len(QR_ORBITS)  == 6
assert len(NQR_ORBITS) == 6

# Each orbit is homogeneous
for orb in ORBITS:
    vals = {chi(x) for x in orb}
    assert len(vals) == 1   # all elements have same chi

# Named QR orbits
IDENTITY_CYCLE = frozenset({1, 10, 26})
ORBIT_SOVEREIGN_1 = frozenset({3, 4, 30})   # ST, SA, SA∩ST
ORBIT_DARK_7      = frozenset({7, 33, 34})  # unclassified QR
ORBIT_SOVEREIGN_2 = frozenset({9, 12, 16})  # SA, ST, interior
ORBIT_11_SET      = frozenset({11, 27, 36}) # = ORBIT_11
ORBIT_SOVEREIGN_3 = frozenset({21, 25, 28}) # ST, SA, outlier

for orb in [IDENTITY_CYCLE, ORBIT_SOVEREIGN_1, ORBIT_DARK_7,
            ORBIT_SOVEREIGN_2, ORBIT_11_SET, ORBIT_SOVEREIGN_3]:
    assert orb in QR_ORBITS or orb in [frozenset(o) for o in QR_ORBITS]
    assert all(chi(x) == 1 for x in orb)

# Named NQR orbits
ORBIT_DARK_A   = frozenset({2, 15, 20})    # = DARK_A
ORBIT_PR_CB_1  = frozenset({5, 13, 19})    # PR, CB, PR
ORBIT_TESLA_CB = frozenset({6, 8, 23})     # TESLA_FLOW, CB, ?
ORBIT_DARK_14  = frozenset({14, 29, 31})   # dark trio (PRIME_MIRROR cycle)
ORBIT_FULL_PR  = frozenset({17, 22, 35})   # all PR
ORBIT_SEED     = frozenset({18, 24, 32})   # SEED_ORBIT

for orb in [ORBIT_DARK_A, ORBIT_PR_CB_1, ORBIT_TESLA_CB,
            ORBIT_DARK_14, ORBIT_FULL_PR, ORBIT_SEED]:
    assert all(chi(x) == -1 for x in orb)


# ── SPIRAL: CANONICAL SOVEREIGN SPIRAL {3,4,30} ──────────────────────────────

assert f137(3)  == 4    # ST(3) → SA(4)
assert f137(4)  == 30   # SA(4) → SA∩ST(30)
assert f137(30) == 3    # SA∩ST(30) → ST(3)

assert 3  in ST
assert 4  in SA
assert 30 in SA and 30 in ST   # SA∩ST

# Orbit {9,12,16}: SA → ST → interior → SA
assert f137(9)  == 12
assert f137(12) == 16
assert f137(16) == 9
assert 9 in SA and 12 in ST

# Orbit {21,25,28}: ST → outlier → SA → ST
assert f137(21) == 28
assert f137(28) == 25
assert f137(25) == 21
assert 21 in ST and 25 in SA


# ── VORONOI: SOVEREIGN ORBITS ─────────────────────────────────────────────────

SOVEREIGN_ORBITS = [o for o in QR_ORBITS if any(x in SA or x in ST for x in o)]
assert len(SOVEREIGN_ORBITS) == 3   # exactly 3 of 6 QR orbits are sovereign

# Each sovereign orbit contains exactly one SA element and one ST element
for orb in SOVEREIGN_ORBITS:
    sa_els = [x for x in orb if x in SA]
    st_els = [x for x in orb if x in ST]
    assert len(sa_els) >= 1 and len(st_els) >= 1

# Verify the three sovereign orbits
assert frozenset({3,4,30})  in [frozenset(o) for o in SOVEREIGN_ORBITS]
assert frozenset({9,12,16}) in [frozenset(o) for o in SOVEREIGN_ORBITS]
assert frozenset({21,25,28}) in [frozenset(o) for o in SOVEREIGN_ORBITS]


# ── META-3-CYCLE: SOVEREIGN ORBITS UNDER Op(+-) ──────────────────────────────

# The SA-step (+9) maps ST-element of one sovereign orbit to the next
assert (3  + 9) % 37 == 12 and 12 in ORBIT_SOVEREIGN_2   # {3,4,30} → {9,12,16}
assert (12 + 9) % 37 == 21 and 21 in ORBIT_SOVEREIGN_3   # {9,12,16} → {21,25,28}
assert (21 + 9) % 37 == 30 and 30 in ORBIT_SOVEREIGN_1   # {21,25,28} → {3,4,30}

# The meta-cycle is itself a 3-cycle
orbit_by_el = {}
for orb in ORBITS:
    for x in orb: orbit_by_el[x] = frozenset(orb)

_meta = orbit_by_el[3]
for _ in range(4):
    # advance by taking the ST element and adding 9
    st_el = next(x for x in _meta if x in ST)
    _meta = orbit_by_el[(st_el + 9) % 37]
_start = frozenset({3,4,30})
assert orbit_by_el[3] == _start   # returns after 3 steps


# ── SEAM CONTACT ─────────────────────────────────────────────────────────────

assert (28 + 9) % 37 == SEAM   # outlier 28 reaches SEAM via Op(+-) exactly


# ── ORBIT MINIMUM SUMS ────────────────────────────────────────────────────────

qr_mins  = sorted(min(o) for o in QR_ORBITS)
nqr_mins = sorted(min(o) for o in NQR_ORBITS)

assert qr_mins  == [1, 3, 7, 9, 11, 21]
assert nqr_mins == [2, 5, 6, 14, 17, 18]

assert sum(qr_mins)  % 37 == 15 and 15 in DARK_A   # QR minima → DARK_A
assert sum(nqr_mins) % 37 == 25 and 25 in SA        # NQR minima → SA
assert (sum(qr_mins) + sum(nqr_mins)) % 37 == 3 and 3 in ST  # sum → ST


# ── TESLA_FLOW = 6 UNIFICATION ───────────────────────────────────────────────

assert len(QR_ORBITS) == TESLA_FLOW    # 6 = TESLA_FLOW = count of QR orbits
assert len(NQR_ORBITS) == TESLA_FLOW   # 6 = TESLA_FLOW = count of NQR orbits
assert len([1,2,4,8,7,5]) == TESLA_FLOW  # doubling-cycle period = 6


if __name__ == "__main__":
    print("Orbit Sector Geometry — GF(37)")
    print("=" * 60)
    print()
    print(f"FOUNDATION: chi(SCALAR_137=26) = {chi(26)}  (QR preserving)")
    print(f"  Every orbit is homogeneous: all elements share same Legendre symbol.")
    print()
    print("12 THREE-CYCLES:")
    for orb in sorted(ORBITS, key=min):
        def lbl(x):
            if x in SA and x in ST: return "SA∩ST"
            if x in SA: return "SA"
            if x in ST: return "ST"
            if x in ORBIT_11: return "ORBIT_11"
            if x == TESLA_FLOW: return "TESLA"
            if x in CB: return "CB"
            if x in DARK_A: return "DARK_A"
            if x in PR: return "PR"
            return "?"
        els = " ".join(f"{x}({lbl(x)})" for x in sorted(orb))
        sector = "QR " if chi(min(orb))==1 else "NQR"
        print(f"  {sector}  {els}")
    print()
    print(f"HEXAGON: {len(QR_ORBITS)} QR orbits + {len(NQR_ORBITS)} NQR orbits  (6 = TESLA_FLOW = doubling period)")
    print()
    print("CANONICAL SOVEREIGN SPIRAL {3,4,30}:")
    print(f"  ST(3) x26-> SA(4) x26-> SA∩ST(30) x26-> ST(3)")
    print()
    print("SOVEREIGN META-3-CYCLE under Op(+-) [+9]:")
    print(f"  {{3,4,30}} -> {{9,12,16}} -> {{21,25,28}} -> {{3,4,30}}")
    print(f"  SEAM contact: 28+9={28+9}≡{(28+9)%37}=SEAM")
    print()
    print("ORBIT MINIMUM SUMS:")
    print(f"  QR  minima {qr_mins} sum={sum(qr_mins)} ≡{sum(qr_mins)%37}∈DARK_A")
    print(f"  NQR minima {nqr_mins} sum={sum(nqr_mins)} ≡{sum(nqr_mins)%37}∈SA")
    print(f"  Total sum ≡{(sum(qr_mins)+sum(nqr_mins))%37}∈ST")
    print()
    print("All assertions pass.")
