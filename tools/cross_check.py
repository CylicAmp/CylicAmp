#!/usr/bin/env python3
"""Ask several AI models the same question; save every answer as your own record.

Why: a single provider can return an edited answer and you cannot see what was
left out. The same question to several independent models makes omissions
visible -- what one leaves out, others include. Every answer is written to
records/cross_check/<timestamp>.json (and .md), so the record is yours, in this
repo, not on any provider's server.

Uses OpenRouter (https://openrouter.ai): one key reaches models from many
providers through one OpenAI-compatible endpoint. Plain Python 3, no packages;
runs on Termux.

    export OPENROUTER_API_KEY=sk-or-...
    python3 tools/cross_check.py "your question"
    python3 tools/cross_check.py -m anthropic/claude-sonnet-4.5 -m openai/gpt-5 "question"
    python3 tools/cross_check.py --list            # model ids available to your key

Each answer records what the response says served it (model name, provider,
system_fingerprint, response id). If any of these differ from the previous
record for the same requested model, the run prints CHANGED SINCE LAST RECORD
and writes it into the record: a renamed or re-routed model shows up in your
own files. A change of weights behind an unchanged name and fingerprint cannot
be seen this way; only weights you hold and hash can rule that out.

Defaults were looked up on 2026-10-02; ids change, `--list` shows the current ones. No system prompt is sent
unless you pass --system, so each model answers with only your words.
"""
import argparse
import datetime
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

API = "https://openrouter.ai/api/v1"
# Each provider's top model on OpenRouter, looked up 2026-10-02 from
# https://openrouter.ai/api/v1/models (466 models listed). Price per million
# tokens, input / output. DeepSeek and Llama publish open weights.
DEFAULT_MODELS = [
    "anthropic/claude-opus-5.5",      # $4 / $20
    "openai/gpt-6.1-sol-pro",         # $2 / $10
    "google/gemini-3.1-pro-preview",  # $2 / $12
    "x-ai/grok-4.7",                  # $2 / $6
    "deepseek/deepseek-v4-pro",       # $0.21 / $0.42  (open weights)
    "meta-llama/llama-4-maverick",    # $0.19 / $0.65  (open weights)
]
OUT = pathlib.Path(__file__).resolve().parent.parent / "records" / "cross_check"


def call(path, key, body=None, timeout=180):
    req = urllib.request.Request(API + path, data=None if body is None else json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def served(d):
    """What actually answered, as the response reports it. An alias such as
    "anthropic/claude-opus-5.5" can be pointed at new weights without notice;
    these fields are what a later record can be compared against."""
    return {"served_by": d.get("model"), "provider": d.get("provider"),
            "system_fingerprint": d.get("system_fingerprint"), "response_id": d.get("id")}


NO_SERVE = {"served_by": None, "provider": None, "system_fingerprint": None, "response_id": None}


def ask(model, question, key, system=None):
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": question}]
    try:
        d = call("/chat/completions", key, {"model": model, "messages": msgs})
        return {"model": model, "answer": d["choices"][0]["message"]["content"], **served(d), "error": None}
    except urllib.error.HTTPError as e:
        return {"model": model, "answer": None, **NO_SERVE,
                "error": f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}"}
    except Exception as e:  # network, timeout, malformed reply
        return {"model": model, "answer": None, **NO_SERVE, "error": repr(e)[:300]}


def last_served(out=None):
    """requested model -> (served_by, provider, system_fingerprint, utc) from the newest earlier record."""
    seen = {}
    for f in sorted((out or OUT).glob("*.json")):
        try:
            rec = json.loads(f.read_text())
        except (OSError, ValueError):
            continue
        for r in rec.get("results", []):
            if r.get("served_by"):
                seen[r["model"]] = (r.get("served_by"), r.get("provider"), r.get("system_fingerprint"), rec.get("utc"))
    return seen


def changes(results, seen):
    """One line per model whose served name, provider or fingerprint differs from the last record."""
    out = []
    for r in results:
        prev = seen.get(r["model"])
        now = (r.get("served_by"), r.get("provider"), r.get("system_fingerprint"))
        if prev and r.get("served_by") and now != prev[:3]:
            out.append(f"{r['model']}: was {prev[:3]} at {prev[3]}, now {now}")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("question", nargs="?")
    ap.add_argument("-m", "--model", action="append", help="model id (repeatable)")
    ap.add_argument("--system", help="optional system prompt, sent identically to every model")
    ap.add_argument("--list", action="store_true", help="list model ids available to your key")
    a = ap.parse_args(argv)
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("Set OPENROUTER_API_KEY first (create one at https://openrouter.ai/keys).")
        return 2
    if a.list:
        for m in sorted(x["id"] for x in call("/models", key)["data"]):
            print(m)
        return 0
    if not a.question:
        ap.error("give a question")
    models = a.model or DEFAULT_MODELS
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    seen = last_served()
    results = []
    for m in models:
        print(f"... {m}", flush=True)
        results.append(ask(m, a.question, key, a.system))
    shifted = changes(results, seen)
    for line in shifted:
        print("CHANGED SINCE LAST RECORD:", line)
    rec = {"utc": stamp, "question": a.question, "system": a.system, "results": results, "changed": shifted}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{stamp}.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
    md = [f"# Cross-check {stamp}", "", f"**Question:** {a.question}", ""]
    if shifted:
        md += ["**Changed since last record:**", ""] + [f"- {x}" for x in shifted] + [""]
    for r in results:
        tag = ", ".join(f"{k}: {r[k]}" for k in ("served_by", "provider", "system_fingerprint") if r[k])
        md += [f"## {r['model']}" + (f" ({tag})" if tag else ""), "",
               r["answer"] if r["answer"] else f"_error: {r['error']}_", ""]
    (OUT / f"{stamp}.md").write_text("\n".join(md))
    print(f"saved records/cross_check/{stamp}.json and .md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
