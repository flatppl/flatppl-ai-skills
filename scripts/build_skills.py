#!/usr/bin/env python3
"""Build the dist/*.skill bundles from .claude/skills/<name>/.

Bundles are deterministic — fixed entry timestamps and ordering — so a rebuild on
unchanged sources is byte-identical, which lets CI verify dist/ is up to date with a
plain `git diff`. Mirrors skill-creator's package_skill exclusion rules.
"""
import fnmatch
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".claude" / "skills"
DIST = ROOT / "dist"
SKILLS = ["flatppl-docs", "flatppl-model", "flatppl-learn"]

EXCLUDE_DIRS = {"__pycache__", "node_modules"}
EXCLUDE_GLOBS = {"*.pyc"}
EXCLUDE_FILES = {".DS_Store"}
ROOT_EXCLUDE_DIRS = {"evals"}
FIXED_DATE = (1980, 1, 1, 0, 0, 0)  # ZIP epoch — keeps rebuilds reproducible


def excluded(rel: Path) -> bool:
    parts = rel.parts
    if any(p in EXCLUDE_DIRS for p in parts):
        return True
    if len(parts) > 1 and parts[1] in ROOT_EXCLUDE_DIRS:
        return True
    if rel.name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(rel.name, g) for g in EXCLUDE_GLOBS)


def build(name: str) -> Path:
    skill_path = SKILLS_DIR / name
    out = DIST / f"{name}.skill"
    files = sorted(f for f in skill_path.rglob("*") if f.is_file())
    # ZIP_STORED (no compression) keeps the output byte-identical across environments;
    # DEFLATE bytes vary with the zlib version, which would break the CI diff check.
    with zipfile.ZipFile(out, "w", zipfile.ZIP_STORED) as zf:
        for f in files:
            rel = f.relative_to(skill_path.parent)
            if excluded(rel):
                continue
            info = zipfile.ZipInfo(str(rel), date_time=FIXED_DATE)
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o644 << 16
            zf.writestr(info, f.read_bytes())
    return out


def main() -> None:
    DIST.mkdir(exist_ok=True)
    for name in SKILLS:
        out = build(name)
        print(f"built {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
