"""
THEOREM 116 — Multiplicative Orders of All Residues Modulo 37

Since 37 is prime, every a with 1 ≤ a ≤ 36 is invertible and
ord₃₇(a) divides φ(37) = 36.

COMPLETE ORDER TABLE (verified by direct computation)

  a   ord |  a   ord |  a   ord |  a   ord
  1    1  |  10   3  |  19  36  |  28  18
  2   36  |  11   6  |  20  36  |  29  12
  3   18  |  12   9  |  21  18  |  30  18
  4   18  |  13  36  |  22  36  |  31   4
  5   36  |  14  12  |  23  12  |  32  36
  6    4  |  15  36  |  24  36  |  33   9
  7    9  |  16   9  |  25  18  |  34   9
  8   12  |  17  36  |  26   3  |  35  36
  9    9  |  18  36  |  27   6  |  36   2

PARTITION BY ORDER
  Every d | 36 gives exactly φ(d) elements of that order:

  Order  1:  {1}                                count =  1 = φ(1)
  Order  2:  {36}                               count =  1 = φ(2)
  Order  3:  {10, 26}                           count =  2 = φ(3)
  Order  4:  {6, 31}                            count =  2 = φ(4)
  Order  6:  {11, 27}                           count =  2 = φ(6)
  Order  9:  {7, 9, 12, 16, 33, 34}            count =  6 = φ(9)
  Order 12:  {8, 14, 23, 29}                    count =  4 = φ(12)
  Order 18:  {3, 4, 21, 25, 28, 30}            count =  6 = φ(18)
  Order 36:  {2,5,13,15,17,18,19,20,22,24,32,35}  count = 12 = φ(36)

ORDER PROFILES OF NAMED FRAMEWORK CLASSES

  Class       Elements        Orders          Uniform?
  IC          {1, 10, 26}     {1, 3, 3}       No  — identity + cube roots of unity
  SA          {4, 9, 25, 30}  {9,18,18,18}    No  — 9 is order-9, rest order-18
  ST          {3,12,21,30}    {9,18,18,18}    No  — 12 is order-9, rest order-18
  CB          {8,13,24}       {12,36,36}      No  — 8 is order-12, 13,24 are PR
  ORBIT_11    {11,27,36}      {6,6,2}         No  — 36≡-1 has order 2
  SEED_ORBIT  {18,24,32}      {36,36,36}      YES — entirely primitive roots
  BASIN_Y     {17,22,35}      {36,36,36}      YES — entirely primitive roots
  D7          {7,33,34}       {9,9,9}         YES — uniform order 9

KEY STRUCTURAL FACTS

  (A) ord₃₇(26) = 3.
      The 137-map f(n)=26n mod 37 has period 3. All orbits are 3-cycles.
      This is the algebraic reason every orbit in the framework has length 3.

  (B) SEED_ORBIT {18,24,32} ⊂ PR.
      The seed orbit of the reference run (seed=246, 246 mod 37=24) consists
      entirely of primitive roots — generators of (ℤ/37ℤ)×.

  (C) BASIN_Y {17,22,35} ⊂ PR.
      Basin Y is also entirely primitive roots.

  (D) D7 = {7,33,34} has uniform order 9 = 36/4.
      These are elements of the unique subgroup of index 4 (order 9)
      in the cyclic group (ℤ/37ℤ)×.

  (E) 36 ≡ -1 (mod 37), ord₃₇(36) = 2.
      The lone element of order 2 is −1 (Fermat: (−1)² = 1).
      36 ∈ ORBIT_11 — the element of lowest order in that set.

  (F) IC = {1, 10, 26}: the three cube roots of unity mod 37.
      1 has order 1; 10 and 26 have order 3.
      26 is simultaneously the 137-map multiplier and a cube root of unity.
"""

P = 37


def multiplicative_order(g, p):
    o, x = 1, g % p
    while x != 1:
        x = (x * g) % p
        o += 1
    return o


# Complete order table as stated
ORDER_TABLE = {
     1: 1,   2:36,  3:18,  4:18,  5:36,  6: 4,  7: 9,  8:12,  9: 9,
    10: 3,  11: 6, 12: 9, 13:36, 14:12, 15:36, 16: 9, 17:36, 18:36,
    19:36,  20:36, 21:18, 22:36, 23:12, 24:36, 25:18, 26: 3, 27: 6,
    28:18,  29:12, 30:18, 31: 4, 32:36, 33: 9, 34: 9, 35:36, 36: 2,
}

SA         = {4, 9, 25, 30}
ST         = {3, 12, 21, 30}
IC         = {1, 10, 26}
CB         = {8, 13, 24}
ORBIT_11   = {11, 27, 36}
SEED_ORBIT = {18, 24, 32}
BASIN_Y    = {17, 22, 35}
D7         = {7, 33, 34}
PR         = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}


def run():
    from collections import defaultdict
    from sympy import totient, divisors

    print("=" * 66)
    print("THEOREM 116 — MULTIPLICATIVE ORDERS OF ALL RESIDUES MOD 37")
    print("=" * 66)

    # ---------------------------------------------------------------
    # PART 1 — Verify the complete table
    # ---------------------------------------------------------------
    print("\n--- Part 1: Verify all 36 orders ---")
    for a, expected in ORDER_TABLE.items():
        actual = multiplicative_order(a, P)
        assert actual == expected, f"ord({a}) = {actual}, expected {expected}"
    print("  All 36 orders match the stated table.  ✓")

    # ---------------------------------------------------------------
    # PART 2 — Partition by order; verify φ(d) law
    # ---------------------------------------------------------------
    print("\n--- Part 2: Partition by order — count = φ(d) for each d | 36 ---")
    by_order = defaultdict(list)
    for a, o in sorted(ORDER_TABLE.items()):
        by_order[o].append(a)

    for d in sorted(divisors(36)):
        count  = len(by_order[d])
        phi_d  = totient(d)
        assert count == phi_d, f"order-{d} count={count} ≠ φ({d})={phi_d}"
        print(f"  ord={d:>2}: {str(by_order[d]):<45}  count={count} = φ({d})")

    assert sum(len(v) for v in by_order.values()) == 36
    print("  Partition is complete: all 36 residues accounted for.  ✓")

    # ---------------------------------------------------------------
    # PART 3 — Order profiles of named classes
    # ---------------------------------------------------------------
    print("\n--- Part 3: Order profiles of named framework classes ---")
    named = [
        ('IC',       IC),
        ('SA',       SA),
        ('ST',       ST),
        ('CB',       CB),
        ('ORBIT_11', ORBIT_11),
        ('SEED_ORBIT', SEED_ORBIT),
        ('BASIN_Y',  BASIN_Y),
        ('D7',       D7),
    ]
    for name, cls in named:
        profile = sorted(ORDER_TABLE[g] for g in cls)
        uniform = len(set(profile)) == 1
        print(f"  {name:<12} {sorted(cls)}  orders={profile}  uniform={uniform}")

    # ---------------------------------------------------------------
    # PART 4 — Key structural facts
    # ---------------------------------------------------------------
    print("\n--- Part 4: Key structural facts ---")

    # (A) ord(26) = 3
    assert ORDER_TABLE[26] == 3
    assert all(ORDER_TABLE[g] == 3 for g in {10, 26})
    print(f"  (A) ord₃₇(26) = {ORDER_TABLE[26]}  →  all 137-map orbits are 3-cycles")

    # (B) SEED_ORBIT ⊂ PR
    assert SEED_ORBIT <= PR
    assert all(ORDER_TABLE[g] == 36 for g in SEED_ORBIT)
    print(f"  (B) SEED_ORBIT {{18,24,32}} ⊂ PR  (all primitive roots, orders all 36)")

    # (C) BASIN_Y ⊂ PR
    assert BASIN_Y <= PR
    assert all(ORDER_TABLE[g] == 36 for g in BASIN_Y)
    print(f"  (C) BASIN_Y {{17,22,35}} ⊂ PR  (all primitive roots, orders all 36)")

    # (D) D7 uniform order 9
    assert all(ORDER_TABLE[g] == 9 for g in D7)
    subgroup_order9 = set(by_order[9])
    assert D7 <= subgroup_order9
    print(f"  (D) D7 {{7,33,34}} ⊂ order-9 elements {sorted(subgroup_order9)}")
    print(f"      order 9 = 36/4: unique subgroup of index 4 in (ℤ/37ℤ)×")

    # (E) 36 = -1 mod 37, order 2
    assert ORDER_TABLE[36] == 2
    assert 36 % P == P - 1   # 36 ≡ -1
    assert 36 in ORBIT_11
    print(f"  (E) 36 ≡ -1 (mod 37),  ord₃₇(36) = {ORDER_TABLE[36]}")
    print(f"      36 ∈ ORBIT_11 — sole element of order 2 in that set")

    # (F) IC = cube roots of unity
    assert ORDER_TABLE[1] == 1
    assert ORDER_TABLE[10] == 3 and ORDER_TABLE[26] == 3
    assert {g for g in range(1, P) if pow(g, 3, P) == 1} == IC
    print(f"  (F) IC = {{1,10,26}} = cube roots of unity mod 37")
    print(f"      26 = 137-map multiplier = primitive cube root of unity")

    # CB mixed: 8 is order-12, 13 and 24 are PR
    assert ORDER_TABLE[8] == 12
    assert ORDER_TABLE[13] == 36 and ORDER_TABLE[24] == 36
    print(f"  (G) CB = {{8,13,24}}: 8 has order 12 (not PR); 13,24 have order 36 (PR)")

    # ORBIT_11 mixed: 11→6, 27→6, 36→2
    assert ORDER_TABLE[11] == 6 and ORDER_TABLE[27] == 6 and ORDER_TABLE[36] == 2
    print(f"  (H) ORBIT_11 = {{11,27,36}}: 11,27 have order 6; 36≡-1 has order 2")

    print()
    print("All assertions passed. THEOREM 116 verified.")


if __name__ == "__main__":
    run()
