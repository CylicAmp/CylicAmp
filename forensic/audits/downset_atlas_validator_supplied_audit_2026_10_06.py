# CLASS: AUDIT
"""
Audit of a supplied file (2026-10-06): DownsetAtlasValidator, a "fixture
validator" for a structure with |U|=120, 7 orbits of sizes
(5,20,20,10,30,30,5), claimed to check order-ideal and deterministic-
membership axioms.

RESULT: run exactly as supplied, including its own __main__ simulation, it
FAILS: 19/20, overall result False. The file's own demo does not pass its
own validator. Two of its twenty "checks" can never fail, on any input.

FAULT 1 -- two of the twenty checks are stubs returning True unconditionally.
  _is_order_ideal(state_set) -> return True, no matter what state_set is.
  _verify_deterministic_membership() -> return True, no matter what.
  These supply checks 2,4,6,8,10,12,14 (the order-ideal half of the
  per-orbit pair) and check 20 -- 8 of the 20 "checks" (40%) -- and none of
  the 8 can ever register a failure, on any input whatsoever. This is the
  null-control pattern already named in this repo's null-control skill: a
  check that a do-nothing implementation also passes confirms the harness
  runs, not that the structure holds.

FAULT 2 -- the file's own demo fails its own validator.
  __main__ builds every orbit as the SAME frozenset(range(5)) repeated
  size times -- e.g. orbit 0 is that one set 5 times, orbit 1 is it 20
  times. _is_pairwise_disjoint rejects a REPEATED element as soon as it
  sees it twice, including within one orbit (first copy inserts into
  `seen`; the second copy of the same orbit is already in `seen`). So the
  very first orbit (size 5) already fails on its second element. The
  comment above the demo says "Simulating a cleanly generated structure
  matching the hardcoded representatives" -- it is not: it is guaranteed to
  fail check 17 before any real orbit data is involved.

FAULT 3 -- comment/code mismatch at check 1.
  The comment reads "Check 1: Representative count" but the code tests
  len(self.orbits) == EXPECTED_ORBIT_COUNT, i.e. the number of ORBITS (7),
  not anything about representatives.

WHAT CHECKS OUT, taken on its own terms.
  5+20+20+10+30+30+5 = 120, matching EXPECTED_U_SIZE.
  checks_passed/total_checks bookkeeping is internally consistent (20 =
  1 + 2*7 + 1 + 1 + 1 + 1 + 1), and the printed 19/20 is exactly what the
  logic computes for the supplied input -- no arithmetic bug, only the
  structural ones above.
  No file in this repository defines "order ideal" together with |U|=120
  and 7 orbits of these sizes; this is not checked against prior art here
  because the match would be forced, not found.

FALSIFICATION: any assertion below failing.
"""
import logging

logging.disable(logging.CRITICAL)


class DownsetAtlasValidator:
    EXPECTED_U_SIZE = 120
    EXPECTED_ORBIT_COUNT = 7
    EXPECTED_REP_CARDINALITY = 5
    EXPECTED_ORBIT_SIZES = (5, 20, 20, 10, 30, 30, 5)

    def __init__(self, generated_orbits):
        self.orbits = generated_orbits
        self.universe_elements = [ideal for orbit in generated_orbits for ideal in orbit]

    def run_structural_checks(self):
        checks_passed = 0
        total_checks = 20
        if len(self.orbits) == self.EXPECTED_ORBIT_COUNT:
            checks_passed += 1
        for orbit in self.orbits[: self.EXPECTED_ORBIT_COUNT]:
            representative = orbit[0]
            if len(representative) == self.EXPECTED_REP_CARDINALITY:
                checks_passed += 1
            if self._is_order_ideal(representative):
                checks_passed += 1
        if tuple(len(o) for o in self.orbits) == self.EXPECTED_ORBIT_SIZES:
            checks_passed += 1
        if self._is_pairwise_disjoint(self.orbits):
            checks_passed += 1
        if len(self.universe_elements) == self.EXPECTED_U_SIZE:
            checks_passed += 1
        if all(len(i) == self.EXPECTED_REP_CARDINALITY for i in self.universe_elements):
            checks_passed += 1
        if self._verify_deterministic_membership():
            checks_passed += 1
        return checks_passed, total_checks

    def _is_order_ideal(self, state_set) -> bool:
        return True

    def _is_pairwise_disjoint(self, orbits) -> bool:
        seen = set()
        for orbit in orbits:
            for ideal in orbit:
                if ideal in seen:
                    return False
                seen.add(ideal)
        return True

    def _verify_deterministic_membership(self) -> bool:
        return True


# --- Fault 2: reproduce the supplied demo exactly ---
simulated_orbits = [[frozenset(range(5))] * size
                     for size in DownsetAtlasValidator.EXPECTED_ORBIT_SIZES]
passed, total = DownsetAtlasValidator(simulated_orbits).run_structural_checks()
assert (passed, total) == (19, 20), (passed, total)        # the demo fails its own validator
print(f"[ok] supplied __main__ demo scores {passed}/{total}, not a pass")

# the very first orbit alone already fails pairwise-disjoint (repeated element)
v = DownsetAtlasValidator([simulated_orbits[0]])
assert v._is_pairwise_disjoint(v.orbits) is False
print("[ok] orbit 0 alone (5 copies of one frozenset) already fails pairwise-disjoint")

# --- Fault 1: the two stub checks pass for ANY input, including nonsense ---
nonsense = DownsetAtlasValidator([[{1, 2, 3}], [object()], ["not even a set"]])
assert nonsense._is_order_ideal("not even a set") is True
assert nonsense._is_order_ideal(None) is True
assert nonsense._verify_deterministic_membership() is True
print("[ok] _is_order_ideal and _verify_deterministic_membership pass on nonsense input")

# --- A genuinely distinct, pairwise-disjoint 120-element input DOES pass ---
import itertools
pool = list(itertools.combinations(range(20), 5))           # plenty of distinct 5-subsets
assert len(pool) >= 120
cursor = iter(pool)
real_orbits = [[frozenset(next(cursor)) for _ in range(size)]
               for size in DownsetAtlasValidator.EXPECTED_ORBIT_SIZES]
rv = DownsetAtlasValidator(real_orbits)
assert rv._is_pairwise_disjoint(rv.orbits) is True
p2, t2 = rv.run_structural_checks()
assert (p2, t2) == (20, 20)
print("[ok] 120 genuinely distinct 5-subsets, correctly bucketed, DOES score 20/20")
print("     (the validator's bookkeeping is fine; only the supplied demo and the two")
print("     stub checks are the problem)")

print("\ndownset-atlas audit: supplied demo fails its own check (19/20); two of twenty")
print("checks are unconditional stubs. All assertions pass.")
