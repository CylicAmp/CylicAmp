#!/usr/bin/env python3
"""meeus_lunar.py -- pure Python 3, standard library only.

Implements, from Jean Meeus, "Astronomical Algorithms", 2nd ed. (Willmann-Bell 1998):
  Ch. 7   Julian Day <-> calendar date (Gregorian)
  Ch. 22  nutation in longitude, low-accuracy series (0.5"), applied to the Moon
  Ch. 25  solar coordinates, lower-accuracy method (apparent longitude, R)
  Ch. 47  geocentric Moon: longitude, latitude, distance, full Tables 47.A and 47.B
  Ch. 48  elongation psi (48.2, ecliptic form cos psi = cos b cos(l - l0)),
          phase angle i (48.3), illuminated fraction k (48.1)
  Ch. 49  true instants of New and Full Moon with the periodic terms and the
          14 additional (planetary) corrections
Delta T (TD - UT): 2026 = 69.2 s, 2027 = 69.4 s (TT - UTC = 69.184 s since 2017).

Validation on Meeus's worked examples 49.a and 47.a is printed first, with residuals.
"""
import math

D2R = math.pi / 180.0
AU_KM = 149597870.7          # IAU 2012 astronomical unit, km
DELTA_T = {2026: 69.2, 2027: 69.4}   # seconds, TD - UT


def sind(x):
    return math.sin(x * D2R)


def cosd(x):
    return math.cos(x * D2R)


def norm360(x):
    return x % 360.0


# ---------------------------------------------------------------- Ch. 7
def jd_from_cal(y, m, d):
    """Gregorian calendar date (d may carry a day fraction) -> JD (Meeus 7.1)."""
    if m <= 2:
        y -= 1
        m += 12
    a = y // 100
    b = 2 - a + a // 4
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + b - 1524.5


def cal_from_jd_int(z):
    """Integer Z (= JD + 0.5 truncated) -> (year, month, day)  (Meeus Ch. 7, F = 0)."""
    if z < 2299161:
        a = z
    else:
        alpha = int((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - alpha // 4
    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(365.25 * c)
    e = int((b - d) / 30.6001)
    day = b - d - int(30.6001 * e)
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    return year, month, day


def fmt_jd(jd):
    """JD -> 'YYYY-MM-DD hh:mm:ss' rounded to the nearest second."""
    total = math.floor((jd + 0.5) * 86400.0 + 0.5)
    z, s = divmod(total, 86400)
    y, mo, d = cal_from_jd_int(int(z))
    hh, rem = divmod(int(s), 3600)
    mm, ss = divmod(rem, 60)
    return "%04d-%02d-%02d %02d:%02d:%02d" % (y, mo, d, hh, mm, ss)


def year_of_jd(jd):
    total = math.floor((jd + 0.5) * 86400.0 + 0.5)
    return cal_from_jd_int(int(total // 86400))[0]


def delta_t_days(jd):
    y = year_of_jd(jd)
    if y not in DELTA_T:
        raise ValueError("Delta T not given for year %d" % y)
    return DELTA_T[y] / 86400.0


def ut_to_td(jd_ut):
    return jd_ut + delta_t_days(jd_ut)


def td_to_ut(jde):
    return jde - delta_t_days(jde)


def parse_ut(s):
    """'YYYY-MM-DD hh:mm' (UT) -> JD(UT)."""
    date, hm = s.split()
    y, mo, d = (int(v) for v in date.split("-"))
    hh, mm = (int(v) for v in hm.split(":"))
    return jd_from_cal(y, mo, d + (hh + mm / 60.0) / 24.0)


# ---------------------------------------------------------------- Ch. 49
# periodic terms: (coefficient New, coefficient Full, power of E, multipliers of (M, M', F, Omega))
PHASE_TERMS = [
    (-0.40720, -0.40614, 0, (0, 1, 0, 0)),
    (0.17241, 0.17302, 1, (1, 0, 0, 0)),
    (0.01608, 0.01614, 0, (0, 2, 0, 0)),
    (0.01039, 0.01043, 0, (0, 0, 2, 0)),
    (0.00739, 0.00734, 1, (-1, 1, 0, 0)),
    (-0.00514, -0.00515, 1, (1, 1, 0, 0)),
    (0.00208, 0.00209, 2, (2, 0, 0, 0)),
    (-0.00111, -0.00111, 0, (0, 1, -2, 0)),
    (-0.00057, -0.00057, 0, (0, 1, 2, 0)),
    (0.00056, 0.00056, 1, (1, 2, 0, 0)),
    (-0.00042, -0.00042, 0, (0, 3, 0, 0)),
    (0.00042, 0.00042, 1, (1, 0, 2, 0)),
    (0.00038, 0.00038, 1, (1, 0, -2, 0)),
    (-0.00024, -0.00024, 1, (-1, 2, 0, 0)),
    (-0.00017, -0.00017, 0, (0, 0, 0, 1)),
    (-0.00007, -0.00007, 0, (2, 1, 0, 0)),
    (0.00004, 0.00004, 0, (0, 2, -2, 0)),
    (0.00004, 0.00004, 0, (3, 0, 0, 0)),
    (0.00003, 0.00003, 0, (1, 1, -2, 0)),
    (0.00003, 0.00003, 0, (0, 2, 2, 0)),
    (-0.00003, -0.00003, 0, (1, 1, 2, 0)),
    (0.00003, 0.00003, 0, (-1, 1, 2, 0)),
    (-0.00002, -0.00002, 0, (-1, 1, -2, 0)),
    (-0.00002, -0.00002, 0, (1, 3, 0, 0)),
    (0.00002, 0.00002, 0, (0, 4, 0, 0)),
]

# additional corrections (all phases): (coefficient, A0, rate per lunation k)
PLANET_TERMS = [
    (0.000325, 299.77, 0.107408),   # A1 also has -0.009173 T^2
    (0.000165, 251.88, 0.016321),
    (0.000164, 251.83, 26.651886),
    (0.000126, 349.42, 36.412478),
    (0.000110, 84.66, 18.206239),
    (0.000062, 141.74, 53.303771),
    (0.000060, 207.14, 2.453732),
    (0.000056, 154.84, 7.306860),
    (0.000047, 34.52, 27.261239),
    (0.000042, 207.19, 0.121824),
    (0.000040, 291.34, 1.844379),
    (0.000037, 161.72, 24.198154),
    (0.000035, 239.56, 25.513099),
    (0.000023, 331.55, 3.592518),
]


def moon_phase(k):
    """k integer -> New Moon, k + 0.5 -> Full Moon.  Returns dict with JDE (TD) and parts."""
    frac = k - math.floor(k)
    if abs(frac) < 1e-9:
        col = 0
    elif abs(frac - 0.5) < 1e-9:
        col = 1
    else:
        raise ValueError("only New (integer k) and Full (k + 0.5) are implemented")
    T = k / 1236.85
    jde_mean = (2451550.09766 + 29.530588861 * k + 0.00015437 * T ** 2
                - 0.000000150 * T ** 3 + 0.00000000073 * T ** 4)
    E = 1 - 0.002516 * T - 0.0000074 * T ** 2
    M = 2.5534 + 29.10535670 * k - 0.0000014 * T ** 2 - 0.00000011 * T ** 3
    Mp = (201.5643 + 385.81693528 * k + 0.0107582 * T ** 2 + 0.00001238 * T ** 3
          - 0.000000058 * T ** 4)
    F = (160.7108 + 390.67050284 * k - 0.0016118 * T ** 2 - 0.00000227 * T ** 3
         + 0.000000011 * T ** 4)
    Om = 124.7746 - 1.56375588 * k + 0.0020672 * T ** 2 + 0.00000215 * T ** 3
    periodic = 0.0
    for cn, cf, ep, (a, b, c, d) in PHASE_TERMS:
        coef = cn if col == 0 else cf
        periodic += coef * E ** ep * sind(a * M + b * Mp + c * F + d * Om)
    planetary = 0.0
    for i, (coef, a0, rate) in enumerate(PLANET_TERMS):
        A = a0 + rate * k
        if i == 0:
            A -= 0.009173 * T ** 2
        planetary += coef * sind(A)
    jde = jde_mean + periodic + planetary
    return {"k": k, "T": T, "E": E, "M": norm360(M), "Mp": norm360(Mp), "F": norm360(F),
            "Om": norm360(Om), "jde_mean": jde_mean, "periodic": periodic,
            "planetary": planetary, "jde": jde}


def k_estimate(jd):
    return (2000.0 + (jd - 2451545.0) / 365.25 - 2000.0) * 12.3685


def nearest_phase(jd_target, kind):
    """Phase of the given kind ('new' / 'full') whose TD instant is nearest jd_target."""
    off = 0.0 if kind == "new" else 0.5
    k0 = math.floor(k_estimate(jd_target)) + off
    cands = [moon_phase(k0 + j) for j in range(-2, 3)]
    return min(cands, key=lambda p: abs(p["jde"] - jd_target))


def preceding_new_moon_ut(jd_ut):
    """Latest computed New Moon with UT instant <= jd_ut.  Returns (phase dict, JD UT)."""
    k = math.floor(k_estimate(jd_ut)) + 2
    while True:
        p = moon_phase(k)
        ut = td_to_ut(p["jde"])
        if ut <= jd_ut:
            return p, ut
        k -= 1


# ---------------------------------------------------------------- Ch. 47
# Table 47.A: D, M, M', F, coefficient of sine (Sigma l, 1e-6 deg), coefficient of cosine (Sigma r, 1e-3 km)
TAB_47A = [
    (0, 0, 1, 0, 6288774, -20905355),
    (2, 0, -1, 0, 1274027, -3699111),
    (2, 0, 0, 0, 658314, -2955968),
    (0, 0, 2, 0, 213618, -569925),
    (0, 1, 0, 0, -185116, 48888),
    (0, 0, 0, 2, -114332, -3149),
    (2, 0, -2, 0, 58793, 246158),
    (2, -1, -1, 0, 57066, -152138),
    (2, 0, 1, 0, 53322, -170733),
    (2, -1, 0, 0, 45758, -204586),
    (0, 1, -1, 0, -40923, -129620),
    (1, 0, 0, 0, -34720, 108743),
    (0, 1, 1, 0, -30383, 104755),
    (2, 0, 0, -2, 15327, 10321),
    (0, 0, 1, 2, -12528, 0),
    (0, 0, 1, -2, 10980, 79661),
    (4, 0, -1, 0, 10675, -34782),
    (0, 0, 3, 0, 10034, -23210),
    (4, 0, -2, 0, 8548, -21636),
    (2, 1, -1, 0, -7888, 24208),
    (2, 1, 0, 0, -6766, 30824),
    (1, 0, -1, 0, -5163, -8379),
    (1, 1, 0, 0, 4987, -16675),
    (2, -1, 1, 0, 4036, -12831),
    (2, 0, 2, 0, 3994, -10445),
    (4, 0, 0, 0, 3861, -11650),
    (2, 0, -3, 0, 3665, 14403),
    (0, 1, -2, 0, -2689, -7003),
    (2, 0, -1, 2, -2602, 0),
    (2, -1, -2, 0, 2390, 10056),
    (1, 0, 1, 0, -2348, 6322),
    (2, -2, 0, 0, 2236, -9884),
    (0, 1, 2, 0, -2120, 5751),
    (0, 2, 0, 0, -2069, 0),
    (2, -2, -1, 0, 2048, -4950),
    (2, 0, 1, -2, -1773, 4130),
    (2, 0, 0, 2, -1595, 0),
    (4, -1, -1, 0, 1215, -3958),
    (0, 0, 2, 2, -1110, 0),
    (3, 0, -1, 0, -892, 3258),
    (2, 1, 1, 0, -810, 2616),
    (4, -1, -2, 0, 759, -1897),
    (0, 2, -1, 0, -713, -2117),
    (2, 2, -1, 0, -700, 2354),
    (2, 1, -2, 0, 691, 0),
    (2, -1, 0, -2, 596, 0),
    (4, 0, 1, 0, 549, -1423),
    (0, 0, 4, 0, 537, -1117),
    (4, -1, 0, 0, 520, -1571),
    (1, 0, -2, 0, -487, -1739),
    (2, 1, 0, -2, -399, 0),
    (0, 0, 2, -2, -381, -4421),
    (1, 1, 1, 0, 351, 0),
    (3, 0, -2, 0, -340, 0),
    (4, 0, -3, 0, 330, 0),
    (2, -1, 2, 0, 327, 0),
    (0, 2, 1, 0, -323, 1165),
    (1, 1, -1, 0, 299, 0),
    (2, 0, 3, 0, 294, 0),
    (2, 0, -1, -2, 0, 8752),
]

# Table 47.B: D, M, M', F, coefficient of sine (Sigma b, 1e-6 deg)
TAB_47B = [
    (0, 0, 0, 1, 5128122),
    (0, 0, 1, 1, 280602),
    (0, 0, 1, -1, 277693),
    (2, 0, 0, -1, 173237),
    (2, 0, -1, 1, 55413),
    (2, 0, -1, -1, 46271),
    (2, 0, 0, 1, 32573),
    (0, 0, 2, 1, 17198),
    (2, 0, 1, -1, 9266),
    (0, 0, 2, -1, 8822),
    (2, -1, 0, -1, 8216),
    (2, 0, -2, -1, 4324),
    (2, 0, 1, 1, 4200),
    (2, 1, 0, -1, -3359),
    (2, -1, -1, 1, 2463),
    (2, -1, 0, 1, 2211),
    (2, -1, -1, -1, 2065),
    (0, 1, -1, -1, -1870),
    (4, 0, -1, -1, 1828),
    (0, 1, 0, 1, -1794),
    (0, 0, 0, 3, -1749),
    (0, 1, -1, 1, -1565),
    (1, 0, 0, 1, -1491),
    (0, 1, 1, 1, -1475),
    (0, 1, 1, -1, -1410),
    (0, 1, 0, -1, -1344),
    (1, 0, 0, -1, -1335),
    (0, 0, 3, 1, 1107),
    (4, 0, 0, -1, 1021),
    (4, 0, -1, 1, 833),
    (0, 0, 1, -3, 777),
    (4, 0, -2, 1, 671),
    (2, 0, 0, -3, 607),
    (2, 0, 2, -1, 596),
    (2, -1, 1, -1, 491),
    (2, 0, -2, 1, -451),
    (0, 0, 3, -1, 439),
    (2, 0, 2, 1, 422),
    (2, 0, -3, -1, 421),
    (2, 1, -1, 1, -366),
    (2, 1, 0, 1, -351),
    (4, 0, 0, 1, 331),
    (2, -1, 1, 1, 315),
    (2, -2, 0, -1, 302),
    (0, 0, 1, 3, -283),
    (2, 1, 1, -1, -229),
    (1, 1, 0, -1, 223),
    (1, 1, 0, 1, 223),
    (0, 1, -2, -1, -220),
    (2, 1, -1, -1, -220),
    (1, 0, 1, 1, -185),
    (2, -1, -2, -1, 181),
    (0, 1, 2, 1, -177),
    (4, 0, -2, -1, 176),
    (4, -1, -1, -1, 166),
    (1, 0, 1, -1, -164),
    (4, 0, 1, -1, 132),
    (1, 0, -1, -1, -119),
    (4, -1, 0, -1, 115),
    (2, -2, 0, 1, 107),
]
assert len(TAB_47A) == 60 and len(TAB_47B) == 60


def moon_position(jde):
    """Geocentric Moon, mean equinox of date (Meeus Ch. 47)."""
    T = (jde - 2451545.0) / 36525.0
    Lp = (218.3164477 + 481267.88123421 * T - 0.0015786 * T ** 2 + T ** 3 / 538841.0
          - T ** 4 / 65194000.0)
    D = (297.8501921 + 445267.1114034 * T - 0.0018819 * T ** 2 + T ** 3 / 545868.0
         - T ** 4 / 113065000.0)
    M = 357.5291092 + 35999.0502909 * T - 0.0001536 * T ** 2 + T ** 3 / 24490000.0
    Mp = (134.9633964 + 477198.8675055 * T + 0.0087414 * T ** 2 + T ** 3 / 69699.0
          - T ** 4 / 14712000.0)
    F = (93.2720950 + 483202.0175233 * T - 0.0036539 * T ** 2 - T ** 3 / 3526000.0
         + T ** 4 / 863310000.0)
    A1 = 119.75 + 131.849 * T
    A2 = 53.09 + 479264.290 * T
    A3 = 313.45 + 481266.484 * T
    E = 1 - 0.002516 * T - 0.0000074 * T ** 2
    Lp, D, M, Mp, F = (norm360(v) for v in (Lp, D, M, Mp, F))
    A1, A2, A3 = (norm360(v) for v in (A1, A2, A3))
    sl = sr = sb = 0.0
    for d, m, mp, f, cl, cr in TAB_47A:
        arg = d * D + m * M + mp * Mp + f * F
        e = E ** abs(m)
        sl += cl * e * sind(arg)
        sr += cr * e * cosd(arg)
    for d, m, mp, f, cb in TAB_47B:
        arg = d * D + m * M + mp * Mp + f * F
        sb += cb * E ** abs(m) * sind(arg)
    sl += 3958 * sind(A1) + 1962 * sind(Lp - F) + 318 * sind(A2)
    sb += (-2235 * sind(Lp) + 382 * sind(A3) + 175 * sind(A1 - F) + 175 * sind(A1 + F)
           + 127 * sind(Lp - Mp) - 115 * sind(Lp + Mp))
    lam = norm360(Lp + sl / 1e6)
    beta = sb / 1e6
    dist = 385000.56 + sr / 1000.0
    return {"T": T, "Lp": Lp, "D": D, "M": M, "Mp": Mp, "F": F, "A1": A1, "A2": A2,
            "A3": A3, "E": E, "sl": sl, "sb": sb, "sr": sr,
            "lam": lam, "beta": beta, "dist_km": dist}


# ---------------------------------------------------------------- Ch. 22 (low accuracy)
def nutation_longitude_deg(jde):
    T = (jde - 2451545.0) / 36525.0
    Om = 125.04452 - 1934.136261 * T + 0.0020708 * T ** 2 + T ** 3 / 450000.0
    L = 280.4665 + 36000.7698 * T
    Lp = 218.3165 + 481267.8813 * T
    dpsi = -17.20 * sind(Om) - 1.32 * sind(2 * L) - 0.23 * sind(2 * Lp) + 0.21 * sind(2 * Om)
    return dpsi / 3600.0


# ---------------------------------------------------------------- Ch. 25 (lower accuracy)
def sun_position(jde):
    T = (jde - 2451545.0) / 36525.0
    L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T ** 2
    M = 357.52911 + 35999.05029 * T - 0.0001537 * T ** 2
    e = 0.016708634 - 0.000042037 * T - 0.0000001267 * T ** 2
    C = ((1.914602 - 0.004817 * T - 0.000014 * T ** 2) * sind(M)
         + (0.019993 - 0.000101 * T) * sind(2 * M) + 0.000289 * sind(3 * M))
    true_lon = L0 + C
    nu = M + C
    R = 1.000001018 * (1 - e * e) / (1 + e * cosd(nu))
    Om = 125.04 - 1934.136 * T
    app_lon = true_lon - 0.00569 - 0.00478 * sind(Om)
    return {"T": T, "L0": norm360(L0), "M": norm360(M), "e": e, "C": C,
            "true_lon": norm360(true_lon), "R_au": R, "Om": norm360(Om),
            "app_lon": norm360(app_lon)}


# ---------------------------------------------------------------- Ch. 48
def phase_quantities(jde):
    mo = moon_position(jde)
    su = sun_position(jde)
    dpsi = nutation_longitude_deg(jde)
    lam_moon_app = norm360(mo["lam"] + dpsi)
    lam_sun_app = su["app_lon"]
    dlon = norm360(lam_moon_app - lam_sun_app)
    cospsi = cosd(mo["beta"]) * cosd(lam_moon_app - lam_sun_app)          # 48.2 (ecliptic form)
    cospsi = max(-1.0, min(1.0, cospsi))
    psi = math.degrees(math.acos(cospsi))
    R_km = su["R_au"] * AU_KM
    i = math.degrees(math.atan2(R_km * sind(psi), mo["dist_km"] - R_km * cosd(psi)))  # 48.3
    k = (1 + cosd(i)) / 2.0                                                # 48.1
    return {"moon": mo, "sun": su, "dpsi": dpsi, "lam_moon_app": lam_moon_app,
            "lam_sun_app": lam_sun_app, "dlon": dlon, "psi": psi, "i": i, "k": k}


# ---------------------------------------------------------------- output
def main():
    print("=" * 78)
    print("VALIDATION 1 -- Meeus Example 49.a (New Moon, 1977 February, k = -283)")
    p = moon_phase(-283)
    ref = {"T": -0.22881, "jde_mean": 2443192.94102, "periodic": -0.28916,
           "planetary": -0.00068, "jde": 2443192.65118}
    for key in ("T", "jde_mean", "periodic", "planetary", "jde"):
        print("  %-10s computed %18.6f   Meeus %16.5f   residual %+.6f"
              % (key, p[key], ref[key], p[key] - ref[key]))
    print("  E = %.7f  M = %.4f  M' = %.4f  F = %.4f  Omega = %.4f (deg)"
          % (p["E"], p["M"], p["Mp"], p["F"], p["Om"]))
    print("  JDE residual = %+.1f s ; instant TD = %s (Meeus: 1977 Feb 18 03:37:42 TD)"
          % ((p["jde"] - ref["jde"]) * 86400, fmt_jd(p["jde"])))

    print("=" * 78)
    print("VALIDATION 2 -- Meeus Example 47.a (1992 April 12, 0h TD, JDE 2448724.5)")
    jde = 2448724.5
    m = moon_position(jde)
    ref = {"T": -0.077221081451, "Lp": 134.290182, "D": 113.842304, "M": 97.643514,
           "Mp": 5.150833, "F": 219.889721, "E": 1.000194,
           "sl": -1127527, "sb": -3229126, "sr": -16590875,
           "lam": 133.162655, "beta": -3.229126, "dist_km": 368409.7}
    for key in ("T", "Lp", "D", "M", "Mp", "F", "E", "sl", "sb", "sr", "lam", "beta",
                "dist_km"):
        print("  %-8s computed %20.6f   Meeus %18.6f   residual %+.6f"
              % (key, m[key], ref[key], m[key] - ref[key]))
    print("  residuals: lambda %+.4f arcsec, beta %+.4f arcsec, distance %+.3f km"
          % ((m["lam"] - ref["lam"]) * 3600, (m["beta"] - ref["beta"]) * 3600,
             m["dist_km"] - ref["dist_km"]))
    dpsi = nutation_longitude_deg(jde)
    print("  Delta psi (low-accuracy 4-term series) = %+.6f deg ; Meeus Ex 47.a uses +0.004610"
          % dpsi)
    print("  apparent lambda = %.6f deg ; Meeus 133.167265 ; residual %+.4f arcsec"
          % (m["lam"] + dpsi, (m["lam"] + dpsi - 133.167265) * 3600))

    print("=" * 78)
    print("DELTA T used (TD - UT): 2026 = 69.2 s, 2027 = 69.4 s")
    print("=" * 78)
    print("MOON PHASES (Meeus Ch. 49, true instants)")
    targets = [("New", "2026-02-17 00:00"), ("Full", "2026-03-03 00:00"),
               ("New", "2026-03-19 00:00"), ("Full", "2026-04-02 00:00"),
               ("New", "2026-04-17 00:00"), ("Full", "2027-05-09 00:00"),
               ("New", "2027-05-09 00:00")]
    for kind, tstr in targets:
        jt = ut_to_td(parse_ut(tstr))
        ph = nearest_phase(jt, kind.lower())
        ut = td_to_ut(ph["jde"])
        print("  %-4s nearest %s : k = %8.1f  JDE = %.5f  TD %s  UT %s  (JD UT %.5f)"
              % (kind, tstr[:10], ph["k"], ph["jde"], fmt_jd(ph["jde"]), fmt_jd(ut), ut))

    print("=" * 78)
    print("PHASE GEOMETRY at given UT instants")
    print("  dlon = apparent lambda(Moon) - apparent lambda(Sun), 0..360 deg")
    print("  psi  = geocentric elongation, cos psi = cos(beta) cos(lambda - lambda0)  (48.2)")
    print("  i    = phase angle, tan i = R sin psi / (Delta - R cos psi)              (48.3)")
    print("  k    = illuminated fraction (1 + cos i)/2                                (48.1)")
    print("  age  = days since preceding computed New Moon (UT to UT)")
    times = ["2026-03-03 11:38", "2026-04-02 02:12", "2026-04-03 00:00",
             "2026-04-03 12:00", "2026-04-05 00:00", "2026-04-05 11:38",
             "2026-04-05 12:00", "2026-04-05 18:00", "2026-04-15 11:38",
             "2027-05-09 11:38"]
    for tstr in times:
        jd_ut = parse_ut(tstr)
        jde = ut_to_td(jd_ut)
        q = phase_quantities(jde)
        nm, nm_ut = preceding_new_moon_ut(jd_ut)
        age = jd_ut - nm_ut
        mo, su = q["moon"], q["sun"]
        print("  %s UT (JD UT %.6f, JDE %.6f)" % (tstr, jd_ut, jde))
        print("     Moon: lambda_app %10.6f  beta %+9.6f  Delta %10.1f km | "
              "Sun: lambda_app %10.6f  R %.6f AU"
              % (q["lam_moon_app"], mo["beta"], mo["dist_km"], q["lam_sun_app"], su["R_au"]))
        print("     dlon %10.6f deg  psi %10.6f deg  i %10.6f deg  k %.6f  "
              "age %8.5f d (since New Moon %s UT)"
              % (q["dlon"], q["psi"], q["i"], q["k"], age, fmt_jd(nm_ut)))


if __name__ == "__main__":
    main()
