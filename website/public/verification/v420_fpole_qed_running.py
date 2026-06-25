"""v420 -- F_pole, the external side: the Koide source->pole transfer is a
ONE-LOOP ELECTROMAGNETIC effect, not an algebraic step.  This is the honest
"do the external physics" follow-up to v93 (which left the source->pole flow
time t~2.84 as an undetermined [P] generator) and to the clock No-Go (the
unitary/algebraic lens cannot reach a contraction rate).  It IDENTIFIES the
open piece as QED -- size, sign and scheme-dependence -- and keeps it firewalled
([C], external), NOT promoted.  Numerical (mpmath), Python-only (like v93/v371).

  [E] 1. KOIDE RESCALING INVARIANCE.  Q(m) = sum m / (sum sqrt m)^2 is homogeneous
         of degree 0: Q(c*m) = Q(m) for every c>0.  So any FLAVOR-UNIVERSAL
         running (a common factor on all three masses) leaves the Koide ratio
         EXACTLY fixed -- the source->pole shift is purely the FLAVOR-SPLIT
         (per-lepton) part of the running.
  [C] 2. THE GAP IS ONE-LOOP-EM-SIZED.  The tree (source) ladder gives
         2/3 - Q_src = 0.002203, which is the TFPT seed quantum phi0/24 = 0.002216
         to 0.6% AND the electromagnetic one-loop scale alpha/pi = 0.002323 to ~5%;
         the PDG pole sits AT 2/3 (gap 2.2e-6, the IR attractor).  So the
         source->pole gap is a one-loop EM size -- the transfer is QED.
  [C] 3. FLAVOR-SPLIT QED ESTIMATE (order + sign).  A standard 1-loop QED
         pole<->MSbar relation with the per-lepton log shifts the Koide by an
         EM-loop-order amount, and the pole (IR) is closer to 2/3 than the MSbar
         (UV) value -- i.e. the IR is the attractor (v82 direction).  The size is
         EM-loop; the exact value is scheme/scale-dependent.
  [O]/[C] 4. HONEST NEGATIVE / FIREWALL.  The EXACT flow time t~2.84 (v93)
         depends on the renormalisation scheme and the tree-scale identification
         -- external QED choices -- so it is NOT derived here, only sized.  The
         algebraic lens forces the RATE (2/3)^6 (v327/v82); this external EM
         physics supplies the source->pole flow.  F_pole stays [C], firewalled
         (v187): never re-pressed into the compiler.

VERDICT: the Koide source->pole transfer is identified as a one-loop EM effect
(size ~alpha/pi, IR-attractor direction), confirming F_transfer is genuinely
external -- the open theme is sharpened (QED), not closed.
"""
import mpmath as mp

from tfpt_constants import check, summary, reset, phi0

mp.mp.dps = 40

ALPHA = 1 / mp.mpf('137.0359992168')          # the TFPT-derived alpha (v3)
TWO3 = mp.mpf(2) / 3
# PDG 2024 pole masses (MeV)
ME, MMU, MTAU = mp.mpf('0.51099895069'), mp.mpf('105.6583755'), mp.mpf('1776.93')
MZ = mp.mpf('91187.6')


def koide(m1, m2, m3):
    return (m1 + m2 + m3) / (mp.sqrt(m1) + mp.sqrt(m2) + mp.sqrt(m3))**2


def run():
    reset()
    print("v420 F_pole external: the Koide source->pole transfer is one-loop EM")

    me, mmu, mtau = mp.mpf(16) / 7 * phi0**5, mp.mpf(4) / 3 * phi0**3, mp.mpf(7) / 6 * phi0**2
    q_src = koide(me, mmu, mtau)
    q_pole = koide(ME, MMU, MTAU)
    gap = TWO3 - q_src

    # ---- 1. Koide rescaling invariance (exact) ----
    inv = all(abs(koide(c * me, c * mmu, c * mtau) - q_src) < mp.mpf('1e-30')
              for c in (mp.mpf('0.137'), mp.mpf('3.7'), mp.mpf('1e6')))
    check("KOIDE RESCALING INVARIANCE [E]: Q(c*m)=Q(m) for all c>0 (degree-0 "
          "homogeneous) -- flavor-UNIVERSAL running leaves Koide exactly fixed, "
          "so the source->pole shift is purely the flavor-SPLIT part",
          inv)

    # ---- 2. the gap is one-loop-EM-sized ----
    check("ONE-LOOP-EM SIZE [C]: 2/3 - Q_src(tree) = %.6f = phi0/24 (%.6f) to "
          "0.6%% and = alpha/pi (%.6f, one-loop EM) to ~5%%; the PDG pole sits "
          "AT 2/3 (gap %.1e, the IR attractor) -- the source->pole gap is a "
          "one-loop EM size"
          % (float(gap), float(phi0 / 24), float(ALPHA / mp.pi), float(TWO3 - q_pole)),
          abs(gap / (phi0 / 24) - 1) < mp.mpf('0.01')
          and mp.mpf('0.85') < gap / (ALPHA / mp.pi) < mp.mpf('1.0')
          and abs(TWO3 - q_pole) < mp.mpf('1e-5'))

    # ---- 3. flavor-split 1-loop QED estimate (order + sign) ----
    def mbar(mpole):     # standard 1-loop QED pole->MSbar (per-lepton log)
        return mpole * (1 - (ALPHA / mp.pi) * (1 + mp.mpf(3) / 4 * mp.log(MZ**2 / mpole**2)))
    q_msbar = koide(mbar(ME), mbar(MMU), mbar(MTAU))
    shift = q_msbar - q_pole
    check("FLAVOR-SPLIT QED ESTIMATE [C]: a 1-loop QED pole<->MSbar relation "
          "(per-lepton log) shifts Koide by |dQ|/(alpha/pi) = %.2f (EM-loop "
          "order), and the pole (IR) is closer to 2/3 than the MSbar (UV) -- the "
          "IR is the attractor (v82 direction); exact value scheme-dependent"
          % float(abs(shift) / (ALPHA / mp.pi)),
          mp.mpf('0.1') < abs(shift) / (ALPHA / mp.pi) < mp.mpf('3')
          and abs(TWO3 - q_pole) < abs(TWO3 - q_msbar))

    # ---- 4. honest negative / firewall ----
    def rho(q):
        return (3 * q - 2) / (5 - 3 * q)
    mu = (mp.mpf(2) / 3)**6
    t_flow = mp.log(rho(q_pole) / rho(q_src)) / mp.log(mu)
    check("HONEST NEGATIVE / FIREWALL [O]/[C]: the EXACT flow time t = %.3f "
          "(v93) is scheme/scale-dependent external QED -- NOT derived, only "
          "sized; the algebraic lens forces the RATE (2/3)^6 (v327/v82), this "
          "external EM physics supplies the flow; F_pole stays [C], firewalled "
          "(v187)" % float(t_flow),
          mp.mpf('2.7') < t_flow < mp.mpf('3.0')
          and abs(t_flow - mp.nint(t_flow)) > mp.mpf('0.05'))

    return summary("v420 F_pole external (source->pole = one-loop EM; rate "
                   "forced, flow external [C])")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
