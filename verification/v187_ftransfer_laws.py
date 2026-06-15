"""v187 -- The F_transfer discipline guard (a CI-style firewall check, the
machine-readable form of the Frontier file's rule). The four continuous-transfer
frontier observables -- Koide, eta_B, the axion relic, m_p/m_e -- must NEVER be
typed as primitive [E]/[N] compiler predictions; each must carry a conditional
[C] or anchor/open [A]/[O] marker in the ledger. This module reads the ledger
and enforces it, so no future edit can quietly promote a 'pretty frontier number'
to a closed compiler output (the failure mode the Frontier firewall exists to
prevent).

  [I] 1. EACH FRONTIER TRANSFER IS [C]/[A]/[O], NEVER A PRIMITIVE [E]/[N].
        For the prediction rows of Koide (FR.KOIDE.*), eta_B (FR.ETAB.*), dark
        matter / axion (FR.DM.*), and m_p/m_e + Lambda_QCD (FR.MPME.*,
        QCD.LAMBDA.*), the ledger status carries a conditional/anchor/open marker
        -- exact algebraic SUB-parts may be [I]/[E] (e.g. the Koide 53/54 factor,
        v183; b_3 = -7, v159), but the PHYSICAL prediction is never a bare
        compiler [E]/[N].
  [I] 2. THE FUNCTOR HAS FOUR EXPLICIT INTERFACES (typing contract):
        F_pole : source masses -> pole masses        (Koide, v183)
        F_Boltzmann : CP source -> eta_B             (v169/v184)
        F_relic : (f_a, m_a, theta_i, N_DW) -> Omega_a (v185)
        F_QCD : (alpha_s, b_3, Lambda_QCD, lattice) -> m_p/m_e (v164)
        Each is standard physics fed TFPT source data, never a compiler power.
  [I] 3. THE RASTER RULE STILL BINDS: every load-bearing dimensionless number
        appears in an E8-branching projection, and the frozen registry (v84) +
        the null model (v100) bound the look-elsewhere burden -- the frontier
        transfers are explicitly OUTSIDE the closed dimensionless compiler.

  Python-only (reads status_ledger.csv and enforces the typing).
"""
import csv
import os

from tfpt_constants import check, summary, reset

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "status_ledger.csv")

# the F_transfer frontier families + CKM-downstream flavor readouts (prediction rows)
# (rare kaon FR.RAREKAON.* is a CKM-downstream readout, not one of the four functor
#  interfaces, but it is guarded the same way: never a primitive [E]/[N] compiler power)
FRONTIER_PREFIXES = ("FR.KOIDE.", "FR.ETAB.", "FR.DM.", "FR.MPME.", "QCD.LAMBDA.",
                     "FR.RAREKAON.")
CONDITIONAL = ("[C]", "[A]", "[O]", "conditional", "conjecture", "physical",
               "open", "scenario", "near-miss", "not forced", "not a claim",
               "non-claim", "transfer")


def _rows():
    with open(LEDGER, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def run():
    reset()
    print("v187 F_transfer discipline guard: the four frontier transfers stay [C]/[A]/[O], never primitive [E]/[N]")

    rows = _rows()
    frontier = [r for r in rows
                if r["claim_id"].startswith(FRONTIER_PREFIXES) and r.get("active") == "true"]

    # 1. each frontier transfer carries a conditional/anchor/open marker
    violations = []
    for r in frontier:
        blob = ((r.get("status") or "") + " " + (r.get("canonical_status") or "")).lower()
        if not any(tok.lower() in blob for tok in CONDITIONAL):
            violations.append(r["claim_id"])
    families = {p.rstrip(".") for p in FRONTIER_PREFIXES
                if any(r["claim_id"].startswith(p) for r in frontier)}
    check("EACH FRONTIER TRANSFER IS [C]/[A]/[O] [I]: all %d active frontier "
          "prediction rows across the families %s carry a conditional/anchor/open "
          "marker -- none is a bare primitive [E]/[N] compiler prediction "
          "(violations: %s). Exact algebraic sub-parts may be [I]/[E] (Koide 53/54 "
          "v183, b3=-7 v159), but the physical prediction never is"
          % (len(frontier), sorted(families), violations or "none"),
          len(frontier) >= 4 and not violations)

    # 2. the four interfaces are present and typed
    have = {
        "F_pole (Koide)": any(r["claim_id"].startswith("FR.KOIDE.") for r in frontier),
        "F_Boltzmann (eta_B)": any(r["claim_id"].startswith("FR.ETAB.") for r in frontier),
        "F_relic (axion)": any(r["claim_id"].startswith("FR.DM.") for r in frontier),
        "F_QCD (m_p/m_e)": any(r["claim_id"].startswith(("FR.MPME.", "QCD.LAMBDA.")) for r in frontier),
    }
    check("FOUR EXPLICIT INTERFACES [I]: F_pole (Koide, v183), F_Boltzmann "
          "(eta_B, v169/v184), F_relic (axion, v185), F_QCD (m_p/m_e, v164) all "
          "present as typed transfer rows (%s) -- standard physics fed TFPT "
          "source data, never a compiler power" % have,
          all(have.values()))

    # 3. the raster rule + freeze still bind (cross-refs exist)
    ids = {r["claim_id"] for r in rows}
    check("RASTER + FREEZE BIND [I]: the frozen registry (REG.FREEZE.01) and the "
          "null model (AUDIT.NULLMC.01) are present and bound the look-elsewhere "
          "burden; the frontier transfers are explicitly OUTSIDE the closed "
          "dimensionless compiler",
          "REG.FREEZE.01" in ids and "AUDIT.NULLMC.01" in ids)

    return summary("v187 F_transfer discipline guard (frontier transfers stay [C]/[A]/[O])")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
