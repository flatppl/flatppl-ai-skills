---
name: flatppl-spec-review
description: Review a FlatPPL plan, design doc, ADR, or PR description — a DOWNSTREAM artifact that cites the normative spec, NOT the spec docs themselves — for fidelity to the flatppl-design docs and consistency with the cross-repo roadmap (TODO-*.md), shipped code, and ARCHITECTURE. Use when the user wants a plan/design/ADR reviewed before implementation, or asks whether a plan's claims match the spec. To review changes to the spec docs themselves, use flatppl-doc-review instead.
---

# Reviewing a FlatPPL plan or design doc

`flatppl-design/docs/` is **normative**. FlatPPL is niche and **not in your training
set**; your priors are likely wrong — work from the docs, not memory. A plan, design
doc, ADR, or PR description is a downstream artifact: every claim it makes about FlatPPL
must be verified against the docs, and any conflict means the artifact is wrong
**unless a very good reason is stated**. Verify, don't trust — a citation existing is
not the same as the cited section saying what the artifact claims.

This skill reviews such an artifact along two separate axes and resolves conflicts
spec-first. It does NOT review changes to the spec docs themselves (use
`flatppl-doc-review`), `.flatppl` models (use `flatppl-author`), or a code diff (use
`/review`).

## Workflow

1. **Identify the claim surface.** List every design-doc citation, every semantic claim
   about FlatPPL behavior, and every roadmap/phase placement the artifact makes.
2. **Verify each claim against the docs — route, don't guess.** Use the `flatppl-docs` skill
   against `flatppl-design/docs/`. For each cited section: does it exist, and does it
   *say* what the artifact claims? Quote it, citing the doc **section heading**
   (headings outlast line numbers). Section map: design/phases →
   `04`, syntax → `05`, measure-algebra → `06`, functions → `07`, distributions → `08`,
   standard modules → `09`, examples → `10`, FlatPIR → `11`, profiles → `12`,
   value-types → `03`. If the docs don't cover a claim, say so — don't invent.
3. **Run two axes, kept separate** (**default: run both inline**; fan out only for a
   large artifact and on explicit user go — the Workflow opt-in rule. When you do, spawn
   one sub-agent per axis and tier by model: **spec-fidelity → `opus`** (matching a claim
   to the spec's *semantics* is the hard reasoning), **roadmap-consistency → `sonnet`**
   (mostly cross-referencing TODO / code / ARCHITECTURE). Finder-up-when-unsure +
   rationale: `.claude/references/fan-out-and-tiering.md`):
   - **Spec-fidelity** — claim vs normative docs. Group findings:
     *misrepresentation* (docs contradict or don't support the claim),
     *unverifiable* (cited section or quote not found),
     *correct-but-risky* (faithful, but the doc is ambiguous or silent — the artifact
     should flag it, not state it as settled).
   - **Roadmap-consistency** — vs `flatppl-dev/TODO-*.md` (phase placement, scope-creep,
     committed invariants), shipped code + `ARCHITECTURE.md`, `CONVENTIONS.md` /
     `AGENTS.md`, plus internal consistency and cross-doc interface contracts when
     several docs are in scope.
4. **Resolve spec-first.** Docs are normative. A doc–spec conflict ⇒ the artifact is
   wrong absent a stated good reason. When a *TODO invariant* conflicts with the
   normative docs, fix to match the docs **and sync the TODO in lockstep**
   (`AGENTS.md` — keep the roadmap accurate); never bake an override into a plan-doc
   footnote.
5. **Report** grouped by axis. Cite the `artifact:line` + the doc **section heading** per finding;
   distinguish hard violations from judgement calls; end with a one-line summary per
   axis and the worst single issue. Apply fixes only if asked.

## Principles

- **Docs normative; cite the heading.** Every finding carries the doc section heading it
  rests on (headings outlast line numbers; add a line only as a transient pointer).
- **Verify, don't trust.** Citation-exists ≠ says-what-claimed; no-ERROR ≠ correct.
- **Two axes stay separate.** A doc can pass spec-fidelity and fail roadmap-consistency,
  or the reverse; merging them lets one mask the other.
- **Paths are relative to the repo root.** If an `ls`/`cd` on `flatppl-dev/`, the docs,
  or shipped code comes back empty (subdir/worktree), resolve the root first — don't
  judge roadmap consistency from memory on an empty listing.
- **Read `flatppl-dev/CONVENTIONS.md` + `AGENTS.md`** for ecosystem invariants and the
  cross-repo read-first protocol before judging roadmap consistency.
