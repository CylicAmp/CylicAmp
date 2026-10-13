#!/usr/bin/env python3
"""The power tower x, x^x, x^(x^x), ... taken in every direction the numbers allow -- exact.

Built 2026-10-13 from the owner's request (owner_work #257: "Do all that this algorithm can do in
every direction allowed to go by numbers"), on the tower of x = 1/4 from x^(x^x) = (1/2)^sqrt2.

    python3 power_tower.py               x = 1/4
    python3 power_tower.py 1/27 --heights 30 --cut 15

Directions:
  1. UP the tower: every height, its exact value (80 digits, mpmath), its first `cut` decimal
     digits TRUNCATED (rounding the last digit changes the digit sum -- see the 1/4 record), the
     digit sum and digital root.
  2. TO THE LIMIT: the fixed point t = x^t, the contraction factor at it, which side of the limit
     each height sits on, and the first height that agrees with the limit to `cut` digits.
  3. ACROSS x: every tower that converges has t = x^t, i.e. x = t^(1/t), and the contraction there is
     exactly ln t -- so the tower converges exactly when 1/e < t < e (x in [e^-e, e^(1/e)]).
     The family table runs x = t^(1/t) for t = 1/2, 2, 1/3, 3, 1/e, e.
"""
import sys
from fractions import Fraction

import mpmath as mp

mp.mp.dps = 80


def dr(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def tower(x, n):
    t = x
    for _ in range(n - 1):
        t = x ** t
    return t


def cut_digits(v, k):
    """First k decimal digits after the point, truncated."""
    s = mp.nstr(abs(v), mp.mp.dps - 5, strip_zeros=False)
    frac = s.split(".")[1] if "." in s else ""
    return (frac + "0" * k)[:k]


def fixed_point(x):
    """The limit of the tower, or None. Euler/Eisenstein: the tower converges exactly for
    e^-e <= x <= e^(1/e); on the edges the limits are 1/e and e; above it runs to infinity,
    below it settles into a 2-cycle. Inside, the limit is the attracting root of t = x^t."""
    lo, hi = mp.e ** (-mp.e), mp.e ** (1 / mp.e)
    if abs(x - lo) < mp.mpf(10) ** -60:
        return 1 / mp.e
    if abs(x - hi) < mp.mpf(10) ** -60:
        return mp.e
    if x > hi or x < lo:
        return None
    return mp.findroot(lambda t: x ** t - t, tower(x, 3000))


def up(x, heights, cut):
    rows = []
    for n in range(1, heights + 1):
        v = tower(x, n) if not rows or rows[-1][1] < mp.mpf(10) ** 60 else mp.inf
        if v == mp.inf or v > mp.mpf(10) ** 60:
            rows.append((n, v, "(> 10^60: the tower is running to infinity)", 0, 0))
            break
        d = cut_digits(v, cut)
        s = sum(map(int, d)) + sum(map(int, str(int(v))))
        rows.append((n, v, d, s, dr(s)))
    return rows


def report(x_text="1/4", heights=30, cut=15):
    x = mp.mpf(Fraction(x_text).numerator) / Fraction(x_text).denominator if "/" in x_text else mp.mpf(x_text)
    out = [f"POWER TOWER of x = {x_text}   (exact, {mp.mp.dps} digits; digits cut at {cut}, truncated)", ""]
    out.append("1. UP THE TOWER")
    out.append(f"{'height':>6}  {'value (22 digits)':>26}  {'digits':<{cut}}  {'sum':>4} root")
    for n, v, d, s, r in up(x, heights, cut):
        out.append(f"{n:>6}  {mp.nstr(v, 22):>26}  {d}" + ("" if d.startswith("(") else f"  {s:>4}  {r}"))
    t = fixed_point(x)
    out.append("")
    out.append("2. TO THE LIMIT")
    if t is None and x > 1:
        out.append(f"  does not converge: x > e^(1/e) = {mp.nstr(mp.e ** (1 / mp.e), 12)}, the heights run to infinity")
    elif t is None:
        odd, even = tower(x, 401), tower(x, 400)
        out.append(f"  does not converge: the heights split into two limits, odd -> {mp.nstr(odd, 18)}, "
                   f"even -> {mp.nstr(even, 18)} (a 2-cycle)")
    else:
        lam = t * mp.log(x)
        out.append(f"  limit t = {mp.nstr(t, 30)}   (t = x^t: {mp.nstr(x ** t - t, 3)})")
        out.append(f"  contraction at t: t*ln(x) = ln(t) = {mp.nstr(lam, 18)}   "
                   f"({'alternates above/below' if lam < 0 else 'approaches from one side'})")
        errs = [tower(x, n) - t for n in range(1, 41)]
        out.append("  error ratios, heights 30-34: " + ", ".join(mp.nstr(errs[n] / errs[n - 1], 10) for n in range(29, 34)))
        first = next((n for n in range(1, 2000) if abs(tower(x, n) - t) < mp.mpf(10) ** -cut), None)
        out.append(f"  first height within 10^-{cut} of the limit: {first}")
        tail = [r for _, _, _, _, r in up(x, first + 6, cut)][first - 1:]
        out.append(f"  roots from that height on, at the {cut}-digit cut: {tail}")
    out.append("")
    out.append("3. ACROSS x: towers whose limit is t have x = t^(1/t); contraction = ln t; converge iff 1/e < t < e")
    for name, tt in [("1/2", mp.mpf(1) / 2), ("2", mp.mpf(2)), ("1/3", mp.mpf(1) / 3), ("3", mp.mpf(3)),
                     ("1/e", 1 / mp.e), ("e", mp.e)]:
        xx = tt ** (1 / tt)
        lim = fixed_point(xx)
        state = (f"converges to {mp.nstr(lim, 12)}" if lim is not None
                 else ("runs to infinity" if xx > 1 else "does not converge (2-cycle)"))
        if lim is not None and abs(lim - tt) > mp.mpf(10) ** -20:
            state += f"  (not to t = {name}: that root repels, |ln t| > 1)"
        if lim is not None and abs(abs(mp.log(tt)) - 1) < mp.mpf(10) ** -30:
            state += "  (on the edge: converges, slowly)"
        out.append(f"  t = {name:>3}: x = t^(1/t) = {mp.nstr(xx, 14):>16}   ln t = {mp.nstr(mp.log(tt), 8):>11}   tower {state}")
    return "\n".join(out)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = dict(zip(sys.argv[1::2], sys.argv[2::2]))
    print(report(args[0] if args else "1/4", int(opts.get("--heights", 30)), int(opts.get("--cut", 15))))
