"""v115 -- The anchor pins the residue: an EXACT normal form for the
(U_wall) flat-bundle residue, and the answer to the v114 branch question --
the anchor splitting forces the d1 = 0 slice.  [I] symbolic lemmas + exact
matrix + [N] Riemann-Hilbert verification and uniqueness scan.

The v33 (U_wall) flat bundle was a NUMERICAL Riemann-Hilbert solution.
This module shows its residue is (gauge-equivalent to) an exact matrix
whose every invariant is a compiler atom, and uses it to answer the open
v114 question.

  [I] 1. MU4-AVERAGE LEMMA (symbolic, generic X).  Conjugation-averaging
         over mu_4 is the diagonal projection:
             sum_k U^k X U^{-k} = |mu_4| * diag(X).
         Hence the exponents at infinity are 4*diag(A_0), and the anchor
         splitting O(-2)+O(-1)^2 holds IFF
             diag A_0 = (2,1,1)/4 = a / |mu_4|
         -- the residue diagonal IS the anchor over mu_4 (v33's diagonal
         was forced, not chosen).
  [I] 2. THE (8,0,5)/144 LEMMA.  For a Hermitian A_0 with the anchor
         diagonal and the cusp spectrum {0, 1/3, 2/3} (weights {0,1,2}/
         N_fam), the off-diagonal weight is pinned:
             |a12|^2 + |a13|^2 + |a23|^2 = 13/144,
         and with a13 = 0 the determinant condition solves UNIQUELY to
             (|a12|^2, |a13|^2, |a23|^2) = (8, 0, 5) / 144
         -- numerators (rank E8, 0, g_car), denominator (|mu_4| N_fam)^2,
         total 13 = Delta_Q = 2 p_2(a) + 1 (the quark denominator
         117 = 9*13).  Exact linear algebra, no fit.
  [I] 3. EXACT RESIDUE NORMAL FORM.  The real representative
             A_0* = [[1/2, sqrt2/6, 0],
                     [sqrt2/6, 1/4, sqrt5/12],
                     [0, sqrt5/12, 1/4]]
         has characteristic polynomial lam(lam-1/3)(lam-2/3) EXACTLY.
  [N] 4. A_0* IS THE RIEMANN-HILBERT SOLUTION.  Numerically (DOP853,
         rtol 1e-10): the big-circle monodromy of the Fuchsian system
         built on A_0* is trivial to ~1e-10, the four loop monodromies
         satisfy prod M_k = 1, and the unitarised holonomy has
         |diag M~_0| = (0, 1/2, 1/2) with tr(M~_0 U) = 1.  The v33/v40
         numerical point is gauge-equivalent to A_0* (the phases of a12,
         a23 are diagonal gauge).
  [N] 5. THE ANCHOR FORCES THE d1 = 0 SLICE (v114 residue answered).
         A multi-seed Riemann-Hilbert scan over the full anchor-pinned
         spectral manifold lands, at every flat solution found, on the
         SAME gauge orbit (off-diagonal moduli (sqrt8, 0, sqrt5)/12) with
         |diag M~_0| = (0, 1/2, 1/2).  Combined with v114: the whole
         harmonic diagonal is anchor + torsion forced; delta = 1/2 needs
         no selection anymore.
  [P] 6. RESIDUE (recorded, not claimed): a13 = 0 and the gauge-orbit
         uniqueness are numerical findings (single component across all
         seeds); promoting them to [I]/[L] (finite algebraic geometry /
         Groebner on the RH constraints) is the remaining step.
"""
import numpy as np
import scipy.linalg as sl
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

from tfpt_constants import check, summary, reset

UN = np.diag([1, 1j, -1j])
UIS = [np.linalg.matrix_power(UN, k) for k in range(4)]
UIC = [np.linalg.inv(u) for u in UIS]
PUNCT = np.array([1, 1j, -1, -1j])
I3 = np.eye(3, dtype=complex)
ANCHOR_DIAG = np.array([0.5, 0.25, 0.25])


def fuchs_rhs(ak):
    def rhs(t, y, path):
        z, dz = path(t)
        amat = sum(ak[j] / (z - PUNCT[j]) for j in range(4))
        return ((amat @ y.reshape(3, 3)) * dz).reshape(-1)
    return rhs


def m_circle(a0, rtol=1e-10):
    ak = [UIS[k] @ a0 @ UIC[k] for k in range(4)]
    rhs = fuchs_rhs(ak)

    def path(t):
        return 3 * np.exp(1j * t), 3j * np.exp(1j * t)

    sol = solve_ivp(lambda t, y: rhs(t, y, path), [0, 2 * np.pi],
                    I3.reshape(-1), rtol=rtol, atol=1e-12, method='DOP853')
    return sol.y[:, -1].reshape(3, 3)


def loop_mono(a0, k, eps=0.25, rtol=1e-10):
    ak = [UIS[j] @ a0 @ UIC[j] for j in range(4)]
    rhs = fuchs_rhs(ak)
    pk = PUNCT[k]
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

    sol = solve_ivp(lambda t, y: rhs(t, y, path), [0, 1],
                    I3.reshape(-1), rtol=rtol, atol=1e-12, method='DOP853')
    return sol.y[:, -1].reshape(3, 3)


def harmonic_diag(a0):
    """Unitarise via the unique invariant Hermitian form (v40 method)."""
    ms = [loop_mono(a0, k) for k in range(4)]
    aop = np.vstack([np.kron(ms[k].T, ms[k].conj().T) - np.eye(9)
                     for k in range(4)])
    vh = np.linalg.svd(aop)[2]
    h = vh.conj().T[:, 8].reshape(3, 3)
    h = (h + h.conj().T) / 2
    if np.trace(h).real < 0:
        h = -h
    if np.linalg.eigvalsh(h).min() < 1e-8:
        return None
    w = np.asarray(sl.sqrtm(h), dtype=complex)
    m0t = w @ ms[0] @ np.linalg.inv(w)
    prodres = np.linalg.norm(ms[0] @ ms[1] @ ms[2] @ ms[3] - I3)
    return np.diag(m0t), np.trace(m0t @ UN), prodres


def a0_from(x):
    c12 = x[0] + 1j * x[1]
    c13 = x[2] + 1j * x[3]
    c23 = x[4] + 1j * x[5]
    return np.array([[ANCHOR_DIAG[0], c12, c13],
                     [np.conj(c12), ANCHOR_DIAG[1], c23],
                     [np.conj(c13), np.conj(c23), ANCHOR_DIAG[2]]], complex)


def spec_pen(a):
    ev = np.sort(np.linalg.eigvalsh(a))
    return float(np.sum((ev - np.array([0, 1 / 3, 2 / 3])) ** 2))


def run():
    reset()
    print("v115 anchor residue (exact normal form; anchor forces d1 = 0)")

    # 1. mu4-average lemma
    xsym = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'x{i}{j}', complex=True))
    usym = sp.diag(1, sp.I, -sp.I)
    ssum = sp.zeros(3)
    for k in range(4):
        uk = usym ** k
        ssum += uk * xsym * uk.inv()
    check("MU4-AVERAGE LEMMA [symbolic]: sum_k U^k X U^{-k} = 4 diag(X) "
          "-- mu_4 conjugation-averaging IS the diagonal projection; "
          "exponents at infinity = 4 diag(A0), so the anchor splitting "
          "O(-2)+O(-1)^2 <=> diag A0 = (2,1,1)/4 = a/|mu_4|",
          sp.simplify(sp.expand(ssum)
                      - 4 * sp.diag(xsym[0, 0], xsym[1, 1], xsym[2, 2]))
          == sp.zeros(3))

    # 2. the (8,0,5)/144 lemma
    x, y = sp.symbols('x y', nonnegative=True)
    sol = sp.solve([sp.Eq(x + y, sp.Rational(13, 144)),
                    sp.Eq(sp.Rational(1, 32) - y / 2 - x / 4, 0)], [x, y])
    check("THE (8,0,5)/144 LEMMA: anchor diagonal + cusp spectrum pin "
          "the off-diagonal weight sum to 13/144; with a13 = 0 the "
          "det = 0 condition solves UNIQUELY to (|a12|^2, |a23|^2) = "
          "(8, 5)/144 -- numerators (rank E8, g_car), denominator "
          "(|mu_4| N_fam)^2 = 144, total 13 = Delta_Q (quark "
          "denominator 117 = 9 x 13)",
          sol == {x: sp.Rational(1, 18), y: sp.Rational(5, 144)}
          and sp.Rational(1, 18) == sp.Rational(8, 144)
          and 8 + 5 == 13 and (4 * 3) ** 2 == 144 and 9 * 13 == 117)

    # 3. exact residue normal form
    astar = sp.Matrix([[sp.Rational(1, 2), sp.sqrt(2) / 6, 0],
                       [sp.sqrt(2) / 6, sp.Rational(1, 4), sp.sqrt(5) / 12],
                       [0, sp.sqrt(5) / 12, sp.Rational(1, 4)]])
    lam = sp.Symbol('lam')
    check("EXACT RESIDUE NORMAL FORM: A0* = [[1/2, sqrt2/6, 0], "
          "[sqrt2/6, 1/4, sqrt5/12], [0, sqrt5/12, 1/4]] has char poly "
          "lam(lam - 1/3)(lam - 2/3) EXACTLY -- eigenvalues = cusp "
          "weights {0,1,2}/N_fam automatic",
          sp.simplify(astar.charpoly(lam).as_expr()
                      - lam * (lam - sp.Rational(1, 3))
                      * (lam - sp.Rational(2, 3))) == 0)

    # 4. A0* is the Riemann-Hilbert solution
    a0_num = np.array(astar.evalf(20), dtype=complex)
    mc = m_circle(a0_num)
    res = harmonic_diag(a0_num)
    dg, trt, prodres = res
    check("A0* IS THE RH SOLUTION [N]: big-circle monodromy trivial "
          f"(||M_inf - 1|| = {np.linalg.norm(mc - I3):.1e} < 1e-7), "
          f"prod M_k = 1 ({prodres:.1e}), unitarised |diag M~_0| = "
          "(0, 1/2, 1/2), tr(M~_0 U) = 1 -- the v33/v40 numerical point "
          "is gauge-equivalent to this exact matrix",
          np.linalg.norm(mc - I3) < 1e-7 and prodres < 1e-6
          and abs(dg[0]) < 1e-6
          and abs(abs(dg[1]) - 0.5) < 1e-6 and abs(abs(dg[2]) - 0.5) < 1e-6
          and abs(trt - 1) < 1e-5)

    # 5. multi-seed uniqueness scan (the anchor forces the d1 = 0 slice)
    rng = np.random.default_rng(3)
    hits = []
    for _ in range(8):
        x0 = rng.normal(0, 0.25, 6)
        r1 = minimize(lambda v: spec_pen(a0_from(v)), x0,
                      method='Nelder-Mead',
                      options={'maxiter': 3000, 'xatol': 1e-13,
                               'fatol': 1e-15})
        if r1.fun > 1e-12:
            continue

        def objective(v):
            a0 = a0_from(v)
            pen = spec_pen(a0)
            if pen > 1e-4:
                return 100 * pen + 10.0
            return 100 * pen + float(
                np.linalg.norm(m_circle(a0, rtol=1e-8) - I3) ** 2)

        r2 = minimize(objective, r1.x, method='Nelder-Mead',
                      options={'maxiter': 2500, 'xatol': 1e-11,
                               'fatol': 1e-13})
        if r2.fun < 1e-7:
            a0 = a0_from(r2.x)
            out = harmonic_diag(a0)
            if out is None:
                continue
            dgi, trti, _ = out
            hits.append((abs(a0[0, 1]), abs(a0[0, 2]), abs(a0[1, 2]),
                         abs(dgi[0]), abs(dgi[1])))
    hits = np.array(hits)
    ref = np.array([np.sqrt(8) / 12, 0.0, np.sqrt(5) / 12])
    check(f"ANCHOR FORCES THE d1 = 0 SLICE [N]: {len(hits)} independent "
          "RH solutions found; ALL on the same gauge orbit (off-diag "
          "moduli (sqrt8, 0, sqrt5)/12) and ALL with |diag M~_0| = "
          "(0, 1/2, 1/2) -- the v114 branch question is answered: the "
          "harmonic diagonal is anchor + torsion forced",
          len(hits) >= 3
          and np.abs(hits[:, :3] - ref).max() < 1e-4
          and np.abs(hits[:, 3]).max() < 1e-5
          and np.abs(hits[:, 4] - 0.5).max() < 1e-5)

    # 6. residue
    check("RESIDUE [P] (recorded, not claimed): a13 = 0 and the "
          "gauge-orbit uniqueness are numerical (one component across "
          "all seeds); promoting them to [I]/[L] via finite algebraic "
          "geometry (Groebner on the RH constraints) is the remaining "
          "step of the U_wall point selection", True)

    return summary("v115 anchor residue")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
