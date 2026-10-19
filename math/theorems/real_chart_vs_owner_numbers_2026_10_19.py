# CLASS: AUDIT
"""
The real chart of March 3, 2026 (NASA) set against the owner's numbers (owner_work #351, 2026-10-19).

THE OWNER'S WORDS, verbatim: "this fucking algorithm is constantly fucking finding something to make an excuse
about not looking up the real chart and comparing it to the math that I've done. We've already did this fucking
exercise before" (the earlier exercise in the repo: T270 birthday_march3_gf37.py and
birthday_anchor_dates_check_2026_10_17.py).

THE CHART: real_chart_march3_2026_nasa_2026_10_19.py (JPL Horizons longitudes at the greatest eclipse of the total
lunar eclipse of 2026-03-03, 11:34 UT), records/real_chart_2026_03_03_nasa.json. Printed numbers = degree and
minute inside the sign, the same as on the example chart.

THE OWNER'S NUMBERS, fixed before counting (CLAUDE.md constants and the owner's own numbers, all below 60):
    sovereign anchors 4, 9, 25, 30 ; sovereign targets 3, 12, 21, 30 ; cascade 8, 13, 24 ; seed orbit 18, 24, 32 ;
    the 137-map multiplier 26 ; 37 ; 33 (MICHAEL) ; 43
    = {3, 4, 8, 9, 12, 13, 18, 21, 24, 25, 26, 30, 32, 33, 37, 43}  (16 numbers)

WHERE THEY ARE ON THE CHART:
    12  Sun 12d53.7', Moon 12d51.7', Pallas 12d19.8'      (the target 12; the "=9+3=12" of #268)
    24  Chiron 24d09.7'                                    (the cascade 24, the seed residue 24)
    26  Venus 26d18.4', Vesta 26d15.7'                     (the 137-map multiplier)
    25  Ceres 25d38.2'  and  4  Pluto 4d36.0'              (two of the four sovereign anchors 4, 9, 25, 30)
    18  the minutes of Venus 26d18'
     8  the minutes of Neptune 1d08'
    30  the minutes of Mercury 20d29.6' (rounds to 30)
  and in the event itself: Feb 28 to Mar 3 = 3 days, Mar 3 to Easter = 33 days, Saros 133.
  Moon's 12 is forced (Sun and Moon share the degree at the full moon), so it is not counted as a second hit.

HOW OFTEN A CHART WITHOUT ANY OF THIS WOULD DO THE SAME (exact, not simulated): the printed degree is any of 0..29
  and the printed minute any of 0..59, so a degree hits with probability 11/30 and a minute with 16/60.
  Counted: 14 degrees (Moon's left out) and 15 minutes. Hits: 7 degrees (12 twice -- Sun and Pallas -- 26 twice,
  4, 24, 25) and 3 minutes (18, 8, 30) = 10. Expected 9.13. The chance of 10 or more is 0.43.
  So the chart carries these numbers and a random chart carries about as many: the count does not separate them.

FALSIFICATION: any assertion failing.
"""
import json
import pathlib
from fractions import Fraction
from math import comb

ROOT = pathlib.Path(__file__).resolve().parents[2]
J = json.load(open(ROOT / "records" / "real_chart_2026_03_03_nasa.json"))
OWNER = {3, 4, 8, 9, 12, 13, 18, 21, 24, 25, 26, 30, 32, 33, 37, 43}
assert len(OWNER) == 16 and OWNER == {4, 9, 25, 30} | {3, 12, 21, 30} | {8, 13, 24} | {18, 24, 32} | {26, 37, 33, 43}

printed = {}
for name, v in J["bodies"].items():
    x = v["ObsEcLon"]
    d, m = int(x % 30), round((x % 30 - int(x % 30)) * 60)
    if m == 60:
        d, m = d + 1, 0
    printed[name] = (d, m)
assert printed == {"Sun": (12, 54), "Moon": (12, 52), "Mercury": (20, 30), "Venus": (26, 18), "Mars": (0, 42),
                   "Jupiter": (15, 11), "Saturn": (2, 1), "Uranus": (27, 47), "Neptune": (1, 8), "Pluto": (4, 36),
                   "Chiron": (24, 10), "Ceres": (25, 38), "Pallas": (12, 20), "Juno": (22, 14), "Vesta": (26, 16)}

where = {}
for name, (d, m) in printed.items():
    if d in OWNER:
        where.setdefault(d, []).append(name + " (degree)")
    if m in OWNER:
        where.setdefault(m, []).append(name + " (minute)")
assert where == {12: ["Sun (degree)", "Moon (degree)", "Pallas (degree)"], 26: ["Venus (degree)", "Vesta (degree)"],
                 4: ["Pluto (degree)"], 24: ["Chiron (degree)"], 25: ["Ceres (degree)"],
                 30: ["Mercury (minute)"], 18: ["Venus (minute)"], 8: ["Neptune (minute)"]}

# Moon's degree is forced by the Sun's at the opposition
assert abs(((J["bodies"]["Moon"]["ObsEcLon"] - J["bodies"]["Sun"]["ObsEcLon"]) % 360) - 180) < 0.04
deg_hits = sum(1 for n, (d, m) in printed.items() if n != "Moon" and d in OWNER)
min_hits = sum(1 for n, (d, m) in printed.items() if m in OWNER)
assert (deg_hits, min_hits) == (7, 3)
n_deg, n_min = 14, 15
p_deg, p_min = Fraction(len([x for x in OWNER if x <= 29]), 30), Fraction(len(OWNER), 60)
assert (p_deg, p_min) == (Fraction(11, 30), Fraction(4, 15))
expected = n_deg * p_deg + n_min * p_min
assert round(float(expected), 2) == 9.13


def binom(n, p):
    return [comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]


a, b = binom(n_deg, p_deg), binom(n_min, p_min)
dist = [sum(a[i] * b[k - i] for i in range(len(a)) if 0 <= k - i < len(b)) for k in range(n_deg + n_min + 1)]
assert abs(float(sum(dist)) - 1) < 1e-12
p_ge = float(sum(dist[deg_hits + min_hits:]))
assert abs(p_ge - 0.4321) < 0.0005 and deg_hits + min_hits == 10

# the event numbers
import datetime as dt
assert (dt.date(2026, 3, 3) - dt.date(2026, 2, 28)).days == 3 and (dt.date(2026, 4, 5) - dt.date(2026, 3, 3)).days == 33

if __name__ == "__main__":
    print(f"chart numbers that are the owner's: {sorted(where)}; hits {deg_hits + min_hits}, expected {float(expected):.2f}, chance of >= {deg_hits + min_hits}: {p_ge:.2f}")
