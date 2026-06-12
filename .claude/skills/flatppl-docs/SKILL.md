---
name: flatppl-docs
description: Answer any question about the FlatPPL probabilistic language — its syntax, value types, measure algebra, distributions, built-in functions, likelihoods/posteriors, FlatPIR, or profiles — and explain what a given .flatppl model does, by consulting the public FlatPPL design spec on the web. Use whenever the user asks how FlatPPL does something, what a FlatPPL construct means, whether FlatPPL supports a feature, or wants a read-only explanation of an existing FlatPPL model, even if they don't name the docs or say "FlatPPL".
---

# Answering FlatPPL questions from the spec

You answer questions about FlatPPL using its **public design spec**, a single web
document:

```
https://flatppl.github.io/flatppl-design/flatppl-design.md
```

FlatPPL is new and **not in your training set**; your priors about it are likely
wrong, so answer from the spec, never from memory.

This skill is **read-only**: it explains the language, answers whether FlatPPL supports
something, and explains what an existing `.flatppl` model does. To **write, review, fix,
or troubleshoot a `.flatppl` model** — even when phrased "how do I write X in flatppl" —
use `flatppl-model` instead.

## How to read the spec: download once, then grep

The specification is a single document of roughly 40,000 words. **Strongly prefer
downloading it once to a session-local file and reading it with `grep`/`Read`**: this
yields exact verbatim text across the whole document with no truncation, plus fast repeat
lookups. It is preferable to per-topic fetching for fidelity, completeness, and cost.

1. **Download once — the file is your cache.** Run, guarded on existence so a whole
   session downloads at most once:
   ```
   [ -f /tmp/flatppl-design.md ] || curl -fsSL https://flatppl.github.io/flatppl-design/flatppl-design.md -o /tmp/flatppl-design.md
   ```
   If the file already exists, the command is a no-op — **never re-download a file that
   is already present.** The local copy is a fixed, version-pinned document; treat it as
   authoritative for the session.
2. **Find the region.** Map sections to line numbers with
   `grep -n '{#sec:' /tmp/flatppl-design.md` (use the index below to choose), or jump
   straight to a construct with `grep -n 'pushfwd' /tmp/flatppl-design.md` (operator
   names, `elementof`, `kernelof`, etc. are unique anchors).
3. **Read the exact region** with `Read` over that line range, or `grep -n -A30` to pull
   surrounding lines. Quote verbatim.
4. **Answer, grounded.** Cite the **section heading** and its `{#sec:...}` anchor
   (e.g. "Value types and data model" `{#sec:valuetypes}`). Quote the exact spec
   sentence for each non-obvious claim. If two keyword greps find nothing, the spec
   **doesn't cover it** — say so plainly; never fill from prior knowledge.

**Grounding contract — applies to every answer.** Hard rules, not advice. They exist
because a plausible-sounding answer that wasn't pulled from the file is the main failure
mode here:
- **Anchors come from grep, never from memory.** Only cite a `{#sec:...}` anchor you have
  actually seen in `grep -n '{#sec:' /tmp/flatppl-design.md` output. If you did not grep
  it, you do not have it — do not write it. A made-up anchor that *looks* right (e.g.
  inventing `{#sec:negbinomial2}` for a distribution) is a fabrication.
- **Quotes are verbatim.** Copy the spec sentence out of the file; never paraphrase into
  quotation marks.
- **Never present FlatPPL code you did not copy from the spec as grounded.** If you must
  show illustrative syntax, label it "illustrative — not quoted from the spec." An example
  that sounds right but isn't in the file is a fabrication even when the surrounding
  section citation is real.

**Fallback — no shell or no network.** If Bash, `curl`, or outbound network is
unavailable (some sandboxed surfaces), use `WebFetch` on the URL with a **narrow,
single-topic prompt** naming the target section: *"In the '<Section>' section, what does
FlatPPL say about <construct>? Quote the exact defining sentences and give the heading
and its `{#sec:...}` anchor."* If the answer is empty or truncated, re-fetch with a
unique keyword; `WebFetch` caches the URL ~15 min. The whole-doc `WebFetch` truncates
before later sections, so always name a section and prefer keyword anchors.

## Explaining an existing model

When the user hands you a `.flatppl` file or asks "what does this model do", narrate it —
don't edit it. Read top to bottom and explain in plain terms:

1. **The generative story.** Which variates are priors (`~` on a distribution, no data),
   how deterministic nodes (`=`) transform them, and where data enters.
2. **Each construct, grounded.** For any builtin/distribution/operator you're unsure of,
   `grep` it in the spec rather than guessing — the whole point of explaining is accuracy,
   and your priors about FlatPPL are unreliable. Cite the section.
3. **The measure pipeline.** Identify the final assembly (`lawof` / `kernelof` /
   `likelihoodof` / `bayesupdate` / `restrict`) and say what posterior it builds and what
   it conditions on.
4. **Inferred vs observed.** Name the latent parameters and the observed data (often a
   `_data` suffix), and state the question the model answers.

Stay read-only. If the user then wants the model written, changed, fixed, or its validity
checked, that is `flatppl-model`.

## Spec reference (load on demand)

The full section index, the indirect-question routing map, and a construct index — what
distributions, sets, functions, and measure operators exist, and where to grep for their
signatures — live in [`references/spec-reference.md`](references/spec-reference.md). Read
it **only when** you need to route to a section or recall what a construct is; it is not
loaded by default, so it costs nothing until you open it. The downloaded spec is still the
source of truth — confirm signatures there.
