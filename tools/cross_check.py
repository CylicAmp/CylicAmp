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

Model ids change; `--list` shows the current ones. No system prompt is sent
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
DEFAULT_MODELS = ["anthropic/claude-sonnet-4.5", "openai/gpt-5", "google/gemini-2.5-pro",
                  "meta-llama/llama-3.3-70b-instruct", "deepseek/deepseek-chat"]
OUT = pathlib.Path(__file__).resolve().parent.parent / "records" / "cross_check"


def call(path, key, body=None, timeout=180):
    req = urllib.request.Request(API + path, data=None if body is None else json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def ask(model, question, key, system=None):
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": question}]
    try:
        d = call("/chat/completions", key, {"model": model, "messages": msgs})
        return {"model": model, "answer": d["choices"][0]["message"]["content"],
                "served_by": d.get("model"), "error": None}
    except urllib.error.HTTPError as e:
        return {"model": model, "answer": None, "served_by": None,
                "error": f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}"}
    except Exception as e:  # network, timeout, malformed reply
        return {"model": model, "answer": None, "served_by": None, "error": repr(e)[:300]}


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
    results = []
    for m in models:
        print(f"... {m}", flush=True)
        results.append(ask(m, a.question, key, a.system))
    rec = {"utc": stamp, "question": a.question, "system": a.system, "results": results}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{stamp}.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
    md = [f"# Cross-check {stamp}", "", f"**Question:** {a.question}", ""]
    for r in results:
        md += [f"## {r['model']}" + (f" (served: {r['served_by']})" if r["served_by"] else ""), "",
               r["answer"] if r["answer"] else f"_error: {r['error']}_", ""]
    (OUT / f"{stamp}.md").write_text("\n".join(md))
    print(f"saved records/cross_check/{stamp}.json and .md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
