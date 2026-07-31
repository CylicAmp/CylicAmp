#!/usr/bin/env python3
"""
vault/audit/http_security_auditor.py

HTTP security header auditor with PASS / WARN / FAIL grading and risk scoring.

Risk weights are aligned with the project auditor scale:
  FAIL on critical header  →  1.0   (≡ HIGH violation)
  FAIL on important header →  0.7   (≡ HIGH session anomaly)
  FAIL on advisory header  →  0.3   (≡ attachment anomaly)
  WARN                     →  ~half the FAIL weight
  Catch-22 (robots+noindex) → 2.0  (instant CRITICAL)

Verdicts follow the same thresholds as ClaudeProjectAuditor:
  CLEAN            risk < 0.5
  REVIEW REQUIRED  0.5 ≤ risk < 2.0
  CRITICAL         risk ≥ 2.0

Usage:
    python http_security_auditor.py https://example.com
    python http_security_auditor.py urls.txt
    python http_security_auditor.py urls.txt --output report.json
"""

import json
import sys
import re
import ssl
import http.client
import argparse
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict
from urllib.parse import urlparse, urljoin


# ── Risk weights ──────────────────────────────────────────────────────────────

WEIGHTS: Dict[str, Dict[str, float]] = {
    # Critical — FAIL = 1.0 (≡ HIGH violation in project auditor)
    "x_robots_tag":           {"FAIL": 1.0, "WARN": 0.3},
    "hsts":                   {"FAIL": 1.0, "WARN": 0.3},
    "x_content_type_options": {"FAIL": 1.0, "WARN": 0.3},
    # Important — FAIL = 0.7 (≡ HIGH session anomaly)
    "csp":                    {"FAIL": 0.7, "WARN": 0.2},
    "cache_control":          {"FAIL": 0.7, "WARN": 0.2},
    # Advisory — FAIL = 0.3 (≡ attachment anomaly)
    "x_frame_options":        {"FAIL": 0.3, "WARN": 0.1},
    "referrer_policy":        {"FAIL": 0.3, "WARN": 0.1},
    # Info only — no score contribution
    "permissions_policy":     {"FAIL": 0.0, "WARN": 0.0},
    # robots.txt
    "robots_catch22":         {"FAIL": 2.0},   # instant CRITICAL
    "robots_disallowed":      {"FAIL": 0.5, "WARN": 0.2},
    "robots_error":           {"WARN": 0.2},
}


# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class CheckResult:
    header: str
    key: str
    grade: str               # PASS | WARN | FAIL | INFO
    value: Optional[str]
    note: str
    weight: float

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class RobotsResult:
    origin: str
    path: str
    http_status: Optional[int]
    matched_rules: List[str]
    grade: str               # PASS | WARN | FAIL | CATCH22
    note: str
    weight: float

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class HeaderAuditReport:
    url: str
    final_url: str
    http_status: Optional[int]
    checks: List[CheckResult]
    robots: RobotsResult
    risk_score: float
    verdict: str             # CLEAN | REVIEW REQUIRED | CRITICAL

    def to_dict(self) -> Dict:
        return asdict(self)

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"[HTTPAudit] Report saved to: {path}")


# ── Auditor ───────────────────────────────────────────────────────────────────

class HTTPSecurityAuditor:

    MAX_REDIRECTS = 10
    TIMEOUT = 10

    # ── Network helpers ───────────────────────────────────────────────────────

    def _fetch_headers(self, url: str):
        """Follow redirects with HEAD requests. Returns (final_url, status, headers)."""
        current = url
        for _ in range(self.MAX_REDIRECTS):
            parsed = urlparse(current)
            try:
                if parsed.scheme == "https":
                    ctx = ssl.create_default_context()
                    conn = http.client.HTTPSConnection(
                        parsed.netloc, timeout=self.TIMEOUT, context=ctx
                    )
                else:
                    conn = http.client.HTTPConnection(
                        parsed.netloc, timeout=self.TIMEOUT
                    )
                path = parsed.path or "/"
                if parsed.query:
                    path += "?" + parsed.query
                conn.request("HEAD", path, headers={"User-Agent": "HTTPSecurityAuditor/1.0"})
                resp = conn.getresponse()
                if resp.status in (301, 302, 303, 307, 308):
                    loc = resp.getheader("Location")
                    if loc:
                        current = urljoin(current, loc)
                        continue
                return current, resp.status, resp.headers
            except Exception:
                return current, None, None
        return current, None, None

    def _fetch_robots(self, origin: str):
        """Fetch robots.txt. Returns (http_status, body_text)."""
        try:
            parsed = urlparse(origin)
            if parsed.scheme == "https":
                ctx = ssl.create_default_context()
                conn = http.client.HTTPSConnection(
                    parsed.netloc, timeout=self.TIMEOUT, context=ctx
                )
            else:
                conn = http.client.HTTPConnection(parsed.netloc, timeout=self.TIMEOUT)
            conn.request("GET", "/robots.txt", headers={"User-Agent": "HTTPSecurityAuditor/1.0"})
            resp = conn.getresponse()
            body = resp.read().decode("utf-8", errors="replace") if resp.status == 200 else ""
            return resp.status, body
        except Exception:
            return None, ""

    def _val(self, raw: str) -> str:
        """Strip 'Header-Name: ' prefix, return value only."""
        return raw.split(":", 1)[1].strip() if raw and ":" in raw else (raw or "").strip()

    # ── Header checks ─────────────────────────────────────────────────────────

    def _check_x_robots_tag(self, headers, is_https: bool) -> CheckResult:
        raw = headers.get("x-robots-tag") if headers else None
        if raw:
            v = self._val(raw).lower()
            if re.search(r"\bnone\b|noindex", v):
                note = "'none' = noindex, nofollow per Google spec" if re.search(r"\bnone\b", v) \
                       else "noindex directive present"
                return CheckResult("X-Robots-Tag", "x_robots_tag", "PASS", raw, note, 0.0)
            return CheckResult("X-Robots-Tag", "x_robots_tag", "WARN", raw,
                               "present but no noindex directive",
                               WEIGHTS["x_robots_tag"]["WARN"])
        return CheckResult("X-Robots-Tag", "x_robots_tag", "FAIL", None, "missing",
                           WEIGHTS["x_robots_tag"]["FAIL"])

    def _check_cache_control(self, headers) -> CheckResult:
        raw = headers.get("cache-control") if headers else None
        if raw:
            v = self._val(raw).lower()
            if "no-store" in v:
                return CheckResult("Cache-Control", "cache_control", "PASS", raw, "no-store", 0.0)
            if re.search(r"private|no-cache", v):
                return CheckResult("Cache-Control", "cache_control", "WARN", raw,
                                   "no-store preferred for sensitive responses",
                                   WEIGHTS["cache_control"]["WARN"])
            if "public" in v:
                return CheckResult("Cache-Control", "cache_control", "FAIL", raw,
                                   "public caching on sensitive endpoint",
                                   WEIGHTS["cache_control"]["FAIL"])
            return CheckResult("Cache-Control", "cache_control", "WARN", raw,
                               "unrecognized directives", WEIGHTS["cache_control"]["WARN"])
        return CheckResult("Cache-Control", "cache_control", "FAIL", None, "missing",
                           WEIGHTS["cache_control"]["FAIL"])

    def _check_hsts(self, headers, is_https: bool) -> CheckResult:
        if not is_https:
            return CheckResult("Strict-Transport-Security", "hsts", "INFO", None,
                               "HTTP — HSTS not applicable", 0.0)
        raw = headers.get("strict-transport-security") if headers else None
        if raw:
            v = self._val(raw)
            m = re.search(r"max-age=(\d+)", v, re.IGNORECASE)
            if m:
                age = int(m.group(1))
                if age >= 31536000:
                    return CheckResult("Strict-Transport-Security", "hsts", "PASS", raw,
                                       f"max-age={age} (≥ 1 year)", 0.0)
                return CheckResult("Strict-Transport-Security", "hsts", "WARN", raw,
                                   f"max-age={age} < 31536000 — recommend 1 year minimum",
                                   WEIGHTS["hsts"]["WARN"])
            return CheckResult("Strict-Transport-Security", "hsts", "WARN", raw,
                               "no max-age found", WEIGHTS["hsts"]["WARN"])
        return CheckResult("Strict-Transport-Security", "hsts", "FAIL", None, "missing",
                           WEIGHTS["hsts"]["FAIL"])

    def _check_x_content_type_options(self, headers) -> CheckResult:
        raw = headers.get("x-content-type-options") if headers else None
        if raw:
            v = self._val(raw).lower()
            if "nosniff" in v:
                return CheckResult("X-Content-Type-Options", "x_content_type_options",
                                   "PASS", raw, "nosniff", 0.0)
            return CheckResult("X-Content-Type-Options", "x_content_type_options",
                               "WARN", raw, "expected nosniff",
                               WEIGHTS["x_content_type_options"]["WARN"])
        return CheckResult("X-Content-Type-Options", "x_content_type_options",
                           "FAIL", None, "missing", WEIGHTS["x_content_type_options"]["FAIL"])

    def _check_x_frame_options(self, headers) -> CheckResult:
        raw = headers.get("x-frame-options") if headers else None
        if raw:
            v = self._val(raw).upper()
            if v in ("DENY", "SAMEORIGIN"):
                return CheckResult("X-Frame-Options", "x_frame_options", "PASS", raw, v, 0.0)
            return CheckResult("X-Frame-Options", "x_frame_options", "WARN", raw,
                               "unexpected value — expected DENY or SAMEORIGIN",
                               WEIGHTS["x_frame_options"]["WARN"])
        return CheckResult("X-Frame-Options", "x_frame_options", "WARN", None,
                           "missing — verify CSP frame-ancestors covers this",
                           WEIGHTS["x_frame_options"]["WARN"])

    def _check_referrer_policy(self, headers) -> CheckResult:
        raw = headers.get("referrer-policy") if headers else None
        if raw:
            v = self._val(raw).lower()
            if re.search(r"no-referrer\b|strict-origin", v):
                return CheckResult("Referrer-Policy", "referrer_policy", "PASS", raw,
                                   "strong policy", 0.0)
            return CheckResult("Referrer-Policy", "referrer_policy", "WARN", raw,
                               "consider strict-origin-when-cross-origin or no-referrer",
                               WEIGHTS["referrer_policy"]["WARN"])
        return CheckResult("Referrer-Policy", "referrer_policy", "WARN", None, "missing",
                           WEIGHTS["referrer_policy"]["WARN"])

    def _check_csp(self, headers) -> CheckResult:
        raw = headers.get("content-security-policy") if headers else None
        if raw:
            return CheckResult("Content-Security-Policy", "csp", "PASS",
                               self._val(raw), "present", 0.0)
        return CheckResult("Content-Security-Policy", "csp", "FAIL", None, "missing",
                           WEIGHTS["csp"]["FAIL"])

    def _check_permissions_policy(self, headers) -> CheckResult:
        raw = headers.get("permissions-policy") if headers else None
        v = (self._val(raw) or "")[:100] if raw else None
        return CheckResult("Permissions-Policy", "permissions_policy", "INFO", v,
                           v or "missing — not graded; site-specific", 0.0)

    # ── robots.txt check ──────────────────────────────────────────────────────

    def _check_robots_txt(self, origin: str, path: str, noindex_present: bool) -> RobotsResult:
        status, body = self._fetch_robots(origin)

        if status != 200:
            return RobotsResult(
                origin=origin, path=path, http_status=status,
                matched_rules=[], grade="WARN",
                note=f"robots.txt HTTP {status} — cannot verify path rules",
                weight=WEIGHTS["robots_error"]["WARN"],
            )

        matched = []
        for line in body.splitlines():
            line = line.strip()
            if not line.lower().startswith("disallow:"):
                continue
            rule_path = line.split(":", 1)[1].strip().rstrip("*")
            if rule_path and path.startswith(rule_path):
                matched.append(line)

        if not matched:
            return RobotsResult(
                origin=origin, path=path, http_status=status,
                matched_rules=[], grade="PASS",
                note="path not disallowed — crawlers can reach noindex signal",
                weight=0.0,
            )

        if noindex_present:
            return RobotsResult(
                origin=origin, path=path, http_status=status,
                matched_rules=matched, grade="CATCH22",
                note=(
                    "Catch-22: path disallowed in robots.txt AND noindex signal present. "
                    "Crawlers are locked out before they can read the noindex directive — "
                    "already-indexed pages cannot be de-indexed by Googlebot."
                ),
                weight=WEIGHTS["robots_catch22"]["FAIL"],
            )

        return RobotsResult(
            origin=origin, path=path, http_status=status,
            matched_rules=matched, grade="FAIL",
            note="path disallowed — crawlers cannot reach any noindex signal",
            weight=WEIGHTS["robots_disallowed"]["FAIL"],
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def audit_url(self, url: str) -> HeaderAuditReport:
        print(f"[HTTPAudit] Auditing: {url}")
        parsed = urlparse(url)
        is_https = parsed.scheme == "https"

        final_url, status, headers = self._fetch_headers(url)

        checks = [
            self._check_x_robots_tag(headers, is_https),
            self._check_cache_control(headers),
            self._check_hsts(headers, is_https),
            self._check_x_content_type_options(headers),
            self._check_x_frame_options(headers),
            self._check_referrer_policy(headers),
            self._check_csp(headers),
            self._check_permissions_policy(headers),
        ]

        noindex_present = any(
            c.key == "x_robots_tag" and c.grade == "PASS" for c in checks
        )

        origin = f"{parsed.scheme}://{parsed.netloc}"
        path = parsed.path or "/"
        robots = self._check_robots_txt(origin, path, noindex_present)

        risk_score = round(sum(c.weight for c in checks) + robots.weight, 4)
        verdict = (
            "CLEAN"           if risk_score < 0.5 else
            "REVIEW REQUIRED" if risk_score < 2.0 else
            "CRITICAL"
        )

        print(f"[HTTPAudit] {verdict}  risk={risk_score:.2f}  {url}")
        return HeaderAuditReport(
            url=url, final_url=final_url, http_status=status,
            checks=checks, robots=robots,
            risk_score=risk_score, verdict=verdict,
        )

    def audit_file(self, url_list_path: str) -> List[HeaderAuditReport]:
        """Audit every URL in a line-delimited file (skips blanks and # comments)."""
        reports = []
        with open(url_list_path) as f:
            for line in f:
                url = line.strip()
                if not url or url.startswith("#"):
                    continue
                reports.append(self.audit_url(url))
        return reports


# ── Terminal output ───────────────────────────────────────────────────────────

_GRADE_SYM = {"PASS": "✓", "WARN": "!", "FAIL": "✗", "INFO": "i", "CATCH22": "⚠"}


def print_report(report: HeaderAuditReport):
    print(f"\n=== {report.url} ===")
    if report.http_status:
        print(f"  HTTP {report.http_status}  →  {report.final_url}")
    for c in report.checks:
        sym = _GRADE_SYM.get(c.grade, "?")
        val = f"  [{c.value}]" if c.value and c.grade != "PASS" else ""
        print(f"  [{sym}] {c.header}{val}")
        if c.note and c.grade not in ("PASS", "INFO"):
            print(f"       {c.note}")
    r = report.robots
    sym = _GRADE_SYM.get(r.grade, "?")
    print(f"  [{sym}] robots.txt ({r.grade}): {r.note}")
    for rule in r.matched_rules:
        print(f"       {rule}  ←  matches {r.path}")
    print(f"\n  risk_score={report.risk_score:.4f}  verdict={report.verdict}\n")


def print_summary(reports: List[HeaderAuditReport]):
    if len(reports) <= 1:
        return
    print("=" * 72)
    print(f"  {'URL':<50}  {'RISK':>6}  VERDICT")
    print(f"  {'-'*50}  {'------':>6}  -------")
    for r in reports:
        print(f"  {r.url[:50]:<50}  {r.risk_score:>6.2f}  {r.verdict}")
    print()


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="HTTP security header auditor — PASS/WARN/FAIL with risk scoring"
    )
    parser.add_argument(
        "target",
        help="Single URL (https://...) or path to file containing one URL per line",
    )
    parser.add_argument(
        "--output", "-o", metavar="FILE",
        help="Write JSON report to FILE",
    )
    args = parser.parse_args()

    auditor = HTTPSecurityAuditor()

    if args.target.startswith("http://") or args.target.startswith("https://"):
        reports = [auditor.audit_url(args.target)]
    else:
        reports = auditor.audit_file(args.target)

    for r in reports:
        print_report(r)
    print_summary(reports)

    if args.output:
        payload = [r.to_dict() for r in reports] if len(reports) > 1 else reports[0].to_dict()
        with open(args.output, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"[HTTPAudit] Report written to {args.output}")


if __name__ == "__main__":
    main()
