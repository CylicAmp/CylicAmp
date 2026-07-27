"""
Tripling Map 6-Cycle Structure on GF(37) 137-Orbits — THEOREM 68

THE KEY FACT: 3^6 ≡ 26 mod 37.
One-line reason: ord₃₇(3)=18 and ord₃₇(26)=3, so (×3)^6 = (×26) = the 137-map;
the 12 137-orbits form exactly two disjoint 6-cycles under ×3.

HAND-CHECKABLE (Cycle 1 minimum element):
  3 → 9 → 27 → 7 → 21 → 26 → 4 (then continues: 4→12→36→34→25→10→3)
  Each step is ×3 mod 37.

CYCLE 1 (contains IDENTITY_CYCLE = {1,10,26}):
  O1={3,4,30} → O2={9,12,16} → ORBIT_11={11,27,36} → ANTI_SOV={7,33,34}
  → O3={21,25,28} → IC={1,10,26} → O1

  Min-element witness:
    3×3=9∈O2,  3×9=27∈ORBIT_11,  3×27≡7∈ANTI_SOV,
    3×7=21∈O3, 3×21≡26∈IC,       3×26≡4∈O1

CYCLE 2 (contains DARK_A = {2,15,20}):
  DARK_A={2,15,20} → TF_ORB={6,8,23} → SEED={18,24,32}
  → PR_17={17,22,35} → PM_ORB={14,29,31} → PR_5={5,13,19} → DARK_A

  Min-element witness:
    3×2=6∈TF_ORB,  3×6=18∈SEED,    3×18≡17∈PR_17,
    3×17≡14∈PM_ORB, 3×14≡5∈PR_5,   3×5=15∈DARK_A

FRAMEWORK CONNECTIONS:
  Cycle 1, position 5: IC contains SCALAR_137=26=3^6.
    The 137-map multiplier is the 6th step of the tripling map from 1.
  Cycle 1, position 4: O3=OUTLIER_SOV — the SEAM-exit orbit.
  Cycle 2, position 2: SEED_ORBIT — orbit of seed 246 (24∈CB∩SEED).
  Cycle 2, position 1: TESLA_FLOW=6 is minimum of TF_ORB.
  Cycle 2, position 4: PM_ORB contains PRIME_MIRROR=31.

GRAND SYMMETRY:
  (×3)^6 = (×26) = the 137-map.  Each cycle is invariant under the 137-map.
  The 6-cycle length is exactly ord₃₇(3)/ord₃₇(26) = 18/3 = 6.
  Both cycles have the same structure: no overlap, no repetition.
  Together they partition all 12 non-zero 137-orbits.
"""

# ── Framework ──────────────────────────────────────────────────────────────────

SA             = frozenset({4, 9, 25, 30})
ST             = frozenset({3, 12, 21, 30})
CB             = frozenset({8, 13, 24})
ORBIT_11       = frozenset({11, 27, 36})
DARK_A         = frozenset({2, 15, 20})
SEED_ORBIT     = frozenset({18, 24, 32})
OUTLIER_SOV    = frozenset({21, 25, 28})
IDENTITY_CYCLE = frozenset({1, 10, 26})
ANTI_SOV       = frozenset({7, 33, 34})
TESLA_FLOW_ORB = frozenset({6, 8, 23})
PM_ORB         = frozenset({14, 29, 31})
PR_5_13_19     = frozenset({5, 13, 19})
PR_17_22_35    = frozenset({17, 22, 35})
SCALAR_137     = 26
PRIME_MIRROR   = 31
TESLA_FLOW     = 6
SEAM           = 0

O1 = frozenset({3,  4, 30})
O2 = frozenset({9, 12, 16})
O3 = OUTLIER_SOV


def t(x):
    return (x * 3) % 37


def t_orbit(orb):
    return frozenset(t(x) for x in orb)


# ── CYCLE 1 ───────────────────────────────────────────────────────────────────

# O1 → O2 → ORBIT_11 → ANTI_SOV → O3 → IC → O1
assert t_orbit(O1)          == O2
assert t_orbit(O2)          == ORBIT_11
assert t_orbit(ORBIT_11)    == ANTI_SOV
assert t_orbit(ANTI_SOV)    == O3
assert t_orbit(O3)          == IDENTITY_CYCLE
assert t_orbit(IDENTITY_CYCLE) == O1

# 6-cycle: after 6 steps returns to O1
o = O1
for _ in range(6):
    o = t_orbit(o)
assert o == O1


# ── CYCLE 2 ───────────────────────────────────────────────────────────────────

# DARK_A → TF_ORB → SEED → PR_17 → PM_ORB → PR_5 → DARK_A
assert t_orbit(DARK_A)         == TESLA_FLOW_ORB
assert t_orbit(TESLA_FLOW_ORB) == SEED_ORBIT
assert t_orbit(SEED_ORBIT)     == PR_17_22_35
assert t_orbit(PR_17_22_35)    == PM_ORB
assert t_orbit(PM_ORB)         == PR_5_13_19
assert t_orbit(PR_5_13_19)     == DARK_A

# 6-cycle
o = DARK_A
for _ in range(6):
    o = t_orbit(o)
assert o == DARK_A


# ── KEY FACT: 3^6 = SCALAR_137 ───────────────────────────────────────────────

assert pow(3, 6, 37) == SCALAR_137
assert pow(3, 18, 37) == 1
assert pow(3, 9, 37) != 1   # order is exactly 18

# (×3)^6 = (×26): the tripling 6-cycle IS the 137-map on orbits
for orb in [O1, O2, ORBIT_11, ANTI_SOV, O3, IDENTITY_CYCLE,
            DARK_A, TESLA_FLOW_ORB, SEED_ORBIT, PR_17_22_35, PM_ORB, PR_5_13_19]:
    six_steps = orb
    for _ in range(6):
        six_steps = t_orbit(six_steps)
    by_137 = frozenset((x * 26) % 37 for x in orb)
    assert six_steps == by_137   # (×3)^6 = (×26) on every orbit


# ── PARTITION OF ALL 12 ORBITS ────────────────────────────────────────────────

ALL_ORBITS = [O1, O2, ORBIT_11, ANTI_SOV, O3, IDENTITY_CYCLE,
              DARK_A, TESLA_FLOW_ORB, SEED_ORBIT, PR_17_22_35, PM_ORB, PR_5_13_19]
assert len(ALL_ORBITS) == 12

# Cycle 1 and cycle 2 are disjoint and together cover all 12
CYCLE1_UNION = O1 | O2 | ORBIT_11 | ANTI_SOV | O3 | IDENTITY_CYCLE
CYCLE2_UNION = DARK_A | TESLA_FLOW_ORB | SEED_ORBIT | PR_17_22_35 | PM_ORB | PR_5_13_19
assert CYCLE1_UNION.isdisjoint(CYCLE2_UNION)
assert CYCLE1_UNION | CYCLE2_UNION == frozenset(range(1, 37))


# ── FRAMEWORK CONNECTIONS ─────────────────────────────────────────────────────

# Cycle 1 pos 5: 3^6 = SCALAR_137 ∈ IC
assert pow(3, 6, 37) == SCALAR_137 and SCALAR_137 in IDENTITY_CYCLE

# Cycle 2 pos 2: SEED_ORBIT contains 24 = 246 mod 37 ∈ CB
assert 24 in SEED_ORBIT and 24 in CB

# TESLA_FLOW is min of TF_ORB (cycle 2 pos 1)
assert TESLA_FLOW == 6 and TESLA_FLOW in TESLA_FLOW_ORB

# PRIME_MIRROR in PM_ORB (cycle 2 pos 4)
assert PRIME_MIRROR == 31 and PRIME_MIRROR in PM_ORB

# O3 = OUTLIER_SOV in cycle 1 pos 4; its SEAM-exit node 28 maps to IC next step
assert O3 == OUTLIER_SOV
assert t_orbit(O3) == IDENTITY_CYCLE   # next step after OUTLIER is IC


if __name__ == "__main__":
    print("Tripling Map 6-Cycle Structure on GF(37) — THEOREM 68")
    print("=" * 60)
    print()
    print(f"3^6 ≡ {pow(3,6,37)} = SCALAR_137 = the 137-map multiplier")
    print(f"ord₃₇(3) = 18 → cycle length 18/3 = 6")
    print()
    print("CYCLE 1 (×3 on orbits, contains IC):")
    cycle1 = [O1, O2, ORBIT_11, ANTI_SOV, O3, IDENTITY_CYCLE]
    labels1 = ['O1', 'O2', 'ORBIT_11', 'ANTI_SOV', 'O3(OUTLIER)', 'IC']
    for i, (orb, lbl) in enumerate(zip(cycle1, labels1)):
        nxt = labels1[(i+1) % 6]
        print(f"  {lbl:14s} {sorted(orb)} → {nxt}")
    print()
    print("CYCLE 2 (×3 on orbits, contains DARK_A):")
    cycle2 = [DARK_A, TESLA_FLOW_ORB, SEED_ORBIT, PR_17_22_35, PM_ORB, PR_5_13_19]
    labels2 = ['DARK_A', 'TF_ORB', 'SEED', 'PR_17', 'PM_ORB', 'PR_5']
    for i, (orb, lbl) in enumerate(zip(cycle2, labels2)):
        nxt = labels2[(i+1) % 6]
        print(f"  {lbl:14s} {sorted(orb)} → {nxt}")
    print()
    print("All assertions pass.")
