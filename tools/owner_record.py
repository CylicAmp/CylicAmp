#!/usr/bin/env python3
"""Verbatim record of everything the owner writes (owner, 2026-10-12: "You should have a
whole thing of everything I wrote out! That's the proof that I did the work!").

    python3 tools/owner_record.py --hook          # UserPromptSubmit hook; prompt JSON on stdin
    python3 tools/owner_record.py --transcripts   # backfill from this repo's session transcripts
    python3 tools/owner_record.py --check         # exit 1 unless every message is stored verbatim

Store: owner_work/messages.json (the record), owner_work/index.json (sha256 per message),
owner_work/messages/<YYYY-MM-DD>.txt (the same messages, one plain-text file per day).
Nothing is edited except credentials, which are removed and marked where they were.
The hook never blocks a prompt and prints nothing (UserPromptSubmit stdout reaches the model).
"""
import datetime as dt
import glob
import hashlib
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STORE = ROOT / "owner_work"
MSGS = STORE / "messages.json"
INDEX = STORE / "index.json"
DAYS = STORE / "messages"
SAME_MESSAGE_WINDOW = 30  # seconds: the hook copy and the transcript copy of ONE message;
                          # a resend minutes later is a second message and is kept

CREDENTIALS = [
    r"\bsk-(?:ant-|kimi-|proj-)?[A-Za-z0-9_\-]{20,}",
    r"\bgh[pousr]_[A-Za-z0-9]{20,}",
    r"\bgithub_pat_[A-Za-z0-9_]{20,}",
    r"\bAKIA[0-9A-Z]{16}",
    r"\bxox[abpr]-[A-Za-z0-9-]{10,}",
    r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----",
]
MARK = "[REDACTED: credential removed before commit]"


def redact(text):
    for p in CREDENTIALS:
        text = re.sub(p, MARK, text)
    return text


def is_harness(text):
    s = text.strip()
    return (not s
            or (s.startswith("<system-reminder>") and s.endswith("</system-reminder>"))
            or s.startswith(("<task-notification>", "Stop hook feedback", "<local-command",
                             "<command-name>", "<command-message>", "Base directory for this skill:",
                             "# Workflow authoring reference", "This session is being continued"))
            or "[SYSTEM NOTIFICATION" in s[:200]
            or s == "[Request interrupted by user]")


def parse_ts(ts):
    return dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))


def load():
    return json.loads(MSGS.read_text(encoding="utf-8")) if MSGS.exists() else []


def add(msgs, ts, text):
    text = redact(text)
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    t = parse_ts(ts)
    for m in msgs:
        if (hashlib.sha256(m["text"].encode("utf-8")).hexdigest() == h
                and abs((parse_ts(m["ts"]) - t).total_seconds()) <= SAME_MESSAGE_WINDOW):
            return False
    msgs.append({"ts": ts, "text": text})
    msgs.sort(key=lambda m: m["ts"])
    return True


def write_all(msgs):
    DAYS.mkdir(parents=True, exist_ok=True)
    by_day, index = {}, []
    for n, m in enumerate(msgs, 1):
        by_day.setdefault(m["ts"][:10], []).append((n, m))
    for day, items in by_day.items():
        with open(DAYS / f"{day}.txt", "w", encoding="utf-8") as f:
            f.write(f"Owner's messages, {day}, verbatim as written (UTC timestamps).\n"
                    "Nothing below is edited, except credentials, which are removed and marked "
                    "where they were.\n")
            for n, m in items:
                f.write(f"\n\n===== #{n}  {m['ts']} =====\n{m['text']}\n")
                index.append({"n": n, "ts": m["ts"], "file": f"messages/{day}.txt",
                              "sha256": hashlib.sha256(m["text"].encode("utf-8")).hexdigest(),
                              "chars": len(m["text"])})
    MSGS.write_text(json.dumps(msgs, ensure_ascii=False, indent=1), encoding="utf-8")
    INDEX.write_text(json.dumps(index, indent=1), encoding="utf-8")


def from_transcripts():
    slug = str(ROOT).replace("/", "-")
    found = []
    for path in sorted(glob.glob(os.path.expanduser(f"~/.claude/projects/{slug}/*.jsonl"))):
        for line in open(path, encoding="utf-8"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("type") != "user" or d.get("isMeta") or d.get("isSidechain"):
                continue
            c = d.get("message", {}).get("content")
            texts = [c] if isinstance(c, str) else [
                b.get("text", "") for b in (c or []) if isinstance(b, dict) and b.get("type") == "text"]
            for t in texts:
                if not is_harness(t):
                    found.append((d.get("timestamp", ""), t))
    return found


def check():
    msgs, index = load(), json.loads(INDEX.read_text()) if INDEX.exists() else []
    bad = []
    if len(msgs) != len(index):
        bad.append(f"{len(msgs)} messages but {len(index)} index rows")
    for row, m in zip(index, msgs):
        if hashlib.sha256(m["text"].encode("utf-8")).hexdigest() != row["sha256"]:
            bad.append(f"#{row['n']} sha mismatch")
        day = (STORE / row["file"]).read_text(encoding="utf-8")
        if f"===== #{row['n']}  {m['ts']} =====\n{m['text']}\n" not in day:
            bad.append(f"#{row['n']} not verbatim in {row['file']}")
        if any(re.search(p, m["text"]) for p in CREDENTIALS):
            bad.append(f"#{row['n']} contains a credential")
    return bad


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if mode == "--hook":
        try:
            d = json.loads(sys.stdin.read() or "{}")
            prompt = d.get("prompt")
            if isinstance(prompt, str) and not is_harness(prompt):
                msgs = load()
                now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
                if add(msgs, now, prompt):
                    write_all(msgs)
        except Exception as e:  # never block the owner's prompt
            print(f"owner_record: {e}", file=sys.stderr)
        return 0
    if mode == "--transcripts":
        msgs = load()
        new = sum(add(msgs, ts, t) for ts, t in from_transcripts())
        write_all(msgs)
        print(f"owner_record: {new} new, {len(msgs)} total")
        return 0
    bad = check()
    print("owner_record: " + ("OK, %d messages verbatim" % len(load()) if not bad else "; ".join(bad[:10])))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
