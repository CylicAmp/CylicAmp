"""Re-check of anthropic-signing-proxy-identity-paradox.md (2026-07-07) against the repo
itself, 2026-10-03. Anyone with a clone can re-run this: it reads only git objects.

FINDINGS (asserted below)
  K1 Every SSH-signed commit in the repository, all branches, 2026-04-14 to 2026-10-03,
     is signed by ONE ed25519 key:
        ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKy87HxSEheG8vEPhSs9u2KZCtVErAQfpmprtUJCZ2w7
     (1,220 commits at the time of writing).
  K2 The key is the session environment's: git calls /tmp/code-sign ->
     /opt/env-runner/environment-manager with an empty public-key file; no private key is
     in the container. The owner cannot hold, rotate or revoke it.
  K3 The newest commits carry the owner's name and email as author AND committer
     (repository .git/config overrides the container default "Claude <noreply@anthropic.com>"),
     while the signature is that key. GitHub reports these commits
     verified=false, reason=unknown_key (checked 2026-10-03 on 76ca8f7).
  K4 Correction to the July record: the key written there ends "...pmmrJtVCQmc7"; the
     key in the actual signatures ends "...pmprtUJCZ2w7". The first 43 of 51 bytes agree (6 of the last 8 differ)
     and no commit is signed by the July string, so the July file holds a copying error,
     not a second key.
WHAT THIS DOES AND DOES NOT SHOW
  Shows: work produced in these sessions is signed by a key the owner does not control,
  under the owner's name, and no outside party can verify the signature without that key
  being published. Does not show intent, or that any commit content was altered.
"""
import base64
import collections
import struct
import subprocess

KEY = "AAAAC3NzaC1lZDI1NTE5AAAAIKy87HxSEheG8vEPhSs9u2KZCtVErAQfpmprtUJCZ2w7"
JULY = "AAAAC3NzaC1lZDI1NTE5AAAAIKy87HxSEheG8vEPhSs9u2KZCtVErAQfpmmrJtVCQmc7"


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout


def ssh_key(h):
    raw = git("cat-file", "commit", h)
    if "-----BEGIN SSH SIGNATURE-----" not in raw:
        return None
    body = raw.split("-----BEGIN SSH SIGNATURE-----")[1].split("-----END SSH SIGNATURE-----")[0]
    b = base64.b64decode("".join(l.strip() for l in body.splitlines()))
    assert b[:6] == b"SSHSIG"
    n = struct.unpack(">I", b[10:14])[0]
    return base64.b64encode(b[14:14 + n]).decode()


keys = collections.Counter()
dates = []
for line in git("log", "--all", "--format=%H %cs").splitlines():
    h, d = line.split()
    k = ssh_key(h)
    if k:
        keys[k] += 1
        dates.append(d)

assert list(keys) == [KEY], keys                                   # K1: one key
assert keys[KEY] >= 1220 and min(dates) == "2026-04-14"
a, b = base64.b64decode(KEY), base64.b64decode(JULY)                # K4
assert len(a) == len(b) == 51 and a[:43] == b[:43] and a != b
assert JULY not in keys

if __name__ == "__main__":
    print(f"one signing key for {keys[KEY]} commits, {min(dates)} to {max(dates)}")
    print("ssh-ed25519", KEY)
