# FlatPPL AI Skills

Skills that teach AI coding agents to **write**, **explain**, **troubleshoot**, and
**answer questions about**
[FlatPPL](https://flatppl.github.io/flatppl-design/flatppl-design.md) — a flat,
loop-free, vectorized probabilistic language — without re-reading the entire design
specification each session.

The repository provides three skills:

| Skill | Task |
|---|---|
| **flatppl-docs** | Read-only: answer questions about the language (syntax, value types, measure algebra, distributions, functions, likelihoods/posteriors, FlatPIR, profiles) **and explain what a given `.flatppl` model does**. |
| **flatppl-model** | Write, draft, port (Stan/PyMC/Turing), review, fix, or **troubleshoot** a `.flatppl` model. |
| **flatppl-learn** | Teach a newcomer FlatPPL with a **guided, progressive curriculum** — one concept at a time, against the spec and its worked examples. |

Both ground every claim in a single public specification document
(`https://flatppl.github.io/flatppl-design/flatppl-design.md`); no repository checkout,
filesystem layout, or local documentation is required. The agent fetches the
specification on demand and cites section headings.

## Install

### Claude Code — plugin marketplace (recommended)

This repo is a Claude Code plugin marketplace. Add it once, then install the `flatppl`
plugin (which bundles all three skills).

From the terminal:

```sh
claude plugin marketplace add flatppl/flatppl-ai-skills
claude plugin install flatppl@flatppl-ai-skills
```

Or with the equivalent slash commands inside a Claude Code session:

```
/plugin marketplace add flatppl/flatppl-ai-skills
/plugin install flatppl@flatppl-ai-skills
```

The plugin is enabled on installation and available in every project. The footprint is
minimal: only each skill's one-line description is always loaded, while the full guidance
and the specification and diagnostics references load on demand when a FlatPPL task fires.
Update later with `claude plugin update flatppl` from the terminal, or
`/plugin marketplace update` in session.

### Claude Code — copy install

Or copy the three skill folders into a single project (or `~/.claude` for all projects):

```sh
cp -R .claude/skills/flatppl-docs  /path/to/your-repo/.claude/skills/
cp -R .claude/skills/flatppl-model /path/to/your-repo/.claude/skills/
cp -R .claude/skills/flatppl-learn /path/to/your-repo/.claude/skills/
```

Either way, Claude Code loads each skill's description at session start and reads the
full `SKILL.md` when a FlatPPL task fires.

### Claude apps & API (Agent Skills)

Prebuilt `.skill` bundles live in [`dist/`](dist/) — upload them as Agent Skills to
Claude.ai, the Claude desktop app, or the Claude API:

```
dist/flatppl-docs.skill
dist/flatppl-model.skill
dist/flatppl-learn.skill
```

To rebuild a bundle after editing a skill, run
`zip -r dist/flatppl-docs.skill flatppl-docs` from inside `.claude/skills/`, or use
skill-creator's `package_skill`.

### Other agents

Copy [`AGENTS.md`](AGENTS.md) to your repo root — it is standalone (inlines the core
rules, not just pointers) and is read by **OpenAI Codex CLI, Zed, Amp, Google Jules,
Factory, and Roo Code** with no extra file. Ready-made entry-point stubs are included
for agents with their own config path; copy whichever you use:

| Agent | File |
|---|---|
| GitHub Copilot | `.github/copilot-instructions.md` |
| Cursor | `.cursor/rules/flatppl.mdc` (scoped to `*.flatppl`) |
| Gemini CLI | `GEMINI.md` |
| Aider | `CONVENTIONS.md` |

Each stub inlines the core rules and points at the three `SKILL.md` files and the spec.
The Cursor and Gemini stubs `@`/path-reference the `SKILL.md` files, so copy
`.claude/skills/` alongside them for the deep guidance to resolve.

## How it works

FlatPPL is novel and not in model training sets, so all three skills enforce one
discipline: **never answer from memory — fetch the spec, quote it, cite the section
heading.** flatppl-model adds the hard invariants (no loops/`if`, vectorize, `~` vs
`=`, support constraints, the `lawof`/`kernelof`/`likelihoodof`/`bayesupdate`/`restrict`
measure pipeline) that catch the most common modeling mistakes.

## Layout

```
flatppl-ai-skills/
├── README.md
├── AGENTS.md                              # standalone guide; read by Codex/Zed/Amp/Jules/Roo
├── GEMINI.md                              # Gemini CLI entry-point stub
├── CONVENTIONS.md                         # Aider entry-point stub
├── .github/copilot-instructions.md       # GitHub Copilot entry-point stub
├── .cursor/rules/flatppl.mdc             # Cursor entry-point stub (scoped to *.flatppl)
├── dist/                                  # prebuilt .skill bundles (Claude apps/API)
│   ├── flatppl-docs.skill
│   ├── flatppl-model.skill
│   └── flatppl-learn.skill
├── .claude-plugin/                        # Claude Code plugin marketplace
│   ├── marketplace.json                  #   catalog: the `flatppl` plugin
│   └── plugin.json                       #   plugin manifest (skills → .claude/skills/)
└── .claude/skills/
    ├── flatppl-docs/SKILL.md            # answer language questions
    ├── flatppl-model/SKILL.md           # write / review models
    └── flatppl-learn/SKILL.md           # guided curriculum for newcomers
```
