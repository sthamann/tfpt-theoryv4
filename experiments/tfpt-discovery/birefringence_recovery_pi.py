"""EXPLORATION (experiments/ only -- NOT a suite module, NOT in the ledger/papers).

Question: where does the cosmic birefringence come from, and what happens if you
combine it with the information-reconstruction (recovery) formula and apply it to pi?

ORIGIN (v8 / origin_theory / Appendix H): the birefringence is a seam BOUNDARY
PHASE -- the determinant-line / Chern-Simons rotation of the CMB polarisation:
    beta_rad = phi0 / (4 pi) ~ 0.2424 deg ,   phi0 = 1/(6 pi) + 48 c3^4 .
It is a 'live fossil': the SAME retarded seed phi0 that fixes the Cabibbo angle
(flavor) predicts the CMB EB/TB rotation (cosmology) -- one seed, no extra
parameter. Data: ACT DR6 0.215 +- 0.074 deg (0.37 sigma).

VERDICT (see prints): birefringence is the seam's pi made OBSERVABLE -- it is the
MOST pi-rich readout (beta = 1/(24 pi^2) + 3/(1024 pi^5), a phase, two/five powers
of pi). Combining it with the recovery operator yields NOTHING new: the recovery
is pi-FREE (anchor (2/3)^6), beta is a small phase, so every combination is
near-trivial; "applying to pi" only re-derives phi0 (beta*4pi = phi0). So the
phase (pi-rich) and the recovery dynamics (pi-free) are ORTHOGONAL. pi does not
encode the recovery information; the real, falsifiable content is the live-fossil
cross-link (beta_rad = the Cabibbo seed), not a pi relation.
"""
import mpmath as mp

mp.mp.dps = 40
PI = mp.pi
C3 = 1 / (8 * PI)
PHI0 = 1 / (6 * PI) + 48 * C3**4
BETA = PHI0 / (4 * PI)                    # birefringence angle (rad)
LAM2 = (mp.mpf(2) / 3)**6                 # recovery rate (pi-free)


def f_entropy(x):
    return (x**2 + 1) / (x**2 + x + 1)


def sec(t):
    print("\n" + "=" * 72 + "\n" + t + "\n" + "=" * 72)


def main():
    sec("ORIGIN: birefringence = the seam boundary phase phi0/(4 pi)")
    print(f"beta_rad = phi0/(4 pi) = {float(BETA):.10f} rad = {float(BETA*180/PI):.5f} deg")
    print(f"phi0 = 1/(6 pi) + 48 c3^4 = {float(PHI0):.8f}  (the retarded seed)")
    print("LIVE FOSSIL: the same phi0 fixes the Cabibbo angle (flavor) AND the CMB")
    print("birefringence (cosmology) -- one seed. Data: ACT DR6 0.215+-0.074 (0.37 sigma).")
    exact = 1 / (24 * PI**2) + 3 / (1024 * PI**5)
    print(f"exact pi-powers: beta = 1/(24 pi^2) + 3/(1024 pi^5) = {float(exact):.10f}  (match: {mp.almosteq(exact, BETA)})")
    print("  -> the MOST pi-rich readout: a seam PHASE carries 2 (and 5) powers of pi.")

    sec("COMBINE with the recovery operator (which is pi-FREE)")
    print(f"recovery rate (2/3)^6 = {float(LAM2):.8f}  (anchor rational, NO pi)")
    print(f"  beta * (2/3)^6      = {float(BETA*LAM2):.8e}   (tiny)")
    print(f"  beta / (2/3)^6      = {float(BETA/LAM2*180/PI):.5f} deg   (no clean meaning)")
    print(f"  entropy f(beta)     = {float(f_entropy(BETA)):.6f}   (~1, beta tiny)")
    print(f"  (2/3)^(6 beta)      = {float(LAM2**BETA):.6f}   (~1, beta tiny)")
    print("  -> every combination is near-trivial: beta is a small PHASE, the recovery")
    print("     is pi-free DYNAMICS. They are orthogonal.")

    sec("APPLY TO pi: no new relation emerges")
    print(f"  beta * 4 pi   = {float(BETA*4*PI):.8f} = phi0           (trivial inverse)")
    print(f"  beta * 24 pi^2= {float(BETA*24*PI**2):.8f} = 1 + 9/(128 pi^3)  (just phi0's definition)")
    print(f"  beta * pi     = {float(BETA*PI):.8f} = phi0/4")
    print("  -> pi 'hides' nothing in beta: multiplying back by powers of pi only")
    print("     undoes the phi0/(4pi) construction. No information is recovered from pi.")

    sec("VERDICT (firewall)")
    print("Birefringence is the seam's pi made OBSERVABLE -- the clearest physical")
    print("manifestation of the seam phase (a measurable polarisation rotation). But:")
    print("  * the recovery / reconstruction operator is pi-FREE (anchor (2/3)^6);")
    print("  * beta is the pi-rich PHASE; the two are orthogonal (phase vs dynamics);")
    print("  * 'applying to pi' only re-derives phi0 -- pi encodes no recovery info.")
    print("The REAL, falsifiable content is NOT a pi relation but the live-fossil")
    print("cross-link: beta_rad = phi0/(4pi) = the Cabibbo seed (flavor <-> cosmology,")
    print("one seed). Kill test: beta far from 0.2424 deg (controlled systematics)")
    print("breaks the shared-seed prediction. Stays in experiments/.")


if __name__ == "__main__":
    main()
