# FlatPPL spec reference

Routing + recall aid for the public spec (`flatppl-design.md`). Read this **only when you
need to locate a topic or recall what exists** — it is not loaded by default. It is **not**
a signature reference: names are current as of the spec version pinned in "Language
design" → versioning, but **grep the cited section in the downloaded spec for exact
arguments, semantics, and the full list** before relying on any construct. FlatPPL is new,
so the spec — not memory, not this file — is the source of truth.

`grep -n '{#sec:' /tmp/flatppl-design.md` lists every section anchor with its line.

## Basic syntax

Surface syntax of FlatPPL (section "Syntax" `{#sec:syntax}`; grep there for the formal
grammar and full detail). The language is deliberately lean.

- **Statements** — one per line, or separated by `;`. A module is a sequence of bindings.
- **Bindings** — `name = expr` is deterministic; `name ~ expr` is a stochastic node,
  exactly `name = draw(expr)`. Positional decomposition: `a, b, c = expr` / `a, b ~ expr`,
  `x, y = some_record`, `value, _ = rand(...)`.
- **Comments** — `#` starts a plain line comment; `### … ###` is a plain block comment
  (both discarded). **Doc-comments** attach to a binding and survive into
  FlatPIR: `% text` (single line, leading or trailing on the binding's line) and
  `%%% … %%%` (block, leading only), with an optional markup tag
  `%md` (default, Markdown + `$…$` math) or `%typ` (Typst).
- **Literals** — numbers (`3.14`, `42`, `0xF7`, `1_000_000`, `1.45e7`), strings (`"foo"`),
  booleans (`true` / `false`), arrays (`[1, 2, 3]`), records (`record(a = 1, b = 2)`),
  tuples (`(a, b)`).
- **Operators** — infix `+ - * / ^` and unary `-`; comparisons `< > == != <= >=` and `in`
  (set membership), chainable (`a < b <= c`); logical `&& || !`. `^` is right-associative.
  No implicit broadcasting: plain `+` / `-` require matching shapes, `*` is matrix/vector
  multiplication, and `/` and `^` are scalar-only.
- **Broadcasting** — dot forms desugar to `broadcast`: dot-call `f.(x)`, dotted binary
  `a .+ b`, dotted unary `.- x`. (`in` has no dotted form.)
- **Lambdas** — `arg -> expr` or `(a, b) -> expr` (sugar for `functionof`); a single
  argument takes no parentheses, at least one argument is required, and the body extends as
  far right as possible.
- **Indexing** — 1-based. `A[i]`, `A[i, j]`, field access `r.field`; `A[:, j]` selects a
  whole axis (lowers to `get(A, all, j)`); `A[!, j]` extracts the sole element of a
  length-1 axis.
- **Aggregation** — `C[.i, .k] := expr` is sum-`aggregate` over axis names `.i`, `.k`; the
  metric form `g: C[.mu^, .nu_] := expr` is `metricsum`.
- **Excluded** — no type annotations, no loops or `if`/`else` (use `ifelse`), no
  function-definition blocks (use `functionof`).
- **Special operations** (their own syntax, not ordinary calls): `elementof`, `valueset`,
  `draw`, `lawof`, `functionof`, `kernelof`, `fn`, `load_module`.

## Section index

| Section | Topic |
|---|---|
| Context and motivation | Why FlatPPL exists, goals |
| Language overview | Nutshell, targets, first example, core concepts, tour |
| Value types and data model | Scalars, constants, arrays, records, presets, tables, sets |
| Language design | Names/modules, binding, calling conventions, tuples, variates & measures, `elementof`/`external` (param domains), phases, reification, composition, holes, broadcasting, reductions, einsum, standard/composed modules, versioning, doc comments |
| Measure algebra | Foundations, measure monad, measure algebra, `truncate`/support restriction, `normalize`, `pushfwd`, likelihoods & posteriors |
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

## Common indirect questions → where to look
- "for-loop / iterate over data / map over points" → FlatPPL is loop-free; broadcasting &
  reductions in "Language design", excluded constructs in "Syntax".
- "if / else / conditional / branching" → no control flow; `ifelse` and logic in
  "Functions and deterministic operations", excluded constructs in "Syntax".
- "constrain a parameter's domain / restrict a value to a set" → `elementof` / `external`
  in "Language design"; the set catalogue in "Value types and data model".
- "truncate / restrict support / half-normal / normalize a sub-measure" → `truncate`,
  support restriction & `normalize` in "Measure algebra".
- "condition on data / posterior / Bayes update" → "Likelihoods and posteriors".
- "serialize / binary format / wire format" → textual FlatPIR S-expressions in
  "Intermediate representation"; JSON-based interop in "Profiles and interoperability".

## Construct index (what exists, and where to grep for signatures)

**Distributions** — "Distributions" (univariate continuous, univariate discrete,
multivariate, composite):
`Bernoulli` `Beta` `BinnedPoissonProcess` `Binomial` `Categorical` `Categorical0`
`Cauchy` `ChiSquared` `Dirichlet` `Exponential` `Gamma` `GeneralizedNormal` `Geometric`
`InverseGamma` `InverseWishart` `Laplace` `LKJ` `LKJCholesky` `Logistic` `LogNormal`
`Multinomial` `MvNormal` `NegativeBinomial` `NegativeBinomial2` `Normal` `Pareto` `Poisson`
`PoissonProcess` `StudentT` `Uniform` `VonMises` `Weibull` `Wishart`.

**Value sets & parameter domains** — "Value types and data model" + "Language design":
predefined `reals` `posreals` `nonnegreals` `unitinterval` `posintegers` `nonnegintegers`
`integers` `booleans` `complexes` `anything` `rngstates`; constructors `interval(lo, hi)`
`cartprod(...)` `cartpow(S, size)` `stdsimplex(n)` `valueset(x)`; domains via
`elementof(S)` and `external(...)`.

**Functions & deterministic operations** — same-named section (grep it for each
category's members and signatures): array/table generation, field & element access,
array/table operations, convolution, scalar restrictions & constructors, elementary
functions, operator-equivalent functions, scalar predicates, checked values, linear
algebra, reductions, norms & normalization, logic & conditionals (`ifelse`, …),
membership/filtering/binning, binning, approximation functions, random generation,
measure-kernel evaluation primitives. Reusable functions: `functionof`; broadcast with
dotted forms (`.+`, `f.(x)`).

**Measure algebra & posteriors** — "Measure algebra":
- Reification: `lawof` `kernelof` `functionof`.
- Composition: `joint` `jointchain` `kchain` `fchain` `kscan` `scan` `markovchain` `iid`
  `superpose` `weighted` / `logweighted`.
- Transform & restrict: `pushfwd` `truncate` `normalize` `disintegrate` `relabel`.
- Likelihood / posterior: `likelihoodof` `bayesupdate` `restrict`.
- Mass / density: `totalmass` `densityof` `logdensityof`.

**Standard modules** — "Standard modules": `particle-physics`
`generalized-linear-models` `ext-linear-algebra` `special-functions` `polynomials`
`distances`. Load via `load_module` / `standard_module`; a function absent from
"Functions" may be a standard-module builtin — check both.
