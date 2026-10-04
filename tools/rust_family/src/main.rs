//! Port of scratch fam_chunk5.py (T245 proper-divisor family search).
//! Same algorithm, same pruning, same node order. Usage:
//!   family_search <M> <DEPTH> <state_file> [seed_json]
use num_bigint::BigUint;
use num_integer::Integer;
use num_traits::{One, ToPrimitive, Zero};
use rayon::prelude::*;
use std::collections::{HashMap, HashSet, BTreeMap};
use std::cell::RefCell;
use std::sync::OnceLock;

const T: u64 = 250;
const SM: u64 = 1_000_000;
const C0: u128 = 100_000;

struct Cfg {
    m: u128,
    depth: usize,
    small: Vec<u64>,
    tail: Vec<f64>,
    table: HashMap<(u64, u32), Vec<u128>>,
    primorial: BigUint,
    seed: Vec<(u128, u32)>,
}
static CFG: OnceLock<Cfg> = OnceLock::new();
fn cfg() -> &'static Cfg { CFG.get().unwrap() }

fn primes_upto(n: u64) -> Vec<u64> {
    let n = n as usize;
    let mut s = vec![true; n + 1];
    s[0] = false; if n >= 1 { s[1] = false; }
    let mut i = 2;
    while i * i <= n { if s[i] { let mut j = i * i; while j <= n { s[j] = false; j += i; } } i += 1; }
    (0..=n).filter(|&k| s[k]).map(|k| k as u64).collect()
}

/// sigma_2(q^e) = (q^(2(e+1)) - 1) / (q^2 - 1), exact.
fn s2pe(q: u128, e: u32) -> BigUint {
    let qb = BigUint::from(q);
    let q2 = &qb * &qb;
    (q2.pow(e + 1) - 1u32) / (q2 - 1u32)
}

fn vp(mut n: u32, p: u32) -> u32 { let mut k = 0; while n % p == 0 { n /= p; k += 1; } k }

/// Same test as Python feasible(): exact 2/3-supply bookkeeping, surplus is final.
fn feasible(jn: usize, c: u128, comps: &[(u128, u32)]) -> bool {
    let g = cfg();
    let (mut a, mut b, mut s2, mut s3) = (0u32, 0u32, 0u32, 0u32);
    for &(p, e) in comps {
        if p == 2 { a = e } else { s2 += vp(e + 1, 2) }
        if p == 3 { b = e } else { s3 += vp(e + 1, 3) }
    }
    let p0 = if jn < g.small.len() { g.small[jn] } else { T } as u128;
    let r = g.m / c;
    let f2 = if r >= p0 { ((r as f64).ln() / (p0 as f64).ln() + 1e-9) as u32 } else { 0 };
    s2 <= a && s3 <= b && s2 + f2 >= a && s3 + f2 / 2 >= b
}

thread_local! {
    static SMALLPART: RefCell<HashMap<(u128, u32), Vec<u128>>> = RefCell::new(HashMap::new());
    static FULLPART: RefCell<HashMap<(u128, u32), Vec<u128>>> = RefCell::new(HashMap::new());
}

/// All prime factors of n (BigUint). Panics if factorization is incomplete:
/// a silently partial factorization would make the search non-exhaustive.
fn prime_factors(n: &BigUint) -> Vec<u128> {
    if n <= &BigUint::one() { return vec![]; }
    let (fs, rest) = num_prime::nt_funcs::factors(n.clone(), None);
    if let Some(r) = rest { panic!("incomplete factorization of {}: remaining {:?}", n, r); }
    fs.keys().map(|k| k.to_u128().expect("factor exceeds u128")).collect()
}

/// Python large(p,e) for p < 250: from the precomputed table.
fn large_small(p: u128, e: u32) -> &'static [u128] {
    cfg().table.get(&(p as u64, e)).map(|v| v.as_slice())
        .unwrap_or_else(|| panic!("table missing ({},{})", p, e))
}

/// Python large_upto(q,e,R): primes a, T <= a <= R, dividing sigma_2(q^e).
fn large_upto(q: u128, e: u32, r: u128) -> Vec<u128> {
    if r < T as u128 { return vec![]; }
    if (q as u64) < T && q < T as u128 {
        return large_small(q, e).iter().copied().filter(|&a| a <= r).collect();
    }
    if r >= SM as u128 {
        let full = FULLPART.with(|c| c.borrow().get(&(q, e)).cloned());
        let full = full.unwrap_or_else(|| {
            let v: Vec<u128> = prime_factors(&s2pe(q, e)).into_iter().filter(|&a| a >= T as u128).collect();
            FULLPART.with(|c| c.borrow_mut().insert((q, e), v.clone()));
            v
        });
        return full.into_iter().filter(|&a| a <= r).collect();
    }
    let sp = SMALLPART.with(|c| c.borrow().get(&(q, e)).cloned());
    let sp = sp.unwrap_or_else(|| {
        let s = s2pe(q, e);
        let rem = &cfg().primorial % &s;
        let g = s.gcd(&rem);
        let v: Vec<u128> = if g.is_one() { vec![] } else { prime_factors(&g) };
        SMALLPART.with(|c| c.borrow_mut().insert((q, e), v.clone()));
        v
    });
    sp.into_iter().filter(|&a| a <= r).collect()
}

fn is_prime_big(n: &BigUint) -> bool {
    num_prime::nt_funcs::is_prime(n, None).probably()
}

/// Python check(): exact membership test.
fn check(m: u128, s2: &BigUint, hits: &mut Vec<(u128, BigUint)>) {
    let mb = BigUint::from(m);
    let mm = &mb * &mb;
    if s2 * 2u32 > &mm * 3u32 && (s2 % &mb).is_zero() {
        let q = s2 / &mb - &mb;
        if q > &mb / 2u32 && is_prime_big(&q) { hits.push((m, q)); }
    }
}

fn ratio(s2: &BigUint, c: u128) -> f64 {
    let cb = BigUint::from(c);
    s2.to_f64().unwrap() / (&cb * &cb).to_f64().unwrap()
}

fn large_any(p: u128, e: u32) -> Vec<u128> {
    if p < T as u128 { large_small(p, e).to_vec() } else { large_upto(p, e, u128::MAX) }
}

type Key = Vec<(u128, u32)>;

/// Python big_ext(): read large primes off sigma_2 of the current part.
fn big_ext(c: u128, s2: &BigUint, l: &Vec<u128>, hits: &mut Vec<(u128, BigUint)>) {
    let mut seen: HashSet<Key> = HashSet::new();
    fn ext(depth: usize, m: u128, s2m: &BigUint, l: &Vec<u128>, chosen: &Key,
           seen: &mut HashSet<Key>, hits: &mut Vec<(u128, BigUint)>) {
        let g = cfg();
        if depth == g.depth { return; }
        let seed_has = |q: u128| g.seed.iter().any(|&(a, _)| a == q);
        for &q in l {
            if seed_has(q) || chosen.iter().any(|&(a, _)| a == q) { continue; }
            let mut pe: u128 = 1; let mut e = 0u32;
            loop {
                pe = match pe.checked_mul(q) { Some(v) => v, None => break };
                e += 1;
                let m2 = match m.checked_mul(pe) { Some(v) if v <= g.m => v, _ => break };
                let mut key = chosen.clone(); key.push((q, e)); key.sort();
                if seen.contains(&key) { continue; }
                seen.insert(key.clone());
                let s22 = s2m * s2pe(q, e);
                check(m2, &s22, hits);
                let mut l2 = l.clone();
                for a in large_upto(q, e, g.m / m2) { if !l2.contains(&a) { l2.push(a); } }
                ext(depth + 1, m2, &s22, &l2, &key, seen, hits);
            }
        }
    }
    ext(0, c, s2, l, &vec![], &mut seen, hits);
}

fn node(c: u128, s2: &BigUint, l: &Vec<u128>, hits: &mut Vec<(u128, BigUint)>) {
    check(c, s2, hits);
    let g = cfg();
    if ratio(s2, c) * g.tail[g.small.len()] >= 1.5 && !l.is_empty() { big_ext(c, s2, l, hits); }
}

#[derive(Clone)]
struct Item { j: usize, c: u128, s2: BigUint, comps: Vec<(u128, u32)> }

fn children(it: &Item) -> Vec<Item> {
    let g = cfg(); let mut out = vec![];
    let r = ratio(&it.s2, it.c);
    for jj in it.j..g.small.len() {
        let p = g.small[jj] as u128;
        match it.c.checked_mul(p) { Some(v) if v <= g.m => {}, _ => break }
        if r * g.tail[jj] < 1.5 { break; }
        let mut pe: u128 = 1; let mut e = 0u32;
        loop {
            pe *= p; e += 1;
            let c2 = match it.c.checked_mul(pe) { Some(v) if v <= g.m => v, _ => break };
            let mut nc = it.comps.clone(); nc.push((p, e));
            if feasible(jj + 1, c2, &nc) {
                out.push(Item { j: jj + 1, c: c2, s2: &it.s2 * s2pe(p, e), comps: nc });
            }
        }
    }
    out
}

fn union_large(comps: &[(u128, u32)]) -> Vec<u128> {
    let mut l: Vec<u128> = vec![];
    for &(p, e) in comps { for a in large_any(p, e) { if !l.contains(&a) { l.push(a); } } }
    l
}

/// Python subtree(): DFS over small primes, returns (hits, nodes).
fn subtree(item: &Item) -> (Vec<(u128, BigUint)>, u64) {
    let mut hits = vec![]; let mut n = 0u64;
    fn dfs(it: &Item, l: &Vec<u128>, hits: &mut Vec<(u128, BigUint)>, n: &mut u64) {
        *n += 1; node(it.c, &it.s2, l, hits);
        for ch in children(it) {
            let &(p, e) = ch.comps.last().unwrap();
            let mut l2 = l.clone();
            for a in large_any(p, e) { if !l2.contains(&a) { l2.push(a); } }
            dfs(&ch, &l2, hits, n);
        }
    }
    let l0 = union_large(&item.comps);
    dfs(item, &l0, &mut hits, &mut n);
    (hits, n)
}

fn build() -> (Vec<Item>, Vec<Item>) {
    let g = cfg();
    let mut seedp: u128 = 1; let mut seeds2 = BigUint::one();
    for &(p, e) in &g.seed { seedp *= p.pow(e); seeds2 *= s2pe(p, e); }
    let mut stack = vec![]; let (mut items, mut top) = (vec![], vec![]);
    for a in 1..60u32 { for b in 1..40u32 {
        let c = match 2u128.checked_pow(a).and_then(|x| x.checked_mul(3u128.pow(b))).and_then(|x| x.checked_mul(seedp)) {
            Some(v) if v <= g.m => v, _ => break };
        let s2 = s2pe(2, a) * s2pe(3, b) * &seeds2;
        if ratio(&s2, c) * g.tail[2] < 1.5 { continue; }
        let mut comps = vec![(2u128, a), (3u128, b)]; comps.extend(g.seed.iter().copied());
        if !feasible(2, c, &comps) { continue; }
        stack.push(Item { j: 2, c, s2, comps });
    }}
    while let Some(it) = stack.pop() {
        if it.c >= C0 { items.push(it); continue; }
        let ch = children(&it); top.push(it); stack.extend(ch);
    }
    items.sort_by(|x, y| (x.c, &x.comps).cmp(&(y.c, &y.comps)));
    (top, items)
}

fn parse_seed(s: &str) -> Vec<(u128, u32)> {
    // "[[p,e],[p,e]]"
    let nums: Vec<u128> = s.split(|ch: char| !ch.is_ascii_digit()).filter(|t| !t.is_empty())
        .map(|t| t.parse().unwrap()).collect();
    nums.chunks(2).map(|c| (c[0], c[1] as u32)).collect()
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let m: u128 = args[1].parse::<f64>().map(|x| x as u128).unwrap();
    let m = if args[1].contains('e') { let (a, b) = args[1].split_once('e').unwrap();
        a.parse::<u128>().unwrap() * 10u128.pow(b.parse().unwrap()) } else { m };
    let depth: usize = args[2].parse().unwrap();
    let state = args[3].clone();
    let seed = if args.len() > 4 { parse_seed(&args[4]) } else { vec![] };
    let small = primes_upto(T - 1);
    let mut tail = vec![1.0f64; small.len() + 1];
    tail[small.len()] = (1.0 - (T as f64).powi(-2)).powi(-(depth as i32)) * (1.0 + 1e-9);
    for i in (0..small.len()).rev() { tail[i] = tail[i + 1] / (1.0 - (small[i] as f64).powi(-2)); }
    let mut table = HashMap::new();
    let tpath = std::env::var("SMALL_TABLE").unwrap_or("small_table.txt".into());
    for line in std::fs::read_to_string(&tpath).expect("small_table.txt").lines() {
        let v: Vec<u128> = line.split_whitespace().map(|t| t.parse().unwrap()).collect();
        table.insert((v[0] as u64, v[1] as u32), v[2..].to_vec());
    }
    let mut primorial = BigUint::one();
    for p in primes_upto(SM - 1) { if p >= T { primorial *= p; } }
    CFG.set(Cfg { m, depth, small, tail, table, primorial, seed }).ok();

    let t0 = std::time::Instant::now();
    let (top, items) = build();
    // state: next, nodes, top_done, then "m q" lines
    let (mut next, mut nodes, mut top_done, mut hits) = (0usize, 0u64, false, BTreeMap::<u128, BigUint>::new());
    if let Ok(s) = std::fs::read_to_string(&state) {
        let mut ls = s.lines();
        next = ls.next().unwrap().parse().unwrap(); nodes = ls.next().unwrap().parse().unwrap();
        top_done = ls.next().unwrap() == "1";
        for l in ls { let (a, b) = l.split_once(' ').unwrap(); hits.insert(a.parse().unwrap(), b.parse().unwrap()); }
    }
    let save = |next: usize, nodes: u64, top_done: bool, hits: &BTreeMap<u128, BigUint>| {
        let mut s = format!("{}\n{}\n{}\n", next, nodes, if top_done { 1 } else { 0 });
        for (a, b) in hits { s += &format!("{} {}\n", a, b); }
        let tmp = format!("{}.tmp", state); std::fs::write(&tmp, s).unwrap(); std::fs::rename(&tmp, &state).unwrap();
    };
    if !top_done {
        for it in &top { let mut h = vec![]; node(it.c, &it.s2, &union_large(&it.comps), &mut h);
            for (a, b) in h { hits.insert(a, b); } nodes += 1; }
        top_done = true; save(next, nodes, top_done, &hits);
    }
    let batch = std::env::var("BATCH").ok().and_then(|b| b.parse().ok()).unwrap_or(64usize);
    while next < items.len() {
        let end = (next + batch).min(items.len());
        let res: Vec<(Vec<(u128, BigUint)>, u64)> = items[next..end].par_iter().map(subtree).collect();
        for (h, n) in res { nodes += n; for (a, b) in h { hits.insert(a, b); } }
        next = end; save(next, nodes, top_done, &hits);
        eprintln!("M={:e}: items {}/{} ({:.1}%), top nodes {}, nodes so far {}, members so far {}, {:.0}s",
            m as f64, next, items.len(), 100.0 * next as f64 / items.len() as f64, top.len(), nodes, hits.len(), t0.elapsed().as_secs_f64());
    }
    println!("COMPLETE. M={} items {} top {} nodes {} members {}", m, items.len(), top.len(), nodes, hits.len());
}
