"""
Ulam spiral mapped through the GF(37) framework.

Standard Ulam construction: integers placed in a square spiral starting from 1
at center, moving right. Each cell is classified by:
  - prime / composite
  - digital root (DR)
  - residue mod 37
  - 137-map orbit: f(n) = (137 * n) mod 37 = (26 * n) mod 37
  - sovereign anchor: {4, 9, 25, 30} in Z/37Z
  - DR=7 prime (the primary filter in DualityVerifier)
"""

import math
from typing import List, Tuple, Dict, Optional


SOVEREIGN_ANCHORS_37 = {4, 9, 25, 30}

# Orbit under 137-map (multiply by 26, order 3)
# Each non-zero residue mod 37 belongs to one of 12 three-cycles
def _build_137_orbits():
    orbits = {}
    seen = set()
    for start in range(1, 37):
        if start in seen:
            continue
        cycle = []
        n = start
        for _ in range(3):
            cycle.append(n)
            seen.add(n)
            n = (26 * n) % 37
        for elem in cycle:
            orbits[elem] = tuple(cycle)
    return orbits

_ORBITS_137 = _build_137_orbits()


def digital_root(n: int) -> int:
    n = abs(n)
    if n == 0:
        return 0
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def ulam_coordinates(n: int) -> Tuple[int, int]:
    """Return (col, row) of integer n in the Ulam spiral (1 at origin)."""
    if n == 1:
        return (0, 0)
    # Layer k contains numbers from (2k-1)^2 + 1 to (2k+1)^2
    k = math.ceil((math.sqrt(n) - 1) / 2)
    side = 2 * k
    start = (2 * k - 1) ** 2 + 1

    pos = n - start
    # Four sides of length `side`
    if pos < side:            # bottom edge: moving right, then up on last
        return (k - side + pos, -k)
    pos -= side
    if pos < side:            # left edge going up
        return (-k, -k + pos)
    pos -= side
    if pos < side:            # top edge going right
        return (-k + pos, k)
    pos -= side
    return (k, k - pos)      # right edge going down


def classify(n: int) -> Dict:
    dr = digital_root(n)
    residue = n % 37
    prime = is_prime(n)
    orbit = _ORBITS_137.get(residue) if residue != 0 else None
    sovereign = residue in SOVEREIGN_ANCHORS_37
    dr7_prime = prime and dr == 7
    col, row = ulam_coordinates(n)
    return {
        "n": n,
        "col": col,
        "row": row,
        "dr": dr,
        "mod37": residue,
        "prime": prime,
        "dr7_prime": dr7_prime,
        "sovereign": sovereign,
        "orbit_137": orbit,
    }


def build_spiral(limit: int) -> List[Dict]:
    return [classify(n) for n in range(1, limit + 1)]


def render_text(limit: int = 121, mark_primes: bool = True) -> None:
    """
    Print the Ulam spiral as text up to limit numbers.
    Symbols:
      [P] DR=7 prime
       p  other prime
       S  sovereign anchor (mod 37 ∈ {4,9,25,30})
       .  composite
    """
    cells = build_spiral(limit)
    if not cells:
        return
    cols = [c["col"] for c in cells]
    rows = [c["row"] for c in cells]
    min_c, max_c = min(cols), max(cols)
    min_r, max_r = min(rows), max(rows)

    grid = {}
    for c in cells:
        grid[(c["col"], c["row"])] = c

    print(f"\n=== Ulam Spiral (1 to {limit}) ===")
    print("  [P] = DR=7 prime   p = prime   S = sovereign mod 37   . = other\n")

    for r in range(max_r, min_r - 1, -1):
        row_str = []
        for col in range(min_c, max_c + 1):
            cell = grid.get((col, r))
            if cell is None:
                row_str.append("  . ")
            elif cell["dr7_prime"]:
                row_str.append(f"[{cell['n']:>2}]")
            elif cell["prime"]:
                row_str.append(f" {cell['n']:>2} ")
            elif cell["sovereign"]:
                row_str.append(f" S{cell['n']:>2}")
            else:
                row_str.append("  . ")
        print(" ".join(row_str))


def dr_distribution(limit: int = 1000) -> Dict[int, int]:
    """Count primes by digital root in Ulam spiral up to limit."""
    counts = {dr: 0 for dr in range(1, 10)}
    for n in range(2, limit + 1):
        if is_prime(n):
            counts[digital_root(n)] += 1
    return counts


def sovereign_primes(limit: int = 1000) -> List[int]:
    """Primes whose mod-37 residue is a sovereign anchor."""
    return [n for n in range(2, limit + 1)
            if is_prime(n) and n % 37 in SOVEREIGN_ANCHORS_37]


def orbit_prime_counts(limit: int = 1000) -> Dict[tuple, int]:
    """Count primes per 137-map orbit."""
    counts: Dict[tuple, int] = {}
    for n in range(2, limit + 1):
        if not is_prime(n):
            continue
        residue = n % 37
        if residue == 0:
            continue
        orbit = _ORBITS_137[residue]
        counts[orbit] = counts.get(orbit, 0) + 1
    return counts


if __name__ == "__main__":
    render_text(limit=121)

    print("\n=== DR distribution of primes to 1000 ===")
    dist = dr_distribution(1000)
    for dr, count in sorted(dist.items()):
        bar = "#" * count
        print(f"  DR={dr}: {count:>4}  {bar}")

    print("\n=== Sovereign-anchor primes (mod 37 ∈ {{4,9,25,30}}) up to 200 ===")
    sp = sovereign_primes(200)
    print(f"  {sp}")
    print(f"  Count: {len(sp)}")

    print("\n=== 137-map orbit prime counts (primes up to 500) ===")
    oc = orbit_prime_counts(500)
    for orbit, count in sorted(oc.items(), key=lambda x: x[0]):
        print(f"  orbit {orbit}: {count} primes")
