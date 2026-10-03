"""tools/commit_origin.py: classification rules."""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from commit_origin import classify


def c(an="Michael Song", ae="red3rdeye@gmail.com", ce="red3rdeye@gmail.com", date="2026-10-02T23:00:00+00:00", body="x"):
    return {"an": an, "ae": ae, "ce": ce, "date": date, "body": body}


def test_rules():
    assert classify(c(an="Claude", ae="noreply@anthropic.com")) == "claude-name"
    assert classify(c(body="x\n\nClaude-Session: https://claude.ai/code/session_1")) == "claude-tagged"
    assert classify(c(ce="noreply@github.com")) == "github"
    assert classify(c()) == "claude-window"
    assert classify(c(date="2026-09-01T00:00:00+00:00")) == "owner-or-unknown"
    assert classify(c(an="CylicAmp", date="2026-10-01T18:18:25+00:00")) == "owner-or-unknown"
