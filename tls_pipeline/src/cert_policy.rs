// cert_policy.rs
//
// Fixes vs. the submitted code:
//   1. Wrong trait signature: submitted used `certs: &[CertificateDer]` + `_sni`.
//      Correct: end_entity + intermediates + UnixTime.
//   2. Missing sha256 helper: was called but never defined.
//   3. Missing Debug impl: required by ClientCertVerifier bounds.
//   4. Missing required methods: verify_tls12_signature, verify_tls13_signature,
//      supported_verify_schemes.
//   5. HandshakeSignatureValid lives in rustls::client::danger, not top-level.
//   6. extract_san error type must be TlsError, not a bare string.

use std::fmt;

use ring::digest::{digest, SHA256};
use rustls::client::danger::HandshakeSignatureValid;
use rustls::pki_types::{CertificateDer, UnixTime};
use rustls::server::danger::{ClientCertVerified, ClientCertVerifier};
use rustls::{DigitallySignedStruct, DistinguishedName, Error as TlsError, SignatureScheme};
use x509_parser::prelude::*;

// ── Helpers ───────────────────────────────────────────────────────────────────

fn sha256_cert(der: &[u8]) -> [u8; 32] {
    let d = digest(&SHA256, der);
    let mut out = [0u8; 32];
    out.copy_from_slice(d.as_ref());
    out
}

fn extract_san(cert_der: &[u8]) -> Result<Vec<String>, TlsError> {
    let (_, cert) = X509Certificate::from_der(cert_der)
        .map_err(|_| TlsError::General("ERR_CERT_PARSE".into()))?;

    let mut sans = Vec::new();
    if let Ok(Some(ext)) = cert.subject_alternative_name() {
        for name in &ext.value.general_names {
            let s = match name {
                GeneralName::DNSName(dns)    => dns.to_string(),
                GeneralName::RFC822Name(e)   => e.to_string(),
                GeneralName::URI(uri)        => uri.to_string(),
                _                            => continue,
            };
            sans.push(s);
        }
    }
    Ok(sans)
}

// ── StrictClientPolicy ────────────────────────────────────────────────────────

pub struct StrictClientPolicy {
    pub allowed_sans: Vec<String>,
    pub pinned_fingerprints: Vec<[u8; 32]>,   // SHA-256 of DER bytes
}

impl fmt::Debug for StrictClientPolicy {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("StrictClientPolicy")
            .field("allowed_sans", &self.allowed_sans)
            .field("pinned_count", &self.pinned_fingerprints.len())
            .finish()
    }
}

impl ClientCertVerifier for StrictClientPolicy {
    fn root_hint_subjects(&self) -> &[DistinguishedName] {
        &[]
    }

    fn offer_client_auth(&self) -> bool {
        true
    }

    fn client_auth_mandatory(&self) -> bool {
        true
    }

    fn verify_client_cert(
        &self,
        end_entity: &CertificateDer<'_>,
        _intermediates: &[CertificateDer<'_>],
        _now: UnixTime,
    ) -> Result<ClientCertVerified, TlsError> {
        // 1. Fingerprint pinning
        let fp = sha256_cert(end_entity.as_ref());
        if !self.pinned_fingerprints.iter().any(|p| *p == fp) {
            return Err(TlsError::General("ERR_CERT_FINGERPRINT_REJECTED".into()));
        }

        // 2. SAN allowlist
        let sans = extract_san(end_entity.as_ref())?;
        if !sans.iter().any(|san| self.allowed_sans.contains(san)) {
            return Err(TlsError::General("ERR_SAN_NOT_ALLOWED".into()));
        }

        Ok(ClientCertVerified::assertion())
    }

    // Delegate TLS 1.2 / 1.3 signature verification to the ring crypto provider.
    fn verify_tls12_signature(
        &self,
        message: &[u8],
        cert: &CertificateDer<'_>,
        dss: &DigitallySignedStruct,
    ) -> Result<HandshakeSignatureValid, TlsError> {
        rustls::crypto::verify_tls12_signature(
            message,
            cert,
            dss,
            &rustls::crypto::ring::default_provider().signature_verification_algorithms,
        )
    }

    fn verify_tls13_signature(
        &self,
        message: &[u8],
        cert: &CertificateDer<'_>,
        dss: &DigitallySignedStruct,
    ) -> Result<HandshakeSignatureValid, TlsError> {
        rustls::crypto::verify_tls13_signature(
            message,
            cert,
            dss,
            &rustls::crypto::ring::default_provider().signature_verification_algorithms,
        )
    }

    fn supported_verify_schemes(&self) -> Vec<SignatureScheme> {
        rustls::crypto::ring::default_provider()
            .signature_verification_algorithms
            .supported_schemes()
    }
}

// ── Tests ─────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    // sha256 of an empty byte slice — known value
    #[test]
    fn sha256_known_vector() {
        let empty_sha256 = hex::decode(
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        ).unwrap();
        let got = sha256_cert(&[]);
        assert_eq!(got.as_ref(), empty_sha256.as_slice());
    }

    #[test]
    fn fingerprint_pin_rejected_on_unknown_cert() {
        let policy = StrictClientPolicy {
            allowed_sans: vec!["example.com".into()],
            pinned_fingerprints: vec![[0u8; 32]], // wrong fingerprint
        };
        let dummy = CertificateDer::from(vec![0xaau8; 32]);
        let result = policy.verify_client_cert(&dummy, &[], UnixTime::now());
        assert!(matches!(
            result,
            Err(TlsError::General(s)) if s.contains("FINGERPRINT_REJECTED")
        ));
    }

    #[test]
    fn policy_debug_does_not_leak_fingerprints() {
        let policy = StrictClientPolicy {
            allowed_sans: vec!["example.com".into()],
            pinned_fingerprints: vec![[0u8; 32], [1u8; 32]],
        };
        let dbg = format!("{:?}", policy);
        // Shows count, not raw bytes
        assert!(dbg.contains("pinned_count: 2"));
        assert!(!dbg.contains("000000000000"));
    }
}
