# CLASS: AUDIT
"""
Audit of a screenshot from another tool (2026-10-05, "Build" tab): a "pok_v1"
Ed25519 scheme. Its claims:
  * the signed message is pok_v1|statement on both sides (prove and verify);
  * verify accepts raw 32-byte public-key bytes or a parsed Ed25519PublicKey;
  * a wrong statement, wrong context, bad key or bad signature returns False;
  * n = 10,000: prove 37.6 us, verify 118 us (raw bytes and parsed key alike);
    from_public_bytes about 0-4 us.
The code itself was not supplied and is not in this repository. This file
rebuilds the scheme exactly as described and checks the behaviour claims.

WHAT IT IS: a signature with a domain prefix. "pok_v1|" means a signature made
for this purpose cannot be replayed as a signature on the bare statement or under
another prefix -- the same idea as forensic/mdh/signatures.py's "mdh-event-v1\\x00"
prefix. Despite the name, it is not a zero-knowledge proof of knowledge: it shows
the holder of the private key signed that statement, not that the statement is
true.

MEASURED HERE (this machine, n = 10,000): prove 47.5 us, verify raw 124.7 us,
verify parsed 114.5 us, from_public_bytes 4.8 us -- the same shape as the
screenshot (37.6 / 118 / 118 / 0-4 us).
CHECKED HERE: all four rejection cases return False; raw-bytes and parsed-key
verification agree. Timings are machine-dependent and are measured, not
asserted (verify slower than sign, parse cost small, as claimed).

FALSIFICATION: any assertion below failing.
"""
import time
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

CTX = b"pok_v1"

def prove(sk, statement, ctx=CTX):
    return sk.sign(ctx + b"|" + statement)

def verify(pk, statement, sig, ctx=CTX):
    try:
        if isinstance(pk, (bytes, bytearray)):
            pk = Ed25519PublicKey.from_public_bytes(bytes(pk))
        pk.verify(sig, ctx + b"|" + statement)
        return True
    except (InvalidSignature, ValueError):
        return False

sk = Ed25519PrivateKey.generate()
pk = sk.public_key()
raw = pk.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
st = b"the statement"
sig = prove(sk, st)
assert verify(pk, st, sig) and verify(raw, st, sig)
assert not verify(pk, b"another statement", sig)
assert not verify(pk, st, sig, ctx=b"pok_v2")
assert not verify(Ed25519PrivateKey.generate().public_key(), st, sig)
assert not verify(b"\x00" * 31, st, sig)
assert not verify(pk, st, sig[:-1] + bytes([sig[-1] ^ 1]))
assert not verify(pk, st, sk.sign(st))          # unprefixed signature rejected

def timing(n=10000):
    t = time.perf_counter(); [prove(sk, st) for _ in range(n)]; p = (time.perf_counter() - t) / n
    t = time.perf_counter(); [verify(raw, st, sig) for _ in range(n)]; vr = (time.perf_counter() - t) / n
    t = time.perf_counter(); [verify(pk, st, sig) for _ in range(n)]; vp = (time.perf_counter() - t) / n
    t = time.perf_counter(); [Ed25519PublicKey.from_public_bytes(raw) for _ in range(n)]; f = (time.perf_counter() - t) / n
    return p * 1e6, vr * 1e6, vp * 1e6, f * 1e6

if __name__ == "__main__":
    p, vr, vp, f = timing()
    print(f"prove {p:.1f} us  verify raw {vr:.1f} us  verify parsed {vp:.1f} us  from_public_bytes {f:.2f} us")
    print("all assertions pass")
