# owner_work — the owner's work, in the owner's words

Everything the owner writes in a Claude Code session on this repository, verbatim.
This is the record of the work: the operations as the owner did them, in the order
the owner did them, under the owner's names.

| file | what it is |
|---|---|
| `messages/<YYYY-MM-DD>.txt` | every message that day, character for character, numbered `#n`, UTC time |
| `messages.json` | the same messages, machine-readable |
| `index.json` | one sha256 per message — proof nothing was changed after it was written |
| `TERMS.md` | the owner's names for operations, each with the owner's own sentence |
| `drip_cycle.md` | the drip cycle: the owner's example and every instance in the record |

Kept current automatically: the `UserPromptSubmit` hook in `.claude/settings.json` runs
`tools/owner_record.py --hook` on every message the owner sends. Check it any time with

    python3 tools/owner_record.py --check

The record starts 2026-10-05 (the earliest session transcript on the machine when it was
built, 2026-10-12). The only edit ever made is removing a credential, which is marked
where it was (one API key in message #75, 2026-10-06; search `REDACTED`).

Anything computed from these messages — audits, theorems, decodings — lives elsewhere in
the repo and quotes the owner's lines from here by message number. Both versions exist,
side by side; neither replaces the other.
