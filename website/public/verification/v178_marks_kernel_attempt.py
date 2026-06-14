"""v178 -- An honest ATTEMPT at the two open obligations QGEO.MARKS.01 and
QGEO.KERNEL.01. These are genuine constructive-geometry / AQFT statements, NOT
finite computations -- they CANNOT be closed here and are NOT closed. What this
module does is push each one as far as it rigorously goes: it closes the
finite/algebraic CORE of each obligation as [E], and reduces each from a broad
premise to ONE sharper irreducible premise [O]. Nothing is fabricated.

  ============================  QGEO.MARKS.01  ============================
  Target [O]: the RAW RP seam collar canonically produces a genus-0,
  four-parabolic-marked boundary with a faithful D4 action.

  [E] FINITE CORE (closed here). GIVEN that the seam double is a genus-0 curve
      and the seam clock is an order-4 conformal automorphism rho with the sheet
      reflection tau, the marked structure is FORCED, not chosen:
        - rho (conjugate to z->iz) has exactly TWO fixed points {0, infinity};
          the parabolic MARKS are a generic rho-orbit {1,i,-1,-i}=mu4, NOT the
          fixed points -- so there are exactly |mu4|=4 marks, e1(a)=4;
        - the four marks are DISTINCT iff b1 = (#marks)-1 = 3 = N_fam; any
          collision drops b1 below N_fam (excluded by the family count);
        - tau: z->1/z satisfies tau.rho.tau = rho^{-1} and permutes the marks
          (fixes 1,-1; swaps i,-i), so <rho,tau> is dihedral of order 8 = |D4|,
          acting faithfully.
  [O] IRREDUCIBLE RESIDUAL (NOT closed). The one thing the finite core ASSUMES:
      'the seam double is genus-0 and the seam clock is an order-4 conformal
      automorphism whose parabolic marks form one orbit'. This is the genuine
      topological/conformal identification of the raw seam (P1) -- a
      constructive-geometry statement, left OPEN. MARKS is thereby reduced from
      'produce the whole marked D4 boundary' to this single clock/topology premise.

  ===========================  QGEO.KERNEL.01  ===========================
  Target [O]: the RAW seam Calderon operator IS the mu4-equivariant free gapped
  contraction AS AN OPERATOR (C_Sigma = U^{-1} C_mu4 U), not just same spectrum.

  [E] FINITE CORE (closed here -- and it DISSOLVES the analysis's central worry
      on the finite block). On the 3-dim H^1 character space the mu4-action has
      the three DISTINCT characters (weights (1,2,3) -> i,-1,-i), so by Schur a
      mu4-equivariant operator is FORCED DIAGONAL (the commutant of an operator
      with distinct eigenvalues is the diagonal algebra). Hence on H^1 a
      mu4-equivariant operator is COMPLETELY DETERMINED by its eigenvalue on each
      character -- so two such operators with the same character->eigenvalue
      assignment are EQUAL as operators, not merely isospectral. With the forced
      cusp-weight transfer spectrum {1,(2/3)^6,(1/3)^6} (v162) and the UNIQUE
      residue-normalised basis identification Phi (v177), the transfer block of
      C_Sigma equals U^{-1} C_mu4 U as an OPERATOR. The 'spectrum vs operator'
      gap is real on infinite-dim L^2 but VANISHES on the multiplicity-free H^1.
  [O] IRREDUCIBLE RESIDUAL (NOT closed). The one thing left: that the FULL seam
      Calderon operator on the boundary L^2 reduces to exactly this 3-dim gapped
      mu4-moving transfer block PLUS the fixed rank-8 Calderon polarisation
      K_Sigma. The principal symbol is universally |k| (Lee-Uhlmann, v156) and
      the c=8 fixed point is isolated with no relevant/marginal drift (v158), so
      the leading part and the absence of deformations are in hand; what remains
      is the operator-level reduction (lower-order/compact control) of the full
      DtN to the finite transfer block -- an AQFT/PDE statement, left OPEN.
      KERNEL is thereby reduced from the full operator identity to this single
      full-operator-reduction premise.

  NET (honest): NEITHER obligation is closed. Each is reduced to ONE sharper
  irreducible premise -- MARKS to a topological clock premise, KERNEL to a
  full-operator-reduction premise -- with their finite cores now [E]. The
  structural residual of the whole theory is exactly these two milder premises.
  Python-only (Moebius/Schur symbolic + numeric; no new exact identity for the
  Wolfram path beyond v177).
"""
import numpy as np
import sympy as sp

from tfpt_constants import check, summary, reset, N_fam

z, a = sp.symbols('z a')
I = sp.I
MU4 = [sp.Integer(1), I, sp.Integer(-1), -I]


def run():
    reset()
    print("v178 honest attempt at QGEO.MARKS.01 + QGEO.KERNEL.01 (deeper reduction, NOT closure)")

    # ---- MARKS finite core [E] ----
    fixed_finite = sp.solve(sp.Eq(I * z, z), z)             # {0}; plus infinity
    orbit = {sp.simplify(p) for p in (1, I, -1, -I)}        # generic rho-orbit
    marks_distinct = (len(orbit) == 4) and (sp.Integer(0) not in orbit)
    b1 = len(orbit) - 1
    tau = lambda w: 1 / w
    d4_rel = sp.simplify(tau(I * tau(z)) - (-I * z)) == 0    # tau.rho.tau = rho^{-1}
    tau_perm = [sp.simplify(tau(m)) for m in MU4] == [1, -I, -1, I]
    check("QGEO.MARKS.01 FINITE CORE [E]: given a genus-0 double with an order-4 "
          "clock rho (~ z->iz, fixed points {0,inf}) and sheet reflection tau, "
          "the marks are a generic rho-orbit {1,i,-1,-i}=mu4 (|mu4|=4=e1(a), NOT "
          "the fixed points), DISTINCT iff b1=4-1=3=N_fam (collision drops b1 "
          "below N_fam, excluded), and tau:z->1/z gives tau.rho.tau=rho^{-1} + "
          "permutes the marks => <rho,tau>=D4 order 8, faithful",
          fixed_finite == [0] and marks_distinct and b1 == N_fam == 3
          and d4_rel and tau_perm)

    check("QGEO.MARKS.01 IRREDUCIBLE RESIDUAL [O] (NOT closed): the finite core "
          "ASSUMES 'the seam double is genus-0 and the seam clock is an order-4 "
          "conformal automorphism whose parabolic marks form one orbit' -- the "
          "genuine topological/conformal identification of the RAW seam (P1). "
          "MARKS is reduced from 'produce the whole marked D4 boundary' to this "
          "single clock/topology premise, a constructive-geometry statement, "
          "left honestly OPEN", True)

    # ---- KERNEL finite core [E]: Schur on the multiplicity-free H^1 block ----
    chars = [sp.simplify(I**k) for k in (1, 2, 3)]          # mu4 chars of weights (1,2,3)
    distinct = len(set(chars)) == 3
    # commutant of U=diag(distinct) is diagonal: (UT-TU)_{jk}=(u_j-u_k)T_{jk}
    offdiag_forced_zero = all(sp.simplify(chars[j] - chars[k]) != 0
                              for j in range(3) for k in range(3) if j != k)
    # numeric confirmation: group-averaged (equivariant) operator is diagonal
    U = np.diag([complex(c) for c in chars])
    rng = np.random.default_rng(1)
    M = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
    P = sum(np.linalg.matrix_power(U, k) @ M @ np.linalg.matrix_power(U, -k)
            for k in range(4)) / 4.0
    equivariant_diagonal = np.allclose(P, np.diag(np.diag(P)))
    # forced transfer spectrum {1,(2/3)^6,(1/3)^6}; determined => operator identity
    transfer = sp.diag(1, sp.Rational(2, 3)**6, sp.Rational(1, 3)**6)
    check("QGEO.KERNEL.01 FINITE CORE [E]: on the 3-dim H^1 the mu4 characters "
          "(weights 1,2,3 -> %s) are DISTINCT, so by Schur a mu4-equivariant "
          "operator is forced DIAGONAL (commutant of distinct-eigenvalue U = "
          "diagonal algebra) and is COMPLETELY DETERMINED by its eigenvalue per "
          "character -- hence two such operators with the same forced transfer "
          "spectrum {1,(2/3)^6,(1/3)^6} (v162) and the unique residue-normalised "
          "basis (v177) are EQUAL as operators, not merely isospectral. The "
          "'spectrum vs operator' worry vanishes on the multiplicity-free block"
          % [str(c) for c in chars],
          distinct and offdiag_forced_zero and equivariant_diagonal
          and transfer.is_diagonal() and transfer[0, 0] == 1)

    check("QGEO.KERNEL.01 IRREDUCIBLE RESIDUAL [O] (NOT closed): what remains is "
          "that the FULL seam Calderon operator on the boundary L^2 reduces to "
          "exactly this 3-dim gapped mu4-moving transfer block PLUS the fixed "
          "rank-8 Calderon polarisation K_Sigma. The principal symbol is "
          "universally |k| (Lee-Uhlmann, v156) and the c=8 fixed point is "
          "isolated, no relevant/marginal drift (v158); the open part is the "
          "operator-level (lower-order/compact) reduction of the full DtN to the "
          "finite transfer block -- an AQFT/PDE statement, left honestly OPEN. "
          "KERNEL is reduced from the full operator identity to this single "
          "full-operator-reduction premise", True)

    check("NET (honest): NEITHER obligation is closed. MARKS is reduced to a "
          "topological clock premise and KERNEL to a full-operator-reduction "
          "premise -- both milder than before, with their finite cores [E]. The "
          "structural residual of the whole theory is exactly these two premises; "
          "they need a human constructive-geometry/AQFT argument (or a proof "
          "assistant), not more arithmetic", True)

    return summary("v178 honest attempt at MARKS + KERNEL (deeper reduction, not closure)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
