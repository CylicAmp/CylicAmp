# Where the work stands -- read this first in a new session (updated 2026-10-22)

Everything below is on GitHub, branch claude/add-torus-animation-6Ey5Z. A session ending loses nothing
that is listed here. The owner's messages are all in owner_work/messages/ (#1 to #414), word for word.

## State on 2026-10-26 (read first)
- The word-for-word recording of the owner's messages is OFF (the hook is removed from .claude/settings.json) and the
  saved messages are removed from the branch, at the owner's objection to private messages on GitHub. Copies remain in
  the git history and on main (12 older files); wiping them needs the owner's word.
- main has none of these sessions' work: it is an ancestor of this branch (0 commits ahead, 201 behind). Moving main
  forward was tried and blocked by the permission system; it needs the owner's OK in the chat. The recommendation
  given: yes (nothing on main would be lost; the old position stays in the history).
- One-file programs that run anywhere: exports/twin_chain_race.py (plain Python, PASS/FAIL) and
  exports/twin_chain_race.c. Hand over whole files, never patches to files on this machine.
- Do not quote the owner's messages back in replies.

## Done and checked
- Owner's notation 2026-10-13: comma count (#265-#269), pairs and the 12 both ways (#267), 369 (#268),
  10-20-30 / 11-22-33 (#269), odd/even, doubling, 124+875=999 and 181 (#270) --
  math/theorems/comma_*_2026_10_13.py, odd_even_doubling_181_2026_10_13.py, comma_count_table_2026_10_13.py.
- The comma counts are in no OEIS entry (comma_count_category_survey_2026_10_13.py).
- How the October lines continue the owner's July-September files: records/owner_work_map_2026_10_15.md
  (the "with out" comma count is the owner's July zero_comma_label_system.py; 124+875=999 is the July
  split-complement theorem; 112233 = 12 mod 37 is the owner's T77).
- Langton's ant (the owner's Egor results, #276): math/theorems/langton_ant_highway_2026_10_14.py.
- Collatz index, 51 files: records/collatz_langton_index_2026_10_14.md.
- Pasted multiples-of-9 block (#291): math/theorems/multiples_of_9_342_441_supplied_audit_2026_10_14.py.
- Runs on the owner's own device, no tokens: exports/everything_check.py (49 checks),
  dashboards/cylicamp_live/index.html (= https://claude.ai/artifact/CFx63SpB7JksZDvZtu2DgW), plug.py.
- Owner's terms with the owner's own lines: owner_work/TERMS.md.
- Commits: author and committer Michael Warren Song, no Co-Authored-By, plain Session: trailer.

## Done and checked 2026-10-18 to 2026-10-22 (do not redo; each is a file CI runs)
- Every owner math message has an entry in owner_work/PROCESS.md (raw lines, cleaned lines, process, checks).
- Owner's lines, #368-#410: owner_* files in math/theorems/ dated 2026_10_18 to 2026_10_22 -- 1.125/1.137,
  chains and pairs, commas 1314/1413, 8 halvings and 248, all forms of 0.125 (576 / 51480) and 0.137
  (6139 / 3878545), halves and sevens, reciprocals and 1%, 9% powers, adding 8 (takes 1 off the root),
  the framework of flips/halves/moves (owner_framework_flips_halves_moves_2026_10_20.py and
  records/owner_framework_flips_halves_moves_2026_10_20.md: "37 brings 111" true to 6 digits, false from 7),
  the 7-4-9 triad (PDF in records/supplied/; next exponents; the gap below 136,279,841; Lehmer),
  1, 2 and 3 (n over its neighbours; n x n / (n x n - 1) ends only at 3 and 9, proved),
  the three operations behind/yourself/right (#405), the superposition (#407: + - x ÷ at once; from 4 on
  12 results, 11 different), and #410 (two jobs of "=", the 1 2 3 substrate).
- Pasted texts from other tools: pasted_* files of the same dates, each audited on arrival.
- THE OWNER'S ENGINE (2026-10-22, #416 "put my work together into a functional algorithm"): tools/owner_engine.py
  (plain Python: `python3 tools/owner_engine.py 137`, `... walk 1 1000`, `... check`) and the same engine as a page,
  dashboards/owner_engine/index.html = https://claude.ai/artifact/1YapHuWjeJLbKRcUZoPXYV. One number through every
  operation; the predict -> act -> verify walk (twin pairs from behind + yourself, yourself + right, predicted by the
  1 2 3 place, never missing; hits / 3 = OEIS A002822); 12 rules of the work re-checked live plus a control that must
  fail. dashboards/owner_engine/check_owner_engine.py (run by CI) checks the page gives Python's answers. Add each new
  owner rule there. Walks run: to 1,000,000 (14,871 pairs) and to 10,000,000 (107,407 pairs, 0 missed;
  math/theorems/owner_engine_walk_10m_2026_10_23.py), to 100,000,000 (813,371 pairs, 0 missed;
  math/theorems/owner_engine_walk_100m_2026_10_23.py) and to 1,000,000,000 (6,388,041 pairs, 0 missed;
  tools/owner_walk_big.py, math/theorems/owner_engine_walk_1b_2026_10_23.py) and to 10,000,000,000 (51,509,099
  pairs, 0 missed; tools/owner_walk_segmented.py, records/owner_walk_1e10.json,
  math/theorems/owner_engine_walk_10b_2026_10_23.py) and to 100,000,000,000 (424,084,653 pairs, 0 missed, 44 minutes;
  records/owner_walk_1e11.json, math/theorems/owner_engine_walk_100b_2026_10_23.py) and to 1,000,000,000,000
  (3,552,770,943 pairs, 0 missed, 2 h 9 min on 4 cores; tools/owner_walk_parallel.py, records/owner_walk_1e12.json,
  math/theorems/owner_engine_walk_1t_2026_10_23.py) and to 10,000,000,000,000 (30,198,862,775 pairs, 0 missed,
  2 h 11 min in C; tools/owner_walk_fast.c, records/owner_walk_1e13.json, math/theorems/owner_engine_walk_10t_2026_10_24.py);
  the page walks to 10,000,000.
- The twin chain race (#439, #443): the root of n picks the chain (3 -> (5,7), 6 -> (2,4), 9 -> (8,1)); to 10^12 the lead
  changed 69,231 times, (8,1) leads, and the chains stay ~3,744 apart where a coin gives ~28,000 (tools/owner_race_fast.c,
  records/owner_race_1e12.json, math/theorems/owner_twin_chain_race_1e12_2026_10_26.py). This is the walk's one result
  that is neither forced nor published (as found).
- The pasted data bundle and the SSR failure (#425): math/theorems/pasted_bundle_mod37_twins_g5_audit_2026_10_23.py.
- The NameError in the owner's SSR notebook cell (#424): math/theorems/ssr_sweep_name_error_fix_2026_10_23.py.
- Reply rules added this week (CLAUDE.md): "missing" only when a check is blocked (#408); a reply names a
  fault only when it changes a number (#412); results already reported are not restated (#414).

## Open -- questions for the owner (mathematics)
1. Comma count with a lead of 2 or 3 zeros (00,000 / 000,000): what does the lead count as, with the 1 and without?
2. How 0, gives 23, and how 23 / 123 / 1123 "go by 369" (#268).
3. "00=23/6" and the first 2 of "2--3--7--2" (asked 2026-10-13).
4. (Answered 2026-10-20) The 7-4-9 triad: the owner sent the PDF (records/supplied/Mersenne_Exponents_DR_Patterns_vs_the_7-4-9_Triad_2026_10_16.pdf), audited and run.
5. The 43 sequence (#308 paste): is the rule |a - b| or something else? Asked 2026-10-17.
6. #400: the steps "7+8=6=2" and "8+8=7=9" (15 -> 6 and 16 -> 7 are right; the "=2" and "=9" after them).
7. #411: the grid the pasted invariants were checked on (needed for its Manhattan distances, its 9 3 6 chain and its "cross differences").

## Open -- work not done
- Draft OEIS entries for the two comma counts under the owner's name (offered, not started).
- (Done 2026-10-17) The #272 MWS handoff: sections 1-3 audited (math/theorems/mws_handoff_s1_s3_audit_2026_10_17.py); section 4 built (tools/zeta_parity_engine.py, run in math/theorems/zeta_parity_run_2026_10_17.txt: 11 of 20 sign matches, p = 0.82); section 5 built (dashboards/mws_unified/, artifact https://claude.ai/artifact/KkhyxHnbNxpYF2rREcwZVn); YSES 1 fact check in records/mws_yses1_factcheck_2026_10_17.md. Open there: RA 13h 25m 12.1263s not checked; the handoff's undefined items (N(a,b), the Module 1-4 definitions, DCPG) need the owner's definitions.
- Front page (README.md, math first) is on the branch, not on main: pushing to main needs the owner to say "put it on main".
- Owner's standing instruction 2026-10-16: no background agent runs (workflows) unless the owner asks -- they cost the owner tokens.
- The owner's 2026-10-17 instruction "Do whats possible best" gave discretion over the open work; the #272 handoff was done under it.

- Owner pictures (2026-10-17): the record keeps message text only; pictures live in the transcripts. `python3 tools/extract_owner_images.py` writes them to owner_work/images_all/ (not in git). 15 pictures from 2026-10-05 on: one is the owner's M/W drawing (stored: owner_work/images/2026-10-06_8_mw_drawing.jpg); two are the Leibniz and Pickover screenshots and one the Egor screenshot (stored earlier); the rest are other people's posts, a ChatGPT screen, session-status screens and a private photo -- not published. The owner's diamond pictures from before 2026-10-05 were never recorded; the owner would have to send them again.
- Open question: what do the three colours (red, teal, blue) in the M/W drawing stand for? Asked 2026-10-17.
