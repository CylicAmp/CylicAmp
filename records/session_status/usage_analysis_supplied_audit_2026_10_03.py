"""Audit of a supplied analysis (2026-10-03) of this session's usage record.

Record (get_session, 2026-10-03): cache_read 13,252,313,603; cache_write 264,411,657;
input 3,654,466; output 29,033,005; cost_usd 9,436.91989045; used_tokens 300,729;
worker_epoch 1119.

CORRECT
  U1 Total ingested 13,520,379,726; shares 98.02% / 1.96% / 0.03%.
WRONG
  U2 "~456 cached read tokens for every new INPUT token": 456 is cache reads per OUTPUT
     token. Per input token it is 3,626.
  U3 "Total billed $9,436.92": the record's field is a computed cost; what was billed is
     not in the record.
  U4 "~$15/MTok base input on Opus-class" -> "$198,000": the model serving this session,
     claude-opus-5.5, listed at $4 input / $20 output per MTok (OpenRouter, looked up
     2026-10-02, tools/cross_check.py). Uncached at $4: ~$53,000, not $198,000.
  U5 "Output accounted for the largest expense" / "70-80% of cost is output": at list
     prices with the standard cache multipliers (read 0.1x, 5-minute write 1.25x),
     cache reads ~$5,301 and output ~$581 -- reads are the largest cost, output ~8%.
     These list-price parts sum to ~$7,218, not the record's $9,437; the difference is
     not explained here (earlier turns ran on other models; long-context or 1-hour cache
     pricing may apply -- not checked).
NOT ESTABLISHED
  U6 "1,119 tool/agent handoffs (worker_epoch)": the field's meaning is not documented in
     the record; it is not a handoff count by any stated definition.
  U7 "~44,000 iterations against a ~300k prefix": 13.25B / 300,729, but context size varied
     (compactions) -- an order-of-magnitude figure at most.
  U8 "31+ artifact models stay live in memory": the artifact list is session metadata,
     not context contents.
"""
READ, WRITE, INP, OUT = 13_252_313_603, 264_411_657, 3_654_466, 29_033_005
TOTAL = READ + WRITE + INP
assert TOTAL == 13_520_379_726                                             # U1
assert round(100 * READ / TOTAL, 2) == 98.02 and round(100 * WRITE / TOTAL, 2) == 1.96
assert round(READ / OUT) == 456 and round(READ / INP) == 3626               # U2
P_IN, P_OUT = 4.0, 20.0                                                    # $/MTok, opus-5.5
uncached = READ / 1e6 * P_IN
assert 52_000 < uncached < 54_000 and READ / 1e6 * 15 > 198_000             # U4
parts = {"read": READ / 1e6 * P_IN * 0.1, "write": WRITE / 1e6 * P_IN * 1.25,
         "input": INP / 1e6 * P_IN, "output": OUT / 1e6 * P_OUT}
assert max(parts, key=parts.get) == "read"                                 # U5
assert parts["output"] / sum(parts.values()) < 0.1
assert 7_100 < sum(parts.values()) < 7_300

if __name__ == "__main__":
    for k, v in parts.items():
        print(f"{k:7s} ${v:,.0f}")
    print(f"sum    ${sum(parts.values()):,.0f}   (record: $9,437)   uncached reads at $4: ${uncached:,.0f}")
