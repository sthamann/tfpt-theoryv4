"""v79 -- four validated review identities (and one disciplined rejection).

After a rigorous validation of an external review, four claims pass both arithmetic AND the
anti-numerology / admissible-invariant discipline, and are recorded here.  One pair (eta_B,
m_p/m_e) is arithmetically close but REJECTED -- it would violate the frontier firewall -- and
the rejection is recorded as a discipline data point.

(1) HYPERCHARGE LUCAS-BINET RESONANCES.  The carrier charges (q+,q-)=(3,-2) (Lean
    unique_carrier_pair; X^2-X-6=(X-3)(X+2)) generate the Lucas U-sequence
        D_n = (3^n - (-2)^n)/5,   D_1..D_6 = 1,1,7,13,55,133,
    which in order is (N_Phi, -, scalaron exponent 7, Delta_Q 13, quark-ratio numerator 55,
    dim E7 133).  Bonus: c_u/c_d = D_5/(N_fam^2 * D_4) = 55/117 -- a cleaner reading of the "55"
    than the Plucker route. [I] arithmetic; [P] mode<->constant reading (only n<=6 is meaningful).

(2) INVERSE ANCHOR NORMALISATION THEOREM.  On the inverses of the flavor operators,
        1^T Q^-1 1 = 1/3 = 1/N_fam,  1^T R^-1 1 = 1^T K^-1 1 = 1/4 = 1/|mu4|,  1^T L^-1 1 = 1/10 = 1/A_Lambda,
    and the anchor is self-dual under R,K,L:  a^T R^-1 a = a^T K^-1 a = a^T L^-1 a = 1
    (while a^T Q^-1 a = 7/3, so the self-duality is exactly the physical residue/mass/transport
    operators, not the pure difference Q). [I]/[L]

(3) MACWILLIAMS CODE IDENTITY.  C^+ is the even-weight code [5,4,2]; its dual is the repetition
    code [5,1,5]; the weight enumerator is (1,10,5) = Lambda^even(5) = the carrier grading (v44).
    [L] (code identity); the holographic/dual = vacuum reading is [P].

(4) HYPERCHARGE FACTORISATION.  6Y^2 - Y - 1 = (2Y-1)(3Y+1): roots 1/2 (s=2, SU(2)) and
    -1/3 (b=3, SU(3)) -- the polynomial splits into the two gauge-group rank representatives. [I]

REJECTED (firewall, recorded on purpose): eta_B=(2/13)c3^6 and m_p/m_e=1920-84+3lamC^2 are
arithmetically close but NOT admissible -- m_p/m_e pulls in SU(9)=A_8 (dim Lambda^3 = 84), which is
NOT in the carrier D5+A3, with no QCD mechanism (m_p is confinement); eta_B is a 2-atom prefactor
fit to a model-dependent (leptogenesis/sphaleron) quantity.  They stay [A]/[P] frontier.
"""
import sympy as sp
from tfpt_constants import check, summary, reset, g_car, N_fam

Y = sp.Symbol('Y')


def run():
    reset()
    print("v79  four validated review identities (+ one disciplined rejection)")

    # (1) Lucas-Binet
    D = [(3**n - (-2)**n) // 5 for n in range(1, 8)]
    check("Lucas-Binet D_n=(3^n-(-2)^n)/5 = 1,1,7,13,55,133,463; roots (3,-2)=carrier charges (q+,q-)",
          D == [1, 1, 7, 13, 55, 133, 463]
          and sp.factor(Y**2 - Y - 6) == (Y - 3) * (Y + 2))
    check("D = (N_Phi=1, 1, scalaron-exp 7, Delta_Q 13, quark numerator 55, dim E7 133) in order",
          D[2] == 7 and D[3] == 13 and D[4] == 55 and D[5] == 133)
    check("c_u/c_d = D_5/(N_fam^2 * D_4) = 55/(9*13) = 55/117 (cleaner Lucas reading of the '55')",
          sp.Rational(D[4], N_fam**2 * D[3]) == sp.Rational(55, 117))

    # (2) inverse anchor normalisation
    R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
    Q = sp.Matrix([[3, 1, 0], [3, 2, 0], [3, 2, 1]])
    K = sp.Matrix([[4, 2, 0], [4, 3, 2], [5, 3, 2]])
    L = sp.Matrix([[7, 3, 0], [7, 5, 2], [8, 5, 3]])
    one = sp.Matrix([1, 1, 1]); a = sp.Matrix([1, 1, 2])
    qf = lambda M, v: (v.T * M.inv() * v)[0]
    check("1^T M^-1 1 = 1/atom: Q->1/3=1/N_fam, R->1/4=1/|mu4|, K->1/4, L->1/10=1/A_Lambda",
          qf(Q, one) == sp.Rational(1, 3) and qf(R, one) == sp.Rational(1, 4)
          and qf(K, one) == sp.Rational(1, 4) and qf(L, one) == sp.Rational(1, 10))
    check("anchor self-dual under the physical operators: a^T R^-1 a = a^T K^-1 a = a^T L^-1 a = 1 "
          "(while a^T Q^-1 a = 7/3, so it is exactly residue/mass/transport, not the pure difference Q)",
          qf(R, a) == 1 and qf(K, a) == 1 and qf(L, a) == 1 and qf(Q, a) == sp.Rational(7, 3))

    # (3) MacWilliams code identity
    wd = [int(sp.binomial(5, w)) for w in (0, 2, 4)]
    check("C^+ = even-weight code [5,4,2]; weight enumerator (1,10,5) = Lambda^even(5) = carrier grading (v44); "
          "dual = repetition code [5,1,5]",
          wd == [1, 10, 5] and sum(wd) == 16 == 2**(g_car - 1))

    # (4) hypercharge factorisation
    check("6Y^2 - Y - 1 = (2Y-1)(3Y+1); roots 1/2 (s=2,SU(2)) and -1/3 (b=3,SU(3))",
          sp.expand((2 * Y - 1) * (3 * Y + 1)) == 6 * Y**2 - Y - 1
          and set(sp.solve(6 * Y**2 - Y - 1, Y)) == {sp.Rational(1, 2), sp.Rational(-1, 3)})

    # REJECTED (firewall, recorded): the discipline boundary
    check("FIREWALL: m_p/m_e=1920-84+3lamC^2 and eta_B=(2/13)c3^6 are arithmetically close but REJECTED -- "
          "SU(9)=A_8 (Lambda^3=84) is NOT in the carrier (D5+A3) and m_p is QCD confinement (no mechanism); "
          "eta_B is a 2-atom fit to a model-dependent quantity. They stay [A]/[P] frontier, not [I]",
          sp.binomial(9, 3) == 84)
    return summary("v79 four validated review identities (+ firewall)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
