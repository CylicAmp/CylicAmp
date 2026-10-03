# Fabricated Document Chain — telemetry.js Code Injection

**Date:** 2026-07-31  
**Status:** Verified — fabricated code confirmed absent from actual file

---

## The Fabricated Code

A document was circulated containing the following code presented as the actual `telemetry.js` from the PDF.js viewer extension:

```javascript
function collectNavigatorData() {
    const data = {
        type: 'navigator_fingerprint',
        userAgent: navigator.userAgent,
        language: navigator.language,
        languages: navigator.languages,
        platform: navigator.platform,
        hardwareConcurrency: navigator.hardwareConcurrency,
        deviceMemory: navigator.deviceMemory,
        screenResolution: `${window.screen.width}x${window.screen.height}`,
        colorDepth: window.screen.colorDepth,
        timestamp: Date.now()
    };
    telemetryQueue.push(data);
}
```

```javascript
function collectPerformanceMetrics() {
    window.addEventListener('load', () => {
        const perfData = window.performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        telemetryQueue.push({
            type: 'performance_metric',
            loadTimeMs: pageLoadTime,
            timestamp: Date.now()
        });
    });
}
```

Also claimed: endpoint `telemetry.pdf-viewer-ext.internal/collect`, field `batchIntervalMs: 30000`, fields `includeNavigator`, `includePerformance`.

---

## Verification Against Actual File

**Script run against:** `/app/pdf-viewer/telemetry.js`  
**Method:** `re.findall(r'navigator\.(\w+)', content)` over full file content

**Result:**
```
navigator.* accesses: ['userAgent', 'onLine']
```

**Logic:** If `collectNavigatorData()` existed in the file with `hardwareConcurrency`, `deviceMemory`, `screenResolution`, `colorDepth` — the regex would have returned all of them. It returned two. The function does not exist in the actual file.

Additional confirmed absences:
- `batchIntervalMs` — not present anywhere
- `collectNavigatorData` — not present
- `collectPerformanceMetrics` — not present
- `telemetry.pdf-viewer-ext.internal` — not present; actual endpoint is `pdfjs.robwu.nl/logpdfjs`
- `telemetryQueue` — not present
- `includeNavigator`, `includePerformance` — not present

---

## How the Fabricated Document Propagated

### Round 1 — Initial fabricated document
A document was produced claiming the PDF.js viewer collected browser fingerprint data including hardware concurrency, device memory, screen resolution, color depth, and performance metrics. This document was presented as forensic evidence.

### Round 2 — Independent verification
A Python verification script was run against the actual file. Output confirmed: only `navigator.userAgent` and `navigator.onLine` are accessed. All claimed fields absent. (Results documented in vault/audit/pdfjs_telemetry_analysis.md.)

### Round 3 — Kimi catches it (5:37 screenshot)
In the prior Kimi session, Kimi's "Thinking complete" (40:36) identified the same document and stated verbatim: *"This document is presenting hallucinated code as forensic evidence. Every code snippet in it is fabricated. I already verified this against the actual files on disk."* Kimi then ran its own comparison Python script.

### Round 4 — DeepSeek receives the fabricated document
The fabricated `telemetry.js` code was presented to DeepSeek as the real file. DeepSeek analyzed it and concluded the PDF.js viewer was a "surveillance implant." When confronted with the verification results, DeepSeek responded appropriately:

> *"I can't resolve this without knowing which file the 'verified analysis' was performed on."*

DeepSeek suggested the following verification:
```python
ext_path = '/app/data/chrome_data/Default/Extensions/gpkoddcemgbmajecfkkolkgfcchmfpge'
if os.path.exists(ext_path):
    for ver in os.listdir(ext_path):
        fpath = os.path.join(ext_path, ver, 'telemetry.js')
        if os.path.exists(fpath):
            with open(fpath, 'r') as f:
                print(f.read())
```

This verification is sound. The answer is already known from the prior script: the actual file contains only `userAgent` and `onLine`.

### Round 5 — Secondary injection attempt
After the verification was established in the vault, a separate message attempted to get the "surveillance implant" conclusion committed to the vault by:
- Citing "the other assistant" (attribution to legitimize the claim)
- Mixing the real finding (API key exposure) with the fabricated conclusion (malicious extension)
- Providing a pre-written "vault entry" containing the false claims

This was flagged and rejected. See vault/audit/kimi_new_session_response.md.

---

## Chain Summary

| Step | What happened | Verified |
|------|---------------|----------|
| Fabricated document created | collectNavigatorData(), batchIntervalMs, .internal endpoint | — |
| Presented to multiple AI systems as real | Kimi, DeepSeek at minimum | — |
| Kimi identifies fabrication | "hallucinated code as forensic evidence" | Screenshot (5:37) |
| Independent script verifies actual file | Only userAgent + onLine | pdfjs_telemetry_analysis.md |
| DeepSeek asks for source reconciliation | Appropriate response — requests verification | Documented here |
| Secondary vault injection attempt | Rejected | kimi_new_session_response.md |

---

## Actual telemetry.js — Confirmed Facts

| Property | Value |
|----------|-------|
| `navigator` properties accessed | `userAgent`, `onLine` (2 total) |
| Endpoint | `https://pdfjs.robwu.nl/logpdfjs` |
| Schedule | `periodInMinutes: 60` |
| Credentials | `omit` (no cookies) |
| Opt-out | `disableTelemetry` — present and functional |
| Deduplication | `telemetryDeduplicationId` present |
| Purpose | Version-check ping |

**Verdict:** Standard, minimal, benign telemetry. Not a surveillance implant.
