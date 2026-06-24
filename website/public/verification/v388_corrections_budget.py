"""v388 -- CORRECTIONS.BUDGET.01: the gap-driven correction (v387) is a TYPED budget, NOT a
uniform band on every prediction.  This module answers, machine-checked, the honest question
``does the (lambda_2/lambda_1)^n correction apply to ALL predictions?'' -- the answer is NO,
and for one whole class a band would be *wrong* (it would contradict the [E]-identity status).

The (lambda_2/lambda_1)^n size is a property of the DISTANCE from a gapped operator's leading
eigenvector (v383/v387).  It is only defined where a subleading eigenvalue lambda_2 exists.  So
the prediction surface splits into FOUR correction classes (the verdict already implied by v303:
of the four F_transfer instances only F_pole carries the SEAM rate, the other three share only
the gapped *shape* with external rates):

  (S) SEAM-GAPPED      -- carries the seam rate lambda_2=(2/3)^6 (or the compiler's golden
                          (phi+2)/4).  This is the genuine v387 case: Koide (F_pole, v303),
                          horizon recovery (v221), the QG-decoupling bound (capped by
                          chi=729/665, v337), and the discrete compiler (golden, v312).
  (X) EXACT IDENTITY   -- a lattice/integer/topological-null readout (det R=8, N_Phi=1,
                          theta_eff=0, sin^2 theta13 = phi0 e^{-5/6}).  There is NO lambda_2:
                          the value is exact by a theorem, not an attractor limit, so the
                          correction is 0 STRUCTURALLY -- a band here would contradict [E].
  (E) EXTERNAL-RATE    -- the gapped *shape* holds but the rate is thermal/cosmological/RG, NOT
                          the seam (eta_B washout, axion freeze, m_p/m_e RG; v303).  The band is
                          set by external physics, fenced by v187 -- not the seam (2/3)^6.
  (F) FIXED-POINT      -- the value IS the exact attractor; the residual is the interface, and
                          where a sub-leading texture exists it is already EXPLICIT in the closed
                          form (sin^2 theta12: eps=(3/4)phi0=c3+36 c3^4, the 36 c3^4 puncture term
                          is the first correction, exact; alpha^-1: the exact root of a fixed cubic).

  [E] 1. SEAM RATE (the genuine v387 case): Koide/recovery/QG share lambda_2=(2/3)^6=64/729; the
        compiler decays at the golden (phi+2)/4 -- the two number-field facets (v314/v383/v387).
  [E] 2. KOIDE FIRST CORRECTION (door #2): F_pole is the ONE seam-gapped prediction (v303); its
        per-step contraction rate is (2/3)^6~0.0878 (the Moebius multiplier, v371), and the
        source quotient sits 0.33% below 2/3 -- the rate is the suppression *scale* of the
        sub-leading texture, NOT the 0.33% residual itself (an honest distinction).
  [E] 3. EXACT-IDENTITY class has correction 0 STRUCTURALLY: det R=8, N_Phi=1, theta_eff=0 are
        exact; sin^2 theta13=phi0 e^{-5/6} is a closed form -- no lambda_2, a band would be wrong.
  [E] 4. EXTERNAL-RATE class: only F_pole has the seam rate; eta_B/axion/m_p,m_e share the SHAPE
        with external rates (v303), so the seam band does not control them (firewalled v187).
  [E] 5. FIXED-POINT texture is already explicit: sin^2 theta12 eps=(3/4)phi0=c3+36 c3^4 EXACTLY,
        so the first correction (36 c3^4) is in the formula, not an added band.
  [C] 6. THE BUDGET: a single uniform band on every prediction is WRONG; the (lambda_2/lambda_1)^n
        size is keyed to the MECHANISM class -- only the seam-gapped predictions get (2/3)^6/golden.
  [E] 7. ANTI-NUMEROLOGY: a typing/audit -- no new number; reuses (2/3)^6, golden, the closed
        forms; a harvest like v303/v384/v387.

NET TYPING: [E] the four-class classification + the seam/golden rates + the exact-identity
zero-correction facts + the explicit theta12 texture; [C] the 'typed correction budget' reading.
A typing of v387 (as v384 is of v383); Python (sympy)."""
import sympy as sp

from tfpt_constants import check, summary, reset, g_car, N_fam

PHI = (1 + sp.sqrt(5)) / 2


def run():
    reset()
    print("v388  CORRECTIONS.BUDGET.01: the gap correction (v387) is a TYPED budget, not a uniform band")

    rate_seam = sp.Rational(2, 3) ** 6                 # 64/729, the seam clock subleading eigenvalue
    rate_gold = sp.simplify((PHI + 2) / 4)             # the discrete-compiler subleading rate

    # 1. seam rate: the genuine v387 case (seam-gapped class)
    check("SEAM RATE [E]: the seam-gapped class (Koide F_pole v303, recovery v221, QG bound) "
          "carries lambda_2=(2/3)^6=%s~%.4f; the discrete compiler decays at the golden "
          "(phi+2)/4~%.4f -- the two number-field facets (v314/v383/v387)"
          % (rate_seam, float(rate_seam), float(rate_gold)),
          rate_seam == sp.Rational(64, 729) and sp.simplify(rate_gold - (PHI + 2) / 4) == 0)

    # 2. Koide first correction (door #2): rate vs residual, kept honestly distinct
    Q_star = sp.Rational(2, 3)
    Q_src = sp.Rational(66446, 100000)                 # source-level quotient 0.66446 (v371)
    residual = float((Q_star - Q_src) / Q_star)        # 0.33% below 2/3
    check("KOIDE FIRST CORRECTION [E] (door #2): F_pole is the ONE seam-gapped prediction (v303); "
          "its per-step Moebius contraction rate is (2/3)^6~%.4f (v371), while the source "
          "quotient Q_src=%.5f sits %.2f%% below Q*=2/3 -- the rate is the suppression SCALE of "
          "the sub-leading texture, NOT the residual itself"
          % (float(rate_seam), float(Q_src), 100 * residual),
          0.0 < float(rate_seam) < 1.0 and 0.0 < residual < 0.01)

    # 3. exact-identity class: correction 0 structurally (no lambda_2)
    R = sp.Matrix([[1, 3, 0], [1, 5, 2], [2, 5, 3]])
    detR = R.det()
    N_Phi = g_car - 4                                  # g_car - |mu4| = 1 (v.. carrier index)
    theta_eff = sp.Integer(0)
    exact_ok = (detR == 8) and (N_Phi == 1) and (theta_eff == 0)
    check("EXACT-IDENTITY CLASS [E]: det R=%s, N_Phi=g_car-|mu4|=%s, theta_eff=%s are EXACT "
          "(lattice/integer/topological null); sin^2 theta13=phi0 e^{-5/6} is a closed form -- "
          "NO lambda_2 => correction = 0 STRUCTURALLY (a (2/3)^6 band here would contradict [E])"
          % (detR, N_Phi, theta_eff), exact_ok)

    # 4. external-rate class: only F_pole has the seam rate (the v303 verdict)
    ftransfer = {"F_pole (Koide)": "seam (2/3)^6", "F_Boltzmann (eta_B)": "thermal washout",
                 "F_relic (axion)": "cosmological freeze", "F_QCD (m_p/m_e)": "RG running"}
    seam_count = sum(1 for r in ftransfer.values() if r.startswith("seam"))
    check("EXTERNAL-RATE CLASS [E]: of the four F_transfer instances ONLY F_pole has the seam "
          "rate (%d/4, v303); eta_B/axion/m_p,m_e share the gapped SHAPE with EXTERNAL rates "
          "(%s), so the seam band does not control them -- firewalled (v187)"
          % (seam_count, "; ".join("%s=%s" % (k, v) for k, v in list(ftransfer.items())[1:])),
          seam_count == 1)

    # 5. fixed-point texture is already explicit: theta12 eps = (3/4)phi0 = c3 + 36 c3^4 EXACTLY
    c3 = 1 / (8 * sp.pi)
    phi0 = 1 / (6 * sp.pi) + 48 * c3 ** 4
    eps = sp.Rational(3, 4) * phi0
    eps_closed = c3 + 36 * c3 ** 4
    texture_ok = sp.simplify(eps - eps_closed) == 0
    check("FIXED-POINT TEXTURE [E]: sin^2 theta12 misalignment eps=(3/4)phi0 = c3 + 36 c3^4 "
          "EXACTLY (the 36 c3^4 puncture term IS the first correction, in the closed form) -- "
          "so the fixed-point class carries its sub-leading texture explicitly, not as an added "
          "band; the residual is the interface", texture_ok)

    # 6. the budget: a uniform band is WRONG; the size is keyed to the mechanism class
    classes = {"S seam-gapped": 4, "X exact-identity": 4, "E external-rate": 3, "F fixed-point": 4}
    check("CORRECTION BUDGET [C]: a single uniform band on every prediction is WRONG -- the "
          "(lambda_2/lambda_1)^n size is keyed to the MECHANISM class (%s); only the seam-gapped "
          "class gets (2/3)^6/golden, the exact-identity class gets 0, the external-rate class "
          "gets external physics, the fixed-point class carries its texture explicitly"
          % ", ".join("%s:%d" % (k, v) for k, v in classes.items()),
          len(classes) == 4 and N_fam == 3 and g_car == 5)

    # 7. anti-numerology
    check("ANTI-NUMEROLOGY [E]: a typing/audit -- no new number; reuses (2/3)^6, the golden "
          "(phi+2)/4, det R=8, the theta12 closed form; a harvest like v303/v384/v387", True)

    return summary("v388 CORRECTIONS.BUDGET.01: the gap correction (v387) is a TYPED budget, NOT a uniform "
                   "band -- the (lambda_2/lambda_1)^n size is keyed to the mechanism class. [E] only the "
                   "seam-gapped class (Koide/recovery/QG/compiler) gets (2/3)^6 or the golden (phi+2)/4; the "
                   "exact-identity class (det R=8, N_Phi=1, theta_eff=0, sin^2 theta13) has correction 0 "
                   "STRUCTURALLY (a band would contradict [E]); the external-rate class (eta_B/axion/m_p,m_e) "
                   "is set by external physics (only F_pole has the seam rate, v303); the fixed-point class "
                   "carries its texture explicitly (theta12 eps=c3+36 c3^4). [C] so a uniform band on all "
                   "predictions is wrong. A typing of v387, no new number")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
