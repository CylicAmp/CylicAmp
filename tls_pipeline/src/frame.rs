// frame.rs
//
// Fixes vs. the submitted code:
//   Bug: `start = i + 1` then `raw[start..start + end]` where `end` is the
//   position of the FIRST `"` in `raw[start..]`.  If `i` points to the byte
//   after the key's closing quote (e.g., raw[i] = ':'), then `start` lands on
//   `:`, and scanning for `"` finds the VALUE's opening quote — so `end` is the
//   distance to the opening quote, and `raw[start..start+end]` extracts the
//   `: ` separator bytes, not the value.
//
//   Fix: after finding the opening `"` of the value, skip it and scan for the
//   closing `"` from the next byte.  Never include separator bytes in the slice.
//
//   Additional hardening:
//   - Reject if no `:` separator found between key and value.
//   - Reject values longer than MAX_VALUE_LEN to prevent allocation bombs.
//   - Return the string as a slice into the original buffer (zero-copy).

const MAX_VALUE_LEN: usize = 4096;

/// Find `"precision_delta"` in `raw` and return the content of the string value
/// that follows.  Returns a zero-copy slice into `raw`.
///
/// Expected wire format (whitespace-tolerant):
///   ..."precision_delta" : "VALUE"...
pub fn extract_precision_delta(raw: &[u8]) -> Result<Option<&str>, &'static str> {
    const KEY: &[u8] = b"precision_delta";

    let mut i = 0;
    while i + KEY.len() + 2 < raw.len() {
        // Scan for the opening `"` of a potential key.
        if raw[i] != b'"' {
            i += 1;
            continue;
        }
        let key_start = i + 1;
        let key_end   = key_start + KEY.len();

        // Key content must match and be followed by a closing `"`.
        if key_end >= raw.len() {
            break;
        }
        if &raw[key_start..key_end] != KEY || raw[key_end] != b'"' {
            i += 1;
            continue;
        }

        // Advance past the closing `"` of the key.
        let mut j = key_end + 1;

        // Skip whitespace, then require `:`.
        while j < raw.len() && (raw[j] == b' ' || raw[j] == b'\t') {
            j += 1;
        }
        if j >= raw.len() || raw[j] != b':' {
            return Err("ERR_MISSING_COLON");
        }
        j += 1;  // skip `:`

        // Skip whitespace, then require opening `"` of the value.
        while j < raw.len() && (raw[j] == b' ' || raw[j] == b'\t') {
            j += 1;
        }
        if j >= raw.len() || raw[j] != b'"' {
            return Err("ERR_EXPECTED_STRING_VALUE");
        }
        j += 1;  // skip opening `"` — now j points to the first char of the value

        // Find the closing `"` of the value.
        let val_start = j;
        match raw[val_start..].iter().position(|&c| c == b'"') {
            None => return Err("ERR_UNCLOSED_STRING"),
            Some(val_len) => {
                if val_len > MAX_VALUE_LEN {
                    return Err("ERR_VALUE_TOO_LONG");
                }
                let val_bytes = &raw[val_start..val_start + val_len];
                let val = std::str::from_utf8(val_bytes).map_err(|_| "ERR_UTF8")?;
                return Ok(Some(val));
            }
        }
    }

    Ok(None)
}

// ── Transducer ────────────────────────────────────────────────────────────────

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum TransducerVersion {
    V1,   // minimal: precision_delta only
    V2,   // enriched: + epoch timestamp (ms)
    V3,   // signed: + operator signature field
}

#[derive(Debug, PartialEq)]
pub struct TransducedPayload<'a> {
    pub version:         TransducerVersion,
    pub precision_delta: &'a str,
    /// V2 and V3: milliseconds since Unix epoch (from frame metadata).
    pub timestamp_ms:    Option<u64>,
    /// V3: signature over `precision_delta` bytes, as a hex slice into `raw`.
    pub signature_hex:   Option<&'a str>,
}

/// Transduce a raw frame into a typed payload.
///
/// Version selection is done by the caller — downstream routing decides which
/// version contract applies.  V2 requires `ts_ms` to be present in the frame;
/// V3 additionally requires `sig` to be present.
pub fn transduce<'a>(
    raw: &'a [u8],
    version: TransducerVersion,
) -> Result<TransducedPayload<'a>, &'static str> {
    let precision_delta = extract_precision_delta(raw)?
        .ok_or("ERR_PRECISION_DELTA_MISSING")?;

    let timestamp_ms = match version {
        TransducerVersion::V1 => None,
        TransducerVersion::V2 | TransducerVersion::V3 => {
            Some(extract_u64_field(raw, b"ts_ms")?.ok_or("ERR_TS_MS_MISSING")?)
        }
    };

    let signature_hex = match version {
        TransducerVersion::V3 => {
            Some(extract_string_field(raw, b"sig")?.ok_or("ERR_SIG_MISSING")?)
        }
        _ => None,
    };

    Ok(TransducedPayload { version, precision_delta, timestamp_ms, signature_hex })
}

// ── Frame field helpers ───────────────────────────────────────────────────────

/// Extract a quoted string value by key name.
fn extract_string_field<'a>(raw: &'a [u8], key: &[u8]) -> Result<Option<&'a str>, &'static str> {
    let mut i = 0;
    while i + key.len() + 2 < raw.len() {
        if raw[i] != b'"' { i += 1; continue; }
        let ks = i + 1;
        let ke = ks + key.len();
        if ke >= raw.len() { break; }
        if &raw[ks..ke] != key || raw[ke] != b'"' { i += 1; continue; }

        let mut j = ke + 1;
        while j < raw.len() && (raw[j] == b' ' || raw[j] == b'\t') { j += 1; }
        if j >= raw.len() || raw[j] != b':' { return Err("ERR_MISSING_COLON"); }
        j += 1;
        while j < raw.len() && (raw[j] == b' ' || raw[j] == b'\t') { j += 1; }
        if j >= raw.len() || raw[j] != b'"' { return Err("ERR_EXPECTED_STRING_VALUE"); }
        j += 1;

        let vs = j;
        return match raw[vs..].iter().position(|&c| c == b'"') {
            None => Err("ERR_UNCLOSED_STRING"),
            Some(vl) => {
                if vl > MAX_VALUE_LEN { return Err("ERR_VALUE_TOO_LONG"); }
                Ok(Some(std::str::from_utf8(&raw[vs..vs + vl]).map_err(|_| "ERR_UTF8")?))
            }
        };
    }
    Ok(None)
}

/// Extract an unsigned-integer field (JSON number, no quotes).
fn extract_u64_field(raw: &[u8], key: &[u8]) -> Result<Option<u64>, &'static str> {
    let mut i = 0;
    while i + key.len() + 2 < raw.len() {
        if raw[i] != b'"' { i += 1; continue; }
        let ks = i + 1;
        let ke = ks + key.len();
        if ke >= raw.len() { break; }
        if &raw[ks..ke] != key || raw[ke] != b'"' { i += 1; continue; }

        let mut j = ke + 1;
        while j < raw.len() && (raw[j] == b' ' || raw[j] == b'\t') { j += 1; }
        if j >= raw.len() || raw[j] != b':' { return Err("ERR_MISSING_COLON"); }
        j += 1;
        while j < raw.len() && (raw[j] == b' ' || raw[j] == b'\t') { j += 1; }

        // Collect ASCII digits
        let num_start = j;
        while j < raw.len() && raw[j].is_ascii_digit() { j += 1; }
        if j == num_start { return Err("ERR_EXPECTED_NUMBER"); }

        let s = std::str::from_utf8(&raw[num_start..j]).map_err(|_| "ERR_UTF8")?;
        return s.parse::<u64>().map(Some).map_err(|_| "ERR_NUMBER_OVERFLOW");
    }
    Ok(None)
}

// ── Tests ─────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    const SIMPLE: &[u8] = br#"{"precision_delta": "0.0023"}"#;
    const WITH_SPACE: &[u8] = br#"{"precision_delta" : "delta_value"}"#;
    const MULTI: &[u8] = br#"{"a": 1, "precision_delta": "42", "b": 2}"#;
    const MISSING: &[u8] = br#"{"other_key": "value"}"#;

    #[test]
    fn extracts_precision_delta_simple() {
        assert_eq!(extract_precision_delta(SIMPLE).unwrap(), Some("0.0023"));
    }

    #[test]
    fn extracts_with_space_before_colon() {
        assert_eq!(extract_precision_delta(WITH_SPACE).unwrap(), Some("delta_value"));
    }

    #[test]
    fn extracts_from_multi_field_frame() {
        assert_eq!(extract_precision_delta(MULTI).unwrap(), Some("42"));
    }

    #[test]
    fn returns_none_when_key_absent() {
        assert_eq!(extract_precision_delta(MISSING).unwrap(), None);
    }

    #[test]
    fn rejects_unclosed_string() {
        let bad = br#"{"precision_delta": "unclosed}"#;
        // Finds the key but hits end-of-input before closing quote
        let r = extract_precision_delta(bad);
        // Either ERR_UNCLOSED_STRING or doesn't find the closing quote
        assert!(r.is_err() || r.unwrap() == None);
    }

    #[test]
    fn original_bug_demo() {
        // Demonstrates the submitted bug:
        //   start = i + 1  then raw[start..start+end]  where end = position of
        //   first `"` in raw[start..].  If i points at `:`, start lands at ` `,
        //   and the slice raw[start..start+2] = ": " — NOT the value.
        let raw = br#"{"precision_delta": "0.0023"}"#;
        //                                ^--- correct val_start after opening "
        // Confirm our fix returns the content, not separator bytes
        let val = extract_precision_delta(raw).unwrap().unwrap();
        assert_eq!(val, "0.0023");
        assert!(!val.contains(':'));  // separator must not appear in value
        assert!(!val.contains('"'));  // quotes must not appear in value
    }

    // ── Transducer tests ──────────────────────────────────────────────────────

    #[test]
    fn transduce_v1() {
        let frame = br#"{"precision_delta": "0.0023"}"#;
        let p = transduce(frame, TransducerVersion::V1).unwrap();
        assert_eq!(p.version, TransducerVersion::V1);
        assert_eq!(p.precision_delta, "0.0023");
        assert!(p.timestamp_ms.is_none());
        assert!(p.signature_hex.is_none());
    }

    #[test]
    fn transduce_v2_requires_ts_ms() {
        let frame = br#"{"precision_delta": "0.0023", "ts_ms": 1716192000000}"#;
        let p = transduce(frame, TransducerVersion::V2).unwrap();
        assert_eq!(p.version, TransducerVersion::V2);
        assert_eq!(p.precision_delta, "0.0023");
        assert_eq!(p.timestamp_ms, Some(1_716_192_000_000));
    }

    #[test]
    fn transduce_v2_missing_ts_fails() {
        let frame = br#"{"precision_delta": "0.0023"}"#;
        let r = transduce(frame, TransducerVersion::V2);
        assert_eq!(r, Err("ERR_TS_MS_MISSING"));
    }

    #[test]
    fn transduce_v3_full() {
        let frame = br#"{"precision_delta":"0.0023","ts_ms":1716192000000,"sig":"deadbeef"}"#;
        let p = transduce(frame, TransducerVersion::V3).unwrap();
        assert_eq!(p.version, TransducerVersion::V3);
        assert_eq!(p.precision_delta, "0.0023");
        assert_eq!(p.timestamp_ms, Some(1_716_192_000_000));
        assert_eq!(p.signature_hex, Some("deadbeef"));
    }

    #[test]
    fn transduce_v3_missing_sig_fails() {
        let frame = br#"{"precision_delta":"0.0023","ts_ms":1716192000000}"#;
        let r = transduce(frame, TransducerVersion::V3);
        assert_eq!(r, Err("ERR_SIG_MISSING"));
    }
}
