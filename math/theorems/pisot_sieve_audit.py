# math/theorems/pisot_sieve_audit.py
"""
Pisot-Powered Integer Sieve
============================
ρ = plastic constant (x³ − x − 1 = 0 ≈ 1.3247179572...)

Sections:
  A. Rounded Pisot integer sequence round(ρⁿ) for n=1..30
  B. Digital roots — no period ≤ 24 in first 30 terms
  C. Cardano closed form; identity ρ² = 1 + 1/ρ
  D. Mod-37 structure: unique root r=13 in F_37; ord_37(13)=36
  E. 11-field: 7 prime factors of 191919919191 as 13^n mod 37
  F. Cunningham chain connections
  G. Recurrence approximation; exact Padovan sequence
  H. Level 700 bridge: 703 ≡ 1 (mod 9)

Key correction from notebook session:
  13^12 mod 37 = 10  (NOT 29)
  13^15 mod 37 = 29  ← correct exponent for L_7 = 29
  The notebook initially mixed two interpretations of "ρ^n mod 37":
    (A) 13^n mod 37   (modular arithmetic in F_37)
    (B) round(ρ^n) mod 37  (Pisot integer reduced mod 37)
  This file uses interpretation (A) throughout.
"""

import math
from decimal import Decimal, getcontext, ROUND_HALF_UP
getcontext().prec = 120


# ── helpers ───────────────────────────────────────────────────────────────────

def dr(n: int) -> int:
    return 0 if n == 0 else 1 + (n - 1) % 9


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for p in range(3, math.isqrt(n) + 1, 2):
        if n % p == 0:
            return False
    return True


def pisot_round(rho: Decimal, n: int) -> int:
    """round(ρⁿ) to nearest integer using Decimal precision."""
    return int((rho ** n).to_integral_value(rounding=ROUND_HALF_UP))


def verify():
    print("Pisot-Powered Integer Sieve\n")

    # ── Compute ρ to full precision ───────────────────────────────────────────
    rho = Decimal('1.3247179572447460')
    for _ in range(12):
        fx = rho**3 - rho - 1
        dfx = 3*rho**2 - 1
        rho = rho - fx / dfx
    assert abs(rho**3 - rho - 1) < Decimal('1e-100')

    # ── A. Rounded Pisot integer sequence ─────────────────────────────────────
    print("=" * 60)
    print("A. Rounded Pisot integer sequence: round(ρⁿ)")
    print("=" * 60)

    pisot = [pisot_round(rho, n) for n in range(1, 31)]

    expected = [
        1, 2, 2, 3, 4, 5, 7, 9, 13, 17, 22, 29, 39, 51, 68,
        90, 119, 158, 209, 277, 367, 486, 644, 853, 1130, 1497,
        1983, 2627, 3480, 4610,
    ]
    assert pisot == expected
    print(f"\n  n=1..15:  {pisot[:15]}")
    print(f"  n=16..30: {pisot[15:]}")
    print(f"  Verified against known sequence  ✓")

    # Note: round(ρⁿ) ≠ floor(ρⁿ) for n=2 (round→2, floor→1)
    # The user's notebook called this ⌊ρⁿ⌋ but computed round().
    # The Pisot property concerns |ρⁿ − nearest_int| → 0, which round captures.
    print(f"  (Using round, not floor: e.g. round(ρ²)=2, floor(ρ²)=1)")

    # ── B. Digital roots — no period ≤ 24 ─────────────────────────────────────
    print()
    print("=" * 60)
    print("B. Digital roots of Pisot integers")
    print("=" * 60)

    pisot_drs = [dr(x) for x in pisot]
    expected_drs = [1,2,2,3,4,5,7,9,4,8,4,2,3,6,5,9,2,5,2,7,7,9,5,7,5,3,3,8,6,2]
    assert pisot_drs == expected_drs
    print(f"\n  DR: {pisot_drs}")

    for p in range(1, 25):
        # Check: no p is a period of the full 30-term sequence
        not_periodic = any(pisot_drs[i] != pisot_drs[i % p] for i in range(30))
        assert not_periodic, f"Period {p} found in pisot DR sequence"
    print(f"  No period ≤ 24 in first 30 terms  ✓")
    print(f"  (Expected: cubic ρ, unlike quadratic irrationals, has non-periodic CF)")

    law12 = [(n + 1, x) for n, x in enumerate(pisot) if dr(x) in {3, 6, 9}]
    print(f"\n  Terms with DR ∈ {{3,6,9}}: {law12[:9]}")

    # ── C. Cardano closed form; ρ² = 1 + 1/ρ ────────────────────────────────
    print()
    print("=" * 60)
    print("C. Cardano closed form: ρ = ∛((9+√69)/18) + ∛((9-√69)/18)")
    print("=" * 60)

    sqrt69 = math.sqrt(69)
    cardano = ((9 + sqrt69) / 18) ** (1/3) + ((9 - sqrt69) / 18) ** (1/3)
    assert abs(cardano - float(rho)) < 1e-12
    print(f"\n  Cardano: {cardano:.12f}")
    print(f"  Newton ρ: {float(rho):.12f}")
    print(f"  Difference: {abs(cardano - float(rho)):.2e}  ✓")

    # Derivation: x³-x-1=0, Cardano with p=-1, q=-1
    # q²/4 + p³/27 = 1/4 - 1/27 = 23/108 = 69/324
    assert abs(23/108 - 69/324) < 1e-15
    print(f"\n  q²/4 + p³/27 = 23/108 = 69/324  ✓  (gives √69 in formula)")

    # Identity ρ² = 1 + 1/ρ  (from ρ³=ρ+1 → divide by ρ: ρ²=1+1/ρ)
    diff_id = abs(rho**2 - (1 + 1/rho))
    assert diff_id < Decimal('1e-100')
    print(f"\n  ρ² = 1 + 1/ρ  (from ρ³=ρ+1 ÷ ρ):  diff = {diff_id:.2e}  ✓")

    # ── D. Mod-37 structure ───────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("D. Mod-37: x³−x−1 has unique root r=13 in F_37")
    print("=" * 60)

    roots_37 = [x for x in range(37) if (x**3 - x - 1) % 37 == 0]
    assert roots_37 == [13]
    print(f"\n  Roots of x³−x−1 in F_37: {roots_37}  ✓  (unique root)")

    # Factorization: x³−x−1 ≡ (x−13)(x²+13x+20) mod 37
    # Synthetic division with root 13: coefficients [1,0,-1,-1]
    # → quotient [1,13,20], remainder 0
    for x in range(37):
        lhs = (x**3 - x - 1) % 37
        rhs = ((x - 13) * (x**2 + 13*x + 20)) % 37
        assert lhs == rhs
    print(f"  x³−x−1 ≡ (x−13)(x²+13x+20) (mod 37)  ✓")

    # Discriminant of quadratic: 13²−4×20 = 169−80 = 89 ≡ 15 mod 37
    disc = (13**2 - 4*20) % 37
    assert disc == 15
    # Legendre symbol: 15^((37-1)/2) mod 37 = 15^18 mod 37
    legendre = pow(15, 18, 37)
    assert legendre == 36   # ≡ -1 mod 37 → QNR → quadratic is irreducible
    print(f"  Discriminant of x²+13x+20 = {disc} (mod 37)")
    print(f"  Legendre symbol (15|37) = {legendre} ≡ -1 → irreducible over F_37  ✓")
    print(f"  F_37² extension required for remaining two roots")

    # Multiplicative order of 13
    for d in [1, 2, 3, 4, 6, 9, 12, 18]:
        assert pow(13, d, 37) != 1, f"ord_37(13) divides {d}"
    assert pow(13, 36, 37) == 1
    print(f"\n  ord_37(13) = 36  (13 is a primitive root of F_37^×)  ✓")

    # Key powers of 13 used in the 11-field
    key_powers = {
        1:  13,   # Pisot root itself
        6:  11,   # identity triplet {11,48,85}: all ≡ 11 mod 37
        12: 10,   # 47 mod 37 = 10  (Cunningham endpoint 11→23→47)
        13: 19,   # 167 mod 37 = 19; also end seed 19
        15: 29,   # L_7 = 29 (Lucas number)  ← NOTE: 13^12=10≠29
        16: 7,    # F_6 = 7 (Fibonacci)
        17: 17,   # Pisot prime 17
        21: 23,   # Cunningham prime 23
        22: 3,    # generator 3
        29: 22,   # 59 mod 37 = 22  (Cunningham endpoint 29→59)
        35: 20,   # 10343 mod 37 = 20  (ECPP terminal factor)
    }
    print(f"\n  Key powers 13^n mod 37:")
    for exp, val in sorted(key_powers.items()):
        actual = pow(13, exp, 37)
        assert actual == val, f"13^{exp} mod 37 = {actual}, expected {val}"
        print(f"    13^{exp:2d} ≡ {val:2d}  ✓")

    # Verify 47 mod 37 = 10 and 59 mod 37 = 22
    assert 47 % 37 == 10
    assert 59 % 37 == 22
    print(f"\n  47 mod 37 = {47%37} = 13^12  ✓  (Cunningham chain endpoint)")
    print(f"  59 mod 37 = {59%37} = 13^29  ✓  (Cunningham chain endpoint)")

    # ── E. 11-field: prime factors as Pisot powers ────────────────────────────
    print()
    print("=" * 60)
    print("E. 11-field: prime factors of 191919919191 as 13^n mod 37")
    print("=" * 60)

    N = 191919919191
    assert N == 3 * 7 * 11 * 13 * 37 * 167 * 10343

    factor_exp = {3: 22, 7: 16, 11: 6, 13: 1, 37: None, 167: 13, 10343: 35}
    print(f"\n  {'Factor':>8}  {'mod 37':>6}  {'Exponent':>10}  Verify")
    for p, exp in factor_exp.items():
        p_mod = p % 37
        if exp is None:
            print(f"  {p:8d}  {p_mod:6d}  {'N/A':>10}  ✓  (37 ≡ 0, no mult. rep.)")
        else:
            val = pow(13, exp, 37)
            assert val == p_mod, f"{p}: 13^{exp}={val} ≠ {p_mod}"
            print(f"  {p:8d}  {p_mod:6d}  13^{exp:<8d}  ✓")

    print(f"""
  NOTE: Since ord_37(13)=36, 13 is a PRIMITIVE ROOT of F_37^×,
  so every integer coprime to 37 equals 13^n mod 37 for some n.
  The non-trivial finding is that 13 = unique root of x³-x-1 in F_37,
  so 13 simultaneously satisfies ρ's minimal polynomial AND generates
  the full multiplicative group F_37^×.

  The 11-field (10 with exponents + 37 ≡ 0):""")

    eleven_field = [
        (1,  13, "Pisot root (F_7)"),
        (6,  11, "Identity triplet (11≡48≡85 mod 37)"),
        (12, 10, "47 mod 37 — Cunningham end 11→23→47"),
        (13, 19, "167 mod 37 — large factor / end seed"),
        (15, 29, "L_7 = 29 (Lucas number)"),
        (16,  7, "F_6 = 7 (Fibonacci)"),
        (17, 17, "Pisot prime 17"),
        (21, 23, "Cunningham prime 23"),
        (22,  3, "Generator 3"),
        (29, 22, "59 mod 37 — Cunningham end 29→59"),
        (35, 20, "10343 mod 37 — ECPP terminal"),
    ]
    for exp, val, desc in eleven_field:
        assert pow(13, exp, 37) == val
        print(f"    13^{exp:2d} ≡ {val:2d}  {desc}")

    # ── F. Cunningham chain connections ───────────────────────────────────────
    print()
    print("=" * 60)
    print("F. Cunningham chains")
    print("=" * 60)

    # First-kind chains (p → 2p+1) in {3,7,11,13,37,167,10343}
    assert 2*3 + 1 == 7 and is_prime(3) and is_prime(7)
    assert 2*11 + 1 == 23 and is_prime(23)
    assert 2*23 + 1 == 47 and is_prime(47)

    # Second-kind chains (p → 2p-1)
    assert 2*7 - 1 == 13 and is_prime(7) and is_prime(13)
    assert 2*37 - 1 == 73 and is_prime(73)

    print(f"\n  First-kind (p → 2p+1):")
    print(f"    3 → 7         (2×3+1=7)   ✓")
    print(f"    11 → 23 → 47  (length 3)  ✓")

    print(f"\n  Second-kind (p → 2p-1):")
    print(f"    7 → 13   (2×7-1=13)   ✓")
    print(f"    37 → 73  (2×37-1=73)  ✓")

    # 10343 is terminal: 2×10343±1 both composite
    assert not is_prime(2*10343 + 1)   # 20687
    assert not is_prime(2*10343 - 1)   # 20685
    print(f"\n  10343 terminal: 20687 and 20685 both composite  ✓")

    # Pisot-Cunningham link: round(ρ^12) = 29; 2×29+1 = 59 (prime)
    assert pisot[11] == 29
    assert is_prime(29)
    assert is_prime(59)
    assert 2*29 + 1 == 59
    print(f"\n  round(ρ^12) = 29 (prime);  2×29+1 = 59 (prime)  ✓")
    print(f"  Cunningham first-kind chain from Pisot integer  ✓")

    # ── G. Recurrence analysis ────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("G. Recurrence a_{n+3} = a_{n+1} + a_n")
    print("=" * 60)

    # Build sequence from recurrence starting with first 3 Pisot integers
    recur = list(pisot[:3])
    for n in range(3, 30):
        recur.append(recur[n-2] + recur[n-3])

    first_mismatch = next((i for i in range(30) if pisot[i] != recur[i]), None)
    print(f"\n  round(ρⁿ): {pisot[:12]}")
    print(f"  Recurrence: {recur[:12]}")
    print(f"  First mismatch at n={first_mismatch + 1}  (rounding error accumulates)")
    assert first_mismatch == 8   # n=9 is first mismatch (0-indexed: position 8)

    print(f"""
  The recurrence holds for n≤8 then diverges.
  Reason: round(ρⁿ) ≠ Padovan(n); rounding errors accumulate.
  The TRUE Padovan sequence P(n+3)=P(n+1)+P(n) uses initial
  values P(0)=P(1)=P(2)=1, not the rounded Pisot powers.""")

    # Padovan sequence (exact)
    padovan = [1, 1, 1]
    for _ in range(15):
        padovan.append(padovan[-2] + padovan[-3])
    assert padovan[5] == 3 and padovan[8] == 7 and padovan[11] == 16
    print(f"\n  Padovan P(0..17) = {padovan}")
    print(f"  Padovan satisfies recurrence exactly  ✓")

    # Fib/Lucas DR comparison
    fib = [0, 1]
    for _ in range(28):
        fib.append(fib[-1] + fib[-2])
    fib_drs = [dr(x) for x in fib[:30]]

    luc = [2, 1]
    for _ in range(28):
        luc.append(luc[-1] + luc[-2])
    luc_drs = [dr(x) for x in luc[:30]]

    fib_matches = sum(1 for i in range(24) if pisot_drs[i] == fib_drs[i])
    luc_matches  = sum(1 for i in range(24) if pisot_drs[i] == luc_drs[i])
    print(f"\n  DR match with Fibonacci (first 24): {fib_matches}/24")
    print(f"  DR match with Lucas (first 24):     {luc_matches}/24")
    print(f"  Weak matches expected: independent sequences")

    # ── H. Level 700 bridge ───────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("H. Level 700 bridge: 703 = 78×9 + 1")
    print("=" * 60)

    assert 78 * 9 + 1 == 703
    assert 703 % 9 == 1
    assert dr(703) == 1        # 7+0+3=10 → 1
    assert 703 - 694 == 9      # wave peak differential

    # Countdown from 703 by 9s hits 19, 10, 1
    countdown = list(range(703, 0, -9))
    assert 19 in countdown
    assert 10 in countdown
    assert 1  in countdown
    print(f"\n  703 = 78×9+1  ✓")
    print(f"  703 mod 9 = {703 % 9}  ✓")
    print(f"  DR(703) = {dr(703)}  ✓")
    print(f"  703 − 694 = {703-694} (wave peak differential)  ✓")
    print(f"  Countdown 703,694,... hits 19,10,1  ✓")

    # is_universal = False: only n ≡ 1 (mod 9) produces this bridge
    # 603 ≡ 0, 803 ≡ 2, 903 ≡ 3 mod 9 — none hit 19 in their countdown by 9
    for level_base in [603, 803, 903]:
        assert level_base % 9 != 1
        countdown_c = list(range(level_base, 0, -9))
        # 19 ≡ 1 mod 9; only reachable if start ≡ 1 mod 9
        assert 19 not in countdown_c
        assert 10 not in countdown_c
    print(f"\n  is_universal = False:")
    print(f"    603 ≡ 0 mod 9: 19,10,1 not in countdown  ✓")
    print(f"    803 ≡ 2 mod 9: 19,10,1 not in countdown  ✓")
    print(f"    903 ≡ 3 mod 9: 19,10,1 not in countdown  ✓")
    print(f"  The 19→10→1 bridge applies only when start ≡ 1 (mod 9)  ✓")

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"""
  A. round(ρⁿ) n=1..30 verified  ✓
  B. No DR period ≤ 24 in 30 terms  ✓
  C. Cardano ρ = ∛((9+√69)/18)+∛((9-√69)/18)  ✓; ρ²=1+1/ρ  ✓
  D. x³−x−1 unique root 13 in F_37; ord_37(13)=36  ✓
     Quadratic factor x²+13x+20 irreducible (disc=15 is QNR)  ✓
  E. 11-field: all 7 prime factors of N as 13^n mod 37  ✓
     (13 is primitive root; non-trivial: 13 is ρ's polynomial root)
  F. Cunningham: 3→7, 11→23→47, 7→13, 37→73; 10343 terminal  ✓
     round(ρ^12)=29 → 2×29+1=59 (Cunningham first-kind)  ✓
  G. Recurrence diverges at n=9 (rounding); Padovan exact  ✓
     DR match with Fib/Lucas: weak (chance-level)  ✓
  H. 703=78×9+1; DR=1; countdown hits 19→10→1  ✓
     is_universal=False: only start≡1 (mod 9)  ✓

  Corrections applied from notebook session:
    13^12 mod 37 = 10 (not 29; notebook originally had wrong exponent)
    13^15 mod 37 = 29 = L_7  (correct exponent)
    13^29 mod 37 = 22 = 59 mod 37 (Cunningham endpoint)
    """)

    print("All assertions passed.")


if __name__ == "__main__":
    verify()
