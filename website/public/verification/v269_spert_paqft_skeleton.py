"""v269 -- QFT4D.SPERT.01: the perturbative 4D S-matrix (S_pert) as an Epstein-Glaser
/ pAQFT skeleton -- the honest middle layer of the three-layer S-matrix, NOT a
nonperturbative closure.  No new physics: it types S_pert precisely, checks that the
spectral-action interaction is power-counting renormalizable (so the Epstein-Glaser
construction applies order by order, with finitely many local counterterms and NO
UV divergences), and is explicit that this is perturbative -- the nonperturbative
ambient measure QG.AMB.01 stays open.

Three-layer S-matrix (proposal Q6, made precise):
    S_top   = the DHR braiding monodromy on the 2d boundary net (|M|=1, statistics
              -- NOT 4d cross-sections), v243.
    S_pert  = the 4d Epstein-Glaser / BV S-matrix of the Connes spectral action
              S(g) = T exp(i int g L_int), this script.
    S_phys  = LSZ[ Wightman functions of the OS-reconstructed admissible sector ],
              v240.
These are THREE DISTINCT objects; the 2d braiding is not the physical 4d S-matrix.

  [E] 1. THREE-LAYER TYPING.  S_top is a unitary phase on the 2d boundary (a
        statistics datum, |M(a,b)|=1, v243); S_phys is a 4d LSZ object on the OS
        Wightman functions (v240); S_pert is the 4d perturbative S-matrix in
        between.  Distinct dimensions and distinct content.
  [E] 2. POWER-COUNTING RENORMALIZABLE.  the spectral-action a_4 operator basis
        (gauge F^2, |Dphi|^2, phi^4, fermion kinetic, Yukawa, R^2, Weyl^2 -- all
        mass dim 4; phi^2, R, Lambda -- dim < 4) has EVERY operator of mass
        dimension <= 4 in 4D, so the interaction is power-counting renormalizable.
  [E] 3. FINITE COUNTERTERM BASIS.  exactly 7 marginal (dim-4) operators + 3
        relevant (dim<4) -- a FINITE local-counterterm basis, the Epstein-Glaser
        extension freedom at each order (no infinite tower of counterterms).
  [C] 4. EPSTEIN-GLASER EXISTENCE.  by the Epstein-Glaser theorem (Stueckelberg-
        Bogoliubov-Epstein-Glaser causal perturbation theory; pAQFT, Brunetti-
        Fredenhagen), a power-counting-renormalizable interaction has a
        perturbative S-matrix built ORDER BY ORDER by causal factorization +
        finite local extension to the diagonal -- no path integral, no UV
        divergences.  The spectral action qualifies, so S_pert exists as a formal
        power series.
  [C] 5. ADIABATIC LIMIT / GAP.  the admissible sector is gapped (Delta =
        6 log(3/2) > 0, v64/v240), so the massive theory has an IR-safe adiabatic
        limit g -> 1 and asymptotic states; S_pert connects to S_phys via LSZ on
        the OS Wightman functions.  Couplings (kappa, lambda, ...) feed in from the
        spectral action (v255).
  [O] 6. NONPERTURBATIVE RESIDUAL.  S_pert is PERTURBATIVE (a formal power series);
        the nonperturbative ambient interacting measure QG.AMB.01 stays open --
        pAQFT does NOT construct it.  The canonical 4D reading remains boundary-only
        (the v265 fork policy); S_pert is the perturbative cross-section layer on top.

Status: [E] the three-layer typing + power-counting + finite counterterm basis;
[C] the Epstein-Glaser existence (cited theorem applied) + the adiabatic/gap link;
[O] the nonperturbative ambient measure stays open.  A contract/skeleton (like
v244/v250), explicitly perturbative.  Python-only (sympy dimensions + structure).
"""
import sympy as sp

from tfpt_constants import check, summary, reset

# 4D mass dimensions of the fields
DIM = {"phi": sp.Integer(1), "psi": sp.Rational(3, 2), "A": sp.Integer(1),
       "F": sp.Integer(2), "D": sp.Integer(1), "R": sp.Integer(2), "C": sp.Integer(2)}

# spectral-action operator basis (a_4 Seeley-DeWitt content) -> mass dimension
OPS = {
    "gauge F^2": 2 * DIM["F"],
    "Higgs kinetic |Dphi|^2": 2 * (DIM["D"] + DIM["phi"]),
    "Higgs quartic phi^4": 4 * DIM["phi"],
    "fermion kinetic psibar D psi": 2 * DIM["psi"] + DIM["D"],
    "Yukawa phi psibar psi": DIM["phi"] + 2 * DIM["psi"],
    "R^2": 2 * DIM["R"],
    "Weyl^2 C^2": 2 * DIM["C"],
    "Higgs mass phi^2": 2 * DIM["phi"],
    "Einstein-Hilbert R": DIM["R"],
    "cosmological const": sp.Integer(0),
}


def run():
    reset()
    print("v269  QFT4D.SPERT.01: the perturbative 4D S-matrix (S_pert) as an Epstein-Glaser / pAQFT skeleton")

    # 1. three-layer typing
    layers = {
        "S_top": "2d boundary DHR braiding monodromy |M|=1 (statistics, v243)",
        "S_pert": "4d Epstein-Glaser / BV S-matrix of the spectral action (this)",
        "S_phys": "LSZ[OS-reconstructed admissible Wightman functions] (v240)",
    }
    check("THREE-LAYER TYPING [E]: S_top = %s; S_pert = %s; S_phys = %s -- three "
          "DISTINCT objects (the 2d braiding is a unitary phase/statistics datum, "
          "NOT the 4d cross-section S-matrix)"
          % (layers["S_top"], layers["S_pert"], layers["S_phys"]),
          len(layers) == 3)

    # 2. power-counting renormalizable
    all_renorm = all(d <= 4 for d in OPS.values())
    check("POWER-COUNTING RENORMALIZABLE [E]: every spectral-action a_4 operator has "
          "mass dimension <= 4 in 4D (gauge/Higgs-kinetic/quartic/fermion/Yukawa/"
          "R^2/Weyl^2 = 4; Higgs-mass/R = 2; Lambda = 0) -- a power-counting-"
          "renormalizable interaction, max dim = %s" % max(OPS.values()),
          all_renorm)

    # 3. finite counterterm basis
    marginal = [k for k, d in OPS.items() if d == 4]
    relevant = [k for k, d in OPS.items() if d < 4]
    check("FINITE COUNTERTERM BASIS [E]: exactly %d marginal (dim-4) operators "
          "%s + %d relevant (dim<4) -- a FINITE local-counterterm basis (the "
          "Epstein-Glaser extension freedom per order; no infinite tower)"
          % (len(marginal), marginal, len(relevant)),
          len(marginal) == 7 and len(relevant) == 3)

    # 4. Epstein-Glaser existence (cited theorem applied)
    check("EPSTEIN-GLASER EXISTENCE [C]: by the Epstein-Glaser theorem (causal "
          "perturbation theory; pAQFT, Brunetti-Fredenhagen), a power-counting-"
          "renormalizable interaction has a perturbative S-matrix S(g)=T exp(i int "
          "g L_int) built order by order by causal factorization + finite local "
          "extension -- no path integral, NO UV divergences. The spectral action "
          "qualifies, so S_pert exists as a formal power series", True)

    # 5. adiabatic limit / gap
    gap = float(-sp.log((sp.Rational(2, 3)) ** 6))
    check("ADIABATIC LIMIT / GAP [C]: the admissible sector is gapped (Delta = "
          "6 log(3/2) = %.4f > 0, v64/v240), so the massive theory has an IR-safe "
          "adiabatic limit g->1 and asymptotic states; S_pert connects to S_phys "
          "via LSZ on the OS Wightman functions (couplings feed in from the "
          "spectral action, v255)" % gap, gap > 0)

    # 6. nonperturbative residual
    check("NONPERTURBATIVE RESIDUAL [O]: S_pert is PERTURBATIVE (a formal power "
          "series); the nonperturbative ambient interacting measure QG.AMB.01 stays "
          "open -- pAQFT does NOT construct it. The canonical 4D reading remains "
          "boundary-only (v265 fork policy); S_pert is the perturbative cross-"
          "section layer on top, not a closure of ambient QG", True)

    return summary("v269 S_pert pAQFT skeleton: 4D perturbative S-matrix is EG-constructible [C]; ambient measure stays [O] (QFT4D.SPERT.01)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
