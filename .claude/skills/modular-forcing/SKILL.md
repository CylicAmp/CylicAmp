---
name: modular-forcing
description: Climb the 2-adic ladder to close cases — parity, then mod 4, then mod 8, recording which residues survive each rung. Use on any Diophantine or divisor-structure problem where some parameter looks forced, and before reaching for a case tree or a search. This is what actually closed k=2, k=3, k=6 and k=5-even in T245; it is cheap, it either fires in three lines or it does not fire at all, and knowing which is the point. Also records the two failure modes: a rung that gives a necessary condition mistaken for a contradiction, and a ladder that cannot fire because the parity count is even.
---

# modular-forcing

Parity, then mod 4, then mod 8. Stop when a rung closes the case or when
you can show no rung will.

## Run it

```
python3 .claude/skills/modular-forcing/ladder.py "1+d2^2+d3^2+d4^2" --even
python3 .claude/skills/modular-forcing/ladder.py --divisor-sum 6
```

## The ladder

| rung | what it sees | typical kill |
|---|---|---|
| mod 2 | parity counts | forces the smallest prime to be 2 |
| mod 4 | odd squares = 1, even squares = 0 | pins *how many* terms are odd |
| mod 8 | odd squares = 1, so the count is exact | forces a divisor that must not fit |
| mod 16+ | rarely adds anything for squares | stop unless you have a reason |

Squares stop giving new information at 8: every odd square is 1 (mod 8), so
mod 16 tells you nothing mod-8 did not. If you are still climbing past 8 on
a sum of squares, the ladder is not your tool.

## The parity lemma, and when this skill is useless

For `n = 1 + (k-1) squares` with every divisor odd:

    k even  ->  n = 1 + (k-1) odd = even  ->  contradiction, p = 2 FORCED
    k odd   ->  n = odd                   ->  consistent, NOTHING forced

That one line predicts which layers are easy. In T245 every even k fell to
this ladder alone; every odd k resisted and needed quadratic residues
(k=3) or a case tree (k=5). **Check the parity count before you start.**
If k is odd, expect the ladder to fail and plan the next instrument now.

## The two failure modes, both seen in this corpus

**A necessary condition read as a contradiction.** Mod 8 giving `8 | n` is
not a kill by itself. It becomes one only when you then show 8 cannot sit
where the divisor order requires — as in k=6, where `8 | n` forces
d4, d5, d6 < 8 and the odd divisors in (4,8) are only 5 and 7, two slots for
three divisors. Write the second half down or you have proved nothing.

**A rung that cannot fire.** Before claiming a residue class is excluded,
check it is reachable. `n = 21 + q^2` is 2 (mod 4) for every odd q, so
`4 | n` dies — but only because 21 + 1 = 22 and odd squares are always 1.
State the residue set you are ruling out and confirm it is non-empty first;
this is the miss-test applied to a congruence.

## Procedure

1. **Count the parity** of the whole expression. If it forces a prime, take
   it and rewrite.
2. **Go to mod 4.** Classify each term as odd (1), 2-mod-4 (0) or 4-divisible
   (0). Solve for how many terms are odd. Usually this leaves two cases.
3. **Go to mod 8** on each surviving case. Odd squares are 1, so the count
   becomes exact and you learn a divisibility like `8 | n`.
4. **Convert the divisibility into an ordering contradiction.** This is the
   step people skip. A new divisor has to fit somewhere in the sorted list,
   and usually it cannot.
5. **If nothing closed**, stop climbing and say so. Record which residues
   survived at each rung — that list is the input to `case-tree`, not a
   failure.

## What it cannot do

It cannot close a case where both parities are consistent, which is every
odd layer. It cannot handle a congruence with three or more free squares on
one side — the quadratic-residue step that closed k=3 needs a *lone* square,
and with three there is nothing to invert. When either is true, hand off:
`case-tree` for branching, `search-bounds` for a bounded check.
