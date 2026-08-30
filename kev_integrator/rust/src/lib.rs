use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashSet;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KEVEntry {
    pub cve_id: String,
    pub vendor: String,
    pub product: String,
    pub name: String,
    pub date_added: DateTime<Utc>,
    pub due_date: DateTime<Utc>,
    pub required_action: String,
    pub known_ransomware: bool,
    pub notes: String,
}

pub mod cache;
pub mod circuit;
pub mod client;
pub mod fetcher;
pub mod metrics;
pub mod parser;
pub mod state;

pub use client::{get_kev_catalog, get_kev_cve_ids};
