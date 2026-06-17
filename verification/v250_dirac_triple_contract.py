"""v250 -- CONTRACT.QFT4D.DIRAC.01: the spectral-triple contract that would turn
"carrier is gauged" from a FORK into a THEOREM (Reviewer-A Theorem 3 + Reviewer-B
sigma=scalaron).  This module TYPES the obligations honestly and checks the finite
facts; it does NOT construct the operator or close the NCG axioms.

The target object is a real, even, almost-commutative spectral triple
    (A, H, D, J, gamma) = (C^inf(M) (x) A_F,  L^2(M,S) (x) H_F,
                           D_M (x) 1 + gamma_5 (x) D_F,  J, gamma)
with A_F the Pati-Salam algebra (v248), H_F = 3 x 16, and D_F built from the TFPT
flavor data (R, L, phi0, Majorana branch).

  [E] 1. FINITE HILBERT SPACE.  H_F = N_fam x dim S^+ = 3 x 16 = 48 (three
        generations of the SO(10) spinor); the PS algebra A_F (v248) acts on it.
  [E] 2. THE YUKAWAS ARE NOT THE TEST.  The charged-fermion mass ratios are ALREADY
        fixed by the TFPT flavor layer (FLAV.QUARK.01 / v18: mt/mb=40.8, etc.), so
        D_F's textbook output is in place -- the OPEN test is NCG CONSISTENCY of
        D_F, not "do we get nice Yukawas" (Reviewer A's point).
  [O] 3. THE NCG OBLIGATIONS (the contract).  For the explicit D_F one must verify,
        exactly: reality J (J^2 = +/-1), grading gamma, KO-DIMENSION (6 mod 8),
        the FIRST-ORDER CONDITION [[D,a],Jb*J^-1]=0 (the historic SO(10)-NCG
        obstruction), orientability, Poincare duality, and NO-JUNK (the quotient by
        junk forms).  None is closed here.
  [O] 4. sigma = SCALARON HYPOTHESIS.  Chamseddine-Connes-Mukhanov rescue the
        first-order condition with a singlet scalar sigma that also generates the
        nu_R Majorana mass.  Conjecture (supported by M_PS = kappa M_s, v249): this
        sigma IS the R+R^2 scalaron.  CAVEAT [honest]: the scalaron's coupling to
        nu_R nu_R (Majorana) is NOT automatic -- the identification (matching
        quantum numbers + couplings) must be PROVEN, not assumed.
  [O] 5. INNER FLUCTUATIONS -> HIGGS CONTENT.  The 1-forms Omega^1_D(A_F) should
        yield the Higgs content 10 + 16 + 45 and NOT the 126; this is the NCG
        complement of the E8-hull no-126 result (v247), to be derived from D_F.
  [C] 6. VERDICT.  The contract reduces the whole "4d QFT" residual to ONE
        constructive object (the spectral triple) + the finite NCG checks above.
        The gauge group (v248), matter rep (v245), Yukawas (v18) and unification
        corridor (v249) are already in place; what is missing is D_F + its axioms.

Status: [E] finite Hilbert space + the Yukawa-is-not-the-test framing; [O] all NCG
obligations, the sigma=scalaron identification and the inner-fluctuation Higgs
content.  Python-only (bookkeeping/typing; the operator construction is the open
contract).
"""
from tfpt_constants import check, summary, reset, dim_Splus, N_fam


def run():
    reset()
    print("v250  CONTRACT.QFT4D.DIRAC.01: the spectral-triple contract (carrier gauged as a theorem)")

    # 1. finite Hilbert space
    H_F = N_fam * dim_Splus
    check("FINITE HILBERT SPACE [E]: H_F = N_fam x dim S^+ = %d x %d = %d (three "
          "generations of the SO(10) spinor); the PS algebra A_F (v248) acts on it"
          % (N_fam, dim_Splus, H_F),
          H_F == 48 and N_fam == 3 and dim_Splus == 16)

    # 2. yukawas already in place
    check("THE YUKAWAS ARE NOT THE TEST [E]: the charged-fermion mass ratios are "
          "already fixed by the TFPT flavor layer (FLAV.QUARK.01/v18: mt/mb=40.8, "
          "mc/ms=13.6, ...); the open test is NCG CONSISTENCY of D_F, not 'nice "
          "Yukawas' (Reviewer A)", True)

    # 3. the NCG obligations (typed open)
    obligations = ["reality J (J^2=+/-1)", "grading gamma", "KO-dimension (6 mod 8)",
                   "first-order condition [[D,a],Jb*J^-1]=0", "orientability",
                   "Poincare duality", "no-junk forms"]
    check("NCG OBLIGATIONS [O]: for the explicit D_F one must verify exactly (%d "
          "axioms): %s. The first-order condition is the historic SO(10)-NCG "
          "obstruction. None closed here" % (len(obligations), "; ".join(obligations)),
          len(obligations) == 7)

    # 4. sigma = scalaron hypothesis
    check("sigma = SCALARON HYPOTHESIS [O]: the Chamseddine-Connes-Mukhanov singlet "
          "sigma (rescues first-order + gives nu_R Majorana) is conjectured to BE "
          "the R+R^2 scalaron (supported by M_PS = kappa M_s, v249). CAVEAT: the "
          "scalaron coupling to nu_R nu_R is NOT automatic -- must be proven, not "
          "assumed", True)

    # 5. inner fluctuations -> Higgs content
    check("INNER FLUCTUATIONS -> HIGGS [O]: Omega^1_D(A_F) should give 10+16+45 and "
          "NOT 126 -- the NCG complement of the E8-hull no-126 result (v247), to be "
          "derived from D_F", True)

    # 6. verdict
    check("VERDICT [C]: the contract reduces the '4d QFT' residual to ONE "
          "constructive object (the spectral triple) + the finite NCG checks; the "
          "gauge group (v248), matter rep (v245), Yukawas (v18) and unification "
          "corridor (v249) are already in place -- what is missing is D_F + its axioms",
          True)

    return summary("v250 spectral-triple contract (CONTRACT.QFT4D.DIRAC.01)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
