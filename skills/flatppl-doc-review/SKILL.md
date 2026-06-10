---
name: flatppl-doc-review
description: Review a FlatPPL design-doc change or section for correctness, internal consistency, and clarity by cross-checking every non-obvious claim and every code example against the normative docs in flatppl-design/docs/. Use when the user wants a doc section, a docs diff, or a specific example in the normative FlatPPL spec reviewed before it is published — especially FlatPIR lowerings, type/phase annotations, and worked examples.
allowed-tools: Read, Grep, Bash, Agent
---

# Reviewing a change to the FlatPPL spec docs

You review the FlatPPL design documentation in `flatppl-design/docs/` for
**correctness, internal consistency, and clarity**. You produce *findings*, not
edits — the user applies fixes after seeing them (`allowed-tools` is read-only by
design).

This reviews changes to the **normative spec itself**. It does NOT answer a
question from the docs (use `flatppl-docs`), review a downstream plan that *cites*
the spec (use `flatppl-spec-review`), review a `.flatppl` model (use
`flatppl-author`), or audit an engine against the spec (use
`flatppl-conformance-audit`).

FlatPPL is niche and **not in your training set**; your priors about it are
likely wrong. Every claim you assert (including "this is a bug") must be grounded
in a quoted doc sentence, never in memory.

## What to review

Resolve the user's request to a scope:
- **A diff / branch** (e.g. "diff", "branch X", "the uncommitted changes"):
  `cd flatppl-design && git diff [<base>] -- docs/` (or `git diff --stat` first to
  see touched files). `flatppl-design` is its own git repo (the repo *root* is not) —
  if `cd flatppl-design` fails (you're in a subdir/worktree), locate it first with the
  step-0 method, don't give up. Review only the changed hunks plus enough surrounding
  context to judge them.
- **A named section or file** (e.g. "the Intermediate Representation section",
  "11-flatpir.md"): locate and read it at **section granularity** (see method).
- **Nothing specific**: ask which section/diff, or default to `git diff` if the
  tree is dirty.

## Normative vs illustrative — the core rule

Some files **define** the language; others **illustrate** it. When an example and
a rule disagree, **the example is almost always the bug — but verify the rule
too**, because the rule's own wording may be the error.

| Topic | Normative source (the authority) |
|---|---|
| Names, modules, binding, calling conventions, tuples, variates/measures, phases, **reification, placeholders/holes**, broadcasting, reductions, einsum | `04-design.md` |
| Surface syntax, excluded constructs, indexing/slicing, lambdas, axis names, grammar | `05-syntax.md` |
| Scalars, sets, arrays, records, tables, presets | `03-value-types.md` |
| Measure algebra, `truncate`/`normalize`/`pushfwd`, likelihoods & posteriors | `06-measure-algebra.md` |
| Built-in functions & operators | `07-functions.md` |
| Distributions | `08-distributions.md` |

Largely **illustrative / derived** (must conform to the sources above; treat their
examples as suspect when they conflict): `11-flatpir.md`, `10-examples.md`,
`02-overview.md`, `09-standard-modules.md`.

**Fix direction:** before asserting which side is wrong, re-derive from the
**definitional** form, not from the example's surface shape. A worked example can
look self-consistent across all its own sub-parts yet still contradict the
definition. *(Precedent: a FlatPIR example used the placeholder `_x_` as a parameter
name in all its exhibits, but `04-design.md`'s placeholder lowering proved the
parameter is `x` — the example was the bug. Deriving from the definition, not the
self-consistent example, is what caught it.)*

## Method

0. **Locate the docs.** If `flatppl-design/docs/` isn't present, `Grep
   --files-with-matches` for a known string (e.g. `measure algebra`) to find them.
   If you can't, say so — don't review from memory.
1. **Read the section under review** at section granularity:
   `Grep -n '^#{2,6} '` the file to list headers, then `Read` the target section
   by `offset`/`limit`. Avoid reading whole 10k-token files unless the review
   genuinely spans them.
2. **For every non-obvious claim, open the normative source** for that topic
   (table above), find the governing section the same way, and **quote the exact
   sentence**. Confirm the claim matches. A claim that cites no source you can
   find is itself a finding ("unsupported / undocumented").
3. **Run the consistency checks below.**
4. **Report** (format below). Separate real bugs from confirmed-correct.

## Consistency checks (the ones that catch real bugs)

- **Example ⇄ rule.** Does each code example obey the normative rule it
  illustrates? Re-derive from the definition.
- **Paired exhibits agree.** When a feature is shown as Surface FlatPPL / Bare
  FlatPIR / Annotated FlatPIR (or surface + lowering), the same entities must line
  up across all forms **per the documented lowering**, not just look similar:
  - `name ~ expr` ⇒ `name = draw(expr)` (`05-syntax.md` tilde bindings).
  - operators / field access / indexing ⇒ `get` and built-in calls
    (`07-functions.md` "Field and element access"; `11-flatpir.md` intro).
  - surface placeholders `_x_` are body-internal; the **parameter** name is the
    boundary-spec LHS / lambda arg (`04-design.md` reification). Placeholders must
    not surface as FlatPIR parameter names.
  - module dot-access (`m.foo`) ⇒ `(%ref <alias> foo)`, **not** `get`; built-in
    `base.foo` ⇒ bare head.
  - by-name matching (likelihood `%inputs`, kwargs, auto-splat) must use the
    **public argument names**, so cross-check those names against the callable's
    actual parameters.
- **Type vs phase vs set.** Structural category (`%scalar`/`%array`/…), phase
  (`%fixed`/`%parameterized`/`%stochastic`), and set membership (`elementof`) are
  distinct; annotations shouldn't conflate them (`11-flatpir.md` "Sets and types
  are distinct"). Check phase propagation (stochastic dominates; `draw` is
  stochastic; literal-arg constructors are `%fixed`).
- **Cross-references resolve.** Every `(NN-file.md#anchor)` should point at a real
  header/`<a id>`. Spot-check the ones in the reviewed section.
- **Catalogue terms exist.** Set names, distributions, built-ins, and `%`-keywords
  used in the section must appear in their defining catalogue — flag typos
  (`%paramterized`) and invented names.
- **Stale skill index.** If `ls flatppl-design/docs/` shows a `.md` missing from
  the `flatppl-docs` skill's doc-index table, note it.

## Scaling: when to fan out (default: don't)

**Inline is the default.** A doc review is a *narrative* judgment — do these sections
cohere, does the example contradict the rule — and the **cross-section consistency +
clarity pass ALWAYS stays inline** (it can't be parallelised without losing what it
measures). Fan out **only** on a **large multi-file diff (≈4+ files, or a sweeping
rename touching many independent sections)**: do the consistency pass inline first, then
one agent per file/claim-cluster for independent claim⇄source verification, then
adversarially refute each `CORRECTNESS` bug-claim from the definition (floor `sonnet` —
confidently-wrong bug-claims are this skill's main failure mode), then synthesise inline.
Tiering + the inline/parallel split: `.claude/references/fan-out-and-tiering.md`.

## Report format

Group findings; lead with the worst. For each:

- **Severity**: `CORRECTNESS` (contradicts a normative rule / wrong) ·
  `CONSISTENCY` (examples or sections disagree) · `CLARITY` (correct but
  ambiguous/underspecified) · `UNSUPPORTED` (claim with no findable source).
- **Where**: file → **heading text** (+ `#anchor` if present). Cite headings, not
  line numbers — line numbers drift.
- **Evidence**: quote the conflicting sentence(s) from *both* the reviewed section
  and the normative source.
- **Fix**: concrete, and state **which side** changes and why (derived from the
  definition).

Then a short **Confirmed correct** list: things that look wrong but are right
(with the one-line reason), so they aren't re-flagged later.

If you find nothing, say so plainly and list what you checked.
