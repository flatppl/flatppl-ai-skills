---
name: flatppl-docs
description: Answer any question about the FlatPPL language, its design, syntax, value types, measure algebra, built-in functions/distributions, FlatPIR, or profiles by consulting the FlatPPL design docs. Use this whenever the user asks how FlatPPL does something, what a FlatPPL construct means, or whether FlatPPL supports a feature — even if they don't name a doc file or say "docs".
---

# Answering FlatPPL questions from the docs

You answer questions about FlatPPL using its design documentation in
`flatppl-design/docs/`. FlatPPL is niche and **not in your training set**; your
priors about it are likely wrong, so answer from the docs, never from memory.

This skill *reads* the spec to explain a construct or answer whether FlatPPL supports
something. It does NOT review changes to the spec docs (use `flatppl-doc-review`),
review a downstream plan against the spec (use `flatppl-spec-review`), build a working
`.flatppl` model — even when phrased "how do I write X in flatppl" (use
`flatppl-author`) — or audit an engine (use `flatppl-conformance-audit`).

Reading whole doc files is expensive (`04-design.md` and `07-functions.md` are each
10k+ tokens), so read at **section** granularity, not file granularity:

0. **Locate the docs.** Paths below are relative to the FlatPPL repo root. If
   `flatppl-design/docs/` isn't there (you're in a subdir or worktree), Grep with
   `--files-with-matches` for a known doc string (e.g. `measure algebra`) to find
   the actual docs dir before answering — do not answer from
   memory if the docs can't be found; say you can't locate them.
1. **Route to the file(s)** using the index and indirect-question map below. When
   the wording is indirect or spans topics, `Grep` the docs dir first — the index
   lists topics, not every term ("loops", "constraining a domain", "truncating a
   distribution" won't appear verbatim, but Grep lands you on the right file).
2. **Find the section.** In the chosen file, `Grep -n '^#{2,6} '` to list its
   headers (e.g. `### Convolution` or `### <a id="sec:broadcasting"></a>Broadcasting`).
   Use `^#{2,6} ` not `^#` — a single `#` matches code-block comments like
   `# equivalent to:`, not headers. Pick the matching header.
3. **Read only that section** with `Read` `offset`/`limit` (header line → next
   header). Do **not** `Read` a whole file >5KB unless the question genuinely
   spans it. If a section turns out too narrow, widen the range — still cheaper
   than the whole file.
4. **Answer, grounded.** Cite the file and section **heading text**
   (e.g. `04-design.md` → "Convolution"); add the `#anchor` when the header has one
   (only some do). Cite headings, not line numbers — line numbers drift, headings
   don't. Quote the exact doc sentence for each non-obvious claim. If Grep finds
   nothing, the docs **don't cover it** — say so plainly; never fill from prior
   knowledge.

If a doc file is **already present in this conversation** from an earlier answer,
do not re-Read it — its content is still in context. Only re-Read if you have
reason to think it changed this session.

### Common indirect questions → where to look
- "for-loop / iterate over data / map over points" → FlatPPL is loop-free; see
  broadcasting & reductions in `04-design.md`, excluded constructs in `05-syntax.md`.
- "if / else / conditional / branching" → no control flow; `ifelse` and logic in
  `07-functions.md`, excluded constructs in `05-syntax.md`.
- "constrain a parameter's domain / restrict a value to a set" → `elementof` /
  `external` in `04-design.md`, the set catalogue in `03-value-types.md`.
- "truncate / restrict support / half-normal / normalize a sub-measure" →
  `truncate`, support restriction & `normalize` in `06-measure-algebra.md`
  (the *same* sets from `03-value-types.md` serve as truncation regions).
- "serialize / binary format / wire format" → only lightly covered; textual
  FlatPIR S-expressions in `11-flatpir.md` (binary "not yet specified"),
  JSON-based interop in `12-profiles.md`.

## Doc index (`flatppl-design/docs/`)

Section structure is discovered live by Grep (step 2) — this table only routes to
the file. If `ls flatppl-design/docs/` shows a `.md` file absent from this table,
flag it as a stale index.

| File | Topic |
|---|---|
| `01-context.md` | Context and motivation: why FlatPPL exists, goals |
| `02-overview.md` | Language overview: nutshell, targets, first example, core concepts, tour |
| `03-value-types.md` | Value types & data model: scalars, constants, arrays, records, presets, tables, sets |
| `04-design.md` | Language design: names/modules, binding, calling conventions, tuples, variates & measures, `elementof`/`external` (param domains), phases, reification, composition, holes, broadcasting, reductions, einsum, standard/composed modules, versioning, doc comments |
| `05-syntax.md` | Canonical syntax: statements, comments, supported/excluded constructs, indexing/slicing, broadcasting, lambdas, axis names, host embedding, formal grammar |
| `06-measure-algebra.md` | Measure algebra & analysis: foundations, measure monad, measure algebra, `truncate`/support restriction, `normalize`, `pushfwd`, likelihoods & posteriors |
| `07-functions.md` | Built-in functions: array/table ops, access, convolution, elementary fns, operators, predicates, linalg, reductions, norms, logic/conditionals, membership/filtering/binning, random gen, measure-kernel primitives |
| `08-distributions.md` | Built-in distributions: univariate continuous/discrete, multivariate, composite |
| `09-standard-modules.md` | Standard modules: `particle-physics`, `generalized-linear-models`, `ext-linear-algebra`, `special-functions`, `polynomials`, `distances` |
| `10-examples.md` | Worked end-to-end model examples |
| `11-flatpir.md` | FlatPIR (intermediate representation): naming, module structure, doc forms, type/phase annotations, expressions, cross-module inference |
| `12-profiles.md` | Profiles & interoperability: exchange platform, target profiles, HS³/RooFit, Stan, future |
| `13-implementations.md` | Implementations (appendix): known/planned |
| `15-references.md` | References / citations |

(`00-frontmatter.md` = abstract/authors; `14-ai-declaration.md` = AI-usage note. Skip unless asked.)
