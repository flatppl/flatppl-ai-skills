# FlatPPL — Copilot instructions

This project uses **FlatPPL**, a flat, loop-free, vectorized probabilistic language.
It is new and not yet in your training set — **do not answer from memory.**

Specification (one web document, roughly 40,000 words):
`https://flatppl.github.io/flatppl-design/flatppl-design.md`
Preferred: download it once (`curl -fsSL <that url> -o /tmp/flatppl-design.md`) and
`grep` it for exact text across the whole document. Without a shell, fetch one topic at a
time instead.

Core rules:
- No loops, no `if`/`else`, no control flow. Vectorize with broadcasting (`.+`, `f.(x)`),
  reductions, `iid(dist, n)`, and `ifelse(cond, a, b)`.
- `~` for random variables, `=` for deterministic transforms. `#` for plain comments, `%` / `%%%` for doc-comments.
- Constrain support via `elementof(...)` or `truncate(...)` (wrap in `normalize(...)`
  for a proper prior).
- Assemble posteriors with the measure pipeline: `lawof` / `kernelof` / `likelihoodof`
  / `bayesupdate` / `restrict`.
- Copy the shape of a worked example from the spec, and verify every construct against
  the spec before using it.

Full guidance:
- Answering language questions, or explaining a model → `.claude/skills/flatppl-docs/SKILL.md`
- Writing / reviewing / fixing / troubleshooting a `.flatppl` model → `.claude/skills/flatppl-model/SKILL.md`
- Catch-all → `AGENTS.md`
