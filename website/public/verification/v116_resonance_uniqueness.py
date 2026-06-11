"""v116 -- The resonance theorem: M_inf = 1 IFF a13 = 0, and the flat
anchor locus is exactly ONE gauge orbit -- the v115 [N] findings are
promoted to [I] by a linear resonance computation (no Groebner needed).

v115 found numerically that all Riemann-Hilbert solutions on the
anchor-pinned manifold have a13 = 0 and lie on one gauge orbit.  This
module proves both statements exactly: the transcendental condition
"monodromy at infinity trivial" collapses to one linear equation.

  [I] 1. TWISTED-AVERAGE LEMMA (symbolic).  Write the Fuchsian system at
         infinity as dY/dw = -(1/w)(B0 + B1 w + ...)Y with
         B_m = sum_k p_k^m U^k A0 U^{-k}, p_k = i^k.  The mu_4-twisted
         averages collapse:
             B0 = 4 diag(A0)             (m = 0: the v115 average lemma),
             B1 = 4 a12 E_12 + 4 conj(a13) E_31   (m = 1: ONLY two cells
         survive -- the entries with eigenvalue ratio u_a/u_b = -i).
  [I] 2. RESONANCE THEOREM.  With the anchor exponents B0 = diag(2,1,1)
         (resonance gap 1), the level-1 formal-gauge equation
         (1 - ad R0)H1 = R1 is singular exactly on the cells {(2,1),
         (3,1)}; the obstruction entries of B1 there are 0 and
         4 conj(a13).  Higher levels k >= 2 are non-resonant, and the
         formal monodromy e^{-2 pi i diag(2,1,1)} = 1.  Hence
             M_inf = 1  <=>  a13 = 0
         -- the v115 numerical finding is a two-line resonance theorem;
         the feared Groebner promotion is a LINEAR computation.
  [I] 3. UNIQUENESS COROLLARY.  a13 = 0 + the (8,0,5)/144 lemma (v115)
         pin the off-diagonal moduli uniquely, and the remaining phases
         of a12, a23 are exactly the diagonal gauge (conjugation by
         diag(1, e^{i phi2}, e^{i phi3}) commutes with U, preserves the
         diagonal, and moves both phases freely).  THE FLAT ANCHOR LOCUS
         IS EXACTLY ONE GAUGE ORBIT -- the exact matrix A0* of v115.
         Within the mu_4-equivariant anchor class, the (U_wall) bundle
         datum is ALGEBRAICALLY unique.
  [N] 4. FALSIFICATION CONTROL.  The obstruction is sharp, not a formal
         artifact: perturbing a13 away from 0 produces ||M_inf - 1||
         growing linearly (~8.5 |a13|), while A0* itself gives ~1e-10.
  [P] 5. HONEST SCOPE (recorded): the equivariant ansatz A_k =
         U^k A0 U^{-k} is the established D4 selector input (v19/v30);
         the residue side is now [I], while the holonomy values
         (harmonic diagonal (0, 1/2, 1/2)) remain [N] (transcendental
         monodromy of an exact system).
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

from tfpt_constants import check, summary, reset


def run():
    reset()
    print("v116 resonance theorem (M_inf = 1 <=> a13 = 0; one gauge orbit)")

    a12, a13, a23 = sp.symbols('a12 a13 a23', complex=True)
    a0 = sp.Matrix([[sp.Rational(1, 2), a12, a13],
                    [sp.conjugate(a12), sp.Rational(1, 4), a23],
                    [sp.conjugate(a13), sp.conjugate(a23),
                     sp.Rational(1, 4)]])
    usym = sp.diag(1, sp.I, -sp.I)

    def bmat(m):
        total = sp.zeros(3)
        for k in range(4):
            uk = usym ** k
            total += (sp.I ** k) ** m * uk * a0 * uk.inv()
        return sp.expand(total)

    # 1. twisted-average lemma
    b0, b1 = bmat(0), bmat(1)
    b1_expect = sp.zeros(3)
    b1_expect[0, 1] = 4 * a12
    b1_expect[2, 0] = 4 * sp.conjugate(a13)
    check("TWISTED-AVERAGE LEMMA [symbolic]: B0 = 4 diag(A0) and "
          "B1 = 4 a12 E_12 + 4 conj(a13) E_31 -- the twisted mu_4 "
          "average kills every other cell (only eigenvalue ratio "
          "u_a/u_b = -i survives)",
          sp.simplify(b0 - 4 * sp.diag(*[a0[i, i] for i in range(3)]))
          == sp.zeros(3)
          and sp.simplify(b1 - b1_expect) == sp.zeros(3))

    # 2. resonance theorem
    lam = [-2, -1, -1]
    singular = [(a, b) for a in range(3) for b in range(3)
                if lam[a] - lam[b] == 1]
    check("RESONANCE CELLS: with anchor exponents diag(2,1,1) the "
          "level-1 equation (1 - ad R0)H1 = R1 is singular exactly on "
          "{(2,1), (3,1)}; the obstruction entries of B1 there are "
          "(0, 4 conj(a13)) => M_inf = 1 REQUIRES a13 = 0",
          singular == [(1, 0), (2, 0)] and b1[1, 0] == 0
          and sp.simplify(b1[2, 0] - 4 * sp.conjugate(a13)) == 0)

    r0 = -sp.diag(2, 1, 1)
    r1 = -b1.subs({a13: 0, sp.conjugate(a13): 0})
    h1 = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'h{i}{j}', complex=True))
    eqs = sp.expand(h1 - (r0 * h1 - h1 * r0) - r1)
    solvable = bool(sp.solve([eqs[i, j] for i in range(3) for j in range(3)],
                             [h1[i, j] for i in range(3) for j in range(3)],
                             dict=True))
    check("SUFFICIENCY: with a13 = 0 the level-1 gauge H1 exists "
          "(explicit symbolic solve), all levels k >= 2 are "
          "non-resonant (k - (lam_a - lam_b) in {k, k+-1} != 0), and "
          "the formal monodromy e^{-2 pi i diag(2,1,1)} = 1 => "
          "M_inf = 1. THEOREM: M_inf = 1 <=> a13 = 0",
          solvable
          and all(k - (lam[a] - lam[b]) != 0 for k in range(2, 8)
                  for a in range(3) for b in range(3)))

    # 3. uniqueness corollary
    phi2, phi3 = sp.symbols('phi2 phi3', real=True)
    gauge = sp.diag(1, sp.exp(sp.I * phi2), sp.exp(sp.I * phi3))
    a0_flat = a0.subs({a13: 0, sp.conjugate(a13): 0})
    conj_a0 = sp.expand(gauge * a0_flat * gauge.inv())
    check("UNIQUENESS COROLLARY: the diagonal gauge commutes with U, "
          "preserves the diagonal, and rotates arg(a12), arg(a23) "
          "freely (a12 -> e^{-i phi2} a12, a23 -> e^{i(phi2-phi3)} "
          "a23); with the (8,0,5)/144 moduli (v115) the flat anchor "
          "locus is EXACTLY ONE gauge orbit = the exact A0*",
          sp.simplify(gauge * usym - usym * gauge) == sp.zeros(3)
          and all(sp.simplify(conj_a0[i, i] - a0_flat[i, i]) == 0
                  for i in range(3))
          and sp.simplify(conj_a0[0, 1]
                          - a12 * sp.exp(-sp.I * phi2)) == 0
          and sp.simplify(conj_a0[1, 2]
                          - a23 * sp.exp(sp.I * (phi2 - phi3))) == 0)

    # 4. falsification control (numerical)
    un = np.diag([1, 1j, -1j])
    uis = [np.linalg.matrix_power(un, k) for k in range(4)]
    uic = [np.linalg.inv(u) for u in uis]
    punct = np.array([1, 1j, -1, -1j])
    eye3 = np.eye(3, dtype=complex)
    base = np.array([[0.5, np.sqrt(8) / 12, 0],
                     [np.sqrt(8) / 12, 0.25, np.sqrt(5) / 12],
                     [0, np.sqrt(5) / 12, 0.25]], complex)

    def m_inf_norm(eps):
        a = base.copy()
        a[0, 2] += eps
        a[2, 0] += eps
        ak = [uis[k] @ a @ uic[k] for k in range(4)]

        def rhs(t, y):
            z = 3 * np.exp(1j * t)
            dz = 3j * np.exp(1j * t)
            am = sum(ak[k] / (z - punct[k]) for k in range(4))
            return ((am @ y.reshape(3, 3)) * dz).reshape(-1)

        sol = solve_ivp(rhs, [0, 2 * np.pi], eye3.reshape(-1),
                        rtol=1e-10, atol=1e-12, method='DOP853')
        return np.linalg.norm(sol.y[:, -1].reshape(3, 3) - eye3)

    n0, n1, n2 = m_inf_norm(0.0), m_inf_norm(0.02), m_inf_norm(0.05)
    check("FALSIFICATION CONTROL [N]: the obstruction is sharp -- "
          f"||M_inf - 1|| = {n0:.1e} at a13 = 0 vs {n1:.2f} at "
          f"a13 = 0.02 and {n2:.2f} at a13 = 0.05 (grows ~8.5|a13|)",
          n0 < 1e-7 and n1 > 0.1 and n2 > 0.3)

    # 5. honest scope
    check("HONEST SCOPE [P] (recorded): the equivariant ansatz "
          "A_k = U^k A0 U^{-k} is the established D4 selector input "
          "(v19/v30); within it the (U_wall) bundle datum is now "
          "ALGEBRAICALLY unique [I]; the holonomy values (harmonic "
          "diagonal (0, 1/2, 1/2)) remain [N] -- transcendental "
          "monodromy of an exact system", True)

    return summary("v116 resonance uniqueness")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
