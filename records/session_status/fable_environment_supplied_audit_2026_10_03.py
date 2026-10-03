"""Audit of a supplied claim (2026-10-03): "The container runtime binds model availability at
instantiation ... a model like Fable typically requires a dedicated custom environment
profile or an explicit internal routing flag in flag_settings (effortLevel: ultracode)."

VERDICT
  F1 "Binds model availability at instantiation": CONTRADICTED by this session's own record.
     The same session, same environment (env_0148232NweDK6fvitmevBYag), was created on
     claude-sonnet-4-6 and switched to claude-opus-5-5 (user_switched_model).
  F2 Fable is a public model, not an internal one: OpenRouter lists anthropic/claude-fable-5.1
     at $10 / $50 per MTok (fetched 2026-10-03); GitHub announced it generally available in
     Copilot on 2026-09-01. Published Claude Code guides select it with `/model fable` inside
     a running session, no restart.
  F3 effortLevel "ultracode" is, by its name, an effort setting; nothing in the record ties it
     to model routing. Not established.
  F4 Not checked: whether this account's plan includes Fable (guides say it requires data
     retention by default for safety classifiers).
CORRECTION found while checking: tools/cross_check.py listed anthropic/claude-opus-5.5 as
  Anthropic's top model on 2026-10-02. Fable 5.1 sits above it ($10/$50 vs $4/$20); the
  default is now claude-fable-5.1.
"""
import json
import pathlib

rec = json.loads((pathlib.Path(__file__).parent / "2026-10-02T2350Z.json").read_text())
assert rec["configured_model"] == "claude-sonnet-4-6"                       # F1
assert rec["user_switched_model"] == rec["model"] == "claude-opus-5-5"
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools"))
import cross_check
assert "anthropic/claude-fable-5.1" in cross_check.DEFAULT_MODELS
assert "anthropic/claude-opus-5.5" not in cross_check.DEFAULT_MODELS
