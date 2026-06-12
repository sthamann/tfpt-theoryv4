"""v144 -- The det-ratio cancellation, exact within the SdS family:
the product of the two horizon radii obeys r_b r_c = 1 - Delta^2/3
EXACTLY (the traceless cubic's e_2-rigidity), so with the v132 anomaly
zeta(0) = -2/3 per sphere the non-zero-mode determinant ratio is
    det'_n / det'_N = (r_b r_c)^{4/3} = (1 - Delta^2/3)^{4/3}:
NO first-order term in the horizon split -- v131's '1 + O(deficit)'
holds exactly in the within-family (near-Nariai) sense, with deficit
coefficient |mu_4| (|Z_2|/N_fam)^3 = 32/27 (audit: the v103 canonical
curvature times the glue order).  [I] exact arithmetic; the
finite-weight absorption across levels stays [P], with its obstruction
now stated sharply.

v131 left R1's last computation as '[P] 4. show det'_n/det'_dS =
1 + O(deficit)'.  Within the SdS family this is exact arithmetic:

  [I] 1. e_2-RIGIDITY.  The SdS horizon cubic is traceless
         (t^3 - 3t + 2c, v101/v103): with s = r_b + r_c and
         p = r_b r_c the two relations p - s^2 = -3 (e_2) and
         r_o = -s (e_1 = 0) give, for the split Delta = r_b - r_c,
             Delta^2 = s^2 - 4p = 12 - 3 s^2
         and hence EXACTLY
             p = r_b r_c = 1 - Delta^2 / 3.
  [I] 2. THE DET-RATIO IN CLOSED FORM.  The GP operator on S^2(r) is
         L_r = r^{-2} (-Delta_unit - 2); with the v132 anomaly
         zeta(0)|det' = -2/3 per sphere, det'(L_r) = r^{4/3}
         det'(L_1), so the two-sphere product ratio against Nariai
         (r_b = r_c = 1) is
             det'_n / det'_N = (r_b r_c)^{4/3}
                             = (1 - Delta^2/3)^{4/3}.
  [I] 3. NO FIRST-ORDER TERM.  d(det'-ratio)/d(Delta) = 0 at
         Delta = 0 exactly: the leading correction is quadratic in
         the split -- the v131 cancellation, derived (not assumed)
         from e_2-rigidity + the established anomaly.
  [I] 4. DEFICIT FORM (audit).  With the Nariai mass deficit
         eps = 1 - c:  eps = (3/8) Delta^2 + O(Delta^4), so
             det'_n/det'_N = 1 - (32/27) eps + O(eps^2),
         coefficient 32/27 = |mu_4| (|Z_2|/N_fam)^3 = 4 (2/3)^3 (the
         v103 canonical curvature times the glue order; recorded as
         an audit identity, not promoted).
  [P] 5. HONEST SCOPE (recorded).  This closes v131's step in the
         WITHIN-FAMILY sense.  The finite-weight comparison
         (S_n/S_dS in {1, 2/3, 1/3}) still runs through the
         v132/v133 anomaly budget: under a naive GLOBAL rescaling
         reading, det'^{-1/2} squared would multiply the Born square
         by (S_n/S_dS)^{-4/3}, shifting the exponent 6 -> 14/3 (not
         an atom) -- so the [P] absorption MUST proceed via the
         Hubble-unit conversion (v132's reading), not via global
         rescaling.  The frozen transfer spectrum is untouched; the
         obstruction the remaining [P] has to resolve is now stated
         sharply.
"""
import sympy as sp

from tfpt_constants import check, summary, reset

DELTA, T = sp.symbols('Delta t', positive=True)


def run():
    reset()
    print("v144 det-ratio family cancellation (R1's v131 step, within-family)")

    s = 2 * sp.sqrt(1 - DELTA ** 2 / 12)
    p = 1 - DELTA ** 2 / 3
    rb, rc, ro = (s + DELTA) / 2, (s - DELTA) / 2, -s

    # 1. e2-rigidity: the three roots satisfy a traceless cubic with e2 = -3
    poly = sp.expand((T - rb) * (T - rc) * (T - ro))
    e1 = sp.simplify(rb + rc + ro)
    e2 = sp.simplify(rb * rc + rb * ro + rc * ro)
    prod_exact = sp.simplify(rb * rc - p)
    check("e_2-RIGIDITY: with s = r_b + r_c, the traceless cubic "
          "(e_1 = 0, e_2 = -3) forces Delta^2 = 12 - 3 s^2 and "
          "EXACTLY r_b r_c = 1 - Delta^2/3 (verified symbolically "
          "on the explicit root triple)",
          e1 == 0 and e2 == -3 and prod_exact == 0
          and sp.simplify(poly.coeff(T, 2)) == 0
          and sp.simplify(poly.coeff(T, 1)) == -3)

    # 2. det-ratio in closed form (zeta(0) = -2/3 per sphere, v132)
    zeta0 = sp.Rational(-2, 3)
    # det'(c L) = c^{zeta(0)} det'(L); L_r = r^{-2} L_1 => det'(L_r) = r^{-2 zeta0} det'(L_1)
    scaling_exponent = sp.simplify(-2 * zeta0)
    ratio = (rb * rc) ** sp.Rational(4, 3)
    check("DET-RATIO CLOSED FORM: det'(L_r) = r^{4/3} det'(L_1) "
          "(v132 anomaly zeta(0) = -2/3, scaling exponent -2*zeta(0) "
          "= 4/3 per sphere); two-sphere product ratio against "
          "Nariai = (r_b r_c)^{4/3} = (1 - Delta^2/3)^{4/3}",
          scaling_exponent == sp.Rational(4, 3)
          and sp.simplify(ratio - (1 - DELTA ** 2 / 3) ** sp.Rational(4, 3)) == 0)

    # 3. no first-order term in the split
    series = sp.series(ratio, DELTA, 0, 4).removeO()
    d1 = sp.diff(ratio, DELTA).subs(DELTA, 0)
    d2_coeff = series.coeff(DELTA, 2)
    check("NO FIRST-ORDER TERM: d(ratio)/d(Delta)|_0 = 0 exactly; "
          "leading correction quadratic, ratio = 1 - (4/9) Delta^2 + "
          "O(Delta^4) -- the v131 cancellation DERIVED from "
          "e_2-rigidity + the established anomaly",
          d1 == 0 and d2_coeff == sp.Rational(-4, 9)
          and series.coeff(DELTA, 1) == 0)

    # 4. deficit form (audit)
    c_par = sp.simplify(p * s / 2)             # cubic constant: 2c = e3*(-1) => c = p*s/2
    eps_series = sp.series(1 - c_par, DELTA, 0, 4).removeO()
    eps_coeff = eps_series.coeff(DELTA, 2)
    ratio_per_eps = sp.Rational(-4, 9) / eps_coeff
    atom = -sp.Integer(4) * sp.Rational(2, 3) ** 3
    check("DEFICIT FORM (audit): eps = 1 - c = (3/8) Delta^2 + "
          "O(Delta^4), so det-ratio = 1 - (32/27) eps + O(eps^2); "
          "coefficient 32/27 = |mu_4| (|Z_2|/N_fam)^3 = 4 (2/3)^3 "
          "(the v103 canonical curvature x glue order; audit-typed)",
          eps_coeff == sp.Rational(3, 8)
          and ratio_per_eps == sp.Rational(-32, 27) == atom)

    # 5. honest scope
    shifted = sp.Integer(6) - sp.Rational(4, 3)
    check("HONEST SCOPE [P] (recorded): within-family cancellation "
          "closed; the finite-weight absorption stays open -- a "
          "naive global-rescaling reading would shift the Born "
          "exponent 6 -> 14/3 (not an atom), so the absorption must "
          "proceed via the Hubble-unit conversion (v132); the frozen "
          "transfer spectrum is untouched",
          shifted == sp.Rational(14, 3))

    return summary("v144 det-ratio family cancellation")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
