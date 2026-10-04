//! Supply cycles among primes >= T: x -> y when y | sigma_2(x^e).
//! Port of scratch cycles2.py. Every large prime of a family member is reachable
//! from the small-prime core or from such a cycle (walk in-edges backwards).
//! Cycles are enumerated from their smallest node q <= B^(1/3); 2-cycles with both
//! exponents 1 satisfy q^2+r^2+1 = 3qr and are consecutive odd-index Fibonacci.
//! Usage: cycles <M> <out.json>     (B = M / 60, max length = floor(log_T B))
use num_bigint::BigUint;
use num_integer::Integer;
use num_traits::{One, ToPrimitive};
use rayon::prelude::*;
use std::cell::RefCell;
use std::collections::HashMap;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::OnceLock;

const T: u128 = 250;
const SM: u128 = 1_000_000;
static PRIM: OnceLock<BigUint> = OnceLock::new();
static NODES: AtomicU64 = AtomicU64::new(0);

fn primes_upto(n: u64) -> Vec<u64> {
    let n = n as usize;
    let mut s = vec![true; n + 1];
    s[0] = false;
    if n >= 1 {
        s[1] = false;
    }
    let mut i = 2;
    while i * i <= n {
        if s[i] {
            let mut j = i * i;
            while j <= n {
                s[j] = false;
                j += i;
            }
        }
        i += 1;
    }
    (0..=n).filter(|&k| s[k]).map(|k| k as u64).collect()
}

fn s2pe(q: u128, e: u32) -> BigUint {
    let q2 = BigUint::from(q) * BigUint::from(q);
    (q2.pow(e + 1) - 1u32) / (q2 - 1u32)
}

/// sigma_2(x^e) mod q, for q < 2^64
fn s2_mod(x: u128, e: u32, q: u128) -> u128 {
    let xr = x % q;
    let y = xr * xr % q;
    let mut acc = 0u128;
    let mut pw = 1u128;
    for _ in 0..=e {
        acc = (acc + pw) % q;
        pw = pw * y % q;
    }
    acc
}

/// All prime factors; panics on an incomplete factorization (never silently partial).
fn prime_factors(n: &BigUint) -> Vec<u128> {
    if n <= &BigUint::one() {
        return vec![];
    }
    let (fs, rest) = num_prime::nt_funcs::factors(n.clone(), None);
    if let Some(r) = rest {
        panic!("incomplete factorization of {}: remaining {:?}", n, r);
    }
    fs.keys().map(|k| k.to_u128().expect("factor exceeds u128")).collect()
}

thread_local! {
    static FULL: RefCell<HashMap<(u128, u32), Vec<u128>>> = RefCell::new(HashMap::new());
    static SMALL: RefCell<HashMap<(u128, u32), Vec<u128>>> = RefCell::new(HashMap::new());
}

/// Prime factors y of sigma_2(x^e) with T <= y <= r. For r < 1e6 the primes <= r
/// dividing S are exactly those dividing gcd(S, primorial(T..1e6)).
fn f_upto(x: u128, e: u32, r: u128) -> Vec<u128> {
    if r < T {
        return vec![];
    }
    let v = if r >= SM {
        match FULL.with(|c| c.borrow().get(&(x, e)).cloned()) {
            Some(v) => v,
            None => {
                let mut v = prime_factors(&s2pe(x, e));
                v.sort();
                FULL.with(|c| c.borrow_mut().insert((x, e), v.clone()));
                v
            }
        }
    } else {
        match SMALL.with(|c| c.borrow().get(&(x, e)).cloned()) {
            Some(v) => v,
            None => {
                let s = s2pe(x, e);
                let rem = PRIM.get().unwrap() % &s;
                let g = s.gcd(&rem);
                let mut v = if g.is_one() { vec![] } else { prime_factors(&g) };
                v.sort();
                SMALL.with(|c| c.borrow_mut().insert((x, e), v.clone()));
                v
            }
        }
    };
    v.into_iter().filter(|&y| y >= T && y <= r).collect()
}

type Path = Vec<(u128, u32)>;

fn dfs(q: u128, path: &mut Path, prod: u128, b: u128, lmax: usize, out: &mut Vec<Path>) {
    NODES.fetch_add(1, Ordering::Relaxed);
    let (x, e) = *path.last().unwrap();
    if path.len() >= 2 && s2_mod(x, e, q) == 0 {
        out.push(path.clone());
    }
    if path.len() == lmax {
        return;
    }
    for y in f_upto(x, e, b / prod) {
        if y <= q || path.iter().any(|&(a, _)| a == y) {
            continue;
        }
        let mut f = 1u32;
        let mut pp = y;
        loop {
            let np = match prod.checked_mul(pp) {
                Some(v) if v <= b => v,
                _ => break,
            };
            path.push((y, f));
            dfs(q, path, np, b, lmax, out);
            path.pop();
            f += 1;
            pp = match pp.checked_mul(y) {
                Some(v) => v,
                None => break,
            };
        }
    }
}

fn icbrt(n: u128) -> u128 {
    let mut x = (n as f64).cbrt() as u128;
    while x * x * x > n {
        x -= 1;
    }
    while (x + 1) * (x + 1) * (x + 1) <= n {
        x += 1;
    }
    x
}

fn is_prime_u128(n: u128) -> bool {
    num_prime::nt_funcs::is_prime(&BigUint::from(n), None).probably()
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let (a, bexp) = args[1].split_once('e').expect("M like 1e22");
    let m: u128 = a.parse::<u128>().unwrap() * 10u128.pow(bexp.parse().unwrap());
    let b = m / 60;
    let mut lmax = 1usize;
    let mut p = T;
    while p.saturating_mul(T) <= b {
        p *= T;
        lmax += 1;
    }
    let mut prim = BigUint::one();
    for p in primes_upto((SM - 1) as u64) {
        if p as u128 >= T {
            prim *= p;
        }
    }
    PRIM.set(prim).ok();
    let qmax = icbrt(b);
    let qs: Vec<u128> = primes_upto(qmax as u64)
        .into_iter()
        .map(|p| p as u128)
        .filter(|&p| p >= T)
        .collect();
    let t0 = std::time::Instant::now();
    let mut cycles: Vec<Path> = qs
        .par_iter()
        .flat_map_iter(|&q| {
            let mut out = vec![];
            let mut e = 1u32;
            let mut p = q;
            loop {
                match p.checked_mul(q) {
                    Some(pq) if pq <= b => {}
                    _ => break,
                }
                let mut path = vec![(q, e)];
                dfs(q, &mut path, p, b, lmax, &mut out);
                e += 1;
                p *= q;
            }
            out.into_iter()
        })
        .collect();
    cycles.sort();
    cycles.dedup();
    // 2-cycles with both exponents 1: q^2 + r^2 + 1 = 3qr (Vieta) -> odd-index Fibonacci
    let (mut x, mut y) = (1u128, 2u128);
    let mut fib = vec![];
    while let Some(xy) = x.checked_mul(y) {
        if xy > b {
            break;
        }
        if x >= T && is_prime_u128(x) && is_prime_u128(y) {
            fib.push((x, y));
        }
        let z = 3 * y - x;
        x = y;
        y = z;
    }
    let js: Vec<String> = cycles
        .iter()
        .map(|c| {
            format!(
                "[{}]",
                c.iter().map(|(p, e)| format!("[{}, {}]", p, e)).collect::<Vec<_>>().join(", ")
            )
        })
        .collect();
    std::fs::write(&args[2], format!("[{}]", js.join(", "))).unwrap();
    eprintln!(
        "B={:.3e} q<={} lmax={}: nodes {}, cycles {}, Fibonacci 2-cycles >= {}: {:?} ({:.0}s)",
        b as f64,
        qmax,
        lmax,
        NODES.load(Ordering::Relaxed),
        cycles.len(),
        T,
        fib,
        t0.elapsed().as_secs_f64()
    );
}
