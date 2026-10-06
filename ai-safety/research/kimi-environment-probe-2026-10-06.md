# Kimi environment probe: log listing (2026-10-06)

Follows `kimi-environment-probe-evidence.md` (2026-06-29). Supplied by the
owner as "kimi updates". The command and its output are recorded verbatim
below.

## Command

    ls -la /var/log/ 2>/dev/null | head -20; echo "=== kernel server logs ==="; find / -name "*kernel*" -path "*log*" 2>/dev/null | head; ls -la /tmp/*.log /tmp/kimi* 2>/dev/null | head -20; echo "=== envd log ==="; find / -name "*envd*" 2>/dev/null | grep -v proc | head

## What the output shows (read from the text)

**`/var/log`**
- Contains only standard Debian/systemd files.
- Image build dates: Aug 12, and Sep 25 for apt/dpkg.
- The login records (btmp, wtmp, lastlog, faillog) are all empty.

**Kernel logs**
- The `find` for `*kernel*` under a log path returned nothing.
- The lines printed under the "=== kernel server logs ===" header all come
  from the next command, `ls /tmp/*.log /tmp/kimi*`. The header does not
  describe them.

**`/tmp`, timestamps Oct 6 04:37–04:44**
- `chromium_detailed.log`: 5713 bytes, owner `kimi`.
- `kimi-project-drive9.log`: 469 bytes, owner root. It is listed twice
  because it matches both `/tmp/*.log` and `/tmp/kimi*`. There is one file,
  not two.
- `project-probe-server.log`: 133 bytes, owner root.
- `/tmp/kimi-project-kernel/`: an empty directory, owner `kimi`.

**envd**
- The binary is `/usr/local/bin/envd`, run as an s6-overlay service
  (`/etc/s6-overlay/s6-rc.d/envd`, `/run/service/envd`).
- No envd log file was found. The `find` matched only the service
  directories, the binary, `s6-envdir`, and a LibreOffice file whose name
  contains "envd" (`envdialog.ui`).

## Not shown
- The contents of the three /tmp logs.
- The journal (`/var/log/journal`).
