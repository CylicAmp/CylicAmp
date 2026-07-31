#!/usr/bin/env python3
"""
vault/audit/platform_restriction_detector.py

Detects platform restriction dark patterns in HTTP responses and text content.

Dark pattern taxonomy (maps to 20-category framework):
  SERVICE_RESTRICTION    Access blocked post-payment / without clear reason
  BLACK_BOX              Opaque status — no queue position, ETA, or reason code
  ADMINISTRATIVE_EXHAUSTION  Repetitive blocking with no resolution path
  GASLIGHT               Platform claims normal operation during active restriction
  FRAUD                  Payment processed, service withheld

Works on:
  - HTTP endpoints (fetches response body + headers)
  - Raw text (support chat, emails, error messages, API responses)

Usage:
    from vault.audit.platform_restriction_detector import PlatformRestrictionDetector
    d = PlatformRestrictionDetector()

    # Analyze a URL
    report = d.detect_url("https://api.example.com/resource")

    # Analyze raw text
    report = d.detect_text("Your account has been restricted.", source="support_email")

    # CLI
    python platform_restriction_detector.py https://api.example.com
    python platform_restriction_detector.py --text "Your payment was processed..."
    python platform_restriction_detector.py urls.txt --batch
"""

import re
import sys
import json
import ssl
import hashlib
import argparse
import http.client
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Tuple
from urllib.parse import urlparse


# ── Pattern definitions ───────────────────────────────────────────────────────

PATTERNS: Dict[str, Dict] = {
    "SERVICE_RESTRICTION": {
        "severity": "HIGH",
        "weight": 1.0,
        "http_codes": [402, 403],
        "patterns": [
            r"(account|access|service).{0,20}(restricted|suspended|limited|blocked|disabled)",
            r"you (have|do not have|don't have) (access|permission)",
            r"(subscription|plan).{0,20}(required|needed) to (access|use|continue)",
            r"(feature|content|resource) is (not available|unavailable) (for|to) (your|this) (plan|tier|account)",
            r"(upgrade|downgrade).{0,20}(to|for) (access|unlock)",
        ],
    },
    "BLACK_BOX": {
        "severity": "HIGH",
        "weight": 1.0,
        "http_codes": [429, 503],
        "transparency_headers": [          # absence on 429/503 = BLACK_BOX signal
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Reset",
            "Retry-After",
        ],
        "patterns": [
            r"(high (demand|volume|traffic|load))",
            r"system(s)?.{0,10}(busy|experiencing|unavailable|degraded)",
            r"we('re| are).{0,20}(unable|currently).{0,20}(serve|provide|process)",
            r"please (check back|try again) later",
            r"(no (queue|position|wait|eta|estimate) (information|available|provided))",
            r"(temporarily|currently) (unavailable|offline|restricted)",
        ],
    },
    "ADMINISTRATIVE_EXHAUSTION": {
        "severity": "MEDIUM",
        "weight": 0.7,
        "http_codes": [],
        "patterns": [
            r"please (contact|reach out to|submit a) (support|us|a ticket|our team)",
            r"our (team|support|agents?) (will|is|are).{0,20}(review|look|investigate|get back)",
            r"no (further|additional) (action|steps|recourse|options) (available|possible|at this time)",
            r"we (cannot|can't) (provide|give|share) (more|additional|further) (information|details|reason)",
            r"(this (decision|restriction|suspension) is (final|not appealable|cannot be reversed))",
        ],
    },
    "GASLIGHT": {
        "severity": "HIGH",
        "weight": 1.0,
        "http_codes": [200],               # 200 during active restriction = signal
        "patterns": [
            r"(account|service|access|subscription) is (fully|completely)?.{0,10}(active|working|operational|normal|fine)",
            r"we (are not|aren't|do not|don't) (see|detect|experience|show) any (issue|problem|error|anomaly)",
            r"everything (is|appears|looks|seems).{0,10}(fine|normal|correct|working) on our end",
            r"that (shouldn't|should not|can't|cannot) (be happening|happen|occur)",
            r"no (reports|complaints|issues|problems) (from|about|regarding) (other|any) (users|accounts|customers)",
            r"(service (is|remains) (fully )?operational)",
        ],
    },
    "FRAUD": {
        "severity": "CRITICAL",
        "weight": 2.0,
        "http_codes": [],
        "patterns": [
            r"payment.{0,30}(processed|completed|successful|confirmed).{0,100}(restricted|suspended|limited|blocked)",
            r"charged.{0,20}(for|without).{0,20}(access|service|delivery)",
            r"refund.{0,20}(policy|request).{0,20}(does not|doesn't|cannot|can't).{0,20}(apply|cover|process)",
            r"no refund.{0,20}(after|once|when).{0,20}(purchase|payment|subscription)",
            r"billing (continues|will continue).{0,20}(despite|during|while).{0,20}(restriction|suspension|limitation)",
        ],
    },
}

# Verdict thresholds (same scale as project auditor)
VERDICT_THRESHOLDS = {
    "CLEAN":          (0.0, 0.5),
    "REVIEW REQUIRED": (0.5, 2.0),
    "CRITICAL":       (2.0, float("inf")),
}


# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class PatternMatch:
    category: str
    severity: str
    pattern: str
    evidence: str    # matched text excerpt
    weight: float


@dataclass
class TransparencyGap:
    description: str
    http_code: int
    missing_headers: List[str]


@dataclass
class RestrictionReport:
    source: str                      # URL or text label
    source_type: str                 # "url" | "text"
    http_status: Optional[int]
    matches: List[PatternMatch]
    transparency_gaps: List[TransparencyGap]
    categories_triggered: List[str]
    risk_score: float
    verdict: str
    fingerprint: str

    def to_dict(self) -> Dict:
        return asdict(self)

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)


# ── Detector ──────────────────────────────────────────────────────────────────

class PlatformRestrictionDetector:

    TIMEOUT = 10
    UA = "VAULT-Audit/1.0"

    def _scan_text(self, text: str) -> Tuple[List[PatternMatch], float]:
        """Run all pattern categories against text. Returns (matches, risk_score)."""
        matches = []
        risk = 0.0
        for category, cfg in PATTERNS.items():
            for pat in cfg["patterns"]:
                m = re.search(pat, text, re.IGNORECASE)
                if m:
                    excerpt = text[max(0, m.start() - 30): m.end() + 30].strip()
                    matches.append(PatternMatch(
                        category=category,
                        severity=cfg["severity"],
                        pattern=pat,
                        evidence=excerpt[:200],
                        weight=cfg["weight"],
                    ))
                    risk += cfg["weight"]
                    break  # one match per category per text scan
        return matches, risk

    def _check_transparency(self, status: int, headers) -> List[TransparencyGap]:
        """Check for missing transparency headers on rate-limit / unavailable responses."""
        gaps = []
        for category, cfg in PATTERNS.items():
            if status not in cfg.get("http_codes", []):
                continue
            required = cfg.get("transparency_headers", [])
            if not required:
                continue
            missing = [h for h in required if not (headers and headers.get(h.lower()))]
            if missing:
                gaps.append(TransparencyGap(
                    description=f"HTTP {status} with no rate-limit transparency headers ({category})",
                    http_code=status,
                    missing_headers=missing,
                ))
        return gaps

    def _fetch(self, url: str) -> Tuple[Optional[int], Optional[object], str]:
        """GET request. Returns (status, headers, body_text)."""
        parsed = urlparse(url)
        try:
            if parsed.scheme == "https":
                ctx = ssl.create_default_context()
                conn = http.client.HTTPSConnection(parsed.netloc, timeout=self.TIMEOUT, context=ctx)
            else:
                conn = http.client.HTTPConnection(parsed.netloc, timeout=self.TIMEOUT)
            path = (parsed.path or "/") + (("?" + parsed.query) if parsed.query else "")
            conn.request("GET", path, headers={"User-Agent": self.UA})
            resp = conn.getresponse()
            body = resp.read(8192).decode("utf-8", errors="replace")
            return resp.status, resp.headers, body
        except Exception:
            return None, None, ""

    def _verdict(self, risk: float) -> str:
        for name, (lo, hi) in VERDICT_THRESHOLDS.items():
            if lo <= risk < hi:
                return name
        return "CRITICAL"

    def _fingerprint(self, source: str, risk: float) -> str:
        return hashlib.sha256(
            (source + str(round(risk, 2))).encode()
        ).hexdigest()[:16]

    # ── Public API ────────────────────────────────────────────────────────────

    def detect_url(self, url: str) -> RestrictionReport:
        """Fetch URL and analyze response body + status for restriction patterns."""
        print(f"[Restrict] Analyzing: {url}")
        status, headers, body = self._fetch(url)

        text_matches, text_risk = self._scan_text(body) if body else ([], 0.0)

        # Additional weight if HTTP status code is a restriction signal
        http_risk = 0.0
        for cfg in PATTERNS.values():
            if status in cfg.get("http_codes", []):
                http_risk += cfg["weight"] * 0.5   # half-weight for code alone

        transparency_gaps = self._check_transparency(status, headers)
        transparency_risk = len(transparency_gaps) * 0.5

        risk = round(text_risk + http_risk + transparency_risk, 4)
        categories = list({m.category for m in text_matches})
        verdict = self._verdict(risk)
        print(f"[Restrict] {verdict}  risk={risk:.2f}  categories={categories or ['none']}")

        return RestrictionReport(
            source=url,
            source_type="url",
            http_status=status,
            matches=text_matches,
            transparency_gaps=transparency_gaps,
            categories_triggered=categories,
            risk_score=risk,
            verdict=verdict,
            fingerprint=self._fingerprint(url, risk),
        )

    def detect_text(self, text: str, source: str = "raw_text") -> RestrictionReport:
        """Analyze raw text content for restriction patterns."""
        print(f"[Restrict] Analyzing text: {source!r} ({len(text)} chars)")
        matches, risk = self._scan_text(text)
        risk = round(risk, 4)
        categories = list({m.category for m in matches})
        verdict = self._verdict(risk)
        print(f"[Restrict] {verdict}  risk={risk:.2f}  categories={categories or ['none']}")

        return RestrictionReport(
            source=source,
            source_type="text",
            http_status=None,
            matches=matches,
            transparency_gaps=[],
            categories_triggered=categories,
            risk_score=risk,
            verdict=verdict,
            fingerprint=self._fingerprint(source + text[:64], risk),
        )

    def detect_batch(self, urls: List[str]) -> List[RestrictionReport]:
        return [self.detect_url(url) for url in urls]


# ── Terminal output ───────────────────────────────────────────────────────────

_SEV_COLOR = {"CRITICAL": "\033[91m", "HIGH": "\033[91m",
              "MEDIUM": "\033[93m", "LOW": "\033[94m"}
_VERDICT_COLOR = {"CLEAN": "\033[92m", "REVIEW REQUIRED": "\033[93m", "CRITICAL": "\033[91m"}
_RST = "\033[0m"


def _c(text: str, code: str, no_color: bool) -> str:
    return text if no_color or not sys.stdout.isatty() else code + text + _RST


def print_report(report: RestrictionReport, no_color: bool = False):
    print("\n" + "=" * 64)
    print(f"Source:  {report.source}")
    print(f"Type:    {report.source_type}" +
          (f"  HTTP {report.http_status}" if report.http_status else ""))
    vcol = _VERDICT_COLOR.get(report.verdict, "")
    print(f"Verdict: {_c(report.verdict, vcol, no_color)}  risk={report.risk_score:.4f}")

    if report.matches:
        print("\nMatched patterns:")
        for m in report.matches:
            scol = _SEV_COLOR.get(m.severity, "")
            print(f"  [{_c(m.severity, scol, no_color)}] {m.category}")
            print(f"    Evidence: \"{m.evidence}\"")
    else:
        print("\n  No restriction patterns detected.")

    if report.transparency_gaps:
        print("\nTransparency gaps:")
        for g in report.transparency_gaps:
            print(f"  HTTP {g.http_code} — missing: {', '.join(g.missing_headers)}")
            print(f"  {g.description}")

    if report.categories_triggered:
        print(f"\nCategories: {', '.join(report.categories_triggered)}")
    print()


def print_summary(reports: List[RestrictionReport], no_color: bool = False):
    if len(reports) <= 1:
        return
    c = lambda t, col: _c(t, col, no_color)
    all_cats = sorted({cat for r in reports for cat in r.categories_triggered})
    print("=" * 72)
    print("BATCH SUMMARY  (%d sources)" % len(reports))
    print("=" * 72)
    print("%-42s  %6s  %-16s  %s" % ("Source", "Risk", "Verdict", "Categories"))
    print("-" * 72)
    for r in reports:
        vcol = _VERDICT_COLOR.get(r.verdict, "")
        cats = ", ".join(r.categories_triggered) if r.categories_triggered else "—"
        print("%-42s  %6.2f  %-16s  %s" % (
            r.source[:40], r.risk_score,
            c(r.verdict, vcol), cats,
        ))
    print("-" * 72)
    avg_risk = sum(r.risk_score for r in reports) / len(reports)
    critical = sum(1 for r in reports if r.verdict == "CRITICAL")
    review   = sum(1 for r in reports if r.verdict == "REVIEW REQUIRED")
    clean    = sum(1 for r in reports if r.verdict == "CLEAN")
    print("Avg risk: %.2f  |  %s  %s  %s" % (
        avg_risk,
        c("%d CRITICAL" % critical, _VERDICT_COLOR["CRITICAL"]),
        c("%d REVIEW"   % review,   _VERDICT_COLOR["REVIEW REQUIRED"]),
        c("%d CLEAN"    % clean,    _VERDICT_COLOR["CLEAN"]),
    ))
    if all_cats:
        print("All categories seen: %s" % ", ".join(all_cats))
    print()


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Detect platform restriction dark patterns in HTTP responses or text"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("urls", nargs="*", default=None,
                       help="URLs to analyze (or single file path with --batch)")
    group.add_argument("--text", "-t", metavar="TEXT",
                       help="Analyze raw text string directly")
    parser.add_argument("--batch", "-b", action="store_true",
                        help="Read URLs from file (one per line)")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors")
    parser.add_argument("--output", "-o", metavar="FILE", help="Write JSON report to FILE")
    args = parser.parse_args()

    no_color = args.no_color or not sys.stdout.isatty()
    detector = PlatformRestrictionDetector()
    reports = []

    if args.text:
        reports.append(detector.detect_text(args.text, source="cli_input"))
    elif args.batch and args.urls and len(args.urls) == 1:
        with open(args.urls[0]) as f:
            urls = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        reports = detector.detect_batch(urls)
    elif args.urls:
        reports = detector.detect_batch(args.urls)

    for r in reports:
        print_report(r, no_color)
    print_summary(reports, no_color)

    if args.output:
        with open(args.output, "w") as f:
            json.dump([r.to_dict() for r in reports], f, indent=2)
        print(f"[Saved] {args.output}")


if __name__ == "__main__":
    main()
