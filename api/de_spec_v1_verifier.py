"""
de_spec_v1_verifier.py  —  Implementation B (Independent Verifier)

DE-SPEC v1 §8: Two executions are equivalent iff
  state_hash_A == state_hash_B  AND  transition_hash_A == transition_hash_B.

This module shares ZERO code with de_spec_v1_runner.py (Implementation A).
It reimplements §2 canonicalization and §6 transition independently from
first principles so the equivalence proof is not circular.

Imports: stdlib only (hashlib, json, unicodedata).
No wasmtime. No FastAPI. No shared utilities.

The verifier consumes serialized ExecutionEnvelope dicts and:
  1. Recomputes CANON(input) and H(input) from raw input_obj
  2. Recomputes H(output) from raw output_obj
  3. Recomputes transition_hash via §6 chain
  4. Compares every field against the claimed envelope

A VALID verdict means the transition is cryptographically locked.
A INVALID verdict means the envelope is forged, corrupted, or produced
by a non-compliant implementation.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import unicodedata
from typing import Any, Dict, Optional


# ---------------------------------------------------------------------------
# §2  Independent canonicalization (no shared code with runner)
# ---------------------------------------------------------------------------

def _v_normalize(obj: Any) -> Any:
    """Verifier-side recursive normalization. Must match runner §2 exactly."""
    if isinstance(obj, dict):
        return {_v_normalize(k): _v_normalize(v)
                for k, v in sorted(obj.items(), key=lambda p: str(p[0]))}
    if isinstance(obj, list):
        return [_v_normalize(v) for v in obj]
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    if isinstance(obj, float):
        if obj != obj or obj in (float("inf"), float("-inf")):
            raise ValueError(f"Non-finite float not permitted: {obj!r}")
        if obj.is_integer():
            return int(obj)
    return obj


def v_canon(obj: Any) -> bytes:
    """§2 verifier canonical encoding. Independent of CanonicalSerializer."""
    return json.dumps(
        _v_normalize(obj),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def v_hash(obj: Any) -> str:
    """H(canonical(obj)) — verifier side."""
    return hashlib.sha256(v_canon(obj)).hexdigest()


def v_hash_bytes(b: bytes) -> str:
    """H(raw bytes) — for chain components already in canonical form."""
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------------------
# §6  Independent state transition (no shared code with runner)
# ---------------------------------------------------------------------------

def v_transition(
    prev_state_hash: str,
    input_hash: str,
    engine_id: str,
    runtime_id: str,
    output_hash: str,
) -> str:
    """
    §6: S(n+1) = H(S(n) || H(in) || engine_id || runtime_id || H(out))
    Separator: "||"  — must match runner exactly.
    """
    chain = "||".join([prev_state_hash, input_hash, engine_id, runtime_id, output_hash])
    return hashlib.sha256(chain.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Verification result
# ---------------------------------------------------------------------------

@dataclasses.dataclass(frozen=True)
class VerificationResult:
    valid: bool
    envelope_id: str          # claimed transition_hash (identifier)
    checks: Dict[str, bool]   # per-field pass/fail
    recomputed_transition: str
    failure_reason: Optional[str] = None

    def __str__(self) -> str:
        status = "VALID" if self.valid else f"INVALID: {self.failure_reason}"
        fields = "  ".join(f"{k}={'✓' if v else '✗'}" for k, v in self.checks.items())
        return f"[{status}]  {self.envelope_id[:16]}...  {fields}"


# ---------------------------------------------------------------------------
# Core verifier
# ---------------------------------------------------------------------------

class DESpecV1Verifier:
    """
    Implementation B.

    Usage:
        verifier = DESpecV1Verifier()
        result = verifier.verify(
            envelope=env.as_dict(),
            input_obj=original_input,
            output_obj=original_output,
        )
        assert result.valid
    """

    SERIALIZATION_ID = "de-spec-v1-json-canonical"

    def verify(
        self,
        envelope: Dict[str, str],
        input_obj: Any,
        output_obj: Any,
    ) -> VerificationResult:
        """
        Independently recompute every hash in the envelope and compare.

        Parameters
        ----------
        envelope   : dict with keys matching ExecutionEnvelope fields
        input_obj  : original Python object passed to execute()
        output_obj : original Python object returned by engine
        """
        claimed_transition = envelope.get("transition_hash", "")
        checks: Dict[str, bool] = {}
        failure: Optional[str] = None

        # §2: serialization_id must match the locked identifier
        checks["serialization_id"] = (
            envelope.get("serialization_id") == self.SERIALIZATION_ID
        )

        # §2: Recompute input_hash independently
        recomputed_input_hash = v_hash(input_obj)
        checks["input_hash"] = (recomputed_input_hash == envelope.get("input_hash"))

        # §2: Recompute output_hash independently
        recomputed_output_hash = v_hash(output_obj)
        checks["output_hash"] = (recomputed_output_hash == envelope.get("output_hash"))

        # §6: Recompute transition_hash from its components
        recomputed_transition = v_transition(
            prev_state_hash=envelope.get("state_hash",  ""),
            input_hash=recomputed_input_hash,
            engine_id=envelope.get("engine_id",  ""),
            runtime_id=envelope.get("runtime_id", ""),
            output_hash=recomputed_output_hash,
        )
        checks["transition_hash"] = (recomputed_transition == claimed_transition)

        # §8: All checks must pass for VALID
        all_pass = all(checks.values())
        if not all_pass:
            failed = [k for k, v in checks.items() if not v]
            failure = f"fields failed: {failed}"

        return VerificationResult(
            valid=all_pass,
            envelope_id=claimed_transition,
            checks=checks,
            recomputed_transition=recomputed_transition,
            failure_reason=failure,
        )

    def verify_chain(
        self,
        envelopes: list,
        inputs: list,
        outputs: list,
    ) -> list:
        """
        Verify a sequence of transitions and check chain continuity.
        §6: state_hash[n+1] must equal transition_hash[n].
        """
        if not (len(envelopes) == len(inputs) == len(outputs)):
            raise ValueError("envelopes, inputs, outputs must have equal length")

        results = []
        for i, (env, inp, out) in enumerate(zip(envelopes, inputs, outputs)):
            r = self.verify(env, inp, out)

            # Chain continuity check (for all but the first)
            if i > 0:
                prev_transition = envelopes[i - 1].get("transition_hash", "")
                chain_ok = env.get("state_hash") == prev_transition
                r = dataclasses.replace(
                    r,
                    checks={**r.checks, "chain_continuity": chain_ok},
                    valid=r.valid and chain_ok,
                    failure_reason=(
                        r.failure_reason
                        if not chain_ok
                        else (f"chain broken at position {i}" if not chain_ok else r.failure_reason)
                    ),
                )
            results.append(r)
        return results


# ---------------------------------------------------------------------------
# Conformance vector self-test (run independently of runner)
# ---------------------------------------------------------------------------

def run_conformance_selftest() -> bool:
    """
    Verify the verifier's own canonicalization against the locked vectors.
    Returns True iff all pass.
    """
    from de_spec_v1_conformance_vectors import (
        CANON_VECTORS, STATE_TRANSITION_VECTOR,
        TRANSITION_CHAIN_WITNESS, GENESIS_STATE_HASH,
        CANON_MUST_FAIL,
    )

    ok = True

    for label, obj, expected_canon, expected_hash in CANON_VECTORS:
        c = v_canon(obj)
        h = v_hash_bytes(c)
        if c != expected_canon:
            print(f"  FAIL canon [{label}]: got {c!r}, expected {expected_canon!r}")
            ok = False
        if h != expected_hash:
            print(f"  FAIL hash [{label}]: got {h!r}, expected {expected_hash!r}")
            ok = False

    # State transition vector
    tv = STATE_TRANSITION_VECTOR
    recomputed = v_transition(
        prev_state_hash=tv["prev_state_hash"],
        input_hash=tv["input_hash"],
        engine_id=tv["engine_id"],
        runtime_id=tv["runtime_id"],
        output_hash=tv["output_hash"],
    )
    if recomputed != tv["transition_hash"]:
        print(f"  FAIL transition_hash: got {recomputed!r}, expected {tv['transition_hash']!r}")
        ok = False

    # Witness string
    witness_hash = v_hash_bytes(TRANSITION_CHAIN_WITNESS.encode("utf-8"))
    if witness_hash != tv["transition_hash"]:
        print(f"  FAIL witness: got {witness_hash!r}, expected {tv['transition_hash']!r}")
        ok = False

    # Genesis
    genesis = v_hash_bytes(b"DE-SPEC-V1-GENESIS")
    if genesis != GENESIS_STATE_HASH:
        print(f"  FAIL genesis: got {genesis!r}, expected {GENESIS_STATE_HASH!r}")
        ok = False

    # MUST-FAIL canon inputs
    for label, bad_obj in CANON_MUST_FAIL:
        try:
            v_canon(bad_obj)
            print(f"  FAIL must-fail [{label}]: no exception raised")
            ok = False
        except (ValueError, Exception):
            pass   # correct

    return ok
