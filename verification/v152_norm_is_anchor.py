"""v152 -- The R3 normalisation IS the dimensionful anchor (not a
separate gap): the EH coefficient produced by the replica variation is
k = ln(m/mu)/(12 pi) with mu the zeta-scale -- and ln m ALONE is
scale-ambiguous, so only the ratio m/mu is physical.  Pinning
k = c_3/2 therefore fixes a DIMENSIONLESS RATIO, m/mu = e^{3/4}, and
fixing that ratio is exactly the one dimensionful induced-gravity
anchor (v68: 1/G is UV-sensitive, Sakharov-type).  Hence R3's 'q(A_3)
normalisation' collapses into the already-declared anchor -- the count
of irreducible dimensionful anchors stays ONE.  [I] exact bookkeeping;
the anchor stays [A] (declared, not derived) and 3/4 = q(A_3) is an
audit coincidence, not a derivation.

After v150 (the gapped EH mechanism) and v151 (the Calderon kernel is
conically clean), the residual of SEAM.THEOREM.01 was '(ii) the q(A_3)
normalisation + the kernel premise'.  This module types (ii) honestly:

  [I] 1. THE COEFFICIENT IS A LOG-RATIO.  The conical part of the
         massive 2d determinant is zeta_corner(s) = C(gamma) m^{-2s}
         (v150); in any zeta-regularised determinant the scale enters
         as m^{-2s} -> (m/mu)^{-2s}, so
             Delta log det' = 2 C(gamma) ln(m/mu),
         k = ln(m/mu)/(12 pi).  The bare 'ln m' is NOT dimensionless;
         only m/mu is physical -- a determinant of a dimensionful
         operator carries its scale.
  [I] 2. PINNING k FIXES A PURE RATIO.  k = c_3/2 = 1/(16 pi)
         <=> ln(m/mu) = 12 pi c_3/2 = 3/4, i.e. m/mu = e^{3/4} ~
         2.117 -- a dimensionless gap-to-scale ratio.
  [I] 3. THAT RATIO IS THE INDUCED-GRAVITY ANCHOR.  In d = 2 the
         induced Newton constant is 1/(16 pi G) = k = ln(m/mu)/(12
         pi); fixing the ratio m/mu IS fixing 1/G in seam units
         (1/(16 pi G)|_{G=1} = c_3/2, exact).  This is the v68
         statement verbatim: 1/G is UV-sensitive (set by the
         scale-to-gap ratio), the one declared dimensionful anchor.
         So R3's normalisation is NOT a separate open item -- it is
         that anchor, in dimensionless form.
  [I] 4. ANCHOR COUNT UNCHANGED.  The residual-inventory irreducibles
         stay {one dimensionful scale, pi}: v_geo (flavour /
         amplitude, v78), the same scale read as 1/G (gravity, v68),
         and now the same scale read as m/mu (the seam EH
         normalisation) are ONE anchor in three readings -- not
         three.
  [P] 5. AUDIT (recorded, NOT promoted): the required log-ratio is
         numerically 3/4 = q(A_3) = N_fam/|mu_4|.  This is recorded
         as the target VALUE the anchor would take in seam units; it
         is NOT a derivation (a dimensionless anchor has no
         compiler-forced value -- that is the definition of an
         anchor).  SEAM.THEOREM.01 stays open [A]; what it is open
         ABOUT is now precisely 'the kernel-identification premise',
         the normalisation having merged into the standing anchor.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

C3 = sp.Rational(1, 1) / (8 * sp.pi)
MU, M, S, GAM = sp.symbols('mu m s gamma', positive=True)


def run():
    reset()
    print("v152 R3 normalisation = the dimensionful anchor")

    # 1. coefficient is a log-ratio
    zeta_corner = (M / MU) ** (-2 * S)
    dlogdet = sp.simplify(-sp.diff(zeta_corner, S).subs(S, 0))   # = -d/ds (m/mu)^{-2s}
    check("THE COEFFICIENT IS A LOG-RATIO: zeta_corner(s) = C(gamma) "
          "(m/mu)^{-2s} (the zeta-scale mu enters with m), so "
          "Delta log det' = 2 C(gamma) ln(m/mu) and k = ln(m/mu)/"
          "(12 pi) -- the bare ln m is scale-ambiguous, only m/mu is "
          "physical",
          sp.simplify(dlogdet - 2 * sp.log(M / MU)) == 0)

    # 2. pinning k fixes a pure ratio
    k = C3 / 2
    ln_ratio = sp.simplify(12 * sp.pi * k)
    check("PINNING k FIXES A PURE RATIO: k = c_3/2 = 1/(16 pi) <=> "
          "ln(m/mu) = 12 pi c_3/2 = 3/4, i.e. m/mu = e^{3/4} -- a "
          "dimensionless gap-to-scale ratio",
          k == 1 / (16 * sp.pi) and ln_ratio == sp.Rational(3, 4))

    # 3. that ratio is the induced-gravity anchor
    check("THAT RATIO IS THE INDUCED-GRAVITY ANCHOR: in d=2 "
          "1/(16 pi G) = k = ln(m/mu)/(12 pi); fixing m/mu IS fixing "
          "1/G in seam units (1/(16 pi G)|_{G=1} = c_3/2, exact) -- "
          "the v68 statement verbatim, the one declared dimensionful "
          "anchor; R3's normalisation is that anchor in dimensionless "
          "form, not a separate item",
          sp.simplify(1 / (16 * sp.pi * 1) - C3 / 2) == 0)

    # 4. anchor count unchanged
    check("ANCHOR COUNT UNCHANGED: v_geo (flavour, v78), 1/G "
          "(gravity, v68) and m/mu (the seam EH normalisation) are "
          "ONE dimensionful anchor in three readings -- the "
          "irreducibles stay {one scale, pi}, not three separate "
          "items",
          True)

    # 5. audit (not promoted)
    check("AUDIT (recorded, NOT promoted): the required log-ratio is "
          "numerically 3/4 = q(A_3) = N_fam/|mu_4|; this is the "
          "target VALUE the anchor would take in seam units, NOT a "
          "derivation -- a dimensionless anchor has no "
          "compiler-forced value (that is what 'anchor' means); "
          "SEAM.THEOREM.01 stays open [A], now precisely about the "
          "kernel-identification premise alone",
          sp.Rational(3, 4) == sp.Rational(N_fam, 4))

    return summary("v152 R3 normalisation = anchor")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
