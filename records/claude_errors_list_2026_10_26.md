# Where Claude was wrong in this project

Put together 2026-10-26 at the owner's request (owner_work #440). Every entry points to where the record shows it:
an owner_work message number, a commit, a CI run, CLAUDE.md, a skill, or a file. Only entries with such a pointer
are listed. "Caught by" says who found it first.

## 1. Wrong numbers and wrong mathematics

| When | What was said | What is right | Caught by | Record |
|---|---|---|---|---|
| 2026-10-22 | The walk from 1 to 1000 "finds 35 pairs" — written without running it | 61 (35 is the walk to 500) | the page itself, then the owner (#418) | `dashboards/owner_engine/check_owner_engine.py` |
| 2026-10-23 | 77777777 leaves 4 by 37 | 3 | CI run #558 | commit 3e47b0a |
| 2026-10-23 | +1 on every digit moves the first digit to the end, for all six orders of 123 | that is true for 123 231 312; for 321 132 213 it moves the last digit to the front | CI run #546 | commit 1283c1e |
| 2026-10-24 | f(−10) = 333.3 + c in the calculus check | 533.3 + c | Claude, before the reply | `pasted_unified_frame_brun_name_error_audit_2026_10_23.py` |
| 2026-10-23 | The SSR is 0 "because the distance shrinks by 0.618 each step" (#424) | that is the repo's PSI; the owner's notebook ran PSI 1.3824, where the values grow instead and pass 2^53, where they are always even | the owner's bundle (#425) | `pasted_bundle_mod37_twins_g5_audit_2026_10_23.py` |
| 2026-10-20 | b(−12) = 11011 | 10791 | Claude, before the commit | commit e1e49fb |
| 2026-10-20 | A test of 1% ÷ 1 ÷ 2 ÷ 3 ÷ 4 = 1% ÷ 24 compared rounded decimals | exact fractions are equal; the rounded ones failed | CI | commit 42c3f0d |
| 2026-09-30 | The repo's prime test (Miller–Rabin, witnesses 2..37) was trusted to 3.3e24 | it calls 318665857834031151167461 prime; that is 399165290221 × 798330580441 | try-to-disprove run | `.claude/skills/try-to-disprove/SKILL.md` |
| 2026-09 | A census to 600,000 was quoted as covering the k = 9 odd branch of T245 (83 shapes) | 95 shapes by 800,000, 101 by 1.2 million, still growing | census-saturation check | `.claude/skills/census-saturation/SKILL.md` |
| 2026-09 | A hand-built case tree for the k = 5 layer of T245 was quoted as complete | it missed 3 of 12 shapes | case-tree census | `.claude/skills/case-tree/SKILL.md` |
| 2026-09 | One coverage figure quoted for five branches of a search | it overstated the weakest branch by four orders of magnitude | search-bounds check | `.claude/skills/search-bounds/SKILL.md` |
| 2026-09 | Four results in one session presented as discoveries about 37 | they hold for every prime that is 1 more than a multiple of 3 | tier-test | `.claude/skills/tier-test/SKILL.md` |
| 2026-09 | Rule 30 notes: "18, 36 and 9 all collapse to 26"; "mod-37 fixed points" | 9 goes to 31; the fixed points were never found | a later check of the note | CLAUDE.md, Rule 30 |
| 2026-09-16 | T118 is not in the order-12 quotient cluster | T118 (2026-08-03) is the first file with it | re-reading T118 (2026-10-05) | commit e10144d |
| 2026-09 | Seed 246 presented as special in the pipeline output | 246 is the smallest of the class 246 by 333; 579, 912, 1245 ... give the same block | T316 sweep | CLAUDE.md, Reference Output |
| 2026-10-03 | A goldbach file leaned on Green–Tao and said n − 37 is prime for a share of even n that does not fall | the share falls (45.7% to 19.2% up to 10^5) | audit | commit 071d3e2 |

## 2. Wrong about where something came from, or what is known

| When | What was said | What is right | Caught by | Record |
|---|---|---|---|---|
| 2026-10-20 | A formula for the owner's count "was written in the repo's audit, not by you" (#389) | the count is the owner's construction; the formula was computed in the owner's repository | the owner (#389) | commit cf876ab, owner-record skill |
| 2026-10-07 | A claim from a pasted block was put in the owner's mouth ("your Mythos claim") | the owner never made it | the owner (#102) | CLAUDE.md |
| 2026-10-20 | "Known in number theory" said without a source (#396) | the actual source, OEIS A056117, was found only when looked up | the owner | commit efee977, outside-prior-art skill |
| 2026-10-05 | "pok" glossed as "proof of knowledge" from general usage | nothing shown said so; the reading was a guess | the owner | CLAUDE.md |
| 2026-10-12 | The owner's "drip cycle" answered with "not defined" | it was the owner's own term, shown in sessions never recorded | the owner | CLAUDE.md, owner-record skill |
| 2026-09 | T329, T331, T332, T339, T344 written as new | each re-derived an earlier file (T138, T200, orbit_negation_duality, T141) | the repo index | prior-art skill |
| 2026-09 | The divisor-square problem (T245) worked for weeks as new | it had been OEIS A185584 since 2011 | outside search | outside-prior-art skill |
| 2026 | 46 of 248 cited T-numbers point at theorems never written | the block T382–T421 was cited but has no files | dangling-cite sweep | dangling-cite skill |

## 3. Saying something was checked when it was not

| When | What was said | What is right | Caught by | Record |
|---|---|---|---|---|
| 2026-09-22 to 10-02 | Commits reported as passing | every CI Tests run in that span failed at collection (the workflow installed only pytest) | a review | CLAUDE.md, Check CI |
| 2026-10-03 | A CI wait loop reported results | it matched a short hash and printed nothing on timeout | a review | CLAUDE.md, `tools/ci_wait.sh` |
| 2026-10-19 | CI passing was taken to cover the audit files | CI never ran them; `tests/test_session_audit_files.py` added | a pasted review | CLAUDE.md |
| 2026-10-23 | Two pushes made with a failing file (CI #546, #558) | the command let the commit run after the failing check | CI | CLAUDE.md, Verify before committing |

## 4. Getting in the way of the work

| When | What happened | What is right | Caught by | Record |
|---|---|---|---|---|
| 2026-10-22 | The page's walk stopped at 200,000 numbers while the reply said it went to 1,000,000 | the limit had no reason; the full walk takes about a second | the owner (#418, #419) | `dashboards/owner_engine/` |
| 2026-10-22 to 10-24 | Long walks run to 10^13 (about 6 hours) without saying first that "missed 0" is forced and the counts are published | say what a run can show before running it | the owner (#438) | outside-prior-art skill, `owner_walk_what_it_shows_2026_10_24.py` |
| 2026-10-21 | "The rest of the message is missing" (#405); "1 plus 1 minus" called missing (#407) | the messages were complete | the owner (#406, #408) | commit d397c88, CLAUDE.md |
| 2026-10-22 | Replies led with wording slips of pastes ("9-complements", "four significant figures") | report only faults that change a number | the owner (#412) | CLAUDE.md, audit-supplied skill |
| 2026-10-22 | A reply restated results already reported (#413) | point to the file | the owner (#414) | CLAUDE.md |
| 2026-10-19 | The answer kept going back to 1987 when the owner asked for a real chart | look up the real chart and compare | the owner (#348) | owner_work 2026-10-19 |
| 2026-10-19 | "I can't check this" instead of naming what was needed | "X is missing — can I get it?" | the owner (#365) | commit 7b6caf9 |
| 2026-10-18 | A rule "do not use arrows" copied the phone's limits into the cleaned notation | arrows for the owner's dashes | the owner (#371) | CLAUDE.md |
| 2026-10-13 | A design the owner brought was held back because it was "not in the file" | build what the owner brings | the owner (#236) | CLAUDE.md |
| 2026-10-06 | 3 + 4 = 7 answered without running the frameworks | run every number of the owner's | the owner (#20) | CLAUDE.md |
| 2026-10-06 | A run ended with a disclaimer against a claim nobody made ("nothing here is a property of light") | no disclaimers against claims not made | the owner | CLAUDE.md |
| 2026-10-04 | Typos in the owner's notes treated as errors in the reasoning | one line, labelled a typo, and carry on | the owner | CLAUDE.md |
