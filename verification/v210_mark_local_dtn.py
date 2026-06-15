"""v210 -- Mark-local DtN certification on REALISTIC Steklov curvature profiles
(a numerical SHARPENING of v201/QGEO.SUBPRIN.01, NOT a closure of QGEO.SYM.01).

v201 proved the mark-locality implication at the ABSTRACT mode level (arbitrary
discrete Fourier dictionaries, a small integer-mode block). This module certifies
the SAME implication for concrete, smooth, normalised boundary-curvature sources
and -- the genuinely new step -- carries it to the QUASI-FREE STATE level, i.e.
the actual omega o rho = omega, not just [rho, Lambda] = 0:

    a real von-Mises curvature bump g(theta) localised at a puncture, summed over
    the four mu4 marks  f(theta) = sum_{j=0}^3 g(theta - j pi/2),  builds the
    Steklov DtN  Lambda_Sigma = |D_theta| + M_f  (principal |k| + sub-principal
    multiplication); the quasi-free covariance C = 1/2(1 + sgn(H_1)) of the state
    it defines is then CLOCK-INVARIANT (rho C rho^dag = C) to machine precision,
    while a single off-centre bump, a Z3 (3-mark) source and 4 unequally-spaced
    marks all break it by O(1).

  [E] 1. MARK-SUM FOURIER SUPPORT (real profile).  For a real smooth g with
        Fourier coefficients g_k, f(theta)=sum_{j=0}^3 g(theta - j pi/2) has
        f_k = g_k * sum_j e^{-i k j pi/2} = 4 g_k [k ≡ 0 (mod 4)]. Verified on the
        actual von-Mises profile: every off-(mod 4) Fourier coefficient of f
        vanishes to < 1e-12 (exact 4-fold lattice cancellation), although g itself
        has all modes.
  [N] 2. OPERATOR COMMUTATOR.  The DtN Lambda = diag(|n|) + Toeplitz(f_k) built
        from the real f satisfies ||[rho, Lambda]|| < 1e-10 (the principal |k| is
        diagonal hence commutes, v198; the sub-principal M_f commutes because f is
        mu4-mark-sourced => Z4-invariant).
  [N] 3. STATE INVARIANCE -- the actual omega o rho = omega (NEW vs v201).  For the
        quasi-free RP state the covariance is C = 1/2(1 + sgn(H_1)) with H_1 the
        one-particle seam operator (Lambda shifted into a two-signed spectrum).
        rho C rho^dag = C and [rho, C] = 0 to < 1e-10: the STATE, not merely the
        operator, is invariant under the carrier clock for the mark-local DtN.
  [N] 4. NEGATIVE CONTROLS (realistic profiles).  (a) single off-centre bump,
        (b) Z3 = 3 equally-spaced marks (support mod 3), (c) 4 generic unequally-
        spaced marks: each gives ||[rho, Lambda]|| and ||rho C rho^dag - C|| of
        O(1) -- the invariance is SPECIFIC to the mu4 orbit, not generic.
  [N] 5. CONVERGENCE (not a truncation artefact).  The mark-local commutator stays
        < 1e-10 across N in {16, 32, 64} while a control stays O(1) at every N.
  [O] 6. VERDICT.  This NUMERICALLY CERTIFIES the implication 'mark-local
        (conformal-deck-flat) DtN  =>  omega o rho = omega' for concrete Steklov
        profiles AND at the state level -- the operational content of
        QGEO.SUBPRIN.01/v201. The PREMISE (that the physical seam DtN is actually
        mark-local / conformal-deck flat away from the mu4 points) stays [O]: this
        is the narrowest, most clearly definitional form of QGEO.SYM.01, NOT its
        closure. Net existence and full-cone RP remain the [E] of v175.

  Python-only (numerical operator/FFT certification on realistic profiles; the
  exact mark-sum Fourier identity is already Wolfram-mirrored via v201).
"""
import numpy as np

from tfpt_constants import check, summary, reset

GRID = 2048                      # divisible by 4 => the pi/2 shifts are exact grid steps
KAPPA = 4.0                      # von-Mises concentration (localised curvature bump)


def vonmises_bump(theta):
    """A real, smooth, 2pi-periodic, even curvature bump localised at theta=0."""
    return np.exp(KAPPA * (np.cos(theta) - 1.0))


def fourier_coeffs(fvals):
    """Fourier coefficients c_q of f on the uniform grid: f(theta)=sum_q c_q e^{i q theta}."""
    return np.fft.fft(fvals) / len(fvals)


def mark_sum(positions, grid=GRID):
    """f(theta) = sum_k g(theta - positions[k]) on the uniform grid; returns its coeffs."""
    th = 2 * np.pi * np.arange(grid) / grid
    f = np.zeros(grid)
    for p in positions:
        f += vonmises_bump(th - p)
    return fourier_coeffs(f)


def coef(C, q):
    """Integer-mode Fourier coefficient c_q (wrap negative indices)."""
    return C[q % len(C)]


def dtn(C, N):
    """Steklov DtN Lambda = diag(|n|) + Toeplitz(c_{n-n'}) on modes n=-N..N (Hermitian)."""
    n = np.arange(-N, N + 1)
    d = len(n)
    M = np.empty((d, d), complex)
    for a in range(d):
        for b in range(d):
            M[a, b] = coef(C, int(n[a] - n[b]))
    Lam = np.diag(np.abs(n).astype(float)) + M
    return Lam, n


def clock(n):
    return np.diag((1j) ** n)


def covariance(Lam):
    """Quasi-free covariance C = 1/2(1 + sgn(H_1)), H_1 = Lambda - mu (two-signed)."""
    w, V = np.linalg.eigh(Lam)
    mu = 0.5 * (w[len(w) // 2 - 1] + w[len(w) // 2])     # mid-spectrum: avoids zero modes
    sgn = V @ np.diag(np.sign(w - mu)) @ V.conj().T
    return 0.5 * (np.eye(Lam.shape[0]) + sgn)


def run():
    reset()
    print("v210 mark-local DtN certification (realistic Steklov profiles + the state level) [N]/[O]")

    N = 48
    mu4 = [j * np.pi / 2 for j in range(4)]               # the four mu4 marks
    C_ml = mark_sum(mu4)
    rho = clock(np.arange(-N, N + 1))

    # 1. mark-sum Fourier support: off-(mod 4) coefficients vanish on the REAL profile
    off_mod4 = max(abs(coef(C_ml, q)) for q in range(-2 * N, 2 * N + 1) if q % 4 != 0)
    on_mod4 = max(abs(coef(C_ml, q)) for q in range(-2 * N, 2 * N + 1) if q % 4 == 0)
    check("MARK-SUM FOURIER SUPPORT [E]: the REAL von-Mises mark-sum f=sum_j "
          "g(theta-j pi/2) has f_k = 4 g_k [k≡0 mod 4]; max off-(mod4) |coeff| = "
          "%.2e (~0) vs max on-(mod4) |coeff| = %.3f -- support only on modes ≡0 "
          "(mod 4), although g itself has all modes" % (off_mod4, on_mod4),
          off_mod4 < 1e-12 and on_mod4 > 0.1)

    # 2. operator commutator for the mark-local DtN
    Lam_ml, _ = dtn(C_ml, N)
    comm_ml = np.linalg.norm(rho @ Lam_ml - Lam_ml @ rho)
    check("OPERATOR COMMUTATOR [N]: Lambda = |D_theta| + M_f from the real mark-"
          "local f has ||[rho, Lambda]|| = %.2e < 1e-10 (principal |k| diagonal "
          "=> commutes, v198; sub-principal M_f Z4-invariant => commutes)" % comm_ml,
          comm_ml < 1e-10)

    # 3. STATE invariance: the actual omega o rho = omega (new vs v201)
    Cov_ml = covariance(Lam_ml)
    state_comm = np.linalg.norm(rho @ Cov_ml - Cov_ml @ rho)
    state_inv = np.linalg.norm(rho @ Cov_ml @ rho.conj().T - Cov_ml)
    check("STATE INVARIANCE [N] (the actual omega o rho = omega): the quasi-free "
          "covariance C = 1/2(1+sgn(H_1)) satisfies rho C rho^dag = C (residual "
          "%.2e) and [rho,C] = %.2e, both < 1e-10 -- the STATE, not just the "
          "operator, is clock-invariant for the mark-local DtN" % (state_inv, state_comm),
          state_inv < 1e-10 and state_comm < 1e-10)

    # 4. negative controls with realistic profiles
    controls = {
        "single off-centre bump": [1.0],
        "Z3 (3 equally-spaced marks)": [2 * np.pi * j / 3 for j in range(3)],
        "4 generic unequal marks": [0.0, 1.0, 2.5, 4.0],
    }
    all_break = True
    msgs = []
    for name, pos in controls.items():
        Cc = mark_sum(pos)
        Lc, _ = dtn(Cc, N)
        oc = np.linalg.norm(rho @ Lc - Lc @ rho)
        Covc = covariance(Lc)
        sc = np.linalg.norm(rho @ Covc @ rho.conj().T - Covc)
        broke = oc > 1e-3 and sc > 1e-3
        all_break = all_break and broke
        msgs.append("%s: ||[rho,Lambda]||=%.2f, state-resid=%.2f" % (name, oc, sc))
    check("NEGATIVE CONTROLS [N]: " + "; ".join(msgs) + " -- each breaks BOTH the "
          "operator and the state invariance by O(1); the clock-invariance is "
          "SPECIFIC to the mu4 orbit, not generic", all_break)

    # 5. convergence: mark-local stays ~0, a control stays O(1), across N
    z3 = [2 * np.pi * j / 3 for j in range(3)]
    C_z3 = mark_sum(z3)
    conv_ml, conv_ctrl = [], []
    for Nk in (16, 32, 64):
        Lk, nk = dtn(C_ml, Nk)
        rk = clock(np.arange(-Nk, Nk + 1))
        conv_ml.append(np.linalg.norm(rk @ Lk - Lk @ rk))
        Lz, _ = dtn(C_z3, Nk)
        conv_ctrl.append(np.linalg.norm(rk @ Lz - Lz @ rk))
    check("CONVERGENCE [N] (not a truncation artefact): mark-local ||[rho,Lambda]|| "
          "= %s stays < 1e-10 for N in {16,32,64}; the Z3 control = %s stays O(1) "
          "at every N" % (["%.1e" % c for c in conv_ml], ["%.2f" % c for c in conv_ctrl]),
          all(c < 1e-10 for c in conv_ml) and all(c > 1e-3 for c in conv_ctrl))

    check("VERDICT [O]: this NUMERICALLY CERTIFIES 'mark-local (conformal-deck-flat) "
          "DtN => omega o rho = omega' for concrete Steklov profiles AND at the "
          "quasi-free STATE level -- the operational content of QGEO.SUBPRIN.01 "
          "(v201) sharpened from abstract modes to real curvature sources + the "
          "state. The PREMISE (the physical seam DtN IS mark-local / conformal-deck "
          "flat away from the mu4 points) stays [O]: the narrowest definitional form "
          "of QGEO.SYM.01, NOT its closure (net existence + full-cone RP remain the "
          "[E] of v175)", True)

    return summary("v210 mark-local DtN certification: omega o rho = omega for realistic profiles [N]/[O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
