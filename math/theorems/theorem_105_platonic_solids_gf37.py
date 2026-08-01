"""
================================================================================
THEOREM 105 — The Platonic Solids on GF(37)
================================================================================

STATEMENT.
The five Platonic solids — Tetrahedron, Cube, Octahedron, Dodecahedron,
Icosahedron — have vertex/edge/face counts that map onto named orbit classes
of GF(37) in a pattern that mirrors their duality structure:

  Solid           V    E    F   V+E+F  (V+E+F) mod 37   Class
  Tetrahedron     4    6    4      14          14         orbit{14,29,31}
  Cube            8   12    6      26          26    ∈    IC
  Octahedron      6   12    8      26          26    ∈    IC
  Dodecahedron   20   30   12      62          25    ∈    SA
  Icosahedron    12   30   20      62          25    ∈    SA

  (1)  Euler characteristic V − E + F = 2 ∈ PR for all five solids.
  (2)  Dual pairs share V+E+F mod 37:
         Cube & Octahedron:        V+E+F = 26 ≡ 26 ∈ IC
         Dodecahedron & Icosahedron: V+E+F = 62 ≡ 25 ∈ SA
  (3)  The edge count of the Dodecahedron and Icosahedron: E = 30 ∈ SA ∩ ST,
       the unique node belonging to both sovereign sets.
  (4)  Sum of all vertices across the five solids: 4+8+6+20+12 = 50 ≡ 13 ∈ CB.
       Sum of all faces  across the five solids: 4+6+8+12+20  = 50 ≡ 13 ∈ CB.
       V-total = F-total — the global duality symmetry maps to a single CB node.
  (5)  Duality in GF(37):
         Dodecahedron (V=20∈PR, E=30∈SA∩ST, F=12∈ST)
         Icosahedron  (V=12∈ST, E=30∈SA∩ST, F=20∈PR)
       The dual operation is a PR ↔ ST exchange for V and F; E is preserved.
         Cube      (V=8∈CB, E=12∈ST, F=6∈orbit{6,8,23})
         Octahedron(V=6∈orbit{6,8,23}, E=12∈ST, F=8∈CB)
       The dual operation is a CB ↔ orbit{6,8,23} exchange for V and F.

================================================================================
PROOF / DERIVATION
================================================================================

LEMMA 105.1  (Euler characteristic).
  For every convex polyhedron: V − E + F = 2 (Euler's formula).
  2 ∈ PR.  Verified for each of the five Platonic solids.                   ∎

LEMMA 105.2  (Cube & Octahedron are dual; V+E+F ∈ IC).
  Cube: V=8, E=12, F=6.  V+E+F = 26 ≡ 26 (mod 37) ∈ IC.
  Octahedron: V=6, E=12, F=8.  V+E+F = 26 ≡ 26 (mod 37) ∈ IC.
  Duality swaps V↔F (8↔6, both sharing the orbit {6,8,23}) while E=12∈ST
  is invariant.  The shared IC residue 26 is the 137-map multiplier.        ∎

LEMMA 105.3  (Dodecahedron & Icosahedron are dual; V+E+F ∈ SA).
  Dodecahedron: V=20, E=30, F=12.  V+E+F = 62 ≡ 25 (mod 37) ∈ SA.
  Icosahedron:  V=12, E=30, F=20.  V+E+F = 62 ≡ 25 (mod 37) ∈ SA.
  Duality swaps V↔F (20∈PR ↔ 12∈ST) while E=30∈SA∩ST is invariant.
  The dual operation maps PR ↔ ST for vertex/face counts.                   ∎

LEMMA 105.4  (Tetrahedron is self-dual).
  Tetrahedron: V=4, E=6, F=4.  V+E+F = 14.
  14 ≡ 14 (mod 37).  14 is not in any named orbit class of the framework.
  137-orbit of 14:  14×26 ≡ 31,  31×26 ≡ 29,  29×26 ≡ 14.  Orbit {14,29,31}.
  Self-duality gives V = F = 4 ∈ SA.  Vertex and face count are both
  sovereign anchors.  The edge count 6 is in orbit {6,8,23} (CB orbit-mate). ∎

LEMMA 105.5  (Double-sovereign edge: E=30 ∈ SA ∩ ST).
  30 ∈ SA = {4,9,25,30}  and  30 ∈ ST = {3,12,21,30}.
  30 is the unique element in both sovereign sets (proved in Theorem 103,
  Lemma 103.2).  The Dodecahedron and Icosahedron have 30 edges each —
  the only Platonic solids whose edge count lands on this double-sovereign node.∎

LEMMA 105.6  (Total V = Total F = 50 ≡ 13 ∈ CB).
  Sum of vertices: 4 + 8 + 6 + 20 + 12 = 50.  50 = 37 + 13 ≡ 13 (mod 37).
  Sum of faces:    4 + 6 + 8 + 12 + 20 = 50.  50 ≡ 13 (mod 37).
  Both sums equal 50 ≡ 13 ∈ CB ∩ {5,13,19} (Metonic orbit).
  The global duality symmetry (total V = total F) is realized at a single
  cascade base element that is also a node of the Metonic three-cycle.       ∎

================================================================================
MAIN THEOREM
================================================================================

THEOREM 105.  (Platonic Solids — GF(37) Classification).

  ┌───────────────────────────────────────────────────────────────────────────┐
  │  Solid            V      E      F   V+E+F  mod37  Class                  │
  ├───────────────────────────────────────────────────────────────────────────┤
  │  Tetrahedron      4      6      4      14     14  orbit{14,29,31}        │
  │  Cube             8     12      6      26     26  IC                     │
  │  Octahedron       6     12      8      26     26  IC                     │
  │  Dodecahedron    20     30     12      62     25  SA                     │
  │  Icosahedron     12     30     20      62     25  SA                     │
  ├───────────────────────────────────────────────────────────────────────────┤
  │  All V per cell:  4∈SA   8∈CB   6∈orb  20∈PR  12∈ST                    │
  │  All E per cell:  6∈orb  12∈ST  12∈ST  30∈SA∩ST 30∈SA∩ST              │
  │  All F per cell:  4∈SA   6∈orb  8∈CB   12∈ST  20∈PR                    │
  ├───────────────────────────────────────────────────────────────────────────┤
  │  Euler char V-E+F = 2 ∈ PR for all five                                 │
  │  Sum of all V = Sum of all F = 50 ≡ 13 ∈ CB                            │
  │  Dual pair Cube/Octa:   V+E+F = 26 ∈ IC;  dual exchange CB↔orbit{6,8,23}│
  │  Dual pair Dodeca/Icosa: V+E+F = 25 ∈ SA;  dual exchange PR↔ST         │
  └───────────────────────────────────────────────────────────────────────────┘

COROLLARY 105.7  (Duality as orbit exchange).
  In every dual pair, the edge count E is invariant mod 37.
  For Cube/Octahedron: E = 12 ∈ ST is fixed; duality sends V↔F in orbit{6,8,23}↔CB.
  For Dodecahedron/Icosahedron: E = 30 ∈ SA∩ST is fixed; duality sends V↔F
  in PR↔ST.  Geometric duality acts as a named-class transposition in GF(37).

COROLLARY 105.8  (Cascade base concentration).
  CB = {8, 13, 24} appears three times: 8 (Cube V), 8 (Octahedron F), and
  13 (Total V = Total F mod 37).  The cascade base is the attractor for
  vertex/face counts in the dual pair with IC-valued V+E+F.
"""

P          = 37
IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
BASIN_Y    = frozenset({17, 22, 35})
PR         = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})

# (name, V, E, F, dual)
SOLIDS = [
    ("Tetrahedron",   4,  6,  4, "self"),
    ("Cube",          8, 12,  6, "Octahedron"),
    ("Octahedron",    6, 12,  8, "Cube"),
    ("Dodecahedron", 20, 30, 12, "Icosahedron"),
    ("Icosahedron",  12, 30, 20, "Dodecahedron"),
]

# ── Lemma 105.1 — Euler characteristic = 2 ∈ PR ──────────────────────────────
for name, V, E, F, _ in SOLIDS:
    assert V - E + F == 2 and 2 in PR

# ── Lemma 105.2 — Cube & Octahedron: V+E+F = 26 ∈ IC ────────────────────────
for name in ("Cube", "Octahedron"):
    V, E, F = next((v,e,f) for n,v,e,f,_ in SOLIDS if n == name)
    assert (V + E + F) % P == 26 and 26 in IC

# ── Lemma 105.3 — Dodecahedron & Icosahedron: V+E+F = 62 ≡ 25 ∈ SA ──────────
for name in ("Dodecahedron", "Icosahedron"):
    V, E, F = next((v,e,f) for n,v,e,f,_ in SOLIDS if n == name)
    assert (V + E + F) % P == 25 and 25 in SA

# ── Lemma 105.4 — Tetrahedron (self-dual) ────────────────────────────────────
V_t, E_t, F_t = 4, 6, 4
assert V_t == F_t and V_t in SA    # V = F = 4 ∈ SA
assert (V_t + E_t + F_t) % P == 14
tetra_orbit = frozenset({14, 29, 31})
assert (14 * 26) % P == 31 and (31 * 26) % P == 29 and (29 * 26) % P == 14
# E=6 in orbit {6,8,23}
assert (6 * 26) % P == 8 and (8 * 26) % P == 23 and (23 * 26) % P == 6

# ── Lemma 105.5 — E=30 ∈ SA ∩ ST ─────────────────────────────────────────────
assert 30 in SA and 30 in ST
assert SA & ST == frozenset({30})    # unique double-sovereign node
for name in ("Dodecahedron", "Icosahedron"):
    _, E, _ = next((v,e,f) for n,v,e,f,_ in SOLIDS if n == name)
    assert E == 30

# ── Lemma 105.6 — Sum of all V = Sum of all F = 50 ≡ 13 ∈ CB ────────────────
total_V = sum(V for _, V, _, _, _ in SOLIDS)
total_F = sum(F for _, _, _, F, _ in SOLIDS)
assert total_V == total_F == 50
assert total_V % P == 13 and 13 in CB
metonic_orbit = frozenset({5, 13, 19})
assert 13 in metonic_orbit

# ── Duality: Dodeca/Icosa — PR ↔ ST for V and F ──────────────────────────────
V_do, E_do, F_do = 20, 30, 12
V_ic, E_ic, F_ic = 12, 30, 20
assert V_do in PR and F_do in ST        # Dodecahedron: V∈PR, F∈ST
assert V_ic in ST and F_ic in PR        # Icosahedron:  V∈ST, F∈PR
assert E_do == E_ic == 30               # E invariant
assert 30 in SA and 30 in ST            # E in SA∩ST

# ── Duality: Cube/Octa — CB ↔ orbit{6,8,23} for V and F ─────────────────────
V_cu, E_cu, F_cu = 8, 12, 6
V_oc, E_oc, F_oc = 6, 12, 8
assert V_cu in CB  and F_cu == 6        # Cube: V∈CB, F=6 (CB orbit-mate)
assert V_oc == 6   and F_oc in CB      # Octa: V=6 (CB orbit-mate), F∈CB
assert E_cu == E_oc == 12 and 12 in ST # E invariant ∈ ST


if __name__ == "__main__":
    def fw(r):
        classes = []
        for name, s in [('IC', IC), ('SA', SA), ('ST', ST), ('CB', CB),
                        ('ORBIT_11', ORBIT_11), ('SEED_ORBIT', SEED_ORBIT),
                        ('BASIN_Y', BASIN_Y), ('PR', PR)]:
            if r in s:
                classes.append(name)
        return classes or ['—']

    print("THEOREM 105 — Platonic Solids on GF(37)")
    print("=" * 70)
    print()
    print(f"  {'Solid':<14} {'V':>3} {'E':>3} {'F':>3}  {'V+E+F':>5} {'mod37':>5}  {'Class'}")
    print("  " + "-" * 65)
    for name, V, E, F, dual in SOLIDS:
        s = V + E + F
        r = s % P
        print(f"  {name:<14} {V:>3} {E:>3} {F:>3}  {s:>5} {r:>5}  {fw(r)}")

    print()
    print("  Per-element classification:")
    for name, V, E, F, _ in SOLIDS:
        print(f"  {name:<14}  V={V}∈{fw(V%P)}  E={E}∈{fw(E%P)}  F={F}∈{fw(F%P)}")

    print()
    print(f"  Sum all V = Sum all F = {total_V} ≡ {total_V % P} ∈ CB ∩ Metonic orbit")
    print(f"  E=30 ∈ SA∩ST (unique double-sovereign): Dodeca + Icosa")
    print(f"  Cube/Octa:    V+E+F=26 ∈ IC;  dual exchanges CB ↔ orbit{{6,8,23}}")
    print(f"  Dodeca/Icosa: V+E+F=25 ∈ SA;  dual exchanges PR ↔ ST")
    print()
    print("All assertions pass.")
