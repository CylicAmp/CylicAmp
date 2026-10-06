# CLASS: AUDIT
"""
RECONSTRUCTION, not the original source. The owner's bug report (2026-10-06)
describes a revised DownsetAtlasValidator with fields (poset_parents, a
classifier) and check numbering (17 hashes before 19 checks types) that do
not exist in the file audited in
downset_atlas_validator_supplied_audit_2026_10_06.py. That revised file was
never supplied. This builds the smallest implementation consistent with the
report's own description, to test its three claims directly rather than
wait on the source.

THREE CLAIMS, ALL REPRODUCED BELOW:
  1. Stale universe snapshot: mutating self.orbits after construction does
     not change self.universe_elements or self.classifier, because both
     were built once at __init__ time from plain (mutable) list/dict copies
     that hold old references.
  2. Mutable member crash: pairwise-disjoint hashes an element (`in seen`)
     before any type check runs, so a plain (unhashable) set raises
     TypeError instead of being rejected cleanly.
  3. Iterator-consuming parent check: the constructor accepts a live
     iterator as a poset_parents value because it validates only the outer
     dict (`isinstance(poset_parents, dict) and len(...) == len(orbits)`),
     never what each value actually is. The real fault is there, at
     construction; its visible symptom is that the SAME check, called
     twice on the same object with no data change, gives two different
     answers -- True, then False -- because the first call permanently
     consumes the iterator. Whether that reads as a false pass or a false
     failure depends only on which call happens to run first.

THE THREE REPAIRS, APPLIED AND TESTED:
  Freeze orbits into a tuple of tuples of frozensets at construction, so
  mutation after that raises TypeError instead of silently diverging.
  Reject non-frozenset members with a clear error before they reach `in`.
  Normalize every poset_parents value to frozenset(...) once at
  construction (consuming any iterator exactly once, permanently), then
  validate every parent is a universe element, and check the covering
  relation is acyclic.

FALSIFICATION: any assertion below failing.
"""


# =====================================================================
# PART 1: the broken reconstruction, matching the bug report exactly
# =====================================================================

class BrokenValidator:
    def __init__(self, orbits, poset_parents, classifier=None):
        self.orbits = orbits
        # constructor "validates only the outer dictionary"
        assert isinstance(poset_parents, dict) and len(poset_parents) == len(orbits)
        self.poset_parents = poset_parents
        self.universe_elements = [e for orbit in orbits for e in orbit]   # snapshot: no hashing here
        # classifier is supplied, not derived -- matches "update its classifier entry"
        # being something the caller does to an existing structure, and means no
        # member is hashed at construction time; the first hash happens in check 17
        self.classifier = dict(classifier) if classifier is not None else {}

    def check_17_pairwise_disjoint(self):
        seen = set()
        for orbit in self.orbits:
            for ideal in orbit:
                if ideal in seen:              # hashes `ideal` here -- no type check first
                    return False
                seen.add(ideal)
        return True

    def check_19_cardinality_and_domain(self):
        # intends: every universe element has the right size AND is classified
        return all(len(e) == 5 and e in self.classifier for e in self.universe_elements)

    def check_required_parent(self, idx):
        rep = self.orbits[idx][0]
        return any(p in rep for p in self.poset_parents[idx])     # iterates and may exhaust


def test_claim_1_stale_snapshot():
    elems = [frozenset({1, 2, 3, 4, 5}), frozenset({2, 3, 4, 5, 6})]
    orbits = [elems]
    v = BrokenValidator(orbits, {0: frozenset()}, classifier={e: 0 for e in elems})
    before = v.check_19_cardinality_and_domain()
    assert before is True

    bad = frozenset({999})                         # wrong cardinality, not in classifier
    v.orbits[0][1] = bad                            # mutate the live orbit
    v.classifier[bad] = 0                            # "update its classifier entry to 0"

    after_17 = v.check_17_pairwise_disjoint()         # sees the NEW element: no duplicate, passes
    after_19 = v.check_19_cardinality_and_domain()    # sees the OLD snapshot: still "fine"
    assert after_17 is True
    assert after_19 is True                           # FALSE PASS: bad is len 1, never examined here
    assert bad not in v.universe_elements             # the snapshot never saw it
    assert any(len(e) != 5 for e in v.orbits[0])       # the live data is actually wrong
    print("[ok] claim 1 reproduced: check 19 passes on a stale snapshot while orbits[0][1] is len 1")


def test_claim_2_mutable_member_crash():
    orbits = [[frozenset({1, 2, 3}), {4, 5, 6}]]      # second member is a plain mutable set
    v = BrokenValidator(orbits, {0: frozenset()})      # construction succeeds: nothing hashed yet
    try:
        v.check_17_pairwise_disjoint()                  # first hash happens here
        raised = False
    except TypeError:
        raised = True
    assert raised, "expected TypeError: plain set is unhashable, hit before any type check"
    print("[ok] claim 2 reproduced: construction succeeds; check 17 hashes and crashes;")
    print("     check 19 (type check) never runs because check 17 crashed first")


def test_claim_3_iterator_exhaustion():
    # the real fault: construction accepts a bare iterator as a poset_parents value
    v = BrokenValidator([[frozenset({1, 2, 3})]], {0: iter([1])})    # does not raise -- it should
    first = v.check_required_parent(0)                 # consumes the iterator, finds the parent
    second = v.check_required_parent(0)                 # same object, same inputs, now empty
    assert first is True
    assert second is False                                # SAME check, SAME data: different answer
    print("[ok] claim 3 reproduced: construction wrongly accepts a live iterator; the same")
    print("     check on the same unchanged object then returns True, then False")


# =====================================================================
# PART 2: the three repairs, applied, closing all three holes
# =====================================================================

class RepairedValidator:
    def __init__(self, orbits, poset_parents):
        # repair 1: freeze into an immutable nested structure
        self.orbits = tuple(tuple(self._checked_member(e) for e in orbit) for orbit in orbits)
        self.universe_elements = tuple(e for orbit in self.orbits for e in orbit)
        self.classifier = {e: i for i, orbit in enumerate(self.orbits) for e in orbit}
        # repair 3: normalize every parent collection to a frozenset ONCE, consuming any iterator here
        assert isinstance(poset_parents, dict) and len(poset_parents) == len(self.orbits)
        self.poset_parents = {k: frozenset(v) for k, v in poset_parents.items()}
        for idx, parents in self.poset_parents.items():
            for p in parents:
                assert p in self.classifier, f"parent {p} of orbit {idx} is not a universe element"
        # build the orbit-index-level graph: idx -> the orbit index of each parent element
        index_graph = {idx: frozenset(self.classifier[p] for p in parents)
                        for idx, parents in self.poset_parents.items()}
        assert self._is_acyclic(index_graph)

    @staticmethod
    def _checked_member(e):
        # repair 2: reject malformed members BEFORE anything hashes them
        if not isinstance(e, frozenset):
            raise ValueError(f"member {e!r} is not a frozenset; rejected before hashing")
        return e

    @staticmethod
    def _is_acyclic(index_graph):
        """index_graph: orbit index -> frozenset of orbit indices it depends on."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {k: WHITE for k in index_graph}

        def visit(k):
            if color.get(k) == BLACK:
                return True
            if color.get(k) == GRAY:
                return False                       # back edge: cycle
            color[k] = GRAY
            for j in index_graph.get(k, ()):
                if j in index_graph and not visit(j):
                    return False
            color[k] = BLACK
            return True

        return all(visit(k) for k in index_graph)

    def check_17_pairwise_disjoint(self):
        seen = set()
        for orbit in self.orbits:
            for ideal in orbit:
                if ideal in seen:
                    return False
                seen.add(ideal)
        return True

    def check_19_cardinality_and_domain(self):
        return all(len(e) == 5 and e in self.classifier for e in self.universe_elements)


def test_repair_1_freeze_blocks_mutation():
    orbits = [[frozenset({1, 2, 3, 4, 5}), frozenset({2, 3, 4, 5, 6})]]
    v = RepairedValidator(orbits, {0: []})
    try:
        v.orbits[0][1] = frozenset({999})
        raised = False
    except TypeError:
        raised = True
    assert raised, "frozen (tuple-of-tuples) orbits must reject item assignment"
    print("[ok] repair 1: orbits[0][1] = ... now raises TypeError, mutation is blocked")


def test_repair_2_rejects_mutable_member_cleanly():
    orbits = [[frozenset({1, 2, 3}), {4, 5, 6}]]
    try:
        RepairedValidator(orbits, {0: []})
        raised_type = None
    except ValueError:
        raised_type = ValueError
    except TypeError:
        raised_type = TypeError
    assert raised_type is ValueError, "must fail with a clear, typed rejection, not TypeError from hashing"
    print("[ok] repair 2: the plain set is rejected with ValueError before it ever reaches `in seen`")


def test_repair_3_iterator_normalized_and_validated():
    base, dependent = frozenset({1, 2, 3}), frozenset({4, 5, 6})
    v = RepairedValidator([[base], [dependent]], {0: [], 1: iter([base])})
    first = base in v.poset_parents[1]
    second = base in v.poset_parents[1]           # reusable now, not exhausted
    assert v.poset_parents[1] == frozenset({base})
    assert first == second is True
    # an unknown parent (not a universe element) is now caught at construction, not silently passed
    try:
        RepairedValidator([[frozenset({1, 2, 3})]], {0: [frozenset({999})]})
        caught = False
    except AssertionError:
        caught = True
    assert caught, "a parent outside the universe must be rejected at construction"
    print("[ok] repair 3: parent collections are normalized once and validated against the universe")


def test_repair_catches_a_cycle():
    # orbit 1 lists orbit 0 as parent and orbit 0 lists orbit 1 as parent: a 2-cycle
    orbits = [[frozenset({1, 2, 3})], [frozenset({4, 5, 6})]]
    try:
        RepairedValidator(orbits, {0: [frozenset({4, 5, 6})], 1: [frozenset({1, 2, 3})]})
        caught = False
    except AssertionError:
        caught = True
    assert caught, "a 2-cycle in the parent relation must be rejected"
    print("[ok] repair 3b: a cyclic parent relation is rejected at construction")


def test_repaired_validator_passes_on_good_input():
    orbits = [[frozenset({1, 2, 3, 4, 5})], [frozenset({2, 3, 4, 5, 6})]]
    v = RepairedValidator(orbits, {0: [], 1: [frozenset({1, 2, 3, 4, 5})]})
    assert v.check_17_pairwise_disjoint() is True
    assert v.check_19_cardinality_and_domain() is True
    print("[ok] repaired validator still passes genuinely well-formed input")


def self_test():
    test_claim_1_stale_snapshot()
    test_claim_2_mutable_member_crash()
    test_claim_3_iterator_exhaustion()
    test_repair_1_freeze_blocks_mutation()
    test_repair_2_rejects_mutable_member_cleanly()
    test_repair_3_iterator_normalized_and_validated()
    test_repair_catches_a_cycle()
    test_repaired_validator_passes_on_good_input()
    print("\nAll self-tests passed.")
    print("RESULT: all three reported failure modes reproduce exactly as described")
    print("        against this reconstruction, and the three stated repairs close")
    print("        all three, verified against both bad and good input.")
    print("SCOPE: this is a reconstruction from the bug report, not an audit of the")
    print("       owner's actual revised file, which has not been supplied.")


if __name__ == "__main__":
    self_test()
