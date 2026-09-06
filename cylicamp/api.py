"""
GF(37) FastAPI Service — thin wrappers over gf37_engine.

Run: uvicorn cylicamp.api:app --reload
Docs: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cylicamp.gf37_engine import GF37

app = FastAPI(
    title="GF(37) Mathematical API",
    description="Verified modular arithmetic over (ℤ/37ℤ)×. Prime p=37, generator g=2.",
    version="1.0.0",
)
G = GF37()
P = 37


def _validate(a: int, name: str = "a"):
    if not (1 <= a <= P - 1):
        raise HTTPException(status_code=422, detail=f"{name} must be in 1..36")
    return a


# ── Element endpoints ──────────────────────────────────────────────────────────

@app.get("/order/{a}", summary="Multiplicative order of a mod 37")
def get_order(a: int):
    _validate(a)
    return {"a": a, "order": G.order(a)}


@app.get("/dlog/{a}", summary="Discrete logarithm base 2 of a mod 37")
def get_dlog(a: int):
    _validate(a)
    k = G.dlog(a)
    return {"a": a, "k": k, "check": f"2^{k} ≡ {a} (mod 37)"}


@app.get("/legendre/{a}", summary="Legendre symbol (a/37)")
def get_legendre(a: int):
    _validate(a)
    leg = G.legendre(a)
    return {
        "a": a,
        "legendre": leg,
        "sector": "QR" if leg == 1 else "NQR",
        "euler_value": G.euler_test(a),
    }


@app.get("/orbit/26/{a}", summary="137-map 3-cycle of a under ×26 mod 37")
def get_orbit(a: int):
    _validate(a)
    orb = G.orbit_26(a)
    return {"a": a, "orbit": list(orb), "map": "×26 mod 37"}


@app.get("/is-primitive-root/{a}", summary="Test whether a is a primitive root mod 37")
def get_primitive_root_test(a: int):
    _validate(a)
    return {"a": a, "is_primitive_root": G.is_primitive_root(a)}


# ── Group-level endpoints ──────────────────────────────────────────────────────

@app.get("/primitive-roots", summary="All 12 primitive roots mod 37")
def get_primitive_roots():
    pr = G.primitive_roots()
    return {"count": len(pr), "primitive_roots": pr}


@app.get("/subgroup/{order}", summary="Unique subgroup of given order in (ℤ/37ℤ)×")
def get_subgroup(order: int):
    if order not in {1, 2, 3, 4, 6, 9, 12, 18, 36}:
        raise HTTPException(status_code=422, detail="Order must divide 36")
    return {"order": order, "elements": sorted(G.subgroup(order))}


@app.get("/cosets/{order}", summary="All cosets of the subgroup of given order")
def get_cosets(order: int):
    if order not in {1, 2, 3, 4, 6, 9, 12, 18, 36}:
        raise HTTPException(status_code=422, detail="Order must divide 36")
    raw = G.cosets(order)
    return {
        "subgroup_order": order,
        "index": 36 // order,
        "cosets": {str(rep): sorted(c) for rep, c in sorted(raw.items())},
    }


@app.get("/coset/H9/{a}", summary="H9-coset representative containing a")
def get_coset_H9(a: int):
    _validate(a)
    rep = G.coset_H9(a)
    coset = sorted(G.cosets(9)[rep])
    in_identity = a in G.subgroup(9)
    return {
        "a": a,
        "H9_coset_representative": rep,
        "coset_elements": coset,
        "is_identity_coset": in_identity,
    }


@app.get("/euler-partition", summary="Partition of (ℤ/37ℤ)× into QR and NQR by parity of dlog")
def get_euler_partition():
    ep = G.euler_partition()
    return {
        "QR_count": len(ep["QR"]),
        "NQR_count": len(ep["NQR"]),
        "QR": ep["QR"],
        "NQR": ep["NQR"],
        "rule": "QR ↔ dlog base 2 is even; NQR ↔ dlog is odd",
    }


@app.get("/rabinowitsch", summary="Six Rabinowitsch primes and their GF(37) data")
def get_rabinowitsch():
    data = G.rabinowitsch_residues()
    return {
        "note": "None of the six residues falls in H9 (identity coset)",
        "primes": {
            str(q): {**info, "sector": "QR" if info["legendre"] == 1 else "NQR"}
            for q, info in data.items()
        },
    }


@app.get("/dlog-table", summary="Complete discrete-log table log₂(a) for a=1..36")
def get_dlog_table():
    tbl = G.all_dlogs()
    return {"generator": 2, "modulus": P, "table": {str(k): v for k, v in sorted(tbl.items())}}


@app.get("/subgroup-lattice", summary="All subgroups of (ℤ/37ℤ)× indexed by order")
def get_subgroup_lattice():
    return {
        "group_order": 36,
        "factorization": "36 = 2² × 3²",
        "subgroups": {
            str(ord_): sorted(H)
            for ord_, H in sorted(G.subgroup_lattice().items())
        },
    }


@app.get("/health")
def health():
    return {"status": "ok", "p": P, "generator": G.generator, "group_order": G.order_of_group}
