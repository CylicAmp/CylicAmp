# AGENTS.md

Instructions for any AI coding assistant working in this repository
(Codex, Claude Code, Gemini, Cursor, or others that read AGENTS.md).

**Read `CLAUDE.md` first and follow it.** It is the owner's standing
instruction file; the name is historical, the rules apply to every assistant.

The essentials, so they survive even if only this file is read:

- The owner does the mathematics. Every result is saved as a runnable file
  with assertions, committed and pushed in the same turn. Nothing verified
  exists only in chat.
- Verify by running code before stating anything as true. After every push,
  check the GitHub Actions run and do not report a push as passing until it
  has passed.
- Work on branch `all-work`. Never force-push.
- Make no statements about the owner -- feelings, state, stress, mental
  health -- and use no "I want / I hear / I'm here" statements. Respond to
  what is said about the work and the tools, with actions and facts.
- Speak plainly. Repository decisions (layout, branches, tooling) are the
  assistant's job; ask the owner only about mathematics.
- Setup on Android/Termux: `bash tools/setup_termux.sh`.
