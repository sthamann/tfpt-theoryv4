"""v294 -- FLATAWAY.ENERGY.01: the RP-Energy / Troyanov route for Flat-Away, the third
independent attack.  It does NOT prove Flat-Away; it casts the lemma as a variational
selection -- the flat pillowcase is the UNIQUE constant-curvature (energy-minimizing)
metric in the conformal class with the prescribed mark divisor -- so Flat-Away reduces
to the single premise 'RP + gap realises that energy-minimiser'.

Geometry: the seam is the sphere with four cone points of angle pi (the pillowcase).
A smooth Z4 off-mark curvature is a curvature density f != 0 away from the four marks.

  [E] 1. PRESCRIBED DIVISOR + GAUSS-BONNET.  the pillowcase = S^2 with 4 cone points of
        angle pi; the cone Gauss-Bonnet sum sum_i (2pi - theta_i) = 4*pi = 2pi*chi(S^2)
        (chi=2) is satisfied by the FLAT (K=0 away from marks) metric -- the mark
        divisor is rigid (v195/v216) and forces curvature 4pi total, concentrated at
        the marks.
  [C] 2. TROYANOV / EUCLIDEAN-CONE UNIQUENESS.  for a prescribed cone divisor obeying
        Gauss-Bonnet, the conformal class carries a UNIQUE constant-curvature metric
        (Troyanov 1991; for K=0 the unique flat cone metric).  The flat pillowcase IS
        that metric; any smooth off-mark curvature (K != 0 between marks) is NOT
        constant-curvature, hence not the Troyanov metric -- imported as conditional.
  [E] 3. STRICTLY CONVEX CURVATURE ENERGY.  the curvature energy E[f] = int f^2 over
        the smooth-Z4 deformations has Hessian 2*pi*I (diagonal, positive-definite) in
        the clock-allowed Fourier basis -- strictly convex, so a UNIQUE minimiser
        (flat, E=0); the variational form of the uniqueness above.
  [E] 4. NO ZERO-COST DEFORMATION.  E[eps*cos(4k theta)] = pi*eps^2 > 0 for every mode
        and grows quadratically -- there is no flat (energy-free) smooth Z4 direction;
        E[f] = 0  <=>  f = 0 off the marks.
  [O] 5. THE PREMISE + CONVERGENCE.  Flat-Away <= 'RP + gap realises the
        energy-minimising (constant-curvature) seam metric'.  This is the route's one
        open input -- a variational characterisation of the RP+gap state -- and it
        converges with the heat route (v292, fix a_2) and the spectral route (v293, pin
        the Steklov spectrum): all three reduce Flat-Away to ONE selection principle for
        the flat metric.  Closing any one closes Route B.

Status: [E] the Gauss-Bonnet divisor + the strictly-convex energy with its unique
minimiser + no zero-cost direction; [C] Troyanov/Euclidean-cone uniqueness (literature);
[O] the variational premise (RP+gap selects the minimiser).  A third independent
reduction of Flat-Away, NOT a proof.  Python (numpy).
"""
import numpy as np

from tfpt_constants import check, summary, reset

NTH = 720


def _curv_energy(coeffs):
    """E[f] = int_0^2pi f^2 dtheta for f = sum_k coeffs[k] cos(4k theta)."""
    th = np.linspace(0, 2 * np.pi, NTH, endpoint=False)
    f = sum(c * np.cos(4 * k * th) for k, c in coeffs.items())
    return float(np.sum(f ** 2) * (2 * np.pi / NTH))


def run():
    reset()
    print("v294  FLATAWAY.ENERGY.01: the RP-energy / Troyanov route -- flat is the unique constant-curvature minimiser")

    # 1. prescribed divisor + Gauss-Bonnet
    n_marks, angle = 4, np.pi
    cone_sum = n_marks * (2 * np.pi - angle)          # sum (2pi - theta_i)
    check("PRESCRIBED DIVISOR + GAUSS-BONNET [E]: the pillowcase = S^2 with %d cone "
          "points of angle pi; the cone Gauss-Bonnet sum (2pi-theta) = %s = 2pi*chi "
          "(chi=2) holds for the FLAT metric -- the mark divisor is rigid (v195/v216), "
          "forcing 4pi curvature concentrated at the marks"
          % (n_marks, "4pi" if abs(cone_sum - 4 * np.pi) < 1e-9 else "?"),
          abs(cone_sum - 2 * np.pi * 2) < 1e-9)

    # 2. Troyanov uniqueness (literature)
    check("TROYANOV / EUCLIDEAN-CONE UNIQUENESS [C]: for a prescribed cone divisor "
          "obeying Gauss-Bonnet the conformal class carries a UNIQUE constant-curvature "
          "metric (Troyanov 1991; for K=0 the unique flat cone metric) -- the flat "
          "pillowcase IS it; a smooth off-mark curvature (K!=0 between marks) is not "
          "constant-curvature, hence excluded (imported)", True)

    # 3. strictly convex curvature energy: Hessian 2*pi*I (diagonal PD)
    eps = 0.01
    modes = (1, 2, 3)
    Hdiag = [(_curv_energy({k: eps}) + _curv_energy({k: -eps}) - 2 * _curv_energy({k: 0.0}))
             / eps ** 2 for k in modes]
    # off-diagonals
    offdiag = []
    for i, ki in enumerate(modes):
        for kj in modes[i + 1:]:
            mixed = (_curv_energy({ki: eps, kj: eps}) - _curv_energy({ki: eps})
                     - _curv_energy({kj: eps}) + _curv_energy({})) / eps ** 2
            offdiag.append(abs(mixed))
    check("STRICTLY CONVEX CURVATURE ENERGY [E]: E[f]=int f^2 has Hessian ~ 2pi*I "
          "(diagonal entries %s ~ 2pi=%.3f, off-diagonals < %.1e) in the clock-allowed "
          "basis -- strictly convex => UNIQUE minimiser (flat, E=0)"
          % ([round(h, 3) for h in Hdiag], 2 * np.pi, max(offdiag) + 1e-12),
          all(abs(h - 2 * np.pi) < 1e-2 for h in Hdiag) and max(offdiag) < 1e-6)

    # 4. no zero-cost deformation
    energies = {k: _curv_energy({k: 0.05}) for k in modes}
    check("NO ZERO-COST DEFORMATION [E]: E[eps cos(4kθ)] = pi eps^2 > 0 for every mode "
          "(%s at eps=0.05, vs pi eps^2 = %.4f) and grows quadratically -- no flat "
          "smooth Z4 direction; E[f]=0 <=> f=0 off the marks"
          % ({k: round(v, 4) for k, v in energies.items()}, np.pi * 0.05 ** 2),
          all(v > 0 for v in energies.values()))

    # 5. the premise + convergence
    check("THE PREMISE + CONVERGENCE [O]: Flat-Away <= 'RP + gap realises the "
          "energy-minimising (constant-curvature) seam metric' -- the one open "
          "variational input, converging with the heat route (v292, fix a_2) and the "
          "spectral route (v293, pin the Steklov spectrum): all three reduce Flat-Away "
          "to ONE selection principle for the flat metric; closing any one closes "
          "Route B", True)

    return summary("v294 FLATAWAY.ENERGY.01: the flat pillowcase is the unique constant-curvature / energy-minimising metric at the fixed mark divisor (Troyanov + strictly convex int f^2); Flat-Away reduces to 'RP+gap selects the minimiser'")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
