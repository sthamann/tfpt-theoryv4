"""Frozen TFPT prediction layer for the pulsar-glitch search.

Everything here is *derived* from the two TFPT axioms (identical to
``verification/tfpt_constants.py`` and the recovery-channel experiment):

    P1   c3    = 1 / (8*pi)                       seam / boundary constant
    P2   g_car = 5                                carrier rank

No SI value and no pulsar number is hard-coded.  The boundary-recovery kernel is
the *same* frozen object tested in FRB.02/09 and the GW-ringdown echo, so the
pulsar leg uses an identical candidate set -- this is what makes a coincidence a
genuine **cross-domain** statement instead of a per-dataset fit.

``problem_1.txt`` (section "Pulsar Glitches") asks, specifically, for

* (C) glitch sizes ``Delta nu / nu`` showing recurring *log* spacings near
  ``log(1+phi0)``, ``log 4``, ``log 8``, ``log 8pi``;
* (A) a recovery/healing parameter ``Q`` clustering at
  ``{phi0, 2 phi0, 4 phi0, 8 phi0, 1-phi0}``.

These are *targets to test against*, never fitted parameters.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

PI: float = math.pi
C3: float = 1.0 / (8.0 * PI)                              # P1
G_CAR: int = 5                                            # P2

# direct consequences (computed, never hand-assigned)
PHI0: float = 1.0 / (6.0 * PI) + 3.0 / (256.0 * PI**4)    # retained seed varphi_0 ~ 0.05317
N_FAM: int = 3
P2_EXP: int = 6                                           # |R^+(A_3)|, transport-cycle exponent
TWO_THIRDS: float = 2.0 / 3.0

# the boundary-recovery kernel (energy / amplitude survival), shared with
# recovery-channel and the FRB/GW echo tests
LAMBDA = (1.0, TWO_THIRDS**P2_EXP, (1.0 / 3.0) ** P2_EXP)            # 1, 64/729, 1/729
AMPLITUDE = (1.0, TWO_THIRDS ** (P2_EXP // 2), (1.0 / 3.0) ** (P2_EXP // 2))  # 1, 8/27, 1/27
DELTA_GAP: float = P2_EXP * math.log(1.5)                # 6 ln(3/2) ~ 2.4328


@dataclass(frozen=True)
class RatioTarget:
    """A preregistered size/spacing ratio (>1) a glitch-size ladder is tested
    against.  ``kind`` separates the cross-domain *kernel* ratios from the
    ``problem_1.txt`` section-C candidate set and from audit-only ratios."""

    name: str
    value: float
    kind: str          # "kernel" | "problem1" | "audit"
    provenance: str


def candidate_size_ratios() -> list[RatioTarget]:
    """Adjacent-family size ratios that would count as TFPT corroboration.

    A measured log-periodic spacing matching one of these (within the spacing
    uncertainty) is a theory-anchored indication; a smooth distribution with no
    preferred ratio is a negative result for TFPT.
    """
    return [
        # --- cross-domain kernel (same frozen object as FRB.02/09, GW echo) ---
        RatioTarget("carrier_3/2", 1.5, "kernel", "carrier step 3/2 (g_car geometry)"),
        RatioTarget("(3/2)^3=27/8", 27 / 8, "kernel", "amplitude gap (2/3)^3 inverted"),
        RatioTarget("(3/2)^6=729/64", 729 / 64, "kernel", "energy gap (2/3)^6 inverted = e^{Delta}"),
        # --- problem_1.txt section C (glitch-size specific) ---
        RatioTarget("1+phi0", 1.0 + PHI0, "problem1", "problem_1.txt C: log(1+phi0)"),
        RatioTarget("4", 4.0, "problem1", "problem_1.txt C: log 4 (mu4 / index-4)"),
        RatioTarget("8", 8.0, "problem1", "problem_1.txt C: log 8 (rank E8)"),
        RatioTarget("8pi", 8.0 * PI, "problem1", "problem_1.txt C: log 8pi (1/c3)"),
    ]


def candidate_Q_clusters() -> dict[str, float]:
    """``problem_1.txt`` section-A recovery-parameter ``Q`` targets.

    Not testable on the Jodrell Bank size catalogue (which carries ``Delta nu/nu``
    and ``Delta nudot/nudot``, *not* the per-glitch healing fraction ``Q``); kept
    here so the data-limited PG.04 channel has its frozen targets on record.
    """
    return {"phi0": PHI0, "2phi0": 2 * PHI0, "4phi0": 4 * PHI0,
            "8phi0": 8 * PHI0, "1-phi0": 1 - PHI0}


def kernel_log_ratios() -> dict[str, float]:
    """The kernel step ratios in *log10* (dex) -- the cross-domain comb teeth
    a per-pulsar size ladder is tested for (PG.02)."""
    return {
        "3/2": math.log10(1.5),
        "(3/2)^3": math.log10(27 / 8),
        "(3/2)^6": math.log10(729 / 64),
    }


# The exact discrete->dynamic clock (v124/v126/v147): rate(n) = -6 ln(1 - n/3),
# spectrum (1-n/3)^6, pole/wall at n = N_fam = 3.  A single recovery is therefore a
# TWO-mode + protected-floor clock with the det'-clean bend rate ratio below -- the
# correct multi-timescale candidate for PG.04 (not a (3/2)^k size ladder).
RECOVERY_RATE_1: float = P2_EXP * math.log(1.5)     # 6 ln(3/2) = Delta = 2.4328
RECOVERY_RATE_2: float = P2_EXP * math.log(3.0)     # 6 ln 3 = 6.5917
RECOVERY_BEND: float = math.log(3.0) / math.log(1.5)  # rate(2)/rate(1) = log_{3/2}3 = 2.7095
RECOVERY_WALL: int = N_FAM                           # >=3 robust decay modes is a tension


def summary() -> dict[str, float]:
    """Numeric snapshot printed by ``tfpt-pulsar audit``."""
    return {
        "c3": C3, "g_car": float(G_CAR), "phi0": PHI0,
        "N_fam": float(N_FAM), "p2_exp": float(P2_EXP),
        "delta_gap_6ln(3/2)": DELTA_GAP,
        "kernel_energy_(2/3)^6": LAMBDA[1],
        "kernel_amp_(2/3)^3": AMPLITUDE[1],
        "(3/2)^6": 729 / 64, "8pi": 8 * PI, "1+phi0": 1 + PHI0,
    }
