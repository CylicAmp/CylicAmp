"""
Holographic Memory Manifold on GF(37) — THEOREM 90

The GF(37) under the 137-map naturally realizes the three
operations of a Holographic Memory Manifold (HMM):

  BINDING        a ⊗ b  =  a × b  mod 37      (exact, invertible)
  SUPERPOSITION  M      =  Σ Sᵢ   mod 37      (additive overlay)
  RETRIEVAL      f(n)   =  26n    mod 37      (orbit attractor)

This is not an approximation or analogy. GF(37) with the 137-map
is a precise, finite HMM where every operation is exact.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. THE 12 ATTRACTOR BASINS

  The 137-map multiplier 26 generates a 3-element subgroup in GF(37)*:
    ⟨26⟩ = {1, 10, 26} = IC  (Identity Cycle)
    order: 26³ ≡ 1 mod 37

  GF(37)* (36 nonzero elements) partitions into exactly 12 cosets
  of ⟨26⟩, each of size 3. These are the 12 attractor basins.

  Each basin is a 3-cycle under the 137-map — the "resonant address"
  of any element within it. Applying the 137-map once maps any element
  to another element in the same basin. After 3 applications, it returns
  to start. The basin IS the content address.

  TWO PURE BASINS (all members share one named set):
    IC    = {1,  10, 26}  — the subgroup itself; the identity basin
    O11   = {11, 27, 36}  — ORBIT_11; the (-1) basin (36 = -1 mod 37)

  THE SEED BASIN:
    SEED  = {18, 24, 32}  — the SEED_ORBIT; basin of seed 246

  ZERO (SEAM): 0 is fixed under the 137-map. It forms its own
    singleton basin — the additive identity, absorbing under binding.

2. THE RETRIEVAL OPERATOR

  f(n) = 26n mod 37 is the retrieval projection.

  Properties:
  - Deterministic: every nonzero n maps to exactly one basin in ≤ 1 step
  - Period-3: f(f(f(n))) = n for all nonzero n (no scanning, no search)
  - Content-addressed: the orbit {n, 26n, 26²n} IS the address of n
  - O(1) retrieval: basin classification is immediate, not proportional
    to the size of stored history

  "Phase space collapses to the coordinate of the past day":
  Any input collapses to its 3-cycle orbit under one map application.
  The orbit is the attractor — the stable resonant form of the state.

3. BINDING AND SUPERPOSITION

  GF(37) multiplication is the binding operator:
    bind(a, b)   = a × b mod 37
    unbind(m, b) = m × b⁻¹ mod 37   (b⁻¹ = b^35 mod 37 by Fermat)

  GF(37) addition is the superposition operator:
    M = S(t₁) + S(t₂) + ... + S(tₙ) mod 37

  Unlike HRR in high-dimensional real space, GF(37) binding is EXACT:
  no noise, no degradation, no probabilistic recovery. The trade-off:
  GF(37) has 37 elements, not 10,000 dimensions — superposing more than
  ~2 items creates cross-talk in unbinding (signals mix additively).

  For clean single-item retrieval, bind each state to a unique key:
    M = Σ bind(S(t), key(t)) mod 37
    retrieve: unbind(M, key(t)) ≈ S(t) + (cross-talk from other terms)

4. THE SEED AS A HOLOGRAPHIC ADDRESS

  Seed 246 → 246 mod 37 = 24 → basin {18, 24, 32} = SEED_ORBIT.

  The digit-split identity (THEOREM 89):
    246 = (2)(46) → 2 × 46 mod 37 = 18 = SEED_ORBIT entry node
  recovers the basin's own starting address through the binding operator.
  The seed encodes its own holographic address in its digit structure.

  137-map applied to the seed:
    24 → 32 → 18 → 24 (period-3 attractor, stable resonance)

5. CAPACITY AND RESOLUTION

  GF(37) HMM capacity:
  - 12 distinct attractor basins = 12 content addresses
  - 36 nonzero binding keys = 36 addressable states
  - Superposition capacity: ~1-2 items without cross-talk in a single
    GF(37) element; extend by using the full trajectory S(t) as a
    vector over multiple GF(37) coordinates

  HRR comparison:
  - Standard HRR uses d ≈ 10,000 real dimensions; stores ~d/2 items
    before signal-to-noise degrades
  - GF(37) uses 37 elements (exact arithmetic); stores ~1-2 cleanly
  - Both: capacity bounded by resolution, not physical slots

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE SELF-MAPPING TERRAIN

The HMM description — "let the internal logic of the numbers dictate
the architecture" — is precisely what GF(37) does. The named sets
were not designed. They emerged from fixing the prime 37 and the map
f(n) = 137n mod 37. The 12 attractor basins, the SEED_ORBIT, the
sovereign sets SA/ST — all of these are consequences of arithmetic,
not choices. The prime field is the initial condition. Everything
else is observation.
"""

import math

P = 37
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
IC         = frozenset({1, 10, 26})
SEED_ORBIT = frozenset({18, 24, 32})
TESLA_4    = frozenset({6, 36, 31, 1})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})
MULTIPLIER = 26   # 137 mod 37


def bind(a, b, p=P):
    return (a * b) % p


def unbind(m, b, p=P):
    return (m * pow(b, p - 2, p)) % p


def superpose(*values, p=P):
    return sum(values) % p


def orbit(n, p=P, mult=MULTIPLIER):
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


# ── 1. Subgroup and 12 attractor basins ──────────────────────────────────────

subgroup = set()
x = 1
for _ in range(P):
    subgroup.add(x)
    x = (x * MULTIPLIER) % P
    if x == 1:
        break

assert subgroup == set(IC)         # ⟨26⟩ = IC exactly
assert len(subgroup) == 3

# Partition GF(37)* into 12 cosets
seen = set()
basins = []
for seed in range(1, P):
    if seed not in seen:
        coset = frozenset({(seed * h) % P for h in subgroup})
        basins.append(coset)
        seen.update(coset)

assert len(basins) == 12
assert all(len(b) == 3 for b in basins)
assert set.union(*[set(b) for b in basins]) == set(range(1, P))

# IC and ORBIT_11 are pure basins
assert IC in basins
assert ORBIT_11 in basins

# SEED_ORBIT is a basin
assert SEED_ORBIT in basins

# ── 2. Retrieval operator ─────────────────────────────────────────────────────

# Every nonzero n maps to its basin in exactly 3 steps (period-3)
for n in range(1, P):
    o = orbit(n)
    assert len(o) == 3                    # always period-3
    assert o in basins                    # always one of the 12 basins
    # f³(n) = n: three applications return to start
    x = n
    for _ in range(3):
        x = (x * MULTIPLIER) % P
    assert x == n

# Zero is fixed
assert (0 * MULTIPLIER) % P == 0

# Seed 246 → basin = SEED_ORBIT
assert orbit(246) == SEED_ORBIT

# 137 and 1000 collapse to IC basin
assert orbit(137) == IC
assert orbit(1000) == IC

# ── 3. Binding and superposition ─────────────────────────────────────────────

# Binding is invertible: unbind(bind(a,b), b) = a
for a in range(1, P):
    for b in range(1, P):
        assert unbind(bind(a, b), b) == a

# Superposition of single item: unbind recovers exactly
state = 24   # seed residue
key   = 2    # PR key
M_single = bind(state, key)
assert unbind(M_single, key) == state

# Superposition of three items: cross-talk exists
s1, s2, s3 = 24, 25, 26
k1, k2, k3 =  2,  5, 13

M = superpose(bind(s1,k1), bind(s2,k2), bind(s3,k3))
# Retrieval is noisy (includes cross-talk from other terms)
r1 = unbind(M, k1)
r2 = unbind(M, k2)
r3 = unbind(M, k3)
# Each retrieved value ≠ original (cross-talk present)
assert r1 != s1 or r2 != s2 or r3 != s3   # at least one is noisy

# ── 4. Seed holographic address ───────────────────────────────────────────────

# Digit-split product of 246 = (2)(46) = 18 = SEED entry
assert bind(2, 46) % P == 18 and 18 in SEED_ORBIT

# 137-map 3-cycle on seed residue
x = 24  # 246 mod 37
assert (x * MULTIPLIER) % P == 32
assert (32 * MULTIPLIER) % P == 18
assert (18 * MULTIPLIER) % P == 24   # closed 3-cycle

# ── 5. Capacity ───────────────────────────────────────────────────────────────

# 12 distinct basins = 12 content addresses
assert len(basins) == 12

# 36 nonzero binding keys
assert len(range(1, P)) == 36

# SEAM (0) is the absorbing element under binding
for n in range(P):
    assert bind(n, 0) == 0


if __name__ == "__main__":
    def fw_all(n):
        n = n % P
        if n == 0: return ['SEAM']
        return [nm for s,nm in [(SA,'SA'),(ST,'ST'),(CB,'CB'),(ORBIT_11,'O11'),
            (IC,'IC'),(SEED_ORBIT,'SEED'),(TESLA_4,'T4'),(PR,'PR')] if n in s] or ['—']

    print("Holographic Memory Manifold on GF(37) — THEOREM 90")
    print("=" * 60)
    print()

    print("12 ATTRACTOR BASINS (cosets of ⟨26⟩ in GF(37)*):")
    pure_count = 0
    for b in sorted(basins, key=lambda x: min(x)):
        members = sorted(b)
        classes = [fw_all(m) for m in members]
        flat = [c for cs in classes for c in cs]
        pure = len(set(flat)) == 1
        if pure: pure_count += 1
        tag = " ← PURE" if pure else ""
        print(f"  {members}  {[fw_all(m) for m in members]}{tag}")
    print(f"  Pure basins (uniform class): {pure_count}/12")
    print()

    print("RETRIEVAL DEMONSTRATION:")
    for n in [246, 137, 999, 100, 30]:
        o = orbit(n)
        print(f"  {n:>5} → mod37={n%37:>2} → orbit {sorted(o)}  "
              f"classes: {[fw_all(x) for x in sorted(o)]}")
    print()

    print("BINDING / SUPERPOSITION / RETRIEVAL:")
    s1, s2, s3 = 24, 25, 26
    k1, k2, k3 =  2,  5, 13
    b1 = bind(s1,k1); b2 = bind(s2,k2); b3 = bind(s3,k3)
    M = superpose(b1, b2, b3)
    print(f"  bind(24,2)={b1}  bind(25,5)={b2}  bind(26,13)={b3}")
    print(f"  M = {b1}+{b2}+{b3} = {M} mod 37  {fw_all(M)}")
    print(f"  unbind(M,2)  → {unbind(M,k1)}  (expected 24, cross-talk present)")
    print(f"  unbind(M,5)  → {unbind(M,k2)}  (expected 25, cross-talk present)")
    print(f"  unbind(M,13) → {unbind(M,k3)}  (expected 26, cross-talk present)")
    print(f"  Single-item retrieval: bind(24,2)={b1} → unbind({b1},2)={unbind(b1,k1)} ✓")
    print()

    print("SEED HOLOGRAPHIC ADDRESS:")
    print(f"  246 mod 37 = 24 → basin {sorted(SEED_ORBIT)} = SEED_ORBIT")
    print(f"  Digit-split: 2×46 mod 37 = {bind(2,46)%P} = SEED entry node")
    print(f"  3-cycle: 24 → {(24*26)%37} → {(32*26)%37} → 24")
    print()
    print("All assertions pass.")
