#!/usr/bin/env python3
"""Unified Operator Module -- the recursion loop that grows the owner's math in all directions.

Built 2026-10-13 from the owner's request (message #235 in owner_work):

    def recurse(z):
        required = compute_required(z); available = compute_available()
        if available < required: return refuse(z, "INSUFFICIENT_COMPUTE")
        reserve(required)
        O = generate_operators(z)                 # 2
        expansions = [F(z) for F in O]            # 3
        merged = merge(expansions)                # 4
        C = classify(merged)                      # 5
        updated = update_priorities(z, C)         # 6
        checkpoint(updated)                       # 7
        return updated                            # 8
    z = initial_state
    while True: z = recurse(z)

Every one of those steps is implemented below, as written, and the module adds only what
the request says it guarantees:
  * compute reservation  -- a step starts only if its whole cost fits the budget left;
                            otherwise it refuses, and the loop ends there (no half step).
  * checkpointing        -- the full state is written after every step (atomic replace);
                            a rerun with the same checkpoint resumes from the last step.
  * operators fail alone -- each operator runs in its own try/except, so one failure is
                            logged and the others still expand (the request says "even if
                            one operator fails, the others continue"; a bare list
                            comprehension would not do that, so each is guarded).

    python3 unified_operator.py 246                     seed 246, default budget
    python3 unified_operator.py 1 2 12 21 --steps 4     several seeds
    python3 unified_operator.py 246 --budget 50000 --width 40 --checkpoint my_run.json

The operators are the owner's operations already in this repo (see OPERATORS); the
classification is the owner's frameworks (GF(37) orbit, digital root, prime / twin /
Sophie Germain / safe).
"""
import argparse
import importlib.util
import json
import os
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
MAX_DIGITS = 24                      # results stay below 10**24, inside Miller-Rabin's proven range
WITNESSES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)   # deterministic for n < 3.3e24


def _gf37():
    spec = importlib.util.spec_from_file_location("gf37", ROOT / ".claude" / "skills" / "gf37.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


G = _gf37()


def is_prime(n):
    if n < 2:
        return False
    for p in WITNESSES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in WITNESSES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def rev(n):
    return int(str(n)[::-1])


# --- 2. operators: the owner's operations already in the repo ---------------------------------
UNARY = {
    "flip":        rev,                                   # 12 <-> 21 (drip example, #228)
    "flip-sum":    lambda n: n + rev(n),                  # digit-protocols FLIP register
    "flip-gap":    lambda n: abs(n - rev(n)),
    "digit-sum":   lambda n: sum(map(int, str(n))),       # SUM register
    "x137":        lambda n: n * 137,                     # frameworks: x137
    "137-map":     lambda n: 26 * n % 37,                 # f(n) = 26n mod 37
    "sophie":      lambda n: 2 * n + 1,                   # Sophie Germain map
    "twin-up":     lambda n: n + 2,                       # twin neighbour
    "twin-down":   lambda n: n - 2,
}
PAIR = {                                                  # bilinear part: every pair of the frontier
    "sum":         lambda a, b: a + b,
    "product":     lambda a, b: a * b,
    "join":        lambda a, b: int(f"{a}{b}"),           # 1, 2 -> 12   (drip example shape)
    "join-back":   lambda a, b: int(f"{b}{a}"),           # 1, 2 -> 21
}


def generate_operators(z):
    """Unary operators on each frontier number, pair operators on each frontier pair."""
    front = z["frontier"]
    ops = [(name, (n,)) for n in front for name in UNARY]
    ops += [(name, (a, b)) for i, a in enumerate(front) for b in front[i + 1:] for name in PAIR]
    return ops


# --- 1. compute reservation -------------------------------------------------------------------
def compute_required(z):
    k = len(z["frontier"])
    return k * len(UNARY) + k * (k - 1) // 2 * len(PAIR)


def compute_available(z):
    return z["budget"] - z["used"]


# --- 3/4. expand and merge ----------------------------------------------------------------------
def expand(z, ops):
    out, errors = [], []
    for name, args in ops:
        try:
            v = (UNARY[name](*args) if len(args) == 1 else PAIR[name](*args))
        except Exception as e:                       # one operator fails, the rest continue
            errors.append(f"{name}{args}: {e}")
            continue
        if 0 < v < 10 ** MAX_DIGITS:
            out.append((v, name, list(args)))
    return out, errors


def merge(z, expansions):
    new = []
    for v, name, args in sorted(expansions, key=lambda t: (t[0], t[1], t[2])):
        key = str(v)
        if key in z["seen"]:
            continue
        z["seen"][key] = {"step": z["step"] + 1, "op": name, "from": args}
        new.append(v)
    return new


# --- 5. classify: the owner's frameworks ----------------------------------------------------------
def classify(n):
    p = is_prime(n)
    return {
        "orbit": G.orbit(n),
        "dr": G.dr(n),
        "prime": p,
        "twin": p and (is_prime(n - 2) or is_prime(n + 2)),
        "sophie": p and is_prime(2 * n + 1),
        "safe": p and n > 2 and is_prime((n - 1) // 2),
    }


def class_keys(c):
    keys = {f"orbit:{c['orbit']}", f"dr:{c['dr']}"}
    keys |= {k for k in ("prime", "twin", "sophie", "safe") if c[k]}
    return keys


# --- 6. priorities -------------------------------------------------------------------------------------
def update_priorities(z, new):
    """A new number scores one point per class it reaches that nothing reached before.
    The next frontier is the top `width` new numbers; everything else stays recorded."""
    scored = []
    for n in new:
        c = classify(n)
        z["seen"][str(n)]["class"] = c
        fresh = class_keys(c) - set(z["covered"])
        scored.append((-len(fresh), len(str(n)), n, fresh))
    scored.sort()
    for _, _, n, fresh in scored:
        z["covered"].extend(sorted(fresh - set(z["covered"])))
    z["frontier"] = [n for _, _, n, _ in scored[: z["width"]]]
    return z


# --- 7. checkpoint ---------------------------------------------------------------------------------------
def checkpoint(z, path):
    if not path:
        return
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name, suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        json.dump(z, f, indent=1, sort_keys=True)
    os.replace(tmp, path)                     # atomic: a restart sees the old or the new state


def initial_state(seeds, budget, width):
    z = {"seeds": sorted(set(seeds)), "step": 0, "budget": budget, "used": 0, "width": width,
         "frontier": sorted(set(seeds)), "seen": {}, "covered": [], "log": [], "stopped": None}
    for n in z["frontier"]:
        z["seen"][str(n)] = {"step": 0, "op": "seed", "from": [], "class": classify(n)}
        z["covered"].extend(sorted(class_keys(z["seen"][str(n)]["class"]) - set(z["covered"])))
    return z


# --- 8. the recursion ------------------------------------------------------------------------------------
def recurse(z, path=None):
    required, available = compute_required(z), compute_available(z)
    if not z["frontier"]:
        z["stopped"] = "NOTHING_NEW"
        return z
    if available < required:
        z["stopped"] = f"INSUFFICIENT_COMPUTE (step {z['step'] + 1} needs {required}, {available} left)"
        return z
    z["used"] += required                                 # reserve
    ops = generate_operators(z)
    expansions, errors = expand(z, ops)
    new = merge(z, expansions)
    covered_before = len(z["covered"])
    z = update_priorities(z, new)
    z["step"] += 1
    z["log"].append({"step": z["step"], "operations": required, "new_numbers": len(new),
                     "new_classes": len(z["covered"]) - covered_before, "errors": errors[:5]})
    checkpoint(z, path)
    return z


def run(seeds, budget=20000, width=12, steps=None, path=None):
    z = None
    if path and pathlib.Path(path).exists():
        saved = json.loads(pathlib.Path(path).read_text())
        if saved["seeds"] == sorted(set(seeds)) and saved["width"] == width:
            z = saved
            z["budget"] = max(z["budget"], budget)
            z["stopped"] = None
    if z is None:
        z = initial_state(seeds, budget, width)
        checkpoint(z, path)
    while z["stopped"] is None and (steps is None or z["step"] < steps):
        z = recurse(z, path)
    return z


def path_to_seed(z, n):
    chain, key = [], str(n)
    while z["seen"][key]["op"] != "seed":
        e = z["seen"][key]
        chain.append(f"{key} = {e['op']}({', '.join(map(str, e['from']))})")
        key = str(e["from"][0])
    return chain


def report(z):
    lines = [f"seeds {z['seeds']}   steps {z['step']}   numbers reached {len(z['seen'])}   "
             f"operations used {z['used']} of {z['budget']}   stopped: {z['stopped'] or 'step limit'}"]
    for e in z["log"]:
        lines.append(f"  step {e['step']}: {e['operations']} operations, {e['new_numbers']} new numbers, "
                     f"{e['new_classes']} new classes" + (f", errors {e['errors']}" if e["errors"] else ""))
    orbits = sorted(k[6:] for k in z["covered"] if k.startswith("orbit:"))
    lines.append(f"orbits reached ({len(orbits)} of 13 incl. SEAM): {orbits}")
    lines.append(f"digital roots reached: {sorted(int(k[3:]) for k in z['covered'] if k.startswith('dr:'))}")
    for kind in ("twin", "sophie", "safe"):
        hits = sorted(int(k) for k, v in z["seen"].items() if v.get("class", {}).get(kind))
        lines.append(f"{kind} primes reached: {len(hits)}  first: {hits[:10]}")
    first = {}
    for k in sorted(z["seen"], key=lambda k: (z["seen"][k]["step"], int(k))):
        o = z["seen"][k]["class"]["orbit"]
        first.setdefault(o, k)
    lines.append("how each orbit was first reached:")
    for o in sorted(first):
        lines.append(f"  {o:8s} {first[o]:>12s}   " + " <- ".join(path_to_seed(z, int(first[o]))[:4]))
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Unified Operator Module: grow numbers through the owner's operators.")
    ap.add_argument("seeds", nargs="+", type=int)
    ap.add_argument("--budget", type=int, default=20000, help="total operator applications allowed")
    ap.add_argument("--width", type=int, default=12, help="numbers expanded per step (the rest are kept)")
    ap.add_argument("--steps", type=int, default=None)
    ap.add_argument("--checkpoint", default=None, help="state file; rerun with it to resume")
    a = ap.parse_args()
    z = run(a.seeds, a.budget, a.width, a.steps, a.checkpoint)
    print(report(z))
