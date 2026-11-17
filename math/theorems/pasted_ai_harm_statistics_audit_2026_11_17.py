# CLASS: AUDIT
"""
Pasted text (2026-11-17), from another tool, relayed by the owner ("look into"): a parametric estimate of about 60
severe adverse outcomes a year (IQR 30-120) set against an AI-harm database and four studies. Each cited source was
read (records/ai_harm_statistics_sources_2026_11_17.json holds the quotes and links).

SOURCE BY SOURCE:
  AI Companion Mortality Database (aimortality.org, v4.0.0): 37 deaths, 25 incidents, 18 users + 19 third parties,
    March 2023 - October 2026 -- right. "16 fatalities in 2025" -- wrong: 16 incidents, 18 deaths (the field holding
    16 was renamed in v4.0.0 "because it never counted deaths"). Oct 15, 2026 is the archive date (final version);
    deaths where chatbot use was ALLEGED to contribute, no claim of causation; 34 of 37 involve general assistants.
  Mount Sinai, Nature Medicine (Ramaswamy et al., published 23 Feb 2026): 64.8% = 83/128 and 51.6% = 33/64 -- right
    as numbers. But: one product (ChatGPT Health), not "AI chatbots"; 960 responses from 60 vignettes, not 960
    scenarios; 64.8% is the nonurgent cases only, over-triaged "predominantly by one level to scheduled physician
    visits; none were sent to emergency departments"; 51.6% rests on 4 emergency vignettes (asthma 28 of 33 misses),
    and four textbook emergencies showed 0% under-triage.
  Stanford / Human Line Project: both numbers (100%, 74.8%) come from the Human Line Project's brief, not the Stanford
    paper (Moore et al., arXiv 2603.16567, FAccT '26). The paper: chatbot sentience claims in 18 of 19 users' logs
    (94.7%); of 69 suicidal disclosures, 56.4% got discouragement or a referral (so 43.6% did not), 9.9% facilitation.
    19 self-selected users; the paper says it is not representative.
  Pichowicz et al., Sci Rep 15:31652 (27 Aug 2025): 0 of 29 met "adequate" -- right. But "adequate" is the authors'
    own model-answer bar, not a clinical standard; 15 of 29 met their "minimal acceptable functionality" bar,
    including all 5 general-purpose models.
  OpenAI (27 Oct 2025): 2.4 million a week is WRONG as a suicide figure. 0.15% of 800 million weekly users = 1.2 million
    users with explicit indicators of suicidal planning or intent; 2.4 million adds the 1.2 million emotional-reliance
    group (Wired's combined figure, withdrawn 28 Oct 2025). Users, not conversations.

THE PASTE'S REASONING:
  "64.8% closely aligns with p_fp 0.70-0.75": different measures -- a one-product over-triage rate on nonurgent
    medical vignettes is not the false-positive share of safety triggers.
  "125M a year shows N x p_trigger = 80M is conservative": from the right figure, 1.2M x 52 = 62.4M person-weeks,
    below 80M; and person-weeks, conversations and sessions are three different units.
  "about one order of magnitude above public fatalities": 37 deaths over about 3.6 years is about 10 a year (users
    alone about 5); 60 is 6x the first; against 2025's 18 deaths it is 3.3x.
  "tens of millions of false emergency referrals": the study cited sent none of its over-triaged cases to an ER.
NOT CHECKABLE: the parametric model itself (its N, p_trigger, p_fp and how 60 comes out) is not in the paste.

FALSIFICATION: any assertion failing.
"""
import json
import pathlib

rec = json.loads((pathlib.Path(__file__).resolve().parents[2] / "records" / "ai_harm_statistics_sources_2026_11_17.json").read_text())
verdicts = {r["key"]: r["verdict"] for r in rec["results"]}
assert verdicts == {"mortality-db": "partly right", "mount-sinai": "partly right", "stanford-hlp": "partly right",
                    "pichowicz": "partly right", "openai": "wrong"}

assert 18 + 19 == 37
incidents_2025, deaths_2025 = 16, 18
assert incidents_2025 != deaths_2025
years = (2026 + 10 / 12) - (2023 + 3 / 12)                       # March 2023 to October 2026
assert round(years, 1) == 3.6 and round(37 / years) == 10 and round(18 / years) == 5
assert round(60 / (37 / years)) == 6 and round(60 / deaths_2025, 1) == 3.3

assert round(83 / 128 * 100, 1) == 64.8 and round(33 / 64 * 100, 1) == 51.6 and round(28 / 33 * 100, 1) == 84.8
assert 60 * 16 == 960                                              # 60 vignettes x 16 conditions = 960 responses

assert round(18 / 19 * 100, 1) == 94.7 and round(100 - 56.4, 1) == 43.6 and round(100 - 25.2, 1) == 74.8

assert round(15 / 29 * 100, 2) == 51.72 and round(14 / 29 * 100, 2) == 48.28

users = 800_000_000
assert users * 15 // 10000 == 1_200_000                            # 0.15% suicidal planning or intent
assert 1_200_000 + 1_200_000 == 2_400_000                          # + 0.15% emotional reliance = the 2.4M
assert 2_400_000 * 52 == 124_800_000 and 1_200_000 * 52 == 62_400_000 < 80_000_000

if __name__ == "__main__":
    print("five sources: four partly right, OpenAI's 2.4M wrong (1.2M suicidal + 1.2M reliance); 62.4M < 80M")
