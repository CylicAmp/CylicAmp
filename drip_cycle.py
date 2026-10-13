#!/usr/bin/env python3
"""The drip cycle -- in the shape of the owner's example (owner_work #228, 2026-10-12):

    1        1        2        2
    12       21       12       21

Each digit of the number is set against every ordering of the digits. Run at every length:
every pair of the number's digits (both orders, as in the example) and every ordering of all
of its digits. Every number the cycle produces goes through the frameworks.

    python3 drip_cycle.py 246
"""
import importlib.util
import itertools
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("gf37", ROOT / ".claude" / "skills" / "gf37.py")
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)


def arrangements(digits, k):
    out = []
    for combo in itertools.combinations(range(len(digits)), k):
        for perm in itertools.permutations(combo):
            s = "".join(digits[i] for i in perm)
            if s not in out:
                out.append(s)
    return out


def drip(n):
    d = str(n)
    levels = []
    for k in range(2, len(d) + 1):
        lines = []
        for combo in itertools.combinations(range(len(d)), k):
            sub = [d[i] for i in combo]
            arr = ["".join(p) for p in dict.fromkeys(itertools.permutations(sub))]
            for digit in dict.fromkeys(sub):
                for a in arr:
                    lines.append((digit, a))
        levels.append((k, lines))
    return levels


def frame(x):
    v = int(x)
    p = G.prime_profile(v)
    return {"n": v, "mod37": v % 37, "orbit": G.orbit(v), "dr": G.dr(v), "prime": p["prime"],
            "twin": p.get("twin", False), "sophie": p.get("sophie_germain", False),
            "x137": v * 137 % 37, "mod137": v % 137}


def main(n):
    out = []
    for k, lines in drip(n):
        nums = list(dict.fromkeys(a for _, a in lines))
        out.append(f"--- length {k}: {len(lines)} drip lines over {len(nums)} arrangements ---")
        for digit, a in lines:
            out.append(f"{digit}\n{a}\n")
        out.append(f"{'n':>6} {'mod37':>5} {'orbit':>8} {'dr':>3} {'prime':>6} {'twin':>5} {'SG':>5} {'x137%37':>8} {'%137':>5}")
        for a in nums:
            f = frame(a)
            out.append(f"{f['n']:>6} {f['mod37']:>5} {f['orbit']:>8} {f['dr']:>3} {str(f['prime']):>6} "
                       f"{str(f['twin']):>5} {str(f['sophie']):>5} {f['x137']:>8} {f['mod137']:>5}")
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    for arg in sys.argv[1:] or ["246"]:
        print(f"===== DRIP CYCLE: {arg} =====")
        print(main(int(arg)))
