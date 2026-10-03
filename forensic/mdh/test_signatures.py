"""Signature layer tests with real Ed25519 keys. Run: python3 -m pytest forensic/mdh -q"""
import json

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from forensic.mdh import signatures
from forensic.mdh.pipeline import reconstruct
from forensic.mdh.validate import validate

SRC = "plant-a"


def pubhex(k):
    return k.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw).hex()


ALICE, BOB, MALLORY = (Ed25519PrivateKey.generate() for _ in range(3))
KEYRING = {"alice": {"algorithm": "ed25519", "public_key_hex": pubhex(ALICE)},
           "bob": {"algorithm": "ed25519", "public_key_hex": pubhex(BOB), "revoked": True}}


def line(obj):
    return json.dumps(obj, ensure_ascii=False).encode() + b"\n"


def signed(obj, key=ALICE, kid="alice", src=SRC):
    return signatures.sign_event(obj, key, kid, src)


def run(raw, keyring=KEYRING):
    rec, _ = reconstruct([raw], SRC, keyring=keyring)
    assert validate(rec, raw, keyring) == [], validate(rec, raw, keyring)
    return rec


def sig_of(rec, event_id):
    return next(e["signature"]["state"] for e in rec["events"] if e["event_id"] == event_id)


def state_of(rec, event_id):
    return next(s for s in rec["states"] if any(x.split("#")[0] == event_id for x in s["event_refs"]))


A = {"id": "a", "t": 1, "q": 1}
B = {"id": "b", "t": 2, "q": 2, "parent": "a"}


def test_valid_chain_is_verified():
    rec = run(line(signed(A)) + line(signed(B)))
    assert sig_of(rec, "a") == sig_of(rec, "b") == "SIGNED_VALID"
    assert state_of(rec, "b")["state"] == "VERIFIED"


def test_whitespace_and_key_order_do_not_matter():
    e = signed(A)
    reordered = json.dumps(dict(reversed(list(e.items()))), indent=3).replace("\n", " ").encode() + b"\n"
    assert sig_of(run(reordered), "a") == "SIGNED_VALID"


def test_one_changed_value_breaks_the_signature():
    e = signed(A)
    e["t"] = 1.5
    rec = run(line(e) + line(signed(B)))
    assert sig_of(rec, "a") == "INVALID_SIGNATURE"
    assert state_of(rec, "a")["state"] == "QUARANTINED"
    assert state_of(rec, "a")["certainty_limit"] == 0.0


def test_wrong_key_under_trusted_id_fails():
    rec = run(line(signed(A, key=MALLORY, kid="alice")))
    assert sig_of(rec, "a") == "INVALID_SIGNATURE"


def test_unknown_and_revoked_keys():
    rec = run(line(signed(A, key=MALLORY, kid="mallory")) + line(signed(B, key=BOB, kid="bob")))
    assert sig_of(rec, "a") == "UNTRUSTED_KEY" and sig_of(rec, "b") == "REVOKED_KEY"
    assert all(e["certainty"] <= 0.25 for e in rec["events"])


def test_unsigned_event_blocks_verified():
    rec = run(line(signed(A)) + line(B))
    assert sig_of(rec, "b") == "UNSIGNED"
    s = state_of(rec, "b")
    assert s["state"] == "CANDIDATE" and s["certainty_limit"] == 0.5


def test_signature_copied_to_another_event_fails():
    good = signed(A)
    forged = dict(B, kid="alice", sig=good["sig"])
    assert sig_of(run(line(good) + line(forged)), "b") == "INVALID_SIGNATURE"


def test_signature_from_another_source_fails():
    other = signed(A, src="plant-b")                       # same event, signed for a different source
    assert sig_of(run(line(other)), "a") == "INVALID_SIGNATURE"


def test_swapping_kid_after_signing_fails():
    e = signed(A)
    e["kid"] = "bob"
    kr = dict(KEYRING, bob={"algorithm": "ed25519", "public_key_hex": pubhex(BOB)})
    assert sig_of(run(line(e), keyring=kr), "a") == "INVALID_SIGNATURE"


@pytest.mark.parametrize("bad", ["", "zz", "00" * 63, "00" * 65, 12345])
def test_malformed_signatures(bad):
    e = dict(signed(A), sig=bad)
    assert sig_of(run(line(e)), "a") == "INVALID_SIGNATURE"


def test_validator_rejects_forged_signature_claim():
    raw = line(signed(A, key=MALLORY, kid="alice"))
    rec, _ = reconstruct([raw], SRC, keyring=KEYRING)
    rec["events"][0]["signature"]["state"] = "SIGNED_VALID"      # claim what is not true
    assert any("re-verification gives INVALID_SIGNATURE" in p for p in validate(rec, raw, KEYRING))


def test_validator_rejects_different_keyring():
    raw = line(signed(A))
    rec, _ = reconstruct([raw], SRC, keyring=KEYRING)
    other = {"alice": {"algorithm": "ed25519", "public_key_hex": pubhex(MALLORY)}}
    assert "record was built with a different keyring" in validate(rec, raw, other)


def test_no_keyring_means_no_signature_fields():
    rec, _ = reconstruct([line(A)], SRC)
    assert "signature" not in rec["events"][0] and "keyring_sha256" not in rec["constraints"]


def test_null_verifier_would_fail_these_tests(monkeypatch):
    # a verifier that accepts everything must be caught: tampered input must not come out valid
    class AcceptAll:
        @staticmethod
        def from_public_bytes(b):
            return AcceptAll()

        def verify(self, s, m):
            return None
    monkeypatch.setattr(signatures, "Ed25519PublicKey", AcceptAll)
    e = signed(A)
    e["t"] = 99
    rec, _ = reconstruct([line(e)], SRC, keyring=KEYRING)
    assert rec["events"][0]["signature"]["state"] == "SIGNED_VALID"   # the null verifier lies...
    monkeypatch.undo()
    assert validate(rec, line(e), KEYRING) != []                       # ...and the validator catches it
