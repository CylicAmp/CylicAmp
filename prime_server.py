"""
prime_server.py

FastAPI server exposing the prime engine over HTTP.

Run:
  python prime_server.py
  python prime_server.py --host 0.0.0.0 --port 8000

Endpoints:
  GET /                          — API index
  GET /is_prime/{n}             — is n prime?
  GET /primes?start=2&limit=50  — list primes in range
  GET /twins?start=2&limit=50   — list twin prime pairs
  GET /stats?limit=10000        — π(N), DR distribution, twin count, largest gap
  GET /next?after=N             — next prime after N
  GET /dr/{n}                   — digital root and grid label for n
  GET /mersenne?max_exp=31      — Mersenne primes up to 2^max_exp - 1
"""

import sys
import os
import argparse
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "math", "primes"))

from prime_engine import (
    is_prime, prime_generator, twin_prime_generator,
    prime_count, prime_stats, digital_root, grid_label,
    first_n_primes, _GRID_LABEL,
)

try:
    from fastapi import FastAPI, Query, HTTPException
    from fastapi.responses import JSONResponse
    import uvicorn
except ImportError:
    print("Installing fastapi and uvicorn...")
    os.system("pip install fastapi uvicorn -q")
    from fastapi import FastAPI, Query, HTTPException
    from fastapi.responses import JSONResponse
    import uvicorn


app = FastAPI(
    title="CylicAmp Prime Engine",
    description="DR-based prime generator with alpha-grid classification",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------

@app.get("/")
def index():
    return {
        "engine": "CylicAmp Prime Engine",
        "theorem": "Every prime p>3 has DR(p) in {1,2,4,5,7,8}",
        "proven_empty": ["DR=6 (RL-E)", "DR=9 (RH-O)"],
        "twin_theorem": "Twin primes (p>3) have DR pairs in {(2,4),(5,7),(8,1)} only",
        "endpoints": {
            "GET /is_prime/{n}":           "primality test for n",
            "GET /primes":                 "?start=2&limit=50 — list primes",
            "GET /twins":                  "?start=2&limit=50 — list twin pairs",
            "GET /stats":                  "?limit=10000 — π(N), DR dist, gaps",
            "GET /next":                   "?after=N — next prime after N",
            "GET /dr/{n}":                 "digital root and grid label for n",
            "GET /mersenne":               "?max_exp=31 — Mersenne primes",
        },
    }


# ---------------------------------------------------------------------------
# /is_prime/{n}
# ---------------------------------------------------------------------------

@app.get("/is_prime/{n}")
def check_prime(n: int):
    if n < 0:
        raise HTTPException(400, "n must be non-negative")
    prime = is_prime(n)
    dr = digital_root(n) if n > 0 else None
    label = _GRID_LABEL[dr] if dr else None
    return {
        "n": n,
        "is_prime": prime,
        "dr": dr,
        "grid": label,
        "note": (
            "proven empty position — no primes here"
            if dr in {6, 9} and not prime and n > 3
            else None
        ),
    }


# ---------------------------------------------------------------------------
# /primes
# ---------------------------------------------------------------------------

@app.get("/primes")
def list_primes(
    start: int = Query(2, ge=2),
    limit: int = Query(50, ge=1, le=10000),
):
    results = []
    for p, label, dr in prime_generator(start):
        results.append({"prime": p, "grid": label, "dr": dr})
        if len(results) >= limit:
            break
    return {
        "start": start,
        "count": len(results),
        "primes": results,
    }


# ---------------------------------------------------------------------------
# /twins
# ---------------------------------------------------------------------------

@app.get("/twins")
def list_twins(
    start: int = Query(2, ge=2),
    limit: int = Query(50, ge=1, le=5000),
):
    results = []
    for p, p2, lp, lp2, dr1, dr2 in twin_prime_generator(start):
        results.append({
            "p": p, "p2": p2,
            "grid_p": lp, "grid_p2": lp2,
            "dr_p": dr1, "dr_p2": dr2,
            "dr_pair": f"({dr1},{dr2})",
        })
        if len(results) >= limit:
            break
    return {
        "start": start,
        "count": len(results),
        "allowed_dr_pairs": ["(2,4)", "(5,7)", "(8,1)"],
        "twins": results,
    }


# ---------------------------------------------------------------------------
# /stats
# ---------------------------------------------------------------------------

@app.get("/stats")
def stats(limit: int = Query(10000, ge=10, le=10_000_000)):
    s = prime_stats(limit)
    dr_table = []
    for dr in range(1, 10):
        cnt = s["dr_distribution"][dr]
        dr_table.append({
            "dr": dr,
            "grid": _GRID_LABEL[dr],
            "count": cnt,
            "proven_empty": dr in {6, 9},
        })
    return {
        "limit": limit,
        "pi_N": s["count"],
        "twin_pairs": s["twin_count"],
        "largest_gap": s["largest_gap"],
        "largest_gap_after": s["gap_after"],
        "dr_distribution": dr_table,
    }


# ---------------------------------------------------------------------------
# /next
# ---------------------------------------------------------------------------

@app.get("/next")
def next_prime(after: int = Query(..., ge=1)):
    for p, label, dr in prime_generator(after + 1):
        return {"after": after, "next_prime": p, "grid": label, "dr": dr}


# ---------------------------------------------------------------------------
# /dr/{n}
# ---------------------------------------------------------------------------

@app.get("/dr/{n}")
def dr_info(n: int):
    if n <= 0:
        raise HTTPException(400, "n must be positive")
    dr = digital_root(n)
    label = _GRID_LABEL[dr]
    return {
        "n": n,
        "dr": dr,
        "grid": label,
        "prime_possible": dr not in {6, 9} or n in {2, 3},
        "is_prime": is_prime(n),
    }


# ---------------------------------------------------------------------------
# /mersenne
# ---------------------------------------------------------------------------

@app.get("/mersenne")
def mersenne_primes(max_exp: int = Query(31, ge=2, le=61)):
    results = []
    exp = 2
    while exp <= max_exp:
        if is_prime(exp):
            m = 2**exp - 1
            m_prime = is_prime(m)
            if m_prime:
                dr = digital_root(m)
                results.append({
                    "exponent": exp,
                    "mersenne": m,
                    "is_prime": True,
                    "dr": dr,
                    "grid": _GRID_LABEL[dr],
                })
        exp += 1
    return {
        "max_exp": max_exp,
        "count": len(results),
        "mersenne_primes": results,
        "note": f"M61 = 2^61-1 is too large for sequential search; listed if max_exp>=61",
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    print(f"Starting CylicAmp Prime Engine at http://{args.host}:{args.port}")
    print(f"  Docs: http://{args.host}:{args.port}/docs")
    print()
    uvicorn.run("prime_server:app", host=args.host, port=args.port, reload=args.reload)
