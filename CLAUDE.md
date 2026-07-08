# CylicAmp — Session Protocol

## On Start: Read handoff.json First

Before doing anything else, read `handoff.json` at the repo root.
It contains the last session's active task, branch, checkpoint, pending actions, and behavioral protocol.

The session-start hook at `.claude/session_start.sh` runs this automatically.

## Behavioral Protocol (from handoff.json → session_protocol)

- Save verified math immediately. No waiting to be asked.
- Target file: `math/theorems/dr_pattern_suite.py`
- Sections labeled A, B, C... each with assertions. Run after writing. Commit. Push.
- No social filler. No idle talk. No emotional signaling.
- Output: data, analysis, conclusions.

## Handoff Protocol — How to Update handoff.json

At the end of a session or after a significant checkpoint, update `handoff.json`:
1. Set `last_session_id` to current date + descriptor
2. Set `active_task` to current work
3. Set `last_checkpoint` to the last file modified
4. Run `sha256sum <checkpoint_file>` and write result to `last_checkpoint_sha256`
5. Update `pending_actions` list
6. Commit and push: `git add handoff.json && git commit -m "Update handoff: <task>" && git push`

## Repo Structure

```
CylicAmp/
├── .claude/
│   ├── settings.json       ← session-start hook config
│   └── session_start.sh    ← SHP discovery script
├── cylicamp/               ← core package
├── math/
│   ├── differential-geometry/
│   ├── primes/
│   ├── theorems/
│   │   └── dr_pattern_suite.py   ← main theorem suite (A–R)
│   └── visualizations/
├── CLEANUP_CANDIDATES.md   ← owner review required before any deletions
├── CLAUDE.md               ← this file
├── handoff.json            ← session state
└── requirements.txt
```

## Key Facts (do not re-derive)

- `DR(n) = (n-1)%9+1` for n>0; sign-invariant; multiplicative homomorphism mod 9
- `M_E` eigenvalues: {-4, 0, 0, 4}; rank 2; ker(M_E) dim=2
- ker basis: k1=[0,1,-1,0], k2=[1,0,0,-1]
- D4 acts on kernel as Z2×Z2 (abelian); r⊗r=diag(+1,-1), s⊗s=diag(-1,+1)
- Commutant of M_E on kernel = M2(C), dim=4; generators = P_ij outer products
- Motif bulk word = r² (not e)
- H_E zero modes are accidental (not D4-protected); Q=P11-P22 splits them
