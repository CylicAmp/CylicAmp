# PDF.js Viewer Telemetry — Verified Analysis

**Extension:** PDF Viewer (pdfjs-telemetry by Rob--W)  
**Source:** `/app/pdf-viewer/telemetry.js`, `/app/pdf-viewer/manifest.json`  
**Method:** Static code analysis + runtime property extraction  
**Date:** 2026-07-31  

---

## What the Code Actually Does

### Data Collected

| Property | Source | Value |
|----------|--------|-------|
| `navigator.userAgent` | telemetry.js | Browser version string |
| `navigator.onLine` | telemetry.js | Boolean — device online status |
| `telemetryDeduplicationId` | telemetry.js | Persistent ID to prevent double-counting |
| `telemetryLastVersion` | telemetry.js | Last recorded extension version |

**Total: 4 fields. Two from the browser, two from local storage.**

### Transmission

- **Endpoint:** `https://pdfjs.robwu.nl/logpdfjs`
- **Method:** POST
- **Schedule:** `periodInMinutes: 60` via `chrome.alarms` (not an active polling loop)
- **Credentials:** `omit` — no cookies, no session tokens sent
- **CORS mode:** `cors`
- **Opt-out:** `disableTelemetry` flag — present and functional

### Purpose

This is a version-check ping. It tells the extension author how many installs are active and what browser version they're running on. It is not analytics, behavioral tracking, or fingerprinting.

---

## What the Code Does NOT Do

The following were claimed in a prior document and are **not present in the code**:

| Claimed | Verified |
|---------|----------|
| `navigator.hardwareConcurrency` | Not accessed |
| `navigator.deviceMemory` | Not accessed |
| `screen.width` / `screen.height` | Not accessed |
| `screen.colorDepth` | Not accessed |
| `performance` metrics | Not accessed |
| `batchIntervalMs` | Not present anywhere |
| Internal placeholder URIs | Not present — endpoint is hardcoded |

---

## Permissions Analysis

| Permission | Claimed concern | Reality |
|------------|-----------------|---------|
| `<all_urls>` (host) | "Exceeds minimal requirements" | Required — PDF viewer must intercept PDF links across all sites |
| `alarms` | Flagged | Used for scheduled telemetry ping only |
| `declarativeNetRequestWithHostAccess` | Flagged | Required for referrer rewriting when loading PDFs |
| `webRequest` | Flagged | Required for PDF interception |
| `tabs` | Flagged | Required for tab URL routing |
| `webNavigation` | Flagged | Required for navigation error handling |
| `storage` | Flagged | Required for settings and deduplication ID |

All six permissions have direct functional justification for a PDF viewer. None are anomalous.

---

## Prior Document Errors

The document this corrects made the following errors:

1. **Inflated data collection** — Listed 6 browser properties as collected; only 2 are accessed (`userAgent`, `onLine`).
2. **False field names** — Referenced `batchIntervalMs`; this field does not exist. Actual field is `periodInMinutes: 60`.
3. **Phantom URIs** — Claimed "internal placeholder URIs"; no placeholders exist. The endpoint is a single hardcoded production URL.
4. **Misleading framing of permissions** — Presented `<all_urls>` as a surveillance capability without acknowledging it is architecturally required for PDF interception.
5. **Omitted opt-out** — Did not disclose that `disableTelemetry` is present and functional.

---

## Verdict

**The PDF.js viewer sends a minimal version-check ping once per hour.** It collects browser version and online status. It has an opt-out. The permissions are functionally justified. There is no evidence of fingerprinting, behavioral tracking, or data collection beyond what is visible in the code.

Static analysis of the actual files does not support the surveillance framing in the prior document.

---

## Verification Checklist

- [ ] `navigator.userAgent` — only navigator property confirmed in code  
- [ ] `navigator.onLine` — only other navigator property confirmed  
- [ ] `hardwareConcurrency`, `deviceMemory`, `colorDepth`, `screen` — confirmed absent  
- [ ] `batchIntervalMs` — confirmed absent; actual field is `periodInMinutes: 60`  
- [ ] Endpoint is `pdfjs.robwu.nl` — hardcoded, no placeholders  
- [ ] `credentials: "omit"` — confirmed, no cookies transmitted  
- [ ] `disableTelemetry` opt-out — confirmed present  
- [ ] `Deduplication-Id` — confirmed present  
- [ ] All 6 permissions have documented functional justification  
- [ ] `<all_urls>` required for PDF interception across all sites — confirmed  
