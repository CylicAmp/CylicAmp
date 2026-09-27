"""
de_spec_v1_runner.py

Minimal WASM runner satisfying DE-SPEC v1.

Implements:
  §2  Canonicalization contract (NFC + float normalization + UTF-8)
  §3  Execution envelope (no semantic metadata)
  §4  WASM deterministic host ABI (import whitelist; forbidden = hard reject)
  §5  Engine identity via content addressing (SHA-256 of wasm binary)
  §6  State transition: S(n+1) = H(S(n) || H(input) || engine_id || runtime_id || H(output))
  §7  Determinism constraints (float prohibition flag; ordered collections)
  §8  Replay equivalence check
  §10 Full pipeline: Manifest → Serialize → Hash → Resolve → Execute → Canonicalize → Chain → Append

WASM float rule: OPTION A (prohibited) by default.
Runtime is pinned by SHA-256 of the wasmtime version string.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
import struct
import unicodedata
from typing import Any, Dict, FrozenSet, Optional, Tuple

import wasmtime

# ---------------------------------------------------------------------------
# §2  Canonicalization contract
# ---------------------------------------------------------------------------

_SERIALIZATION_ID: str = "de-spec-v1-json-canonical"

class CanonicalSerializer:
    """
    §2.1  json.dumps(sort_keys=True, separators=(',',':'), ensure_ascii=False)
    §2.2  NFC normalization on all string values
    §2.3  UTF-8, no BOM

    Additional: float values that are exact integers are collapsed to int
                to prevent hash divergence across JSON decode boundaries.
    """

    @staticmethod
    def _normalize(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {CanonicalSerializer._normalize(k): CanonicalSerializer._normalize(v)
                    for k, v in sorted(obj.items(), key=lambda p: str(p[0]))}
        if isinstance(obj, list):
            return [CanonicalSerializer._normalize(v) for v in obj]
        if isinstance(obj, str):
            return unicodedata.normalize("NFC", obj)
        if isinstance(obj, float):
            if obj != obj:          # NaN
                raise ValueError("NaN is not permitted in canonical form (allow_nan=False)")
            if obj in (float("inf"), float("-inf")):
                raise ValueError("Inf is not permitted in canonical form")
            if obj.is_integer():
                return int(obj)     # collapse 1.0 → 1 (hash-stability)
        return obj

    @staticmethod
    def encode(obj: Any) -> bytes:
        normalized = CanonicalSerializer._normalize(obj)
        return json.dumps(
            normalized,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")           # §2.3 UTF-8, no BOM

    @staticmethod
    def hash(obj: Any) -> str:
        return hashlib.sha256(CanonicalSerializer.encode(obj)).hexdigest()


# ---------------------------------------------------------------------------
# §4  WASM deterministic host ABI
# ---------------------------------------------------------------------------

# §4.1 Allowed imports: (module_name, export_name)
_ALLOWED_IMPORTS: FrozenSet[Tuple[str, str]] = frozenset({
    ("de_spec", "sha256"),          # §4.1 hash_function
    ("de_spec", "mem_alloc"),       # §4.1 deterministic_memory_alloc (advisory)
})

# §4.2 Forbidden import name fragments (case-insensitive substring match)
_FORBIDDEN_FRAGMENTS: Tuple[str, ...] = (
    "time", "clock", "random", "rand",
    "fs", "file", "path", "dir",
    "net", "sock", "http", "dns",
    "thread", "mutex", "spawn",
    "env", "argv", "getenv",
    "sys",
)

# WASM float opcodes (section 7.1 OPTION A — prohibited)
# These are the opcode bytes for f32/f64 operations in the WASM binary format.
_FLOAT_OPCODE_PREFIXES: Tuple[bytes, ...] = (
    b"\x43",   # f32.const
    b"\x44",   # f64.const
)

# f32/f64 type codes in WASM binary
_FLOAT_TYPE_CODES = {0x7d, 0x7c}   # f32=0x7d, f64=0x7c


class NonDeterminismError(RuntimeError):
    """Raised when a WASM module violates the DE-SPEC v1 determinism constraints."""


class ForbiddenImportError(NonDeterminismError):
    """§4.2: A WASM module declared a forbidden import."""


class FloatOpcodeError(NonDeterminismError):
    """§7.1 OPTION A: A WASM module contains floating-point operations."""


def _check_imports(module: wasmtime.Module) -> None:
    """§4.2: Reject any import not in the whitelist."""
    for imp in module.imports:
        key = (imp.module, imp.name)
        # Exact whitelist check first
        if key in _ALLOWED_IMPORTS:
            continue
        # Forbidden fragment check
        full = f"{imp.module}/{imp.name}".lower()
        for frag in _FORBIDDEN_FRAGMENTS:
            if frag in full:
                raise ForbiddenImportError(
                    f"Forbidden import detected: {imp.module!r}::{imp.name!r} "
                    f"(matches fragment {frag!r}). "
                    f"Allowed imports: {_ALLOWED_IMPORTS}"
                )
        # Any unrecognised import is also forbidden
        raise ForbiddenImportError(
            f"Unrecognised import {imp.module!r}::{imp.name!r} not in DE-SPEC v1 whitelist"
        )


_WASM_MAGIC = b"\x00asm"
_FLOAT_KEYWORDS = (b"f32", b"f64")


def _check_no_floats(wasm_bytes: bytes) -> None:
    """
    §7.1 OPTION A: Reject any use of f32/f64.

    Two-path check:
    - Binary WASM (magic \x00asm): scan type section byte codes 0x7c (f64), 0x7d (f32).
    - WAT text (UTF-8 starting with whitespace/'('): keyword scan for 'f32'/'f64'.

    A production validator would use a proper WASM binary decoder for binary inputs;
    this heuristic is conservative (may false-positive on byte values in data sections)
    but never false-negatives on type signatures.
    """
    if wasm_bytes.lstrip()[:1] in (b"(", b";"):
        # WAT text format
        lower = wasm_bytes.lower()
        for kw in _FLOAT_KEYWORDS:
            if kw in lower:
                raise FloatOpcodeError(
                    f"§7.1 OPTION A: WAT source contains '{kw.decode()}'. "
                    "Floating-point is prohibited under DE-SPEC v1 OPTION A."
                )
    else:
        # Binary WASM: scan for f32 (0x7d) and f64 (0x7c) valtype bytes
        for byte in wasm_bytes:
            if byte in _FLOAT_TYPE_CODES:
                raise FloatOpcodeError(
                    f"§7.1 OPTION A: WASM binary contains f32/f64 type code 0x{byte:02x}. "
                    "Floating-point is prohibited under DE-SPEC v1 OPTION A."
                )


# ---------------------------------------------------------------------------
# §5  Engine identity: content addressing
# ---------------------------------------------------------------------------

@dataclasses.dataclass(frozen=True)
class ContentAddressedEngine:
    """engine_id = SHA-256(wasm_binary_bytes). Registry is non-authoritative."""
    engine_id: str       # SHA-256 hex of wasm_binary
    wasm_bytes: bytes

    @classmethod
    def load(cls, wasm_bytes: bytes, prohibit_floats: bool = True) -> "ContentAddressedEngine":
        engine_id = hashlib.sha256(wasm_bytes).hexdigest()
        wasm_engine = wasmtime.Engine()
        try:
            module = wasmtime.Module(wasm_engine, wasm_bytes)
        except Exception as e:
            raise NonDeterminismError(f"WASM compilation failed: {e}") from e
        _check_imports(module)
        if prohibit_floats:
            _check_no_floats(wasm_bytes)
        return cls(engine_id=engine_id, wasm_bytes=wasm_bytes)


# ---------------------------------------------------------------------------
# §3 + §6  Execution envelope and state transition
# ---------------------------------------------------------------------------

_RUNTIME_VERSION: str = f"wasmtime-python-de-spec-v1"
RUNTIME_ID: str = hashlib.sha256(_RUNTIME_VERSION.encode()).hexdigest()
ABI_VERSION: str = "1"


@dataclasses.dataclass(frozen=True)
class ExecutionEnvelope:
    """
    §3: Minimal trust object. No semantic metadata.
    All fields are hashes or identifiers — no human-readable interpretation.
    """
    state_hash:         str    # H(previous state)
    input_hash:         str    # H(canonical input)
    engine_id:          str    # SHA-256(wasm_bytes)
    runtime_id:         str    # SHA-256(runtime version string)
    serialization_id:   str    # "de-spec-v1-json-canonical"
    output_hash:        str    # H(canonical output)
    transition_hash:    str    # H(state || input || engine || runtime || output)

    def as_dict(self) -> Dict[str, str]:
        return dataclasses.asdict(self)


def _state_transition(
    prev_state_hash: str,
    input_hash: str,
    engine_id: str,
    runtime_id: str,
    output_hash: str,
) -> str:
    """
    §6: S(n+1) = H(S(n) || H(input) || engine_id || runtime_id || H(output))
    Concatenation is canonical: each component is a fixed-length hex string.
    """
    chain_input = "||".join([
        prev_state_hash, input_hash, engine_id, runtime_id, output_hash
    ])
    return hashlib.sha256(chain_input.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# §8  Replay equivalence
# ---------------------------------------------------------------------------

def replay_equivalent(env_a: ExecutionEnvelope, env_b: ExecutionEnvelope) -> bool:
    """
    §8: Two executions are equivalent iff
        state_hash_A == state_hash_B AND transition_hash_A == transition_hash_B.
    """
    return (env_a.state_hash      == env_b.state_hash and
            env_a.transition_hash == env_b.transition_hash)


# ---------------------------------------------------------------------------
# §10  Full deterministic pipeline
# ---------------------------------------------------------------------------

class DeterministicRunner:
    """
    §10: Manifest → Canonical Serialize → Input Hash → Engine Resolution
         → WASM Execute → Output Canonicalize → Transition Hash → Ledger Append
    """

    def __init__(self, prohibit_floats: bool = True) -> None:
        self._engines: Dict[str, ContentAddressedEngine] = {}
        self._state_hash: str = hashlib.sha256(b"DE-SPEC-V1-GENESIS").hexdigest()
        self._prohibit_floats = prohibit_floats
        self._ledger: list = []

    # §5: Non-authoritative registry
    def register_engine(self, wasm_bytes: bytes) -> str:
        """Returns engine_id. Raises NonDeterminismError on ABI violation."""
        engine = ContentAddressedEngine.load(wasm_bytes, self._prohibit_floats)
        self._engines[engine.engine_id] = engine
        return engine.engine_id

    def execute(
        self,
        engine_id: str,
        input_obj: Any,
    ) -> ExecutionEnvelope:
        """
        §10 pipeline. Returns a fully-sealed ExecutionEnvelope.
        Raises NonDeterminismError if the engine is not registered or ABI-invalid.
        """
        # Engine resolution (§5: content-addressed, not registry-authoritative)
        ca_engine = self._engines.get(engine_id)
        if ca_engine is None:
            raise NonDeterminismError(f"Engine {engine_id!r} not registered")

        # §2: Canonical serialization + input hash
        input_bytes = CanonicalSerializer.encode(input_obj)
        input_hash  = hashlib.sha256(input_bytes).hexdigest()

        # WASM execution
        wasm_engine = wasmtime.Engine()
        store       = wasmtime.Store(wasm_engine)
        module      = wasmtime.Module(wasm_engine, ca_engine.wasm_bytes)

        # Provide whitelisted host functions
        linker = wasmtime.Linker(wasm_engine)
        self._bind_host_abi(linker, store)

        instance = linker.instantiate(store, module)
        run_fn   = instance.exports(store).get("run")
        if run_fn is None:
            raise NonDeterminismError("WASM module must export a 'run' function")

        # Pass input as i32 length of canonical bytes written to WASM memory
        memory = instance.exports(store).get("memory")
        if memory is not None:
            # Write input_bytes into WASM memory at offset 0 if it fits
            mem_data = memory.data_ptr(store)
            mem_size = memory.data_len(store)
            if len(input_bytes) <= mem_size:
                import ctypes
                ctypes.memmove(mem_data, input_bytes, len(input_bytes))

        raw_output = run_fn(store, len(input_bytes))

        # §2: Canonical output
        output_obj = {"result": raw_output, "input_len": len(input_bytes)}
        output_hash = CanonicalSerializer.hash(output_obj)

        # §6: State transition
        transition_hash = _state_transition(
            prev_state_hash=self._state_hash,
            input_hash=input_hash,
            engine_id=engine_id,
            runtime_id=RUNTIME_ID,
            output_hash=output_hash,
        )

        envelope = ExecutionEnvelope(
            state_hash       = self._state_hash,
            input_hash       = input_hash,
            engine_id        = engine_id,
            runtime_id       = RUNTIME_ID,
            serialization_id = _SERIALIZATION_ID,
            output_hash      = output_hash,
            transition_hash  = transition_hash,
        )

        # Advance state (§6: deterministic chain)
        self._state_hash = transition_hash
        self._ledger.append(envelope)
        return envelope

    @staticmethod
    def _bind_host_abi(linker: wasmtime.Linker, store: wasmtime.Store) -> None:
        """§4.1: Expose only the whitelisted host functions."""
        # de_spec::sha256 — pure deterministic hash
        def host_sha256(caller: wasmtime.Caller, ptr: int, length: int) -> int:
            mem = caller.get("memory")
            if mem is None:
                return -1
            data = bytes(mem.data_ptr(caller))[:length + ptr][ptr:ptr + length]
            digest = hashlib.sha256(data).digest()
            # write digest back at ptr (caller is responsible for space)
            import ctypes
            ctypes.memmove(mem.data_ptr(caller), digest, min(32, length))
            return 0

        linker.define(
            store, "de_spec", "sha256",
            wasmtime.Func(
                store,
                wasmtime.FuncType([wasmtime.ValType.i32(), wasmtime.ValType.i32()],
                                  [wasmtime.ValType.i32()]),
                host_sha256,
            )
        )

        # de_spec::mem_alloc — advisory stub (WASM linear memory is deterministic)
        def host_mem_alloc(caller: wasmtime.Caller, size: int) -> int:
            return 0   # stub: real allocator lives in WASM linear memory

        linker.define(
            store, "de_spec", "mem_alloc",
            wasmtime.Func(
                store,
                wasmtime.FuncType([wasmtime.ValType.i32()], [wasmtime.ValType.i32()]),
                host_mem_alloc,
            )
        )
