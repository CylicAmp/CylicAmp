"""
Fetch geocentric ecliptic longitudes from NASA/JPL Horizons for one UT instant and write them to a JSON file.

    python3 tools/horizons_ecliptic.py "1987-09-27 23:42" records/chart_check_1987_09_27_nasa.json

Request used for every body (Horizons API v1.2): CENTER=500@399 (geocenter), EPHEM_TYPE=OBSERVER,
QUANTITIES=31 (ObsEcLon, ObsEcLat), TIME_TYPE=UT, one TLIST time, ANG_FORMAT=DEG. Standard library only;
needs network access to ssd.jpl.nasa.gov. The JSON keeps the exact lines Horizons returned, so the numbers
can be checked without running this again.
"""
import datetime
import json
import re
import sys
import urllib.parse
import urllib.request

BODIES = {"Sun": "10", "Moon": "301", "Mercury": "199", "Venus": "299", "Mars": "499", "Jupiter": "599",
          "Saturn": "699", "Uranus": "799", "Neptune": "899", "Pluto": "999", "Chiron": "2060",
          "Ceres": "1;", "Pallas": "2;", "Juno": "3;", "Vesta": "4;"}


def fetch(command, when):
    q = {"format": "text", "COMMAND": f"'{command}'", "OBJ_DATA": "'NO'", "MAKE_EPHEM": "'YES'",
         "EPHEM_TYPE": "'OBSERVER'", "CENTER": "'500@399'", "TLIST": f"'{when}'", "TIME_TYPE": "'UT'",
         "QUANTITIES": "'31'", "ANG_FORMAT": "'DEG'"}
    url = "https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q)
    text = urllib.request.urlopen(url, timeout=60).read().decode()
    block = text.split("$$SOE")[1].split("$$EOE")[0].strip()
    nums = re.findall(r"-?\d+\.\d+", block.splitlines()[0])
    return block.splitlines()[0].strip(), float(nums[-2]), float(nums[-1])


if __name__ == "__main__":
    when, out = sys.argv[1], sys.argv[2]
    result = {"time_UT": when, "source": "NASA/JPL Horizons API, QUANTITIES=31, CENTER=500@399", "bodies": {},
              "motion_12h_before_and_after": {}}
    before = (datetime.datetime.strptime(when, "%Y-%m-%d %H:%M") - datetime.timedelta(hours=12)).strftime("%Y-%m-%d %H:%M")
    after = (datetime.datetime.strptime(when, "%Y-%m-%d %H:%M") + datetime.timedelta(hours=12)).strftime("%Y-%m-%d %H:%M")
    for name, cmd in BODIES.items():
        line, lon, lat = fetch(cmd, when)
        result["bodies"][name] = {"command": cmd, "line": line, "ObsEcLon": lon, "ObsEcLat": lat}
        lon_b, lon_a = fetch(cmd, before)[1], fetch(cmd, after)[1]
        result["motion_12h_before_and_after"][name] = {"before_UT": before, "ObsEcLon_before": lon_b,
                                                       "after_UT": after, "ObsEcLon_after": lon_a,
                                                       "deg_per_day": ((lon_a - lon_b + 180) % 360) - 180}
        print(f"{name:8s} {lon:12.6f}  {lat:10.6f}   motion {result['motion_12h_before_and_after'][name]['deg_per_day']:+.4f} deg/day")
    json.dump(result, open(out, "w"), indent=1)
