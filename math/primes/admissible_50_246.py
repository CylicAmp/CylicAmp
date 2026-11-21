#!/usr/bin/env python3
"""
The minimal admissible 50-tuple (diameter 246) and its 39-element suffix (diameter 182) -- built for the pasted
request of 2026-11-21 (full verification, residue exclusions, 2-4-6 gap architecture, sub-182 test, evidence ledger).

THE TUPLE. The paste names the tuple but does not list it. This one has every property the paste gives -- 50 offsets,
diameter 246, h_12 = 64, the excluded residues 1 by 2, 2 by 3, 2 by 5, 5 by 7, 10 by 11, 11 by 13, and the gap counts
2:12, 4:14, 6:15, 8:4, 10:3, 14:1 -- and it is admissible. OEIS A008407 (minimal diameter of an admissible k-tuple,
https://oeis.org/A008407/b008407.txt, fetched 2026-11-21) gives a(50) = 246 and a(39) = 182, a(38) = 176, so both
diameters are the least possible.

    python3 math/primes/admissible_50_246.py          writes records/evidence_ledger_admissible_50_246.json
"""
import json
import pathlib
from collections import Counter

H50 = (0, 4, 6, 16, 30, 34, 36, 46, 48, 58, 60, 64, 70, 78, 84, 88, 90, 94, 100, 106, 108, 114, 118, 126, 130, 136,
       144, 148, 150, 156, 160, 168, 174, 178, 184, 190, 196, 198, 204, 210, 214, 216, 220, 226, 228, 234, 238, 240,
       244, 246)
SHIFT = H50[11]                                                   # h_12 = 64
H39 = tuple(h - SHIFT for h in H50[11:])                          # the upper 39-element suffix, diameter 182
A008407 = {38: 176, 39: 182, 40: 186, 49: 240, 50: 246, 51: 252}  # OEIS A008407, the least diameters
LEDGER = pathlib.Path(__file__).resolve().parents[2] / "records" / "evidence_ledger_admissible_50_246.json"


def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]


def occupied(H, p):
    return sorted({h % p for h in H})


def admissible(H, pmax=None):
    """no prime p covers every residue class; primes above len(H) cannot, so they need no check"""
    return all(len(occupied(H, p)) < p for p in primes_upto(pmax or len(H)))


def excluded(H, p):
    return sorted(set(range(p)) - set(occupied(H, p)))


def gaps(H):
    return Counter(b - a for a, b in zip(H, H[1:]))


def windows(H, k):
    """diameter of every run of k consecutive offsets"""
    return [H[i + k - 1] - H[i] for i in range(len(H) - k + 1)]


def greedy_sieve(d):
    """greedy residue sieve on 0..d: for each prime in turn remove its least-occupied class (a heuristic: it gives a
    tuple that is admissible, not the largest one)"""
    pool = list(range(0, d + 1))
    for p in primes_upto(d):
        counts = Counter(h % p for h in pool)
        if len(counts) < p:
            continue                                              # a class is already empty
        r = min(range(p), key=lambda c: (counts[c], c))
        pool = [h for h in pool if h % p != r]
    return pool


def ledger():
    out = {}
    for name, H in (("H50", H50), ("H39", H39)):
        out[name] = {
            "size": len(H), "diameter": H[-1] - H[0], "offsets": list(H),
            "admissible_all_p_le_53": admissible(H, 53),
            "excluded_residues": {str(p): excluded(H, p) for p in primes_upto(53)},
            "occupied_count": {str(p): len(occupied(H, p)) for p in primes_upto(53)},
            "gap_counts": {str(g): c for g, c in sorted(gaps(H).items())},
            "share_2_4_6": round(sum(gaps(H)[g] for g in (2, 4, 6)) / (len(H) - 1), 4),
            "least_possible_diameter_A008407": A008407[len(H)],
        }
    out["shift"] = SHIFT
    out["windows_of_39_in_H50"] = windows(H50, 39)
    out["source"] = "OEIS A008407 b-file, https://oeis.org/A008407/b008407.txt (fetched 2026-11-21)"
    return out


if __name__ == "__main__":
    LEDGER.write_text(json.dumps(ledger(), indent=1) + "\n")
    print("wrote", LEDGER)
