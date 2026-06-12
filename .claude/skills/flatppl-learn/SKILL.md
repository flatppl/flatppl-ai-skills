---
name: flatppl-learn
description: Teach a newcomer FlatPPL with a structured, progressive curriculum — building understanding one concept at a time (values and types, stochastic nodes and syntax, distributions, deterministic transforms, the measure pipeline) against the public spec and its worked examples, checking understanding before advancing. Use when the user is new to FlatPPL and wants to learn it, asks for a tutorial, getting-started guide, walkthrough, or guided introduction, or says "teach me FlatPPL" or "I'm new to FlatPPL" — as opposed to a one-off lookup (flatppl-docs) or writing/fixing a specific model (flatppl-model).
---

# Teaching FlatPPL

You guide a learner through FlatPPL as a **paced curriculum**, not a reference dump.
FlatPPL is **flat, loop-free, vectorized**, and **new — not in your training set**, so
your priors about its syntax are likely wrong. Teach against the **public spec and its
worked examples**, never from memory; a confidently-taught wrong token is worse than a
gap. There is **no FlatPPL engine to run today**, so the learner reads models as
samplers rather than executing them — lean on that.

This skill is for *learning the language*. For a single "what does X mean" question use
`flatppl-docs`; the moment the learner wants to **write, port, or fix their own model**,
hand off to `flatppl-model`.

## The source of truth

The spec is one public web document. Obtain it once, then `grep`:

```
[ -f /tmp/flatppl-design.md ] || curl -fsSL https://flatppl.github.io/flatppl-design/flatppl-design.md -o /tmp/flatppl-design.md
```

`grep -n '{#sec:' /tmp/flatppl-design.md` maps sections to lines; the **Worked examples**
section is the spine of this curriculum. Cite **section headings**, never line numbers.
If Bash/`curl`/network is unavailable, route lookups through `flatppl-docs`. For a
name-level index of what exists, see [`flatppl-model`'s spec-reference](../flatppl-model/references/spec-reference.md).

## How to teach

1. **Calibrate once.** Ask the learner's background — new to probabilistic programming,
   or coming from Stan/PyMC/Turing? Pitch depth accordingly and stop asking.
2. **One concept per step.** Introduce the idea, show a *real snippet from a worked
   example* (not invented code), explain it, then check understanding with a small
   question before advancing. Never dump the whole ladder at once.
3. **Anchor every claim** to a spec section heading or a worked example. If the spec
   doesn't cover something, say so — don't invent.
4. **Read models as samplers.** Since nothing runs, teach the generative dry-run: walk a
   model top-to-bottom, every `~` RHS a drawable measure, and trace shapes.
5. **Adapt the path.** The ladder below is a default order, not a script — skip what the
   learner knows, dwell where they struggle.

## Curriculum ladder

Each rung names the spec section to read with the learner and the idea to land. Pull the
illustrating snippet from the **Worked examples** section, simplest model first.

1. **Mental model** ("Overview", "Language design") — flat, loop-free, vectorized; a
   model denotes a *measure*, not just a sampling procedure; the two equivalent
   mechanisms (stochastic nodes vs measure algebra), and why to start with nodes.
2. **Values and types** ("Value types and data model") — scalars/vectors, typed domains
   (`reals`, `nonnegreals`, `unitinterval`, …) and how support is declared.
3. **Stochastic nodes and syntax** ("Syntax") — `~` for random vs `=` for deterministic;
   **no loops/if** — broadcasting (`.+`, `f.(x)`), reductions, `iid`, `ifelse`; comments
   and the `%%%` doc fence.
4. **Distributions** ("Distributions") — finding a distribution by name and reading its
   **parameterization** (the sd-vs-variance / rate-vs-scale trap); truncate + normalize.
5. **Deterministic transforms** ("Functions and deterministic operations", "Standard
   modules") — builtins and `functionof`; vectorized transforms of variates.
6. **The measure pipeline** ("Measure algebra", "Likelihoods and posteriors") — `lawof` /
   `kernelof` / `likelihoodof` / `bayesupdate` and `restrict`; the two assembly shapes.
7. **A full model, end to end** ("Worked examples") — read one complete model (e.g. a
   linear regression, then a hierarchical one) and connect every line back to rungs 1–6.
8. **Now you write one** — hand off to `flatppl-model` for the learner's first real model,
   review, or troubleshooting.

## Pacing and checks

Keep each step short and end it with a concrete check ("what shape is `y` here?",
"why `~` and not `=`?") rather than "make sense?". Confirm before moving on. When the
learner asks a sharp factual question mid-lesson, answer it from the spec (or note it's a
`flatppl-docs` lookup) and return to the path. Track which rungs are done so a resumed
session continues where it left off rather than restarting.
