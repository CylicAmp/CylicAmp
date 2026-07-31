# Claude Shared Chat Indexing — Privacy Finding (CORRECTED)

**Date:** 2026-07-31  
**Investigated by:** CylicAmp audit session  
**Correction issued:** 2026-07-31  

## Corrected Finding

Claude shared chat URLs (`claude.ai/share/*`) **are** protected from search engine indexing via the `X-Robots-Tag` response header. The original finding was incorrect on this point.

## Evidence

### HTTP header audit (`curl -sI https://claude.ai/share/test`)

```
x-robots-tag: none
cache-control: private, no-store
```

**Correction:** `X-Robots-Tag: none` is a recognized Google directive equivalent to `noindex, nofollow`. It explicitly instructs search engines not to index the page and not to follow its links. Share URLs are protected.

Reference: [Google Robots meta tag specification](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag) — `none` is synonymous with `noindex, nofollow`.

### robots.txt audit (`https://claude.ai/robots.txt`)

The following paths are explicitly disallowed for crawlers:
- `/new?*`
- `/chat/*`
- `/join/*`
- `/magic-link*`
- `/api/*`
- `/onboarding*`
- `/upgrade*`
- `/lti/*`
- `/settings*`
- `/task*`

**`/share/*` is absent from the disallow list.**

This is a minor gap: robots.txt controls whether compliant crawlers fetch the page at all. Since the response header already carries `X-Robots-Tag: none`, crawlers that do fetch a share URL receive the noindex directive and must not index it regardless. Adding `Disallow: /share/*` to robots.txt would prevent the fetch entirely and is a defense-in-depth improvement, but the current state is not an indexing vulnerability.

## Status

- **Indexing protection:** Present (`X-Robots-Tag: none` = `noindex, nofollow`)
- **Crawl prevention (robots.txt):** Absent for `/share/*` — minor gap, not critical
- **Cache-Control:** `private, no-store` — correct, no caching

## Re: The Reddit Report

The Reddit post reporting `site:claude.ai/share` returning results may reflect:
1. A prior state before the `X-Robots-Tag: none` header was deployed
2. Pages indexed before the header was present (Google de-indexes these over time)
3. Misinterpretation of `X-Robots-Tag: none` as "no directive set"

The current header state is protective. The finding as originally stated was wrong.

## What Would Further Harden This

In `robots.txt` (defense-in-depth, not strictly required):
```
Disallow: /share/*
```

This prevents compliant crawlers from fetching share URLs at all, which is cleaner than relying on the response header alone.

## Source

User-reported finding, verified independently via HTTP header and robots.txt inspection.  
Original report surfaced on Reddit, 2026-07-30.  
Corrected after re-reading Google's `X-Robots-Tag: none` specification.
