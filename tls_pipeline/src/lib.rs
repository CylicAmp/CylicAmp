// TLS pipeline modules:
//   cert_policy  — mTLS client certificate verifier (fingerprint + SAN)
//   identity     — JCS canonicalization + Ed25519 signature verification
//   frame        — zero-copy frame decoder + V1/V2/V3 transducer

pub mod cert_policy;
pub mod frame;
pub mod identity;
