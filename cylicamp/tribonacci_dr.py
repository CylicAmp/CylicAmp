"""
Tribonacci Digital Root Cycle — Period 39.

Instead of summing the last 2 terms (Fibonacci), this sums
the last 3 terms and collapses to a digital root (Tribonacci DR).

The sequence [2,4,7,...] has period 39: after 39 steps it repeats.
Displayed in rows of 10 to reveal block structure.
"""


import sys as _sys, pathlib as _pl
_sys.path.append(str(next(p for p in _pl.Path(__file__).resolve().parents if (p / "functions.py").exists())))
from functions import dr9_iter as dr


CYCLE = [2, 4, 7, 4, 6, 8, 9, 5, 4, 9, 9, 4, 4, 8, 7, 1, 7, 6, 5, 9,
         2, 7, 9, 9, 7, 7, 5, 1, 4, 1, 6, 2, 9, 8, 1, 9, 9, 1, 1]


def show_triples(seq: list, count: int = 8) -> None:
    """Show Tribonacci DR triples: DR(a+b+c) for consecutive sliding window."""
    print("Tribonacci DR triples:\n")
    for i in range(count):
        a, b, c = seq[i], seq[i + 1], seq[i + 2]
        s = dr(a + b + c)
        print(f"  {a} + {b} + {c} = {a + b + c} → DR {s}")


def show_cycle_grid(cycle: list, cols: int = 10) -> None:
    """Display the cycle in rows of `cols` to reveal block structure."""
    print(f"\nTribonacci Digital Root Cycle (Period {len(cycle)})\n")
    for i in range(0, len(cycle), cols):
        row = cycle[i:i + cols]
        print(" ".join(f"{x:2}" for x in row))


def run_analysis() -> None:
    print(f"Cycle length: {len(CYCLE)}")
    print(f"First 20: {CYCLE[:20]}\n")
    show_triples(CYCLE, 8)
    show_cycle_grid(CYCLE, 10)


if __name__ == "__main__":
    run_analysis()
