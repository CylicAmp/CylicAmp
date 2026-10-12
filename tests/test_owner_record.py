"""CI check: every owner message in owner_work/ is stored verbatim and carries no credential."""
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("owner_record", ROOT / "tools" / "owner_record.py")
owner_record = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner_record)


def test_owner_record_is_verbatim():
    assert owner_record.check() == []
    assert len(owner_record.load()) >= 228
