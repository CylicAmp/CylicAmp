"""
ABCABC ≡ 2·ABC (mod 37): Full orbit analysis of Z37* via primitive root 2
=========================================================================

Core theorem:
  ABCABC = ABC × 1001,  and  1001 ≡ 2 (mod 37)
  → ABCABC ≡ 2 · ABC (mod 37)

This lifts to a group-theoretic statement: the map ABC ↦ ABCABC
acts as multiplication by 2 on Z/37Z, which—since ord_37(2) = 36 = φ(37)—
generates the full multiplicative group (Z/37Z)*.

Verified facts:
  - 1001 ≡ 2 (mod 37)
  - ord_37(2) = 36  (2 is a primitive root mod 37)
  - 2^18 ≡ -1 (mod 37)
  - 2^{-1} ≡ 19 (mod 37)  (since 2·19 = 38 ≡ 1)
  - Starting residue r_0 = 24 = 2^29 (mod 37)
  - r_n = 2^{29+n} (mod 37): closed-form orbit definition
  - The orbit {r_n} traverses all 36 elements of (Z/37Z)*
"""


# =============================================================================
# Foundational constants
# =============================================================================

MOD     = 37
FACTOR  = 1001          # 1001 = 1000 + 1 = 10^3 + 1
FACTOR_MOD = FACTOR % MOD   # 2: the key congruence
INV2    = 19            # 2 * 19 ≡ 1 (mod 37)
R0      = 24            # starting residue = 2^29 mod 37


# =============================================================================
# Verification functions
# =============================================================================

def verify_primitive_root():
    """Confirm ord_37(2) = 36 by checking no smaller exponent gives 1."""
    order = next(k for k in range(1, MOD) if pow(2, k, MOD) == 1)
    return {
        "order":      order,
        "is_prim_root": order == MOD - 1,
        "2^18_mod37": pow(2, 18, MOD),   # must be -1 = 36
        "2^36_mod37": pow(2, 36, MOD),   # must be 1
    }


def verify_1001_congruence():
    """1001 ≡ 2 (mod 37): the engine of the ABCABC theorem."""
    return {
        "1001 mod 37":  FACTOR % MOD,
        "1001 = 37×27": 37 * 27 + 2,
    }


def compute_orbit():
    """Full orbit r_n = 2^{29+n} mod 37 for n = 0..35."""
    return [pow(2, 29 + n, MOD) for n in range(36)]


def abcabc_theorem(abc):
    """
    Verify ABCABC ≡ 2·ABC (mod 37) for a given 3-digit integer abc.
    Returns (abcabc, abcabc mod 37, 2*abc mod 37, match).
    """
    abcabc = abc * FACTOR
    lhs = abcabc % MOD
    rhs = (2 * abc) % MOD
    return abcabc, lhs, rhs, lhs == rhs


def abc_from_residue(r):
    """Recover ABC mod 37 from ABCABC residue r using ABC = r · 19 mod 37."""
    return (r * INV2) % MOD


# =============================================================================
# Main summary
# =============================================================================

def summarise():
    print("=" * 60)
    print("ABCABC ≡ 2·ABC (mod 37): ORBIT ANALYSIS")
    print("=" * 60)

    v1001 = verify_1001_congruence()
    print(f"\n1001 mod 37 = {v1001['1001 mod 37']}  (1001 = 37×27 + 2 → {v1001['1001 = 37×27']})")

    vpr = verify_primitive_root()
    print(f"\nPrimitive root 2 mod 37:")
    print(f"  ord_37(2)  = {vpr['order']}  (== φ(37)={MOD-1}: {vpr['is_prim_root']})")
    print(f"  2^18 mod 37 = {vpr['2^18_mod37']}  (≡ -1: {vpr['2^18_mod37'] == 36})")
    print(f"  2^36 mod 37 = {vpr['2^36_mod37']}  (≡  1: {vpr['2^36_mod37'] == 1})")
    print(f"  2^-1 mod 37 = {INV2}  (2·19={2*19} ≡ 1: {(2*19)%37 == 1})")

    print(f"\nStarting residue r_0 = 2^29 mod 37 = {pow(2, 29, MOD)}  (== {R0}: {pow(2,29,MOD)==R0})")

    orbit = compute_orbit()
    print(f"\nOrbit r_n = 2^{{29+n}} mod 37 (n=0..35):")
    print(f"  {orbit}")
    print(f"  Unique elements: {len(set(orbit))}  (full orbit: {len(set(orbit))==36})")

    abc_vals = [abc_from_residue(r) for r in orbit]
    print(f"\nABC values (= r·19 mod 37):")
    print(f"  {abc_vals}")
    print(f"  All distinct: {len(set(abc_vals)) == 36}")

    print("\nABCABC theorem — concrete checks:")
    for abc in [123, 456, 100, 999, 37]:
        abcabc, lhs, rhs, ok = abcabc_theorem(abc)
        print(f"  {abc}×1001 = {abcabc},  mod37={lhs},  2·{abc} mod37={rhs}  {'✓' if ok else '✗'}")

    print(f"\nClosed-form discrete log:")
    dlog = next(n for n in range(36) if pow(2, n, MOD) == R0)
    print(f"  r_0 = {R0} = 2^{dlog} mod 37")
    print(f"  r_n = 2^{{{dlog}+n}} mod 37")


def run_assertions():
    assert FACTOR_MOD == 2, f"1001 mod 37 = {FACTOR_MOD}, expected 2"
    assert 37 * 27 + 2 == 1001

    vpr = verify_primitive_root()
    assert vpr["order"] == 36, f"ord_37(2) = {vpr['order']}, expected 36"
    assert vpr["is_prim_root"]
    assert vpr["2^18_mod37"] == 36, "2^18 must be ≡ -1 ≡ 36 (mod 37)"
    assert vpr["2^36_mod37"] == 1,  "2^36 must be ≡ 1 (mod 37)"

    assert (2 * INV2) % MOD == 1, f"2·{INV2} mod 37 must be 1"
    assert pow(2, 29, MOD) == R0,  f"2^29 mod 37 = {pow(2,29,MOD)}, expected {R0}"

    orbit = compute_orbit()
    assert len(set(orbit)) == 36, f"orbit size = {len(set(orbit))}, expected 36"
    assert set(orbit) == set(range(1, MOD)), "orbit must cover all of (Z/37Z)*"

    for abc in [123, 456, 100, 999, 37]:
        _, lhs, rhs, ok = abcabc_theorem(abc)
        assert ok, f"ABCABC theorem failed for abc={abc}: {lhs} ≠ {rhs}"

    assert verify_1001_congruence()["1001 mod 37"] == 2


if __name__ == "__main__":
    run_assertions()
    summarise()
