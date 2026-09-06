"""
T289 — Quadratic Twist Pairs of j=0 Curves over F_37 = H_4-Coset Partition

From T288: the 6 isomorphism classes of y^2=x^3+a over F_37 (a≠0) correspond
to the 6 antipodal orbit pairs, with Frobenius traces ±{1,10,11}.

The quadratic twist of y^2=x^3+a by a non-square d is y^2=x^3+a·d, which
negates the Frobenius trace: t(twist) = -t.  This pairs the 6 classes into
3 quadratic twist pairs.

Result: each twist pair differs by exactly +3 in Z/12Z.  The 3 twist pairs
are exactly the 3 cosets of H_4 = {IC, TESLA, NEG_H, C9} (Z/12Z classes
{0,3,6,9}) in Z/12Z.  This is the subgroup of order 4 (T286).

H_4-coset structure of the twist pairs:

  Coset         Classes    Orbits                    |t|  ord_⟨11⟩(|t|)
  H_4           {0,3,6,9}  IC,TESLA,NEG_H,C9         10   3
  H_4 + DARK_A  {1,4,7,10} DARK_A,SA_ST_A,NQR17,SA_ST_B  11   6
  H_4 + C3      {2,5,8,11} C3,CAS_EXT,D7,SEED         1   1  ← ANOMALOUS

Each coset contains exactly one twist pair of antipodal-pair classes.
The absolute trace within a coset has a fixed order in ⟨11⟩:
  H_4 coset:       |t|=10, ord_⟨11⟩=3  (element of order 3 in cyclic-6 group)
  H_4+1 coset:     |t|=11, ord_⟨11⟩=6  (generator of ⟨11⟩)
  H_4+2 coset:     |t|=1,  ord_⟨11⟩=1  (identity; anomalous trace)

The three element orders {1,3,6} are the three distinct orders in a cyclic
group of order 6, one per coset.

The anomalous class (t=1, SEED↔CAS_EXT) is in H_4+C3.  Its twist is C3↔D7
(t=-1, #E=39).  The anomalous trace is the identity element of ⟨11⟩.

Quadratic twist = multiply a by any element of TESLA = {6,8,23} (shift +3
in Z/12Z). TESLA elements are all non-squares mod 37.
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
OPERATOR_GROUP = {1, 10, 11, 26, 27, 36}  # ⟨11⟩ = IC ∪ NEG_H

ELEM_TO_ORBIT = {}
for name, elems in ORBITS.items():
    for e in elems:
        ELEM_TO_ORBIT[e] = name

QR = {(i * i) % 37 for i in range(1, 37)}


def get_class(x):
    H = {1, 10, 26}
    for m in range(12):
        if x % 37 in {(pow(2, m, 37) * h) % 37 for h in H}:
            return m
    return None


def count_points(a):
    n = 1
    for x in range(37):
        rhs = (x ** 3 + a) % 37
        for y in range(37):
            if (y * y) % 37 == rhs:
                n += 1
    return n


def gf37_order(x):
    """Multiplicative order of x in GF(37)*."""
    x = x % 37
    if x == 0:
        return None
    acc, k = x, 1
    while acc != 1:
        acc = (acc * x) % 37
        k += 1
    return k


# ─── Part 1: traces per isomorphism class ────────────────────────────────────

def trace_table():
    table = {}
    for a_name, b_name in ANTIPODAL:
        a = sorted(ORBITS[a_name])[0]
        E = count_points(a)
        t = 38 - E
        ca = get_class(a)
        cb = get_class(sorted(ORBITS[b_name])[0])
        table[(a_name, b_name)] = {'E': E, 't': t, 'ca': ca, 'cb': cb}
    return table


# ─── Part 2: twist pairs ──────────────────────────────────────────────────────

def find_twist_pairs(table):
    pairs = list(ANTIPODAL)
    used = set()
    twist_pairs = []
    for i, k1 in enumerate(pairs):
        if i in used:
            continue
        t1 = table[k1]['t']
        for j, k2 in enumerate(pairs):
            if j <= i or j in used:
                continue
            if table[k2]['t'] + t1 == 0:
                twist_pairs.append((k1, k2))
                used.add(i)
                used.add(j)
    assert len(twist_pairs) == 3, f"Expected 3 twist pairs, got {len(twist_pairs)}"
    return twist_pairs


# ─── Part 3: twist pairs = H_4 cosets ────────────────────────────────────────

def verify_h4_cosets(twist_pairs, table):
    H4_classes = {get_class(x) for orb in ['IC', 'TESLA', 'NEG_H', 'C9']
                  for x in ORBITS[orb]}
    assert H4_classes == {0, 3, 6, 9}, f"H_4 classes: {H4_classes}"

    for k1, k2 in twist_pairs:
        ca1 = table[k1]['ca']
        ca2 = table[k2]['ca']
        diff = (ca2 - ca1) % 12
        assert diff == 3, f"Twist pair {k1}↔{k2}: class diff = {diff}, expected 3"

    # Each twist pair must lie in one H_4 coset
    for rep in range(3):
        coset = {(h + rep) % 12 for h in H4_classes}
        found = False
        for k1, k2 in twist_pairs:
            ca1, cb1 = table[k1]['ca'], table[k1]['cb']
            ca2, cb2 = table[k2]['ca'], table[k2]['cb']
            if {ca1, cb1, ca2, cb2} == coset:
                found = True
        assert found, f"Coset {coset} not matched by any twist pair"

    return H4_classes


# ─── Part 4: absolute trace orders in ⟨11⟩ ───────────────────────────────────

def verify_trace_orders(twist_pairs, table):
    orders = set()
    for k1, k2 in twist_pairs:
        abs_t = abs(table[k1]['t'])
        ord_t = gf37_order(abs_t)
        assert ord_t in {1, 3, 6}, f"|t|={abs_t} has order {ord_t}, expected in {{1,3,6}}"
        orders.add(ord_t)
    assert orders == {1, 3, 6}, f"Trace orders: {orders}, expected {{1,3,6}}"


# ─── Part 5: TESLA elements are all NQR ──────────────────────────────────────

def verify_tesla_nqr():
    for t in ORBITS['TESLA']:
        assert t not in QR, f"TESLA element {t} is QR"


# ─── Part 6: full report ──────────────────────────────────────────────────────

def run():
    table = trace_table()
    twist_pairs = find_twist_pairs(table)
    H4_classes = verify_h4_cosets(twist_pairs, table)
    verify_trace_orders(twist_pairs, table)
    verify_tesla_nqr()

    print("=" * 68)
    print("T289 — Quadratic Twist Pairs = H_4-Coset Partition of Z/12Z")
    print("=" * 68)

    print("\n--- Part 1: Twist pairs (t ↔ -t), each at Z/12Z distance 3 ---")
    for k1, k2 in twist_pairs:
        t1, t2 = table[k1]['t'], table[k2]['t']
        ca1, ca2 = table[k1]['ca'], table[k2]['ca']
        abs_t = abs(t1)
        ord_t = gf37_order(abs_t)
        print(f"  {k1[0]}↔{k1[1]} (t={t1:+3d}, cl {ca1},{table[k1]['cb']}) "
              f"↔ {k2[0]}↔{k2[1]} (t={t2:+3d}, cl {ca2},{table[k2]['cb']})"
              f"  |t|={abs_t}  ord_<11>({abs_t})={ord_t}")

    print("\n--- Part 2: H_4 cosets contain exactly one twist pair each ---")
    H4_classes = {0, 3, 6, 9}
    for rep in range(3):
        coset = {(h + rep) % 12 for h in H4_classes}
        for k1, k2 in twist_pairs:
            ca1, cb1 = table[k1]['ca'], table[k1]['cb']
            ca2, cb2 = table[k2]['ca'], table[k2]['cb']
            if {ca1, cb1, ca2, cb2} == coset:
                abs_t = abs(table[k1]['t'])
                ord_t = gf37_order(abs_t)
                anom = " ← ANOMALOUS coset" if abs_t == 1 else ""
                print(f"  Coset {sorted(coset)}: {k1[0]}↔{k1[1]} / {k2[0]}↔{k2[1]}"
                      f"  |t|={abs_t}  ord={ord_t}{anom}")

    print("\n--- Part 3: Absolute trace orders = {{1,3,6}} in <11> ---")
    print("  Orders {1,3,6} are the three distinct element orders in Z/6Z")
    print("  (cyclic group of order 6 ≅ <11>): generators(ord 6), order-3, identity")

    print("\n--- Part 4: Quadratic twist = multiply a by TESLA = {6,8,23} ---")
    for t_elem in sorted(ORBITS['TESLA']):
        qr_status = 'QR' if t_elem in QR else 'NQR'
        print(f"  a → a×{t_elem}  ({qr_status}, shift class +3 in Z/12Z)")

    print("\n--- Part 5: Anomalous class in H_4+C3 coset ---")
    print(f"  SEED↔CAS_EXT: t=1  (identity in <11>)")
    print(f"  Twist = C3↔D7:    t=-1, #E=39")
    print(f"  Anomalous twist has #E=39=p+2, 2 more points than the prime itself")
    print(f"  39 mod 37 = 2 ∈ DARK_A")

    print("\nAll T289 assertions passed.")


if __name__ == '__main__':
    run()
