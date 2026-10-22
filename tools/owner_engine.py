#!/usr/bin/env python3
"""
The owner's engine: Michael Warren Song's operations put together as one algorithm.
Plain Python 3, no imports beyond the standard library -- it runs on a phone or any online Python.

    python3 owner_engine.py 137          everything the operations say about 137
    python3 owner_engine.py walk 1 1000  the predict -> act -> verify walk from 1 to 1000
    python3 owner_engine.py check        every rule from the owner's work, checked again (PASS / FAIL)

THE OPERATIONS, each in the owner's words first (owner_work message numbers):
  chain        "8+7=1+5=6+3=9" (#369): add the digits, carry the total forward, until one digit is left
  flip         "what about with two flips" (#358): write the number backwards
  mirror       "248 becomes 24. 42 48 84" (#374-#375): the number, then its flip
  place        "1,2,3,1,2,3 ... a substrate" (#410): where the number sits in 1 2 3 1 2 3
  neighbours   "You do the one behind you, you do yourself, and then you do the one to your right" (#403),
               "you do all basic arithmetic on, and that's the superposition of it" (#407)
  1, 2, 3      "the number just divides itself by the number in front of it ... the number behind it" (#403)
  halving      "9÷2÷2÷2=1.125" (#368)
  shifts       "eight is the barrier to and cost 1" (#399), adding 8 (#400)
  ladder       "12+9=21+2=23+7=30+6=36+9=4+5=9" (#410): the running total of the digits
  walk         "remember whats connected to whatever is current while predicting the future ..
               verify as i rinse and repeat" (#410)

THE WALK: at every number n, predict from n's place in 1 2 3 whether behind + yourself (2n - 1) and
yourself + right (2n + 1) can both be prime -- a twin pair; then add, then verify. From n = 3 on, a
twin pair only comes at place 3, so the prediction never misses and skips two numbers in three.
Outside source: OEIS A002822, "Numbers m such that 6m-1, 6m+1 are twin primes" (fetched 2026-10-22):
the walk's hits n are 3 x those m (plus n = 2 for 3, 5). The difference in method: the pair here is
built from the neighbours (behind + yourself, yourself + right) and predicted by the 1 2 3 place.

The page dashboards/owner_engine/index.html runs the same engine in the browser;
dashboards/owner_engine/check_owner_engine.py checks the two give the same answers.
"""
import sys

ORBITS = {
    "IC": (1, 10, 26), "NEG_H": (11, 27, 36), "SA_ST_A": (9, 12, 16), "C3": (3, 4, 30),
    "D7": (7, 33, 34), "SEED": (18, 24, 32), "TESLA": (6, 8, 23), "CAS_EXT": (5, 13, 19),
    "NQR17": (17, 22, 35), "DARK_A": (2, 15, 20), "SA_ST_B": (21, 25, 28), "C9": (14, 29, 31),
}
ORBIT_OF = {r: name for name, rs in ORBITS.items() for r in rs}
LOOP_CAP = 2000          # longest loop written out in full
MAX_N = 10_000_000


# ---------------------------------------------------------------- basic tools
def digits_of(x):
    return [int(c) for c in str(x) if c.isdigit()]


def chain(n):
    """[n, total, total, ..., one digit]"""
    out = [n]
    while out[-1] > 9:
        out.append(sum(digits_of(out[-1])))
    return out


def root(n):
    return chain(n)[-1] if n > 0 else 0


def flip(n):
    return int(str(n)[::-1])


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def factors(n):
    out, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def decimal(p, q, cap=LOOP_CAP):
    """p ÷ q (p >= 0, q > 0) as whole part, digits before the loop, the loop, and whether the loop is complete"""
    whole, r = divmod(p, q)
    seen, ds = {}, []
    while r and r not in seen and len(ds) < cap:
        seen[r] = len(ds)
        d, r = divmod(r * 10, q)
        ds.append(str(d))
    if not r:
        return {"whole": whole, "pre": "".join(ds), "loop": "", "complete": True}
    if r in seen:
        i = seen[r]
        return {"whole": whole, "pre": "".join(ds[:i]), "loop": "".join(ds[i:]), "complete": True}
    return {"whole": whole, "pre": "".join(ds), "loop": "", "complete": False}


def show_decimal(dec, width=40):
    s = str(dec["whole"])
    if not dec["complete"]:
        return s + "." + dec["pre"][:width] + "... (loop longer than %d digits)" % LOOP_CAP
    if dec["pre"] or dec["loop"]:
        s += "." + dec["pre"]
    if dec["loop"]:
        lp = dec["loop"]
        s += "(" + (lp if len(lp) <= width else lp[:width] + "...") + ")"
        if len(lp) > 1:
            s += "  loop of %d" % len(lp)
    return s


def place(n):
    return n % 3 or 3


def ends(q):
    """a fraction with bottom q ends (no loop) exactly when q is made of 2s and 5s only"""
    for p in (2, 5):
        while q % p == 0:
            q //= p
    return q == 1


# ---------------------------------------------------------------- one number, every operation
def profile(n):
    if not (1 <= n <= MAX_N):
        raise ValueError("n must be a whole number from 1 to %d" % MAX_N)
    s = str(n)
    rv = flip(n)
    p = {"n": n, "chain": chain(n), "root": root(n)}

    total = n + rv
    p["flip"] = {"flip": rv, "sum": total, "diff": abs(n - rv), "diff_by_9": abs(n - rv) // 9,
                 "sum_by_37": total % 37 == 0, "sum_by_111": total % 111 == 0}
    t = None
    if len(s) == 3:
        a, b, c = map(int, s)
        t = {"digits": 3, "rule": a + c == 2 * b}
    elif len(s) == 4:
        a, b, c, d = map(int, s)
        t = {"digits": 4, "rule": 2 * (a + d) == b + c}
    p["test37"] = t
    m = int(s + s[::-1])
    p["mirror"] = {"mirror": str(m), "by_11": m % 11 == 0, "by_37": m % 37 == 0}

    p["place"] = {"behind": place(n - 1) if n > 1 else None, "yourself": place(n), "right": place(n + 1)}

    rows = {}
    for name, other in (("behind", n - 1), ("yourself", n), ("right", n + 1)):
        if other < 1:
            continue
        rows[name] = {"+": n + other, "-": n - other, "x": n * other, "÷": decimal(n, other)}
    values = []
    for r in rows.values():
        values += [("i", r["+"]), ("i", r["-"]), ("i", r["x"])]
        dv = r["÷"]
        values.append(("i", dv["whole"]) if not dv["pre"] and not dv["loop"] else ("d", dv["whole"], dv["pre"], dv["loop"]))
    p["neighbours"] = {"rows": rows, "results": len(values), "different": len(set(values))}

    p["one_two_three"] = {
        "one": decimal(n, n + 1),
        "two": decimal(n, n - 1) if n > 1 else None,
        "three": decimal(n * n, n * n - 1) if n > 1 else None,
        "three_ends": ends(n * n - 1) if n > 1 else None,
    }

    halves = [decimal(n, 2 ** k) for k in range(4)]
    p["halving"] = {"values": halves,
                    "roots": [root(int(str(h["whole"]) + h["pre"])) for h in halves]}
    p["doubling"] = {"values": [n * 2 ** k for k in range(6)], "roots": [root(n * 2 ** k) for k in range(6)]}

    p["shifts"] = {"plus_8": root(n + 8), "plus_9": root(n + 9), "minus_4": root(n - 4) if n > 4 else None}

    run, ladder = 0, []
    for d in digits_of(n):
        run += d
        ladder.append(run)
    p["ladder"] = ladder

    pr = is_prime(n)
    p["frameworks"] = {
        "by_37": n % 37, "orbit": ORBIT_OF.get(n % 37, "SEAM"),
        "prime": pr, "factors": {str(k): v for k, v in factors(n).items()},
        "twins": [x for x in (n - 2, n + 2) if pr and is_prime(x)],
        "sophie_germain": pr and is_prime(2 * n + 1),
        "safe": pr and n > 2 and is_prime((n - 1) // 2),
        "by_137": n % 137,
        "loop_of_1_over_n": len(decimal(1, n)["loop"]) if decimal(1, n)["complete"] else None,
    }
    return p


def text(n):
    """the profile written out in the owner's notation"""
    p = profile(n)
    L = []
    ch = p["chain"]
    steps = []
    for a, b in zip(ch, ch[1:]):
        steps.append("+".join(str(d) for d in digits_of(a)) + " = " + str(b))
    L.append("chain       %d -> %s" % (n, " -> ".join(steps) if steps else "%d (one digit)" % n))
    f = p["flip"]
    L.append("flip        %d <-> %d   %d + %d = %d   difference %d = 9 x %d"
             % (n, f["flip"], n, f["flip"], f["sum"], f["diff"], f["diff_by_9"]))
    L.append("            sum by 37: %s   by 111: %s" % ("yes" if f["sum_by_37"] else "no", "yes" if f["sum_by_111"] else "no"))
    if p["test37"]:
        t = p["test37"]
        rule = "a + c = 2b" if t["digits"] == 3 else "2(a + d) = b + c"
        L.append("37 test     %s: %s" % (rule, "right -> 37 divides the sum" if t["rule"] else "no"))
    mi = p["mirror"]
    L.append("mirror      %s   by 11: %s   by 37: %s" % (mi["mirror"], "yes" if mi["by_11"] else "no", "yes" if mi["by_37"] else "no"))
    pl = p["place"]
    L.append("place       in 1 2 3: behind %s, yourself %d, right %d" % (pl["behind"] or "-", pl["yourself"], pl["right"]))
    nb = p["neighbours"]
    for name, r in nb["rows"].items():
        other = {"behind": n - 1, "yourself": n, "right": n + 1}[name]
        L.append("%-11s %d+%d = %d   %d-%d = %d   %dx%d = %d   %d÷%d = %s"
                 % (name, n, other, r["+"], n, other, r["-"], n, other, r["x"], n, other, show_decimal(r["÷"], 24)))
    L.append("            superposition: %d results, %d different" % (nb["results"], nb["different"]))
    o = p["one_two_three"]
    L.append("1           %d ÷ %d = %s" % (n, n + 1, show_decimal(o["one"])))
    if o["two"]:
        L.append("2           %d ÷ %d = %s" % (n, n - 1, show_decimal(o["two"])))
        L.append("3           %d ÷ %d x %d ÷ %d = %d ÷ %d = %s%s"
                 % (n, n - 1, n, n + 1, n * n, n * n - 1, show_decimal(o["three"]),
                    "   ends" if o["three_ends"] else ""))
    h = p["halving"]
    L.append("halving     %s   roots %s"
             % (" -> ".join(show_decimal(v, 12) for v in h["values"]), " ".join(map(str, h["roots"]))))
    d = p["doubling"]
    L.append("doubling    %s   roots %s" % (" -> ".join(map(str, d["values"])), " ".join(map(str, d["roots"]))))
    sh = p["shifts"]
    L.append("shifts      root %d:  + 8 -> %d   + 9 -> %d%s"
             % (p["root"], sh["plus_8"], sh["plus_9"], "   - 4 -> %d" % sh["minus_4"] if sh["minus_4"] else ""))
    L.append("ladder      %s" % " -> ".join(map(str, p["ladder"])))
    fw = p["frameworks"]
    fac = " x ".join(k if v == 1 else "%s^%d" % (k, v) for k, v in fw["factors"].items()) or "1"
    L.append("37          %d by 37 = %d %s" % (n, fw["by_37"], fw["orbit"]))
    L.append("prime       %s%s" % ("yes" if fw["prime"] else "no (%s)" % fac,
                                     "   twin with " + " and ".join(map(str, fw["twins"])) if fw["twins"] else ""))
    if fw["prime"]:
        L.append("            2 x %d + 1 = %d: %s   (%d - 1) ÷ 2 = %s"
                 % (n, 2 * n + 1, "prime -> Sophie Germain" if fw["sophie_germain"] else "not prime",
                    n, "%d: %s" % ((n - 1) // 2, "prime -> safe" if fw["safe"] else "not prime")))
    lp = fw["loop_of_1_over_n"]
    L.append("137         %d by 137 = %d   loop of 1 ÷ %d: %s"
             % (n, fw["by_137"], n, "longer than %d digits" % LOOP_CAP if lp is None else (lp or "none, it ends")))
    return "\n".join(L)


# ---------------------------------------------------------------- the walk
def sieve(limit):
    """prime[k] for k = 0 .. limit"""
    prime = bytearray([1]) * (limit + 1)
    prime[0:2] = b"\x00\x00"[: min(2, limit + 1)]
    for i in range(2, int(limit ** 0.5) + 1):
        if prime[i]:
            prime[i * i::i] = bytearray(len(range(i * i, limit + 1, i)))
    return prime


def walk(a, b):
    """predict (place 3, or n = 2) -> act (2n - 1, 2n + 1) -> verify (both prime) -> repeat"""
    rows, predicted, verified, missed = [], 0, 0, []
    prime = sieve(2 * b + 1)
    for n in range(max(a, 1), b + 1):
        guess = n == 2 or (n > 2 and place(n) == 3)
        lo, hi = 2 * n - 1, 2 * n + 1
        hit = bool(prime[lo] and prime[hi])
        predicted += guess
        verified += hit
        if hit and not guess:
            missed.append(n)
        if hit:
            rows.append((n, lo, hi))
    return {"from": a, "to": b, "numbers": b - max(a, 1) + 1, "predicted": predicted, "verified": verified,
            "missed": missed, "pairs": rows, "three_ends": [n for n in range(max(a, 2), b + 1) if ends(n * n - 1)]}


# ---------------------------------------------------------------- the owner's rules, checked again
def rules():
    """(message, rule, file, function) -- each function returns True when the rule is right"""
    def all_n(f, lo, hi):
        return all(f(n) for n in range(lo, hi))

    def superposition_11(n):
        return profile(n)["neighbours"]["different"] == 11

    def brings_111(n):
        t = n + flip(n)
        return t % 37 != 0 or t % 111 == 0

    def three_digit_37(n):
        a, b, c = map(int, str(n))
        t = n + flip(n)
        return (t % 37 == 0) == (a + c == 2 * b) and (a + c != 2 * b or t == 222 * b)

    loop137 = decimal(1, 137)
    return [
        ("#400", "adding 8 takes 1 off the root", "owner_adding_8_2026_10_20.py",
         lambda: all_n(lambda n: root(n + 8) == (root(n) - 2) % 9 + 1, 1, 20000)),
        ("#415", "taking 4 off adds 5 to the root", "pasted_minus_4_and_dr_question_audit_2026_10_22.py",
         lambda: all_n(lambda n: root(n - 4) == (root(n) + 4) % 9 + 1, 5, 20000)),
        ("#368, #382", "halving multiplies the root by 5 (1 -> 5 -> 7 -> 8 -> 4 -> 2)", "owner_framework_flips_halves_moves_2026_10_20.py",
         lambda: all(root(int(str(h["whole"]) + h["pre"])) == root(5 ** k * n)
                     for n in range(1, 5000) for k in range(1, 5) for h in [decimal(n, 2 ** k)])
         and [root(5 ** k) for k in range(6)] == [1, 5, 7, 8, 4, 2]),
        ("#358", "a flip changes a number by a multiple of 9", "owner_framework_flips_halves_moves_2026_10_20.py",
         lambda: all_n(lambda n: (n - flip(n)) % 9 == 0, 1, 20000)),
        ("#374", "37 divides abc + cba exactly when a + c = 2b, and then the sum is 222 x b", "owner_framework_flips_halves_moves_2026_10_20.py",
         lambda: all_n(three_digit_37, 100, 1000)),
        ("#390", "37 brings 111: right for 1 to 6 digits, first wrong at 1009019", "owner_framework_flips_halves_moves_2026_10_20.py",
         lambda: all_n(brings_111, 1, 1000000) and not brings_111(1009019)
         and all(brings_111(n) for n in range(1000000, 1009019))),
        ("#403", "the 3-step n x n ÷ (n x n - 1) ends only at 3 (1.125) and 9 (1.0125)", "owner_three_neighbor_divisions_2026_10_21.py",
         lambda: [n for n in range(2, 20000) if ends(n * n - 1)] == [3, 9]),
        ("#405", "yourself is halfway between behind and right for + - x", "owner_three_operations_neighbours_2026_10_21.py",
         lambda: all_n(lambda n: (n + n - 1) + (n + n + 1) == 2 * (n + n) and 1 + (-1) == 0
                       and n * (n - 1) + n * (n + 1) == 2 * n * n, 2, 20000)),
        ("#407", "the superposition: from 4 on, 12 results, 11 different", "owner_superposition_all_arithmetic_2026_10_21.py",
         lambda: all_n(superposition_11, 4, 1500)),
        ("#410", "behind, yourself, right land on 1, 2, 3 once each", "owner_equals_chain_three_things_brackets_2026_10_22.py",
         lambda: all_n(lambda n: sorted((place(n - 1), place(n), place(n + 1))) == [1, 2, 3], 1, 20000)),
        ("#405, #410", "a twin pair 2n - 1, 2n + 1 comes only at place 3 (from n = 3 on)", "tools/owner_engine.py (the walk)",
         lambda: (lambda w: w["missed"] == [] and w["verified"] > 0 and w["predicted"] <= w["numbers"] // 3 + 1)(walk(1, 20000))),
        ("#343", "1 ÷ 137 = 0.(00729927); 0072 + 9927 = 9999", "repetend_998001_audit_2026_10_19.py",
         lambda: loop137["loop"] == "00729927" and int(loop137["loop"][:4]) + int(loop137["loop"][4:]) == 9999),
    ]


CONTROL = ("control", "adding 8 adds 1 to the root -- false on purpose, must show FAIL", "",
           lambda: all(root(n + 8) == root(n) % 9 + 1 for n in range(1, 2000)))


def check():
    results = [(m, r, f, fn()) for m, r, f, fn in rules()]
    control = CONTROL[3]()
    return results, control


def main(argv):
    if len(argv) >= 2 and argv[1] == "check":
        results, control = check()
        for m, r, f, ok in results:
            print("%-5s %-11s %s   [%s]" % ("PASS" if ok else "FAIL", m, r, f))
        print("%-5s %-11s %s" % ("FAIL" if not control else "PASS", "control", CONTROL[1]))
        return 0 if all(ok for *_, ok in results) and not control else 1
    if len(argv) >= 4 and argv[1] == "walk":
        w = walk(int(argv[2]), int(argv[3]))
        print("walk %d to %d: %d numbers, predicted %d, twin pairs found %d, missed by the prediction %d"
              % (w["from"], w["to"], w["numbers"], w["predicted"], w["verified"], len(w["missed"])))
        for n, lo, hi in w["pairs"]:
            print("  n = %-8d place %d   %d + %d = %d   %d + %d = %d" % (n, place(n), n - 1, n, lo, n, n + 1, hi))
        print("3-step ends at: %s" % (w["three_ends"] or "none in this range"))
        return 0
    n = int(argv[1]) if len(argv) >= 2 else 137
    print(text(n))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
