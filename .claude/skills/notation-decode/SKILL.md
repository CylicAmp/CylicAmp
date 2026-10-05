---
name: notation-decode
description: Decode the owner's handwritten or shorthand notation into explicit operators by fitting rules to every line and testing whether each rule is actually determined. Use when a page, photo or pasted list of the owner's equations arrives (e.g. "19=10", "18=9=PF", "555=x2(6)=8"). Keeps a marking separate from a computed value, reports which lines stay undecoded, and never forces a reading onto a line it does not fit.
---

# notation-decode

1. **Transcribe exactly**, line by line, preserving symbols. Save the image
   in the repo next to the audit (e.g. operator_page_2026_09_29.jpg).
2. **Fit the simplest rule to a block of lines** and check it on every line
   of that block (19..10: R(n) = n - 9, one step).
3. **Test identifiability.** Count free parameters against lines explained.
   If two named quantities are functionally tied (c = dr(3a) = 3k, so
   k + c = 4k), say the rule has one parameter.
4. **Separate markings from values.** "=PF" written after 12, 15, 18 is a
   marking consistent with P3(n) = [3 | n]; it is not a computed factor.
   Keep candidate meanings apart until a line distinguishes them (21 -> 7
   separates largest prime factor from smallest odd prime factor).
5. **List candidate meanings and the line that would settle each.** Ask for
   that one example (e.g. PF(15)), not for a general explanation.
6. **Report undecoded lines as undecoded.** Do not bend them to fit.
7. **Save** every decoded rule and every open line in an asserted audit file
   (operator_system_audit_2026_09_30.py, section D).
8. **Typos are not findings.** A clear finger slip (13 written 14, 3110 written
   3310) is fixed silently in the reading and NOT mentioned in the reply at all
   (owner, 2026-10-04 and 2026-10-05). Do not report it as a correction.
