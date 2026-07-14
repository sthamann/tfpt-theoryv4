#!/usr/bin/env bash
# Export a filtered working tree for the Overleaf GitHub-sync mirror (tfpt5-shadow).
#
# Included:  all git-tracked files except the exclusions below.
#            figures/*.pdf ARE mirrored (the manifest references them).
# Excluded:  _archive/, website/, .cursor/, .github/, and every NON-figure *.pdf
#            (compiled paper/archive PDFs).
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
    figures/*.pdf) return 0 ;;   # ship the figures: manifest.sha256 references them
    *.pdf) return 1 ;;           # but no compiled paper / archive PDFs
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
| Active \`.tex\` papers, \`tex-artefacts/\`, \`figures/*.pdf\` | \`_archive/\`, \`website/\` |
| \`verification/\` (Python suite, ledger, maps, redteam, wolfram) | \`.cursor/\`, \`.github/\` |
| \`experiments/\` (Lean, discovery) | Compiled paper \`*.pdf\` (non-figure) |
| \`build.sh\`, manifests, README | |

**Shadow-mode note.** This subset ships \`figures/\` (so \`python3 verification/make_manifest.py --check\`
passes literally on the export) but **not** \`website/\`. The single-source generators
(\`verification/make_script_index.py\`, \`make_changelog_web.py\`, \`make_docs_map.py\`) detect the
missing \`website/\` and skip their website mirrors (\`ScriptIndex.tsx\`, \`lib/changelog.ts\`,
\`website_map.csv\`), so \`bash build.sh notes\` and \`bash build.sh gen\` run on the subset
non-destructively. \`bash build.sh audit\` is likewise shadow-aware: it skips the website mirror,
website version and website wolfram-page checks and prints which sections it skipped.

**Export coherence gate.** \`scripts/export-shadow.sh\` re-runs \`make_manifest.py --check\` and the
(shadow-aware) \`audit_sync.py\` on this filtered tree before the mirror is published, so a package
that says \"ALL CHECKS PASSED\" cannot ship unless it actually reproduces as exported.

**Do not edit here.** Changes flow: main repo → this mirror (GitHub Action) → Overleaf pull.

Source: \`${GITHUB_REPOSITORY:-sthamann/tfpt}\` @ \`${GITHUB_SHA:-local}\`
Last export: $(date -u +"%Y-%m-%d %H:%M:%SZ")
Files exported: ${file_count}
EOF

printf 'export-shadow: %s files -> %s\n' "$file_count" "$DEST"

# --- export coherence gate --------------------------------------------------
# The mirror must be reproducible AS SHIPPED.  Two cheap, stdlib-only checks run
# on the FILTERED tree before it is ever pushed/zipped, catching exactly the
# Alessandro shadow-export findings:
#   * make_manifest.py --check  -> every manifest-referenced file is present and
#     current in the export (catches uncommitted modules dropped by git ls-files,
#     and a stale manifest.sha256), so run_all.py can't reference a missing vN;
#   * audit_sync.py (shadow-aware) -> suite <-> run_all <-> registry <-> ledger
#     and the non-website generated surfaces agree on the subset.
# A failure here means: regenerate manifest.sha256 (python3 verification/make_manifest.py)
# and/or commit the missing files in the MAIN repo, then re-export.
if command -v python3 >/dev/null 2>&1; then
  echo "== shadow export coherence gate =="
  if ! ( cd "$DEST" && python3 verification/make_manifest.py --check ); then
    echo "::error::shadow export FAILED make_manifest.py --check on the filtered tree." >&2
    echo "  Fix in the MAIN repo: ensure every manifest-referenced file is committed, then" >&2
    echo "  re-run 'python3 verification/make_manifest.py' as the LAST step and re-export." >&2
    exit 1
  fi
  if ! ( cd "$DEST" && python3 verification/audit_sync.py ); then
    echo "::error::shadow export FAILED the (shadow-aware) sync audit on the filtered tree." >&2
    exit 1
  fi
  echo "shadow export coherence gate: PASS"
else
  echo "WARNING: python3 not found -- skipping shadow export coherence gate" >&2
fi
