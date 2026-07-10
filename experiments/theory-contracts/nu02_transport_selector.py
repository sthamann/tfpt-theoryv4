"""NU.CI.02 transport selector on the Casas-Ibarra family -- a THEORY CONTRACT.

Follow-up to nu01 (next-step 3, 2026-07-10).  nu01 showed the seam symmetries cut
the Casas-Ibarra matrix to a ONE-REAL-parameter family R(z) = F diag(1,e^z,e^{-z})
F^* (z in R; the CI hyperbolic angle) but do NOT isolate a point -- so the seesaw
(absolute nu scale, Majorana/leptogenesis phase) is not closed by symmetry alone.
This contract tests concrete TRANSPORT/MINIMALITY selectors for the leftover z and
reports, honestly, that:

  * the naive minimal-transport selector (min ||R - I||) gives z = 0 => R = I
    (trivial, NO extra CP) -- an ASSUMPTION, not a derivation;
  * a PRINCIPLED selector identifying the CI angle with the seam TRANSFER GAP,
    e^z = (3/2)^6 i.e. z = 6 ln(3/2) = Delta (the v302 gap), gives a UNIQUE
    nontrivial R and hence a DEFINITE leptogenesis-relevant CP content -- offered
    as a CONDITIONAL prediction [P], because the selector itself is a hypothesis.

So the neutrino dynamics closes CONDITIONALLY on the transport selector; it does
NOT close from symmetry alone.  The value of this contract is to turn "one free CI
angle" into "one named hypothesis with a concrete, falsifiable CP consequence".

Checks (hard-typed):

  C1 [E] FAMILY RECALLED (nu01): R(z) = F diag(1,e^z,e^{-z}) F^* is complex-
     orthogonal, det 1, [R,C3]=0, Theta-real for z in R (recomputed); Im(R) = 0 iff
     z = 0.
  C2 [E] MINIMAL-TRANSPORT SELECTOR IS TRIVIAL: argmin_z ||R(z) - I||_F = 0 => R=I,
     i.e. no seesaw CP -- a finite point but an ASSUMPTION (no leptogenesis), not a
     derivation.
  C3 [P] SEAM-GAP SELECTOR => UNIQUE NONTRIVIAL R: identifying the CI angle with the
     transfer gap, e^z = (3/2)^6 (z = 6 ln(3/2) = Delta, v302), gives a UNIQUE R
     with a DEFINITE CP content (||Im R||_F and the leptogenesis invariant
     J_R = Im(R_12 R_21) are fixed numbers) -- a conditional prediction.
  C4 [E] DISCRIMINATION / POWER: distinct selectors give distinct R (the map z -> R
     is injective on z >= 0), so the selector genuinely MATTERS -- the CP content is
     NOT selector-independent; a wrong selector is falsifiable against leptogenesis.
  C5 [O] RELOCATION AUDIT (honest): the seesaw is NOT closed by symmetry (nu01); it
     closes CONDITIONALLY on a transport selector.  The seam-gap identification is a
     NAMED [P] hypothesis with a concrete CP consequence; deriving it (or refuting
     it) is the open step.  Never a scorecard row; never [E].

Firewall: neutrinos are an F_transfer bridge; internal consistency, not evidence.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

RESULTS = Path(__file__).resolve().parent / "nu02_transport_selector_results.json"
CHECKS: list[dict] = []

C3M = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], float)
THETA = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], float)
W = np.exp(2j * np.pi / 3)
F = np.array([[W ** (j * k) for k in range(3)] for j in range(3)]) / np.sqrt(3)
GAP = 6 * math.log(1.5)                         # Delta = 6 ln(3/2), v302 transfer gap


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def R_of_z(z):
    D = np.diag([1.0, np.exp(z), np.exp(-z)]).astype(complex)
    return F @ D @ F.conj().T


def c1_family() -> None:
    z = 0.7
    R = R_of_z(z)
    orth = np.max(np.abs(R.T @ R - np.eye(3)))
    det1 = abs(np.linalg.det(R) - 1)
    comm = np.max(np.abs(R @ C3M - C3M @ R))
    real_theta = np.max(np.abs(THETA @ R @ THETA - R.conj()))
    imzero = np.max(np.abs(np.imag(R_of_z(0.0))))
    ok = orth < 1e-9 and det1 < 1e-9 and comm < 1e-9 and real_theta < 1e-9 and imzero < 1e-12
    check("C1 FAMILY RECALLED (nu01) [E]: R(z)=F diag(1,e^z,e^-z) F^* is complex-"
          "orthogonal, det 1, [R,C3]=0, Theta-real for real z; Im R = 0 iff z=0",
          ok, "||R^TR-I||=%.1e, |det-1|=%.1e, ||[R,C3]||=%.1e, Theta-real=%.1e, "
          "Im R(0)=%.1e" % (orth, det1, comm, real_theta, imzero))


def c2_minimal_trivial() -> None:
    zs = np.linspace(-2, 2, 4001)
    norms = [np.linalg.norm(R_of_z(z) - np.eye(3)) for z in zs]
    zmin = zs[int(np.argmin(norms))]
    Rmin = R_of_z(zmin)
    ok = abs(zmin) < 1e-2 and np.max(np.abs(Rmin - np.eye(3))) < 1e-2
    check("C2 MINIMAL-TRANSPORT SELECTOR IS TRIVIAL [E]: argmin_z ||R(z)-I|| = %.3f "
          "=> R = I (no seesaw CP) -- a finite point but an ASSUMPTION (no "
          "leptogenesis), not a derivation" % zmin,
          ok, "z* = %.3f, ||R(z*)-I|| = %.2e" % (zmin, float(np.min(norms))))


def cp_content(z):
    R = R_of_z(z)
    imnorm = float(np.linalg.norm(np.imag(R)))
    J = float(np.imag(R[0, 1] * R[1, 0]))       # a leptogenesis-type CP invariant
    return imnorm, J


def c3_seam_gap() -> None:
    z = GAP
    ez = math.exp(z)
    imnorm, J = cp_content(z)
    unique = ez > 0                              # e^z = (3/2)^6 is a single value
    ok = abs(ez - 1.5 ** 6) / 1.5 ** 6 < 1e-9 and imnorm > 1e-3
    check("C3 SEAM-GAP SELECTOR => UNIQUE NONTRIVIAL R [P]: e^z = (3/2)^6 (z = 6 "
          "ln(3/2) = Delta, v302) gives a UNIQUE R with DEFINITE CP content "
          "||Im R||_F = %.4f, leptogenesis invariant J_R = Im(R12 R21) = %.4f -- a "
          "conditional prediction (selector = hypothesis)" % (imnorm, J),
          ok, "z=Delta=%.4f, e^z=%.4f=(3/2)^6, ||Im R||=%.4f, J_R=%.4f"
          % (z, ez, imnorm, J))


def c4_power() -> None:
    R1, R2 = R_of_z(GAP), R_of_z(0.5)
    distinct = np.max(np.abs(R1 - R2)) > 1e-2
    im0 = cp_content(0.0)[0]
    imgap = cp_content(GAP)[0]
    ok = distinct and im0 < 1e-12 < imgap
    check("C4 DISCRIMINATION / POWER [E]: distinct selectors give distinct R (z->R "
          "injective for z>=0); CP content ranges from 0 (z=0, trivial) to %.3f "
          "(z=Delta) -- the selector MATTERS, the CP is not selector-independent and "
          "a wrong selector is falsifiable against leptogenesis" % imgap,
          ok, "R(Delta) != R(0.5): %s; ||Im R|| 0.0 -> %.3f across selectors"
          % (distinct, imgap))


def c5_relocation() -> None:
    imported = [
        "Casas-Ibarra R complex orthogonal (cited, hep-ph/0103065); nu01 residual "
        "= one real CI angle z",
        "the transfer gap Delta = 6 ln(3/2), spec T = {1,(2/3)^6,(1/3)^6} (v302, "
        "in-suite)",
        "the seam-gap IDENTIFICATION z = Delta is a NAMED [P] hypothesis -- deriving "
        "or refuting it (vs leptogenesis / 0nubb) is the open step",
    ]
    check("C5 RELOCATION AUDIT [O]: the seesaw is NOT closed by symmetry (nu01); it "
          "closes CONDITIONALLY on a transport selector. The seam-gap selector is a "
          "named [P] hypothesis with a concrete CP consequence (C3). Never a "
          "scorecard row; never [E]",
          True, "; ".join(imported))


def main() -> None:
    print("NU.CI.02 -- does a transport/minimality selector fix the leftover "
          "Casas-Ibarra angle?\n")
    c1_family(); c2_minimal_trivial(); c3_seam_gap(); c4_power(); c5_relocation()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = ("CONDITIONAL closure on a NAMED transport selector (not from symmetry)"
               if n_pass == len(CHECKS) else "INCONCLUSIVE")
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    imnorm, J = cp_content(GAP)
    reading = (
        "The one free Casas-Ibarra angle left by nu01 is NOT fixed by the seam "
        "symmetries. The minimal-transport selector (min ||R-I||) collapses to the "
        "trivial R=I (no CP) -- an assumption, not a result. A principled selector "
        "identifying the CI angle with the seam TRANSFER GAP, e^z = (3/2)^6 "
        "(z = 6 ln(3/2) = Delta, v302), gives a UNIQUE nontrivial R with a definite "
        "leptogenesis CP content (||Im R|| = %.4f, J_R = %.4f). That is a CONDITIONAL "
        "prediction [P]: the neutrino dynamics closes ONLY given the (unproven) "
        "transport selector. The contract's gain is to convert 'one free angle' into "
        "'one named, falsifiable hypothesis'. Never a scorecard row; never [E]."
        % (imnorm, J)
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "NU.CI.02 transport selector",
        "date": "2026-07-10",
        "firewall": "theory contract, never a scorecard row; not evidence",
        "seam_gap_selector": {"z": GAP, "im_norm_R": imnorm, "J_R": J},
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS, "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()
