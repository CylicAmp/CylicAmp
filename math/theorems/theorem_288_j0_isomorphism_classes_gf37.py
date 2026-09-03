"""
T288 — j=0 Elliptic Curves over F_37: Isomorphism Classes = Antipodal Pairs

The family y^2 = x^3 + a (j-invariant 0, A=0) over F_37 has exactly 6
isomorphism classes for a ≠ 0. Two curves y^2=x^3+a and y^2=x^3+a' are
isomorphic over F_37 iff a'/a is a 6th power in F_37*.

The 6th powers in F_37* form the subgroup <27> = <11> = IC ∪ NEG_H (T284),
of order 6.  The 36 nonzero a-values partition into 6 cosets of <11>,
each coset of size 6.  Each coset is exactly one ANTIPODAL PAIR of orbits
(T283/T285): two orbits at Z/12Z distance 6.

Result: the 6 isomorphism classes of y^2=x^3+a over F_37 correspond
bijectively to the 6 antipodal orbit pairs.

Point count (#E) and Frobenius trace (t = 38 - #E) are constant on each
isomorphism class.  The traces are exactly ±{1, 10, 11} — the elements of
<11> = IC ∪ NEG_H reduced to balanced Z-representatives.

The anomalous class (#E=37=p, t=1) is the antipodal pair SEED ↔ CAS_EXT.
The pipeline seed 246 mod 37 = 24 ∈ SEED, placing it in the anomalous class.
The anomalous point count 37 ≡ 0 (mod 37) is the unique SEAM residue.

Full table:
  Pair            a-orbit values              #E   t=38-#E  |t| ∈ orbit
  IC ↔ NEG_H     {1,10,26} ∪ {11,27,36}      48     -10    IC
  DARK_A ↔ NQR17 {2,15,20} ∪ {17,22,35}      49     -11    NEG_H/{11}
  C3 ↔ D7        {3,4,30}  ∪ {7,33,34}        39      -1    IC/{1}
  TESLA ↔ C9     {6,8,23}  ∪ {14,29,31}       28      10    IC
  SA_ST_A↔SA_ST_B {9,12,16} ∪ {21,25,28}      27      11    NEG_H/{11}
  SEED ↔ CAS_EXT {18,24,32}∪ {5,13,19}        37       1    IC/{1}  ← ANOMALOUS

Note: trace sign convention t = p+1 - #E = 38 - #E.  The six traces
{-10, -11, -1, 10, 11, 1} = ±{1, 10, 11} are the elements of <11> under
the isomorphism GF(37)* → Z that maps x to min(x, 37-x) with sign.
"""

ORBITS = {
    'IC':      {1, 10, 26},
    'DARK_A':  {2, 15, 20},
    'C3':      {3, 4, 30},
    'CAS_EXT': {5, 13, 19},
    'TESLA':   {6, 8, 23},
    'D7':      {7, 33, 34},
    'SA_ST_A': {9, 12, 16},
    'NEG_H':   {11, 27, 36},
    'C9':      {14, 29, 31},
    'NQR17':   {17, 22, 35},
    'SEED':    {18, 24, 32},
    'SA_ST_B': {21, 25, 28},
}

ANTIPODAL = [
    ('IC', 'NEG_H'), ('DARK_A', 'NQR17'), ('C3', 'D7'),
    ('TESLA', 'C9'), ('SA_ST_A', 'SA_ST_B'), ('SEED', 'CAS_EXT'),
]

OPERATOR_GROUP = {1, 10, 11, 26, 27, 36}  # <11> = IC ∪ NEG_H

ELEM_TO_ORBIT = {}
for name, elems in ORBITS.items():
    for e in elems:
        ELEM_TO_ORBIT[e] = name


def get_orbit(x):
    return ELEM_TO_ORBIT.get(x % 37, 'SEAM')


def count_points(a):
    """Exact point count on y^2 = x^3 + a (mod 37) including point at infinity."""
    n = 1
    for x in range(37):
        rhs = (x ** 3 + a) % 37
        for y in range(37):
            if (y * y) % 37 == rhs:
                n += 1
    return n


def sixth_powers():
    """Subgroup of 6th powers in F_37* = <11> = IC ∪ NEG_H."""
    return {pow(x, 6, 37) for x in range(1, 37)}


# ─── Part 1: 6th power subgroup = <11> ───────────────────────────────────────

def verify_sixth_power_subgroup():
    sp = sixth_powers()
    assert sp == OPERATOR_GROUP, f"6th powers ≠ <11>: {sp}"
    assert sp == ORBITS['IC'] | ORBITS['NEG_H'], "6th powers ≠ IC ∪ NEG_H"
    return sp


# ─── Part 2: isomorphism classes = cosets of <11> = antipodal pairs ──────────

def isomorphism_classes():
    """
    Partition F_37* into cosets of <11>.
    Each coset of size 6 = union of two orbits = one antipodal pair.
    """
    og = OPERATOR_GROUP
    classes = []
    covered = set()
    for a in range(1, 37):
        if a in covered:
            continue
        coset = {(a * g) % 37 for g in og}
        classes.append(coset)
        covered |= coset
    assert len(classes) == 6, f"Expected 6 classes, got {len(classes)}"
    assert all(len(c) == 6 for c in classes), "Each class must have 6 elements"
    return classes


def match_cosets_to_antipodal(classes):
    """Verify each coset = one antipodal pair's orbit union."""
    for coset in classes:
        orbit_names = {get_orbit(x) for x in coset}
        assert len(orbit_names) == 2, f"Coset spans {len(orbit_names)} orbits: {orbit_names}"
        a_name, b_name = sorted(orbit_names)
        found = False
        for ant_a, ant_b in ANTIPODAL:
            if sorted([ant_a, ant_b]) == [a_name, b_name]:
                found = True
                break
        assert found, f"Orbit pair {orbit_names} is not an antipodal pair"


# ─── Part 3: point count constant on each class ───────────────────────────────

def point_count_table():
    """
    Compute #E for each isomorphism class.
    Verify constancy within each class and match to antipodal pair.
    """
    table = {}
    for name, elems in ORBITS.items():
        counts = [count_points(a) for a in elems]
        assert len(set(counts)) == 1, f"{name}: {counts}"
        table[name] = counts[0]
    return table


# ─── Part 4: traces are exactly ±{1, 10, 11} ─────────────────────────────────

def verify_traces(table):
    """
    Trace t = (p+1) - #E = 38 - #E.
    For each antipodal pair: trace must be constant and in ±{1,10,11}.
    """
    target_traces = {1, 10, 11, -1, -10, -11}
    traces_seen = set()
    for a_name, b_name in ANTIPODAL:
        Ea = table[a_name]
        Eb = table[b_name]
        assert Ea == Eb, f"Antipodal {a_name}↔{b_name}: #E differs {Ea}≠{Eb}"
        t = 38 - Ea
        traces_seen.add(t)
    assert traces_seen == target_traces, f"Traces {traces_seen} ≠ ±{{1,10,11}}"
    return traces_seen


# ─── Part 5: anomalous class = SEED ↔ CAS_EXT ───────────────────────────────

def verify_anomalous_class(table):
    anomalous = {name for name, E in table.items() if E == 37}
    assert anomalous == {'SEED', 'CAS_EXT'}, f"Anomalous orbits: {anomalous}"
    assert 24 in ORBITS['SEED'], "Pipeline seed residue 24 must be in SEED"
    assert 246 % 37 == 24, "246 mod 37 must be 24"
    assert 37 % 37 == 0, "#E=37 ≡ 0 (SEAM)"


# ─── Part 6: Hasse bound check ────────────────────────────────────────────────

def verify_hasse(table):
    import math
    bound = 2 * math.sqrt(37)
    for name, E in table.items():
        t = abs(38 - E)
        assert t <= bound, f"{name}: |t|={t} exceeds Hasse bound {bound:.2f}"


# ─── Part 7: full report ──────────────────────────────────────────────────────

def run():
    sp = verify_sixth_power_subgroup()
    classes = isomorphism_classes()
    match_cosets_to_antipodal(classes)
    table = point_count_table()
    traces = verify_traces(table)
    verify_anomalous_class(table)
    verify_hasse(table)

    print("=" * 68)
    print("T288 — j=0 Elliptic Curves over F_37: Isomorphism Classes")
    print("=" * 68)

    print("\n--- Part 1: 6th power subgroup = <11> = IC ∪ NEG_H ---")
    print(f"  {sorted(sp)} (size {len(sp)})")
    print(f"  = IC ∪ NEG_H = T284 operator group")

    print("\n--- Part 2: 6 isomorphism classes = 6 antipodal pairs ---")
    print("  y^2=x^3+a ≅ y^2=x^3+a' iff a'/a ∈ <11>")
    print("  Each coset of <11> in F_37* = one antipodal orbit pair")

    print("\n--- Part 3: Point counts and traces ---")
    print(f"  {'Antipodal pair':25s}  #E   trace   |t|∈orbit  anomalous")
    print(f"  {'-'*25}  ---  ------  ---------  ---------")
    for a_name, b_name in ANTIPODAL:
        E = table[a_name]
        t = 38 - E
        abs_t = abs(t)
        t_orbit = get_orbit(abs_t) if abs_t > 0 else 'SEAM'
        anom = E == 37
        print(f"  {a_name:10s} ↔ {b_name:10s}   {E:3d}    {t:4d}   {t_orbit:8s}  {'← ANOMALOUS' if anom else ''}")

    print(f"\n--- Part 4: Traces = ±{{1,10,11}} = ±|<11>| ---")
    print(f"  Observed traces: {sorted(traces)}")
    print(f"  <11> = {{1,10,11,26,27,36}}; balanced representatives = ±{{1,10,11}}")

    print(f"\n--- Part 5: Anomalous class = SEED ↔ CAS_EXT ---")
    print(f"  #E = 37 = p;  trace t = 1")
    print(f"  246 mod 37 = {246%37} ∈ SEED  (pipeline reference seed)")
    print(f"  37 mod 37 = 0 = SEAM  (anomalous count hits prime boundary)")
    print(f"  The orbit containing the pipeline seed is the anomalous class.")

    print(f"\n--- Part 6: Hasse bound check ---")
    print(f"  Hasse bound: |t| ≤ 2√37 ≈ 12.17")
    for a_name, b_name in ANTIPODAL:
        E = table[a_name]
        print(f"  {a_name}↔{b_name}: |t|={abs(38-E)}")

    print("\nAll T288 assertions passed.")


if __name__ == '__main__':
    run()
