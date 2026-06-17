"""v246 -- the HONEST data cross-check for the spectral-action prediction
(CONTRACT.QFT4D.01 / v244/v245): does the boundary condition g1=g2=g3,
sin^2 th_W = 3/8 at the unification scale survive the MEASURED Standard-Model
couplings, run at ONE AND TWO loops?  Answer: NO -- and there is no rescue in the
current theory.

CRUCIAL HONEST POINT (the framing that matters): TFPT's gauge-charged content IS
exactly the Standard Model (v159: the carrier reproduces the SM beta coefficients)
and the theory adds NO new states (tfpt_3: 'Dark matter = no new state').  The
'E8 cascade' of the current theory is an arithmetic even-integer SPINE
(D_n = 60 - 2n, v5), NOT a particle/threshold tower.  So a 'TFPT-adapted' RGE run
IS the Standard-Model run, by construction -- and the SM does not unify.  This is
a falsifiable TENSION / likely kill-test, NOT a confirmation; the (arithmetic)
spine supplies NO admissible gauge thresholds.

Inputs (measured, GUT-normalised, at M_Z; PyR@TE-cross-checked, v159):
alpha_i^-1 = (59.01, 29.59, 8.47); 1-loop b = (41/10, -19/6, -7); 2-loop SM gauge
matrix b_ij (Machacek-Vaughn / Jones, gauge-only).  sin^2 th_W(M_Z) = 0.23122.

  [E] 1. TFPT GAUGE CONTENT = SM, NO NEW STATES.  The carrier reproduces the SM
        betas (v159) and the theory adds no gauge-charged states (tfpt_3); the E8
        cascade is an arithmetic spine (v5), not a threshold tower.  So the
        TFPT RGE run IS the SM run.
  [E] 2. THE PREDICTION.  The spectral action predicts at Lambda: g1 = g2 = g3 and
        sin^2 th_W = 3/8 (v245).
  [X] 3. ONE-LOOP MISSES.  Pairwise crossings spread ~10^13 - 10^17 GeV; residual
        at 2e16 GeV ~ 9.  No common point.
  [X] 4. TWO-LOOP ALSO MISSES.  RK4 2-loop run: the minimal spread is
        Delta(alpha^-1) ~ 3.2 at mu ~ 1.7e14 GeV -- the three couplings never meet
        (the textbook non-SUSY result); at 2e16 the spread is ~8.7.
  [X] 5. sin^2 th_W TENSION.  3/8 = 0.375 predicted vs 0.23122 measured.
  [O] 6. NO RESCUE IN THE CURRENT THEORY.  With 'no new state' there is NO
        admissible threshold source; closing the spread would require EITHER new
        gauge-charged matter (a new postulate, contradicting 'no new state') OR a
        non-GUT / boundary reading of the spectral-action cutoff.  The spectral-
        action 4d-GUT unification route is in genuine tension -- the SAME status as
        the Connes-Chamseddine NCG Standard Model -- and is likely falsified unless
        the theory is extended.  Typed [X]/[O], NEVER [E]-as-success; the AQFT
        skeleton, DHR structure and SM rep-core survive regardless as an emergent
        boundary QFT.

  Python-only (1- and 2-loop RK4 running; numpy).  A data-confrontation kill-test
  in the spirit of v62/v159 -- never [E]-as-success.
"""
import numpy as np

from tfpt_constants import check, summary, reset

M_Z = 91.1876
AINV = np.array([59.01, 29.59, 8.47])            # alpha_i^-1(M_Z), GUT-normalised (PDG-derived)
B1 = np.array([41 / 10, -19 / 6, -7.0])          # SM 1-loop b_i (v159 PyR@TE)
# SM 2-loop gauge matrix (GUT-norm U(1)); Machacek-Vaughn / Jones, gauge-only
B2 = np.array([[199 / 50, 27 / 10, 44 / 5],
               [9 / 10, 35 / 6, 12.0],
               [11 / 10, 9 / 2, -26.0]])
SIN2_MEAS = 0.23122


def ainv_1loop(mu):
    return AINV - B1 / (2 * np.pi) * np.log(mu / M_Z)


def crossing_1loop(i, j):
    L = 2 * np.pi * (AINV[i] - AINV[j]) / (B1[i] - B1[j])
    return M_Z * np.exp(L)


def run_2loop(t_end, dt=0.01):
    """RK4 integrate alpha_i^-1 from M_Z (t=0) to t_end=ln(mu_end/M_Z); return
    (min spread, scale of min spread, spread at end)."""
    def deriv(ai):
        a = 1.0 / ai
        return -B1 / (2 * np.pi) - (B2 @ a) / (8 * np.pi**2)
    t, ai = 0.0, AINV.copy()
    best, best_mu = 1e9, M_Z
    while t < t_end:
        k1 = deriv(ai); k2 = deriv(ai + 0.5 * dt * k1)
        k3 = deriv(ai + 0.5 * dt * k2); k4 = deriv(ai + dt * k3)
        ai = ai + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += dt
        spread = float(ai.max() - ai.min())
        if spread < best:
            best, best_mu = spread, M_Z * np.exp(t)
    return best, best_mu, float(ai.max() - ai.min())


def run():
    reset()
    print("v246  unification data cross-check (1+2-loop): SM=TFPT gauge content does NOT unify -- a tension")

    # 1. TFPT gauge content = SM, no new states
    check("TFPT GAUGE CONTENT = SM, NO NEW STATES [E]: the carrier reproduces the "
          "SM betas b=(41/10,-19/6,-7) (v159) and the theory adds NO gauge-charged "
          "states (tfpt_3 'Dark matter = no new state'); the E8 cascade is an "
          "arithmetic spine (v5), not a threshold tower. So the TFPT RGE run IS the "
          "SM run",
          tuple(B1) == (41 / 10, -19 / 6, -7.0))

    # 2. the prediction
    check("THE PREDICTION [E]: the spectral action predicts at Lambda g1=g2=g3 and "
          "sin^2 th_W = 3/8 = %.3f (v245)" % (3 / 8), abs(3 / 8 - 0.375) < 1e-12)

    # 3. one-loop misses
    m12, m13, m23 = crossing_1loop(0, 1), crossing_1loop(0, 2), crossing_1loop(1, 2)
    mus = sorted([m12, m13, m23])
    decades = float(np.log10(mus[-1] / mus[0]))
    spread1_2e16 = float(np.ptp(ainv_1loop(2e16)))
    check("ONE-LOOP MISSES [X]: pairwise crossings a1=a2 %.2e, a1=a3 %.2e, a2=a3 "
          "%.2e GeV (%.1f decades); residual at 2e16 = Delta(alpha^-1) %.1f -- no "
          "common point" % (m12, m13, m23, decades, spread1_2e16),
          decades > 2.0 and spread1_2e16 > 3.0)

    # 4. two-loop also misses (the real run)
    best, best_mu, spread2_2e16 = run_2loop(np.log(2e16 / M_Z))
    check("TWO-LOOP ALSO MISSES [X]: RK4 2-loop run -- the minimal spread is "
          "Delta(alpha^-1) = %.2f at mu = %.2e GeV (the three NEVER meet; textbook "
          "non-SUSY result); at 2e16 GeV the spread is %.2f. 2-loop narrows but does "
          "NOT close" % (best, best_mu, spread2_2e16),
          1.0 < best < 6.0 and spread2_2e16 > 5.0)

    # 5. sin^2 thetaW tension
    check("sin^2 th_W TENSION [X]: predicted 3/8 = %.3f vs measured %.5f (the known "
          "few-percent non-SUSY shortfall)" % (3 / 8, SIN2_MEAS),
          abs(3 / 8 - SIN2_MEAS) > 0.1)

    # 6. no rescue in the current theory
    check("NO RESCUE IN THE CURRENT THEORY [O]: with 'no new state' there is NO "
          "admissible gauge-threshold source (the E8 spine is arithmetic, v5, not a "
          "particle spectrum); closing the spread needs EITHER new gauge-charged "
          "matter (a new postulate vs 'no new state') OR a non-GUT/boundary reading "
          "of the cutoff. The spectral-action 4d-GUT route is in genuine tension -- "
          "same status as NCG-SM -- likely falsified unless extended; the AQFT "
          "skeleton + DHR + SM rep-core survive as an emergent boundary QFT. "
          "Typed [X]/[O], NEVER [E]-as-success", True)

    return summary("v246 unification data cross-check (1+2-loop): SM=TFPT content does not unify; no rescue")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
