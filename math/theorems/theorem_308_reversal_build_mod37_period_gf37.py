# CLASS: COMPUTATION
"""
Theorem 308: The additive-reversal-build recurrence is eventually periodic
mod 37 with period 3 or 6 for every tested seed
Author: Michael Warren Song (CyclicAmp)

THE RECURRENCE (digit-protocols skill, protocol 9)
    term_0 = seed
    term_k = 10^k + reverse(term_{k-1})
    e.g. seed=9: 9 -> 19 -> 191 -> 1191 -> 11911 -> 111911 -> ...

RESULT (checked for every seed 0..399, each run out 40 terms)
    The residue sequence term_k mod 37 is eventually periodic, and the
    period is ALWAYS 3 or 6 -- no other period occurs in the tested range.
    354/400 seeds give period 6, 46/400 give period 3.

    Which one occurs is NOT a function of seed mod 37 alone: both period-3
    and period-6 seeds occur at the same residue (e.g. seed=1 and seed=38
    are both == 1 mod 37, but only one gives period 3 in the tested range).
    It depends on the seed's decimal digit structure, not on its GF(37)
    class.

WHAT IS AND ISN'T ESTABLISHED HERE
    ord_37(10) = 3 (theorem_265, theorem_303, stacked_zeros_gf37) is
    clearly a necessary ingredient, since term_k's own growth is driven by
    10^k, and 10^k mod 37 itself cycles with period 3 -- (1, 10, 26).

    An earlier draft of this file additionally claimed that term_k is a
    palindrome exactly when k is even (so reverse() is a no-op every other
    step), and used that period-2 structural alternation together with
    ord_37(10)=3 to argue every period must divide lcm(3,2)=6. That
    alternation claim is FALSE in general -- checked directly: for
    seed=1 every term is an all-1s repunit, a palindrome at every k, not
    just even k (351 of the 400 tested seeds break the claimed
    alternation). So that mechanism does not explain the general result.
    No correct mechanism is given here: period-in-{3,6} is reported as an
    exhaustively checked computational fact over the tested range, not as
    a proven theorem. This gap is recorded rather than papered over.

CONNECTION
    This is the same ord_37(10) = 3 fact that makes the comma-group
    protocol's 3-digit grouping meaningful and gives 1/37 its period-3
    decimal expansion (theorem_265_decimal_antipodal_gf37.py). The
    reversal-build recurrence is a different construction entirely, but
    its necessary ingredient is the same forced fact -- even though the
    full mechanism forcing period 3-or-6 specifically remains open.

FALSIFICATION
    Any assert below failing, or any tested seed showing a period other
    than 3 or 6.
"""

P = 37
SEEDS_TESTED = 400
TERMS_PER_SEED = 40
MAX_TRANSIENT = 20
MAX_PERIOD = 12


def rev(n):
    return int(str(n)[::-1])


def build_seq(seed, n_terms):
    terms = [seed]
    for k in range(1, n_terms):
        terms.append(10 ** k + rev(terms[-1]))
    return terms


def is_palindrome(n):
    s = str(n)
    return s == s[::-1]


def eventual_period(residues, max_transient=MAX_TRANSIENT, max_period=MAX_PERIOD):
    for t in range(max_transient):
        for p in range(1, max_period + 1):
            if all(residues[t + i] == residues[t + i + p]
                   for i in range(len(residues) - t - p)):
                return t, p
    return None


def run():
    assert pow(10, 3, P) == 1  # ord_37(10) = 3: a necessary ingredient, not a full explanation

    by_period = {}
    alternation_seeds, non_alternation_seeds = [], []
    for seed in range(SEEDS_TESTED):
        terms = build_seq(seed, TERMS_PER_SEED)
        residues = [t % P for t in terms]
        tp = eventual_period(residues)
        assert tp is not None, f"no period found for seed={seed} within bounds"
        t0, p = tp
        assert p in (3, 6), f"seed={seed} gave period {p}, expected 3 or 6"
        by_period.setdefault(p, []).append(seed)

        alternates = all(is_palindrome(t) == (k % 2 == 0)
                          for k, t in enumerate(terms) if k >= 1)
        (alternation_seeds if alternates else non_alternation_seeds).append(seed)

    assert set(by_period) == {3, 6}
    assert len(by_period[3]) + len(by_period[6]) == SEEDS_TESTED
    # the palindrome-alternation mechanism from an earlier draft is not general:
    assert non_alternation_seeds, "expected the alternation claim to fail for some seed"
    assert 1 in non_alternation_seeds  # seed=1: all-1s repunits, palindrome at every k

    print("All assertions passed.\n")
    print(f"10^3 mod 37 = {pow(10, 3, P)}  (ord_37(10) = 3)\n")
    print(f"Tested seeds 0..{SEEDS_TESTED - 1}, {TERMS_PER_SEED} terms each:")
    print(f"  period 6: {len(by_period[6])} seeds  (e.g. {by_period[6][:6]})")
    print(f"  period 3: {len(by_period[3])} seeds  (e.g. {by_period[3][:6]})")
    print(f"  no other period observed\n")
    print(f"palindrome-alternation (term_k palindrome iff k even, k>=1):")
    print(f"  holds for {len(alternation_seeds)} seeds, fails for "
          f"{len(non_alternation_seeds)} seeds (e.g. seed=1, all-1s repunits)")
    print(f"  -> NOT a general mechanism; period-in-{{3,6}} is reported as an")
    print(f"     exhaustively checked fact, not a proven theorem\n")

    print("Worked example, seed=9 (where the alternation does hold):")
    terms = build_seq(9, 7)
    for k, t in enumerate(terms):
        r = t % P
        print(f"  term_{k} = {t:<10} mod 37 = {r:2d}  palindrome={is_palindrome(t)}")


if __name__ == "__main__":
    run()
