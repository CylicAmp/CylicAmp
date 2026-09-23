"""Report theorem numbers cited in file text that have no theorem file."""
import re, subprocess, sys
from collections import Counter

def scan(root="math/theorems"):
    files = subprocess.run(["git", "ls-files", root],
                           capture_output=True, text=True).stdout.split()
    have = {int(m.group(1)) for f in files
            if (m := re.search(r"theorem_0*(\d+)", f))}
    cited = {}
    for f in files:
        if not f.endswith((".py", ".md")):
            continue
        try:
            txt = open(f, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for n in {int(x) for x in re.findall(r"\bT(\d{1,3})\b", txt)}:
            cited.setdefault(n, []).append(f)
    return have, cited

if __name__ == "__main__":
    have, cited = scan()
    lo = min(have) if have else 0
    dangling = sorted(n for n in cited if n not in have and n >= lo)
    print(f"numbered theorem files present : {len(have)}  (range {lo}-{max(have)})")
    print(f"distinct T-numbers cited       : {len(cited)}")
    pct = 100 * len(dangling) / len(cited) if cited else 0
    print(f"cited with no file             : {len(dangling)}  ({pct:.0f}% of citations)")
    if not dangling:
        print("\nno dangling citations")
        sys.exit(0)
    print(f"\n  {' '.join(map(str, dangling))}\n")
    c = Counter(f for n in dangling for f in cited[n])
    print("files making dangling citations:")
    for f, k in c.most_common(10):
        print(f"  {k:3}  {f.split('/')[-1]}")
    sys.exit(1)
