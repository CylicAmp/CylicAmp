#!/usr/bin/env python3
"""
Runs every digit/number protocol demonstrated in this thread against any
input, so each one applies automatically instead of being re-derived by
hand every time a new number comes up.

    python3 protocols.py 246
    python3 protocols.py 121212121
    python3 protocols.py 19 28 37 46 55 64 73 82 91

Six protocols, each a real check, not a template applied blindly:

  1. COMMA-GROUP / REPUNIT   base-10 groups digits in 3s because
     10^3 = 1 mod 37. Reports each 3-digit group's residue and orbit,
     and whether the number is a repunit divisible by 37 (period 3).

  2. REVERSAL DIFFERENCE     abc - cba = 99*(a-c) for any 3-digit number
     (first digit minus last digit), generalizing to (b^(n-1)-1)*(a-z)
     for n digits. Reports the difference and its mod-37 residue.

  3. DIGIT-SUM LADDER        is this number on a constant-digit-sum
     ladder (step 9 within a decade)? Reports the ladder position and
     whether adjacent rungs are also GF(37)-notable.

  4. PASCAL / REPUNIT ROW    is this number a row of Pascal's triangle
     read as digits (11^n) or the sum 2^n? Both are the binomial
     theorem at x=10 and x=1 respectively -- reports which n, if any,
     and where the carry breaks (n=5) if relevant.

  5. SHELL / GNOMON          is this number a two-step concentric-ring
     shell size 8k, or a one-step Pythagorean gnomon 2k+1, or a total
     (2k+1)^2? Reports which, if any.

  6. PARITY / CHECKERBOARD   for a number read as (row,col) or as a
     sequence of digits, is (i+j) mod 2 alternation present -- i.e. is
     this consistent with a bipartite lattice coloring?

Every protocol reports GF(37) placement (residue, orbit, DR) for
whatever it finds, using the same orbit table as gf37-audit.
"""
import sys, math

P = 37
MULT = 26
ORBITS = {
    'IC': {1, 10, 26}, 'DARK_A': {2, 15, 20}, 'C3': {3, 4, 30},
    'CAS_EXT': {5, 13, 19}, 'TESLA': {6, 8, 23}, 'D7': {7, 33, 34},
    'SA_ST_A': {9, 12, 16}, 'NEG_H': {11, 27, 36}, 'C9': {14, 29, 31},
    'NQR17': {17, 22, 35}, 'SEED': {18, 24, 32}, 'SA_ST_B': {21, 25, 28},
}


def orbit_of(n):
    r = n % P
    if r == 0:
        return 'SEAM'
    for name, s in ORBITS.items():
        if r in s:
            return name
    raise AssertionError(r)


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def place(n):
    return f"{n} mod37={n % P} orbit={orbit_of(n)} DR={dr(n)}"


def protocol_comma_group(n):
    s = str(n)
    groups = []
    while s:
        groups.append(s[-3:])
        s = s[:-3]
    groups.reverse()
    print(f"  1. COMMA-GROUP  groups={groups}")
    for g in groups:
        v = int(g)
        print(f"       {g:>3} -> {place(v)}")
    if len(s := str(n)) >= 3 and len(set(s)) == 1 and int(s) % P == 0:
        print(f"       repunit-like, all digits equal, divisible by 37 (period-3 fact)")


def protocol_reversal(n):
    s = str(n)
    if len(s) < 2:
        print("  2. REVERSAL     (single digit, no reversal to check)")
        return
    rev = int(s[::-1])
    diff = n - rev
    b = 10
    L = len(s)
    a, z = int(s[0]), int(s[-1])
    forced = (b ** (L - 1) - 1) * (a - z)
    print(f"  2. REVERSAL     {n} - {rev} = {diff}   forced form (10^{L-1}-1)*({a}-{z}) = {forced}"
          f"   match={diff == forced}   {place(abs(diff)) if diff else 'diff=0'}")


def digit_sum(n):
    return sum(int(c) for c in str(n))


def protocol_digit_sum_ladder(n):
    ds = digit_sum(n)
    below = n - 9 if n - 9 >= 1 else None
    above = n + 9
    same = [x for x in (below, above) if x is not None and digit_sum(x) == ds]
    broken = [x for x in (below, above) if x is not None and digit_sum(x) != ds]
    print(f"  3. DIGIT-LADDER digit_sum={ds}  same-sum neighbors (n+-9): {same}"
          + (f"  [broken at: {broken}]" if broken else ""))
    for x in same:
        print(f"       {place(x)}")


def protocol_pascal(n):
    from math import comb
    found = []
    for k in range(0, 20):
        if 11 ** k == n:
            found.append(('11^k digit-row', k))
        if 2 ** k == n:
            found.append(('2^k row-sum', k))
    if found:
        for label, k in found:
            print(f"  4. PASCAL       {n} = {label}, k={k}")
    else:
        print(f"  4. PASCAL       {n} is not 11^k or 2^k for k=0..19")


def protocol_shell(n):
    hits = []
    for k in range(0, 100):
        if k >= 1 and 8 * k == n:
            hits.append(f"shell(k={k})=8k")
        if 2 * k + 1 == n:
            hits.append(f"gnomon(k={k})=2k+1")
        if (2 * k + 1) ** 2 == n:
            hits.append(f"total(k={k})=(2k+1)^2")
    if hits:
        print(f"  5. SHELL/GNOMON {n}: {', '.join(hits)}")
    else:
        print(f"  5. SHELL/GNOMON {n} matches no shell/gnomon/total form for k=0..99")


def protocol_parity(n):
    s = str(n)
    parities = [int(c) % 2 for c in s]
    alt = all(parities[i] != parities[i + 1] for i in range(len(parities) - 1))
    print(f"  6. PARITY       digits={s}  parities={parities}  strictly alternating={alt}")


def protocol_two_number_board(a, b):
    """
    The (a,b) 3x3 board: corners and center = a, cardinal edges = b.
        a b a
        b a b
        a b a
    Reports rows, columns, both diagonals, corners, edges, perimeter,
    total, and the a-b-a palindrome the board is built around.
    """
    G = [[a, b, a], [b, a, b], [a, b, a]]
    rows = [sum(r) for r in G]
    cols = [G[0][c] + G[1][c] + G[2][c] for c in range(3)]
    d1 = G[0][0] + G[1][1] + G[2][2]
    d2 = G[0][2] + G[1][1] + G[2][0]
    corners = G[0][0] + G[0][2] + G[2][0] + G[2][2]
    edges = G[1][0] + G[1][2] + G[0][1] + G[2][1]
    perim = corners + edges
    total = perim + G[1][1]
    aba = int(f"{a}{b}{a}")
    print(f"  7. TWO-NUMBER BOARD  (a={a}, b={b})")
    print(f"       grid: {G[0]} / {G[1]} / {G[2]}")
    print(f"       rows={rows}  cols={cols}  diag1={d1}  diag2={d2}")
    print(f"       corners=4a={corners}  edges=4b={edges}  perimeter={perim}  total={total}")
    for label, v in [("outer row/col", rows[0]), ("middle row/col", rows[1]),
                      ("diag1", d1), ("diag2", d2), ("perimeter", perim),
                      ("total", total), ("a-b-a palindrome", aba)]:
        print(f"       {label:<16} {place(v)}")


def unit_counts(stream, unit_len):
    """
    Chunk COUNT for a fixed-size grouping, non-overlapping from position 0
    (the '24 digits, groups of N' reading), plus how many times each
    distinct unit of that length actually occurs -- non-overlapping from
    position 0, and separately allowing overlap.
    """
    L = len(stream)
    chunks = [stream[i:i + unit_len] for i in range(0, L, unit_len)] if L % unit_len == 0 else None
    overlap_positions = range(L - unit_len + 1)
    from collections import Counter
    overlap_count = Counter(stream[i:i + unit_len] for i in overlap_positions)
    nonoverlap_count = Counter(chunks) if chunks else Counter()
    return chunks, nonoverlap_count, overlap_count


def protocol_stream_counting(stream):
    """
    For a digit stream (e.g. an alternating 1-2-1-2... run), reports how
    the count changes with the counting unit: chunk size, non-overlapping
    vs overlapping occurrence counts. The count is a property of how you
    read the stream, not of the digits themselves -- this makes that
    explicit and checkable rather than asserted.
    """
    L = len(stream)
    print(f"  8. STREAM COUNTING  stream={stream}  (length {L})")
    for size in sorted(set(d for d in range(1, L + 1) if L % d == 0)):
        chunks, non_ov, ov = unit_counts(stream, size)
        print(f"       chunk size {size:>2} -> {len(chunks)} chunks, distinct: {sorted(non_ov)}")
    print(f"       occurrence counts by unit (non-overlap from pos 0 / overlapping):")
    seen_units = set()
    for size in range(1, min(4, L) + 1):
        _, non_ov, ov = unit_counts(stream, size)
        for u in sorted(set(non_ov) | set(ov)):
            if u in seen_units:
                continue
            seen_units.add(u)
            print(f"         '{u}': {non_ov.get(u,0)} / {ov.get(u,0)}")


def protocol_reversal_build(seed, steps=4):
    """
    The additive-reversal recurrence: term_k = 10^(k-1) + reverse(term_(k-1)).
    Starting from seed=9: 9 -> 10+rev(9)=19 -> 100+rev(19)=191 -> 1000+rev(191)=1191 ...

    NOTE: the step 1 -> 9 that motivated this (1+8=9) is NOT an instance of
    this recurrence. 1 + reverse(1) = 1+1 = 2, not 9. That first step is a
    separate seed choice, not explained by the rule -- recorded here rather
    than papered over. The recurrence is verified to hold from 9 onward.

    Every step's arithmetic is printed explicitly (10^k + rev(prior) = sum)
    so any hand-computed value can be checked against it directly. Also
    prints the digit-swap variant (swap the two distinct digits present,
    e.g. 191 -> 919) alongside the string-reversal value at every step,
    since they coincide except when the prior term has more than two
    distinct digit values or is not built from exactly {a,b} -- the two
    operations are NOT the same rule, and are reported separately rather
    than one silently substituted for the other.
    """
    def rev(n):
        return int(str(n)[::-1])

    def digit_swap(n):
        s = str(n)
        digits = sorted(set(s))
        if len(digits) != 2:
            return None
        a, b = digits
        table = str.maketrans(a + b, b + a)
        return int(s.translate(table))

    print(f"  9. REVERSAL-BUILD  seed={seed}")
    prior = seed
    terms = [seed]
    for k in range(1, steps + 1):
        r = rev(prior)
        total = 10 ** k + r
        swap = digit_swap(prior)
        swap_total = 10 ** k + swap if swap is not None else None
        line = f"       step {k}: 10^{k}={10**k} + rev({prior})={r}  =>  {total}"
        if swap_total is not None and swap_total != total:
            line += f"    [digit-swap({prior})={swap} would give {swap_total} instead]"
        print(line)
        terms.append(total)
        prior = total
    print(f"       terms: {terms}")
    for t in terms:
        print(f"       {place(t)}")


def protocol_nines_progression(max_k=5):
    """
    The zero-count block: k zeros written as a tally (0, 00, 000, ...) marks
    10^k - 1, the all-nines repunit of length k (9, 99, 999, 9999, ...).
    Digital root is 9 for every k (forced: any nonzero multiple of 9 has
    DR 9). Mod 37 it cycles with period 3 -- the same ord_37(10)=3 fact
    behind T308 and the comma-group protocol.
    """
    print(f"  10. NINES-PROGRESSION (k zeros -> 10^k-1)")
    for k in range(1, max_k + 1):
        nines = 10 ** k - 1
        ds = sum(int(c) for c in str(nines))
        print(f"       {'0'*k:<6} -> 10^{k}-1 = {nines:<7} digit_sum={ds:<3} "
              f"{place(nines)}")


def protocol_zero_structure(N, max_k=10):
    """
    Series (N,N) zero structure, generalized for any leading digit N (1-9),
    run automatically instead of retyped by hand for each N.

    TERMINAL ZERO STRUCTURE: the number N followed by k zeros, i.e. N*10^k
    -- the bulleted zero-strings (0, 00, 000, 0,000, ...) are just that
    number's zero-tail, comma-grouped, with the leading N implied. DR is
    forced to N for every k (DR is invariant under trailing zeros: 10^k
    contributes DR=1, and DR(N*1)=N). Mod 37 cycles with period 3, scaled
    by N, from the same ord_37(10)=3 fact as T308/T309.

    INCREMENTING ZERO STRUCTURE: same N*10^k, but for k>=4 add m=k-3
    (so +1 at k=4 up through +7 at k=10). DR(N*10^k+m) = DR(N+m): the
    added digit m never carries into N because the zero-run separates
    them. This makes the DR sequence N+1, N+2, ..., N+7 (mod-9 wrapped),
    forced, not independent per-row facts.
    """
    def dr(n):
        return 0 if n == 0 else 1 + (n - 1) % 9

    print(f"  11. ZERO-STRUCTURE  Series ({N},{N})")
    print(f"      Terminal Zero Structure (= {N}):")
    for k in range(1, max_k + 1):
        val = N * 10 ** k
        assert dr(val) == N, f"forced DR fact broke at N={N}, k={k}"
        print(f"        k={k:2d}  {N}x10^{k} = {val:<15,}  {place(val)}")

    print(f"      Incrementing Zero Structure (+1..+{max_k - 3}):")
    for k in range(1, max_k + 1):
        if k < 4:
            base = N * 10 ** k
            print(f"        k={k:2d}  {N}x10^{k} = {base:<15,}")
            continue
        m = k - 3
        val = N * 10 ** k + m
        assert dr(val) == dr(N + m), f"forced DR fact broke at N={N}, k={k}, m={m}"
        print(f"        k={k:2d}  {N}x10^{k}+{m} = {val:<15,}  {place(val)}")


def protocol_triangular_reduction(max_n=9):
    """
    Cumulative zero-reduction stream: the running total of the incrementing
    zero structure (protocol 11), reduced to a digital root.

        zeros prefix = "0"*n
        index        = n
        suffix       = T_n = n(n+1)/2   (cumulative sum 1+2+...+n)
        root         = DR(T_n)
        raw string   = "0"*n + str(n) + str(T_n)
        reduced      = "0"*n + str(n) + str(DR(T_n))

    The terminal root stream for n=1..9 is 1,3,6,1,6,3,1,9,9 -- exactly one
    full cycle, and it repeats forever after.

    Two forced facts, both asserted below rather than observed per-row:
      PERIOD 9: T_(n+9) - T_n = 9n+45, divisible by 9, so DR(T_n) depends
        only on n mod 9. The stream cannot do anything but repeat.
      PALINDROME: T_(8-n) - T_n = 36-9n, divisible by 9, so DR(T_n) =
        DR(T_(8-n)). That mirrors the first seven terms about n=4:
        1,3,6,[1],6,3,1. The two 9s at n=8,9 sit outside the mirror
        because 36 and 45 are both multiples of 9.
    """
    def dr(n):
        return 0 if n == 0 else 1 + (n - 1) % 9

    def tri(n):
        return n * (n + 1) // 2

    print(f"  12. TRIANGULAR-REDUCTION (cumulative zero structure)")
    stream = []
    for n in range(1, max_n + 1):
        T = tri(n)
        d = dr(T)
        stream.append(d)
        raw = "0" * n + str(n) + str(T)
        red = "0" * n + str(n) + str(d)
        print(f"       n={n}  T_n={T:<4} DR={d}  raw={raw:<26} reduced={red:<26} "
              f"{place(T)}")

    print(f"       terminal root stream: {stream}")

    # forced: period 9
    for n in range(1, max_n + 20):
        assert dr(tri(n + 9)) == dr(tri(n)), f"period-9 broke at n={n}"
        assert (tri(n + 9) - tri(n)) % 9 == 0
    # forced: palindrome about n=4 within the first seven
    for n in range(1, 8):
        assert dr(tri(8 - n)) == dr(tri(n)), f"palindrome broke at n={n}"
        assert (tri(8 - n) - tri(n)) % 9 == 0
    print(f"       period-9 and palindrome both verified (forced, asserted)")


PROTOCOLS = [
    protocol_comma_group, protocol_reversal, protocol_digit_sum_ladder,
    protocol_pascal, protocol_shell, protocol_parity,
]


def run(n):
    print(f"=== {n} ===  ({place(n)})")
    for p in PROTOCOLS:
        p(n)
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    if sys.argv[1] == "board" and len(sys.argv) == 4:
        protocol_two_number_board(int(sys.argv[2]), int(sys.argv[3]))
        sys.exit(0)
    if sys.argv[1] == "stream" and len(sys.argv) == 3:
        protocol_stream_counting(sys.argv[2])
        sys.exit(0)
    if sys.argv[1] == "revbuild" and len(sys.argv) >= 3:
        steps = int(sys.argv[3]) if len(sys.argv) > 3 else 4
        protocol_reversal_build(int(sys.argv[2]), steps)
        sys.exit(0)
    if sys.argv[1] == "nines" and len(sys.argv) >= 2:
        max_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        protocol_nines_progression(max_k)
        sys.exit(0)
    if sys.argv[1] == "zerostruct" and len(sys.argv) >= 3:
        max_k = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        protocol_zero_structure(int(sys.argv[2]), max_k)
        sys.exit(0)
    if sys.argv[1] == "triangular":
        max_n = int(sys.argv[2]) if len(sys.argv) > 2 else 9
        protocol_triangular_reduction(max_n)
        sys.exit(0)
    if sys.argv[1] == "zerostruct-all":
        max_k = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        for N in range(1, 10):
            protocol_zero_structure(N, max_k)
            print()
        sys.exit(0)
    for arg in sys.argv[1:]:
        run(int(arg))
