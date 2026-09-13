#!/usr/bin/env python3
"""
Multi-Register State Engine.

Every number that appears gets expanded into the 6 registers automatically,
so nothing is dropped or passed over as background math. Nothing here has to
be flagged by hand.

    python3 engine.py n 34                 one number, all 6 registers
    python3 engine.py trace 27 82 41       a sequence, engine on each
    python3 engine.py collatz 27           full trajectory, engine on each
    python3 engine.py collatz 27 --summary trajectory + triad-state audit
    python3 engine.py matrix               the 9x9 R-matrix, shells, borders
    python3 engine.py blocks 1             the 1B blocks for B=1..9

THE 6 REGISTERS
  1. POSITIONAL VECTOR  string form, digits, length, comma/period tier
  2. COMMUTATIVE FLIP   reverse, reversal difference |N - N_rev| and its dr
  3. INTERNAL SUM       explicit sum of constituent digits
  4. MODULAR REDUCTION  digital root, dr mod 9 in {1..9}
  5. PARTITION FILTER   Triad attractor {3,6,9} vs Dynamic circuit {1,2,4,5,7,8}
  6. HARMONIC TIE       alignment with the triangular cycle 1,3,6,1,6,3,1,9,9

A 7th line reports GF(37) placement (residue and orbit), because this is the
CylicAmp repo and CLAUDE.md's standing analysis requires it. It is labelled
separately and is not one of the 6.

THE TWO OPERATOR TABLES (verified exhaustively, see verify())
  3n+1 by digital root:   dr(n) in {1,4,7} -> 4
                          dr(n) in {2,5,8} -> 7
                          dr(n) in {3,6,9} -> 1
    so 3n+1 can NEVER output a triad root. Forced: 3*dr lands in {3,6,9},
    and +1 carries it to {4,7,1}.

  n/2 by digital root (x5 mod 9, since 2*5 = 10 = 1 mod 9):
      1 -> 5 -> 7 -> 8 -> 4 -> 2 -> 1     the non-triad 6-cycle
      3 <-> 6                              closed 2-cycle in the triad
      9 -> 9                               fixed point

  TRAPDOOR: odd steps land only in {1,4,7}; halving keeps {1,2,4,5,7,8}
  closed. So once a trajectory leaves the triad it can never return.
"""
import sys

P = 37
TRIAD = (3, 6, 9)
CIRCUIT = (1, 2, 4, 5, 7, 8)
ORBITS = {
    'IC': {1, 10, 26}, 'DARK_A': {2, 15, 20}, 'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23}, 'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36}, 'C9': {14, 29, 31},
    'NQR17': {17, 22, 35}, 'SEED': {18, 24, 32}, 'SA_ST_B': {21, 25, 28},
}


def dr(n):
    n = abs(n)
    return 0 if n == 0 else 1 + (n - 1) % 9


def tri(n):
    return n * (n + 1) // 2


def orbit_of(n):
    r = abs(n) % P
    if r == 0:
        return 'SEAM'
    for name, s in ORBITS.items():
        if r in s:
            return name
    raise AssertionError(r)


R_CYCLE = [dr(tri(n)) for n in range(1, 10)]      # 1,3,6,1,6,3,1,9,9


def registers(N, step=None):
    """The 6 registers for N, plus the GF(37) line. Returns a dict."""
    s = str(abs(N))
    rev = int(s[::-1])
    delta = abs(N - rev)
    ds = sum(int(c) for c in s)
    root = dr(N)
    groups = []
    t = s
    while t:
        groups.append(t[-3:])
        t = t[:-3]
    groups.reverse()
    reg = {
        'N': N,
        'string': s,
        'digits': [int(c) for c in s],
        'length': len(s),
        'comma_groups': groups,
        'period_tier': len(groups),
        'reverse': rev,
        'rev_delta': delta,
        'rev_delta_dr': dr(delta) if delta else 0,
        'digit_sum': ds,
        'dr': root,
        'partition': 'TRIAD' if root in TRIAD else 'CIRCUIT',
        'harmonic_positions': [i + 1 for i, v in enumerate(R_CYCLE) if v == root],
        'mod37': abs(N) % P,
        'orbit': orbit_of(N),
    }
    if step is not None:
        reg.update(harmonic_tie(N, step))
    return reg


def harmonic_tie(N, step):
    """
    Register 6's step-relative part.

    The earlier version reported only (dr(N) - R_step) mod 9. That is a
    tautology whenever N IS the triangular number for its step: running the
    engine across the cycle itself printed delta=0 nine times out of nine
    because it could not print anything else. Fixed here three ways:

      - the degenerate case is DETECTED and labelled, not silently zeroed
      - phase_delta measures signed step-distance to the nearest position
        where the cycle actually takes dr(N), which is not degenerate
      - dr(N) in {2,4,5,7,8} has NO tie at all (the cycle only ever takes
        {1,3,6,9}); that returns None rather than a misleading number
    """
    root = dr(N)
    pos = ((step - 1) % 9) + 1                      # cycle has period 9 in n
    aligns = [i + 1 for i, v in enumerate(R_CYCLE) if v == root]
    out = {
        'step': step,
        'cycle_pos': pos,
        'T_n': tri(step),
        'R_n': dr(tri(step)),
        'root_delta': (root - dr(tri(step))) % 9,
        'tautological': N == tri(step),
    }
    if not aligns:
        out['phase_delta'] = None
    else:
        best = None
        for p in aligns:
            d = (p - pos) % 9
            if d > 4:
                d -= 9
            if best is None or (abs(d), d) < (abs(best), best):
                best = d
        out['phase_delta'] = best
    return out


def show(N, step=None):
    g = registers(N, step)
    print(f"[{N}]")
    print(f"  1. POSITIONAL  '{g['string']}'  digits={g['digits']}  "
          f"len={g['length']}  groups={g['comma_groups']}  tier={g['period_tier']}")
    print(f"  2. FLIP        rev={g['reverse']}  |N-rev|={g['rev_delta']}"
          f"  dr(delta)={g['rev_delta_dr']}")
    print(f"  3. SUM         {' + '.join(map(str, g['digits']))} = {g['digit_sum']}")
    print(f"  4. ROOT        dr = {g['dr']}")
    print(f"  5. PARTITION   {g['partition']}"
          f"   ({'attractor {3,6,9}' if g['partition'] == 'TRIAD' else 'circuit {1,2,4,5,7,8}'})")
    if g['harmonic_positions']:
        print(f"  6. HARMONIC    dr={g['dr']} sits at cycle position(s) "
              f"{g['harmonic_positions']} of {R_CYCLE}")
    else:
        print(f"  6. HARMONIC    dr={g['dr']} has NO tie -- the triangular cycle "
              f"{R_CYCLE}\n                 only ever takes values "
              f"{sorted(set(R_CYCLE))}, so 2,4,5,7,8 never align")
    if step is not None:
        print(f"                 step {step} (cycle pos {g['cycle_pos']}): "
              f"T_{step}={g['T_n']}  R={g['R_n']}  root_delta={g['root_delta']}")
        if g['tautological']:
            print(f"                 TAUTOLOGICAL: N is T_{step} itself, so "
                  f"root_delta is 0 by construction, not a measurement")
        if g['phase_delta'] is None:
            print(f"                 phase_delta: none -- dr={g['dr']} never "
                  f"occurs in the cycle, so there is no position to measure to")
        else:
            d = g['phase_delta']
            where = "on an alignment" if d == 0 else \
                    f"{abs(d)} step{'s' if abs(d) > 1 else ''} " \
                    f"{'past' if d < 0 else 'before'} the nearest one"
            print(f"                 phase_delta={d:+d}  ({where})")
    print(f"  -- GF(37)      mod 37 = {g['mod37']}  orbit = {g['orbit']}")


def collatz(n):
    seq = [n]
    while n != 1:
        n = 3 * n + 1 if n % 2 else n // 2
        seq.append(n)
    return seq


def collatz_audit(start):
    seq = collatz(start)
    roots = [dr(v) for v in seq]
    print(f"Collatz from {start}: {len(seq) - 1} steps to 1\n")
    print("  step  value        dr  partition  op")
    for k, v in enumerate(seq):
        op = "start" if k == 0 else (f"3({seq[k-1]})+1" if seq[k - 1] % 2
                                      else f"{seq[k-1]}/2")
        part = "TRIAD" if roots[k] in TRIAD else "circuit"
        mark = "  <- expulsion" if k > 0 and roots[k - 1] in TRIAD and roots[k] not in TRIAD else ""
        if k <= 16 or k >= len(seq) - 4:
            print(f"  {k:>4}  {v:<12} {roots[k]}   {part:<9}  {op}{mark}")
        elif k == 17:
            print(f"  ...   ...          ...  ...")
    triad_steps = [k for k, r in enumerate(roots) if r in TRIAD]
    print(f"\n  steps with a TRIAD root: {triad_steps}")
    print(f"  distinct roots after step 0: {sorted(set(roots[1:]))}")
    print(f"  re-entered the triad after leaving: "
          f"{any(roots[k] in TRIAD for k in range(1, len(roots)))}")
    print(f"  terminal tail: {seq[-4:]}")
    return seq


def build_matrix():
    """M[i][j] = dr(R_i + R_j), 1-indexed over the triangular root cycle."""
    return [[dr(R_CYCLE[i] + R_CYCLE[j]) for j in range(9)] for i in range(9)]


def matrix_report():
    M = build_matrix()
    print(f"R vector (dr of T_n, n=1..9): {R_CYCLE}")
    print(f"M[i][j] = dr(R_i + R_j)\n")
    print("        " + "  ".join(f"C{j+1}({R_CYCLE[j]})" for j in range(9)))
    for i in range(9):
        print(f"  R{i+1}({R_CYCLE[i]})  " + "     ".join(str(v) for v in M[i]))

    def ring(r):
        return [M[i][j] for i in range(9) for j in range(9)
                if max(abs(i - 4), abs(j - 4)) == r]

    def core(r):
        return [M[i][j] for i in range(9) for j in range(9)
                if max(abs(i - 4), abs(j - 4)) <= r]

    print("\n  CONCENTRIC SHELLS (Chebyshev radius from centre (5,5))")
    print("   r  scope        cells   ring sum  dr    core sum  dr")
    for r in range(5):
        rs, cs = sum(ring(r)), sum(core(r))
        scope = f"{2*r+1}x{2*r+1}"
        print(f"   {r}  {scope:<11}  {len(ring(r)):>5}   {rs:>7}  {dr(rs)}    "
              f"{cs:>7}   {dr(cs)}")
    print(f"\n  shell root pulse:      {[dr(sum(ring(r))) for r in range(5)]}")
    print(f"  cumulative core roots: {[dr(sum(core(r))) for r in range(5)]}")

    edges = {
        'top': sum(M[0]), 'bottom': sum(M[8]),
        'left': sum(M[i][0] for i in range(9)),
        'right': sum(M[i][8] for i in range(9)),
    }
    corners = [M[0][0], M[0][8], M[8][0], M[8][8]]
    print(f"\n  BORDERS")
    for k, v in edges.items():
        print(f"   {k:<7} sum {v:>3}  dr {dr(v)}")
    print(f"   corners {corners} sum {sum(corners)} dr {dr(sum(corners))}")
    print(f"   perimeter ring (32 cells) {sum(ring(4))} dr {dr(sum(ring(4)))}")
    print(f"   7x7 core {sum(core(3))} dr {dr(sum(core(3)))}"
          f"   -> {sum(ring(4))} + {sum(core(3))} = {sum(ring(4)) + sum(core(3))}")

    print(f"\n  DIAGONALS")
    for lo, hi, lab in ((3, 6, '3x3'), (2, 7, '5x5'), (1, 8, '7x7'), (0, 9, '9x9')):
        m = sum(M[i][i] for i in range(lo, hi))
        a = sum(M[i][8 - i] for i in range(lo, hi))
        print(f"   {lab}  main {m:>3} dr {dr(m)}   anti {a:>3} dr {dr(a)}"
              f"   {'(equal)' if m == a else ''}")
    print(f"\n  symmetric (M[i][j]=M[j][i]): "
          f"{all(M[i][j] == M[j][i] for i in range(9) for j in range(9))}")


def blocks(lead=1):
    print(f"  {lead}B blocks, B = 1..9")
    for B in range(1, 10):
        base = int(f"{lead}{B}")
        flip = int(f"{B}{lead}")
        print(f"   {base}  {base}  {flip}(flip)   {lead}+{B} = {lead+B} -> dr {dr(lead+B)}"
              f"   |flip-base| = {abs(flip-base)}")
    print(f"   root progression: {[dr(lead + B) for B in range(1, 10)]}")


def verify():
    """Every claim this engine encodes, asserted. Fails loudly."""
    M = build_matrix()

    def ring(r):
        return [M[i][j] for i in range(9) for j in range(9)
                if max(abs(i - 4), abs(j - 4)) == r]

    def core(r):
        return [M[i][j] for i in range(9) for j in range(9)
                if max(abs(i - 4), abs(j - 4)) <= r]

    assert R_CYCLE == [1, 3, 6, 1, 6, 3, 1, 9, 9]
    assert M[4][4] == 3
    assert [M[i][3:6] for i in range(3, 6)] == [[2, 7, 4], [7, 3, 9], [4, 9, 6]]
    assert M[1][1:8] == [6, 9, 4, 9, 6, 4, 3]
    assert M[7][1:8] == [3, 6, 1, 6, 3, 1, 9]
    assert all(M[i][j] == M[j][i] for i in range(9) for j in range(9))

    assert [len(ring(r)) for r in range(5)] == [1, 8, 16, 24, 32]
    assert [sum(ring(r)) for r in range(5)] == [3, 48, 83, 119, 125]
    assert [sum(core(r)) for r in range(5)] == [3, 51, 134, 253, 378]
    assert [dr(sum(ring(r))) for r in range(5)] == [3, 3, 2, 2, 8]
    assert [dr(sum(core(r))) for r in range(5)] == [3, 6, 8, 1, 9]
    assert sum(ring(4)) + sum(core(3)) == 378

    assert sum(M[0]) == 30 and sum(M[8]) == 39
    assert sum(M[i][0] for i in range(9)) == 30
    assert sum(M[i][8] for i in range(9)) == 39
    assert all(dr(v) == 3 for v in (30, 39))
    assert [M[0][0], M[0][8], M[8][0], M[8][8]] == [2, 1, 1, 9]
    assert dr(2 + 1 + 1 + 9) == 4

    assert sum(M[i][i] for i in range(3, 6)) == sum(M[i][5 - i + 3] for i in range(3, 6)) == 11
    assert sum(M[i][i] for i in range(1, 8)) == sum(M[i][8 - i] for i in range(1, 8)) == 31
    assert dr(sum(M[i][i] for i in range(2, 7))) == dr(sum(M[i][8 - i] for i in range(2, 7))) == 7

    # operator tables
    for d in range(1, 10):
        outs = {dr(3 * n + 1) for n in range(1, 3000) if dr(n) == d}
        assert outs == {4 if d in (1, 4, 7) else 7 if d in (2, 5, 8) else 1}
        assert not (outs & set(TRIAD))
    h = [1]
    for _ in range(6):
        h.append(dr(5 * h[-1]))
    assert h == [1, 5, 7, 8, 4, 2, 1]
    assert dr(5 * 3) == 6 and dr(5 * 6) == 3 and dr(5 * 9) == 9

    # trapdoor, on a real trajectory
    seq = collatz(27)
    assert len(seq) - 1 == 111
    assert seq[:8] == [27, 82, 41, 124, 62, 31, 94, 47]
    assert seq[-4:] == [8, 4, 2, 1]
    assert dr(27) == 9
    assert not any(dr(v) in TRIAD for v in seq[1:])

    # repo ties
    assert 111 == 3 * 37 and 999 // 37 == 27

    # --- register 6: the fix ---
    # every triangular number at its own step is flagged, not silently zeroed
    for n in range(1, 40):
        h = harmonic_tie(tri(n), n)
        assert h['tautological'] is True
        assert h['root_delta'] == 0                  # 0 BY CONSTRUCTION here
        assert h['phase_delta'] == 0                 # it does sit on an alignment
    # a value that is not its step's triangular number is not flagged
    assert harmonic_tie(82, 1)['tautological'] is False
    assert harmonic_tie(34, 4)['tautological'] is False
    # roots outside {1,3,6,9} have no tie at all, and say so
    assert sorted(set(R_CYCLE)) == [1, 3, 6, 9]
    for N in (34, 41, 5, 2, 8):
        assert dr(N) not in (1, 3, 6, 9)
        assert harmonic_tie(N, 4)['phase_delta'] is None
    # phase_delta is a real signed distance, not always 0
    assert harmonic_tie(82, 3)['phase_delta'] == 1      # dr 1 aligns at 1,4,7
    assert harmonic_tie(82, 5)['phase_delta'] == -1
    assert harmonic_tie(82, 1)['phase_delta'] == 0
    assert {harmonic_tie(82, s)['phase_delta'] for s in range(1, 10)} == {-1, 0, 1}
    # period 9 in the step index
    for s in range(1, 30):
        assert harmonic_tie(82, s)['phase_delta'] == harmonic_tie(82, s + 9)['phase_delta']
    print("engine.verify(): all assertions passed")


USAGE = __doc__

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(USAGE)
    elif a[0] == "n":
        for x in a[1:]:
            show(int(x))
            print()
    elif a[0] == "trace":
        for k, x in enumerate(a[1:]):
            show(int(x), step=k + 1)
            print()
    elif a[0] == "collatz":
        collatz_audit(int(a[1]))
    elif a[0] == "matrix":
        matrix_report()
    elif a[0] == "blocks":
        blocks(int(a[1]) if len(a) > 1 else 1)
    elif a[0] == "verify":
        verify()
    else:
        print(USAGE)
