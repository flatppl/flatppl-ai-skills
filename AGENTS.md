# AGENTS.md — `flatppl-ai-skills`

Orientation for AI coding agents (and humans) working **in this repo**. This
repo holds the canonical Claude skills for the FlatPPL ecosystem; `README.md` is
the source of truth for the layout and the one-time symlink bootstrap. Read it
first.

## What lives here

- `skills/<kebab-name>/SKILL.md` — one skill per directory, auto-triggering,
  `flatppl-` prefix for ecosystem skills.
- `references/<name>.md` — doctrine shared between skills (kebab-case, no prefix).
- `scripts/` — workspace-wiring automation (`setup-claude-symlinks.sh`).

These are the **canonical** copies. They are *consumed* from a workspace-root
`.claude/` symlink, not edited there — always edit them here.

## Adding or changing a skill / reference / script

- **New skill** → `skills/<kebab-name>/SKILL.md` with the `flatppl-` prefix for
  ecosystem skills; shared doctrine goes in `references/<name>.md`. Add it to the
  README "Skills" list in the same commit.
- **Route, don't embed.** Skills cite the normative spec (`flatppl-design/docs/`)
  and shared doctrine (`.claude/references/…`) by **workspace-root-relative**
  path; they don't copy spec text in. Keep new skills self-routing the same way.
- **Workspace-relative paths only.** Skills and scripts reference sibling repos
  and the shared references by paths relative to the workspace root (where
  `claude` runs), never absolute ones. The runtime path for a reference is
  `.claude/references/<name>.md` (the symlink), not this repo's `references/`.
- **New script** → keep it dependency-light and idempotent (safe to re-run);
  register it in the README "Layout" in the same commit.
- **No clone-time execution.** Git won't — and shouldn't — run repo code at
  clone/checkout. Don't add a tool that *requires* an auto-run hook to work;
  bootstrap stays a manual, documented one-shot the user runs.
- **No posture changes for every contributor.** Never bundle lifecycle hooks,
  permission allowlists, or git-config side-effects into tooling that runs on
  pull. The symlink script's non-destructive contract (creates only in empty
  slots; never deletes/overwrites/repoints) is load-bearing — preserve it.

## Commit conventions

One topic per commit. Match the repo's existing subject style (capitalized
subject, optional `area:` prefix — e.g. `Add flatppl-foo skill`,
`scripts: harden symlink guard`). Commit messages and PR descriptions stand on
their own — no references to a chat session. No AI self-attribution in commits.
