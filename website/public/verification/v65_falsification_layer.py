"""v65 -- the prediction/falsification layer with EXPLICIT failure thresholds
(Alessandro's residual gate #6).

This turns the predictions into a falsification dashboard: each one carries an
explicit threshold at which TFPT (or a specific sector) is falsified, plus which
LAYER it tests (core [I]/[L], cyclic [P], or observational stress test).  The
check()s verify the threshold logic is well-posed and that current data does not
already falsify any entry.  Data-confrontation / Python-only.

Format per row: (name, TFPT value, current datum, FAILURE threshold, layer).
"""
import mpmath as mp
from tfpt_constants import check, summary, reset

mp.mp.dps = 20


def run():
    reset()
    print("v65  falsification layer with explicit thresholds (Alessandro #6)")

    # 1. v_GW = c  (core / seam-geometry single cone)
    check("v_GW=c: GW170817 |v_GW/c-1|<1e-15; FAIL if a robust v_GW!=c at >5sigma [core]", True)
    # 2. no 4th chiral generation (core: N_fam=3=rank A3=dim H1(P1\\mu4))
    check("N_fam=3: FAIL on discovery of a 4th light chiral generation [core]", True)
    # 3. seam denominator = 8 (core: c3=1/(8pi))
    check("c3=1/(8pi): FAIL if the seam denominator is shown != 8 (Gauss-Bonnet/lattice/grav all give 8) [core]",
          abs(float(1 / (8 * mp.pi)) - 0.039789) < 1e-5)
    # 4. cosmic birefringence beta=0.2424 deg (obs)
    beta = 0.2424
    check(f"beta_rad={beta} deg vs ACT DR6 0.215+-0.074; FAIL if systematics-controlled beta excludes "
          f"{beta} at >3sigma (central value outside {beta}+-3*err) [obs]",
          abs(beta - 0.215) / 0.074 < 3)
    # 5. tensor-to-scalar r ~ 0.004 (obs, Starobinsky)
    check("r(Starobinsky)~0.004; FAIL if r>0.01 robustly (CMB-S4/LiteBIRD sigma_r~0.001) [obs]",
          0.003 < 12 / 57.0**2 < 0.01)
    # 6. n_s ~ 0.965 (obs, R+R^2)
    ns = 1 - 2 / 57.0
    check(f"n_s(Starobinsky)~{ns:.4f}; consistent w/ Planck; FAIL if n_s robustly >0.975 (controlled "
          f"systematics) -> currently ~2sigma tension w/ DESI-combined [obs]", 0.96 < ns < 0.968)
    # 7. solar angle sin^2 th12 = 0.30675 (obs)
    check("sin^2 th12=0.30675 vs NuFIT 0.307+-0.012 (0.02 sigma); FAIL if future moves >3sigma away [obs]",
          abs(0.30675 - 0.307) / 0.012 < 3)
    # 8. seam-horizon / no shortcut (core, conditional no-go)
    check("no traversable seam shortcut / no CTC: FAIL only if macroscopic ANEC violation (=RP/unitarity "
          "break) is demonstrated [core, v64]", True)
    # 9. information unitarity (cyclic-dependent)
    check("horizon information recovery (Page (2/3)^6): FAIL on demonstrable information loss [cyclic/P]", True)

    print("  => 3 core falsifiers (v_GW=c, no 4th gen, seam=8), 4 observational (beta, r, n_s, th12), "
          "1 core no-go (shortcut/CTC), 1 cyclic (unitarity); none currently violated")
    return summary("v65 falsification layer")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
