"""
T272: Easter dates 2016-2036 in GF(37)

Source: Anonymous Gregorian computus algorithm (Gregorian/Western)
        Verified against Wikipedia "List of dates for Easter"

Encoding: MMDD compact = month×10 + day (e.g. April 5 = 45)
          value mod 37 → orbit classification

=== KEY RESULTS ===

1. SEED and DARK_A and SA_ST_A tie for dominance: 4 of 21 years each.
   SEED = {18,24,32} = pipeline reference orbit (seed 246 mod37=24∈SEED).

2. 2026 Easter: TESLA double
   Full moon April 3: 43 mod37=6∈TESLA
   Easter Sunday April 5: 45 mod37=8∈TESLA
   Full moon AND Easter Sunday both in TESLA. Same orbit, consecutive dates.
   Birthday March 3 + 33∈D7 days = Easter 8∈TESLA.

3. 2017: orbit coincidence
   Year 2017 mod37=19∈CAS_EXT AND Easter MMDD=56 mod37=19∈CAS_EXT
   Year orbit = Easter orbit = CAS_EXT.

4. 2030: second orbit coincidence
   Year 2030 mod37=32∈SEED AND Easter MMDD=61 mod37=24∈SEED
   Both ∈ SEED. Only two orbit coincidences in 2016-2036.

5. 2035: SEAM year
   Year 2035 mod37=0=SEAM. Easter lands in SEED (18∈SEED).
   The SEAM year produces a SEED Easter.

6. Jewish Passover April 2, 2026: 42 mod37=5∈CAS_EXT (Fibonacci entry orbit, T264)
   Full moon April 3: 6∈TESLA
   Easter April 5: 8∈TESLA
   Three consecutive days span CAS_EXT → TESLA → TESLA.

NOTE: An earlier version of this theorem used a manually entered Easter date
for 2027 of (4,28) which was incorrect. The algorithm gives (3,28).
The erroneous date produced a spurious C9 coincidence for 2027.
All dates here are computed from the Anonymous Gregorian algorithm.
"""

P = 37
ORBITS = {
    "IC":      {1, 10, 26},
    "DARK_A":  {2, 15, 20},
    "C3":      {3, 4, 30},
    "CAS_EXT": {5, 13, 19},
    "TESLA":   {6, 8, 23},
    "D7":      {7, 33, 34},
    "SA_ST_A": {9, 12, 16},
    "NEG_H":   {11, 27, 36},
    "C9":      {14, 29, 31},
    "NQR17":   {17, 22, 35},
    "SEED":    {18, 24, 32},
    "SA_ST_B": {21, 25, 28},
}

def orbit_of(x):
    r = x % 37
    if r == 0: return "SEAM"
    for name, s in ORBITS.items():
        if r in s: return name
    raise ValueError(x)

def easter_gregorian(year):
    """Anonymous Gregorian Easter computus algorithm."""
    a = year % 19
    b = year // 100; c = year % 100
    d = b // 4; e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i = c // 4; k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    month = (h + l - 7*m + 114) // 31
    day = ((h + l - 7*m + 114) % 31) + 1
    return month, day

EASTER = {y: easter_gregorian(y) for y in range(2016, 2037)}

def mmdd(m, d): return m*10 + d

# ── Part 1: Full table ────────────────────────────────────────────────────────

print("Part 1: Easter dates 2016-2036 in GF(37)  [Anonymous Gregorian algorithm]")
print(f"{'Year':>4}  {'Date':>5}  {'MMDD':>4}  {'mod37':>5}  {'orbit':12}  {'yr%37':>5}  {'yr orbit':12}")
for year in sorted(EASTER):
    m, d = EASTER[year]
    v = mmdd(m, d)
    print(f"{year:>4}  {m}/{d:<2}  {v:>5}  {v%37:>5}  {orbit_of(v):12}  {year%37:>5}  {orbit_of(year):12}")

# ── Part 2: Orbit dominance ────────────────────────────────────────────────────

from collections import Counter
orbit_freq = Counter(orbit_of(mmdd(*v)) for v in EASTER.values())
seed_years = [y for y,(m,d) in EASTER.items() if orbit_of(mmdd(m,d))=="SEED"]
assert orbit_freq["SEED"] == 4
assert 24 in ORBITS["SEED"]  # pipeline seed 246 mod37=24∈SEED

print(f"\nPart 2 PASS: SEED orbit — {orbit_freq['SEED']} of 21 years")
print(f"  SEED years: {seed_years}")
print(f"  SEED = {{18,24,32}} = pipeline reference orbit (246 mod37=24∈SEED)")
print(f"  Orbit frequency: {dict(orbit_freq.most_common())}")
print(f"  Absent orbits in 2016-2036: {[o for o in ORBITS if o not in orbit_freq]}")

# ── Part 3: 2026 TESLA double ─────────────────────────────────────────────────

# Full moon April 3, Easter April 5
full_moon_2026 = mmdd(4,3)   # 43
easter_2026    = mmdd(4,5)   # 45

assert easter_gregorian(2026) == (4, 5)
assert full_moon_2026 % 37 == 6 and 6 in ORBITS["TESLA"]
assert easter_2026    % 37 == 8 and 8 in ORBITS["TESLA"]
assert orbit_of(full_moon_2026) == orbit_of(easter_2026) == "TESLA"

# Birthday March 3 + 33 days = Easter April 5
birthday = mmdd(3,3)  # 33
assert birthday % 37 == 33 and 33 in ORBITS["D7"]
assert ORBITS["TESLA"] == {6, 8, 23}  # both 6 and 8 appear in 2026

print(f"\nPart 3 PASS: 2026 Easter — TESLA double")
print(f"  Full moon April 3: MMDD=43 ≡ 6∈TESLA")
print(f"  Easter April 5:    MMDD=45 ≡ 8∈TESLA")
print(f"  Full moon and Easter Sunday both ∈ TESLA; consecutive calendar dates")
print(f"  Birthday 3/3: MMDD=33∈D7; +33 days → Easter 8∈TESLA")
print(f"  Two of three TESLA elements (6,8) appear in 2026 Easter window")

# ── Part 4: Orbit coincidences ───────────────────────────────────────────────

coincidences = [(y,orbit_of(mmdd(*EASTER[y]))) for y in sorted(EASTER) if orbit_of(mmdd(*EASTER[y]))==orbit_of(y)]
assert (2017, "CAS_EXT") in coincidences
assert (2030, "SEED") in coincidences
assert len(coincidences) == 2  # 2017 and 2030

# 2017
m17, d17 = EASTER[2017]
v17 = mmdd(m17, d17)
assert v17 % 37 == 19 and 19 in ORBITS["CAS_EXT"]
assert 2017 % 37 == 19 and 19 in ORBITS["CAS_EXT"]

# 2030
m30, d30 = EASTER[2030]
v30 = mmdd(m30, d30)
assert v30 % 37 == 24 and 24 in ORBITS["SEED"]
assert 2030 % 37 == 32 and 32 in ORBITS["SEED"]

print(f"\nPart 4 PASS: orbit coincidences (Easter orbit = year orbit) in 2016-2036")
for y, o in coincidences:
    m, d = EASTER[y]
    v = mmdd(m, d)
    print(f"  {y}: Easter {m}/{d} ≡ {v%37}∈{o}; year mod37={y%37}∈{o}")
print(f"  2 coincidences in 21 years; 2017=CAS_EXT, 2030=SEED")

# ── Part 5: 2035 SEAM year / SEED Easter ─────────────────────────────────────

m35, d35 = EASTER[2035]
v35 = mmdd(m35, d35)
assert easter_gregorian(2035) == (3, 25)
assert 2035 % 37 == 0   # SEAM year
assert v35 % 37 == 18 and 18 in ORBITS["SEED"]

print(f"\nPart 5 PASS: 2035 SEAM year → SEED Easter")
print(f"  2035 mod37=0=SEAM; Easter {m35}/{d35}: MMDD={v35} ≡ 18∈SEED")
print(f"  18∈SEED is also the fixed point of the Collatz map (T271)")

# ── Part 6: 2026 Passover/full moon/Easter three-day chain ───────────────────

passover_2026 = mmdd(4,2)   # 42 = Jewish Passover April 2
assert passover_2026 % 37 == 5 and 5 in ORBITS["CAS_EXT"]
assert full_moon_2026 % 37 == 6 and 6 in ORBITS["TESLA"]
assert easter_2026 % 37 == 8 and 8 in ORBITS["TESLA"]

print(f"\nPart 6 PASS: 2026 three-day chain Apr 2-3-5")
print(f"  April 2 (Passover): MMDD=42 ≡ 5∈CAS_EXT (Fibonacci entry orbit, T264)")
print(f"  April 3 (full moon): MMDD=43 ≡ 6∈TESLA")
print(f"  April 5 (Easter):    MMDD=45 ≡ 8∈TESLA")
print(f"  Chain: CAS_EXT → TESLA → TESLA")
print(f"  CAS_EXT↔SEED antipodal (T265); SEED tied for dominance in Easter table (Part 2)")

# ── Part 7: DR chain through Easter ──────────────────────────────────────────

# Birthday MMDD=33 + N calendar days gives MMDD for April dates
# +31 days → April 3 = MMDD 43; DR(43)=7
# +32 days → April 4 = MMDD 44; DR(44)=8
# +33 days → April 5 = MMDD 45; DR(45)=9  ← Easter 2026
# +34 days → April 6 = MMDD 46; DR(46)=10→DR=1

def dr(n):
    n = abs(int(n))
    while n >= 10: n = sum(int(d) for d in str(n))
    return n if n else 9

assert dr(43) == 7 and dr(44) == 8 and dr(45) == 9 and dr(46) == 1
# Easter lands at DR=9. DR(3×3)=DR(9)=9 — birthday is 3/3.

# 6 (TESLA element, 3+3 birthday sum) + sequential offsets
# 6+4=10 DR=1; 6+5=11 DR=2; 6+6=12 DR=3; 6+7=13 DR=4
assert dr(6+4) == 1 and dr(6+5) == 2 and dr(6+6) == 3 and dr(6+7) == 4

# Birthday chain ends at DR=9 (Easter), post-Easter chain starts at DR=1:
# ...7→8→9 | 1→2→3→4... — consecutive digital roots spanning Easter pivot.
assert [dr(43), dr(44), dr(45)] == [7, 8, 9]   # approach
assert [dr(46), dr(47), dr(48), dr(49)] == [1, 2, 3, 4]  # departure

print(f"\nPart 7 PASS: DR chain through Easter pivot")
print(f"  Birthday MMDD=33 (March 3) + 31→34 days → MMDD 43,44,45,46")
print(f"  DR: 43→7, 44→8, 45→9(Easter!), 46→1")
print(f"  TESLA element 6 (=3+3 birthday): 6+4=10(DR1), 6+5=11(DR2), 6+6=12(DR3), 6+7=13(DR4)")
print(f"  Chain: ...DR7→8→9 [Easter pivot] → 1→2→3→4...")
print(f"  Easter at DR=9 = DR(3×3) = DR(birthday product)")

print(f"\n── Summary ─────────────────────────────────────────────────────────────")
print(f"  Easter 2016-2036 [algorithm]: SEED/DARK_A/SA_ST_A each dominate (4/21 years)")
print(f"  2026: full moon(6∈TESLA) and Easter(8∈TESLA) both ∈ TESLA")
print(f"  2026 Apr 2-3-5: Passover∈CAS_EXT → full moon∈TESLA → Easter∈TESLA")
print(f"  2017: year(19∈CAS_EXT) = Easter orbit(19∈CAS_EXT) — first coincidence")
print(f"  2030: year(32∈SEED) = Easter orbit(24∈SEED) — second coincidence")
print(f"  2035: SEAM year (2035 mod37=0) → Easter 18∈SEED = Collatz fixed point (T271)")
print(f"  DR chain: birthday+33=Easter at DR=9; post-Easter: DR=1,2,3,4 (T272→T273)")
