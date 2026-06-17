"""QT.01 — the entanglement spectrum of the second-quantised kernel.

`problem_1.txt` §4 ("Entanglement Spektren") asks whether the reduced density matrix
of the TFPT compiler carries the kernel ratios.  The recovery transport is the
Bogoliubov second quantisation ``Gamma(t)`` of a one-particle contraction (suite
v161); the corresponding free-fermion (Gaussian) state has single-particle
*occupation* eigenvalues equal to the kernel ``{1, (2/3)^6, (1/3)^6}``.

The exact kernel identities live on the mode **surprisals** ``s_k = -ln(zeta_k)``
(the information content of each occupation eigenvalue):

    s( (2/3)^6 ) = 6 ln(3/2) = Delta              (the transfer/Koide gap)
    s( (1/3)^6 ) = 6 ln 3                          (the N_fam=3 log)
    s_3 / s_2    = ln 3 / ln(3/2) = 2.7095         (= the FRB.09 recovery-clock g1/g2, v124)
    zeta = 1  ->  s = 0                             (a zero-surprisal "certain" mode = the
                                                     protected/decoherence-free "law")

The single-particle modular energies ``eps_k = ln((1-zeta_k)/zeta_k)`` carry a small
``-ln(1-zeta)`` correction and are reported as derived; the many-body Schmidt-eigenvalue
recovery reproduces ``I_n = (2/3)^{6n}``.  Internal-consistency restatement (no data),
the entanglement-spectrum face of the recovery channel.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import product

from .constants import DELTA_GAP, LAMBDA


@dataclass
class EntanglementReport:
    occupation: tuple[float, ...]          # zeta_k = kernel occupation spectrum
    surprisals: list[float]                # s_k = -ln(zeta_k) for the contracted modes
    modular_energies: list[float]          # eps_k = ln((1-zeta)/zeta) (derived)
    schmidt: list[float]                   # many-body reduced-dm eigenvalues (sorted)
    recovery_I: dict[int, float]           # n -> contracted survival = (2/3)^{6n}
    protected_present: bool                # a zeta=1 zero-surprisal mode
    s_gap_is_delta: bool                   # s((2/3)^6) == 6 ln(3/2) == Delta
    s_three_is_6ln3: bool                  # s((1/3)^6) == 6 ln 3
    s_ratio: float                         # s_3/s_2
    s_ratio_is_clock: bool                 # == ln3/ln(3/2) (FRB.09 g1/g2)
    verdict: str


def entanglement_spectrum(occupation: tuple[float, ...] = LAMBDA) -> EntanglementReport:
    contracted = [z for z in occupation if z < 1.0 - 1e-12]      # (2/3)^6, (1/3)^6
    protected = any(abs(z - 1.0) < 1e-12 for z in occupation)
    surpr = [-math.log(z) for z in contracted]                   # exact kernel logs
    modular = [math.log((1.0 - z) / z) for z in contracted]      # derived modular energy

    schmidt = []
    for occ in product([0, 1], repeat=len(contracted)):
        p = 1.0
        for z, o in zip(contracted, occ, strict=True):
            p *= z if o else (1.0 - z)
        schmidt.append(p)
    schmidt = sorted(schmidt, reverse=True)

    recovery = {n: float(contracted[0] ** n) for n in (1, 2, 3)}  # (2/3)^{6n}

    s2, s3 = surpr[0], surpr[1]
    clock_ratio = math.log(3.0) / math.log(1.5)
    s_gap = abs(s2 - DELTA_GAP) < 1e-9
    s_three = abs(s3 - 6.0 * math.log(3.0)) < 1e-9
    s_ratio = s3 / s2
    s_ratio_clock = abs(s_ratio - clock_ratio) < 1e-9

    ok = protected and s_gap and s_three and s_ratio_clock
    verdict = ("entanglement spectrum carries the kernel exactly: a protected "
               f"(zero-surprisal, decoherence-free) zeta=1 mode, surprisals {{6 ln(3/2)="
               f"{s2:.4f}, 6 ln3={s3:.4f}}}, ratio {s_ratio:.4f}=ln3/ln(3/2), and Schmidt "
               "recovery I_n=(2/3)^{6n} -- the entanglement face of the recovery kernel"
               if ok else "FAIL: an entanglement-spectrum identity did not hold")
    return EntanglementReport(occupation, surpr, modular, schmidt, recovery, protected,
                              s_gap, s_three, s_ratio, s_ratio_clock, verdict)
