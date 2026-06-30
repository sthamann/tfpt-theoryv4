"""v452 -- SEAM.EQUIV.E8.MODULAR.01: the (E8)_1 torus modular data -- one primary,
S-invariant, T-phase e^{-2pi i/3}, the holomorphic c=8 signature.

v156 verified the (E8)_1 character q-expansion chi = E_4/eta^8 = q^{-1/3}(1 + 248 q
+ ...).  A q-expansion alone does not certify a consistent chiral CFT; the MODULAR
TRANSFORMATION DATA does.  A holomorphic (single-primary) RCFT must have its torus
character transform as a weight-0 modular form: S-invariant (one primary => S is
the 1x1 identity) and T-multiplied by e^{-2 pi i c/24}.  This module verifies, to
~1e-30, that chi = E_4/eta^8 satisfies exactly this with c=8:
  S:  chi(-1/tau) = chi(tau)              (one primary, modular invariant)
  T:  chi(tau+1)  = e^{-2 pi i*8/24} chi  = e^{-2 pi i/3} chi
  leading power q^{-c/24} = q^{-1/3}  =>  c = 8,
and that 8 satisfies the holomorphic constraint c = 0 mod 8 (the rank-8 even
unimodular lattice E_8).  Together with v376-v379 (torus GSD=1) this is the full
(E8)_1 modular signature -- exactly the data the seam keystone asserts for the
boundary net.

  [E] 1. S-INVARIANCE.  chi(-1/tau) = chi(tau) (E_4 weight 4, eta^8 weight 4 =>
         chi weight 0), to ~1e-30 at generic tau -- ONE primary, the S-matrix is
         [1].
  [E] 2. T-PHASE.  chi(tau+1)/chi(tau) = e^{-2 pi i/3} to ~1e-30 -- the central
         charge appears in the modular T eigenvalue e^{-2 pi i c/24} with c=8.
  [E] 3. LEADING POWER => c=8.  chi(tau)*q^{1/3} -> 1, so the leading power is
         q^{-c/24} = q^{-1/3} => c = 8 = g_car + N_fam (v148).
  [E] 4. HOLOMORPHIC CONSTRAINT.  c = 8 = 0 mod 8 -- the minimal holomorphic
         (single-primary) chiral central charge, realised by the even unimodular
         rank-8 lattice E_8 (the SO(16)-spinor control c=8 is the SAME lattice
         class; only index-4 closes to E_8, v281/v344).
  [C]/[O] 5. VERDICT.  the (E8)_1 modular data (one primary, S-invariant, T-phase
         e^{-2pi i/3}, c=8) is the torus signature of the seam boundary net; with
         the edge readings (v444/v447/v450/v451) the (E8)_1 identity is pinned on
         the torus AND the edge; SEAM.EQUIV.01 stays [O] -- the abstract continuum
         existence theorem (v336) is the residual.

Independent Wolfram mirror: the modular character facts are exact special-function
identities, mirrored in tfpt_readouts_extension.wl (v452 round).
"""
import mpmath as mp

from tfpt_constants import check, summary, reset, g_car, N_fam

mp.mp.dps = 40


def _eta(tau):
    q = mp.e ** (2j * mp.pi * tau)
    return mp.e ** (1j * mp.pi * tau / 12) * mp.qp(q)   # q^{1/24} prefactor from tau


def _E4(tau, N=300):
    q = mp.e ** (2j * mp.pi * tau)
    s = mp.mpf(1)
    for n in range(1, N):
        sig3 = sum(d ** 3 for d in range(1, n + 1) if n % d == 0)
        s += 240 * sig3 * q ** n
    return s


def _chi(tau):
    return _E4(tau) / _eta(tau) ** 8


def run():
    reset()
    print("v452 SEAM.EQUIV.E8.MODULAR: the (E8)_1 torus modular data -- one primary, "
          "S-invariant, T-phase e^{-2pi i/3}, holomorphic c=8")

    taus = [mp.mpf('0.27') + mp.mpf('1.3') * 1j, mp.mpf('0.1') + mp.mpf('1.1') * 1j]

    # ---- 1. S-invariance ----
    s_err = max(abs(_chi(-1 / t) - _chi(t)) for t in taus)
    s_ok = s_err < mp.mpf('1e-25')
    check("S-INVARIANCE [E]: chi(-1/tau)=chi(tau) (E_4 wt 4 / eta^8 wt 4 => chi wt "
          "0), max error %.1e over two generic tau -- ONE primary, S-matrix=[1]"
          % float(s_err), s_ok)

    # ---- 2. T-phase e^{-2pi i/3} ----
    target = mp.e ** (-2j * mp.pi / 3)
    t_err = max(abs(_chi(t + 1) / _chi(t) - target) for t in taus)
    t_ok = t_err < mp.mpf('1e-25')
    check("T-PHASE [E]: chi(tau+1)/chi(tau)=e^{-2pi i/3} (=e^{-2pi i c/24}, c=8), "
          "max error %.1e -- the central charge in the modular T eigenvalue"
          % float(t_err), t_ok)

    # ---- 3. leading power => c=8 ----
    tau = mp.mpf('3.0') * 1j
    q = mp.e ** (2j * mp.pi * tau)
    lead = _chi(tau) * q ** (mp.mpf(1) / 3)
    c_ok = abs(lead - 1) < mp.mpf('1e-4')
    check("LEADING POWER => c=8 [E]: chi(tau)*q^{1/3} -> %.6f (->1), so the leading "
          "power is q^{-c/24}=q^{-1/3} => c=8=g_car+N_fam" % float(abs(lead)),
          c_ok and (g_car + N_fam == 8))

    # ---- 4. holomorphic constraint c = 0 mod 8 ----
    c = g_car + N_fam
    holo = (c % 8 == 0)
    check("HOLOMORPHIC CONSTRAINT [E]: c=8=0 mod 8 -- the minimal holomorphic "
          "(single-primary) chiral central charge, realised by the even unimodular "
          "rank-8 lattice E_8 (only the index-4 extension closes to E_8, v281/v344)",
          holo)

    # ---- 5. verdict ----
    check("VERDICT [C]/[O]: the (E8)_1 modular data (one primary, S-invariant, "
          "T-phase e^{-2pi i/3}, c=8) is the torus signature of the seam boundary "
          "net; with the edge readings (v444/v447/v450/v451) the (E8)_1 identity is "
          "pinned on torus AND edge; SEAM.EQUIV.01 stays [O] -- the cited continuum "
          "existence theorem (v336) is the residual", s_ok and t_ok and c_ok and holo)

    return summary("v452 SEAM.EQUIV.E8.MODULAR: the (E8)_1 character chi=E_4/eta^8 "
                   "is S-invariant (one primary), T-multiplies by e^{-2pi i/3} "
                   "(=e^{-2pi i c/24}, c=8) and has leading power q^{-1/3} (c=8=0 "
                   "mod 8, holomorphic) -- the full torus modular signature of the "
                   "seam (E8)_1 net; SEAM.EQUIV.01 stays [O]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
