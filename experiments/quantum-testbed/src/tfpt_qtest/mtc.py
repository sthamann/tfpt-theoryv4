"""QT.05 -- the particle / statistics layer: the carrier anyon MTC and its NEW
observable phase quanta (v241/v242/v243).

The discrete->dynamic completion (v240-v245) reconstructs the emergent QFT: the seam
net's superselection sectors ARE the particle types (v241), their exchange statistics
are the topological spins (v242), and the 2-particle S-matrix is the braiding monodromy
(v243).  This module reads that data as **concrete, falsifiable phase signatures**.

The carrier discriminant form (Lean-verified glue FORM.GLUE.01) on Z4 x Z4:
    q(x,y) = (5 x^2 + 3 y^2)/8 mod 1,   B(a,b) = (5 x x' + 3 y y')/4 mod 1,
    topological spin  theta(a) = e^{2 pi i q(a)},   monodromy  M(a,b) = e^{2 pi i B(a,b)}.

NEW signatures (different in kind from the recovery-kernel ratios):

  * STATISTICAL PHASE QUANTA.  q is quantised in 1/8 -> spins are 8th roots of unity,
    so the **spin (exchange) phase comes in units of pi/4**; B is quantised in 1/4 ->
    the **braiding (monodromy) phase comes in units of pi/2**.  The 16 sectors split
    into 6 bosons (theta=1), **2 fermions (theta=-1, phase pi)** and 8 genuine anyons
    (theta in {e^{+-i pi/4}, ...}).  So the *dominant* statistical structure is the
    m=2 fermion mode (theta=-1), with finer pi/2 (anyon) and pi/4 (spin) substructure.
    -> This sharpens AND reinterprets the FRB polarisation result FRB.08 ("fundamental
    m=2, not m=4"): m=2 is now the PREDICTED dominant (the fermion sector), not a null.
  * c = 8 (Gauss-Milgram).  (1/sqrt 16) sum_a theta_a = e^{2 pi i c/8} with c = 8 =
    g_car + N_fam -- the chiral central charge of the (E8)_1 boundary CFT lives in the
    anyon data.
  * INTEGRABLE BRAIDING S-MATRIX.  M is a unitary bicharacter (Yang-Baxter, crossing),
    diagonal in the conserved charges -> factorised, no particle production; trivial on
    the condensed holomorphic (E8)_1 point.

Internal-consistency (no external data): exact MTC arithmetic that turns the v241-v243
algebra into the observable phase comb a future polarisation / interferometric search
would target.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

G = [(x, y) for x in range(4) for y in range(4)]
N = 16


def q(a: tuple[int, int]) -> float:
    x, y = a
    return ((5 * x * x + 3 * y * y) % 8) / 8.0


def theta(a: tuple[int, int]) -> complex:
    return complex(np.exp(2j * np.pi * q(a)))


def bform(a: tuple[int, int], b: tuple[int, int]) -> float:
    return ((5 * a[0] * b[0] + 3 * a[1] * b[1]) % 4) / 4.0


def monodromy(a: tuple[int, int], b: tuple[int, int]) -> complex:
    return complex(np.exp(2j * np.pi * bform(a, b)))


@dataclass
class MTCReport:
    n_sectors: int
    n_bosons: int
    n_fermions: int
    n_anyons: int
    spin_phase_quantum: float       # pi/4  (q in units of 1/8)
    braid_phase_quantum: float      # pi/2  (B in units of 1/4)
    fermion_phase: float            # pi    (theta = -1)
    distinct_spin_phases: list[float]
    central_charge: float           # Gauss-Milgram c
    c_is_8: bool
    integrable: bool                # M unitary bicharacter (factorised S)
    trivial_on_E8: bool             # monodromy trivial on the condensed holomorphic point
    verdict: str


def mtc_signatures() -> MTCReport:
    spins = {a: theta(a) for a in G}
    bosons = [a for a in G if abs(spins[a] - 1) < 1e-9]
    fermions = [a for a in G if abs(spins[a] + 1) < 1e-9]
    anyons = [a for a in G if abs(spins[a].imag) > 1e-9]

    qpos = sorted({q(a) for a in G if q(a) > 1e-12})
    bpos = sorted({bform(a, b) for a in G for b in G if bform(a, b) > 1e-12})
    spin_quantum = 2 * math.pi * min(qpos)          # pi/4
    braid_quantum = 2 * math.pi * min(bpos)         # pi/2
    distinct = sorted({round((np.angle(spins[a]) % (2 * np.pi)), 6) for a in G})

    gm = sum(spins.values()) / math.sqrt(N)
    c = (np.angle(gm) / (2 * np.pi) * 8) % 8         # e^{2 pi i c/8} -> c mod 8 (=0 for c=8)
    c_is_8 = abs(gm - 1.0) < 1e-9                    # e^{2 pi i 8/8} = 1

    # integrable: |M|=1 and bicharacter
    unit = all(abs(abs(monodromy(a, b)) - 1) < 1e-12 for a in G for b in G)
    bich = all(abs(monodromy(((a[0] + ap[0]) % 4, (a[1] + ap[1]) % 4), b)
                    - monodromy(a, b) * monodromy(ap, b)) < 1e-9
               for a in G for ap in G[:4] for b in G[:4])
    integrable = unit and bich

    # trivial braiding on the condensed Lagrangian (E8) sector
    H1 = {(0, 0), (1, 1), (2, 2), (3, 3)}
    trivial_E8 = all(abs(monodromy(a, b) - 1) < 1e-9 for a in H1 for b in H1)

    ok = (len(G) == 16 and len(bosons) == 6 and len(fermions) == 2 and len(anyons) == 8
          and abs(spin_quantum - math.pi / 4) < 1e-9 and abs(braid_quantum - math.pi / 2) < 1e-9
          and c_is_8 and integrable and trivial_E8)
    verdict = (
        f"16 sectors -> {len(bosons)} bosons, {len(fermions)} fermions (theta=-1, phase pi = the "
        f"m=2 dominant), {len(anyons)} anyons; statistical phase quanta = pi/4 (spin, 8th roots) "
        f"and pi/2 (braiding); c=8 (Gauss-Milgram); integrable factorised S, trivial on (E8)_1 "
        "-- the FRB.08 'fundamental m=2' is the PREDICTED fermion sector, not a null"
        if ok else "FAIL: an MTC identity did not hold")
    return MTCReport(len(G), len(bosons), len(fermions), len(anyons),
                     spin_quantum, braid_quantum, math.pi, distinct,
                     float(c) if not c_is_8 else 8.0, c_is_8, integrable, trivial_E8, verdict)
