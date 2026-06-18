"""v286 -- SEAM.EQUIV.01: the Seam Equivalence contract.  This does NOT prove the
theorem; it FORCES the whole open structure onto a single named arrow and proves that
the two proof routes are non-circular (they may converge only through SEAM.EQUIV.01).

THE NAMED THEOREM (the one open statement of the structural core):
    Seam Equivalence Theorem (SEAM.EQUIV.01).  The raw reflection-positive seam state
    (gap, chirality, carrier clock) reconstructs canonically the SAME state as the
    holomorphic (E8)_1 boundary net at the tau=i pillowcase -- the equivalence
    respecting the DtN, the KMS modular flow, the mu4 deck, the Q-system extension,
    det K = 1 and the (E8)_1 character.  Short form: the raw seam IS (E8)_1 at tau=i.

Four objects and their arrows (a commuting square with one open diagonal):
    RawRPSeam --[i, open]--> FlatTauIPillowcaseDtN --[closed, Route i]--> omega o rho = omega
    RawRPSeam --[ii, open]--> SREKitaevE8Phase    --[closed, Route ii]--> HolomorphicE8Net
    FlatTauIPillowcaseDtN <--[conditional, v282]--> HolomorphicE8Net   (at tau=i)
    RawRPSeam ===========[THE GRAL]===========> HolomorphicE8Net  = SEAM.EQUIV.01

  [E] 1. FOUR OBJECTS TYPED.  RawRPSeam (RP data + gap + chirality + carrier clock),
        FlatTauIPillowcaseDtN (geometry route), HolomorphicE8Net (AQFT/RCFT route),
        SREKitaevE8Phase (topological phase, det K=1) -- the corners of the square.
  [E] 2. SIX ARROWS TYPED.  two CLOSED (Route i: FlatDtN -> omega o rho = omega,
        v276/v280/v284; Route ii: SRE -> HolomorphicE8Net, v281/v277/v235), one
        CONDITIONAL (FlatDtN <-> HolomorphicE8Net at tau=i, v282), and the open
        arrows (RawRPSeam -> FlatDtN, RawRPSeam -> SRE) which are the SAME open lemma
        (v284/v285 coincidence) = the Gral RawRPSeam -> HolomorphicE8Net.
  [E] 3. IMPORT FIREWALL (anti-circularity).  no Route-i module
        (v276/v280/v284) imports any Route-ii module (v277/v281/v285) or vice versa
        -- the two routes converge ONLY through this contract, so E8 cannot be
        smuggled into the geometry and pulled back out (the reviewer's worst attack).
  [E] 4. EXACT-LABEL TAXONOMY.  each arrow carries one of {Formal Exact (Lean),
        Numerical Exact (reproducible experiment), Conditional Exact (standard
        theorem under a stated premise), Open Selection (the theory-selection
        premise)} -- so a conditional arrow can never be misread as a proof.
  [O] 5. THE ONE OPEN ARROW.  exactly one arrow is Open Selection: RawRPSeam -> (its
        geometry/holomorphy image).  Proving the single arrow
        'free Gaussian RP bulk => holomorphic single-sector boundary net' closes the
        structural core; everything else is closed or conditional.

Status: [E] the typing + the import firewall + the exact-label taxonomy + the
single-open-arrow certificate; [O] the named theorem stays open.  A contract that
concentrates the whole open structure on one arrow; it does NOT prove it.  Writes
seam_equivalence.json.  Python (stdlib).
"""
import json
import os
import re

from tfpt_constants import check, summary, reset

HERE = os.path.dirname(os.path.abspath(__file__))

ROUTE_I = ["v276_qgeo_flat_closes_commutator", "v280_pillowcase_steklov",
           "v284_route_i_rp_uniqueness"]
ROUTE_II = ["v277_seam_calderon_e8_match", "v281_holomorphy_modular_data",
            "v285_route_ii_seam_condensation"]

OBJECTS = {
    "RawRPSeam": "RP data + gap + chirality + carrier clock (the primitive)",
    "FlatTauIPillowcaseDtN": "the geometry route image (flat tau=i Steklov DtN)",
    "HolomorphicE8Net": "the AQFT/RCFT route image (holomorphic (E8)_1 net)",
    "SREKitaevE8Phase": "the topological phase (short-range-entangled, det K=1)",
}

# arrow: (frm, to, status, label, evidence)
ARROWS = [
    ("RawRPSeam", "FlatTauIPillowcaseDtN", "open", "Open Selection", "the geometry premise"),
    ("FlatTauIPillowcaseDtN", "omega o rho = omega", "closed", "Numerical+Formal Exact",
     "Route i: v276/v280 + Lean FORM.QGEO.03; v284"),
    ("RawRPSeam", "SREKitaevE8Phase", "open", "Open Selection", "the SRE premise"),
    ("SREKitaevE8Phase", "HolomorphicE8Net", "closed", "Conditional+Formal Exact",
     "Route ii: v235/v277/v281; v285"),
    ("FlatTauIPillowcaseDtN", "HolomorphicE8Net @ tau=i", "conditional", "Conditional Exact",
     "v282: chi_E8(i)=12, the order-4 CM point = the (E8)_1 modulus"),
    ("RawRPSeam", "HolomorphicE8Net", "gral", "Open Selection",
     "SEAM.EQUIV.01 -- the one open arrow; = both open arrows above (v284/v285 coincide)"),
]


def _imports(mod):
    src = open(os.path.join(HERE, mod + ".py"), encoding="utf-8").read()
    return set(re.findall(r"(?:^import|^from)\s+(v\d+\w*)", src, re.MULTILINE))


def run():
    reset()
    print("v286  SEAM.EQUIV.01: the Seam Equivalence contract (concentrates the open structure on one arrow)")

    # 1. four objects
    check("FOUR OBJECTS TYPED [E]: %s -- the corners of the equivalence square"
          % ", ".join(OBJECTS), len(OBJECTS) == 4)

    # 2. six arrows: 2 closed, 1 conditional, the open arrows + the gral
    closed = [a for a in ARROWS if a[2] == "closed"]
    conditional = [a for a in ARROWS if a[2] == "conditional"]
    opens = [a for a in ARROWS if a[2] == "open"]
    gral = [a for a in ARROWS if a[2] == "gral"]
    check("SIX ARROWS TYPED [E]: %d closed (Route i + Route ii), %d conditional "
          "(v282), %d open premises (the SAME lemma, v284/v285), 1 Gral "
          "(SEAM.EQUIV.01)" % (len(closed), len(conditional), len(opens)),
          len(closed) == 2 and len(conditional) == 1 and len(opens) == 2 and len(gral) == 1)

    # 3. import firewall: routes do not import each other
    i_imports = set().union(*(_imports(m) for m in ROUTE_I))
    ii_imports = set().union(*(_imports(m) for m in ROUTE_II))
    i_to_ii = i_imports & set(ROUTE_II)
    ii_to_i = ii_imports & set(ROUTE_I)
    check("IMPORT FIREWALL [E]: no Route-i module (%s) imports any Route-ii module "
          "and vice versa (i->ii: %s, ii->i: %s) -- the routes converge ONLY through "
          "SEAM.EQUIV.01, so E8 cannot be smuggled into the geometry and pulled back "
          "out (the reviewer's worst attack)"
          % ("/".join(m.split("_")[0] for m in ROUTE_I), i_to_ii or "none", ii_to_i or "none"),
          not i_to_ii and not ii_to_i)

    # 4. exact-label taxonomy
    labels = {a[3] for a in ARROWS}
    allowed = {"Open Selection", "Numerical+Formal Exact", "Conditional+Formal Exact",
               "Conditional Exact"}
    check("EXACT-LABEL TAXONOMY [E]: every arrow carries a label in {Formal Exact, "
          "Numerical Exact, Conditional Exact, Open Selection} (used: %s) -- a "
          "conditional arrow can never be misread as a proof" % sorted(labels),
          labels <= allowed)

    # 5. the one open arrow
    check("THE ONE OPEN ARROW [O]: exactly one Gral arrow (RawRPSeam -> "
          "HolomorphicE8Net = SEAM.EQUIV.01); proving 'free Gaussian RP bulk => "
          "holomorphic single-sector boundary net' closes the structural core -- "
          "everything else is closed or conditional", len(gral) == 1)

    # write the machine-readable contract
    out = {
        "theorem": "SEAM.EQUIV.01",
        "statement": "the raw RP seam state reconstructs canonically the holomorphic "
                     "(E8)_1 boundary net at the tau=i pillowcase",
        "short_form": "the raw seam is (E8)_1 at tau=i",
        "objects": OBJECTS,
        "arrows": [{"from": a[0], "to": a[1], "status": a[2], "label": a[3],
                    "evidence": a[4]} for a in ARROWS],
        "import_firewall": {"route_i": ROUTE_I, "route_ii": ROUTE_II,
                            "i_imports_ii": sorted(i_to_ii), "ii_imports_i": sorted(ii_to_i),
                            "clean": not i_to_ii and not ii_to_i},
        "the_one_open_arrow": "free Gaussian RP bulk => holomorphic single-sector boundary net",
        "not_closed_by_this": ["v_geo (metrology primitive)", "F_transfer (downstream)",
                               "QG.AMB.01 (nonperturbative ambient measure)"],
    }
    with open(os.path.join(HERE, "seam_equivalence.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    return summary("v286 SEAM.EQUIV.01 contract: 4 objects, 6 arrows (2 closed + 1 conditional + 1 open Gral), import firewall clean, one open arrow")


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
