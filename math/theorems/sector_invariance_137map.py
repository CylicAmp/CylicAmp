"""
Sector Invariance under the 137-Map — GF(37)

The 137-map f(n) = 26n mod 37 preserves the Legendre symbol (sector).

THEOREM: For every n in GF(37)*, χ(f(n)) = χ(n).

Proof: χ(26n) = χ(26) · χ(n) = (+1) · χ(n) = χ(n). □
  [26 is a quadratic residue: 26 ≡ 15² mod 37, so χ(26)=+1]
  [10 is a quadratic residue: 10 ≡ 6² · ... → pow(10,18,37)=1]

CONSEQUENCE: Every 3-cycle under the 137-map is sector-homogeneous —
  all three elements are QR (visible) or all three are NQR (dark).
  Mixed cycles (1 or 2 NQR elements) do not exist in GF(37).

COROLLARY: The 12 three-cycles admit a 2×2 classification by two
  independent binary properties:
    (1) Sector:  visible (all QR) vs dark (all NQR)
    (2) Group:   A (sum=37)       vs B   (sum=74)
  Exactly 3 cycles per cell:

    Visible × Group A: (1,10,26), (3,4,30), (9,12,16)
    Visible × Group B: (7,33,34), (11,27,36), (21,25,28)
    Dark × Group A:    (2,15,20), (5,13,19), (6,8,23)
    Dark × Group B:    (14,29,31), (17,22,35), (18,24,32)

WHY SCALAR_137=26 MATTERS:
  The map multiplier 26 is visible (QR). This is the structural reason
  cycles are sector-homogeneous. Had the 137-map used an NQR multiplier,
  every step would flip the sector and cycles would alternate dark-visible.
  The fact that 137 ≡ 26 (mod 37) and 26 ∈ QR is what makes the sovereign
  GF(37) possible: SA and ST can both live entirely in the visible sector
  because the orbiting map that connects them is visible-preserving.

  More precisely: 10 = 26² mod 37 (the two-step multiplier) is also QR.
  Both the 1-step and 2-step maps preserve sector.

ADDITIONAL STRUCTURE:
  - The seed orbit {18,24,32} is entirely dark (all ∈ NQR), Group B.
  - The sovereign cycle (3,4,30) is entirely visible (all ∈ QR), Group A.
  - ORBIT_11 = {11,27,36} is entirely visible, Group B.
  - χ(b)·χ(c) = 1 for any cycle {a,b,c}: b and c always share a sector.
    (From a·b·c = a³ and χ(a³) = χ(a), so χ(b)·χ(c) = 1.)
"""

# ── Constants ────────────────────────────────────────────────────────

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_FLOW = 6
SCALAR_137 = 26


def f137(n):
    return (n * 26) % 37


def chi(n, p=37):
    """Legendre symbol (n/p): +1 QR/visible, −1 NQR/dark, 0 if p|n."""
    n = n % p
    if n == 0:
        return 0
    return 1 if pow(n, (p - 1) // 2, p) == 1 else -1


QR  = frozenset(n for n in range(1, 37) if chi(n) ==  1)
NQR = frozenset(n for n in range(1, 37) if chi(n) == -1)


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


# ── Core theorem: 26 and 10 are both QR ───────────────────────────────────────

assert chi(SCALAR_137) == 1              # 26 ∈ QR: the map multiplier is visible
assert chi(10) == 1                      # 10 ∈ QR: the two-step multiplier is visible
assert (26 * 26) % 37 == 10             # 26² ≡ 10 (mod 37)


# ── Sector invariance of the 137-map ──────────────────────────────────────────

for n in range(1, 37):
    assert chi(f137(n)) == chi(n)        # sector is preserved at every step


# ── Consequence: every cycle is sector-homogeneous ────────────────────────────

VISIBLE_CYCLES = []
DARK_CYCLES    = []

for cyc in ALL_CYCLES:
    sectors = [chi(v) for v in cyc]
    assert len(set(sectors)) == 1, f"Mixed cycle found: {cyc}"   # all same sector
    if sectors[0] == 1:
        VISIBLE_CYCLES.append(cyc)
    else:
        DARK_CYCLES.append(cyc)

assert len(VISIBLE_CYCLES) == 6
assert len(DARK_CYCLES)    == 6

# No mixed cycles
assert all(all(v in QR  for v in c) for c in VISIBLE_CYCLES)
assert all(all(v in NQR for v in c) for c in DARK_CYCLES)


# ── 2×2 classification ────────────────────────────────────────────────────────

GROUP_A = [c for c in ALL_CYCLES if sum(c) == 37]
GROUP_B = [c for c in ALL_CYCLES if sum(c) == 74]

VISIBLE_A = [c for c in VISIBLE_CYCLES if c in GROUP_A]
VISIBLE_B = [c for c in VISIBLE_CYCLES if c in GROUP_B]
DARK_A    = [c for c in DARK_CYCLES    if c in GROUP_A]
DARK_B    = [c for c in DARK_CYCLES    if c in GROUP_B]

assert len(VISIBLE_A) == 3
assert len(VISIBLE_B) == 3
assert len(DARK_A)    == 3
assert len(DARK_B)    == 3

# Exact membership
assert set(VISIBLE_A) == {(1,10,26), (3,4,30), (9,12,16)}
assert set(VISIBLE_B) == {(7,33,34), (11,27,36), (21,25,28)}
assert set(DARK_A)    == {(2,15,20), (5,13,19), (6,8,23)}
assert set(DARK_B)    == {(14,29,31), (17,22,35), (18,24,32)}


# ── Notable cycles in context ─────────────────────────────────────────────────

# Sovereign cycle: visible + Group A
assert (3, 4, 30) in VISIBLE_CYCLES and (3, 4, 30) in GROUP_A

# Seed orbit: dark + Group B
assert SEED_ORBIT == frozenset({18, 24, 32})
assert (18, 24, 32) in DARK_CYCLES and (18, 24, 32) in GROUP_B

# ORBIT_11: visible + Group B
assert all(v in ORBIT_11 for v in (11, 27, 36))
assert (11, 27, 36) in VISIBLE_CYCLES and (11, 27, 36) in GROUP_B

# chi(b)·chi(c) = 1 for every cycle (b and c always share a sector)
for cyc in ALL_CYCLES:
    a, b, c = cyc
    assert chi(b) * chi(c) == 1          # b and c have the same sector
    assert chi(a) * chi(b) * chi(c) == chi(a)   # product = chi(min element)

# a·b·c = a³ for every cycle (algebraic basis)
for cyc in ALL_CYCLES:
    a, b, c = sorted(cyc)
    assert (a * b * c) % 37 == pow(a, 3, 37)


if __name__ == "__main__":
    print("Sector Invariance under the 137-Map — GF(37)")
    print("=" * 60)
    print()
    print(f"χ(26) = {chi(26)}  [SCALAR_137 is visible → map preserves sector]")
    print(f"χ(10) = {chi(10)}  [two-step multiplier is visible]")
    print()
    print("All 12 cycles — sector and group:")
    print(f"  {'Cycle':<16} Sector   Group  Classes")
    print(f"  {'-'*60}")
    for cyc in sorted(ALL_CYCLES):
        sect  = "visible" if cyc in VISIBLE_CYCLES else "dark"
        group = "A" if cyc in GROUP_A else "B"
        tags  = []
        for v in cyc:
            if v in SA and v in ST: tags.append(f"{v}(SA∩ST)")
            elif v in SA:           tags.append(f"{v}(SA)")
            elif v in ST:           tags.append(f"{v}(ST)")
            elif v in CB:           tags.append(f"{v}(CB)")
            elif v in PR:           tags.append(f"{v}(PR)")
            elif v in ORBIT_11:     tags.append(f"{v}(O11)")
            elif v in SEED_ORBIT:   tags.append(f"{v}(seed)")
            else:                   tags.append(str(v))
        mark = ""
        if cyc == (3,4,30):     mark = "  ← sovereign"
        if cyc == (18,24,32):   mark = "  ← seed orbit"
        if cyc == (11,27,36):   mark = "  ← ORBIT_11"
        print(f"  {str(cyc):<16} {sect:<8} {group}      {tags}{mark}")
    print()
    print("2×2 classification (3 cycles per cell):")
    print(f"  Visible × A: {sorted(VISIBLE_A)}")
    print(f"  Visible × B: {sorted(VISIBLE_B)}")
    print(f"  Dark    × A: {sorted(DARK_A)}")
    print(f"  Dark    × B: {sorted(DARK_B)}")
    print()
    print("All assertions pass. The 137-map multiplier (26∈QR) locks sector.")
