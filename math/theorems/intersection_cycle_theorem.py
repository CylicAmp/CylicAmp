"""
Intersection Cycle Theorem — GF(37)

The 3-cycle (3, 4, 30) under the 137-map f(n)=26n mod 37 is the unique cycle
where every element belongs to a sovereign class (SA or ST).

Three elements, three distinct sovereign roles:
  3 ∈ ST        — sovereign target
  4 ∈ SA        — sovereign anchor
  30 ∈ SA ∩ ST  — the unique intersection node: both anchor and target

No other 3-cycle has all elements in SA ∪ ST.

Orbit direction: 3 → 4 → 30 → 3

Proof: verified by exhaustive check over all 12 three-cycles.
"""

SA         = frozenset({4, 9, 25, 30})
ST         = frozenset({3, 12, 21, 30})
CB         = frozenset({8, 13, 24})
PR         = frozenset({2, 5, 13, 15, 17, 18, 19, 20, 22, 24, 32, 35})
ORBIT_11   = frozenset({11, 27, 36})
TESLA_FLOW = 6
SOVEREIGN  = SA | ST   # {3, 4, 9, 12, 21, 25, 30}


def f137(n):
    return (n * 26) % 37


def get_all_cycles():
    seen = set(); cycles = []
    for start in range(1, 37):
        if start not in seen:
            c = [start]; x = f137(start)
            while x != start:
                c.append(x); x = f137(x)
            cycles.append(tuple(sorted(c))); seen.update(c)
    return cycles


ALL_CYCLES = get_all_cycles()
assert len(ALL_CYCLES) == 12

# ── The sovereign cycle ───────────────────────────────────────────────────────

SOVEREIGN_CYCLE = (3, 4, 30)

assert SOVEREIGN_CYCLE in ALL_CYCLES

# Each element has a distinct sovereign role
assert 3 in ST  and 3 not in SA            # pure target
assert 4 in SA  and 4 not in ST            # pure anchor
assert 30 in SA and 30 in ST               # the intersection node

# Every element in the cycle is sovereign
assert all(v in SOVEREIGN for v in SOVEREIGN_CYCLE)

# The 137-map orbit direction
assert f137(3)  == 4                       # target → anchor
assert f137(4)  == 30                      # anchor → intersection
assert f137(30) == 3                       # intersection → target (cycle closes)

# ── Uniqueness ────────────────────────────────────────────────────────────────

# Count how many cycles have ALL elements in SA∪ST
sovereign_cycles = [c for c in ALL_CYCLES if all(v in SOVEREIGN for v in c)]
assert len(sovereign_cycles) == 1          # exactly one
assert sovereign_cycles[0] == SOVEREIGN_CYCLE

# ── Additional structure ──────────────────────────────────────────────────────

# SA∩ST = {30} — the intersection node is unique in the entire field
assert SA & ST == frozenset({30})
assert 30 in SOVEREIGN_CYCLE

# Three cycles touch at least one SA and one ST node
cycles_touching_both = [c for c in ALL_CYCLES
                        if any(v in SA for v in c) and any(v in ST for v in c)]
assert len(cycles_touching_both) == 3
# (3,4,30), (9,12,16), (21,25,28) — but only (3,4,30) has ALL elements sovereign
# The other two have one non-sovereign element each: 16 and 28
assert (3, 4, 30)   in cycles_touching_both
assert (9, 12, 16)  in cycles_touching_both   # 16 is unclassified
assert (21, 25, 28) in cycles_touching_both   # 28 is unclassified

# Sum = 37 (the prime itself — this cycle is in Group A)
assert sum(SOVEREIGN_CYCLE) == 37

# SOVEREIGN = {3,4,9,12,21,25,30} has 7 elements covering all SA and ST members
assert SOVEREIGN == frozenset({3, 4, 9, 12, 21, 25, 30})
assert len(SOVEREIGN) == len(SA) + len(ST) - 1   # -1 for the shared node 30

# The other cycles that contain sovereign elements but are NOT all-sovereign:
partial_sovereign = [c for c in ALL_CYCLES
                     if any(v in SOVEREIGN for v in c)
                     and not all(v in SOVEREIGN for v in c)]
# These are the "partial" cycles — they touch but don't fully belong
assert all(SOVEREIGN_CYCLE != c for c in partial_sovereign)


if __name__ == "__main__":
    print("Intersection Cycle Theorem — GF(37)")
    print("=" * 50)
    print()
    print("The sovereign cycle:")
    print(f"  {SOVEREIGN_CYCLE}  sum={sum(SOVEREIGN_CYCLE)}")
    print(f"  3  ∈ ST  (sovereign target)")
    print(f"  4  ∈ SA  (sovereign anchor)")
    print(f"  30 ∈ SA∩ST  (unique intersection node)")
    print()
    print("Orbit: 3 → 4 → 30 → 3")
    print()
    print("All 12 cycles — sovereign elements marked:")
    for c in ALL_CYCLES:
        labels = []
        for v in c:
            if v in SA and v in ST: labels.append(f"{v}(SA∩ST)")
            elif v in SA:           labels.append(f"{v}(SA)")
            elif v in ST:           labels.append(f"{v}(ST)")
            elif v in CB:           labels.append(f"{v}(CB)")
            elif v in PR:           labels.append(f"{v}(PR)")
            elif v in ORBIT_11:     labels.append(f"{v}(O11)")
            else:                   labels.append(f"{v}")
        mark = " ← SOVEREIGN CYCLE" if c == SOVEREIGN_CYCLE else ""
        print(f"  {str(c):<14}  sum={sum(c)}  {labels}{mark}")
    print()
    print(f"All-sovereign cycle (all elements in SA∪ST): {sovereign_cycles}")
    print(f"Cycles touching both SA and ST ({len(cycles_touching_both)}): {cycles_touching_both}")
    print(f"  (3,4,30) is the unique all-sovereign one; 16 and 28 are unclassified")
    print()
    print("All assertions pass. Everything connects through prime 37.")
