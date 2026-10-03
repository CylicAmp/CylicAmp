"""Offline tests for tools/cross_check.py: served-model fields and change detection."""
import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cross_check as cc


def test_served_fields():
    d = {"id": "gen-1", "model": "x/m-2026-10-01", "provider": "P", "system_fingerprint": "fp1"}
    assert cc.served(d) == {"served_by": "x/m-2026-10-01", "provider": "P",
                            "system_fingerprint": "fp1", "response_id": "gen-1"}
    assert cc.served({}) == cc.NO_SERVE


def test_change_detected(tmp_path):
    old = {"utc": "20261001T000000Z", "results": [
        {"model": "x/m", "served_by": "x/m-a", "provider": "P", "system_fingerprint": "fp1"}]}
    (tmp_path / "20261001T000000Z.json").write_text(json.dumps(old))
    seen = cc.last_served(tmp_path)
    same = [{"model": "x/m", "served_by": "x/m-a", "provider": "P", "system_fingerprint": "fp1"}]
    moved = [{"model": "x/m", "served_by": "x/m-b", "provider": "P", "system_fingerprint": "fp2"}]
    failed = [{"model": "x/m", "served_by": None, "provider": None, "system_fingerprint": None}]
    new = [{"model": "y/n", "served_by": "y/n-a", "provider": "Q", "system_fingerprint": None}]
    assert cc.changes(same, seen) == []
    assert len(cc.changes(moved, seen)) == 1 and "x/m-b" in cc.changes(moved, seen)[0]
    assert cc.changes(failed, seen) == []
    assert cc.changes(new, seen) == []
