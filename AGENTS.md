# FlatPPL — agent guide

This project uses **FlatPPL**, a flat, loop-free, vectorized probabilistic language.
FlatPPL is new and not yet in your training set — **do not answer from
memory.** Ground every claim and every construct in the public spec.

**Spec (single web document):**
`https://flatppl.github.io/flatppl-design/flatppl-design.md`

It is ~40k words. Best: download it once
(`curl -fsSL <that url> -o /tmp/flatppl-design.md`) and `grep`/read it — exact text,
whole doc, no truncation. No shell? Fall back to targeted single-topic web fetches.
Quote the relevant section heading and `{#sec:...}` anchor when you cite it.

## Two tasks, two guides

- **Answer a question about the language** (syntax, measure algebra, distributions,
  functions, likelihoods/posteriors, FlatPIR, profiles), **or explain what an existing
  model does** (read-only) →
  see [`.claude/skills/flatppl-query/SKILL.md`](.claude/skills/flatppl-query/SKILL.md).
- **Write, port, review, fix, or troubleshoot a `.flatppl` model** →
  see [`.claude/skills/flatppl-model/SKILL.md`](.claude/skills/flatppl-model/SKILL.md).

Both files are written for agents: dense reference, navigation method, and the hard
invariants that prevent the most common FlatPPL mistakes. Read the relevant one in
full before working.

## Core rules

The deeper `SKILL.md` files have the full reference; if your tool can't open them, this
section is enough to work safely.

- **The one rule:** copy the shape of a worked example from the spec's "Worked examples"
  section, and verify every construct against the spec before using it. Never invent
  syntax — token names below are illustrative shape, not a guarantee of current spelling.
- **No loops, no `if`/`else`, no control flow.** Vectorize: broadcasting (`.+`, `f.(x)`),
  reductions, `iid(dist, n)`, `ifelse(cond, a, b)` for piecewise.
- `~` for random variables, `=` for deterministic transforms. `%` for line comments.
- **Constrain support** with `elementof(...)` (typed domain) or `truncate(...)`; wrap in
  `normalize(...)` for a proper prior.
- **Assemble posteriors** with the measure pipeline: `lawof` / `kernelof` /
  `likelihoodof` / `bayesupdate` (explicit prior + kernel + data), or
  `restrict(lawof(...), data)` (one joint law conditioned on data).
- Prefer stochastic nodes (`x ~ Dist(...)`) over measure-composition operators
  (`joint`, `kchain`, `pushfwd`, …); justify the latter if you must use them.
