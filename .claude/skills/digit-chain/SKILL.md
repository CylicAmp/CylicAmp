---
name: digit-chain
description: Build and audit the full chain from a digit pair — a, b, ab, ba, aba, bab, abab, baba — with factorizations, residues mod 37, orbits, primality, and decimal periods. Use whenever a digit pattern, palindrome, repdigit, alternating grid, or two-digit combination comes up, or when someone asks what a pair of digits produces. Reports the closed forms that govern every such chain (aba+bab = 111(a+b) = 37*3(a+b), aba-bab = 91(a-b), abab = 101*ab) so the forced part is separated from the contingent part before anything is recorded.
---

# digit-chain

One command for the whole family a digit pair generates.

```
python3 .claude/skills/digit-chain/chain.py pair 1 9      # one pair, full chain
python3 .claude/skills/digit-chain/chain.py sweep         # all 90 two-digit rows
python3 .claude/skills/digit-chain/chain.py sweep --primes  # only rows with a prime
python3 .claude/skills/digit-chain/chain.py grid 0 7 5    # alternating grid, 5 rows
```

## The closed forms

Everything in a two-digit chain is one of these. Compute them, do not rediscover
them.

```
aba  = 101a + 10b            bab  = 101b + 10a
aba + bab = 111(a+b) = 37 * 3(a+b)        <- always a multiple of 37
aba - bab =  91(a-b) =  7 * 13 * (a-b)
r_aba + r_bab = 37                        <- antipodal orbit pair, always
residue depends only on (a-b)             <- table diagonals are constant

abab = 1010a + 101b = 101 * (10a+b)       <- 101 divides every one
abab + baba = 1111(a+b) = 11 * 101 * (a+b)
abab - baba =  909(a-b) =  9 * 101 * (a-b)
```

`aba` hits SEAM exactly when `a = b`, since `aba = 111a`.
No `abab`/`baba` pair can both be prime: 101 divides both.

## What is contingent

Only three things vary in a way the closed forms do not fix:

- **primality** of `ab`, `aba`, `bab`. Over all 90 pairs, both palindromes are
  prime for `1,3` and `1,9` only; all three of `ab, aba, bab` are prime for
  `13, 19, 31` only.
- **which** antipodal pair the residues land on — set by `a-b`, so it is fixed
  along a diagonal but not by `a` or `b` alone.
- **decimal periods** of the reciprocals.

Anything else a chain "produces" is one of the closed forms above wearing
different digits. Run `forced-check digits <n>` on any single number before
recording an observation about it.

## Grids

`grid a b rows` builds the alternating checkerboard and reports:
period-2 digit vectors have a two-tone DFT (DC + Nyquist, everything else
exactly zero) **iff the length is even**; at odd length the spectrum is full.
Checkerboards of odd height are singular because row 1 = row 3, for any digits.

## Reference

`reference/two_digit_chains.txt` holds the full 90-row table.
