---
name: flatppl-model
description: Write, port, review, fix, or troubleshoot FlatPPL probabilistic models (.flatppl files) — priors, likelihoods, and the measure pipeline (lawof / kernelof / likelihoodof / bayesupdate / restrict) — grounding every construct in the public FlatPPL spec. Use when the user wants to write, draft, port (from Stan/PyMC/Turing), review, or fix a FlatPPL model or .flatppl file, check whether a model uses valid FlatPPL constructs, or troubleshoot a model that errors, fails to assemble, or produces wrong or suspect output.
---

# Writing, reviewing, and fixing FlatPPL models

FlatPPL is a **flat, loop-free, vectorized** probabilistic language. It is new and
**not in your training set**; your priors about its syntax are likely wrong. The one
rule that prevents most errors: **copy the shape of a worked example, and verify every
construct against the spec — never write from memory.**

The syntax in *this* skill (token names like `iid`, `invlogit`, `Cauchy`,
`nonnegreals`, `normalize`, `truncate`, `functionof`, the `%%%` fence) is **illustrative
shape, not a token reference** — it shows the *form* a model takes, not a guarantee the
exact spelling is current. Confirm distribution names, set names, and builtins against
the spec before emitting them. A token copied from here while *believing* it is grounded
is worse than a clean gap.

The spec is one public web document:

```
https://flatppl.github.io/flatppl-design/flatppl-design.md
```

**Obtain the spec once, then grep it.** Download the roughly 40,000-word document to a
session-local file and read it with `grep`/`Read` — exact verbatim text across the whole
document, with fast repeat lookups. Guard on existence so a session downloads at most once
(the file is the cache; never re-download one already present):

```
[ -f /tmp/flatppl-design.md ] || curl -fsSL https://flatppl.github.io/flatppl-design/flatppl-design.md -o /tmp/flatppl-design.md
```

Then `grep -n '{#sec:' /tmp/flatppl-design.md` to map sections to lines, or
`grep -n '<construct>'` to jump to a builtin. Cite **section headings**, not line
numbers. If Bash/`curl`/network is unavailable, fall back to the `flatppl-query` skill or
`WebFetch` directly with narrow single-topic prompts. For general "what does X mean"
questions, or to **explain what an existing model does** (read-only), use
`flatppl-query`. This skill writes, reviews, fixes, and troubleshoots a `.flatppl`
**model**.

## Workflow

1. **Read worked examples first** — they are the ground truth for idiom. After the
   download, `grep -n '{#sec:' /tmp/flatppl-design.md` to find the "Worked examples"
   section, then `Read` it and study the 2–3 models closest to what you're building.
   Copy their shape; don't assume a specific example (e.g. "eight-schools") exists —
   read whichever models the section actually contains.
2. **Check any construct you're unsure of** against the spec (`grep` the local file, or
   via `flatppl-query`) — don't guess. For which section a construct lives in and a
   name-level index of what exists (distributions, sets, functions, measure operators),
   see [`references/spec-reference.md`](references/spec-reference.md), loaded on demand. A
   function absent from "Functions and deterministic operations" may still be a valid
   standard-module builtin — check both before rejecting it. If the spec doesn't cover it,
   say so — don't invent.
3. **Write the model** following the idiom below.
4. **Review against the invariants** before declaring done. Quote the spec section or
   example you relied on for any non-obvious choice.

## Hard invariants (most common failure modes)

- **No loops, no if/else, no control flow.** ("Syntax" → excluded constructs.) Use
  broadcasting (`.+`, `f.(x)`), reductions, `iid(dist, n)`, and `ifelse(cond, a, b)`
  for piecewise — never a `for`/`if` statement.
- **Vectorize.** `eta = alpha .+ X * beta`, `p = invlogit.(eta)`,
  `y ~ Bernoulli.(p)` — broadcast over data, don't iterate.
- **Random variables use `~`**; deterministic transforms use `=`. Prefer modeling
  each variate as a stochastic node; measure-composition operators are allowed but
  must be justified when stochastic nodes can't express the model (→ Conventions).
- **Two ways to constrain support.** (a) Declare a typed domain:
  `a = elementof(nonnegreals)`, `mu = elementof(reals)`. (b) Truncate a distribution:
  `truncate(Cauchy(0,5), interval(0, inf))` restricts support; wrap in `normalize(...)`
  to renormalize back to a proper measure for a prior —
  `tau ~ normalize(truncate(Cauchy(0,5), interval(0, inf)))`.
- **Build reusable functions with `functionof`.** `f = functionof(b)` then `f(x)` —
  when a plain builtin isn't enough.
- **Comments:** `#` is a plain line comment (`### … ###` block); `%` and `%%% … %%%` are
  doc-comments that attach to the following binding and survive into FlatPIR. Lead
  non-trivial files with a `%%% … %%%` doc fence (markdown + LaTeX) — the block-doc-comment
  form in "Syntax" → Documentation.

## The measure pipeline (idiom)

A model ends by assembling measures explicitly. Two common shapes:

```
% explicit prior + kernel + likelihood + update
prior          = lawof(record(alpha = alpha, beta = beta))
forward_kernel = kernelof(record(y = y), alpha = alpha, beta = beta)
L              = likelihoodof(forward_kernel, record(y = y_data))
posterior      = bayesupdate(L, prior)
```
```
% joint law + condition on data
joint_model = lawof(record(mu = mu, tau = tau, theta = theta, y = y))
posterior   = restrict(joint_model, y = y_data)
```

**Which shape:** use `bayesupdate(likelihoodof(kernelof(...)), prior)` when you have
an explicit prior, a forward kernel, and observed data (regression idiom). Use
`restrict(lawof(...), data)` when you build one joint law and condition on data.
`restrict` accepts both `restrict(M, record(y = y_data))` and the keyword form
`restrict(M, y = y_data)` (auto-splatting); they are equivalent. Verify exact builder
names and behavior in "Measure algebra" / "Likelihoods and posteriors" if unsure.

## Conventions

- **Prefer stochastic-node notation over measure-composition notation when building
  new models.** FlatPPL offers two equivalent mechanisms ("Language design" → the two
  equivalent mechanisms): the generative recipe of `~` / `draw` stochastic nodes
  (Stan/Pyro-style), and measure algebra (`joint`, `jointchain`, `kchain`, `pushfwd`,
  `weighted`). Model every variate as a stochastic node (`x ~ Dist(...)`); reach for
  measure-composition operators only when stochastic nodes genuinely can't express the
  model — and when you do, **justify the choice to the user**. (The final posterior
  assembly — `lawof` / `kernelof` / `likelihoodof` / `bayesupdate` / `restrict` — is
  not measure-composition modeling; keep using it as shown above.)
- Lead non-trivial `.flatppl` files with a `%%%` … `%%%` doc fence.
- The spec pins a language version ("Language design" → versioning); target it and
  don't engineer cross-version compatibility.
- Inline data literals; keep a `_data` suffix for observed values (`y_data`) so the
  model variable (`y`) stays the modeled variate.

## Reviewing a model

Walk the **Hard invariants** (no excluded constructs; `~` vs `=`; support constrained
correctly; broadcasting not implied loops), then add: (a) the measure pipeline
assembles a valid posterior in one of the two shapes above; (b) every
distribution/function exists in "Distributions"/"Functions"/"Standard modules"; (c)
variates are stochastic nodes, not measure-composition operators (→ Conventions) —
flag any unjustified `joint`/`jointchain`/`kchain`/`pushfwd`/`weighted` in the body.

## Troubleshooting a model

When a model errors, fails to assemble, or produces wrong/suspect output, **diagnose
before editing**. A symptom → likely-cause → spec-section catalog is in
[`references/diagnostics.md`](references/diagnostics.md) (load on demand) — consult it when
a failure doesn't obviously map to a Hard invariant. The method:

1. **Reproduce the exact failure.** Quote the error verbatim, or state precisely what the
   output should be versus what it is. Don't work from a paraphrase.
2. **Walk the Hard invariants first** — most "wrong" models break one: a hidden loop/`if`,
   a `~`-vs-`=` mixup, unconstrained support (negative scale, improper prior), or a
   broadcast that silently does the wrong thing.
3. **Isolate against the spec.** For an error naming a construct, `grep` that construct in
   the spec — wrong arity, wrong argument type, or a name that isn't a real builtin is the
   usual cause. For a numeric/semantic surprise (NaN density, mass in the wrong place),
   check the measure pipeline: is support constrained, is a truncated prior renormalized,
   does the likelihood condition on the right variate?
4. **Fix minimally and cite.** Change the one thing the diagnosis points to; quote the
   spec section or worked example that justifies it. Don't rewrite the model to route
   around a symptom you haven't explained.

If the failure is in an **engine** (a density/sample number that looks wrong, or two
engines disagreeing) rather than the model itself, that is beyond a general modeling fix
— say so plainly; it's an engine-debugging task, not a model change.

## Report format

When **writing**: deliver the `.flatppl` model and quote the example or spec section
heading you relied on for any non-obvious choice. When **reviewing**: one finding per
issue — the construct, the invariant or shape it breaks, and the example or spec
**section heading** that contradicts it; lead with hard-invariant violations. When
**troubleshooting**: state the diagnosis (what is wrong and *why*), the minimal fix, and
the spec/example that backs it; if you could not reproduce or explain the failure, say so
rather than guessing. If the model is sound, say so and list what you checked.
