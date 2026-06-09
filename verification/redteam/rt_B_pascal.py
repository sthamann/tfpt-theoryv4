"""RED TEAM  Target B -- Theorem A / carrier-rank uniqueness.

Minimal formal claim (Lean carrier_rank_pascal_unique, ledger FORM.CAR.01):
    2^g = g^2 + g + 2  has the unique natural-number solution g = 5.

That arithmetic is Lean-verified, so it is NOT attacked here.  Following
Alessandro, the attack is on the UPSTREAM physical assumption:

    why must the physical carrier satisfy exactly this Pascal condition
        2^(g-1) = C(g,0) + C(g,1) + C(g,2)   (half-spinor exhaustion) ?

The stress test scans nearby admissible rules (shifted constant, different
truncation degree, signed variants) and asks whether g=5 is physically forced
by the boundary/seam principle, or merely selected because it yields g=5.

FOLLOW-UP (../v83_e8net_holomorphic_uniqueness.py, ledger CAR.PASCAL.01): this residual is now
REDUCED -- the truncation degree is NOT free: K=(g-1)/2 is the Pascal-row midpoint
sum_{k<=(g-1)/2} C(g,k)=2^(g-1) (odd g) = the half-spinor split, i.e. the carrier is the even
Clifford half-spinor Lambda^even(C^5)=1+10+5=16.  So the residual reduces to the single standard
input "carrier = half-spinor of Spin(10)"; the Lean arithmetic core stays [F].  The scan below
stands unchanged.

Adversarial finding: the truncation DEGREE is the load-bearing physical choice
(it sets g = 2*degree + 1), so the Pascal rule -- not the arithmetic -- carries
the selection, and it must be typed as a physical postulate, not [I].
"""
from math import comb
from rt_common import (banner, step, note, verdict, check, summary, reset,
                       g_car, N_fam, dim_Splus, SURVIVES_NARROWED)

REPORT = {}
GMAX = 60   # search horizon for solutions


def solutions_const(c):
    """g with 2^g = g^2 + g + c (division-free Pascal family, constant c)."""
    return [g for g in range(0, GMAX) if 2**g == g * g + g + c]


def solutions_trunc(K):
    """g with 2^(g-1) = sum_{k=0}^K C(g,k) (truncation degree K)."""
    return [g for g in range(1, GMAX) if 2**(g - 1) == sum(comb(g, k) for k in range(K + 1))]


def run():
    reset()
    banner("B", "carrier-rank / Pascal condition (upstream physical premise)")

    # --- 1 minimal statement ------------------------------------------------
    step(1, "minimal statement")
    note("formal: 2^g = g^2+g+2 <=> g=5 (Lean-verified, NOT attacked).\n"
         "physical premise under attack: the carrier obeys the Pascal half-spinor\n"
         "exhaustion 2^(g-1) = C(g,0)+C(g,1)+C(g,2).")

    # --- 2 assumptions ------------------------------------------------------
    step(2, "assumptions")
    note("(i) a generation fills the EVEN exterior algebra of the carrier;\n"
         "(ii) the exterior sum is TRUNCATED at degree 2;\n"
         "(iii) the count equals the half-spinor dimension 2^(g-1).")

    # --- 3 logical chain (restate the verified core) -----------------------
    step(3, "logical chain (verified arithmetic core)")
    check("Lean core restated: g=5 is the UNIQUE solution of 2^g=g^2+g+2",
          solutions_const(2) == [5])
    check("equivalently 2^(g-1)=C(g,0)+C(g,1)+C(g,2) has unique solution g=5 "
          "(Pascal row (1,5,10), sum 16 = dim S+)",
          solutions_trunc(2) == [5] and 1 + 5 + 10 == dim_Splus)

    # --- 4 validity conditions ---------------------------------------------
    step(4, "validity conditions")
    check("the rule is exact-integer (no rounding); both forms agree because "
          "(g^2+g+2)/2 = C(g,0)+C(g,1)+C(g,2)",
          all((g * g + g + 2) // 2 == 1 + g + comb(g, 2) for g in range(0, 12)))

    # --- 5 counterexample search: perturb the constant ---------------------
    step(5, "counterexample search -- nearby admissible rules select OTHER g")
    landscape_c = {c: solutions_const(c) for c in range(-2, 9)}
    note("2^g = g^2+g+c :  " + ", ".join(f"c={c}->{landscape_c[c]}" for c in sorted(landscape_c)))
    check("the constant is load-bearing: c=2 gives {5}, but neighbours give other/empty "
          "solution sets (g=5 is NOT robust to the constant)",
          landscape_c[2] == [5] and landscape_c[1] != [5] and landscape_c[3] != [5])

    # --- 6 limiting / degenerate cases: truncation degree ------------------
    step(6, "the truncation DEGREE sets g = 2*degree+1 (the real choice)")
    trunc = {K: solutions_trunc(K) for K in range(0, 5)}
    note("2^(g-1)=sum_{k<=K} C(g,k):  " + ", ".join(f"K={K}->{trunc[K]}" for K in sorted(trunc)))
    check("degree drives the rank: K=0->g=1, K=1->g=3, K=2->g=5, K=3->g=7  (g = 2K+1) "
          "=> choosing K=2 to land on g=5 is the physical input, not the arithmetic",
          trunc[0] == [1] and trunc[1] == [3] and trunc[2] == [5] and trunc[3] == [7])

    # --- 7 alternative structures: does anything ELSE force g=5? ------------
    step(7, "alternative (corroborating) structures that independently give g=5")
    check("D5 half-spinor route: dim S+ = 2^(g-1) = 16 <=> g=5 (Spin(10) spinor), "
          "an INDEPENDENT selection of 5 (over-determination, README 'forced 3 ways')",
          dim_Splus == 16 and 2**(g_car - 1) == 16)
    check("family-closure route: N_fam = (2^(g-1)-1)/g integer & g+N_fam=8 also pin g=5",
          N_fam == 3 and g_car + N_fam == 8)
    note("so g=5 is robust ACROSS independent rules, but each rule is itself a physical\n"
         "postulate (half-spinor exhaustion / degree-2 truncation), not a theorem.")

    # --- 8 verdict ----------------------------------------------------------
    fails = summary("rt_B Pascal carrier rank")
    verdict(
        REPORT, target_id="B",
        claim="the carrier rank g=5 is forced by the Pascal condition",
        assumptions="even-exterior generation + truncation at degree 2 + count = 2^(g-1)",
        works="arithmetic uniqueness g=5 is Lean-verified [F]; g=5 is over-determined "
              "(Pascal, D5 half-spinor 16, family closure all give 5)",
        fails="the SELECTION rule is not derived: degree K sets g=2K+1, so K=2 (=>5) is a "
              "physical choice; perturbing the constant breaks g=5",
        status=SURVIVES_NARROWED,
        verdict_text="Theorem A's arithmetic core stands; the Pascal SELECTION must be "
                     "typed as an explicit physical postulate [A]/[P], not [I].",
        residual="a boundary/seam derivation of half-spinor exhaustion (why degree-2 "
                 "truncation / why count = 2^(g-1)).",
    )
    return fails


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
