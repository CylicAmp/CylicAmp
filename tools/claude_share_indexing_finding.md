# Claude Shared Chat Indexing — Privacy Finding

**Date:** 2026-07-31  
**Investigated by:** CylicAmp audit session  

## Finding

Claude shared chat URLs (`claude.ai/share/*`) are not protected from search engine indexing.

## Evidence

### robots.txt audit (`https://claude.ai/robots.txt`)

The following paths are explicitly disallowed:
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

### HTTP header audit (`curl -sI https://claude.ai/share/test`)

```
x-robots-tag: none
cache-control: private, no-store
```

`x-robots-tag: none` means no indexing directive is explicitly set.  
Without a `noindex` directive, search engines treat shared URLs as indexable.

## Impact

Any conversation shared via `claude.ai/share` is potentially:
- Indexed by Google and other search engines
- Cached and stored by web crawlers
- Discoverable via site-specific search dorks (`site:claude.ai/share`)

This affects user privacy. Conversations shared with a link (intended for a specific recipient) become publicly searchable without the user's knowledge.

## Same Issue: DeepSeek

The Reddit post that surfaced this finding also reported `site:chat.deepseek.com/share` returns indexed results — the same missing `noindex` pattern.

## What Should Exist

In `robots.txt`:
```
Disallow: /share/*
```

Or on every share response header:
```
X-Robots-Tag: noindex, nofollow
```

## Source

User-reported finding, verified independently via HTTP header and robots.txt inspection.  
Original report surfaced on Reddit, 2026-07-30.
