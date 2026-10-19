"""
The Sun's apparent ecliptic longitude of date at 12:00 UT on one calendar day, for a range of years (JPL DE440s).

    python3 tools/sun_longitude_range.py de440s.bsp 3 3 1900 2100 records/sun_longitude_march3_1900_2100.json

Needs skyfield and de440s.bsp; not collected by pytest.
"""
import json
import math
import sys

import numpy as np
from skyfield import nutationlib
from skyfield.api import load
from skyfield.jpllib import SpiceKernel

if __name__ == "__main__":
    kernel, month, day, y0, y1, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    eph, ts = SpiceKernel(kernel), load.timescale()
    earth, sun = eph["earth"], eph["sun"]
    lons = {}
    for y in range(y0, y1 + 1):
        t = ts.utc(y, month, day, 12, 0)
        dpsi, deps = nutationlib.iau2000b(t.tt)
        e = math.radians(nutationlib.mean_obliquity(t.tdb) / 3600 + deps / (3600 * 1e7))
        Rx = np.array([[1, 0, 0], [0, math.cos(e), math.sin(e)], [0, -math.sin(e), math.cos(e)]])
        v = Rx @ (t.M @ earth.at(t).observe(sun).apparent().position.km)
        lons[y] = math.degrees(math.atan2(v[1], v[0])) % 360
    json.dump({"month": month, "day": day, "time_UT": "12:00", "kernel": "DE440s", "years": [y0, y1],
               "min": min(lons.values()), "max": max(lons.values()), "longitude": {str(k): v for k, v in lons.items()}},
              open(out, "w"), indent=1)
    print(min(lons.values()), max(lons.values()))
