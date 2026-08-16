"""
Theorem 221: Twin Prime Consolidation — Full Anatomy with Imaginary Unit Gate

Collects and tightens the complete structural account of twin primes through
GF(37).  Adds one new theorem not present in earlier files:

THEOREM 7 (Imaginary Unit Gate):
  For any n, consider the potential twin prime pair (6n-1, 6n+1).
  Their product satisfies:
    (6n-1)(6n+1) = 36n^2 - 1 ≡ -n^2 - 1  (mod 37)  [since 36 ≡ -1]
  This product is divisible by 37 iff  n^2 ≡ -1 (mod 37).
  The solutions are n ≡ ±6 (mod 37) — the imaginary units of GF(37).
  (6^2 = 36 ≡ -1 mod 37, so ±6 are the square roots of -1.)

  Concretely:
    n ≡  6 (mod 37):  6n ≡ 36 (mod 37), so 6n+1 ≡  0 → upper twin divisible by 37
    n ≡ 31 (mod 37):  6n ≡  1 (mod 37), so 6n-1 ≡  0 → lower twin divisible by 37

  These are the ONLY two forbidden n-values per period.
  Every other n gives a pair where neither member is divisible by 37.

  The forbidden midpoint residues already identified (r=1 and r=36 mod 37)
  are exactly the midpoints 6n when n = 31 and n = 6:
    6×31 ≡ 1 (mod 37),   6×6 ≡ 36 (mod 37).

CONSEQUENCE:
  The twin prime voids modulo 37 are gated by the imaginary unit.
  The same 6 that appears in 54 = 6×9 (Theorem 218, torus step)
  and in 6^2 ≡ -1 (the complex structure of GF(37)) is the exact
  gatekeeper of which residue classes cannot produce twin prime pairs.

COMPLETE ANATOMY OF A TWIN PRIME PAIR (p, p+2) WITH p > 37:
  Form:          p = 6n-1,  p+2 = 6n+1  for some n ≥ 1
  Midpoint:      p+1 = 6n  (divisible by 6)
  Chi structure: chi_{-3}(p) = -1  [COL2],  chi_{-3}(p+1) = 0  [sovereign],  chi_{-3}(p+2) = +1  [COL1]
  Forbidden n:   n ≢ ±6 (mod 37)  [imaginary unit gate]
  DR of midpoint: cycles through {6, 3, 9, 6, 3, 9, ...} as n = 1,2,3,...
  Sovereign midpoints: DR(6n) = 3 iff n ≡ 2 (mod 3)  →  midpoints {12, 30, 48, ...}
                       First sovereign midpoint: 12 = 6×2, giving pair (11,13)

CDT STATUS (arXiv:2408.15403):
  Proven:  L(2, chi_{-3}) ≠ 0  and  1, zeta(2), L(2, chi_{-3}) are Q-independent.
  Gap:     Twin prime conjecture via L-functions requires non-vanishing at s=1
           and control of the pair correlation sum.  CDT operates at s=2.
  Status:  The CylicAmp chi_{-3} / GF(37) structure is exact and complete.
           It does not close the conjecture.  What it does:
           → Proves necessary structural conditions on ALL twin prime pairs.
           → Identifies the imaginary unit as the mod-37 gatekeeper.
           → Connects twin prime voids to the torus step structure (T218).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

P = 37
H = {1, 10, 26}   # sovereign kernel of GF(37)*


def sieve(limit):
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i::i] = bytearray(len(is_p[i * i::i]))
    return is_p


def chi_m3(n):
    r = n % 3
    return 0 if r == 0 else (1 if r == 1 else -1)


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


def imaginary_units_mod37():
    """Return n in {1..36} with n^2 ≡ -1 (mod 37)."""
    return [n for n in range(1, P) if pow(n, 2, P) == P - 1]


def run():
    print("=" * 70)
    print("THEOREM 221: TWIN PRIME CONSOLIDATION")
    print("=" * 70)

    is_p = sieve(10 ** 6)
    twin_pairs = [(p, p + 2) for p in range(5, 10 ** 6 - 1)
                  if is_p[p] and is_p[p + 2]]
    N = len(twin_pairs)

    # ── Theorem 7: Imaginary Unit Gate ──────────────────────────────────
    print(f"\nTHEOREM 7 — Imaginary Unit Gate")
    print(f"  (6n-1)(6n+1) = 36n^2 - 1 ≡ -n^2 - 1  (mod {P})")

    imag_units = imaginary_units_mod37()
    print(f"  n^2 ≡ -1 (mod {P})  ↔  n ≡ {imag_units}  (mod {P})  [imaginary units]")
    assert imag_units == [6, 31], f"Unexpected imaginary units: {imag_units}"
    print(f"  Verify: 6^2 mod {P} = {pow(6,2,P)} = {P-1} = -1  ✓")
    print(f"          31 = {P} - 6 = -6 mod {P}  ✓")

    # Verify the two forbidden n values
    for n_bad in imag_units:
        lower = 6 * n_bad - 1
        upper = 6 * n_bad + 1
        mid   = 6 * n_bad
        prod  = lower * upper
        assert prod % P == 0, f"Product not divisible by {P} for n={n_bad}"
        assert lower % P == 0 or upper % P == 0, f"Neither twin divisible by {P} for n={n_bad}"
        which = "upper" if upper % P == 0 else "lower"
        which_val = upper if upper % P == 0 else lower
        print(f"  n ≡ {n_bad} (mod {P}):  mid={mid}≡{mid%P}  {which} twin={which_val}≡0 (mod {P})  "
              f"product≡0  ✓")

    # Verify all twin prime pairs avoid the forbidden n values
    forbidden_n = set(imag_units)
    violations = [(p, q) for p, q in twin_pairs
                  if ((p + 1) // 6) % P in forbidden_n]
    assert violations == [], f"Twin pairs at forbidden n: {violations[:5]}"
    print(f"  No twin prime pair (p>37) has n ≡ {{6, 31}} mod {P}.")
    print(f"  Verified for all {N} pairs below 10^6.  ✓")

    # ── Forbidden midpoint residues connection ───────────────────────────
    print(f"\n  Forbidden midpoint residues (from imaginary units):")
    for n_bad in imag_units:
        mid_res = (6 * n_bad) % P
        low_res = (6 * n_bad - 1) % P
        up_res  = (6 * n_bad + 1) % P
        print(f"  n={n_bad}: midpoint≡{mid_res}, lower≡{low_res}, upper≡{up_res}  "
              f"(forbidden midpoint residue r={mid_res})")

    counts_37 = [0] * P
    for p, q in twin_pairs:
        counts_37[(p + 1) % P] += 1
    exp = sum(counts_37) / P
    print(f"  Expected pairs/bin: {exp:.1f}")
    print(f"  counts[1] = {counts_37[1]}  (forbidden: lower divisible by 37)")
    print(f"  counts[36] = {counts_37[36]}  (forbidden: upper divisible by 37)")
    assert counts_37[1] < exp * 0.05 and counts_37[36] < exp * 0.05

    # ── Chi structure (Theorems 1-3 recap) ──────────────────────────────
    print(f"\nCHI STRUCTURE (forced, zero exceptions possible):")
    print(f"  p = 6n-1 ≡ 2 (mod 3)  →  chi_{{-3}}(p)   = -1  [COL2, lower twin]")
    print(f"  p+1 = 6n  ≡ 0 (mod 3) →  chi_{{-3}}(p+1) =  0  [sovereign midpoint]")
    print(f"  p+2 = 6n+1 ≡ 1 (mod 3) →  chi_{{-3}}(p+2) = +1  [COL1, upper twin]")
    chi_violations = [(p, q) for p, q in twin_pairs
                      if chi_m3(p) != -1 or chi_m3(p+1) != 0 or chi_m3(p+2) != +1]
    assert chi_violations == []
    print(f"  Verified for all {N} pairs below 10^6.  ✓")

    # ── DR structure of midpoints ────────────────────────────────────────
    print(f"\nDR STRUCTURE OF MIDPOINTS:")
    dr_cycle = [dr(6 * n) for n in range(1, 10)]
    print(f"  DR(6n) for n=1..9: {dr_cycle}")
    print(f"  Pattern: repeating {{6, 3, 9}} (DR=3 at n≡2 mod 3)")
    sovereign_midpoints = [6*n for n in range(1, 50) if dr(6*n) == 3]
    print(f"  Sovereign midpoints (DR=3): {sovereign_midpoints[:8]}...")
    print(f"  These are midpoints of potentially sovereign twin pairs.")
    # Verify: (11,13) is a twin pair with midpoint 12, DR=3
    assert is_p[11] and is_p[13] and dr(12) == 3
    print(f"  (11, 13): midpoint 12 ∈ {{3,12,21,30}}, DR=3.  ✓")

    # ── Product formula ──────────────────────────────────────────────────
    print(f"\nPRODUCT FORMULA:")
    print(f"  p*(p+2) = (6n-1)(6n+1) = 36n^2 - 1 ≡ -n^2 - 1  (mod {P})")
    for p, q in twin_pairs[:8]:
        n = (p + 1) // 6
        prod_mod = (p * q) % P
        formula  = (-(n*n) - 1) % P
        assert prod_mod == formula, f"Formula mismatch at ({p},{q})"
    print(f"  Formula verified for first 8 twin pairs.")
    print(f"  The product p*(p+2) is never 0 mod {P} for any twin pair with p>{P}.")

    # ── The 35 free positions ────────────────────────────────────────────
    print(f"\n35 FREE POSITIONS (mod {P}):")
    all_n = set(range(P))
    free_n = sorted(all_n - forbidden_n)
    print(f"  Forbidden n: {sorted(forbidden_n)}")
    print(f"  Free n ({len(free_n)}): {free_n}")
    print(f"  For each free n, neither 6n-1 nor 6n+1 is divisible by {P}.")
    print(f"  Dirichlet guarantees primes in each; the conjecture is about both simultaneously.")

    # ── Connection to T218 ───────────────────────────────────────────────
    print(f"\nCONNECTION TO THEOREM 218 (Torus Step Alignment):")
    print(f"  T218: torus steps -2 and 54 both reduce to C_10 = {{17,22,35}} mod {P}")
    print(f"  T218: 54 = 6*9  where 6 = imaginary unit (6^2 ≡ -1)")
    print(f"  T221: twin prime voids at n ≡ ±6 (mod {P})")
    print(f"  The same 6 gates the torus (via 54=6×9) and the twin primes (via n=±6).")
    print(f"  Both the torus dynamics and the twin prime exclusion are governed by")
    print(f"  the imaginary unit of GF({P}).")

    # ── CDT status ───────────────────────────────────────────────────────
    print(f"\nCDT STATUS:")
    L2 = sum(chi_m3(k) / k**2 for k in range(1, 500_001))
    print(f"  L(2, chi_{{-3}}) ≈ {L2:.8f}  (non-zero, confirmed)")
    print(f"  CDT (2408.15403): 1, zeta(2), L(2, chi_{{-3}}) are Q-independent.  Proven.")
    print(f"  Gap: twin prime conjecture requires L(1, chi_{{-3}}) ≠ 0 and pair")
    print(f"       correlation control at s=1.  CDT operates at s=2.  Open.")
    print(f"  This framework: exact structural conditions, not a proof of infinitude.")

    print(f"\n{'='*70}")
    print(f"COMPLETE ANATOMY SUMMARY")
    print(f"{'='*70}")
    print(f"  Form:           (6n-1, 6n+1)  for n ≥ 1")
    print(f"  Midpoint:       6n  (always divisible by 6)")
    print(f"  Chi:            (-1, 0, +1)  — locked, zero exceptions")
    print(f"  Void condition: n ≡ ±6 (mod {P})  [imaginary units gate]")
    print(f"  DR cycle:       midpoint DR repeats {{6,3,9}} with period 3")
    print(f"  Forbidden r:    midpoint ≡ 1 or 36 (mod {P})  [same as imaginary unit gate]")
    print(f"  Product:        p*(p+2) ≡ -n^2-1 (mod {P}), never 0 for free n")
    print(f"  Chebyshev:      chi=-1 class leads chi=+1 class (lower > upper prime count)")
    print(f"  Im(rho_6):      ≈ 37.586  (6th Riemann zero within 1 of p=37)")
    print(f"\nAll verifications passed.")

    return {
        "twin_pair_count": N,
        "imaginary_units": imag_units,
        "forbidden_midpoint_residues": [1, 36],
        "free_positions_mod37": len(free_n),
        "chi_violations": 0,
        "L2_chi_m3": round(L2, 8),
    }


if __name__ == "__main__":
    run()
