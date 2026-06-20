# math/theorems/multiplication_dr_chains_audit.py
"""
Multiplication DR Chains — Seeds 2, 3, 4, 5
============================================
Each chain starts 1×n = n and applies a multiplier sequence.
Identity steps (×1) mark positions but do not change the running product.
The ~ or final = notation marks DR collapse to the terminal value.

Chain 5 (three equivalent forms):
  1×5=5 → ×2=10 ~ DR=1
  1×5=5 → ×1=5 → ×2=10 ~ DR=1   (×1 inserted, same result)

Chain 2:
  1×2=2 → ×2=4 → ×1=4 → ×2=8 → ×1=8 → ×2=16 → DR=7
  Effective multipliers: [2, 2, 2]  (×1 steps are identities)

Chain 3:
  1×3=3 → ×1=3 → ×1=3 → ×2=6 → ×3=18 → ×1=18 ~ DR=9
  Effective multipliers: [2, 3]

Chain 4:
  1×4=4 → ×1=4 → ×2=8 → ×3=24 → ×4=96 → DR=6
  Effective multipliers: [2, 3, 4]

Terminal DRs: {2→7, 3→9, 4→6, 5→1}
Sum of terminal DRs: 7+9+6+1 = 23.
"""


def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


def dr_mult_row(n: int) -> list:
    """DR multiplication table row n: [dr(n*j) for j in 1..9]."""
    return [dr(n * j) for j in range(1, 10)]


def run_chain(seed: int, multipliers: list) -> list:
    """Apply multiplier sequence to seed; return all intermediate products."""
    products = [seed]
    cur = seed
    for m in multipliers:
        cur *= m
        products.append(cur)
    return products


def verify():
    print("Multiplication DR Chains — Seeds 2, 3, 4, 5\n")

    # ── Chain 5 ───────────────────────────────────────────────────────────────
    print("Chain 5 (seed 5)")
    # v1: minimal form
    assert 1 * 5 == 5
    assert 5 * 2 == 10
    assert dr(10) == 1
    # v2: with ×1 step inserted
    assert 5 * 1 == 5    # identity step
    assert 5 * 2 == 10
    assert dr(10) == 1
    chain5 = run_chain(5, [2])
    assert chain5 == [5, 10]
    assert dr(chain5[-1]) == 1
    print(f"  5 → ×2 → {chain5[1]}  DR={dr(chain5[-1])}  ✓")
    print(f"  Effective multipliers: [2]")
    print(f"  Identity steps (×1) do not alter the product  ✓")

    # ── Chain 2 ───────────────────────────────────────────────────────────────
    print("\nChain 2 (seed 2)")
    # Full step-by-step with identities interleaved
    assert 1 * 2 == 2
    assert 2 * 2 == 4
    assert 4 * 1 == 4    # identity
    assert 4 * 2 == 8
    assert 8 * 1 == 8    # identity
    assert 8 * 2 == 16
    assert dr(16) == 7
    # Effective chain (no ×1 steps)
    chain2 = run_chain(2, [2, 2, 2])
    assert chain2 == [2, 4, 8, 16]
    assert dr(chain2[-1]) == 7
    print(f"  2 → ×2 → 4 → ×2 → 8 → ×2 → {chain2[-1]}  DR={dr(chain2[-1])}  ✓")
    print(f"  Effective multipliers: [2,2,2]  product=8=2³  ✓")
    print(f"  Full sequence with identities: [2,4,4,8,8,16]  ✓")

    # ── Chain 3 ───────────────────────────────────────────────────────────────
    print("\nChain 3 (seed 3)")
    assert 1 * 3 == 3
    assert 3 * 1 == 3    # identity
    assert 3 * 1 == 3    # identity
    assert 3 * 2 == 6
    assert 6 * 3 == 18
    assert 18 * 1 == 18  # identity
    assert dr(18) == 9
    chain3 = run_chain(3, [2, 3])
    assert chain3 == [3, 6, 18]
    assert dr(chain3[-1]) == 9
    print(f"  3 → ×2 → 6 → ×3 → {chain3[-1]}  DR={dr(chain3[-1])}  ✓")
    print(f"  Effective multipliers: [2,3]  product=6=3!/1  ✓")
    print(f"  Full sequence with identities: [3,3,3,6,18,18]  ✓")

    # ── Chain 4 ───────────────────────────────────────────────────────────────
    print("\nChain 4 (seed 4)")
    assert 1 * 4 == 4
    assert 4 * 1 == 4    # identity
    assert 4 * 2 == 8
    assert 8 * 3 == 24
    assert 24 * 4 == 96
    assert dr(96) == 6
    chain4 = run_chain(4, [2, 3, 4])
    assert chain4 == [4, 8, 24, 96]
    assert dr(chain4[-1]) == 6
    print(f"  4 → ×2 → 8 → ×3 → 24 → ×4 → {chain4[-1]}  DR={dr(chain4[-1])}  ✓")
    print(f"  Effective multipliers: [2,3,4]  product=24=4!/1  ✓")
    print(f"  Full sequence with identity: [4,4,8,24,96]  ✓")

    # ── Effective multiplier pattern ──────────────────────────────────────────
    print("\nEffective multiplier sequences (ignoring ×1 identities):")
    eff_muls = {2: [2, 2, 2], 3: [2, 3], 4: [2, 3, 4], 5: [2]}
    eff_products = {n: 1 for n in [2, 3, 4, 5]}
    for n, muls in eff_muls.items():
        p = 1
        for m in muls: p *= m
        eff_products[n] = p
    print(f"  Seed 2: [2,2,2]  product={eff_products[2]}=2³")
    print(f"  Seed 3: [2,3]    product={eff_products[3]}=3!/1")
    print(f"  Seed 4: [2,3,4]  product={eff_products[4]}=4!/1")
    print(f"  Seed 5: [2]      product={eff_products[5]}")

    # For seeds 3 and 4: product = n!/1 = n!  (ascending from 2 to n)
    import math
    assert eff_products[3] == math.factorial(3) // 1    # 6
    assert eff_products[4] == math.factorial(4) // 1    # 24
    print(f"  Ascending [2..n] pattern confirmed for seeds 3,4  ✓")

    # ── Terminal DRs ──────────────────────────────────────────────────────────
    print("\nTerminal DRs:")
    terminal_dr = {2: dr(16), 3: dr(18), 4: dr(96), 5: dr(10)}
    chain_product = {2: 16, 3: 18, 4: 96, 5: 10}
    assert terminal_dr == {2: 7, 3: 9, 4: 6, 5: 1}
    for n in [2, 3, 4, 5]:
        print(f"  Seed {n}: chain product={chain_product[n]}  DR={terminal_dr[n]}")

    # Sum of terminal DRs = 23
    dr_sum = sum(terminal_dr.values())
    assert dr_sum == 23
    print(f"\n  Sum of terminal DRs: {'+'.join(str(terminal_dr[n]) for n in [2,3,4,5])} = {dr_sum}  (prime 23)  ✓")

    # ── DR multiplication matrix connection ───────────────────────────────────
    print("\nDR multiplication matrix connection: first j in row n where DR(n×j) = terminal DR:")
    for n in [2, 3, 4, 5]:
        row = dr_mult_row(n)
        target = terminal_dr[n]
        first_j = next(j + 1 for j, v in enumerate(row) if v == target)
        print(f"  Row {n}: {row}  →  DR={target} first at j={first_j}  (n×{first_j}={n*first_j})")
        assert dr(n * first_j) == target
    # Verify chain products match n × (effective_product) = n × first_j × ... combinations
    # For seed 5: n=5, first_j=2, chain product=10=5×2  ✓
    assert dr(5 * 2) == 1 and 5 * 2 == 10
    # For seed 3: n=3, first j with DR=9 is j=3 (3×3=9). Chain uses j=6 (3×6=18).
    # Both hit DR=9; chain uses second occurrence (j=6 > n=3).
    assert dr(3 * 3) == 9 and dr(3 * 6) == 9
    first_j_beyond_n = {n: next(j + 1 for j, v in enumerate(dr_mult_row(n)) if v == terminal_dr[n] and j + 1 > n)
                         for n in [3, 4]}
    assert first_j_beyond_n[3] == 6   # 3×6=18, DR=9
    assert first_j_beyond_n[4] == 6   # 4×6=24, DR=6
    print(f"\n  Seeds 3,4: terminal DR first appears at j>n (first j>n with target DR):")
    for n in [3, 4]:
        j = first_j_beyond_n[n]
        print(f"    Seed {n}: j={j}  n×j={n*j}  DR={dr(n*j)}  ✓")

    # ── Complement and structure ───────────────────────────────────────────────
    print("\nComplement structure:")
    # Seed 2: 2+7=9 (DR complement pair)
    assert 2 + terminal_dr[2] == 9
    print(f"  Seed 2 + terminal DR: 2+{terminal_dr[2]} = {2+terminal_dr[2]}  (complement to 9)  ✓")
    # Seed 3: terminal DR=9 (identity element of DR addition mod 9)
    assert terminal_dr[3] == 9
    print(f"  Seed 3: terminal DR={terminal_dr[3]}  (DR identity)  ✓")
    # Seed 4: 4+6=10→DR=1; also 4×6=24, DR(24)=6 (self-referential)
    assert dr(4 + terminal_dr[4]) == 1
    assert dr(4 * terminal_dr[4]) == terminal_dr[4]
    print(f"  Seed 4: DR(4+6)=DR(10)={dr(10)}; DR(4×6)=DR(24)={dr(24)}=6 (self-ref)  ✓")
    # Seed 5: terminal DR=1 (multiplicative identity of DR); 5×2=10, DR=1
    assert terminal_dr[5] == 1
    print(f"  Seed 5: terminal DR={terminal_dr[5]}  (DR multiplicative identity)  ✓")

    # ── AP {5,14,23,32} connection ────────────────────────────────────────────
    print("\nAP {5,14,23,32} connection:")
    AP = [5, 14, 23, 32]
    # Terminal DR sum = 23, the third AP member
    assert dr_sum == 23 == AP[2]
    print(f"  Sum of terminal DRs {list(terminal_dr.values())} = {dr_sum} = AP member 3  ✓")
    # Seed values {2,3,4,5}: 2+3=5 (first AP member); 2×3=6, 4+5=9
    assert 2 + 3 == AP[0]
    print(f"  Seed sum 2+3={2+3} = AP[0]=5  ✓")
    # Chain products: 16+18+96+10 = 140; DR(140)=5 = first AP member
    total_cp = sum(chain_product.values())
    assert total_cp == 140
    assert dr(total_cp) == 5
    print(f"  Sum of chain products: {chain_product[2]}+{chain_product[3]}+{chain_product[4]}+{chain_product[5]} = {total_cp},  DR={dr(total_cp)} = AP[0]=5  ✓")

    print()
    print("All assertions passed.")


if __name__ == "__main__":
    verify()
