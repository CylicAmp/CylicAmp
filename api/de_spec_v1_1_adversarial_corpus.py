"""
de_spec_v1_1_adversarial_corpus.py

Parser Policy Leak Test Corpus — DE-SPEC v1.1

57 adversarial JSON fixtures organized into fracture vectors.
Each fixture is a dict with the following fields:

  id            : unique string identifier
  category      : fracture vector (GAP-1 / GAP-2 / GAP-3 / GAP-4 / BOUNDARY)
  input         : raw JSON string (what an attacker or non-compliant impl sends)
  expected      : "REJECT" or "ACCEPT"
  exception     : (REJECT only) expected exception class name
  canon         : (ACCEPT only) expected canonical bytes as Python bytes literal
  hash          : (ACCEPT only) expected SHA-256 hex of canonical bytes
  note          : human-readable explanation

REJECT fixtures are the MUST-FAIL suite.
ACCEPT fixtures define the canonical form that any compliant impl must produce.
"""

from __future__ import annotations
from typing import List, Dict, Any


CORPUS: List[Dict[str, Any]] = [

    # =========================================================================
    # GAP-1: Duplicate Key Policy (MUST REJECT)
    # =========================================================================

    {
        "id": "dup-001",
        "category": "GAP-1",
        "input": '{"x": 1, "x": 2}',
        "expected": "REJECT",
        "exception": "DuplicateKeyError",
        "note": "Basic duplicate: last-wins in Python/Rust Value, but v1.1 REJECTS",
    },
    {
        "id": "dup-002",
        "category": "GAP-1",
        "input": '{"a": 1, "b": 2, "a": 3}',
        "expected": "REJECT",
        "exception": "DuplicateKeyError",
        "note": "Duplicate non-adjacent key",
    },
    {
        "id": "dup-003",
        "category": "GAP-1",
        "input": '{"": 1, "": 2}',
        "expected": "REJECT",
        "exception": "DuplicateKeyError",
        "note": "Duplicate empty-string key",
    },
    {
        "id": "dup-004",
        "category": "GAP-1",
        "input": '{"a": 1, "b": {"x": 1, "x": 2}}',
        "expected": "REJECT",
        "exception": "DuplicateKeyError",
        "note": "Duplicate key in nested object",
    },
    {
        "id": "dup-005",
        "category": "GAP-1",
        "input": '{"x": 1, "x": 1}',
        "expected": "REJECT",
        "exception": "DuplicateKeyError",
        "note": "Duplicate with identical values — still REJECT",
    },
    {
        "id": "dup-006",
        "category": "GAP-1",
        "input": '{"a": 1, "b": 2, "c": 3, "b": 4}',
        "expected": "REJECT",
        "exception": "DuplicateKeyError",
        "note": "Triplicate field set, second dup later in sequence",
    },
    {
        "id": "dup-007",
        "category": "GAP-1",
        "input": '[{"x": 1, "x": 2}]',
        "expected": "REJECT",
        "exception": "DuplicateKeyError",
        "note": "Duplicate inside array element",
    },
    {
        "id": "dup-008",
        "category": "GAP-1",
        "input": '{"a": {"b": {"c": 1, "c": 2}}}',
        "expected": "REJECT",
        "exception": "DuplicateKeyError",
        "note": "Deeply nested duplicate",
    },

    # =========================================================================
    # GAP-1 ACCEPT: Case-distinct keys are NOT duplicates
    # =========================================================================

    {
        "id": "dup-accept-001",
        "category": "GAP-1",
        "input": '{"A": 1, "a": 2}',
        "expected": "ACCEPT",
        "canon": b'{"A":1,"a":2}',
        "hash": None,   # computed in test runner
        "note": "Case-distinct keys are different — ACCEPT",
    },
    {
        "id": "dup-accept-002",
        "category": "GAP-1",
        "input": '{"ab": 1, "ba": 2}',
        "expected": "ACCEPT",
        "canon": b'{"ab":1,"ba":2}',
        "hash": None,
        "note": "Anagram keys are different — ACCEPT",
    },

    # =========================================================================
    # GAP-2: Numeric Type Contract — REJECT (floats)
    # =========================================================================

    {
        "id": "num-001",
        "category": "GAP-2",
        "input": '{"f": 100.0}',
        "expected": "REJECT",
        "exception": "FloatNotPermittedError",
        "note": "100.0 is a float literal — REJECT even though integer-valued",
    },
    {
        "id": "num-002",
        "category": "GAP-2",
        "input": '{"f": 1.5}',
        "expected": "REJECT",
        "exception": "FloatNotPermittedError",
        "note": "Non-integer float",
    },
    {
        "id": "num-003",
        "category": "GAP-2",
        "input": '{"f": 0.0}',
        "expected": "REJECT",
        "exception": "FloatNotPermittedError",
        "note": "0.0 is a float literal — REJECT",
    },
    {
        "id": "num-004",
        "category": "GAP-2",
        "input": '{"f": -0.0}',
        "expected": "REJECT",
        "exception": "FloatNotPermittedError",
        "note": "Negative zero float — REJECT",
    },
    {
        "id": "num-005",
        "category": "GAP-2",
        "input": '{"f": 1e10}',
        "expected": "REJECT",
        "exception": "FloatNotPermittedError",
        "note": "Scientific notation is a float literal — REJECT",
    },
    {
        "id": "num-006",
        "category": "GAP-2",
        "input": '{"f": 1.0e0}',
        "expected": "REJECT",
        "exception": "FloatNotPermittedError",
        "note": "Explicit exponent float — REJECT",
    },
    {
        "id": "num-007",
        "category": "GAP-2",
        "input": '{"f": 1.5e2}',
        "expected": "REJECT",
        "exception": "FloatNotPermittedError",
        "note": "1.5e2 = 150.0 — REJECT (float literal)",
    },
    {
        "id": "num-008",
        "category": "GAP-2",
        "input": '{"f": 1.23456789}',
        "expected": "REJECT",
        "exception": "FloatNotPermittedError",
        "note": "Decimal float",
    },
    {
        "id": "num-009",
        "category": "GAP-2",
        "input": '{"f": 1e300}',
        "expected": "REJECT",
        "exception": "FloatNotPermittedError",
        "note": "Float outside i64 range — REJECT at float stage",
    },

    # =========================================================================
    # GAP-2: Numeric Type Contract — REJECT (integer range)
    # =========================================================================

    {
        "id": "num-010",
        "category": "GAP-2",
        "input": '{"n": 9223372036854775808}',
        "expected": "REJECT",
        "exception": "IntegerRangeError",
        "note": "2^63 = i64_MAX + 1 — REJECT (Rust default serde_json fails here too)",
    },
    {
        "id": "num-011",
        "category": "GAP-2",
        "input": '{"n": -9223372036854775809}',
        "expected": "REJECT",
        "exception": "IntegerRangeError",
        "note": "-2^63 - 1 = i64_MIN - 1 — REJECT",
    },
    {
        "id": "num-012",
        "category": "GAP-2",
        "input": '{"n": 99999999999999999999999999999999}',
        "expected": "REJECT",
        "exception": "IntegerRangeError",
        "note": "Arbitrarily large integer — Python accepts, v1.1 REJECTS",
    },
    {
        "id": "num-013",
        "category": "GAP-2",
        "input": '{"n": -99999999999999999999999999999999}',
        "expected": "REJECT",
        "exception": "IntegerRangeError",
        "note": "Arbitrarily large negative — REJECT",
    },

    # =========================================================================
    # GAP-2 ACCEPT: i64 boundary values
    # =========================================================================

    {
        "id": "num-accept-001",
        "category": "GAP-2",
        "input": '{"n": 9223372036854775807}',
        "expected": "ACCEPT",
        "canon": b'{"n":9223372036854775807}',
        "hash": None,
        "note": "2^63 - 1 = i64_MAX — ACCEPT",
    },
    {
        "id": "num-accept-002",
        "category": "GAP-2",
        "input": '{"n": -9223372036854775808}',
        "expected": "ACCEPT",
        "canon": b'{"n":-9223372036854775808}',
        "hash": None,
        "note": "-2^63 = i64_MIN — ACCEPT",
    },
    {
        "id": "num-accept-003",
        "category": "GAP-2",
        "input": '{"n": 0}',
        "expected": "ACCEPT",
        "canon": b'{"n":0}',
        "hash": None,
        "note": "Zero integer — ACCEPT",
    },
    {
        "id": "num-accept-004",
        "category": "GAP-2",
        "input": '{"n": -1}',
        "expected": "ACCEPT",
        "canon": b'{"n":-1}',
        "hash": None,
        "note": "Negative one — ACCEPT",
    },

    # =========================================================================
    # GAP-3: Unicode — REJECT (lone surrogates)
    # =========================================================================

    {
        "id": "uni-001",
        "category": "GAP-3",
        "input": r'{"s": "\uD800"}',
        "expected": "REJECT",
        "exception": "LoneSurrogateError",
        "note": "Lone high surrogate — Python accepts, Rust rejects, v1.1 REJECTS",
    },
    {
        "id": "uni-002",
        "category": "GAP-3",
        "input": r'{"s": "\uDBFF"}',
        "expected": "REJECT",
        "exception": "LoneSurrogateError",
        "note": "Lone high surrogate (max) — REJECT",
    },
    {
        "id": "uni-003",
        "category": "GAP-3",
        "input": r'{"s": "\uDC00"}',
        "expected": "REJECT",
        "exception": "LoneSurrogateError",
        "note": "Lone low surrogate — REJECT",
    },
    {
        "id": "uni-004",
        "category": "GAP-3",
        "input": r'{"s": "\uDFFF"}',
        "expected": "REJECT",
        "exception": "LoneSurrogateError",
        "note": "Lone low surrogate (max) — REJECT",
    },
    {
        "id": "uni-005",
        "category": "GAP-3",
        "input": r'{"s": "\uD800\uD801"}',
        "expected": "REJECT",
        "exception": "LoneSurrogateError",
        "note": "Two consecutive high surrogates (no low) — REJECT",
    },
    {
        "id": "uni-006",
        "category": "GAP-3",
        "input": r'{"s": "abc\uD800def"}',
        "expected": "REJECT",
        "exception": "LoneSurrogateError",
        "note": "Surrogate embedded in valid text — REJECT",
    },
    {
        "id": "uni-007",
        "category": "GAP-3",
        "input": r'{"s": "\uDC00\uD800"}',
        "expected": "REJECT",
        "exception": "LoneSurrogateError",
        "note": "Reversed surrogate order (low then high) — REJECT",
    },
    {
        "id": "uni-008",
        "category": "GAP-3",
        "input": r'{"\uD800": 1}',
        "expected": "REJECT",
        "exception": "LoneSurrogateError",
        "note": "Lone surrogate in key — REJECT",
    },
    {
        "id": "uni-009",
        "category": "GAP-3",
        "input": r'{"a": [1, "\uD800", 2]}',
        "expected": "REJECT",
        "exception": "LoneSurrogateError",
        "note": "Lone surrogate inside array — REJECT",
    },
    {
        "id": "uni-010",
        "category": "GAP-3",
        "input": r'{"outer": {"inner": "\uD800"}}',
        "expected": "REJECT",
        "exception": "LoneSurrogateError",
        "note": "Lone surrogate deeply nested — REJECT",
    },

    # =========================================================================
    # GAP-3 ACCEPT: valid surrogate pair + NFC normalization
    # =========================================================================

    {
        "id": "uni-accept-001",
        "category": "GAP-3",
        "input": r'{"s": "😀"}',   # 😀 = U+1F600
        "expected": "ACCEPT",
        "canon": '{"s":"😀"}'.encode("utf-8"),
        "hash": None,
        "note": "Valid surrogate pair (emoji) — ACCEPT; decodes to U+1F600",
    },
    {
        "id": "uni-accept-002",
        "category": "GAP-3",
        "input": '{"s": "é"}',              # NFD decomposed
        "expected": "ACCEPT",
        "canon": '{"s":"é"}'.encode("utf-8"),  # NFC
        "hash": None,
        "note": "NFD input normalized to NFC in canonical form",
    },
    {
        "id": "uni-accept-003",
        "category": "GAP-3",
        "input": '{"s": "hello"}',
        "expected": "ACCEPT",
        "canon": b'{"s":"hello"}',
        "hash": None,
        "note": "Pure ASCII string — ACCEPT",
    },

    # =========================================================================
    # GAP-4: Canonicalization (key ordering, whitespace stripping)
    # =========================================================================

    {
        "id": "canon-001",
        "category": "GAP-4",
        "input": '{"z": 1, "a": 2}',
        "expected": "ACCEPT",
        "canon": b'{"a":2,"z":1}',
        "hash": None,
        "note": "Keys sorted: a before z",
    },
    {
        "id": "canon-002",
        "category": "GAP-4",
        "input": '{ "b" : 2 , "a" : 1 }',
        "expected": "ACCEPT",
        "canon": b'{"a":1,"b":2}',
        "hash": None,
        "note": "Whitespace stripped in canonical form",
    },
    {
        "id": "canon-003",
        "category": "GAP-4",
        "input": '{"nested": {"z": 1, "a": 2}}',
        "expected": "ACCEPT",
        "canon": b'{"nested":{"a":2,"z":1}}',
        "hash": None,
        "note": "Recursive key sort on nested object",
    },
    {
        "id": "canon-004",
        "category": "GAP-4",
        "input": '{"z": 1, "a": 2}',   # same as canon-001, different whitespace
        "expected": "ACCEPT",
        "canon": b'{"a":2,"z":1}',
        "hash": None,
        "note": "Canonical form is identical regardless of input whitespace",
    },
    {
        "id": "canon-005",
        "category": "GAP-4",
        "input": '{"b": {"z": 9, "a": 0}, "a": 1}',
        "expected": "ACCEPT",
        "canon": b'{"a":1,"b":{"a":0,"z":9}}',
        "hash": None,
        "note": "Two-level recursive sort",
    },

    # =========================================================================
    # BOUNDARY: Valid edge cases
    # =========================================================================

    {
        "id": "edge-001",
        "category": "BOUNDARY",
        "input": '{}',
        "expected": "ACCEPT",
        "canon": b'{}',
        "hash": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
        "note": "Empty object — ACCEPT (locked hash from v1.0 conformance vectors)",
    },
    {
        "id": "edge-002",
        "category": "BOUNDARY",
        "input": '{"k": null}',
        "expected": "ACCEPT",
        "canon": b'{"k":null}',
        "hash": None,
        "note": "Null value — ACCEPT",
    },
    {
        "id": "edge-003",
        "category": "BOUNDARY",
        "input": '{"k": true}',
        "expected": "ACCEPT",
        "canon": b'{"k":true}',
        "hash": None,
        "note": "Boolean true — ACCEPT",
    },
    {
        "id": "edge-004",
        "category": "BOUNDARY",
        "input": '{"k": false}',
        "expected": "ACCEPT",
        "canon": b'{"k":false}',
        "hash": None,
        "note": "Boolean false — ACCEPT",
    },
    {
        "id": "edge-005",
        "category": "BOUNDARY",
        "input": '{"k": ""}',
        "expected": "ACCEPT",
        "canon": b'{"k":""}',
        "hash": None,
        "note": "Empty string value — ACCEPT",
    },
    {
        "id": "edge-006",
        "category": "BOUNDARY",
        "input": '{"": 1}',
        "expected": "ACCEPT",
        "canon": b'{"":1}',
        "hash": None,
        "note": "Empty string key — ACCEPT (single occurrence)",
    },
    {
        "id": "edge-007",
        "category": "BOUNDARY",
        "input": '{"k": [1, 2, 3]}',
        "expected": "ACCEPT",
        "canon": b'{"k":[1,2,3]}',
        "hash": None,
        "note": "Integer array value — ACCEPT",
    },
    {
        "id": "edge-008",
        "category": "BOUNDARY",
        "input": '{"k": []}',
        "expected": "ACCEPT",
        "canon": b'{"k":[]}',
        "hash": None,
        "note": "Empty array value — ACCEPT",
    },
    {
        "id": "edge-009",
        "category": "BOUNDARY",
        "input": '{"a": 1, "b": 2}',
        "expected": "ACCEPT",
        "canon": b'{"a":1,"b":2}',
        "hash": "43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777",
        "note": "Standard two-key object (locked hash from v1.0 conformance vectors)",
    },
    {
        "id": "edge-010",
        "category": "BOUNDARY",
        "input": '{"a": 1, "b": {"c": 2, "d": [3, 4]}}',
        "expected": "ACCEPT",
        "canon": b'{"a":1,"b":{"c":2,"d":[3,4]}}',
        "hash": None,
        "note": "Mixed nested structure — ACCEPT",
    },

    # =========================================================================
    # Cross-implementation trap: inputs that DIVERGE between Python and Rust
    # These are the exact inputs from Divergence Report #1
    # =========================================================================

    {
        "id": "diverge-001",
        "category": "GAP-1",
        "input": '{"x": 1, "x": 2}',   # duplicate of dup-001 — keep for report
        "expected": "REJECT",
        "exception": "DuplicateKeyError",
        "note": "DIVERGENCE: Python last-wins, Rust Value last-wins, Rust struct ERRORS. "
                "v1.1 mandates REJECT (closes divergence by choosing strictest)",
    },
    {
        "id": "diverge-002",
        "category": "GAP-2",
        "input": '{"n": 9223372036854775808}',
        "expected": "REJECT",
        "exception": "IntegerRangeError",
        "note": "DIVERGENCE: Python accepts (arbitrary int), Rust default fails. "
                "v1.1 mandates REJECT (i64 ceiling)",
    },
    {
        "id": "diverge-003",
        "category": "GAP-2",
        "input": '{"f": 100.0}',
        "expected": "REJECT",
        "exception": "FloatNotPermittedError",
        "note": "DIVERGENCE: Python → float(100.0), Rust → Number(f64). "
                "v1.1 mandates REJECT (no float literals permitted)",
    },
    {
        "id": "diverge-004",
        "category": "GAP-3",
        "input": r'{"s": "\uD800"}',
        "expected": "REJECT",
        "exception": "LoneSurrogateError",
        "note": "DIVERGENCE: Python accepts, Rust rejects. "
                "v1.1 mandates REJECT (closes in Rust's direction)",
    },
]
