#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$repo_root/skills"
target_dir="${1:-$HOME/.codex/skills}"

mkdir -p "$target_dir"

linked=0
for skill_dir in "$source_dir"/*; do
    [[ -d "$skill_dir" && -f "$skill_dir/SKILL.md" ]] || continue

    skill_name="$(basename "$skill_dir")"
    link_path="$target_dir/$skill_name"

    if [[ -e "$link_path" && ! -L "$link_path" ]]; then
        echo "Refusing to replace real path: $link_path" >&2
        exit 1
    fi

    if [[ -L "$link_path" ]]; then
        rm -- "$link_path"
    fi

    relative_target="$(python3 - "$skill_dir" "$target_dir" <<'PY'
import os
import sys

print(os.path.relpath(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])))
PY
)"
    ln -s "$relative_target" "$link_path"
    linked=$((linked + 1))
done

if [[ "$linked" -eq 0 ]]; then
    echo "No skills with SKILL.md found under $source_dir" >&2
    exit 1
fi

echo "Linked $linked skills from $source_dir into $target_dir"
