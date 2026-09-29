"""Stage 2 extension: Ed25519 signatures on events (who wrote a frame, not just which bytes).

What is signed (defined exactly, so a signature cannot be moved):
    b"mdh-event-v1\\x00" + source_id.encode() + b"\\x00" + JCS(event without "sig")
The signature therefore binds the event's full content (canonical form, so
whitespace or key order in the file does not matter), the key id inside it, and
the source it belongs to. Copying a signature onto another event, another key id
or another source fails verification.

Event fields: "kid" (key id) and "sig" (hex Ed25519 signature, 64 bytes).

Keyring (JSON): {"<kid>": {"algorithm": "ed25519", "public_key_hex": "<32-byte hex>",
                           "revoked": false}}
Only Ed25519 is accepted: one encoding, deterministic signatures, no
signature-malleability variants to reason about.

Signature states:
    SIGNED_VALID       signature verifies under a trusted, unrevoked key
    UNSIGNED           no "sig" field
    UNTRUSTED_KEY      "kid" not in the keyring (or malformed key entry)
    REVOKED_KEY        key present but marked revoked
    INVALID_SIGNATURE  signature malformed or does not verify
A signature proves which key signed. It does not prove the keyholder told the
truth.
"""
import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .jcs import canonicalize

DOMAIN = b"mdh-event-v1\x00"
SIG_STATES = ["SIGNED_VALID", "UNSIGNED", "UNTRUSTED_KEY", "REVOKED_KEY", "INVALID_SIGNATURE"]


def signing_bytes(event_obj, source_id):
    body = {k: v for k, v in event_obj.items() if k != "sig"}
    return DOMAIN + source_id.encode("utf-8") + b"\x00" + canonicalize(body).encode("utf-8")


def sign_event(event_obj, private_key, kid, source_id):
    """Return a copy of event_obj carrying kid and a valid sig (for producers and tests)."""
    e = dict(event_obj)
    e.pop("sig", None)
    e["kid"] = kid
    e["sig"] = private_key.sign(signing_bytes(e, source_id)).hex()
    return e


def keyring_fingerprint(keyring):
    return hashlib.sha256(canonicalize(keyring).encode("utf-8")).hexdigest()


def check(event_obj, source_id, keyring):
    """Return (state, kid) for one event. Never raises on bad input."""
    sig = event_obj.get("sig")
    kid = event_obj.get("kid")
    if sig is None:
        return "UNSIGNED", kid if isinstance(kid, str) else None
    if not isinstance(kid, str) or kid not in keyring:
        return "UNTRUSTED_KEY", kid if isinstance(kid, str) else None
    entry = keyring[kid]
    if not isinstance(entry, dict) or entry.get("algorithm") != "ed25519":
        return "UNTRUSTED_KEY", kid
    if entry.get("revoked"):
        return "REVOKED_KEY", kid
    try:
        pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(entry["public_key_hex"]))
    except (KeyError, ValueError, TypeError):
        return "UNTRUSTED_KEY", kid
    try:
        raw = bytes.fromhex(sig) if isinstance(sig, str) else None
    except ValueError:
        raw = None
    if raw is None or len(raw) != 64:
        return "INVALID_SIGNATURE", kid
    try:
        pub.verify(raw, signing_bytes(event_obj, source_id))
    except InvalidSignature:
        return "INVALID_SIGNATURE", kid
    return "SIGNED_VALID", kid
