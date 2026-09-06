"""
Cycle Symmetry Maps — GF(37)

Three maps on GF(37)* — negation (n→-n), squaring (n→n²), and inversion
(n→n⁻¹) — induce well-defined maps on the 12 three-cycles (cosets of <26>).

THEOREM 1: Negation is a bijection Group A ↔ Group B, preserving sector.
  Algebraic proof:
    If {a,b,c} is a cycle with sum S, then {-a,-b,-c} sums to 3·37 - S = 111 - S.
    If S=37 (Group A): negated sum = 74 (Group B).
    If S=74 (Group B): negated sum = 37 (Group A).
  Sector preservation: χ(-a) = χ(36)·χ(a) = (+1)·χ(a) = χ(a).
  [36 ∈ QR since 36 ≡ −1 and (−1)^{(37−1)/2} = (−1)^{18} = 1]
  Negation pairs:
    Visible×A ↔ Visible×B  (3 pairs)
    Dark×A    ↔ Dark×B     (3 pairs)

THEOREM 2: The two self-inverse cycles are (1,10,26) and (11,27,36).
  These are the only cycles closed under multiplicative inversion.
  Both are the cycles of subgroups: <26>={1,10,26} (order 3) and
  {1,36,11,27,...} contains ORBIT_11 (the cycle {11,27,36}).
  In both cycles, elements pair as inverses within the cycle.

THEOREM 3: The sovereign cycle and outlier cycle are mutual inverses.
  (3,4,30) ↔ (21,25,28) under element-wise inversion:
    3⁻¹ = 25   (ST → SA)
    4⁻¹ = 28   (SA → unclassified)
    30⁻¹ = 21  (SA∩ST → ST)
  Inversion transmutes sovereign roles: the unique intersection node 30
  inverts to the sole ST element 21 of the outlier cycle.

THEOREM 4: Squaring maps every dark cycle to a visible cycle (2-to-1 over 3 targets).
  Dark → visible: χ(a²) = χ(a)² = 1 for any a∈NQR.
  The 6 dark cycles map 2-to-1 onto exactly 3 visible cycles:
    Sovereign (3,4,30) ← (2,15,20) and (17,22,35)
    Outlier   (21,25,28) ← (5,13,19) and (18,24,32)  [includes seed orbit]
    ORBIT_11  (11,27,36) ← (6,8,23) and (14,29,31)

CHAIN: seed orbit →⁻¹ (17,22,35) →² sovereign cycle
  (18,24,32)⁻¹ = (17,22,35)  and  (17,22,35)² = (3,4,30)
  The seed orbit reaches the sovereign cycle in two algebraic steps.

NEGATION PAIRS:
  Visible×A (1,10,26) ↔ Visible×B (11,27,36)    [<26> ↔ ORBIT_11]
  Visible×A (3,4,30)  ↔ Visible×B (7,33,34)      [sovereign ↔ ?]
  Visible×A (9,12,16) ↔ Visible×B (21,25,28)     [SA/ST shadow ↔ outlier]
  Dark×A (2,15,20)    ↔ Dark×B (17,22,35)
  Dark×A (5,13,19)    ↔ Dark×B (18,24,32)         [? ↔ seed orbit]
  Dark×A (6,8,23)     ↔ Dark×B (14,29,31)

SQUARING MAP ON ALL CYCLES:
  (1,10,26)  →² (1,10,26)   [fixed: self-squares]
  (11,27,36) →² (1,10,26)   [ORBIT_11 squares to identity cycle]
  (3,4,30)   →² (9,12,16)
  (9,12,16)  →² (7,33,34)   ↔² (9,12,16)  [2-cycle among visible]
  (7,33,34)  →² (9,12,16)
  (21,25,28) →² (7,33,34)
"""

# ── Constants ──────────────────────────────────────────────────────────────────

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})


def f137(n):
    return (n * 26) % 37


def chi(n):
    return 1 if pow(n % 37, 18, 37) == 1 else -1


def get_cycle_map():
    seen = set(); result = {}
    for s in range(1, 37):
        if s not in seen:
            c = [s]; x = f137(s)
            while x != s:
                c.append(x); x = f137(x)
            cyc = tuple(sorted(c))
            for v in c:
                result[v] = cyc
            seen.update(c)
    return result


C = get_cycle_map()
ALL = sorted(set(C.values()))

QR   = frozenset(n for n in range(1, 37) if chi(n) ==  1)
NQR  = frozenset(n for n in range(1, 37) if chi(n) == -1)

VISIBLE = [c for c in ALL if all(v in QR  for v in c)]
DARK    = [c for c in ALL if all(v in NQR for v in c)]
GROUP_A = [c for c in ALL if sum(c) == 37]
GROUP_B = [c for c in ALL if sum(c) == 74]


# ── THEOREM 1: Negation maps A ↔ B, preserves sector ─────────────────────────

# 36 ≡ -1 is QR (since 36^18 mod 37 = 1)
assert chi(36) == 1

for cyc in ALL:
    neg_cyc = C[(37 - min(cyc)) % 37]
    # Group swap
    if cyc in GROUP_A: assert neg_cyc in GROUP_B
    if cyc in GROUP_B: assert neg_cyc in GROUP_A
    # Sector preserved
    if cyc in VISIBLE: assert neg_cyc in VISIBLE
    if cyc in DARK:    assert neg_cyc in DARK

# Algebraic proof: sum of negated cycle = 3×37 - sum = 111 - sum
for cyc in ALL:
    neg_elems = tuple(sorted((37 - v) % 37 for v in cyc))
    assert sum(cyc) + sum(neg_elems) == 111   # always 37+74 = 111 = 3×37


# ── THEOREM 2: Self-inverse cycles ────────────────────────────────────────────

SELF_INVERSE = [c for c in ALL if all(pow(v, -1, 37) in c for v in c)]
assert len(SELF_INVERSE) == 2
assert set(SELF_INVERSE) == {(1, 10, 26), (11, 27, 36)}

# (1,10,26): 1⁻¹=1, 26⁻¹=10, 10⁻¹=26  — elements pair as inverses within cycle
assert pow(1,  -1, 37) == 1  and 1  in (1, 10, 26)
assert pow(26, -1, 37) == 10 and 10 in (1, 10, 26)
assert pow(10, -1, 37) == 26 and 26 in (1, 10, 26)

# (11,27,36): 36⁻¹=36, 11⁻¹=27, 27⁻¹=11
assert pow(36, -1, 37) == 36 and 36 in (11, 27, 36)
assert pow(11, -1, 37) == 27 and 27 in (11, 27, 36)
assert pow(27, -1, 37) == 11 and 11 in (11, 27, 36)


# ── THEOREM 3: Sovereign ↔ outlier under inversion ────────────────────────────

# Element-wise inversion
assert pow(3,  -1, 37) == 25  and 25 in (21, 25, 28)   # 3∈ST → 25∈SA
assert pow(4,  -1, 37) == 28  and 28 in (21, 25, 28)   # 4∈SA → 28 (unclassified)
assert pow(30, -1, 37) == 21  and 21 in (21, 25, 28)   # 30∈SA∩ST → 21∈ST

# Cycle-level: C_{3^{-1}} = outlier
assert C[pow(3, -1, 37)] == (21, 25, 28)
assert C[pow(21,-1, 37)] == (3, 4, 30)   # inverse of inverse = back to sovereign


# ── THEOREM 4: Squaring maps dark → visible (2-to-1 over 3 targets) ───────────

# All dark cycles square to visible cycles
for cyc in DARK:
    a = min(cyc)
    assert C[pow(a, 2, 37)] in VISIBLE

# Exactly 3 visible cycles are squares of dark cycles
dark_square_targets = set(C[pow(min(d), 2, 37)] for d in DARK)
assert len(dark_square_targets) == 3

# Each target gets exactly 2 dark preimages
for target in dark_square_targets:
    preimages = [d for d in DARK if C[pow(min(d), 2, 37)] == target]
    assert len(preimages) == 2

# The 3 targets are: sovereign cycle, outlier cycle, and ORBIT_11 cycle
assert dark_square_targets == {(3,4,30), (21,25,28), (11,27,36)}

# Specific preimage pairs
sovereign_preimages = sorted(d for d in DARK if C[pow(min(d),2,37)]==(3,4,30))
outlier_preimages   = sorted(d for d in DARK if C[pow(min(d),2,37)]==(21,25,28))
orbit11_preimages   = sorted(d for d in DARK if C[pow(min(d),2,37)]==(11,27,36))

assert set(sovereign_preimages) == {(2,15,20), (17,22,35)}
assert set(outlier_preimages)   == {(5,13,19), (18,24,32)}   # seed orbit in here
assert set(orbit11_preimages)   == {(6,8,23),  (14,29,31)}

# Seed orbit squares to outlier sovereign
assert C[pow(18, 2, 37)] == (21, 25, 28)


# ── CHAIN: seed →⁻¹ (17,22,35) →² sovereign ──────────────────────────────────

# Step 1: invert seed orbit elements
assert C[pow(18, -1, 37)] == (17, 22, 35)   # 18⁻¹ = 35 ∈ (17,22,35)
assert C[pow(24, -1, 37)] == (17, 22, 35)   # 24⁻¹ = ?
assert C[pow(32, -1, 37)] == (17, 22, 35)   # 32⁻¹ = ?

# Step 2: square (17,22,35) to get sovereign cycle
assert C[pow(17, 2, 37)] == (3, 4, 30)

# Full chain in one expression
seed_inverse_cycle = C[pow(18, -1, 37)]      # (17,22,35)
seed_chain_target  = C[pow(min(seed_inverse_cycle), 2, 37)]   # (3,4,30)
assert seed_chain_target == (3, 4, 30)


# ── Negation pair table ────────────────────────────────────────────────────────

NEG_PAIRS = {}
for cyc in ALL:
    a = min(cyc)
    neg = C[(37 - a) % 37]
    if cyc < neg:
        NEG_PAIRS[cyc] = neg

# Verify all 6 pairs are (A,B) crossing pairs
assert len(NEG_PAIRS) == 6
for a_cyc, b_cyc in NEG_PAIRS.items():
    assert (a_cyc in GROUP_A and b_cyc in GROUP_B) or \
           (a_cyc in GROUP_B and b_cyc in GROUP_A)

# The specific pairs
assert NEG_PAIRS.get((1,10,26)) == (11,27,36) or (11,27,36) in NEG_PAIRS and NEG_PAIRS[(11,27,36)]==(1,10,26)
assert C[(37-1)%37] == (11,27,36)   # 36 ∈ ORBIT_11 cycle


if __name__ == "__main__":
    print("Cycle Symmetry Maps — GF(37)")
    print("=" * 60)
    print()

    print("NEGATION PAIRS (Group A ↔ Group B, sector preserved):")
    neg_done = set()
    for cyc in sorted(ALL):
        a = min(cyc)
        neg = C[(37 - a) % 37]
        if cyc not in neg_done and neg not in neg_done:
            sect = "visible" if cyc in VISIBLE else "dark"
            print("  %s  ↔  %s  [%s]" % (str(cyc), str(neg), sect))
            neg_done.update([cyc, neg])

    print()
    print("SELF-INVERSE CYCLES:")
    for c in SELF_INVERSE:
        print("  %s" % str(c))

    print()
    print("INVERSION PAIRS:")
    inv_done = set()
    for cyc in sorted(ALL):
        a = min(cyc)
        inv = C[pow(a, -1, 37)]
        if cyc not in inv_done and inv not in inv_done:
            label = "[SELF]" if cyc == inv else ""
            print("  %s  ↔  %s  %s" % (str(cyc), str(inv), label))
            inv_done.update([cyc, inv])

    print()
    print("SQUARING: dark cycle square targets:")
    for target in sorted(dark_square_targets):
        pres = sorted(d for d in DARK if C[pow(min(d),2,37)]==target)
        print("  %s  ←²  %s" % (str(target), pres))

    print()
    print("CHAIN: seed orbit (18,24,32) →⁻¹ (17,22,35) →² (3,4,30) [sovereign]")
    print()
    print("All assertions pass.")
