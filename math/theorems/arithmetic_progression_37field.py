"""
Arithmetic Progression on Z/37Z — Field Collapse and 1/9 Attractor

Classification: Theorem

The 37-term arithmetic progression a_k = a + 18k (k=0..36) over Z/37Z
forms a complete residue system (gcd(18,37)=1), and its sum collapses to
the NULL element mod 37 while preserving the anchor residue mod 9.

Formula:
  S_37 = (37/2)[2a + 36·18] = 37a + 18·18·37 = 37(a + 324)

Field collapse table:
  Z:         37(a + 324)   — integer; 37 is the spectral carrier
  Z/37Z:     0             — NULL element lockdown (sum = 666 = 18×37 ≡ 0)
  Z/9Z:      a mod 9       — anchor preserved (18≡0 mod 9, 37≡1 mod 9)

The universal cycle sum:
  Σ_{k=0}^{36} (a + 18k) ≡ Σ_{r=0}^{36} r = 36×37/2 = 666 ≡ 0 (mod 37)
  666 = 18×37 = 2×333 = DR-cascade: 666→18→9

1/9 attractor mechanism:
  37 ≡ 1 (mod 9)  →  S_37 ≡ 1×(a+0) ≡ a (mod 9)
  The 37-period is a null projector on the 37-field and
  an identity operator on the 9-subfield.
"""

from math import gcd


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


# ── Step-18 is coprime to 37 → complete residue system ────────────────────

assert gcd(18, 37) == 1

residues_18 = [(18 * k) % 37 for k in range(37)]
assert sorted(residues_18) == list(range(37)), "Not a complete residue system"

# ── Universal cycle sum = 666 ──────────────────────────────────────────────

cycle_sum = sum(range(37))    # = 36×37/2
assert cycle_sum == 666
assert cycle_sum == 18 * 37
assert cycle_sum == 36 * 37 // 2
assert cycle_sum % 37 == 0    # NULL element mod 37

# DR cascade: 666 → 18 → 9
assert 6 + 6 + 6 == 18
assert 1 + 8 == 9
assert dr(666) == 9

# ── S_37 formula: S = 37(a + 324) ─────────────────────────────────────────

def S37_formula(a):
    return 37 * (a + 324)

def S37_direct(a):
    return sum(a + 18 * k for k in range(37))

for a in range(50):
    assert S37_formula(a) == S37_direct(a), f"Formula mismatch at a={a}"

# ── Mod-37 collapse: always 0 ─────────────────────────────────────────────

for a in range(37):
    assert S37_formula(a) % 37 == 0, f"S37 mod 37 ≠ 0 at a={a}"

# ── Mod-9 attractor: preserves anchor ─────────────────────────────────────

assert 37 % 9 == 1     # 37 ≡ 1 (mod 9) — identity on 9-subfield
assert 18 % 9 == 0     # 18 ≡ 0 (mod 9) — differential annihilated
assert 324 % 9 == 0    # 324 = 18² ≡ 0 (mod 9)

for a in range(37):
    assert S37_formula(a) % 9 == a % 9, \
        f"Attractor broken: S37 mod 9 = {S37_formula(a)%9}, a mod 9 = {a%9}"

# ── Key anchors: mod-37 null, mod-9 anchor set {4,9,25,30} ──────────────

QR37    = frozenset((x * x) % 37 for x in range(1, 37))
CYCLE18 = [pow(3, k, 37) for k in range(1, 19)]
ANCHORS = frozenset({4, 9, 25, 30})
TARGETS = frozenset({3, 12, 21, 30})

# Sovereign anchor a=30: mod-37→0, mod-9→3 (target DR)
assert S37_formula(30) % 37 == 0
assert S37_formula(30) % 9 == 30 % 9    # = 3

# # 26 = 137 mod 37
assert S37_formula(26) % 37 == 0
assert S37_formula(26) % 9 == 26 % 9    # = 8

# ── Bifurcation exactness ─────────────────────────────────────────────────

# For a ≡ 1 (mod 9): attractor locks at 1 while collapsing to 0 mod 37
a_test = 1    # DR=1 (identity)
assert S37_formula(a_test) % 37 == 0
assert S37_formula(a_test) % 9  == 1


if __name__ == "__main__":
    print("Arithmetic Progression Z/37Z — Field Collapse and 1/9 Attractor")
    print()
    print(f"  gcd(18,37) = {gcd(18,37)}  → step-18 generates Z/37Z ✓")
    print(f"  Universal cycle sum = {cycle_sum} = 18×37 = 36×37/2")
    print(f"  DR(666): {666} → {6+6+6} → {dr(666)}  ✓")
    print()
    print(f"  S_37 = 37(a + 324)")
    print(f"  37 mod 9 = {37%9}  (identity on 9-subfield)")
    print(f"  18 mod 9 = {18%9}  (differential annihilated)")
    print(f"  324 mod 9 = {324%9}")
    print()
    print("  Field collapse for selected anchors:")
    print(f"  {'a':>4}  {'mod 37':>8}  {'mod 9':>6}  {'a mod 9':>8}")
    print("  " + "─" * 34)
    for a in [0, 1, 3, 9, 26, 30, 37]:
        print(f"  {a:4d}  {S37_formula(a)%37:8d}  {S37_formula(a)%9:6d}  {a%9:8d}")
    print()
    print(f"  Bifurcation (a=1): mod 37 = 0 (null), mod 9 = 1 (attractor) ✓")
    print()
    print("All assertions passed.")
