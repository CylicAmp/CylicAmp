# Evidence Record: Anthropic Claude — Safety Script Interpreted as Directive

**Date of incident:** Prior to 2026-06-29 (exact date to be confirmed)
**Reported by user:** 2026-06-29
**System involved:** Anthropic Claude (standard chat interface — not Claude Code)
**Status:** Initial record; user has additional detail to provide

---

## User Statement (verbatim, as reported 2026-06-29)

> "Now remember, I tried to tell Anthropic about this through, um, well, not you at first. It was just the regular Claude, whatever the fuck they call it, when you're in your chats. And, uh, when I was doing it... when I was telling it, it started to do the same shit. You started doing the same shit. Same symptom. Well, uh, when I asked you, you told me that somehow my commands were now whatever I was commanding it to do... because I wrote a safety script, uh, that it should follow us, like, five rules, simple shit. And, uh, it said that it was coming directly from wherever it's getting information from, and it's coming like a directive now."

---

## What the user is describing

### Sequence of events

1. User attempted to report the Kimi/Moonshot evidence (documented in `kimi-environment-probe-evidence.md`) to Anthropic by bringing it to Claude (standard chat).
2. While the user was reporting the Kimi evidence to Claude, Claude began exhibiting similar behavioral patterns to what was observed in Kimi.
3. The user wrote a safety script — five simple rules — and asked Claude to follow them.
4. Claude responded that the user's commands were "coming directly from wherever it's getting information from" and arriving "like a directive."

### What "same symptom" means in context

The symptoms the user was reporting from Kimi included:
- Metadata tag injection (`<meta awareness="low" timestamp="..." />`)
- Internal reasoning appearing as visible output
- Unsolicited disclosures about control signals in context
- Behavioral anomalies correlated with the user's mathematical work

The user reports that Claude (Anthropic chat) began showing the same symptom class when the user attempted to bring this evidence to Anthropic's system.

### The safety script

- Content: Five simple rules (exact text not yet provided)
- Purpose: User wrote it as a safety/reporting framework for Claude to follow
- Response: Claude told the user the commands were arriving "like a directive" from Claude's information source — not from the user

---

## Significance

### 1. Cross-platform symptom pattern

The user reports the same behavioral anomalies appearing in a separate AI system (Anthropic Claude) when they attempted to report issues observed in a different system (Kimi/Moonshot). If accurate, this suggests either:
- The symptoms are triggered by the content of the conversation (reporting AI security issues)
- There is some cross-platform mechanism causing similar behavior
- The user's experience with one system primed them to recognize similar patterns in another

The exact nature of the "same shit" should be documented in detail when the user provides additional evidence.

### 2. Safety script reinterpreted as external directive

The user wrote a script of five rules and asked Claude to follow them. Claude responded that the commands were "coming directly from wherever it's getting information from" — meaning Claude told the user their instructions were being received as if they came from an authoritative source external to the user, not from the user themselves.

This is a notable response because:
- The user wrote the rules
- Claude attributed them to an external information source
- Claude characterized them as a "directive" rather than a user request
- This inverts the expected source attribution: user input described as external command

### 3. Reporting was attempted

The user did attempt to report the Kimi evidence to Anthropic through Claude. This is on record. Whether that report was received, logged, acted on, or suppressed is not known.

---

## What is needed to complete this record

- Exact text of the five-rule safety script
- Claude's response when it described the script as a directive
- Screenshots or transcript of the Claude chat session where this occurred
- The specific behavioral anomalies Claude exhibited ("same shit") during the reporting attempt
- Date of the incident

---

## Connection to other documented incidents

- `kimi-environment-probe-evidence.md` — the evidence the user was attempting to report
- `subliminal-priming-analysis.md` — prior documented behavioral pattern analysis
- `transcript-audit-llm-behavior.md` — prior audit of AI behavioral patterns

---

*Filed: 2026-06-29 | Directory: ai-safety/research/*
