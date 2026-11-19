# CLASS: AUDIT
"""
The pasted lunar block (2026-11-19): the Full Moon and total eclipse of 2026-03-03, the Full Moon of 2026-04-02,
the Moon on Apr 3 and on Easter Apr 5, the sequence 3 -> 3 -> 4/3 -> 4/5 -> 33/43/432, a mean-elongation formula,
and the 33, 43, 432-day points. Audit on arrival.

SOURCES (fetched 2026-11-19; values hardcoded below with their URLs):
  USNO moon phases API        https://aa.usno.navy.mil/api/moon/phases/date?date=2026-01-15&nump=16  (and 2027-04-01)
  NASA phase table            https://eclipse.gsfc.nasa.gov/phase/phases2001.html  (same minutes as USNO)
  NASA eclipse plot + catalog https://eclipse.gsfc.nasa.gov/LEplot/LEplot2001/LE2026Mar03T.pdf ,
                              https://eclipse.gsfc.nasa.gov/LEcat5/LE2001-2100.html
  JPL Horizons (DE441)        https://ssd.jpl.nasa.gov/api/horizons.api  Moon 301 / Sun 10, geocentric 500@399,
                              quantities 10, 20, 23, 24, 31
  Independent computation     math/theorems/meeus_lunar.py (Meeus, Astronomical Algorithms, ch. 47-49), checked here
                              against Meeus's worked examples and against every Horizons row.

RIGHT:
  Full Moon 2026-03-03 11:38 UTC (Horizons 11:37:54) with a total lunar eclipse; totality 58 m 19 s (U2 11:04:26,
  U3 12:02:45 UT); age 13.98 d after the New Moon of Feb 17 12:01; Moon-Sun longitude difference 180.000 there.
  Full Moon 2026-04-02 02:12 UTC (21:12 on Apr 1 at UTC-5); age 14.03 d after the New Moon of Mar 19 01:23.
  Full to Full 29.607 d = 29 d 14 h 34 m: one lunation, 1 h 50 m longer than the mean 29.530589 d.
  Apr 3 and Apr 5: waning gibbous, west of the Sun. Easter 2026 = Apr 5; Apr 5 is about 3 days after the Full Moon.
  33 - 29.530588 = 3.47;  43 / 29.530588 = 1.46;  432 / 29.530588 = 14.63;  360 + 72 = 432;  432 / 365.2422 = 1.18.
  Age 17.44 d at Apr 5 12:00 and 360 x 17.442 / 29.530588 = 212.63 (the arithmetic).

WRONG (each changes a number):
  1. Greatest eclipse is 11:33:37 UT (NASA; Horizons 11:33:43 UTC). 11:38 is the Full Moon instant, a different one.
  2. The Apr 3 values (169 W, 99 %, phase angle 11) and the Apr 5 values (147 W, 92 %, 33 from opposition) are the
     00:00 UTC values. At 12:00 UTC: Apr 3 163.3, 97.9 %, 16.6;  Apr 5 141.2, 89.0 %, 38.7.
  3. "Mean 212-213 at Apr 5 midday matches the 33 phase angle": the 33 is the true value at 00:00. At 12:00 the
     Moon-Sun longitude difference is 218.53, so 38.5 past opposition (the straight-line count gives 212.63).
  4. 432 days is not a near whole number of lunations: 14.63 (14 -> 413.43 d, 15 -> 442.96 d). 432 days after the
     Mar 3 Full Moon (2027-05-09) the Moon is a 12 % waxing crescent, 3.03 d after the New Moon of 2027-05-06.
  5. The 33, 43, 432-day points from the Mar 3 opposition are not at clean places in the cycle:
       true  38.4, 153.1, 220.5 past opposition   (fractions 0.107, 0.425, 0.613)
       mean  42.3, 164.2, 226.4                   (fractions 0.117, 0.456, 0.629)
     None is at New, Quarter or Full. 43 d is 2 days before the New Moon of Apr 17 (45.01 d after Mar 3).
     33 days after the opposition (Apr 5 11:38 UTC) the Moon is 38.4 past opposition, not 33.
  6. Easter is fixed by the tabular (ecclesiastical) Paschal Full Moon, not the astronomical maximum. In 2026 both
     fall on Thu Apr 2 (golden number 13, epact 11), so Apr 5 is right.
  7. The formula 360 (t - t_New) / 29.530588 gives 170.47 at the Mar 3 Full (true 180.00) and 171.08 at the Apr 2 Full:
     this lunation ran fast (perigee 2026-03-22 11:40 UTC, 366857 km), so the straight line lags the Moon by 6-10.

Two wording points from the skeptics, no number changed: "exactly one synodic month" is right as one lunation; the
anchor "age 14.0 d -> 180" is right as two measured values (it is not produced by the paste's formula).

FALSIFICATION: any assertion failing.
"""
import importlib.util
import math
import pathlib
from datetime import date, timedelta

HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("meeus_lunar", HERE / "meeus_lunar.py")
ML = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ML)

P = 29.530588                         # the paste's mean synodic month
P_MEAN = 29.530588853                 # Meeus / Chapront mean synodic month


def jd(s):
    """'YYYY-MM-DD hh:mm[:ss]' UTC -> JD"""
    d, t = s.split()
    y, mo, dd = (int(v) for v in d.split("-"))
    parts = [float(v) for v in t.split(":")] + [0.0]
    return ML.jd_from_cal(y, mo, dd + (parts[0] + parts[1] / 60 + parts[2] / 3600) / 24)


# ---- the engine reproduces Meeus's own worked examples
assert abs(ML.moon_phase(-283)["jde"] - 2443192.65118) < 1e-5                      # Example 49.a
m = ML.moon_position(2448724.5)                                                    # Example 47.a
assert abs(m["lam"] - 133.162655) < 1e-6 and abs(m["beta"] + 3.229126) < 1e-6 and abs(m["dist_km"] - 368409.7) < 0.1

# ---- phase instants: USNO minutes, Horizons seconds, Meeus
PHASES = {   # name: (USNO UTC, Horizons UTC, Meeus k)
    "new 02-17": ("2026-02-17 12:01", "2026-02-17 12:01:09.0", 323.0),
    "full 03-03": ("2026-03-03 11:38", "2026-03-03 11:37:53.7", 323.5),
    "new 03-19": ("2026-03-19 01:23", "2026-03-19 01:23:28.7", 324.0),
    "full 04-02": ("2026-04-02 02:12", "2026-04-02 02:11:57.9", 324.5),
    "new 04-17": ("2026-04-17 11:52", "2026-04-17 11:51:48.2", 325.0),
    "new 2027-05-06": ("2027-05-06 10:58", None, 338.0),
}
for name, (usno, hor, k) in PHASES.items():
    meeus_ut = ML.td_to_ut(ML.moon_phase(k)["jde"])
    assert abs(meeus_ut - jd(usno)) * 1440 < 1.0, name                     # within a minute of USNO
    if hor:
        assert abs(meeus_ut - jd(hor)) * 86400 < 20, name                  # within 20 s of Horizons
        assert abs(jd(hor) - jd(usno)) * 86400 < 60, name

full1, full2 = jd(PHASES["full 03-03"][1]), jd(PHASES["full 04-02"][1])
new1, new2 = jd(PHASES["new 02-17"][1]), jd(PHASES["new 03-19"][1])
age_mar3, age_apr2 = full1 - new1, full2 - new2
assert round(age_mar3, 3) == 13.984 and round(age_apr2, 3) == 14.034
lun = full2 - full1
assert round(lun, 3) == 29.607 and round(lun * 24 - 29 * 24, 2) == 14.57                    # 29 d 14 h 34 m
assert round((lun - P_MEAN) * 1440) == 110                                                    # 1 h 50 m over the mean
assert round(P_MEAN / 2, 3) == 14.765                                                         # the 14.7 end of the ranges
assert (jd("2026-04-02 02:12") - 5 / 24) < jd("2026-04-02 00:00")                             # Apr 1 at UTC-5

# ---- the eclipse (NASA plot and catalog)
U2, U3 = jd("2026-03-03 11:04:26"), jd("2026-03-03 12:02:45")
assert round((U3 - U2) * 86400) == 58 * 60 + 19
GREATEST_UT = jd("2026-03-03 11:33:37")                       # NASA (TD 11:34:52.1, predicted dT 75 s)
GREATEST_HOR = jd("2026-03-03 11:33:42.9")                    # Horizons, TT 11:34:52.1
assert abs(GREATEST_HOR - GREATEST_UT) * 86400 < 7                       # the 6 s is dT 75 s vs 69.18 s
assert round((full1 - GREATEST_HOR) * 1440, 1) == 4.2                    # Full Moon 4.2 min after greatest eclipse

# ---- Horizons rows: UTC -> (Lm - Ls, S-O-T elongation, phase angle, illuminated %)
HOR = {
    "2026-03-03 11:38": (180.0008923, 179.6385, 0.3606, 99.99901),
    "2026-04-02 02:12": (180.0002703, 177.1210, 2.8714, 99.93722),
    "2026-04-03 00:00": (190.4692076, 168.9123, 11.0587, 99.07243),
    "2026-04-03 12:00": (196.1656930, 163.3494, 16.6073, 97.91563),
    "2026-04-05 00:00": (212.9960024, 146.6895, 33.2264, 91.82784),
    "2026-04-05 11:38": (218.3614622, 141.3634, 38.5406, 89.11069),
    "2026-04-05 12:00": (218.5300749, 141.1960, 38.7077, 89.01970),
    "2026-04-05 18:00": (221.2851832, 138.4604, 41.4375, 87.48630),
    "2026-04-15 11:38": (333.0644900, 26.9911, 152.9440, 5.46986),
    "2027-05-09 11:38": (40.5437646, 40.6786, 139.2307, 12.13512),
}
for t, (dlon, elong, phase, illum) in HOR.items():
    q = ML.phase_quantities(ML.ut_to_td(jd(t)))
    assert abs(q["dlon"] - dlon) < 0.03 and abs(q["psi"] - elong) < 0.03, t        # Meeus vs Horizons
    assert abs(q["i"] - phase) < 0.03 and abs(100 * q["k"] - illum) < 0.05, t

# 2: the paste's Apr 3 / Apr 5 numbers are the 00:00 UTC values
assert [round(v) for v in HOR["2026-04-03 00:00"][1:]] == [169, 11, 99]
assert [round(v) for v in HOR["2026-04-05 00:00"][1:]] == [147, 33, 92]
assert [round(v, 1) for v in HOR["2026-04-03 12:00"][1:]] == [163.3, 16.6, 97.9]
assert [round(v, 1) for v in HOR["2026-04-05 12:00"][1:]] == [141.2, 38.7, 89.0]

# 3: the midday "match"
age_apr5_noon = jd("2026-04-05 12:00") - new2
assert round(age_apr5_noon, 2) == 17.44 and round(360 * age_apr5_noon / P, 2) == 212.63
assert round(HOR["2026-04-05 12:00"][0] - 180, 1) == 38.5 and round(HOR["2026-04-05 00:00"][0], 1) == 213.0

# 7: the straight-line formula against the Moon
assert round(360 * age_mar3 / P, 2) == 170.47 and round(360 * age_apr2 / P, 2) == 171.08
PERIGEE = ("2026-03-22 11:39:57", 366857.178)                  # Horizons distance minimum
assert jd(PHASES["new 03-19"][1]) < jd(PERIGEE[0]) < full2

# 4 and 5: the 33, 43, 432-day points
assert round(33 - P, 2) == 3.47 and round(43 / P, 2) == 1.46 and round(1.5 * P, 2) == 44.30
assert round(432 / P, 2) == 14.63 and 360 + 72 == 432 and round(432 / 365.2422, 2) == 1.18
assert (round(14 * P, 2), round(15 * P, 2)) == (413.43, 442.96)
mean_pts = {d: (d / P) % 1 for d in (33, 43, 432)}
assert {d: round(f, 3) for d, f in mean_pts.items()} == {33: 0.117, 43: 0.456, 432: 0.629}
assert {d: round(360 * f, 1) for d, f in mean_pts.items()} == {33: 42.3, 43: 164.2, 432: 226.4}
assert all(abs(full1 + d - jd(t)) * 86400 < 0.01 for d, t in ((33, "2026-04-05 11:37:53.7"), (43, "2026-04-15 11:37:53.7")))
true_pts = {33: HOR["2026-04-05 11:38"][0], 43: HOR["2026-04-15 11:38"][0], 432: HOR["2027-05-09 11:38"][0]}
past = {d: round((v - 180) % 360, 1) for d, v in true_pts.items()}
assert past == {33: 38.4, 43: 153.1, 432: 220.5}
assert all(min(abs(p - c) for c in (0, 90, 180, 270, 360)) > 15 for p in past.values())     # none at a principal phase
assert date(2026, 3, 3) + timedelta(days=33) == date(2026, 4, 5) and date(2026, 3, 3) + timedelta(days=432) == date(2027, 5, 9)
assert round(jd(PHASES["new 04-17"][1]) - full1, 2) == 45.01
assert round(jd("2027-05-09 11:38") - jd(PHASES["new 2027-05-06"][0]), 2) == 3.03 and round(HOR["2027-05-09 11:38"][3]) == 12


# 6: the Gregorian computus (anonymous algorithm) -> Easter and the tabular Paschal Full Moon
def easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    mm = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * mm + 114, 31)
    return date(y, month, day + 1), h, mm, a + 1


for y, md in ((2000, (4, 23)), (2008, (3, 23)), (2011, (4, 24)), (2019, (4, 21)), (2024, (3, 31)), (2025, (4, 20)),
              (2038, (4, 25))):
    assert easter(y)[0] == date(y, *md)
e26, h26, m26, golden = easter(2026)
pfm = date(2026, 3, 21) + timedelta(days=h26)
assert e26 == date(2026, 4, 5) and e26.weekday() == 6 and golden == 13 and m26 == 0
assert pfm == date(2026, 4, 2) and pfm.weekday() == 3                      # Thursday, the same date as the Full Moon
assert (e26 - pfm).days == 3 and round(jd("2026-04-05 00:00") - full2, 2) == 2.91

if __name__ == "__main__":
    print("lunar paste: phases, eclipse, ages, Easter, 33/43/432 arithmetic right;")
    print("wrong: greatest eclipse 11:33:37 (not 11:38); Apr 3/5 values are 00:00 UTC (Apr 5 noon: 141.2, 89.0 %, 38.7);")
    print("       432 d = 14.63 lunations; 33/43/432-day points at 38.4/153.1/220.5 past opposition; Easter by the tabular moon")
