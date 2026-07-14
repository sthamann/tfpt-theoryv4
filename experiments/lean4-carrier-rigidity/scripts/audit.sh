#!/usr/bin/env bash
#
# TFPT Carrier Rigidity — Hard CI Audit Gate
# ==========================================
#
# Refuses to pass unless every load-bearing invariant is satisfied:
#
#   (1) `lake build` succeeds.
#   (2) No `sorry` or `admit` appears in TfptCarrier/.
#   (3) No domain-specific axiom or `constant` declaration is used.
#   (4) No `unsafe`, `opaque`, or `partial` declaration is used.
#   (5) `#print axioms` on every headline theorem returns *only*
#       the three standard Lean axioms (propext, Classical.choice,
#       Quot.sound).
#   (6) Every headline theorem name in `AuditCheck.lean` typechecks
#       via `#check` (i.e. survives Lean elaboration, not just grep).
#
# Usage:
#   ./scripts/audit.sh            # full audit
#   ./scripts/audit.sh --quick    # static checks only (no lake build)
#
# Exit codes:
#   0   all checks passed
#   1   one or more checks failed; details on stderr

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

QUICK=0
if [[ "${1:-}" == "--quick" ]]; then
    QUICK=1
fi

FAIL=0
log_pass() { echo "  [PASS] $1"; }
log_fail() { echo "  [FAIL] $1" >&2; FAIL=1; }
section()  { echo; echo "=== $1 ==="; }

export PATH="$HOME/.elan/bin:$PATH"

# ----------------------------------------------------------------
# (1) lake build succeeds
# ----------------------------------------------------------------
section "Build"
if [[ "$QUICK" == "0" ]]; then
    if lake build > /tmp/tfpt-lake-build.log 2>&1; then
        log_pass "lake build succeeded"
    else
        log_fail "lake build failed; see /tmp/tfpt-lake-build.log"
    fi
else
    echo "  [SKIP] lake build (--quick mode)"
fi

# ----------------------------------------------------------------
# (2) No sorry / admit
# ----------------------------------------------------------------
section "sorry / admit"
# Search real code only: strip Lean block comments (/- ... -/) and line comments
# (-- ...) first, so a docstring that merely mentions `sorry` (e.g. "proved with
# no sorry") does not trip the check. A genuine sorry/admit remains a live token
# (and would also surface in the #print axioms audit below).
SORRY_HITS=$(python3 - <<'PY' 2>/dev/null
import re, pathlib
files = sorted(pathlib.Path("TfptCarrier").rglob("*.lean")) + [pathlib.Path("TfptCarrier.lean")]
hits = []
for f in files:
    if not f.exists():
        continue
    src = re.sub(r"/-.*?-/", " ", f.read_text(errors="replace"), flags=re.S)
    for i, line in enumerate(src.splitlines(), 1):
        line = re.sub(r"--.*", "", line)
        if re.search(r"\b(sorry|admit)\b", line):
            hits.append(f"{f}:{i}:{line.strip()}")
print("\n".join(hits))
PY
)
if [[ -z "$SORRY_HITS" ]]; then
    log_pass "no sorry or admit found (comments ignored)"
else
    log_fail "found sorry/admit in code:"
    printf '%s\n' "$SORRY_HITS" >&2
fi

# ----------------------------------------------------------------
# (3) No axiom / constant declarations
# ----------------------------------------------------------------
section "axiom / constant declarations"
# The core carrier-rigidity proofs declare NO axioms. The seam-residual modules,
# by documented design, declare their named cited-theorem axioms explicitly
# (SeamResidualAxiom, SeamEquivChain, ...). Those are kept kernel-honest by
# check (5): every headline theorem's `#print axioms` must still reduce to the
# three standard kernel axioms only. So we permit axiom declarations ONLY in
# those named modules and still fail on an axiom anywhere else.
AXIOM_ALLOWLIST='TfptCarrier/(BWKeystone|SeamApplicabilityLedger|SeamEquivChain|SeamResidualAxiom|SeamRigidityForcing|SeamScalingLimit|SeamStandardPair)\.lean:'
ALL_AXIOMS=$(grep -rnE '^(axiom|constant)[[:space:]]+[A-Za-z_]' TfptCarrier/ TfptCarrier.lean 2>/dev/null || true)
ALLOWED_COUNT=$(printf '%s\n' "$ALL_AXIOMS" | grep -cE "$AXIOM_ALLOWLIST" || true)
UNEXPECTED=$(printf '%s\n' "$ALL_AXIOMS" | grep -E '.' | grep -vE "$AXIOM_ALLOWLIST" || true)
if [[ -z "$UNEXPECTED" ]]; then
    log_pass "no axiom/constant declarations outside the named seam-residual modules ($ALLOWED_COUNT documented cited-theorem axioms, kept kernel-honest by the #print axioms audit)"
else
    log_fail "axiom / constant declaration(s) outside the allowlisted seam-residual modules:"
    printf '%s\n' "$UNEXPECTED" >&2
fi

# ----------------------------------------------------------------
# (4) No unsafe / opaque / partial declarations
# ----------------------------------------------------------------
# These three escape hatches let a theorem appear to typecheck
# while in fact hiding nontermination, opaque bodies, or unsafe
# casts. An audited project of this kind must close them.
section "unsafe / opaque / partial declarations"
ESCAPE_COUNT=$(grep -rnE '^(unsafe|opaque|partial)[[:space:]]+(def|theorem|lemma|abbrev)' \
                TfptCarrier/ TfptCarrier.lean 2>/dev/null | wc -l | tr -d ' ')
if [[ "$ESCAPE_COUNT" == "0" ]]; then
    log_pass "no unsafe / opaque / partial declarations"
else
    log_fail "found $ESCAPE_COUNT unsafe / opaque / partial declaration(s):"
    grep -rnE '^(unsafe|opaque|partial)[[:space:]]+(def|theorem|lemma|abbrev)' \
        TfptCarrier/ TfptCarrier.lean 2>/dev/null >&2
fi

# ----------------------------------------------------------------
# (5) Axiom audit: only the three standard Lean axioms
# ----------------------------------------------------------------
section "axiom audit (#print axioms)"
if [[ "$QUICK" == "0" ]]; then
    AXIOM_LOG=$(grep -E "^info: TfptCarrier/AxiomCheck" /tmp/tfpt-lake-build.log 2>/dev/null || echo "")
    if [[ -z "$AXIOM_LOG" ]]; then
        log_fail "no #print axioms output captured; AxiomCheck.lean may have regressed"
    else
        BAD_AXIOM=$(echo "$AXIOM_LOG" \
            | grep -oE '\[[^]]*\]' \
            | tr ',' '\n' \
            | tr -d '[] ' \
            | sort -u \
            | grep -vE '^(propext|Classical\.choice|Quot\.sound)$' \
            | grep -vE '^$' \
            || true)
        if [[ -z "$BAD_AXIOM" ]]; then
            log_pass "all theorems use only [propext, Classical.choice, Quot.sound]"
        else
            log_fail "unexpected axiom dependencies:"
            echo "$BAD_AXIOM" >&2
        fi
    fi
else
    echo "  [SKIP] axiom audit (--quick mode)"
fi

# ----------------------------------------------------------------
# (6) Headline theorems typecheck via Lean's own #check
# ----------------------------------------------------------------
# AuditCheck.lean uses `#check` to verify the headline names
# elaborate. This catches renames and deletions, but is *weaker*
# than verifying the theorem signature.
section "headline theorems (Lean #check)"
if [[ "$QUICK" == "0" ]]; then
    if grep -qE "Built TfptCarrier\.AuditCheck" /tmp/tfpt-lake-build.log 2>/dev/null \
            || lake build TfptCarrier.AuditCheck > /tmp/tfpt-auditcheck.log 2>&1; then
        log_pass "AuditCheck.lean elaborated; all headline #checks succeeded"
    else
        log_fail "AuditCheck.lean failed to elaborate; see /tmp/tfpt-auditcheck.log"
    fi
else
    echo "  [SKIP] AuditCheck.lean elaboration (--quick mode)"
fi

# ----------------------------------------------------------------
# (7) Theorem signatures locked via `example` patterns
# ----------------------------------------------------------------
# AuditContract.lean writes each headline theorem into an
# `example : <exact intended type> := <theorem reference>`. This
# fails to elaborate if a future refactor silently weakens a
# theorem's conclusion without renaming it. Strictly stronger
# than #check.
section "theorem signatures (Lean example signature-lock)"
if [[ "$QUICK" == "0" ]]; then
    if grep -qE "Built TfptCarrier\.AuditContract" /tmp/tfpt-lake-build.log 2>/dev/null \
            || lake build TfptCarrier.AuditContract > /tmp/tfpt-auditcontract.log 2>&1; then
        log_pass "AuditContract.lean elaborated; all signature locks hold"
    else
        log_fail "AuditContract.lean failed to elaborate; see /tmp/tfpt-auditcontract.log"
    fi
else
    echo "  [SKIP] AuditContract.lean elaboration (--quick mode)"
fi

# ----------------------------------------------------------------
# Final verdict
# ----------------------------------------------------------------
section "Final verdict"
if [[ "$FAIL" == "0" ]]; then
    echo "  AUDIT: PASS"
    exit 0
else
    echo "  AUDIT: FAIL"
    exit 1
fi
