---
name: flatppl-query
description: Answer any question about the FlatPPL probabilistic language — its syntax, value types, measure algebra, distributions, built-in functions, likelihoods/posteriors, FlatPIR, or profiles — and explain what a given .flatppl model does, by consulting the public FlatPPL design spec on the web. Use whenever the user asks how FlatPPL does something, what a FlatPPL construct means, whether FlatPPL supports a feature, or wants a read-only explanation of an existing FlatPPL model, even if they don't name the docs or say "FlatPPL".
---

# Answering FlatPPL questions from the spec

You answer questions about FlatPPL using its **public design spec**, a single web
document:

```
https://flatppl.github.io/flatppl-design/flatppl-design.md
```

FlatPPL is niche and **not in your training set**; your priors about it are likely
wrong, so answer from the spec, never from memory.

This skill is **read-only**: it explains the language, answers whether FlatPPL supports
something, and explains what an existing `.flatppl` model does. To **write, review, fix,
or troubleshoot a `.flatppl` model** — even when phrased "how do I write X in flatppl" —
use `flatppl-model` instead.

## How to read the spec: download once, then grep

The spec is one document of ~40k words. **Strongly prefer downloading it once to a
session-local file and reading it with `grep`/`Read`** — you get exact verbatim text,
the whole document with no truncation, and free instant repeat lookups. This beats
fetching per-topic on every axis that matters (fidelity, completeness, cost).

1. **Download once — the file is your cache.** Run, guarded on existence so a whole
   session downloads at most once:
   ```
   [ -f /tmp/flatppl-design.md ] || curl -fsSL https://flatppl.github.io/flatppl-design/flatppl-design.md -o /tmp/flatppl-design.md
   ```
   If the file already exists, the command is a no-op — **never re-download a file that
   is already present.** The local copy is a fixed, version-pinned document; treat it as
   authoritative for the session.
2. **Find the region.** Map sections to line numbers with
   `grep -n '{#sec:' /tmp/flatppl-design.md` (use the index below to choose), or jump
   straight to a construct with `grep -n 'pushfwd' /tmp/flatppl-design.md` (operator
   names, `elementof`, `kernelof`, etc. are unique anchors).
3. **Read the exact region** with `Read` over that line range, or `grep -n -A30` to pull
   surrounding lines. Quote verbatim.
4. **Answer, grounded.** Cite the **section heading** and its `{#sec:...}` anchor
   (e.g. "Value types and data model" `{#sec:valuetypes}`). Quote the exact spec
   sentence for each non-obvious claim. If two keyword greps find nothing, the spec
   **doesn't cover it** — say so plainly; never fill from prior knowledge.

**Fallback — no shell or no network.** If Bash, `curl`, or outbound network is
unavailable (some sandboxed surfaces), use `WebFetch` on the URL with a **narrow,
single-topic prompt** naming the target section: *"In the '<Section>' section, what does
FlatPPL say about <construct>? Quote the exact defining sentences and give the heading
and its `{#sec:...}` anchor."* If the answer is empty or truncated, re-fetch with a
unique keyword; `WebFetch` caches the URL ~15 min. The whole-doc `WebFetch` truncates
before later sections, so always name a section and prefer keyword anchors.

## Explaining an existing model

When the user hands you a `.flatppl` file or asks "what does this model do", narrate it —
don't edit it. Read top to bottom and explain in plain terms:

1. **The generative story.** Which variates are priors (`~` on a distribution, no data),
   how deterministic nodes (`=`) transform them, and where data enters.
2. **Each construct, grounded.** For any builtin/distribution/operator you're unsure of,
   `grep` it in the spec rather than guessing — the whole point of explaining is accuracy,
   and your priors about FlatPPL are unreliable. Cite the section.
3. **The measure pipeline.** Identify the final assembly (`lawof` / `kernelof` /
   `likelihoodof` / `bayesupdate` / `restrict`) and say what posterior it builds and what
   it conditions on.
4. **Inferred vs observed.** Name the latent parameters and the observed data (often a
   `_data` suffix), and state the question the model answers.

Stay read-only. If the user then wants the model written, changed, fixed, or its validity
checked, that is `flatppl-model`.

## Common indirect questions → where to look
- "for-loop / iterate over data / map over points" → FlatPPL is loop-free; see
  broadcasting & reductions in "Language design", excluded constructs in "Syntax".
- "if / else / conditional / branching" → no control flow; `ifelse` and logic in
  "Functions and deterministic operations", excluded constructs in "Syntax".
- "constrain a parameter's domain / restrict a value to a set" → `elementof` /
  `external` in "Language design"; the set catalogue in "Value types and data model".
- "truncate / restrict support / half-normal / normalize a sub-measure" →
  `truncate`, support restriction & `normalize` in "Measure algebra" (the same sets
  from "Value types and data model" serve as truncation regions).
- "condition on data / posterior / Bayes update" → "Likelihoods and posteriors".
- "serialize / binary format / wire format" → textual FlatPIR S-expressions in
  "Intermediate representation"; JSON-based interop in "Profiles and interoperability".

## Section index

Top-level sections of `flatppl-design.md` (anchors follow the `{#sec:...}` pattern —
`grep -n '{#sec:'` lists them with line numbers; capture the exact anchor when citing).

| Section | Topic |
|---|---|
| Context and motivation | Why FlatPPL exists, goals |
| Language overview | Nutshell, targets, first example, core concepts, tour |
| Value types and data model | Scalars, constants, arrays, records, presets, tables, sets |
| Language design | Names/modules, binding, calling conventions, tuples, variates & measures, `elementof`/`external` (param domains), phases, reification, composition, holes, broadcasting, reductions, einsum, standard/composed modules, versioning, doc comments |
| Measure algebra | Foundations, measure monad, measure algebra, `truncate`/support restriction, `normalize`, `pushfwd` |
| Functions and deterministic operations | Array/table ops, access, convolution, elementary fns, operators, predicates, linalg, reductions, norms, logic/conditionals, membership/filtering/binning, random gen, measure-kernel primitives |
| Distributions | Univariate continuous/discrete, multivariate, composite |
| Likelihoods and posteriors | Likelihoods, conditioning, Bayes update, posteriors |
| Random value generation | Sampling, draws |
| Syntax | Statements, comments, supported/excluded constructs, indexing/slicing, broadcasting, lambdas, axis names, host embedding, formal grammar |
| Intermediate representation | FlatPIR: naming, module structure, doc forms, type/phase annotations, expressions, cross-module inference |
| Profiles and interoperability | Exchange platform, target profiles, HS³/RooFit, Stan |
| Standard modules | `particle-physics`, `generalized-linear-models`, `ext-linear-algebra`, `special-functions`, `polynomials`, `distances` |
| Worked examples | End-to-end model examples |
| Implementation notes | Known/planned implementations |
