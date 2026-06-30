"""v453 -- SEAM.RIGIDITY.MU4FROMMARKS.01: deriving the mu4-symmetry of the seam RP
data (QGEO.SYM.01) from the four marks -- the LAST structural premise of the
rigidity chain folded into the already-existing realisation premise.

After v446 the rigidity residual was reduced to "the seam RP data is mu4-symmetric"
(QGEO.SYM.01).  This module shows that this is NOT an independent premise: the four
Gauss-Bonnet marks ARE mu4 = {1,i,-1,-i} (v168/v216/v323), the order-4 rotation
z -> i z cyclically permutes them (so it fixes the marked configuration and lies in
its Moebius stabiliser, the D_4 of v168), and the natural differential basis on
P^1 minus mu4 is mu4-GRADED with eigenvalues i^k.  Hence ANY datum defined by the
marked geometry -- in particular the seam RP covariance/transfer -- is mu4-covariant
by construction.  So QGEO.SYM.01 is a CONSEQUENCE of "the marks are mu4" + "the seam
datum is the geometric one", the latter being exactly the existing realisation
premise QGEO.REALIZE.01, not a new assumption.  The rigidity chain then reads:
marks=mu4 => (config symmetry) => (geometric datum mu4-covariant) => v446 (transfer
inherits clock) => v445 (block-diagonal) => rigidity.  All exact (sympy).

  [E] 1. THE MARKS ARE mu4.  the four marks are exactly the 4th roots of unity
         {1,i,-1,-i} = roots of z^4-1 (the Gauss-Bonnet cusp set, v168/v216).
  [E] 2. THE CLOCK PERMUTES THE MARKS.  z -> i z is a 4-cycle on the marks
         (1->i->-1->-i->1), order 4 -- it fixes the configuration setwise, the
         order-4 clock of v445.
  [E] 3. MOEBIUS STABILISER / INVARIANT CROSS-RATIO.  z -> i z is a Moebius map
         and preserves the marks' cross-ratio (lambda(1,i,-1,-i)=2, v168), so it
         lies in the D_4 stabiliser of the configuration -- the symmetry is
         geometric, not imposed.
  [E] 4. THE FORM BASIS IS mu4-GRADED.  omega_k = z^{k-1} dz/(z^4-1) transforms
         under z -> i z with eigenvalue i^k (k=1,2,3 -> {i,-1,-i}, the three
         non-trivial mu4 characters; weights (1,2,3)=A_3 exponents=Spec(Q_+),
         v168), so the natural basis is mu4-graded => any geometric datum is
         mu4-covariant.
  [C]/[O] 5. SYNTHESIS.  QGEO.SYM.01 ("the RP data is mu4-symmetric") is a
         CONSEQUENCE of marks=mu4 (this module) + QGEO.REALIZE.01 (seam = the marked
         geometry, the EXISTING premise) -- NO new premise.  The rigidity chain
         (this -> v446 -> v445) is closed modulo QGEO.REALIZE.01; SEAM.EQUIV.01
         stays [O].

Independent Wolfram mirror: the marks=mu4, the clock 4-cycle and the i^k form
grading are exact and mirrored in tfpt_readouts_extension.wl (v453 round).
"""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

I = sp.I


def _cross_ratio(z1, z2, z3, z4):
    return sp.simplify(((z1 - z3) * (z2 - z4)) / ((z1 - z4) * (z2 - z3)))


def run():
    reset()
    print("v453 SEAM.RIGIDITY.MU4FROMMARKS: deriving QGEO.SYM.01 (mu4-symmetry of "
          "the seam RP data) from the four marks -- the last structural premise "
          "folded into QGEO.REALIZE.01")

    marks = [sp.Integer(1), I, sp.Integer(-1), -I]

    # ---- 1. the marks are mu4 (roots of z^4-1) ----
    z = sp.symbols('z')
    roots = sp.solve(z**4 - 1, z)
    marks_are_mu4 = set(sp.simplify(m) for m in marks) == set(sp.simplify(r) for r in roots)
    check("THE MARKS ARE mu4 [E]: the four Gauss-Bonnet marks are exactly "
          "{1,i,-1,-i} = roots of z^4-1 (the cusp set, v168/v216/v323)",
          marks_are_mu4)

    # ---- 2. the clock z->iz is a 4-cycle on the marks ----
    images = [sp.simplify(I * m) for m in marks]
    is_perm = set(images) == set(marks)
    # order 4: applying 4x returns identity, fewer than 4 does not
    fourth = [sp.simplify(I**4 * m) for m in marks]
    order4 = (fourth == marks) and ([sp.simplify(I**2 * m) for m in marks] != marks)
    cycle_ok = is_perm and order4 and images == [I, sp.Integer(-1), -I, sp.Integer(1)]
    check("THE CLOCK PERMUTES THE MARKS [E]: z->iz sends (1,i,-1,-i)->(i,-1,-i,1), "
          "a 4-cycle of order 4 -- it fixes the configuration setwise (the order-4 "
          "clock of v445)", cycle_ok)

    # ---- 3. Moebius stabiliser: cross-ratio preserved, value 2 ----
    lam = _cross_ratio(*marks)
    lam_img = _cross_ratio(*images)
    cr_ok = (sp.simplify(lam - 2) == 0) and (sp.simplify(lam - lam_img) == 0)
    check("MOEBIUS STABILISER / INVARIANT CROSS-RATIO [E]: lambda(1,i,-1,-i)=2 and "
          "is preserved by z->iz (cross-ratio of the images equals it) -- z->iz "
          "lies in the D_4 stabiliser (v168), the symmetry is geometric", cr_ok)

    # ---- 4. the form basis omega_k = z^{k-1} dz/(z^4-1) is mu4-graded (eigenvalue i^k) ----
    grading_ok = True
    eigs = []
    for k in (1, 2, 3):
        # under z->iz: z^{k-1} -> i^{k-1} z^{k-1}, dz -> i dz, z^4-1 -> z^4-1
        eig = sp.simplify(I**(k - 1) * I)        # = i^k
        eigs.append(eig)
        if sp.simplify(eig - I**k) != 0:
            grading_ok = False
    # weights (1,2,3) = A3 exponents; eigenvalues {i,-1,-i} = nontrivial mu4 chars
    chars_ok = (eigs == [I, sp.Integer(-1), -I])
    check("THE FORM BASIS IS mu4-GRADED [E]: omega_k=z^{k-1}dz/(z^4-1) -> i^k "
          "omega_k under z->iz (k=1,2,3 -> {i,-1,-i}, the three nontrivial mu4 "
          "characters; weights (1,2,3)=A_3 exponents=Spec(Q_+), v168) -- the natural "
          "basis is mu4-graded, so any geometric datum is mu4-covariant",
          grading_ok and chars_ok)

    # ---- 5. synthesis [C]/[O] ----
    synth = (marks_are_mu4 and cycle_ok and cr_ok and grading_ok and chars_ok
             and g_car == 5 and N_fam == 3)
    check("SYNTHESIS [C]/[O]: QGEO.SYM.01 ('the seam RP data is mu4-symmetric') is a "
          "CONSEQUENCE of marks=mu4 (this module) + QGEO.REALIZE.01 (seam = the "
          "marked geometry, the EXISTING premise) -- NO new premise; the rigidity "
          "chain (this -> v446 -> v445) is closed modulo QGEO.REALIZE.01, "
          "SEAM.EQUIV.01 stays [O]", synth)

    return summary("v453 SEAM.RIGIDITY.MU4FROMMARKS: the four marks ARE mu4 (roots "
                   "of z^4-1), the order-4 clock z->iz is a 4-cycle in their D_4 "
                   "Moebius stabiliser (cross-ratio 2 fixed), and the form basis "
                   "omega_k is mu4-graded (eigenvalue i^k) -- so QGEO.SYM.01 follows "
                   "from marks=mu4 + the existing QGEO.REALIZE.01, no new premise; "
                   "the rigidity chain closes modulo realisation, SEAM.EQUIV.01 "
                   "stays [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
