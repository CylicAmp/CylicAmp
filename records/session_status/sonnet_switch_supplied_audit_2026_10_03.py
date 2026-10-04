"""Audit of a supplied claim (2026-10-03): switching this session from claude-opus-5-5 to
claude-sonnet-4-6 would cut cost 75-80%, from $9,436.92 to ~$2,000-2,300.

Prices per MTok, OpenRouter /api/v1/models, fetched 2026-10-03:
                       input  output  cache read  cache write
  claude-opus-5.5        4.00   20.00     0.20        5.00
  claude-sonnet-4.6      3.00   15.00     0.30        3.75
  claude-opus-4.1       15.00   75.00     1.50       18.75   <- the supplied "Opus" column

VERDICT
  S1 The supplied Opus prices are Opus 4.1's, not the model serving this session.
  S2 The supplied table contradicts its own conclusion: its Sonnet column sums to $5,413.69,
     not $2,000-2,300; its Opus column sums to $27,068, not $9,437. The $1,880-2,350 is
     $9,437 / 5, not anything the table computes.
  S3 At current prices for the actual models, on this session's volumes:
        opus-5.5   $4,568      sonnet-4.6  $5,414
     Sonnet would cost ~19% MORE, because its cache-read price ($0.30) is higher than
     opus-5.5's ($0.20) and cache reads are 98% of the volume.
  S4 The session was created on sonnet-4-6 and switched to opus-5-5 (user_switched_model).
  S5 "1,119 worker epochs" as a measure of work is unsupported (field undefined in the record).
  S6 "Sonnet is faster" and "needs more corrective turns on theorem work": not checked.
CORRECTION to usage_analysis_supplied_audit_2026_10_03.py: it assumed a 0.1x cache-read
  price ($0.40); the listed price is $0.20. Reads cost ~$2,650, not ~$5,301; the
  list-price total is ~$4,568, not ~$7,218. Its conclusions (reads are the largest cost,
  output < 15%) still hold.
"""
VOL = {"input": 3_654_466, "output": 29_033_005, "read": 13_252_313_603, "write": 264_411_657}
PRICES = {
    "opus-5.5":   {"input": 4.00, "output": 20.00, "read": 0.20, "write": 5.00},
    "sonnet-4.6": {"input": 3.00, "output": 15.00, "read": 0.30, "write": 3.75},
    "opus-4.1":   {"input": 15.0, "output": 75.0,  "read": 1.50, "write": 18.75},
}
cost = {m: sum(VOL[k] / 1e6 * p[k] for k in VOL) for m, p in PRICES.items()}

assert abs(cost["sonnet-4.6"] - 5413.69) < 0.5                         # S2
assert abs(cost["opus-4.1"] - 27068) < 2
assert not (1880 <= cost["sonnet-4.6"] <= 2350)
assert abs(cost["opus-5.5"] - 4568) < 2 and cost["sonnet-4.6"] > cost["opus-5.5"]   # S3
assert 0.18 < cost["sonnet-4.6"] / cost["opus-5.5"] - 1 < 0.2
op = PRICES["opus-5.5"]
assert VOL["read"] / 1e6 * op["read"] > VOL["output"] / 1e6 * op["output"]          # reads > output
assert VOL["output"] / 1e6 * op["output"] / cost["opus-5.5"] < 0.15

if __name__ == "__main__":
    for m, c in cost.items():
        print(f"{m:11s} ${c:,.2f}")
