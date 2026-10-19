"""Run every audit file dated 2026-10-13 or later, so a green CI run means those files' assertions ran.

Until this test existed, the Tests workflow collected only tests/test_*.py: an audit file in math/theorems or math/lemmas was checked
on the machine that wrote it and nowhere else, and a green push said nothing about it (found 2026-10-19 when a pasted review credited
a CI pass for an audit file that CI never executed). Each file is run as a script in its own process; a non-zero exit fails the test.
Files are found by name: a date 2026_10_13 .. 2026_10_31 or 2026_11/2026_12 before the extension, in math/theorems and math/lemmas,
plus the check_*.py scripts next to the dashboards.
"""
import pathlib
import re
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATED = re.compile(r"_2026_(10_(1[3-9]|2\d|3[01])|1[12]_\d\d)")


def audit_files():
    out = []
    for folder in ("math/theorems", "math/lemmas"):
        out += [p for p in (ROOT / folder).glob("*.py") if DATED.search(p.stem)]
    out += list((ROOT / "dashboards").glob("*/check_*.py"))
    return sorted(out)


def run_file(path, timeout=300):
    r = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, timeout=timeout, cwd=ROOT)
    return r.returncode, (r.stderr.strip().splitlines() or [""])[-1]


FILES = audit_files()


def test_the_list_is_not_empty():
    assert len(FILES) >= 50, len(FILES)


def test_the_runner_can_fail(tmp_path):
    bad = tmp_path / "bad.py"
    bad.write_text("assert 1 + 1 == 3\n")
    rc, last = run_file(bad)
    assert rc != 0 and "AssertionError" in last


@pytest.mark.parametrize("path", FILES, ids=lambda p: str(p.relative_to(ROOT)))
def test_audit_file_runs_clean(path):
    rc, last = run_file(path)
    assert rc == 0, last
