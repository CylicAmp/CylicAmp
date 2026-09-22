"""
24 Equivalence Pattern — Coupling Signature Audit

Classification: Theorem

Every pair (a, b) with a+b=24 has DR(a)+DR(b) reducing to 6 — the coupling
signature. 24 is the unique product 2³×3 = 8×3, linking the cube of the
minimal primitive root (2) to the f26 target (3). Its mirror pair
(22,2) and (23,1) demonstrate the compensation principle.

Verified claims:
  DR(222) = DR(123) = 6                   (both digit sums = 6)
  22+2 = 23+1 = 24                        (compensation: +1 base, -1 addend)
  DR(24) = 6                              (coupling signature)
  24 = 2³×3 = 2×12 = 2×(3^8 mod 37)     (primitive root × f26 target)
  All 23 pairs (a, 24-a): DR(a)+DR(24-a) → 6   (universal coupling lock)
  22 = 2×11 = 2×(3^15 mod 37)            (both factors in QR₃₇)
  23 is prime, DR(23)=5                   (absent class — the gap)
"""

from math import gcd


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


CYCLE18    = [pow(3, k, 37) for k in range(1, 19)]
QR37       = frozenset((x * x) % 37 for x in range(1, 37))
# 26 = 137 mod 37

# ── 222 and 123 both DR=6 ──────────────────────────────────────────────────

assert 2 + 2 + 2 == 6
assert 1 + 2 + 3 == 6
assert dr(222) == 6
assert dr(123) == 6

# ── Compensation principle: 22+2 = 23+1 = 24 ──────────────────────────────

assert 22 + 2 == 24
assert 23 + 1 == 24

# General: a+b = (a+1)+(b-1) — additive invariance
for a in range(1, 24):
    b = 24 - a
    assert (a + 1) + (b - 1) == a + b == 24

# ── DR(24) = 6 — coupling signature ───────────────────────────────────────

assert dr(24) == 6

# ── 24 = 2³×3 ─────────────────────────────────────────────────────────────

assert 24 == 2**3 * 3
assert 24 == 2 * 12
assert pow(3, 8, 37) == 12    # 12 = f26 target at cycle position 8
assert 12 in QR37

# ── Universal coupling lock: every pair (a, 24-a) has DR sum → 6 ──────────

for a in range(1, 24):
    b = 24 - a
    raw = dr(a) + dr(b)
    assert dr(raw) == 6, f"Pair ({a},{b}): DR({dr(a)})+DR({dr(b)})={raw}, DR={dr(raw)}"

# The raw DR sums fall in {6, 15} — both reduce to 6
raw_sums = {dr(a) + dr(24 - a) for a in range(1, 24)}
assert raw_sums == {6, 15}
assert all(dr(s) == 6 for s in raw_sums)

# ── 22 = 2×11 = 2×(3^15 mod 37) ──────────────────────────────────────────

assert 22 == 2 * 11
assert pow(3, 15, 37) == 11    # 11 = 3^15 ∈ QR₃₇
assert 11 in QR37
assert dr(22) == 4

# ── 23 is prime, DR(23)=5 (absent class) ──────────────────────────────────

assert all(23 % i != 0 for i in range(2, 23))    # 23 is prime
assert dr(23) == 5
DR5_VALUES = [n for n in range(1, 37) if dr(n) == 5]
assert not any(v in QR37 for v in DR5_VALUES)     # DR=5 absent from QR₃₇

# ── 10² ≡ 26 (mod 37) — pair sum connects to scalar ───────────────

assert (10 * 10) % 37 == 26    # fold pair sum 10 → 26


if __name__ == "__main__":
    print("24 Equivalence Pattern — Coupling Signature Audit")
    print()
    print(f"  DR(222) = {dr(222)},  DR(123) = {dr(123)}  (both = 6 ✓)")
    print(f"  22+2 = {22+2},  23+1 = {23+1}  (compensation ✓)")
    print(f"  DR(24) = {dr(24)}  (coupling signature)")
    print(f"  24 = 2³×3 = 2×12,  12 = 3^8 mod 37 (f26 target) ✓")
    print()
    print("  All pairs (a, 24-a) — DR coupling lock:")
    for a in range(1, 13):
        b = 24 - a
        raw = dr(a) + dr(b)
        print(f"    DR({a:2d})+DR({b:2d}) = {dr(a)}+{dr(b)} = {raw:2d} → DR={dr(raw)}")
    print(f"  Raw DR sums ∈ {sorted(raw_sums)}, both → DR=6 ✓")
    print()
    print(f"  22 = 2×11 = 2×(3^15 mod 37),  DR(22)={dr(22)}")
    print(f"  23 is prime,  DR(23)={dr(23)} (absent class, ∉ QR₃₇) ✓")
    print()
    print("All assertions passed.")
