#!/usr/bin/env python3
"""Structural lint for the FlatPPL skills plugin and marketplace.

Stdlib only, offline — no Claude Code CLI required. Verifies the manifests parse and
carry their required fields, that plugin sources and the skills directory resolve, and
that every SKILL.md has frontmatter whose `name` matches its directory.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def load_json(rel: str):
    path = ROOT / rel
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        err(f"{rel} not found")
    except json.JSONDecodeError as e:
        err(f"{rel} is not valid JSON: {e}")
    return None


def frontmatter(path: Path) -> dict:
    lines = path.read_text().splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm


# marketplace.json
mp = load_json(".claude-plugin/marketplace.json")
if mp is not None:
    for key in ("name", "owner", "plugins"):
        if key not in mp:
            err(f"marketplace.json missing '{key}'")
    if isinstance(mp.get("owner"), dict) and "name" not in mp["owner"]:
        err("marketplace.json owner.name missing")
    for entry in mp.get("plugins", []):
        for key in ("name", "source"):
            if key not in entry:
                err(f"marketplace.json plugin entry missing '{key}'")
        src = entry.get("source")
        if isinstance(src, str) and src.startswith("./") and not (ROOT / src).exists():
            err(f"marketplace.json plugin source path does not resolve: {src}")

# plugin.json
pj = load_json(".claude-plugin/plugin.json")
if pj is not None and "name" not in pj:
    err("plugin.json missing 'name'")
if pj is not None and isinstance(pj.get("skills"), str):
    skills_path = ROOT / pj["skills"].removeprefix("./")
    if not skills_path.is_dir():
        err(f"plugin.json skills path does not resolve: {pj['skills']}")

# SKILL.md frontmatter
skills_root = ROOT / ".claude" / "skills"
skill_dirs = sorted(
    d for d in skills_root.iterdir() if d.is_dir() and (d / "SKILL.md").exists()
) if skills_root.is_dir() else []
if not skill_dirs:
    err("no skills found under .claude/skills/")
for d in skill_dirs:
    fm = frontmatter(d / "SKILL.md")
    name = fm.get("name")
    if not name:
        err(f"{d.name}/SKILL.md missing frontmatter 'name'")
    elif name != d.name:
        err(f"{d.name}/SKILL.md frontmatter name '{name}' != directory '{d.name}'")
    if not fm.get("description"):
        err(f"{d.name}/SKILL.md missing frontmatter 'description'")

if errors:
    print("LINT FAILED:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(f"lint OK: {len(skill_dirs)} skills, {len(mp.get('plugins', [])) if mp else 0} plugin(s)")
