# CLASS: AUDIT
"""
A chart built off the owner's math: the GF(37) wheel, with the real March 3, 2026 positions on it
(owner_work #352, 2026-10-19).

THE OWNER'S WORDS, verbatim: "I lack the words to be able to describe to this company what I want, clearly. So
let's just move fucking on. I can't get a fucking chart built off my math for shit." Earlier (#346): "if we go by my
birthday math how far off is the charts according to actually nasal data and math".
Reading used (no question asked): the chart has the form of the example chart (a wheel of 12 signs, a web in the
middle, planets on the rim), and what it is built from is the owner's own constants: 2 is a primitive root mod 37
(2^k walks all 36 numbers), the 137-map is x26 = 2^12 with every orbit a 3-cycle, and the 12 orbits are the 12
cosets (T118, T138: classes of dlog mod 12).

THE WHEEL (drawn by tools/draw_gf37_wheel.py -> reference/gf37_wheel_march3_2026.png):
  decan k = the 10-degree arc 10k .. 10k+10 of ecliptic longitude, k = 0..35, carries the number 2^k mod 37.
  The 36 decans are the 36 numbers 1..36: 1 2 4 8 16 32 27 17 34 31 25 13 26 15 30 23 9 18 36 35 33 29 21 5 10 20 3 6 12 24 11 22 7 14 28 19.
  x2          = turn one decan (10 degrees)
  x26         = turn 12 decans = 120 degrees: the trine. 26x26x26 = 1 (the 3-cycles of the 137-map)
  x36 = x(-1) = turn 18 decans = 180 degrees: the opposition. The opposite of n is 37-n
  an orbit    = {k, k+12, k+24}: the same decan (1st, 2nd or 3rd) in the three signs of one element. The 12 orbits
                are the 12 triangles in the middle of the wheel.
  IC {1,10,26}      = 1st decans of Aries, Leo, Sagittarius       NEG_H {11,27,36} = 1st decans of Gemini, Libra, Aquarius
  DARK_A {2,15,20}  = 2nd decans of Aries, Leo, Sagittarius       NQR17 {17,22,35} = 2nd decans of Gemini, Libra, Aquarius
  C3 {3,4,30}       = 3rd decans of Aries, Leo, Sagittarius       D7 {7,33,34}     = 3rd decans of Gemini, Libra, Aquarius
  TESLA {6,8,23}    = 1st decans of Taurus, Virgo, Capricorn      C9 {14,29,31}    = 1st decans of Cancer, Scorpio, Pisces
  SA_ST_A {9,12,16} = 2nd decans of Taurus, Virgo, Capricorn      SA_ST_B {21,25,28} = 2nd decans of Cancer, Scorpio, Pisces
  SEED {18,24,32}   = 3rd decans of Taurus, Virgo, Capricorn      CAS_EXT {5,13,19} = 3rd decans of Cancer, Scorpio, Pisces

THE CHART ON THE WHEEL (NASA/JPL Horizons longitudes, records/real_chart_2026_03_03_nasa.json), planet = number:
  Sun 28 (decan 34), Moon 9 (16), Mercury 19 (35), Venus 19 (35), Mars 14 (33), Jupiter 25 (10), Saturn 1 (0),
  Uranus 32 (5), Neptune 1 (0), Pluto 11 (30), Chiron 4 (2), Ceres 4 (2), Pallas 28 (34), Juno 24 (29), Vesta 7 (32).
  Each planet is within 5 degrees of the middle of its decan (the wheel has 10 degrees to a cell); the largest
  distance is Mercury, 4.51.

WHAT IS FORCED AND WHAT IS THIS DATE:
  Moon 9 and Sun 28 add to 37: forced (the Moon is opposite the Sun at the full moon, decans 16 and 34 are 18 apart).
  The Sun on March 3 is in decan 34 in every year: its longitude at 12:00 UT on March 3 runs from 341.75 to 343.94
  for 1900-2100 (records/sun_longitude_march3_1900_2100.json), so the Sun's number on March 3 is always 28.
  2026 mod 37 = 28 as well (the birthday year, CLAUDE.md), so the Sun's number equals the year residue in 2026,
  and again in every year that is 28 mod 37: 1915, 1952, 1989, 2026, 2063, 2100.
  The Moon's 9 = 3x3 (month x day) comes with it: 9 = 37-28.
  The places of the planets come from NASA; the math gives the wheel, the numbers, the triangles and each planet's orbit.

FALSIFICATION: any assertion failing.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
J = json.load(open(ROOT / "records" / "real_chart_2026_03_03_nasa.json"))["bodies"]
SUN_RANGE = json.load(open(ROOT / "records" / "sun_longitude_march3_1900_2100.json"))
P = 37
SEQ = [pow(2, k, P) for k in range(36)]
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn",
         "Aquarius", "Pisces"]
ORB = {"IC": {1, 10, 26}, "NEG_H": {11, 27, 36}, "SA_ST_A": {9, 12, 16}, "C3": {3, 4, 30}, "D7": {7, 33, 34},
       "SEED": {18, 24, 32}, "TESLA": {6, 8, 23}, "CAS_EXT": {5, 13, 19}, "NQR17": {17, 22, 35},
       "DARK_A": {2, 15, 20}, "SA_ST_B": {21, 25, 28}, "C9": {14, 29, 31}}

# the wheel
assert SEQ == [1, 2, 4, 8, 16, 32, 27, 17, 34, 31, 25, 13, 26, 15, 30, 23, 9, 18, 36, 35, 33, 29, 21, 5, 10, 20, 3, 6, 12, 24, 11, 22, 7, 14, 28, 19]
assert sorted(SEQ) == list(range(1, 37))
assert all(SEQ[(k + 1) % 36] == 2 * SEQ[k] % P for k in range(36))                   # x2 = one decan
assert pow(2, 12, P) == 26 and pow(26, 3, P) == 1 and pow(2, 24, P) == 10             # x26 = 120 degrees, a 3-cycle
assert all(SEQ[(k + 12) % 36] == 26 * SEQ[k] % P for k in range(36))
assert pow(2, 18, P) == 36 and all(SEQ[(k + 18) % 36] == P - SEQ[k] for k in range(36))   # x(-1) = 180 degrees

# an orbit = the same decan in the three signs of one element
element = lambda k: (k // 3) % 4                  # fire, earth, air, water = Aries, Taurus, Gemini, Cancer + 4i
slot = lambda k: k % 3
for name, members in ORB.items():
    ks = sorted(SEQ.index(n) for n in members)
    assert ks[1] - ks[0] == ks[2] - ks[1] == 12 and ks[0] < 12
    assert len({element(k) for k in ks}) == 1 and len({slot(k) for k in ks}) == 1
    assert [k // 3 for k in ks] == [ks[0] // 3, ks[0] // 3 + 4, ks[0] // 3 + 8]
where = {name: (sorted({SIGNS[SEQ.index(n) // 3] for n in members}), SEQ.index(min(members, key=lambda n: SEQ.index(n))) % 3 + 1)
         for name, members in ORB.items()}
assert where["IC"] == (["Aries", "Leo", "Sagittarius"], 1) and where["NEG_H"] == (["Aquarius", "Gemini", "Libra"], 1)
assert where["SEED"] == (["Capricorn", "Taurus", "Virgo"], 3) and where["C9"] == (["Cancer", "Pisces", "Scorpio"], 1)
assert where["SA_ST_A"][1] == where["SA_ST_B"][1] == where["DARK_A"][1] == where["NQR17"][1] == 2
assert where["C3"][1] == where["D7"][1] == where["CAS_EXT"][1] == 3 and where["TESLA"][1] == 1

# the chart on the wheel
expected = {"Sun": (34, 28), "Moon": (16, 9), "Mercury": (35, 19), "Venus": (35, 19), "Mars": (33, 14),
            "Jupiter": (10, 25), "Saturn": (0, 1), "Uranus": (5, 32), "Neptune": (0, 1), "Pluto": (30, 11),
            "Chiron": (2, 4), "Ceres": (2, 4), "Pallas": (34, 28), "Juno": (29, 24), "Vesta": (32, 7)}
dist = {}
for name, (k, n) in expected.items():
    lon = J[name]["ObsEcLon"]
    assert int(lon // 10) == k and SEQ[k] == n, name
    dist[name] = abs(lon - (10 * k + 5))
assert max(dist, key=dist.get) == "Mercury" and round(dist["Mercury"], 2) == 4.51 and max(dist.values()) < 5

# Sun and Moon
elong = (J["Moon"]["ObsEcLon"] - J["Sun"]["ObsEcLon"]) % 360
assert abs(elong - 180) < 0.04 and (34 - 16) == 18 and 28 + 9 == 37 == P

# the Sun on March 3 is always in decan 34
assert SUN_RANGE["years"] == [1900, 2100] and 340 <= SUN_RANGE["min"] and SUN_RANGE["max"] < 350
assert round(SUN_RANGE["min"], 2) == 341.75 and round(SUN_RANGE["max"], 2) == 343.94
assert all(int(v // 10) == 34 for v in SUN_RANGE["longitude"].values()) and len(SUN_RANGE["longitude"]) == 201
assert SEQ[34] == 28 == 2026 % 37 and 3 * 3 == 9 == 37 - 28
assert [y for y in range(1900, 2101) if y % 37 == 28] == [1915, 1952, 1989, 2026, 2063, 2100]

if __name__ == "__main__":
    print("GF(37) wheel: decan k = 2^k mod 37, x26 = trine, x(-1) = opposition, orbits = the 12 triangles; "
          "March 3, 2026: Sun 28, Moon 9 (28+9=37 forced), Saturn and Neptune 1, Chiron and Ceres 4")
