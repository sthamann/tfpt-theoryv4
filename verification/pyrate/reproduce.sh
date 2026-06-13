#!/usr/bin/env bash
# Independent cross-check of the TFPT F_transfer gauge-running inputs with PyR@TE 3.
#
# PyR@TE 3 (github.com/LSartore/pyrate, arXiv:2007.12700) is a third-party tool that
# derives the renormalization-group equations of any non-SUSY gauge theory from its
# field content alone. We run it on the Standard-Model field content (which is exactly
# the TFPT carrier content) and read off the one- and two-loop gauge beta functions.
# The committed evidence is verification/pyrate/sm_gauge_betas.txt; the numeric
# cross-check against the TFPT derivation lives in v159_pyrate_gauge_crosscheck.py.
#
# PyR@TE is NOT vendored: it is cloned on demand into experiments/pyrate (git-ignored).
# Usage:  bash verification/pyrate/reproduce.sh        # from anywhere in the repo
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo="$(cd "$here/../.." && pwd)"
venv="$repo/experiments/tfpt-discovery/.venv"
pyrate="$repo/experiments/pyrate"
out="$here/sm_gauge_betas.generated.txt"

# 1. activate the TFPT venv (mpmath/numpy/sympy/scipy + PyYAML/h5py/matplotlib)
# shellcheck disable=SC1091
source "$venv/bin/activate"

# 2. clone PyR@TE 3 on demand
if [ ! -f "$pyrate/pyR@TE.py" ]; then
  echo "[reproduce] cloning PyR@TE 3 into experiments/pyrate ..."
  git clone --depth 1 https://github.com/LSartore/pyrate.git "$pyrate"
fi

# 3. neutralise the interactive 'pdflatex' EndCommands hang (no-op)
if grep -q '^EndCommands : "pdflatex' "$pyrate/default.settings" 2>/dev/null; then
  python3 - "$pyrate/default.settings" <<'PY'
import sys, re
p = sys.argv[1]
s = open(p).read()
s = re.sub(r'^EndCommands : ".*"$', 'EndCommands : "true"', s, flags=re.M)
open(p, "w").write(s)
PY
fi

# 4. run the SM model at one and two loops
cd "$pyrate"
rm -rf results/SM
python3 "pyR@TE.py" -m models/SM.model -l 2 --no-LatexOutput --no-MathematicaOutput -q

# 5. extract the gauge beta functions
python3 - "$pyrate/results/SM/PythonOutput/RGEs.py" "$out" <<'PY'
import re, sys
src = open(sys.argv[1]).read()
lines = ["PyR@TE 3 -- regenerated gauge beta functions (SM, GUT normalization)", ""]
for g in ("g1", "g2", "g3"):
    m = re.search(rf"def beta_{g}\(.*?\):(.*?)(?=\ndef |\Z)", src, re.S)
    lines.append(f"### beta_{g}")
    lines.append(m.group(1).strip())
    lines.append("")
open(sys.argv[2], "w").write("\n".join(lines))
print("[reproduce] wrote", sys.argv[2])
print("\n".join(lines))
PY

echo "[reproduce] compare with the committed evidence:"
echo "            diff <(grep -E 'return' \"$here/sm_gauge_betas.txt\") <(grep -E 'return' \"$out\")"
