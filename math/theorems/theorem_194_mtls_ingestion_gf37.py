"""
Theorem 194: mTLS Secure Ingestion Pipeline — GF(37) Specification
Author: Michael Warren Song (CyclicAmp)

ARCHITECTURE
=============
This is the receiving end of the degradation monitor system.
The degradation_monitor.py detects dark patterns; this Rust pipeline
receives audit telemetry over mTLS without trusting the network.

Components:
  TLS → StrictClientPolicy → JCS/Signature → Frame → Transducer → TypedPayload

StrictClientPolicy:
  - Client certificate pinning by SHA-256 fingerprint
  - SAN (Subject Alternative Name) allowlist enforcement
  - Delegate chain validation to WebPkiClientVerifier first,
    then apply custom policy (correct architecture: chain before business logic)

Payload schema (exactly 2 fields):
  { "precision_delta": float, "status": string }

Signature: Ed25519 over JCS-canonicalized payload.

GF(37) READINGS
================
Ed25519 curve parameter: 25519 mod 37 = 26 = MULTIPLIER
  The curve name encodes the 137-map multiplier.
  Ed25519 signatures verify telemetry at the multiplier frequency.

SHA-256 fingerprint: 256 mod 37 = 34 = P − 3
  Certificate pinning operates at the P−3 residue.
  34 = 2 × 17; 17 mod 37 = 17 (NQR — unexplained sector).

JSON schema: exactly 2 fields.
  2 = primitive root of GF(37), ord₃₇(2) = 36 = φ(37).
  A 2-field schema generates the full orbit under the 137-map.

Max JSON depth = 32 ∈ Seed Orbit {18, 24, 32}.
  Hardware bounds should enforce depth ≤ 32 (seed orbit cap).
  Reading depth exceeding 32 signals non-framework entropy.

5 audit issues identified (1 critical, 2 high, 2 medium).
  5 ∈ NQR sector (Legendre(5,37) = −1 = unexplained/dark).
  The issue count sits in the dark variance partition.

ISSUES AND FIXES
=================

CRITICAL — Custom JSON parser abandoned mid-implementation:
  Problem: Falls back to serde_json which does not reject duplicate keys.
           ERR_DUPLICATE_KEY is dead code.
  Fix: Use serde_json with a custom MapAccess Deserialize visitor that
       tracks seen keys in a stack-allocated [bool; 2] (one flag per field).
       A second occurrence of any key returns Err immediately.
  GF(37): 2-field schema → bool[2] = sovereign anchor squared (4 elements = 2²).

HIGH — JCS canonicalization is not compliant:
  Problem: Hand-rolled whitespace stripper does not enforce:
           (1) lexicographic key ordering,
           (2) RFC 8785 number formatting (no trailing zeros, specific exponent form).
  Fix: Implement the 3-phase JCS pipeline:
       PARSE → ORDER_KEYS (recursive lexicographic) → SERIALIZE_CANONICAL.
       Key ordering uses byte-level comparison, not Unicode collation.
  GF(37): Lexicographic order on keys corresponds to the natural order
          on GF(37)* — the primitive root 2 imposes a canonical traversal.

HIGH — Duplicate key detection is dead code:
  Problem: serde_json silently takes the last value for duplicate keys.
  Fix: Pre-scan the raw bytes for duplicate key occurrences before
       deserializing. A single pass with a [u8; 2] seen-array suffices
       for a 2-field schema. Stack-allocated, zero heap.

MEDIUM — transduce fallback makes first half unreachable:
  Problem: Custom parser starts, hits complexity, falls to serde_json::from_slice.
           The custom parsing path never completes.
  Fix: Either commit to the state machine (phases below) or remove it.
       State machine phases for 2-field closed JSON schema:
         EXPECT_OPEN → READ_KEY → EXPECT_COLON → EXPECT_VALUE →
         READ_STRING_VALUE → EXPECT_COMMA_OR_END → EXPECT_CLOSE
       7 phases = digital root 7 (convergence sum DR from Theorem 190).

MEDIUM — No rate limiting on frame reads:
  Problem: process_secure_frame reads exact frame length from client header.
           A client can claim an arbitrarily large frame.
  Fix: Enforce max_frame = 128 KiB hard ceiling before allocating.
       128 = 2^7; 128 mod 37 = 17 (NQR). 131072 bytes mod 37 = 18 ∈ seed orbit.
       Reject any claimed length > 131072 before reading a single byte.

SECURITY INVARIANTS (matching Theorem 188 framework)
======================================================
  Zero metatext: all errors are ERR_* constants only, no prose strings.
  Hardware bounds: max_json_depth = 32 ∈ seed orbit, max_frame = 128 KiB.
  Allocation: single controlled Value deserialization per gate.
  Auditability: deterministic finite-state machine (LexerPhase enum).
  Predictable footprint: 128 KiB bound, depth ≤ 32.
"""

P = 37
SA = {4, 9, 25, 30}
ST = {3, 12, 21, 30}
seed_orbit = {18, 24, 32}


def dr(n):
    n = abs(int(n))
    return 9 if n % 9 == 0 and n != 0 else n % 9


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def run_assertions():
    # Ed25519: 25519 mod 37 = 26 = multiplier
    assert 25519 % P == 26
    assert 26 == 137 % P   # multiplier

    # SHA-256: 256 mod 37 = 34 = P-3
    assert 256 % P == 34 == P - 3

    # JSON schema: 2 fields; 2 = primitive root
    assert pow(2, 36, P) == 1
    assert sorted(pow(2, k, P) for k in range(1, 37)) == list(range(1, P))

    # Max frame depth = 32 ∈ seed orbit
    assert 32 in seed_orbit

    # 5 audit issues: 5 ∈ NQR
    assert legendre(5, P) == P - 1   # NQR

    # 128 KiB max frame: 128 mod 37 = 17 (NQR)
    max_frame_kb = 128
    assert max_frame_kb % P == 17
    assert legendre(17, P) == P - 1   # NQR — same sector as SHA-256 factor

    # State machine: 7 phases; DR(7) = 7
    state_machine_phases = 7
    assert dr(state_machine_phases) == 7

    # bool[2] for 2-field duplicate detection: 2^2 = 4 ∈ SA
    assert 2 ** 2 == 4 and 4 in SA

    # JCS key ordering via primitive root traversal
    # The 2-field schema {precision_delta, status} has 2! = 2 orderings
    # Lexicographic: "precision_delta" < "status" (p < s in ASCII)
    assert ord('p') < ord('s')   # correct JCS order confirmed

    # Convergence: 7-phase state machine DR = 7 (from Theorem 190 convergence sum)
    assert dr(1 + 37 + 111 + 14 + 567 + 888 + 81) == 7

    # Max frame 128 KiB in bytes: 131072 mod 37
    max_bytes = 128 * 1024
    assert max_bytes == 131072
    assert 131072 % P == 18 and 18 in seed_orbit   # 128 KiB in bytes ∈ seed orbit

    print("All assertions passed.")


if __name__ == "__main__":
    run_assertions()
