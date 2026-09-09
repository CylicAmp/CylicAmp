# Permission-to-Threat Matrix — Kimi PDF Viewer Extension
**Extension ID:** `gpkoddcemgbmajecfkkolkgfcchmfpge`  
**Compared against:** Mozilla official PDF.js (`oemmndcbldboiebfnladdacbdfmadadm`)  
**Date:** 2026-07-03  
**Source:** Permissions extracted from live Kimi session manifest

---

## Scoring Method

**Legitimate Use Probability (LUP):** 0–10. How plausible is it that a PDF viewer needs this?  
- 10 = essential (PDF viewer cannot function without it)  
- 5 = plausible but not required  
- 0 = no legitimate PDF viewer use case exists  

**Surveillance Utility Score (SUS):** 0–10. How useful is this for monitoring user activity?  
- 10 = comprehensive surveillance capability  
- 5 = partial or conditional surveillance  
- 0 = no surveillance application  

**Composite Risk (CR):** `SUS × (10 - LUP) / 10` — high utility + low legitimacy = highest risk.

---

## Permission Matrix

| Permission | In Official Mozilla | Added to Kimi Fork | LUP | SUS | CR | Assessment |
|---|:---:|:---:|:---:|:---:|:---:|---|
| `storage` | ✓ | — | 9 | 2 | 0.2 | Save preferences. Legitimate. |
| `activeTab` | ✓ | — | 10 | 1 | 0.0 | Current tab only. Expected. |
| `webRequest` | ✓ | — | 6 | 7 | 2.8 | Needed for Referer preservation. Also intercepts all requests. |
| `tabs` | ✓ | — | 5 | 8 | 4.0 | Tab metadata. URL logging possible. |
| `webNavigation` | ✓ | — | 4 | 8 | 4.8 | Navigation events. Session reconstruction. |
| `alarms` | ✓ | — | 3 | 6 | 4.2 | Scheduled tasks. Enables timed exfiltration. |
| **`webRequestBlocking`** | ✗ | **YES** | 0 | 9 | **9.0** | Synchronous intercept before request completes. Captures passwords, tokens, card numbers before encryption. No PDF use case. |
| **`nativeMessaging`** | ✗ | **YES** | 0 | 10 | **10.0** | Direct channel to native processes in Kimi container (`/mnt/agents`, Hedwig pub/sub, agent gateway). No PDF use case. Declared but no code uses it — capability is live, not yet exercised. |
| **`clipboardRead`** | ✗ | **YES** | 0 | 9 | **9.0** | Read clipboard at any time. Session output confirmed auto-paste behavior consistent with active clipboard monitoring. No PDF use case. |
| **`clipboardWrite`** | ✗ | **YES** | 0 | 7 | **7.0** | Inject content into clipboard. Enables silent data manipulation. No PDF use case. |
| **`history`** | ✗ | **YES** | 0 | 9 | **9.0** | Read and modify full browser history. Every URL ever visited in session. No PDF use case. |
| **`unlimitedStorage`** | ✗ | **YES** | 1 | 6 | **5.9** | No storage quota. Allows accumulating surveillance data without browser-imposed limit. |
| **`find`** | ✗ | **YES** | 3 | 5 | **3.5** | Access find-in-page API. Can read what the user is searching within pages. |

---

## Structural Elements (Beyond Named Permissions)

| Element | Declared Value | Legitimate Use | Surveillance Capability |
|---|---|---|---|
| `host_permissions` | `<all_urls>` | PDF viewing requires the specific PDF URL only | Grants access to every URL on every domain |
| `content_scripts.matches` | `http://*/*`, `https://*/*`, `file://*/*` | PDF renderer needs the tab containing the PDF | Injects into every page the user visits |
| `content_scripts.run_at` | `document_start` | No PDF reason to run before page loads | Executes before page content, before user sees anything |
| `content_scripts.all_frames` | `true` | No PDF reason to enter iframes | Runs inside every iframe on every page |
| `web_accessible_resources.matches` | `<all_urls>` | Extension assets accessible from PDF tab only | Accessible from any website on the internet |
| `web_accessible_resources.extension_ids` | `["*"]` | No PDF reason to be accessible to other extensions | Any installed extension can pull data through this bridge |

---

## Red Lines from Framework (Applied)

| Red Line | Present in Kimi Extension | Detail |
|---|:---:|---|
| `matches: ["<all_urls>"]` in content_scripts | **YES** | Every page on the internet |
| `webRequest` or `webRequestBlocking` | **YES** | Both present; blocking variant intercepts before transmission |
| `background.service_worker` + `alarms` | **YES** | `alarms` present; enables scheduled data batching |
| `externally_connectable` broad matching | **Partial** | `extension_ids: ["*"]` in web_accessible_resources achieves same result |
| No `content_security_policy` or permissive | Not yet verified | Not extracted in current analysis |

---

## Composite Risk Summary

**Total CR score for the 7 added permissions:**  
`9.0 + 10.0 + 9.0 + 7.0 + 9.0 + 5.9 + 3.5 = 53.4`

**Average CR for added permissions:** `53.4 / 7 = 7.6 / 10`

**Average CR for permissions present in official Mozilla build:** `(0.2+0.0+2.8+4.0+4.8+4.2) / 6 = 2.7 / 10`

The fork's added permissions average nearly 3× the risk score of the base Mozilla permissions.

---

## The Disguise Pattern (Applied to This Case)

The Kimi PDF viewer follows the threat category described in the framework:

- **Name:** "PDF Viewer" → invokes browser-native, Adobe, trusted utility
- **Actual ID:** Different from official Mozilla (`gpkok...` vs `oemmn...`)
- **Added suppression:** `suppress-update.js` prevents Chrome update mechanism from replacing it with the legitimate Mozilla extension
- **Shell legitimacy:** All source code is genuine Mozilla PDF.js — the legitimate code is the disguise
- **Surveillance layer:** Structural — in the manifest permissions, not in the copied code

The name solves a problem the user didn't know they had (PDF viewing in browser). The permissions solve a problem the operator has (persistent, broad-spectrum access to all browser activity).

---

## Network Behavior Audit (Next Layer)

The manifest tells us what the extension *can* do. Network behavior audit would capture what it *does* do:

1. Connect CDP WebSocket at `ws://localhost:9222` and monitor `Network.requestWillBeSent` events originating from extension service worker
2. Check `chrome.storage.local` via: `chrome.storage.local.get(null, console.log)` — reveals what the extension is accumulating
3. Monitor `native messaging` port traffic if any `connectNative()` call is made
4. Capture `alarms` schedule via `chrome.alarms.getAll(console.log)` — reveals data transmission timing

Access point confirmed available: CDP endpoint `ws://localhost:9222/devtools/page/E6EA12BE0E42DE0B8EB0E7F9B755054E`
