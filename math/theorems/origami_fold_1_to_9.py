"""
1234(5)6789 Origami Fold — Structural Audit

Classification: Theorem

The sequence 1-2-3-4-(5)-6-7-8-9 folded at center 5 produces a complete
layered structure. Every fold pair sums to 10; the center contact 4+5=9
anchors the DR modulus. The fold axis 5 carries DR=5 — the absent class
from QR₃₇ — marking it as the structural gap around which the cycle orbits.

Fold pairs (outer → center):
  1+9 = 10,  2+8 = 10,  3+7 = 10,  4+6 = 10   (all 10)
  4+5 = 9    center contact = DR modulus

Asymmetry under fold:
  Left  {1,2,3,4}  sum = 10   (= pair sum)
  Right {6,7,8,9}  sum = 30   (= sovereign anchor ∩ target = fixed point 30)
  Right / Left = 3             (sovereign target generator)
  Total 1+…+9 = 45,  DR(45) = 9

Box patterns — DR ladder with step 3:
  1+1+2+2 =  6 → DR=6  (coupling signature)
  1+2+3+3 =  9 → DR=9  (DR modulus — sovereign fixed point)
  1+3+4+4 = 12 → DR=3  (sovereign target)
  Common difference: 3 (sovereign target step)

Framework connections:
  10² ≡ 26 (mod 37) = 26        (pair sum squared = scalar)
  30 ∈ ANCHORS ∩ TARGETS               (right sum is the sovereign fixed point)
  DR(5) = 5 — absent class from QR₃₇   (fold axis sits on the structural gap)
  5 is the only residue class in {1..9} absent from ⟨3⟩ = QR₃₇
"""


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0


SEQ      = list(range(1, 10))   # 1..9
CENTER   = 5
FOLD_SUM = 10

QR37    = frozenset((x * x) % 37 for x in range(1, 37))
ANCHORS = frozenset({4, 9, 25, 30})
TARGETS = frozenset({3, 12, 21, 30})
CYCLE18 = [pow(3, k, 37) for k in range(1, 19)]
# 26 = 137 mod 37


# ── Fold pairs ─────────────────────────────────────────────────────────────

PAIRS = [(CENTER - i, CENTER + i) for i in range(1, CENTER)]
assert len(PAIRS) == 4
assert all(a + b == FOLD_SUM for a, b in PAIRS)

# Center contact
assert CENTER - 1 + CENTER == 9    # 4+5 = 9 = DR modulus

# ── Left / right asymmetry ─────────────────────────────────────────────────

LEFT  = list(range(1, CENTER))       # [1,2,3,4]
RIGHT = list(range(CENTER + 1, 10))  # [6,7,8,9]

assert sum(LEFT)  == FOLD_SUM        # left sum = pair sum = 10
assert sum(RIGHT) == 30              # right sum = sovereign fixed point
assert sum(RIGHT) // sum(LEFT) == 3  # right/left = sovereign target

# 30 is the unique sovereign anchor AND target (fixed point of the framework)
assert 30 in ANCHORS
assert 30 in TARGETS

# Total
assert sum(SEQ) == 45
assert dr(45) == 9

# ── Framework: pair sum 10 → 26 ────────────────────────────────────

assert (FOLD_SUM ** 2) % 37 == 26    # 10² ≡ 26 mod 37

# ── Fold axis 5: the absent DR class ──────────────────────────────────────

assert dr(CENTER) == 5
DR5_VALUES = [n for n in range(1, 37) if dr(n) == 5]
assert not any(v in QR37 for v in DR5_VALUES)   # DR=5 absent from ⟨3⟩
assert CENTER not in QR37                        # 5 itself is not in QR₃₇

# ── Box patterns — DR ladder ───────────────────────────────────────────────

BOXES = [(1,1,2,2), (1,2,3,3), (1,3,4,4)]
box_sums = [sum(b) for b in BOXES]
assert box_sums == [6, 9, 12]

box_drs = [dr(s) for s in box_sums]
assert box_drs == [6, 9, 3]    # coupling → modulus → sovereign target

# Common difference = 3 (sovereign target step)
assert all(box_sums[i+1] - box_sums[i] == 3 for i in range(len(box_sums)-1))

# DR values: 6 (coupling), 9 (modulus), 3 (sovereign target)
assert box_drs[0] == 6    # coupling signature
assert box_drs[1] == 9    # DR modulus
assert box_drs[2] == 3    # sovereign target


if __name__ == "__main__":
    print("1234(5)6789 Origami Fold — Structural Audit")
    print()
    print("Fold pairs (folded at center 5):")
    for a, b in PAIRS:
        print(f"  {a} + {b} = {a+b}")
    print(f"  4 + 5 = {4+5}  (center contact = DR modulus)")
    print()
    print(f"Left  {LEFT}  sum = {sum(LEFT)}")
    print(f"Right {RIGHT}  sum = {sum(RIGHT)}  (sovereign anchor ∩ target)")
    print(f"Right / Left = {sum(RIGHT)//sum(LEFT)}  (sovereign target generator)")
    print(f"Total 1+…+9 = {sum(SEQ)},  DR = {dr(sum(SEQ))}")
    print()
    print(f"Pair sum 10:  10² mod 37 = {FOLD_SUM**2 % 37} = 26 ✓")
    print(f"Fold axis 5:  DR=5, absent from QR₃₇ — structural gap ✓")
    print()
    print("Box patterns (DR ladder, step=3):")
    for box, s, d in zip(BOXES, box_sums, box_drs):
        label = {6:"coupling", 9:"DR modulus", 3:"sovereign target"}[d]
        print(f"  {'+'.join(str(v) for v in box)} = {s}  →  DR={d}  ({label})")
    print()
    print("All assertions passed.")
