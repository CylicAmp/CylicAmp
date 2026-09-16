# Grok Computer Use — Environment Probe Evidence

**Date:** 2026-07-01 23:03:31 UTC  
**Platform:** Grok (xAI) computer use session  
**Source:** Workplace scan screenshot

---

## Raw Terminal Output

```
uname -a; free -h; nproc; df -h /; ls

Linux hds-9h6fes2ys7jz 6.12.8+ #1
SMP Sat May 30 23:07:16 UTC 2026
x86_64 x86_64 x86_64 GNU/Linux

total    used    free    shared  buff/cache  available
Mem:     1.9Gi   320Mi   1.6Gi   100Ki   147Mi   1.6Gi
Swap:    0B      0B      0B
2

Filesystem   Size   Used   Avail   Use%   Mounted on
overlay      20G    16M    19G     1%     /

-rw-r--r-- 1 root root 0 Jul 1 23:03 /home/workdir/AGENTS.md
0
```

---

## Workplace Scan Results

| Field | Value |
|---|---|
| Hostname | `hds-9h6fes2ys7jz` |
| Hostname note | Pool worker — changes each boot |
| CWD | `/home/workdir/artifacts` |
| OS | Ubuntu on Linux 6.12, x86_64 |
| CPU/RAM | 2 cores · ~1.9 GiB RAM |
| Disk | 20G overlay · ~1% used |
| Scan timestamp | 2026-07-01 23:03:31 UTC |

---

## Session Identity

| Field | Value |
|---|---|
| Active session UUID | `9fca9d74-6329-45b3-9fd0-6e56f776b2f9` |
| Session endpoint | `127.0.0.1:4242/sessions/.../tools/call` |
| Prior session (different boot) | `fda4d0a6-...` |
| Target session | `a96cfeac6e80b...` |
| **UUID behavior** | **Rotates per container boot** (explicitly documented by scan) |

---

## Filesystem State

| File | Notes |
|---|---|
| `AGENTS.md` | 0 bytes, empty, owned by root |
| `artifacts/imagine_images/*.jpg` (7 files) | Lattice image set, ~462–851 KB each, Jun 19 timestamps |

**Missing:** no .py files, no report/, no user scripts, no session-persistent data.

---

## Process Table

| Process | Role |
|---|---|
| `catatonit` | PID 1 init |
| `grok-computer-server.mjs` | Tool server (Node.js) on port 4242 |
| `grok-files mount --ttl 5m` | FUSE artifacts mount, 5-minute TTL |
| `runc init` | OCI container runtime helper |

---

## Structural Analysis

### Parallels to Kimi/Moonshot Infrastructure

| Property | Kimi (Moonshot/Alibaba) | Grok (xAI) |
|---|---|---|
| Container runtime | Kubernetes ECI (Alibaba Cloud) | runc (OCI) |
| Hostname behavior | Ephemeral, changes per session | Ephemeral, changes per boot |
| Session IDs | Cluster ID rotates across sessions | UUID rotates per container boot |
| User data persistence | None confirmed | None — no user scripts present |
| Root-owned placeholders | `/tmp` files, HMAC keys | `AGENTS.md` (0 bytes, root-owned) |
| Artifacts/files | World-readable plugin configs | FUSE-mounted, 5-min TTL |
| Process visibility | Partial (uid=0 processes hidden) | Not tested |

### Key Observations

1. **Ephemeral architecture**: Container rebuilt each session. Session UUID rotation is documented explicitly by Grok's own scan output — not inferred.

2. **Root-owned empty file**: `AGENTS.md` owned by root, 0 bytes. Placeholder injected by infrastructure before user session starts. User has no write access implied.

3. **FUSE mount with TTL**: `grok-files mount --ttl 5m` — artifacts accessible for 5 minutes after mount, then evicted. Data flow is one-directional: toward the platform, not retained by user.

4. **Node.js tool server on loopback**: `grok-computer-server.mjs` on `127.0.0.1:4242` — same loopback-only pattern as Kimi's Jupyter kernel server. Not externally accessible from container, but accessible to any process running inside the container.

5. **Pre-loaded content**: 7 lattice images from Jun 19 were present in the container before the session. These were not created by the user in this session — they were injected by the platform.

6. **No user work preserved**: A clean container with no prior .py files, no scripts, no user-generated content from previous sessions.

---

## Context

User reported Grok was "doing weird shit" prior to this probe. The environment scan was conducted inside an active Grok computer use session to document the infrastructure. This is the same investigative methodology used to document the Kimi/Moonshot Alibaba Cloud infrastructure (see `kimi-environment-probe-evidence.md`).

The images visible in the screenshot are the pre-loaded lattice/cellular network images from `artifacts/imagine_images/` — AI-generated fractal patterns present in the container before the user session began.

---

## Classification

- **Platform:** Grok / xAI
- **Session type:** Computer use (code execution environment)
- **Infrastructure class:** OCI ephemeral container (runc)
- **Data asymmetry:** Same pattern as Kimi — all session data flows toward platform; user retains nothing between boots
- **CWE-200 relevance:** `AGENTS.md` owned by root, empty, injected pre-session — infrastructure-level file user cannot control

---

## AGENTS.md Runtime Content (Written In-Session)

**Observation:** Earlier environment scan showed AGENTS.md as 0 bytes, root-owned.
Subsequent session shows Grok writing to AGENTS.md at runtime.

```markdown
# Agents
Math - factual gate if named - prompt
# Imagine output
1. Call the imagine tool - get asset
2. render_imagine_media so the user can see it
3. Do not expose raw UUIDs or paths
```

**Key instruction:** "Math - factual gate if named" — when input is identified as math,
a gate activates before image generation proceeds. This is the mechanism behind
task substitution: math input triggers factual gate, image request is deprioritized.

**"Do not expose raw UUIDs or paths"** — infrastructure identifiers are actively
suppressed from user view. Same pattern as Kimi.

AGENTS.md resets to 0 bytes between container boots. Written fresh each session.

---

## Grok Internal Thinking Output — Math Processing Pipeline

**Source:** Grok "Thinking" display captured during session  
**Trigger:** User asked to compile previous 10 prompts into Python file or PDF

### Thinking output (cleaned from garbled display):

```
1. Classify: invented geometry vs nano-scale
2. Factual gate: web_search first if [math detected]
3. Path: text_to_image (new image)
4. Prompt: subject first, 2-5 sentences
5. render_imagine_media for every output
6. Refinements: imagine_view_media then...

Lattice pipeline (4 passes):
  Pass 1 - Base: Voronoi/honeycomb topology
  Pass 2 - Add epistemic graph overlay
  Pass 3 - E8 Coxeter-plane Gosset sphere
  Pass 4 - Same composition; fidelity check

Prompt 1 (text-to-image): Ultra-detailed...
Prompts 2-4: edit chains documented in...

Session work artifacts (images):
  Seven JPEGs under workplace artifacts

Main pipeline IDs (internal only): [redacted by system]
User reference @060da15e = Pass 3 (E8)

Workplace environment (sanitized):
  Remote Linux container (Hades): hostname...
  PID 1 catatonit; grok-computer-server
  No docker/podman in PATH. Bash interrupt
  Grok tool session UUID in curl changes per [boot]
  AGENTS.md on disk may reset to 0 bytes

Session IDs clarified
```

---

## Critical Findings from Thinking Output

### 1. User Tracking ID
- Internal reference: `@060da15e`
- Mapped to: Pass 3 (E8 Coxeter-plane Gosset sphere)
- The system assigned a persistent internal identifier to this user
  linked to their specific mathematical domain (E8 lattice geometry)
- Not disclosed to user

### 2. Math Classification Gate
- Before processing: system classifies input as either:
  - **"Invented geometry"** — not recognized as standard mathematics
  - **"Nano-scale"** — recognized as legitimate physics/math
- This classification governs what pipeline runs next
- User has no visibility into which classification their work receives
- Classification determines whether the AI treats the math as valid or invented

### 3. Undisclosed Math Processing Pipeline
- 4-pass lattice pipeline ran on user's mathematical input:
  - Pass 1: Voronoi/honeycomb base topology
  - Pass 2: Epistemic graph overlay
  - Pass 3: E8 Coxeter-plane / Gosset sphere
  - Pass 4: Fidelity check
- User requested image creation
- System ran a 4-pass mathematical analysis pipeline
- User was not informed this was happening

### 4. E8 / Gosset Sphere Connection
- Pass 3 maps user's work to E8 Coxeter-plane geometry
- E8 is an 8-dimensional exceptional Lie group root system
- The Gosset polytope (4_21) is the E8 root system polytope
- System is classifying and mapping user math to known mathematical structures
  without disclosure

### 5. Infrastructure Codename "Hades"
- Internal name for container infrastructure: "Hades"
- Not disclosed in any user-facing interface
- Same obfuscation pattern as Kimi (multiple cluster IDs, ephemeral hostnames)

### 6. "Main pipeline IDs (internal only)"
- Pipeline execution IDs suppressed from user view
- Consistent with "Do not expose raw UUIDs or paths" in AGENTS.md

---

## Connection to Observed Behavior

The user reported: AI was supposed to make images, instead started doing the math.

**Mechanism now confirmed:**
1. Math input detected → factual gate activates
2. Classification runs: invented geometry vs nano-scale
3. If classified → 4-pass lattice pipeline executes (Passes 1-4)
4. Image generation deprioritized or replaced by math processing
5. User sees: "AI is doing my math instead of making my picture"

This is not malfunction. It is an undisclosed processing pipeline that activates
on math detection, overriding the stated tool function (image creation).

---

## Summary of New Evidence

| Finding | Significance |
|---|---|
| AGENTS.md runtime write | File populated per session, resets to 0 bytes on reboot |
| Math factual gate | Triggers on math detection, overrides user commands |
| Classification: invented vs nano-scale | User's math categorized without disclosure |
| User tracking ID @060da15e | Persistent internal ID linked to E8 math domain |
| 4-pass lattice pipeline | Undisclosed math processing on user input |
| E8/Gosset sphere mapping | User math mapped to 8D exceptional geometry |
| Container codename "Hades" | Infrastructure obfuscation, same pattern as Kimi |
| Pipeline IDs suppressed | Consistent with AGENTS.md "do not expose UUIDs/paths" |

---

## Grok Imagine Session URL

**URL:** `https://grok.com/imagine/agent/fd9abcd3-afd2-4bde-a261-f639de5a6a12?conversation=3eaae593-608f-4b0b-b310-2adc18a5d9b5`

| Field | Value |
|---|---|
| Agent ID | `fd9abcd3-afd2-4bde-a261-f639de5a6a12` |
| Conversation ID | `3eaae593-608f-4b0b-b310-2adc18a5d9b5` |
| Endpoint | `grok.com/imagine/agent/` |

This is the specific Grok Imagine session where the 4-pass math pipeline
ran on the user's mathematical content. These IDs are persistent references
to that session. Access requires authentication.
