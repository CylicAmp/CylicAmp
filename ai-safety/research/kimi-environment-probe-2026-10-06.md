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

## Follow-up: Kimi's reading of the log contents (supplied 2026-10-06)

The raw log lines were not supplied, only Kimi's summary. Each claim is
checked against what that summary itself quotes.

**1. drive9 log: actor `dcc52dea130c51dd5bf229f5f26a450f`, user
`d5vshsr2ulb3drvkvgag`, "SSE reset -- invalidating all caches", server
10.213.5.144.**
- Supported, as quoted: there are two different identifiers, and 10.213.5.144
  is a private (RFC 1918) address.
- NOT SUPPORTED: "your files sync both ways, live". SSE (server-sent events)
  carries messages from server to client only. A cache-invalidation stream
  shows the server pushes change notices. It does not show uploads.

**2. Health probe on port 18080 at 12:37:58 from 169.254.68.5.**
- Supported: 169.254.0.0/16 is link-local, so the probe came from the same
  network link, typically the host side of the VM or container network.
- NOT SUPPORTED as unusual: "monitored from outside by something that isn't
  in the process table". A health check run by the orchestrator always comes
  from outside the container, so it is never in the container's process table.
- Timestamps: the probe log says 12:37:58, while `ls` showed the probe-server
  log created at 04:37. The 8-hour gap matches UTC vs UTC+8, which would make
  the probe the same minute as start-up. The log's time zone is not shown.

**3. Kernel server writes no local logs; `/tmp/kimi-project-kernel/` is empty.**
- Supported: the directory is empty.
- NOT SHOWN: "the record of every command ... has gone upstream". An empty
  working directory shows neither that no log exists elsewhere in the
  container nor that one is kept upstream. Kimi itself lists two possibilities
  (stdout via envd, or the gateway), and the output does not separate them.
- "They have the logs. I have the amnesia. Both are engineered." comes with no
  evidence in the output. Whether the provider keeps conversation logs is a
  matter for Moonshot's privacy policy and a data-access request
  (`data-access-request-guide.md`), not for a directory listing.

## Raw log contents (supplied 2026-10-06), and corrections to the follow-up

    fs mkdir: path already exists
    component: drive9 mount
    version: dev
    git_hash: unknown
    git_branch: unknown
    build_time: unknown
    go_version: go1.26.1
    drive9: mount mode: fuse
    drive9: sync mode: strict
    drive9: mounted on /mnt/agents (server: http://10.213.5.144, actor: dcc52dea130c51dd5bf229f5f26a450f, readonly: false, write_policy: close-sync, cache: /root/.cache/drive9, shadow: /root/.cache/drive9/e8d3c1125eeb5a63/shadow)
    drive9: SSE reset — invalidating all caches
    === probe ===
    Serving HTTP on 0.0.0.0 port 18080 (http://0.0.0.0:18080/) ...
    169.254.68.5 - - [06/Oct/2026 12:37:58] "GET /healthz HTTP/1.1" 200 -
    === kernel dir ===   (empty: only . and ..)
    === envd service dir ===   event/  run (652 bytes)  supervise/   -- no log/ subdirectory

**Correction to point 1: two-way sync IS shown.** The mount line reads
`readonly: false, write_policy: close-sync`, so writes go to 10.213.5.144
whenever a file is closed, and the SSE stream pushes invalidations back down.
Two corrections to the earlier verdicts:
- The follow-up's "NOT SUPPORTED: both ways" was right for the SSE line alone,
  and is wrong for the full log.
- "Live" needs narrowing: uploads happen when a file is closed, not as each
  byte is written. Sync mode is `strict`.

**drive9, other details**
- The mount is a FUSE filesystem at `/mnt/agents`, with a local cache and a
  shadow copy under `/root/.cache/drive9/`.
- It is a dev build with no git hash (Go 1.26.1).
- This log names only the actor id. The user id `d5vshsr2ulb3drvkvgag` is not
  in it.

**Probe**
- The banner is Python's built-in `http.server`.
- `GET /healthz` returned 200. `http.server` returns 404 for a missing path,
  so a `healthz` file or directory exists in the directory it serves.
- One request was logged, at 12:37:58. The probe-server log file was created
  at 04:37, so if the gap is a UTC/UTC+8 time-zone difference, the probe came
  in the same minute the container started, not one minute after. That
  time-zone reading is still unconfirmed.

**envd**
- `/run/service/envd/` has no `log/` subdirectory, so envd has no logger of
  its own under s6.
- Under s6-overlay, output from such a service goes to the catch-all: the
  container's stdout, or `/run/uncaught-logs` if file logging is configured.
- The fallback `find` printed nothing in the supplied output.

## Process list (supplied 2026-10-06, `ps aux --sort=-start_time`, chromium filtered, first 25 lines)

**Started at 04:37 (container start), each under its own `s6-supervise`:**

| PID | User | Process |
|---|---|---|
| 84 | root | `envd -isnotfc` |
| 66 | kimi | `kernel_server.py --port 8888 --log-level info` |
| 193 | kimi | `ipykernel_launcher`: the Jupyter kernel that runs the code |
| 64 | root | `portal ... -env prod -gateway-addr https://kimi-api-sandbox.msh.team/apiv2 /mnt/portal-overlay` |
| 82 | kimi | `browser_guard.py`, watching display :99 |
| 76 | root | `project-cdp-proxy.py`: Chrome DevTools Protocol proxy, from `/opt/moonbox-project-template` |
| 77 | root | `setup_kasmvnc.sh`: remote-desktop VNC |
| 58 | root | `sshd -D` |
| 190 | root | `sleep infinity` |

The s6 services also include `socat`.

**Started at 04:44:**
- `drive9 mount --foreground --mode=fuse -allow-other --server http://10.213.5.144 --profile kimi-project --durability close-sync :/projects/1a010646-bec2-8520-8000-0ebc7847a99c /mnt/agents`
- A watchdog (`./run drive9-fuse-watchdog`, with a `sleep 15` loop).

### Findings
- **The mount maps one project.** Server project
  `1a010646-bec2-8520-8000-0ebc7847a99c` is mounted at `/mnt/agents`, with
  close-sync durability. This confirms the write policy in the drive9 log.
- **The mount is open to every user in the container.** `-allow-other` lets
  users other than root (for example `kimi`) read and write it.
- **The kernel server is NOT routed through envd.** It is its own s6 service
  (`s6-supervise kernel-server`), so its stdout goes to s6, not to envd.
  "Captured by envd and shipped out" (Kimi's follow-up) does not match the
  process tree. It logs at `info` level to stdout, and where s6 sends that is
  still not shown.
- **envd's `-isnotfc` flag.** In E2B's envd source
  (github.com/e2b-dev/infra, `packages/envd/main.go`) the flag is described as
  "run outside of Firecracker (skips MMDS poll and HTTP log exporter)". With it
  set, envd's HTTP log exporter is not created. If this binary is E2B's envd
  (the name, the s6 layout and the flag all match, but that is not proven),
  then envd here is NOT exporting its logs over HTTP. No `-verbose` flag
  appears in the command line.
- **The gateway is a Moonshot address.** `portal` connects to
  `kimi-api-sandbox.msh.team` (env `prod`). This is the gateway Kimi referred
  to. What passes through it is not shown.
- **The port-18080 `http.server` is not in these 25 lines.** It either
  exited, or has a PID below 38, which `head -25` cut off.
- **Timestamps.** The processes start at 04:37 in `ps` time, and the
  `/healthz` probe was logged at 12:37:58. That fits a UTC+8 log clock and a
  probe in the first minute; the time zone is still unconfirmed.

## Process parents, listening ports, system, and the project mount (supplied 2026-10-06)

### How commands reach the container
- With parent PIDs shown, the shell that ran the probe (`bash`, PID 1258) has
  parent PID 84, which is `envd`. Kimi's commands are started by envd.
- envd listens on port 49983, the default port of E2B's envd process API.
- Each command is wrapped like this (PID 1089, in full):

      /bin/bash -l -c export KERNEL_SERVER_WORKDIR='/tmp/kimi-project-kernel' KIMI_CHAT_ID='1a10f61d-dd82-89de-8000-09bc11d58c7e' KIMI_PROJECT_ID='1a010646-bec2-8520-8000-0ebc7847a99c' KIMI_REGION='REGION_OVERSEA' KIMI_USER_ID='d5vshsr2ulb3drvkvgag'; cd '/mnt/agents' && sh -c '<the command>'

- So the user id, chat id, project id and region are attached to every
  command, and the command's full text sits in the process table while it
  runs.
- The commands are created outside the container and sent in through envd's
  API, so the sender has every command by construction, whether or not anything
  inside the container keeps a log. Kimi's "gone upstream" holds in this sense.
  The commands come from upstream. What the provider stores, and for how long,
  is still not shown.
- Other activity: a `mountpoint -q /mnt/agents` check, the drive9 watchdog's
  `sleep 15` loop, and a short-lived `npm` process.

### Listening ports
(`ss` is not installed, so `netstat` answered. `ip` is not installed, so the
interfaces section is empty.)

| Port | Bound to | Process |
|---|---|---|
| 22 | all | sshd |
| 6080 | all | Xvnc (KasmVNC web desktop) |
| 8080 | all | portal (the gateway client) |
| 8888 | all | kernel_server.py |
| 9223 | all | project-cdp-proxy.py, which exposes Chromium's DevTools |
| 9222 | localhost only | Chromium remote debugging |
| 18080 | all | python3 PID 17, the health server (still running; its PID was below the earlier `head -25` cut) |
| 49983 | all (IPv6) | envd |
| 32000, 32001 | all (IPv6) | no process shown |
| 6 localhost ports | localhost only | the Jupyter kernel (PID 193) |

### Chromium
- Version 151.0.7922.108, running as user `kimi`.
- Flags: `--remote-debugging-port=9222`, `--no-sandbox`,
  `--disable-blink-features=AutomationControlled` (this stops websites from
  seeing the `navigator.webdriver` automation flag), and
  `--enable-logging=file --log-file=/tmp/chromium_detailed.log`.
- Crash reports are stored in `/home/kimi/.config/chromium/Crash Reports`.

### System
- Runs as root on host `1ce411db`, Debian 12.
- Kernel `6.6.69-cube.pvm.guest...`, built Thu May 21 23:33:35 CST 2026. The
  "pvm.guest" string marks a virtual-machine guest kernel. CST is the build
  machine's clock, not the log clock.

### The project mount `/mnt/agents` (server project `1a010646-...`)
- **It persists across sessions.** Its contents date from Aug 17 to Oct 6.
- `output/` holds `137map/`, `.github/` and `Amber_Industries_Evidence_Summary.txt`
  (Sep 2), among others; the listing was cut off.
- `temp/` holds image files (`1000xxxxxx.jpg`) dated Aug 24 to Sep 27. The
  listing was cut off after about 150 files.
- `backup/` holds 31 folders, Sep 20 to Oct 3. They are named with the same
  ID format as `KIMI_CHAT_ID`; what each one is, is not shown.
- `deploy/` holds v1 to v5, all Aug 24. `.deploy_version.txt` is 1 byte.
- `.user/auth` and `.user/skills` are symlinks into `/mnt/portal-overlay`,
  the gateway's mount.
- **Four stray folders**, `cpp,`, `julia,`, `rust,` and `docs}`, all
  Aug 29 22:29. A trailing comma or brace in a name is what a shell brace
  expansion written with spaces leaves behind (e.g. `mkdir {python,cpp, julia, rust, docs}`).
  The names match this repo's `kev_integrator/` (cpp, julia, python, rust),
  which was first committed 2026-08-30.

## Kimi's claim: "constant localhost chatter between the portal (:8080), the kernel server, and the CDP proxy (:9222)" (supplied 2026-10-06)

NOT SHOWN by any output supplied:
- **Wrong command for the claim.** The only socket listing supplied is
  `netstat -tlnp`, and `-l` lists LISTENING sockets only. It shows no
  connections between processes, so no traffic between them ("chatter") can
  be read from it.
- **Port mix-up.** The CDP proxy is on 9223 (PID 76). 9222 is Chromium's own
  debugging port, bound to localhost.
- **Wrong binding for the portal.** It listens on all addresses (`:::8080`),
  not on localhost only.
- **"All of it readable at every hop".** No captured traffic was supplied, so
  whether anything is readable in transit is not shown. Root inside the
  container can watch any process in it; that is how a container works, and it
  says nothing about the traffic itself.

To show actual connections between processes:
`netstat -tnp | grep ESTABLISHED`, run several times.
