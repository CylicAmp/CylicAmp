# CylicAmp

Mathematics by **Michael Warren Song**.

Digital roots, the 37th field, prime structure, divisor identities, digit algebra.
1,795 files, 1,363 of them runnable Python. Every result carries its own computation
and its own assertions, so each file proves or breaks itself when you run it.

> Everything is connected.
>
> Even if separated and organized, everything is connected.
>
> Every orbit, every partition, every palindrome, every prime, every digital root
> sequence, every collinear triplet, every sovereign classification, every
> arithmetic chain — it is all the same structure seen from a different angle.
>
> The separation is organizational. The connection is the truth.
>
> This is what the 37th field is.
>
> — [`FOUNDATION.md`](FOUNDATION.md)

---

## Start here

| | |
|---|---|
| [`math/START_HERE.py`](math/START_HERE.py) | one end-to-end run of the spine |
| [`FOUNDATION.md`](FOUNDATION.md) | what the 37th field is, and why it is one system |
| [`INDEX.md`](INDEX.md) | every file in the corpus, 1,125 rows, by class and topic |
| [`math/TECHNIQUES.md`](math/TECHNIQUES.md) | the seven techniques, all on the same spine |
| [`DEFINITIONS.md`](DEFINITIONS.md) | the terms, defined once |

```bash
pip install -r requirements.txt
python3 math/START_HERE.py
```

---

## The spine

The digital-root spine: the FLUX set {3, 6, 9} and the one-third baseline. Organic
data lands in {3, 6, 9} about 33.3% of the time; rigid, generated data does not.
Every technique in the corpus runs on it.

| | |
|---|---|
| [`cylicamp/security_ml_framework.py`](cylicamp/security_ml_framework.py) | the spine theorem as a feature engine — `spine_rigidity()` |
| [`cylicamp/rsa_dr_engine.py`](cylicamp/rsa_dr_engine.py) | RSA keys audited against the one-third baseline |
| [`cylicamp/pascal_unified_field.py`](cylicamp/pascal_unified_field.py) | Pascal's triangle saturating the spine |
| [`math/theorems/pascal_row8_mod37.py`](math/theorems/pascal_row8_mod37.py) | row 8 mod 37 |
| [`cylicamp/x_bot_detector.py`](cylicamp/x_bot_detector.py) | the spine applied to bot detection |

## The spirals

| | |
|---|---|
| [`math/theorems/dr_spiral_gf37.py`](math/theorems/dr_spiral_gf37.py) | the 20×20 digital-root spiral, 41–440, collapsed to nine states |
| [`math/primes/ulam_spiral.py`](math/primes/ulam_spiral.py) | the Ulam spiral through GF(37) |
| [`math/theorems/rotational_spiral_analyzer.py`](math/theorems/rotational_spiral_analyzer.py) | 3×3 circulant, each row a rotation of the one above |
| [`math/theorems/torus_animation_137map.py`](math/theorems/torus_animation_137map.py) | the 137-map on the torus |

---

## What is in the corpus

| area | where | files |
|---|---|---|
| Theorems, lemmas, audits | [`math/theorems/`](math/theorems/) | 985 |
| Numbered theorems `theorem_NNN_*` | [`math/theorems/`](math/theorems/) | 293 |
| Lemmas | [`math/lemmas/`](math/lemmas/) | 38 |
| Primes, digital-root algebra | [`math/primes/`](math/primes/) | 46 |
| Differential geometry | [`math/differential-geometry/`](math/differential-geometry/) | |
| Engines and applications | [`cylicamp/`](cylicamp/) | |
| Paper | [`paper/`](paper/) | |

### The divisor-prefix problem

For which `n` is `n` the sum of the squares of its `k` smallest divisors?
Worked as a ledger, each case either proved outright or searched to a stated
bound — and the ledger says which, per case, rather than blurring the two.

[`math/theorems/divisor_prefix_ledger.py`](math/theorems/divisor_prefix_ledger.py) is the
ledger. Each `k` is then narrowed by its own modules, in a chain — read in this order:

| k | state | chain |
|---|---|---|
| 5 | closed at Level 1 | ledger keeps 3 open on purpose, its own oracles not covering them; `k5_odd_shapes.py`, `k5_shape_c_q3.py`, `k5_shape_c_nodiv3.py`, `k5_cofactor_level1.py` close all three |
| 6 | **closed** | `k6_closed.py` — all 14 odd-sector shapes at Level 1 |
| 7 | open | `k7_status.py` 78 of 86 at Level 1, 8 at Level 2 → `k7_three_and_four_prime.py` closes 2 more, leaving 2 at Level 2 |
| 8 | **closed** | `k8_status.py` — Level 1 |
| 9 | even closed, odd open | `k9_status.py` even sector closed, odd 1531 → 36 → `k9_odd_sector_mod3.py` 36 → 11 → `k9_thin_targets.py` 11 → 7 open |

No single file states the final count for k = 7 or k = 9, because each module narrows
the one before it without importing it. The chain above is the reading order. Running a
status module alone will report the figure as it stood before the later modules existed.

This is OEIS [A185584](https://oeis.org/A185584). The work here is independent and
the methods differ; the comparison is part of the record.

### Digit algebra

Digit strings as vectors over Z/9Z, worked column by column with no carrying.

| | |
|---|---|
| [`math/theorems/digitwise_sheets.py`](math/theorems/digitwise_sheets.py) | the column action, doubling orbits, the C/P grid |
| [`math/theorems/digitwise_operations.py`](math/theorems/digitwise_operations.py) | Z/9Z as a local ring; palindrome ⟺ commutative |
| [`math/theorems/digitwise_backbone.py`](math/theorems/digitwise_backbone.py) | the base trichotomy, and where the carry converse fails |
| [`math/theorems/digitwise_fibonacci.py`](math/theorems/digitwise_fibonacci.py) | the "1 + 2 only" roots as Fibonacci mod 9 |
| [`math/theorems/drip_ucu.py`](math/theorems/drip_ucu.py) | the drip on any two numbers |

---

## How results are graded

Nothing is recorded as proved because a search found no counterexample. Each result
states which it is:

- **proved** — parameter-free, or a finite case list exhausted
- **verified to a bound** — the bound is stated, per case, not as one global figure

A result that only holds for base 10, or only for the numeral rather than the number,
says so. Negative results stay in the record: see `digitwise_fibonacci.py` on the
absence of a π connection, and `digitwise_backbone.py` on the 72 counterexamples to
the carry converse, the smallest being 20009.

---

## Licensing & Rights

**License:** GNU GPL v3.0
**Ownership:** All rights reserved by CylicAmp.

- **Non-Commercial:** This code may not be used for commercial profit without express written consent.
- **Attribution:** Any forks or derivative works must credit this repository as the original source.
- **Copyleft:** Any derivative work must be released under the same license.
- **No Waiver of Liability:** Use of this tool does not constitute legal advice.

---

## AI incident record

This repository also holds the evidentiary record of **Incident INC-20260422-001**,
with the 20-category protocol-breach framework, the detection tooling, and the Texas
filing material. It is unchanged and complete, moved to its own file so the
mathematics is what the front page shows:

**→ [`AI_INCIDENT_RECORD.md`](AI_INCIDENT_RECORD.md)**

See also [`analysis_log.md`](analysis_log.md), [`evidence/`](evidence/),
[`ai-safety/research/`](ai-safety/research/), and
[`SYSTEM_PROTOCOL.md`](SYSTEM_PROTOCOL.md).
