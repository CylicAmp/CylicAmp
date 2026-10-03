# CLASS: AUDIT
"""
Audit of the supplied paper (2026-10-02): "Forensic Stream Reconstruction: A
Causal and Provenance-Preserving Framework for Discontinuous Conversational
Telemetry", M. W. Song, MWS Verification Protocol v1.0.0 -- checked against
the two implementations in this repo: forensic/mdh/pipeline.py (+ branching,
jcs, validate; tests test_mdh.py) and forensic/mdh/strict_linker.py.

The formulas did not survive the paste: "governed by the fundamental law:",
Invariants 1-4 and section 2.1 are followed by nothing.  Only the text is
audited.

IMPLEMENTED AND TESTED IN THE REPO (the paper's claims hold there)
 Inv. 1 transport closure      test_AT01_rechunking_invariance, test_AT02_utf8_split
 Inv. 2 provenance to bytes     test_AT04_provenance_to_bytes
 Inv. 3 causal feasibility      test_AT06_causal_admissibility; strict_linker A1/A2
 Inv. 5 ceiling C <= E          test_AT12_certainty_ceiling; strict_linker A5
 RFC 8785 / quarantine          test_AT14_AT16, test_AT17 (source hash kept)
 Discarded edges retained       test_AT10; strict_linker A3 (and rejected edges)

CORRECTIONS
 1. Invariant 4 (inversion M = W + eps).  Exact only when a SPANNING
    arborescence exists; with a vertex that has no admissible in-edge it
    selects the empty set.  The repo uses maximum branching for that reason
    (counterexample asserted below).  eps is not needed for exactness.  And
    Invariant 3 makes the graph a DAG, on which the maximum tree is simply
    each node's best parent: Edmonds' contraction never fires
    (strict_linker v3; checked against brute force on 59 random DAGs, 22 with
    ties).
 2. The graph state space in section 2 lists four states (SINGLETON,
    CANDIDATE, VERIFIED, UNRESOLVED); the text itself uses AMBIGUOUS
    (Inv. 5) and QUARANTINED (AT-17).  The implemented space has six, with
    precedence QUARANTINED > UNRESOLVED > AMBIGUOUS > VERIFIED > CANDIDATE >
    SINGLETON.
 3. Tie rule W(T1) = W(T2) -> AMBIGUOUS.  On a DAG this holds iff some node
    has two equal-weight best parents, so it is checkable per node;
    implemented in strict_linker v3 with the canonical tuple tie-break.
 4. "|V| > 1 and no edges -> UNRESOLVED" and the table's AT-13 ("multi-node
    disconnected graph ... certainty 0.0, UNRESOLVED") cannot both describe
    the engine: components are weakly connected components, so a component
    with no edges has one vertex and is SINGLETON (implemented AT-07).  The
    implemented AT-13 is a different test (edge-free certainty = min event
    certainty, 0.5 in the fixture).
 5. Test numbering does not match the implemented suite: the paper's AT-04
    (truncated tail) is the repo's AT-03; its AT-10 (equal timestamps) is the
    repo's AT-06; its AT-06 (asymmetric schema keys) has no counterpart; its
    AT-13 differs (item 4).  FIX-01..FIX-08 do not exist in the repo.  AT-08
    is undefined.
 6. Section 5 reverses edge direction.  With (u, v) meaning "u imports v",
    out-degree 0 means u imports nothing (a foundation), not "unimported by
    downstream files"; the files nothing imports have IN-degree 0.  And on
    this repo the rule cannot partition anything: 933 math modules, 34
    import edges, and all 7 files in math/lemmas have in-degree 0 (nothing
    imports them).  N = 237 is not this repo's count.
 7. Reference: Tarjan 1972 (SIAM J. Comput. 1(2) 146-160) is depth-first
    search / strongly connected components.  The efficient optimum-branching
    algorithm is Tarjan 1977, "Finding optimum branchings", Networks 7, 25-35.
 8. Wording: "grooming grooming state space" (section 2) and "groomer can
    apply" (section 5) stand where "the state space" and "one can apply"
    belong.
 9. Not tested by any code here: the abstract's "operational benchmarks"
    (no numbers are given), and the claims about batchexecute / HTTP-200
    gRPC error envelopes, soft locks and classifiers.

FALSIFICATION: any assertion failing.
"""
import ast
import collections
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, ROOT)
from forensic.mdh.branching import maximum_branching  # noqa: E402
from forensic.mdh import strict_linker as S            # noqa: E402
from forensic.mdh.pipeline import STATE_PRECEDENCE     # noqa: E402

# 1. inversion needs a spanning arborescence; maximum branching does not
edges = [("r", "a", 1.0, "r->a"), ("a", "c", 5.0, "a->c"), ("r", "c", 4.0, "r->c")]
assert maximum_branching(["r", "a", "b", "c"], edges) == {"r->a", "a->c"}
reach = S._descendants([(u, v) for u, v, _, _ in edges], "r") | {"r"}
assert "b" not in reach                                          # 'b' unreachable: no spanning tree exists

# 2. state space
assert STATE_PRECEDENCE == ["QUARANTINED", "UNRESOLVED", "AMBIGUOUS", "VERIFIED", "CANDIDATE", "SINGLETON"]
assert {"AMBIGUOUS_COMPONENT", "QUARANTINED"} <= {s.value for s in S.GraphComponentStatus}

# 4. a no-edge component is a single vertex
assert S._weak_components(list("abc"), []) == [{"a"}, {"b"}, {"c"}]

# 5. implemented test names
names = re.findall(r"def (test_AT\d+\w*)", open(os.path.join(ROOT, "forensic/mdh/test_mdh.py")).read())
assert "test_AT03_incomplete_tail_is_isolated" in names and "test_AT06_causal_admissibility" in names
assert "test_AT13_edge_free_component_certainty_is_min_event" in names
assert not any("AT08" in n for n in names)
assert not any("FIX-0" in open(os.path.join(dp, f)).read()
               for dp, _, fs in os.walk(os.path.join(ROOT, "forensic")) for f in fs
               if f.endswith(".py") and not f.startswith("audit_paper"))

# 6. direction and the repo's import graph
toy = [("theorem", "lemma")]                                 # theorem imports lemma
assert [n for n in ("theorem", "lemma") if not any(u == n for u, _ in toy)] == ["lemma"]    # out-degree 0
assert [n for n in ("theorem", "lemma") if not any(v == n for _, v in toy)] == ["theorem"]  # in-degree 0
mods = {}
for d in ("math/theorems", "math/lemmas", "math/primes"):
    for f in os.listdir(os.path.join(ROOT, d)):
        if f.endswith(".py"):
            mods[f[:-3]] = os.path.join(ROOT, d, f)
E = set()
for m, p in mods.items():
    try:
        t = ast.parse(open(p).read())
    except SyntaxError:
        continue
    for n in ast.walk(t):
        xs = [a.name.split(".")[-1] for a in n.names] if isinstance(n, ast.Import) else \
             ([n.module.split(".")[-1]] if isinstance(n, ast.ImportFrom) and n.module else [])
        E |= {(m, x) for x in xs if x in mods and x != m}
inn = collections.Counter(v for _, v in E)
lemmas = [m for m, p in mods.items() if "/math/lemmas/" in p]
assert len(lemmas) == 7 and all(inn[m] == 0 for m in lemmas)
assert len(E) < len(mods) / 10

if __name__ == "__main__":
    print(f"paper audit 2026-10-02: all assertions pass; import graph {len(mods)} modules, {len(E)} edges")
