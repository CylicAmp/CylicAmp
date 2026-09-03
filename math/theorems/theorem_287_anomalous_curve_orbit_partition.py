"""
T287 — Anomalous Elliptic Curve over F_37: Orbit Partition via Cubic Invariance

The curve E: y^2 = x^3 + 5 (mod 37) has #E(F_37) = 37 (anomalous, trace t=1).

Core mechanism: ord_37(26) = 3, so 26^3 ≡ 1 (mod 37).  The three elements of
every 137-map orbit are {x, 26x, 26^2 x}.  The cubic f(x) = x^3 + 5 satisfies
f(26x) = (26x)^3 + 5 = 26^3 * x^3 + 5 ≡ x^3 + 5 = f(x) (mod 37).
Therefore f is CONSTANT on each orbit.  Whether orbit O supplies x-coordinates
to E is determined entirely by whether f(O) is a quadratic residue mod 37.

Result: the 12 orbits split exactly 6+6 by QR status of f(orbit).
The 6 QR-valued orbits = the 6 orbits appearing as x-coordinates of E(F_37).

Verified quantities:
  Curve:           y^2 = x^3 + 5 (mod 37)
  Anomalous check: #E(F_37) = 37, trace t = 38 - 37 = 1
  Generator:       G = (6, 6)  [both coordinates in TESLA, class 3]
  Doubling slope:  lambda = 9 in SA_ST_A (class 4)
  2G:              (32, 19)   x in SEED (class 5), y in CAS_EXT (class 11)
  5G:              (31, 14)   both coordinates in C9 (class 9) — same-orbit event
  10G:             (8,  6)    both coordinates in TESLA (class 3) — same-orbit event
  37G:             point at infinity (confirms order 37)

All computations verified by explicit enumeration.
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

ELEM_TO_ORBIT = {}
for name, elems in ORBITS.items():
    for e in elems:
        ELEM_TO_ORBIT[e] = name

QR_MOD37 = {(i * i) % 37 for i in range(1, 37)}


def get_orbit(x):
    return ELEM_TO_ORBIT.get(x % 37, 'SEAM')


def get_class(x):
    H = {1, 10, 26}
    for m in range(12):
        if x % 37 in {(pow(2, m, 37) * h) % 37 for h in H}:
            return m
    return None


def cubic_f(x):
    return (x ** 3 + 5) % 37


# ─── Part 1: Orbit invariance of f(x) = x^3 + 5 ──────────────────────────────

def verify_orbit_invariance():
    """26^3 ≡ 1 forces f constant on each orbit."""
    assert pow(26, 3, 37) == 1, "26^3 mod 37 must be 1"

    fval_by_orbit = {}
    for name, elems in ORBITS.items():
        vals = {cubic_f(x) for x in elems}
        assert len(vals) == 1, f"{name}: f not constant — {vals}"
        fval_by_orbit[name] = vals.pop()

    return fval_by_orbit


# ─── Part 2: QR partition of the 12 orbits ────────────────────────────────────

def qr_partition(fval_by_orbit):
    """
    Classify each orbit by whether f(orbit) is QR or NQR.

    QR-valued orbits supply x-coordinates to E; NQR-valued orbits do not.
    Partition is exactly 6+6.
    """
    qr_orbits  = {o for o, v in fval_by_orbit.items() if v in QR_MOD37}
    nqr_orbits = {o for o, v in fval_by_orbit.items() if v not in QR_MOD37}
    assert len(qr_orbits) == 6 and len(nqr_orbits) == 6, "Expected 6+6 partition"
    return qr_orbits, nqr_orbits


# ─── Part 3: Anomalous curve point count and x-orbit support ──────────────────

def count_points_and_orbits():
    """
    Enumerate all points on y^2 = x^3 + 5 (mod 37).
    Confirm #E = 37 (anomalous) and record which orbits appear as x-coordinates.
    """
    affine_points = []
    for x in range(37):
        rhs = cubic_f(x)
        for y in range(37):
            if (y * y) % 37 == rhs:
                affine_points.append((x, y))
    total = len(affine_points) + 1  # +1 for point at infinity
    assert total == 37, f"Expected #E=37, got {total}"

    x_orbits = {}
    for x, _ in affine_points:
        if x % 37 != 0:
            o = get_orbit(x)
            x_orbits[o] = x_orbits.get(o, 0) + 1
    return affine_points, x_orbits


# ─── Part 4: Point sequence G, 2G, ..., 36G ───────────────────────────────────

def point_sequence():
    """
    Scalar multiples of G = (6, 6) on y^2 = x^3 + 5 (mod 37).

    Records orbit of x- and y-coordinate at each step.
    Same-orbit events (x and y in same orbit) occur at k = 5, 10, 13, 17, 19, 22, 26, 35.
    """
    x1, y1 = 6, 6
    cx, cy = x1, y1
    sequence = [{'k': 1, 'pt': (x1, y1), 'x_orbit': get_orbit(x1),
                 'y_orbit': get_orbit(y1), 'x_class': get_class(x1)}]

    for k in range(2, 37):
        x0, y0 = cx, cy
        if (x0 - x1) % 37 == 0 and y0 == y1:
            lam = (3 * x0 * x0 * pow(2 * y0, -1, 37)) % 37
        else:
            lam = ((y0 - y1) * pow(x0 - x1, -1, 37)) % 37
        cx = (lam * lam - x0 - x1) % 37
        cy = (lam * (x0 - cx) - y0) % 37
        sequence.append({'k': k, 'pt': (cx, cy), 'x_orbit': get_orbit(cx),
                         'y_orbit': get_orbit(cy), 'x_class': get_class(cx)})
    return sequence


# ─── Part 5: Structural summary ───────────────────────────────────────────────

def structural_summary(fval_by_orbit, qr_orbits, nqr_orbits, x_orbits, sequence):
    """Print full T287 verification report."""

    print("=" * 68)
    print("T287 — Anomalous Curve y^2 = x^3 + 5 over F_37: Orbit Partition")
    print("=" * 68)

    print("\n--- Part 1: 26^3 ≡ 1 (mod 37) — f orbit-invariant ---")
    print(f"  26^3 mod 37 = {pow(26, 3, 37)}  (ord_37(26)=3, so 26^3≡1)")
    print("  f(26x) = 26^3·x^3 + 5 ≡ x^3 + 5 = f(x)  ∀x ∈ F_37*")
    print()
    print(f"  {'Orbit':10s}  {'f(orbit)':8s}  {'f orbit':10s}  QR?")
    print(f"  {'-'*10}  {'-'*8}  {'-'*10}  ---")
    for name in sorted(ORBITS):
        fv = fval_by_orbit[name]
        is_qr = fv in QR_MOD37
        fo = get_orbit(fv)
        mark = 'QR ✓ (x-coords)' if is_qr else 'NQR  (absent)'
        print(f"  {name:10s}  {fv:8d}  {fo:10s}  {mark}")

    print("\n--- Part 2: QR partition (6+6) ---")
    print(f"  QR-valued  (supply x-coords): {sorted(qr_orbits)}")
    print(f"  NQR-valued (absent from E):   {sorted(nqr_orbits)}")

    print("\n--- Part 3: #E(F_37) = 37, trace t = 1 (anomalous) ---")
    print(f"  Point count confirmed:  37")
    print(f"  X-orbit hit counts (2G..36G): {dict(sorted(x_orbits.items()))}")
    print(f"  Absent x-orbits:  {sorted(nqr_orbits)}")
    print(f"  QR-orbits == appearing orbits: {qr_orbits == set(x_orbits.keys())}")

    print("\n--- Part 4: G = (6,6) and notable multiples ---")
    notable = {1, 2, 5, 10, 13, 17, 19, 22, 26, 35}
    same_orbit_ks = []
    for row in sequence:
        k = row['k']
        x, y = row['pt']
        xo = row['x_orbit']
        yo = row['y_orbit']
        same = xo == yo
        if same:
            same_orbit_ks.append(k)
        if k in notable:
            tag = ' ← SAME ORBIT' if same else ''
            print(f"  {k:2d}G = ({x:2d},{y:2d})  x:{xo:8s}(cl{row['x_class']:2d})  y:{yo:8s}{tag}")
    print(f"\n  Same-orbit (x,y) events at k = {same_orbit_ks}")
    print(f"  Orbits at same-orbit events: "
          f"{[sequence[k-1]['x_orbit'] for k in same_orbit_ks]}")
    print()
    print("  Same-orbit k-orbit → x-orbit rule (exact):")
    print("    k ∈ IC      = {1,10,26}  → x,y ∈ TESLA  (Z/12Z classes 0→3)")
    print("    k ∈ CAS_EXT = {5,13,19}  → x,y ∈ C9     (Z/12Z classes 11→9)")
    print("    k ∈ NQR17   = {17,22,35} → x,y ∈ SEED   (Z/12Z classes 7→5)")
    print("  Note: TESLA↔C9 antipodal (T283); SEED↔CAS_EXT antipodal (T283).")
    print("  The three k-orbits {IC,CAS_EXT,NQR17} are the NQR-valued orbits")
    print("  that are NOT absent from E — i.e., their antipodals {NEG_H,SEED,DARK_A}?")
    # Verify exact: which k-orbits trigger same-orbit events
    ko_set = {sequence[k-1]['x_orbit'] for k in same_orbit_ks}  # x-orbits at event k
    k_orbit_set = set()
    elem_to_orbit = {}
    for nm, els in ORBITS.items():
        for e in els:
            elem_to_orbit[e] = nm
    for k in same_orbit_ks:
        k_orbit_set.add(elem_to_orbit.get(k, '?'))
    print(f"  k-orbits at same-orbit events: {sorted(k_orbit_set)}")
    print(f"  x-orbits at same-orbit events: {sorted(ko_set)}")

    print("\n--- Part 5: Standing analysis ---")
    for v, label in [(6,'G.x=G.y'), (9,'lambda'), (32,'2G.x'), (19,'2G.y'),
                     (31,'5G.x'), (14,'5G.y')]:
        from_prime = 'prime' if all(v % i != 0 for i in range(2, v)) and v > 1 else 'composite'
        twin = from_prime == 'prime' and (
            all((v-2) % i != 0 for i in range(2, v-2)) and v-2 > 1 or
            all((v+2) % i != 0 for i in range(2, v+2)) and v+2 > 1)
        r30 = _rule30(v)
        print(f"  v={v:2d} ({label}): orbit={get_orbit(v)}, cl={get_class(v)}, "
              f"{from_prime}, twin={twin}, "
              f"R30={r30}≡{r30%37}(mod37)={get_orbit(r30%37)}, "
              f"×137≡{(v*137)%37}={get_orbit((v*137)%37)}")

    print("\n  5 ∈ CAS_EXT: prime, twin, Sophie-Germain (2·5+1=11 prime), safe prime check:")
    print(f"    5 SG: 2·5+1=11 prime → True; 5 safe: (5-1)/2=2 prime → True")
    print(f"    5 × 137 mod 37 = {(5*137)%37} ∈ CAS_EXT (orbit-closed)")


def _rule30(n, bits=8):
    s = format(n, f'0{bits}b')
    r = ''
    for i in range(bits):
        L = int(s[(i-1) % bits])
        C = int(s[i])
        R = int(s[(i+1) % bits])
        r += str(L ^ (C | R))
    return int(r, 2)


if __name__ == '__main__':
    fval_by_orbit = verify_orbit_invariance()
    qr_orbits, nqr_orbits = qr_partition(fval_by_orbit)
    affine_points, x_orbits = count_points_and_orbits()
    sequence = point_sequence()
    structural_summary(fval_by_orbit, qr_orbits, nqr_orbits, x_orbits, sequence)

    # Final assertions
    assert pow(26, 3, 37) == 1
    assert len(affine_points) + 1 == 37
    assert qr_orbits == set(x_orbits.keys())
    print("\nAll T287 assertions passed.")
