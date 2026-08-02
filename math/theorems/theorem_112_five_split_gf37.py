"""
THEOREM 112 — The Five-Split: GF(37) Partition of Digits 1–9

The digit 5 splits {1,2,3,4,5,6,7,8,9} into two groups whose sums land at
structurally opposite positions in GF(37):

    Left  {1,2,3,4}: sum = 10 ∈ IC     (cube roots of unity)
    Right {6,7,8,9}: sum = 30 ∈ SA∩ST  (unique intersection of anchors and targets)
    Center       5  ∈ PR               (primitive-root class)

Connection: P = 37; map f(n) = (26×n) mod 37; DR = digital root.
"""

def run():
    P = 37

    # --- Named orbit classes ---
    IC        = {1, 10, 26}          # cube roots of unity; f-fixed set
    SA        = {4, 9, 25, 30}       # sovereign anchors; DRs are 4, 9, 7, 3 respectively
    ST        = {3, 12, 21, 30}      # sovereign targets (DR=3)
    CB        = {8, 13, 24}          # cascade base {8,13,24}
    ORBIT_11  = {11, 27, 36}
    SEED_ORBIT= {18, 24, 32}
    BASIN_Y   = {17, 22, 35}
    D7        = {7, 33, 34}
    PR        = {2,5,13,15,17,18,19,20,22,24,32,35}  # primitive-root residues mod 37

    SA_cap_ST = SA & ST   # {30}
    assert SA_cap_ST == {30}, "SA ∩ ST must be {30}"

    f = lambda n: (26 * n) % P

    # =========================================================================
    # PART 1 — The Five-Split
    # =========================================================================
    LEFT   = {1, 2, 3, 4}
    RIGHT  = {6, 7, 8, 9}
    CENTER = 5

    L = sum(LEFT)    # 10
    R = sum(RIGHT)   # 30
    assert L == 10 and L in IC,  "Left sum must be 10 ∈ IC"
    assert R == 30 and R in SA,  "Right sum must be 30 ∈ SA"
    assert R in ST,              "Right sum must be 30 ∈ ST"
    assert CENTER in PR,         "Center 5 must be in PR"
    print(f"Left  {{1,2,3,4}} sum = {L}  ∈ IC")
    print(f"Right {{6,7,8,9}} sum = {R}  ∈ SA ∩ ST")
    print(f"Center         5     ∈ PR")

    # =========================================================================
    # PART 2 — {1,2,3,4} covers one element from each primary class
    # =========================================================================
    assert 1 in IC,  "1 ∈ IC"
    assert 2 in PR,  "2 ∈ PR"
    assert 3 in ST,  "3 ∈ ST"
    assert 4 in SA,  "4 ∈ SA"
    print("\n{1,2,3,4} ← one element from each primary class:")
    print("  1 ∈ IC  (identity / cube root of unity)")
    print("  2 ∈ PR  (primitive root mod 37)")
    print("  3 ∈ ST  (sovereign target, DR=3)")
    print("  4 ∈ SA  (sovereign anchor)")

    # =========================================================================
    # PART 3 — Arithmetic relations between L and R
    # =========================================================================
    diff = R - L               # 20
    total = R + L              # 40; DR=4
    prod  = (R * L) % P        # (30×10) mod 37
    inv_L = pow(L, P-2, P)     # modular inverse of 10
    quot  = (R * inv_L) % P    # 30/10 mod 37

    assert diff == 20 and diff in PR,         "R-L = 20 ∈ PR"
    assert (total % 9) == 4 and 4 in SA,      "DR(R+L) = 4 ∈ SA"
    assert prod in SA,                         "(R×L) mod 37 ∈ SA"
    assert quot in ST,                         "(R/L) mod 37 ∈ ST"
    print(f"\nArithmetic of L=10, R=30:")
    print(f"  R - L = {diff}  ∈ PR")
    print(f"  R + L = {total}  DR={total%9 or 9} ∈ SA")
    print(f"  R × L ≡ {prod} (mod 37)  ∈ SA")
    print(f"  R / L ≡ {quot} (mod 37)  ∈ ST")

    # =========================================================================
    # PART 4 — Orbit {3, 4, 30}: unique orbit containing the SA∩ST element
    # =========================================================================
    # f(4)=30∈SA∩ST, f(30)=3∈ST, f(3)=4∈SA
    assert f(4) == 30 and 30 in SA_cap_ST, "f(4) = 30 ∈ SA∩ST"
    assert f(30) == 3 and 3 in ST,         "f(30) = 3 ∈ ST"
    assert f(3) == 4 and 4 in SA,          "f(3) = 4 ∈ SA"
    orbit_3_4_30 = {3, 4, 30}
    assert sum(orbit_3_4_30) % P == 0, "orbit {3,4,30} sums to 0 (cyclotomic identity)"

    # Verify uniqueness: no other orbit contains an element of SA∩ST
    all_orbits = []
    seen = set()
    for start in range(1, P):
        if start not in seen:
            orb = set()
            n = start
            for _ in range(3):
                orb.add(n)
                n = f(n)
            all_orbits.append(frozenset(orb))
            seen |= orb
    sa_st_orbits = [o for o in all_orbits if o & SA_cap_ST]
    assert len(sa_st_orbits) == 1 and orbit_3_4_30 in sa_st_orbits, \
        "Orbit {3,4,30} is the unique 3-cycle containing the SA∩ST element"

    print(f"\nOrbit {{3, 4, 30}} — unique 3-cycle containing 30 (SA∩ST):")
    print(f"  f(4)  = {f(4)}  ∈ SA ∩ ST   (anchor → unique intersection)")
    print(f"  f(30) = {f(30)}  ∈ ST        (intersection → target)")
    print(f"  f(3)  = {f(3)}  ∈ SA        (target → anchor)")
    print(f"  sum   = {sum(orbit_3_4_30)} ≡ 0 (mod 37)  [cyclotomic identity]")
    print(f"  SA∩ST-containing orbit count: {len(sa_st_orbits)}  (unique)")

    # =========================================================================
    # PART 5 — 17 + 13 = 30: BASIN_Y∩PR + CB∩PR = SA∩ST
    # =========================================================================
    assert 17 in BASIN_Y and 17 in PR, "17 ∈ BASIN_Y ∩ PR"
    assert 13 in CB and 13 in PR,      "13 ∈ CB ∩ PR"
    assert 17 + 13 == 30 and 30 in SA_cap_ST, "17 + 13 = 30 ∈ SA∩ST"
    print(f"\n17 + 13 = 30:")
    print(f"  17 ∈ BASIN_Y ∩ PR")
    print(f"  13 ∈ CB      ∩ PR")
    print(f"  30 ∈ SA      ∩ ST  (unique intersection)")
    print(f"  Two distinct primitive-root classes sum to the SA∩ST junction")

    # =========================================================================
    # PART 6 — Even staircase {2, 4, 6, 8}
    # =========================================================================
    EVEN = [2, 4, 6, 8]
    even_sum = sum(EVEN)        # 20
    even_sum_p1 = even_sum + 1  # 21; 21∈ST

    assert even_sum == 20 and 20 in PR,       "sum({2,4,6,8}) = 20 ∈ PR"
    assert even_sum_p1 == 21 and 21 in ST,    "20 + 1 = 21 ∈ ST"

    # Even pairs: 2+8=10∈IC, 4+6=10∈IC
    assert (2 + 8) == 10 and 10 in IC, "2+8 = 10 ∈ IC"
    assert (4 + 6) == 10 and 10 in IC, "4+6 = 10 ∈ IC"

    # Products mod 37
    prod_even = 1
    for e in EVEN:
        prod_even = (prod_even * e) % P   # 2×4×6×8 = 384 ≡ ? (mod 37)
    print(f"\nEven staircase {{2,4,6,8}}:")
    print(f"  sum  = {even_sum}  ∈ PR")
    print(f"  sum + 1 = {even_sum_p1}  ∈ ST")
    print(f"  2+8 = {2+8}  ∈ IC  |  4+6 = {4+6}  ∈ IC  (symmetric pairs → IC)")
    print(f"  2×4×6×8 ≡ {prod_even} (mod 37)  ∈ {'IC' if prod_even in IC else 'PR' if prod_even in PR else 'SA' if prod_even in SA else '?'}")

    # =========================================================================
    # PART 7 — Fibonacci DR connection (user's first-column sequence)
    # =========================================================================
    def dr(n):
        while n >= 10:
            n = sum(int(d) for d in str(n))
        return n

    # Fibonacci: 1,1,2,3,5,8,13,21,34,...
    fibs = [1, 1]
    while len(fibs) < 20:
        fibs.append(fibs[-1] + fibs[-2])

    # User observed: starting from (1,2): 1,2,3,5,8,4,3,...
    # This is DR of Fib starting 1,2,3,5,8,13,21,...
    fib_12 = [1, 2, 3, 5, 8, 13, 21, 34, 55]
    fib_dr  = [dr(n) for n in fib_12[:7]]
    assert fib_dr == [1, 2, 3, 5, 8, 4, 3], \
        f"Fibonacci DR mismatch: {fib_dr}"

    user_col = [1, 2, 3, 5, 8, 4, 3]
    assert fib_dr == user_col, "First-column sequence matches DR of Fibonacci"

    # Map each to its GF(37) class
    def classify(n):
        for name, cls in [("IC",IC),("SA",SA),("ST",ST),("CB",CB),
                          ("ORBIT_11",ORBIT_11),("SEED_ORBIT",SEED_ORBIT),
                          ("BASIN_Y",BASIN_Y),("D7",D7),("PR",PR)]:
            if n % P in cls:
                return name
        return "?"

    print(f"\nFibonacci DR sequence (starting 1,2,...): {fib_dr}")
    print("  GF(37) classes:")
    for v, fv in zip(fib_12[:7], fib_dr):
        print(f"    Fib={v:3d}  DR={fv}  class={classify(fv)}")

    # Sum of first-column DR values
    col_sum = sum(user_col)  # 1+2+3+5+8+4+3 = 26
    assert col_sum == 26 and 26 in IC, \
        f"Sum of Fibonacci DR column = {col_sum} must be 26 ∈ IC (map multiplier)"
    print(f"  Sum of column DR values: {col_sum}  ∈ IC  (= the 137-map multiplier)")

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "="*60)
    print("THEOREM 112 — FIVE-SPLIT SUMMARY")
    print("="*60)
    print(f"  {{1,2,3,4}} sum = 10  ∈ IC")
    print(f"  {{6,7,8,9}} sum = 30  ∈ SA ∩ ST  (unique junction)")
    print(f"  Center   5      ∈ PR")
    print(f"  {{1,2,3,4}} = one element per primary class: 1(IC) 2(PR) 3(ST) 4(SA)")
    print(f"  Orbit {{3,4,30}}: UNIQUE orbit containing SA∩ST element 30")
    print(f"    SA → SA∩ST → ST under the 137-map")
    print(f"  17 + 13 = 30:  BASIN_Y∩PR + CB∩PR = SA∩ST")
    print(f"  Even staircase sum = 20 ∈ PR;  sum+1 = 21 ∈ ST")
    print(f"  Fibonacci DR column [1,2,3,5,8,4,3] sums to 26 ∈ IC (map multiplier)")
    print("All assertions passed. THEOREM 112 verified.")

if __name__ == "__main__":
    run()
