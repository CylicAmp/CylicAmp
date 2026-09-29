"""RFC 8785 JSON Canonicalization Scheme (JCS) for the value types MDH emits.

Keys sorted by UTF-16 code units, no insignificant whitespace, strings escaped
per RFC 8785 section 3.2.2.2, numbers in ECMAScript Number.prototype.toString
form (section 3.2.2.3). Non-finite numbers are rejected: JCS has no encoding
for them, and AT-17 requires such output to be refused rather than repaired.
"""
import hashlib
import math
from decimal import Decimal


class CanonicalizationError(ValueError):
    pass


def _es_number(x):
    """ECMAScript Number::toString on the shortest round-trip digits (RFC 8785 3.2.2.3)."""
    if isinstance(x, bool):
        raise CanonicalizationError("bool is not a number")
    if isinstance(x, int):
        if abs(x) > 2 ** 53:
            raise CanonicalizationError(f"integer {x} exceeds IEEE-754 exact range")
        x = float(x)
    if not math.isfinite(x):
        raise CanonicalizationError(f"non-finite number {x!r}")
    if x == 0:
        return "0"
    sign = "-" if x < 0 else ""
    d = Decimal(repr(abs(x)))
    _, dig, exp = d.as_tuple()
    digits = "".join(map(str, dig)).rstrip("0")
    exp += len("".join(map(str, dig))) - len(digits)
    k = len(digits)
    n = exp + k                                   # value = 0.digits * 10**n
    if k <= n <= 21:
        return sign + digits + "0" * (n - k)
    if 0 < n <= 21:
        return sign + digits[:n] + "." + digits[n:]
    if -6 < n <= 0:
        return sign + "0." + "0" * (-n) + digits
    e = n - 1
    mant = digits[0] + ("." + digits[1:] if k > 1 else "")
    return sign + mant + "e" + ("+" if e > 0 else "-") + str(abs(e))


def _es_string(s):
    out = ['"']
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "\b":
            out.append("\\b")
        elif ch == "\f":
            out.append("\\f")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif o < 0x20:
            out.append(f"\\u{o:04x}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _utf16_key(k):
    return k.encode("utf-16-be")


def canonicalize(v):
    """Return the JCS text of v (dict / list / str / int / float / bool / None)."""
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, (int, float)):
        return _es_number(v)
    if isinstance(v, str):
        return _es_string(v)
    if isinstance(v, (list, tuple)):
        return "[" + ",".join(canonicalize(x) for x in v) + "]"
    if isinstance(v, dict):
        for k in v:
            if not isinstance(k, str):
                raise CanonicalizationError(f"non-string key {k!r}")
        items = sorted(v.items(), key=lambda kv: _utf16_key(kv[0]))
        return "{" + ",".join(_es_string(k) + ":" + canonicalize(x) for k, x in items) + "}"
    raise CanonicalizationError(f"unsupported type {type(v).__name__}")


def canonical_sha256(v):
    return hashlib.sha256(canonicalize(v).encode("utf-8")).hexdigest()
