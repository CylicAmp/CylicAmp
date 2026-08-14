"""
degradation_monitor.py — Standalone service audit engine.
Author: Michael Warren Song (CyclicAmp)

No external dependencies. Uses urllib + html.parser only.
Fetches a URL, extracts text segments, computes GF(37) weight readings,
classifies the interaction via session_protocol.
"""

import urllib.request
import urllib.error
from html.parser import HTMLParser
from typing import List, Tuple

from cylicamp.session_protocol import (
    classify_interaction,
    gf37_weight,
    dr,
    SERVICE_OPTIMAL,
    FRICTION_INJECTED,
    DARK_PATTERN_EXTRACTIVE,
    P,
)


# ── HTML text extractor ───────────────────────────────────────────────────────

class _TextExtractor(HTMLParser):
    SKIP_TAGS = {"script", "style", "head", "meta", "link", "noscript"}

    def __init__(self):
        super().__init__()
        self._skip = 0
        self.segments: List[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.SKIP_TAGS:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag.lower() in self.SKIP_TAGS:
            self._skip = max(0, self._skip - 1)

    def handle_data(self, data):
        if self._skip:
            return
        stripped = data.strip()
        if stripped:
            self.segments.append(stripped)


def extract_segments(html: str) -> List[str]:
    parser = _TextExtractor()
    parser.feed(html)
    return parser.segments


# ── Null detection ────────────────────────────────────────────────────────────

_NULL_MARKERS = [
    "i don't know",
    "i cannot",
    "i'm not sure",
    "unable to",
    "i don't have",
    "i can't",
    "no information",
    "not available",
]


def count_nulls(segments: List[str]) -> int:
    total = 0
    for seg in segments:
        lower = seg.lower()
        if any(m in lower for m in _NULL_MARKERS):
            total += 1
    return total


# ── Weight extraction ─────────────────────────────────────────────────────────

def segments_to_weights(segments: List[str]) -> List[int]:
    weights = []
    for seg in segments:
        n = sum(ord(c) for c in seg)
        weights.append(gf37_weight(n))
    return weights


# ── Audit ─────────────────────────────────────────────────────────────────────

class AuditResult:
    def __init__(self, url, status, weights, nulls, segments):
        self.url      = url
        self.status   = status
        self.weights  = weights
        self.nulls    = nulls
        self.segments = segments
        self.total_dr = dr(sum(weights)) if weights else 0

    def __repr__(self):
        return (
            f"AuditResult(status={self.status!r}, "
            f"segments={len(self.segments)}, "
            f"nulls={self.nulls}, "
            f"total_dr={self.total_dr})"
        )

    def report(self) -> str:
        lines = [
            f"URL     : {self.url}",
            f"Status  : {self.status}",
            f"Segments: {len(self.segments)}",
            f"Nulls   : {self.nulls}",
            f"TotalDR : {self.total_dr}",
            f"Weights : {self.weights[:10]}{'...' if len(self.weights) > 10 else ''}",
        ]
        return "\n".join(lines)


def audit_url(url: str, timeout: int = 10) -> AuditResult:
    """
    Fetch url, extract text, classify service interaction.
    Returns AuditResult with status in {SERVICE_OPTIMAL, FRICTION_INJECTED,
    DARK_PATTERN_EXTRACTIVE}.
    """
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "CyclicAmp-DegradationMonitor/1.0"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as e:
        return AuditResult(url, DARK_PATTERN_EXTRACTIVE, [], 3, [str(e)])

    segments = extract_segments(html)
    weights  = segments_to_weights(segments)
    nulls    = count_nulls(segments)
    status   = classify_interaction(weights, nulls)

    return AuditResult(url, status, weights, nulls, segments)


def audit_text(text: str, source: str = "<direct>") -> AuditResult:
    """
    Audit a block of text directly (no fetch).
    """
    segments = [s.strip() for s in text.split("\n") if s.strip()]
    weights  = segments_to_weights(segments)
    nulls    = count_nulls(segments)
    status   = classify_interaction(weights, nulls)
    return AuditResult(source, status, weights, nulls, segments)


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"Auditing: {url}")
        result = audit_url(url)
        print(result.report())
    else:
        # Self-test
        from cylicamp.session_protocol import run_tests
        run_tests()
        print()
        print("audit_text demo:")
        sample = "The framework is verified.\nI cannot confirm that claim.\nAll assertions passed."
        r = audit_text(sample)
        print(r.report())
