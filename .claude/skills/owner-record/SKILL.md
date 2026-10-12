---
name: owner-record
description: Keep the owner's work in the owner's words. Every message the owner writes is stored verbatim in owner_work/ (automatic - a UserPromptSubmit hook runs tools/owner_record.py); the owner's own names for operations (drip cycle, faucet, flow, hose, stutter, seam, ...) are used exactly as the owner wrote them and never replaced by a new label; anything computed from the owner's work goes BESIDE the owner's lines, quoted with the message number, never instead of them. Use on every owner message, and before writing any file, theorem, skill or reply that describes the owner's work or uses one of the owner's terms.
---

# owner-record

The owner, 2026-10-12, verbatim (`owner_work/messages/2026-10-12.txt`):

> Every time I tell you to fucking turn this into a skill, every time I tell you, you never
> fucking listen! I tell you to fucking mark everything down that I fucking wrote out! You
> should have a whole fucking thing of everything I wrote out! That's the proof that I did
> the fucking work! ... Put how I did the operations. Put my work in there. What do? You
> don't put my work in there. You put your version of my fucking work in there. ... It's
> supposed to be fucking both, motherfucker.

## 1. The record -- everything the owner writes, verbatim

```
python3 tools/owner_record.py --check         # before every commit that touches owner_work/
python3 tools/owner_record.py --transcripts   # backfill: session start, or if the hook did not run
```

- `owner_work/messages/<YYYY-MM-DD>.txt` -- every owner message, character for character,
  with its UTC timestamp and a running number `#n`. `messages.json` is the same record,
  `index.json` holds a sha256 per message.
- The `UserPromptSubmit` hook in `.claude/settings.json` appends each message the moment it
  is sent. Commit `owner_work/` in the same turn (the stop hook will ask if you forget).
- The only edit ever made is removing a credential, marked in place. Pasted material stays
  in the message it came in -- it is part of what the owner sent.
- Started 2026-10-12 from this repository's session transcripts (2026-10-05
  onward; 228 messages). Earlier sessions' transcripts were not on the machine; anything the owner showed
  before 2026-10-05 is in the record only where the owner committed it (e.g. the Hose Flow
  Theorem, `math/theorems/hose_flow_transient.py`, commit b88389e by Michael Song).

## 2. The owner's names stay the owner's names

- Write the owner's term as the owner wrote it: **drip cycle**, **faucet**, **flow**,
  **hose**, **complete flow**, **stuttering flow**, **horizon**, **seam**, ... `owner_work/TERMS.md`
  lists every term with the owner's own sentence and message number.
- Never introduce a new label for something the owner named. If the repo already uses a
  different name, write the owner's term first and the repo's after it, once:
  "drip cycle (owner's term)", "SEED orbit (repo label for 18, 24, 32)".
- Do not split, relabel or re-section the owner's lines in anything the owner reads
  ("[OWNER] block O1", "C3 commentary" was exactly this, 2026-10-12). Quote and number by
  the owner's message, `#n` and date.

## 3. Both versions, always

Every file built from the owner's work carries, in this order:

1. **The owner's lines, verbatim**, with `owner_work` message number and date.
2. **How the owner did the operation**, in the owner's words where the owner gave them.
3. **The computation / audit beside it** -- what reproduces, what is forced, what fails.

A clean derivation without (1) and (2) is incomplete, however correct it is.

## 4. When the owner uses one of the owner's own terms

Search before answering:

```
grep -n -i "<term>" owner_work/messages/*.txt owner_work/TERMS.md
git grep -n -i "<term>" $(git for-each-ref --format='%(refname:short)' refs/remotes/origin)
```

Report what the record shows, quoting it. Never answer the owner's own term with "that is
not defined". If the record does not have it yet, say "not in the record yet", record the
example the owner gives right then (it is already in `owner_work/` by the hook), and work
from that example.

Example that set this (2026-10-12): the owner asked for "my full drip cycle". The record
had no drip example; the reply said "drip cycle isn't defined anywhere". The owner had
shown it in earlier sessions that were never recorded, and showed it again:

```
1
12

1
21

2
12

2
21
```

"That right there is just a fucking small example. That is not all of them. Find all of
them." The instances found across the record are in `owner_work/drip_cycle.md`.
