# Fan-out & model-tiering doctrine (shared by the FlatPPL review/audit skills)

Referenced by `flatppl-conformance-audit`, `flatppl-engine-debug`,
`flatppl-spec-review`, and the `flatppl-doc-review` skill. Each of those keeps its own
*trigger* for when fan-out applies; this file holds the rules they share. Read it when a
skill points you here.

## 1. Default is inline. The connective reasoning never leaves the thread.

Most reviews/audits/debugs are a *continuous, whole-picture* judgment — does this cohere,
which hypothesis does the evidence back, which side of a conflict is wrong. That judgment
lives in one head; fragmenting it loses the thing it measures. So **the synthesis, the
arbitration, and the fix-direction call always stay inline.** Don't fan out to look busy
— continuity is usually what cracks the problem.

## 2. Fan out only when scope is genuinely wide AND the work is genuinely independent.

Each skill states its own concrete trigger (a large multi-file diff; ≥2 competing
root-cause hypotheses; many independent audit targets). The common test: the parallel
units must not depend on each other's intermediate results. Token-heavy **Workflow**
fan-out is **opt-in** — spawn it only on explicit user go (the Workflow opt-in rule). A
handful of items → run inline; lightweight `agent()` spawns for clearly independent
sub-work are fine without ceremony.

## 3. What parallelises vs what stays inline.

- **Parallelises:** independent evidence-gathering — per-claim correctness checks,
  per-hypothesis `file:line` evidence, per-target conformance checks. Each agent returns
  a *verdict + confidence*, not a fix.
- **Stays inline:** the minimise/scoping step, cross-item synthesis, arbitration (which
  finding/hypothesis the evidence backs), and the fix + regression decision.

## 4. Tier the model to the reasoning (fit, not "save tokens").

`agent(prompt, { model })` — omitting `model` inherits the session model (usually Opus).
Tier so Opus is spent only where the judgment needs it:

- **`haiku`** — existence / presence checks (is the op implemented? is the keyword
  wired?), pure grep-level.
- **`sonnet`** — code-tracing / cross-referencing (is a guard reachable, is a ref
  threaded, does a cited section say what's claimed) where the underlying rule is simple.
- **`opus`** — semantics reasoning (does the density actually marginalize; is the
  change-of-variables / disintegration route correct; does a claim match the spec's
  *meaning*) where judging needs real probability/measure reasoning.

**Framing:** this lowers **$-cost** (cheaper models price well below Opus), **not token
count** — a weaker model may take more tool iterations, so tokens stay roughly flat.
Don't claim a token/efficiency cut. On reasoning-heavy surfaces (measure-algebra) most
targets still need Opus, so the saving is modest; tiering pays off on mechanical surfaces
(existence sweeps, syntax/grammar). It's model-fit.

## 5. The asymmetry that sets the floor.

A too-weak **finder** causes a **false negative** — a real problem is never surfaced, and
nothing downstream recovers it. That is the worst outcome. So **tier finders UP when
unsure.** A too-weak **verifier** only causes a false positive, which the human (or a
later pass) catches. Therefore: default the finder conservatively; the **adversarial
verifier floor is `sonnet`, never `haiku`** — refutation reasoning is what kills
plausible-but-wrong over-claims.
