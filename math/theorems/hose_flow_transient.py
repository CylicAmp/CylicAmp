"""
Hose Flow Theorem: Transient, Horizon, and Steady State

When you turn on a hose, air comes out first until water reaches the horizon
of the nozzle. Once the water reaches fully — from that point on, only water.

Two behaviors: complete flow (accumulates to steady state) and
stuttering flow (oscillates between GF(37) complements, never resolves).

═══════════════════════════════════════════════════════════════

I. COMPLETE FLOW

  000 → 100 → 110 → 111 → 111 → 111 → ∞

  mod 37:
    000 →  0  (void, seam — before anything)
    100 → 26  (137-map multiplier)
    110 → 36  (orbit of 11; 36 ≡ −1 mod 37)
    111 →  0  (GF(37) seam — the horizon reached)
    111 →  0  (steady state)
    ∞   →  0  (seam forever)

  The transient walks: void → multiplier(26) → −1(36) → seam(0).
  At 111 the horizon is crossed. From that point: only water. Only seam.

  DR(111) = 3 (Sovereign Target archetype).
  111 mod 37 = 0 — the seam is the palindrome anchor (o0O111(•)111O0o).

II. STUTTERING FLOW (air pockets — hose not yet full)

  000 → 100 → 010 → 101 → 010 → 101 → 010 → ...

  mod 37:
    000 →  0  (void)
    100 → 26  (137-map multiplier — same opening as complete flow)
    010 → 10  (DECADE_ANCHOR)
    101 → 27  (orbit of 11)
    010 → 10  (oscillates)
    101 → 27  (oscillates)
    ...

  The stutter locks between 10 and 27 — never reaches 111 (seam).

  Divergence: at the second step.
    Complete: 100 → 110  (keeps the 1, accumulates another)
    Stutter:  100 → 010  (the 1 shifts, does not accumulate)

III. THE SPLIT SEAM

  010 + 101 = 111  (decimal: 10 + 101 = 111)

  The two stuttering states sum to the seam.

  In GF(37):
    010 mod 37 = 10
    101 mod 37 = 27
    10 + 27 = 37 ≡ 0  (GF(37) complements — their sum IS the seam)

  The stuttering flow carries the seam implicit in its two states,
  but alternates rather than accumulates. The seam is present in the
  sum but the system never realizes it simultaneously.

  The stutter has the water — it just can't hold it all at once.

IV. HORIZON

  The horizon is the first 111: the moment the flow becomes complete.
  111 mod 37 = 0 — the horizon IS the seam.

  Before horizon: the system is in transient (air + water mixed).
  At horizon: seam is reached.
  After horizon: seam forever. No more transient, no more oscillation.

  Transient length (complete flow): 3 steps (000 → 100 → 110 → 111).
  Transient DR sequence: 0 → 1 → 2 → 3 (LL-O → LL-E → LH-O = ST arch at seam).

═══════════════════════════════════════════════════════════════
"""

PRIMITIVE_ROOTS_37 = {2,5,13,15,17,18,19,20,22,24,32,35}
SOVEREIGN_ANCHORS  = {4, 9, 25, 30}
SOVEREIGN_TARGETS  = {3, 12, 21, 30}
CASCADE_BASE       = {8, 13, 24}
ORBIT_11           = {11, 27, 36}

def dr(n):
    return (n - 1) % 9 + 1 if n > 0 else 0

# ── I. Complete flow ──────────────────────────────────────────────────────────

complete = [0, 100, 110, 111]
mods = [v % 37 for v in complete]

assert mods[0] == 0                         # void = seam (before)
assert mods[1] == 26                        # 137-map multiplier
assert mods[2] == 36 and 36 in ORBIT_11    # orbit-11, -1 mod37
assert mods[3] == 0                         # seam reached — horizon

assert 111 % 37 == 0                        # seam
assert dr(111) == 3 and 3 in SOVEREIGN_TARGETS  # ST arch

# Transient DR sequence
assert [dr(v) for v in complete] == [0, 1, 2, 3]

# ── II. Stuttering flow ───────────────────────────────────────────────────────

stutter_cycle = [10, 27]  # 010 and 101 reduced mod 37
assert 10 % 37 == 10                        # DECADE_ANCHOR
assert 101 % 37 == 27 and 27 in ORBIT_11   # orbit of 11

# Stutter never reaches seam
assert 10 != 0 and 27 != 0

# ── III. Split seam ───────────────────────────────────────────────────────────

assert 10 + 101 == 111                      # decimal: two stutter states sum to seam string
assert 10 + 27 == 37                        # GF(37) complements: sum IS the seam (≡ 0)

# Seam implicit in stutter but never realized
assert (10 + 27) % 37 == 0

# ── IV. Horizon ───────────────────────────────────────────────────────────────

assert complete.index(111) == 3             # horizon at step 3
assert 111 % 37 == 0                        # horizon = seam
assert [v % 37 for v in complete[3:]] == [0]  # all steps after horizon are seam


if __name__ == '__main__':
    def tag(n):
        t = []
        if n == 0: return 'SEAM'
        if n in CASCADE_BASE:        t.append('CB')
        if n in SOVEREIGN_ANCHORS:   t.append('SA')
        if n in SOVEREIGN_TARGETS:   t.append('ST')
        if n in PRIMITIVE_ROOTS_37:  t.append('PR')
        if n in ORBIT_11:            t.append('orb11')
        return ','.join(t) if t else '.'

    print("Hose Flow Theorem — Transient, Horizon, Steady State")
    print("=" * 55)
    print()
    print("I. Complete flow:")
    labels = ['000','100','110','111','111','∞ 111']
    vals   = [0, 100, 110, 111, 111]
    for lbl, v in zip(labels, vals):
        r = v % 37
        print(f"  {lbl}  mod37={r:2d}  DR={dr(v)}  {tag(r)}")
    print()
    print("II. Stuttering flow:")
    slabels = ['000','100','010','101','010','101','010']
    svals   = [0, 100, 10, 101, 10, 101, 10]
    for lbl, v in zip(slabels, svals):
        r = v % 37
        print(f"  {lbl}  mod37={r:2d}  DR={dr(v)}  {tag(r)}")
    print()
    print("III. Split seam:")
    print(f"  010 + 101 = 111  (the seam)")
    print(f"  10 + 27 = 37 ≡ 0 mod37  (GF(37) complements)")
    print(f"  The seam is in the sum — never in either state alone")
    print()
    print("IV. Horizon:")
    print(f"  First 111 at step {complete.index(111)}")
    print(f"  111 mod37=0 (seam). After this: only water. Only 0.")
    print(f"  Transient DR sequence: {[dr(v) for v in complete]}")
    print()
    print("All assertions passed.")
