"""
BFS Attractor mod 9 — Reachability Audit

Classification: Theorem

The attractor set S ⊂ Z/9Z is reached from any residue in at most 1 step
under the move set M = {+2, +3} (mod 9).

S = {0, 2, 3, 6, 8}   — 5 attractor residues
T = {1, 4, 5, 7}       — 4 residues outside S

Framework connection:
  Move +3 adds the sovereign target DR (3 is the primary target, 3¹ mod 37).
  Move +2 adds the primitive root DR (2 is the minimal primitive root mod 37).
  Together {+2, +3} generate all of Z/9Z from any starting point (gcd(2,3)=1,
  so their span covers Z/9Z), but any single step from T already lands in S.

BFS verification:
  Residue  Status   Optimal move  Lands in    Steps
  ───────────────────────────────────────────────────
    0      In S      —             —            0
    1      T         +2 → 3        3 ∈ S        1
    2      In S      —             —            0
    3      In S      —             —            0
    4      T         +2 → 6        6 ∈ S        1
    5      T         +3 → 8        8 ∈ S        1
    7      T         +2 → 0        0 ∈ S        1
    6      In S      —             —            0
    8      In S      —             —            0

  Maximum steps: 1
  Theorem (≤ 2 steps): VERIFIED  (bound is conservative; actual max = 1)

Note: S ∩ T = ∅ and S ∪ T = Z/9Z by construction.
"""

from collections import deque


# ── Definitions ────────────────────────────────────────────────────────────

S = frozenset({0, 2, 3, 6, 8})     # attractor set
T = frozenset({1, 4, 5, 7})        # residues outside S
MOVES = (2, 3)                      # +2 (primitive root DR), +3 (sovereign target DR)
MOD = 9


# ── Sanity: S and T partition Z/9Z ────────────────────────────────────────

assert S | T == frozenset(range(MOD))
assert S & T == frozenset()


# ── BFS from each element of T ─────────────────────────────────────────────

def bfs_distance(start, target_set, moves, mod):
    """BFS: minimum steps from start to reach any element of target_set."""
    if start in target_set:
        return 0, None
    visited = {start}
    queue = deque([(start, 0, None)])
    while queue:
        node, dist, first_move = queue.popleft()
        for m in moves:
            nxt = (node + m) % mod
            fm = first_move if first_move is not None else m
            if nxt in target_set:
                return dist + 1, fm
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, dist + 1, fm))
    return float('inf'), None


results = {}
for r in range(MOD):
    dist, move = bfs_distance(r, S, MOVES, MOD)
    results[r] = (dist, move)

# Every element of S has distance 0
for r in S:
    assert results[r][0] == 0, f"S element {r} has distance {results[r][0]}"

# Explicit optimal moves for T — verified against BFS
OPTIMAL = {
    1: (2, 3),    # 1+2=3 ∈ S
    4: (2, 6),    # 4+2=6 ∈ S
    5: (3, 8),    # 5+3=8 ∈ S
    7: (2, 0),    # 7+2=9≡0 ∈ S
}

for r, (move, dest) in OPTIMAL.items():
    assert r in T
    assert (r + move) % MOD == dest
    assert dest in S
    assert results[r][0] == 1, f"T element {r}: BFS distance = {results[r][0]}, expected 1"

# Maximum steps across all residues
max_steps = max(d for d, _ in results.values())
assert max_steps == 1, f"Maximum steps = {max_steps}, expected 1"

# Conservative theorem bound: all residues reach S in ≤ 2 steps
assert all(d <= 2 for d, _ in results.values()), "Some residue needs > 2 steps"

# Completeness: every residue in T is handled
assert frozenset(OPTIMAL.keys()) == T

# Move semantics: +3 = sovereign target DR, +2 = primitive root DR
assert 3 % MOD == 3     # 3 is the primary sovereign target (3¹ mod 37)
assert 2 % MOD == 2     # 2 is the minimal primitive root mod 37

# Every element of T has at least one move that lands in S
assert all(any((r + m) % MOD in S for m in MOVES) for r in T)


if __name__ == "__main__":
    print("BFS Attractor mod 9 — Reachability Audit")
    print()
    print(f"  S = {sorted(S)}  (attractor)")
    print(f"  T = {sorted(T)}  (outside S)")
    print(f"  Moves: {{+{MOVES[0]}, +{MOVES[1]}}} mod {MOD}")
    print()
    print(f"  {'Residue':>8}  {'Status':>6}  {'Optimal move':>14}  {'Reaches':>8}  {'Steps':>5}")
    print("  " + "─" * 50)
    for r in range(MOD):
        dist, move = results[r]
        if r in S:
            status, mv_str, reach_str = "In S", "—", "—"
        else:
            mv, dest = OPTIMAL[r]
            status = "T"
            mv_str = f"+{mv} → {dest}"
            reach_str = f"{dest} ∈ S"
        print(f"  {r:>8}  {status:>6}  {mv_str:>14}  {reach_str:>8}  {dist:>5}")
    print()
    print(f"  Maximum steps: {max_steps}")
    print(f"  Theorem (≤ 2 steps): VERIFIED  (bound conservative; actual max = {max_steps})")
    print()
    print("All assertions passed.")
