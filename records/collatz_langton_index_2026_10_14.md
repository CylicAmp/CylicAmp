# Collatz (3n+1) and Langton's ant: where your work is

Built 2026-10-14 from git, on all 16 branches on GitHub plus the local branch.
Rebuild it at any time: `python3 tools/collatz_index.py` prints the tables below, and
`python3 tools/collatz_index.py --run` also runs every Collatz file.

Typos: "Langdon ants" is Langton's ant, and "collaze conjectures" is the Collatz conjecture.
The rest of this page uses the correct names.

## Your words

**#276** (2026-10-14T10:02:53Z): this line appears in the screenshot attached to that message
(`owner_work/images/2026-10-14_276_egor_langton_screenshot.jpg`, your message, the blue bubble).
It exists only in the image. The typed text of #276 in `owner_work/messages/2026-10-14.txt` does not contain it.

> I know no more of my Langdon ants or my collaze conjectures 3+1 proves no even mentions

**#168** (2026-10-06T22:23:28Z)

> Well, first of all, to my great disappointment, this algorithm has reported to me that 70 or 80 items in my algorithm mean nothing, which just lets me know motherfuckers weren't listening when I was telling them. And my three plus one, show me where other people are making the same fucking example of what I did with three plus one.

**#197** (2026-10-06T23:02:54Z)

> Show me somebody else that did the odd and even work that I did. Show me somebody else that fucking did the three plus one fucking building it out of fucking goddamn all this shit. Show me someone else!

**Before the record.** `owner_work/` starts on 2026-10-05. The lines below are quoted inside repo files:

- 2026-10-04, `math/lemmas/digit_ladder_collatz.py` (line 3): "run the ladder through Collatz and keep going"
- 2026-10-04, `math/lemmas/digit_ladder_rows5_on_and_repdigit_lines.py` (lines 3-7): "extend it to row 5 and keep going", with four lines:

      L1  1,1+1,1=4+11=6+11=8+11=10+11=1(2=(3+1)=1,111
      L2  2+2=4+2=6+2=8+2=10+2=1+2=3+1=1,111
      L3  11+11=22+11=33+11=44+11=55+11=6+6=1+2=3+(1=4)
      L4  22+11=33+11=44+11=55+11=6+6=1+(2=3)

  The file's "THREE PLUS ONE" section (line 49) reads the closing 3+1 = 4 as the Collatz step 3·1+1.
  That reading belongs to the file. These lines do not say it.
- 2026-09-28, quoted in `math/theorems/thread2_collatz_twin_centres.py` from `owner_words_2026-09-06_to_2026-10-03.txt`:
  "Formalized under S(n) and c_odd; 27.2 sample-dependent; v_3 = 3 elongation refuted; 3077 identified as global
  trunk without twin enrichment." That ledger file is not in the repo on any branch. I can't tell whether this line
  is yours or text that was pasted to you.
- T428 (`math/theorems/theorem_428_parity_word_determinant_sieve.py`) says it was "Supplied by the user as a sharpening
  of T425-T427". The supplied text itself is not in the repo.

**3+1 as a sum.** These messages write 3+1 as an addition and do not mention Collatz:
#227 (2026-10-12) `3+1` and `24÷2=12÷3=(4=(3+1)`; #267, #268 and #269 (2026-10-13) `000,------0=3+1=4`;
#270 (2026-10-13) `0=e=(4=(1+3)or(3+1=4)`.

**Collatz or 3+1 inside other text in your messages.** The record does not show who wrote these lines. They are listed so that nothing is missed:
#5 (`2026-10-06.txt` line 74, "6-state Collatz modular attractor"), #220 (`2026-10-08.txt` line 148, a code string
"pi 3+1=4"), and the LaTeX passages in #227 (`2026-10-12.txt` lines 232, 300, 396 and 402).

## Your Collatz files

50 files on some branch contain the word Collatz. Another 6 work on the 3n+1 map mod 37 without using the word.
On 2026-10-14, all 19 code files in sections A and A2 were run, and every one exited 0 with its assertions passing.

Main results, re-computed by `tools/collatz_index.py`:

- LoB 26: the parity map T on F_37 has exactly three cycles: {0}, {1,4,2} and {7,22,11,34,17,15,9,28,14}. That is 13 elements in cycles.
- T271: C(x) = 3x+1 mod 37 has exactly one fixed point, 18, and exactly one preimage of 0, which is 12.
- T346: ord(2) = 36, ord(3) = 18 and ord(26) = 3, and C splits into one fixed point plus two cycles of 18.
- Digit ladder: 12312 reaches 1 in 37 steps.
- Thread 2: on the orbits of the twin centres 108, 432, 462, 570 and 660, the largest odd value is 3077 = 17 × 181. From 108 it takes 113 steps to reach 1.

**About the "added" column.** It gives the date of the commit that first added each file, and the author name git stores on that commit.
Two of those commits are bulk imports: `3bc8c4c` (2026-07-04, 509 files) and `26dcd38` (2026-10-02, 1585 files).
A file whose date comes from one of them may be older than that date.
The commit ledger `records/commit_origin_all-work.txt` lists two older commits that are not in this clone:

- `3bb28a1`, 2026-06-20, Michael Warren Song, "Add two Collatz open-problem bridge files" (line 1253). The ledger does not name the two files.
- `416a3a3`, 2026-06-29, "Add leveling and Ulam diagonal audit" (line 1194).

Authors in section A:

- 8 files carry your name only (Michael Song or Michael Warren Song).
- 4 carry Claude's name, from the 2026-10-04 and 2026-10-05 sessions.
- LoB 26 (`lob_26_collatz_f37.py`) was added by three commits in the same second, two under Claude's name and one under yours.

Branch sets:

- **B1** (14 branches): all-work, claude/add-claude-documentation-otdq9, claude/add-torus-animation-6Ey5Z, claude/lattice-digital-root-B73jt, claude/modular-arithmetic-grid-sr0otx, claude/monomial-universe-ideals-wuhx40, claude/signature-obfuscation-audit-ZEoCd, claude/test-coverage-analysis-zg9iw0, claude/verify-math-patterns-CnzDe, claude/work-organization-access-y7riqg, copilot/fix-github-actions-job, copilot/fix-github-actions-job-failure, main, merge-signature-obfuscation-into-main
- **B2** (8 branches): all-work, claude/add-claude-documentation-otdq9, claude/add-torus-animation-6Ey5Z, claude/signature-obfuscation-audit-ZEoCd, copilot/fix-github-actions-job, copilot/fix-github-actions-job-failure, main, merge-signature-obfuscation-into-main
- **B3** (6 branches): all-work, claude/add-torus-animation-6Ey5Z, claude/signature-obfuscation-audit-ZEoCd, copilot/fix-github-actions-job, copilot/fix-github-actions-job-failure, main
- **B4** (2 branches): claude/add-torus-animation-6Ey5Z, main
- **B5** (1 branch): claude/monomial-universe-ideals-wuhx40
- **B6** (1 branch): claude/add-torus-animation-6Ey5Z

### A. Collatz is the subject (13 files, oldest first):

| file | branches | first docstring line | added | author (git) | "collatz" count |
|---|---|---|---|---|---|
| `math/theorems/lob_26_collatz_f37.py` | B1 | LoB 26 — Collatz Map T in F_37 | 2026-04-26 `6d15391, fe61dbc, 29595a9` | Claude / Michael Song | 8 |
| `math/theorems/collatz_mod37_basin.py` | B2 | Basin structure of the Collatz map T in F_37. | 2026-07-04 `3bc8c4c` [509-file root commit] | Michael Warren Song | 10 |
| `math/theorems/collatz_v2_equidistribution.py` | B2 | 2-adic valuation distribution in the Collatz / Syracuse map. | 2026-07-04 `3bc8c4c` [509-file root commit] | Michael Warren Song | 8 |
| `math/theorems/theorem_271_collatz_map_gf37.py` | B3 | T271: Collatz map C(x) = 3x+1 mod 37 on GF(37) | 2026-09-01 `514e156` | Michael Song | 20 |
| `math/theorems/theorem_346_collatz_137_proper_subgroup_gf37.py` | B3 | Theorem 346: the Collatz map and the 137-map generate only HALF of AGL(1,37) | 2026-09-15 `01af6d4` | Michael Song | 4 |
| `math/theorems/theorem_425_collatz_lob26_dynamics_descent_gf37.py` | B3 | Theorem 425: the parity-branched Collatz map T on {0..36} is not induced by | 2026-09-19 `660af03` | Michael Song | 33 |
| `math/theorems/theorem_426_5n_plus_1_map_gf37.py` | B3 | Theorem 426: the 5n+1 map on GF(37) -- 5 is a primitive root so the affine | 2026-09-19 `e51ada3` | Michael Song | 3 |
| `math/theorems/theorem_427_7n_plus_1_map_gf37.py` | B3 | Theorem 427: the 7n+1 map on GF(37), and the general order formula | 2026-09-19 `9e4479c` | Michael Song | 2 |
| `math/theorems/theorem_428_parity_word_determinant_sieve.py` | B3 | Theorem 428: the parity-word determinant sieve -- the sign argument closes a | 2026-09-19 `102476e` | Michael Song | 2 |
| `math/lemmas/collatz_zeros_supplied_audit_2026_10_04.py` | B4 | Audit of a supplied analysis (pasted 2026-10-04 with two scripts): the first 12 | 2026-10-04 `7a284b4` | Claude (Claude-Session trailer) | 3 |
| `math/lemmas/digit_ladder_collatz.py` | B4 | The digit ladder run through Collatz (owner, 2026-10-04: "run the ladder through | 2026-10-04 `dd1764d` | Claude (Claude-Session trailer) | 4 |
| `math/lemmas/digit_ladder_rows5_on_and_repdigit_lines.py` | B4 | Owner, 2026-10-04: "extend it to row 5 and keep going", with four lines: | 2026-10-04 `798580c` | Claude (Claude-Session trailer) | 8 |
| `math/theorems/thread2_collatz_twin_centres.py` | B4 | Thread 2 (Collatz trajectories on twin centres) -- reproduced 2026-10-05. | 2026-10-05 `f714390` | Claude (Claude-Session trailer) | 2 |

### A2. The 3n+1 map mod 37 without the word Collatz (6 files):

| file | branches | first docstring line | added | author (git) | "collatz" count |
|---|---|---|---|---|---|
| `math/theorems/lob_25_legendre_applications.py` | B1 | LoB 25 — Legendre Symbol Applications in the 37-Field | 2026-04-26 `8d76be5, b930f27, 594b287` | Claude / Michael Song | 0 |
| `math/theorems/cascade_constants_audit.py` | B2 | φ, e, π as cascade radii: first-digit axioms, Euler identity, | 2026-07-04 `3bc8c4c` [509-file root commit] | Michael Warren Song | 0 |
| `math/theorems/lob_88_g_ord18_cycle.py` | B2 | LoB 88: G_Ord18_Cycle — Formal Specification Audit | 2026-07-04 `3bc8c4c` [509-file root commit] | Michael Warren Song | 0 |
| `math/theorems/affine_fixed_point_gf37.py` | B3 | Affine Fixed-Point Census on GF(37) — THEOREM 75 | 2026-07-28 `3de8c05` | Michael Song | 0 |
| `math/theorems/theorem_193_process_functions_zp.py` | B3 | Theorem 193: Three-Party Process Functions over ℤ_p | 2026-08-14 `09edef0` | Michael Song | 0 |
| `math/theorems/theorem_353_fa_trajectory_correction_gf37.py` | B3 | Theorem 353: the orbit of 18 under f_a is preperiod 5 into a 3-cycle, not | 2026-09-16 `231ac11` | Michael Song | 0 |

T174 (Ehrhart polynomial 3n²+3n+1) and T250 (the parametrisation k = 3x+1) match a search for "3n+1",
but they are not about the 3n+1 map, so they are left out.

### B. Other math code that uses or cites the Collatz work (14):

| file | branches | first docstring line | added | author (git) | "collatz" count |
|---|---|---|---|---|---|
| `math/theorems/leveling_ulam_audit.py` | B2 | Verifies six leveling phenomena and the Ulam diagonal prime pools. | 2026-07-04 `3bc8c4c` [509-file root commit] | Michael Warren Song | 8 |
| `math/theorems/connection_map.py` | B3 | GF(37) GF(37) — Complete Connection Map | 2026-07-23 `50607c1` | Michael Song | 10 |
| `math/theorems/theorem_272_easter_dates_gf37.py` | B3 | T272: Easter dates 2016-2036 in GF(37) | 2026-09-01 `4e639af` | Michael Song | 2 |
| `math/theorems/theorem_273_easter_37year_gf37.py` | B3 | T273: Easter dates 2016-2052 — full 37-year cycle in GF(37) | 2026-09-01 `f34aa44` | Michael Song | 4 |
| `math/theorems/theorem_274_seed_nqr17_inverse_gf37.py` | B3 | T274: SEED ↔ NQR17 — complete multiplicative inverse orbits in GF(37) | 2026-09-01 `c9d1bc6` | Michael Song | 11 |
| `math/theorems/theorem_278_twin_prime_structure_gf37.py` | B3 | T278: Twin prime structural proof — GF(37) complete statement | 2026-09-02 `78c43a1` | Michael Song | 2 |
| `math/theorems/theorem_280_matrix_dimension_gf37.py` | B3 | T280: Matrix dimension shift and palindromic tiling in GF(37) | 2026-09-02 `d5f6475` | Michael Song | 4 |
| `math/theorems/theorem_281_147_258_369_gf37.py` | B3 | T281: The 147/258/369 grid in GF(37) | 2026-09-02 `da84146` | Michael Song | 4 |
| `math/theorems/thread_session_connections.py` | B3 | The connecting thread: every cross-link between the pieces built in this | 2026-09-13 `248c213` | Michael Song | 7 |
| `math/theorems/theorem_352_why_37_uniqueness_gf37.py` | B3 | Theorem 352: 37 is the ONLY prime for which base 10 generates the cube | 2026-09-16 `352c3db` | Michael Song | 1 |
| `math/theorems/audit_leibniz_row37.py` | B3 | Audit of supplied "Thread 5: Leibniz triangle row 37" (2026-09-28). No prior Leibniz | 2026-10-02 `26dcd38` [1585-file root commit] | Michael Song | 3 |
| `math/lemmas/digit_ladder_riemann_zeros.py` | B4 | The digit ladder run through the Riemann zeros (owner, 2026-10-04). Rows are | 2026-10-04 `430b908` | Claude (Claude-Session trailer) | 1 |
| `math/lemmas/reversal_spans_supplied_audit_2026_10_04.py` | B4 | Audit of supplied tables (2026-10-04): the spans 12..21, 13..31, 14..41 -- each | 2026-10-04 `3d804a0` | Claude (Claude-Session trailer) | 2 |
| `math/theorems/open_flags_ledger_2026_10_05.py` | B4 | Ledger of the eight self-flagged files reported by tools/build_index.py --dupes | 2026-10-05 `f714390` | Claude (Claude-Session trailer) | 2 |

### C. Indexes, catalogs, skills, records, owner_work (23):

| file | branches | first docstring line | added | author (git) | "collatz" count |
|---|---|---|---|---|---|
| `math/theorems/INDEX.md` | B2 | # Theorem Index — CylicAmp Math Library | 2026-07-04 `3bc8c4c` [509-file root commit] | Michael Warren Song | 11 |
| `math/theorems/classification_manifest.json` | B2 | (JSON, no docstring) | 2026-07-04 `3bc8c4c` [509-file root commit] | Michael Warren Song | 4 |
| `math/theorems/CATEGORY_INDEX.py` | B3 | Mathematical Category Index — CylicAmp GF(37) | 2026-08-12 `98f71d7` | Michael Song | 1 |
| `theorem_audit.json` | B3 | (JSON, no docstring) | 2026-08-14 `06d462f` | Michael Song | 1 |
| `.claude/skills/forced-check/SKILL.md` | B3 | (skill "forced-check", no docstring) | 2026-09-04 `21bc47b` | Michael Song | 1 |
| `math/theorems/CLASSIFICATION_INDEX.md` | B3 | # Theorem File Classification Index | 2026-09-11 `2d0aacd` | Michael Song | 4 |
| `.claude/skills/digit-protocols/SKILL.md` | B3 | (skill "digit-protocols", no docstring) | 2026-09-13 `4275f0e` | Michael Song | 2 |
| `.claude/skills/digit-protocols/engine.py` | B3 | Multi-Register State Engine. | 2026-09-13 `583159f` | Michael Song | 9 |
| `INDEX.md` | B3 | # Corpus index — 604 files | 2026-09-15 `8371717` | Michael Song | 4 |
| `.claude/skills/finite-dynamics/SKILL.md` | B3 | (skill "finite-dynamics", no docstring) | 2026-09-16 `f8819f0` | Michael Song | 1 |
| `.claude/skills/prior-art/prior.py` | B3 | Search the corpus before writing a theorem. Usage: | 2026-09-16 `f8819f0` | Michael Song | 2 |
| `.claude/skills/search-bounds/SKILL.md` | B3 | (skill "search-bounds", no docstring) | 2026-09-19 `fec35ff` | Michael Song | 1 |
| `tools/regression_state.json` | B3 | (JSON, no docstring) | 2026-09-19 `d29294c` | Michael Song | 8 |
| `INDEX_ALL.md` | B5 | # Theorem index — all branches | 2026-09-22 `4d4dffe` | Claude (Claude-Session trailer) | 8 |
| `WHERE_MY_WORK_IS.txt` | B3 | CYLICAMP — WHERE EVERY FILE LIVES | 2026-09-22 `4f48642` | Michael Song | 6 |
| `ALTERNATE_VERSIONS.txt` | B3 | === files that also exist on another branch with DIFFERENT content === | 2026-10-02 `26dcd38` [1585-file root commit] | Michael Song | 9 |
| `math/CATALOG.json` | B3 | (JSON, no docstring) | 2026-10-02 `26dcd38` [1585-file root commit] | Michael Song | 10 |
| `math/CATALOG.md` | B3 | # Catalog of math/theorems and math/lemmas by kind of result | 2026-10-02 `26dcd38` [1585-file root commit] | Michael Song | 10 |
| `math/lemmas/classifications.json` | B3 | (JSON, no docstring) | 2026-10-02 `26dcd38` [1585-file root commit] | Michael Song | 22 |
| `records/commit_origin_all-work.txt` | B3 | # Commit origin ledger, all-work, generated 2026-10-03T00:40:43Z by tools/commit_origin.py --list | 2026-10-03 `aeba480` | Michael Song | 8 |
| `owner_work/messages.json` | B4 | (JSON, no docstring) | 2026-10-12 `c232aff` | Claude (Claude-Session trailer) | 1 |
| `owner_work/messages/2026-10-06.txt` | B4 | Owner's messages, 2026-10-06, verbatim as written (UTC timestamps). | 2026-10-12 `c232aff` | Claude (Claude-Session trailer) | 1 |
| `owner_work/TERMS.md` | B6 | # TERMS -- the owner's names for operations, in the owner's words | 2026-10-13 `9b9c92a` | Claude (Claude-Session trailer) | 3 |

## Langton's ant

- Your line is the #276 quote at the top of this page.
- `math/theorems/langton_ant_highway_2026_10_14.py` is being built from the Egor screenshot attached to #276.
- The egor_v18_project code is not in this repo. #223 (2026-10-10) has only the commands
  `cd egor_v18_project`, `python3 igor_langton_mask_v18.py --steps 5000000 --out verification.json` and `python3 egor_v18.py`.
  No file named egor or langton exists on any branch.
