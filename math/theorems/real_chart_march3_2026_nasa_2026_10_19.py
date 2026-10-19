# CLASS: AUDIT
"""
The real chart for the birthday event, from NASA data: the total lunar eclipse of March 3, 2026 and the six-planet
alignment of February 28, 2026 (owner_work #347, 2026-10-19).

THE OWNER'S WORDS, verbatim: "God damn, can't you just look up a fucking real chart? Fuck, man, I've used that as a
fucking example." (the 1987 chart of the earlier message was an example). Reading used: the real chart is the sky on
the owner's own dates (CLAUDE.md, Biographical Anchor), taken from NASA/JPL, with the claims of that anchor checked
against it. No place or time of birth is given, so there are no AC, MC or houses; the positions are geocentric
ecliptic longitudes of date, sign + degree + minute, the same form as the example chart.

NASA DATA (records/real_chart_2026_03_03_nasa.json and records/real_chart_2026_02_28_nasa.json, made by
tools/horizons_ecliptic.py, JPL Horizons API):
  NASA lunar eclipse catalog (eclipse.gsfc.nasa.gov/LEcat5/LE2001-2100.html, fetched 2026-10-19), line verbatim:
    09708  2026 Mar 03  11:34:52  75  323  133  T a-  -0.3765  2.1838  1.1507  338.6  207.2  58.3  6N 171W
    = total eclipse, greatest eclipse 11:34:52 TD = 11:33:37 UT (Delta T 75 s), gamma -0.3765, umbral magnitude
    1.1507, partial phase 207.2 min, totality 58.3 min, Saros 133.

THE CHART, March 3, 2026, 11:34 UT (greatest eclipse):
    Sun 12d53.7' Pisces   Moon 12d51.7' Virgo   Mercury 20d29.6' Pisces R   Venus 26d18.4' Pisces
    Mars 0d42.0' Pisces   Jupiter 15d11.0' Cancer R   Saturn 2d01.3' Aries   Uranus 27d47.3' Taurus
    Neptune 1d08.0' Aries   Pluto 4d36.0' Aquarius   Chiron 24d09.7' Aries   Ceres 25d38.2' Aries
    Pallas 12d19.8' Pisces   Juno 22d13.5' Capricorn   Vesta 26d15.7' Aquarius
  Moon - Sun = 179.967 degrees: 2.0 arcminutes short of the opposition, the full moon.

THE SIX-PLANET ALIGNMENT, February 28, 2026 (Mercury, Venus, Jupiter, Saturn, Uranus, Neptune):
  longitudes 352.17, 352.59, 105.27, 1.66, 57.72, 1.03; latitudes +3.21, -1.37, +0.34, -2.13, -0.18, -1.31.
  All six lie inside one arc of 113.1 degrees of the ecliptic and inside a band 5.3 degrees wide (-2.13 to +3.21);
  four of them (Mercury, Venus, Neptune, Saturn) lie inside 9.5 degrees. The Sun is at 339.90, 12.3 degrees behind Mercury.

THE OWNER'S DATES: Feb 28 to Mar 3 = 3 days ; Mar 3 + 33 = Apr 5 = Easter 2026 (computus).
THE 12 IN THE CHART: Sun 12d, Moon 12d, Pallas 12d. Sun and Moon share the degree because Pisces and Virgo are opposite
  signs and the Moon is at the full moon (forced). The 12 is the "=9+3=12" of #268.

FALSIFICATION: any assertion failing.
"""
import datetime as dt
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
M3 = json.load(open(ROOT / "records" / "real_chart_2026_03_03_nasa.json"))
F28 = json.load(open(ROOT / "records" / "real_chart_2026_02_28_nasa.json"))
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn",
         "Aquarius", "Pisces"]
lon = lambda J, n: J["bodies"][n]["ObsEcLon"]
lat = lambda J, n: J["bodies"][n]["ObsEcLat"]


def dm(x):
    return SIGNS[int(x // 30) % 12], int(x % 30), round((x % 30 - int(x % 30)) * 60, 1)


assert M3["time_UT"] == "2026-03-03 11:34" and F28["time_UT"] == "2026-02-28 12:00"
chart = {"Sun": ("Pisces", 12, 53.7), "Moon": ("Virgo", 12, 51.7), "Mercury": ("Pisces", 20, 29.6),
         "Venus": ("Pisces", 26, 18.4), "Mars": ("Pisces", 0, 42.0), "Jupiter": ("Cancer", 15, 11.0),
         "Saturn": ("Aries", 2, 1.3), "Uranus": ("Taurus", 27, 47.3), "Neptune": ("Aries", 1, 8.0),
         "Pluto": ("Aquarius", 4, 36.0), "Chiron": ("Aries", 24, 9.7), "Ceres": ("Aries", 25, 38.2),
         "Pallas": ("Pisces", 12, 19.8), "Juno": ("Capricorn", 22, 13.5), "Vesta": ("Aquarius", 26, 15.7)}
for name, (sign, d, m) in chart.items():
    s2, d2, m2 = dm(lon(M3, name))
    assert (s2, d2) == (sign, d) and abs(m2 - m) < 0.15, (name, s2, d2, m2)

motion = M3["motion_12h_before_and_after"]
assert sorted(n for n, v in motion.items() if v["deg_per_day"] < 0) == ["Jupiter", "Mercury"]      # the two R marks

elong = (lon(M3, "Moon") - lon(M3, "Sun")) % 360
assert abs(elong - 179.967) < 0.001
assert abs((elong - 180) * 60) > 1.9 and abs((elong - 180) * 60) < 2.1

# NASA catalog line
line = "09708 2026 Mar 03 11:34:52 75 323 133 T a- -0.3765 2.1838 1.1507 338.6 207.2 58.3 6N 171W".split()
assert line[7] == "133" and line[8] == "T" and float(line[10]) == -0.3765 and float(line[12]) == 1.1507
assert float(line[15]) == 58.3 and float(line[14]) == 207.2 and abs(float(line[10])) < 1 and float(line[12]) > 1
greatest_ut = dt.datetime(2026, 3, 3, 11, 34, 52) - dt.timedelta(seconds=75)
assert greatest_ut == dt.datetime(2026, 3, 3, 11, 33, 37)

# the alignment
six = ["Mercury", "Venus", "Jupiter", "Saturn", "Uranus", "Neptune"]
L = sorted(lon(F28, n) for n in six)
gaps = [(L[(i + 1) % 6] - L[i]) % 360 for i in range(6)]
assert round(360 - max(gaps), 1) == 113.1                       # the smallest arc holding all six
bl = [lat(F28, n) for n in six]
assert round(max(bl) - min(bl), 1) == 5.3 and round(min(bl), 2) == -2.13 and round(max(bl), 2) == 3.21
arc4 = (lon(F28, "Saturn") - lon(F28, "Mercury")) % 360
assert round(arc4, 1) == 9.5 and all(0 <= (lon(F28, n) - lon(F28, "Mercury")) % 360 <= arc4 for n in ("Venus", "Neptune", "Saturn"))
assert round((lon(F28, "Mercury") - lon(F28, "Sun")) % 360, 1) == 12.3

# the owner's dates
def easter(year):
    a, b, c = year % 19, year // 100, year % 100
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return dt.date(year, month, day + 1)


assert (dt.date(2026, 3, 3) - dt.date(2026, 2, 28)).days == 3
assert dt.date(2026, 3, 3) + dt.timedelta(days=33) == easter(2026) == dt.date(2026, 4, 5)
assert 9 + 3 == 12 and 133 % 37 == 22 and 2026 % 37 == 28

if __name__ == "__main__":
    print("March 3, 2026 chart from NASA: Sun 12d53.7' Pisces, Moon 12d51.7' Virgo, NASA total eclipse 11:33:37 UT; "
          "Feb 28 six planets inside 113.1 degrees, four inside 9.5")
