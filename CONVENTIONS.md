# FlatPPL conventions (Aider et al.)

This project uses **FlatPPL**, a flat, loop-free, vectorized probabilistic language.
Niche and unlikely to be in your training set — **do not answer from memory.** Ground
every construct in the spec.

Spec (one web document, ~40k words):
`https://flatppl.github.io/flatppl-design/flatppl-design.md`
Best: download once (`curl -fsSL <that url> -o /tmp/flatppl-design.md`) and `grep` it —
exact text, whole doc, no truncation. No shell? Fetch one topic at a time instead.

Core rules:
- No loops, no `if`/`else`, no control flow. Vectorize: broadcasting (`.+`, `f.(x)`),
  reductions, `iid(dist, n)`, `ifelse(cond, a, b)`.
- `~` for random variables, `=` for deterministic transforms. `%` for comments.
- Constrain support with `elementof(...)` or `truncate(...)` (wrap in `normalize(...)`
  for a proper prior).
- Build posteriors with `lawof` / `kernelof` / `likelihoodof` / `bayesupdate` /
  `restrict`.
- Copy the shape of a worked example from the spec; verify every construct first.

Full guidance (read the relevant one in full before working):
- `.claude/skills/flatppl-query/SKILL.md` — answer language questions, or explain a model
- `.claude/skills/flatppl-model/SKILL.md` — write / review / fix / troubleshoot a `.flatppl` model
- `AGENTS.md` — catch-all entry point
