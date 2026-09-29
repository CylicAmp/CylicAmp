# MDH — Maximum Defensible History reconstruction

A runnable implementation of the six-stage pipeline in the supplied v1.0.0
spec: raw bytes → frames → events → candidate edges → maximum branching →
component states → canonical audit record (`MDHRecord`).

```
python3 -m forensic.mdh.cli forensic/mdh/sample.ndjson --source-id demo
python3 -m pytest forensic/mdh -q          # 24 tests
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
