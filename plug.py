#!/usr/bin/env python3
"""Plug your work in. Paste your lines -- everything else is automatic. No Claude needed.

    python3 plug.py              paste your lines, then a line with just END (or Ctrl-D)
    python3 plug.py notes.txt    or give it a file
    python3 plug.py --no-push    save and run everything, but do not send it to GitHub

Every run:
  1. Your lines are saved exactly as you wrote them, numbered and timestamped
     (owner_work/messages/<date>.txt -- the same record the session hook keeps).
  2. Every number in them goes through the frameworks: the six registers
     (digit-protocols engine) and the full GF(37) audit (gf37-audit).
  3. Every number you wrote in both orders (12 and 21) gets the full flip-pair expansion.
  4. One report, your lines first, the results beside them:
     owner_work/plugged/<time>.txt
  5. It commits and pushes to GitHub if this copy of the repo can, and says plainly if not.
"""
import datetime as dt
import importlib.util
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
ENGINE = ROOT / ".claude" / "skills" / "digit-protocols" / "engine.py"
AUDIT = ROOT / ".claude" / "skills" / "gf37-audit" / "audit.py"
PLUGGED = ROOT / "owner_work" / "plugged"
MAX_DIGITS = 18          # longer numbers get the six registers only; the audit factors


def load_recorder():
    spec = importlib.util.spec_from_file_location("owner_record", ROOT / "tools" / "owner_record.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_input(args):
    files = [a for a in args if not a.startswith("--")]
    if files:
        return pathlib.Path(files[0]).read_text(encoding="utf-8")
    if sys.stdin.isatty():
        print("Paste your lines. When done, type END on its own line (or press Ctrl-D).")
    lines = []
    for line in sys.stdin:
        if line.rstrip("\n").strip() == "END":
            break
        lines.append(line)
    return "".join(lines)


def run(cmd):
    try:
        r = subprocess.run([sys.executable] + cmd, cwd=ROOT, capture_output=True, text=True, timeout=600)
        return (r.stdout + (("\n" + r.stderr) if r.returncode else "")).rstrip()
    except Exception as e:
        return f"(could not run {' '.join(cmd[:2])}: {e})"


def numbers_by_line(text):
    order, by_line = [], []
    for i, line in enumerate(text.splitlines(), 1):
        found = [int(m) for m in re.findall(r"\d+", line)]
        by_line.append((i, line, found))
        for n in found:
            if n not in order:
                order.append(n)
    return order, by_line


def flip_pairs(nums):
    s, pairs = set(nums), []
    for n in nums:
        rs = str(n)[::-1]
        r = int(rs)
        if n >= 10 and rs[0] != "0" and r != n and r in s and (r, n) not in pairs:
            pairs.append((n, r))
    return pairs


def lines_both_ways(by_line):
    """Lines that use the same numbers in a different order: 2+4=6 / 4+2=6, 2÷11 / 11÷2."""
    groups = {}
    for i, line, found in by_line:
        if len(found) >= 2:
            groups.setdefault(tuple(sorted(found)), []).append((i, line.strip(), found))
    return [g for g in groups.values() if len({tuple(f) for _, _, f in g}) > 1]


def git_save(stamp, first_line):
    def g(*a):
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)
    if g("rev-parse", "--git-dir").returncode:
        return "Not a git copy of the repo -- saved on this device only."
    g("add", "owner_work")
    msg = f"plug {stamp}: {first_line[:60]}"
    c = g("commit", "-q", "-m", msg)
    if c.returncode:
        return "Saved. Nothing new to commit." if "nothing to commit" in (c.stdout + c.stderr) \
            else "Saved on this device. Commit failed: " + (c.stderr or c.stdout).strip()[:200]
    branch = g("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    p = g("push", "-u", "origin", branch)
    return (f"Saved and sent to GitHub (branch {branch})." if p.returncode == 0
            else f"Saved and committed on this device. Push failed: {(p.stderr or p.stdout).strip()[:200]}")


def main(args):
    text = read_input(args)
    if not text.strip():
        print("Nothing pasted.")
        return 1
    now = dt.datetime.now(dt.timezone.utc)
    ts = now.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    stamp = now.strftime("%Y-%m-%dT%H%M%SZ")

    rec = load_recorder()
    msgs = rec.load()
    rec.add(msgs, ts, text)
    rec.write_all(msgs)
    n_msg = len(msgs)

    nums, by_line = numbers_by_line(text)
    pairs = flip_pairs(nums)
    swaps = lines_both_ways(by_line)
    out = [f"PLUGGED {ts}   (your message #{n_msg} in owner_work/messages/{ts[:10]}.txt)", "",
           "=" * 78, "YOUR LINES, exactly as written", "=" * 78]
    out += [f"{i:4d}  {line}" for i, line, _ in by_line]
    out += ["", "=" * 78, "THE NUMBERS IN EACH LINE", "=" * 78]
    out += [f"{i:4d}  {found}" for i, _, found in by_line if found]
    if swaps:
        out += ["", "=" * 78, "LINES YOU WROTE BOTH WAYS ROUND (same numbers, different order)", "=" * 78]
        for g in swaps:
            out += [f"{i:4d}  {line}" for i, line, _ in g] + [""]
    out += ["", "=" * 78, "SIX REGISTERS, every number (digit-protocols engine)", "=" * 78]
    out += [run([str(ENGINE), "n", str(n)]) for n in nums]
    if pairs:
        out += ["", "=" * 78, "PAIRS YOU WROTE IN BOTH ORDERS", "=" * 78]
        out += [run([str(ENGINE), "pair", str(a), str(b)]) for a, b in pairs]
    small = [str(n) for n in nums if len(str(n)) <= MAX_DIGITS]
    if small:
        out += ["", "=" * 78, "GF(37) AUDIT, every number (gf37-audit)", "=" * 78, run([str(AUDIT), *small])]
    report = "\n".join(out) + "\n"

    PLUGGED.mkdir(parents=True, exist_ok=True)
    path = PLUGGED / f"{stamp}.txt"
    path.write_text(report, encoding="utf-8")

    print(f"\nSaved your lines as message #{n_msg}.  {len(nums)} numbers, {len(pairs)} numbers written "
          f"both ways (like 12 and 21), {len(swaps)} line groups written both ways round.")
    print(f"Report: {path.relative_to(ROOT)}")
    if "--no-push" not in args:
        print(git_save(stamp, text.strip().splitlines()[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
