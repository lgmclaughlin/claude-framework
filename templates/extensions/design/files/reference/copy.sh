#!/usr/bin/env bash
set -euo pipefail

# Copies the most recently modified file from ~/Pictures into .claude/reference
#
# If a filename argument is provided, the file is saved as <name>.<ext>.
# Otherwise, it defaults to new.<ext>.
#
# Intended for quick screenshot importing during development.
# Can be invoked directly or via the project CLI.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [[ -d "$HOME/Pictures" ]]; then
  SRC_DIR="$HOME/Pictures"
elif [[ -d "$HOME/pictures" ]]; then
  SRC_DIR="$HOME/pictures"
else
  echo "Could not find Pictures directory."
  exit 1
fi

DEST_DIR="$PROJECT_ROOT/.claude/reference"

mkdir -p "$DEST_DIR"

if stat --version >/dev/null 2>&1; then
  # GNU stat (Linux)
  latest_file="$(find "$SRC_DIR" -type f -print0 | xargs -0 stat -c "%Y %n" | sort -nr | head -n 1 | sed 's/^[0-9]* //')"
else
  # BSD stat (macOS)
  latest_file="$(find "$SRC_DIR" -type f -print0 | xargs -0 stat -f "%m %N" | sort -nr | head -n 1 | sed 's/^[0-9]* //')"
fi

if [[ -z "$latest_file" ]]; then
  echo "No files found in $SRC_DIR"
  exit 1
fi

ext="${latest_file##*.}"

if [[ $# -ge 1 ]]; then
  dest_name="$1.$ext"
else
  dest_name="new.$ext"
fi

cp "$latest_file" "$DEST_DIR/$dest_name"

echo "Copied $latest_file to $DEST_DIR/$dest_name"
