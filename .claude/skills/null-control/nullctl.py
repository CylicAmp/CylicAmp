"""Classify a check as FORCED or CONTINGENT by running a null implementation."""
import sys

def classify(check, real_impl, null_impl, inputs=None):
    real_ok = bool(check(real_impl, inputs))
    null_ok = bool(check(null_impl, inputs))
    if null_ok:
        return {"classification": "FORCED", "bits": 0.0,
                "real_passes": real_ok, "null_passes": True,
                "reason": "a null implementation passes; the check confirms the "
                          "harness, not the mathematics"}
    return {"classification": "CONTINGENT", "bits": 1.0,
            "real_passes": real_ok, "null_passes": False,
            "reason": "the null implementation is rejected; the check discriminates"}

def _demo():
    import hashlib, json
    h = lambda v: hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest()[:12]
    BASE = {"triggers": ["unauthenticated", "replayed", "physically_impossible"]}
    MUT  = {"triggers": ["physically_impossible"]}
    null = lambda ins: {"count": 0}
    real = lambda ins: {"count": len([t for t in ins["triggers"]
                                      if t not in {"unauthenticated", "replayed"}])}
    with_hash = lambda i, r: {"value": r, "hash": h(i)}
    semantic  = lambda i, r: {"value": r}
    for label, proj in [("equality includes input value_hash", with_hash),
                        ("hashes moved to provenance      ", semantic)]:
        chk = lambda impl, _, P=proj: P(BASE, impl(BASE)) != P(MUT, impl(MUT))
        r = classify(chk, real, null)
        print(f"  {label}  {r['classification']:11} {r['bits']} bits "
              f"(null passes: {r['null_passes']})")

if __name__ == "__main__":
    print("null-control")
    _demo()
