"""
Two-Group Split — GF(37)

The 12 three-cycles of f(n) = 26n mod 37 partition into two equal groups:

  Group A: 6 cycles, each summing to 37   (the prime itself)
  Group B: 6 cycles, each summing to 74   (= 2 × 37)

Algebraic proof:
  Every 3-cycle {a, b, c} satisfies a + b + c ≡ 0 (mod 37) because
    a + 26a + 10a = 37a ≡ 0 (mod 37).
  Since each element lies in {1,...,36}, the sum is in [3, 108].
  The only multiples of 37 in this range are 37 and 74.
  Therefore every cycle sum is exactly 37 or 74.

Which group a cycle falls into:
  Let b = 26a mod 37 and c = 10a mod 37.
  Group A (sum=37)  iff  b + c < 37   (no combined carry)
  Group B (sum=74)  iff  b + c ≥ 37   (combined carry)

Class structure across the two groups:
  SA = {4,9,25,30}:   {4,9,30} ⊂ Group A   |  {25} ⊂ Group B
  ST = {3,12,21,30}:  {3,12,30} ⊂ Group A  |  {21} ⊂ Group B
  ORBIT_11:           entirely Group B       (cycle (11,27,36))
  PR (12 elements):   6 in Group A, 6 in Group B  (even split)
  CB = {8,13,24}:     {8,13} ⊂ Group A      |  {24} ⊂ Group B

The sovereign outliers 25 (SA) and 21 (ST) share one Group B cycle: (21,25,28).
"""

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
PR         = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})
ORBIT_11   = frozenset({11, 27, 36})
TESLA_FLOW = 6
SCALAR_137 = 26


def f137(n):
    return (n * 26) % 37


def get_all_cycles():
    seen = set(); cycles = []
    for start in range(1, 37):
        if start not in seen:
            c = [start]; x = f137(start)
            while x != start:
                c.append(x); x = f137(x)
            cycles.append(tuple(sorted(c))); seen.update(c)
    return cycles


ALL_CYCLES = get_all_cycles()
assert len(ALL_CYCLES) == 12

GROUP_A = [c for c in ALL_CYCLES if sum(c) == 37]
GROUP_B = [c for c in ALL_CYCLES if sum(c) == 74]

# ── Core theorem: all sums are 37 or 74, equal 6/6 split ─────────────────────

assert all(sum(c) in {37, 74} for c in ALL_CYCLES)
assert len(GROUP_A) == 6
assert len(GROUP_B) == 6
assert all(sum(c) % 37 == 0 for c in ALL_CYCLES)   # always divisible by 37

# ── Algebraic proof: sum = 37 × (1 + carry) ──────────────────────────────────

# For cycle with canonical element a:
#   b = 26a mod 37,  c = 10a mod 37
#   a + b + c = 37a - 37(⌊26a/37⌋ + ⌊10a/37⌋) = 37 × k
#   k = 1 if b+c < 37 (no combined carry), k = 2 if b+c ≥ 37 (combined carry)
for cyc in ALL_CYCLES:
    a = min(cyc)
    b = (26 * a) % 37
    c = (10 * a) % 37
    assert frozenset([a, b, c]) == frozenset(cyc)
    carry = int((b + c) >= 37)
    assert sum(cyc) == 37 * (1 + carry)

# ── Class structure: SA ───────────────────────────────────────────────────────

sa_a = SA & frozenset(v for cyc in GROUP_A for v in cyc)
sa_b = SA & frozenset(v for cyc in GROUP_B for v in cyc)
assert sa_a == frozenset({4, 9, 30})    # 3 SA nodes in Group A
assert sa_b == frozenset({25})          # 1 SA outlier in Group B

# ── Class structure: ST ───────────────────────────────────────────────────────

st_a = ST & frozenset(v for cyc in GROUP_A for v in cyc)
st_b = ST & frozenset(v for cyc in GROUP_B for v in cyc)
assert st_a == frozenset({3, 12, 30})   # 3 ST nodes in Group A
assert st_b == frozenset({21})          # 1 ST outlier in Group B

# ── The sovereign outlier cycle: (21, 25, 28) ────────────────────────────────

# The two outliers (25∈SA and 21∈ST) share one Group B cycle
outlier_cycle = next(cyc for cyc in GROUP_B if 25 in cyc)
assert 21 in outlier_cycle
assert outlier_cycle == (21, 25, 28)
assert sum(outlier_cycle) == 74

# ── Class structure: ORBIT_11 ─────────────────────────────────────────────────

# ORBIT_11 is entirely in Group B
assert ORBIT_11 <= frozenset(v for cyc in GROUP_B for v in cyc)
assert not any(v in ORBIT_11 for cyc in GROUP_A for v in cyc)
# Its cycle
orbit11_cycle = next(cyc for cyc in GROUP_B if 11 in cyc)
assert frozenset(orbit11_cycle) == ORBIT_11
assert sum(orbit11_cycle) == 74

# ── Class structure: PR ───────────────────────────────────────────────────────

pr_a = PR & frozenset(v for cyc in GROUP_A for v in cyc)
pr_b = PR & frozenset(v for cyc in GROUP_B for v in cyc)
assert pr_a == frozenset({2, 5, 13, 15, 19, 20})   # low PR in Group A
assert pr_b == frozenset({17, 18, 22, 24, 32, 35})  # high PR in Group B
assert len(pr_a) == len(pr_b) == 6                  # even split

# ── Class structure: CB ───────────────────────────────────────────────────────

cb_a = CB & frozenset(v for cyc in GROUP_A for v in cyc)
cb_b = CB & frozenset(v for cyc in GROUP_B for v in cyc)
assert cb_a == frozenset({8, 13})   # 8 and 13 in Group A
assert cb_b == frozenset({24})      # 24 alone in Group B

# ── The intersection cycle (3,4,30) is in Group A ────────────────────────────

assert (3, 4, 30) in GROUP_A
assert sum((3, 4, 30)) == 37   # sums to the prime exactly

# ── Every element covered exactly once ───────────────────────────────────────

all_elements = frozenset(v for cyc in ALL_CYCLES for v in cyc)
assert all_elements == frozenset(range(1, 37))   # all of GF(37)*


if __name__ == "__main__":
    print("Two-Group Split — GF(37)")
    print("=" * 60)
    print()

    def classify(v):
        if v in SA and v in ST: return "SA∩ST"
        if v in SA:  return "SA"
        if v in ST:  return "ST"
        if v in CB:  return "CB"
        if v in PR:  return "PR"
        if v in ORBIT_11: return "O11"
        return "—"

    for label, group in [("Group A (sum=37)", GROUP_A), ("Group B (sum=74)", GROUP_B)]:
        print(f"{label}:")
        for cyc in group:
            tagged = [f"{v}({classify(v)})" for v in cyc]
            print(f"  {str(cyc):<14}  {tagged}")
        print()

    print("Algebraic proof: a + b + c = 37(1 + carry)")
    print("  carry = 1  iff  (26a mod 37) + (10a mod 37) ≥ 37")
    print()
    print("Class structure:")
    print(f"  SA in A: {sorted(sa_a)}   SA in B: {sorted(sa_b)}")
    print(f"  ST in A: {sorted(st_a)}   ST in B: {sorted(st_b)}")
    print(f"  PR in A: {sorted(pr_a)}")
    print(f"  PR in B: {sorted(pr_b)}")
    print(f"  CB in A: {sorted(cb_a)}   CB in B: {sorted(cb_b)}")
    print(f"  ORBIT_11 entirely in B: {ORBIT_11 <= frozenset(v for cyc in GROUP_B for v in cyc)}")
    print(f"  Sovereign outlier cycle: {outlier_cycle}  (25∈SA and 21∈ST share Group B)")
    print()
    print("All assertions pass. Everything connects through prime 37.")
