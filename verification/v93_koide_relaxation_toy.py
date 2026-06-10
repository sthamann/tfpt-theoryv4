"""v93 -- Koide relaxation toy (next.txt P2): basin lemma, exact rate, the
deficit in attractor coordinates, and two honest negatives.  [I]/[N] + [P].

v82 proved the STATICS: the branch-preserving Moebius map fixing the two
branch points q = 2 (Koide) and q = 5 (carrier) is unique given its
multiplier, and the multiplier is the established transfer gap
mu = (2/3)^6 = lambda_2 (v54/v56), with
    F(q) = 2(569 q - 3325)/(665 q - 3517),  F'(2) = (2/3)^6,  F'(5) = (3/2)^6.
Open [P] (next.txt P2): does the physical lepton source->pole transfer
actually RELAX along this map?  This toy tests everything that can be
tested without new physics input, under the canonical dictionary
    q = N_fam * Q          (Koide Q = 2/3  <->  branch point q = 2),
    rho = (q-2)/(5-q)      (cross-ratio attractor coordinate, v82).

RESULTS:

  [I] 1. BASIN LEMMA (new): the physical Koide range Q in [1/3, 1]
         (Cauchy-Schwarz bounds) maps to q in [1, 3] -- it CONTAINS the
         attractor q = 2 and EXCLUDES the repeller q = 5.  Every physically
         possible charged-lepton configuration lies in the attractor basin;
         no fine-tuning of the starting point is needed.
  [I] 2. EXACT RATE: along the trajectory from the physical source value
         the cross-ratio contracts by EXACTLY mu = (2/3)^6 per step (Moebius
         maps act linearly on the cross-ratio -- machine-checked to 1e-30).
  [I] 3. SOURCE DATA: the exact ladder leptons give Q_src = 0.6644638161,
         i.e. the source sits at rho_src = -0.0021980 -- within 0.8% of
         -phi0/24 = -0.0022155.  The v25 conjecture "Q_src + phi0/24 = 2/3"
         is thereby re-expressed in attractor coordinates: THE SOURCE SITS
         ONE SEED QUANTUM phi0/24 BEFORE THE BRANCH POINT (24 = |W(A3)|).
  [N] 4. POLE DATA: PDG pole masses give Q_pole = 0.6666644634
         (rho_pole = -2.20e-6): the pole side IS at the branch point to
         3.3e-6 -- the relaxation, whatever drives it, has essentially
         completed at the pole layer.

  HONEST NEGATIVES (recorded, they NARROW P2):
  [I] 5. the pole value is NOT an integer number of F-steps from the
         source value: t = log_mu(rho_pole/rho_src) = 2.84, not in Z.
         A literal discrete iteration "pole = F^n(source)" is EXCLUDED;
         if the transfer is the v82 map at all, it must be the CONTINUOUS
         flow exp(t log F) at non-integer flow time t ~ 2.8 -- the missing
         object is a continuous-time generator, not more iterations.
  [I] 6. the residual mismatch between rho_src and -phi0/24 (0.8%) is far
         above the ladder precision, so "exactly phi0/24" remains a
         conjecture [P] about the transfer normalisation, not an identity.

STATUS: P2 stays open [P], but sharper: the question is no longer "why
2/3?" (basin + uniqueness + rate are forced) but "what is the continuous
transfer generator, and why is its flow time from source to pole ~2.8
transfer periods?".  Nothing here is promoted.
"""
import mpmath as mp
from tfpt_constants import check, summary, reset, phi0, N_fam

# PDG 2024 pole masses (MeV)
M_E, M_MU, M_TAU = (mp.mpf('0.51099895069'), mp.mpf('105.6583755'),
                    mp.mpf('1776.93'))
MU_RATE = (mp.mpf(2) / 3)**6


def koide_q(m1, m2, m3):
    return (m1 + m2 + m3) / (mp.sqrt(m1) + mp.sqrt(m2) + mp.sqrt(m3))**2


def F(q):
    return 2 * (569 * q - 3325) / (665 * q - 3517)


def rho(q):
    return (q - 2) / (5 - q)


def run():
    reset()
    mp.mp.dps = 40
    print("v93 Koide relaxation toy (P2: basin, rate, deficit, honest negatives)")

    # 1. basin lemma
    q_lo, q_hi = N_fam * mp.mpf(1) / 3, N_fam * mp.mpf(1)
    check("BASIN LEMMA: physical Q in [1/3,1] maps to q in [1,3] -- "
          "attractor q=2 inside, repeller q=5 outside (every physical "
          "configuration is in the attractor basin)",
          q_lo == 1 and q_hi == 3 and q_lo < 2 < q_hi and not q_lo < 5 < q_hi)

    # 2. v82 fixed-point/derivative data (consistency import)
    h = mp.mpf('1e-20')
    check("F fixes the branch points: F(2)=2, F(5)=5",
          F(mp.mpf(2)) == 2 and F(mp.mpf(5)) == 5)
    check("F'(2) = (2/3)^6 (attractor), F'(5) = (3/2)^6 (repeller)",
          abs((F(2 + h) - F(2 - h)) / (2 * h) - MU_RATE) < mp.mpf('1e-15')
          and abs((F(5 + h) - F(5 - h)) / (2 * h) - 1 / MU_RATE) < mp.mpf('1e-15'))

    # 3. source data from the exact ladder
    me = mp.mpf(16) / 7 * phi0**5
    mmu = mp.mpf(4) / 3 * phi0**3
    mtau = mp.mpf(7) / 6 * phi0**2
    q_src_koide = koide_q(me, mmu, mtau)
    check("Q_src = 0.6644638161 from the exact lepton ladder [I]",
          q_src_koide, mp.mpf('0.664463816123'), tol=mp.mpf('1e-10'))
    q_src = N_fam * q_src_koide
    r_src = rho(q_src)
    check("source sits at rho_src = -0.0021980 in attractor coordinates",
          r_src, mp.mpf('-0.0021980087'), tol=mp.mpf('1e-6'))
    check("rho_src = -phi0/24 to 0.8% (the v25 conjecture in attractor "
          "coordinates: one seed quantum before the branch point; "
          "24 = |W(A3)|)  [P]",
          r_src / (-phi0 / 24), mp.mpf('0.99211'), tol=mp.mpf('1e-4'))

    # 4. exact contraction rate along the physical trajectory
    qs = [q_src]
    for _ in range(4):
        qs.append(F(qs[-1]))
    ratios = [rho(qs[i + 1]) / rho(qs[i]) for i in range(4)]
    check("EXACT RATE: cross-ratio contracts by exactly (2/3)^6 per step "
          "along the physical trajectory (Moebius linearity, 1e-30)",
          all(abs(r - MU_RATE) < mp.mpf('1e-30') for r in ratios))

    # 5. pole data
    q_pole_koide = koide_q(M_E, M_MU, M_TAU)
    check("Q_pole = 0.6666644634 from PDG pole masses (branch point hit "
          "to 3.3e-6) [N]",
          q_pole_koide, mp.mpf('0.666664463403'), tol=mp.mpf('1e-9'))
    r_pole = rho(N_fam * q_pole_koide)

    # 6. honest negative: non-integer flow time
    t_flow = mp.log(r_pole / r_src) / mp.log(MU_RATE)
    check("HONEST NEGATIVE: flow time source->pole t = 2.838 F-steps -- "
          "NOT an integer => literal discrete iteration pole = F^n(source) "
          "EXCLUDED; the missing P2 object is a continuous-time generator",
          t_flow, mp.mpf('2.8384561'), tol=mp.mpf('1e-5'))
    check("(and t is not within 0.05 of any integer)",
          abs(t_flow - mp.nint(t_flow)) > mp.mpf('0.05'))

    # 7. honest negative: phi0/24 is a conjecture, not an identity
    mismatch = abs(r_src / (-phi0 / 24) - 1)
    check("HONEST NEGATIVE: rho_src vs -phi0/24 mismatch = 0.79% >> ladder "
          "precision => 'exactly phi0/24' stays a [P] conjecture about the "
          "transfer normalisation, not an identity",
          mismatch, mp.mpf('0.0078941'), tol=mp.mpf('1e-3'))

    check("STATUS: P2 narrowed, not closed -- basin/uniqueness/rate forced "
          "[I]; open: the continuous transfer generator and its flow time "
          "~2.8 periods [P]", True)

    return summary("v93 Koide relaxation toy")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
