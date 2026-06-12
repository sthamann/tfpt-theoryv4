#!/usr/bin/env bash
# Reproducible build for the TFPT 4.5 document set.
# Usage:  bash build.sh           (build everything)
#         bash build.sh notes     (only the three new bridge-layer notes)
#         bash build.sh papers    (only the tfpt-45 papers 00-07)
#
# Requirements: a TeX Live / MacTeX installation providing `pdflatex`.
# All relative \input paths resolve when each document is compiled from the
# directory shown below, so no manual file copying is needed.

set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
PASS=0; FAIL=0; FAILED=()

build_one() {  # $1 = working dir, $2 = tex basename (no extension)
  local dir="$1" base="$2"
  ( cd "$dir" && pdflatex -interaction=nonstopmode -halt-on-error "$base.tex" >/dev/null 2>&1 \
                && pdflatex -interaction=nonstopmode -halt-on-error "$base.tex" >/dev/null 2>&1 )
  if [ -f "$dir/$base.pdf" ] && [ "$dir/$base.tex" -ot "$dir/$base.pdf" ]; then
    local pages=""
    command -v pdfinfo >/dev/null 2>&1 && pages=$(pdfinfo "$dir/$base.pdf" 2>/dev/null | awk '/^Pages/{print $2" pages"}')
    printf "  [OK]   %-52s %s\n" "$base" "${pages:+($pages)}"; PASS=$((PASS+1))
  else
    printf "  [FAIL] %-52s\n" "$base"; FAIL=$((FAIL+1)); FAILED+=("$base")
  fi
}

NOTES=(
  introduction
  tfpt_1_architecture_e8
  tfpt_2_standard_model
  tfpt_3_e8_audit_bootstrap
  tfpt_4_frontier
  tfpt_5_redteam
  tfpt_horizon_readouts
  tfpt_research_contracts
  origin_theory
  changelog
)
PAPERS=(
  00_orientation_note
  01_boundary_kernel
  02_carrier_rigidity_standard_model_packet
  03_electromagnetic_closure_flavor_transport
  04_admissibility_strong_cp_qft_closure
  05_geometric_hodge_closure_dimensionless_metrology
  06_cosmology_interfaces_downstream_closure
  07_cmb_operational_closure_planck_pipeline
)

WHAT="${1:-all}"
if [ "$WHAT" = "all" ] || [ "$WHAT" = "notes" ]; then
  echo "== Bridge-layer notes (compiled from repo root) =="
  for b in "${NOTES[@]}"; do build_one "$ROOT" "$b"; done
fi
if [ "$WHAT" = "all" ] || [ "$WHAT" = "papers" ]; then
  echo "== TFPT 4.5 papers (compiled from tfpt-45/) =="
  for b in "${PAPERS[@]}"; do build_one "$ROOT/tfpt-45" "$b"; done
fi

echo "------------------------------------------------------------"
echo "build summary: $PASS ok, $FAIL failed"
if [ "$FAIL" -gt 0 ]; then printf '  failed: %s\n' "${FAILED[*]}"; exit 1; fi
