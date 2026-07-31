#!/usr/bin/env python3
"""
vault/audit/runner.py

Single entry point that runs both auditors against each URL and produces
combined terminal output and a unified JSON envelope.

Usage:
    python runner.py https://example.com
    python runner.py urls.txt --batch
    python runner.py urls.txt --batch --output report.json --no-color
"""

import sys
import json
import argparse
from typing import List, Dict

from vault.audit.http_security_auditor import (
    HTTPHeaderAuditor, URLReport,
    build_json_output as header_json,
    print_report as print_header_report,
    print_summary as print_header_summary,
    colorize, _VERDICT_COLOR as _H_VERDICT_COLOR,
)
from vault.audit.platform_restriction_detector import (
    PlatformRestrictionDetector, RestrictionReport,
    build_json_output as restrict_json,
    print_report as print_restrict_report,
    print_summary as print_restrict_summary,
    _VERDICT_COLOR as _R_VERDICT_COLOR, _c, _RST,
)


# ── Combined report ───────────────────────────────────────────────────────────

def run_url(url: str, header_auditor: HTTPHeaderAuditor,
            restrict_detector: PlatformRestrictionDetector):
    h = header_auditor.audit_url(url)
    r = restrict_detector.detect_url(url)
    return h, r


def print_combined_report(h: URLReport, r: RestrictionReport, no_color: bool = False):
    c = lambda t, col: colorize(t, col, no_color)
    rc = lambda t, code: _c(t, code, no_color)

    print("\n" + "█" * 64)
    print("URL: %s" % h.url)
    print("█" * 64)

    # Header audit block
    print("\n  ── Header Audit ──────────────────────────────────")
    hcol = _H_VERDICT_COLOR.get(h.verdict, "reset")
    print("  Score: %d/%d  Verdict: %s" % (
        h.total_score, h.max_possible, c(h.verdict, hcol),
    ))
    _STATUS_COLOR = {"PASS": "green", "WARN": "yellow", "FAIL": "red", "INFO": "blue"}
    for g in h.grades:
        print("    [%s] %-30s %s" % (
            c(g.status, _STATUS_COLOR.get(g.status, "reset")), g.name, g.detail,
        ))

    # Restriction audit block
    print("\n  ── Restriction Audit ─────────────────────────────")
    vcol = _R_VERDICT_COLOR.get(r.verdict, "")
    print("  Risk: %.4f  Verdict: %s" % (
        r.risk_score, rc(r.verdict, vcol),
    ))
    if r.matches:
        _SEV_COLOR = {"CRITICAL": "\033[91m", "HIGH": "\033[91m",
                      "MEDIUM": "\033[93m", "LOW": "\033[94m"}
        for m in r.matches:
            print("    [%s] %s" % (rc(m.severity, _SEV_COLOR.get(m.severity, "")), m.category))
            print("      \"%s\"" % m.evidence)
    else:
        print("    No restriction patterns detected.")
    if r.transparency_gaps:
        for g in r.transparency_gaps:
            print("    [TRANSPARENCY GAP] HTTP %d — missing: %s" % (
                g.http_code, ", ".join(g.missing_headers),
            ))
    print()


def print_combined_summary(pairs: List, no_color: bool = False):
    c = lambda t, col: colorize(t, col, no_color)
    rc = lambda t, code: _c(t, code, no_color)

    h_reports = [h for h, _ in pairs]
    r_reports = [r for _, r in pairs]

    if len(pairs) <= 1:
        return

    print("=" * 72)
    print("COMBINED BATCH SUMMARY  (%d URLs)" % len(pairs))
    print("=" * 72)
    print("%-36s  %-12s  %-8s  %-16s  %s" % (
        "URL", "Hdr Verdict", "Hdr Scr", "Restr Verdict", "Categories",
    ))
    print("-" * 72)

    for h, r in pairs:
        hcol = _H_VERDICT_COLOR.get(h.verdict, "reset")
        vcol = _R_VERDICT_COLOR.get(r.verdict, "")
        cats = ", ".join(r.categories_triggered) if r.categories_triggered else "—"
        print("%-36s  %-12s  %4d/%-3d  %-16s  %s" % (
            h.url[:34],
            c(h.verdict, hcol),
            h.total_score, h.max_possible,
            rc(r.verdict, vcol),
            cats,
        ))

    print("-" * 72)
    avg_h = sum(h.total_score for h in h_reports) / len(h_reports)
    avg_r = sum(r.risk_score  for r in r_reports) / len(r_reports)
    all_cats = sorted({cat for r in r_reports for cat in r.categories_triggered})
    print("Avg header score: %.1f/%d  |  Avg restriction risk: %.2f" % (
        avg_h, h_reports[0].max_possible if h_reports else 0, avg_r,
    ))
    if all_cats:
        print("Restriction categories seen: %s" % ", ".join(all_cats))
    print()


# ── JSON envelope ─────────────────────────────────────────────────────────────

def build_combined_json(pairs: List) -> Dict:
    h_reports = [h for h, _ in pairs]
    r_reports = [r for _, r in pairs]
    h_out = header_json(h_reports)
    r_out = restrict_json(r_reports)
    return {
        "summary": {
            "total_urls": len(pairs),
            "header_audit":      h_out["summary"],
            "restriction_audit": r_out["summary"],
        },
        "reports": [
            {
                "url":              h.url,
                "header_audit":     h.to_dict(),
                "restriction_audit": r.to_dict(),
            }
            for h, r in pairs
        ],
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Run header + restriction auditors against one or more URLs"
    )
    parser.add_argument("urls", nargs="+",
                        help="URLs to audit, or a single file path with --batch")
    parser.add_argument("--batch", "-b", action="store_true",
                        help="Read URLs from file (one per line)")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors")
    parser.add_argument("--output", "-o", metavar="FILE",
                        help="Write combined JSON report to FILE")
    args = parser.parse_args()

    no_color = args.no_color or not sys.stdout.isatty()

    if args.batch and len(args.urls) == 1:
        with open(args.urls[0]) as f:
            urls = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    else:
        urls = args.urls

    header_auditor   = HTTPHeaderAuditor()
    restrict_detector = PlatformRestrictionDetector()

    pairs = [run_url(url, header_auditor, restrict_detector) for url in urls]

    for h, r in pairs:
        print_combined_report(h, r, no_color)
    print_combined_summary(pairs, no_color)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(build_combined_json(pairs), f, indent=2)
        print("[Saved] %s" % args.output)


if __name__ == "__main__":
    main()
