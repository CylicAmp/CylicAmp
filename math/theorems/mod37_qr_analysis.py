"""
MOD-37 QUADRATIC RESIDUE ANALYSIS: <3> = QR_37
================================================================

The 18-cycle of powers of 3 mod 37 is exactly the quadratic residue
subgroup of (Z/37Z)*.

Key verified facts:
- ord_37(3) = 18  (3 is a QR mod 37, Legendre (3/37) = 1)
- <3> = QR_37   (unique index-2 subgroup of (Z/37Z)* of order 18)
- 3^9 ≡ -1 (mod 37), giving the involution 3^k + 3^{k+9} ≡ 0
- DR=5 values {5, 14, 23, 32} are entirely excluded from QR_37
- DR=3 and DR=7 are the only DR classes fully contained in QR_37
"""


def digital_root(n):
    if n == 0:
        return 9
    return (n - 1) % 9 + 1


# =============================================================================
# Core cycle
# =============================================================================

CYCLE = [pow(3, n, 37) for n in range(1, 19)]
QR37  = set(CYCLE)   # <3> = QR_37


def power_in_cycle(val):
    """Return k such that 3^k ≡ val (mod 37), or None."""
    for k, v in enumerate(CYCLE, 1):
        if v == val:
            return k
    return None


# =============================================================================
# Verification functions
# =============================================================================

def verify_qr_equality():
    """Confirm <3> equals the set of quadratic residues mod 37."""
    qr_direct = {(a * a) % 37 for a in range(1, 37)}
    return qr_direct == QR37


def verify_power_assignments():
    """
    Verify specific discrete log values.
    Returns dict mapping label -> (expected_val, computed_val, ok).
    """
    assignments = [
        ("4=3^7",   4,  7),
        ("9=3^2",   9,  2),
        ("25=3^17", 25, 17),
        ("30=3^13", 30, 13),
        ("3=3^1",   3,  1),
        ("12=3^8",  12, 8),
        ("21=3^5",  21, 5),
        ("26=3^6",  26, 6),
    ]
    results = {}
    for label, val, exp in assignments:
        computed = pow(3, exp, 37)
        results[label] = (val, computed, computed == val)
    return results


def verify_mirror_involution():
    """
    Check 3^k + 3^{k+9} ≡ 0 (mod 37) for all k in 1..9.
    Follows from 3^9 ≡ -1 (mod 37).
    """
    pairs = []
    for k in range(1, 10):
        a = pow(3, k, 37)
        b = pow(3, k + 9, 37)
        pairs.append((k, a, b, (a + b) % 37))
    return pairs


def dr_membership_in_qr():
    """
    For each DR class 1-9, classify elements of {1..36} as QR or QNR.
    """
    result = {}
    for dr in range(1, 10):
        vals = [n for n in range(1, 37) if digital_root(n) == dr]
        result[dr] = {
            "all":  vals,
            "qr":   [v for v in vals if v in QR37],
            "qnr":  [v for v in vals if v not in QR37],
            "fully_qr":  all(v in QR37 for v in vals),
            "fully_qnr": all(v not in QR37 for v in vals),
        }
    return result


# =============================================================================
# Key structural results
# =============================================================================

def summarise():
    print("=" * 60)
    print("<3> = QR_37: MOD-37 QUADRATIC RESIDUE ANALYSIS")
    print("=" * 60)

    print(f"\nCycle of 3^n mod 37 (n=1..18):")
    print(f"  {CYCLE}")
    print(f"  Length: {len(CYCLE)},  3^9 = {CYCLE[8]} ≡ -1 (mod 37)")

    print(f"\n<3> == QR_37: {verify_qr_equality()}")
    print(f"QR_37 = {sorted(QR37)}")

    print("\nPower assignments (discrete logarithms):")
    for label, (expected, computed, ok) in verify_power_assignments().items():
        print(f"  {label}: {'✓' if ok else '✗'}")

    print("\nMirror involution  3^k + 3^{k+9} ≡ 0 (mod 37):")
    all_ok = True
    for k, a, b, s in verify_mirror_involution():
        ok = s == 0
        print(f"  k={k}: {a} + {b} = {a+b} ≡ {s}  {'✓' if ok else '✗'}")
        if not ok:
            all_ok = False
    print(f"  All pairs verified: {all_ok}")

    print("\nDR class membership in QR_37:")
    mem = dr_membership_in_qr()
    for dr, info in mem.items():
        tag = ""
        if info["fully_qr"]:  tag = "  ← FULLY IN QR_37"
        if info["fully_qnr"]: tag = "  ← FULLY EXCLUDED"
        print(f"  DR={dr}: {info['all']}  QR={info['qr']}  QNR={info['qnr']}{tag}")

    print("\nStructural summary:")
    print("  DR classes fully in  QR_37: DR=3, DR=7")
    print("  DR classes fully out QR_37: DR=5 → {5, 14, 23, 32}")
    print("  DR(419) = 5 → 419 is in the excluded class")

    # Verify 137 mod 37 = 26 = 3^6
    print(f"\n  137 mod 37 = {137 % 37} = 3^6 mod 37 = {pow(3,6,37)}")
    print(f"  7 + 23 = 30 = 3^13 mod 37 = {pow(3,13,37)}")
    print(f"  7 + 7 + 23 = 37 ≡ 0 (mod 37)")
    print(f"  30 ≡ -7 (mod 37): {30 == (-7) % 37}")


if __name__ == "__main__":
    summarise()
