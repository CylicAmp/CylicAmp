"""
Moon phases, equinox and lunar eclipses around one date, from the JPL kernel DE440s (skyfield), added to the
"events" section of a JSON file.

    python3 tools/lunation_events.py de440s.bsp records/chart_check_1987_09_27_nasa.json 1987 8 25 1987 11 15

Also stores the Sun-Moon angular separation around the 1987-09-23 new moon (hourly, 02:00-04:00 UT).
Needs skyfield and de440s.bsp; not collected by pytest.
"""
import json
import sys

from skyfield import almanac, eclipselib
from skyfield.api import load
from skyfield.jpllib import SpiceKernel

if __name__ == "__main__":
    kernel, out = sys.argv[1], sys.argv[2]
    y0, m0, d0, y1, m1, d1 = map(int, sys.argv[3:9])
    eph, ts = SpiceKernel(kernel), load.timescale()
    t0, t1 = ts.utc(y0, m0, d0), ts.utc(y1, m1, d1)
    ti, yi = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))
    phases = [[almanac.MOON_PHASES[int(b)], a.utc_strftime("%Y-%m-%d %H:%M")] for a, b in zip(ti, yi)]
    ti, yi = almanac.find_discrete(ts.utc(y0, 1, 1), ts.utc(y0 + 1, 1, 1), almanac.seasons(eph))
    seasons = [[almanac.SEASON_EVENTS[int(b)], a.utc_strftime("%Y-%m-%d %H:%M")] for a, b in zip(ti, yi)]
    t, y, det = eclipselib.lunar_eclipses(ts.utc(y0, 1, 1), ts.utc(y0 + 1, 1, 1), eph)
    lunar = [[eclipselib.LUNAR_ECLIPSES[int(b)], a.utc_strftime("%Y-%m-%d %H:%M")] for a, b in zip(t, y)]
    earth = eph["earth"]
    sep = {}
    for hh in (2, 3, 4):
        tt = ts.utc(1987, 9, 23, hh, 0)
        sep[f"1987-09-23 {hh:02d}:00"] = earth.at(tt).observe(eph["sun"]).apparent().separation_from(
            earth.at(tt).observe(eph["moon"]).apparent()).degrees
    data = json.load(open(out))
    data["events"] = {"kernel": "DE440s", "moon_phases_UT": phases, "seasons_UT": seasons,
                      "lunar_eclipses_UT": lunar, "sun_moon_separation_deg": sep,
                      "NASA_solar_eclipse_catalog_line": None}
    json.dump(data, open(out, "w"), indent=1)
    print(phases, seasons, lunar, sep, sep="\n")
