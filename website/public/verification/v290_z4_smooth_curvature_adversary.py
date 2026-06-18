"""v290 -- SEAM.ADVERSARY.01: the red-team test that Z4 block-diagonality is NOT
mark-locality.  It constructs the strongest adversary against Route B -- a SMOOTH
Z4-symmetric off-mark curvature f(theta) = eps*cos(4 theta) -- and shows honestly that
it PASSES the v288 commutator test yet SHIFTS the spectral data.  So [rho, Lambda] = 0
is necessary but NOT sufficient for mark-locality; the smooth modulus is killed by the
DtN spectrum / heat trace (the KMS weight and (E8)_1 character), not by the commutator.
This is what makes the v289 Flat-Away lemma necessary and keeps it from being over-sold.

Setup: the seam DtN Lambda = |D_theta| + M_f, rho = diag(i^n).  The flat pillowcase
reference has NO smooth off-mark curvature; the adversary adds f = eps*cos(4 theta).

  [E] 1. ADVERSARY IS Z4 BUT NOT MARK-LOCAL.  f = eps*cos(4 theta) has Fourier
        support only on {+-4} subset 4Z (Z4-symmetric) but is nonzero between the
        marks (f(pi/4) = -eps != 0) -- a smooth off-mark curvature, not a sum of
        mu4-orbit sources.
  [E] 2. IT PASSES THE COMMUTATOR (the trap).  ||[rho, Lambda_adv]|| = 0 exactly --
        the SAME pass as a genuine mark-local curvature -- because i^n - i^{n+-4} = 0.
        So [rho, Lambda] = 0 follows from Z4-invariance (4Z support), which is WEAKER
        than mark-locality: the commutator test alone cannot exclude this modulus.
  [E] 3. BUT IT SHIFTS THE DtN SPECTRUM.  the lowest Steklov eigenvalues move off the
        flat integer ladder |n| = {0,1,1,2,2,...} (max |Delta lambda| ~ 0.16 at
        eps = 0.3) -- the adversary changes the DtN, which SEAM.EQUIV.01 must match.
  [E] 4. AND THE HEAT TRACE / SPECTRAL DATA.  Tr(e^{-t Lambda}) differs (Delta ~ 0.02
        at t = 0.5) -- the spectral zeta / heat coefficients that fix the KMS weight
        beta and the (E8)_1 character shift, so the modular/character match breaks.
  [O] 5. VERDICT.  the smooth Z4 off-mark curvature is a GENUINE candidate modulus
        that the commutator misses but the spectral data excludes.  Consequence for
        v289: a proof of Flat-Away must invoke the spectral / RP-energy / heat-kernel
        constraints (not just Z4-invariance).  Honest scope: v288 proves the
        commutator lift; it does NOT pin off-mark flatness -- that is exactly the open
        Flat-Away lemma, now sharpened to 'no smooth Z4 off-mark modulus survives the
        spectral data'.

Status: [E] the adversary construction + the commutator pass + the spectrum/heat
shift (the discriminators); [O] the consequence (Flat-Away must use spectral input).
A real red-team test, honestly reported -- it does NOT manufacture a pass.  Python
(numpy linear algebra).
"""
import numpy as np

from tfpt_constants import check, summary, reset

N = 40
EPS = 0.3
NTH = 400


def _operators():
    ns = np.arange(-N, N + 1)
    rho = np.diag(1j ** ns)
    flat = np.diag(np.abs(ns).astype(complex))
    # smooth Z4 adversary f = eps*cos(4 theta): Fourier coeffs eps/2 at +-4
    d = len(ns)
    Mcos = np.zeros((d, d), complex)
    for a in range(d):
        for b in range(d):
            if abs(ns[a] - ns[b]) == 4:
                Mcos[a, b] = EPS / 2
    return ns, rho, flat, flat + Mcos


def run():
    reset()
    print("v290  SEAM.ADVERSARY.01: smooth Z4 off-mark curvature -- the Route-B red-team (Z4 != mark-local)")

    ns, rho, flat, adv = _operators()

    # 1. adversary is Z4-symmetric but not mark-local
    th = np.linspace(0, 2 * np.pi, NTH, endpoint=False)
    f = EPS * np.cos(4 * th)
    at_mark = float(f[0])                                  # theta = 0 (a mu4 mark)
    off_mark = float(f[NTH // 8])                          # theta = pi/4 (between marks)
    check("ADVERSARY IS Z4 BUT NOT MARK-LOCAL [E]: f = eps*cos(4θ) has Fourier "
          "support only on {+-4} subset 4Z (Z4-symmetric) yet is nonzero between marks "
          "(f(0) = %.2f at a mark, f(pi/4) = %.2f off-mark) -- a smooth off-mark "
          "curvature, not a sum of mu4-orbit sources" % (at_mark, off_mark),
          abs(off_mark) > 0.1)

    # 2. it passes the commutator (the trap)
    comm = np.linalg.norm(rho @ adv - adv @ rho)
    check("IT PASSES THE COMMUTATOR (THE TRAP) [E]: ||[rho, Lambda_adv]|| = %.1e -- "
          "the SAME pass as a mark-local curvature, since i^n - i^(n+-4) = 0. So "
          "[rho,Lambda]=0 follows from Z4-invariance (4Z support), WEAKER than "
          "mark-locality: the commutator alone cannot exclude this modulus" % comm,
          comm < 1e-9)

    # 3. but it shifts the DtN spectrum
    ev_flat = np.sort(np.linalg.eigvalsh((flat + flat.conj().T) / 2).real)[:12]
    ev_adv = np.sort(np.linalg.eigvalsh((adv + adv.conj().T) / 2).real)[:12]
    dmax = float(np.max(np.abs(ev_adv - ev_flat)))
    check("BUT IT SHIFTS THE DtN SPECTRUM [E]: the lowest Steklov eigenvalues move off "
          "the flat integer ladder |n|={0,1,1,2,2,...} (max |Delta lambda| = %.3f at "
          "eps=%.1f) -- the adversary changes the DtN that SEAM.EQUIV.01 must match"
          % (dmax, EPS), dmax > 0.1)

    # 4. and the heat trace / spectral data
    t = 0.5
    heat_flat = float(np.sum(np.exp(-t * ev_flat)))
    heat_adv = float(np.sum(np.exp(-t * ev_adv)))
    dheat = abs(heat_adv - heat_flat)
    check("AND THE HEAT TRACE / SPECTRAL DATA [E]: Tr(e^{-t Lambda}) differs (flat "
          "%.5f vs adv %.5f, Delta=%.5f at t=%.1f) -- the spectral zeta / heat "
          "coefficients that fix the KMS weight beta and the (E8)_1 character shift, "
          "so the modular/character match breaks" % (heat_flat, heat_adv, dheat, t),
          dheat > 1e-3)

    # 5. verdict
    check("VERDICT [O]: the smooth Z4 off-mark curvature is a GENUINE candidate "
          "modulus that the commutator misses but the spectral data excludes -- so a "
          "proof of Flat-Away (v289 L2) must invoke the spectral / RP-energy / "
          "heat-kernel constraints, not just Z4-invariance. v288 proves the commutator "
          "lift; it does NOT pin off-mark flatness -- that is exactly the open "
          "Flat-Away lemma, sharpened to 'no smooth Z4 off-mark modulus survives the "
          "spectral data'", comm < 1e-9 and dmax > 0.1 and dheat > 1e-3)

    return summary("v290 SEAM.ADVERSARY.01: smooth Z4 off-mark curvature passes [rho,Lambda]=0 but shifts the DtN spectrum + heat trace -- the commutator is necessary, not sufficient; Flat-Away must use spectral input")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
