#!/usr/bin/env python3
"""
vault/audit/runner.py

Single entry point that runs all three auditors and produces combined
terminal output and a unified JSON envelope.

Usage:
    python runner.py https://example.com
    python runner.py urls.txt --batch
    python runner.py urls.txt --batch --output report.json --no-color
    python runner.py https://example.com --kimi      # also emit Kimi gate
"""

import sys
import json
import argparse
from typing import List, Dict, Tuple, Optional

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
from vault.audit.kimi_session_protocol import (
    EpistemicGate, Status, Finding,
    ResidueFingerprint, DRIntegrityChain,
    build_kimi_gate, STATUS_ORBIT,
)


# ── Gate: classify restriction findings into the epistemic lattice ─────────────

_SEV_TO_STATUS = {
    "CRITICAL": Status.PROVISIONAL,   # text match alone is provisional
    "HIGH":     Status.PROVISIONAL,
    "MEDIUM":   Status.UNVERIFIABLE,
    "LOW":      Status.UNVERIFIABLE,
}

_HTTP_CORROBORATION = {402, 403, 429, 451}  # codes that confirm restriction claims


def gate_from_restriction(h: URLReport,
                           r: RestrictionReport) -> Tuple[EpistemicGate, ResidueFingerprint]:
    """
    Build an EpistemicGate from one (URLReport, RestrictionReport) pair.

    Classification logic:
      CRITICAL/HIGH + corroborating HTTP code → VERIFIED
      CRITICAL/HIGH text match only           → PROVISIONAL
      MEDIUM/LOW                              → UNVERIFIABLE
      TransparencyGap                         → PROVISIONAL
      Internal contradiction (same URL claims
        restriction AND no restriction)       → SEAM (INADMISSIBLE)

    Corroboration: HTTP status in {402, 403, 429, 451} confirms any match.
    """
    gate = EpistemicGate()
    fp   = ResidueFingerprint()

    fp.ingest(r.source)  # fingerprint the URL/label itself

    corroborated = r.http_status in _HTTP_CORROBORATION if r.http_status else False

    for m in r.matches:
        base = _SEV_TO_STATUS.get(m.severity, Status.UNVERIFIABLE)
        status = Status.VERIFIED if (corroborated and base == Status.PROVISIONAL) else base
        gate.add(m.category, status, m.evidence[:120], r.source)
        fp.ingest(m.evidence, chunk_size=32)

    for tg in r.transparency_gaps:
        gate.add(
            "TRANSPARENCY_GAP HTTP %d" % tg.http_code,
            Status.PROVISIONAL,
            "Missing headers: %s" % ", ".join(tg.missing_headers),
            r.source,
        )

    # Contradiction: verdict says no restriction but HTTP code says otherwise
    if r.verdict == "CLEAN" and corroborated:
        gate.add(
            "Verdict/HTTP contradiction",
            Status.INADMISSIBLE,
            "Verdict=CLEAN but HTTP %d indicates restriction" % r.http_status,
            r.source,
        )

    return gate, fp


# ── Terminal output ───────────────────────────────────────────────────────────

_STATUS_LABEL = {
    Status.VERIFIED:     "VERIFIED",
    Status.PROVISIONAL:  "PROVISIONAL",
    Status.UNVERIFIABLE: "UNVERIFIABLE",
    Status.INADMISSIBLE: "INADMISSIBLE",
}

_STATUS_ANSI = {
    Status.VERIFIED:     "\033[92m",   # green
    Status.PROVISIONAL:  "\033[93m",   # yellow
    Status.UNVERIFIABLE: "\033[94m",   # blue
    Status.INADMISSIBLE: "\033[91m",   # red
}


def _sc(text: str, status: Status, no_color: bool) -> str:
    if no_color:
        return text
    return "%s%s%s" % (_STATUS_ANSI[status], text, _RST)


def print_gate_section(gate: EpistemicGate, fp: ResidueFingerprint,
                       no_color: bool = False) -> None:
    ev = gate.evaluate()
    print("\n  ── Epistemic Gate ────────────────────────────────")
    print("  Findings: %d  |  V:%d  P:%d  U:%d  I:%d%s" % (
        ev['total'],
        ev['verified'], ev['provisional'],
        ev['unverifiable'], ev['inadmissible'],
        ("  [SEAM]" if ev['seam_triggered'] else ""),
    ))
    for status in reversed(Status):
        names = ev['findings'][status.name]
        if names:
            orbit = STATUS_ORBIT[status.name]
            label = _sc("%s → %s" % (_STATUS_LABEL[status], orbit), status, no_color)
            print("    %s" % label)
            for n in names:
                print("      · %s" % n)
    if ev['seam_triggered']:
        seam_msg = _sc("SEAM (contradiction): %s" % ev['contradictions'], Status.INADMISSIBLE, no_color)
        print("    %s" % seam_msg)

    dom = fp.dominant_orbit()
    sig = fp.signature()
    top = sorted(sig.items(), key=lambda x: -x[1])[:3]
    top_str = "  ".join("%s:%d" % (k, v) for k, v in top if v > 0)
    print("  Residue fingerprint: dominant=%s  [%s]" % (dom, top_str))


def print_combined_report(h: URLReport, r: RestrictionReport,
                           gate: EpistemicGate, fp: ResidueFingerprint,
                           no_color: bool = False) -> None:
    c  = lambda t, col: colorize(t, col, no_color)
    rc = lambda t, code: _c(t, code, no_color)

    print("\n" + "█" * 64)
    print("URL: %s" % h.url)
    print("█" * 64)

    # Header audit
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

    # Restriction audit
    print("\n  ── Restriction Audit ─────────────────────────────")
    vcol = _R_VERDICT_COLOR.get(r.verdict, "")
    print("  Risk: %.4f  Verdict: %s" % (
        r.risk_score, rc(r.verdict, vcol),
    ))
    if r.matches:
        _SEV_COLOR = {"CRITICAL": "\033[91m", "HIGH": "\033[91m",
                      "MEDIUM": "\033[93m",   "LOW":  "\033[94m"}
        for m in r.matches:
            print("    [%s] %s" % (rc(m.severity, _SEV_COLOR.get(m.severity, "")), m.category))
            print("      \"%s\"" % m.evidence)
    else:
        print("    No restriction patterns detected.")
    if r.transparency_gaps:
        for tg in r.transparency_gaps:
            print("    [TRANSPARENCY GAP] HTTP %d — missing: %s" % (
                tg.http_code, ", ".join(tg.missing_headers),
            ))

    # Epistemic gate
    print_gate_section(gate, fp, no_color)
    print()


def print_combined_summary(triples: List, chain: DRIntegrityChain,
                            no_color: bool = False) -> None:
    c  = lambda t, col: colorize(t, col, no_color)
    rc = lambda t, code: _c(t, code, no_color)

    h_reports = [h for h, _, __, ___ in triples]
    r_reports = [r for _, r, __, ___ in triples]
    gates     = [g for _, __, g, ___ in triples]

    if len(triples) <= 1:
        _print_chain_summary(chain, no_color)
        return

    print("=" * 72)
    print("COMBINED BATCH SUMMARY  (%d URLs)" % len(triples))
    print("=" * 72)
    print("%-30s  %-10s  %-6s  %-14s  %-6s  %s" % (
        "URL", "Hdr Verdict", "Score", "Restr Verdict", "Gate", "SEAM",
    ))
    print("-" * 72)

    for h, r, g, _ in triples:
        hcol = _H_VERDICT_COLOR.get(h.verdict, "reset")
        vcol = _R_VERDICT_COLOR.get(r.verdict, "")
        ev   = g.evaluate()
        seam = "YES" if ev['seam_triggered'] else "—"
        gate_sum = "V%d P%d U%d I%d" % (
            ev['verified'], ev['provisional'], ev['unverifiable'], ev['inadmissible'],
        )
        print("%-30s  %-10s  %4d/%-2d  %-14s  %-6s  %s" % (
            h.url[:28],
            c(h.verdict, hcol),
            h.total_score, h.max_possible,
            rc(r.verdict, vcol),
            gate_sum,
            seam,
        ))

    print("-" * 72)
    avg_h    = sum(h.total_score for h in h_reports) / len(h_reports)
    avg_r    = sum(r.risk_score  for r in r_reports) / len(r_reports)
    all_cats = sorted({cat for r in r_reports for cat in r.categories_triggered})
    seam_count = sum(1 for g in gates if g.evaluate()['seam_triggered'])
    print("Avg header score: %.1f  |  Avg restriction risk: %.2f  |  SEAM triggers: %d/%d" % (
        avg_h, avg_r, seam_count, len(triples),
    ))
    if all_cats:
        print("Restriction categories: %s" % ", ".join(all_cats))
    print()

    _print_chain_summary(chain, no_color)


def _print_chain_summary(chain: DRIntegrityChain, no_color: bool = False) -> None:
    ok  = chain.integrity_ok()
    col = "\033[92m" if ok else "\033[91m"
    r   = chain.ratio()
    if chain._drs:
        status = _c("OK" if ok else "FAIL", col, no_color)
        print("Session DR chain:  %d messages  ratio=%.6f  integrity=%s" % (
            len(chain._drs), r if r else 0.0, status,
        ))
        print()


def print_kimi_gate(no_color: bool = False) -> None:
    gate = build_kimi_gate()
    ev   = gate.evaluate()
    print("=" * 64)
    print("KIMI SESSION GATE (vault/audit/kimi_friction_pattern_report.md)")
    print("=" * 64)
    for status in reversed(Status):
        names = ev['findings'][status.name]
        if names:
            orbit = STATUS_ORBIT[status.name]
            label = _sc("%s → %s (%d)" % (_STATUS_LABEL[status], orbit, len(names)),
                        status, no_color)
            print("  %s" % label)
            for n in names:
                print("    · %s" % n)
    if ev['seam_triggered']:
        seam = _sc("SEAM: %s" % ev['contradictions'], Status.INADMISSIBLE, no_color)
        print("  %s" % seam)
    print()


# ── JSON envelope ─────────────────────────────────────────────────────────────

def _gate_to_dict(gate: EpistemicGate, fp: ResidueFingerprint) -> Dict:
    ev = gate.evaluate()
    return {
        "total":           ev['total'],
        "verified":        ev['verified'],
        "provisional":     ev['provisional'],
        "unverifiable":    ev['unverifiable'],
        "inadmissible":    ev['inadmissible'],
        "seam_triggered":  ev['seam_triggered'],
        "contradictions":  ev['contradictions'],
        "findings":        ev['findings'],
        "residue_fingerprint": {
            "dominant_orbit": fp.dominant_orbit(),
            "signature":      fp.signature(),
        },
    }


def build_combined_json(triples: List, chain: DRIntegrityChain,
                         kimi: bool = False) -> Dict:
    h_reports = [h for h, _, __, ___ in triples]
    r_reports = [r for _, r, __, ___ in triples]
    h_out = header_json(h_reports)
    r_out = restrict_json(r_reports)

    result: Dict = {
        "summary": {
            "total_urls":        len(triples),
            "header_audit":      h_out["summary"],
            "restriction_audit": r_out["summary"],
            "gate": {
                "seam_count": sum(
                    1 for _, __, g, ___ in triples if g.evaluate()['seam_triggered']
                ),
            },
            "session_integrity": {
                "messages":    len(chain._drs),
                "ratio":       chain.ratio(),
                "integrity_ok": chain.integrity_ok(),
            },
        },
        "reports": [
            {
                "url":              h.url,
                "header_audit":     h.to_dict(),
                "restriction_audit": r.to_dict(),
                "gate":             _gate_to_dict(g, fp),
            }
            for h, r, g, fp in triples
        ],
    }

    if kimi:
        kimi_gate = build_kimi_gate()
        result["kimi_gate"] = kimi_gate.evaluate()

    return result


# ── URL runner ────────────────────────────────────────────────────────────────

def run_url(url: str,
            header_auditor: HTTPHeaderAuditor,
            restrict_detector: PlatformRestrictionDetector,
            chain: DRIntegrityChain):
    h = header_auditor.audit_url(url)
    r = restrict_detector.detect_url(url)
    g, fp = gate_from_restriction(h, r)
    chain.add_message(url)
    return h, r, g, fp


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Run header + restriction + epistemic gate auditors"
    )
    parser.add_argument("urls", nargs="+",
                        help="URLs to audit, or a single file path with --batch")
    parser.add_argument("--batch", "-b", action="store_true",
                        help="Read URLs from file (one per line)")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors")
    parser.add_argument("--output", "-o", metavar="FILE",
                        help="Write combined JSON report to FILE")
    parser.add_argument("--kimi", action="store_true",
                        help="Also emit the pre-built Kimi session gate")
    args = parser.parse_args()

    no_color = args.no_color or not sys.stdout.isatty()

    if args.batch and len(args.urls) == 1:
        with open(args.urls[0]) as f:
            urls = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    else:
        urls = args.urls

    header_auditor    = HTTPHeaderAuditor()
    restrict_detector = PlatformRestrictionDetector()
    chain             = DRIntegrityChain()

    triples = [run_url(url, header_auditor, restrict_detector, chain) for url in urls]

    for h, r, g, fp in triples:
        print_combined_report(h, r, g, fp, no_color)

    print_combined_summary(triples, chain, no_color)

    if args.kimi:
        print_kimi_gate(no_color)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(build_combined_json(triples, chain, kimi=args.kimi), f, indent=2)
        print("[Saved] %s" % args.output)


if __name__ == "__main__":
    main()
