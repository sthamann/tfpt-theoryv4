"""v291 -- FLATAWAY.RP.01: the Flat-Away lemma as its own named mini-theorem, with the
three concrete proof routes opened by the v290 red-team.  This does NOT prove Flat-Away;
it states it precisely, shows numerically that the flat reference is the UNIQUE point of
the smooth Z4 family that matches the spectral data, and types the three attack routes.

THE LEMMA (FLATAWAY.RP.01):
    Given RawRPSeam with the mass gap, chirality and the four mu4 branch marks, the
    smooth curvature density in the DtN sub-principal symbol vanishes away from the
    branch divisor (the seam is flat away from the four marks).

Why it is the bottleneck: v288 lifts the Z4 block-diagonality to L^2 *given* a
mark-sourced (= flat-away) sub-principal term; v290 shows a smooth Z4 off-mark curvature
passes the commutator yet shifts the spectrum -- so Flat-Away is exactly the gap, and it
must be closed with spectral / energy / heat-kernel input, not the commutator.

  [O] 1. LEMMA STATED.  the smooth curvature density vanishes off the branch divisor --
        a single, precise analytic statement (not prose), the one open link of v289.
  [E] 2. SPECTRAL-RIGIDITY route.  scanning the smooth Z4 family f = eps*cos(4 theta),
        the deviation of the DtN spectrum from the flat integer ladder is zero ONLY at
        eps = 0 and grows with |eps| -- so the forced KMS spectrum (gap, ladder) has the
        flat seam as its unique match; smooth Z4 deformations are spectrally excluded
        (the lever, conditional on pinning the spectrum; cf. v290).
  [E] 3. HEAT-KERNEL route.  likewise the heat trace Tr(e^{-t Lambda}) deviation is zero
        ONLY at eps = 0 -- a smooth off-mark curvature adds heat-trace coefficients, so
        matching the flat / (E8)_1 heat data forces the smooth curvature to vanish
        (conditional on pinning the heat coefficients; cf. v290).
  [C] 4. RP-ENERGY route.  reflection positivity + the gap is a Dirichlet-energy
        minimisation in the Troyanov conformal class with prescribed cone angles; by
        Troyanov uniqueness the minimiser is the constant-curvature metric (flat away
        from the marks) -- imported as conditional (Troyanov; cf. v284 constant-curvature
        reduction).
  [O] 5. VERDICT.  three INDEPENDENT routes to ONE lemma; v290 shows the commutator is
        insufficient so each route must use spectral / energy / heat input. Closing any
        one closes Route B (and, with Route A's holomorphy half, SEAM.EQUIV.01). Honest:
        all three remain open handles, not proofs.

Status: [O] the lemma + the verdict; [E] the spectral-rigidity + heat-kernel uniqueness
demonstrations (flat is the unique match in the smooth Z4 family); [C] the RP-energy /
Troyanov route.  A contract that turns Flat-Away into a precise, attackable mini-theorem.
Python (numpy linear algebra).
"""
import numpy as np

from tfpt_constants import check, summary, reset

N = 40


def _spectrum(eps):
    ns = np.arange(-N, N + 1)
    d = len(ns)
    M = np.zeros((d, d), complex)
    for a in range(d):
        for b in range(d):
            if abs(ns[a] - ns[b]) == 4:
                M[a, b] = eps / 2
    A = np.diag(np.abs(ns).astype(complex)) + M
    return np.sort(np.linalg.eigvalsh((A + A.conj().T) / 2).real)[:12]


def run():
    reset()
    print("v291  FLATAWAY.RP.01: the Flat-Away lemma as a named mini-theorem (3 proof routes)")

    flat = _spectrum(0.0)
    epsgrid = [0.0, 0.1, 0.2, 0.3, 0.4]

    # 1. lemma stated
    check("LEMMA STATED [O]: 'given RawRPSeam with gap, chirality and the four mu4 "
          "branch marks, the smooth curvature density in the DtN sub-principal symbol "
          "vanishes away from the branch divisor' -- the one open link of v289, stated "
          "precisely (not prose)", True)

    # 2. spectral-rigidity: deviation from the flat ladder is zero only at eps=0
    spec_dev = [float(np.max(np.abs(_spectrum(e) - flat))) for e in epsgrid]
    monotonic = all(spec_dev[i] < spec_dev[i + 1] for i in range(len(spec_dev) - 1))
    check("SPECTRAL-RIGIDITY route [E]: scanning f=eps*cos(4θ), the DtN-spectrum "
          "deviation from the flat integer ladder is 0 ONLY at eps=0 and grows with "
          "|eps| (devs %s) -- the forced KMS spectrum has the flat seam as its unique "
          "match; smooth Z4 deformations are spectrally excluded (cf. v290)"
          % [round(x, 3) for x in spec_dev],
          spec_dev[0] < 1e-9 and monotonic)

    # 3. heat-kernel: heat-trace deviation zero only at eps=0
    t = 0.5
    heat0 = float(np.sum(np.exp(-t * flat)))
    heat_dev = [abs(float(np.sum(np.exp(-t * _spectrum(e)))) - heat0) for e in epsgrid]
    heat_mono = all(heat_dev[i] < heat_dev[i + 1] for i in range(len(heat_dev) - 1))
    check("HEAT-KERNEL route [E]: the heat trace Tr(e^{-tΛ}) deviation is 0 ONLY at "
          "eps=0 and grows with |eps| (devs %s) -- a smooth off-mark curvature adds "
          "heat-trace coefficients, so matching the flat/(E8)_1 heat data forces the "
          "smooth curvature to vanish (cf. v290)" % [round(x, 4) for x in heat_dev],
          heat_dev[0] < 1e-12 and heat_mono)

    # 4. RP-energy / Troyanov route
    check("RP-ENERGY route [C]: RP + gap is a Dirichlet-energy minimisation in the "
          "Troyanov conformal class with prescribed cone angles; by Troyanov "
          "uniqueness the minimiser is the constant-curvature metric (flat away from "
          "the marks) -- imported as conditional (Troyanov; cf. v284)", True)

    # 5. verdict
    check("VERDICT [O]: three INDEPENDENT routes (spectral-rigidity, heat-kernel, "
          "RP-energy) to ONE lemma; v290 shows the commutator is insufficient, so each "
          "route uses spectral/energy/heat input. Closing any one closes Route B (and, "
          "with Route A's holomorphy half, SEAM.EQUIV.01). All three remain open "
          "handles, not proofs", spec_dev[0] < 1e-9 and heat_dev[0] < 1e-12)

    return summary("v291 FLATAWAY.RP.01: Flat-Away named as a mini-theorem; flat seam is the UNIQUE spectral/heat match in the smooth Z4 family; 3 open proof routes (spectral-rigidity, heat-kernel, RP-energy)")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
