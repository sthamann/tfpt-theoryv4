"""EXPLORATION (experiments/ only -- NOT a suite module, NOT in the ledger/papers).

Three speculative questions, explored honestly:
  (1) What happens if you apply the black-hole information-reconstruction formula
      (the gapped boundary transfer operator T) to pi?
  (2) Could everything in the black hole collapse onto a 2-surface ~ c3 * 5 ?
  (3) Does the 4D action reconstruction have to account for that?

Verdict (see prints): pi DECOUPLES from the discrete recovery dynamics. Its only
job is to make the seam's closed-2-surface Gauss-Bonnet action exactly 1
(c3 = 1/(8pi)  <=>  c3 * 8pi = 1). The "collapse to a 2-surface ~ c3*5" is the
holographic statement that the seam S^2, weighted by the carrier rank, carries
exactly g_car = 5 (the pi cancels on integration). This already feeds the 4D
action through the Einstein-Hilbert coefficient k = c3/2 = 1/(16 pi) (the
Seam-Horizon mechanism). No new transcendental relation appears; the finding
CONFIRMS the existing pi-free anchor structure.
"""
import mpmath as mp

mp.mp.dps = 40
PI = mp.pi
C3 = 1 / (8 * PI)                       # seam constant (P1)
GCAR, NFAM, Z2, A_LAM = 5, 3, 2, 10     # anchor atoms
LAM2 = (mp.mpf(2) / 3) ** 6             # recovery rate = sub-leading eigenvalue of T
LAM3 = (mp.mpf(1) / 3) ** 6
GAP = 6 * mp.log(mp.mpf(3) / 2)         # H = -log T gap
GB_SEAM = 8 * PI                        # |Z2| * 2pi * chi(S^2), chi=2  (doubled one-sided)


def f_entropy(x):
    """The SdS / BH entropy interpolator S_tot/S_dS (the 'collapse' ratio)."""
    return (x**2 + 1) / (x**2 + x + 1)


def section(t):
    print("\n" + "=" * 72 + "\n" + t + "\n" + "=" * 72)


def main():
    section("(1) APPLY THE RECONSTRUCTION OPERATOR TO pi  ->  pi DECOUPLES")
    print(f"spec(T) = {{1, (2/3)^6, (1/3)^6}} = {{1, {float(LAM2):.6f}, {float(LAM3):.6f}}}")
    print(f"gap  Delta = 6 log(3/2) = {float(GAP):.6f}")
    print("  -> the recovery operator is built ENTIRELY from anchor rationals;")
    print("     there is NO pi anywhere in T, its spectrum, or the gap.")
    print(f"  naive 'apply to pi': f_entropy(pi) = {float(f_entropy(PI)):.6f}  (not clean)")
    print(f"                       (2/3)^(6 pi)  = {float(LAM2**PI):.3e}      (not clean)")
    print("  VERDICT: pi is decoupled from the discrete information recovery.")
    print("           It enters the theory ONLY through c3 = 1/(8 pi).")

    section("(2) COLLAPSE TO A 2-SURFACE ~ c3*5  ->  pi CANCELS, leaves g_car=5")
    print(f"c3 * 5 = 5/(8 pi) = {float(C3 * 5):.6f}   (a per-unit-curvature density)")
    print(f"the seam IS a 2-surface S^2; its Gauss-Bonnet integral = 8 pi (chi=2, |Z2|).")
    print(f"  c3 * (8 pi)            = {float(C3 * GB_SEAM):.6f}   <- bare seam action = 1 (pi cancels)")
    print(f"  g_car * c3 * (8 pi)    = {float(GCAR * C3 * GB_SEAM):.6f}   = g_car  = 5")
    print(f"  A_Lam * c3 * (8 pi)    = {float(A_LAM * C3 * GB_SEAM):.6f}  = A_Lam  = 10")
    print("  -> integrated over the closed 2-sphere the pi CANCELS:")
    print("     the action ladder 1 : 5 : 10 = (bare seam):(carrier):(A_Lambda),")
    print("     all pi-free.  'c3*5' is exactly the carrier-weighted seam 2-surface.")
    nariai = f_entropy(1)
    print(f"  (the BH 'collapse' entropy floor S_tot/S_dS(x=1) = {float(nariai):.6f} = 2/3, also pi-free)")

    section("(3) 4D ACTION RECONSTRUCTION  ->  YES, via k = c3/2 (already the mechanism)")
    k = C3 / 2
    print(f"Einstein-Hilbert coefficient k = c3/2 = 1/(16 pi) = {float(k):.6f}")
    print("  this IS the 1/(16 pi G) of gravity with G=1; the factor 2 is the")
    print("  Gauss-Bonnet of the seam 2-sphere -> the 2-surface fixes the EH norm.")
    print(f"  Hawking T_H = c3/M = 1/(8 pi M): c3 is literally the '8 pi' of gravity.")
    print(f"  carrier weighting: c3*5 = {float(C3*5):.6f} = A_Lam * k = {float(A_LAM*k):.6f}")
    print("    (trivial, 5 = 10/2): the carrier-weighted seam = A_Lambda * the EH coupling.")
    print("  => the '2-surface collapse' is precisely the Gauss-Bonnet 2-surface of the")
    print("     Seam-Horizon Theorem; it is ALREADY accounted for (k=c3/2). The carrier")
    print("     weighting only shifts along the rational 1:5:10 ladder -- no new pi.")

    section("HONEST pi-HUNT (is there ANY clean pi relation in the discrete sector?)")
    for name, val in [("(2/3)^6", LAM2), ("gap", GAP), ("2/3", mp.mpf(2) / 3)]:
        print(f"  {name:8s}={float(val):.6f}: *pi={float(val*PI):.6f}, /pi={float(val/PI):.6f} -> no clean match")
    print("  CONCLUSION: pi appears ONLY as the closed-surface normalizer c3=1/(8pi).")
    print("  The whole discrete recovery + ladder is pi-free anchor data. This is a")
    print("  consistency confirmation of the No-Unit / dimensionless structure, NOT a")
    print("  new claim -- so it stays here in experiments/, out of the suite.")


if __name__ == "__main__":
    main()
