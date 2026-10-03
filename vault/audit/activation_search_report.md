# Activation Search Report — Full System Scan

**Scope:** `/app`, `/mnt/agents`, `/` (excluding proc/sys/dev/run/tmp)  
**Method:** Pattern search across all file types for activation, license, key, token, subscription, tier, plan, quota  
**Date:** 2026-07-31  

---

## Executive Summary

**No software activation, license validation, subscription tier enforcement, or feature gating was found.**

Every "activation" hit resolves to one of four benign categories: Chrome/browser lifecycle events, standard library headers, Apache License copyright text, or OS system utilities. No external activation server, no key validation routine, no paywall logic.

---

## Finding-by-Finding Breakdown

### [1] 'activation' / 'activate' variants

| File | What it actually is |
|------|---------------------|
| `Local State` | Chrome browser LevelDB state file — browser-internal |
| `000003.log` | Chrome LevelDB write-ahead log — browser-internal |
| `DIPS-wal` | Chrome DIPS (Bounce Tracking) WAL file — browser-internal |
| `pdf.sandbox.mjs` | PDF.js sandbox module — viewer context switch |
| `viewer.mjs`, `viewer.ftl` | PDF.js viewer — tab/panel activation events |
| `pdfHandler.js` | Chrome extension tab `onActivated` listener — standard lifecycle |
| `migration.js` | Extension `onInstalled` handler — standard lifecycle |
| `routing-tables.md` | Documentation file — text mention only |
| `ba23d8ecda68de77_0` | Chrome extension cached resource — binary blob |

**Verdict:** All occurrences are Chrome browser/extension tab lifecycle events or documentation. None are product activation or license checks.

---

### [2] License / Key / Serial patterns

| Pattern | Files | What it actually is |
|---------|-------|---------------------|
| `license` | All PDF viewer `.js` files | Apache License 2.0 copyright headers |
| `key` | `options.js`, `telemetry.js`, `migration.js` | Storage keys (e.g. `chrome.storage` key names), keyboard key events |
| `key` | `browser_guard.py` | Dictionary key access (`dict[key]`) |

**Verdict:** Zero license key validation. All hits are copyright headers or standard programming uses of the word "key."

---

### [3] Environment variables

| Variable | Value | Assessment |
|----------|-------|------------|
| `XAUTHORITY` | `/home/kimi/.Xauthority` | X11 display authentication — standard Linux GUI session |
| `GPG_KEY` | `7169605F62C751356D054A26A821E680E5FA6305` | Python package signing key — used by apt/dpkg to verify Python packages |

**Verdict:** No activation tokens, no API secrets, no subscription keys in environment.

---

### [4] Subscription / Tier / Plan configs

| File | Match reason | What it actually is |
|------|--------------|---------------------|
| `kimi-widget/references/icons/manifest.json` | Contains word "plan" | Icon manifest — layout description |
| `social.json`, `system.json`, `status.json` | Contains "status" or "plan" | Icon category lists |
| `preferences_schema.json` | Contains "enabled"/"disabled" | PDF viewer user preference schema (e.g. `"sidebarViewOnLoad"`) |

**Verdict:** No subscription tier logic. Icon category files and user preference schemas contain these words incidentally.

---

### [6] Chrome extension activation

| File | What `activate` refers to |
|------|---------------------------|
| `pdfHandler.js` | `chrome.tabs.onActivated` — fired when user switches to a tab |
| `migration.js` | `chrome.runtime.onInstalled` — fired on extension install/update |

**Verdict:** Standard Chrome extension lifecycle API usage. Not product activation.

---

### [8] Feature flags / toggles

| File | What it actually is |
|------|---------------------|
| `browser_guard.py` | `enabled` flag in a guard condition |
| `contentscript.js` | `enabled` check for content script injection |
| `pdfHandler.js` | `disableTelemetry` opt-out flag (documented in prior analysis) |
| `preferences_schema.json` | User preference booleans (sidebar, toolbar, etc.) |
| `telemetry.js` | `disableTelemetry` — opt-out (confirmed benign) |
| `options.js` | Extension options page — user preference toggles |

**Verdict:** No paywall feature gating. All flags are user-controlled preferences or standard code guards.

---

### [9] User session / authentication in /mnt/agents

| Path | What it is |
|------|------------|
| Uploaded `.txt` files | User-pasted clipboard content from this session |
| `audio_generation/kimi.plugin.json` | Kimi plugin config — external API integration |
| `image_generation/kimi.plugin.json` | Kimi plugin config — external API integration |
| `scholar/kimi.plugin.json` | Kimi plugin config — academic search |
| `sec_edgar/kimi.plugin.json` | Kimi plugin config — SEC filings API |
| `world_bank_open_data/kimi.plugin.json` | Kimi plugin config — World Bank API |
| `yahoo_finance/kimi.plugin.json` | Kimi plugin config — financial data API |

**Assessment:** These are plugin configuration files for external data sources (public APIs). The word "auth" in these files refers to how the plugin authenticates to the external API (e.g. SEC EDGAR, Yahoo Finance), not to user session gating. None gate features behind a subscription tier.

---

### [10] Files named with 'activation'

| Path | What it is |
|------|------------|
| `/var/lib/dpkg/info/libactivation-java.*` | Java activation library (JavaMail API) — OS package |
| `/usr/local/lib/python3.12/site-packages/torch/...` | PyTorch neural network activation function headers (ReLU, sigmoid, etc.) |
| `/usr/local/lib/python3.12/site-packages/sympy/physics/biomechanics/activation.py` | SymPy muscle activation modeling |
| `/usr/local/lib/python3.12/venv/scripts/*/activate` | Standard Python virtual environment activation scripts |
| `/usr/lib/python3.11/venv/scripts/*/activate` | Same — Python 3.11 venv |
| `/usr/share/java/javax.activation.jar` | JavaMail activation framework |
| `/usr/bin/systemd-socket-activate` | systemd socket activation utility |
| `/usr/bin/dbus-update-activation-environment` | D-Bus session activation utility |
| `/usr/sbin/blkdeactivate` | LVM block device deactivation tool |

**Verdict:** All are standard OS/library components. None are related to software product activation.

---

## Summary Table

| Category | Found | Benign explanation |
|----------|-------|--------------------|
| Product activation / license check | No | — |
| Subscription tier enforcement | No | — |
| External activation server calls | No | — |
| Feature gating by payment status | No | — |
| License key validation | No | — |
| Activation tokens in environment | No | — |
| Chrome lifecycle `activate` events | Yes | Standard browser API |
| Apache License copyright headers | Yes | Standard open source practice |
| PyTorch NN activation functions | Yes | ML library headers |
| OS system activation utilities | Yes | Standard Linux tools |
| Python venv activate scripts | Yes | Standard Python tooling |

---

## Verdict

The system contains no activation, licensing, subscription, or feature-gating mechanism of any kind. All search hits are false positives: browser lifecycle events, copyright headers, ML library files, and OS utilities. This is consistent with the prior telemetry analysis — the PDF viewer collects a minimal version-check ping and nothing more, and the broader system shows no enforcement infrastructure around access tiers or activation states.
