#!/usr/bin/env bash
# Export a filtered working tree for the Overleaf GitHub-sync mirror (tfpt5-shadow).
#
# Included:  all git-tracked files except the exclusions below.
# Excluded:  _archive/, website/, *.pdf, .cursor/
#
# Usage:
#   bash scripts/export-shadow.sh /path/to/shadow-checkout
#
# Typical local test:
#   rm -rf /tmp/tfpt5-shadow && mkdir /tmp/tfpt5-shadow
#   bash scripts/export-shadow.sh /tmp/tfpt5-shadow
#
# The GitHub Action .github/workflows/shadow-sync.yml runs this on every push to main.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${1:?Usage: bash scripts/export-shadow.sh <destination-directory>}"

should_export() {
  local f="$1"
  case "$f" in
    _archive/*|website/*|.cursor/*|.github/*) return 1 ;;
  esac
  case "$f" in
    *.pdf) return 1 ;;
  esac
  return 0
}

mkdir -p "$DEST"

LIST="$(mktemp)"
trap 'rm -f "$LIST"' EXIT

git -C "$ROOT" ls-files | while IFS= read -r f; do
  should_export "$f" && printf '%s\n' "$f"
done | sort > "$LIST"

while IFS= read -r f; do
  [ -n "$f" ] || continue
  mkdir -p "$DEST/$(dirname "$f")"
  cp "$ROOT/$f" "$DEST/$f"
done < "$LIST"

file_count=0
while IFS= read -r _; do
  file_count=$((file_count + 1))
done < "$LIST"

# Drop mirror files that no longer belong (keeps incremental git diffs small).
while IFS= read -r existing; do
  rel="${existing#"$DEST"/}"
  case "$rel" in
    SHADOW_MIRROR.md) continue ;;
  esac
  if ! grep -Fxq "$rel" "$LIST"; then
    rm -f "$existing"
  fi
done < <(find "$DEST" -type f ! -path "$DEST/.git/*" 2>/dev/null || true)

find "$DEST" -type d -empty ! -path "$DEST/.git/*" -delete 2>/dev/null || true

cat > "$DEST/SHADOW_MIRROR.md" <<EOF
# tfpt5-shadow (auto-generated mirror)

This repository is a **one-way mirror** of the main TFPT repository, maintained for
[Overleaf GitHub synchronization](https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/github-synchronization).

| Included | Excluded |
|----------|----------|
| Active \`.tex\` papers, \`tex-artefacts/\`, \`figures/\` | \`_archive/\` |
| \`verification/\` (Python suite, ledger, maps) | \`website/\` |
| \`experiments/\` (Lean, discovery) | All \`*.pdf\` |
| \`build.sh\`, manifests, README | \`.cursor/\` |

**Do not edit here.** Changes flow: main repo → this mirror (GitHub Action) → Overleaf pull.

Source: \`${GITHUB_REPOSITORY:-sthamann/tfpt-theoryv4}\` @ \`${GITHUB_SHA:-local}\`
Last export: $(date -u +"%Y-%m-%d %H:%M:%SZ")
Files exported: ${file_count}
EOF

printf 'export-shadow: %s files -> %s\n' "$file_count" "$DEST"
