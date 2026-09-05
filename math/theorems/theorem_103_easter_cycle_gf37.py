"""
================================================================================
THEOREM 103 — The Easter Cycle and the Saltus Lunae on GF(37)
================================================================================

STATEMENT.
The fundamental constants of the Easter computus — epact, intercalary
threshold, Metonic period, Callippic cycle — map onto named orbit classes
of GF(37) under the 137-map f(n) = (26 × n) mod 37. In particular:

  (1)  The annual epact (11 days) ≡ 11 (mod 37) ∈ ORBIT_11
  (2)  The intercalary threshold (30 days) ≡ 30 (mod 37) ∈ SA ∩ ST
         — the unique node in both the sovereign anchor and sovereign target sets
  (3)  The 19-year accumulated epact (209 days) ≡ 24 (mod 37) ∈ SEED_ORBIT ∩ CB
  (4)  The saltus lunae correction (+1 day) moves 209 → 210:
         24 ∈ SEED_ORBIT  →  25 ∈ SA
         The correction that synchronizes lunar and solar cycles is a
         SEED_ORBIT→SA transit in GF(37).
  (5)  The Metonic period: 19 ≡ 19 (mod 37) and 235 ≡ 13 (mod 37) share
         the same 137-map orbit {5, 13, 19}.
         "19 tropical years = 235 synodic months" is an equality between
         two elements of the same orbit.
  (6)  The solar year (365) ≡ 32 ∈ SEED_ORBIT;
       the lunar year (354) ≡ 21 ∈ ST.
       The solar–lunar gap is a SEED_ORBIT→ST split.
  (7)  The Callippic cycle (27,759 days) ≡ 9 ∈ SA, DR = 3 ∈ ST.
  (8)  12 lunar months per year: 12 ∈ ST.
  (9)  The paschal full moon range bounds: 21 March (day 21 ∈ ST),
       25 April (day 25 ∈ SA).

================================================================================
PROOF / DERIVATION
================================================================================

LEMMA 103.1  (Annual epact).
  The Easter cycle adds 11 days to the epact each year because the solar
  year (365 days) exceeds the lunar year (354 days) by exactly 11 days.
  11 ≡ 11 (mod 37) ∈ ORBIT_11.                                            ∎

LEMMA 103.2  (Intercalary threshold).
  When the epact reaches or exceeds 30, an intercalary month is inserted
  and 30 is subtracted from the epact. The threshold 30 ∈ SA ∩ ST:
    SA = {4, 9, 25, 30}  (sovereign anchors, all QR)
    ST = {3, 12, 21, 30} (sovereign targets, DR = 3 residues)
  30 is the only residue belonging to both sets.                            ∎

LEMMA 103.3  (19-year epact accumulation).
  Over 19 years the epact increases by 19 × 11 = 209 days.
  209 ≡ 24 (mod 37).
  Proof: 209 = 5 × 37 + 24.
  24 ∈ CB ∩ SEED_ORBIT ∩ PR.
  24 is the residue of the reference seed 246 mod 37, placing the
  accumulated calendar error directly in the seed orbit.                    ∎

LEMMA 103.4  (Saltus lunae — the leap of the moon).
  209 ≡ 29 (mod 30), not 0 (mod 30). The Metonic cycle requires a one-day
  correction (saltus lunae) so that the epact cycle repeats exactly.
  After correction: 210 = 209 + 1.
  210 ≡ 25 (mod 37).
  Proof: 210 = 5 × 37 + 25.
  25 ∈ SA.
  The saltus moves the 19-year epact sum from 24 ∈ SEED_ORBIT to 25 ∈ SA.
  The calendar synchronization is a SEED_ORBIT → SA transit.               ∎

LEMMA 103.5  (Metonic orbit unity).
  The Metonic cycle equates 19 tropical years with 235 synodic months.
    19  ≡ 19 (mod 37)
    235 ≡ 13 (mod 37)   [235 = 6 × 37 + 13]
  137-map orbit of 19:  19 × 26 = 494 ≡ 13;  13 × 26 = 338 ≡ 5;
                         5 × 26 = 130 ≡ 19.  Orbit = {5, 13, 19}.
  137-map orbit of 235 mod 37 = 13: same orbit {5, 13, 19}.
  The Metonic equality "19 years = 235 months" is an equality between
  two elements of the same 137-map orbit.
  Note: 13 ∈ CB (cascade base), 19 ∈ PR, 5 ∈ PR. DR(235) = 1 ∈ IC.      ∎

LEMMA 103.6  (Solar–lunar year gap).
  Solar year: 365 ≡ 32 (mod 37) ∈ SEED_ORBIT.  [365 = 9 × 37 + 32]
  Lunar year: 354 ≡ 21 (mod 37) ∈ ST.          [354 = 9 × 37 + 21]
  Their difference is 11 ∈ ORBIT_11 (the annual epact, Lemma 103.1).
  The solar year lives in the seed orbit; the lunar year lives in the
  sovereign target set. The gap between them is ORBIT_11.                   ∎

LEMMA 103.7  (Callippic cycle).
  The 76-year Callippic cycle (4 Metonic cycles) spans 27,759 days
  and 940 lunar months.
    27,759 ≡ 9 (mod 37).  [27,759 = 750 × 37 + 9]
    9 ∈ SA.  DR(27,759) = 3 ∈ ST.
    940 ≡ 15 (mod 37).    [940 = 25 × 37 + 15]
    15 ∈ PR.
  The day count of the most accurate pre-Gregorian cycle lands in SA.      ∎

LEMMA 103.8  (Paschal bounds).
  The paschal full moon always falls on a date between 21 March and
  18 April; Easter Sunday therefore falls between 22 March and 25 April.
    Day 21 (earliest full moon day): 21 ∈ ST.
    Day 25 (latest Easter day-of-month for April): 25 ∈ SA.
    Day 22 (earliest Easter day-of-month): 22 ∈ BASIN_Y.
    12 (months counted in the lunar year): 12 ∈ ST.                        ∎

================================================================================
MAIN THEOREM
================================================================================

THEOREM 103.  (Easter Cycle — GF(37) Classification).

  ┌──────────────────────────────────┬────────┬────────────────────────────┐
  │  Quantity                        │ mod 37 │  Named set           │
  ├──────────────────────────────────┼────────┼────────────────────────────┤
  │  Annual epact (11)               │  11    │  ORBIT_11                  │
  │  Intercalary threshold (30)      │  30    │  SA ∩ ST  (unique node)    │
  │  19-yr epact accumulation (209)  │  24    │  SEED_ORBIT ∩ CB ∩ PR      │
  │  After saltus correction (210)   │  25    │  SA                        │
  │  Metonic years (19)              │  19    │  orbit {5,13,19} ∈ PR      │
  │  Metonic months (235)            │  13    │  orbit {5,13,19} ∈ CB      │
  │  Solar year (365)                │  32    │  SEED_ORBIT                │
  │  Lunar year (354)                │  21    │  ST                        │
  │  Callippic days (27,759)         │   9    │  SA;  DR=3 ∈ ST            │
  │  Callippic months (940)          │  15    │  PR                        │
  │  12 lunar months                 │  12    │  ST                        │
  │  Paschal full moon start (Mar 21)│  21    │  ST                        │
  │  Easter latest (Apr 25)          │  25    │  SA                        │
  └──────────────────────────────────┴────────┴────────────────────────────┘

COROLLARY 103.9  (The saltus as synchronization transit).
  The saltus lunae — the single-day correction that makes the 19-year
  Metonic cycle exact — is algebraically a SEED_ORBIT → SA transit in GF(37):
      19 × 11 = 209  ≡  24 ∈ SEED_ORBIT   (pre-correction)
      209 + 1 = 210  ≡  25 ∈ SA            (post-correction)
  The correction that synchronizes the Moon to the Sun moves the cumulative
  epact out of GF(37)'s dark non-QR seed orbit and into the
  sovereign anchor set.

COROLLARY 103.10  (Metonic orbit unity).
  The two quantities equated by the Metonic discovery — 19 tropical years
  and 235 synodic months — satisfy
      19 ≡ 19 (mod 37)  and  235 ≡ 13 (mod 37),
  both in the 137-map orbit {5, 13, 19}.
  The fundamental astronomical commensurability is a relation between
  two elements of the same GF(37) three-cycle.
"""

P          = 37
IC         = frozenset({1, 10, 26})
SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
ORBIT_11   = frozenset({11, 27, 36})
SEED_ORBIT = frozenset({18, 24, 32})
BASIN_Y    = frozenset({17, 22, 35})
PR         = frozenset({2,5,13,15,17,18,19,20,22,24,32,35})


def dr(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


# ── Lemma 103.1 — Annual epact ────────────────────────────────────────────────
assert 365 - 354 == 11
assert 11 % P == 11 and 11 in ORBIT_11

# ── Lemma 103.2 — Intercalary threshold ──────────────────────────────────────
assert 30 in SA and 30 in ST
assert SA & ST == frozenset({30})   # 30 is the unique SA∩ST node

# ── Lemma 103.3 — 19-year epact accumulation ─────────────────────────────────
assert 19 * 11 == 209
assert 209 % P == 24
assert 24 in CB and 24 in SEED_ORBIT and 24 in PR

# ── Lemma 103.4 — Saltus lunae ───────────────────────────────────────────────
assert 209 % 30 == 29          # one short of cycle repeat
assert (209 + 1) % P == 25    # saltus correction
assert 25 in SA                # lands in sovereign anchor
assert 24 in SEED_ORBIT and 25 not in SEED_ORBIT   # SEED_ORBIT → SA transit

# ── Lemma 103.5 — Metonic orbit unity ────────────────────────────────────────
assert 19 % P == 19 and 235 % P == 13
# Both in orbit {5, 13, 19} under ×26
metonic_orbit = frozenset({5, 13, 19})
assert 19 in metonic_orbit and 13 in metonic_orbit
assert (19 * 26) % P == 13
assert (13 * 26) % P == 5
assert (5  * 26) % P == 19
assert dr(235) == 1 and 1 in IC

# ── Lemma 103.6 — Solar–lunar year gap ───────────────────────────────────────
assert 365 % P == 32 and 32 in SEED_ORBIT
assert 354 % P == 21 and 21 in ST
assert (365 - 354) % P == 11 and 11 in ORBIT_11

# ── Lemma 103.7 — Callippic cycle ────────────────────────────────────────────
CALLIPPIC_DAYS   = 27_759
CALLIPPIC_MONTHS = 940
assert CALLIPPIC_DAYS % P == 9 and 9 in SA
assert dr(CALLIPPIC_DAYS) == 3
assert 3 == dr(3)   # DR=3 is the characteristic of ST elements: 3,12,21,30
assert CALLIPPIC_MONTHS % P == 15 and 15 in PR

# ── Lemma 103.8 — Paschal bounds ─────────────────────────────────────────────
assert 21 in ST    # Mar 21 earliest paschal full moon
assert 25 in SA    # Apr 25 latest Easter day-of-month
assert 22 in BASIN_Y   # Mar 22 earliest possible Easter
assert 12 in ST    # 12 lunar months per year


if __name__ == "__main__":
    def fw(r):
        classes = []
        for name, s in [('IC',IC),('SA',SA),('ST',ST),('CB',CB),
                        ('ORBIT_11',ORBIT_11),('SEED_ORBIT',SEED_ORBIT),
                        ('BASIN_Y',BASIN_Y),('PR',PR)]:
            if r in s: classes.append(name)
        return classes or ['—']

    print("THEOREM 103 — Easter Cycle on GF(37)")
    print("=" * 60)
    rows = [
        ("Annual epact (11)",               11),
        ("Intercalary threshold (30)",       30),
        ("19-yr epact sum (209)",            209),
        ("After saltus (210)",              210),
        ("Metonic years (19)",               19),
        ("Metonic months (235)",            235),
        ("Solar year (365)",                365),
        ("Lunar year (354)",                354),
        ("Callippic days (27,759)",    27_759),
        ("Callippic months (940)",        940),
        ("12 lunar months",                  12),
        ("Paschal full moon start (21)",     21),
        ("Easter latest day-of-month (25)", 25),
    ]
    print(f"\n  {'Quantity':<38} {'mod37':>5}  {'DR':>3}  Classes")
    print("  " + "-" * 70)
    for label, val in rows:
        r = val % P
        print(f"  {label:<38} {r:>5}  {dr(val):>3}  {fw(r)}")

    print()
    print("  Saltus lunae: 209≡24∈SEED_ORBIT  →  210≡25∈SA")
    print("  Metonic orbit: 19≡19 and 235≡13, both in {5,13,19}")
    print("  Solar(365)≡32∈SEED_ORBIT,  Lunar(354)≡21∈ST,  gap=11∈ORBIT_11")
    print()
    print("All assertions pass.")
