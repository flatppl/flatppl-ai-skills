#!/usr/bin/env bash
#
# Symlink this repo's Claude skills into the parent workspace so that `claude`,
# invoked from the workspace root (the FlatPPL super-repo that holds this clone
# alongside flatppl-design/, flatppl-js/, ...), discovers them.
#
# Run this ONCE after cloning. It is idempotent — re-run any time the links go
# missing (e.g. someone deleted the workspace `.claude/`). The symlinks point at
# the `skills` / `references` directories themselves, so new skills added inside
# them show up with no re-run. Git cannot run repo code at clone/checkout time —
# by design — so linking is always a manual step; nothing re-links automatically.
#
# NON-DESTRUCTIVE BY CONTRACT. This script only ever *creates* a symlink in an
# empty slot. It never deletes, overwrites, or repoints anything — not a real
# file/dir, not an existing symlink (even one pointing elsewhere), not even to
# "fix" a wrong link. Anything other than "slot is empty" or "link already
# correct" is reported loudly and the script exits non-zero, leaving your
# filesystem exactly as it was. To repoint a link, remove it yourself and re-run.
#
# Expected layout:
#   <workspace>/                       <- run `claude` here; siblings: flatppl-design/, flatppl-js/, ...
#   <workspace>/<this-repo>/{skills,references}   <- canonical, version-controlled here
#   <workspace>/.claude/{skills,references}       <- symlinks this script creates
set -euo pipefail

repo_root="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
repo_name="$(basename "$repo_root")"
workspace="$(dirname "$repo_root")"

# Refuse to proceed if the workspace .claude path is anything other than a real
# directory or absent — never mkdir over a file or a symlink we don't control.
claude_dir="$workspace/.claude"
if [ -L "$claude_dir" ]; then
  echo "ERROR: $claude_dir is a symlink — refusing to touch it. Remove it and re-run." >&2
  exit 1
fi
if [ -e "$claude_dir" ] && [ ! -d "$claude_dir" ]; then
  echo "ERROR: $claude_dir exists and is not a directory — refusing to touch it." >&2
  exit 1
fi
mkdir -p "$claude_dir"

skipped=0

link_one() {
  local name="$1"
  local link="$workspace/.claude/$name"
  local target="../$repo_name/$name"   # relative, so it survives a move/rename of the workspace

  # Source must exist, else we'd create a dangling link.
  if [ ! -d "$repo_root/$name" ]; then
    echo "ERROR: source $repo_root/$name does not exist — nothing to link." >&2
    skipped=$((skipped + 1))
    return
  fi

  # Existing symlink: only acceptable if it already points exactly where we want
  # (idempotent re-run). Pointing anywhere else is left untouched, not repointed.
  if [ -L "$link" ]; then
    local current
    current="$(readlink "$link")"
    if [ "$current" = "$target" ]; then
      echo "ok      .claude/$name  already -> $target"
      return
    fi
    echo "WARN: $link is a symlink to '$current', not '$target' — leaving it untouched." >&2
    echo "      Remove it and re-run if you want it repointed." >&2
    skipped=$((skipped + 1))
    return
  fi

  # Any other existing path (real file or dir): never clobber it.
  if [ -e "$link" ]; then
    echo "WARN: $link exists and is NOT a symlink — leaving it untouched. Remove it and re-run to link." >&2
    skipped=$((skipped + 1))
    return
  fi

  # Slot is empty: safe to create. No -f/-n — there is provably nothing to clobber.
  ln -s "$target" "$link"
  echo "linked  .claude/$name  ->  $target"
}

link_one skills
link_one references

if [ "$skipped" -gt 0 ]; then
  echo "WARNING: $skipped of 2 links were NOT created (see WARN above)." >&2
  echo "Remove the conflicting non-symlink path(s) under $workspace/.claude/ and re-run;" >&2
  echo "until then \`claude\` will NOT see all the skills." >&2
  exit 1
fi
echo "done. From $workspace, \`claude\` now sees the skills."
