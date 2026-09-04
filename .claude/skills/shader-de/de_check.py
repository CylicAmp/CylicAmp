#!/usr/bin/env python3
"""
Analyse a golfed raymarching shader: recover its structure, compute the
Lipschitz bound implied by its folds, and check the distance estimate is a
genuine underestimate.

    python3 de_check.py scan  <file.glsl|->      static scan of the source
    python3 de_check.py verify <de_module.py>    numerical DE validation
    python3 de_check.py ray   <aspect>           unnormalised-ray factor

The scan is automatic. The numerical check needs the DE transcribed into
Python — see the template printed by `de_check.py template`.
"""
import sys, re, math, importlib.util

# ── static scan ─────────────────────────────────────────────────────────────

FOLD_RE = re.compile(
    r'(\w+)\s*=\s*abs\(\s*(?:(\w+)\s*\+\s*\2|(\w+)\s*\*\s*([\d.]+)|(\w+))\s*\)'
    r'\s*-\s*([\d.]+)')
LOOP_RE = re.compile(r'for\s*\(\s*(?:int|float)?\s*([\w,\s]*);\s*(\w+)\+\+\s*<\s*([\d.eE+]+)')
DIV_RE  = re.compile(r'\)\s*/\s*([\d.]+e?\d*)\s*[;,)]')
ROT3_RE = re.compile(r'rotate3D\(\s*([\d.]+)\s*,\s*vec3\(([^)]*)\)')
UNINIT_RE = re.compile(r'for\s*\(\s*(?:float|int)\s+([a-zA-Z]\w*(?:\s*,\s*[a-zA-Z]\w*)+)\s*;')

CONSTS = {'pi': math.pi, 'pi/2': math.pi/2, 'pi/3': math.pi/3,
          'pi/4': math.pi/4, 'tau': 2*math.pi, 'phi': (1+5**0.5)/2,
          'sqrt2': math.sqrt(2), 'e': math.e}


def scan(src):
    L = []
    A = L.append
    A("=" * 70)
    A("STATIC SCAN")
    A("=" * 70)

    # loops
    loops = LOOP_RE.findall(src)
    A("\nloops:")
    for decl, var, bound in loops:
        try:
            b = int(float(bound))
        except ValueError:
            b = bound
        A(f"  {var}++ < {bound}   -> {b} iterations   (decl: {decl.strip()})")

    # folds
    folds = FOLD_RE.findall(src)
    A("\nfold operations:")
    scale = None
    for m in folds:
        tgt = m[0]
        if m[1]:
            s, c = 2.0, float(m[5])
            form = f"abs({m[1]}+{m[1]}) - {c}"
        elif m[2]:
            s, c = float(m[3]), float(m[5])
            form = f"abs({m[2]}*{s}) - {c}"
        else:
            s, c = 1.0, float(m[5])
            form = f"abs({m[4]}) - {c}"
        scale = s
        A(f"  {tgt} = {form}     scale factor {s}")
    if not folds:
        A("  none found")

    # Lipschitz
    A("\nLipschitz bound:")
    inner = None
    for decl, var, bound in loops:
        try:
            n = int(float(bound))
        except ValueError:
            continue
        if n <= 32:                    # heuristic: fold loops are short
            inner = n
    if scale and inner:
        lip = scale ** inner
        A(f"  {inner} folds x scale {scale}  ->  L = {scale}^{inner} = {lip:g}")
        divs = [float(d) for d in DIV_RE.findall(src)]
        if divs:
            d = max(divs)
            A(f"  DE divisor found: {d:g}")
            margin = d / lip
            A(f"  safety factor = {d:g}/{lip:g} = {margin:.2f}x")
            if margin >= 1:
                A(f"  -> divisor covers the fold scaling"
                  f"{' (conservative)' if margin > 2 else ' (tight)'}")
            else:
                A(f"  -> DIVISOR TOO SMALL: DE can overshoot. Needs >= {lip:g}")
        else:
            A("  no divisor found — check the DE is scaled by 1/L")
    else:
        A("  could not infer (need a fold scale and a short loop bound)")

    # rotate3D axes
    A("\nrotate3D axes:")
    found = False
    for ang, axis in ROT3_RE.findall(src):
        found = True
        comps = [c.strip() for c in axis.split(',')]
        lits = []
        for c in comps:
            try:
                lits.append(float(c))
            except ValueError:
                lits.append(None)
        A(f"  angle {ang}, axis ({', '.join(comps)})")
        if all(v is not None for v in lits):
            n = math.sqrt(sum(v * v for v in lits))
            A(f"    |axis| = {n:.4f}" +
              ("  unit" if abs(n - 1) < 1e-6 else
               "  NOT unit — relies on rotate3D normalising internally"))
        else:
            A("    axis has runtime components; length varies. If any branch")
            A("    is non-unit, the rotation is only orthogonal when the")
            A("    builtin normalises. Verify before porting.")
    if not found:
        A("  none found")

    # constant approximations
    A("\nnumeric literals near named constants:")
    hits = False
    for lit in sorted(set(re.findall(r'(?<![\w.])(\d+\.\d+)', src)), key=float):
        v = float(lit)
        for name, cv in CONSTS.items():
            if cv and abs(v - cv) / cv < 0.01 and v != cv:
                A(f"  {lit} vs {name} = {cv:.6f}   error {abs(v-cv):.2e}"
                  f"  ({abs(v-cv)/cv*100:.3f}%)")
                hits = True
    if not hits:
        A("  none within 1%")

    # implicit dependencies
    A("\nimplicit dependencies:")
    un = UNINIT_RE.findall(src)
    if un:
        for d in un:
            A(f"  uninitialised locals: {d}  — undefined in GLSL, zero in")
            A("    practice. Standard golf idiom; first thing to break on an")
            A("    unusual compiler.")
    if re.search(r'vec3\(\s*\(?\s*FC|gl_FragCoord', src):
        if not re.search(r'normalize\s*\(', src):
            A("  ray direction is not normalize()d — g understates true")
            A("    distance. Run `de_check.py ray <aspect>` for the factor.")
    return "\n".join(L)


# ── unnormalised ray factor ─────────────────────────────────────────────────

def ray_factor(aspect):
    ux, uy = aspect / 2, 0.5
    d = math.sqrt(ux * ux + uy * uy + 1)
    return math.hypot(ux, uy), d


# ── numerical DE validation ─────────────────────────────────────────────────

def verify(de, samples=400, dirs=24, box=3.0, seed=0):
    """
    de(p) -> float, p a length-3 sequence.
    Checks no point within the DE-sphere has opposite sign: if the DE says
    'the surface is at least d away', nothing inside radius d may be inside
    the surface.
    """
    import numpy as np
    rng = np.random.default_rng(seed)
    tested = viol = 0
    worst = None
    for _ in range(samples):
        p = rng.uniform(-box, box, 3)
        d = de(p)
        if not (d > 0) or not math.isfinite(d):
            continue
        tested += 1
        for _ in range(dirs):
            u = rng.normal(size=3)
            u /= np.linalg.norm(u)
            if de(p + u * d * 0.999) < 0:
                viol += 1
                if worst is None:
                    worst = (p.tolist(), d)
                break
    return tested, viol, worst


TEMPLATE = '''\
# de_module.py — transcribe the shader DE, then:
#   python3 de_check.py verify de_module.py
import numpy as np, math

def rot3(a, axis):
    ax = np.array(axis, float); ax /= np.linalg.norm(ax)   # twigl normalises
    x, y, z = ax; c, s = math.cos(a), math.sin(a); C = 1 - c
    return np.array([[c+x*x*C, x*y*C-z*s, x*z*C+y*s],
                     [y*x*C+z*s, c+y*y*C, y*z*C-x*s],
                     [z*x*C-y*s, z*y*C+x*s, c+z*z*C]])

def de(p, t=0.0):
    ss = min(max((math.sin(t*.4)+1)/2, 0), 1)
    sm = ss*ss*(3-2*ss)                     # smoothstep(-1,1,sin(t*.4))
    R = rot3(1.57, [1, 1.5*sm-.5, 0])
    q = np.array(p, float)
    for _ in range(7):
        q = R @ q
        q = np.abs(q+q) - 2.
    return (np.linalg.norm([np.linalg.norm(q[[0,2]])-2., (q[1]-q[0])*.7]) - .6)/8e2
'''

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(1)
    if a[0] == 'scan':
        src = sys.stdin.read() if a[1] == '-' else open(a[1]).read()
        print(scan(src))
    elif a[0] == 'ray':
        for asp in (a[1:] or ['1.7778']):
            m, d = ray_factor(float(asp))
            print(f"  aspect {float(asp):.4f}: max|uv| = {m:.3f}, |dir| = {d:.3f}"
                  f"  -> corner rays advance {d:.2f}x faster than g")
    elif a[0] == 'template':
        print(TEMPLATE)
    elif a[0] == 'verify':
        spec = importlib.util.spec_from_file_location("dem", a[1])
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        t, v, w = verify(m.de)
        print(f"  points tested: {t}   sign flips inside the DE sphere: {v}")
        if v == 0:
            print("  VALID underestimate on this sample")
        else:
            print(f"  OVERSHOOTS — e.g. p = {w[0]}, DE = {w[1]:.3e}")
            print("  The DE claims more clearance than it has. Increase the")
            print("  divisor to at least the Lipschitz bound from `scan`.")
    else:
        print(__doc__); sys.exit(1)
