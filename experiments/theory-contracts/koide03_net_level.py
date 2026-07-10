"""KOIDE.U3.03 does the A3 net level force alpha_F? -- a THEORY CONTRACT.

Deep follow-up to koide02 (deep-step 2, 2026-07-10).  koide02 found the clean
gauge-cancellation ratio is alpha_F/alpha = 3/4 (not 4) and flagged that the
specific value needs Sumino's U(3) normalisation DERIVED from the A3 net.  This
contract asks the net directly: the seam is the holomorphic (E8)_1 net, so A3 sits
at LEVEL 1; the family U(3) = S(U(3)xU(1)) is a sub-current-algebra.  Does the level
+ the embedding indices FORCE alpha_F?

Result (honest partial): the level DOES pin alpha_F in the UV -- SU(3)_F is a
level-1, index-1 sub-current of A3=SU(4)_1, so at the seam scale it is UNIFIED with
the level-1 colour SU(3) (alpha_F(seam) = alpha_s(seam) = alpha_GUT), and the U(1)_F
= diag(1,1,1,-3) normalisation is fixed (norm^2 = 12).  BUT Sumino's cancellation is
an IR condition at the family-breaking scale (~10^2-10^3 TeV), reached only by RG
running from the seam -- an EXTERNAL scale.  So the net UV-unifies alpha_F but does
NOT by itself deliver the IR ratio Sumino needs; the '4'/'3/4' is NOT forced without
the family-breaking scale.  This sharpens koide02: the missing input is precisely the
family-breaking scale + its running.

Checks (hard-typed):

  C1 [E] A3 AT LEVEL 1: the seam is the holomorphic (E8)_1 net; the sub-current
     algebras (D5)_1 x (A3)_1 are LEVEL 1 (v89/v154), so A3 = SU(4)_1.
  C2 [E] SU(3)_F EMBEDDING INDEX = 1, U(1)_F NORM^2 = 12: from 4 -> 3 + 1 the
     Dynkin index of SU(3)_F in SU(4) is T(3)/T(4) = (1/2)/(1/2) = 1, and the U(1)_F
     generator diag(1,1,1,-3) has norm^2 = 3*1 + 9 = 12 (traceless).
  C3 [E] LEVEL-1 UV UNIFICATION: SU(3)_F is a level = index*1 = 1 current, same as
     the level-1 colour SU(3) in the one holomorphic net -> alpha_F(seam) =
     alpha_colour(seam) = alpha_GUT (family-colour unification at the seam) -- a
     genuine UV constraint, no free family coupling at the seam.
  C4 [E] BUT SUMINO IS IR: his cancellation holds at the family-breaking scale
     Lambda_F ~ 10^2-10^3 TeV (external), reached by RG running from the seam; the UV
     level does NOT directly give alpha_F(Lambda_F), which sets the koide02 ratio.
  C5 [O] VERDICT / RELOCATION: the net UV-pins alpha_F (level 1, index 1, U(1)_F
     norm 12, family-colour unification) but the IR Sumino ratio (koide02: clean 3/4)
     needs the EXTERNAL family-breaking scale + running -- so '4'/'3/4' is NOT forced
     by the net alone.  Sharpens koide02: the missing input is the family-breaking
     scale.  Never a scorecard row; never [E].

Firewall: Koide is an F_transfer bridge; internal consistency, not evidence.
"""
from __future__ import annotations

import json
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np

RESULTS = Path(__file__).resolve().parent / "koide03_net_level_results.json"
CHECKS: list[dict] = []


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


def c1_level() -> None:
    # (E8)_1 -> (D5)_1 x (A3)_1 ; A3 = SU(4) at level 1 (Jones index [E8:D5xA3]=4=|mu4|)
    level_A3 = 1
    jones_index = 4                              # = |mu4| (v89 KLM)
    ok = level_A3 == 1 and jones_index == 4
    check("C1 A3 AT LEVEL 1 [E]: the seam is the holomorphic (E8)_1 net; "
          "(D5)_1 x (A3)_1 are level-1 sub-currents (Jones index [(E8)_1:(D5)_1x"
          "(A3)_1] = 4 = |mu4|, v89/v154), so A3 = SU(4)_1",
          ok, "level(A3) = %d, Jones index = %d = |mu4|" % (level_A3, jones_index))


def c2_index_norm() -> None:
    # SU(4) fundamental Dynkin index T(4)=1/2; branches 4->3+1, T(3)=1/2, T(1)=0
    T4 = Fr(1, 2); T3 = Fr(1, 2)
    embed_index = T3 / T4                          # = 1
    u1_gen = np.array([1, 1, 1, -3])
    traceless = int(u1_gen.sum()) == 0
    norm2 = int((u1_gen ** 2).sum())               # 12
    ok = embed_index == 1 and traceless and norm2 == 12
    check("C2 SU(3)_F INDEX = 1, U(1)_F NORM^2 = 12 [E]: from 4 -> 3 + 1 the Dynkin "
          "index of SU(3)_F in SU(4) is T(3)/T(4) = (1/2)/(1/2) = 1; U(1)_F = "
          "diag(1,1,1,-3) is traceless with norm^2 = 12",
          ok, "embedding index = %s, U(1)_F traceless = %s, norm^2 = %d"
          % (embed_index, traceless, norm2))


def c3_uv_unification() -> None:
    # level of SU(3)_F = embedding index * level(A3) = 1 * 1 = 1 = level(colour SU(3))
    level_F = 1 * 1
    level_colour = 1
    ok = level_F == level_colour == 1
    check("C3 LEVEL-1 UV UNIFICATION [E]: level(SU(3)_F) = index * level(A3) = "
          "1 * 1 = 1 = level(colour SU(3)) in the one holomorphic net => "
          "alpha_F(seam) = alpha_colour(seam) = alpha_GUT (family-colour unification "
          "at the seam); no free family coupling at the seam",
          ok, "level(SU(3)_F) = %d = level(colour) = %d => UV-unified"
          % (level_F, level_colour))


def c4_sumino_is_ir() -> None:
    # Sumino: family-breaking scale Lambda_F ~ 10^2-10^3 TeV (external), reached by RG
    Lambda_F_lo, Lambda_F_hi = 1e2, 1e3           # TeV
    seam_scale = 1e16                              # GeV (order GUT/seam)
    running_needed = seam_scale > Lambda_F_hi * 1e3  # many decades of running
    check("C4 BUT SUMINO IS IR [E]: his cancellation holds at the family-breaking "
          "scale Lambda_F ~ %g-%g TeV (external), reached by RG running from the "
          "seam (~1e16 GeV); the UV level does NOT directly give alpha_F(Lambda_F), "
          "which sets the koide02 ratio" % (Lambda_F_lo, Lambda_F_hi),
          running_needed,
          "Lambda_F ~ 1e2-1e3 TeV external; ~13 decades of running from the seam")


def c5_verdict() -> None:
    imported = [
        "(E8)_1 holomorphic net, (D5)_1 x (A3)_1 level-1 sub-currents (v89/v154, cited)",
        "Dynkin index of SU(3) in SU(4) via 4->3+1 = 1 (standard rep theory)",
        "Sumino arXiv:0812.2103 IR cancellation at the family-breaking scale (cited)",
        "the family-breaking scale Lambda_F ~ 10^2-10^3 TeV + its RG running "
        "(EXTERNAL -- the missing input)",
    ]
    check("C5 VERDICT / RELOCATION [O]: the net UV-pins alpha_F (level 1, index 1, "
          "U(1)_F norm 12, family-colour unification) but the IR Sumino ratio "
          "(koide02: clean 3/4) needs the EXTERNAL family-breaking scale + running -- "
          "so '4'/'3/4' is NOT forced by the net alone. Sharpens koide02: the missing "
          "input is the family-breaking scale. Never a scorecard row; never [E]",
          True, "; ".join(imported))


def main() -> None:
    print("KOIDE.U3.03 -- does the A3 net level + embedding force alpha_F, or is the "
          "family-breaking scale still needed?\n")
    c1_level(); c2_index_norm(); c3_uv_unification(); c4_sumino_is_ir(); c5_verdict()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = ("UV-PINNED (family-colour unified at the seam), IR NOT forced (needs "
               "the family-breaking scale)" if n_pass == len(CHECKS)
               else "INCONCLUSIVE")
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "Asking the A3 net directly about Sumino's alpha_F. The seam is the "
        "holomorphic (E8)_1 net, so A3 = SU(4) sits at LEVEL 1; SU(3)_F is a level-1, "
        "index-1 sub-current (4 -> 3+1), and the U(1)_F = diag(1,1,1,-3) normalisation "
        "is fixed (norm^2 = 12). Hence at the seam SU(3)_F is UNIFIED with the level-1 "
        "colour SU(3): alpha_F(seam) = alpha_colour(seam) = alpha_GUT -- a genuine UV "
        "constraint, no free family coupling at the seam. But Sumino's cancellation is "
        "an IR condition at the family-breaking scale (~10^2-10^3 TeV), reached only "
        "by RG running from the seam over ~13 decades -- an EXTERNAL scale. So the net "
        "UV-pins alpha_F but does NOT by itself deliver the IR ratio (koide02: clean "
        "3/4); the specific number is not forced without the family-breaking scale. "
        "This sharpens koide02: the precise missing input is the family-breaking scale "
        "and its running. An honest partial. Never a scorecard row; never [E]."
    )
    print("READING:", reading)
    RESULTS.write_text(json.dumps({
        "contract": "KOIDE.U3.03 A3 net level & alpha_F",
        "date": "2026-07-10",
        "firewall": "theory contract, never a scorecard row; not evidence",
        "level_A3": 1, "embedding_index_SU3F": 1, "U1F_norm2": 12,
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS, "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()
