# `flatppl-ai-skills` — Shared AI skills for the FlatPPL ecosystem

The canonical, version-controlled [Claude](https://claude.com/claude-code)
skills for working across the FlatPPL ecosystem — the language design
(`flatppl-design`), reference implementations (`flatppl-js`, `flatppl-rust`,
`FlatPPL.jl`, `flatppl-python`, …), grammars (`flatppl-grammars`), and examples
(`flatppl-examples`).

Keeping the skills in their own repo means a contributor can `git pull` this one
and get the current set without touching any implementation tree, and the skills
don't risk diverging from history or being confused with source.

## Layout

```
skills/<skill-name>/SKILL.md   <- one skill per directory
references/<name>.md           <- doctrine shared between skills
scripts/                       <- workspace-wiring automation
```

### Skills

All auto-triggering; each routes to the normative spec rather than embedding it:

- `flatppl-docs` — answer language questions from `flatppl-design/docs/`
- `flatppl-author` — write / review `.flatppl` models
- `flatppl-doc-review` — review a change to the normative spec docs
- `flatppl-spec-review` — review a downstream plan/ADR that cites the spec
- `flatppl-conformance-audit` — audit an engine/examples/grammar vs the spec
- `flatppl-engine-debug` — diagnose one wrong/divergent/crashing engine result
- `flatppl-grammar-change` — edit/verify a `flatppl-grammars` change
- `references/fan-out-and-tiering.md` — shared fan-out + model-tiering doctrine

**File-naming convention:** one skill per directory at
`skills/<skill-name>/SKILL.md`, where `<skill-name>` is kebab-case and carries
the `flatppl-` prefix for ecosystem skills (e.g. `flatppl-docs`,
`flatppl-engine-debug`). Doctrine shared between skills lives in
`references/<name>.md` (kebab-case, no prefix). Add a skill to the list above in
the same commit that introduces it.

## Setup

`claude` is normally run from the **workspace root** (the parent dir that holds
this repo alongside `flatppl-design/`, `flatppl-js/`, …), and it discovers skills
from the working directory's `.claude/`, not from sibling repos. So the skills
are **symlinked up** into `<workspace>/.claude/`:

```
<workspace>/.claude/skills      -> ../flatppl-ai-skills/skills
<workspace>/.claude/references  -> ../flatppl-ai-skills/references
```

**Prerequisite:** clone this repo *into your workspace root*, as a sibling of
the other FlatPPL repos (`flatppl-design/`, `flatppl-js/`, …) — the script
derives the workspace from this repo's parent directory, so a standalone clone
elsewhere will link `.claude/` into the wrong place. The script uses whatever the
clone directory is actually called (it builds the target from the clone's
basename, `../<clone-dir>/…`), so the links resolve even if you renamed it.

```
<workspace>/
├── flatppl-design/
├── flatppl-js/
├── flatppl-ai-skills/   <- this repo
└── …
```

**Run once after cloning:**

```
flatppl-ai-skills/scripts/setup-claude-symlinks.sh
```

It creates those two symlinks and does nothing else. **It is non-destructive by
contract:** it only ever creates a link in an *empty* slot. It never deletes,
overwrites, or repoints anything — not a real file/dir, not an existing symlink
(even one pointing elsewhere). Any occupied slot is reported loudly and the
script exits non-zero, leaving your filesystem untouched; to repoint a link,
remove it yourself and re-run. The script is idempotent — a re-run where the
links are already correct is a no-op. New skills added inside the already-linked
`skills` / `references` directories appear with no re-run. **Linking is always a
manual step**: nothing re-links automatically on checkout or pull (git
deliberately won't run repo code at clone/checkout time), so re-run the script
yourself after a pull if the top-level links were removed.

**What this changes in your clone (security posture):** nothing beyond two
symlinks. The script creates `<workspace>/.claude/{skills,references}` (only when
those slots are empty) and runs no network, build, or install steps, sets no git
config, and installs no hooks. To opt back out, delete the
`<workspace>/.claude/{skills,references}` symlinks.

Notes:
- The skills reference sibling repos and the shared doctrine by
  **workspace-root-relative** paths (`flatppl-design/docs/`, `flatppl-js/…`, and
  `.claude/references/fan-out-and-tiering.md` — the symlinked runtime location,
  not this repo's `references/`). Run `claude` from the workspace root; from a
  standalone checkout those paths won't resolve and the skills will say so rather
  than guess.
- A few skills point at external/global skills (`diagnose`,
  `agent-teams:parallel-debugging`, `/review`); if a contributor doesn't have
  those installed the reference is just a no-op pointer.

## License

MIT — see [`LICENSE`](LICENSE). AI-assistance policy: [`AI_POLICY.md`](AI_POLICY.md).
