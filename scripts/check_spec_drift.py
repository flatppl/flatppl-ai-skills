#!/usr/bin/env python3
"""Detect drift between the live FlatPPL spec and references/spec-reference.md.

The spec-reference is a recall aid; the published specification is authoritative. As the
spec evolves (most often by gaining distributions), the bundled index can fall behind
silently. This script fetches the spec and compares its built-in distribution roster
against the names listed in spec-reference.md, exiting nonzero on any difference so the
scheduled CI run flags it for a human to reconcile.

Distributions are checked because they are a clean, enumerable, frequently-extended list.
Other categories (functions, measure operators) are organized by category in the spec and
are intentionally listed non-exhaustively in the reference, so they are not drift-checked.
"""
import re
import sys
import urllib.request
from pathlib import Path

SPEC_URL = "https://flatppl.github.io/flatppl-design/flatppl-design.md"
ROOT = Path(__file__).resolve().parent.parent
REFERENCES = [
    ROOT / ".claude/skills/flatppl-query/references/spec-reference.md",
    ROOT / ".claude/skills/flatppl-model/references/spec-reference.md",
]


def fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=60) as resp:
        return resp.read().decode("utf-8", "replace")


def backticked_caps(text: str) -> set[str]:
    """Backtick-wrapped capitalized identifiers, e.g. `Normal`, `StudentT`."""
    return set(re.findall(r"`([A-Z][A-Za-z0-9]+)`", text))


def spec_distributions(spec: str) -> set[str]:
    """Names within the spec's distributions section (its anchor to the next anchor)."""
    start = re.search(r"\{#sec:distributions\}", spec)
    if not start:
        print("ERROR: could not locate {#sec:distributions} in the spec.", file=sys.stderr)
        sys.exit(2)
    rest = spec[start.end():]
    nxt = re.search(r"\{#sec:", rest)
    section = rest[: nxt.start()] if nxt else rest
    return backticked_caps(section)


def reference_distributions(ref: str) -> set[str]:
    """Names in the reference's '**Distributions**' block."""
    m = re.search(r"\*\*Distributions\*\*(.*?)(?=\n\*\*|\Z)", ref, re.S)
    return backticked_caps(m.group(1)) if m else set()


def main() -> None:
    spec = fetch(SPEC_URL)
    spec_names = spec_distributions(spec)
    if not spec_names:
        print("ERROR: extracted no distribution names from the spec.", file=sys.stderr)
        sys.exit(2)

    drifted = False
    for ref_path in REFERENCES:
        ref_names = reference_distributions(ref_path.read_text())
        missing = spec_names - ref_names   # in spec, absent from reference
        extra = ref_names - spec_names     # in reference, absent from spec
        rel = ref_path.relative_to(ROOT)
        if missing or extra:
            drifted = True
            print(f"DRIFT in {rel}:")
            if missing:
                print(f"  spec has, reference lacks: {', '.join(sorted(missing))}")
            if extra:
                print(f"  reference has, spec lacks: {', '.join(sorted(extra))}")
        else:
            print(f"OK {rel}: {len(ref_names)} distributions match the spec.")

    if drifted:
        print("\nspec-reference.md is out of date with the spec. Reconcile the construct "
              "index (and the .skill bundles via 'pixi run build').")
        sys.exit(1)


if __name__ == "__main__":
    main()
