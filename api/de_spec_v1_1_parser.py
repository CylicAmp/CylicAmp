"""
de_spec_v1_1_parser.py

DE-SPEC v1.1 — Strict Canonical Parser

Closes the four underspecified surfaces identified in Divergence Report #1:

  GAP-1: Duplicate-key policy → REJECT on first duplicate (No-Repair Rule)
  GAP-2: Numeric type contract → signed 64-bit integers only; floats = parse error
  GAP-3: Unicode contract → strict UTF-8; lone surrogates = parse error
  GAP-4: Canonical form → exact byte-for-byte algorithm locked here

All rules are enforced BEFORE canonicalization.  A parser that silently
repairs any of these conditions violates the No-Repair Rule and MUST NOT
be used as a DE-SPEC v1.1 implementation.

Python implementation notes
---------------------------
- `json.loads` with `object_pairs_hook` → duplicate-key detection
- `json.loads` with `parse_float` → float rejection
- `json.loads` with `parse_int` → i64-range enforcement
- Post-parse surrogate walk → lone surrogate rejection
- `unicodedata.normalize("NFC", ...)` → canonical string form
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from typing import Any

# ---------------------------------------------------------------------------
# DE-SPEC v1.1 Formal Constants
# ---------------------------------------------------------------------------

SPEC_VERSION: str = "de-spec-v1.1"
SERIALIZATION_ID: str = "de-spec-v1.1-json-canonical"

I64_MIN: int = -(2 ** 63)
I64_MAX: int =   2 ** 63 - 1


# ---------------------------------------------------------------------------
# Parse-time rejection hooks  (GAP-1, GAP-2)
# ---------------------------------------------------------------------------

class DESpecParseError(ValueError):
    """Any input that violates the No-Repair Rule at parse time."""

class DuplicateKeyError(DESpecParseError):
    """GAP-1: Input contains a duplicate JSON object key."""

class FloatNotPermittedError(DESpecParseError):
    """GAP-2: Input contains a floating-point literal."""

class IntegerRangeError(DESpecParseError):
    """GAP-2: Integer value is outside the signed 64-bit range."""

class LoneSurrogateError(DESpecParseError):
    """GAP-3: String contains a lone UTF-16 surrogate code point."""


def _hook_reject_duplicates(pairs: list) -> dict:
    """object_pairs_hook: fail on first duplicate key (GAP-1)."""
    seen: set = set()
    result: dict = {}
    for k, v in pairs:
        if k in seen:
            raise DuplicateKeyError(
                f"Duplicate key {k!r} violates No-Repair Rule (GAP-1)"
            )
        seen.add(k)
        result[k] = v
    return result


def _hook_reject_float(s: str) -> float:
    """parse_float: floats are a parse error in v1.1 (GAP-2)."""
    raise FloatNotPermittedError(
        f"Floating-point literal {s!r} not permitted in DE-SPEC v1.1 (GAP-2). "
        "Only JSON integers in signed 64-bit range are allowed."
    )


def _hook_check_int_range(s: str) -> int:
    """parse_int: enforce signed 64-bit range (GAP-2)."""
    n = int(s)
    if not (I64_MIN <= n <= I64_MAX):
        raise IntegerRangeError(
            f"Integer {s!r} is outside signed 64-bit range "
            f"[{I64_MIN}, {I64_MAX}] (GAP-2)"
        )
    return n


# ---------------------------------------------------------------------------
# Post-parse surrogate check  (GAP-3)
# ---------------------------------------------------------------------------

def _check_surrogates(obj: Any, path: str = "") -> None:
    """Walk the parsed object and reject any lone surrogate code point (GAP-3)."""
    if isinstance(obj, str):
        for i, ch in enumerate(obj):
            cp = ord(ch)
            if 0xD800 <= cp <= 0xDFFF:
                raise LoneSurrogateError(
                    f"Lone surrogate U+{cp:04X} at position {i} in {path!r} (GAP-3). "
                    "DE-SPEC v1.1 requires strict UTF-8 — surrogates are not scalar values."
                )
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _check_surrogates(k, path=f"{path}/{k!r}[key]")
            _check_surrogates(v, path=f"{path}/{k!r}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            _check_surrogates(item, path=f"{path}[{i}]")


# ---------------------------------------------------------------------------
# GAP-4: Canonical form (exact algorithm)
# ---------------------------------------------------------------------------

def _canonicalize(obj: Any) -> Any:
    """
    Recursive canonical normalization.

    Rules (in application order):
      1. dict  → keys sorted lexicographically by NFC-normalized key string;
                 values normalized recursively
      2. list  → elements normalized recursively; ORDER PRESERVED (caller must order)
      3. str   → unicodedata.normalize("NFC", value)
      4. float → prohibited; must have been rejected at parse time
      5. int   → unchanged (already i64-range-checked)
      6. None, bool → unchanged
    """
    if isinstance(obj, dict):
        return {
            _canonicalize(k): _canonicalize(v)
            for k, v in sorted(obj.items(), key=lambda p: _canonicalize(p[0]))
        }
    if isinstance(obj, list):
        return [_canonicalize(v) for v in obj]
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    if isinstance(obj, float):
        # Should never reach here after parse-time rejection, but guard anyway
        raise FloatNotPermittedError(
            f"Float {obj!r} in canonicalization — parse stage did not enforce GAP-2"
        )
    return obj   # int, bool, None


def _encode_canonical(obj: Any) -> bytes:
    """Produce the canonical byte string (UTF-8, no BOM, no whitespace)."""
    return json.dumps(
        _canonicalize(obj),
        sort_keys=False,     # already sorted by _canonicalize
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse(text: str) -> Any:
    """
    DE-SPEC v1.1 strict parse.

    Accepts a JSON text string and returns the validated Python object.
    Raises a DESpecParseError subclass on any violation.

    Enforcement order (matches No-Repair Rule §2 priority):
      1. Float rejection (parse_float hook — fires during tokenization)
      2. Integer range (parse_int hook — fires during tokenization)
      3. Duplicate key rejection (object_pairs_hook — fires per object)
      4. Lone surrogate rejection (post-parse walk)
    """
    obj = json.loads(
        text,
        parse_float=_hook_reject_float,
        parse_int=_hook_check_int_range,
        object_pairs_hook=_hook_reject_duplicates,
    )
    _check_surrogates(obj)
    return obj


def canonical_bytes(obj: Any) -> bytes:
    """
    Return the DE-SPEC v1.1 canonical byte representation of a validated object.
    Input MUST have been produced by parse() — no raw Python dicts from other sources.
    """
    return _encode_canonical(obj)


def canonical_hash(obj: Any) -> str:
    """SHA-256 of canonical_bytes(obj). Hexdigest."""
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def parse_and_hash(text: str) -> tuple[Any, str]:
    """
    Convenience: parse + hash in one call.
    Returns (validated_obj, canonical_hash_hex).
    Raises DESpecParseError on any violation.
    """
    obj = parse(text)
    return obj, canonical_hash(obj)
