#!/usr/bin/env python3
"""Search the corpus before writing a theorem. Usage:
   prior.py claim "orbits sum to 37 or 74"      # topic + phrase search
   prior.py value 495                            # every file mentioning a value
   prior.py topic quotient                       # collision report for a topic
"""
import re, sys, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[3]
DIRS = ["math/theorems", "math/primes", "math/turbulence", "cylicamp"]

TOPICS = {
    "quotient": [r"Z/12", r"quotient group", r"orbit index", r"dlog"],
    "orbit-sum": [r"1 \+ 10 \+ 26", r"orbit sum", r"sums? to (?:37|74)"],
    "phi3": [r"Phi_3", r"x\^2 ?\+ ?x ?\+ ?1", r"cube root"],
    "dr-law": [r"37 ?== ?1 \(mod 9\)", r"DR subtraction", r"wrap count"],
    "negation": [r"negation dual", r"37 ?- ?x", r"self-negating"],
    "koopman": [r"Koopman"],
    "twin": [r"twin prime"],
    "sophie": [r"Sophie ?Germain"],
    "rule30": [r"Rule ?30"],
    "zeta": [r"Riemann zero", r"zeta zero", r"floor\(gamma"],
    "golden": [r"golden ratio", r"Fibonacci", r"Pisano"],
    "collatz": [r"Collatz", r"3x ?\+ ?1"],
    "kaprekar": [r"Kaprekar"],
    "cycle": [r"cycle type", r"functional graph", r"preperiod", r"transient"],
}

def files():
    for d in DIRS:
        p = ROOT / d
        if p.is_dir():
            yield from sorted(p.glob("*.py"))

def hits(pats):
    out = []
    for f in files():
        try:
            t = f.read_text(errors="replace")
        except OSError:
            continue
        n = sum(len(re.findall(p, t, re.I)) for p in pats)
        if n:
            out.append((n, f.name))
    return sorted(out, reverse=True)

def title(name):
    try:
        t = (ROOT / "math/theorems" / name).read_text(errors="replace")
    except OSError:
        return ""
    m = re.search(r'"""\s*\n\s*(.+)', t)
    return m.group(1)[:78] if m else ""

def main():
    if len(sys.argv) < 3:
        print(__doc__); return
    mode, arg = sys.argv[1], " ".join(sys.argv[2:])
    if mode == "topic":
        pats = TOPICS.get(arg)
        if not pats:
            print(f"topics: {', '.join(sorted(TOPICS))}"); return
        h = hits(pats)
        print(f"topic '{arg}': {len(h)} files\n")
        for n, f in h[:20]:
            print(f"  {n:4d}  {f}\n        {title(f)}")
    elif mode == "value":
        h = hits([r"\b" + re.escape(arg) + r"\b"])
        print(f"value {arg}: {len(h)} files\n")
        for n, f in h[:20]:
            print(f"  {n:4d}  {f}\n        {title(f)}")
    elif mode == "claim":
        words = [w for w in re.findall(r"[a-zA-Z_]{4,}|\d{2,}", arg)][:6]
        print(f"claim words: {words}\n")
        best = {}
        for t, pats in TOPICS.items():
            h = hits(pats)
            if h:
                best[t] = h
        for w in words:
            h = hits([r"\b" + re.escape(w) + r"\b"])
            if h:
                print(f"  '{w}' -> {len(h)} files, top: "
                      f"{', '.join(f for _, f in h[:4])}")
        print("\n  RULE: open every file above before writing. A hit is a")
        print("  shortlist entry, not a verdict -- the detector over-flags.")
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
