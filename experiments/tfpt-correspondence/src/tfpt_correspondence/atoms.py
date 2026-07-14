"""Frozen TFPT atoms (from axioms P1+P2) and the correspondence phase-boundary constants.

Every value here is an EXACT rational built from the two axioms -- P1 ``c3 = 1/(8 pi)``
and P2 ``g_car = 5`` -- plus the derived carrier atoms, with the single transcendental
primitive ``pi``.  No fitted exponents, no SI inputs.  ``tests/test_frozen_kernel.py``
asserts these equal ``hypotheses/correspondence_v1.yaml`` byte-for-byte.
"""

from __future__ import annotations

import math
from fractions import Fraction

# --- axioms -----------------------------------------------------------------
C3 = 1.0 / (8.0 * math.pi)          # P1: boundary seam constant
G_CAR = 5                            # P2: carrier rank

# --- derived integer atoms --------------------------------------------------
MU4 = 4                              # |mu4|: four Gauss-Bonnet marks / order-4 clock (= h(A3))
Z2 = 2                               # |Z2|: Moebius sheet involution
N_FAM = 4 - 1                        # A3 family count = |mu4| - 1 = 3
ANCHOR = (1, 1, 2)                   # parabolic anchor a

# anchor symmetric functions
E1_ANCHOR = sum(ANCHOR)              # e1(a) = 4
P2_ANCHOR = sum(x * x for x in ANCHOR)  # p2(a) = sum a_i^2 = 6

# --- the four correspondence phase-boundary constants, as EXACT atom fractions
# entropy (Bekenstein / holographic) density: 1/4 = 1/|mu4|
BEKENSTEIN_DENSITY = Fraction(1, MU4)                       # = 1/4
# de Sitter horizon endpoint of the SdS compactness quotient: 1/2 = |Z2|/|mu4|
DE_SITTER_ENDPOINT = Fraction(Z2, MU4)                      # = 1/2
# Nariai / max-horizonless-compactness threshold: 3/8 = p2(a)/e1(a)^2
NARIAI_THRESHOLD = Fraction(P2_ANCHOR, E1_ANCHOR ** 2)      # = 3/8
# recovery reflectivity / transfer gap: (2/3)^6 = (|Z2|/N_fam)^(2 N_fam)
GAP6 = Fraction(Z2, N_FAM) ** (2 * N_FAM)                   # = 64/729

# Bekenstein-bound coefficient: 1/(2 pi) = 4 c3  (atom-locked; the critical-quotient scale)
FOUR_C3 = 4.0 * C3                                          # = 1/(2 pi)

# --- classical compactness landmarks (geometric, C = M/R) -------------------
PHOTON_SPHERE = Fraction(1, 3)       # light-trapping threshold (surface inside 3M)
BUCHDAHL = Fraction(4, 9)            # Buchdahl bound
HORIZON = Fraction(1, 2)             # Schwarzschild horizon


def atom_lock_table() -> dict[str, tuple[Fraction | float, str, bool]]:
    """Each phase-boundary constant -> (value, atom identity, holds-exactly)."""
    return {
        "bekenstein_density_1_4": (
            BEKENSTEIN_DENSITY, "1/|mu4|", BEKENSTEIN_DENSITY == Fraction(1, 4)),
        "de_sitter_endpoint_1_2": (
            DE_SITTER_ENDPOINT, "|Z2|/|mu4|", DE_SITTER_ENDPOINT == Fraction(1, 2)),
        "nariai_threshold_3_8": (
            NARIAI_THRESHOLD, "p2(a)/e1(a)^2", NARIAI_THRESHOLD == Fraction(3, 8)),
        "recovery_gap_64_729": (
            GAP6, "(|Z2|/N_fam)^(2 N_fam)", GAP6 == Fraction(64, 729)),
        "bekenstein_coeff_4c3": (
            FOUR_C3, "1/(2 pi)", math.isclose(FOUR_C3, 1.0 / (2.0 * math.pi), rel_tol=1e-15)),
    }
