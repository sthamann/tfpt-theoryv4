"""TFPT prediction layer for the FRB-signature search.

Everything here is *derived* from the two TFPT axioms

    P1   c3     = 1 / (8*pi)          (seam / boundary constant)
    P2   g_car  = 5                   (carrier rank)

exactly as in ``verification/tfpt_constants.py`` and ``v5_e8_cascade.py``.
No SI value and no FRB number is hard-coded here.

The FRB hypotheses in ``problem_b.txt`` are *qualitative*: a black hole hopping
between neighbouring phi-attractors releases field energy

    Delta E_n  ~  E_0 * gamma(n)

so that bursts from one source should *not* be a smooth power law but should
show a **discrete / log-periodic cascade**.  TFPT does not (yet) publish a unique
numeric energy-ladder for FRBs, so this module is explicit about the distinction:

* the **model-independent** TFPT signature is *discreteness / log-periodicity* of
  the per-source energy distribution (a cascade instead of a continuum);
* a **TFPT-specific corroboration** is whether the measured log-spacing ratio
  coincides with a ratio that is natural in the compiler (the E8 dimension
  cascade, the transfer/Koide gap ``Delta = 6*ln(3/2)``, or the carrier ``3/2``).

These candidate ratios are *targets to test against*, not fitted parameters.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# --- the two axioms (identical to tfpt_constants.py) -----------------------
PI: float = math.pi
C3: float = 1.0 / (8.0 * PI)          # P1
G_CAR: int = 5                        # P2

# --- direct consequences (computed, never hand-assigned) -------------------
PHI0: float = 1.0 / (6.0 * PI) + 3.0 / (256.0 * PI**4)   # retained seed varphi_0
DIM_SPLUS: int = 2 ** (G_CAR - 1)                        # 16
N_FAM: int = (2 ** (G_CAR - 1) - 1) // G_CAR             # 3
RANK_E8: int = G_CAR + N_FAM                             # 8

# --- the E8 dimension cascade used across the TFPT documents ---------------
# 248 -> 120 -> 56 -> 27 -> 8 -> 3   (adjoint E8, SO(16), E7-56, E6-27, octet,
# colour-triplet).  This is the "Hierarchiekaskade" referenced in problem_b.
E8_CASCADE: tuple[int, ...] = (248, 120, 56, 27, 8, 3)

# --- the v5 nilpotent-orbit spine  D_n = 60 - 2n  (n = 0..26) ---------------
D_SPINE: tuple[int, ...] = tuple(60 - 2 * n for n in range(27))

# --- the transfer / Koide relaxation gap (F_transfer, v183/Koide) ----------
# rho(t) = e^{-t*Delta} rho(0),  Delta = 6 ln(3/2);  Koide gap rate (2/3)^6.
DELTA_GAP: float = 6.0 * math.log(1.5)        # ~2.4328
LAMBDA2_KOIDE: float = (2.0 / 3.0) ** 6       # ~0.0878


def cascade_ratios() -> list[float]:
    """Consecutive ratios of the E8 dimension cascade ``E8_CASCADE``."""
    c = E8_CASCADE
    return [c[i] / c[i + 1] for i in range(len(c) - 1)]


def gamma(n: int, ladder: str = "cascade") -> float:
    """The cascade amplitude ``gamma(n)`` (normalised to the top rung = 1).

    ``ladder="cascade"`` uses the E8 dimension cascade directly,
    ``gamma(n) = E8_CASCADE[n] / E8_CASCADE[0]``.

    ``ladder="geometric_three_half"`` uses the carrier geometric ladder
    ``gamma(n) = (2/3)**n`` (one carrier step per rung), i.e. neighbouring
    attractors a factor 3/2 apart in energy.
    """
    if ladder == "cascade":
        if not 0 <= n < len(E8_CASCADE):
            raise IndexError(f"cascade rung {n} out of range 0..{len(E8_CASCADE) - 1}")
        return E8_CASCADE[n] / E8_CASCADE[0]
    if ladder == "geometric_three_half":
        return (2.0 / 3.0) ** n
    raise ValueError(f"unknown ladder {ladder!r}")


@dataclass(frozen=True)
class RatioTarget:
    """A TFPT-natural log-spacing ratio that a real energy cascade can be
    compared against.  ``value`` is the energy ratio between neighbouring
    families (E_k / E_{k+1} > 1); ``provenance`` records where it comes from."""

    name: str
    value: float
    provenance: str


def candidate_ratios() -> list[RatioTarget]:
    """Energy-ratio targets that would count as TFPT-specific corroboration.

    A measured log-periodic spacing ratio matching one of these (within the
    spacing uncertainty) is a positive, *theory-anchored* indication; a smooth
    power law with no preferred ratio is a negative result for TFPT.
    """
    cr = cascade_ratios()
    mean_cascade = sum(cr) / len(cr)
    return [
        RatioTarget("carrier_3_2", 1.5, "carrier step 3/2 (g_car geometry)"),
        RatioTarget("two_thirds_inverse", 1.0 / (2.0 / 3.0), "Z2/N_fam attractor 2/3 inverted"),
        RatioTarget("exp_delta_gap", math.exp(DELTA_GAP), "e^{6 ln 3/2} = (3/2)^6 transfer gap"),
        RatioTarget("cascade_mean", mean_cascade, "mean of E8 dimension-cascade ratios"),
        RatioTarget("phi0_inverse", 1.0 / PHI0, "1/phi0 (retained seed)"),
    ]


def summary() -> dict[str, float]:
    """Numeric snapshot of the prediction layer (printed by ``frb-tfpt audit``)."""
    return {
        "c3": C3,
        "g_car": float(G_CAR),
        "phi0": PHI0,
        "delta_gap_6ln(3/2)": DELTA_GAP,
        "exp_delta_gap": math.exp(DELTA_GAP),
        "lambda2_koide": LAMBDA2_KOIDE,
        "cascade_ratio_mean": sum(cascade_ratios()) / len(cascade_ratios()),
        "phi0_inverse": 1.0 / PHI0,
    }
