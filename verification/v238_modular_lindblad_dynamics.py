"""v238 -- the STATIC->DYNAMIC flip: modular flow (reversible) + the recovery
channel read as a Markov/Lindblad generator (irreversible), with the dissipative
gap EQUAL to the OS mass gap.  Companion to v196/v198 (modular) and v221/v64
(recovery): those state the seam structure STATICALLY -- a commutator condition,
a per-step contraction bound, a mass-gap number.  This module reads the SAME
objects DYNAMICALLY and shows the two are one.

The seam already owns (a) a modular Hamiltonian Lambda_Sigma = log Delta_omega on
the H^1 block (v196/v198) and (b) a recovery channel T with spectrum
{1, (2/3)^6, (1/3)^6} (v221).  Treated statically they are a commutator and a
contraction bound.  Treated dynamically:

  * the modular flow sigma_t = e^{i t Lambda_Sigma} is the REVERSIBLE
    (Hamiltonian) one-parameter group (Tomita-Takesaki).  [rho, Lambda_Sigma] = 0
    -- the v198 state-invariance -- IS the conservation of the mu4 charge along
    that flow.  So the STATIC v198 commutator is the conservation law of modular
    time.
  * the recovery generator L = log T is the IRREVERSIBLE (dissipative) generator
    of a continuous doubly-stochastic / CPTP-classical semigroup e^{L tau}, with
    e^{L*1} = T (it reproduces the v221 channel) and a unique stationary state
    (the arrow of time, matching v64's T^n -> rank-1 projector).
  * THE KEYSTONE IDENTITY: the dissipative spectral gap (the slowest relaxation
    rate) = -log((2/3)^6) = 6 log(3/2) = the OS/RP mass gap Delta of v64.  The
    STATIC recovery bound (2/3)^6 (v221) and the DYNAMICAL mass gap 6 log(3/2)
    (v64) are ONE number, one exponentiated -- exactly the point at which the
    static compiler becomes a dynamics.

  [E] 1. MODULAR FLOW = REVERSIBLE GENERATOR.  sigma_t = e^{i t Lambda_Sigma} is a
        unitary one-parameter group (sigma_s sigma_t = sigma_{s+t}, generator
        d/dt|_0 = i Lambda_Sigma); the mu4 clock is conserved, rho sigma_t
        rho^{-1} = sigma_t for all t  <=>  [rho, Lambda_Sigma] = 0 (the v198
        state-invariance).  NEG: a mu4-breaking off-diagonal Lambda breaks it.
  [E] 2. RECOVERY = DISSIPATIVE GENERATOR.  L = log T is real-symmetric with
        off-diagonals >= 0 and zero row/column sums (a valid doubly-stochastic /
        CPTP-classical Markov generator); e^{L*1} = T, and e^{L tau} -> the
        rank-1 projector onto the stationary (democratic) mode (the arrow of
        time).
  [E] 3. KEYSTONE: dissipative gap = OS mass gap.  -log((2/3)^6) = 6 log(3/2) =
        Delta (v64).  NEG: a free rate r != (2/3)^6 breaks the identity.
  [E] 4. GKSL SPLIT.  G = i Lambda_Sigma + L: reversible part anti-Hermitian
        (purely imaginary spectrum, conserving) + dissipative part symmetric
        (real spectrum <= 0, gap Delta) -- the canonical Hamiltonian + Lindbladian
        split of a quantum dynamical semigroup; the arrow of time is the
        dissipative (real) part.
  [O] 5. THE RESIDUAL.  What is NOT closed: (a) that sigma_t is the GEOMETRIC
        modular flow on the FULL seam algebra (Connes-Rovelli 'thermal time =
        physical time' = the Bisognano-Wichmann / QGEO.SYM.01 residual, v198), and
        (b) that L's continuum embedding extends beyond the finite block.  The
        same single open premise as v196/v198 -- a target, not a closure.

  Python-only (finite-block linear algebra; matrix exp/log via the symmetric
  eigendecomposition, numpy only).  The finite identities are exact; the
  geometric-modular-flow premise is the open QGEO.SYM.01 residual (v198), [O].
"""
import numpy as np

from tfpt_constants import check, summary, reset

LAMBDA2 = (2 / 3) ** 6      # 64/729, the v221 recovery rate
LAMBDA3 = (1 / 3) ** 6


def _sym_funcm(M, f):
    """f(M) for a real-symmetric M via its eigendecomposition (numpy only)."""
    w, V = np.linalg.eigh(M)
    return (V * f(w)) @ V.T


def _expm_iH(H, t):
    """exp(i t H) for a Hermitian H via its eigendecomposition (numpy only)."""
    w, V = np.linalg.eigh(H)
    return (V * np.exp(1j * t * w)) @ V.conj().T


def run():
    reset()
    print("v238  static->dynamic flip: modular flow + recovery Markov generator; "
          "dissipative gap = OS mass gap 6 log(3/2)")

    # ---- the seam recovery channel T (exactly as v221) ---------------------
    u2 = np.array([1.0, -1.0, 0.0]); u2 /= np.linalg.norm(u2)
    u3 = np.array([1.0, 1.0, -2.0]); u3 /= np.linalg.norm(u3)   # Nariai traceless anchor
    J = np.ones((3, 3)) / 3.0
    T = J + LAMBDA2 * np.outer(u2, u2) + LAMBDA3 * np.outer(u3, u3)

    # ---- 1. modular flow = reversible (Hamiltonian) generator --------------
    rho = np.diag([1j, -1.0 + 0j, -1j])                 # the mu4 clock (v196/v198)
    Lam = np.diag([1.0, 2.0, 3.0]).astype(complex)       # Lambda_Sigma = log Delta_omega (any real diagonal)
    ts = [0.3, 0.7, 1.1]

    def sigma(t):
        return _expm_iH(Lam, t)

    grp = all(np.allclose(sigma(s) @ sigma(t), sigma(s + t)) for s in ts for t in ts)
    unitary = all(np.allclose(sigma(t).conj().T @ sigma(t), np.eye(3)) for t in ts)
    dt = 1e-6
    gen_ok = np.allclose((sigma(dt) - np.eye(3)) / dt, 1j * Lam, atol=1e-4)
    conserved = all(np.allclose(rho @ sigma(t) @ np.linalg.inv(rho), sigma(t)) for t in ts)
    comm0 = np.allclose(rho @ Lam - Lam @ rho, 0)
    check("MODULAR FLOW = REVERSIBLE GENERATOR [E]: sigma_t = e^{i t Lambda_Sigma} "
          "is a unitary one-parameter group (sigma_s sigma_t = sigma_{s+t}, "
          "d/dt|_0 = i Lambda_Sigma); the mu4 clock is CONSERVED -- rho sigma_t "
          "rho^{-1} = sigma_t for all t  <=>  [rho,Lambda_Sigma]=0 -- so the STATIC "
          "v198 state-invariance IS the conservation law of modular time",
          grp and unitary and gen_ok and conserved and comm0)

    # NEG: a mu4-breaking off-diagonal Lambda breaks the conservation law
    Lam_b = Lam.copy(); Lam_b[0, 1] = 0.5; Lam_b[1, 0] = 0.5
    sig_b = _expm_iH(Lam_b, 0.7)
    broken = not np.allclose(rho @ sig_b @ np.linalg.inv(rho), sig_b)
    comm_b = not np.allclose(rho @ Lam_b - Lam_b @ rho, 0)
    check("NEG mu4-breaking [E]: an off-diagonal (mu4-breaking) Lambda_Sigma gives "
          "[rho,Lambda]!=0, so rho sigma_t rho^{-1} != sigma_t -- the mu4 charge is "
          "no longer conserved by modular time (cf. v196's E_fail perturbation)",
          broken and comm_b)

    # ---- 2. recovery = dissipative (Lindblad/Markov) generator -------------
    L = _sym_funcm(T, np.log)                            # generator log T (T real-symmetric PD)
    offdiag_nonneg = all(L[i, j] >= -1e-12 for i in range(3) for j in range(3) if i != j)
    zero_sums = np.allclose(L.sum(axis=1), 0) and np.allclose(L.sum(axis=0), 0)
    reproduces = np.allclose(_sym_funcm(L, np.exp), T)   # e^{L*1} = T
    big = _sym_funcm(50.0 * L, np.exp)                   # e^{L tau}, tau=50
    arrow = np.allclose(big, J, atol=1e-6)
    check("RECOVERY = DISSIPATIVE GENERATOR [E]: L = log T is a valid continuous "
          "generator -- real-symmetric, off-diagonals >= 0, zero row/column sums "
          "(a doubly-stochastic / CPTP-classical Markov generator); e^{L*1} = T "
          "reproduces the v221 channel and e^{L tau} -> the rank-1 projector onto "
          "the stationary (democratic) mode as tau->inf (the arrow of time, "
          "matching v64's T^n -> projector)",
          offdiag_nonneg and zero_sums and reproduces and arrow)

    # ---- 3. KEYSTONE: dissipative gap = OS mass gap ------------------------
    evL = sorted(np.linalg.eigvalsh(L))                  # {-6 log 3, -6 log(3/2), 0}
    diss_gap = -max(e for e in evL if e < -1e-9)         # slowest non-zero rate = -log((2/3)^6)
    Delta = 6 * np.log(1.5)                              # the OS/RP mass gap (v64)
    check("KEYSTONE: DISSIPATIVE GAP = OS MASS GAP [E]: the slowest relaxation rate "
          "of L = -log((2/3)^6) = 6 log(3/2) = %.6f = the OS/RP mass gap Delta (v64). "
          "The STATIC recovery bound (2/3)^6 (v221) and the DYNAMICAL mass gap "
          "6 log(3/2) (v64) are ONE number, one exponentiated -- the point where the "
          "static compiler becomes a dynamics" % diss_gap,
          abs(diss_gap - Delta) < 1e-9 and abs(diss_gap + np.log(LAMBDA2)) < 1e-9)

    # NEG: a free recovery rate r != (2/3)^6 breaks the gap=mass-gap identity
    r_free = 0.5
    Tf = J + r_free * np.outer(u2, u2) + LAMBDA3 * np.outer(u3, u3)
    Lf = _sym_funcm(Tf, np.log)
    evLf = sorted(np.linalg.eigvalsh(Lf))
    gap_f = -max(e for e in evLf if e < -1e-9)
    check("NEG free rate [E]: replacing (2/3)^6 by r=0.5 gives dissipative gap "
          "-log(0.5) = %.4f != 6 log(3/2) = %.4f -- the gap=mass-gap identity is NOT "
          "generic (anti-numerology, cf. v221's free-ratio control)" % (gap_f, Delta),
          abs(gap_f + np.log(r_free)) < 1e-9 and abs(gap_f - Delta) > 0.3)

    # ---- 4. GKSL split: reversible (imaginary) + dissipative (real <= 0) ----
    rev_spec = np.linalg.eigvals(1j * Lam)
    rev_imag = np.allclose(rev_spec.real, 0)
    sym = np.allclose(L, L.T)
    check("GKSL SPLIT [E]: G = i Lambda_Sigma (reversible) + L (dissipative): the "
          "reversible generator is anti-Hermitian (spectrum purely IMAGINARY, "
          "unitary/conserving) and the dissipative generator is symmetric (spectrum "
          "REAL and <= 0, gap Delta) -- the canonical Hamiltonian + Lindbladian split "
          "of a quantum dynamical semigroup; the arrow of time is the dissipative "
          "(real) part",
          rev_imag and sym and max(evL) < 1e-9)

    # ---- 5. the residual, honestly typed ----------------------------------
    check("THE RESIDUAL [O] (honest, NOT a closure): this EXHIBITS the static->"
          "dynamic flip on the finite block -- modular flow as the reversible "
          "generator, log T as the dissipative one, dissipative gap = OS mass gap. "
          "NOT closed: (a) that sigma_t is GEOMETRIC modular flow on the FULL seam "
          "algebra (Connes-Rovelli 'thermal time = physical time' = the "
          "Bisognano-Wichmann / QGEO.SYM.01 residual, v198), and (b) that L's "
          "continuum embedding extends beyond the finite block. Same single open "
          "premise as v196/v198 -- a target, not a closure", True)

    return summary("v238 static->dynamic flip (modular flow + recovery Lindblad "
                   "generator; dissipative gap = OS mass gap)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
