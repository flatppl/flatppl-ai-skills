# FlatPPL model troubleshooting catalog

Symptom → likely cause → where to confirm in the spec. Read this **only when diagnosing a
failing model**. Reproduce the exact failure first; FlatPPL is new, so confirm every fix
against the spec rather than guessing.

| Symptom | Likely cause | Where to check |
|---|---|---|
| Parser/syntax error, or "not a statement" | An excluded construct — `for`, `if`/`else`, `while`, mutation, an explicit loop | "Syntax" → supported/excluded constructs. Vectorize with broadcasting/reductions/`iid`; branch with `ifelse`. |
| "unknown name" / "not defined" for a function | Not a core builtin, or it lives in a standard module that isn't loaded | "Functions and deterministic operations" **and** "Standard modules"; `load_module` the module. Grep both before concluding it's absent. |
| Wrong arity / argument-type error | The construct exists but its signature differs from what was assumed | Grep the construct in its section for the exact signature. (This is why the construct index is recall-only, not authoritative.) |
| Improper prior / infinite mass / density won't integrate | Unconstrained support, or a truncated distribution not renormalized | Constrain with `elementof`/`truncate`; wrap a truncated prior in `normalize(...)`. "Measure algebra" → support restriction, normalization. |
| NaN / Inf density | Parameter outside the distribution's support (e.g. negative scale), log of a nonpositive value, or a degenerate transform | Check the variate's domain (`elementof`) and the distribution's support in "Distributions". |
| Data ignored / posterior conditions on the wrong thing | `restrict`/`likelihoodof` names a variate that isn't the observed one, or `_data` wired to the wrong node | "Likelihoods and posteriors"; confirm the observed variate name matches the kernel/law. |
| Result shapes wrong / silent mis-broadcast | A broadcast aligning axes differently than intended | "Syntax"/"Language design" → broadcasting, reductions; check axis alignment, prefer explicit axis names. |
| A transform behaves as random (or a variate as fixed) | `~` vs `=` mixup | `~` = stochastic node, `=` = deterministic transform. |
| Review flags an unjustified `joint`/`kchain`/`pushfwd`/`weighted` | Measure-composition used where stochastic nodes suffice | Rewrite as `~`/`draw` nodes unless the model genuinely needs composition (then justify). |

If the number itself is suspect but the model is correct — two engines disagree, or a
density is wrong versus an independent hand calculation — that is an **engine** bug, not a
model fix. Say so; it is out of scope for modeling.
