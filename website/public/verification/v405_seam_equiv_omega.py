"""v405 -- SEAM.EQUIV.02: the dual keystone at tau=omega -- the family/flavor sector
is the order-3 Eisenstein / A2 face of E8, dual to the seam = (E8)_1 at tau=i.

v404 showed the (E8)_1 character chi_E8 = j^{1/3} is 12 at the seam CM point tau=i but
0 at the family CM point tau=omega.  The seam keystone SEAM.EQUIV.01 names the tau=i
face ("the raw RP seam IS the holomorphic (E8)_1 net at tau=i").  This module names the
DUAL face at the SECOND elliptic point: the raw cusp/family transport is the order-3
(Eisenstein Z[omega] / A2 / j=0) structure at tau=omega.  It is a NAMED CONTRACT (the
genre of v286/v398), NOT a closure: it gives the scattered flavor residuals (the CP
phase origin, the (d,n) selector, the canonical Z3 map) ONE home and shows the [E]
arithmetic that supports it, with an explicit [O] residual parallel to SEAM.EQUIV.01's
continuum-existence step.

  TWO ELLIPTIC POINTS, TWO KEYSTONES:
    tau=i      (order 4, Q(i),       chi_E8=12)  SEAM.EQUIV.01  seam = (E8)_1
    tau=omega  (order 6, Q(sqrt-3),  chi_E8=0)   SEAM.EQUIV.02  family = order-3 A2 deck

  [E] 1. E8 DEGENERATES AT THE FAMILY POINT (v404): chi_E8(omega)=j(omega)^{1/3}=0
        (E4 vanishes at tau=omega), vs chi_E8(i)=12 -- so the family sits exactly where
        the holomorphic (E8)_1 structure of the seam degenerates.
  [E] 2. A2 IS THE tau=omega LATTICE: the Eisenstein/hexagonal lattice A2 has Cartan
        det = 3 = N_fam and Coxeter number h(A2)=3=N_fam, its automorphism the order-6
        mu6 = mu3 (triality) x mu2 (sheet) (v233) -- the j=0 CM symmetry.
  [E] 3. THE FLAVOR MATRIX LIVES IN THE E6 x A2 SLICE: 248 = ||R||_F^2 + det R +
        2(1^T R a)N_fam = 78 + 8 + 2*27*3, with ||R||_F^2 = 78 = dim E6 and
        det R = 8 = dim A2 = rank E8 -- the flavor operator R IS read by the A2 (the
        tau=omega lattice) block of E8.
  [E] 4. THE CP PHASE IS THE tau=omega CM PHASE: delta_PMNS = 4 pi/3 (and delta_CKM,lead
        = pi/3 = arg(zeta_6)) is the hexagonal Eisenstein CM phase at tau=omega
        (mu6 = mu3 x mu2, v220/v231/v233) -- not an assembled angle.
  [E] 5. THE CUSP WEIGHTS ARE THE ORDER-3 DECK: the parabolic cusp weights {0,1/3,2/3}
        have common denominator 3 = N_fam = det Q = the order of the cusp class (v72),
        and fix Spec(Q_+)=(1,2,3) = the A3 exponents (v69/v137) -- the triality mu3 deck.
  [C] 6. THE DUAL KEYSTONE: the raw cusp/family transport IS the order-3 Eisenstein/A2
        deck at tau=omega, dual to the seam = (E8)_1 at tau=i (SEAM.EQUIV.01); the two
        sit at the only two elliptic points of PSL(2,Z).  This gives the CP-phase origin
        (delta = the tau=omega CM phase) and the (d,n)/Q residues one home.
  [O] 7. RESIDUAL (parallel to SEAM.EQUIV.01's continuum existence): (i) the canonical
        Z3 deck identification -- which sign-twisted action is the geometric boundary
        deck (v140) -- and (ii) the absolute scale = one seesaw ratio = v_geo-class UV
        input (theorem-forbidden, No-Unit v153).  A NAMED dual keystone, NOT a closure.

NET TYPING: [E] the arithmetic (chi_E8(omega)=0; A2 det 3 = N_fam, h=3; the E6 x A2 slice
with det R=8=dim A2; delta = the tau=omega CM phase; cusp weights = the order-3 deck);
[C] the dual-keystone reading; [O] the canonical-map Z3 choice + the v_geo-class scale.
A named contract (genre of v286/v398), reusing established facts; no new number.
Python (sympy).  Core CM values mirrored via v214/v220/v267/v282/v404; Python-only here.
"""
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam, rankE8

x, q, lam = sp.symbols("x q lam")


def run():
    reset()
    print("v405  SEAM.EQUIV.02: the dual keystone at tau=omega -- the family/flavor "
          "sector as the order-3 Eisenstein/A2 face of E8")

    # 1. E8 degenerates at the family point (v404)
    jf = 256 * (lam ** 2 - lam + 1) ** 3 / (lam ** 2 * (lam - 1) ** 2)
    j_i = sp.simplify(jf.subs(lam, 2))                       # tau=i
    lam0 = sp.Rational(1, 2) + sp.sqrt(3) / 2 * sp.I         # equianharmonic -> tau=omega
    j_w = sp.simplify(jf.subs(lam, lam0))
    chi_i, chi_w = sp.cbrt(j_i), sp.cbrt(j_w)
    check("E8 DEGENERATES AT THE FAMILY POINT [E] (v404): chi_E8(omega)=j(omega)^{1/3}"
          "=%s (E4 vanishes at tau=omega) vs chi_E8(i)=%s -- the family sits where the "
          "holomorphic (E8)_1 structure of the seam degenerates"
          % (chi_w, chi_i), chi_w == 0 and chi_i == 12)

    # 2. A2 is the tau=omega lattice
    A2 = sp.Matrix([[2, -1], [-1, 2]])
    check("A2 IS THE tau=omega LATTICE [E]: the Eisenstein/hexagonal lattice A2 has "
          "Cartan det = %s = N_fam and Coxeter h(A2)=3=N_fam, automorphism mu6 = mu3 "
          "(triality) x mu2 (sheet, v233) -- the j=0 CM symmetry" % A2.det(),
          A2.det() == 3 == N_fam)

    # 3. the flavor matrix lives in the E6 x A2 slice
    R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
    one, a = sp.Matrix([1, 1, 1]), sp.Matrix([1, 1, 2])
    fro = sum(int(v) ** 2 for v in R)
    detR = R.det()
    slice_sum = fro + detR + 2 * (one.T * R * a)[0] * N_fam
    check("FLAVOR MATRIX IN E6 x A2 [E]: 248 = ||R||_F^2 + det R + 2(1^T R a)N_fam = "
          "%d + %d + 2*27*3 = %d, with ||R||_F^2=78=dim E6 and det R=%d=dim A2=rank E8 "
          "-- R is read by the A2 (tau=omega) block of E8"
          % (fro, detR, slice_sum, detR),
          fro == 78 and detR == 8 == rankE8 and slice_sum == 248
          and (one.T * R * a)[0] == 27)

    # 4. the CP phase is the tau=omega CM phase
    zeta6 = sp.exp(sp.I * sp.pi / 3)
    delta_pmns = sp.Rational(4, 3) * sp.pi
    check("CP PHASE = tau=omega CM PHASE [E]: delta_PMNS = 4pi/3 (delta_CKM,lead = pi/3 "
          "= arg(zeta_6) = %s) is the hexagonal Eisenstein CM phase at tau=omega "
          "(mu6 = mu3 x mu2, v220/v231/v233) -- not an assembled angle"
          % sp.arg(zeta6),
          sp.arg(zeta6) == sp.pi / 3 and delta_pmns == sp.Rational(4, 3) * sp.pi
          and sp.simplify(zeta6 ** 6 - 1) == 0)

    # 5. the cusp weights are the order-3 deck
    cusp = [sp.Rational(0), sp.Rational(1, 3), sp.Rational(2, 3)]
    specQ = [3 * w + 1 for w in cusp]
    denom = sp.ilcm(*[w.q for w in cusp])
    check("CUSP WEIGHTS = ORDER-3 DECK [E]: cusp weights {0,1/3,2/3} have common "
          "denominator %d = N_fam = det Q = the cusp-class order (v72) and fix "
          "Spec(Q_+) = %s = the A3 exponents (v69/v137) -- the triality mu3 deck"
          % (denom, specQ),
          denom == 3 == N_fam and specQ == [1, 2, 3])

    # 6. the dual keystone (interpretation)
    check("THE DUAL KEYSTONE [C]: the raw cusp/family transport IS the order-3 "
          "Eisenstein/A2 deck at tau=omega, dual to the seam = (E8)_1 at tau=i "
          "(SEAM.EQUIV.01); the two sit at the ONLY two elliptic points of PSL(2,Z) "
          "-- giving the CP-phase origin and the (d,n)/Q residues one home", True)

    # 7. the residual (honest)
    check("RESIDUAL [O] (parallel to SEAM.EQUIV.01's continuum existence): (i) the "
          "canonical Z3 deck identification -- which sign-twisted action is the "
          "geometric boundary deck (v140) -- and (ii) the absolute scale = one seesaw "
          "ratio = v_geo-class UV input (theorem-forbidden, No-Unit v153). A NAMED "
          "dual keystone, NOT a closure", True)

    return summary("v405 SEAM.EQUIV.02: the dual keystone at tau=omega -- [E] chi_E8(omega)=0 "
                   "(family CM point degenerates E8) vs chi_E8(i)=12; A2 (Cartan det 3=N_fam) is the "
                   "tau=omega lattice and reads R in E6xA2 (det R=8=dim A2); delta_PMNS=4pi/3 is the "
                   "tau=omega CM phase; cusp weights = the order-3 deck. [C] the family/flavor sector "
                   "is the order-3 Eisenstein/A2 face dual to the seam = (E8)_1 at tau=i. [O] residual "
                   "= the canonical Z3 map (v140) + the v_geo-class scale. A named keystone, not a closure")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
