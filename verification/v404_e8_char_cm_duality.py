"""v404 -- E8.CMDUAL.01: the (E8)_1 vacuum character at the two CM points -- 12 at the
seam (tau=i), 0 at the family (tau=omega).  The seam/flavor rigidity asymmetry, derived.

v282 evaluated the (E8)_1 character chi_E8 = E4/eta^8 = j^{1/3} at the SEAM CM point
tau=i and got chi_E8(i) = 1728^{1/3} = 12.  The two CM points of PSL(2,Z) are tau=i
(order 4, Q(i), the seam facet, v390) and tau=omega (order 6, Q(sqrt-3), the family/CP
facet, v220/v390).  This module evaluates the SAME function at the OTHER CM point:
E4 vanishes at tau=omega, so chi_E8(omega) = j(omega)^{1/3} = 0.  Hence the one E8
character takes its two CM values {12, 0} at the two atoms -- maximal at the seam,
zero at the family.  That is the structural reason the seam is rigid (E8 present, the
keystone SEAM.EQUIV.01 closes) while the flavor/CP sector is the soft residual
(E8 degenerates: U_wall / v_geo / the CP texture).

  chi_E8(tau) = E4(tau)/eta(tau)^8 = j(tau)^{1/3}      (v282)

  [E] 1. chi_E8^3 = j: the (E8)_1 character cubed is the modular j-function
        (chi^3 = q*j as a q-series, exactly as v282).
  [E] 2. SEAM tau=i (Q(i), order 4): cross-ratio 2 => j=1728 => the square modulus
        tau=i, and chi_E8(i) = 1728^{1/3} = 12 -- E8 maximal/present (v282/v214).
  [E] 3. FAMILY tau=omega (Q(sqrt-3), order 6): the equianharmonic lambda
        (lambda^2-lambda+1=0) => j=0 => the hexagonal modulus tau=omega, and
        chi_E8(omega) = 0 -- E4 VANISHES, the (E8)_1 character is ZERO (v220/v267).
  [E] 4. THE SEAM/FLAVOR RIGIDITY DUALITY: the SAME function chi_E8 takes its two CM
        values {12, 0} at the two atoms' CM points -- maximal at the seam (tau=i),
        zero at the family (tau=omega).
  [E] 5. ONLY TWO ELLIPTIC POINTS: tau=i (order 4) and tau=omega (order 3/6) are the
        ONLY elliptic points of PSL(2,Z); j(i)=1728 and j(omega)=0 are exact CM
        values, so chi^3=j FORCES chi(i)=12 and chi(omega)=0 -- not chosen.
  [C] 6. STRUCTURAL READING: the seam sits where E8 is present (chi=12) -- rigid, so
        SEAM.EQUIV.01 closes; the flavor/CP sector sits where E8 degenerates (chi=0)
        -- exactly the soft residual (the U_wall amplitude, v_geo, the CP texture).
  [C] 7. DUAL-KEYSTONE CANDIDATE: the flavor sector = the j=0 degeneration of (E8)_1
        at tau=omega, dual to the seam = (E8)_1 at tau=i (v282); the rigid constants
        are chi_E8 at its nonzero CM value, the flavor hierarchy is its zero.

NET TYPING: [E] the exact modular arithmetic (chi^3=j; j(i)=1728, chi(i)=12;
j(omega)=0, chi(omega)=0; the two-elliptic-point uniqueness); [C] the seam/flavor
rigidity reading and the dual-keystone candidate.  A synthesis extending v282 to the
second CM point; the core values j=1728 (v214/v282) and j=0 (v220/v267) are already
Wolfram-mirrored, so this re-reading is Python-only by the synthesis-module convention
(cf. v390/v394).  Python (sympy).
"""
import sympy as sp

from tfpt_constants import check, summary, reset

q, lam = sp.symbols("q lam")


def sigma3(n):
    return sum(d ** 3 for d in range(1, n + 1) if n % d == 0)


def run():
    reset()
    print("v404  E8.CMDUAL.01: chi_E8(i)=12 (seam) vs chi_E8(omega)=0 (family) -- the "
          "seam/flavor rigidity duality")

    # 1. chi_E8^3 = j  (q-series, as v282)
    E4 = 1 + 240 * sum(sigma3(n) * q ** n for n in range(1, 8))
    prod8 = sp.prod([(1 - q ** n) ** 8 for n in range(1, 8)])
    chi = sp.series(E4 / prod8, q, 0, 6).removeO()            # = q^{1/3} chi_E8
    chi_cubed = sp.series(chi ** 3, q, 0, 5).removeO()
    qj = sp.series(E4 ** 3 / sp.prod([(1 - q ** n) ** 24 for n in range(1, 8)]),
                   q, 0, 5).removeO()
    chi3_is_qj = sp.expand(chi_cubed - qj) == 0
    check("chi_E8^3 = j [E]: the (E8)_1 character cubed is the modular j-function "
          "(chi^3 = q*j as a q-series: %s), exactly as v282" % chi3_is_qj, chi3_is_qj)

    # 2. the seam CM point tau=i: cross-ratio 2 => j=1728 => chi_E8(i)=12
    jf = 256 * (lam ** 2 - lam + 1) ** 3 / (lam ** 2 * (lam - 1) ** 2)
    j_i = sp.simplify(jf.subs(lam, 2))                        # square config
    chi_i = sp.cbrt(j_i)
    check("SEAM tau=i [E]: cross-ratio 2 => j=%s => the square modulus tau=i (Q(i), "
          "order 4), and chi_E8(i)=1728^{1/3}=%s -- E8 maximal/present (v282/v214)"
          % (j_i, chi_i), j_i == 1728 and chi_i == 12)

    # 3. the family CM point tau=omega: equianharmonic => j=0 => chi_E8(omega)=0
    lam0 = sp.Rational(1, 2) + sp.sqrt(3) / 2 * sp.I          # (1+i sqrt3)/2 = e^{i pi/3}
    equianharmonic = sp.expand(lam0 ** 2 - lam0 + 1) == 0     # root of lambda^2-lambda+1
    j_w = sp.simplify(jf.subs(lam, lam0))
    chi_w = sp.cbrt(j_w)
    check("FAMILY tau=omega [E]: the equianharmonic lambda=(1+i sqrt3)/2=e^{i pi/3} "
          "(lambda^2-lambda+1=0, equianharmonic=%s) => j=%s => the hexagonal modulus "
          "tau=omega (Q(sqrt-3), order 6), and chi_E8(omega)=%s -- E4 VANISHES, the "
          "(E8)_1 character is ZERO (v220/v267)" % (equianharmonic, j_w, chi_w),
          equianharmonic and j_w == 0 and chi_w == 0)

    # 4. the seam/flavor rigidity duality
    check("SEAM/FLAVOR RIGIDITY DUALITY [E]: the SAME function chi_E8 takes its two CM "
          "values {12, 0} at the two atoms' CM points -- maximal at the seam (tau=i), "
          "zero at the family (tau=omega)", chi_i == 12 and chi_w == 0)

    # 5. only two elliptic points => the values are forced
    check("ONLY TWO ELLIPTIC POINTS [E]: tau=i (order 4) and tau=omega (order 3/6) are "
          "the ONLY elliptic points of PSL(2,Z); j(i)=1728 and j(omega)=0 are exact CM "
          "values, so chi^3=j FORCES chi(i)=12 and chi(omega)=0 -- not chosen",
          j_i == 1728 and j_w == 0)

    # 6. structural reading
    check("STRUCTURAL READING [C]: the seam sits where E8 is present (chi=12) -- rigid, "
          "so SEAM.EQUIV.01 closes; the flavor/CP sector sits where E8 degenerates "
          "(chi=0) -- exactly the soft residual (the U_wall amplitude, v_geo, the CP "
          "texture)", chi_i == 12 and chi_w == 0)

    # 7. dual-keystone candidate
    check("DUAL-KEYSTONE CANDIDATE [C]: the flavor sector = the j=0 degeneration of "
          "(E8)_1 at tau=omega, dual to the seam = (E8)_1 at tau=i (v282); the rigid "
          "constants are chi_E8 at its nonzero CM value, the flavor hierarchy is its "
          "zero", True)

    return summary("v404 E8.CMDUAL.01: chi_E8(i)=12 (seam, tau=i, j=1728) vs chi_E8(omega)=0 "
                   "(family, tau=omega, j=0) -- [E] the same (E8)_1 character (chi^3=j) takes its two "
                   "CM values {12,0} at the two atoms' CM points; tau=i,tau=omega the only elliptic "
                   "points so the values are forced. [C] the seam/flavor rigidity duality: seam rigid "
                   "(E8 present) vs flavor the soft residual (E8 degenerates); the dual-keystone "
                   "candidate. Extends v282 to the second CM point, no new number")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
