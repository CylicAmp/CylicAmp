"""Acceptance tests. Run: python3 -m pytest forensic/mdh -q

Each AT-nn test encodes the gate as stated in the supplied spec (Stages 1-6).
AT-08 is referenced by the spec's numbering but never defined in it, so there
is no test for it."""
import hashlib
import itertools
import json
import random

import pytest

from forensic.mdh.branching import maximum_branching
from forensic.mdh.jcs import CanonicalizationError, canonicalize
from forensic.mdh.pipeline import Deframer, STATE_PRECEDENCE, reconstruct
from forensic.mdh.validate import validate


def nd(*objs, tail=b""):
    return b"".join(json.dumps(o, ensure_ascii=False).encode() + b"\n" for o in objs) + tail


def run(raw, chunk=None, **kw):
    chunks = [raw] if chunk is None else [raw[i:i + chunk] for i in range(0, len(raw), chunk)]
    rec, text = reconstruct(chunks, "s", **kw)
    assert validate(rec, raw) == [], validate(rec, raw)
    return rec, text


CHAIN = nd({"id": "a", "t": 1, "q": 1}, {"id": "b", "t": 2, "q": 2, "parent": "a"},
           {"id": "c", "t": 3, "q": 3, "parent": "b"})


def state_of(rec, event_id):
    for s in rec["states"]:
        if any(x.split("#")[0] == event_id for x in s["event_refs"]):
            return s


# -- Stage 1 ----------------------------------------------------------------

def test_AT01_rechunking_invariance():
    raw = CHAIN + nd({"id": "d", "t": 4, "corr": "k"}, {"id": "e", "t": 5, "corr": "k"})
    texts = {run(raw, chunk=c)[1] for c in (1, 2, 3, 7, 64, None)}
    assert len(texts) == 1


def test_AT02_utf8_split_across_chunks():
    raw = nd({"id": "déjà-vu", "t": 1}, {"id": "日本", "t": 2, "parent": "déjà-vu"})
    one = run(raw)[1]
    for c in range(1, 8):                     # every split point, incl. inside multibyte chars
        assert run(raw, chunk=c)[1] == one
    assert "MALFORMED_UTF8" not in one


def test_AT03_incomplete_tail_is_isolated():
    base, _ = run(CHAIN)
    rec, _ = run(CHAIN + b'{"id":"x","t":9')
    assert rec["tail"]["tail_state"] == "INCOMPLETE" and rec["tail"]["tail_length"] == 15
    assert rec["frames"] == base["frames"] and rec["events"] == base["events"]


# -- Stage 2 ----------------------------------------------------------------

def test_AT04_provenance_to_bytes():
    rec, _ = run(CHAIN)
    for e in rec["events"]:
        r = e["source_ref"]
        body = CHAIN[r["byte_offset"]:r["byte_offset"] + r["byte_length"]]
        assert hashlib.sha256(body).hexdigest() == r["byte_sha256"]
        assert json.loads(body)["id"] == e["event_id"]


def test_AT05_missing_timestamp():
    rec, _ = run(nd({"id": "a", "t": 1}, {"id": "b", "parent": "a"}))
    b = [e for e in rec["events"] if e["event_id"] == "b"][0]
    assert b["t_state"] == "MISSING"
    edge = rec["edges"][0]
    assert edge["weight"] == 0.0 and edge["classification"] == "MISSING_METADATA"
    assert state_of(rec, "b")["state"] == "UNRESOLVED"


# -- Stage 3 ----------------------------------------------------------------

def test_AT06_causal_admissibility():
    rec, _ = run(nd({"id": "a", "t": 5}, {"id": "b", "t": 3, "parent": "a"},        # backwards in time
                    {"id": "c", "t": 7, "q": 2}, {"id": "d", "t": 7, "q": 1, "parent": "c"},  # equal t, q backwards
                    {"id": "e", "t": 9, "q": 1}, {"id": "f", "t": 9, "q": 2, "parent": "e"}))  # equal t, q forwards
    cls = {e["edge_id"].split("->")[1].split("#")[0]: e for e in rec["edges"]}
    assert cls["b"]["classification"] == "REJECTED" and cls["b"]["score"] == 0.0
    assert cls["d"]["classification"] == "REJECTED"
    assert cls["f"]["classification"] == "ADMISSIBLE"


def test_AT07_disconnected_kept_no_synthetic_edges():
    rec, _ = run(CHAIN + nd({"id": "lonely", "t": 2}))
    assert state_of(rec, "lonely")["state"] == "SINGLETON"
    vids = {e["vertex_id"] for e in rec["events"]}
    assert all(e["u"] in vids and e["v"] in vids for e in rec["edges"])


# -- Stage 4 ----------------------------------------------------------------

def test_AT09_only_admissible_edges_selected():
    rec, _ = run(nd({"id": "a", "t": 5}, {"id": "b", "t": 3, "parent": "a"}, {"id": "c", "t": 6, "parent": "a"}))
    ed = {e["edge_id"]: e for e in rec["edges"]}
    assert all(ed[k]["classification"] == "ADMISSIBLE" for k in rec["selected_edges"])


def test_AT10_all_unselected_edges_kept_as_alternatives():
    rec, _ = run(nd({"id": "a", "t": 1, "corr": "k"}, {"id": "b", "t": 2, "corr": "k"},
                    {"id": "c", "t": 3, "corr": "k"}))
    assert set(rec["selected_edges"]) | set(rec["alternatives"]) == {e["edge_id"] for e in rec["edges"]}
    assert not set(rec["selected_edges"]) & set(rec["alternatives"])


def test_AT15_equal_weight_tie_is_ambiguous_and_deterministic():
    raw = nd({"id": "a", "t": 1, "corr": "k"}, {"id": "b", "t": 2, "corr": "k"}, {"id": "c", "t": 3, "corr": "k"})
    rec, text = run(raw)
    assert state_of(rec, "c")["state"] == "AMBIGUOUS"
    assert all(run(raw)[1] == text for _ in range(5))


# -- Stage 5 ----------------------------------------------------------------

def test_AT11_precedence_order():
    assert STATE_PRECEDENCE == ["QUARANTINED", "UNRESOLVED", "AMBIGUOUS", "VERIFIED", "CANDIDATE", "SINGLETON"]
    # one component holding a duplicate id (-> QUARANTINED), a dangling parent
    # (-> UNRESOLVED) and two equal-weight in-edges to c (-> AMBIGUOUS): QUARANTINED wins
    rec, _ = run(nd({"id": "a", "t": 1}, {"id": "a", "t": 2}, {"id": "c", "t": 3, "parent": "a", "corr": "k"},
                    {"id": "d", "t": 4, "parent": "ghost", "corr": "k"}))
    s = state_of(rec, "d")
    assert set(s["event_refs"]) >= {"c#2", "d#3"} and s["state"] == "QUARANTINED"
    assert "DUPLICATE_EVENT_ID" in s["blocking_conditions"]
    # without the duplicate, the dangling parent (UNRESOLVED) outranks the tie (AMBIGUOUS)
    rec, _ = run(nd({"id": "a", "t": 1, "corr": "j"}, {"id": "b", "t": 1.5, "corr": "j"},
                    {"id": "c", "t": 3, "corr": "j"}, {"id": "d", "t": 4, "parent": "ghost", "corr": "j"}))
    assert state_of(rec, "d")["state"] == "UNRESOLVED"


def test_AT12_certainty_ceiling():
    rec, _ = run(nd({"id": "a", "t": 1, "q": 1, "corr": "k"}, {"id": "b", "t": 2, "q": 2, "corr": "k"}))
    s = state_of(rec, "a")
    assert s["state"] == "CANDIDATE" and s["certainty_limit"] == 0.5     # capped by the correlation edge
    assert rec["certainty_limit"] <= min(x["certainty_limit"] for x in rec["states"])


def test_AT13_edge_free_component_certainty_is_min_event():
    rec, _ = run(nd({"id": "a", "t": 1}))                                # t but no q -> 0.5
    assert state_of(rec, "a")["certainty_limit"] == 0.5


def test_verified_chain():
    rec, _ = run(CHAIN)
    assert [s["state"] for s in rec["states"]] == ["VERIFIED"] and len(rec["selected_edges"]) == 2


# -- Stage 6 ----------------------------------------------------------------

def test_AT14_AT16_canonical_output():
    rec, text = run(CHAIN)
    assert text == canonicalize(json.loads(text))                        # idempotent
    # no whitespace outside strings, keys sorted: equals compact sorted serialisation
    assert text == json.dumps(json.loads(text), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    assert canonicalize({"b": 1, "a": [1.0, 1e21, 1e-7, "é\n"]}) == '{"a":[1,1e+21,1e-7,"é\\n"],"b":1}'


def test_AT17_uncanonicalizable_output_quarantined_source_hash_kept():
    raw = b'{"id":"a","t":Infinity}\n'                                  # json accepts it; JCS cannot encode it
    rec, _ = reconstruct([raw], "s")
    assert rec["status"] == "QUARANTINED"
    assert rec["source_bytes_sha256"] == hashlib.sha256(raw).hexdigest()
    assert validate(rec, raw) == []
    with pytest.raises(CanonicalizationError):
        canonicalize(float("nan"))


# -- the validator must reject tampered records (null control) -----------------

@pytest.mark.parametrize("tamper, expect", [
    (lambda r: next(s for s in r["states"] if s["certainty_limit"] < 1).__setitem__("certainty_limit", 1.0),
     "exceeds ceiling"),
    (lambda r: r["selected_edges"].append(r["alternatives"][0]), "both selected and alternative"),
    (lambda r: r["edges"].append({"edge_id": "x->y", "u": "x", "v": "y", "evidence": "REFERENCE",
                                  "weight": 1.0, "score": 1.0, "classification": "ADMISSIBLE"}),
     "not an event"),
    (lambda r: r["events"][0]["source_ref"].__setitem__("byte_sha256", "0" * 64), "provenance"),
    (lambda r: r.__setitem__("source_id", "other"), "canonical JCS hash"),
    (lambda r: r["states"][0].__setitem__("state", "CONFIRMED"), "unknown state"),
])
def test_validator_rejects_tampering(tamper, expect):
    raw = CHAIN + nd({"id": "d", "t": 4, "corr": "k"}, {"id": "e", "t": 5, "corr": "k"}, {"id": "f", "t": 0.5, "parent": "a"})
    rec, _ = run(raw)
    tamper(rec)
    problems = validate(rec, raw)
    assert any(expect in p for p in problems), problems


# -- optimizer correctness ---------------------------------------------------

def _brute(n, edges):
    best = 0.0
    for k in range(len(edges) + 1):
        for S in itertools.combinations(edges, k):
            heads = [v for _, v, _, _ in S]
            if len(heads) != len(set(heads)):
                continue
            par = {v: u for u, v, _, _ in S}
            ok = True
            for s in par:
                seen, x = set(), s
                while x in par:
                    if x in seen:
                        ok = False
                        break
                    seen.add(x)
                    x = par[x]
            if ok:
                best = max(best, sum(w for *_, w, _ in [(u, v, w, key) for u, v, w, key in S]))
    return best


def test_branching_is_optimal_on_random_graphs():
    rng = random.Random(0)
    for trial in range(300):
        n = rng.randint(1, 6)
        edges = []
        for u in range(n):
            for v in range(n):
                if u != v and rng.random() < 0.4:
                    edges.append((u, v, rng.choice([0.5, 1.0, 1.5, 2.0]), f"{u}->{v}"))
        chosen = maximum_branching(range(n), edges)
        got = sum(w for u, v, w, k in edges if k in chosen)
        assert abs(got - _brute(n, edges)) < 1e-9, (n, edges, chosen)


def test_inversion_counterexample_is_not_reproduced():
    # the spec's w' = W + eps - w picks the empty branching here; maximum branching must not
    edges = [("r", "a", 1.0, "r->a"), ("a", "c", 5.0, "a->c"), ("r", "c", 4.0, "r->c")]
    assert maximum_branching(["r", "a", "b", "c"], edges) == {"r->a", "a->c"}
