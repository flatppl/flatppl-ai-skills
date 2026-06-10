# FlatPPL conventions for AI coding tools

This project uses **FlatPPL**, a flat, loop-free, vectorized probabilistic language.
New and not yet in your training set — **do not answer from memory.** Ground
every construct in the spec.

Specification (one web document, roughly 40,000 words):
`https://flatppl.github.io/flatppl-design/flatppl-design.md`
Preferred: download it once (`curl -fsSL <that url> -o /tmp/flatppl-design.md`) and
`grep` it for exact text across the whole document. Without a shell, fetch one topic at a
time instead.

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
