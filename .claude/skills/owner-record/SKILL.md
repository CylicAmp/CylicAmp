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
them." `owner_work/drip_cycle.md` holds the example, how the cycle is run (`drip_cycle.py`), and each run.

## 5. Work the owner does with the owner's own tools is the owner's work

Results the owner computes in the owner's own projects and tools (Egor / egor_v18, igor_*
scripts, any AI the owner directs) are the owner's results. Label them as the owner's,
naming the tool only as where they were computed: "the owner's Langton's ant results,
computed in the owner's Egor project". Never "the Egor tool's numbers", never "not the
owner's own statements".

Example that set this (2026-10-14): the Langton's ant file labelled the owner's table (onset 9,976,
period 104, +12, 576,486 at 5,000,000) as the Egor tool's words, although the owner ran
igor_langton_mask_v18.py in the owner's egor_v18_project. Corrected the same day.

The attribution rule (do not put a claim in the owner's mouth) is about claims the owner
only relayed or disputed. It is never a reason to take a result away from the owner.

2026-10-20 (#389), the example that exposed it again: a reply said a column formula of the owner's 0.125 count "was written in the repo's audit of the last paste, not by you". Wrong: the count is the owner's construction (#378, #379) and the formula was computed in the owner's repository for the owner's question, so it is the owner's. Never tell the owner that something in this work was not done by the owner; the attribution rule is only for claims made in pasted third-party text.

## 6. Never write "what is yours" next to "what is forced"

2026-10-18: a reply split a check into "forced" and "what is the owner's". The owner read it as "somebody else already did what I did"
and asked to be shown who. It meant the choices the owner made in writing the line. Say "forced (true for every number)" and
"chosen by the owner (not forced)", and when no other source was found say so in the same breath.

## 7. A typo is fixed in the same reply, not parked

2026-10-18: replies listed slips in the owner's lines and in pasted text ("typo for 9", "unsupported") and left them as notes in files.
The owner: "a typo, and you're not going to fix it ... you're just gonna save it for later, for nothing." Write the corrected line, check it
(math/theorems/typo_fixes_2026_10_18.py is the model), use it, and go on. What cannot be fixed because the source lines are missing is said once, plainly,
with what is needed -- not as an open question and not as a note to come back to.

## 8. Right or wrong, not "holds"

2026-10-18: "holds" / "does not hold" was rejected by the owner as ambiguous: a line is right or it is wrong. In replies and in new files write
"right" / "wrong" and show the number ("3+6 = 9, the line says 8: wrong"). Old files keep their wording; new ones use these words.

## 9. Show it in the owner's notation -- corrected, with the process

2026-10-18: the owner could not read corrections written in another style (mod, tables). Write the owner's line, then the fixed line directly under it,
in the owner's own chain of digits, + and = (see math/theorems/typo_fixes_2026_10_18.py for the lines). Missing pieces are written the same way.

2026-10-19 (#371), correcting how this section was first applied: the owner's phone has no arrow key, so a dash between numbers is an arrow or a space,
not a minus ("12-23-36-34" is 12 -> 23 -> 36 -> 34; "5--4" under "6+5" is the pair 5 4). "Keep the owner's notation" never meant "leave it uncorrected":
the cleaned version uses arrows, a minus only for subtraction, spaces between numbers. And the cleaned version documents the PROCESS: the steps the owner
took to reach each answer, in order, each checked. Example that exposed it: #369, now written out in owner_work/PROCESS.md.

## 10. The process log -- owner_work/PROCESS.md

Every math message of the owner gets an entry, in the same turn, under its message number:
1. the owner's lines as typed (or a pointer to the picture);
2. the same lines cleaned (arrows for dashes, spaces, typos fixed and labelled);
3. the process: what the owner did at each step, in order, in plain words and the owner's chain notation;
4. the check of each step, right or wrong, and the file that holds the assertions.
Pasted material from other tools is not the owner's process and does not get an entry (it is audited in its own file).

Every count in an entry is given both ways, with and without (zero, the comma): #269 "no comma count should be explored also", #379 "so totals are for both". The example that exposed it: #378's count was first given without zero only (576); #379 asked for both (with zero: 51480 up to 8 digits).
