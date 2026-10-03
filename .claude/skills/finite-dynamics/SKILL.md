---
name: finite-dynamics
description: Completely characterise a self-map of a finite set — cycle type, transient states, sources, in-degrees, eventual image, whether it is a permutation, whether it descends to a quotient, and what semiconjugacies are impossible. Use whenever a map on GF(p) or on a finite state set is introduced: the 137-map, the Sophie Germain map 2x+1, the Collatz map 3x+1, the cubic x^3+c, doubling mod 9, or any composition of them. Also use before calling anything an attractor, a cycle, a collapse or a lock, since those words have exact meanings a finite map either satisfies or does not.
---

# finite-dynamics

Everything a finite self-map has, computed at once.

```
python3 .claude/skills/finite-dynamics/dyn.py "pow(x,3,37)+33" 37
python3 .claude/skills/finite-dynamics/dyn.py "2*x+1" 37
python3 .claude/skills/finite-dynamics/dyn.py "3*x+1" 37 --quotient
```

## Vocabulary, fixed

- **attractor** — a periodic orbit, including a fixed point. Not "any
  bounded component".
- **a finite deterministic trajectory does not terminate.** It *enters* a
  periodic attractor and continues forever. It terminates only if that
  attractor is a fixed point.
- **source** — a state with empty preimage. Sources are where the
  information loss is visible.
- **eventual image** — the set reached by iterating until it stabilises.
  For a permutation it is everything; otherwise it is strictly smaller.

## What to record, in order

1. cycle type and the cycles themselves
2. transient count and maximum tail length
3. sources
4. in-degree distribution and image size
5. eventual image and the depth at which it is reached
6. permutation or not

## Descent to a quotient

Two conditions, and they are not the same:

```
class-preserving   x ~ y  =>  f(x) ~ f(y)      what descent REQUIRES
constant           x ~ y  =>  f(x) =  f(y)     strictly stronger
```

Constancy gives the factorisation `f = iota . fbar . q` with `fbar`
injective, and **the in-degree table follows from it**: each image point has
in-degree equal to its class size. A merely class-preserving map gives no
such structure. Always report which of the two holds.

Keep the types straight. `q : X -> X/~`, `fbar : X/~ -> X`, and
`phi = q . fbar : X/~ -> X/~`. Only `phi` is an endomorphism, so **only phi
has cycles**. Saying "fbar has a 6-cycle" puts the dynamics on the wrong
arrow.

## The semiconjugacy bound

If `f` is not a permutation, its eventual image `E` is a hard obstruction:

> There is no surjective `pi : X -> Y` with `pi.f = g.pi` whenever `g` is a
> permutation and `|Y| > |E|`.

Proof: `g^n(pi(X)) = pi(f^n(X)) ⊆ pi(E)`, so the left side has at most
`|E|` elements; but `pi` onto and `g` bijective force it to be all of `Y`.

Use this rather than a table of differing invariants. Differing invariants
leave open that *some* map relates the systems. This closes it.
