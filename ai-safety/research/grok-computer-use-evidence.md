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
