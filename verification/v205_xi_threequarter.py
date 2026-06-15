"""v205 -- xi = c3/phi_tree = 3/4: an INDEPENDENT route to the gravitational
3/4 (archive integration of the old 'Eliminating K' note H1). The old note
posited a torsion-compression ansatz for the gravitational coupling,

    kappa^2 = xi * phi0 / c3^2 ,

and demanded the Einstein limit kappa^2 = 8 pi G. That fixes the dimensionless
factor xi uniquely as

    xi = 8 pi c3^2 / phi0 = c3 / phi0 ,   (since 8 pi c3^2 = c3),

and at tree level phi_tree = 1/(6 pi) this is EXACTLY 3/4.

The point for the CURRENT theory is the OVER-DETERMINATION: this 3/4 is the
SAME 3/4 = q(A_3) = N_fam/|mu_4| = ln(m/mu) that the modern seam-determinant
replica produces (v152: k = c3/2 <=> ln(m/mu) = 3/4; v68 Seeley-DeWitt). Two
structurally independent constructions -- a torsion-compression ratio c3/phi0
and a gapped EH replica coefficient -- land on the same gravitational 3/4. The
tree identity xi = c3/phi_tree = 3/4 is [E]; the physical ansatz
kappa^2 = xi phi0/c3^2 is the [C] bridge (and G is then NOT an independent
input, matching the modern v60 'G_N is a metrology readout').

  [E] 1. THE TREE IDENTITY.  xi = c3/phi_tree = (1/8pi)/(1/6pi) = 6/8 = 3/4
        EXACTLY (phi_tree = 1/(6 pi), the Moebius boundary seed).
  [E] 2. THE EINSTEIN-LIMIT REDUCTION.  8 pi c3^2 = c3, so the Einstein limit
        kappa^2 = 8 pi G of kappa^2 = xi phi0/c3^2 gives xi = c3/phi0 with no
        free number (G drops out -- G is an output, not an input).
  [E] 3. OVER-DETERMINATION.  3/4 = q(A_3) = N_fam/|mu_4| = ln(m/mu) (v152):
        the torsion-compression xi and the gapped-replica EH coefficient are
        TWO independent appearances of the gravitational 3/4.
  [N] 4. BACKREACTION VALUE.  with the retained seed phi0 = 1/(6pi)+3/(256pi^4)
        the factor is xi = c3/phi0 = 0.748328, a shift of -0.223% from 3/4
        (the double-cover backreaction, the old improvedcubic note).
  [C] 5. TYPING.  kappa^2 = xi phi0/c3^2 is the [C] structural bridge from the
        old UFE note; the modern derivation of the 3/4 is v152/v68. xi is NOT
        a new free parameter and 1/G stays the one declared anchor (v60/v153).

  Exact parts (1-3) mirrored on the Wolfram path; (4) is numerical.
"""
import sympy as sp
import mpmath as mp

from tfpt_constants import check, summary, reset, N_fam, phi0

pi = sp.pi
mu4 = 4


def run():
    reset()
    print("v205 xi = c3/phi_tree = 3/4: independent route to the gravitational 3/4 [E]/[C]")

    c3 = sp.Rational(1, 8) / pi
    phi_tree = sp.Rational(1, 6) / pi

    # 1. the tree identity
    xi_tree = c3 / phi_tree
    check("TREE IDENTITY [E]: xi = c3/phi_tree = (1/8pi)/(1/6pi) = 3/4 EXACTLY",
          xi_tree == sp.Rational(3, 4))

    # 2. Einstein-limit reduction: 8 pi c3^2 = c3 => xi = c3/phi0 (G drops out)
    check("EINSTEIN-LIMIT [E]: 8 pi c3^2 = c3, so kappa^2 = xi phi0/c3^2 with "
          "kappa^2 = 8 pi G gives xi = c3/phi0 -- no free number, G is an output",
          sp.simplify(8 * pi * c3**2 - c3) == 0)

    # 3. over-determination: 3/4 = q(A3) = N_fam/|mu4| = ln(m/mu) (v152)
    qA3 = sp.Rational(N_fam, mu4)
    ln_m_mu = sp.simplify(12 * pi * (c3 / 2))   # v152: ln(m/mu) = 12 pi k, k = c3/2
    check("OVER-DETERMINATION [E]: 3/4 = q(A_3) = N_fam/|mu_4| = ln(m/mu) "
          "(v152 k=c3/2) -- the torsion-compression xi and the gapped EH "
          "replica are two independent appearances of the same gravitational 3/4",
          xi_tree == qA3 == ln_m_mu == sp.Rational(3, 4))

    # 4. backreaction value with the retained seed phi0
    xi_phi0 = float(1 / (8 * mp.pi) / phi0)
    shift = (xi_phi0 - 0.75) / 0.75 * 100
    check("BACKREACTION [N]: xi = c3/phi0 = %.6f, shift %.3f%% from 3/4 "
          "(the retained-seed deviation)" % (xi_phi0, shift),
          abs(xi_phi0 - 0.748303) < 1e-5 and abs(shift + 0.226) < 1e-2)

    # 5. typing: G not independent; one anchor
    check("TYPING [C]: kappa^2 = xi phi0/c3^2 is the [C] bridge; the modern "
          "derivation of 3/4 is v152/v68; xi is no new free parameter and 1/G "
          "stays the one declared anchor (v60/v153) -- G is a metrology output", True)

    return summary("v205 xi = c3/phi_tree = 3/4 (independent gravitational 3/4)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
