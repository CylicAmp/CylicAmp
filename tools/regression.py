#!/usr/bin/env python3
"""Rerun every runnable theorem file and report which ones now fail.

This is the self-correction that matters: it catches an edit that breaks an
EARLIER proof, which is the failure mode a corpus of 430+ files actually has.

    python3 tools/regression.py                 # run all, write state
    python3 tools/regression.py --timeout 30    # shorter per-file budget
    python3 tools/regression.py --diff          # compare against saved state
    python3 tools/regression.py --only theorem_245
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["math/theorems", "math/primes", "math/turbulence", "cylicamp"]
STATE = ROOT / "tools" / "regression_state.json"
SKIP = {"__init__.py", "CATEGORY_INDEX.py"}


def targets(only=None):
    out = []
    for d in DIRS:
        p = ROOT / d
        if not p.is_dir():
            continue
        for f in sorted(p.glob("*.py")):
            if f.name in SKIP or f.name.startswith("_"):
                continue
            if only and only not in f.name:
                continue
            txt = f.read_text(errors="replace")
            if "__main__" not in txt:      # not a runnable script
                continue
            out.append(str(f.relative_to(ROOT)))
    return out


def run_one(args):
    rel, timeout = args
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, rel], cwd=ROOT, capture_output=True,
                           text=True, timeout=timeout)
        dt = time.time() - t0
        if r.returncode == 0:
            return rel, "PASS", dt, ""
        tail = (r.stderr or r.stdout).strip().splitlines()
        msg = tail[-1][:200] if tail else "exit %d" % r.returncode
        kind = "ASSERT" if "AssertionError" in (r.stderr or "") else "ERROR"
        return rel, kind, dt, msg
    except subprocess.TimeoutExpired:
        return rel, "TIMEOUT", time.time() - t0, "exceeded %ds" % timeout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=int, default=60)
    ap.add_argument("--workers", type=int, default=max(2, (os.cpu_count() or 4) - 1))
    ap.add_argument("--only", default=None)
    ap.add_argument("--diff", action="store_true")
    a = ap.parse_args()

    files = targets(a.only)
    print("regression: %d runnable files, timeout %ds, %d workers"
          % (len(files), a.timeout, a.workers))
    t0 = time.time()
    results = {}
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for rel, status, dt, msg in ex.map(run_one,
                                           [(f, a.timeout) for f in files]):
            results[rel] = {"status": status, "secs": round(dt, 1), "msg": msg}
            if status != "PASS":
                print("  %-8s %-62s %s" % (status, rel, msg[:90]))

    counts = {}
    for v in results.values():
        counts[v["status"]] = counts.get(v["status"], 0) + 1
    print("\n%s   (%.0fs wall)" % (
        "  ".join("%s %d" % (k, counts[k]) for k in sorted(counts)),
        time.time() - t0))

    if a.diff and STATE.exists():
        old = json.load(open(STATE))
        broke = [f for f in results
                 if old.get(f, {}).get("status") == "PASS"
                 and results[f]["status"] != "PASS"]
        fixed = [f for f in results
                 if old.get(f, {}).get("status") not in (None, "PASS")
                 and results[f]["status"] == "PASS"]
        print("\nNEWLY BROKEN (%d): %s" % (len(broke), broke or "none"))
        print("NEWLY FIXED  (%d): %s" % (len(fixed), fixed or "none"))
        if broke:
            return 1
    if not a.only:
        json.dump(results, open(STATE, "w"), indent=1, sort_keys=True)
        print("state written to %s" % STATE.relative_to(ROOT))
    return 0 if counts.get("ASSERT", 0) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
