#!/usr/bin/env python3
"""Detect drift between the live FlatPPL spec and references/spec-reference.md.

The spec-reference is a recall aid; the published specification is authoritative. As the
spec evolves, the bundled construct index can fall behind silently. This script fetches
the spec and checks the reference's enumerated construct lists against it, exiting nonzero
on drift so the scheduled CI run flags it for a human to reconcile.

Two kinds of check, by what each list affords:

- Distributions are a self-contained, cleanly enumerable roster, so they are checked
  *bidirectionally* within the spec's distributions section: a name the spec added but the
  reference lacks, or one the reference carries that the spec dropped, both count as drift.

- Measure operators, predefined value sets, and standard modules are enumerated in the
  reference but are scattered through the spec's prose (and often written with arguments,
  e.g. `truncate(...)`), so a bidirectional check would be noisy. They are checked by
  *presence*: every name the reference lists must still appear in the spec. This catches
  the harmful case — the reference naming a construct that was renamed or removed — without
  false positives. New names the spec adds are not flagged here (an incomplete index still
  routes correctly; a wrong one misleads).

Functions are organized by category in the spec and listed non-exhaustively in the
reference by design, so they are not checked.
"""
import re
import sys
import urllib.request
from pathlib import Path

SPEC_URL = "https://flatppl.github.io/flatppl-design/flatppl-design.md"
ROOT = Path(__file__).resolve().parent.parent
REFERENCES = [
    ROOT / ".claude/skills/flatppl-docs/references/spec-reference.md",
    ROOT / ".claude/skills/flatppl-model/references/spec-reference.md",
]


def fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=60) as resp:
        return resp.read().decode("utf-8", "replace")


def ref_block(ref: str, label: str) -> str:
    """The text of a '**Label**' block in the reference, up to the next '**' line."""
    m = re.search(r"\*\*" + re.escape(label) + r"\*\*(.*?)(?=\n\*\*|\Z)", ref, re.S)
    return m.group(1) if m else ""


def spec_distributions(spec: str) -> set[str]:
    """Capitalized backticked names within the spec's distributions section."""
    start = re.search(r"\{#sec:distributions\}", spec)
    if not start:
        print("ERROR: could not locate {#sec:distributions} in the spec.", file=sys.stderr)
        sys.exit(2)
    rest = spec[start.end():]
    nxt = re.search(r"\{#sec:", rest)
    section = rest[: nxt.start()] if nxt else rest
    return set(re.findall(r"`([A-Z][A-Za-z0-9]+)`", section))


def present_in_spec(name: str, spec: str) -> bool:
    """True if `name` appears as a backticked token, bare or with arguments."""
    return re.search(r"`" + re.escape(name) + r"[`(]", spec) is not None


# (reference label, regex for the names in that block) for the presence-checked lists.
PRESENCE_LISTS = [
    ("Measure algebra & posteriors", r"`([a-z][a-z0-9]+)`"),       # lawof, truncate, …
    ("Value sets & parameter domains", r"`([a-z][a-z0-9]+)`"),     # reals, nonnegreals, …
    ("Standard modules", r"`([a-z][a-z]+(?:-[a-z]+)*)`"),          # particle-physics, …
]


def check_references_identical() -> bool:
    """The bundled spec-references must stay byte-identical across skills.

    Each skill bundle ships its own copy so it is self-contained, but the copies must not
    diverge — a fix applied to one (e.g. adding a distribution) would otherwise silently
    miss the other. Checked offline, before the network fetch. Returns True on drift.
    """
    if len({p.read_bytes() for p in REFERENCES}) > 1:
        rels = ", ".join(str(p.relative_to(ROOT)) for p in REFERENCES)
        print(f"DRIFT: the bundled spec-references differ from each other ({rels}). "
              "They must be byte-identical; sync them, then rebuild with 'pixi run build'.")
        return True
    print(f"OK: {len(REFERENCES)} spec-references are byte-identical.")
    return False


def main() -> None:
    drifted = check_references_identical()
    spec = fetch(SPEC_URL)
    spec_dists = spec_distributions(spec)
    if not spec_dists:
        print("ERROR: extracted no distribution names from the spec.", file=sys.stderr)
        sys.exit(2)

    for ref_path in REFERENCES:
        ref = ref_path.read_text()
        rel = ref_path.relative_to(ROOT)

        # Distributions — bidirectional.
        ref_dists = set(re.findall(r"`([A-Z][A-Za-z0-9]+)`", ref_block(ref, "Distributions")))
        missing = spec_dists - ref_dists
        extra = ref_dists - spec_dists
        if missing or extra:
            drifted = True
            print(f"DRIFT {rel} [distributions]:")
            if missing:
                print(f"  spec has, reference lacks: {', '.join(sorted(missing))}")
            if extra:
                print(f"  reference has, spec lacks: {', '.join(sorted(extra))}")
        else:
            print(f"OK {rel} [distributions]: {len(ref_dists)} match.")

        # Measure ops, value sets, standard modules — presence (reference ⊆ spec).
        for label, pattern in PRESENCE_LISTS:
            names = set(re.findall(pattern, ref_block(ref, label)))
            absent = sorted(n for n in names if not present_in_spec(n, spec))
            if absent:
                drifted = True
                print(f"DRIFT {rel} [{label}]: not found in spec: {', '.join(absent)}")
            else:
                print(f"OK {rel} [{label}]: {len(names)} present in spec.")

    if drifted:
        print("\nspec-reference.md is out of date with the spec. Reconcile the construct "
              "index, then rebuild the bundles with 'pixi run build'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
