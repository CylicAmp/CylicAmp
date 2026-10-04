"""Check an MDHRecord against the schema and the invariants it must satisfy.
Returns a list of violations; an empty list means the record passes."""
import hashlib

import json

from .jcs import CanonicalizationError, canonical_sha256
from . import signatures
from .pipeline import SCHEMA_VERSION, STATE_PRECEDENCE

REQUIRED = {"schema": str, "source_id": str, "source_bytes_sha256": str, "constraints": dict,
            "tail": dict, "frames": list, "diagnostics": list, "events": list, "edges": list,
            "selected_edges": list, "alternatives": list, "states": list,
            "certainty_limit": (int, float), "optimizer_status": str, "audit_manifest": dict}


def validate(rec, raw_bytes=None, keyring=None):
    v = []
    if rec.get("status") == "QUARANTINED":
        if not rec.get("blocking_conditions"):
            v.append("quarantined record without blocking conditions")
        if raw_bytes is not None and rec.get("source_bytes_sha256") != hashlib.sha256(raw_bytes).hexdigest():
            v.append("quarantined record altered the source hash")
        return v
    for k, t in REQUIRED.items():
        if k not in rec:
            v.append(f"missing field {k}")
        elif not isinstance(rec[k], t):
            v.append(f"field {k} has wrong type")
    if v:
        return v
    if rec["schema"] != SCHEMA_VERSION:
        v.append(f"schema {rec['schema']} != {SCHEMA_VERSION}")
    # provenance: frames and events trace back to the source bytes
    if raw_bytes is not None:
        if hashlib.sha256(raw_bytes).hexdigest() != rec["source_bytes_sha256"]:
            v.append("source hash does not match raw bytes")
        for f in rec["frames"]:
            body = raw_bytes[f["offset"]:f["offset"] + f["length"]]
            if hashlib.sha256(body).hexdigest() != f["sha256"]:
                v.append(f"frame {f['frame_id']} hash does not match its bytes")
    frame_hash = {f["frame_id"]: f["sha256"] for f in rec["frames"]}
    for e in rec["events"]:
        r = e["source_ref"]
        if frame_hash.get(r["frame_id"]) != r["byte_sha256"]:
            v.append(f"event {e['vertex_id']} provenance does not match frame {r['frame_id']}")
    # edges: selected are admissible (AT-09); selected + alternatives partition edges (AT-10)
    ed = {e["edge_id"]: e for e in rec["edges"]}
    sel, alt = set(rec["selected_edges"]), set(rec["alternatives"])
    if sel & alt:
        v.append("an edge is both selected and alternative")
    if sel | alt != set(ed):
        v.append("selected + alternatives do not cover all edges")
    for k in sel:
        if ed.get(k, {}).get("classification") != "ADMISSIBLE":
            v.append(f"selected edge {k} is not ADMISSIBLE")
    # branching: at most one selected in-edge per vertex, no cycle
    heads = [ed[k]["v"] for k in sel if k in ed]
    if len(heads) != len(set(heads)):
        v.append("a vertex has two selected in-edges")
    par = {ed[k]["v"]: ed[k]["u"] for k in sel if k in ed}
    for start in par:
        seen, x = set(), start
        while x in par:
            if x in seen:
                v.append("selected edges contain a cycle")
                break
            seen.add(x)
            x = par[x]
    # no synthetic edges: every endpoint is a real event (AT-07)
    vids = {e["vertex_id"] for e in rec["events"]}
    for e in rec["edges"]:
        if e["u"] not in vids or e["v"] not in vids:
            v.append(f"edge {e['edge_id']} touches a vertex that is not an event")
    # states: vocabulary, epistemic ceiling (AT-11..AT-13)
    ev = {e["vertex_id"]: e for e in rec["events"]}
    covered = []
    for s in rec["states"]:
        if s["state"] not in STATE_PRECEDENCE:
            v.append(f"unknown state {s['state']}")
        covered += s["event_refs"]
        bound = min([ev[x]["certainty"] for x in s["event_refs"]]
                    + [ed[k]["weight"] for k in s["supporting_edge_refs"]])
        if s["certainty_limit"] > bound:
            v.append(f"{s['state_record_id']} certainty {s['certainty_limit']} exceeds ceiling {bound}")
        if s["state"] == "SINGLETON" and (len(s["event_refs"]) != 1 or s["supporting_edge_refs"]):
            v.append(f"{s['state_record_id']} SINGLETON with edges or several events")
        if s["state"] == "VERIFIED" and any(ed[k]["evidence"] != "REFERENCE" for k in s["supporting_edge_refs"]):
            v.append(f"{s['state_record_id']} VERIFIED with non-reference evidence")
        if s["state"] in ("QUARANTINED", "UNRESOLVED") and not s["blocking_conditions"]:
            v.append(f"{s['state_record_id']} {s['state']} without blocking conditions")
    if sorted(covered) != sorted(vids):
        v.append("states do not cover every event exactly once")
    if rec["certainty_limit"] > min([s["certainty_limit"] for s in rec["states"]], default=1.0):
        v.append("record certainty exceeds its weakest component")
    # signatures: every claimed state must be what re-verification gives
    if keyring is not None:
        if rec["constraints"].get("keyring_sha256") != signatures.keyring_fingerprint(keyring):
            v.append("record was built with a different keyring")
        elif raw_bytes is not None:
            for e in rec["events"]:
                r = e["source_ref"]
                obj = json.loads(raw_bytes[r["byte_offset"]:r["byte_offset"] + r["byte_length"]])
                try:
                    real, _ = signatures.check(obj, rec["source_id"], keyring)
                except CanonicalizationError:
                    real = "INVALID_SIGNATURE"
                claimed = e.get("signature", {}).get("state")
                if claimed != real:
                    v.append(f"event {e['vertex_id']} claims signature {claimed}, re-verification gives {real}")
        for s in rec["states"]:
            if s["state"] == "VERIFIED" and any(ev[x].get("signature", {}).get("state") != "SIGNED_VALID"
                                                for x in s["event_refs"]):
                v.append(f"{s['state_record_id']} VERIFIED with an event lacking a valid signature")
    # canonical hash (AT-14, AT-16)
    body = {k: x for k, x in rec.items() if k != "audit_manifest"}
    try:
        if canonical_sha256(body) != rec["audit_manifest"].get("canonical_jcs_sha256"):
            v.append("canonical JCS hash does not match audit manifest")
    except CanonicalizationError as e:
        v.append(f"record cannot be canonicalized: {e}")
    return v
