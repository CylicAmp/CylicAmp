# MDH — Maximum Defensible History reconstruction

A runnable implementation of the six-stage pipeline in the supplied v1.0.0
spec: raw bytes → frames → events → candidate edges → maximum branching →
component states → canonical audit record (`MDHRecord`).

```
python3 -m forensic.mdh.cli forensic/mdh/sample.ndjson --source-id demo
python3 -m pytest forensic/mdh -q          # 42 tests
python3 -m forensic.mdh.cli events.ndjson --source-id plant-a --keyring keys.json   # with signatures
```

## Stages

| Stage | File | What it enforces |
|---|---|---|
| 1 Deframe | `pipeline.py` `Deframer` | frames split on bytes, independent of chunking (AT-01, AT-02); incomplete tail isolated (AT-03) |
| 2 Normalize | `normalize` | every event keeps frame id, byte offset, length, SHA-256 (AT-04); missing timestamp → `MISSING`, certainty 0 (AT-05) |
| 3 Constrain | `candidate_edges` | admissible iff t_u < t_v, or equal t with q_u < q_v **in the same source** (AT-06); rejected edges kept with score 0; no synthetic edges (AT-07) |
| 4 Optimize | `branching.py` | maximum-weight branching over ADMISSIBLE edges only (AT-09); every other edge kept as an alternative (AT-10); equal-weight rival in-edges → `AMBIGUOUS` (AT-15) |
| 5 Assign state | `assign_states` | QUARANTINED > UNRESOLVED > AMBIGUOUS > VERIFIED > CANDIDATE > SINGLETON (AT-11); certainty = min over events and selected edges (AT-12, AT-13) |
| 6 Audit | `jcs.py` | RFC 8785 canonical JSON and its SHA-256 (AT-14, AT-16); output that cannot be canonicalized is quarantined with the source hash unchanged (AT-17) |

`validate.py` checks a record against all of the above and rejects tampered
records (tested: raised certainty, edge in both lists, synthetic edge, broken
provenance, changed field, unknown state).

## Where this departs from the supplied spec, and why

1. **No weight inversion in Stage 4.** The spec's w' = W + ε − w(e) is only
   valid for spanning arborescences. With vertices that have no admissible
   in-edge (which AT-07 keeps) it selects the empty branching. Here a maximum
   branching is computed directly (Edmonds, via a virtual root whose edges are
   removed before output). Tested against brute force on 300 random graphs, and
   on the counterexample where inversion returns nothing.
2. **Equal timestamps across sources are rejected** (`CROSS_SOURCE_TIE`):
   sequence numbers from different sources are not comparable.
3. **No wall-clock timestamp in the record**, so the same input always gives
   the same canonical hash.
4. **AT-08 is not implemented**: the spec numbers it but never defines it.

## Choices the spec left open (made here, change as needed)

- Input format: newline-delimited JSON, fields `id`, `t`, `q`, `parent`, `corr`.
  `.pcap`, `.har`, WAL and LevelDB inputs need their own deframers in front of
  Stage 2; none are written yet.
- Edge evidence: `parent` reference = weight 1.0 (`REFERENCE`), shared `corr`
  key = 0.5 (`CORRELATION`).
- Event certainty: 1.0 with `t` and `q`, 0.5 with `t` only, 0 without `t`.
- Ambiguity is detected locally (a competing admissible in-edge of equal
  weight), not by enumerating every optimal branching.

## Signatures (Stage 2 extension, `signatures.py`)

With `--keyring`, every event is checked for an Ed25519 signature (fields `kid`,
`sig`). The signed bytes are `"mdh-event-v1\0" + source_id + "\0" + JCS(event
without sig)`: a signature cannot be moved to another event, another key id or
another source, and whitespace or key order in the file does not matter.

| Signature state | Effect |
|---|---|
| SIGNED_VALID | none; required for VERIFIED when a keyring is used |
| UNSIGNED | certainty capped at 0.5; blocks VERIFIED (component becomes CANDIDATE) |
| UNTRUSTED_KEY, REVOKED_KEY | certainty capped at 0.25 |
| INVALID_SIGNATURE | certainty 0, component QUARANTINED |

Only Ed25519 (via the `cryptography` library). The validator re-verifies every
claimed signature state against the raw bytes and rejects records built with a
different keyring. Tests use real keys: tampered value, wrong key, unknown and
revoked keys, unsigned event, signature copied to another event, signature from
another source, swapped key id, five malformed signatures, and a verifier that
accepts everything (the validator catches it). Without `--keyring` the output is
unchanged from before.

Still true: a signature proves which key signed, not that the signer told the truth.

## StrictForensicLinker (`strict_linker.py`), added 2026-10-02

A second, turn-level linker supplied on 2026-10-02. The supplied text is kept
verbatim in `supplied/strict_linker_2026_10_02.py`; its audit is
`supplied/audit_strict_linker_2026_10_02.py`. `strict_linker.py` fixes the
five audited defects:

| | Supplied behaviour | Fixed |
|---|---|---|
| D1 | explicit root reported but not enforced | every event must be reachable from the root, else `EXPLICIT_ROOT_CONFLICT` |
| D2 | REJECTED (e.g. cross-session) edges dropped | kept in `rejected_edges` |
| D3 | every later event typed `CAUSAL_REPLY`; `MESSAGE_SUCCESSION` unreachable | `role` field; reply / succession / no edge when a role is unknown |
| D4 | `>` on `PayloadIntegrity` fell back to string order | one rank for `<`, `<=`, `>`, `>=` |
| D5 | example JSON not produced by the code | `strict_linker_example.json` is generated by `to_record` and checked byte for byte |

Also: equal-weight rival parents give `TIED_PARENT` and status CANDIDATE (as
AT-15 above); unsupplied event confidence gives confidence `None`, not 0.0.
Axioms A1–A7 and the score's derivative are tested in `test_strict_linker.py`
(163 tests, including 150 random inputs). Each fix was checked by undoing it:
the tests fail without it.
