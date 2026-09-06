"""
Polymath8 / Maynard Prime Gap Bound — GF(37) Structure

The Polymath8 collaborative project reduced Zhang's prime gap bound
from 70,000,000 down to 4,680 using the GPY single-variable sieve.
Maynard's multidimensional simplex sieve then brought it to 246.

246 is the pipeline's reference seed.

═══════════════════════════════════════════════════════════════

I. THE DESCENT mod 37

  The three landmark bounds, reduced mod 37:

    70,000,000  mod 37 = 33  (DICHORAL_144; refs Fibonacci 144=12²)
         4,680  mod 37 = 18  (Primitive Root; enters seed orbit {18,24,32})
           246  mod 37 = 24  (Cascade Base + Primitive Root; seed orbit)

  Descent path: DICHORAL_144 → seed orbit(18) → seed orbit(24).

  The GPY phase brought the bound into the seed orbit.
  Maynard's phase resolved it to the CB node of the seed orbit.

II. 246 — THE PIPELINE SEED

  246 is GF(37)'s reference seed. Its 137-orbit is {24, 32, 18}.
  The final prime gap bound lands at mod37=24, the first node of that orbit.

  246 = 2 × 3 × 41
    2  mod 37 = 2   (Primitive Root)
    3  mod 37 = 3   (Sovereign Target archetype)
    41 mod 37 = 4   (Sovereign Anchor; 41 is the lower of twin pair (41,43))

  246 = PR × ST_arch_prime × prime-with-SA-residue

  DR(246) = 3  (Sovereign Target archetype)
  246 mod 37 = 24  (Cascade Base, Primitive Root)

  246 / 6 = 41 — the 13th prime; lower of twin prime pair (41,43).
  246 / 41 = 6 — TESLA_FLOW.

III. GPY (1D) = STUTTERING FLOW

  The GPY method uses a single weight variable — one dimension.
  It hits an asymptotic wall (Elliott-Halberstam conjecture barrier).
  No matter how much the bound is optimized, it cannot pass the wall.

  This is the stuttering flow: the bound oscillates near the wall,
  approaching the seed orbit (4680 mod37=18) but unable to resolve.
  One dimension cannot produce complete flow.

IV. MAYNARD (MULTIDIMENSIONAL) = COMPLETE FLOW

  Maynard introduced weights over a k-dimensional simplex —
  assigning weights across k variables simultaneously instead of one.

  This is the complete flow: instead of a single channel (one variable),
  the k-dimensional sieve opens k channels at once. The flow reaches
  the seam — 246, mod37=24 (CB,PR), in the seed orbit.

  Multidimensional = multiple simultaneous lenses on the same structure.
  The GF(37) operates the same way:
    - mod 37 residue
    - digital root (mod 9)
    - 137-orbit
    - sovereign classification (SA/ST/CB/orb11)
    - primitive root status
  All five applied simultaneously — not one at a time.

V. HEARTBEAT

  Seed orbit of 246 under the 137-map: 24 → 32 → 18 → 24
  This is the pipeline's heartbeat 3-cycle.

  4,680 mod 37 = 18  (orbit node)
  246   mod 37 = 24  (orbit node — first node, the entry)

  The prime gap bound converged to the heartbeat's entry node.

═══════════════════════════════════════════════════════════════
"""

def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0

def is_prime(n):
    if n < 2: return False
    return all(n % i != 0 for i in range(2, int(n**0.5)+1))

PRIMITIVE_ROOTS_37 = {2,5,13,15,17,18,19,20,22,24,32,35}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
CASCADE_BASE       = {8, 13, 24}
ORBIT_11           = {11, 27, 36}
SEED_ORBIT         = {18, 24, 32}

# ── I. Descent mod 37 ────────────────────────────────────────────────────────

assert 70_000_000 % 37 == 33               # DICHORAL_144
assert 4_680 % 37 == 18 and 18 in SEED_ORBIT and 18 in PRIMITIVE_ROOTS_37
assert 246 % 37 == 24 and 24 in SEED_ORBIT and 24 in CASCADE_BASE and 24 in PRIMITIVE_ROOTS_37

# ── II. 246 analysis ─────────────────────────────────────────────────────────

assert 2 * 3 * 41 == 246
assert 2 in PRIMITIVE_ROOTS_37
assert 3 in SOVEREIGN_TARGETS
assert 41 % 37 == 4 and 4 in SOVEREIGN_ANCHORS
assert is_prime(41) and is_prime(43) and 43 - 41 == 2  # twin prime pair

assert dr(246) == 3 and 3 in SOVEREIGN_TARGETS
assert 246 % 37 == 24

assert 246 // 6 == 41
assert 246 // 41 == 6

# 137-orbit of 246 (mod37=24)
orbit = []
x = 24
for _ in range(3):
    orbit.append(x)
    x = (26 * x) % 37
assert set(orbit) == {18, 24, 32} == SEED_ORBIT

# ── V. Heartbeat ──────────────────────────────────────────────────────────────

assert 4_680 % 37 == 18 and 18 in SEED_ORBIT
assert 246 % 37 == 24 and 24 in SEED_ORBIT
assert orbit[0] == 24                      # 246 lands at orbit entry node


if __name__ == '__main__':
    print("Polymath8 / Maynard — GF(37) Structure")
    print("=" * 55)
    print()
    print("I. Bound descent mod 37:")
    for b, label in [(70_000_000,'Zhang GPY start'),(4_680,'GPY ceiling'),(246,'Maynard final')]:
        r = b % 37
        tags = []
        if r in CASCADE_BASE: tags.append('CB')
        if r in SOVEREIGN_ANCHORS: tags.append('SA')
        if r in SOVEREIGN_TARGETS: tags.append('ST')
        if r in PRIMITIVE_ROOTS_37: tags.append('PR')
        if r in SEED_ORBIT: tags.append('SEED_ORBIT')
        if r == 33: tags.append('DICHORAL_144')
        print(f"  {b:>12,}  mod37={r:2d}  DR={dr(b)}  {','.join(tags)}  [{label}]")
    print()
    print("II. 246 = 2(PR) × 3(ST_arch) × 41(→4=SA)")
    print(f"    DR={dr(246)} (ST arch)  mod37={246%37} (CB,PR,SEED_ORBIT)")
    print(f"    246/6={246//6}=41 (13th prime, lower of (41,43) twin pair)")
    print()
    print("III. GPY (1D) = stuttering: bound stalls, enters orbit at 18 but cannot resolve")
    print("IV.  Maynard (k-D simplex) = complete flow: resolves to 24 = orbit entry node")
    print()
    print("V. Heartbeat: 24→32→18→24")
    print(f"   4680 mod37=18 (orbit), 246 mod37=24 (orbit entry)")
    print(f"   Final prime gap bound = GF(37) seed = heartbeat entry")
    print()
    print("All assertions passed.")
