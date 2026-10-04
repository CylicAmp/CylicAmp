use std::env;
use std::sync::{Arc, Mutex, atomic::{AtomicU64, Ordering}};
use std::time::Instant;
type U64 = u64;
type U128 = u128;
const SEED_MAX: U64 = 10000;
const REPORT_INTERVAL: U64 = 1_000_000;
#[derive(Clone, Copy)]
struct LockedPrime { prime: U64, min_exp_2: u8, min_exp_3: u8, color: u8 }
const LOCKED: &[LockedPrime] = &[
    LockedPrime { prime: 43,  min_exp_2: 6,  min_exp_3: 0, color: 1 },
    LockedPrime { prime: 127, min_exp_2: 6,  min_exp_3: 0, color: 1 },
    LockedPrime { prime: 23,  min_exp_2: 10, min_exp_3: 0, color: 2 },
    LockedPrime { prime: 89,  min_exp_2: 10, min_exp_3: 0, color: 2 },
    LockedPrime { prime: 67,  min_exp_2: 0,  min_exp_3: 2, color: 1 },
    LockedPrime { prime: 109, min_exp_2: 17, min_exp_3: 0, color: 0 },
    LockedPrime { prime: 149, min_exp_2: 73, min_exp_3: 0, color: 0 },
];
#[inline]
fn find_locked(p: U64) -> Option<&'static LockedPrime> { LOCKED.iter().find(|lp| lp.prime == p) }
fn sieve_primes(limit: usize) -> Vec<U64> {
    let mut is_prime = vec![true; limit + 1]; is_prime[0] = false; is_prime[1] = false;
    for i in 2..=((limit as f64).sqrt() as usize) { if is_prime[i] { for j in (i * i..=limit).step_by(i) { is_prime[j] = false; } } }
    (2..=limit).filter(|&i| is_prime[i]).map(|i| i as U64).collect()
}
fn factor(n: U64, small_primes: &[U64]) -> Vec<(U64, u32)> {
    let mut factors = Vec::new(); let mut n = n;
    for &p in small_primes { if p * p > n { break; } if n % p == 0 { let mut e = 0u32; while n % p == 0 { e += 1; n /= p; } factors.push((p, e)); } }
    if n > 1 { factors.push((n, 1)); }
    factors
}
fn sigma2_from_factors(factors: &[(U64, u32)]) -> U128 {
    let mut result = 1u128;
    for &(p, e) in factors { let p2 = (p as U128) * (p as U128); let mut term = 1u128; let mut p_power = 1u128;
        for _ in 0..e { p_power *= p2; term += p_power; } result *= term; }
    result
}
fn sigma2(n: U64, small_primes: &[U64]) -> U128 { if n == 1 { return 1; } let factors = factor(n, small_primes); sigma2_from_factors(&factors) }
#[inline]
fn is_solution(m: U64, small_primes: &[U64]) -> bool { sigma2(m, small_primes) % (m as U128) == 0 }
struct SearchState { bound: U64, small_primes: Vec<U64>, solutions: Mutex<Vec<U64>>, node_count: AtomicU64 }
impl SearchState {
    fn search(&self, prod: U64) {
        let nodes = self.node_count.fetch_add(1, Ordering::Relaxed) + 1;
        if nodes % REPORT_INTERVAL == 0 { let sols = self.solutions.lock().unwrap().len(); eprint!("\rNodes: {} | Solutions: {}", nodes, sols); }
        if prod > self.bound { return; }
        if prod > 1 && is_solution(prod, &self.small_primes) { self.solutions.lock().unwrap().push(prod); }
        let s2_prod = sigma2(prod, &self.small_primes);
        let s2_u64 = s2_prod.min(U128::MAX) as U64;
        let s2_factors = factor(s2_u64, &self.small_primes);
        let prod_factors = factor(prod, &self.small_primes);
        let prod_primes: std::collections::HashSet<U64> = prod_factors.iter().map(|&(p, _)| p).collect();
        for &(q, e_max) in &s2_factors {
            if prod_primes.contains(&q) { continue; }
            for e in 1..=e_max {
                let qe = q.pow(e);
                let new_prod = match prod.checked_mul(qe) { Some(np) => np, None => break };
                if new_prod > self.bound { break; }
                if new_prod.checked_mul(q).map_or(false, |npq| npq <= self.bound) { self.search(new_prod); }
                else { if is_solution(new_prod, &self.small_primes) { self.solutions.lock().unwrap().push(new_prod); } }
            }
        }
    }
}
fn main() {
    let args: Vec<String> = env::args().collect();
    let bound: U64 = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(1_000_000);
    let small_primes = sieve_primes(1_000_000);
    let state = Arc::new(SearchState { bound, small_primes, solutions: Mutex::new(Vec::new()), node_count: AtomicU64::new(0) });
    let start = Instant::now();
    for seed in 2..=SEED_MAX { state.search(seed); }
    let mut sols = state.solutions.lock().unwrap(); sols.sort(); sols.dedup();
    eprintln!("\nfound {} nodes {} time {:.2}s", sols.len(), state.node_count.load(Ordering::Relaxed), start.elapsed().as_secs_f64());
    for s in sols.iter() { println!("{}", s); }
}
