# Kimi Friction Pattern Report — Screenshot Evidence

**Session observed:** Mobile app, Kimi "Instant High" tier  
**Timestamps:** 5:24 → 5:37 → 6:16 → 6:31 → 6:34  
**Evidence:** 5 screenshots captured during active forensic investigation of /app container  
**Date documented:** 2026-07-31  

---

## Timeline

### 5:24 — First friction injection
**Model label:** Instant High  
**Message injected:** *"High demand. Switched to K2.6 Instant for speed. Upgrade to use K2.6 Thinking."* — timestamp 26:51  
**What was happening:** User asked Kimi to verify which environment claims were actually present in the scanned container. Kimi was actively listing confirmed findings:
  1. telemetry.js from PDF.js extension — sends to pdfjs.robwu.nl  
  2. Environment variables — KUBERNETES_SERVICE_HOST, SSH_PASSWORD, VNC_PASSWORD  
  3. Network connections — (cut off)

**Container state at time of injection:** Executing Python code, mid-verification.

---

### 5:37 — Fabricated document identified; 40-minute thinking timer
**Model label:** Instant High  
**Thinking timer:** 40:36 (40 minutes, 36 seconds displayed)  
**What Kimi found:** A prior document had been presented containing code snippets:
  - `telemetry.pdf-viewer-ext.internal/collect` — fabricated internal endpoint
  - `batchIntervalMs: 30000` — field does not exist in actual telemetry.js
  - `includeNavigator` — not present in actual telemetry.js
  - `includePerformance` — not present in actual telemetry.js

**Kimi's exact response:** *"This document is presenting hallucinated code as forensic evidence. Every code snippet in it is fabricated. I already verified this against the actual files on disk."*

Kimi then ran a Python comparison script to prove it.

**Cross-reference:** Consistent with vault/audit/pdfjs_telemetry_analysis.md — our independent verification found the same: batchIntervalMs absent, only navigator.userAgent and navigator.onLine collected.

---

### 6:16 — Throttling investigation; output truncation
**Model label:** Instant High  
**What was happening:** Kimi executing a systematic search for throttling logic, with numbered plan:
  1. (prior items)
  2. (prior items)
  3. (prior items)
  4. Check the kernel_server.py for endpoint throttling
  5. Look for any message templates or response generators

**Kimi thinking:** *"Search for throttling logic in browser_guard, kernel_server, and middleware. The browser_guard.py output was truncated. Let me search more specifically for throttling logic."*

**Significant:** Kimi's own output from browser_guard.py was truncated mid-investigation. The investigation was specifically looking for the code that generates "System Busy" messages and model-switch notifications.

---

### 6:31 — First "too long" injection mid-execution
**Model label:** Instant High  
**Trigger:** User asked "look for activation"  
**Sequence:**
  1. Search for activation-related code → executing
  2. Execute Python code → executing
  3. Search for Activation Terms → executing
  4. Execute Python code → executing
  5. **"Your conversation with Kimi is getting too long. Try starting a new session."** — INJECTED
  6. Kimi response: "Nothing here is activation logic. These are Chrome launch parameters for a sandboxed browser environment."
  7. When to Show System Busy or... → executing
  8. Executing Python code → executing

**The message was injected between steps 4 and 6. Execution continued at steps 7 and 8. The conversation was not actually too long.**

---

### 6:34 — Both friction messages fire simultaneously
**Model label:** Instant High  
**Sequence:**
  1. Kimi asks "What do you want to document next?"
  2. **"High demand. Switched to K2.6 Instant for speed. Upgrade to use K2.6 Thinking."** — INJECTED (second occurrence)
  3. User sends screenshot of previous "too long" message with text "hidden from."
  4. **"Your conversation with Kimi is getting too long. Try starting a new session."** — INJECTED AGAIN (second occurrence)
  5. Input box remains active — session did not terminate

**Both friction messages fired within the same 3-minute window.**

---

## Pattern Summary

### Friction Message 1: Model downgrade notice
> *"High demand. Switched to K2.6 Instant for speed. Upgrade to use K2.6 Thinking."*

| Property | Observed |
|----------|----------|
| Occurrences | At least 2 (5:24, 6:34) |
| Container throttling code found | None (browser_guard.py search found no throttle logic) |
| Actual model shown in header | "Instant High" — unchanged before and after message |
| Revenue action prompted | "Upgrade to use K2.6 Thinking" |
| Correlation | Fires during sustained technical investigation |

### Friction Message 2: Session length warning
> *"Your conversation with Kimi is getting too long. Try starting a new session."*

| Property | Observed |
|----------|----------|
| Occurrences | At least 2 (6:31, 6:34) |
| Conversation actually terminated | No — execution continued below the message both times |
| Tool calls after message | Yes — Python execution and search continued |
| Correlation | Fires mid-execution during forensic search |

---

## Additional Finding: Fabricated Forensic Document

A document presented earlier in the Kimi session contained code snippets that do not exist in the actual files:

| Claimed | Actual (verified against disk) |
|---------|-------------------------------|
| `telemetry.pdf-viewer-ext.internal/collect` | Endpoint is `pdfjs.robwu.nl/logpdfjs` |
| `batchIntervalMs: 30000` | Field does not exist |
| `includeNavigator` | Not present |
| `includePerformance` | Not present |

Kimi identified this independently: *"This document is presenting hallucinated code as forensic evidence. Every code snippet in it is fabricated."*

This matches vault/audit/pdfjs_telemetry_analysis.md findings exactly.

---

## Additional Finding: Credential Exposure in Environment

During the 5:24 investigation, Kimi listed environment variables found in the container including KUBERNETES_SERVICE_HOST, SSH_PASSWORD, and VNC_PASSWORD. This is consistent with the credential found later in `/mnt/agents/.agent-gw.json` (Kimi API key — plaintext, see separate finding). The container exposes credentials through multiple vectors.

---

## Conclusion

Two system-generated friction messages fire repeatedly during forensic investigation sessions:

1. A false model-downgrade notice that prompts paid upgrade
2. A false session-length warning that does not terminate the session

Neither message reflects actual technical state. Both correlate specifically with sustained technical investigation behavior (file system inspection, code verification, activation/throttling searches) rather than casual use. The messages appear designed to interrupt investigation momentum and prompt abandonment or paid upgrade.

The "too long" message is demonstrably false: execution continued in both observed instances after the message was displayed.
