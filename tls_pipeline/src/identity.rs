// identity.rs
//
// Fixes vs. the submitted code:
//   1. canonicalize_identity used serde_json::Serializer directly — this does
//      NOT sort object keys.  JCS (RFC 8785) requires lexicographic key order
//      applied recursively.  Fix: jcs_sort() normalises the Value tree first,
//      then compact-serialises.
//   2. The note about ES6 number formatting: serde_json uses the shortest
//      decimal representation (no trailing zeros), which satisfies JCS for
//      values that round-trip through f64 without loss.  Integral floats like
//      1.0 → "1.0" in serde_json, but JCS wants "1".  We convert f64 that are
//      exact integers to i64 before serialising to match the JCS spec.

use ring::signature::{self, UnparsedPublicKey};
use serde_json::Value;

// ── JCS canonicalization ──────────────────────────────────────────────────────

/// Recursively sort all object keys in lexicographic (Unicode codepoint) order.
/// Array element order is preserved (JCS requirement).
fn jcs_sort(v: Value) -> Value {
    match v {
        Value::Object(map) => {
            let mut keys: Vec<String> = map.keys().cloned().collect();
            keys.sort_unstable();   // lexicographic = Unicode codepoint order
            let mut sorted = serde_json::Map::with_capacity(keys.len());
            for k in keys {
                sorted.insert(k.clone(), jcs_sort(map[&k].clone()));
            }
            Value::Object(sorted)
        }
        Value::Array(arr) => Value::Array(arr.into_iter().map(jcs_sort).collect()),
        Value::Number(n) => {
            // JCS: integral floats must be serialised without decimal point.
            // serde_json emits 1.0 as "1.0"; JCS requires "1".
            if let Some(f) = n.as_f64() {
                if f.fract() == 0.0 && f.abs() < 1e15 {
                    // representable as i64 without loss
                    Value::Number((f as i64).into())
                } else {
                    Value::Number(n)
                }
            } else {
                Value::Number(n)
            }
        }
        scalar => scalar,
    }
}

/// Parse `raw` as JSON, apply JCS key-sort, and serialise to compact bytes.
pub fn canonicalize_identity(raw: &[u8]) -> Result<Vec<u8>, &'static str> {
    let value: Value = serde_json::from_slice(raw).map_err(|_| "ERR_IDENTITY_PARSE")?;
    let canonical = jcs_sort(value);
    serde_json::to_vec(&canonical).map_err(|_| "ERR_JCS_FAIL")
}

// ── Ed25519 signature verification ───────────────────────────────────────────

/// Verify an Ed25519 signature over `canonical` bytes using a 32-byte raw pubkey.
pub fn verify_signature(canonical: &[u8], sig: &[u8], pubkey: &[u8]) -> Result<(), &'static str> {
    let key = UnparsedPublicKey::new(&signature::ED25519, pubkey);
    key.verify(canonical, sig).map_err(|_| "ERR_SIGNATURE_INVALID")
}

// ── Tests ─────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use ring::signature::{Ed25519KeyPair, KeyPair};
    use ring::rand::SystemRandom;

    #[test]
    fn jcs_sorts_top_level_keys() {
        let input = br#"{"z": 1, "a": 2, "m": 3}"#;
        let out = canonicalize_identity(input).unwrap();
        assert_eq!(out, br#"{"a":2,"m":3,"z":1}"#);
    }

    #[test]
    fn jcs_sorts_nested_keys() {
        let input = br#"{"b": {"z": 9, "a": 1}, "a": 0}"#;
        let out = canonicalize_identity(input).unwrap();
        assert_eq!(out, br#"{"a":0,"b":{"a":1,"z":9}}"#);
    }

    #[test]
    fn jcs_preserves_array_order() {
        let input = br#"{"items": [3, 1, 2]}"#;
        let out = canonicalize_identity(input).unwrap();
        assert_eq!(out, br#"{"items":[3,1,2]}"#);
    }

    #[test]
    fn jcs_integral_float_normalised() {
        // 1.0 in JSON must become 1 in JCS output
        let input = br#"{"v": 1.0}"#;
        let out = canonicalize_identity(input).unwrap();
        assert_eq!(out, br#"{"v":1}"#);
    }

    #[test]
    fn jcs_rejects_malformed_json() {
        let result = canonicalize_identity(b"{bad json}");
        assert_eq!(result, Err("ERR_IDENTITY_PARSE"));
    }

    #[test]
    fn ed25519_roundtrip() {
        let rng = SystemRandom::new();
        let pkcs8 = Ed25519KeyPair::generate_pkcs8(&rng).unwrap();
        let kp = Ed25519KeyPair::from_pkcs8(pkcs8.as_ref()).unwrap();

        let msg = b"canonical identity blob";
        let sig = kp.sign(msg);
        let pubkey = kp.public_key().as_ref();

        verify_signature(msg, sig.as_ref(), pubkey).expect("valid signature must verify");
    }

    #[test]
    fn ed25519_wrong_sig_rejected() {
        let rng = SystemRandom::new();
        let pkcs8 = Ed25519KeyPair::generate_pkcs8(&rng).unwrap();
        let kp = Ed25519KeyPair::from_pkcs8(pkcs8.as_ref()).unwrap();

        let msg = b"canonical identity blob";
        let sig = kp.sign(msg);
        let pubkey = kp.public_key().as_ref();

        // Flip one byte of the signature
        let mut bad_sig = sig.as_ref().to_vec();
        bad_sig[0] ^= 0xff;

        let result = verify_signature(msg, &bad_sig, pubkey);
        assert_eq!(result, Err("ERR_SIGNATURE_INVALID"));
    }

    #[test]
    fn ed25519_wrong_message_rejected() {
        let rng = SystemRandom::new();
        let pkcs8 = Ed25519KeyPair::generate_pkcs8(&rng).unwrap();
        let kp = Ed25519KeyPair::from_pkcs8(pkcs8.as_ref()).unwrap();

        let msg = b"canonical identity blob";
        let sig = kp.sign(msg);
        let pubkey = kp.public_key().as_ref();

        let result = verify_signature(b"tampered message", sig.as_ref(), pubkey);
        assert_eq!(result, Err("ERR_SIGNATURE_INVALID"));
    }
}
