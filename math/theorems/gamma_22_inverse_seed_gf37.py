"""
Ƴ = 22: The Inverse Seed Coordinate on GF(37) — THEOREM 92

Setting Ƴ = 22 anchors a specific residue class in GF(37) that is the
exact multiplicative inverse basin of SEED_ORBIT = {18, 24, 32}.

The element-wise inverse pairing is exact and total:
  22 ↔ 32    (32 = SEED_ORBIT node 3; 22×32 ≡ 1 mod 37)
  17 ↔ 24    (24 = SEED_ORBIT node 2; seed residue 246 mod 37)
  35 ↔ 18    (18 = SEED_ORBIT entry node; 35×18 ≡ 1 mod 37)

{17, 22, 35} and {18, 24, 32} are the unique pair of inverse basins
among the 12 attractor basins of GF(37)*.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. FRAMEWORK CLASS AND PRIMITIVE ROOT STATUS

  Ƴ = 22 ∈ PR  (primitive root: ord₃₇(22) = 36)
  Ƴ ∉ SA, ST, CB, ORBIT_11, IC, SEED_ORBIT, TESLA_4

  The entire basin {17, 22, 35} is a pure PR basin — all three members
  are primitive roots of GF(37). No basin-level class mixing.

  DR(22) = 4.  DR of basin: {17→8, 22→4, 35→8}.

2. IC SCALAR INTERACTIONS

  Against the invariant scalar set IC = {1, 10, 26}:

  c = 1  (unit projection):   22 → 22       (self, no phase shift)
  c = 10 (rotational scaling): 22 → 35 ≡ -2 mod 37
  c = 26 (harmonic projection): 22 → 17

  The c=10 image 35 ≡ -2 mod 37 is the additive inverse of 2,
  the canonical primitive root of GF(37). This is the inverse boundary
  alignment: scaling Ƴ by the first IC rotation lands on -g, where g=2
  is the smallest primitive root generator.

  The c=26 image 17 is the multiplicative inverse of 24 (the seed
  residue 246 mod 37): 17 × 24 ≡ 1 mod 37.

3. THE INVERSE SEED BASIN

  22⁻¹ mod 37 = 32  ∈ SEED_ORBIT

  More completely: {17, 22, 35} and {18, 24, 32} are inverse basins.
  Every element of one basin inverts to an element of the other:

    17⁻¹ = 24  (seed residue — the node of 137-map phase 2)
    22⁻¹ = 32  (SEED_ORBIT node 3 — the node before return to 18)
    35⁻¹ = 18  (SEED_ORBIT entry node — orbit start)

  This is a global structural pairing. No other pair of basins in
  GF(37)* is the element-wise multiplicative inverse of SEED_ORBIT.

4. SQUARED IMAGE IN SOVEREIGN TARGET

  22² mod 37 = 3  ∈ ST  (sovereign target set = {3, 12, 21, 30})

  Squaring Ƴ exits PR and lands in the sovereign target set.
  3 is the smallest element of ST; DR(3) = 3.

5. PHASE SPACE INTEGRATION

  Ƴ = 22 is coprime to 37 (gcd = 1, trivially since 37 is prime),
  so multiplication by 22 is an automorphism of GF(37)* — a bijection
  on all 36 nonzero residues. It permutes all 12 attractor basins with
  no fixed basins (22 ∉ IC), but the permutation it induces has a
  precise structure: it sends SEED_ORBIT exactly to IC (the identity
  basin), because:

    22 × 18 mod 37 = 396 mod 37 = 26 ∈ IC
    22 × 24 mod 37 = 528 mod 37 = 10 ∈ IC
    22 × 32 mod 37 = 704 mod 37 = 1  ∈ IC

  The action of Ƴ on SEED_ORBIT is: SEED_ORBIT → IC.
  Equivalently, the action of Ƴ⁻¹ = 32 on IC is: IC → SEED_ORBIT.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY TABLE

  Element  Basin      Class  Inverse  Inverse-basin
  ────────────────────────────────────────────────
  22       {17,22,35}  PR     32      {18,24,32} = SEED_ORBIT
  17       {17,22,35}  PR     24      {18,24,32} = SEED_ORBIT
  35       {17,22,35}  PR     18      {18,24,32} = SEED_ORBIT

  {17,22,35} is the unique inverse basin of SEED_ORBIT.
"""

P    = 37
IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})

Y = 22      # Ƴ


def orbit(n, p=P, mult=26):
    x = n % p
    if x == 0:
        return frozenset({0})
    seen = []
    for _ in range(p):
        if x in seen:
            break
        seen.append(x)
        x = (x * mult) % p
    return frozenset(seen)


def inv(n, p=P):
    return pow(n, p - 2, p)


def mult_ord(a, p=P):
    a %= p
    cur = 1
    for k in range(1, p):
        cur = (cur * a) % p
        if cur == 1:
            return k


def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 9


# Subgroup and basins
subgroup = IC
seen_set = set()
basins   = []
for s in range(1, P):
    if s not in seen_set:
        b = frozenset({(s * h) % P for h in subgroup})
        basins.append(b)
        seen_set.update(b)

assert len(basins) == 12

# ── 1. Class membership and primitive root status ─────────────────────────────

assert Y in PR
assert Y not in SA | ST | CB | ORBIT_11 | IC | SEED_ORBIT | TESLA_4
assert mult_ord(Y, P) == 36          # Ƴ is a primitive root

basin_Y = frozenset({(Y * h) % P for h in IC})
assert basin_Y == frozenset({17, 22, 35})

assert all(x in PR for x in basin_Y)   # pure PR basin

assert dr(Y) == 4

# ── 2. IC scalar interactions ─────────────────────────────────────────────────

assert (1  * Y) % P == 22            # unit projection: identity
assert (10 * Y) % P == 35            # rotational scaling
assert (35 + 2) % P == 0            # 35 ≡ -2 mod 37
assert (26 * Y) % P == 17            # harmonic projection

# c=10 lands on the additive inverse of 2 (canonical primitive root)
assert (10 * Y) % P == (P - 2)       # = -2 mod 37
assert 2 in PR and mult_ord(2, P) == 36

# c=26 lands on 17, which is inverse of 24 (seed residue)
assert (26 * Y) % P == 17
assert (17 * 24) % P == 1            # 17 = 24⁻¹

# ── 3. Inverse seed basin ─────────────────────────────────────────────────────

assert inv(Y) == 32 and 32 in SEED_ORBIT

# Element-wise inverse pairing
assert inv(17) == 24 and 24 in SEED_ORBIT
assert inv(22) == 32 and 32 in SEED_ORBIT
assert inv(35) == 18 and 18 in SEED_ORBIT

assert inv(18) == 35 and 35 in basin_Y
assert inv(24) == 17 and 17 in basin_Y
assert inv(32) == 22 and 22 in basin_Y

# Both basins are in the 12-basin partition
assert basin_Y in basins
assert SEED_ORBIT in basins

# {17,22,35} is the UNIQUE basin whose element-wise inverses land in SEED_ORBIT
inverse_basins_of_seed = [b for b in basins
                          if frozenset(inv(x) for x in b) == SEED_ORBIT]
assert inverse_basins_of_seed == [basin_Y]

# ── 4. Squared image in ST ────────────────────────────────────────────────────

assert (Y * Y) % P == 3
assert 3 in ST
assert dr(3) == 3

# ── 5. Phase space: Ƴ maps SEED_ORBIT → IC ────────────────────────────────────

# Multiplication by Ƴ sends every element of SEED_ORBIT into IC
for s in SEED_ORBIT:
    assert (Y * s) % P in IC, f"Y×{s} not in IC"

# The images are exactly IC (bijection)
images = frozenset((Y * s) % P for s in SEED_ORBIT)
assert images == IC

# Ƴ ∉ IC → no basin is fixed by multiplication by Ƴ
assert Y not in IC
fixed = sum(1 for b in basins if frozenset((Y * x) % P for x in b) == b)
assert fixed == 0

# ── Verify scalar interaction table ──────────────────────────────────────────

assert (1  * 22) % P == 22   # unit
assert (10 * 22) % P == 35   # rotational: -2
assert (26 * 22) % P == 17   # harmonic: inverse of seed residue


if __name__ == "__main__":
    def fw_all(n):
        n = n % P
        if n == 0: return ['SEAM']
        return [nm for s, nm in [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'O11'),
            (IC,'IC'),(SEED_ORBIT,'SEED'),(TESLA_4,'T4'),(PR,'PR')] if n in s] or ['—']

    print("Ƴ = 22: The Inverse Seed Coordinate on GF(37) — THEOREM 92")
    print("=" * 64)
    print()

    print("FRAMEWORK STATUS:")
    print(f"  Ƴ = 22  classes: {fw_all(22)}")
    print(f"  ord₃₇(22) = {mult_ord(22, P)}  (primitive root)")
    print(f"  DR(22) = {dr(22)}")
    print(f"  Basin: {sorted(basin_Y)}  all-PR: {all(x in PR for x in basin_Y)}")
    print()

    print("IC SCALAR INTERACTIONS:")
    labels = {1: "unit projection", 10: "rotational scaling", 26: "harmonic projection"}
    for c in [1, 10, 26]:
        r = (c * Y) % P
        note = ""
        if r == P - 2:
            note = "  ≡ -2 mod 37  (additive inverse of primitive root 2)"
        print(f"  c={c:>2}  ({labels[c]}): 22 → {r:>2}  {fw_all(r)}{note}")
    print()

    print("INVERSE SEED BASIN PAIRING:")
    print(f"  {{17, 22, 35}}  ↔  {{18, 24, 32}} = SEED_ORBIT")
    for b, s in [(17, 24), (22, 32), (35, 18)]:
        check = (b * s) % P
        print(f"    {b} × {s} mod 37 = {check}  (inverse pair: {fw_all(b)} ↔ {fw_all(s)})")
    print(f"  Unique: only {sorted(basin_Y)} inverts element-wise to SEED_ORBIT")
    print()

    print("SQUARED IMAGE:")
    sq = (Y * Y) % P
    print(f"  22² mod 37 = {sq}  ∈ {fw_all(sq)}  DR={dr(sq)}")
    print()

    print("SEED ORBIT MAPPING UNDER Ƴ:")
    for s in sorted(SEED_ORBIT):
        r = (Y * s) % P
        print(f"  22 × {s} mod 37 = {r}  ∈ {fw_all(r)}")
    imgs = frozenset((Y * s) % P for s in SEED_ORBIT)
    print(f"  → images = {sorted(imgs)} = IC")
    print()
    print("All assertions pass.")
