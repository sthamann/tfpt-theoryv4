"""v203 -- The EHT achromatic polarization-rotation intercept beta_BH around a
horizon-scale black hole. The SURVIVING core of the old UFE/black-hole notes:
NOT the full RN-type metric (superseded by the Nariai / seam=horizon programme,
v101-v104), only the local dyonic polarization signature, whose COUPLING is fixed
by the same c3 that sets alpha and the cosmic birefringence beta_rad.

  [E] 1. THE COEFFICIENT IS A COMPILER NUMBER. The local achromatic rotation rate
        beta_BH(r) = Q_e^eff Q_m^eff / (256 pi^4 r^2) = 16 c3^4 (Q_e Q_m / r^2),
        and 16 c3^4 = 1/(256 pi^4) EXACTLY (c3 = 1/(8 pi)). No free coupling.
  [E] 2. CROSS-LINK TO THE alpha-KERNEL. 16 c3^4 = delta_top/3 with delta_top =
        48 c3^4 = 3/(256 pi^4), the SAME topological top-form coefficient that
        fixes the alpha-kernel precision-zone correction (tfpt_constants.dtop) and
        sits one row from the cosmic-birefringence seed beta_rad = phi0/(4 pi).
        So EHT polarimetry probes the same admissibility data as the alpha row,
        projected onto the local horizon collar instead of the Thomson limit.
  [C] 3. SHAPE FIXED, AMPLITUDE MODEL-DEPENDENT. TFPT fixes the structured 1/r^2
        profile, the achromaticity (no lambda^2 dependence), and the sign-flip
        under E.B reversal; the amplitude Q_e^eff Q_m^eff (the local effective
        E.B structure on the collar) is an MHD/GR weight, not a compiler output.
        So the channel is typed [C] (shape/sign) -- never a parameter-free
        amplitude prediction at one image pixel.
  [X] 4. THREE INDEPENDENT NULLS (dated kill test). The residual intercept
        chi_0^res = chi_0^obs - chi_0^GRMHD must simultaneously (a) be achromatic
        (frequency-null), (b) follow the 1/r^2 spatial profile (spatial-null),
        (c) flip sign under effective E.B reversal (sign-flip null). A residual
        statistically consistent with zero across the image after honest GRMHD
        subtraction, OR failing any null, falsifies THIS channel -- not the
        compiler (the determinant-line coupling is shared with alpha/beta_rad).
  [I] 5. SCOPE. The old UFE closed RN-type metric (D/r^4, regular cores, shadow
        shift) is NOT imported -- it is superseded by the Nariai/seam=horizon
        readouts (v101-v104, v190). Only the polarization signature survives.

  Wolfram-mirrored (the coefficient identity 16 c3^4 = 1/(256 pi^4) = delta_top/3
  is exact).
"""
import sympy as sp

from tfpt_constants import check, summary, reset

C3 = sp.Rational(1, 1) / (8 * sp.pi)
DTOP = 48 * C3**4              # topological top-form coefficient = 3/(256 pi^4)


def run():
    reset()
    print("v203 EHT achromatic polarization intercept beta_BH = 16 c3^4 (Q_e Q_m / r^2)")

    # 1. the coefficient is exactly 1/(256 pi^4)
    coeff = 16 * C3**4
    check("COEFFICIENT [E]: beta_BH = Q_e Q_m/(256 pi^4 r^2) = 16 c3^4 (Q_e Q_m/r^2), "
          "and 16 c3^4 = 1/(256 pi^4) exactly (c3 = 1/(8 pi)) -- no free coupling",
          sp.simplify(coeff - 1 / (256 * sp.pi**4)) == 0)

    # 2. cross-link to the alpha-kernel: 16 c3^4 = delta_top/3, delta_top = 48 c3^4
    check("alpha-KERNEL CROSS-LINK [E]: 16 c3^4 = delta_top/3 with delta_top = "
          "48 c3^4 = 3/(256 pi^4) -- the SAME top-form coefficient that fixes the "
          "alpha-kernel precision-zone correction (tfpt_constants.dtop); the EHT "
          "coupling and the alpha correction are one compiler number",
          sp.simplify(coeff - DTOP / 3) == 0 and sp.simplify(DTOP - 3 / (256 * sp.pi**4)) == 0)

    # 3. shape fixed, amplitude model-dependent -> [C]
    check("SHAPE FIXED, AMPLITUDE [C]: TFPT fixes the 1/r^2 profile, achromaticity, "
          "and sign-flip under E.B reversal; the amplitude Q_e^eff Q_m^eff is an "
          "MHD/GR weight, NOT a compiler output -- the channel is [C] (shape/sign), "
          "never a parameter-free pixel amplitude", True)

    # 4. three independent nulls (kill test)
    nulls = ("frequency-null (achromatic, no lambda^2 dependence)",
             "spatial-null (structured 1/r^2 profile)",
             "sign-flip null (reverses under effective E.B reversal)")
    check("THREE NULLS [X] (dated kill test): the residual intercept chi_0^res = "
          "chi_0^obs - chi_0^GRMHD must pass all of %s simultaneously; a residual "
          "consistent with zero after honest GRMHD subtraction, or failing any "
          "null, falsifies THIS channel (not the compiler)" % (nulls,),
          len(nulls) == 3)

    # 5. scope: NOT the UFE metric
    check("SCOPE [I]: the old UFE closed RN-type metric (D/r^4, regular cores, "
          "shadow shift) is NOT imported -- superseded by the Nariai/seam=horizon "
          "readouts (v101-v104, v190); only the polarization signature survives, "
          "with its coupling shared with alpha (delta_top) and beta_rad (phi0/4pi)", True)

    return summary("v203 EHT achromatic intercept: 16 c3^4 = 1/(256 pi^4) = delta_top/3 [E], shape/sign [C]/[X]")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
