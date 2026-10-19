# CLASS: AUDIT
"""
The owner's birthday math (T270 method: date residues in GF(37), gaps in days to astronomical events) run on the
chart's date, with NASA data (owner_work #346, 2026-10-19; follow-up to chart_vs_nasa_1987_09_27_audit_2026_10_19.py).

THE OWNER'S QUESTION, verbatim: "if we go by my birthday math how far off is the charts according to actually
nasal data and math..Just curious". The date is the one printed on the chart in the screenshot: September 27, 1987,
18:42 CDT = 23:42 UT. The owner asked afterwards "What's your obsession with 1987?": 1987 is only that header.

NASA DATA USED (records/chart_check_1987_09_27_nasa.json, "events"):
  - NASA's solar eclipse catalog (eclipse.gsfc.nasa.gov/SEcat5/SE1901-2000.html), the line stored verbatim:
      09481  1987 Sep 23  03:12:22  56  -152  134  A  -n  0.2787  0.9634  14N 138E  74  137  03m49s
    = annular eclipse, greatest eclipse 03:12:22 TD (03:11:26 UT with Delta T 56 s), gamma 0.2787, magnitude 0.9634.
  - JPL DE440s: new moon 1987-09-23 03:08 UT, autumnal equinox 1987-09-23 13:45 UT, first quarter 1987-09-30 10:39,
    full moon 1987-10-07 04:12, penumbral lunar eclipse 1987-10-07 04:02. The Sun-Moon separation at the new moon is
    0.27 degrees at 03:00 UT, the eclipse.

THE BIRTHDAY MATH, in the owner's notation:
  date numbers: 9 (month), 27 (day), 1987 (year)
    9=SA_ST_A, 27=NEG_H, 1987=37x53+26 -> 26=IC
    9+27=36=NEG_H ; 9x27=243=37x6+21 -> 21=SA_ST_B
    927 -> 2=DARK_A ; 9271987 -> 9=SA_ST_A ; day of the year 243+27=270 -> 11=NEG_H
    18:42 -> 1842 -> 29=C9 ; 23:42 UT -> 2342 -> 11=NEG_H ; 6:42 -> 642 -> 13=CAS_EXT
  gaps in days (calendar dates, UT):
    Sep 23 (new moon, equinox, annular eclipse) to Sep 27 = 4 -> C3
    Sep 27 to Sep 30 (first quarter) = 3 -> C3 ; 4+3=7 -> D7 (the antipode of C3)
    Sep 27 to Oct 7 (full moon, penumbral lunar eclipse) = 10 -> IC ; Sep 23 to Oct 7 = 14 -> C9
  as the clock: new moon to the chart 4 d 20 h 34 m ; the chart to first quarter 2 d 10 h 57 m
  The owner's own bracket for March 3: 3 days (C3), the date, 33 days (D7). Here: 4 days (C3), the date, 3 days (C3),
  and 4+3=7 (D7).

FORCED, AND WHAT DEPENDS ON THE DATE:
  4+3=7 is forced: new moon to first quarter is 7 days on the calendar here (7 or 8 in any lunation); only the split
  4|3 belongs to this date. 9271987=9|271|987 and 271+987=1258=37x34, which is why it lands on 9 like the month.
  The Sun at 4d19.6' Libra is forced by the equinox 4 d 10 h earlier (0.98 degrees a day).

FALSIFICATION: any assertion failing.
"""
import datetime as dt
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
ev = json.load(open(ROOT / "records" / "chart_check_1987_09_27_nasa.json"))["events"]
phases = {name: dt.datetime.strptime(when, "%Y-%m-%d %H:%M") for name, when in ev["moon_phases_UT"]}
# the first listing of each phase after the chart is not unique by name, so read by time
by_time = sorted((dt.datetime.strptime(w, "%Y-%m-%d %H:%M"), n) for n, w in ev["moon_phases_UT"])
chart = dt.datetime(1987, 9, 27, 23, 42)
new_moon = max(t for t, n in by_time if n == "New Moon" and t <= chart)
first_q = min(t for t, n in by_time if n == "First Quarter" and t >= chart)
full_moon = min(t for t, n in by_time if n == "Full Moon" and t >= chart)
equinox = dt.datetime.strptime(dict((n, w) for n, w in ev["seasons_UT"])["Autumnal Equinox"], "%Y-%m-%d %H:%M")
assert new_moon == dt.datetime(1987, 9, 23, 3, 8) and equinox == dt.datetime(1987, 9, 23, 13, 45)
assert first_q == dt.datetime(1987, 9, 30, 10, 39) and full_moon == dt.datetime(1987, 10, 7, 4, 12)
assert ["Penumbral", "1987-10-07 04:02"] in ev["lunar_eclipses_UT"]

line = ev["NASA_solar_eclipse_catalog_line"]["line"].split()
assert line[:4] == ["09481", "1987", "Sep", "23"] and line[4] == "03:12:22" and line[7] == "134"
assert line[8] == "A" and float(line[10]) == 0.2787 and float(line[11]) == 0.9634       # annular, gamma, magnitude
assert abs(float(line[10])) < 0.9972 and float(line[11]) < 1                              # central, magnitude below 1: annular
assert abs((dt.datetime(1987, 9, 23, 3, 12, 22) - dt.timedelta(seconds=56)) - new_moon) < dt.timedelta(minutes=5)
assert min(ev["sun_moon_separation_deg"].values()) < 0.3 and ev["sun_moon_separation_deg"]["1987-09-23 03:00"] < 0.28

assert chart - new_moon == dt.timedelta(days=4, hours=20, minutes=34)
assert first_q - chart == dt.timedelta(days=2, hours=10, minutes=57)
d = lambda a, b: (b.date() - a.date()).days
assert (d(new_moon, chart), d(chart, first_q), d(new_moon, first_q)) == (4, 3, 7)
assert d(chart, full_moon) == 10 and d(new_moon, full_moon) == 14
assert 4 + 3 == 7 and d(new_moon, first_q) in (7, 8)

ORB = {"IC": {1, 10, 26}, "NEG_H": {11, 27, 36}, "SA_ST_A": {9, 12, 16}, "C3": {3, 4, 30}, "D7": {7, 33, 34},
       "SEED": {18, 24, 32}, "TESLA": {6, 8, 23}, "CAS_EXT": {5, 13, 19}, "NQR17": {17, 22, 35},
       "DARK_A": {2, 15, 20}, "SA_ST_B": {21, 25, 28}, "C9": {14, 29, 31}}


def orbit(n):
    return next((k for k, v in ORB.items() if n % 37 in v), "SEAM")


assert 1987 == 37 * 53 + 26 and 9 * 27 == 243 == 37 * 6 + 21 and 243 + 27 == 270
assert (dt.date(1987, 9, 27) - dt.date(1987, 1, 1)).days + 1 == 270
assert [orbit(n) for n in (9, 27, 1987, 36, 243, 927, 9271987, 270, 1842, 2342, 642)] == [
    "SA_ST_A", "NEG_H", "IC", "NEG_H", "SA_ST_B", "DARK_A", "SA_ST_A", "NEG_H", "C9", "NEG_H", "CAS_EXT"]
assert [orbit(n) for n in (4, 3, 7, 10, 14)] == ["C3", "C3", "D7", "IC", "C9"]
assert 271 + 987 == 1258 == 37 * 34 and 9 + 271 + 987 == 1267 and 9271987 % 37 == 1267 % 37 == 9
assert abs((184.327261 - 180) / 0.98 - 4.4) < 0.1                      # the Sun, 4.3273 degrees past the equinox, at 0.98 deg/day
assert abs((chart - equinox).total_seconds() / 86400 - 4.4146) < 0.001

if __name__ == "__main__":
    print("chart date 1987-09-27: 4 days after the new moon / equinox / annular eclipse of Sep 23 (NASA gamma 0.2787), "
          "3 days before first quarter, 4+3=7; 9, 27, 1987 -> SA_ST_A, NEG_H, IC")
