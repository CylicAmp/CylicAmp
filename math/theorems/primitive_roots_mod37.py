"""
Primitive Roots mod 37 — Structural Audit

Classification: Theorem

Characterises the 12 primitive roots of (Z/37Z)* and their relationship to
the F₃₇ anchor framework.

Verified claims:
  Count            φ(φ(37)) = φ(36) = 12  — exactly 12 primitive roots
  Explicit set     {2,5,13,15,17,18,19,20,22,24,32,35}
  Non-overlap      No primitive root is a quadratic residue mod 37
                   ⟨3⟩ = QR₃₇ ∩ ⟨3⟩ = QR₃₇; primitive roots ⊆ QNR₃₇
  Anchor gaps      DR=3 absent from primitive roots (DR=3 anchor targets safe)
                   DR=7 absent from primitive roots (DR=7 class ⊆ QR₃₇)
  Generator 2      ord₃₇(2) = 36;  2 ≡ 3^{-1} × ... is the minimal generator
  SCALAR link      2^12 ≡ 26 (mod 37) = 26 = 3^6 mod 37

DR distribution across the 12 primitive roots:
  DR=1: [10]           DR=2: [20]           DR=4: [13,22]
  DR=5: [5,32]         DR=6: [15,24]        DR=8: [17]
  DR=9: [18]           DR=1: [19,10] …      (see full table below)

Key structural fact:
  Every primitive root has odd order 36 = 4×9 as an element of ⟨g⟩.
  Since QR₃₇ = {g^{2k}} (even powers), any primitive root g satisfies
  g^k ∉ QR₃₇ for odd k — confirming primitive roots ⊆ QNR₃₇.
"""

from math import gcd


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


def multiplicative_order(a, mod):
    """Compute ord_mod(a)."""
    if gcd(a, mod) != 1:
        return None
    o = 1
    cur = a % mod
    while cur != 1:
        cur = cur * a % mod
        o += 1
    return o


# ── Core quantities ────────────────────────────────────────────────────────

P = 37
GROUP_ORDER = P - 1    # 36 = φ(37)

from math import isqrt

def euler_phi(n):
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

PHI_36 = euler_phi(GROUP_ORDER)    # φ(36) = 12

CYCLE18 = [pow(3, k, 37) for k in range(1, 19)]
QR37 = frozenset((x * x) % 37 for x in range(1, 37))   # = frozenset(CYCLE18)
QNR37 = frozenset(range(1, 37)) - QR37

ANCHORS = frozenset({4, 9, 25, 30})
TARGETS = frozenset({3, 12, 21, 30})
# 26 = 137 mod 37


# ── Compute primitive roots ────────────────────────────────────────────────

PRIM_ROOTS = sorted(
    a for a in range(1, P) if multiplicative_order(a, P) == GROUP_ORDER
)


# ── Assertions ─────────────────────────────────────────────────────────────

# 1. Count = φ(36) = 12
assert PHI_36 == 12, f"φ(36) = {PHI_36}"
assert len(PRIM_ROOTS) == 12, f"Found {len(PRIM_ROOTS)} primitive roots"

# 2. Exact set
assert PRIM_ROOTS == [2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35], \
    f"Unexpected primitive root set: {PRIM_ROOTS}"

# 3. Every primitive root has order 36
assert all(multiplicative_order(g, P) == GROUP_ORDER for g in PRIM_ROOTS)

# 4. Primitive roots are disjoint from QR₃₇
assert all(g not in QR37 for g in PRIM_ROOTS), \
    "A primitive root lies in QR₃₇ — impossible (primitive roots are QNRs)"
assert frozenset(PRIM_ROOTS) <= QNR37

# 5. QNR₃₇ = {1..36} \ QR₃₇ has 18 elements; primitive roots ⊆ QNR₃₇
assert len(QNR37) == 18
assert len(frozenset(PRIM_ROOTS) & QNR37) == 12   # all 12 primitive roots are QNRs

# 6. DR=3 and DR=7 are absent from primitive roots
#    (both DR classes lie entirely within QR₃₇)
DR3_VALUES = [n for n in range(1, P) if dr(n) == 3]
DR7_VALUES = [n for n in range(1, P) if dr(n) == 7]
assert DR3_VALUES == [3, 12, 21, 30]
assert DR7_VALUES == [7, 16, 25, 34]
assert all(v in QR37 for v in DR3_VALUES)
assert all(v in QR37 for v in DR7_VALUES)
assert not any(g in DR3_VALUES for g in PRIM_ROOTS), "Unexpected: DR=3 anchor target as prim root"
assert not any(g in DR7_VALUES for g in PRIM_ROOTS), "Unexpected: DR=7 value as prim root"

# 7. F26 anchors and targets are NOT primitive roots
assert not (ANCHORS & frozenset(PRIM_ROOTS)), "An anchor is a primitive root — unexpected"
assert not (TARGETS & frozenset(PRIM_ROOTS)), "A target is a primitive root — unexpected"

# 8. Generator 2: ord₃₇(2) = 36, and 2^12 ≡ 26 (mod 37)
assert multiplicative_order(2, P) == GROUP_ORDER
assert pow(2, 12, P) == 26    # 2^12 = 26 = 26

# 9. Generator 2 produces all of (Z/37Z)*
cycle_2 = [pow(2, k, P) for k in range(1, P)]
assert len(set(cycle_2)) == GROUP_ORDER   # hits all 36 non-zero residues

# 10. 3 is NOT a primitive root (ord₃₇(3) = 18, not 36)
assert multiplicative_order(3, P) == 18
assert 3 not in PRIM_ROOTS

# 11. Primitive roots come in pairs g ↔ g⁻¹ (both are primitive roots)
inverses = {g: pow(g, P - 2, P) for g in PRIM_ROOTS}
assert all(inv in PRIM_ROOTS for inv in inverses.values()), \
    "Inverse of a primitive root is not a primitive root"

# 12. DR distribution of the 12 primitive roots
from collections import Counter
pr_dr_freq = Counter(dr(g) for g in PRIM_ROOTS)
# DR=3 and DR=7 must be absent
assert pr_dr_freq[3] == 0
assert pr_dr_freq[7] == 0
# DR=5 appears exactly twice: {5, 32}
assert pr_dr_freq[5] == 2
assert sorted(g for g in PRIM_ROOTS if dr(g) == 5) == [5, 32]

# 13. # 26 = 137 mod 37
assert 26 not in PRIM_ROOTS
assert 26 in QR37


if __name__ == "__main__":
    print("Primitive Roots mod 37 — Structural Audit")
    print()
    print(f"  p = {P},  (Z/{P}Z)* has order {GROUP_ORDER}")
    print(f"  φ({GROUP_ORDER}) = {PHI_36}  →  exactly {PHI_36} primitive roots")
    print()
    print(f"  Primitive roots: {PRIM_ROOTS}")
    print()
    print(f"  All have order {GROUP_ORDER}: {all(multiplicative_order(g,P)==GROUP_ORDER for g in PRIM_ROOTS)}")
    print(f"  All are QNRs (none in QR₃₇): {all(g not in QR37 for g in PRIM_ROOTS)}")
    print()
    print("  DR distribution of primitive roots:")
    for d in range(1, 10):
        vals = sorted(g for g in PRIM_ROOTS if dr(g) == d)
        if vals:
            note = " ← absent from anchor sets" if d == 5 else ""
            print(f"    DR={d}: {vals}{note}")
    print(f"  DR=3: (absent) — anchor targets {{3,12,21,30}} ⊆ QR₃₇")
    print(f"  DR=7: (absent) — DR=7 class {{7,16,25,34}} ⊆ QR₃₇")
    print()
    print(f"  ord₃₇(2) = {multiplicative_order(2,P)}  (minimal primitive root)")
    print(f"  2^12 mod 37 = {pow(2,12,P)} = 26 ✓")
    print(f"  ord₃₇(3) = {multiplicative_order(3,P)}  (not a primitive root — generates QR₃₇ only)")
    print()
    print(f"  Inverse pairing: every g ↔ g⁻¹ both primitive roots ✓")
    pairs = sorted({(min(g,inverses[g]), max(g,inverses[g])) for g in PRIM_ROOTS})
    for a, b in pairs:
        print(f"    {a} ↔ {b}  (product={a*b%P} mod 37)")
    print()
    print(f"  F26 anchors {{4,9,25,30}} ∩ primitive roots = ∅ ✓")
    print(f"  F26 anchor targets {{3,12,21,30}} ∩ primitive roots = ∅ ✓")
    print(f"  26={26} ∈ QR₃₇, not a primitive root ✓")
    print()
    print("All assertions passed.")
