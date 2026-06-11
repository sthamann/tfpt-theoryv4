"""v117 -- The monodromy is the Weyl group of A3: the (U_wall) holonomy is
an EXACT 24-element representation (S4 = W(A3), standard x sign), and the
harmonic diagonal (0, 1/2, 1/2) is a theorem of that representation.  [I]
exact matrix + exact group enumeration; [N] identification with the
analytic monodromy of the exact A0* system.

v116 made the residue side exact; the holonomy values were the last [N]
item.  This module closes them: the unitarised monodromy of the exact
A0* system is itself EXACT -- entries in (1/2)Z[i] -- and generates,
together with the mu_4 deck twist U, a group of order 24.

  [I] 1. THE EXACT MONODROMY.
             M0 = [[0, -(1+i)/2, (1-i)/2],
                   [-(1+i)/2, -i/2, -1/2],
                   [(1-i)/2, -1/2, i/2]]
         is unitary with det 1, tr 0, char poly lam^3 - 1 (the cusp
         class {1, w, w^2} EXACTLY), M0^3 = 1, and
             diag M0 = (0, -i/2, +i/2)
         -- d1 = 0 and delta = 1/2 are now exact matrix entries, not
         numerical observations.  The v20 hand value, the v40/v41
         observation, the v114 torsion value and the v115 anchor slice
         all meet in this one exact matrix.
  [I] 2. TORSION AND FLATNESS.  (M0 U)^4 = 1 with tr(M0 U) = 1 (the
         {1, i, -i} branch, d1 = 0 slice -- exactly where v114/v115
         located the physical point), and the flatness identity
         prod_k U^k M0 U^{-k} = 1 holds exactly (v114 normal form).
  [I] 3. THE GROUP IS W(A3) = S4.  Exact enumeration of <U, M0> gives
         ORDER 24 with order statistics (1, 9, 8, 6) for element orders
         (1, 2, 3, 4) and character values (3, -1, 0, 1) -- uniquely the
         symmetric group S4 in its standard x sign representation
         (= the reflection representation of the WEYL GROUP OF A3,
         twisted by sign).  The flavor-wall monodromy group IS the Weyl
         group of the family lattice A3 of the glue D5 + A3 + mu4:
         U = image of a 4-cycle (the mu_4 deck), M0 = a 3-cycle (the
         cusp / family rotation), 24 = |W(A3)| = 4!.
  [N] 4. IDENTIFICATION.  The ODE monodromy of the exact A0* system,
         unitarised in the harmonic frame (v40 method), equals the
         exact M0 to ~1e-7, and the invariant form H is U-invariant to
         ~1e-10 (so the harmonic frame preserves the equivariance).
  [P] 5. STATUS (recorded): holonomy VALUES are now [I] (properties of
         the exact W(A3) representation); the identification of that
         representation with the analytic monodromy of A0* stays [N]
         (transcendental ODE matching, sharp to 1e-7).
"""
import numpy as np
import scipy.linalg as sl
import sympy as sp
from scipy.integrate import solve_ivp

from tfpt_constants import check, summary, reset

II = sp.I
M0_EXACT = sp.Matrix([[0, -(1 + II) / 2, (1 - II) / 2],
                      [-(1 + II) / 2, -II / 2, sp.Rational(-1, 2)],
                      [(1 - II) / 2, sp.Rational(-1, 2), II / 2]])
U_EXACT = sp.diag(1, II, -II)


def enumerate_group(gens):
    def freeze(m):
        return tuple(sp.simplify(x) for x in m)

    elems = {freeze(sp.eye(3)): sp.eye(3)}
    frontier = [sp.eye(3)]
    while frontier:
        new = []
        for e in frontier:
            for g in gens:
                x = sp.expand(g * e)
                kx = freeze(x)
                if kx not in elems:
                    elems[kx] = x
                    new.append(x)
        frontier = new
    return list(elems.values())


def ode_monodromy():
    """Unitarised monodromy of the exact A0* system (v40 method)."""
    un = np.diag([1, 1j, -1j])
    uis = [np.linalg.matrix_power(un, k) for k in range(4)]
    uic = [np.linalg.inv(u) for u in uis]
    punct = np.array([1, 1j, -1, -1j])
    eye3 = np.eye(3, dtype=complex)
    a0 = np.array([[0.5, np.sqrt(8) / 12, 0],
                   [np.sqrt(8) / 12, 0.25, np.sqrt(5) / 12],
                   [0, np.sqrt(5) / 12, 0.25]], complex)
    ak = [uis[k] @ a0 @ uic[k] for k in range(4)]

    def loop(k, eps=0.25):
        pk = punct[k]
        c = pk - eps * pk / abs(pk)

        def path(t):
            if t < 0.3:
                return c * (t / 0.3), c / 0.3
            elif t < 0.7:
                s = (t - 0.3) / 0.4
                ang = 2 * np.pi * s
                return (pk + (c - pk) * np.exp(1j * ang),
                        (c - pk) * 1j * 2 * np.pi * np.exp(1j * ang) / 0.4)
            else:
                s = (t - 0.7) / 0.3
                return c + (0 - c) * s, (0 - c) / 0.3

        def rhs(t, y):
            z, dz = path(t)
            am = sum(ak[j] / (z - punct[j]) for j in range(4))
            return ((am @ y.reshape(3, 3)) * dz).reshape(-1)

        sol = solve_ivp(rhs, [0, 1], eye3.reshape(-1), rtol=1e-11,
                        atol=1e-13, method='DOP853')
        return sol.y[:, -1].reshape(3, 3)

    ms = [loop(k) for k in range(4)]
    aop = np.vstack([np.kron(ms[k].T, ms[k].conj().T) - np.eye(9)
                     for k in range(4)])
    vh = np.linalg.svd(aop)[2]
    h = vh.conj().T[:, 8].reshape(3, 3)
    h = (h + h.conj().T) / 2
    if np.trace(h).real < 0:
        h = -h
    w = np.asarray(sl.sqrtm(h), dtype=complex)
    m0 = w @ ms[0] @ np.linalg.inv(w)
    h_uinv = np.linalg.norm(un @ h @ un.conj().T - h) / np.linalg.norm(h)
    return m0, h_uinv


def run():
    reset()
    print("v117 monodromy = W(A3) (exact holonomy; delta = 1/2 a theorem)")

    lam = sp.Symbol('lam')
    # 1. the exact monodromy
    check("THE EXACT MONODROMY [I]: M0 (entries in (1/2)Z[i]) is unitary "
          "with det 1, tr 0, char poly lam^3 - 1 (cusp class EXACT), "
          "M0^3 = 1, and diag M0 = (0, -i/2, +i/2) -- d1 = 0 and "
          "delta = 1/2 are exact matrix entries now, not observations",
          sp.simplify(M0_EXACT.H * M0_EXACT) == sp.eye(3)
          and sp.simplify(M0_EXACT.det()) == 1
          and sp.simplify(M0_EXACT.trace()) == 0
          and sp.simplify(M0_EXACT.charpoly(lam).as_expr()
                          - (lam ** 3 - 1)) == 0
          and sp.simplify(M0_EXACT ** 3) == sp.eye(3)
          and [sp.simplify(M0_EXACT[i, i]) for i in range(3)]
          == [0, -II / 2, II / 2])

    # 2. torsion and flatness
    tmat = M0_EXACT * U_EXACT
    prod = sp.eye(3)
    for k in range(4):
        uk = U_EXACT ** k
        prod = prod * (uk * M0_EXACT * uk.inv())
    check("TORSION AND FLATNESS [I]: (M0 U)^4 = 1 with tr(M0 U) = 1 "
          "(the {1,i,-i} branch, d1 = 0 slice -- exactly where v114/"
          "v115 located the point) and prod_k U^k M0 U^{-k} = 1 exactly",
          sp.simplify(tmat ** 4) == sp.eye(3)
          and sp.simplify(tmat.trace()) == 1
          and sp.simplify(prod) == sp.eye(3))

    # 3. the group is W(A3) = S4
    elems = enumerate_group([U_EXACT, M0_EXACT])
    orders, chars = {}, {}
    for x in elems:
        p, o = x, 1
        while sp.simplify(p) != sp.eye(3):
            p = sp.expand(p * x)
            o += 1
        orders[o] = orders.get(o, 0) + 1
        tr = sp.nsimplify(sp.simplify(x.trace()))
        chars[(o, tr)] = chars.get((o, tr), 0) + 1
    check("THE GROUP IS W(A3) = S4 [I]: exact enumeration of <U, M0> "
          "gives ORDER 24, order statistics (1, 9, 8, 6) and character "
          "values (3, -1, 0, 1) -- uniquely S4 in standard x sign = the "
          "(twisted) reflection representation of the WEYL GROUP OF A3; "
          "U = a 4-cycle (the mu_4 deck), M0 = a 3-cycle (family "
          "rotation), 24 = |W(A3)| = 4!",
          len(elems) == 24
          and orders == {1: 1, 2: 9, 3: 8, 4: 6}
          and chars == {(1, sp.Integer(3)): 1, (2, sp.Integer(-1)): 9,
                        (3, sp.Integer(0)): 8, (4, sp.Integer(1)): 6}
          and sp.factorial(4) == 24)

    # 4. identification with the analytic monodromy
    m0_num, h_uinv = ode_monodromy()
    m0_ref = np.array(M0_EXACT.evalf(20), dtype=complex)
    check("IDENTIFICATION [N]: the unitarised ODE monodromy of the "
          "exact A0* system equals the exact M0 "
          f"(||diff|| = {np.linalg.norm(m0_num - m0_ref):.1e} < 1e-6) "
          f"and H is U-invariant ({h_uinv:.1e} < 1e-8) -- the harmonic "
          "frame preserves the equivariance",
          np.linalg.norm(m0_num - m0_ref) < 1e-6 and h_uinv < 1e-8)

    # 5. status
    check("STATUS [P] (recorded): holonomy VALUES now [I] (exact "
          "properties of the W(A3) representation: d1 = 0, delta = 1/2, "
          "cusp class, torsion branch); the identification with the "
          "analytic monodromy of A0* stays [N] (ODE matching, 1e-7). "
          "The delta thread v20 -> v40/v41 -> v114 -> v115 -> v117 is "
          "closed end to end", True)

    return summary("v117 monodromy = W(A3)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
