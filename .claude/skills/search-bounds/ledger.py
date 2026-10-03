#!/usr/bin/env python3
"""Per-branch search ledger: records bounds so no branch hides behind another.

    python3 ledger.py --new "k=5 odd shape C1" 5000 6e14
    python3 ledger.py --show
"""
import json
import os
import sys

STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ledger.json")


def load():
    return json.load(open(STORE)) if os.path.exists(STORE) else []


def show():
    rows = load()
    if not rows:
        print("ledger empty")
        return
    print("%-34s %-14s %-12s %s" % ("branch", "param bound", "n bound", "kind"))
    for r in rows:
        print("%-34s %-14s %-12s %s"
              % (r["branch"], r["param"], r["n"], r["kind"]))
    ns = [float(r["n"]) for r in rows if r["kind"] == "search"]
    if ns:
        print("\nWEAKEST search branch: n <= %.3g" % min(ns))
        print("Quote THAT for the layer, or quote every branch. Never the best.")


def new(branch, param, n, kind="search"):
    rows = load()
    rows.append({"branch": branch, "param": str(param), "n": str(n),
                 "kind": kind})
    json.dump(rows, open(STORE, "w"), indent=1)
    print("recorded:", branch, param, n, kind)
    show()


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--show":
        show()
    elif len(a) >= 4 and a[0] == "--new":
        new(a[1], a[2], a[3], a[4] if len(a) > 4 else "search")
    else:
        print(__doc__)
