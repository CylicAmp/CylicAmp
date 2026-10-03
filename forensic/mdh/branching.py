"""Maximum-weight branching (Edmonds / Chu-Liu), without weight inversion.

The spec's Stage 4 turned maximisation into minimisation with
w'(e) = W + eps - w(e). That is only equivalent when every feasible answer has
the same number of edges (a spanning arborescence). With vertices that have no
admissible in-edge (kept by AT-07, no synthetic edges allowed) the answer is a
branching of variable size, and the inverted problem prefers the EMPTY branching.

Here the maximum branching is computed directly: a virtual root R gets a
0-weight edge to every vertex, a maximum spanning arborescence rooted at R is
found, and every edge out of R is dropped. Those virtual edges never appear in
the output, so no synthetic edge is emitted. Only edges with weight > 0 are
useful in a maximum branching; weight-0 real edges are left to the tie rule.
"""

VIRTUAL_ROOT = ("__virtual_root__",)


def _max_arborescence(nodes, edges, root):
    """edges: list of (u, v, w, key). Returns list of selected edge keys."""
    # best incoming edge per non-root node
    best = {}
    for (u, v, w, key) in edges:
        if v == root or u == v:
            continue
        if v not in best or (w, _neg(key)) > (best[v][2], _neg(best[v][3])):
            best[v] = (u, v, w, key)
    # find a cycle among chosen edges
    parent = {v: e[0] for v, e in best.items()}
    cycle = None
    colour = {}
    for start in nodes:
        path = []
        x = start
        while x is not None and x not in colour:
            colour[x] = start
            path.append(x)
            x = parent.get(x)
        if x is not None and colour.get(x) == start:
            i = path.index(x)
            cycle = path[i:]
            break
    if cycle is None:
        return [e[3] for e in best.values()]
    cyc = set(cycle)
    c = ("__cycle__", len(nodes), tuple(sorted(map(repr, cycle))))
    new_nodes = [n for n in nodes if n not in cyc] + [c]
    new_edges = []
    origin = {}
    for (u, v, w, key) in edges:
        if u in cyc and v in cyc:
            continue
        if v in cyc:
            nw = w - best[v][2]
            new_edges.append((u, c, nw, key))
            origin[key] = ("in", v)
        elif u in cyc:
            new_edges.append((c, v, w, key))
            origin[key] = ("out", None)
        else:
            new_edges.append((u, v, w, key))
            origin[key] = ("plain", None)
    chosen = _max_arborescence(new_nodes, new_edges, root)
    result = []
    entered = None
    for key in chosen:
        kind, target = origin[key]
        if kind == "in":
            entered = target
        result.append(key)
    for v in cycle:
        if v != entered:
            result.append(best[v][3])
    return result


def _neg(key):
    # deterministic tie-break: smaller canonical key wins
    return tuple(-ord(ch) for ch in str(key))


def maximum_branching(nodes, edges):
    """nodes: iterable of hashable ids. edges: list of (u, v, weight, key) with a
    unique, totally ordered key (the canonical edge id). Returns the set of keys
    of a maximum-weight branching (each node <= 1 in-edge, no cycles)."""
    nodes = list(nodes)
    aug = [e for e in edges if e[2] > 0]
    for n in nodes:
        aug.append((VIRTUAL_ROOT, n, 0.0, ("~virtual", str(n))))
    keys = _max_arborescence([VIRTUAL_ROOT] + nodes, aug, VIRTUAL_ROOT)
    real = {e[3] for e in edges}
    return {k for k in keys if k in real}
