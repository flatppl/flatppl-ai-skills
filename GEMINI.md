# FlatPPL — Gemini guide

This project uses **FlatPPL**, a flat, loop-free, vectorized probabilistic language.
It is new and not yet in your training set — **do not answer from memory.**
Ground every claim and every construct in the public spec.

Specification (one web document, roughly 40,000 words):
`https://flatppl.github.io/flatppl-design/flatppl-design.md`
Preferred: download it once (`curl -fsSL <that url> -o /tmp/flatppl-design.md`) and
`grep` it for exact text across the whole document. Without a shell, fetch one topic at a
time instead. Quote the section heading and `{#sec:...}` anchor when you cite it.

Core rules:
- No loops, no `if`/`else`, no control flow. Vectorize: broadcasting (`.+`, `f.(x)`),
  reductions, `iid(dist, n)`, `ifelse(cond, a, b)`.
- `~` for random variables, `=` for deterministic transforms. `#` for plain comments, `%` / `%%%` for doc-comments.
- Constrain support with `elementof(...)` or `truncate(...)` (wrap in `normalize(...)`
  for a proper prior).
- Assemble posteriors with the measure pipeline: `lawof` / `kernelof` / `likelihoodof`
  / `bayesupdate` / `restrict`.
- Prefer stochastic nodes (`x ~ Dist(...)`) over measure-composition operators; justify
  the latter if you must use them.
- Copy the shape of a worked example from the spec, and verify every construct first.
  Token names above are illustrative shape, not a guarantee of current spelling.

Full guidance (read the relevant one in full before working):
- `.claude/skills/flatppl-docs/SKILL.md` — answer language questions, or explain a model
- `.claude/skills/flatppl-model/SKILL.md` — write / review / fix / troubleshoot a `.flatppl` model
- `.claude/skills/flatppl-learn/SKILL.md` — teach a newcomer the language with a guided curriculum
- `AGENTS.md` — catch-all entry point
