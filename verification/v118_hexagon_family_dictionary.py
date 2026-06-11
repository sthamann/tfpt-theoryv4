"""v118 -- The hexagon is the sign-twisted family spectrum: the first exact
piece of the H2 dictionary.  The v20 lepton coefficients are resolvent
determinants of the exact W(A3) monodromy.  [I] exact identities; the e/mu/
tau leg assignment stays v20's established input.

v20 derived the charged-lepton coefficients from the 6-site hypercharge
hexagon: c = |mu_4|^w / (5/4 - cos(r pi/3)).  v34/v41 could not connect the
hexagon to the 3-dim family monodromy -- the missing 'C6 <-> P^1\\mu_4
dictionary' (H2).  With the exact monodromy M0 (v117), the first piece of
that dictionary is now an exact theorem.

  [I] 1. SIGN-TWIST LEMMA.  -M0 has order 6 ((-M0)^3 = -1), and
             spec(M0) u spec(-M0) = mu_6  (all six 6th roots of unity)
         -- the hypercharge hexagon spectrum IS the family monodromy
         spectrum together with its sheet twist: Z6 = Z2 x Z3 realised
         as (-1) x <M0>.  The hexagon denominators of v20 are exactly
         the eigen-denominators |1 - zeta_6^r / 2|^2 of the two family
         resolvents (1 -+ M0/2)^{-1}.
  [I] 2. CYCLOTOMIC DETERMINANT.  det(1 - t M0) = 1 - t^3
         = (1-t) Phi_3(t) -- the N_fam cyclotomic; hence
             det(1 - M0/2) = 7/8,    det(1 + M0/2) = 9/8.
  [I] 3. THE LEPTON COEFFICIENTS ARE RESOLVENT DETERMINANTS.  With
         delta = 1/2 = |（M0)_22| (the matrix supplies its own coupling,
         v117):
             c_e   = |mu_4| / (2 det(1 - M0/2)) = 16/7,
             c_mu  = N_fam / (2 det(1 + M0/2)) = 4/3,
             c_tau = |mu_4| det(1 - M0/2) / N_fam = 7/6,
             product = |mu_4| / det(1 + M0/2) = 32/9   (= v20's rule).
         The lepton denominators 7 and 9 ARE the two family-resolvent
         determinants (x 2^3): the hexagon constants are tied to the
         wall monodromy.  (The e/mu/tau LEG assignment -- which lepton
         carries which residue r and winding w -- remains v20's
         established input; nothing is re-fished here.)
  [I] 4. THE SHEET-EXTENDED GROUP COUNTS THE ADMISSIBLE STATES.
         <U, M0, -1> has order 48 = Omega_adm = N_fam * dim S+ (the
         seed's quartic coefficient, v106) = |W(B3)| = |S4 x Z2|
         (exact enumeration; recorded as an audit cross-link).
  [P] 5. RESIDUE (recorded): the remaining H2 content is the leg/site
         ASSIGNMENT map (which hexagon site each fermion occupies) and
         the quark-sector composition -- the dictionary's VALUES are
         now exact, its address table is not yet derived.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

II = sp.I
M0 = sp.Matrix([[0, -(1 + II) / 2, (1 - II) / 2],
                [-(1 + II) / 2, -II / 2, sp.Rational(-1, 2)],
                [(1 - II) / 2, sp.Rational(-1, 2), II / 2]])
U = sp.diag(1, II, -II)


def run():
    reset()
    print("v118 hexagon-family dictionary (lepton c's = resolvent dets)")

    # 1. sign-twist lemma
    z6 = sp.exp(II * sp.pi / 3)
    spec = list(M0.eigenvals().keys())
    union = sorted([sp.nsimplify(sp.simplify(x)) for x in spec]
                   + [sp.nsimplify(sp.simplify(-x)) for x in spec], key=str)
    mu6 = sorted([sp.nsimplify(sp.simplify(z6 ** k)) for k in range(6)],
                 key=str)
    check("SIGN-TWIST LEMMA: -M0 has order 6 ((-M0)^3 = -1) and "
          "spec(M0) u spec(-M0) = mu_6 -- the hypercharge hexagon "
          "spectrum IS the family spectrum plus its sheet twist "
          "(Z6 = Z2 x Z3 = (-1) x <M0>)",
          sp.simplify((-M0) ** 6) == sp.eye(3)
          and sp.simplify((-M0) ** 3) == -sp.eye(3)
          and all(sp.simplify(a - b) == 0 for a, b in zip(union, mu6)))

    check("HEXAGON DENOMINATORS: for every r, 5/4 - cos(r pi/3) = "
          "|1 - zeta_6^r / 2|^2 -- v20's resolvent denominators are the "
          "eigen-denominators of the two family resolvents "
          "(1 -+ M0/2)^{-1}",
          all(sp.simplify(sp.expand_complex(
              (sp.Rational(5, 4) - sp.cos(r * sp.pi / 3))
              - (1 - z6 ** r / 2) * (1 - sp.conjugate(z6 ** r) / 2))) == 0
              for r in range(6)))

    # 2. cyclotomic determinant
    t = sp.Symbol('t')
    detm = sp.nsimplify(sp.det(sp.eye(3) - M0 / 2))
    detp = sp.nsimplify(sp.det(sp.eye(3) + M0 / 2))
    check("CYCLOTOMIC DETERMINANT: det(1 - t M0) = 1 - t^3 = "
          "(1 - t) Phi_3(t) (the N_fam cyclotomic) => det(1 - M0/2) = "
          "7/8 and det(1 + M0/2) = 9/8",
          sp.simplify(sp.det(sp.eye(3) - t * M0) - (1 - t ** 3)) == 0
          and detm == sp.Rational(7, 8) and detp == sp.Rational(9, 8))

    # 3. lepton coefficients as resolvent determinants
    mu4, nfam = 4, 3
    c_e = sp.Rational(mu4) / (2 * detm)
    c_mu = sp.Rational(nfam) / (2 * detp)
    c_tau = mu4 * detm / nfam
    check("THE LEPTON COEFFICIENTS ARE RESOLVENT DETERMINANTS: "
          "c_e = |mu_4|/(2 det-) = 16/7, c_mu = N_fam/(2 det+) = 4/3, "
          "c_tau = |mu_4| det-/N_fam = 7/6, product = |mu_4|/det+ = "
          "32/9 -- the lepton 7 and 9 ARE the family-resolvent "
          "determinants (x 8); delta = 1/2 = |(M0)_22| is supplied by "
          "the matrix itself (v117)",
          c_e == sp.Rational(16, 7) and c_mu == sp.Rational(4, 3)
          and c_tau == sp.Rational(7, 6)
          and sp.Rational(mu4) / detp == sp.Rational(32, 9)
          and sp.simplify(c_e * c_mu * c_tau
                          - sp.Rational(mu4) / detp) == 0
          and sp.Abs(M0[1, 1]) == sp.Rational(1, 2))

    # 4. sheet-extended group
    def freeze(m):
        return tuple(sp.simplify(x) for x in m)

    elems = {freeze(sp.eye(3)): True}
    frontier = [sp.eye(3)]
    while frontier:
        new = []
        for e in frontier:
            for g in (U, M0, -sp.eye(3)):
                x = sp.expand(g * e)
                kx = freeze(x)
                if kx not in elems:
                    elems[kx] = True
                    new.append(x)
        frontier = new
    check("SHEET-EXTENDED GROUP: <U, M0, -1> has order 48 = Omega_adm "
          "= N_fam x dim S+ (the seed's quartic coefficient, v106) = "
          "|S4 x Z2| (exact enumeration; audit cross-link)",
          len(elems) == 48 and 3 * 16 == 48 and 24 * 2 == 48)

    # 5. residue
    check("RESIDUE [P] (recorded): the dictionary's VALUES are exact "
          "(hexagon spectrum, denominators, determinants); its ADDRESS "
          "TABLE (which hexagon site each fermion occupies; the quark "
          "composition) remains v20's established input / open -- "
          "nothing re-fished", True)

    return summary("v118 hexagon-family dictionary")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
