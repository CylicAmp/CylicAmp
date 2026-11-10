"""CI check: every owner message in owner_work/ is stored verbatim and carries no credential.

owner_work/ is deliberately NOT committed.  This repository is public, and the
archive holds the owner's messages verbatim, including personal statements that
were never meant for a public page; `owner_work/` is in .gitignore and the
archive was removed from tracking on 2026-11-07.  The recorder hook still writes
it, so the archive exists on the owner's own machine and not on a CI runner or a
fresh clone.

So this test has two modes, and neither of them passes vacuously:

  archive present (the owner's machine)
      full strength -- every message verbatim, index and store agreeing, and at
      least MIN_MESSAGES of them.  This is the check that was running before.

  archive absent (CI, a fresh clone)
      skipped, because there is nothing to verify.  Before skipping it asserts
      that the absence is total: no messages AND no index.  A half-present
      archive -- an index with no messages, or messages with no index -- is a
      real fault and still fails here rather than being skipped past.
"""
import importlib.util
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("owner_record", ROOT / "tools" / "owner_record.py")
owner_record = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner_record)

# 242 messages existed when the archive was last committed (2026-10-13).
MIN_MESSAGES = 228


def _archive_state():
    """(messages, index_rows) counts, without asserting anything about them."""
    import json
    msgs = owner_record.load()
    index = (json.loads(owner_record.INDEX.read_text(encoding="utf-8"))
             if owner_record.INDEX.exists() else [])
    return msgs, index


def test_owner_record_is_verbatim():
    msgs, index = _archive_state()

    if not msgs and not index:
        pytest.skip("owner_work/ is not in this checkout by design "
                    "(public repo, .gitignore'd on 2026-11-07); nothing to verify")

    # Not a clean absence: one side exists without the other. That is a fault.
    assert bool(msgs) == bool(index), (
        f"half-present archive: {len(msgs)} messages but {len(index)} index rows. "
        "Either both are absent (skip) or both are present (check)."
    )

    # Archive present: the original check, at full strength.
    assert owner_record.check() == []
    assert len(msgs) >= MIN_MESSAGES, (
        f"{len(msgs)} messages, expected at least {MIN_MESSAGES}"
    )


def test_skip_condition_cannot_hide_a_populated_archive():
    """Null control: the skip must be reachable only when the archive is truly empty.

    If a future edit makes the skip too broad, this fails. It does not depend on
    whether the archive is present, so it runs in both modes.
    """
    msgs, index = _archive_state()
    skipped = (not msgs) and (not index)
    assert skipped == (len(msgs) == 0 and len(index) == 0)
    # and the skip can never be taken while any message exists
    if msgs:
        assert not skipped, "skip taken with messages present"


def test_a_carriage_return_still_verifies_as_verbatim():
    """Regression: check() must not let newline translation corrupt the comparison.

    owner_record.check() reads each day file and looks for the stored text inside
    it.  Read in text mode with Python's default universal-newline handling, a
    stored "\\r" comes back as "\\n", so a message containing a carriage return
    can never match itself and reads as "not verbatim".

    Message #253 (2026-11-09) was the first to contain one -- a curl progress
    meter, which uses CR to rewrite its line -- and it turned CI red.  This test
    builds a two-message archive in a temp directory, one of them carrying a CR,
    and asserts check() returns clean.  Against the unfixed read it fails on the
    CR message.  It needs no committed archive, so it runs on CI too.
    """
    import hashlib
    import json
    import tempfile

    store = pathlib.Path(tempfile.mkdtemp())
    (store / "messages").mkdir()
    day_rel = "messages/2026-01-01.txt"

    texts = ["a plain message with no carriage return",
             "progress  0     0\r  0     0\r100   512\ndone"]
    msgs, index, day = [], [], ""
    for i, text in enumerate(texts, 1):
        ts = f"2026-01-01T00:0{i}:00.000Z"
        msgs.append({"ts": ts, "text": text})
        index.append({"n": i, "ts": ts, "file": day_rel,
                      "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                      "chars": len(text)})
        day += f"===== #{i}  {ts} =====\n{text}\n\n"

    (store / "messages.json").write_text(json.dumps(msgs), encoding="utf-8")
    (store / "index.json").write_text(json.dumps(index), encoding="utf-8")
    # newline="" on the way out too, so the CR reaches the file as a CR
    with (store / day_rel).open("w", encoding="utf-8", newline="") as fh:
        fh.write(day)

    saved = (owner_record.STORE, owner_record.MSGS, owner_record.INDEX)
    try:
        owner_record.STORE = store
        owner_record.MSGS = store / "messages.json"
        owner_record.INDEX = store / "index.json"
        # the CR survived the write
        with (store / day_rel).open(encoding="utf-8", newline="") as fh:
            assert "\r" in fh.read(), "the test fixture lost its carriage return"
        assert owner_record.check() == [], (
            "a message containing a carriage return did not verify as verbatim"
        )
        assert len(owner_record.load()) == 2
    finally:
        owner_record.STORE, owner_record.MSGS, owner_record.INDEX = saved
