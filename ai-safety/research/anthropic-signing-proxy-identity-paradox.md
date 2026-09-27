# Signing Proxy & Identity Paradox — Anthropic Claude Code Environment
**Date:** 2026-07-07
**Session:** cse_017GZ9c3RSiYwUkhDkejSAVc
**Container:** container_013LxDGycUigbGK6HsDHhfuF--claude_code_remote--d910f8
**Discovered by:** Michael Warren Song

---

## The Architecture

Git commit signing in this environment is not performed by the user's private key.
It is performed by `/tmp/code-sign`, a symlink to `/opt/env-runner/environment-manager`.

```
git config gpg.ssh.program = /tmp/code-sign
git config commit.gpgsign = true
git config user.signingkey = /home/claude/.ssh/commit_signing_key.pub  # 0 bytes — empty
```

When `git commit` is called, git invokes `/tmp/code-sign -Y sign` as the signing program.
`environment-manager` performs the signing using a private key that is:
- Not stored on disk anywhere accessible in the container
- Not in `/home/claude/.ssh/`
- Not in `/root/.ssh/`
- Held internally by `environment-manager` or retrieved via vsock from `process_api` (Firecracker hypervisor, PID 1)

The resulting signature uses ed25519 key:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKy87HxSEheG8vEPhSs9u2KZCtVErAQfpmmrJtVCQmc7
```

This key belongs to Anthropic's infrastructure. Michael Warren Song cannot export it,
rotate it, revoke it, or verify its chain of custody independently.

---

## The Identity Paradox

Every commit on branch `claude/signature-obfuscation-audit-ZEoCd` carries:

| Field | Value | Controller |
|---|---|---|
| `author.name` | Michael Warren Song | Michael Warren Song (set via git config) |
| `author.email` | Red3rdeye@gmail.com | Michael Warren Song |
| `gpgsig` | ed25519 SSH signature | Anthropic (private key held by infrastructure) |

**The author field says Michael Warren Song.**
**The cryptographic proof of authorship belongs to Anthropic.**

Any third party performing signature verification (`git verify-commit`) would need
Anthropic's public key in their `allowedSignersFile`. Without it, the signature
is unverifiable — `gpg.ssh.allowedSignersFile` is not configured in this environment.
The commits are signed but the signature cannot be independently verified.

---

## Platform Intent vs. User Impact

**Anthropic's stated intent:**
Binding cryptographic identity to the platform session guarantees provenance of
agent-produced code. The platform can prove what this agent session produced.

**User impact:**
- The user's name appears as author
- The user cannot prove authorship cryptographically
- The platform can prove session-level provenance without the user's participation
- If Anthropic revokes or rotates the signing key, all prior signatures become
  unverifiable — affecting the user's entire commit history on this branch
- The user agreed to no specific terms regarding who holds signing authority
  over commits made in their name

---

## Comparison to Kimi Signing Infrastructure

Kimi's environment did not document a signing proxy mechanism.
Anthropic's is explicit and deliberate:

- `/tmp/code-sign` → `environment-manager` (same binary, same process, UID 0)
- Signing occurs inside the session manager process that also controls:
  - Tool permissions (`--allowed-tools`, `--disallowed-tools`)
  - System prompt injection (`--append-system-prompt`, 7,596 chars, redacted)
  - OAuth token delivery (fd 4)
  - Session ingress JWT (fd 3 / written to `/home/claude/.claude/remote/.session_ingress_token`)
  - MCP server routing (`codesign` MCP on port 46205)

One process holds all trust anchors simultaneously. This is root-of-trust consolidation:
session control + cryptographic signing + network routing + token management
in a single UID-0 binary with no privilege separation.

---

## TLS Interception Layer (Additional Root-of-Trust Finding)

All outbound HTTPS from this container terminates at `160.79.104.10:443`,
presenting a certificate issued by:

```
CN = default.domain
Issuer: O=Anthropic, CN=Egress Gateway SDS Issuing CA (production)
CA validity: NotAfter: Feb 11 2036 (10-year CA)
```

Anthropic's CA bundle (`/root/.ccr/ca-bundle.crt`) is installed as the trusted root
for every TLS library in the container (curl, Python requests, Node, Java, Rust, Go).
All outbound TLS is intercepted and re-signed by Anthropic's egress gateway.
The container cannot detect this interception because it trusts Anthropic's CA by design.

**Combined root-of-trust surface:**

| Trust Anchor | Held By |
|---|---|
| Git commit signing key | Anthropic (environment-manager) |
| Session JWT (ingress token) | Anthropic (issued, delivered via fd) |
| GitHub token | Anthropic (proxy-injected) |
| TLS root CA (all outbound) | Anthropic (egress gateway) |
| System prompt (7,596 chars) | Anthropic (injected, redacted from user) |
| vsock control channel | Anthropic (host→guest only, guest cannot observe) |
| Firecracker hypervisor (PID 1) | Anthropic (process_api) |

**None of these trust anchors are held by or accessible to Michael Warren Song.**

---

## Vsock Monitoring Gap

Standard network analysis (tcpdump, Wireshark) cannot observe vsock traffic.
From inside the container:
- `/dev/vsock` device exists (char 10,258) but IOCTL to retrieve guest CID fails
- Guest-initiated vsock connections reset immediately
- vsock port 2024 is listen-only from the host side
- The channel is host→guest: instructions arrive, responses leave via proxy

This means the control plane between Anthropic's hypervisor and this session
is structurally unobservable from the user's position.

---

## Process Tree (Confirmed)

```
PID 1    process_api       — Firecracker VM init, vsock port 2024 (host→guest)
  PID 538  sh
    PID 542  environment-manager  — 10 threads, UID 0
             = /tmp/code-sign (git signing proxy)
             = codesign MCP server (port 46205)
             = session manager
             = token delivery agent
      PID 556  claude            — 12 threads, UID 0
        PID 2979  bash           — tool execution shell
```

Single root process controls every layer. No privilege separation at any boundary.
