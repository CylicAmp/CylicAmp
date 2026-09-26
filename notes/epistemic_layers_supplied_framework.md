# Supplied framework: L1/L2/L3 epistemic quarantine — audit

Audited 2026-09-26. Material arrived as two blocks: a category-theoretic
formalization of "pseudo-formal synthesis," and a Mersenne-scale argument
about representation. Run through `audit-chain`: reproduce, check prior
art, test mechanism, interpret last.

## Prior art — this is already in the corpus, under other names

Found by grepping the skill set before writing. Both files already contain
the framework's core, and neither is cited by the supplied material.

**`.claude/skills/claim-grade/SKILL.md`** already grades "correspondence
level 1/2/3" via the four cuts of T305, and reports the weakest cut as the
grade. Its description states the separation explicitly:

> Separate from forced-check (which grades scope) and miss-test (which
> grades falsifiability); those three axes are independent and this one
> must not be substituted for either.

**`CLAUDE.md` and `.claude/skills/audit-chain/SKILL.md`** already fix the
ordering the framework calls a "firewall":

> Find -> Check prior art -> Reproduce -> Test mechanism
>      -> Classify dynamics -> Test baseline -> Prove -> Interpret
>
> Interpretation is LAST.

The supplied L1 -> L2 -> L3 stratification, with morphisms flowing only
downward and an "L3 -> L1 leak" as the failure mode, is that ordering
restated. The "unsafe downcast" is interpretation-first.

**What the existing version does better.** `claim-grade` keeps scope,
falsifiability and correspondence-strength as THREE INDEPENDENT AXES and
forbids substituting one for another. The supplied framework collapses
them into a single ladder, so a claim strong on falsifiability and weak on
scope has no way to register that inside it.

**What stands as the supplied material's own.** The Krylov-subspace
statement of reachability -- the reachable set from x_0 under a fixed
operator is confined to span{x_0, Tx_0, T^2 x_0, ...}, so a target outside
it is unreachable at any horizon. That is the same content as
`finite-dynamics`' transitive-closure test, in linear-algebra vocabulary,
and the vocabulary is a genuine addition for continuous state spaces where
the finite-dynamics machinery does not apply.

## Two claims that do not hold

**"For an abstraction functor F to be structurally conservative it must
admit an adjoint (F |- U)."** Not a theorem. Functors do not require
adjoints to be well defined or useful, and many legitimate forgetful
functors have no right adjoint. The observation underneath survives
without it: a projection that discards structure cannot be inverted, and
the fibers are where the discarded information went. Stating it as a
requirement on functors presents an observation as a typing law.

**"The fibers pi^-1(x) are effectively infinite / unbounded fiber
bundles."** False for a finite carrier, where each fiber has size
|V| / |image| -- a computable number. The argument is stronger as a fiber
count than as an appeal to infinity, because a count can be exhibited.

## The Mersenne block verifies completely

Independently checked, nothing wrong in it:

| claim | check |
|---|---|
| 24,862,048 decimal digits | correct |
| leading digits `148894445742041325547806458472397916603026...` | agrees to 42 places, divergence beyond that is our precision limit |
| ~8.28 million commas | 8,287,349 |
| binary is 82,589,933 continuous ones | correct |
| `(1 << p) - 1` generates it | correct |
| ord_9(2) = 6, p = 5 (mod 6), "the 5th step of the 6-step loop" | correct; M_p = 4 (mod 9) |
| Lucas-Lehmer reduction by bitwise folding | correct, since 2^p = 1 (mod M_p) |

Leading digits were computed from the fractional part of p*log10(2) at 80
digits of precision, not by expanding the number.

## Grade

Under `claim-grade`'s rule that the weakest cut is the grade: the framework
is a **restatement** of existing corpus method (correspondence level 1,
literal re-derivation) with two false supporting claims attached. The
Mersenne block is exact and independently verified. The Krylov framing is
the only part that adds vocabulary the corpus did not have.

Per `prior-art`: this is a filing matter, not misconduct. The right action
is to cite `claim-grade` and `audit-chain` from any write-up that uses the
three-layer language, and to say what is new beyond them.
