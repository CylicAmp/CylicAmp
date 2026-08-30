use std::collections::HashMap;
use std::sync::Mutex;
use std::time::{Duration, Instant};

pub struct CircuitBreaker {
    threshold: u32,
    cooldown: Duration,
    failures: Mutex<HashMap<String, u32>>,
    last_failure: Mutex<HashMap<String, Instant>>,
}

impl CircuitBreaker {
    pub fn new(threshold: u32, cooldown_secs: u64) -> Self {
        Self {
            threshold,
            cooldown: Duration::from_secs(cooldown_secs),
            failures: Mutex::new(HashMap::new()),
            last_failure: Mutex::new(HashMap::new()),
        }
    }

    pub fn record_success(&self, source: &str) {
        let mut f = self.failures.lock().unwrap();
        let mut l = self.last_failure.lock().unwrap();
        f.remove(source);
        l.remove(source);
    }

    pub fn record_failure(&self, source: &str) {
        let mut f = self.failures.lock().unwrap();
        let mut l = self.last_failure.lock().unwrap();
        *f.entry(source.to_string()).or_insert(0) += 1;
        l.insert(source.to_string(), Instant::now());
    }

    pub fn is_open(&self, source: &str) -> bool {
        let f = self.failures.lock().unwrap();
        let l = self.last_failure.lock().unwrap();
        match (f.get(source), l.get(source)) {
            (Some(&count), Some(&last)) => {
                count >= self.threshold && last.elapsed() < self.cooldown
            }
            _ => false,
        }
    }
}
