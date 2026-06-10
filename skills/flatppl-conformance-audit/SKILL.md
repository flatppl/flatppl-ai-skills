---
name: flatppl-conformance-audit
description: Audit a FlatPPL implementation (engine code, examples, grammar) for conformance to the normative flatppl-design spec lowerings — measure-algebra, syntax, distributions, FlatPIR. Adversarially verify each lowering and report divergences. Use when the user wants to check an engine / examples / grammar for spec drift, run a conformance audit, or find where an implementation diverges from the spec.
---

# Auditing a FlatPPL implementation for spec conformance

`flatppl-design/docs/` is **normative**. This skill audits an *implementation* — engine
code (`flatppl-js` / `flatppl-rust`), the `flatppl-examples` corpus, or
`flatppl-grammars` — against the spec's lowerings, adversarially verifying each finding
before confirming it, and emits a divergence report shaped like
`flatppl-dev/measure-algebra-audit.md`.

FlatPPL is niche and **not in your training set**; verify every claim against the docs,
never from memory (and a no-ERROR parse / two agreeing engines ≠ correct). Paths are
relative to the repo root; if an `ls`/`cd` on a sibling repo comes back empty (subdir or
worktree), resolve the root first — don't audit from memory on an empty listing.

It does NOT review the normative spec docs (use `flatppl-doc-review`) or a downstream
plan/ADR (use `flatppl-spec-review`), write or review an individual model's
validity/idiom (use `flatppl-author` — this skill is the adversarial spec-conformance
*sweep* of the corpus, not a per-model idiom check), edit or verify a grammar change /
fix a mis-parse (use `flatppl-grammar-change`), diagnose one specific wrong/divergent
engine result (use `flatppl-engine-debug` — this skill is the broad sweep, that one is
targeted), or do generic code review (use `/review`).

## Workflow

1. **Scope the surface.** Pick the spec area × artifact: measure-algebra (`06`),
   syntax (`05`), distributions (`08`), or FlatPIR (`11`) × engine op handlers,
   examples, or grammar rules.
2. **Enumerate the normative lowerings/claims** from `flatppl-design/docs/` via
   the `flatppl-docs` skill. Each lowering is one audit target; quote it and cite its
   **section heading** (headings outlast line numbers).
3. **Tier each target by difficulty.** Tag each with a `tier` and pass
   `agent(prompt, {model: tier})` — `haiku` for existence/keyword checks, `sonnet` for
   code-tracing, `opus` for measure-semantics reasoning. Finder-up-when-unsure;
   adversarial verifier floor `sonnet`. Tier definitions + the false-negative asymmetry:
   `.claude/references/fan-out-and-tiering.md`.
4. **Fan out (Workflow tool), then adversarially verify.** One agent per target:
   locate the implementation, compare to the spec, hypothesize a divergence. Then a
   second agent tries to **refute** each hypothesized divergence before it is confirmed
   (the pattern that produced `measure-algebra-audit.md`) — never `haiku` for the
   refuter. Small audits run inline without a workflow.
5. **Oracle discipline.** The normative docs are the spec oracle. For numeric behavior,
   check against *independent* oracles — closed-form densities
   (`flatppl-dev/flatppl-engine-concepts.md`, "Density rules are normative semantics"),
   Distributions.jl / MeasureBase.jl —
   and **never bake one engine's output in as the expected value** (`TODO-flatppl-rust.md`:
   "neither is the other's oracle"). Engine and LLM outputs are disagreement-detectors,
   not authorities. A no-ERROR parse ≠ correct.
6. **Report.** Per finding: spec **section heading** (quoted), implementation location, the divergence, a
   confidence level, and confirmed/refuted. Mirror the `measure-algebra-audit.md`
   header + one-finding-per-row format.

## Opt-in guard

Spawn the Workflow only on **explicit user go**; for a handful of lowerings, audit
inline. Default-inline / opt-in rationale: `.claude/references/fan-out-and-tiering.md`.

## Priors

- `flatppl-dev/measure-algebra-audit.md` + `measure-lowering-unification-plan.md` —
  prior scar history; the known off-`prior==lawof(draws)` divergence zones the JS suite
  under-covers. Start there.
- `flatppl-dev/CONVENTIONS.md` + `AGENTS.md` — ecosystem invariants + the cross-repo
  read-first protocol.
