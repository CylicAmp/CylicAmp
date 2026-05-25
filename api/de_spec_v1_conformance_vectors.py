"""
de_spec_v1_conformance_vectors.py

DE-SPEC v1 Conformance Test Vectors — frozen at protocol lock.

These are the ground-truth input/output pairs for DE-SPEC v1.
Any compliant implementation MUST reproduce every hash exactly.
These values were computed once from the canonical implementation
and are now hardcoded. They are NOT recomputed from the code under test.

Notation:
  CANON(obj) = CanonicalSerializer.encode(obj)   (§2)
  H(b)       = SHA-256(b), hexdigest             (§1)
  S(n+1)     = H(S(n)||H(in)||engine||runtime||H(out))  (§6)
"""

from __future__ import annotations
from typing import Any, Dict, List, Tuple

# ---------------------------------------------------------------------------
# §2  Canonicalization vectors
# Each entry: (label, input_obj, expected_canon_bytes, expected_hash)
# ---------------------------------------------------------------------------

CANON_VECTORS: List[Tuple[str, Any, bytes, str]] = [
    (
        "empty object",
        {},
        b"{}",
        "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
    ),
    (
        "two keys sorted",
        {"a": 1, "b": 2},
        b'{"a":1,"b":2}',
        "43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777",
    ),
    (
        "sort_keys reversal",
        {"z": 1, "a": 2},           # insertion order irrelevant
        b'{"a":2,"z":1}',
        "c2985c5ba6f7d2a55e768f92490ca09388e95bc4cccb9fdf11b15f4d42f93e73",
    ),
    (
        "float 1.0 collapses to int 1",
        {"v": 1.0},
        b'{"v":1}',
        "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
    ),
    (
        "NFD string normalizes to NFC",
        {"s": "é"},          # decomposed é (U+0065 + U+0301)
        "{\"+s+\":\"+é+\"}".encode().replace(b"+", b""),   # NFC é = \xc3\xa9
        "86028b41ba792eaf82aa26a45b218f6734f7f1096a86f1746c8296e088a0ccb4",
    ),
    (
        "nested dict sort",
        {"nested": {"z": 1, "a": 2}},
        b'{"nested":{"a":2,"z":1}}',
        "872396769f22e9510fb3950e7dab20d79c5301ab12593ffdc76ca26a3656e1a6",
    ),
]

# Correct the NFD vector canonical bytes (set once, not computed):
CANON_VECTORS[4] = (
    "NFD string normalizes to NFC",
    {"s": "é"},
    '{"s":"é"}'.encode("utf-8"),     # NFC precomposed é in UTF-8
    "86028b41ba792eaf82aa26a45b218f6734f7f1096a86f1746c8296e088a0ccb4",
)

# ---------------------------------------------------------------------------
# §1 + §6  State transition vector
# Computed from genesis state; locked here.
# ---------------------------------------------------------------------------

GENESIS_STATE_HASH: str = (
    "13ec9611265450abd4949e46b94ad412"
    "deb44b1f258b6c8668c2ab7112127d7c"
)

STATE_TRANSITION_VECTOR: Dict[str, str] = {
    "prev_state_hash": GENESIS_STATE_HASH,
    "input_obj":       '{"key":"test","n":7}',    # JSON string of canonical input
    "input_hash":      "ec5fdde2c9a7b577ed47a332bc5178ae35796ae8568b465731b8385204d5b1e3",
    "engine_id":       "d10168c65f751c38d0514c6135aa905dba0405c502992ae3baef6b275704c347",
    "runtime_id":      "56704e6c9c102d898108ecfdc94c3ddc40a0510e1565cc7f6501d7930766b206",
    "output_hash":     "435f051d494218f7e0d6d8da8625dfd7996182f821606bcce38aadb84b4eae17",
    "transition_hash": "cf89a22ed5b9c521cfa5c39ef2f21ceaf6fcdf6c79256f6c4735d5512be11c94",
}

# The chain input string that produces transition_hash (§6 separator = "||")
TRANSITION_CHAIN_WITNESS: str = (
    "13ec9611265450abd4949e46b94ad412deb44b1f258b6c8668c2ab7112127d7c"
    "||"
    "ec5fdde2c9a7b577ed47a332bc5178ae35796ae8568b465731b8385204d5b1e3"
    "||"
    "d10168c65f751c38d0514c6135aa905dba0405c502992ae3baef6b275704c347"
    "||"
    "56704e6c9c102d898108ecfdc94c3ddc40a0510e1565cc7f6501d7930766b206"
    "||"
    "435f051d494218f7e0d6d8da8625dfd7996182f821606bcce38aadb84b4eae17"
)

# ---------------------------------------------------------------------------
# §4  MUST-FAIL vectors (nondeterminism injection)
# Each entry: (label, wat_source) — loading MUST raise an error
# ---------------------------------------------------------------------------

MUST_FAIL_VECTORS: List[Tuple[str, str]] = [
    (
        "clock_time_get import",
        '(module (import "env" "clock_time_get" (func (param i64 i64 i32) (result i32)))'
        '  (func (export "run") (param i32) (result i32) (i32.const 0)))',
    ),
    (
        "random_get import",
        '(module (import "env" "random_get" (func (param i32 i32) (result i32)))'
        '  (func (export "run") (param i32) (result i32) (i32.const 0)))',
    ),
    (
        "fd_read (filesystem) import",
        '(module (import "wasi_snapshot_preview1" "fd_read"'
        '           (func (param i32 i32 i32 i32) (result i32)))'
        '  (func (export "run") (param i32) (result i32) (i32.const 0)))',
    ),
    (
        "sock_recv (network) import",
        '(module (import "wasi_snapshot_preview1" "sock_recv"'
        '           (func (param i32 i32 i32 i32 i32) (result i32)))'
        '  (func (export "run") (param i32) (result i32) (i32.const 0)))',
    ),
    (
        "unrecognised import",
        '(module (import "acme" "custom_op" (func (param i32) (result i32)))'
        '  (func (export "run") (param i32) (result i32) (i32.const 0)))',
    ),
    (
        "f32 float opcode",
        '(module (func (export "run") (param i32) (result f32) (f32.const 3.14)))',
    ),
    (
        "f64 float opcode",
        '(module (func (export "run") (param i32) (result f64) (f64.const 2.718)))',
    ),
]

# ---------------------------------------------------------------------------
# §2  MUST-FAIL canonicalization inputs
# ---------------------------------------------------------------------------

CANON_MUST_FAIL: List[Tuple[str, Any]] = [
    ("NaN rejected",       {"v": float("nan")}),
    ("Inf rejected",       {"v": float("inf")}),
    ("-Inf rejected",      {"v": float("-inf")}),
]
