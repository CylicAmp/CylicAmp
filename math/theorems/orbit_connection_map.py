"""
Orbit Connection Map — Full Library Coverage

Scans every theorem file and maps which GF(37) orbits each one touches.
Finds files that bridge multiple orbits — the connective tissue of GF(37).
"""

import os

P = 37
ORBITS = {
    'IC':               frozenset({1, 10, 26}),
    'SOVEREIGN_SPIRAL': frozenset({3, 4, 30}),
    'D7':               frozenset({7, 33, 34}),
    'SA_ORB':           frozenset({9, 12, 16}),
    'ORBIT_11':         frozenset({11, 27, 36}),
    'OUTLIER_ORB':      frozenset({21, 25, 28}),
    'DARK_A':           frozenset({2, 15, 20}),
    'NQR_5':            frozenset({5, 13, 19}),
    'TESLA_ORB':        frozenset({6, 8, 23}),
    'NQR_14':           frozenset({14, 29, 31}),
    'NQR_17':           frozenset({17, 22, 35}),
    'SEED_ORB':         frozenset({18, 24, 32}),
}

THEOREMS_DIR = os.path.join(os.path.dirname(__file__))


def build_map():
    files = sorted([f for f in os.listdir(THEOREMS_DIR) if f.endswith('.py')
                    and f != os.path.basename(__file__)])

    # orbit -> list of files that mention it
    orbit_to_files = {o: [] for o in ORBITS}

    # file -> list of orbits it mentions
    file_to_orbits = {}

    for f in files:
        path = os.path.join(THEOREMS_DIR, f)
        try:
            content = open(path).read()
        except Exception:
            continue
        touched = [o for o in ORBITS if o in content]
        file_to_orbits[f] = touched
        for o in touched:
            orbit_to_files[o].append(f)

    return orbit_to_files, file_to_orbits


def files_bridging(orbit_a, orbit_b, file_to_orbits):
    return sorted([f for f, orbits in file_to_orbits.items()
                   if orbit_a in orbits and orbit_b in orbits])


def summarise():
    orbit_to_files, file_to_orbits = build_map()

    print("=" * 62)
    print("Orbit Connection Map — Full Library")
    print("=" * 62)
    print()
    print("  ORBIT COVERAGE (files mentioning each orbit):")
    for orbit, flist in sorted(orbit_to_files.items(), key=lambda x: -len(x[1])):
        print(f"    {orbit:<20} {len(flist):3d} files")

    print()
    print("  KEY BRIDGES (files connecting two orbits):")
    bridges = [
        ('SEED_ORB', 'IC'),
        ('SEED_ORB', 'NQR_5'),
        ('IC', 'D7'),
        ('SOVEREIGN_SPIRAL', 'SEED_ORB'),
        ('TESLA_ORB', 'SEED_ORB'),
    ]
    for a, b in bridges:
        bridging = files_bridging(a, b, file_to_orbits)
        print(f"    {a} + {b}: {len(bridging)} files")

    print()
    print("  MOST CONNECTED FILES (touching most orbits):")
    ranked = sorted(file_to_orbits.items(), key=lambda x: -len(x[1]))
    for f, orbits in ranked[:10]:
        print(f"    {f}: {len(orbits)} orbits")


if __name__ == "__main__":
    summarise()
