# Theorem corpus audit — does 37 actually do work?

Prompted by T316, which found that the seed-246 reference block in `CLAUDE.md`
displays five `True` values where only two are independent, and that eight of
its sixteen fields are seed-independent constants. The obvious follow-up: does
the same pattern — checks that look like confirmations but cannot fail — appear
across the theorem corpus?

Two sweeps, both runnable: `tools/mutation_audit.py`.

---

## 1. Assertions that cannot fail on data

480 theorem files, **10,266 assertions**, parsed with `ast`.

```
literal-only (no identifier anywhere)    796   7.8%
references data / variables            9,470  92.2%
```

A literal-only assertion (`assert 600 == 8 * 3 * 25`, `assert 3900 % 30 == 0`)
documents the author's arithmetic. It cannot fail on input, so it is not
evidence for anything. 7.8% is low, and the files where it dominates are mostly
scratch/ledger files rather than numbered theorems.

This is the weaker signal, and not the T120/121 failure mode. That one was
assertions which DO reference data but are logically implied by one another.

---

## 2. Mutation test — the real one

A theorem claiming something about GF(37) should break when 37 is replaced.
232 files define a module-level `P = 37`. Rewrite it to 43 (prime, = 1 mod 3)
and to 73 (the other member of {7,37,73}), following the repo's own
forced-check taxonomy.

```
fails 43 and 73       TIER C  specific to 37
fails 43, passes 73   TIER B  the {7,37,73} family
passes both           TIER A  holds for other primes; the 37 is decorative
```

### Result

```
 191   TIER C   fails both mutations
  21   TIER C   caught only by the second pass (literal mutation)
   1   TIER B   the {7,37,73} family
  11   TIER A   >>> 37 IS DECORATIVE <<<
   5   inconclusive (mutation broke them structurally)
   2   slow, not broken (29s and 65s)
```

**213 of 232 (92%) demonstrably depend on 37.** That is the headline and it is
good news for the corpus.

### The 11 where it does not

Every assertion in these still holds with every `37` replaced by `43`:

```
buckingham_pi_gf37.py              orbit_connection_map.py
dr_addition_table.py               ramanujan_tau_gf37.py
gf37_toolkit.py                    theorem_132_dlp_algorithms_gf37.py
monte_carlo_prime_streams.py       theorem_193_process_functions_zp.py
torus_z37_z81.py                   twin_prime_dr_pair.py
theorem_314_twelve_double_closure_gf37.py
```

Several are clearly fine as-is — `gf37_toolkit.py` and `dr_addition_table.py`
are utilities, and `theorem_193_process_functions_zp.py` says `zp` in its name,
i.e. it is about Z/pZ generally and SHOULD survive. A Tier A result is only a
problem where the file's title or placement claims 37-specificity.

**T314 is mine, written this session, and it is a real hit.** It has ZERO
assertions referencing `37` or `P`. Every claim in it — `9 + dr(n) = n` on
{10..18}, `n + 9 = rev(n)` on the a-b=-1 diagonal, their intersection {12} — is
base-10 and mod-9. Its only GF(37) content is placing 12 and 21 in ST, which
the docstring already calls "near-vacuous". The filename ends `_gf37` and the
file is not a GF(37) theorem. Recorded, not renamed: the mathematics in it is
correct and stands; the claim its name makes does not.

---

## 3. Two false negatives in this tool's own first run

Both were corrected before the numbers above, and both are worth knowing
because they bias in the flattering direction — they make the corpus look worse
than it is:

1. **Pass 1 alone over-reports Tier A.** 35 files survived the `P = 37`
   mutation, but 34 of them never reference `P` in any assertion — they
   hardcode the literal, in one case 85 times. The mutation never reached what
   they test. Pass 2 (literal mutation) exists for this, and moved 21 of those
   34 into Tier C.
2. **A short timeout looks like a failure.** Two files reported as "does not
   run" simply needed longer: `jc3_falsification.py` (29s) and
   `theorem_307_seed_orbit_residue_breakdown_gf37.py` (65s). Both pass. The
   tool now reports TIMEOUT separately from ASSERT and says to raise the
   timeout rather than assume breakage.

A mutation that crashes the file proves nothing either way, and is reported as
inconclusive rather than folded into either tier.

---

## 3b. The redundancy axis

Mutation cannot see redundancy: in a fixed computation every assertion passes
by construction, so nothing to delete or perturb changes the outcome. Three
shapes ARE detectable syntactically, and all three mean "this check could not
have been red".

```
D1  exact duplicate assertions, same scope            208
D2  tautologies: assert X == (X's own assigned RHS)    38
D3  conjunct subsumption: assert A; later assert A and B   197
                                                    -----
                                  443 of 10,266 assertions   4.3%
```

D2 is the cleanest — these cannot fail:

```python
DECADE = 10        ; assert DECADE == 10
PRIME_MIRROR = 31  ; assert 31 == PRIME_MIRROR
PHI_37 = 36        ; assert PHI_37 == 36
```

### The T316 gate shape

T120/121's redundancy was SEMANTIC — check 2 entailed checks 3, 4 and 5 — and
that is invisible to syntax. But it has a syntactic signature: a bundle of four
or more named booleans reported together. Across 480 theorem files that shape
appears **4 times in 3 files**, and one of them is T316 itself, which documents
the pattern rather than committing it.

The one real instance is `fps37_scanner.py:51`: fifteen booleans, every one of
the form `residue == <constant>`.

```
'is_null'      residue == 0      'is_lamed'        residue == 23
'is_unity'     residue == 1      'is_inv_3'        residue == 25
'is_trinity'   residue == 3      'is_scalar_137'   residue == 26
...                              'is_inv_unity'    residue == 36
```

They are MUTUALLY EXCLUSIVE by construction — at most one can be true. That is
T316 inverted: not several checks forced true together, but fifteen flags that
between them carry exactly one fact already known (the residue). Fifteen names,
zero information beyond the input. `fps37_scanner.py:74` by contrast holds four
genuinely independent predicates and is fine.

### A caveat about this detector

**The original T120/121 gate sits just under its threshold.** That dict is 5/9
boolean = 0.56 and the ratio cut is 0.6, so the strict pass misses it; only a
looser scan finds it. A detector tuned to miss its own motivating example is
weak evidence, and the "4 instances in 480 files" figure should be read as a
lower bound, not a clean count.

### What remains unmeasured

Semantic entailment among assertions is not detectable by any of this. T316's
redundancy surfaced only because the gate was a PREDICATE OVER A PARAMETER —
sweeping the seed made the implication visible. Most theorems here assert fixed
facts, so there is no parameter to sweep and no analogous test.

So the redundancy axis is **partially** measured: syntactic redundancy at 4.3%,
semantic entailment unmeasured and not reachable this way.

---

## 4. What this says about the T316 pattern

T316's failure mode — five displayed checks, two independent conditions — is
about *redundancy among assertions*, which mutation testing does not directly
detect. What it does detect is the adjacent failure: *assertions that hold
independently of the subject*. The corpus is in good shape on the second
(92%) and the first remains unmeasured at scale.

The general lesson all of it shares: a green check is evidence only in
proportion to how easily it could have been red. Counting checks measures
nothing; the useful question is how many of them could INDEPENDENTLY have
failed.

Three ways a check fails that test, all found in this corpus:
  - it references no data at all                     (796, 7.8%)
  - it restates something already asserted or assigned (443, 4.3%)
  - it holds for a prime that is not 37               (11 theorems)
and one that is not reachable by static analysis at all: it is entailed by a
sibling check. That last is the T316 case, and it is the one worth watching
by hand.

---

## Reproduction

```bash
python3 tools/mutation_audit.py --timeout 90
```

Writes and deletes temporary `_zzmut_*` files inside `math/theorems/`; it
cleans up in a `finally` block, and the run above left zero behind (verified
with `git status`).
