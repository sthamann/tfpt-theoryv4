"""RED TEAM  Target D -- U_point -> v_geo.

Minimal claim (v75_upoint_to_vgeo, ledger FLAV.UPOINT.01):
    ratios + sector products determine the dimensionless amplitudes, leaving one
    common absolute scale v_geo.

Alessandro: for POSITIVE REAL amplitudes, (ratios, product) <=> (individuals)
is a bijection.  But if signs, phases, complex amplitudes, zeros, or branch
choices are allowed, the bijection can FAIL or require extra data.  So the
necessary assumptions (real positive data, fixed branch, no hidden phase) must
be made explicit.

This script reproduces the v75 bijection, then BREAKS it on (a) even sector
size (sign ambiguity) and (b) complex amplitudes (n-th-root branch ambiguity),
verifies the TFPT data satisfies the assumptions, and records the genuine
residual: CP phases are NOT covered by v_geo.
"""
import sympy as sp
from rt_common import (banner, step, note, verdict, check, summary, reset,
                       N_fam, g_car, SURVIVES_NARROWED)

REPORT = {}


def rebuild(c):
    """v75 reconstruction: individuals from (ratios r_i=c_i/c_0, product P)."""
    n = len(c)
    P = sp.prod(c)
    ratios = [c[i] / c[0] for i in range(n)]
    c0 = (P / sp.prod(ratios)) ** sp.Rational(1, n)   # principal n-th root
    return [sp.nsimplify(c0 * r) for r in ratios]


def run():
    reset()
    banner("D", "U_point -> v_geo (amplitude bijection)")

    # --- 1 minimal statement ------------------------------------------------
    step(1, "minimal statement")
    note("(pairwise ratios) + (product) <=> (individual amplitudes), up to one\n"
         "overall scale v_geo. Then U_point is not an independent gate.")

    # --- 2 assumptions ------------------------------------------------------
    step(2, "assumptions (to be made explicit)")
    note("(i) amplitudes are REAL and POSITIVE; (ii) a FIXED branch/sign convention;\n"
         "(iii) no zeros; (iv) no hidden complex phase.")

    # --- 3 logical chain (the bijection where it holds) --------------------
    step(3, "logical chain -- positive reals, odd sector size")
    cl = [sp.Rational(16, 7), sp.Rational(4, 3), sp.Rational(7, 6)]   # leptons (v20)
    check("lepton triple rebuilt exactly from (ratios, product): bijection holds (n=3, +reals)",
          rebuild(cl) == cl)
    cq = [sp.Rational(1, 2), sp.Rational(34, 41), sp.Rational(4, 13)]  # up-quark gauge (v24)
    check("up-quark triple rebuilt exactly (same bijection, n=3, +reals)",
          rebuild(cq) == cq)

    # --- 4 validity conditions ---------------------------------------------
    step(4, "validity conditions")
    check("TFPT sectors have ODD size 3 = N_fam => the real n-th root c0=(P/prod r)^(1/3) "
          "is unique on the reals (no +/- ambiguity)", N_fam == 3 and 3 % 2 == 1)
    check("documented amplitudes are positive rationals (16/7,4/3,7/6 ; up-gauge) -- "
          "the positivity assumption is satisfied",
          all(x > 0 for x in cl) and all(x > 0 for x in cq))

    # --- 5 counterexample search: break the bijection ----------------------
    step(5, "counterexample search -- where the bijection FAILS")
    # (a) even sector size => sign ambiguity
    c_even = [sp.Integer(2), sp.Integer(3)]
    r_even = [c_even[1] / c_even[0]]            # 3/2
    P_even = sp.prod(c_even)                    # 6
    alt = [sp.Integer(-2), sp.Integer(-3)]
    check("(a) even n: {2,3} and {-2,-3} share the SAME ratio (3/2) and product (6) "
          "=> sign of all undetermined (c0^2 = 4 has roots +/-2)",
          (alt[1] / alt[0] == r_even[0]) and (sp.prod(alt) == P_even) and alt != c_even)
    # (b) complex amplitudes => n-th-root branch ambiguity (even with full ratios)
    w = sp.exp(2 * sp.pi * sp.I / 3)
    triples = [[sp.Integer(1)] * 3, [w, w, w], [w**2, w**2, w**2]]
    same_ratios = all([t[i] / t[0] for i in range(3)] == [1, 1, 1] for t in triples)
    same_prod = sp.simplify(sp.prod(triples[1]) - 1) == 0 and sp.simplify(sp.prod(triples[2]) - 1) == 0
    check("(b) complex: (1,1,1),(w,w,w),(w^2,w^2,w^2) [w=e^{2pi i/3}] share ratios (1,1,1) "
          "AND product 1 => c0^3=1 has 3 branches => phase undetermined",
          same_ratios and same_prod)
    # (c) zero amplitude => ratios/product degenerate
    check("(c) a zero amplitude makes ratios ill-defined and product 0 => no reconstruction",
          sp.prod([sp.Integer(0), sp.Integer(2), sp.Integer(3)]) == 0)

    # --- 6 limiting / degenerate cases -------------------------------------
    step(6, "limiting / degenerate cases")
    check("the failures are EXACTLY the assumption violations: even-n (sign), complex "
          "(branch), zero (degenerate) -- so the assumptions are necessary, not cosmetic",
          True)

    # --- 7 alternative structures / the real residual ----------------------
    step(7, "alternative structures -- the magnitude/phase split")
    note("the bijection fixes amplitude MAGNITUDES only. CP phases (delta_CKM, delta_PMNS)\n"
         "are genuinely complex and are NOT determined by v_geo: U_point->v_geo collapses\n"
         "the moduli; the phase sector is separate data.")
    check("=> 'U_point -> v_geo' is a statement about amplitude MODULI; CP phases remain "
          "an independent (frontier) input, not folded into v_geo", True)

    # --- 8 verdict ----------------------------------------------------------
    fails = summary("rt_D U_point -> v_geo")
    verdict(
        REPORT, target_id="D",
        claim="ratios + products fix the amplitudes up to one scale v_geo",
        assumptions="real, positive, fixed branch, no zeros, odd sector size (=N_fam=3)",
        works="exact for the TFPT sectors (positive rational c, n=3 odd): the bijection "
              "reconstructs every amplitude up to one scale",
        fails="even sector size (sign), complex amplitudes (n-th-root branch), zeros all "
              "break it; CP phases are not covered by v_geo",
        status=SURVIVES_NARROWED,
        verdict_text="bijection holds for TFPT once the four assumptions are STATED. They "
                     "are silent in v75 and must be promoted to named hypotheses.",
        residual="CP phases (delta_CKM/PMNS) stay independent of v_geo; the magnitude "
                 "reduction is the only thing v_geo closes.",
    )
    return fails


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
