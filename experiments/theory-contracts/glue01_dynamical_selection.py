"""GLUE.DYN.01 dynamical glue selection -- a THEORY CONTRACT (never a
scorecard row).

Question (2026-07-10, Zuse/"Rechnender Raum" round): the network chain
v298 -> v299 -> v327 -> v395 reaches E8 as a STAR T(2,3,5) -- the last
finite point of a local growth rule.  The compiler closure, however, is a
DECOMPOSITION: D5 (+) A3 glued by mu4.  Its uniqueness is so far STATIC
(v15: discriminant classification under the familyful filter; v1: lattice
certificate).  This contract builds the missing dynamical layer: a pipeline
of LOCAL / SPECTRAL gates on the attractor graph (affine E8-hat, the
endpoint of v299's growth) that selects the D5 (+) A3 + mu4 split among all
single-node punctures -- with honest controls showing what the gates do NOT
do.

Substrate fact (Borel-de Siebenthal, cited external theorem; machine-
recomputed here at graph level): deleting one node from the affine diagram
E8-hat yields exactly the maximal-rank semisimple subalgebras of E8, and the
glue index of the remaining root lattices inside E8 equals the KAC MARK of
the deleted node.  The Kac marks are the PERRON / ATTRACTOR data of the
minimal local diffusion (v298), so the menu of punctures AND their glue
orders is dynamical output, not input.

Gates (each a property of the post-puncture graph / dynamics):

  (i)   TWO-SIDED.   The puncture leaves exactly TWO components (the seam
        has |Z2| = 2 sides; the Z2 atom is the imported input of this gate).
  (ii)  SEAM-PAIRING.  The two discriminant groups are isomorphic AND
        cyclic: the glue is the graph of an anti-isometry through ONE cyclic
        clock -- no one-sided glue vector, every glue class touches BOTH
        factors.
  (iii) SPECTRAL OCTAVE.  The two components' Perron eigenvalues
        rho = 2 cos(pi/h) satisfy h_2 = |Z2| * h_1 -- measurable by running
        the SAME lazy local diffusion m <- (A+2I)/4 m on each side.

Checks (hard-typed):

  C1 [E] MARKS = PERRON: the Kac marks of E6-hat, E7-hat, E8-hat satisfy
     A*m = 2*m exactly (integer arithmetic) -- the deletion menu lives on
     the v298 attractor.
  C2 [E] DELETION TABLE: all single-node deletions of E8-hat reproduce the
     classical Borel-de Siebenthal list, and for EVERY deletion (all three
     diagrams) the glue index sqrt(prod det / det_ambient) is an integer
     equal to the deleted Kac mark.
  C3 [E] TWO-SIDED GATE: exactly five E8-hat punctures are two-sided
     (marks 2,3,4,5,4); one- and three-component punctures excluded.
  C4 [E] SEAM-PAIRING GATE: survivors {A1+E7, A2+E6, A3+D5, A4+A4} = the
     v15 candidate list, RECOMPUTED from the deletion menu; A1+A7 is
     rejected (disc Z2 vs Z8) although its glue index is also 4 -- the
     pairing gate is finer than the index.
  C5 [E] SPECTRAL OCTAVE GATE (measured): per-component Perron values from
     the lazy diffusion reproduce 2 cos(pi/h); the h-ratios over the five
     two-sided punctures are (9,4,2,4,1) -- ratio |Z2| = 2 is UNIQUE at
     A3+D5.
  C6 [E]/[C] INTERSECTION + EMERGENCE: gates (ii) and (iii) independently
     point to the SAME unique puncture; deleted mark 4 => glue = Z4 = mu4
     EMERGES (= h(A3)), h(D5) = 8 = 2|mu4| = rank(E8) (the P1 rank readout,
     COMP.01), ranks (3,5) = (N_fam, g_car), q(A3)+q(D5) = 2 (even glue,
     v1).
  C7 [E] LOOK-ELSEWHERE CONTROLS: on E7-hat the octave gate ALONE fires
     (A2+A5, h = (3,6)) but seam-pairing rejects it (disc 3 vs 6) -- the
     gates are independent and their agreement is E8-specific; on E6-hat
     both gates are empty.
  C8 [O] RELOCATION AUDIT (honest): what stays imported -- the single-node
     puncture, the Z2 two-sidedness, the octave condition itself (post-hoc
     selector until derived; audit-level, same discipline as flav01 C6),
     and Borel-de Siebenthal as cited machinery.  v15 stays the static
     theorem; P2 is NOT closed (the E8-hat substrate is v299's seed-
     dependent growth endpoint).

Firewall: pure graph / lattice arithmetic; belongs in theory-contracts,
never in evidence_scorecard.json; passing is internal consistency, not
evidence, and never [E]-as-physics for the octave reading.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

RESULTS = Path(__file__).resolve().parent / "glue01_dynamical_results.json"

CHECKS: list[dict] = []


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       {detail}")


# ---------------------------------------------------------------------------
# affine diagrams (node 0.. ; Kac marks; ambient root-lattice determinant)
# ---------------------------------------------------------------------------
AFFINE = {
    "E8^": dict(
        edges=[(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)],
        marks=[1, 2, 3, 4, 5, 6, 4, 2, 3],
        det_ambient=1,
    ),
    "E7^": dict(
        edges=[(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 7)],
        marks=[1, 2, 3, 4, 3, 2, 1, 2],
        det_ambient=2,
    ),
    "E6^": dict(
        edges=[(0, 1), (1, 2), (0, 3), (3, 4), (0, 5), (5, 6)],
        marks=[3, 2, 1, 2, 1, 2, 1],
        det_ambient=3,
    ),
}

Z2 = 2  # the two-sidedness atom |Z2|


def adjacency(edges: list, n: int) -> np.ndarray:
    A = np.zeros((n, n), int)
    for a, b in edges:
        A[a, b] = A[b, a] = 1
    return A


def components_after(edges: list, n: int, removed: int):
    """Connected components (+ restricted adjacency lists) after one deletion."""
    adj = {v: [] for v in range(n) if v != removed}
    for a, b in edges:
        if a != removed and b != removed:
            adj[a].append(b)
            adj[b].append(a)
    seen: set = set()
    comps = []
    for v in adj:
        if v in seen:
            continue
        stack, comp = [v], []
        seen.add(v)
        while stack:
            u = stack.pop()
            comp.append(u)
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        comps.append(sorted(comp))
    return comps, adj


def ade_type(comp: list, adj: dict):
    """Recognise a tree component as A_n / D_n / E_n from its leg structure."""
    n = len(comp)
    if any(len(adj[v]) > 3 for v in comp):
        return None
    deg3 = [v for v in comp if len(adj[v]) == 3]
    if not deg3:
        return ("A", n)
    if len(deg3) != 1:
        return None
    c = deg3[0]
    legs = []
    for w in adj[c]:
        length, prev, cur = 1, c, w
        while True:
            nxt = [x for x in adj[cur] if x != prev]
            if not nxt:
                break
            if len(nxt) > 1:
                return None
            prev, cur = cur, nxt[0]
            length += 1
        legs.append(length)
    p, q, r = sorted(legs)
    if (p, q) == (1, 1):
        return ("D", 3 + r)
    if (p, q, r) == (1, 2, 2):
        return ("E", 6)
    if (p, q, r) == (1, 2, 3):
        return ("E", 7)
    if (p, q, r) == (1, 2, 4):
        return ("E", 8)
    return None


def type_data(t) -> dict:
    """(family, n) -> name, disc-group order, cyclicity, Coxeter number, rank."""
    fam, n = t
    if fam == "A":
        return dict(name=f"A{n}", det=n + 1, cyclic=True, h=n + 1, rank=n)
    if fam == "D":
        return dict(name=f"D{n}", det=4, cyclic=(n % 2 == 1), h=2 * n - 2, rank=n)
    return {
        6: dict(name="E6", det=3, cyclic=True, h=12, rank=6),
        7: dict(name="E7", det=2, cyclic=True, h=18, rank=7),
        8: dict(name="E8", det=1, cyclic=True, h=30, rank=8),
    }[n]


def measured_rho(comp: list, adj: dict, iters: int = 6000, seed: int = 0) -> float:
    """Perron eigenvalue of the component adjacency, MEASURED by running the
    v298 lazy local diffusion m <- (A+2I)/4 m (rho_A = 4 lambda_lazy - 2)."""
    idx = {v: i for i, v in enumerate(comp)}
    n = len(comp)
    A = np.zeros((n, n))
    for v in comp:
        for w in adj[v]:
            A[idx[v], idx[w]] = 1.0
    M = (A + 2 * np.eye(n)) / 4
    rng = np.random.default_rng(seed)
    m = rng.random(n) + 0.1
    for _ in range(iters):
        m = M @ m
        m /= np.linalg.norm(m)
    lam = float(m @ (M @ m))
    return 4 * lam - 2


def deletion_table(dg_name: str) -> list:
    """All single-node deletions of one affine diagram, fully analysed."""
    dg = AFFINE[dg_name]
    n = len(dg["marks"])
    rows = []
    for v in range(n):
        comps, adj = components_after(dg["edges"], n, v)
        types = [ade_type(c, adj) for c in comps]
        if any(t is None for t in types):
            raise RuntimeError(f"{dg_name}: unrecognised component at deletion {v}")
        data = [type_data(t) for t in types]
        det_prod = math.prod(d["det"] for d in data)
        idx2, det_amb = det_prod, dg["det_ambient"]
        assert idx2 % det_amb == 0
        glue_index = math.isqrt(idx2 // det_amb)
        rows.append(dict(
            deleted=v,
            mark=dg["marks"][v],
            names=sorted(d["name"] for d in data),
            n_comp=len(comps),
            dets=sorted(d["det"] for d in data),
            cyclic=[d["cyclic"] for d in data],
            hs=sorted(d["h"] for d in data),
            ranks=sorted(d["rank"] for d in data),
            glue_index_sq_ok=(glue_index * glue_index * det_amb == det_prod),
            glue_index=glue_index,
            comps=comps,
            adj=adj,
        ))
    return rows


def two_sided(rows: list) -> list:
    return [r for r in rows if r["n_comp"] == 2]


def pairing_ok(r: dict) -> bool:
    return (r["n_comp"] == 2 and r["dets"][0] == r["dets"][1]
            and all(r["cyclic"]))


def octave_ok(r: dict) -> bool:
    return r["n_comp"] == 2 and r["hs"][1] == Z2 * r["hs"][0]


# ---------------------------------------------------------------------------
def c1_marks_perron() -> None:
    ok, details = True, []
    for name, dg in AFFINE.items():
        A = adjacency(dg["edges"], len(dg["marks"]))
        m = np.array(dg["marks"], int)
        exact = bool(np.array_equal(A @ m, 2 * m))
        ok &= exact
        details.append(f"{name}: A*m == 2m {exact} (sum marks = {int(m.sum())} = h)")
    check("C1 MARKS = PERRON [E]: the Kac marks of E6^/E7^/E8^ satisfy "
          "A*m = 2*m exactly -- the deletion menu lives on the v298 attractor "
          "(marks = the dynamical fixed point of the lazy local diffusion)",
          ok, "; ".join(details))


def c2_deletion_table(tables: dict) -> None:
    expected_e8 = {
        0: ["E8"], 1: ["A1", "E7"], 2: ["A2", "E6"], 3: ["A3", "D5"],
        4: ["A4", "A4"], 5: ["A1", "A2", "A5"], 6: ["A1", "A7"],
        7: ["D8"], 8: ["A8"],
    }
    table_ok = all(tables["E8^"][v]["names"] == expected_e8[v]
                   for v in expected_e8)
    mark_ok = all(r["glue_index_sq_ok"] and r["glue_index"] == r["mark"]
                  for rows in tables.values() for r in rows)
    listing = "; ".join(
        f"del {r['deleted']}(m={r['mark']})->{'+'.join(r['names'])}"
        for r in tables["E8^"])
    check("C2 DELETION TABLE [E]: E8^ single-node deletions = the classical "
          "Borel-de Siebenthal list, and for EVERY deletion of E6^/E7^/E8^ "
          "the glue index sqrt(prod det / det_ambient) is an integer EQUAL to "
          "the deleted Kac mark -- the glue order is attractor data",
          table_ok and mark_ok, listing)


def c3_two_sided(tables: dict) -> list:
    rows = tables["E8^"]
    ts = two_sided(rows)
    marks = sorted(r["mark"] for r in ts)
    excluded = [f"del {r['deleted']}({'+'.join(r['names'])}: {r['n_comp']} comp)"
                for r in rows if r["n_comp"] != 2]
    check("C3 TWO-SIDED GATE [E]: exactly five E8^ punctures leave two sides "
          "(marks 2,3,4,5,4 -> A1+E7, A2+E6, A3+D5, A4+A4, A1+A7); one- and "
          "three-component punctures excluded (|Z2| = 2 sides of the seam)",
          len(ts) == 5 and marks == [2, 3, 4, 4, 5],
          "excluded: " + "; ".join(excluded))
    return ts


def c4_pairing(ts: list) -> list:
    surv = [r for r in ts if pairing_ok(r)]
    names = sorted("+".join(r["names"]) for r in surv)
    a1a7 = next(r for r in ts if r["names"] == ["A1", "A7"])
    check("C4 SEAM-PAIRING GATE [E]: isomorphic + cyclic discriminant groups "
          "-> survivors {A1+E7, A2+E6, A3+D5, A4+A4} = the v15 candidate "
          "list, recomputed from the deletion menu; A1+A7 REJECTED (disc Z2 "
          "vs Z8) although its glue index is also 4 -- the pairing gate is "
          "finer than the index",
          names == ["A1+E7", "A2+E6", "A3+D5", "A4+A4"]
          and not pairing_ok(a1a7) and a1a7["glue_index"] == 4,
          f"survivors {names}; A1+A7 dets {a1a7['dets']} (glue index "
          f"{a1a7['glue_index']})")
    return surv


def c5_octave(ts: list) -> list:
    max_err, ratios = 0.0, {}
    for r in ts:
        for comp in r["comps"]:
            rho = measured_rho(comp, r["adj"])
            t = ade_type(comp, r["adj"])
            h = type_data(t)["h"]
            max_err = max(max_err, abs(rho - 2 * math.cos(math.pi / h)))
        ratios["+".join(r["names"])] = (r["hs"][1] / r["hs"][0])
    surv = [r for r in ts if octave_ok(r)]
    check("C5 SPECTRAL OCTAVE GATE [E]: per-component Perron values MEASURED "
          "by the lazy diffusion reproduce 2cos(pi/h) (max err %.1e); the "
          "h-ratios over the five two-sided punctures are (9,4,2,4,1) -- "
          "ratio |Z2| = 2 is UNIQUE at A3+D5" % max_err,
          max_err < 1e-7 and len(surv) == 1 and surv[0]["names"] == ["A3", "D5"],
          "ratios " + ", ".join(f"{k}: {v:g}" for k, v in ratios.items()))
    return surv


def c6_intersection(pair_surv: list, oct_surv: list) -> None:
    inter = [r for r in pair_surv if octave_ok(r)]
    r = inter[0] if inter else None
    qa3, qd5 = 3.0 / 4, 5.0 / 4
    emergent = (r is not None and r["names"] == ["A3", "D5"]
                and r["mark"] == 4 and r["glue_index"] == 4
                and r["hs"] == [4, 8] and r["ranks"] == [3, 5]
                and qa3 + qd5 == 2.0 and 16 * qa3 * qd5 == 15.0)
    check("C6 INTERSECTION + EMERGENCE [E]/[C]: gates (ii) and (iii) "
          "independently select the SAME unique puncture A3+D5; deleted mark "
          "4 => glue = Z4 = mu4 EMERGES (= h(A3) = 4 = |mu4|), h(D5) = 8 = "
          "2|mu4| = rank(E8) (the P1 rank readout, COMP.01), ranks (3,5) = "
          "(N_fam, g_car), q(A3)+q(D5) = 3/4+5/4 = 2 (even glue, v1), "
          "16 q q = 15 = dim S+ - 1",
          emergent,
          f"unique survivor {'+'.join(r['names']) if r else 'NONE'}, deleted "
          f"mark {r['mark'] if r else '-'}, h pair {r['hs'] if r else '-'}, "
          f"ranks {r['ranks'] if r else '-'}")


def c7_controls(tables: dict) -> None:
    res = {}
    for name in ("E7^", "E6^"):
        ts = two_sided(tables[name])
        pair = ["+".join(r["names"]) for r in ts if pairing_ok(r)]
        octv = ["+".join(r["names"]) for r in ts if octave_ok(r)]
        both = ["+".join(r["names"]) for r in ts
                if pairing_ok(r) and octave_ok(r)]
        res[name] = (pair, octv, both)
    e7_pair, e7_oct, e7_both = res["E7^"]
    e6_pair, e6_oct, e6_both = res["E6^"]
    ok = (e7_pair == [] and set(e7_oct) == {"A2+A5"} and e7_both == []
          and e6_pair == [] and e6_oct == [] and e6_both == [])
    check("C7 LOOK-ELSEWHERE CONTROLS [E]: on E7^ the octave gate ALONE "
          "fires (A2+A5, h = (3,6)) but seam-pairing rejects it (disc Z3 vs "
          "Z6) -- the gates are INDEPENDENT and their agreement is "
          "E8-specific; on E6^ both gates are empty",
          ok,
          f"E7^: pairing {e7_pair}, octave {e7_oct}, both {e7_both}; "
          f"E6^: pairing {e6_pair}, octave {e6_oct}, both {e6_both}")


def c8_relocation() -> None:
    imported = [
        "the single-node puncture (one deletion; why one is not derived)",
        "two-sidedness = the Z2 atom (gate i)",
        "the octave condition h2 = |Z2| h1 itself (POST-HOC selector until "
        "derived; audit-level, same discipline as flav01 C6 -- its resonances "
        "with the c=8->16 octave / half-spinor 2^4 are [C] readings only)",
        "Borel-de Siebenthal deletions <-> maximal-rank subalgebras (cited "
        "external theorem; recomputed here at graph level)",
        "v15 stays the static theorem; P2 is NOT closed (E8^ itself is "
        "v299's seed-dependent growth endpoint)",
    ]
    check("C8 RELOCATION AUDIT [O]: the pipeline REPLACES v15's familyful "
          "filter (imports dim S+ = 16, N_fam = 3) by two structural gates "
          "importing only the Z2 atom -- but the octave selector is new and "
          "post-hoc; recorded honestly",
          True, "; ".join(imported))


def main() -> None:
    print("GLUE.DYN.01 dynamical glue selection -- local gates on the "
          "attractor graph select D5 (+) A3 + mu4\n")
    tables = {name: deletion_table(name) for name in AFFINE}
    c1_marks_perron()
    c2_deletion_table(tables)
    ts = c3_two_sided(tables)
    pair_surv = c4_pairing(ts)
    oct_surv = c5_octave(ts)
    c6_intersection(pair_surv, oct_surv)
    c7_controls(tables)
    c8_relocation()
    n_pass = sum(c["pass"] for c in CHECKS)
    verdict = "CONTRACT HOLDS" if n_pass == len(CHECKS) else "CONTRACT FAILS"
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)} checks pass")
    reading = (
        "The static v15 uniqueness acquires a dynamical formulation: on the "
        "attractor graph E8-hat (whose Kac marks are the fixed point of the "
        "v298 local diffusion), single-node punctures form a Borel-de "
        "Siebenthal menu in which the glue order IS the deleted mark. Two "
        "independent local gates -- seam-pairing (isomorphic cyclic "
        "discriminants) and the spectral octave h2 = |Z2| h1, the latter "
        "measurable by running the same local diffusion on each side -- "
        "select the SAME unique puncture, A3+D5 at mark 4, so mu4 = Z4 = "
        "deleted mark = h(A3) comes OUT of the selection, and (N_fam, g_car) "
        "= (3,5) are the component ranks. The E7-hat control shows the gates "
        "are independent (octave alone fires on A2+A5; pairing kills it); on "
        "E6-hat both are empty. What is NOT claimed: a derivation of the "
        "octave condition (post-hoc until derived), of the single puncture, "
        "or of P2 -- the substrate remains v299's seed-dependent endpoint."
    )
    print("READING:", reading)
    slim_tables = {
        name: [{k: r[k] for k in ("deleted", "mark", "names", "n_comp",
                                  "dets", "hs", "ranks", "glue_index")}
               for r in rows]
        for name, rows in tables.items()
    }
    RESULTS.write_text(json.dumps({
        "contract": "GLUE.DYN.01 dynamical glue selection",
        "date": "2026-07-10",
        "firewall": ("theory contract, never a scorecard row; internal "
                     "consistency, not evidence; octave selector audit-level"),
        "verdict": f"{verdict} ({n_pass}/{len(CHECKS)})",
        "checks": CHECKS,
        "deletion_tables": slim_tables,
        "reading": reading,
    }, indent=2) + "\n")
    print(f"\nresults -> {RESULTS.name}")


if __name__ == "__main__":
    main()
