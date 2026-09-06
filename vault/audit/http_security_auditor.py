#!/usr/bin/env python3
"""
HTTP Security Header Auditor
============================
Grades HTTP response headers against security best practices.
Maps to 20-category framework: BLACK_BOX detection via header transparency.

Usage:
    from vault.audit.http_security_auditor import HTTPHeaderAuditor
    auditor = HTTPHeaderAuditor()
    report = auditor.audit_url("https://example.com")
    print(report.score, report.verdict)

Or CLI:
    python http_security_auditor.py https://example.com https://api.example.com
    python http_security_auditor.py urls.txt --batch
    python http_security_auditor.py https://example.com --no-color
"""

import sys
import hashlib
import argparse
import json
import urllib.request
import urllib.error
from typing import Dict, List, Optional
from dataclasses import dataclass


def _parse_max_age(value: str) -> int:
    """Extract max-age from Strict-Transport-Security header."""
    try:
        for part in value.split(";"):
            part = part.strip()
            if part.lower().startswith("max-age="):
                return int(part.split("=", 1)[1])
    except (ValueError, IndexError):
        pass
    return 0


@dataclass
class HeaderGrade:
    name: str
    present: bool
    value: str
    status: str   # PASS | WARN | FAIL | INFO
    score: int    # penalty: 0 (pass), 3 (warn), 5 (fail)
    detail: str


@dataclass
class URLReport:
    url: str
    status_code: int
    grades: List[HeaderGrade]
    total_score: int
    max_possible: int
    verdict: str          # EXCELLENT | GOOD | FAIR | POOR | CRITICAL
    missing_headers: List[str]
    fingerprint: str

    def to_dict(self) -> Dict:
        return {
            "url": self.url,
            "status_code": self.status_code,
            "score": self.total_score,
            "max": self.max_possible,
            "verdict": self.verdict,
            "missing": self.missing_headers,
            "fingerprint": self.fingerprint,
            "grades": [
                {"name": g.name, "status": g.status, "value": g.value, "detail": g.detail}
                for g in self.grades
            ],
        }


class HTTPHeaderAuditor:
    """Audits 8 security headers with graded analysis. Lower score = better."""

    HEADERS = {
        "X-Robots-Tag": {
            "check": lambda v: "noindex" in v.lower() or "none" in v.lower(),
            "pass_msg": "Contains noindex or none",
            "fail_msg": "Missing noindex/none directive",
            "score": 5,
        },
        "Cache-Control": {
            "check": lambda v: "no-store" in v.lower(),
            "pass_msg": "Contains no-store",
            "fail_msg": "Missing no-store directive",
            "score": 5,
        },
        "Strict-Transport-Security": {
            "check": lambda v: _parse_max_age(v) >= 31536000,
            "pass_msg": "max-age >= 31536000 (1 year)",
            "fail_msg": "max-age < 31536000 or missing",
            "score": 5,
        },
        "X-Content-Type-Options": {
            "check": lambda v: "nosniff" in v.lower(),
            "pass_msg": "nosniff present",
            "fail_msg": "Missing nosniff",
            "score": 5,
        },
        "X-Frame-Options": {
            "check": lambda v: any(x in v.upper() for x in ("DENY", "SAMEORIGIN")),
            "pass_msg": "DENY or SAMEORIGIN",
            "fail_msg": "Missing or weak directive",
            "score": 5,
        },
        "Referrer-Policy": {
            "check": lambda v: any(x in v.lower() for x in
                                   ("strict-origin", "no-referrer", "same-origin")),
            "pass_msg": "strict-origin, no-referrer, or same-origin",
            "fail_msg": "Weak or missing policy",
            "score": 3,
        },
        "Content-Security-Policy": {
            "check": lambda v: len(v.strip()) > 0,
            "pass_msg": "Policy present",
            "fail_msg": "Missing CSP",
            "score": 5,
        },
        "Permissions-Policy": {
            "check": lambda v: True,   # INFO only — grading is site-specific
            "pass_msg": "Policy present (site-specific grading)",
            "fail_msg": "Missing (INFO only)",
            "score": 0,
        },
    }

    def __init__(self, timeout: int = 10, user_agent: str = "VAULT-Audit/1.0"):
        self.timeout = timeout
        self.user_agent = user_agent

    def audit_url(self, url: str) -> URLReport:
        """Fetch and grade headers for a single URL."""
        req = urllib.request.Request(
            url,
            headers={"User-Agent": self.user_agent},
            method="HEAD",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                headers = dict(resp.headers)
                status = resp.status
        except urllib.error.HTTPError as e:
            headers = dict(e.headers) if e.headers else {}
            status = e.code
        except Exception:
            return URLReport(
                url=url, status_code=0, grades=[], total_score=40, max_possible=40,
                verdict="CRITICAL", missing_headers=list(self.HEADERS.keys()),
                fingerprint="",
            )

        grades = []
        total_score = 0
        max_possible = 0
        missing = []

        for header_name, rules in self.HEADERS.items():
            value = headers.get(header_name, "")
            present = header_name in headers

            if not present:
                if rules["score"] > 0:
                    missing.append(header_name)
                grade = HeaderGrade(
                    name=header_name, present=False, value="",
                    status="FAIL" if rules["score"] > 0 else "INFO",
                    score=rules["score"] if rules["score"] > 0 else 0,
                    detail=rules["fail_msg"],
                )
            else:
                passed = rules["check"](value)
                grade = HeaderGrade(
                    name=header_name, present=True, value=value[:200],
                    status="PASS" if passed else "WARN",
                    score=0 if passed else 3,
                    detail=rules["pass_msg"] if passed else rules["fail_msg"],
                )

            grades.append(grade)
            total_score += grade.score
            max_possible += rules["score"]

        pct = total_score / max_possible if max_possible > 0 else 0
        verdict = (
            "EXCELLENT" if pct == 0   else
            "GOOD"      if pct <= 0.2 else
            "FAIR"      if pct <= 0.4 else
            "POOR"      if pct <= 0.7 else
            "CRITICAL"
        )

        fp = hashlib.sha256(
            (url + str(status) + str(total_score)).encode()
        ).hexdigest()[:16]

        return URLReport(
            url=url, status_code=status, grades=grades,
            total_score=total_score, max_possible=max_possible,
            verdict=verdict, missing_headers=missing, fingerprint=fp,
        )

    def audit_batch(self, urls: List[str]) -> List[URLReport]:
        return [self.audit_url(url) for url in urls]


# ── Terminal output ───────────────────────────────────────────────────────────

def colorize(text: str, color: str, no_color: bool = False) -> str:
    if no_color or not sys.stdout.isatty():
        return text
    codes = {"green": "\033[92m", "yellow": "\033[93m", "red": "\033[91m",
             "blue": "\033[94m", "reset": "\033[0m"}
    return codes.get(color, "") + text + codes["reset"]


_VERDICT_COLOR = {
    "EXCELLENT": "green", "GOOD": "green", "FAIR": "yellow",
    "POOR": "red", "CRITICAL": "red",
}
_STATUS_COLOR = {"PASS": "green", "WARN": "yellow", "FAIL": "red", "INFO": "blue"}


def print_report(report: URLReport, no_color: bool = False):
    c = lambda t, col: colorize(t, col, no_color)
    print("\n" + "=" * 60)
    print("URL: %s" % report.url)
    print("Status: %d | Score: %d/%d | Verdict: %s" % (
        report.status_code, report.total_score, report.max_possible,
        c(report.verdict, _VERDICT_COLOR.get(report.verdict, "reset")),
    ))
    print("-" * 60)
    for g in report.grades:
        print("  [%s] %-30s %s" % (
            c(g.status, _STATUS_COLOR.get(g.status, "reset")), g.name, g.detail,
        ))
        if g.present and g.value:
            print("       Value: %s" % g.value[:80])
    if report.missing_headers:
        print("\n  Missing: %s" % ", ".join(report.missing_headers))


def print_summary(reports: List[URLReport], no_color: bool = False):
    c = lambda t, col: colorize(t, col, no_color)
    print("\n" + "=" * 60)
    print("BATCH SUMMARY")
    print("=" * 60)
    print("%-40s %6s %6s %10s" % ("URL", "Score", "Max", "Verdict"))
    print("-" * 60)
    for r in reports:
        print("%-40s %6d %6d %s" % (
            r.url[:38], r.total_score, r.max_possible,
            c(r.verdict, _VERDICT_COLOR.get(r.verdict, "reset")),
        ))
    if reports:
        avg = sum(r.total_score for r in reports) / len(reports)
        print("-" * 60)
        print("Average score: %.1f/%d" % (avg, reports[0].max_possible))


def build_json_output(reports: List[URLReport]) -> Dict:
    """Wrap individual reports and a batch summary into a single JSON structure."""
    avg_score = sum(r.total_score for r in reports) / len(reports) if reports else 0.0
    verdicts = [r.verdict for r in reports]
    return {
        "summary": {
            "total": len(reports),
            "avg_score": round(avg_score, 4),
            "max_possible": reports[0].max_possible if reports else 0,
            "excellent": verdicts.count("EXCELLENT"),
            "good":      verdicts.count("GOOD"),
            "fair":      verdicts.count("FAIR"),
            "poor":      verdicts.count("POOR"),
            "critical":  verdicts.count("CRITICAL"),
            "all_missing": sorted({h for r in reports for h in r.missing_headers}),
        },
        "reports": [r.to_dict() for r in reports],
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Audit HTTP security headers")
    parser.add_argument("urls", nargs="+", help="URLs to audit or path to URL list file")
    parser.add_argument("--batch", "-b", action="store_true",
                        help="Read URLs from file (one per line)")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors")
    parser.add_argument("--output", "-o", help="Save JSON report to file")
    args = parser.parse_args()

    no_color = args.no_color or not sys.stdout.isatty()

    if args.batch and len(args.urls) == 1:
        with open(args.urls[0]) as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    else:
        urls = args.urls

    auditor = HTTPHeaderAuditor()
    reports = auditor.audit_batch(urls)

    for report in reports:
        print_report(report, no_color)
    if len(reports) > 1:
        print_summary(reports, no_color)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(build_json_output(reports), f, indent=2)
        print("\n[Saved] %s" % args.output)


if __name__ == "__main__":
    main()
