---
name: axiom-reduce
description: Find the smallest set of axioms that forces a result, and use it to improve the result -- merge duplicate axioms, settle open conventions, and state each result's exact dependencies. Use after a result is verified and before connecting it to other theorems ("first check what axioms can improve it"). Worked example: grid81_operators_applied.py -- seven results reduce to A1 (10 = 1 mod 9), A2 (3 | 9), A3 (primes > 3 are coprime to 3); A1 merged the "sum collapse" and "mod-9 collapse" axioms and the grid's 1..9 column index fixed the mod-9 representative convention.
---

# axiom-reduce

1. **List every result** in the file, numbered.
2. **For each, name the facts it uses.** Write them as short axioms
   (congruences, divisibility, definitions). Prefer facts about the numbers
   over facts about notation.
3. **Minimise.** Drop any axiom implied by the others. Merge axioms that
   say the same thing in two notations (sum collapse = n mod 9, since
   10 = 1 mod 9).
4. **Dependency table:** result -> axioms used. Record it in the file's
   docstring ("Results 1 and 7 need A1 only; ...").
5. **Settle open conventions from the numbers.** If an axiom forces a
   convention (the grid's columns run 1..9, so residue 0 is 9), record that
   the convention is settled and by what.
6. **Domain.** State where each axiom holds (A1: n >= 1). Then run
   `try-to-disprove` on the domain edges.
7. **Assert each axiom** in the file, on a range, so the file re-checks it.

Never invent an axiom the owner did not state or the numbers do not force.
If an axiom from the owner's list cannot be made precise, say what is
missing (an operand, an order, a cost function) instead of guessing.
