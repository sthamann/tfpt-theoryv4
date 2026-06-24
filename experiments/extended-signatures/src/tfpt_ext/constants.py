"""Frozen TFPT compiler numbers for extended signature searches."""

from __future__ import annotations

import math

C3 = 1.0 / (8.0 * math.pi)
PHI0 = (4.0 / 3.0) * C3 + 48.0 * C3**4
G_CAR = 5
N_FAM = 3
MU4 = 4

# recovery kernel
LAMBDA6 = (2.0 / 3.0) ** 6          # 64/729
LAMBDA3 = (2.0 / 3.0) ** 3          # 8/27
CLOCK_BEND = math.log(3) / math.log(1.5)   # 2.7095...
OMEGA_COMB = 2.0 * math.pi / math.log(1.5 ** 6)

# horizon / seam
DELTA_TOP = 48.0 * C3**4
BETA_RAD_DEG = math.degrees(PHI0 / (4.0 * math.pi))
SEED_SLOPE = 4.0 * math.pi - 1.0
XI = C3 / PHI0

# gravastar joint (experiments/gravastar-compactness)
GRAVASTAR_LAG_MS = 0.7              # round-trip at 62 Msun
GRAVASTAR_C = 3.0 / 8.0

# Hawking / scrambling (horizon_readouts)
W_D5 = 1920
HAWKING_DENOM = W_D5
AREA_LN3 = 4.0 * math.log(N_FAM)
LN3 = math.log(N_FAM)

# Galois-CP
DELTA_CKM_LEAD_DEG = 60.0
DELTA_PMNS_DEG = 240.0
LAMBDA_C = math.sqrt(PHI0 * (1.0 - PHI0))
DELTA_CKM_DEG = math.degrees(math.pi / 3.0 + 3.0 * LAMBDA_C**2)
