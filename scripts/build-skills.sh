#!/usr/bin/env bash
# Rebuild the dist/*.skill bundles from .claude/skills/.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_skills.py
