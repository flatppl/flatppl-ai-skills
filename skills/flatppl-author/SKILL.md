---
name: flatppl-author
description: Write or review FlatPPL probabilistic models (.flatppl files) — priors, likelihoods, and the measure pipeline (lawof / kernelof / likelihoodof / bayesupdate / restrict). Use when the user wants to write, draft, port, fix, or review a FlatPPL model or .flatppl file, translate a Stan/PyMC/Turing model into FlatPPL, or check whether a model uses valid FlatPPL constructs.
---

# Authoring FlatPPL models

FlatPPL is a **flat, loop-free, vectorized** probabilistic language. It is niche;
your priors about its syntax are likely wrong. The one rule that prevents most
errors: **copy the shape of an existing model, and verify every construct against
the docs — never write from memory.**

Filenames, examples, and line numbers drift. Any specific file or `doc:line`
reference (in this skill or elsewhere) is a hint, not a fact — confirm it exists
(`ls`, `Grep`) before relying on it, and prefer heading citations over line numbers.

This skill writes/reviews a `.flatppl` **model**. It does NOT answer general language
questions (use `flatppl-docs`), review the normative spec docs (use
`flatppl-doc-review`), review a downstream plan/ADR (use `flatppl-spec-review`),
diagnose a wrong/crashing engine result (use `flatppl-engine-debug`), or audit an
engine/corpus against the spec (use `flatppl-conformance-audit`).

## Workflow

1. **Read 2–3 nearby examples first.** They are the ground truth for idiom.
   Discover the corpus live (filenames drift) — don't trust a remembered roster. Paths
   are relative to the repo root; if an `ls` comes back empty (you're in a subdir or
   worktree), resolve the root first — don't proceed from memory on an empty listing:
   - `ls flatppl-examples/examples/*.flatppl` — the curated set. The
     `bayesian_inference_*` series is the canonical prior+kernel vs. joint+`restrict`
     comparison (read the whole series before choosing a measure pipeline); pick 2–3
     others by name closest to the model you're writing.
   - `ls flatppl-dev/*.flatppl` for any dev models with code, and `ls flatppl-dev/*.md`
     for design writeups. Writeups carry modeling *intent*; only the `.flatppl` files
     are ground truth for syntax. Some writeups have no companion `.flatppl` — read
     those for intent, not idiom.
   - `Grep` the corpus for a distribution/function you intend to use to see real
     usage before writing it.
2. **Check any construct you're unsure of via the docs**, don't guess. Run the
   `flatppl-docs` skill against `flatppl-design/docs/`:
   syntax → `05-syntax.md`, functions → `07-functions.md`, distributions →
   `08-distributions.md`, measure ops → `06-measure-algebra.md`, standard-library
   builtins → `09-standard-modules.md`, worked models → `10-examples.md`. A function
   not in `07` may still be a valid builtin in `09` — check both before rejecting it.
   If the docs don't cover it, say so — don't invent.
3. **Write the model** following the idiom below.
4. **Review against the invariants** (next section) before declaring done. Quote
   the doc/example you relied on for any non-obvious choice.

## Hard invariants (most common failure modes)

- **No loops, no if/else, no control flow.** See `05-syntax.md` → "Excluded
  constructs". Use broadcasting (`.+`, `f.(x)`), reductions, `iid(dist, n)`, and
  `ifelse(cond, a, b)` for piecewise — never a `for`/`if` statement.
- **Vectorize.** `eta = alpha .+ X * beta`, `p = invlogit.(eta)`,
  `y ~ Bernoulli.(p)` — broadcast over data, don't iterate.
- **Random variables use `~`**; deterministic transforms use `=`. Strongly prefer
  modeling each variate as a stochastic node; measure-composition operators are
  allowed but must be justified when stochastic nodes can't express the model
  (→ Conventions).
- **Two ways to constrain support.** (a) Declare a typed domain:
  `a = elementof(nonnegreals)`, `mu = elementof(reals)` — see `minimal.flatppl`.
  (b) Truncate a distribution: `truncate(Cauchy(0,5), interval(0, inf))` restricts
  support; wrap in `normalize(...)` to renormalize back to a proper measure for a
  prior — `tau ~ normalize(truncate(Cauchy(0,5), interval(0, inf)))` (eight-schools).
- **Build reusable functions with `functionof`.** `f_sqrt = functionof(b)` then
  `f_sqrt(x)` (see `minimal.flatppl`) — when a plain builtin like `sqrt(x)` isn't
  enough.
- **Comments:** `%` for a line comment; lead non-trivial files with a `%%% … %%%`
  doc fence (below).

## The measure pipeline (idiom)

A model ends by assembling measures explicitly. Two common shapes seen in the corpus:

```
# explicit prior + kernel + likelihood + update
prior          = lawof(record(alpha = alpha, beta = beta))
forward_kernel = kernelof(record(y = y), alpha = alpha, beta = beta)
L              = likelihoodof(forward_kernel, record(y = y_data))
posterior      = bayesupdate(L, prior)
```
```
# joint law + condition on data
joint_model = lawof(record(mu = mu, tau = tau, theta = theta, y = y))
posterior   = restrict(joint_model, y = y_data)
```

**Which shape:** use `bayesupdate(likelihoodof(kernelof(...)), prior)` when you have
an explicit prior, a forward kernel, and observed data (regression idiom —
`linear-regression`, `eight-schools`, `bayesian_inference_1`). Use
`restrict(lawof(...), data)` when you build one joint law and condition on data
(`bayesian_inference_4`); a close variant builds the joint law then `disintegrate`s it
(`bayesian_inference_3`). Verify which an example uses by reading it — don't trust this
roster. `restrict` accepts both `restrict(M, record(y = y_data))`
and the keyword form `restrict(M, y = y_data)` (auto-splatting); they are equivalent —
see `06-measure-algebra.md` → "Measure restriction". Verify exact builder names there
if unsure.

## Conventions

- **Prefer stochastic-node notation over measure-composition notation when building
  new models.** FlatPPL offers two equivalent mechanisms (`04-design.md` → "two
  equivalent mechanisms"): the
  generative recipe of `~` / `draw` stochastic nodes (Stan/Pyro-style), and measure
  algebra (`joint`, `jointchain`, `kchain`, `pushfwd`, `weighted`). Model every
  variate as a stochastic node (`x ~ Dist(...)`); reach for measure-composition
  operators only when stochastic nodes genuinely can't express the model — and when
  you do, **justify the choice to the user**. (The final posterior assembly —
  `lawof` / `kernelof` / `likelihoodof` / `bayesupdate` / `restrict` — is not
  measure-composition modeling; keep using it as shown above.)
- Lead non-trivial `.flatppl` files with a `%%%` … `%%%` doc fence (markdown + LaTeX) —
  the block-doc-comment form defined in `05-syntax.md` → "Documentation". A companion
  `*.md` writeup (scenario / setup / math) is the `flatppl-dev` convention for
  non-trivial models.
- Read `flatppl-dev/CONVENTIONS.md` for ecosystem invariants (version pinned at
  `0.1`; don't engineer cross-version compat). For cross-repo work follow
  `flatppl-dev/AGENTS.md` read-first protocol.
- Inline data literals; keep `_data` suffix for observed values (`y_data`) so the
  model variable (`y`) stays the modeled variate.

## Reviewing a model

Walk the **Hard invariants** above (no excluded constructs; `~` vs `=`; support
constrained correctly; broadcasting not implied loops), then add: (a) the measure
pipeline assembles a valid posterior in one of the two shapes above; (b) every
distribution/function exists in `08`/`07`/`09`. (c) variates are stochastic nodes, not
measure-composition operators (→ Conventions) — flag any unjustified
`joint`/`jointchain`/`kchain`/`pushfwd`/`weighted` in the model body.

## Report format

When **writing**: deliver the `.flatppl` model and quote the example/doc heading you
relied on for any non-obvious choice. When **reviewing**: one finding per issue —
the construct, the invariant or shape it breaks, and the example or doc **section
heading** that contradicts it; lead with hard invariant violations. If the model is
sound, say so and list what you checked.
