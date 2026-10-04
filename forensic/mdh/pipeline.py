"""MDH reconstruction pipeline: bytes -> frames -> events -> edges -> branching
-> component states -> canonical audit record (MDHRecord).

Input format (concrete choice made here; the supplied spec leaves it open):
newline-delimited JSON, one event object per line, fields
    id      (str, required)       event identifier
    t       (number)              timestamp; absent -> MISSING (AT-05)
    q       (int)                 per-source sequence number
    parent  (str)                 explicit reference to a predecessor event id
    corr    (str)                 correlation key shared with related events
Any other fields are carried through untouched.
"""
import hashlib
import json

from .branching import maximum_branching
from .jcs import CanonicalizationError, canonical_sha256, canonicalize
from . import signatures

SCHEMA_VERSION = "mdh-record/1"
STATE_PRECEDENCE = ["QUARANTINED", "UNRESOLVED", "AMBIGUOUS", "VERIFIED", "CANDIDATE", "SINGLETON"]
EDGE_WEIGHTS = {"REFERENCE": 1.0, "CORRELATION": 0.5}


def sha256(b):
    return hashlib.sha256(b).hexdigest()


# -- Stage 1: deframe ---------------------------------------------------------

class Deframer:
    """Splits a byte stream into newline-terminated frames. Splitting happens on
    bytes, so the frames do not depend on how the stream was chunked (AT-01) and a
    multibyte UTF-8 character split across chunks is reassembled (AT-02). Bytes
    after the last newline form the tail; they never become an event and never
    alter earlier frames (AT-03)."""

    def __init__(self, source_id):
        self.source_id = source_id
        self.buf = bytearray()
        self.raw = bytearray()
        self.frames = []
        self.offset = 0
        self.finished = False

    def feed(self, chunk):
        if self.finished:
            raise RuntimeError("feed after finish")
        self.raw += chunk
        self.buf += chunk
        while True:
            i = self.buf.find(b"\n")
            if i < 0:
                break
            body = bytes(self.buf[:i])
            self._emit(body, self.offset)
            self.offset += i + 1
            del self.buf[:i + 1]

    def _emit(self, body, offset):
        self.frames.append({
            "frame_id": f"{self.source_id}:{len(self.frames)}",
            "offset": offset,
            "length": len(body),
            "sha256": sha256(body),
            "bytes": body,
        })

    def finish(self):
        self.finished = True
        tail = bytes(self.buf)
        if not tail:
            state = "COMPLETE"
        else:
            state = "INCOMPLETE"
        return {"tail_state": state, "tail_offset": self.offset, "tail_length": len(tail),
                "tail_sha256": sha256(tail) if tail else None}


# -- Stage 2: normalize ---------------------------------------------------------

def normalize(frames, source_id, keyring=None):
    events, diags = [], []
    seen = {}
    for fr in frames:
        ref = {"frame_id": fr["frame_id"], "byte_offset": fr["offset"],
               "byte_length": fr["length"], "byte_sha256": fr["sha256"]}
        if sha256(fr["bytes"]) != fr["sha256"]:                   # AT-04 gate
            diags.append(_diag("HASH_MISMATCH", fr, "frame bytes do not match recorded hash"))
            continue
        if not fr["bytes"].strip():
            diags.append(_diag("EMPTY_FRAME", fr, "blank line"))
            continue
        try:
            text = fr["bytes"].decode("utf-8")
        except UnicodeDecodeError as e:
            diags.append(_diag("MALFORMED_UTF8", fr, str(e)))
            continue
        try:
            obj = json.loads(text)
        except ValueError as e:
            diags.append(_diag("MALFORMED_JSON", fr, str(e)))
            continue
        if not isinstance(obj, dict) or not isinstance(obj.get("id"), str):
            diags.append(_diag("MISSING_ID", fr, "object without string id"))
            continue
        t = obj.get("t")
        t_ok = isinstance(t, (int, float)) and not isinstance(t, bool)
        q = obj.get("q")
        q_ok = isinstance(q, int) and not isinstance(q, bool)
        ev = {
            "event_id": obj["id"],
            "source_id": source_id,
            "t": t if t_ok else None,
            "t_state": "PRESENT" if t_ok else "MISSING",         # AT-05
            "q": q if q_ok else None,
            "parent": obj.get("parent") if isinstance(obj.get("parent"), str) else None,
            "corr": obj.get("corr") if isinstance(obj.get("corr"), str) else None,
            "fields": obj,                                      # carried through untouched
            "source_ref": ref,
            "certainty": 1.0 if (t_ok and q_ok) else (0.5 if t_ok else 0.0),
            "duplicate": False,
            "sig_state": None,
            "kid": None,
        }
        if keyring is not None:                                 # Stage 2 signatures
            try:
                ev["sig_state"], ev["kid"] = signatures.check(obj, source_id, keyring)
            except CanonicalizationError:
                ev["sig_state"], ev["kid"] = "INVALID_SIGNATURE", None
            cap = {"SIGNED_VALID": 1.0, "UNSIGNED": 0.5, "UNTRUSTED_KEY": 0.25,
                   "REVOKED_KEY": 0.25, "INVALID_SIGNATURE": 0.0}[ev["sig_state"]]
            ev["certainty"] = min(ev["certainty"], cap)
        if ev["event_id"] in seen:
            ev["duplicate"] = True
            seen[ev["event_id"]]["duplicate"] = True
            diags.append(_diag("DUPLICATE_ID", fr, f"id {ev['event_id']!r} already used"))
        else:
            seen[ev["event_id"]] = ev
        events.append(ev)
    return events, diags


def _diag(cls, fr, detail):
    return {"classification": cls, "frame_ref": fr["frame_id"], "offset": fr["offset"], "detail": detail}


# -- Stage 3: constrain ---------------------------------------------------------

def _vid(ev, i):
    return f"{ev['event_id']}#{i}"


def candidate_edges(events, max_horizon=None):
    by_id = {}
    for i, ev in enumerate(events):
        by_id.setdefault(ev["event_id"], []).append(i)
    pairs = {}
    for j, v in enumerate(events):
        if v["parent"] is not None:
            for i in by_id.get(v["parent"], []):
                if i != j:
                    pairs[(i, j)] = "REFERENCE"
    groups = {}
    for i, ev in enumerate(events):
        if ev["corr"] is not None:
            groups.setdefault(ev["corr"], []).append(i)
    for idx in groups.values():
        for i in idx:
            for j in idx:
                if i != j and (i, j) not in pairs:
                    pairs[(i, j)] = "CORRELATION"
    edges = []
    for (i, j), kind in sorted(pairs.items()):
        u, v = events[i], events[j]
        e = {"edge_id": f"{_vid(u, i)}->{_vid(v, j)}", "u": i, "v": j, "evidence": kind,
             "weight": EDGE_WEIGHTS[kind]}
        if u["t_state"] == "MISSING" or v["t_state"] == "MISSING":
            e.update(classification="MISSING_METADATA", weight=0.0, score=0.0)   # AT-05
        elif not _causal(u, v):
            reason = "CROSS_SOURCE_TIE" if (u["t"] == v["t"] and u["source_id"] != v["source_id"]) else "NOT_CAUSAL"
            e.update(classification="REJECTED", reason=reason, score=0.0)       # AT-06
        elif max_horizon is not None and v["t"] - u["t"] > max_horizon:
            e.update(classification="OUT_OF_HORIZON_REJECTED", score=0.0)
        else:
            e.update(classification="ADMISSIBLE", score=e["weight"])
        edges.append(e)
    return edges


def _causal(u, v):
    if u["t"] < v["t"]:
        return True
    if u["t"] == v["t"]:
        # sequence numbers only order events of the SAME source
        return (u["source_id"] == v["source_id"] and u["q"] is not None
                and v["q"] is not None and u["q"] < v["q"])
    return False


# -- Stage 4: optimize ----------------------------------------------------------

def optimize(events, edges):
    adm = [e for e in edges if e["classification"] == "ADMISSIBLE"]           # AT-09
    chosen = maximum_branching(range(len(events)),
                               [(e["u"], e["v"], e["weight"], e["edge_id"]) for e in adm])
    selected = [e for e in adm if e["edge_id"] in chosen]
    alternatives = [e for e in edges if e["edge_id"] not in chosen]           # AT-10
    ambiguous_targets = set()
    for s in selected:                                                        # AT-15
        rivals = [e for e in adm if e["v"] == s["v"] and e["edge_id"] != s["edge_id"]
                  and e["weight"] == s["weight"]]
        if rivals:
            ambiguous_targets.add(s["v"])
    return selected, alternatives, ambiguous_targets


# -- Stage 5: assign state ------------------------------------------------------

def components(n, selected):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for e in selected:
        parent[find(e["u"])] = find(e["v"])
    comps = {}
    for i in range(n):
        comps.setdefault(find(i), []).append(i)
    return sorted(comps.values(), key=lambda c: min(c))


def assign_states(events, selected, ambiguous_targets, integrity_ok):
    known = {ev["event_id"] for ev in events}
    out = []
    for k, comp in enumerate(components(len(events), selected)):
        cs = set(comp)
        cedges = [e for e in selected if e["u"] in cs]
        blocking = []
        if not integrity_ok:
            blocking.append("SOURCE_INTEGRITY_FAILURE")
        if any(events[i]["duplicate"] for i in comp):
            blocking.append("DUPLICATE_EVENT_ID")
        blocking += [f"INVALID_SIGNATURE:{events[i]['event_id']}" for i in comp
                     if events[i]["sig_state"] == "INVALID_SIGNATURE"]
        signed_mode = any(events[i]["sig_state"] is not None for i in comp)
        all_signed = all(events[i]["sig_state"] == "SIGNED_VALID" for i in comp)
        missing = [events[i]["event_id"] for i in comp if events[i]["t_state"] == "MISSING"]
        dangling = [events[i]["event_id"] for i in comp
                    if events[i]["parent"] is not None and events[i]["parent"] not in known]
        amb = [events[i]["event_id"] for i in comp if i in ambiguous_targets]
        if blocking:
            state, rule = "QUARANTINED", "integrity, identity or signature failure"
        elif missing or dangling:
            state, rule = "UNRESOLVED", "missing timestamp or dangling reference"
            blocking += [f"MISSING_TIMESTAMP:{x}" for x in missing] + [f"DANGLING_PARENT:{x}" for x in dangling]
        elif amb:
            state, rule = "AMBIGUOUS", "equal-weight competing in-edge"
        elif cedges and all(e["evidence"] == "REFERENCE" for e in cedges) and (not signed_mode or all_signed):
            state, rule = "VERIFIED", "all selected edges are explicit references" + (
                " and every event carries a valid signature" if signed_mode else "")
        elif cedges:
            state, rule = "CANDIDATE", "selected edges include correlation evidence"
        else:
            state, rule = "SINGLETON", "single event, no edges"
        # epistemic ceiling (AT-12) / edge-free component (AT-13)
        cert = min([events[i]["certainty"] for i in comp] + [e["weight"] for e in cedges])
        out.append({
            "state_record_id": f"component:{k}",
            "component_ref": f"component:{k}",
            "state": state,
            "precedence_rule_applied": rule,
            "event_refs": [_vid(events[i], i) for i in sorted(comp)],
            "supporting_edge_refs": [e["edge_id"] for e in cedges],
            "blocking_conditions": blocking,
            "ambiguous_event_ids": amb,
            "certainty_limit": cert,
        })
    return out


# -- Stage 6: audit emission ----------------------------------------------------

def reconstruct(raw_chunks, source_id, max_horizon=None, keyring=None):
    """Run all six stages. raw_chunks: iterable of bytes. Returns (record, canonical_text)."""
    d = Deframer(source_id)
    for c in raw_chunks:
        d.feed(c)
    tail = d.finish()
    source_hash = sha256(bytes(d.raw))
    events, diags = normalize(d.frames, source_id, keyring)
    integrity_ok = not any(x["classification"] == "HASH_MISMATCH" for x in diags)
    edges = candidate_edges(events, max_horizon)
    selected, alternatives, amb = optimize(events, edges)
    states = assign_states(events, selected, amb, integrity_ok)
    record = {
        "schema": SCHEMA_VERSION,
        "source_id": source_id,
        "source_bytes_sha256": source_hash,
        "constraints": {"max_horizon": max_horizon, "cross_source_ties": "rejected"}
        | ({"keyring_sha256": signatures.keyring_fingerprint(keyring)} if keyring is not None else {}),
        "tail": tail,
        "frames": [{k: f[k] for k in ("frame_id", "offset", "length", "sha256")} for f in d.frames],
        "diagnostics": diags,
        "events": [{"vertex_id": _vid(ev, i), "event_id": ev["event_id"], "t": ev["t"], "t_state": ev["t_state"],
                    "q": ev["q"], "certainty": ev["certainty"], "source_ref": ev["source_ref"]}
                   | ({"signature": {"state": ev["sig_state"], "key_id": ev["kid"]}} if keyring is not None else {})
                   for i, ev in enumerate(events)],
        "edges": [{k: e[k] for k in ("edge_id", "evidence", "weight", "score", "classification")}
                  | {"u": _vid(events[e["u"]], e["u"]), "v": _vid(events[e["v"]], e["v"])}
                  | ({"reason": e["reason"]} if "reason" in e else {}) for e in edges],
        "selected_edges": [e["edge_id"] for e in selected],
        "alternatives": [e["edge_id"] for e in alternatives],
        "states": states,
        "certainty_limit": min([s["certainty_limit"] for s in states], default=1.0),
        "optimizer_status": "OPTIMAL_MAXIMUM_BRANCHING",
    }
    try:
        canonicalize(record)
        record["audit_manifest"] = {"canonical_jcs_sha256": canonical_sha256(record),
                                    "source_bytes_sha256": source_hash}
        return record, canonicalize(record)
    except CanonicalizationError as e:                                        # AT-17
        q = {"schema": SCHEMA_VERSION, "source_id": source_id, "source_bytes_sha256": source_hash,
             "status": "QUARANTINED", "blocking_conditions": [f"CANONICALIZATION_FAILED: {e}"]}
        return q, canonicalize(q)
