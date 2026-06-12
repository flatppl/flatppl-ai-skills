# Gaining confidence in a model without an engine

There is **no FlatPPL engine** you can run a `.flatppl` file through today, so you cannot
execute the model and inspect its output. Spec-grounding proves a model is *free of spec
violations*; it does **not** prove the model computes the density you intended. These two
are different, and parameterization and shape mistakes live in the gap between them.

Climb this ladder. Each rung is independent of FlatPPL execution; each is stronger than
the last. Do the cheap ones always; reach for the numerical oracle when the model is
non-trivial or the stakes are real. **Report which rungs you climbed** — "I built a
4-point SciPy oracle and it matched" is evidence; "it looks right" is not.

## 1. Generative dry-run by hand

Read top to bottom as a sampler:
- For each `~` node, ask: *can I actually draw from the right-hand side?* The RHS must be
  a **probability (normalized) measure**. A bare `truncate(...)`, `weighted(...)`,
  `superpose(...)`, or any sub-measure is **not** drawable — that is a bug (`~` requires a
  normalized measure; wrap in `normalize(...)`).
- For each `=` node, ask: *can I compute this from values I already have?* An unresolved
  reference, or a node declared but never used downstream, signals the model doesn't say
  what you mean.

## 2. Shape & cardinality ledger

Write down every node's shape (scalar, length-N, N×K…). At **each likelihood**, the
variate shape must equal the observed-data shape — **FlatPPL does not insert implicit IID
products** ("Likelihoods and posteriors" → multiple observations). A scalar variate scored
against length-N data is a bug: use `iid(dist, N)` or broadcast over length-N parameters
(as eight-schools broadcasts `Normal.(theta, std_errs_data)` only because both are
length-J).

## 3. Support & normalization audit

For every prior:
- Is its support the parameter's declared domain (`elementof`)? A scale on `reals` instead
  of `posreals` admits negative values.
- Is every truncated/restricted measure wrapped in `normalize(...)`? An unnormalized
  truncation is a sub-probability measure.
- Does it integrate to 1 over that support? An accidentally improper/flat prior won't.

## 4. Parameterization round-trip (highest value for a statistics user)

For each distribution, write **two** densities side by side: the one you *intend* (in the
parameterization you know from Stan/PyMC/textbooks) and the one FlatPPL's call *denotes*
(arg names and order from `08-distributions.md`). Confirm they are the same function.
This is where silent errors hide:
- `Normal(mu, sigma)` — second arg is the **standard deviation**, not the variance.
- `Exponential(rate)` — single arg is the **rate** (1/mean), not the scale/mean.
- `Gamma(shape, rate)` — shape-rate. A mean/SD spec (`pm.Gamma(mu, sigma)`) must be
  converted: shape = mu²/sigma², rate = mu/sigma².
- `InverseGamma(shape, scale)` — its `scale` plays the numerical role of `Gamma`'s rate.
- `StudentT(nu)` — degrees of freedom **only**, standard (zero mean, unit scale). A
  location-scale Student-t is `locscale(StudentT(nu), shift, scale)` /
  `pushfwd(fn(mu + sigma * _), StudentT(nu))`.
- `Cauchy(location, scale)` — a Breit-Wigner *width* is `2 * scale`.

Always confirm names/order against `08-distributions.md`; the list above is a reminder of
the *kind* of trap, not a substitute for checking.

## 5. Independent numerical oracle (strongest — gives positive evidence)

Pick a tiny dataset (3–5 points) and compute the model's (log-)density or posterior by a
route that **does not involve FlatPPL**. In order of preference:

- **Closed form, by hand** — the first choice, needs no tools. When the model is conjugate
  (Normal–Normal mean, Gamma–Poisson rate, Beta–Bernoulli, Normal-variance with
  InverseGamma), write the analytic posterior and confirm it's what the model should
  produce.
- **Reimplement the intended density in a numerical stack already available** in your
  environment (SciPy/NumPy, R, or PyMC/Stan's `logp`). You can't run the `.flatppl` file,
  but you *can* run the density it is supposed to denote; a disagreement between "what I
  meant" and "what I wrote" shows up as a number, catching the parameterization (rung 4)
  and shape (rung 2) errors that reading cannot. Keep any code light: a few lines, a couple
  of evaluation points — **not** a full inference run.
- **No stack present? Offer a throwaway venv — opt-in, isolated, leave-no-trace.** These
  skills ship no runtime, so never install silently.

  > **HARD RULE — NEVER install ANYTHING into a global, system, shared, or pre-existing
  > environment.** No global/`--user`/`sudo` `pip install`; never touch the system Python,
  > the user's base interpreter, or any existing project env; no global `npm -g` or `conda`
  > into a shared env. Every install goes ONLY into a fresh, self-created, **isolated**
  > venv that you delete afterward. If you cannot create an isolated venv, do **not**
  > install — stop at the hand calculation. There is no exception to this.

  Protocol:

  1. **Ask first.** Only when a numerical check would *materially* raise confidence (a
     non-trivial model, real stakes) — for a clean conjugate model the hand calculation is
     enough. Ask plainly: *"A quick numerical check would confirm this, but you have no
     numerical stack handy. OK if I spin up an isolated throwaway Python venv, run a small
     check, and delete it afterward?"* Proceed **only on an explicit yes**.
  2. **Isolated, ephemeral, minimal, quiet** — respect the user's tokens and machine. The
     environment is created by you in a **system temp dir, never in the repo and never the
     user's existing env**; install only what the oracle needs (often just `numpy`; add
     `scipy` only for a distribution's `logpdf`); keep output quiet (`-q`) and **do not
     paste install logs into the conversation** — report only the oracle's numeric result.

     **Assume nothing about the user's setup: default to stdlib `venv`** — it ships with
     Python, so it works anywhere Python does. Reach for `uv` or `pixi` instead **only if
     the user already has them** (faster resolve/cache; no reason to expect them). In every
     case the env lives **inside `$SCRATCH`** so one `rm -rf` removes it. Always invoke the
     env's own `python`/`pip` (never a bare `pip install`, which could hit a global env):
     ```sh
     SCRATCH=$(mktemp -d)

     # stdlib venv — the default; assumes only Python
     python3 -m venv "$SCRATCH/venv" \
       && "$SCRATCH/venv/bin/pip" install -q numpy scipy \
       && "$SCRATCH/venv/bin/python" "$SCRATCH/oracle.py"

     # uv (only if the user already has it) — venv inside $SCRATCH, uv's own pip
     uv venv -q "$SCRATCH/venv" && uv pip install -q --python "$SCRATCH/venv/bin/python" \
       numpy scipy && "$SCRATCH/venv/bin/python" "$SCRATCH/oracle.py"

     # pixi (only if the user already has it) — project + env both inside $SCRATCH
     pixi init -q "$SCRATCH" && (cd "$SCRATCH" && pixi add -q numpy scipy \
       && pixi run -q python oracle.py)
     ```
     (Use **one** of the three — the stdlib `venv` unless the user already has uv/pixi. uv
     and pixi keep their package downloads in their own global cache, which is harmless and
     not the user's env; the *environment* itself stays in `$SCRATCH`.)
  3. **Confirm, then tear down.** When the result is in and the user's question looks
     answered, **prompt** them: *"Did that resolve it? I'll remove the venv."* On
     confirmation, delete the whole scratch dir so nothing is left behind:
     ```sh
     rm -rf "$SCRATCH"        # your own temp scratch, outside the repo — leave no trace
     ```
     (It is your own throwaway artifact in a temp location, not the user's data, so a real
     delete is correct here — no venv, no `pip` cache, no stray `oracle.py` left over.)

If nothing trusted is at hand and the user declines a venv, stop at the closed-form/hand
calculation; it is still positive evidence.

Example oracle skeleton (Normal likelihood, checking sd-vs-variance and the IID shape at
once) — for an already-present stack, or as the `oracle.py` inside an opt-in venv:

```python
import numpy as np
from scipy import stats
y = np.array([2.1, 1.8, 2.5, 2.0, 2.3])
mu, sigma = 2.0, 0.4          # a parameter point; sigma is the SD the model must use
# the density the FlatPPL model is SUPPOSED to denote:
logp = stats.norm.logpdf(y, loc=mu, scale=sigma).sum()   # .sum() == the iid product
print(logp)
# if the .flatppl passed a VARIANCE as the 2nd Normal arg, the intended value here
# (with the correct SD) is what the model should match — the mismatch is the bug.
```

## 6. Structural diff against the closest worked example

Diff the model construct-by-construct against the nearest model in the spec's **Worked
examples** section (read whichever models it actually contains — don't assume a specific
one exists). Confirm only the intended things differ. This is necessary but **not**
sufficient — it catches divergence from a known-good shape, not a wrong parameterization
shared with the example.

## What a clean parse does and does not prove

If a FlatPPL parser/grammar is available, a clean parse (no error nodes) confirms only
that the text is **syntactically** well-formed. It says nothing about parameterization,
support, shape, or whether the model means what you intend. Never report a parse as
correctness.
