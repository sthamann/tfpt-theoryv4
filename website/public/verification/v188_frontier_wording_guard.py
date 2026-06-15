"""v188 -- the frontier-wording guard (a prose sentinel, no new physics). v187
protects the *ledger typing*; this guard protects the *prose*: it forbids stale
sentences whose semantics an earlier round superseded, so a frozen Zenodo release
can never re-introduce wording that was true yesterday and is only half-true
today. Each forbidden pattern records what superseded it. The guard PASSES when
none of the stale phrasings appear in the active documents.

  [I] FORBIDDEN STALE PROSE (must be absent from the active .tex set):
    1. "leptogenesis interface (\\mE)"  -> v184 retyped Route B to [C]
       (M_R is the seesaw scale, not a compiler power).
    2. "closed branch also fixes the leptogenesis inputs" -> same; the branch
       fixes the spectrum + a washout anchor, NOT the heavy scale.
    3. "relic scale $f_a,m_a$ open" -> v185 sharpened DM: the scales DEFINE the
       branch; what is open is the hilltop-sensitive relic abundance.
    4. "computed $Q=0.664$, ... near, not exact" -> v183 gave the 53/54 factor an
       exact operator origin; the summary must show that.
    5. "Suite now 187 modules" -> conflates count with ID; the count is 187 and
       the highest ID is v188 (v186 skipped).
    6. "Full quantum dynamics" -> standalone over-claim; the closure is the
       ADMISSIBLE physical sector, not the full ambient 4D theory.
    7. "Here is the complete solution" -> standalone over-claim; scope it to the
       admissible sector and state the ambient measure is not constructed.
    8. "64.36" (the old determinant-line axion mass 64.36 ueV / f_a~8.86e10 GeV)
       -> the SUPERSEDED small-angle (theta_i=phi0) reading; the current closed
       reading is theta_i=170.4 deg, f_a=M_scal/128~2.39e11 GeV, m_a~23.8 ueV.

  Python-only (text sentinel over the active documents).
"""
import os
import re

from tfpt_constants import check, summary, reset

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ACTIVE_DOCS = [
    "introduction.tex", "tfpt_1_architecture_e8.tex", "tfpt_2_standard_model.tex",
    "tfpt_3_e8_audit_bootstrap.tex", "tfpt_4_frontier.tex", "tfpt_5_redteam.tex",
    "tfpt_horizon_readouts.tex", "tfpt_research_contracts.tex", "origin_theory.tex",
    "changelog.tex",
]

# pattern (regex) -> what superseded it
FORBIDDEN = {
    r"leptogenesis interface \(\\mE\)":
        "v184 retyped Route B to [C] (M_R is the seesaw scale, not a compiler power)",
    r"closed branch also fixes the\s+leptogenesis inputs":
        "v184: the branch fixes the spectrum + a washout anchor, NOT the heavy scale M_R",
    r"relic scale \$f_a,m_a\$ open":
        "v185: f_a/m_a DEFINE the branch; the open item is the hilltop-sensitive relic abundance",
    r"computed \$Q=0\.664\$.{0,40}near, not exact":
        "v183: the 53/54 source->pole factor has an exact operator origin (F=R+Q corner)",
    r"Suite now 187 modules":
        "conflates count with ID: the count is 187 and the highest ID is v188 (v186 skipped); "
        "use 'has 187 modules, highest ID v188'",
    r"Full quantum dynamics":
        "standalone over-claim: the closure is the ADMISSIBLE physical sector, not the full "
        "ambient 4D theory; use 'Constructive QFT closure of the admissible physical sector'",
    r"Here is the complete solution":
        "standalone over-claim (gives reviewers free ammunition): scope it to the admissible "
        "sector and state the ambient measure is not constructed (G_metric frontier)",
    r"64\.36":
        "the determinant-line axion mass 64.36 ueV (f_a ~ 8.86e10 GeV) is the SUPERSEDED "
        "small-angle (theta_i=phi0) reading; the current closed reading is theta_i=170.4 deg, "
        "f_a=M_scal/128 ~ 2.39e11 GeV, m_a ~ 23.8 ueV (tfpt_4_frontier)",
}


def run():
    reset()
    print("v188 frontier-wording guard: stale prose must be absent from the active documents")

    texts = {}
    for d in ACTIVE_DOCS:
        p = os.path.join(ROOT, d)
        texts[d] = open(p, encoding="utf-8").read() if os.path.exists(p) else ""

    all_present = all(texts[d] for d in ACTIVE_DOCS)
    check("ACTIVE DOC SET READABLE [I]: all %d active documents present and read "
          "(%s)" % (len(ACTIVE_DOCS), ", ".join(d.replace(".tex", "") for d in ACTIVE_DOCS)),
          all_present)

    for pat, reason in FORBIDDEN.items():
        hits = [d for d, t in texts.items() if re.search(pat, t)]
        check("STALE PROSE ABSENT [I]: /%s/ not in any active doc (superseded by: %s)%s"
              % (pat, reason, "" if not hits else "  --- FOUND IN: %s" % hits),
              not hits)

    return summary("v188 frontier-wording guard (stale prose absent from active documents)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
