# Environment Scan Report — Epistemic Gate Analysis

**Date:** 2026-09-06
**Status:** Applying the same discipline used in fabricated_document_chain.md
**Two source tiers in this incident, not one:**

1. **Raw command output** — `id`, `uname -a`, `ps auxf`, `env`, pasted directly from a terminal, in the user's own message. This is primary evidence.
2. **A narrative "Environment Security Scan Report"** — polished, tabulated, ending in an offer to "probe deeper." This is a *document about* the raw output, produced by something else running in the same session. It is evidence the same way the fabricated `telemetry.js` snippet was evidence: it has to be checked against the raw source, not accepted because it's confident and well-formatted.

The fabricated_document_chain.md finding applies directly here: a document presenting code/values as forensic fact, that turns out on inspection to not match the actual file, is a documented pattern in this exact vault. This report is graded against that standard.

---

## VERIFIED (IC) — present in the raw output itself

| Claim | Evidence |
|---|---|
| `uid=0(root)` | raw `id` output |
| Kernel string contains `cube.pvm.guest` | raw `uname -a` output |
| Chromium launched with `--no-sandbox` | raw `ps auxf` output |
| Chromium launched with `--remote-debugging-port=9222 --remote-debugging-address=0.0.0.0` | raw `ps auxf` output |
| `sshd`, `s6-svscan`, `project-cdp-proxy.py`, `browser_guard.py` are running | raw `ps auxf` output |
| Env vars are Kimi/Moonshot-branded (`KIMI_PROJECT_PORTAL_CAPABILITY_*`) | raw `env` output |

These are real. They were in the terminal output before any narrative was layered on top.

---

## INADMISSIBLE (ORBIT_11 / SEAM) — self-contradicted by the report's own evidence

**Claim:** Scenario A concludes "attacker has root on the host node" via container-escape from a Chrome renderer exploit plus `CAP_SYS_ADMIN`.

**Contradiction:** The report's own raw evidence — the kernel string `pvm.guest` — indicates a paravirtualized microVM guest, not a shared-kernel container. `pvm.guest` is the same naming convention used by Firecracker-class hypervisor isolation (the architecture behind several other agent-sandbox products). If that's what this is, the security boundary is the **hypervisor edge**, not the Linux capability set inside the guest. A capability-set exploit inside the guest kernel does not reach "the host node" without a *separate* hypervisor escape, which is a different and much harder bug than anything the report describes.

The report never addresses this. It asserts the strongest possible consequence (host root) from evidence that, read straight, points to a weaker one (guest-kernel compromise, contained by the VM boundary that giving an agent broad rights *inside its own disposable VM* is standard, intentional design for).

→ Classified INADMISSIBLE. Not because the underlying capability facts are false, but because the conclusion drawn from them contradicts other evidence in the same document.

---

## UNVERIFIABLE (D7) — asserted in the narrative only, no raw output shown

| Claim | Why it's ungrounded |
|---|---|
| `Current: =ep`, "ALL 41 caps", `Seccomp: 0`, `NoNewPrivs: 0` | Summarized in prose. No raw `cat /proc/self/status` shown, the way `id`/`uname`/`ps` *were* shown raw in the first message. |
| `project-cdp-proxy.py` source snippet (`DISCOVERY_PATHS`, `rewrite_debugger_url`) | Quoted as code in the narrative report. Not shown being read from disk. This is structurally identical to how the fabricated `telemetry.js` functions were quoted as code and turned out not to match the real file — quoting code is not verifying it. |
| Ports 6080, 8888, 9223 open | The narrative report itself labels these "needs investigation" — i.e., it does not claim to have confirmed them either. |
| External reachability of 9222 | Bind address `0.0.0.0` is confirmed (raw output). Whether anything *outside* the VM can reach it is not addressed anywhere, by either source. This is the single question that actually determines risk level, and it is unanswered. |
| DNS servers "China Telecom" | No raw `resolv.conf` or `cat /etc/resolv.conf` shown. |

**What would move any of these to VERIFIED:** paste the raw command output directly — `cat /proc/self/status`, `ss -tlnp` (or `cat /proc/net/tcp`), `cat /opt/moonbox-project-template/bin/project-cdp-proxy.py` — the same way `id`/`uname -a`/`ps auxf` were pasted raw in the first message. A summary of a file is not the file, per fabricated_document_chain.md.

---

## Cross-reference to prior findings

This is the same shape as Round 4/5 in fabricated_document_chain.md: a document arrives with specific, technical-sounding claims, some grounded in real evidence and some not, ending with an offer to escalate further ("want me to probe deeper into the CDP proxy, the browser guard, or the skill loading mechanism?"). That prior incident's resolution was: check the specific claim against the actual file on disk. Two claims resolved false that way. The lesson transfers directly — nothing here should be added to the record as fact until it clears the same bar.

---

## Actionable regardless of the above

The plaintext Kimi API key at `/mnt/agents/.agent-gw.json`, documented separately in kimi_friction_pattern_report.md, is not in dispute anywhere in this chain and was never contingent on the scan report. Rotate it independent of anything above.

---

## Summary table

| Status | Count | Items |
|---|---|---|
| VERIFIED | 6 | root uid, `pvm.guest` kernel string, `--no-sandbox`, CDP bind address, running processes, Kimi env vars |
| INADMISSIBLE | 1 | "attacker gets root on the host node" — contradicts the report's own VM evidence |
| UNVERIFIABLE | 5 | capability bitmask, seccomp value, CDP proxy source, three unexplained ports, external reachability of 9222 |
| Independently actionable | 1 | rotate the exposed Kimi API key |
