# CLASS: AUDIT
"""
Langton's ant highway: Michael Warren Song's results, re-run (owner_work #276, 2026-10-14).

THE OWNER'S LINE, verbatim. It is the owner's message in the owner's Egor chat, shown in
the screenshot attached to #276
(owner_work/images/2026-10-14_276_egor_langton_screenshot.jpg):

    I know no more of my Langdon ants or my collaze conjectures 3+1 proves no even mentions

typo: "Langdon ants" for Langton's ant. typo: "collaze conjectures 3+1" for the
Collatz conjecture (3n+1). The correct names are used from here on.

THE OWNER'S RESULTS, as shown in the same screenshot: the owner's Langton's ant work
("my Langdon ants"), computed in the owner's own Egor project (egor_v18_project,
igor_langton_mask_v18.py) and laid out there as this table:

    Highway onset                  Step 9,976
    Highway movement period        104 steps
    Displacement per period        (-2, +2)
    Odd-flip mask                  34 cells
    Black-cell growth              +12 per completed cycle
    Simulation horizon             5,000,000 steps
    Black cells at 5,000,000       576,486
    "The conditional formula for completed highway cycles is
         B(n) = 714 + 12n,   n >= 2."
    "Infinite continuation remains unproved."

THE OWNER'S EGOR COMMANDS IN owner_work #223 (2026-10-10), verbatim. #223 opens with the
first block and ends with the second; a pasted PyPI / C-extension text sits between
them, so the trailing backslash of the first block continues into "--csv
boundaries.csv". #223 shows the commands only, not their output:

    cd egor_v18_project

    python3 igor_langton_mask_v18.py \
      --steps 5000000 \
      --out verification.json \

    [... pasted PyPI / C-extension text ...]

      --csv boundaries.csv

    python3 egor_v18.py
    python3 -m unittest discover -q

egor_v18_project is not in this repository, so the numbers are re-derived from
the rule itself below. igor_langton_mask_v18.py's coordinate and heading
conventions are unknown here (that matters only for the sign of the shift).

CONVENTION (Langton 1986; Wikipedia "Langton's ant"):
  At a white square, turn 90 degrees right (clockwise), flip the square, then step forward.
  At a black square, turn 90 degrees left, flip the square, then step forward.
  The grid starts all white. The ant starts at (0,0) heading north, with x to the right
  and y UP (math axes). pos(t) is the position after t moves (pos(0) = origin).
  Move m (m = 1, 2, ...) goes from pos(m-1) to pos(m). B(t) is the number of black cells after t moves.

REPRODUCTION. The default run covers 200,000 steps plus the induction proof below.
--full also runs all 5,000,000 steps directly, in about 3.3 s of plain Python.
The default run takes about 0.3 s.

  claim                     reproduced                                         verdict
  onset step 9,976          pos(t+104) - pos(t) is constant for every            holds
                            t >= 9976 and not at t = 9975. So moves 9977, 9978,
                            ... repeat every 104 moves. "After 9,976 moves"
                            and "the 9,977th move" are the same event.
  period 104                104 is the least period (no divisor 1..103 works)  holds
  shift (-2,+2)             depends on the start heading and the y axis:     holds for
                            heading N, y up    -> (-2,-2)                       (N, y down)
                            heading E, y up    -> (-2,+2)                       or (E, y up)
                            heading S, y up    -> (+2,+2)
                            heading W, y up    -> (+2,-2)
                            heading N, y DOWN  -> (-2,+2)  (screen/array rows)
  odd-flip mask 34          cells flipped an odd number of times in a period     holds for
                            window [9976+104k, 9976+104(k+1)): 34, for every k   windows starting
                            >= 0 (the same 34 offsets in each window). Each      at the onset phase
                            window visits 41 distinct cells 104 times, with      (the size depends on
                            multiplicities 1:14, 2:1, 3:18, 4:6, 5:2. Windows    the phase)
                            starting at other phases have masks of 28 to 42
                            cells. 34 occurs in 13 of the 104 phases.
  +12 per cycle             B(t+104) - B(t) = 12 for every t >= 9977. The         holds from
                            first window [9976, 10080] gains only +10: its first  t = 9977
                            cell, pos(9976) = (-14,10) (window offset (0,0), not
                            the origin), is flipped once, black-to-white there,
                            and its translate is white-to-black in every later
                            window (22/12 flips, then 23/11).
  B at 5,000,000 = 576,486  5,000,000 - 9,976 = 4,990,024 = 104 * 47,981 exactly, holds
                            so n = 47,981. 714 + 12*47,981 = 576,486. The direct
                            5,000,000-step run (--full) gives 576,486.
  B(n)=714+12n, n>=2        B(9976+104n) = 714+12n holds for EVERY n >= 1,       holds, but n >= 2
                            and fails only at n = 0 (B(9976) = 716, not 714).    is not sharp:
                            It is checked at every cycle to 5,000,000 (--full)   it holds from n = 1
                            and proved for all n >= 1 below.
  "infinite continuation    For THIS start (the all-white grid), it is proved   the statement is wrong
   remains unproved"        below by induction from a finite check (base case:   for this start;
                            periods 0..5).                                       see PROVED / OPEN

OUTSIDE PRIOR ART (checked 2026-10-14):
  OEIS A255938 ("Langton's ant walk: number of black cells on the infinite grid after
    the ant moves n times", A. Wesolowski 2015). The b-file, n = 0..20000, matches
    simulate() term for term (checked while writing this file; the b-file is not
    fetched at run time). Its formula
    "a(n+104) = a(n) + 12 for n > 9976" (A. Zabolotskiy, 2016) is the +12 line above,
    with the same threshold, 9977. A255938 is B(t). The owner's 714 + 12n is the same
    line, read only at cycle boundaries.
  OEIS A126978: a(n) = 104n + 9977, "Langton's Ant Superhighway, the start point (9977th
    iteration, J. Propp) and the period length for the Superhighway (104)." So Propp's 9977 counts the first
    highway MOVE and the owner's 9,976 counts the moves made BEFORE it. These are the same onset.
  Wikipedia "Langton's ant": "The ant traces a pseudo-random path until around 10,000
    steps"; "the ant starts building a recurrent 'highway' pattern of 104 steps that
    repeats indefinitely". Highways from every finite start: "no one has been able to
    prove that this is true for all such initial configurations. It is only known that
    the ant's trajectory is always unbounded regardless of the initial configuration"
    (Bunimovich and Troubetzkoy, J. Stat. Phys. 67 (1992) 289-302); Wikipedia adds that
    "this result was incorrectly attributed and is known as the Cohen-Kong theorem".
  How the methods differ: OEIS states the +12 recurrence for every step n > 9976 and
  Propp states the onset as a move number. The owner reads B only at cycle
  boundaries. It adds the odd-flip mask (34 cells), which is the mechanism behind the
  +12: 23 white-to-black flips minus 11 black-to-white flips.

PROVED / OPEN (exact statement):
  PROVED (Bunimovich-Troubetzkoy 1992): the trajectory is unbounded for EVERY initial
    configuration. This does NOT say a highway forms.
  PROVED HERE, for the all-white start only: the moves are 104-periodic with shift s
    for ALL t >= 9976, forever, and B(9976+104n) = 714 + 12n for ALL n >= 1.
    Proof (prove_forever below). Let T_k = 9976 + 104k and p_k = pos(T_k). Let U be the
    offsets visited in period 0, and C the cells visited before 9976. Period k is decided
    by the heading at T_k and the colours at T_k on p_k + U. Suppose periods 0..k-1
    repeat period 0. Then the colour of p_k + v is
    [visits from C] + #{(u, i): u in U, 1 <= i <= k, u - v = i*s} (mod 2).
    For k >= 5, p_k + U misses C (projection onto s; computed below; this bound is
    sufficient, not sharp: direct set intersection shows p_k + U already misses C
    for every k >= 2). The largest
    such i is D = 2. So for k >= 5 the colours on the window are one fixed pattern f,
    independent of k, and the heading is the heading at the end of period k-1. Period k
    therefore repeats period 5. The base case, periods 0..5, is simulated. The
    induction covers every k. The same argument fixes each period's net change at +12.
    The argument is general: a highway that has moved past the region the chaotic
    phase visited runs on blank cells and can never stop. Neither Wikipedia nor
    OEIS A255938 or A126978 cites a written proof of this argument. Wikipedia states
    "repeats indefinitely" without one.
  OPEN: the highway conjecture, that EVERY finite initial configuration eventually
    builds a highway (Wikipedia, as quoted above).
"""
import sys
from collections import Counter

PERIOD = 104
ONSET = 9976                 # the owner's number; asserted below, not assumed
HORIZON_EGOR = 5_000_000
B_EGOR_5M = 576_486


def simulate(n_steps, heading=(0, 1), y_down=False):
    """Langton's ant from an all-white grid. Returns per-time lists:
    xs[t], ys[t] = pos(t); B[t] = black cells after t moves; col[t] = colour read at
    pos(t) before move t+1 (1 = black)."""
    black = set()
    x = y = 0
    dx, dy = heading
    xs = [0] * (n_steps + 1); ys = [0] * (n_steps + 1)
    B = [0] * (n_steps + 1); col = [0] * n_steps
    nb = 0
    # right turn (clockwise as drawn): y up: (dx,dy)->(dy,-dx); y down: (dx,dy)->(-dy,dx)
    for t in range(n_steps):
        k = (x, y)
        if k in black:
            col[t] = 1
            dx, dy = ((dy, -dx) if y_down else (-dy, dx))      # left
            black.discard(k); nb -= 1
        else:
            dx, dy = ((-dy, dx) if y_down else (dy, -dx))      # right
            black.add(k); nb += 1
        x += dx; y += dy
        xs[t + 1] = x; ys[t + 1] = y; B[t + 1] = nb
    return xs, ys, B, col


def onset_and_shift(xs, ys, period):
    """Smallest t0 with pos(t+period)-pos(t) constant for all t0 <= t <= N-period."""
    N = len(xs) - 1
    sx = xs[N] - xs[N - period]; sy = ys[N] - ys[N - period]
    t = N - period
    while t >= 0 and xs[t + period] - xs[t] == sx and ys[t + period] - ys[t] == sy:
        t -= 1
    return t + 1, (sx, sy)


def window(xs, ys, col, start):
    """Flips in [start, start+104): Counter of offsets from pos(start), plus the
    set of odd-flipped offsets and how many of those go white->black."""
    p = (xs[start], ys[start])
    c = Counter(); first = {}
    for t in range(start, start + PERIOD):
        o = (xs[t] - p[0], ys[t] - p[1])
        c[o] += 1
        first.setdefault(o, col[t])
    odd = {o for o, m in c.items() if m % 2}
    w2b = sum(1 for o in odd if first[o] == 0)   # odd count: final flip = first flip direction
    return c, odd, w2b


def prove_forever(xs, ys, col, T0, s):
    """Induction certificate (see docstring). Returns K* = max(1, K_disjoint, D)."""
    dot = lambda a, b: a[0] * b[0] + a[1] * b[1]
    p0 = (xs[T0], ys[T0])
    C = {(xs[t], ys[t]) for t in range(T0)}
    U = [(xs[T0 + j] - p0[0], ys[T0 + j] - p0[1]) for j in range(PERIOD)]
    Us = set(U)
    s2 = dot(s, s)
    maxC = max(dot(c, s) for c in C)
    minW = min(dot((p0[0] + u[0], p0[1] + u[1]), s) for u in Us)
    Kd = 0
    while minW + Kd * s2 <= maxC:          # for k >= Kd every window cell projects past all of C
        Kd += 1
    D = 0
    for u in Us:
        for v in Us:
            d = (u[0] - v[0], u[1] - v[1])
            if d[0] * s[1] == d[1] * s[0] and dot(d, s) > 0 and dot(d, s) % s2 == 0:
                D = max(D, dot(d, s) // s2)
    Kstar = max(1, Kd, D)
    # f(v): colour on the window predicted by the formula for any k >= Kstar
    flips = Counter(U)
    f = {v: sum(flips[(v[0] + i * s[0], v[1] + i * s[1])] for i in range(1, D + 1)) % 2
         for v in Us}
    # null control: the formula must reproduce the simulated colours at T_k, k = Kstar..Kstar+40
    for k in range(Kstar, Kstar + 41):
        Tk = T0 + PERIOD * k
        for j in range(PERIOD):
            v = U[j]
            # colour read at T_k+j equals colour at T_k unless visited earlier in the period
            if U.index(v) == j:
                assert col[Tk + j] == f[v], (k, j, v)
    return Kd, D, Kstar, len(C)


def full_run(n_steps, T0, s, period=PERIOD):
    """Stream 5,000,000 steps: assert the shift at every t >= T0 and B(n) = 714 + 12n at
    every completed cycle n >= 1. Returns the final black count."""
    black = set(); x = y = 0; dx, dy = 0, 1; nb = 0
    ring = [None] * (period + 1)
    checked_cycles = 0
    for t in range(n_steps + 1):
        ring[t % (period + 1)] = (x, y)
        if t >= T0 + period:
            px, py = ring[(t - period) % (period + 1)]
            assert (x - px, y - py) == s, t
        if t >= T0 and (t - T0) % period == 0:
            n = (t - T0) // period
            if n >= 1:
                assert nb == 714 + 12 * n, (t, n, nb)
                checked_cycles += 1
        if t == n_steps:
            break
        k = (x, y)
        if k in black:
            dx, dy = -dy, dx; black.discard(k); nb -= 1
        else:
            dx, dy = dy, -dx; black.add(k); nb += 1
        x += dx; y += dy
    return nb, checked_cycles


def main(full=False):
    N = 200_000
    xs, ys, B, col = simulate(N)

    # onset, period, shift
    T0, s = onset_and_shift(xs, ys, PERIOD)
    assert T0 == ONSET == 9976 and s == (-2, -2)
    for q in range(1, PERIOD):                       # 104 is the least period
        if PERIOD % q == 0:
            assert onset_and_shift(xs, ys, q)[0] > N // 2, q
    # move-number form (Propp / A126978): first periodic move is 9977
    first_move = T0 + 1
    assert first_move == 9977
    # turn (colour-read) sequence becomes periodic one step later
    t = N - 1 - PERIOD
    while t >= 0 and col[t] == col[t + PERIOD]:
        t -= 1
    assert t + 1 == 9977

    # shift vs heading and axis orientation
    shifts = {}
    for name, h, yd in [("N", (0, 1), False), ("E", (1, 0), False), ("S", (0, -1), False),
                        ("W", (-1, 0), False), ("N, y down", (0, -1), True)]:
        a, b_, _, _ = simulate(20_000, h, yd)
        o, sh = onset_and_shift(a, b_, PERIOD)
        assert o == 9976
        shifts[name] = sh
    assert shifts == {"N": (-2, -2), "E": (-2, 2), "S": (2, 2), "W": (2, -2), "N, y down": (-2, 2)}

    # odd-flip mask
    c0, m0, w0 = window(xs, ys, col, T0)
    assert len(c0) == 41 and len(m0) == 34 and (w0, 34 - w0) == (22, 12)
    for k in range(1, 300):
        c, m, w = window(xs, ys, col, T0 + PERIOD * k)
        assert c == c0 and m == m0 and (w, 34 - w) == (23, 11)
    assert sorted(Counter(c0.values()).items()) == [(1, 14), (2, 1), (3, 18), (4, 6), (5, 2)]
    # the +10 in period 0: window offset (0,0) is pos(9976) = (-14,10), not the origin;
    # flipped once per window, read black at T0 and white at T0+104
    assert (xs[T0], ys[T0]) == (-14, 10) and c0[(0, 0)] == 1 and (0, 0) in m0
    assert col[T0] == 1 and all(col[T0 + PERIOD * k] == 0 for k in range(1, 300))
    phase_sizes = Counter(len(window(xs, ys, col, T0 + 312 + ph)[1]) for ph in range(PERIOD))
    assert min(phase_sizes) == 28 and max(phase_sizes) == 42 and phase_sizes[34] == 13

    # +12 per window, from t = 9977 (OEIS A255938: n > 9976)
    t = N - PERIOD
    while t >= 0 and B[t + PERIOD] - B[t] == 12:
        t -= 1
    assert t + 1 == 9977 and B[T0 + PERIOD] - B[T0] == 10

    # B(n) = 714 + 12n at cycle boundaries: fails at n = 0 only
    assert B[T0] == 716
    nmax = (N - T0) // PERIOD
    assert all(B[T0 + PERIOD * n] == 714 + 12 * n for n in range(1, nmax + 1))

    # arithmetic for 5,000,000
    n5 = (HORIZON_EGOR - T0) // PERIOD
    assert (HORIZON_EGOR - T0) % PERIOD == 0 and n5 == 47_981
    assert 714 + 12 * n5 == B_EGOR_5M

    # proof that the highway never ends (all-white start)
    Kd, D, Kstar, nC = prove_forever(xs, ys, col, T0, s)
    assert (Kd, D, Kstar) == (5, 2, 5) and nC == 1376
    Cset = {(xs[t], ys[t]) for t in range(T0)}
    Uset = set(c0)
    meets = [k for k in range(Kd + 1)
             if any((xs[T0] + k * s[0] + u[0], ys[T0] + k * s[1] + u[1]) in Cset for u in Uset)]
    assert meets == [0, 1]                            # projection bound 5 is not sharp
    assert N >= T0 + PERIOD * (Kstar + 1)             # base case periods 0..K* simulated

    print("Langton's ant, all-white grid, heading N, y up, right on white")
    print(f"  onset t0 = {T0} (moves periodic from move {first_move}); period {PERIOD}; shift {s}")
    print(f"  shift by start: {shifts}")
    print(f"  odd-flip mask (window at onset phase): {len(m0)} cells of {len(c0)} visited; "
          f"flips w->b/b->w = 22/12 in period 0, 23/11 after")
    print(f"  odd-flip mask size over the 104 phases: {dict(sorted(phase_sizes.items()))}")
    print(f"  B(t+104)-B(t) = 12 for all t >= 9977 (checked to {N}); B(9976) = 716")
    print(f"  B(9976+104n) = 714+12n for n = 1..{nmax} (checked); n = 0 fails (716)")
    print(f"  5,000,000 = 9976 + 104*{n5}; 714 + 12*{n5} = {714 + 12 * n5}")
    print(f"  induction: K_disjoint = {Kd}, D = {D}, base periods 0..{Kstar} simulated -> "
          f"highway and B(n) = 714+12n hold for all n >= 1, forever")

    if full:
        nb, cyc = full_run(HORIZON_EGOR, T0, s)
        assert nb == B_EGOR_5M and cyc == n5
        print(f"  --full: direct run to {HORIZON_EGOR}: B = {nb}; shift held at every t >= {T0 + PERIOD}; "
              f"B(n) checked at all {cyc} cycles")
    print("ALL ASSERTIONS PASS")


if __name__ == "__main__":
    main(full="--full" in sys.argv)
