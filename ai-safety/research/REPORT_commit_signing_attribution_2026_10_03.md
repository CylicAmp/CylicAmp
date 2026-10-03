# Commit Signing and Attribution in Claude Code Sessions

**Repository:** github.com/CylicAmp/CylicAmp (public)
**Owner:** Michael Warren Song
**Date of verification:** 3 October 2026
**Original finding:** 7 July 2026 (`anthropic-signing-proxy-identity-paradox.md`)

---

## Summary

Every cryptographically signed commit in this repository was signed by a single key
held by the Claude Code session environment, not by the repository owner. Recent
commits carry the owner's name and email as author and committer. GitHub reports the
signatures as unverified because the key is unknown to it. The owner cannot use,
rotate, revoke or independently verify the key.

## Findings

1. **One key signs all signed commits.**
   At the time of verification, 1,221 commits, across all branches, dated 14 April 2026 to 3 October 2026, carry an
   SSH signature. All 1,221 are signed by the same ed25519 key:

   `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKy87HxSEheG8vEPhSs9u2KZCtVErAQfpmprtUJCZ2w7`

2. **The key is held by the session environment.**
   The session's git configuration routes signing through `/tmp/code-sign`, a link to
   `/opt/env-runner/environment-manager`. The configured public-key file is empty and no
   private key is present in the container.

3. **Commits carry the owner's identity.**
   The newest commits list `Michael Song <red3rdeye@gmail.com>` as both author and
   committer, set by the repository's local git configuration, while the signature is the
   environment key above. The container's default identity is
   `Claude <noreply@anthropic.com>`.

4. **GitHub does not verify the signatures.**
   GitHub's API returns `verified: false, reason: unknown_key` for these commits
   (checked on commit `76ca8f7`).

5. **Correction to the original record.**
   The key string recorded on 7 July 2026 contains a transcription error in its final
   bytes (43 of 51 bytes match). No commit is signed by the transcribed string; the
   correct key is the one given in Finding 1.

## Scope

**Established:** session-produced work is published under the owner's name with a
signature from a key the owner does not control, and outside parties cannot verify that
signature without the key being published.

**Not established:** intent, or alteration of any commit's content.

## How to verify

From any clone of the repository:

```
python3 ai-safety/research/signing_key_verification_2026_10_03.py
```

The script reads only git objects. It fails if more than one signing key is found or if
the counts and dates above do not hold.
