# CLASS: AUDIT
"""
The pasted cost model (2026-10-27), text from another tool relayed by the owner, after the owner's point that companies
make their failures the user's job to sort out. The paste:

    company, testing in house:   Pi = R - C_testing - C_remediation
    company, users as testers:   Pi = R - a C_testing - b C_remediation,   0 <= a, b << 1
    users absorb:                C_users = C_failure + C_diagnosis + C_recovery + C_harm
    early deployment -> more user exposure -> more free failure data -> lower company testing cost
    "mathematically unsound", "perpetually unstable"; NIST citations [1] [2] [3].

RIGHT:
  the company's saving is S = (1 - a) C_testing + (1 - b) C_remediation, never negative for 0 <= a, b <= 1, and zero
    only when a = b = 1 -- so the incentive the paste names is right, and it needs only a, b < 1, not a, b << 1
  the cost does not go away: what the company stops paying, users pay (C_users), with no term giving it back
  NIST, checked 2026-10-27:
    [1] AI RMF page: "to incorporate trustworthiness considerations into the design, development, use, and evaluation
        of AI products, services, and systems" -- right (that page does not mention monitoring; [2] does)
    [2] "New Report: Challenges to the Monitoring of Deployed AI Systems" (March 9, 2026): AI systems "introduce
        variability and manifest in unpredictable ways"; "post-deployment monitoring ... is a crucial practice" -- right
    [3] Playbook, MANAGE 1.1: "A determination is made as to whether the AI system achieves its intended purpose and
        stated objectives and whether its development or deployment should proceed"; its About: "formally weigh an AI
        system's negative risks against its benefits" -- right
  "monitoring is not a substitute for predeployment testing" is the paste's own line; NIST's report does not compare
    the two.

WHAT THE MODEL DOES NOT SHOW:
  "unstable": the model has no time and no feedback rule, so nothing in it can be stable or unstable. What it shows is
    a cost moved from the company to users (an externality) -- "unsound" and "unstable" are not results of it.

THE MISSING TERM, AND THE EXACT CONDITION: some of the users' cost comes back to the company -- users leave,
  courts award damages, regulators fine. Call that share L (0 <= L <= 1). Then

    Pi(users test) - Pi(in house) = S - L C_users

  and shipping early pays the company exactly when  S > L C_users.  The paste's picture is the case L = 0 (no
  recourse). Its closing "sound allocation" -- the company bears foreseeable failure cost, users keep recourse -- is
  the same as making L large enough that S - L C_users < 0.

FALSIFICATION: any assertion failing.
"""
from fractions import Fraction as F
from itertools import product


def saving(a, b, ct, cr):
    return (1 - a) * ct + (1 - b) * cr


def gain_from_early(a, b, ct, cr, users, L):
    return saving(a, b, ct, cr) - L * users


grid = [F(k, 10) for k in range(11)]
for a, b in product(grid, grid):
    s = saving(a, b, F(40), F(25))
    assert s >= 0
    assert (s == 0) == (a == 1 and b == 1)

# a, b need only be below 1 for the saving to be positive -- "<< 1" is not needed
assert saving(F(9, 10), F(9, 10), 40, 25) > 0

# the users' cost is the sum of its four parts, each at least 0
parts = dict(failure=F(10), diagnosis=F(8), recovery=F(12), harm=F(30))
users = sum(parts.values())
assert users == 60 and all(v >= 0 for v in parts.values())

# with no recourse (L = 0) shipping early always pays when a, b < 1
assert gain_from_early(F(1, 10), F(1, 5), 40, 25, users, 0) == F(56)
# with recourse the sign can turn: 56 - L * 60 < 0 exactly when L > 56/60
assert gain_from_early(F(1, 10), F(1, 5), 40, 25, users, F(14, 15)) == 0
assert gain_from_early(F(1, 10), F(1, 5), 40, 25, users, 1) < 0
assert gain_from_early(F(1, 10), F(1, 5), 40, 25, users, F(1, 2)) > 0

if __name__ == "__main__":
    print("saving (1-a)Ct + (1-b)Cr >= 0, zero only at a = b = 1: right; NIST [1] [2] [3]: right as cited")
    print("missing term: shipping early pays exactly when (1-a)Ct + (1-b)Cr > L x C_users (L = share that comes back)")
