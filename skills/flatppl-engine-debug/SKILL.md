---
name: flatppl-engine-debug
description: Diagnose a specific wrong, divergent, or crashing FlatPPL engine result — a density/sample number that looks off, a JS-vs-Rust disagreement, or a failing corpus case. Use when a FlatPPL engine (flatppl-js or flatppl-rust) produces a suspect numeric output, the two engines disagree, an op throws, or a model that should work doesn't. Pins the spec lowering, derives an INDEPENDENT oracle, fixes, and regression-tests.
---

# Debugging a FlatPPL engine result

This skill diagnoses **one specific** engine failure: a number that looks wrong, a
JS↔Rust disagreement, a thrown op, or a corpus case that won't run. It is targeted
debugging, not a broad sweep — use `flatppl-conformance-audit` to systematically
audit many lowerings, `flatppl-author` to write/fix a model, `/review` for generic
code review, and `flatppl-docs` to read the spec. For the debugging *method* itself
(reproduce → minimise → hypothesise → instrument → fix → regression-test), the
`diagnose` / `systematic-debugging` skill is the harness; this skill adds the
FlatPPL-specific spec-grounding and the oracle discipline that keeps you honest.

FlatPPL is niche and **not in your training set**; never decide a number is right
or wrong from your own arithmetic intuition. Correctness is defined by the **spec
lowering**, checked against an **independent oracle** — not by what either engine
emits.

## Where the engines live

- **flatppl-js** — `flatppl-js/packages/engine/`: `density.ts`, `density-prims.ts`,
  `mat-density.ts`, `worker.ts`, `worker-entry.ts`. Discover the actual op handler
  live (`Grep` the op name); files move.
- **flatppl-rust** — `flatppl-rust/crates/` (`core`, `flatpir`, `syntax`); see
  `flatppl-rust/ARCHITECTURE.md`.

Paths are relative to the repo root. If an `ls`/`cd` on a sibling repo comes back empty
(you're in a subdir or worktree), resolve the repo root first (Grep for a known marker)
— never proceed from memory on an empty listing.

## Workflow

1. **Reproduce, then minimise.** Get the smallest `.flatppl` (or direct op call)
   that still shows the wrong number, and pin exactly which engine, which op, and
   which extraction (`logdensityof` / `densityof` / sampling / posterior mean).
2. **Name the spec lowering.** Via the `flatppl-docs` skill, find the normative
   lowering for that op and **quote it, citing the section heading** (headings outlast
   line numbers — add a line only as a transient pointer). The result is wrong relative
   to *the spec*, not relative to the other engine. Write the hypothesis as
   "engine does X; spec at `06-…` → '<heading>' mandates Y."
3. **Derive an INDEPENDENT oracle — never bake an engine's output in as expected.**
   That is oracle contamination (`TODO-flatppl-rust.md` testing strategy: "derive
   oracles INDEPENDENTLY"; "neither is the other's oracle"). Three independent
   traditions:
   - **Closed-form** density/moment math — `flatppl-dev/flatppl-engine-concepts.md`
     → "Density rules are normative semantics".
   - **Distributions.jl / MeasureBase.jl** via the **julia MCP**
     (`mcp__julia__julia_eval`) — compute the expected density/sample stat live in a
     Julia session and compare. This is the cheapest trustworthy oracle for
     univariate/standard distributions.
   - **Cross-engine** JS↔Rust — a *disagreement detector*, never an authority:
     when they differ, at least one is wrong, but agreement does not prove correct
     (both can share the same shortcut). LLM arithmetic is triage too, not an oracle.

   If the julia MCP is unavailable (headless / cron / some sub-agent sessions don't
   expose it, and the `julia` binary may be absent), fall back to closed-form
   derivation. If NO independent oracle is reachable, say so plainly and stop short of a
   verdict — do **not** substitute cross-engine agreement as the oracle; that is the
   contamination this step exists to prevent.
4. **Check the known scar zones first.** `flatppl-dev/measure-algebra-audit.md` maps
   them: the engine is trustworthy only on the canonical
   `bayesupdate(L, lawof(draws))` path where `prior == lawof(the boundary draws)`.
   Step off it — a free `elementof` boundary, a prior that is *not* the law of the
   like-named draws, a kernel parameter reached through a derived binding, a
   record-/multi-leaf variate, a reused named factor, a non-closed-form normalizer —
   and the engine returns a **silently wrong number**, **hard-fails**, or the
   **sampling and density paths of the same measure disagree**. Recurring root
   cause: density machinery resolves a reified-kernel input via `getMeasure(name)`
   (the module-graph binding of the same name) instead of the atoms the lowering
   mandates. If your bug is off this path, start there.
5. **Fix, then regression-test against the oracle.** Add a test/corpus case that
   pins the **oracle** value (closed-form or Distributions.jl), not the old engine
   output. For flatppl-js coverage you must run under **Node 24** — Node 26 breaks
   `c8` and native coverage. Resolve the keg and **assert** you're on 24 — don't
   hardcode the path (the keg may not be installed):
   ```
   N24="$(brew --prefix node@24 2>/dev/null)/bin"
   [ -x "$N24/node" ] && export PATH="$N24:$PATH" || echo "node@24 missing: brew install node@24"
   node --version   # MUST print v24.x — if not, stop; coverage on 26 is silently broken
   cd flatppl-js/packages/engine && npm run test:coverage
   ```
   Plain `npm test` (`node --test`) runs on 24 or 26; coverage only on 24. Rust:
   `cargo test` / `cargo nextest` in `flatppl-rust`.

## Parallel hypotheses (only when the cause is genuinely ambiguous)

**Default: stay inline** — the reproduce → minimise → instrument → fix loop is a
continuous chain and that continuity usually cracks the bug. Fan out **only** when, after
the minimised repro, you have **≥2 competing, mutually-exclusive, independently-
investigable root-cause hypotheses** a single cheap probe can't discriminate — e.g. a
wrong density could be the density walk (`density.ts`), the reified-input `getMeasure`
ref-resolution (`materialiser-shared.ts`), or the marginalization reduction
(`mat-density.ts`). Then spawn one agent per hypothesis (the
`agent-teams:parallel-debugging` pattern) to gather `file:line` evidence confirming or
falsifying ITS hypothesis against the spec lowering + the oracle, returning a verdict —
not a fix. Keep the minimise, the arbitration, and the fix inline.

Tiering, the inline/parallel split, and the finder-up rule: `.claude/references/fan-out-and-tiering.md`.

## Report format

Per finding: the minimal repro, the **hypothesis**, the spec **section heading** it
violates (quote it), the engine location (`file:line`), the **oracle** and its independently
derived value (note which tradition), a **confidence** level, and the fix +
regression test. Keep "verified against an independent oracle" separate from
"matches the other engine" — the latter is not proof.
