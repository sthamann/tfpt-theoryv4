"""TFPT Boundary-Recovery kernel — the prediction layer for the FRB *search targets*.

Firewall (from the user's note and the TFPT horizon docs): FRBs are **not** new
gravity and **not** a direct Hawking signature.  The only admissible statement is

    IF the TFPT boundary recovery is real, THEN FRB repeaters may show a few
    *dimensionless* echoes of the recovery kernel.

These are SEARCH TARGETS, not claims.  The kernel is the Page/boundary
recoverability spectrum, all derived from the two axioms (c3, g_car) via the
attractor ratio  2/3 = |Z2|/N_fam  and the transport-cycle exponent 6 (the
Z6 / A3 cycle that also sets the Koide gap  Delta = 6 ln(3/2)):

    spec(T) = { 1, (2/3)^6, (1/3)^6 }          (information / energy channel)
    Delta   = 6 ln(3/2)                          (gap)

Because many FRB observables read a *field amplitude* or a *visibility window*
rather than an information/energy, the natural quantities are the roots of the
eigenvalues (energy ~ lambda, amplitude ~ sqrt(lambda)).  This gives a hierarchy

    1 -> (2/3) -> (2/3)^3 -> (2/3)^6     and     1 -> (1/3) -> (1/3)^3 -> (1/3)^6

i.e. the unpowered step (sub-burst relaxation), the cube root = field amplitude
(8/27, 1/27), and the sixth power = integrated information (64/729, 1/729).
No new numbers are introduced — only roots of the existing kernel.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from .tfpt_ladder import N_FAM, PHI0  # noqa: F401  (re-exported provenance)

# --- the attractor ratio and the transport exponent (EXACT, frozen) --------
# The kernel is frozen as exact rationals so the search can never "shop" for a
# better exponent: 2/3 = |Z2|/N_fam (Koide attractor), 1/3 = 1/N_fam, and the
# transport exponent is 6 (the Z6/A3 cycle that sets Delta = 6 ln(3/2)).
F_TWO_THIRDS: Fraction = Fraction(2, 3)
F_ONE_THIRD: Fraction = Fraction(1, 3)
CYCLE: int = 6

# energy channel: spec(T) = {1, (2/3)^6, (1/3)^6}
LAMBDA2_FRAC: Fraction = F_TWO_THIRDS ** CYCLE          # 64/729
LAMBDA3_FRAC: Fraction = F_ONE_THIRD ** CYCLE           # 1/729
# amplitude / field-visibility channel = square roots: {(2/3)^3, (1/3)^3}
SQRT_LAMBDA2_FRAC: Fraction = F_TWO_THIRDS ** (CYCLE // 2)   # 8/27
SQRT_LAMBDA3_FRAC: Fraction = F_ONE_THIRD ** (CYCLE // 2)    # 1/27

# float views (defined from the exact fractions, so they never drift)
TWO_THIRDS: float = float(F_TWO_THIRDS)
ONE_THIRD: float = float(F_ONE_THIRD)
LAMBDA2: float = float(LAMBDA2_FRAC)        # 0.08779...
LAMBDA3: float = float(LAMBDA3_FRAC)        # 0.0013717...
SQRT_LAMBDA2: float = float(SQRT_LAMBDA2_FRAC)   # 0.296296...
SQRT_LAMBDA3: float = float(SQRT_LAMBDA3_FRAC)   # 0.037037...
SPECTRUM: tuple[float, float, float] = (1.0, LAMBDA2, LAMBDA3)
DELTA_GAP: float = CYCLE * math.log(1.5)


def kernel_fractions() -> dict[str, Fraction]:
    """The frozen kernel as EXACT rationals (single source of truth).

    Used by the preregistration cross-check and the constant-guard test; no
    floating point and no fitted exponents are permitted to enter here.
    """
    return {
        "energy_2": LAMBDA2_FRAC,        # 64/729
        "energy_3": LAMBDA3_FRAC,        # 1/729
        "field_2": SQRT_LAMBDA2_FRAC,    # 8/27
        "field_3": SQRT_LAMBDA3_FRAC,    # 1/27
        "step_2": F_TWO_THIRDS,          # 2/3
        "step_3": F_ONE_THIRD,           # 1/3
    }


@dataclass(frozen=True)
class KernelRatio:
    """A dimensionless recovery ratio to test an FRB observable against."""

    name: str
    value: float
    channel: str          # "energy" | "amplitude" | "subburst"
    provenance: str


def kernel_ratios() -> list[KernelRatio]:
    """All recovery ratios across the three channels (no fitted exponents)."""
    return [
        KernelRatio("lambda2_energy", LAMBDA2, "energy", "(2/3)^6 = 64/729 Page subleading"),
        KernelRatio("lambda3_energy", LAMBDA3, "energy", "(1/3)^6 = 1/729 Page sub-subleading"),
        KernelRatio("sqrt_lambda2_amp", SQRT_LAMBDA2, "amplitude", "(2/3)^3 = 8/27 field/window root"),
        KernelRatio("sqrt_lambda3_amp", SQRT_LAMBDA3, "amplitude", "(1/3)^3 = 1/27 field/window root"),
        KernelRatio("two_thirds_sub", TWO_THIRDS, "subburst", "2/3 unpowered sub-burst step"),
        KernelRatio("one_third_sub", ONE_THIRD, "subburst", "1/3 unpowered sub-burst step"),
    ]


# --- the seed block: cosmic birefringence and the baryon fraction ----------
# beta_rad = phi0 / (4 pi)  (radians);  Omega_b = (4 pi - 1) * beta_rad.
BETA_RAD: float = PHI0 / (4.0 * math.pi)
BETA_DEG: float = math.degrees(BETA_RAD)
OMEGA_B_TFPT: float = (4.0 * math.pi - 1.0) * BETA_RAD


def summary() -> dict[str, float]:
    return {
        "two_thirds": TWO_THIRDS,
        "lambda2_(2/3)^6": LAMBDA2,
        "lambda3_(1/3)^6": LAMBDA3,
        "sqrt_lambda2_(8/27)": SQRT_LAMBDA2,
        "sqrt_lambda3_(1/27)": SQRT_LAMBDA3,
        "delta_gap": DELTA_GAP,
        "beta_rad_deg": BETA_DEG,
        "Omega_b_TFPT": OMEGA_B_TFPT,
    }
