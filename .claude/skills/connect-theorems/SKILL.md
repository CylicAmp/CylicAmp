---
name: connect-theorems
description: Connect a verified result to the existing theorems it reinforces or is reinforced by -- found by searching the repo, confirmed by running a check, and recorded with the direction of support. Use after axiom-reduce, for every new result ("the second thing: what theorems it connects to, that it reinforces or that reinforce it"). Everything in the repo is connected to itself; the job is to find the connections that are really there, not to route through any favoured constant.
---

# connect-theorems

## 1. Search by the objects the result uses
Grep `math/theorems`, `math/lemmas`, `math/primes`, `cylicamp` for the
objects (not the constants): e.g. "twin" near "dr|digital root",
"(8,1),(5,7),(2,4)", "6m+-1", "{1,2,4,5,7,8}", "sophie", "9x9". Also check
`math/CATALOG.md` / `CATALOG.json` for the kind of each hit.

## 2. Read each hit's stated result
Read the docstring, not the file name. Keep only files whose statement is
about the same objects.

## 3. Test the connection
Write the connection as a checkable statement and run it. Grid example:
chi_-3 is constant on each mod-9 column (T167/T416); T421's m mod 3 fixes
which twin column move occurs; dr(n+g) = dr(dr(n)+dr(g)) (prime_gap_dr_audit).

## 4. Record the direction
- **reinforces**: the new result is a special case or restatement.
- **refines**: the other file adds a finer split (T421 over the grid).
- **explains / contrasts**: one result accounts for another's outcome (mod 9
  carries mod-3 information, mod 37 almost none -> why T336 is null).
- **hands off**: one method stops where another starts (grid -> prime_engine).

## 5. Assert and save
Each connection goes into the new file's docstring under CONNECTIONS with an
assertion below it. Run, commit, push. A connection that fails its check is
reported as not a connection.
