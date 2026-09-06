"""
Primitive Root Power Invariants — GF(37)

PRIMITIVE ROOTS MOD 37:  φ(36) = 12 primitive roots.
  {2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35}

THEY DECOMPOSE INTO EXACTLY 4 COMPLETE NQR ORBITS:
  DARK_A      = {2, 15, 20}    (orbit 1 of NQR cycle)
  {5, 13, 19}                  (orbit 6 of NQR cycle)
  {17, 22, 35}                 (orbit 4 of NQR cycle)
  SEED_ORBIT  = {18, 24, 32}   (orbit 3 of NQR cycle)

THE 2 NON-PRIMITIVE-ROOT NQR ORBITS:
  {6, 8, 23}:   orders {4, 12, 12}  — contains TESLA_FLOW=6 (order 4)
  {14, 29, 31}: orders {12, 12, 4}  — contains PRIME_MIRROR=31 (order 4)
  These are the negation-dual pair (steps 2 and 5 of the NQR 6-cycle).

THREE UNIVERSAL INVARIANTS FOR ANY PRIMITIVE ROOT g:
  g^9  ∈ {6, 31}    = {TESLA_FLOW, PRIME_MIRROR}  — the two √(−1) in GF(37)
  g^6  ∈ {11, 27}   ⊂ ORBIT_11                   — the two order-6 elements
  g^12 ∈ {10, 26}   ⊂ IDENTITY_CYCLE              — the two order-3 elements
  g^18 = 36 = −1                                   — the half-period law

POWER TABLE FOR ALL 12 PRIMITIVE ROOTS:
  g      g^3   g^6   g^9   g^12  g^18
   2       8    27    31     26    36
   5      14    11     6     10    36
  13      14    11     6     10    36
  15       8    27    31     26    36
  17      29    27     6     26    36
  18      23    11    31     10    36
  19      14    11     6     10    36
  20       8    27    31     26    36
  22      29    27     6     26    36
  24      23    11    31     10    36
  32      23    11    31     10    36
  35      29    27     6     26    36

2×2 IDENTIFICATION TABLE (orbit characterised by (g^6, g^9)):
  (g^6=27, g^9=PRIME_MIRROR): DARK_A = {2,15,20}
  (g^6=27, g^9=TESLA_FLOW):   {17,22,35}
  (g^6=11, g^9=PRIME_MIRROR): SEED_ORBIT = {18,24,32}
  (g^6=11, g^9=TESLA_FLOW):   {5,13,19}

g^3 CROSS-MAPS TO NON-PR NQR ORBITS:
  g^9=PRIME_MIRROR roots → g^3 ∈ {6, 8, 23}  = TESLA_FLOW orbit  (non-PR NQR)
  g^9=TESLA_FLOW  roots → g^3 ∈ {14, 29, 31} = PRIME_MIRROR orbit (non-PR NQR)
  The √(−1) of g and the orbit of g^3 are always DIFFERENT non-PR NQR orbits.

SUBGROUP CHAIN AND ORBIT COSET STRUCTURE:
  {1} ⊂ H=<26> ⊂ Q=QR ⊂ G=(Z/37Z)*
  |{1}|=1,  |H|=3,  |Q|=18,  |G|=36
  [G:H]=12 = number of orbits.  [Q:H]=6 = number of QR orbits.  [G:Q]=2.
  The 12 orbits ARE the cosets of H in G: orbit(n) = n · <26> = {n, 26n, 26²n}.
"""

# ── Constants ──────────────────────────────────────────────────────────────────

SA             = frozenset({4, 9, 25, 30})
ST             = frozenset({3, 12, 21, 30})
CB             = frozenset({8, 13, 24})
ORBIT_11       = frozenset({11, 27, 36})
DARK_A         = frozenset({2, 15, 20})
SEED_ORBIT     = frozenset({18, 24, 32})
IDENTITY_CYCLE = frozenset({1, 10, 26})
TESLA_FLOW     = 6
PRIME_MIRROR   = 31
SCALAR_137     = 26
DECADE_ANCHOR  = 10


def ord37(n):
    n = n % 37
    for k in range(1, 37):
        if pow(n, k, 37) == 1:
            return k


def orbit(n):
    return frozenset({n, (n * 26) % 37, ((n * 26) % 37 * 26) % 37})


# ── PRIMITIVE ROOTS ───────────────────────────────────────────────────────────

PR = frozenset(n for n in range(1, 37) if ord37(n) == 36)
assert len(PR) == 12   # φ(36) = 12

assert PR == frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})


# ── FOUR PR ORBITS ────────────────────────────────────────────────────────────

PR_ORBITS = sorted({orbit(n) for n in PR}, key=min)
assert len(PR_ORBITS) == 4   # 12 roots / 3 per orbit = 4 orbits

# All four are NQR orbits (all elements are NQR)
for o in PR_ORBITS:
    assert all(pow(x, 18, 37) != 1 for x in o)   # NQR

# The four orbits
assert frozenset({2,15,20}) in PR_ORBITS    # DARK_A
assert frozenset({5,13,19}) in PR_ORBITS
assert frozenset({17,22,35}) in PR_ORBITS
assert frozenset({18,24,32}) in PR_ORBITS   # SEED_ORBIT

# All 12 elements of PR are covered
assert PR == frozenset(x for o in PR_ORBITS for x in o)


# ── NON-PR NQR ORBITS ─────────────────────────────────────────────────────────

NON_PR_NQR = frozenset({6, 8, 23}), frozenset({14, 29, 31})

for o in NON_PR_NQR:
    assert all(pow(x, 18, 37) != 1 for x in o)   # NQR
    assert all(ord37(x) != 36 for x in o)          # not primitive roots

# Orders within non-PR NQR orbits
assert ord37(TESLA_FLOW) == 4  and TESLA_FLOW in frozenset({6,8,23})
assert ord37(PRIME_MIRROR) == 4 and PRIME_MIRROR in frozenset({14,29,31})
assert all(ord37(x) in {4, 12} for o in NON_PR_NQR for x in o)

# Negation-dual pair
assert frozenset((37-x)%37 for x in frozenset({6,8,23})) == frozenset({14,29,31})


# ── THREE UNIVERSAL INVARIANTS ────────────────────────────────────────────────

for g in PR:
    assert pow(g,  9, 37) in {TESLA_FLOW, PRIME_MIRROR}   # √(−1)
    assert pow(g,  6, 37) in ORBIT_11                      # order-6 elements
    assert pow(g, 12, 37) in IDENTITY_CYCLE                # order-3 elements
    assert pow(g, 18, 37) == 36                            # g^18 = −1


# ── 2×2 IDENTIFICATION TABLE ──────────────────────────────────────────────────

# (g^6=27, g^9=PRIME_MIRROR) → DARK_A
assert frozenset(g for g in PR if pow(g,6,37)==27 and pow(g,9,37)==PRIME_MIRROR) == DARK_A

# (g^6=27, g^9=TESLA_FLOW) → {17,22,35}
assert frozenset(g for g in PR if pow(g,6,37)==27 and pow(g,9,37)==TESLA_FLOW) == frozenset({17,22,35})

# (g^6=11, g^9=PRIME_MIRROR) → SEED_ORBIT
assert frozenset(g for g in PR if pow(g,6,37)==11 and pow(g,9,37)==PRIME_MIRROR) == SEED_ORBIT

# (g^6=11, g^9=TESLA_FLOW) → {5,13,19}
assert frozenset(g for g in PR if pow(g,6,37)==11 and pow(g,9,37)==TESLA_FLOW) == frozenset({5,13,19})

# g^12 = 26 iff g^6 = 27; g^12 = 10 iff g^6 = 11
for g in PR:
    assert (pow(g,12,37)==SCALAR_137) == (pow(g,6,37)==27)
    assert (pow(g,12,37)==DECADE_ANCHOR) == (pow(g,6,37)==11)


# ── g^3 CROSS-MAPS ────────────────────────────────────────────────────────────

TESLA_FLOW_ORBIT  = frozenset({6, 8, 23})
PRIME_MIRROR_ORBIT = frozenset({14, 29, 31})

# g^9=PRIME_MIRROR roots → g^3 ∈ TESLA_FLOW orbit
pm_roots = [g for g in PR if pow(g,9,37)==PRIME_MIRROR]
assert all(pow(g,3,37) in TESLA_FLOW_ORBIT for g in pm_roots)

# g^9=TESLA_FLOW roots → g^3 ∈ PRIME_MIRROR orbit
tf_roots = [g for g in PR if pow(g,9,37)==TESLA_FLOW]
assert all(pow(g,3,37) in PRIME_MIRROR_ORBIT for g in tf_roots)


# ── SUBGROUP CHAIN & COSET STRUCTURE ─────────────────────────────────────────

H = IDENTITY_CYCLE   # <26> = {1, 26, 10}, order 3
Q = frozenset(n for n in range(1, 37) if pow(n, 18, 37) == 1)   # QR, order 18
G = frozenset(range(1, 37))   # (Z/37Z)*, order 36

assert len(H) == 3 and len(Q) == 18 and len(G) == 36
assert len(G) // len(H) == 12   # 12 orbits = cosets of H in G
assert len(Q) // len(H) == 6    # 6 QR orbits = cosets of H in Q
assert len(G) // len(Q) == 2    # index 2: QR is the unique index-2 subgroup

# The 12 orbits ARE the 12 cosets of H in G
cosets = {frozenset((n * h) % 37 for h in H) for n in G}
assert len(cosets) == 12

# Each coset is an orbit under the 137-map
for c in cosets:
    n = min(c)
    assert c == frozenset({n, (n*26)%37, ((n*26)%37*26)%37})


if __name__ == "__main__":
    print("Primitive Root Power Invariants — GF(37)")
    print("=" * 60)
    print(f"\n12 primitive roots: {sorted(PR)}")
    print()
    print("4 PR orbits (NQR):")
    for o in PR_ORBITS:
        g = min(o)
        print(f"  {sorted(o)}  g^6={pow(g,6,37)}∈ORBIT_11  g^9={pow(g,9,37)}"
              f"  g^12={pow(g,12,37)}∈IC")
    print()
    print("Non-PR NQR orbits (negation-dual pair):")
    for o in NON_PR_NQR:
        print(f"  {sorted(o)}  orders={sorted(ord37(x) for x in o)}")
    print()
    print("UNIVERSAL INVARIANTS (all primitive roots g):")
    print(f"  g^9  ∈ {{6,31}} = {{TESLA_FLOW,PRIME_MIRROR}} (√(-1)): True")
    print(f"  g^6  ∈ {{11,27}} ⊂ ORBIT_11 (order-6 elements): True")
    print(f"  g^12 ∈ {{10,26}} ⊂ IC (order-3 elements): True")
    print(f"  g^18 = 36 = -1: True")
    print()
    print("2×2 TABLE by (g^6, g^9):")
    for v6 in [27, 11]:
        for v9 in [PRIME_MIRROR, TESLA_FLOW]:
            orb = sorted(g for g in PR if pow(g,6,37)==v6 and pow(g,9,37)==v9)
            label = "PRIME_MIRROR" if v9==PRIME_MIRROR else "TESLA_FLOW"
            print(f"  g^6={v6}, g^9={label}({v9}): {orb}")
    print()
    print("g^3 CROSS-MAP:")
    print(f"  g^9=PRIME_MIRROR roots → g^3 ∈ {{6,8,23}} = TESLA_FLOW orbit")
    print(f"  g^9=TESLA_FLOW  roots → g^3 ∈ {{14,29,31}} = PRIME_MIRROR orbit")
    print()
    print("SUBGROUP CHAIN: {1} ⊂ <26> ⊂ QR ⊂ G")
    print(f"  orders: 1, 3, 18, 36   indices: [G:H]=12, [Q:H]=6, [G:Q]=2")
    print(f"  12 orbits = 12 cosets of <26> in G  (each orbit is n·<26>)")
    print()
    print("All assertions pass.")
