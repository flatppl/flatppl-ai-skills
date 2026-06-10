# FlatPPL — Copilot instructions

This project uses **FlatPPL**, a flat, loop-free, vectorized probabilistic language.
It is new and not yet in your training set — **do not answer from memory.**

Spec (one web document, ~40k words):
`https://flatppl.github.io/flatppl-design/flatppl-design.md`
Best: download once (`curl -fsSL <that url> -o /tmp/flatppl-design.md`) and `grep` it —
exact text, whole doc, no truncation. No shell? Fetch one topic at a time instead.

Core rules:
- No loops, no `if`/`else`, no control flow. Vectorize with broadcasting (`.+`, `f.(x)`),
  reductions, `iid(dist, n)`, and `ifelse(cond, a, b)`.
- `~` for random variables, `=` for deterministic transforms. `%` for comments.
- Constrain support via `elementof(...)` or `truncate(...)` (wrap in `normalize(...)`
  for a proper prior).
- Assemble posteriors with the measure pipeline: `lawof` / `kernelof` / `likelihoodof`
  / `bayesupdate` / `restrict`.
- Copy the shape of a worked example from the spec, and verify every construct against
  the spec before using it.

Full guidance:
- Answering language questions, or explaining a model → `.claude/skills/flatppl-query/SKILL.md`
- Writing / reviewing / fixing / troubleshooting a `.flatppl` model → `.claude/skills/flatppl-model/SKILL.md`
- Catch-all → `AGENTS.md`
