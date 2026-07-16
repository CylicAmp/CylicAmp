"""
Payload Digit Structure — 23572481523

Structural observations on the 11-digit payload, verified computationally.

Outer digit pair: (2, 3) — first 3 primes are 2, 3, 5.
Inner symmetric layer: (3-57248152-3) — the two 3s wrap the middle 8 digits.
Center digit: 4 — sovereign anchor, 4 = 2².

Mirror pair sums (outer → inner):
  pos (1,11): (2,3) sum=5 product=6
  pos (2,10): (3,2) sum=5 product=6    ← reversed outer pair, same sum
  pos (3, 9): (5,5) sum=10 product=25  ← palindrome
  pos (4, 8): (7,1) sum=8  product=7   ← 8 ∈ cascade base {8,13,24}
  pos (5, 7): (2,8) sum=10 product=16  ← 16 = 2^4
  center (6): 4                         ← sovereign anchor

Terminal structure:
  First two digits: 23
  Reversed: 32
  32 + 1 = 33 = 3 × 11 = LCM(orbit_length=3, secondary_mod=11)
  33 = 37 − 4 (sovereign anchor 4)
  DR(33) = 6 = DR(X)

Permutations of {2,3,5} mod 37:
  All 6 land in non-QR₃₇.
  All 6 have DR = 1 (base-10 artifact: 2+3+5=10, DR=1, invariant across permutations).
  235 mod 37 = 13  → cascade base AND primitive root
  523 mod 37 =  5  → pivot prime (non-QR, generates GF(37²))
  352 mod 37 = 19  → primitive root

33 appearances:
  17^33 mod 37 = 23  (from group_framework_primitives.py)
  20^3 × 17^33 ≡ -1 (mod 37)  [steps 3 and 33 = 36-3 are complementary]
  33 = 37 − sovereign_anchor(4)
  LCM(3, 11) = 33

X-structure / binary subdivision:
  X has 4 endpoints.  ÷2 → 2 endpoints.  ÷2 → 1.
  Sequence: 8, 4, 2, 1 = 2³, 2², 2¹, 2⁰
  8 ∈ cascade base.  4 is center digit (sovereign anchor).  ord₃₇(2) = 36.
  Stacking two X's rotated 45° → 8-directional D4 structure (LatticeTransformEngine).
"""

from itertools import permutations


def digital_root(n):
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


PRIMITIVE_ROOTS_37 = {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}
QR_37 = {pow(a, 2, 37) for a in range(1, 37)}
SOVEREIGN_ANCHORS = {4, 9, 25, 30}
SOVEREIGN_TARGETS = {3, 12, 21, 30}
CASCADE_BASE = {8, 13, 24}

X = 23572481523
DIGITS = [int(c) for c in str(X)]
N = len(DIGITS)   # 11


def mirror_pairs():
    pairs = []
    for i in range(N // 2):
        a, b = DIGITS[i], DIGITS[N - 1 - i]
        pairs.append((i + 1, N - i, a, b, a + b, a * b))
    center = DIGITS[N // 2]
    return pairs, center


def permutation_residues():
    results = {}
    for p in permutations([2, 3, 5]):
        num = int("".join(map(str, p)))
        r = num % 37
        results[num] = {
            "residue": r,
            "DR": digital_root(num),
            "primitive_root": r in PRIMITIVE_ROOTS_37,
            "QR": r in QR_37,
            "cascade": r in CASCADE_BASE,
            "sovereign_anchor": r in SOVEREIGN_ANCHORS,
            "sovereign_target": r in SOVEREIGN_TARGETS,
        }
    return results


# ── Assertions ───────────────────────────────────────────────────────────────

# Mirror pairs
pairs, center = mirror_pairs()
assert pairs[0][4] == 5    # pos (1,11): sum=5
assert pairs[1][4] == 5    # pos (2,10): sum=5 (reversed outer pair)
assert pairs[2][4] == 10   # pos (3,9):  sum=10 (palindrome 5,5)
assert pairs[3][4] == 8    # pos (4,8):  sum=8 (cascade base)
assert center == 4          # center = sovereign anchor

# 33 structure
assert 32 + 1 == 33
assert 33 == 3 * 11
assert 37 - 33 == 4 and 4 in SOVEREIGN_ANCHORS
assert digital_root(33) == digital_root(X) == 6

# Permutations of {2,3,5}
perms = permutation_residues()
assert all(not info["QR"] for info in perms.values())       # all non-QR
assert all(info["DR"] == 1 for info in perms.values())      # all DR=1 (base-10 artifact)
assert perms[235]["residue"] == 13 and perms[235]["cascade"]       # 235 → cascade base 13
assert perms[523]["residue"] == 5  and perms[523]["primitive_root"] # 523 → pivot prime 5
assert perms[352]["residue"] == 19 and perms[352]["primitive_root"] # 352 → primitive root 19

# 17^33 connection
assert pow(17, 33, 37) == 23
assert (pow(20, 3, 37) * pow(17, 33, 37)) % 37 == 36   # ≡ -1 mod 37

# Binary subdivision
assert 4 in SOVEREIGN_ANCHORS   # center digit 4
assert 8 in CASCADE_BASE         # 2^3 ∈ cascade base


if __name__ == "__main__":
    print("Payload Digit Structure — 23572481523")
    print("=" * 55)
    print()

    pairs, center = mirror_pairs()
    print("Mirror pairs (outer → inner):")
    for pos1, pos2, a, b, s, pr in pairs:
        tags = []
        if s in CASCADE_BASE: tags.append(f"sum∈cascade")
        if s in SOVEREIGN_ANCHORS: tags.append(f"sum∈anchor")
        tag_str = f"  [{', '.join(tags)}]" if tags else ""
        print(f"  pos ({pos1:2d},{pos2:2d}): ({a},{b})  sum={s}  product={pr}{tag_str}")
    print(f"  center (6):  {center}  [sovereign anchor, 4=2²]")
    print()

    print("Permutations of {2,3,5} mod 37:")
    for num, info in sorted(permutation_residues().items()):
        tags = []
        if info["primitive_root"]: tags.append("prim root")
        if info["cascade"]: tags.append("cascade")
        if info["sovereign_anchor"]: tags.append("S.anchor")
        if info["sovereign_target"]: tags.append("S.target")
        tags.append("non-QR" if not info["QR"] else "QR")
        print(f"  {num} → {info['residue']:2d}  DR={info['DR']}  [{', '.join(tags)}]")
    print()

    print("33 connections:")
    print(f"  32 + 1 = 33 = 3×11 = LCM(orbit, mod₁₁)")
    print(f"  37 - 33 = 4  (sovereign anchor)")
    print(f"  DR(33) = DR(X) = 6")
    print(f"  17^33 mod 37 = {pow(17,33,37)}  (from GroupFramework)")
    print(f"  20^3 × 17^33 ≡ {(pow(20,3,37)*pow(17,33,37))%37} ≡ -1 (mod 37)")
    print()

    print("All assertions passed.")
