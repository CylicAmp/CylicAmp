"""
T290 — The Squaring Map on Orbits: Exact Sequence H_2 → Z/12Z → H_6

Prompted by the quadratic map z -> z^2 + c (the Mandelbrot iteration) over F_37.

Three tests were stated in advance with explicit miss conditions (T282 method).
Two failed. Recording the failures is part of the result.

────────────────────────────────────────────────────────────────────────────
TEST 1 — HIT (load-bearing)
────────────────────────────────────────────────────────────────────────────
Q: does z -> z^2 induce a well-defined map on the 12 orbits?
MISS CONDITION: any orbit whose elements square into different orbits.

Result: well-defined on all 12 orbits.  The induced map on Z/12Z is
multiplication by 2:  class k -> class 2k (mod 12).

Reason it is forced: squaring doubles the discrete log; orbit class IS the
discrete log mod 12 (T285), so squaring is x2 on Z/12Z.

  kernel = {k : 2k ≡ 0 mod 12} = {0, 6} = {IC, NEG_H} = H_2  (T286, T284 <11>)
  image  = {2k} = {0,2,4,6,8,10}
         = {IC, C3, SA_ST_A, NEG_H, D7, SA_ST_B} = H_6  (T286)

  |kernel| x |image| = 2 x 6 = 12   (first isomorphism theorem)

So the Mandelbrot quadratic's multiplicative part is exactly the short exact
sequence  1 -> H_2 -> Z/12Z -> H_6 -> 1  in the T286 subgroup lattice.
Both H_2 and H_6 were already in that lattice before this test was run.

Contrast with T287: the cubic x^3 is orbit-INVARIANT (26^3 ≡ 1), i.e. x3 on
Z/12Z is the zero map (3k ≡ ... no — 26^3≡1 makes x^3 constant on orbits).
The square is a 2-to-1 collapse; the cube is a constant. Different mechanisms.

────────────────────────────────────────────────────────────────────────────
TEST 2 — MISS (recorded)
────────────────────────────────────────────────────────────────────────────
Q: is the cycle structure of the full map z -> z^2 + c constant on the
   137-map orbit of c?
MISS CONDITION: any orbit whose three c-values give different cycle structures.

Result: ALL 12 orbits scatter.  Hypothesis is FALSE.
e.g. CAS_EXT = {5,13,19} gives cycles (7,), (4,), (1,1,3) — three different
structures inside one orbit.

Reason: "+c" is additive; orbits are multiplicative cosets.  The additive
translation destroys the multiplicative orbit structure. The clean Test-1
result survives only for the pure squaring part.

────────────────────────────────────────────────────────────────────────────
TEST 3 — MISS (recorded)
────────────────────────────────────────────────────────────────────────────
Q: is look-and-say (run-length digit encoding) well-defined on orbits?
MISS CONDITION: any orbit whose elements encode into different orbits.

Result: ALL 12 orbits scatter. Hypothesis is FALSE.
Reason: look-and-say is a base-10 digit operation; orbits are multiplicative
structure in GF(37). No mechanism connects them.

────────────────────────────────────────────────────────────────────────────
T282 classification
────────────────────────────────────────────────────────────────────────────
  Test 1: LOAD-BEARING — forced by discrete-log arithmetic, kernel and image
          land on subgroups that already existed in the T286 lattice.
  Test 2: FALSIFIED    — stated in advance, came back negative.
  Test 3: FALSIFIED    — stated in advance, came back negative.

Two of three predictions failed. That is what a real miss-test looks like.
"""

ORBITS = {
    'IC':      {1, 10, 26},
    'DARK_A':  {2, 15, 20},
    'C3':      {3, 4, 30},
    'CAS_EXT': {5, 13, 19},
    'TESLA':   {6, 8, 23},
    'D7':      {7, 33, 34},
    'SA_ST_A': {9, 12, 16},
    'NEG_H':   {11, 27, 36},
    'C9':      {14, 29, 31},
    'NQR17':   {17, 22, 35},
    'SEED':    {18, 24, 32},
    'SA_ST_B': {21, 25, 28},
}

H_2 = {'IC', 'NEG_H'}
H_6 = {'IC', 'C3', 'SA_ST_A', 'NEG_H', 'D7', 'SA_ST_B'}

ELEM_TO_ORBIT = {}
for _n, _s in ORBITS.items():
    for _e in _s:
        ELEM_TO_ORBIT[_e] = _n


def orb(x):
    return ELEM_TO_ORBIT.get(x % 37, 'SEAM')


def cls(x):
    for m in range(12):
        if x % 37 in {(pow(2, m, 37) * h) % 37 for h in {1, 10, 26}}:
            return m
    return None


# ─── Test 1: squaring is well-defined on orbits ──────────────────────────────

def test1_squaring_well_defined():
    """z -> z^2 induces class k -> 2k on Z/12Z. Kernel H_2, image H_6."""
    for name, elems in ORBITS.items():
        imgs = {orb((z * z) % 37) for z in elems}
        assert len(imgs) == 1, f"{name} squares into {imgs} — not well-defined"

    # induced map is multiplication by 2 on Z/12Z
    for m in range(12):
        rep = pow(2, m, 37)
        assert cls((rep * rep) % 37) == (2 * m) % 12, f"class {m} broke x2 rule"

    kernel = {orb(pow(2, m, 37)) for m in range(12) if (2 * m) % 12 == 0}
    image = {orb(pow(2, (2 * m) % 12, 37)) for m in range(12)}

    assert kernel == H_2, f"kernel {kernel} != H_2"
    assert image == H_6, f"image {image} != H_6"
    assert len(kernel) * len(image) == 12, "first isomorphism theorem violated"
    return kernel, image


# ─── Test 2: cycle structure of z^2+c (FALSIFIED) ────────────────────────────

def cycle_structure(c):
    f = {z: (z * z + c) % 37 for z in range(37)}
    state, cycles = {}, []
    for start in range(37):
        if state.get(start, 0) == 2:
            continue
        path, pos = [], {}
        z = start
        while state.get(z, 0) == 0:
            state[z] = 1
            pos[z] = len(path)
            path.append(z)
            z = f[z]
        if state.get(z, 0) == 1:
            cycles.append(len(path) - pos[z])
        for w in path:
            state[w] = 2
    return tuple(sorted(cycles))


def test2_cycle_structure_falsified():
    """Stated in advance; came back negative. All 12 orbits scatter."""
    scattered = []
    for name, elems in ORBITS.items():
        if len({cycle_structure(c) for c in elems}) != 1:
            scattered.append(name)
    assert len(scattered) == 12, f"Expected all 12 to scatter, got {len(scattered)}"
    return scattered


# ─── Test 3: look-and-say (FALSIFIED) ────────────────────────────────────────

def look_and_say(s):
    out, i = [], 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out.append(str(j - i) + s[i])
        i = j
    return ''.join(out)


def test3_look_and_say_falsified():
    """Stated in advance; came back negative. All 12 orbits scatter."""
    scattered = []
    for name, elems in ORBITS.items():
        imgs = {orb(int(look_and_say(str(z)))) for z in elems}
        if len(imgs) != 1:
            scattered.append(name)
    assert len(scattered) == 12, f"Expected all 12 to scatter, got {len(scattered)}"
    return scattered


def run():
    print("=" * 70)
    print("T290 — Squaring Map Exact Sequence; two falsified hypotheses")
    print("=" * 70)

    kernel, image = test1_squaring_well_defined()
    print("\n--- TEST 1: HIT (load-bearing) ---")
    print("  z -> z^2 is well-defined on all 12 orbits.")
    print("  Induced map on Z/12Z: class k -> class 2k")
    for m in range(12):
        rep = pow(2, m, 37)
        print(f"    class {m:2d} ({orb(rep):8s}) -> class {(2*m)%12:2d} "
              f"({orb((rep*rep)%37):8s})")
    print(f"\n  kernel = {sorted(kernel)} = H_2  (T286; = <11>/IC from T284)")
    print(f"  image  = {sorted(image)} = H_6  (T286)")
    print(f"  |ker| x |img| = {len(kernel)} x {len(image)} = 12")
    print("  => short exact sequence 1 -> H_2 -> Z/12Z -> H_6 -> 1")
    print("  Both subgroups were already in the T286 lattice before this test.")

    scattered2 = test2_cycle_structure_falsified()
    print("\n--- TEST 2: MISS (hypothesis falsified) ---")
    print("  Q: is the cycle structure of z -> z^2+c constant on orbits of c?")
    print(f"  All {len(scattered2)}/12 orbits scatter. FALSE.")
    print("  Example CAS_EXT = {5,13,19}:")
    for c in sorted(ORBITS['CAS_EXT']):
        print(f"    c={c:2d} -> cycles {cycle_structure(c)}")
    print("  Reason: '+c' is additive; orbits are multiplicative cosets.")

    scattered3 = test3_look_and_say_falsified()
    print("\n--- TEST 3: MISS (hypothesis falsified) ---")
    print("  Q: is look-and-say well-defined on orbits?")
    print(f"  All {len(scattered3)}/12 orbits scatter. FALSE.")
    print("  Example IC = {1,10,26}:")
    for z in sorted(ORBITS['IC']):
        print(f"    {z} -> '{look_and_say(str(z))}' -> {int(look_and_say(str(z)))%37} "
              f"({orb(int(look_and_say(str(z))))})")
    print("  Reason: base-10 digit operation vs multiplicative field structure.")

    print("\n--- T282 classification ---")
    print("  Test 1: LOAD-BEARING (forced; lands on pre-existing subgroups)")
    print("  Test 2: FALSIFIED")
    print("  Test 3: FALSIFIED")
    print("  Two of three stated predictions came back negative.")

    print("\nAll T290 assertions passed.")


if __name__ == '__main__':
    run()
