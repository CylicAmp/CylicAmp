# CLASS: AUDIT
"""
A birth chart on a TikTok live screen, checked against NASA/JPL data (owner_work #346, 2026-10-19).

THE OWNER'S QUESTION, verbatim: "if we go by my birthday math how far off is the charts according to actually
nasal data and math..Just curious". Reading used: compare every number printed on the chart with the position
NASA's ephemeris gives for the date and place printed on it. "Birthday math" is taken as the owner's digit chain,
run on the chart's date at the end. The chart is NOT the owner's date (March 3); whose chart it is I don't know.

THE CHART'S HEADER, as read off the screenshot:
    September 27, 1987, 06:42 PM, Springfield (Greene), Missouri [93.17W ; 37.12N] / 5W00, 11:42 PM UT
  Right: 18:42 + 5h = 23:42 UT, and Missouri was on daylight time on 1987-09-27 (US daylight time ran
  1987-04-05 to 1987-10-25), so 5W00 is correct. 93.17W and 37.12N are degrees.minutes (93d17'W, 37d12'N),
  which is where Springfield is (37.209N, 93.2923W = 37d12.5'N, 93d17.5'W). Read as decimal degrees they would be
  about 11 km off.

WHAT NASA DATA GIVES (records/chart_check_1987_09_27_nasa.json, made by tools/horizons_ecliptic.py and
tools/chart_angles_nodes.py; the Horizons lines are stored as returned):
    JPL Horizons API, geocentric, QUANTITIES=31 (apparent ecliptic longitude of date): Sun, Moon, Mercury ... Pluto,
    Chiron, Ceres, Pallas, Juno, Vesta. The JPL kernel DE440s, run separately, agrees with Horizons to under 0.1
    arcsecond for the ten planets and the Moon.
    The angles (MC, AC, East Point, Vertex), the Moon's node and apogee and the Part of Fortune are computed from
    Greenwich apparent sidereal time, the true obliquity and the Moon's state vector (formulas in the tool).

RESULT: every one of the 22 printed positions is right. The printed minutes are whole minutes, so each is within
0.5 of an arcminute of NASA's value; the largest differences are listed by the assertions below. The AC is 1.05'
away when computed from the printed header coordinates (to the minute) and 0.15' away from Springfield's exact
coordinates. The R marks are right: only Jupiter and Juno move backwards on that date (-0.11 and -0.10 degrees a
day); the node marked R is the Moon's node, which runs backwards. The node on the chart is the Moon's actual
(osculating) node, 2d21.7' Aries, not the mean node (2d11.9'); the lilith is the actual apogee, 22d06.1' Leo, not
the mean apogee (4d25.9' Leo).

BIRTHDAY MATH on the chart's date, in the owner's chain:
    9/27/1987 = 9+2+7+1+9+8+7 = 43 = 4+3 = 7 ;  9 | 27 | 1987 -> 9, 9, 1+9+8+7=25=7 ; 9+9+7=25=7
    time 18:42 = 1+8+4+2 = 15 = 6 ; UT 23:42 = 2+3+4+2 = 11 = 2

FALSIFICATION: any assertion failing.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
NASA = json.load(open(ROOT / "records" / "chart_check_1987_09_27_nasa.json"))
B, DERIVED = NASA["bodies"], NASA["derived"]
ANG = DERIVED["angles"]["springfield_exact_coordinates"]
ANG_PRINTED = DERIVED["angles"]["printed_header_coordinates"]

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn",
         "Aquarius", "Pisces"]

# degree, minute as printed on the chart; sign by the longitude it matches
CHART = {
    "Sun": (4, 20, "Libra"), "Moon": (2, 45, "Sagittarius"), "Mercury": (29, 7, "Libra"), "Venus": (13, 58, "Libra"),
    "Mars": (23, 4, "Virgo"), "Jupiter": (27, 19, "Aries"), "Saturn": (15, 47, "Sagittarius"),
    "Uranus": (23, 1, "Sagittarius"), "Neptune": (5, 16, "Capricorn"), "Pluto": (8, 31, "Scorpio"),
    "Chiron": (28, 46, "Gemini"), "Ceres": (27, 52, "Sagittarius"), "Pallas": (1, 9, "Sagittarius"),
    "Juno": (23, 2, "Aquarius"), "Vesta": (25, 38, "Cancer"),
    "Node": (2, 22, "Aries"), "Lilith": (22, 6, "Leo"),
    "MC": (28, 34, "Sagittarius"), "AC": (27, 27, "Pisces"), "EP": (28, 18, "Pisces"), "Vertex": (28, 55, "Virgo"),
    "PartOfFortune": (25, 53, "Taurus"),
}
assert len(CHART) == 15 + 2 + 4 + 1 == 22          # 15 bodies, node, lilith, MC, AC, EP, Vertex, Part of Fortune


def nasa_lon(name):
    if name in B:
        return B[name]["ObsEcLon"]
    return {"Node": DERIVED["osculating_node"], "Lilith": DERIVED["osculating_apogee"], "MC": ANG["MC"],
            "AC": ANG["AC"], "EP": ANG["EP"], "Vertex": ANG["Vertex"], "PartOfFortune": ANG["PartOfFortune_day"]}[name]


diffs = {}
for name, (deg, minute, sign) in CHART.items():
    lon = nasa_lon(name)
    assert SIGNS[int(lon // 30)] == sign, name
    nasa_minutes = (lon % 30) * 60
    diffs[name] = deg * 60 + minute - nasa_minutes             # chart minus NASA, in arcminutes
    assert abs(diffs[name]) <= 0.55, (name, diffs[name])       # printed to the whole minute

assert max(abs(x) for x in diffs.values()) <= 0.55

# the AC from the header's coordinates, to the minute
assert abs((27 * 60 + 27) - ((ANG_PRINTED["AC"] % 30) * 60)) < 1.1 and abs((27 * 60 + 27) - ((ANG_PRINTED["AC"] % 30) * 60)) > 1.0
assert abs(diffs["AC"]) < 0.2

# DE440s against Horizons, ten bodies, in arcseconds
for name, lon in DERIVED["planets_DE440s_apparent_of_date"].items():
    assert abs(lon - B[name]["ObsEcLon"]) * 3600 < 0.1, name

# retrograde marks: R on Jupiter and Juno (and the node), no other body moves backwards
motion = NASA["motion_12h_before_and_after"]
assert sorted(n for n, m in motion.items() if m["deg_per_day"] < 0) == ["Juno", "Jupiter"]
assert -1934.1362891 / 36525 < 0                                    # the mean node runs backwards

# the node and the apogee on the chart are the actual ones, not the mean ones
assert abs(DERIVED["osculating_node"] % 30 * 60 - (2 * 60 + 21.7)) < 0.1 and abs(DERIVED["mean_node"] % 30 * 60 - (2 * 60 + 11.9)) < 0.1
assert abs(DERIVED["osculating_apogee"] % 30 * 60 - (22 * 60 + 6.1)) < 0.1 and abs(DERIVED["mean_apogee"] % 30 * 60 - (4 * 60 + 25.9)) < 0.1

# header
import datetime
assert datetime.datetime(1987, 9, 27, 18, 42) + datetime.timedelta(hours=5) == datetime.datetime(1987, 9, 27, 23, 42)
assert NASA["time_UT"] == "1987-09-27 23:42"
assert datetime.date(1987, 4, 5) <= datetime.date(1987, 9, 27) <= datetime.date(1987, 10, 25)

# birthday math on the chart's date
def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


assert 9 + 2 + 7 + 1 + 9 + 8 + 7 == 43 and 4 + 3 == 7 == dr(43)
assert (dr(9), dr(27), dr(1987)) == (9, 9, 7) and 9 + 9 + 7 == 25 and dr(25) == 7
assert 1 + 8 + 4 + 2 == 15 and dr(15) == 6 and 2 + 3 + 4 + 2 == 11 and dr(11) == 2

if __name__ == "__main__":
    print("chart vs NASA: 22 printed positions, largest difference %.2f arcminutes (printed to the whole minute); "
          "R marks right; node and lilith are the actual ones" % max(abs(x) for x in diffs.values()))
    for n, d in diffs.items():
        print(f"  {n:14s} chart minus NASA {d:+.2f}'")
