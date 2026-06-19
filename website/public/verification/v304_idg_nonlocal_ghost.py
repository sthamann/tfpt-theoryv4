"""v304 -- QGAMB.IDG.01: the KMS spectral-action cutoff suggests a NONLOCAL
(infinite-derivative) graviton form factor; under entire analyticity the Stelle
ghost is a TRUNCATION ARTEFACT.  This is a CONDITIONAL narrowing of the red-team
rt_F perturbative-gravity attack (the R^2/Weyl^2 Stelle ghost), NOT a closure of
QG.AMB.01.  It introduces no new parameter: the cutoff is the seam KMS weight
already derived in v259 (PS.SPECACT.02).

Background.  rt_F / v278 correctly flag that the local R + R^2 / Weyl^2 spectral-
action gravity sector has a four-derivative propagator 1/(p^2(p^2+M^2)) with a
negative-residue massive spin-2 mode -- the Stelle ghost -- so the *perturbative*
gravity S-matrix is non-unitary.  The honest TFPT position keeps QG.AMB.01 [O].
This script asks ONE sharply-bounded question on the theory's own terms: the
R + R^2 sector arises by TRUNCATING the spectral action Tr f(D^2/Lambda^2) at the
a_4 Seeley-DeWitt order; what happens if one keeps the seam-fixed exponential
cutoff f(u) = e^{-u} (v259) WITHOUT truncating?

  [E] 1. STELLE GHOST = TRUNCATION ARTEFACT.  the local four-derivative propagator
        1/(p^2(p^2+M^2)) partial-fractions to (1/M^2)[1/p^2 - 1/(p^2+M^2)]: a
        HEALTHY massless graviton (residue +1/M^2 at p^2=0) plus a massive spin-2
        mode with a NEGATIVE residue -1/M^2 at p^2=-M^2 (the Stelle ghost) --
        reproducing rt_F / v278 exactly.
  [E] 2. ENTIRE FORM FACTOR HAS NO EXTRA POLE.  for an infinite-derivative kinetic
        operator p^2 a(p^2) with a(z) = e^{z/M^2} -- an ENTIRE function, nowhere
        zero (Weierstrass: exp has no zeros) -- the dressed propagator
        1/(p^2 a(p^2)) has its ONLY pole at p^2 = 0 (the massless graviton): no
        new pole, hence no ghost (Tomboulis 1997; Biswas-Mazumdar-Siegel 2006;
        Biswas-Gerwick-Koivisto-Mazumdar 2012).
  [E] 3. NEG CONTROL: A POLYNOMIAL FORM FACTOR RE-INTRODUCES THE GHOST.  a finite
        truncation a(z) = 1 + z/M^2 (the R + R^2 order) is a polynomial with a real
        zero at z = -M^2 -- exactly the ghost pole.  So "entire vs polynomial" is
        the discriminating property: only the UN-truncated (entire) form factor is
        ghost-free; every finite-derivative truncation carries a zero = a ghost.
  [C] 4. THE CUTOFF IS THE SEAM'S OWN WEIGHT, NOT A CHOICE.  v259 fixes the
        spectral-action cutoff to the beta=1 seam KMS weight f(u) = e^{-u}
        (Tomita-Takesaki + the seam unit 2 pi = 1/(4 c3), v58) -- no new
        parameter.  The UN-truncated trace Tr e^{-D^2/Lambda^2} is the nonlocal
        object; truncating it at a_4 is what produces the local R + R^2 and hence
        the Stelle ghost, so reading the spectral action at the seam-fixed cutoff
        WITHOUT truncating is the natural theory-internal move.
  [C] 5. CONDITIONAL NARROWING (the honest claim).  IF the resummed graviton form
        factor of the un-truncated KMS spectral action is an ENTIRE function of
        bounded type (the Biswas-Mazumdar-Siegel class), THEN by items 2-3 the
        perturbative graviton is ghost-free and the rt_F Stelle-ghost attack is a
        truncation artefact -- a perturbative NARROWING of the objection.
  [O] 6. WHAT STAYS OPEN (no overclaim).  two gaps remain: (i) the trace regulator
        f in Tr f(D^2/Lambda^2) is NOT identical to the kinetic form factor
        a(Box) of the graviton propagator -- that the heat-kernel resummation
        yields an ENTIRE a(Box) (rather than a generic nonlocal / non-analytic
        tail) is an UNPROVEN analyticity assumption; (ii) even a ghost-free
        PERTURBATIVE graviton is not the NONPERTURBATIVE ambient measure that
        QG.AMB.01 demands.  So QGAMB.IDG.01 stays [C]/[O]: a conditional narrowing
        of rt_F, consistent with the SEAM.EQUIV.01 firewall, NOT a TOE closure.

Status: [E] the truncation-artefact algebra (items 1-3, exact sympy); [C] the
KMS-cutoff link + the conditional ghost-freedom (items 4-5); [O] the entire-
analyticity assumption + the nonperturbative gap (item 6).  Does NOT change
QG.AMB.01's [O] status.  Python-only (sympy; elementary pole algebra, like v259).
"""
import sympy as sp

from tfpt_constants import check, summary, reset

p2, z = sp.symbols("p2 z", real=True)
M2 = sp.symbols("M2", positive=True)            # M^2 > 0 (the ghost mass-squared scale)


def run():
    reset()
    print("v304  QGAMB.IDG.01: KMS cutoff -> nonlocal graviton form factor; entire => no Stelle ghost (conditional)")

    # ---- 1. Stelle ghost = truncation artefact (local R+R^2 four-derivative propagator) ----
    local_prop = 1 / (p2 * (p2 + M2))
    ap = sp.apart(local_prop, p2)
    res_massless = sp.limit(p2 * local_prop, p2, 0)             # residue at p^2 = 0
    res_massive = sp.limit((p2 + M2) * local_prop, p2, -M2)     # residue at p^2 = -M^2
    check("STELLE GHOST = TRUNCATION ARTEFACT [E]: the local four-derivative "
          "propagator 1/(p^2(p^2+M^2)) = %s has a HEALTHY massless graviton "
          "(residue %s at p^2=0) and a massive spin-2 mode with NEGATIVE residue "
          "%s at p^2=-M^2 (the Stelle ghost) -- exactly rt_F / v278"
          % (ap, res_massless, res_massive),
          sp.simplify(res_massless - 1 / M2) == 0
          and sp.simplify(res_massive + 1 / M2) == 0
          and res_massless > 0 and res_massive < 0, exact=True)

    # ---- 2. entire form factor a(z)=e^{z/M^2} has no zeros => dressed prop has only the p^2=0 pole ----
    a_entire = sp.exp(z / M2)
    zeros_entire = sp.solve(a_entire, z)                        # exp never vanishes -> []
    denom_entire = p2 * sp.exp(p2 / M2)
    poles_entire = sp.solve(denom_entire, p2)                   # only p^2 = 0
    check("ENTIRE FORM FACTOR HAS NO EXTRA POLE [E]: a(z)=e^{z/M^2} is entire and "
          "nowhere zero (solve(e^{z/M^2})=%s), so the dressed IDG propagator "
          "1/(p^2 e^{p^2/M^2}) has its ONLY pole at p^2=%s -- no new pole, no ghost "
          "(Tomboulis 1997; Biswas-Mazumdar-Siegel 2006)"
          % (zeros_entire, poles_entire),
          zeros_entire == [] and poles_entire == [sp.Integer(0)], exact=True)

    # ---- 3. neg control: a polynomial (truncated) form factor re-introduces the ghost ----
    a_poly = 1 + z / M2
    zeros_poly = sp.solve(a_poly, z)                            # z = -M^2 (the ghost)
    poles_poly = sp.solve(p2 * (1 + p2 / M2), p2)               # {0, -M^2}: graviton + ghost
    check("NEG CONTROL -- POLYNOMIAL FORM FACTOR RE-INTRODUCES THE GHOST [E]: a "
          "finite truncation a(z)=1+z/M^2 (the R+R^2 order) is a polynomial with a "
          "real zero at z=%s, so the propagator denominator p^2(1+p^2/M^2) has poles "
          "%s (graviton + ghost) -- 'entire vs polynomial' is the discriminating "
          "property: only the un-truncated (entire) factor is ghost-free"
          % (zeros_poly, poles_poly),
          zeros_poly == [-M2]
          and set(poles_poly) == {sp.Integer(0), -M2}, exact=True)

    # ---- 4. the cutoff is the seam KMS weight, not a choice (v259, recorded) ----
    check("CUTOFF = SEAM KMS WEIGHT, NOT A CHOICE [C]: v259 (PS.SPECACT.02) fixes "
          "the spectral-action cutoff to the beta=1 seam KMS weight f(u)=e^{-u} "
          "(Tomita-Takesaki + the seam unit 2pi=1/(4 c3), v58) -- no new parameter; "
          "the UN-truncated trace Tr e^{-D^2/Lambda^2} is the nonlocal object, and "
          "truncating it at a_4 is what produces the local R+R^2 and the Stelle "
          "ghost (rt_F)", True)

    # ---- 5. conditional narrowing (the honest claim) ----
    check("CONDITIONAL NARROWING [C]: IF the resummed graviton form factor of the "
          "un-truncated KMS spectral action is an ENTIRE function of bounded type "
          "(Biswas-Mazumdar-Siegel class), THEN by items 2-3 the perturbative "
          "graviton is ghost-free and the rt_F Stelle-ghost attack is a truncation "
          "artefact -- a perturbative narrowing of the objection, not a closure", True)

    # ---- 6. what stays open (no overclaim) ----
    check("WHAT STAYS OPEN [O]: (i) the trace regulator f in Tr f(D^2/Lambda^2) is "
          "NOT identical to the kinetic form factor a(Box) -- that the heat-kernel "
          "resummation yields an ENTIRE a(Box) is an UNPROVEN analyticity "
          "assumption; (ii) a ghost-free PERTURBATIVE graviton is not the "
          "NONPERTURBATIVE ambient measure QG.AMB.01 demands. So QGAMB.IDG.01 stays "
          "[C]/[O]: a conditional narrowing of rt_F, consistent with the "
          "SEAM.EQUIV.01 firewall, NOT a TOE closure", True)

    return summary("v304 QGAMB.IDG.01: KMS cutoff -> nonlocal form factor; entire => no Stelle ghost (conditional narrowing of rt_F, NOT a QG.AMB.01 closure)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
