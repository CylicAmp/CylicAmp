use reqwest::Client;
use std::time::Duration;

use crate::circuit::CircuitBreaker;

const CISA_JSON: &str = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json";
const CISA_CSV: &str = "https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv";
const GITHUB_MIRROR: &str = "https://raw.githubusercontent.com/cisagov/kev-data/main/known_exploited_vulnerabilities.json";

lazy_static::lazy_static! {
    static ref BREAKER: CircuitBreaker = CircuitBreaker::new(3, 3600);
}

pub async fn fetch_catalog() -> anyhow::Result<(Vec<serde_json::Value>, serde_json::Value)> {
    let client = Client::builder()
        .timeout(Duration::from_secs(15))
        .build()?;

    // Try CISA JSON
    if !BREAKER.is_open("cisa_json") {
        match client.get(CISA_JSON).send().await {
            Ok(resp) if resp.status().is_success() => {
                let data: serde_json::Value = resp.json().await?;
                BREAKER.record_success("cisa_json");
                let entries = data["vulnerabilities"].as_array()
                    .cloned()
                    .unwrap_or_default();
                let meta = serde_json::json!({
                    "source": "cisa_json",
                    "fetched_at": chrono::Utc::now().to_rfc3339(),
                });
                return Ok((entries, meta));
            }
            _ => BREAKER.record_failure("cisa_json"),
        }
    }

    // Try GitHub mirror
    if !BREAKER.is_open("github_mirror") {
        match client.get(GITHUB_MIRROR).send().await {
            Ok(resp) if resp.status().is_success() => {
                let data: serde_json::Value = resp.json().await?;
                BREAKER.record_success("github_mirror");
                let entries = data["vulnerabilities"].as_array()
                    .cloned()
                    .unwrap_or_default();
                let meta = serde_json::json!({
                    "source": "github_mirror",
                    "fetched_at": chrono::Utc::now().to_rfc3339(),
                });
                return Ok((entries, meta));
            }
            _ => BREAKER.record_failure("github_mirror"),
        }
    }

    Err(anyhow::anyhow!("All KEV sources unavailable"))
}
