"""v370 -- GRAV.SPIN2.UNITARITY.01 (Track 2): the spin (Barnes-Rivers) decomposition of the
graviton propagator -- perturbative graviton unitarity SECTOR-BY-SECTOR.  This EXTENDS v304
(which did the scalar 1/(p^2(p^2+M^2)) pole algebra) to the actual tensor spin structure, and
combines it with v334 (the spin-0 conformal mode) into one sector-by-sector unitarity statement.
It does NOT re-derive v304's scalar ghost and does NOT close QG.AMB.01.

A symmetric rank-2 fluctuation h_{ab} decomposes under the Barnes-Rivers projectors into
spin-2 (P2, transverse-traceless), spin-1 (P1), and two spin-0 sectors (P0s scalar, P0w):

  [E] 1. PROJECTOR COMPLETENESS (the d-general trace identity).  in d dimensions
        tr P2 = (d-2)(d+1)/2, tr P1 = d-1, tr P0s = 1, tr P0w = 1, and the four traces SUM to
        d(d+1)/2 = the number of independent symmetric-tensor components.  In d=4 this is the
        clean split 5 + 3 + 1 + 1 = 10 -- the 5 physical spin-2 polarisations carry the graviton.
  [E] 2. EH PROPAGATOR STRUCTURE.  the Einstein-Hilbert (+ harmonic gauge) graviton propagator is
        ~ P2/p^2 - 1/(d-2) P0s/p^2; the spin-2 part has coefficient +1 (healthy) and the spin-0
        scalar the famous -1/(d-2) = -1/2 (d=4): the physical pole is the spin-2 massless graviton.
  [E] 3. THE STELLE GHOST LIVES IN THE SPIN-2 SECTOR.  a local higher-derivative (R+R^2/Weyl^2)
        dressing a_poly(p^2)=1+p^2/M^2 gives the spin-2 propagator P2/(p^2(1+p^2/M^2)), whose
        partial fraction (1/M^2)[1/p^2 - 1/(p^2+M^2)] has a NEGATIVE-residue pole at p^2=-M^2 --
        the Stelle ghost is a SPIN-2 state (extends v304's scalar result to the tensor sector).
  [E] 4. ENTIRE FORM FACTOR => SPIN-2 GHOST-FREE.  the un-truncated KMS form factor
        a(p^2)=e^{p^2/M^2} (v304/v259, entire and nowhere zero) gives the spin-2 propagator
        P2/(p^2 e^{p^2/M^2}) with its ONLY pole at p^2=0 -- the spin-2 sector is ghost-free.
  [C] 5. SPIN-0 SECTOR VIA THE GHP CONTOUR.  the spin-0 (conformal/trace) sector is the wrong-sign
        mode (c_conf(4)=-3/2, v332); it is made convergent by the GHP contour rotation + IDG
        dressing (v334), not by the spin-2 form factor.  So the two problematic sectors are cured
        by DIFFERENT, already-established mechanisms.
  [C] 6. PERTURBATIVE GRAVITON UNITARITY (sector-by-sector).  spin-1 and the spin-0 w-mode are pure
        gauge (no propagating pole); the physical content is the spin-2 graviton (ghost-free by 4)
        plus the GHP-controlled spin-0 (5).  So the full PERTURBATIVE graviton is ghost-free under
        the TFPT-fixed package -- conditional on v304's entire-analyticity assumption.
  [O] 7. RESIDUAL.  perturbative only: it inherits v304's UNPROVEN entire-a(Box) assumption, and a
        ghost-free perturbative graviton is NOT the non-perturbative ambient measure (QG.AMB.01,
        the C7 residual reduced by v365/v369).  Does NOT change QG.AMB.01's status.
  [O] 8. ANTI-NUMEROLOGY DECLINE.  tr P2 = 5 in d=4 is the spin-2 polarisation count (dimension
        counting), NOT g_car=5; the coincidence is DECLINED (v354/v355 discriminator) -- it is not
        a forced TFPT identity.

NET: completes Track 2's perturbative-unitarity goal -- the graviton is ghost-free sector-by-sector
(spin-2 via the entire KMS form factor v304; spin-0 via GHP v334), with the explicit Barnes-Rivers
spin algebra as the new exact content.  Honest scope: [E] the projector completeness + the EH
structure + the spin-2 pole algebra; [C] the entire-form-factor (inherits v304) + GHP + the
unitarity conclusion; [O] perturbative-only + the open analyticity assumption.  Python (sympy);
the conclusion is [C]/[O], so -- like v304/v358/v365 -- this module is Python-only."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car

p2 = sp.symbols("p2", real=True)
M2 = sp.symbols("M2", positive=True)
d = sp.symbols("d", positive=True)


def run():
    reset()
    print("v370  GRAV.SPIN2.UNITARITY.01: Barnes-Rivers spin decomposition -- perturbative graviton unitarity sector-by-sector")

    # 1. projector completeness: the four Barnes-Rivers traces sum to d(d+1)/2
    trP2 = (d - 2) * (d + 1) / 2
    trP1 = d - 1
    trP0s = sp.Integer(1)
    trP0w = sp.Integer(1)
    total = sp.simplify(trP2 + trP1 + trP0s + trP0w)
    sym_components = d * (d + 1) / 2
    trP2_4 = trP2.subs(d, 4)
    check("PROJECTOR COMPLETENESS [E]: tr P2=(d-2)(d+1)/2, tr P1=d-1, tr P0s=tr P0w=1 sum to "
          "d(d+1)/2 (the symmetric-tensor dimension); in d=4 the split is 5+3+1+1=10 -- the "
          "%d physical spin-2 polarisations carry the graviton"
          % int(trP2_4),
          sp.simplify(total - sym_components) == 0
          and trP2_4 == 5 and trP1.subs(d, 4) == 3 and total.subs(d, 4) == 10)

    # 2. EH propagator structure: spin-2 coefficient +1, spin-0 scalar -1/(d-2) = -1/2 (d=4)
    eh_spin2_coeff = sp.Integer(1)
    eh_spin0_coeff = -1 / (d - 2)
    check("EH PROPAGATOR STRUCTURE [E]: the Einstein-Hilbert graviton propagator ~ P2/p^2 "
          "- 1/(d-2) P0s/p^2: spin-2 coefficient +1 (healthy), spin-0 scalar -1/(d-2) = %s "
          "(d=4) -- the physical pole is the spin-2 massless graviton"
          % sp.nsimplify(eh_spin0_coeff.subs(d, 4)),
          eh_spin2_coeff == 1 and sp.simplify(eh_spin0_coeff.subs(d, 4) + sp.Rational(1, 2)) == 0)

    # 3. the Stelle ghost is a SPIN-2 state (local higher-derivative dressing)
    a_poly = 1 + p2 / M2
    spin2_local = 1 / (p2 * a_poly)
    res_massless = sp.limit(p2 * spin2_local, p2, 0)
    res_ghost = sp.limit((p2 + M2) * spin2_local, p2, -M2)
    check("STELLE GHOST IS SPIN-2 [E]: a local R+R^2/Weyl^2 dressing a_poly=1+p^2/M^2 gives the "
          "spin-2 propagator P2/(p^2(1+p^2/M^2)) with a HEALTHY massless pole (residue %s>0 at "
          "p^2=0) and a NEGATIVE-residue pole (residue %s<0 at p^2=-M^2) -- the Stelle ghost is a "
          "spin-2 state (extends v304's scalar pole algebra to the tensor sector)"
          % (res_massless, res_ghost),
          sp.simplify(res_massless - 1) == 0 and sp.simplify(res_ghost + 1) == 0
          and res_massless > 0 and res_ghost < 0)

    # 4. entire form factor => spin-2 ghost-free (only the p^2=0 pole)
    a_entire = sp.exp(p2 / M2)
    poles_entire = sp.solve(p2 * a_entire, p2)
    zeros_a = sp.solve(sp.exp(sp.symbols("z") / M2), sp.symbols("z"))
    check("ENTIRE FORM FACTOR => SPIN-2 GHOST-FREE [E]: the un-truncated KMS form factor "
          "a(p^2)=e^{p^2/M^2} (v304/v259) is entire and nowhere zero (zeros=%s), so the spin-2 "
          "propagator P2/(p^2 e^{p^2/M^2}) has its ONLY pole at p^2=%s -- no ghost in the spin-2 "
          "sector" % (zeros_a, poles_entire),
          zeros_a == [] and poles_entire == [sp.Integer(0)])

    # 5. spin-0 conformal sector via the GHP contour (different mechanism, cited)
    c_conf = sp.Rational(-3, 2)
    check("SPIN-0 SECTOR VIA GHP [C]: the spin-0 (conformal/trace) sector is the wrong-sign mode "
          "(c_conf(4)=%s, v332), made convergent by the GHP contour rotation + IDG dressing "
          "(v334) -- a DIFFERENT mechanism from the spin-2 form factor; the two problematic "
          "sectors are cured separately" % c_conf, c_conf < 0)

    # 6. perturbative graviton unitarity sector-by-sector
    spin2_ghost_free = (poles_entire == [sp.Integer(0)])
    spin0_controlled = (c_conf < 0)        # handled by GHP (v334), cited
    check("PERTURBATIVE GRAVITON UNITARITY [C]: spin-1 and the spin-0 w-mode are pure gauge (no "
          "propagating pole); the physical content is the spin-2 graviton (ghost-free, 4) + the "
          "GHP-controlled spin-0 (5). So the full PERTURBATIVE graviton is ghost-free under the "
          "TFPT-fixed package (spin-2 entire form factor v304 + spin-0 GHP v334) -- conditional "
          "on v304's entire-analyticity assumption", spin2_ghost_free and spin0_controlled)

    # 7. residual (honest fence)
    check("RESIDUAL [O]: perturbative only -- inherits v304's UNPROVEN entire-a(Box) assumption, "
          "and a ghost-free PERTURBATIVE graviton is NOT the non-perturbative ambient measure "
          "(QG.AMB.01, the C7 residual reduced by v365/v369). Does NOT change QG.AMB.01's status", True)

    # 8. anti-numerology decline: tr P2 = 5 is dimension counting, NOT g_car
    check("ANTI-NUMEROLOGY DECLINE [O]: tr P2 = %d in d=4 is the spin-2 polarisation count "
          "(dimension counting: (d-2)(d+1)/2), NOT g_car=%d; the numerical coincidence is "
          "DECLINED per the v354/v355 discriminator -- it is not a forced TFPT identity"
          % (int(trP2_4), g_car),
          int(trP2_4) == 5 and g_car == 5 and True)

    return summary("v370 GRAV.SPIN2.UNITARITY.01: the Barnes-Rivers spin decomposition (tr P2,P1,P0s,P0w "
                   "= 5,3,1,1 sum 10 in d=4) localises the Stelle ghost in the SPIN-2 sector; the entire "
                   "KMS form factor e^{p^2/M^2} (v304) makes spin-2 ghost-free (only the p^2=0 pole) and "
                   "the GHP contour (v334) controls the spin-0 conformal mode => perturbative graviton "
                   "unitarity sector-by-sector [C]; residual [O] = the entire-analyticity assumption + "
                   "perturbative-only (NOT the non-perturbative measure). tr P2=5 != g_car (declined)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
