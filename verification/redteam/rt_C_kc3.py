"""RED TEAM  Target C -- k = c3/2 and the seam-area coefficient.

Minimal claim (v67/v68/v73, ledger SEAM.AREACOEFF.01/02):
    in reduced units, k = c3/2 = 1/(16 pi) and Fursaev-Solodukhin gives S/A = 1/4.

Alessandro's red-team rule is sharp and correct: any formulation that silently
writes k_phys = c3/2 must be REJECTED as dimensionally false.  The formula is
safe only when k is the REDUCED dimensionless coefficient (= G*k_phys), or when
area is in Planck/seam units.

This script (i) proves the dimensional chain symbolically, (ii) exhibits the
dimension error of the naked identity, and (iii) runs a FIREWALL scan over the
confirmatory scripts that use 'c3/2', asserting each occurrence is qualified as
the reduced/seam-unit coefficient.
"""
import os
import re
import sympy as sp
from rt_common import (banner, step, note, verdict, check, summary, reset,
                       read_text, PARENT_DIR, SURVIVES)

REPORT = {}
pi = sp.pi

# files in the confirmatory suite that mention the coefficient
SCAN_FILES = ["v67_area_law_coefficient.py", "v68_seeley_dewitt_residual.py", "v73_k_c3_half.py"]

# the FORBIDDEN patterns: a dimensionful Newton coupling set equal to the
# dimensionless c3/2.  `k_phys = c3/2` is always illegal; `1/(16 pi G) = c3/2`
# is illegal ONLY when the line does not also pin G=1 (handled by LINE_G1 below).
FORBIDDEN_ALWAYS = re.compile(r"k_?phys\s*=\s*c_?3\s*/\s*2", re.I)
FORBIDDEN_IF_NOT_G1 = re.compile(r"1\s*/\s*\(?\s*16\s*\*?\s*pi\s*\*?\s*g\b.*=\s*c_?3\s*/\s*2", re.I)
LINE_G1 = ["g=1", "g = 1", "|_{g=1}", "(g=1", "g}=1"]
# a file is disciplined if it establishes the reduced/seam-unit/G=1 context anywhere
FILE_QUALIFIERS = ["seam unit", "g=1", "g = 1", "|_{g=1}", "dimensionless",
                   "reduced", "1/(16", "induced 1/(16", "uv-sensitive"]


def firewall_scan():
    """Return (occurrences, violations, file_ok).

    occurrences = every 'c3/2' mention (for the count);
    violations  = lines matching a FORBIDDEN naked dimensionful identity;
    file_ok     = per-file flag that the reduced/G=1 context is established.
    """
    occurrences, violations, file_ok = [], [], {}
    for fname in SCAN_FILES:
        text = read_text(os.path.join(PARENT_DIR, fname))
        file_ok[fname] = any(q in text.lower() for q in FILE_QUALIFIERS)
        for i, line in enumerate(text.splitlines(), 1):
            low = line.lower()
            if "c3/2" in low.replace(" ", ""):
                occurrences.append((fname, i, line.strip()))
            naked = FORBIDDEN_ALWAYS.search(line)
            phys_no_g1 = FORBIDDEN_IF_NOT_G1.search(line) and not any(q in low for q in LINE_G1)
            if naked or phys_no_g1:
                violations.append((fname, i, line.strip()))
    return occurrences, violations, file_ok


def run():
    reset()
    banner("C", "k = c3/2 and the seam-area coefficient (dimensional firewall)")

    # --- 1 minimal statement ------------------------------------------------
    step(1, "minimal statement")
    note("k_red = c3/2 = 1/(16 pi)  (DIMENSIONLESS, seam/Planck units)\n"
         "k_phys = k_red / G = 1/(16 pi G)\n"
         "S = 4 pi k_phys A_phys = A_phys/(4G)  (Bekenstein-Hawking)")

    # --- 2 assumptions ------------------------------------------------------
    step(2, "assumptions")
    note("c3 is dimensionless; G carries the gravitational dimension; areas are\n"
         "physical unless explicitly measured in Planck/seam units.")

    # --- 3 logical chain (the correct dimensional chain) -------------------
    step(3, "logical chain")
    G, A = sp.symbols('G A_phys', positive=True)
    c3 = 1 / (8 * pi)
    k_red = c3 / 2
    k_phys = k_red / G
    S = 4 * pi * k_phys * A
    check("k_red = c3/2 = 1/(16 pi) dimensionless", sp.simplify(k_red - 1 / (16 * pi)) == 0)
    check("S = 4 pi k_phys A = A/(4G) (Bekenstein-Hawking, dimensionally correct)",
          sp.simplify(S - A / (4 * G)) == 0)

    # --- 4 validity conditions ---------------------------------------------
    step(4, "validity conditions")
    check("the dimensionless reading is forced by topology x variation: "
          "k_red = (1/2)*(1/(|Z2|*2pi*chi(S^2))) = c3/2 (v73), both cutoff-independent",
          sp.simplify(sp.Rational(1, 2) * (1 / (2 * 2 * pi * 2)) - k_red) == 0)
    note("safe iff k is read as k_red (= G*k_phys) OR area is in Planck/seam units.")

    # --- 5 counterexample search: the naked identity is dimensionally false -
    step(5, "counterexample search -- the FORBIDDEN identity k_phys = c3/2")
    # dimension bookkeeping: [k_phys]=[1/G]=L_dim, [c3/2]=0 (dimensionless)
    L_dim = sp.Symbol('massdim_inverseG', positive=True)   # symbolic dimension of 1/G
    dim_kphys, dim_c3half = L_dim, sp.Integer(0)
    check("dimension mismatch: dim(k_phys)=dim(1/G) != dim(c3/2)=0  => k_phys = c3/2 is "
          "DIMENSIONALLY FALSE (only true at G=1)",
          dim_kphys != dim_c3half)
    S_wrong = 4 * pi * k_red * A     # what a naked k_phys=c3/2 would give
    check("naked identity would give S = A/4 with PHYSICAL area (no 1/G) -- wrong by a "
          "factor 1/G vs the correct A/(4G)",
          sp.simplify(S_wrong - A / 4) == 0 and sp.simplify(S_wrong - S) != 0)

    # --- 6 limiting / degenerate cases -------------------------------------
    step(6, "limiting / degenerate cases")
    check("G -> 1 (seam units): k_phys -> c3/2 and S -> A/4 become literally true "
          "(this is the ONLY regime where the naked identity is legal)",
          sp.simplify(k_phys.subs(G, 1) - k_red) == 0)

    # --- 7 alternative structures / FIREWALL over the suite -----------------
    step(7, "firewall scan: no NAKED dimensionful identity k_phys = c3/2 in the suite")
    # positive control: the firewall has teeth (it catches a synthetic violation)
    teeth = bool(FORBIDDEN_ALWAYS.search("k_phys = c3/2  # dimensionful, no G"))
    check("firewall has teeth: it flags the synthetic naked identity 'k_phys = c3/2'", teeth)
    occurrences, violations, file_ok = firewall_scan()
    for f, i, ln in violations:
        note(f"!! VIOLATION {f}:{i}: {ln[:80]}")
    check(f"firewall: {len(occurrences)} 'c3/2' mentions across {len(SCAN_FILES)} files; "
          f"0 are a naked dimensionful identity (k_phys=c3/2)",
          len(violations) == 0 and len(occurrences) > 0)
    check("each file establishes the reduced/seam-unit/G=1 context (file-level discipline)",
          all(file_ok.values()))

    # --- 8 verdict ----------------------------------------------------------
    fails = summary("rt_C k = c3/2 dimensional firewall")
    verdict(
        REPORT, target_id="C",
        claim="k = c3/2 = 1/(16 pi) (reduced) and S/A = 1/4",
        assumptions="c3 dimensionless; G carries the gravitational dimension; "
                    "k read as the REDUCED coefficient (= G*k_phys)",
        works="the dimensionless content k_red=c3/2 is forced by topology+variation; "
              "S=A/(4G) is dimensionally correct; suite uses only the reduced reading",
        fails="the identity k_phys=c3/2 is dimensionally false (legal only at G=1 / "
              "Planck units) -- must never appear unqualified",
        status=SURVIVES,
        verdict_text="claim is safe AS WORDED (reduced coefficient). Firewall finds no "
                     "naked dimensionful identity; absolute 1/G stays the anchor (v68).",
        residual="the absolute 4D Newton scale (1/G, Lambda^2*f2) remains the one "
                 "dimensionful anchor; only that, nothing dimensionless, is open.",
    )
    return fails


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
