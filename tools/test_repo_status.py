"""tools/repo_status.py runs inside this repo and reports branch and commits."""
import subprocess
import sys
import pathlib

TOOL = pathlib.Path(__file__).resolve().parent / "repo_status.py"


def test_runs_and_reports():
    r = subprocess.run([sys.executable, str(TOOL), "2"], capture_output=True, text=True,
                       cwd=TOOL.parent.parent)
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("branch:")
    assert "last 2 commits:" in r.stdout and "author:" in r.stdout
