"""
zero_fill_bridge_audit.py

The fill/bridge operation: transferring units from value positions into zeros.

─────────────────────────────────────────────────────────────────
RULES:
  0 = space, no value
  1 = one unit; fills exactly one 0-space

FILL STEP:
  Find the first adjacent (nonzero, 0) pair left-to-right.
  Transfer 1 unit from the nonzero position into the 0:
    (a, 0) → (a-1, 1)

CASES:
  (1, 0) → (0, 1)   perfect fit: 1 fills 0 exactly, 0 leftover
  (2, 0) → (1, 1)   bridge: 1 fills 0, 1 leftover; bridge made and crossed

BRIDGE MECHANISM:
  2 sends 1 unit to fill the 0 → 0 becomes 1 (bridge built).
  The remaining 1 now has a connection to cross.
  Result: (1, 1) — both positions equal.

CONSERVATION:
  sum(state) is invariant under every fill step.
  DR(sum) is invariant throughout.

EQUILIBRIUM:
  Starting (n, 0^(n-1)): n units at one position, n-1 zeros.
  Iterated fill → (1^n) = repunit_n.
  The repunit is the unique equilibrium.

STEP COUNT:
  Steps to reach (1^n) from (n, 0^(n-1)) = T(n-1) = n(n-1)/2.
  These are the triangular numbers.

  n=1:  0 steps  (already repunit)
  n=2:  1 step
  n=3:  3 steps
  n=4:  6 steps
  n=5:  10 steps
  n=6:  15 steps
  n=7:  21 steps
  n=8:  28 steps
  n=9:  36 steps  (T(8) = 36; DR(36) = 9)

CONNECTION TO REPUNIT IDENTITY:
  DR(repunit_n) = n  (from doubling_dr_cycle_audit.py)
  The fill process starts with sum=n (DR=n) and ends at repunit_n (DR=n).
  DR is conserved entry-to-exit.
─────────────────────────────────────────────────────────────────
"""

FAIL = []


def check(cond, label, actual, expected):
    if not cond:
        FAIL.append(f"{label}: actual={actual!r}, expected={expected!r}")
    return cond


def dr(n):
    if n == 0:
        return 0
    r = n % 9
    return r if r else 9


def fill_step(state):
    """Transfer 1 unit from first (nonzero, 0) adjacent pair."""
    s = list(state)
    for i in range(len(s) - 1):
        if s[i] > 0 and s[i + 1] == 0:
            s[i] -= 1
            s[i + 1] += 1
            return tuple(s), True
    return tuple(s), False


def fill_chain(start):
    """Run fill steps to equilibrium; return list of all states."""
    states = [tuple(start)]
    while True:
        ns, changed = fill_step(states[-1])
        if not changed:
            break
        states.append(ns)
    return states


# ── Core fill operation ───────────────────────────────────────────────────────

check(fill_step((1, 0))[0] == (0, 1), "fill(1,0)=(0,1)", fill_step((1, 0))[0], (0, 1))
check(fill_step((2, 0))[0] == (1, 1), "fill(2,0)=(1,1)", fill_step((2, 0))[0], (1, 1))
check(fill_step((3, 0))[0] == (2, 1), "fill(3,0)=(2,1)", fill_step((3, 0))[0], (2, 1))

# fill(1,1): no zeros → no change
check(fill_step((1, 1))[1] == False, "fill(1,1): no change", fill_step((1, 1))[1], False)


# ── Sum (and DR) conservation ─────────────────────────────────────────────────

for a in range(1, 10):
    before = (a, 0)
    after, _ = fill_step(before)
    check(sum(before) == sum(after), f"sum conserved a={a}", sum(before), sum(after))
    check(dr(sum(before)) == dr(sum(after)), f"DR conserved a={a}", dr(sum(before)), dr(sum(after)))


# ── Perfect fit: (1, 0) → (0, 1) ─────────────────────────────────────────────

check(fill_step((1, 0))[0] == (0, 1), "perfect fit", fill_step((1, 0))[0], (0, 1))
check(sum((0, 1)) == 1, "perfect fit sum=1", sum((0, 1)), 1)


# ── Bridge: (2, 0) → (1, 1) ──────────────────────────────────────────────────

result_2_0, changed = fill_step((2, 0))
check(result_2_0 == (1, 1), "bridge (2,0)→(1,1)", result_2_0, (1, 1))
check(changed, "bridge changed", changed, True)
check(sum(result_2_0) == 2, "bridge sum=2", sum(result_2_0), 2)
# Both positions equal after bridge
check(result_2_0[0] == result_2_0[1], "bridge equalizes", result_2_0[0], result_2_0[1])


# ── Equilibrium: (n, 0^(n-1)) → (1^n) ────────────────────────────────────────

for n in range(1, 10):
    start = (n,) + (0,) * (n - 1)
    chain = fill_chain(start)
    eq = chain[-1]
    repunit = (1,) * n
    check(eq == repunit, f"eq n={n} → repunit", eq, repunit)

    # DR preserved throughout
    for state in chain:
        check(dr(sum(state)) == n % 9 or (n == 9 and dr(sum(state)) == 9),
              f"DR={n} preserved n={n}", dr(sum(state)), n if n < 9 else 9)


# ── Step count = T(n-1) = n(n-1)/2 ──────────────────────────────────────────

STEP_COUNTS = {}
for n in range(1, 10):
    start = (n,) + (0,) * (n - 1)
    chain = fill_chain(start)
    STEP_COUNTS[n] = len(chain) - 1

TRIANGULAR = {n: n * (n - 1) // 2 for n in range(1, 10)}

for n in range(1, 10):
    check(
        STEP_COUNTS[n] == TRIANGULAR[n],
        f"steps n={n} = T({n-1})",
        STEP_COUNTS[n],
        TRIANGULAR[n],
    )

# T(8) = 36 for n=9
check(TRIANGULAR[9] == 36, "T(8)=36", TRIANGULAR[9], 36)
check(dr(36) == 9, "DR(36)=9", dr(36), 9)


# ── DR of step counts ─────────────────────────────────────────────────────────

STEP_DRS = [dr(TRIANGULAR[n]) for n in range(1, 10)]
check(STEP_DRS == [0, 1, 3, 6, 1, 6, 3, 1, 9], "DR of step counts", STEP_DRS, [0, 1, 3, 6, 1, 6, 3, 1, 9])


# ── Excess zeros: (2, 0, 0) → (0, 1, 1) ──────────────────────────────────────

chain_200 = fill_chain((2, 0, 0))
check(chain_200[-1] == (0, 1, 1), "(2,0,0)→(0,1,1)", chain_200[-1], (0, 1, 1))
check(sum(chain_200[-1]) == 2, "(2,0,0) sum=2", sum(chain_200[-1]), 2)


# ── Repunit connection ────────────────────────────────────────────────────────

# DR(repunit_n) = n — verified in doubling_dr_cycle_audit.py
# Fill process: start DR=n, end DR=n. The repunit is the equilibrium.
for n in range(1, 10):
    repunit_val = int('1' * n)
    check(dr(repunit_val) == n, f"DR(repunit_{n})={n}", dr(repunit_val), n)


# ── Output ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Zero Fill Bridge Audit")
    print("=" * 62)

    print(f"\n── Core fill step: (a, 0) → (a-1, 1) ──")
    for a in range(1, 5):
        after, _ = fill_step((a, 0))
        note = "perfect fit" if a == 1 else "bridge" if a == 2 else ""
        print(f"  ({a}, 0) → {after}   sum={a}  DR={dr(a)}  {note}")

    print(f"\n── Equilibration to repunit ──")
    print(f"  {'start':20s}  {'steps':>5}  {'end':20s}  DR")
    for n in range(1, 10):
        start = (n,) + (0,) * (n - 1)
        chain = fill_chain(start)
        eq = chain[-1]
        print(f"  {str(list(start)):20s}  {len(chain)-1:>5}  {str(list(eq)):20s}  {dr(n)}")

    print(f"\n── Step counts = T(n-1) = n(n-1)/2 ──")
    for n in range(1, 10):
        t = TRIANGULAR[n]
        print(f"  n={n}: T({n-1}) = {t:>2}  DR={dr(t)}")
    print(f"  T(8) = 36: steps to fill all 9 positions; DR(36)=9")

    print(f"\n── n=5 chain (all states) ──")
    for i, state in enumerate(fill_chain((5, 0, 0, 0, 0))):
        print(f"  step {i:>2}: {list(state)}  sum={sum(state)}")

    print(f"\n── Excess zeros: (2, 0, 0) → (0, 1, 1) ──")
    for i, state in enumerate(chain_200):
        print(f"  step {i}: {list(state)}")
    print(f"  Units push rightward into empty space.")

    print()
    if FAIL:
        print(f"FAILED ({len(FAIL)}):")
        for f in FAIL:
            print(f"  ✗  {f}")
        import sys; sys.exit(1)
    else:
        print("All assertions passed.")
