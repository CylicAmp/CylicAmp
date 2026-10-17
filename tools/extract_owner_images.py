#!/usr/bin/env python3
"""Extract the pictures the owner sent from the Claude Code session transcripts, with the owner_work message number.

The owner_work record keeps the text of every message; pictures live only in the transcripts
(~/.claude/projects/<project>/*.jsonl) and are lost when the session container goes. This writes every owner picture to a
local folder, named <date>_msg<number>_img<k>.<ext>, and prints a table. Nothing is added to git: some pictures are other
people's posts or private, so the owner picks which to publish (copy the chosen file into owner_work/images/).

    python3 tools/extract_owner_images.py                      # -> owner_work/images_all/ (ignored by git)
    python3 tools/extract_owner_images.py --out /some/folder
"""
import argparse
import base64
import datetime as dt
import glob
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent


def message_times():
    rows = []
    for f in sorted(glob.glob(str(ROOT / "owner_work" / "messages" / "*.txt"))):
        for m in re.finditer(r"^===== #(\d+)\s+(\S+) =====$", open(f, encoding="utf-8").read(), re.M):
            rows.append((int(m.group(1)), dt.datetime.fromisoformat(m.group(2).replace("Z", "+00:00"))))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "owner_work" / "images_all"))
    ap.add_argument("--transcripts", default=str(pathlib.Path.home() / ".claude" / "projects" / "*" / "*.jsonl"))
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    msgs = message_times()
    k = 0
    for f in sorted(glob.glob(a.transcripts)):
        for line in open(f, errors="ignore"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            content = d.get("message", {}).get("content") if d.get("type") == "user" else None
            if not isinstance(content, list):
                continue
            for b in content:
                if isinstance(b, dict) and b.get("type") == "image" and b.get("source", {}).get("type") == "base64":
                    ts = dt.datetime.fromisoformat(d["timestamp"].replace("Z", "+00:00"))
                    no, when = min(msgs, key=lambda m: abs((m[1] - ts).total_seconds())) if msgs else (0, ts)
                    ext = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}.get(b["source"].get("media_type"), "bin")
                    k += 1
                    name = f"{d['timestamp'][:10]}_msg{no}_img{k:02d}.{ext}"
                    data = base64.b64decode(b["source"]["data"])
                    (out / name).write_bytes(data)
                    print(f"{name}  {len(data):>8} bytes  sent {d['timestamp']}  nearest message #{no} ({int(abs((when - ts).total_seconds()))} s apart)")
    print(f"{k} pictures written to {out}")


if __name__ == "__main__":
    main()
