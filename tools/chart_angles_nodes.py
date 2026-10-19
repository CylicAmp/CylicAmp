"""
Chart angles, lunar node and apogee, and a DE440s cross-check of the planets, for one UT instant and place.
Adds a "derived" section to the JSON written by tools/horizons_ecliptic.py.

    python3 tools/chart_angles_nodes.py de440s.bsp records/chart_check_1987_09_27_nasa.json \
        1987 9 27 23 42  37.209 -93.2923  37.2 -93.28333333

Needs skyfield and the JPL kernel de440s.bsp (https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp).
Not imported by any test and not collected by pytest, so nothing here is a CI dependency.

What is computed (all ecliptic longitudes in degrees, true equinox and ecliptic of date):
  RAMC from Greenwich apparent sidereal time + east longitude; MC, Ascendant (AC), East Point (EP), Vertex by the
  standard formulas; Part of Fortune (day chart: AC + Moon - Sun); the lunar node and apogee from the Moon's
  osculating orbit (state vector Moon - Earth from DE440s, mu = GM_earth + GM_moon) and the mean node and mean
  apogee from the Meeus series; and the Sun-Neptune apparent longitudes from DE440s, to compare with Horizons.
"""
import json
import math
import sys

import numpy as np
from skyfield import nutationlib
from skyfield.api import load
from skyfield.jpllib import SpiceKernel

NAMES = {"Sun": "sun", "Moon": "moon", "Mercury": "mercury barycenter", "Venus": "venus barycenter",
         "Mars": "mars barycenter", "Jupiter": "jupiter barycenter", "Saturn": "saturn barycenter",
         "Uranus": "uranus barycenter", "Neptune": "neptune barycenter", "Pluto": "pluto barycenter"}


def asc(theta, phi, eps):
    return math.degrees(math.atan2(math.cos(theta), -(math.sin(theta) * math.cos(eps) + math.tan(phi) * math.sin(eps)))) % 360


def main(kernel, out, y, mo, d, h, mi, lat, lon, lat2, lon2):
    eph = SpiceKernel(kernel)
    ts = load.timescale()
    t = ts.utc(y, mo, d, h, mi)
    dpsi, deps = nutationlib.iau2000b(t.tt)
    eps_deg = nutationlib.mean_obliquity(t.tdb) / 3600 + deps / (3600 * 1e7)
    ce, se = math.cos(math.radians(eps_deg)), math.sin(math.radians(eps_deg))
    Rx = np.array([[1, 0, 0], [0, ce, se], [0, -se, ce]])
    to_date = lambda vec: Rx @ (t.M @ vec)

    earth = eph["earth"]
    planets = {}
    for name, key in NAMES.items():
        p = earth.at(t).observe(eph[key]).apparent().position.km
        x = to_date(p)
        planets[name] = math.degrees(math.atan2(x[1], x[0])) % 360

    rel = (eph["moon"] - earth).at(t)
    r, v = to_date(rel.position.km), to_date(rel.velocity.km_per_s)
    hvec = np.cross(r, v)
    mu = 398600.435507 + 4902.800118
    node = math.degrees(math.atan2(hvec[0], -hvec[1])) % 360
    ecc = np.cross(v, hvec) / mu - r / np.linalg.norm(r)
    apogee = math.degrees(math.atan2(-ecc[1], -ecc[0])) % 360
    T = (t.tt - 2451545.0) / 36525
    mean_node = (125.0445479 - 1934.1362891 * T + 0.0020754 * T * T + T ** 3 / 467441) % 360
    mean_apogee = (83.3532465 + 4069.0137287 * T - 0.0103200 * T * T - T ** 3 / 80053 + 180) % 360

    angles = {}
    for tag, la, lo in (("printed_header_coordinates", lat, lon), ("springfield_exact_coordinates", lat2, lon2)):
        ramc = ((t.gast * 15) + lo) % 360
        th, ep = math.radians(ramc), math.radians(eps_deg)
        mc = math.degrees(math.atan2(math.sin(th), math.cos(th) * math.cos(ep))) % 360
        ac = asc(th, math.radians(la), ep)
        angles[tag] = {"lat": la, "lon": lo, "RAMC": ramc, "MC": mc, "AC": ac, "DC": (ac + 180) % 360,
                       "EP": asc(th, 0.0, ep), "Vertex": asc(th + math.pi, math.radians(90 - la), ep),
                       "PartOfFortune_day": (ac + planets["Moon"] - planets["Sun"]) % 360}
    data = json.load(open(out))
    data["derived"] = {"kernel": "DE440s", "true_obliquity_deg": eps_deg, "planets_DE440s_apparent_of_date": planets,
                       "osculating_node": node, "osculating_apogee": apogee, "mean_node": mean_node,
                       "mean_apogee": mean_apogee, "angles": angles}
    json.dump(data, open(out, "w"), indent=1)
    for k, vv in planets.items():
        print(f"{k:8s} DE440s {vv:11.6f}   Horizons {data['bodies'][k]['ObsEcLon']:11.6f}   diff {(vv - data['bodies'][k]['ObsEcLon']) * 3600:+7.2f} arcsec")
    print("osculating node", round(node, 4), "apogee", round(apogee, 4), "mean node", round(mean_node, 4), "mean apogee", round(mean_apogee, 4))
    print(json.dumps(angles, indent=1))


if __name__ == "__main__":
    a = sys.argv
    main(a[1], a[2], int(a[3]), int(a[4]), int(a[5]), int(a[6]), int(a[7]), float(a[8]), float(a[9]), float(a[10]), float(a[11]))
